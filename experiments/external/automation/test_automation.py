from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pytest

from experiments.external.automation.analysis import forecast, classify, overlaps
from experiments.external.automation.contracts import validate_inputs, lint_python
from experiments.external.automation.quota import Gate, Limits


def ledger(errors, fp='current'):
    return {'status': 'partial', 'fingerprint': fp,
            'rows': [{'status': 'pending'} for _ in range(10)],
            'all_checkpoint_events': [{'experiment_fingerprint': fp, 'status': 'fail' if error else 'pass',
                'error_category': 'llm-error' if error else None, 'wall_s': 60} for error in errors]}


def test_forecast_does_not_treat_failed_provider_attempts_as_progress():
    assert forecast(ledger([True]*10))['state'] == 'stalled_no_recent_terminal_outcomes'
    mixed = forecast(ledger([True, False]*5))
    assert mixed['hours']['likely'] == pytest.approx(10*60/0.5/3600)
    assert 'document repair/deep dives' in mixed['excludes']


def test_forecast_ignores_incompatible_fingerprint_and_short_samples():
    d = ledger([False]*5)
    d['all_checkpoint_events'] += ledger([True]*30, 'old')['all_checkpoint_events']
    assert forecast(d)['recent_terminal_fraction'] == 1
    assert forecast(ledger([False]*2))['hours'] is None


def test_rare_provider_recovery_keeps_scenarios_ordered():
    hours = forecast(ledger([True]*29+[False]))['hours']
    assert hours['optimistic'] <= hours['likely'] <= hours['conservative']


def test_path_ownership_checks_parent_child_conflicts_but_allows_same_owner():
    assert overlaps([('A', Path('/x/A')), ('A', Path('/x/A/out'))]) == []
    assert overlaps([('A', Path('/x/A')), ('B', Path('/x/A/out'))])
    assert not overlaps([('A', Path('/x/A')), ('B', Path('/x/AB'))])


def test_review_preserves_native_labels_and_manual_evidence():
    row = {'runner_category': 'infra', 'error': "ImportError: cannot import name 'imaginary'"}
    assert classify(row)[0] == 'api-identity-or-version'
    assert row['runner_category'] == 'infra'
    row.update(review_evidence={'reason': 'source checked'}, primary_category='doc-wrong')
    assert classify(row)[:2] == ('doc-wrong', 'reviewed')


def test_contract_rejects_wrong_dtype_shape_and_unobserved_units():
    contract = {'schema_version': 1, 'api': 'lib.func', 'inputs': {'X': {'shape': [None,40,1], 'dtype': 'float64', 'units': 'Hz'}}}
    actual = {'X': {'shape': [8,40,1], 'dtype': 'float64', 'units': 'Hz'}}
    assert validate_inputs(contract, actual)['status'] == 'metadata_matches'
    actual['X'] = {'shape': [8,40], 'dtype': 'int64'}
    result = validate_inputs(contract, actual)
    assert result['status'] == 'mismatch' and len(result['issues']) == 3
    assert validate_inputs({}, {})['status'] == 'invalid_contract'


def test_contract_rejects_unknown_constraints():
    result = validate_inputs({'schema_version': 1, 'api': 'f', 'inputs': {'x': {'shpae': [2]}}}, {'x': {'shape': [2]}})
    assert result['status'] == 'mismatch'


def test_ast_does_not_count_comments_strings_or_reassigned_imports():
    code = 'import mir_eval.io as io\n# io.load_events(p)\ns="io.load_events(p)"\nio = other\nassert True\n'
    result = lint_python(code, 'mir_eval.io.load_events')
    assert result['candidate_calls'] == []
    assert result['trivial_assertion_lines'] == [5]
    good = lint_python('from mir_eval.io import load_events as load\nx=load(p)\nassert len(x)>0', 'mir_eval.io.load_events')
    assert len(good['candidate_calls']) == 1
    assert good['semantic_validation'].startswith('unverified')


def test_disabled_gate_never_creates_database(tmp_path):
    with pytest.raises(ValueError, match='disabled'):
        Gate(tmp_path/'quota.db', 'project/model', Limits())
    assert not (tmp_path/'quota.db').exists()


def test_quota_counts_failed_requests_tokens_and_cooldowns(tmp_path):
    gate = Gate(tmp_path/'quota.db', 'project/model', Limits(True, 2, 100, 3, 1))
    first = gate.reserve(60, now=1000)
    assert first['admitted']
    assert gate.reserve(10, now=1001)['reason'] == 'inflight'
    gate.finish(first['request_id'], '504')
    assert gate.reserve(50, now=1002)['reason'] == 'input_tpm'
    second = gate.reserve(30, now=1002)
    gate.finish(second['request_id'], 'ok')
    assert gate.reserve(1, now=1003)['reason'] == 'rpm'
    gate.cooldown(90, now=1003)
    assert gate.reserve(1, now=1061)['reason'] == 'shared_cooldown'
    third = gate.reserve(1, now=1100)
    assert third['admitted']
    gate.finish(third['request_id'], 'ok')
    assert gate.reserve(1, now=1200)['reason'] == 'rpd'
    assert gate.reserve(1, now=1200+86400)['admitted']


def test_gate_rejects_conflicting_shared_policy(tmp_path):
    Gate(tmp_path/'quota.db', 'same', Limits(True, 2,100,10,1))
    with pytest.raises(ValueError, match='Conflicting'):
        Gate(tmp_path/'quota.db', 'same', Limits(True, 3,100,10,1))


def reserve_worker(path):
    return Gate(path, 'shared', Limits(True, 10,100,100,2)).reserve(10)['admitted']


def test_concurrent_processes_cannot_overbook_inflight(tmp_path):
    path = str(tmp_path/'quota.db')
    Gate(path, 'shared', Limits(True,10,100,100,2))
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(reserve_worker, [path]*8))
    assert sum(results) == 2
