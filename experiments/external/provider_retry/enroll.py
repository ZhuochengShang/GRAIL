"""Enroll future Python CLI workers without signalling current jobs.

Usage: python -m experiments.external.provider_retry.enroll WORKTREE CONFIG OUTPUT
The bootstrap is scoped to the exact config and resumed zero-fix comprehension.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

from .transport import atomic, sha


BOOTSTRAP = '''# AIDEAL explicit transport-v2 bootstrap; enrolled config only.
from pathlib import Path as _Path
import hashlib as _hashlib
import json as _json
import sys as _sys
_base = _Path(__file__).resolve().parent
_policy_path = _base / "aideal_transport_policy.json"
if _policy_path.exists():
    _policy = _json.loads(_policy_path.read_text())
    if ("comprehension" in _sys.argv and "--resume" in _sys.argv
            and "--config" in _sys.argv
            and str(_Path(_sys.argv[_sys.argv.index("--config")+1]).resolve()) == _policy["config"]):
        try:
            _module = _base / "_aideal_transport_retry.py"
            if _hashlib.sha256(_module.read_bytes()).hexdigest() != _policy["adapter_sha256"]:
                raise RuntimeError("Transport adapter hash mismatch")
            if _hashlib.sha256((_base / "_aideal_input_contract.py").read_bytes()).hexdigest() != _policy["input_contract_sha256"]:
                raise RuntimeError("Input contract hash mismatch")
            from _aideal_transport_retry import install as _install
            _install(_policy_path)
        except Exception as _exc:
            _sys.stderr.write("AIDEAL transport bootstrap failed: " + type(_exc).__name__ + "\\n")
            raise SystemExit(78)
'''


def enroll(worktree, config, output, harness_setup=None):
    worktree, config, output = worktree.resolve(), config.resolve(), output.resolve()
    if not config.is_file() or not config.is_relative_to(worktree):
        raise ValueError('Config must exist inside enrolled worktree')
    source = worktree / 'grail-agent/src'
    if not (source / 'aideal/llm.py').is_file():
        raise ValueError('Expected existing AIDEAL engine')
    payload = Path(__file__).with_name('transport.py').read_bytes()
    contract = Path(__file__).with_name('input_contract.py').read_bytes()
    policy = {'enabled':True,'version':'aideal-provider-transport-v2','config':str(config),
              'output':str(output),'request_timeout_s':600,'sdk_attempts':1,
              'cooldown_base_s':300,'cooldown_max_s':1800,'adapter_sha256':sha(payload),
              'input_contract_sha256':sha(contract),'harness_setup':harness_setup,
              'sdk_versions':{n:importlib.metadata.version(n) for n in ['google-genai','langchain-google-genai']},
              'native_fingerprint_note':'Transport policy is a separate amendment; group new retries by this policy hash. Historical native engine hashes and checkpoints are unchanged.'}
    files={source/'_aideal_transport_retry.py':payload,
           source/'_aideal_input_contract.py':contract,
           source/'aideal_transport_policy.json':(json.dumps(policy,indent=2)+'\n').encode(),
           source/'sitecustomize.py':BOOTSTRAP.encode()}
    for path,raw in files.items():
        if path.exists() and path.read_bytes()!=raw:
            raise ValueError(f'Refusing to overwrite existing file: {path}')
    # Bootstrap last: a new worker sees either no hook or a complete installation.
    for path,raw in files.items():
        tmp=path.with_name(path.name+'.install.tmp');tmp.write_bytes(raw);tmp.replace(path)
    return {'worktree':str(worktree),'config':str(config),'policy_sha256':sha(policy),
            'files':{str(p.relative_to(worktree)):sha(raw) for p,raw in files.items()},
            'activation':'Next naturally launched matching CLI worker; current processes unchanged'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('worktree',type=Path)
    parser.add_argument('config',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    print(json.dumps(enroll(args.worktree,args.config,args.output),indent=2))


if __name__=='__main__':
    main()
