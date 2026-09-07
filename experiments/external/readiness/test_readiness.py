import json

import pytest

from experiments.external.readiness.model import assess, suggestion
from experiments.external.readiness.report import publish
from experiments.external.readiness.review import history, record, state, validate


def example():
    row = {'api': 'load_events', 'status': 'fail', 'runner_category': 'runtime',
           'error': 'ValueError: bad input', 'source': 'lib/io.py:1',
           'checkpoint_attempts': 1, 'provider_error_attempts': 0}
    ledger = {'status': 'complete', 'expected': 2, 'fingerprint': 'fp', 'manifest_file_sha256': 'manifest',
              'rows': [row, {'api': 'other', 'status': 'pass'}]}
    return row, ledger, suggestion('repo', 'A1', row, ledger)


def decision(card, action, actor_type='human', **fields):
    return {'id': card['id'], 'evidence_version': card['evidence_version'], 'action': action,
            'actor': 'Test reviewer', 'actor_type': actor_type, 'note': 'Reviewed test evidence', **fields}


def plan():
    return {'summary': 'Clarify input schema', 'files': ['docs/api.md'], 'validation': 'Isolated fixture test',
            'risks': 'New treatment', 'isolation': 'New worktree'}


def test_readiness_reports_only_measured_capabilities():
    _, ledger, _ = example()
    result = assess(ledger, {}, {})
    assert result['final_raw_pass_percent'] == 50
    assert result['overall_readiness_score'] is None
    assert result['dimensions']['workflow_completion']['status'] == 'not_measured'
    ledger['status'] = 'partial'
    assert assess(ledger, {}, {})['final_raw_pass_percent'] is None


def test_incomplete_or_duplicate_denominator_cannot_be_final():
    _, ledger, _ = example()
    ledger['rows'][0]['status'] = 'pending'
    assert assess(ledger, {}, {})['status'] == 'partial_measurement'
    ledger['rows'][0]['api'] = 'other'
    assert assess(ledger, {}, {})['status'] == 'invalid_evidence'


def test_provider_barrier_is_not_a_codebase_defect():
    row, ledger, _ = example()
    row['runner_category'] = 'llm-error'
    card = suggestion('repo', 'A1', row, ledger)
    assert card['change_kind'] == 'execution_infrastructure'
    assert assess(ledger, {}, {})['final_raw_pass_percent'] is None


def test_retry_counters_do_not_invalidate_review_but_evidence_changes_do():
    row, ledger, card = example()
    row['checkpoint_attempts'] += 1
    again = suggestion('repo', 'A1', row, ledger)
    assert again['evidence_version'] == card['evidence_version']
    row['error'] = 'Different input failure'
    changed = suggestion('repo', 'A1', row, ledger)
    assert changed['id'] == card['id'] and changed['evidence_version'] != card['evidence_version']


def test_agent_cannot_self_approve_or_accept_without_evidence(tmp_path):
    _, _, card = example()
    record(card, [], decision(card, 'propose', 'agent', plan=plan()), tmp_path)
    events = history(tmp_path/'decisions.jsonl')
    with pytest.raises(ValueError, match='Human review'):
        validate(card, events, decision(card, 'approve_plan', 'agent', executor='agent'))
    with pytest.raises(ValueError, match='Human review'):
        validate(card, events, decision(card, 'accept_result'))


def test_full_review_lifecycle_preserves_immutable_submission(tmp_path):
    _, _, card = example()
    def add(action, who='human', **fields):
        return record(card, history(tmp_path/'decisions.jsonl'), decision(card, action, who, **fields), tmp_path)
    add('propose', 'agent', plan=plan())
    add('approve_plan', executor='agent')
    artifact = tmp_path/'validation.txt'
    artifact.write_text('original recorded validation')
    add('submit_result', 'agent', result={'validation_status': 'passed', **{k: str(artifact) for k in ('change','validation','comparison')}})
    artifact.write_text('changed outside the review record')
    add('accept_result')
    reviewed = state(card, history(tmp_path/'decisions.jsonl'))
    assert reviewed['status'] == 'accepted_by_reviewer'
    snapshot = tmp_path/reviewed['result']['validation']['snapshot']
    assert snapshot.read_text() == 'original recorded validation'
    add('propose', 'agent', plan=plan())
    assert state(card, history(tmp_path/'decisions.jsonl'))['status'] == 'proposed'


def test_changed_evidence_invalidates_decisions(tmp_path):
    _, _, card = example()
    old = decision(card, 'propose', 'agent', plan=plan())
    record(card, [], old, tmp_path)
    changed = dict(card, evidence_version='changed')
    assert state(changed, history(tmp_path/'decisions.jsonl'))['status'] == 'stale_review'
    with pytest.raises(ValueError, match='Stale'):
        validate(changed, [], old)


def test_corrupt_history_fails_closed(tmp_path):
    _, _, card = example()
    record(card, [], decision(card,'defer'), tmp_path)
    path = tmp_path/'decisions.jsonl'
    row = json.loads(path.read_text()); row['previous_event'] = 'bad chain'
    path.write_text(json.dumps(row)+'\n')
    with pytest.raises(ValueError, match='inconsistent'):
        history(path)


def test_no_concrete_plan_or_validation_no_approval(tmp_path):
    _, _, card = example()
    with pytest.raises(ValueError, match='concrete plan'):
        validate(card, [], decision(card,'propose',plan={}))
    record(card, [], decision(card,'propose',plan=plan()),tmp_path)
    record(card, history(tmp_path/'decisions.jsonl'), decision(card,'approve_plan',executor='human'),tmp_path)
    with pytest.raises(ValueError, match='artifacts'):
        validate(card, history(tmp_path/'decisions.jsonl'), decision(card,'submit_result',result={}))


def test_publisher_preserves_decisions_and_does_not_credit_disappearing_failures(tmp_path):
    row, ledger, card = example()
    def put(path, value):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))
    put(tmp_path/'data_validation/release_status.json', {'repo': 'WITHHELD/PARTIAL'})
    for cell in ('A1','A2','B1','B2'):
        put(tmp_path/'repo'/cell/'ledger.json', ledger)
    out = tmp_path/'data_validation/readiness'
    assessment, queue = publish(tmp_path)
    assert not assessment['errors'] and len(queue['cards']) == 4
    record(card, [], decision(card,'defer'),out)
    _, queue = publish(tmp_path)
    assert next(c for c in queue['cards'] if c['id'] == card['id'])['review']['status'] == 'deferred'
    ledger['rows'][0]['status'] = 'pass'
    put(tmp_path/'repo/A1/ledger.json',ledger)
    _, queue = publish(tmp_path)
    assert card['id'] in queue['inactive_reviewed_ids']
    assert len(history(out/'decisions.jsonl')) == 1
    assert (tmp_path/'AIDEAL_REPORT.md').is_file()
