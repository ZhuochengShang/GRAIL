import pytest
from .worker import cohort
from .audit import normalized_execution


def baseline():
    return {'doc_source': 'aideal', 'run': {'api_count': 3, 'manifest_api_count': 3,
            'max_fix_rounds': 0}, 'metrics': {'ok': {'status': 'pass'},
            'bad': {'status': 'fail', 'error_category': 'runtime'},
            'dependency': {'status': 'fail', 'error_category': 'infra'}}}


def test_both_branches_keep_dependency_failures_in_frozen_cohort():
    assert cohort(baseline()) == ['bad', 'dependency']


def test_provider_pending_and_incomplete_baselines_are_not_admitted():
    r = baseline()
    r['metrics']['bad']['error_category'] = 'llm-error'
    with pytest.raises(ValueError):
        cohort(r)
    r = baseline()
    r['run']['manifest_api_count'] = 4
    with pytest.raises(ValueError):
        cohort(r)


def test_reuse_ignores_only_owned_paths():
    assert normalized_execution({'work_dir': 'A2', 'timeout_seconds': 30}) == normalized_execution(
        {'work_dir': 'B2', 'timeout_seconds': 30})
    assert normalized_execution({'timeout_seconds': 30}) != normalized_execution({'timeout_seconds': 60})


def test_feedback_execution_never_requests_source_mode(monkeypatch, tmp_path):
    from . import worker
    called = []
    def fake_run(cfg, base, result, name, mode, manifest, **kw):
        called.append(mode)
        return {'status': 'recovered_native', 'rounds': [{'status': 'pass'}],
                'diagnosis': {'report_text': '', 'llm_calls': 0}}
    monkeypatch.setattr(worker, 'run', fake_run)
    state = {'apis': {'bad': {'status': 'ready'}}}
    worker.execute_one(None, None, {}, {}, state, tmp_path, 'manifest', 'bad')
    assert called == ['feedback']
    assert state['apis']['bad']['code_fix_rounds'] == 1
    assert state['complete'] is True


def test_unexpected_source_diagnosis_gets_no_credit(monkeypatch, tmp_path):
    from . import worker
    monkeypatch.setattr(worker, 'run', lambda *a, **kw: {'status': 'recovered_native',
        'diagnosis': {'report_text': 'source leakage'}, 'rounds': []})
    state = {'apis': {'bad': {'status': 'ready'}}}
    worker.execute_one(None, None, {}, {}, state, tmp_path, 'manifest', 'bad')
    assert state['apis']['bad']['status'] == 'evidence_blocked'
