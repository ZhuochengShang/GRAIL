"""Small adapters for the isolated MDAnalysis v4 study; no legacy job mutation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from aideal.config import load_config
from experiments.external.recovery.batch import batch


def verify_inputs(root):
    cfg = load_config(root / 'configs/aideal.full1032.A2.yaml')
    from aideal.doc_checks import _execute_sample_data
    from aideal.readme_agent import public_api_surface
    manifest = json.loads((root / 'docs/full_1032/api_manifest.json').read_text())
    assert sorted(public_api_surface(cfg, override_filter='all')) == manifest['apis']
    assert len(manifest['apis']) == 1032
    inputs = json.loads((root / 'docs/input_manifest.json').read_text())
    fixture_root = root / 'mdanalysis/testsuite/MDAnalysisTests/data'
    for name, expected in inputs['fixtures'].items():
        assert hashlib.sha256((fixture_root / name).read_bytes()).hexdigest() == expected['sha256']
    from aideal.doc_checks import _sha256_files
    assert _sha256_files(cfg.original_readme_files, cfg.root)['sha256'] == inputs['documentation_sha256']
    _, _, warnings = _execute_sample_data(cfg, cfg.comprehension['execute'])
    assert not warnings, warnings
    source = root / 'mdanalysis'
    commit = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    assert commit == '81b8ef51e5bc1aa2824294ac6c52818c74975658'
    script = ('import json,sys,importlib.metadata as meta,MDAnalysis as m; '
              'from pathlib import Path; '
              f'd=Path({str(source / "testsuite/MDAnalysisTests/data")!r}); '
              'u=m.Universe(str(d/"adk.psf"),str(d/"adk_dims.dcd")); '
              'assert len(u.atoms)>0 and len(u.trajectory)>1; '
              'print(json.dumps({"module":m.__file__,"version":m.__version__, '
              '"atoms":len(u.atoms),"frames":len(u.trajectory),"python":sys.version, '
              '"packages":sorted(set((d.metadata["Name"],d.version) for d in meta.distributions()))}))')
    env = dict(os.environ, PYTHONPATH=str(source / 'package'), MPLBACKEND='Agg')
    row = json.loads(subprocess.check_output([str(source / '.venv/bin/python'), '-c', script],
                                            env=env, text=True, timeout=60))
    assert str(source / 'package') in row['module'], row
    return row


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['preflight', 'copy-doc', 'source', 'archive'])
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--baseline-root', type=Path)
    p.add_argument('--baseline-cell', choices=['A2', 'B2'], default='A2')
    p.add_argument('--upstream-result', type=Path)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.action == 'archive':
        worktree = args.root.parents[1]
        subprocess.run(['git', 'add', '--', 'experiments/mdanalysis'], cwd=worktree, check=True)
        changed = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=worktree).returncode
        if changed:
            subprocess.run(['git', 'commit', '-m', 'Preserve MDAnalysis v4 stage evidence'], cwd=worktree, check=True)
        subprocess.run(['git', 'push', '-u', 'origin', 'HEAD'], cwd=worktree, check=True)
    elif args.action == 'preflight':
        parent = args.root.parents[2]
        gates = parent / 'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation/pipeline_v2'
        for repo in ('mir_eval', 'thumbnailator', 'tslearn'):
            jobs = json.loads((gates / repo / 'b2_watchdog.state.json').read_text())['jobs']
            if not jobs or any(j['status'] != 'succeeded' for j in jobs.values()):
                raise ValueError('Two MDAnalysis slots require all priority B2 native jobs to be finished')
        # Adopt the already running local upstream check; never start a duplicate.
        while not args.upstream_result.exists():
            print('Waiting for existing upstream baseline result', flush=True)
            time.sleep(30)
        baseline = json.loads(args.upstream_result.read_text())
        if baseline.get('passed') is not True:
            raise ValueError(f'upstream preflight failed: {baseline.get("counts")}; inspect saved log')
        record = verify_inputs(args.root)
        inventory = json.loads((args.out.parent / 'environment_v4.json').read_text())
        assert {k: record[k] for k in inventory} == inventory, 'runtime changed after registration'
        record['upstream_result'] = str(args.upstream_result)
        record['upstream_sha256'] = hashlib.sha256(args.upstream_result.read_bytes()).hexdigest()
        (args.out / 'preflight.json').write_text(json.dumps(record, indent=2)+'\n')
    elif args.action == 'copy-doc':
        source = args.baseline_root / 'docs/full_1032/A2/LLM_readme.md'
        target = args.root / 'docs/full_1032/B2/LLM_readme.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError('B2 README already differs; refuse to overwrite a repair')
        if not target.exists():
            shutil.copy2(source, target)
    else:
        cell = args.baseline_cell
        state = batch(args.root / f'configs/aideal.full1032.{cell}.yaml',
            args.root / f'docs/full_1032/{cell}/comprehension.json', 'mdanalysis',
            args.out / 'private', args.out, execute=True,
            manifest='docs/full_1032/api_manifest.json', baseline_cell=cell)
        pending = set(state['statuses']) - {'recovered_native', 'stuck', 'exhausted', 'infra_blocked'}
        if pending:
            raise SystemExit(75)


if __name__ == '__main__':
    main()
