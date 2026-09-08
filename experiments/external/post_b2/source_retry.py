"""Resume the existing S_A2 checkpoint after B2 without waiting for A1."""
import os
from pathlib import Path

from aideal.config import load_config
from experiments.external.recovery.batch import batch, environment
from experiments.external.recovery.validation import file_sha
from .evidence import REPOSITORIES


def needed(info):
    return any(r.get('status') in ('provider_blocked', 'blocked') for r in info['source']['apis'].values())


def run(info, parent, upstream):
    repo = info['repo']
    prefix, relative, _ = REPOSITORIES[repo]
    root = Path(parent) / f'{prefix}_A2' / relative
    suffix = '_full235' if repo == 'tslearn' else ''
    config = root / f'configs/aideal_A2{suffix}.yaml'
    cfg = load_config(config)
    expected = info['A2']['run']['fingerprint_components']['interpreter']['environment_sha256']
    inventory = next((p for p in (cfg.root / 'docs/eval/setup').glob('environment_*.txt')
                      if file_sha(p) == expected), None)
    if inventory is None:
        raise ValueError('cannot bind S_A2 inventory; do not create a replacement environment')
    work = Path(info['source']['snapshot']).parents[1]
    with environment(dict(os.environ, AIDEAL_RECOVERY_ENV_INVENTORY=str(inventory))):
        # batch owns the original source/.lock and per-case runner locks.
        # An original driver waking after A1 cannot execute the same case twice.
        return batch(config, info['files']['A2'], repo, work,
                     Path(upstream) / repo / 'source', execute=True)
