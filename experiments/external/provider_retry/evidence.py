"""Read fresh or migrated progress without confusing absent finals with no work."""
import json
from pathlib import Path
import time

from experiments.external.assertion_replay.evidence import collect as legacy_collect, digest


def lines(path):
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)
            if line.endswith(b'\n')]


def manifest(project):
    path = project / 'docs/eval/api_manifest.json'
    if not path.exists():
        return []
    value = json.loads(path.read_text())
    names = value.get('apis', []) if isinstance(value, dict) else value
    if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
        raise ValueError('Report requires a name-based manifest')
    if len(names) != len(set(names)):
        raise ValueError('Duplicate manifest identities')
    return names


def collect(project, cell):
    project = Path(project)
    names = manifest(project)
    checkpoint = project / f'.aideal_exec/{cell}/comprehension_progress.jsonl'
    identity = checkpoint.with_name('run_identity.json')
    record = json.loads(identity.read_text()) if identity.exists() else None
    if record and digest(record['fingerprint_components']) != record['experiment_fingerprint']:
        raise ValueError('Active run identity is corrupt')
    final = project / f'docs/eval/{cell}/comprehension.json'
    final_matches = (not record or (final.exists() and json.loads(final.read_text())
                     ['run']['experiment_fingerprint'] == record['experiment_fingerprint']))
    evidence = legacy_collect(project, cell) if final_matches else None
    if evidence is not None and (not record or final.exists()):
        if names and not set(evidence['rows']).issubset(names):
            raise ValueError('Result contains names outside the frozen manifest')
        evidence['expected'] = len(names) or len(evidence['rows'])
        evidence['complete'] = evidence['complete'] and len(evidence['rows']) == evidence['expected']
        evidence['identity_status'] = 'Final or explicitly migrated evidence'
        return evidence
    raw = checkpoint.read_bytes() if checkpoint.exists() else b''
    journal = [json.loads(line) for line in raw.splitlines(keepends=True) if line.endswith(b'\n')]
    if not journal:
        return None
    if record:
        components = record['fingerprint_components']
        selected = digest(components)
        status = 'Bound to published active-run identity'
    else:
        # Old workers have no active identity sidecar. Never merge their groups
        # or certify a final result merely by picking the most recent group.
        selected = journal[-1]['experiment_fingerprint']
        components = {}
        status = 'Provisional last-observed fingerprint group; final identity unverified'
    rows = {r['name']: r for r in journal if r['experiment_fingerprint'] == selected}
    if names and not set(rows).issubset(names):
        raise ValueError('Checkpoint contains names outside the frozen manifest')
    return {'cell': cell, 'project': str(project), 'complete': False, 'rows': rows,
            'expected': len(names) or len(rows), 'identity_status': status,
            'components': components, 'source_path': str(checkpoint),
            'source_sha256': digest(raw)}


def worker_state(parent, repo, cell):
    audit = parent / 'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation'
    if cell == 'B2':
        path = audit / 'pipeline_v2' / repo.lower() / 'b2_watchdog.state.json'
    elif repo == 'tslearn':
        path = parent / 'GRAIL_tslearn_full235_freeze/experiments/tslearn/docs/eval/watchdogs/full235_baselines.state.json'
    else:
        path = parent / f'{repo.lower()}_baselines_watchdog.state.json'
    if not path.is_file():
        return 'No supervisor evidence'
    state = json.loads(path.read_text())
    row = state.get('jobs', {}).get(f'{repo.lower()}_{cell}_zero', {})
    if row.get('status') == 'running':
        fresh = time.time() - state.get('heartbeat_epoch', 0) < 180
        return 'Supervisor reports running' if fresh else 'Stale running state; process check required'
    return 'Supervisor: ' + row.get('status', 'not scheduled')
