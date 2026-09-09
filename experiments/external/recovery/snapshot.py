"""Freeze A2 inputs and provision a private copy without rebuilding packages."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from aideal.config import load_config
from .engine import digest, save
from .validation import file_sha


def freeze(base, result, destination):
    """One published copy per immutable result; interrupted copies are preserved."""
    key = digest(result)
    destination = Path(destination) / key
    marker = destination / 'snapshot.json'
    if marker.exists():
        record = json.loads(marker.read_text())
        if record['baseline_result_sha256'] != key or record['base'] != str(base.root):
            raise ValueError('snapshot identity mismatch')
        return destination / 'project'
    if destination.exists():
        raise ValueError('unpublished snapshot exists; inspect before reuse')
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + '.partial-' + uuid.uuid4().hex[:8])
    # Physical files, no hardlinks. Python executable symlinks can point to the
    # existing interpreter; target-package imports are attested below.
    shutil.copytree(base.root, temporary / 'project', symlinks=True,
        ignore=shutil.ignore_patterns('.git', '.aideal_exec', '.aideal_recovery',
                                     '__pycache__', '.pytest_cache', 'logs'))
    save(temporary / 'baseline_result.json', result)
    save(temporary / 'snapshot.json', {'base': str(base.root),
        'baseline_result_sha256': key, 'effective_config_sha256': digest(base.raw),
        'policy': 'physical private copy; no baseline output state reused'})
    temporary.rename(destination)
    return destination / 'project'


def runtime_environment(base, cfg, result, repo):
    """Use existing packages; prove the target imports from the private copy."""
    expected = result['run']['fingerprint_components']['interpreter']
    if expected['executable'] != sys.executable or expected['version'] != sys.version:
        raise ValueError('runner interpreter differs from A2')
    inventory = Path(os.environ.get('AIDEAL_RECOVERY_ENV_INVENTORY',
                                    base.root / 'docs/eval/setup/environment_A2.txt'))
    if file_sha(inventory) != expected['environment_sha256']:
        raise ValueError('A2 environment inventory differs from baseline fingerprint')
    env = dict(os.environ, AIDEAL_ENV_FINGERPRINT=expected['environment_sha256'],
               PYTHONDONTWRITEBYTECODE='1')
    if repo == 'thumbnailator':
        ex = cfg.comprehension['execute']
        relative = Path(ex.get('build_cwd', 'source')) / ex['uberjar']
        if file_sha(base.root / relative) != file_sha(cfg.root / relative):
            raise ValueError('copied built dependency differs from baseline')
        return env, {'jar_sha256': file_sha(cfg.root / relative),
                     'assertion_policy': 'native unchanged; independent assertions-on replay required'}
    source_name = {'tslearn': 'tslearn', 'mdanalysis': 'mdanalysis'}.get(repo, 'source')
    module_name = 'MDAnalysis' if repo == 'mdanalysis' else repo
    probe = ('import importlib,importlib.metadata as m,json; '
             f'p=importlib.import_module({module_name!r}); '
             'print(json.dumps({"target":p.__file__,"packages":sorted('
             '(d.metadata["Name"],d.version) for d in m.distributions())}))')
    results = []
    for current in (base, cfg):
        source = current.root / source_name
        interpreter = (source / '.venv/bin/python') if repo in ('mir_eval', 'mdanalysis') else Path(sys.executable)
        import_root = source / 'package' if repo == 'mdanalysis' else source
        current_env = dict(env, PYTHONPATH=str(import_root), MPLBACKEND='Agg',
                           NUMBA_THREADING_LAYER='workqueue', OPENBLAS_NUM_THREADS='1',
                           OMP_NUM_THREADS='1', NUMBA_NUM_THREADS='1')
        output = subprocess.check_output([str(interpreter), '-c', probe],
            cwd=current.root, env=current_env, text=True, timeout=60)
        record = json.loads(output)
        if source.resolve() not in Path(record['target']).resolve().parents:
            raise ValueError(f'{repo} imports from another checkout: {record["target"]}')
        results.append(record)
    # Editable metadata may appear twice after a physical copy; require the
    # same name/version set and retain raw inventories to expose duplicates.
    if set(map(tuple, results[0]['packages'])) != set(map(tuple, results[1]['packages'])):
        raise ValueError('copied runtime package versions differ from A2 runtime')
    env['PYTHONPATH'] = str(cfg.root / source_name / 'package' if repo == 'mdanalysis' else cfg.root / source_name) + os.pathsep + env.get('PYTHONPATH', '')
    return env, {'baseline': results[0], 'isolated': results[1],
                 'limitation': 'package/import identity check, not API-specific semantic validation'}
