import json
import pytest
from .evidence import collect, digest
from .report import publish
from .transport import treatment_policy


def checkpoint(tmp_path, rows):
    manifest = tmp_path / 'docs/eval/api_manifest.json'
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps(['first', 'second']))
    path = tmp_path / '.aideal_exec/B2/comprehension_progress.jsonl'
    path.parent.mkdir(parents=True)
    path.write_text(''.join(json.dumps(row)+'\n' for row in rows) + '{"unfinished":')
    return path


def row(name, fingerprint):
    return {'name': name, 'experiment_fingerprint': fingerprint, 'status': 'pass'}


def test_fresh_journal_never_merges_unproven_groups(tmp_path):
    checkpoint(tmp_path, [row('first', 'old'), row('second', 'new')])
    data = collect(tmp_path, 'B2')
    assert set(data['rows']) == {'second'} and data['expected'] == 2
    assert not data['complete'] and 'Provisional' in data['identity_status']


def test_active_identity_wins_over_last_observed_group(tmp_path):
    parts = {'schema': 4}
    path = checkpoint(tmp_path, [row('first', digest(parts)), row('second', 'other')])
    path.with_name('run_identity.json').write_text(json.dumps({
        'fingerprint_components': parts, 'experiment_fingerprint': digest(parts)}))
    data = collect(tmp_path, 'B2')
    assert set(data['rows']) == {'first'} and 'Bound' in data['identity_status']


def test_corrupt_active_identity_fails_closed(tmp_path):
    path = checkpoint(tmp_path, [row('first', 'other')])
    path.with_name('run_identity.json').write_text(json.dumps({
        'fingerprint_components': {'schema': 4}, 'experiment_fingerprint': 'wrong'}))
    with pytest.raises(ValueError, match='corrupt'):
        collect(tmp_path, 'B2')


def test_manifest_mismatch_rejected(tmp_path):
    checkpoint(tmp_path, [row('unknown', 'fp')])
    with pytest.raises(ValueError, match='manifest'):
        collect(tmp_path, 'B2')


def test_empty_workspace_can_still_publish_status(tmp_path):
    out = tmp_path / 'reports'
    summary = publish(tmp_path, out)
    assert summary['api_rows'] == 0 and len(summary['cells']) == 9
    assert (out / 'API_TIMINGS.csv').read_text().startswith('repository,cell')


def test_transport_match_ignores_output_locations_but_not_timing():
    left = {'config': '/A2/config.yaml', 'output': '/A2/events', 'request_timeout_s': 600}
    right = dict(left, config='/B2/config.yaml', output='/B2/events')
    assert treatment_policy(left) == treatment_policy(right)
    right['request_timeout_s'] = 300
    assert treatment_policy(left) != treatment_policy(right)
