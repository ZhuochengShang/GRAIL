"""RDPro runtime adapter around the unchanged, validated feedback recovery engine."""
import json
import os
from pathlib import Path
import sys
import time

from aideal.config import load_config
from experiments.external.main_plan.worker import cohort, execute_one, publish, TERMINAL
from experiments.external.post_b2.admission import slot
from experiments.external.recovery.engine import digest
from experiments.external.recovery.runner import run
from experiments.external.recovery.snapshot import freeze
from experiments.external.recovery.validation import file_sha


def feedback(root, out, upstream):
    baseline = root / 'docs/main_v5/A2.json'
    result = json.loads(baseline.read_text())
    names = cohort(result)
    base = load_config(root / 'configs/aideal.main_v5.yaml')
    private = freeze(base, result, root.parents[2] / 'AIDEAL_rdpro_v5_feedback')
    cfg = load_config(private / 'configs/aideal.main_v5.yaml')
    expected = result['run']['fingerprint_components']['interpreter']
    if (sys.executable != expected['executable'] or sys.version != expected['version']
            or os.environ['AIDEAL_ENV_FINGERPRINT'] != expected['environment_sha256']):
        raise ValueError('RDPro recovery interpreter/inventory differs from A2')
    build = json.loads((root / 'docs/main_v5/build_identity.json').read_text())
    for relative, sha in build['artifacts'].items():
        if file_sha(root / relative) != sha or file_sha(private / relative) != sha:
            raise ValueError('RDPro copied runtime differs from the validated build')
    identity = {'baseline_sha256': file_sha(baseline), 'worker_sha256': file_sha(Path(__file__)),
                'protocol_sha256': file_sha(Path(os.environ['AIDEAL_RECOVERY_PROTOCOL']))}
    path = out / 'summary.json'
    state = json.loads(path.read_text()) if path.exists() else {
        'stage': 'B2-1', 'mode': 'feedback', 'identity': identity,
        'baseline_result': str(baseline), 'cohort_count': len(names),
        'baseline_manifest_count': len(result['metrics']), 'source_diagnosis_calls': 0,
        'apis': {n: {'status': 'pending'} for n in names},
        'limitations': ['Native acceptance requires independent semantic review.']}
    if state['identity'] != identity:
        raise ValueError('Changed RDPro inputs; register a new namespace')
    manifest = 'docs/main_v5/api_manifest.json'
    for name in names:
        if state['apis'][name]['status'] != 'pending':
            continue
        try:
            proof = run(cfg, base, result, name, 'feedback', manifest, execute=False)
            state['apis'][name] = {'status': 'ready', 'preflight': proof['identity']}
        except ValueError as exc:
            state['apis'][name] = {'status': 'evidence_blocked', 'error': str(exc)}
    publish(out, state)
    while not state['complete']:
        for name, row in list(state['apis'].items()):
            if row['status'] in TERMINAL or row.get('retry_after', 0) > time.time():
                continue
            with slot(upstream, 'RDPro B2-1 ' + name) as admitted:
                if not admitted:
                    break
                if file_sha(baseline) != identity['baseline_sha256']:
                    raise ValueError('Frozen A2 changed')
                execute_one(base, cfg, result, dict(os.environ), state, out, manifest, name)
        if not state['complete']:
            time.sleep(30)
    return state
