"""Provision separate MDAnalysis cells and a dependency-aware, resumable plan."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

import yaml


def prepare(parent, core, out):
    freeze = parent / 'GRAIL_mdanalysis_full1032_freeze'
    seed = freeze / 'experiments/mdanalysis'
    revision = subprocess.check_output(['git', '-C', str(core), 'rev-parse', 'HEAD'], text=True).strip()
    out.mkdir(parents=True, exist_ok=True)
    plan_path = out / 'study_watchdog.yaml'
    if plan_path.exists():
        raise ValueError('Plan already exists; resume its supervisor, do not reprovision')
    cells = {}
    runtimes = {}
    # Source/runtime files are physical copies. No hardlinks or shared fixture writes.
    for cell in ('A1', 'A2', 'B2'):
        wt = parent / f'GRAIL_mdanalysis_full1032_v4_{cell}'
        if wt.exists():
            raise ValueError(f'Inspect existing destination before reuse: {wt}')
        branch = f'aideal/mdanalysis-full1032-v4-{cell}'
        subprocess.run(['git', '-C', str(core), 'worktree', 'add', '-b', branch, str(wt), revision], check=True)
        root = wt / 'experiments/mdanalysis'
        shutil.copytree(seed, root, dirs_exist_ok=True, symlinks=True,
            ignore=shutil.ignore_patterns('.aideal_exec', '__pycache__', '.pytest_cache',
                                         '.aideal_build_tools', 'PASS_TO_PASS_*', '*.log'))
        # There are no measured full1032 artifacts to migrate. Protect that assumption.
        if any((root / 'docs/full_1032').glob('*/comprehension.json')):
            raise ValueError('Unexpected existing full1032 results; inspect compatibility')
        for name in ('A1', 'A2', 'B2'):
            config = root / f'configs/aideal.full1032.{name}.yaml'
            raw = yaml.safe_load(config.read_text())
            raw['comprehension']['execute']['output_dir'] = f'.aideal_exec/full_1032/{name}/output'
            config.write_text(yaml.safe_dump(raw, sort_keys=False))
        profile = root / 'configs/project_profile.yaml'
        profile.write_text(profile.read_text().replace(
            'Use only the version-matched local MDAnalysisTests PSF/DCD fixture.',
            'Use the version-matched checked-in MDAnalysisTests fixtures listed in the harness. Match each API to the appropriate format; never invent paths.'))
        from experiments.mdanalysis.study_worker import verify_inputs
        runtimes[cell] = verify_inputs(root)
        cells[cell] = {'worktree': str(wt), 'root': str(root), 'branch': branch}
        subprocess.run(['git', '-C', str(wt), 'add', '--', 'experiments/mdanalysis'], check=True)
        subprocess.run(['git', '-C', str(wt), 'commit', '-m', f'Freeze isolated MDAnalysis v4 {cell} inputs'], check=True)
    env = {'AIDEAL_GOOGLE_MIN_INTERVAL_S': '3',
           'AIDEAL_GOOGLE_RATE_STATE': '/tmp/aideal_google_rate_gate.txt',
           'AIDEAL_GOOGLE_REQUEST_TIMEOUT_S': '300', 'AIDEAL_GOOGLE_MAX_RETRIES': '2'}
    inventory = out / 'environment_v4.json'
    canonical = {k: runtimes['A1'][k] for k in ('version', 'python', 'packages')}
    assert all({k: record[k] for k in canonical} == canonical for record in runtimes.values())
    inventory.write_text(json.dumps(canonical, indent=2)+'\n')
    (out / 'runtime_preparation.json').write_text(json.dumps(runtimes, indent=2)+'\n')
    upstream = seed / 'docs/full_1032/setup/PASS_TO_PASS_BEFORE.json'
    jobs = []

    def job(name, cell, command, deps, result, kind='exit_zero'):
        item = cells[cell]
        jobs.append({'id': name, 'cwd': item['worktree'], 'branch': item['branch'],
            'environment_inventory': str(inventory),
            'env': {'PYTHONPATH': f"{item['worktree']}/grail-agent/src:{item['worktree']}",
                    'AIDEAL_RECOVERY_ENV_INVENTORY': str(inventory),
                    'AIDEAL_RECOVERY_PROTOCOL': f"{item['root']}/protocol_v4.yaml"},
            'command': [sys.executable, *command], 'depends_on': deps,
            'result': str(result), 'complete': {'kind': kind},
            'max_runtime_seconds': 604800, 'max_restarts': 0})
        if kind != 'exit_zero':
            jobs[-1]['on_success'] = [[sys.executable, '-m', 'experiments.mdanalysis.study_worker',
                'archive', '--root', item['root'], '--out', str(out / cell)]]

    def cli(cell, command):
        return ['-m', 'aideal.cli', '--config',
                f'experiments/mdanalysis/configs/aideal.full1032.{cell}.yaml', *command]

    def evaluation(cell, deps):
        result = Path(cells[cell]['root']) / f'docs/full_1032/{cell}/comprehension.json'
        job(f'{cell}_zero', cell, cli(cell, ['comprehension', '--doc', 'original' if cell=='A1' else 'aideal',
            '--doc-scope', 'relevant', '--manifest', 'docs/full_1032/api_manifest.json', '--execute',
            '--show-code', '--max-fix-rounds', '0', '--resume', '--timeout', '300']),
            deps, result, 'json_metrics_no_transient')

    for cell in cells:
        job(f'preflight_{cell}', cell, ['-m', 'experiments.mdanalysis.study_worker', 'preflight',
            '--root', cells[cell]['root'], '--upstream-result', str(upstream),
            '--out', str(out / cell)], [], out / cell / 'preflight.stdout')
    job('generate_A2', 'A2', ['experiments/external/run_resumable_readme.py', '--config',
        'experiments/mdanalysis/configs/aideal.full1032.A2.yaml', '--limit', '0'],
        ['preflight_A2'], Path(cells['A2']['root']) / 'docs/full_1032/A2/generation_result.json', 'readme_generation')
    evaluation('A1', ['preflight_A1'])
    evaluation('A2', ['generate_A2'])
    job('initialize_B2', 'B2', ['-m', 'experiments.mdanalysis.study_worker', 'copy-doc',
        '--root', cells['B2']['root'], '--baseline-root', cells['A2']['root'], '--out', str(out / 'B2')],
        ['preflight_B2', 'A2_zero'], out / 'B2/initialize.stdout')
    job('repair_generated', 'B2', cli('B2', ['fix-docs', '--from-results',
        str(Path(cells['A2']['root']) / 'docs/full_1032/A2/comprehension.json'),
        '--doc', 'aideal', '--doc-scope', 'relevant', '--manifest', 'docs/full_1032/api_manifest.json',
        '--retry-rounds', '0', '--doc-rounds', '5', '--doc-stuck', '2', '--deep-dive-first',
        '--deep-dive-out', 'docs/full_1032/B2/deepdive', '--report', 'docs/full_1032/B2/docfix.json']),
        ['initialize_B2'], Path(cells['B2']['root']) / 'docs/full_1032/B2/docfix.json', 'docfix')
    evaluation('B2', ['repair_generated'])
    for cell in ('A2', 'B2'):
        job(f'S_{cell}', cell, ['-m', 'experiments.mdanalysis.study_worker', 'source',
            '--root', cells[cell]['root'], '--baseline-cell', cell, '--out', str(out / f'S_{cell}')],
            [f'{cell}_zero'], out / f'S_{cell}/source.stdout')
    plan = {'version': 2, 'max_parallel': 2, 'retry_delay_seconds': 300, 'env': env, 'jobs': jobs}
    plan_path.write_text(yaml.safe_dump(plan, sort_keys=False))
    (out / 'registration.json').write_text(json.dumps({'protocol': 'mdanalysis-separated-v4',
        'core_revision': revision, 'cells': cells, 'upstream_result': str(upstream),
        'plan': str(plan_path), 'B1': 'omitted', 'legacy_waiter': 'preserved, superseded prerequisite',
        'scope': '1032 frozen public names; 1397 definition sites; new v4 extension, not historical v3 replication'}, indent=2)+'\n')
    return plan_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', required=True, type=Path)
    parser.add_argument('--core', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    print(prepare(args.workspace_parent.resolve(), args.core.resolve(), args.out.resolve()))
