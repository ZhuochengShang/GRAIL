"""Continue existing baselines, repair A2 only, and publish separate outcomes."""
from __future__ import annotations

import argparse
import fcntl
import importlib.util
import json
from pathlib import Path
import shutil
import threading
import time

import yaml

from experiments.external import run_external_2x2_pipeline as external
from experiments.external.run_condition_watchdog import Supervisor
from .batch import batch
from .engine import save
from .validation import file_sha
from . import reporting


def layout(repo, setup):
    if repo == 'tslearn':
        relative = Path('experiments/tslearn')
        prefix = 'GRAIL_tslearn_full235'
        plan = setup / relative / 'docs/eval/watchdogs/full235_baselines.yaml'
    else:
        relative = Path('experiments/external') / repo
        prefix = f'GRAIL_{repo}'
        plan = setup.parent / f'{repo}_baselines_watchdog.yaml'
    return relative, prefix, plan


def adapter(repo, setup):
    if repo != 'tslearn':
        return external
    path = setup / 'experiments/tslearn/run_full235_pipeline.py'
    spec = importlib.util.spec_from_file_location('tslearn_frozen_adapter', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def b2_jobs(repo, setup, worktrees, module, relative):
    """There is deliberately no original-document repair job in v2."""
    parent = worktrees['A2']
    start = module.git(parent, 'rev-parse', 'HEAD').stdout.strip()
    if repo == 'tslearn':
        wt = module.ensure_worktree(setup, 'B2', start)
        source = module.ensure_source(setup, wt)
        inventory = wt / relative / 'docs/eval/setup/environment_B2.txt'
        if not inventory.exists():
            inventory = module.environment_inventory(wt, 'B2', source)
        before = wt / relative / 'docs/eval/B2/PASS_TO_PASS_BEFORE.md'
        if not before.exists():
            module.upstream_tests(wt, 'B2', 'before', source)
        jobs = [module.repair_job(wt, 'B2', inventory),
                module.validation_job(wt, 'B2', inventory, ['tslearn_B2_repair']),
                module.comprehension_job(wt, 'B2', inventory, ['tslearn_B2_validate_readme'])]
    else:
        branch = f'aideal/{repo}-B2'
        wt = module.ensure_worktree(setup, branch, setup.parent / f'GRAIL_{repo}_B2', start)
        inventory = wt / relative / 'docs/eval/setup/environment_B2.txt'
        if not inventory.exists():
            inventory = module.ensure_source(setup, wt, repo, module.REPOS[repo], 'B2')
        repair = module.make_job(repo, wt, branch, 'B2', inventory, repair=True)
        fresh = module.make_job(repo, wt, branch, 'B2', inventory)
        fresh['depends_on'] = [repair['id']]
        jobs = [repair, fresh]
    baseline_result = parent / relative / 'docs/eval/A2/comprehension.json'
    inherited_result = wt / relative / 'docs/eval/A2/comprehension.json'
    if not inherited_result.exists():
        inherited_result.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(baseline_result, inherited_result)
    if file_sha(inherited_result) != file_sha(baseline_result):
        raise ValueError('B2 worktree contains a different A2 baseline result')
    target = wt / relative / 'docs/eval/B2/LLM_readme.md'
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(parent / relative / 'docs/eval/A2/LLM_readme.md', target)
    worktrees['B2'] = wt
    return jobs


def completed_cell(repo, cell, worktree, module, relative):
    if repo == 'tslearn':
        module.analyze(worktree, cell)
        after = worktree / relative / f'docs/eval/{cell}/PASS_TO_PASS_AFTER.md'
        if not after.exists():
            module.upstream_tests(worktree, cell, 'after', module.ensure_source(worktree, worktree))
        branch = module.BRANCHES[cell]
    else:
        module.analyze(worktree, repo, cell)
        if cell == 'B2':
            module.upstream_after(worktree, repo, module.REPOS[repo], cell)
        branch = f'aideal/{repo}-{cell}'
    paths = [relative / f'docs/eval/{cell}', relative / f'docs/eval/setup/environment_{cell}.txt',
             relative / ('logs/eval/' + cell if repo == 'tslearn' else 'logs/' + cell)]
    module.commit_push(worktree, branch, f'Complete {repo} {cell} under A2-only repair protocol',
                       [str(path) for path in paths])


def report(repo, worktrees, relative, out):
    cells = {}
    results = {}
    for cell in ('A1', 'A2', 'B2'):
        path = worktrees[cell] / relative / f'docs/eval/{cell}/comprehension.json'
        result = json.loads(path.read_text())
        results[cell] = result
        cells[cell] = {'result': str(path), 'apis': len(result['metrics']),
            'native_pass': sum(m['status'] == 'pass' for m in result['metrics'].values()),
            'fingerprint': result['run']['experiment_fingerprint']}
    if len({r['run']['manifest_sha256'] for r in results.values()}) != 1:
        raise ValueError('ordered API manifest differs between native comparisons')
    if any(set(r['metrics']) != set(results['A2']['metrics']) for r in results.values()):
        raise ValueError('native API identity sets differ')
    source = json.loads((out / 'source/summary.json').read_text())
    cohort = list(source.get('apis', {}))
    n = cells['A2']['apis']
    save(out / 'native_comparison.json', {'protocol': 'aideal-a2-repair-v2', 'repo': repo,
        'cells': cells, 'B1': 'omitted by user; no original-README repair',
        'recovery': str(out / 'source/summary.json'),
        'doc_rounds': str(worktrees['B2'] / relative / 'docs/eval/B2/docfix.json'),
        'generation_effect_raw_pp': 100 * (cells['A2']['native_pass'] - cells['A1']['native_pass']) / n,
        'documentation_transfer_raw_pp': 100 * (cells['B2']['native_pass'] - cells['A2']['native_pass']) / n,
        'source_eligible_A2_failures': len(cohort),
        'B2_native_pass_on_same_failure_cohort': sum(results['B2']['metrics'][name]['status'] == 'pass' for name in cohort),
        'A2_pass_to_B2_fail': [name for name, row in results['A2']['metrics'].items()
            if row['status'] == 'pass' and results['B2']['metrics'][name]['status'] != 'pass'],
        'interpretation': 'A2-A1 generation; B2-A2 fresh-reader documentation transfer; source recovery is a separate endpoint'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', choices=['mir_eval', 'thumbnailator', 'tslearn'])
    parser.add_argument('--freeze-worktree', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--preflight', action='store_true')
    args = parser.parse_args()
    repo, setup = args.repo, args.freeze_worktree.resolve()
    relative, prefix, baselines = layout(repo, setup)
    worktrees = {cell: setup.parent / f'{prefix}_{cell}' for cell in ('A1', 'A2')}
    if not baselines.is_file() or any(not p.is_dir() for p in worktrees.values()):
        raise ValueError('v2 continuation requires existing baseline plan and worktrees')
    module = adapter(repo, setup)
    expected = module.FREEZE_BRANCH if repo == 'tslearn' else module.REPOS[repo]['freeze_branch']
    if module.git(setup, 'branch', '--show-current').stdout.strip() != expected:
        raise ValueError('unexpected freeze branch')
    if args.preflight:
        print(json.dumps({'baseline_plan': str(baselines), 'original_repair': False,
            'stages': ['reuse/adopt A1+A2', 'A2 source-only recovery', 'A2 README repair', 'fresh B2', 'report']}))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'driver.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        reporter_stop, reporter_thread = reporting.start(repo, setup, prefix, relative, args.out)
        # Caller first retires only legacy controllers. This adopts surviving API
        # workers; it never provisions or rewrites their environments/configs.
        supervisor = Supervisor(baselines)
        baseline_outcome = {}
        def supervise_baselines():
            try:
                baseline_outcome['returncode'] = supervisor.run()
            except Exception as exc:
                baseline_outcome['error'] = str(exc)
        baseline_thread = threading.Thread(target=supervise_baselines, daemon=True)
        baseline_thread.start()
        while supervisor.state['jobs'][f'{repo}_A2_zero']['status'] != 'succeeded':
            if not baseline_thread.is_alive():
                raise RuntimeError(f'A2 continuation incomplete: {baseline_outcome}')
            time.sleep(1)
        # A1 is a parallel control, never a dependency of A2 repair.
        completed_cell(repo, 'A2', worktrees['A2'], module, relative)
        project = worktrees['A2'] / relative
        suffix = '_full235' if repo == 'tslearn' else ''
        # Independent branch from frozen A2, not from repaired docs or B2 errors.
        plan = args.out / 'b2_watchdog.yaml'
        if plan.exists():
            # B2 may still have a surviving worker after a controller crash.
            # Adopt it before permitting any additional source-recovery calls.
            state = json.loads((args.out / 'source/summary.json').read_text())
        else:
            try:
                state = batch(project / f'configs/aideal_A2{suffix}.yaml',
                    project / 'docs/eval/A2/comprehension.json', repo, args.work,
                    args.out / 'source', execute=True)
            except Exception as exc:
                state = {'apis': {}, 'statuses': {'preflight_blocked': 1},
                         'error': f'{type(exc).__name__}: {exc}'}
                (args.out / 'source').mkdir(exist_ok=True)
                save(args.out / 'source/summary.json', state)
        jobs = b2_jobs(repo, setup, worktrees, module, relative)
        contents = yaml.safe_dump({'version': 2, 'max_parallel': 1,
            'retry_delay_seconds': 300, 'jobs': jobs}, sort_keys=False)
        if plan.exists() and plan.read_text() != contents:
            raise ValueError('B2 plan changed; preserve previous state and investigate')
        if not plan.exists():
            plan.write_text(contents)
        if Supervisor(plan).run() != 0:
            raise RuntimeError('B2 documentation pipeline incomplete')
        completed_cell(repo, 'B2', worktrees['B2'], module, relative)
        while baseline_thread.is_alive():
            baseline_thread.join(timeout=2)
        if baseline_outcome.get('returncode') != 0:
            raise RuntimeError(f'A1 control incomplete: {baseline_outcome}')
        completed_cell(repo, 'A1', worktrees['A1'], module, relative)
        report(repo, worktrees, relative, args.out)
        # Retry source provider events after the README/fresh-reader pipeline.
        # Preflight blockers remain explicit and resumable instead of blocking B2.
        while any(row['status'] in ('provider_blocked', 'blocked') for row in state['apis'].values()):
            time.sleep(30)
            state = batch(project / f'configs/aideal_A2{suffix}.yaml',
                project / 'docs/eval/A2/comprehension.json', repo, args.work,
                args.out / 'source', execute=True)
        save(args.out / 'completion.json', {'status': ('partial_validation_blocked'
            if state['statuses'].get('preflight_blocked') else 'native_complete_needs_semantic_review'),
            'source_statuses': state['statuses'], 'native_comparison': str(args.out / 'native_comparison.json')})
        reporter_stop.set()
        reporter_thread.join(timeout=5)
        reporting.publish(repo, setup.parent, prefix, relative, args.out)


if __name__ == '__main__':
    main()
