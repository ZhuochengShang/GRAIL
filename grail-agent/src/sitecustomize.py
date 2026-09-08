# AIDEAL explicit transport-v2 bootstrap; enrolled config only.
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
            _sys.stderr.write("AIDEAL transport bootstrap failed: " + type(_exc).__name__ + "\n")
            raise SystemExit(78)
