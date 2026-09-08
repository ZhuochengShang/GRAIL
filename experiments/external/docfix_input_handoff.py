"""Prepare frozen A2 error context and CLI path aliases before B2 repair starts."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time

from aideal.config import load_config
from experiments.external.post_b2.evidence import REPOSITORIES, complete
from experiments.external.recovery.engine import save
from experiments.external.recovery.validation import file_sha


def seed_rows(result, cfg):
    rows, bindings = [], {}
    ex = cfg.comprehension['execute']
    for name, metric in result['metrics'].items():
        if metric['status'] == 'pass':
            continue
        detail = result.get('details', {}).get(name)
        detail = detail if isinstance(detail, dict) else {}
        code, binding = detail.get('code', ''), 'native_detail_prefix'
        script = cfg.root / ex['work_dir'] / f'run_{name}' / ex['test_filename']
        if not code:
            if sum(n.casefold() == name.casefold() for n in result['metrics']) > 1:
                binding = 'unavailable_case_collision'
            elif script.is_file():
                code, binding = script.read_text(), 'retained_unbound_legacy'
                region = ex.get('region', [])
                if len(region) == 2 and region[0] in code and region[1] in code:
                    code = code.split(region[0], 1)[1].split(region[1], 1)[0].strip()
            else:
                binding = 'unavailable'
        rows.append({'run_id': result['run'].get('run_id', ''), 'step': 'frozen-A2-docfix-input',
                     'task': 'independent README repair from A2', 'language': cfg.language,
                     'status': 'fail', 'function': name, 'error_category': metric.get('error_category', 'unknown'),
                     'error': metric.get('error') or detail.get('error', ''),
                     'code': code or '(baseline snippet unavailable; do not infer its contents)', 'round': 0})
        bindings[name] = {'code_binding': binding, 'retained_script_sha256': file_sha(script) if script.is_file() else None}
    return rows, bindings


def prepare(repo, parent):
    prefix, relative, count = REPOSITORIES[repo]
    a2 = Path(parent) / f'{prefix}_A2' / relative
    wt = Path(parent) / f'{prefix}_B2'
    root = wt / relative
    if not (wt / '.git').is_file():
        raise ValueError('waiting for the existing controller to create its B2 worktree')
    original = a2 / 'docs/eval/A2/comprehension.json'
    inherited = root / 'docs/eval/A2/comprehension.json'
    result = json.loads(original.read_text())
    complete(result, count)
    if file_sha(original) != file_sha(inherited):
        raise ValueError('B2 must inherit the exact completed A2 result before admission')
    suffix = '_full235' if repo == 'tslearn' else ''
    base = load_config(a2 / f'configs/aideal_A2{suffix}.yaml')
    cfg = load_config(root / f'configs/aideal_B2{suffix}.yaml')
    alias = wt / 'docs/eval'
    proof_path = root / 'docs/eval/B2/A2_INPUT_HANDOFF.json'
    target = root / 'docs/eval'
    if alias.is_symlink() or alias.exists():
        if not alias.is_symlink() or alias.resolve() != target.resolve() or not proof_path.exists():
            raise ValueError('existing CLI path was not released by this handoff; inspect before writing')
        proof = json.loads(proof_path.read_text())
        prefix_bytes = cfg.error_log.read_bytes()[:proof['seed_bytes']]
        import hashlib
        if proof['A2_sha256'] != file_sha(original) or hashlib.sha256(prefix_bytes).hexdigest() != proof['seed_sha256']:
            raise ValueError('A2 handoff identity or seeded error-log prefix changed')
        return proof
    if (root / 'docs/eval/B2/docfix.json').exists():
        raise ValueError('document work already exists without the verified handoff')
    rows, bindings = seed_rows(result, base)
    # Map only the private project path; preserve the baseline error/code in
    # the A2 artifact and record the mapping, never import S_A2 recovery work.
    raw = ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows)
    raw = raw.replace(str(base.root), str(cfg.root))
    seed = raw.encode()
    if cfg.error_log.exists() and cfg.error_log.read_bytes() != seed:
        raise ValueError('B2 error log already has other evidence; refusing to overwrite')
    cfg.error_log.parent.mkdir(parents=True, exist_ok=True)
    if not cfg.error_log.exists():
        tmp = cfg.error_log.with_suffix('.seed.tmp')
        tmp.write_bytes(seed)
        tmp.replace(cfg.error_log)
    proof = {'repo': repo, 'A2_sha256': file_sha(original), 'A2_fingerprint': result['run']['experiment_fingerprint'],
             'seed_sha256': file_sha(cfg.error_log), 'seed_bytes': len(seed), 'seeded_failures': len(rows),
             'apis': bindings, 'error_log': str(cfg.error_log), 'read_alias': str(alias),
             'alias_target': str(target), 'path_mapping': [str(base.root), str(cfg.root)],
             'source_recovery_evidence_used': False, 'provider_calls': 0,
             'limitation': 'Legacy saved snippets can be unbound; prefix/missing associations remain explicit.'}
    proof_path.parent.mkdir(parents=True, exist_ok=True)
    save(proof_path, proof)
    # Releasing the CLI alias LAST lets the unchanged watchdog retry only
    # after both seed evidence and its proof exist. No worker is restarted.
    alias.parent.mkdir(parents=True, exist_ok=True)
    alias.symlink_to(os.path.relpath(target, alias.parent), target_is_directory=True)
    return proof


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'handoff.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            results = {}
            for repo in REPOSITORIES:
                try:
                    proof = prepare(repo, args.workspace_parent)
                    commit_handoff(repo, args.workspace_parent)
                    results[repo] = {'status': 'prepared', 'proof': proof}
                except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
                    results[repo] = {'status': 'waiting_or_blocked', 'reason': f'{type(exc).__name__}: {exc}'}
            save(args.out / 'status.json', {'updated_epoch': time.time(), 'repos': results, 'provider_calls': 0})
            if not args.watch or all(row['status'] == 'prepared' for row in results.values()):
                print(json.dumps(results, indent=2))
                return
            time.sleep(10)


def commit_handoff(repo, parent):
    prefix, relative, _ = REPOSITORIES[repo]
    wt = Path(parent) / f'{prefix}_B2'
    expected = 'aideal/tslearn-full235-B2' if repo == 'tslearn' else f'aideal/{repo}-B2'
    def git(*args, check=True):
        return subprocess.run(['git', *args], cwd=wt, text=True, capture_output=True, check=check)
    if git('branch', '--show-current').stdout.strip() != expected:
        raise ValueError('unexpected B2 branch; refusing to commit handoff')
    paths = ['docs/eval', f'{relative}/docs/eval/B2/A2_INPUT_HANDOFF.json']
    git('add', '--', *paths)
    if git('diff', '--cached', '--quiet', '--', *paths, check=False).returncode:
        git('commit', '--only', '-m', 'Bind frozen A2 errors and repair CLI paths before B2', '--', *paths)


if __name__ == '__main__':
    main()
