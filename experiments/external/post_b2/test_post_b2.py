from copy import deepcopy
import json
from pathlib import Path

import pytest
import yaml

from experiments.external.recovery.engine import policy
from . import evidence as e, stage, report
from .__main__ import isolated_paths


def result():
    fp = {key: key for key in ('project', 'language', 'manifest_sha256', 'scaffold', 'source', 'fixtures', 'engine')}
    fp.update(schema=3, doc_source='aideal', doc_scope='relevant', max_fix_rounds=0,
              models={'audience': 'same', 'fixer': 'same'}, class_context=False, timeout_s=600,
              document_sha256='a2-doc', execute_config={'work_dir': 'A2', 'output_dir': 'A2/out', 'command': 'test'},
              interpreter={'executable': '/python', 'version': 'same', 'environment_sha256': 'env'})
    return {'doc_source': 'aideal', 'run': {**fp, 'api_count': 2, 'fingerprint_components': fp,
            'experiment_fingerprint': e.fingerprint(fp)},
            'metrics': {'first': {'status': 'fail', 'error_category': 'runtime'}, 'second': {'status': 'pass'}}}


def seal(row):
    row['run']['experiment_fingerprint'] = e.fingerprint(row['run']['fingerprint_components'])
    return row


def test_match_allows_document_treatment_and_output_paths_only():
    left, right = result(), result()
    right['run']['fingerprint_components']['document_sha256'] = 'rewritten'
    right['run']['fingerprint_components']['execute_config']['work_dir'] = 'B2'
    seal(right)
    assert e.matched(left, right, 2)


@pytest.mark.parametrize('field', ['prompt_contract', 'transport_contract'])
def test_schema4_comparison_rejects_prompt_or_transport_drift(field):
    left, right = result(), result()
    for value in (left, right):
        value['run']['fingerprint_components'].update(schema=4, prompt_contract={'hash':'same'},
                                                    transport_contract={'hash':'same'})
        seal(value)
    assert e.matched(left, right, 2)
    right['run']['fingerprint_components'][field] = {'hash':'changed'}
    seal(right)
    with pytest.raises(ValueError, match=field):
        e.matched(left, right, 2)


@pytest.mark.parametrize('field', ['source', 'fixtures', 'scaffold', 'engine', 'models', 'manifest_sha256', 'timeout_s'])
def test_match_rejects_confounders(field):
    left, right = result(), result()
    right['run']['fingerprint_components'][field] = 'changed'
    seal(right)
    with pytest.raises(ValueError, match='mismatch'):
        e.matched(left, right, 2)


def test_incomplete_or_provider_result_cannot_start_recovery():
    value = result()
    value['metrics']['first']['error_category'] = 'llm-error'
    with pytest.raises(ValueError):
        e.complete(value, 2)
    value = result()
    del value['metrics']['second']
    with pytest.raises(ValueError):
        e.complete(value, 2)


def test_frozen_cohort_excludes_infra_but_not_future_validation_blocks():
    value = result()
    value['metrics']['second'] = {'status': 'fail', 'error_category': 'infra'}
    names, excluded = e.cohort(value)
    assert names == ['first'] and list(excluded) == ['second']


def test_composite_preserves_B2_native_and_paired_A2_cohort():
    a2, b2 = result(), result()
    b2['metrics']['first'] = {'status': 'pass'}
    b2['metrics']['second'] = {'status': 'fail', 'error_category': 'runtime'}
    info = {'A2': a2, 'B2': b2, 'source': {'apis': {'first': {'status': 'stuck'}}}}
    state = {'protocol': 'v3', 'identity': {}, 'apis': {'second': {'status': 'recovered_native', 'code_fix_rounds': 1}}}
    original = deepcopy(info)
    row = stage.compare(info, state)
    assert row['B2_native_pass'] == 1 and row['B2_plus_S_B2_composite_native_pass'] == 2
    assert row['on_F_A2']['B2_plus_S_B2_pass'] == 1
    assert row['apis']['second']['B2_regression']
    assert info == original


def test_registration_rejects_changed_source_engine(monkeypatch):
    monkeypatch.setattr(stage, 'implementation', lambda: {'changed': 'engine'})
    with pytest.raises(ValueError, match='changed after'):
        stage.registered()


def test_source_prompt_mismatch_blocks_paired_recovery():
    keys = ('mode', 'max_code_fix_rounds', 'stuck_rounds', 'runner_sha256', 'engine_sha256',
            'validation_sha256', 'compatibility_adapter_sha256', 'protocol_sha256',
            'prompt_sha256', 'context_engine')
    current = dict.fromkeys(keys, 'same')
    prior = {**current, 'prompt_sha256': 'different'}
    with pytest.raises(ValueError, match='source prompt'):
        stage.same_source_treatment({'apis': {'fn': {'identity': prior}}}, current)


def test_preflight_failure_remains_in_denominator(tmp_path, monkeypatch):
    state = {'apis': {'first': {'status': 'pending'}}}
    monkeypatch.setattr(stage, 'load_config', lambda *a: (_ for _ in ()).throw(ValueError('fixture differs')))
    assert stage.one({'config': tmp_path/'config'}, tmp_path/'work', tmp_path, state)
    saved = json.loads((tmp_path/'summary.json').read_text())
    assert len(saved['apis']) == 1 and saved['apis']['first']['status'] == 'preflight_blocked'
    assert saved['native_recovery_by_round']['5'] == 0


def test_document_audit_retains_restart_round_counts(tmp_path):
    folder = tmp_path/'docs/eval/B2'
    folder.mkdir(parents=True)
    text = '\n'.join(f'[docfix 1/1] fn round {r}/5: deep-dive -> diagnose -> rewrite -> run' for r in [1,2,3,4,5,1])
    (folder/'docfix_command.json.stderr.log').write_text(text)
    audit = report.document_audit(tmp_path)
    assert audit['doc_round_starts_in_append_log']['fn'] == 6
    assert audit['apis_with_more_than_five_round_starts'] == ['fn']
    assert audit['validation_outcomes_in_append_log'] == {}


def test_output_ownership_rejects_nested_native_or_report_paths(tmp_path):
    with pytest.raises(ValueError, match='separate'):
        isolated_paths(tmp_path/'out/work', tmp_path/'out', tmp_path/'v2', tmp_path)
    with pytest.raises(ValueError, match='native'):
        isolated_paths(tmp_path/'GRAIL_mir_eval_B2/work', tmp_path/'out', tmp_path/'v2', tmp_path)


@pytest.fixture
def admitted(tmp_path, monkeypatch):
    monkeypatch.setattr(e, 'REPOSITORIES', {'mir_eval': ('GRAIL_mir_eval', 'project', 2)})
    roots = {c: tmp_path/f'GRAIL_mir_eval_{c}'/'project' for c in ('A2','B2')}
    native = result()
    for cell, root in roots.items():
        p = root/f'docs/eval/{cell}/comprehension.json'
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(native))
    inherited = roots['B2']/'docs/eval/A2/comprehension.json'
    inherited.parent.mkdir(parents=True)
    inherited.write_text(json.dumps(native))
    (roots['B2']/'docs/eval/B2/docfix.json').write_text(json.dumps({'attempted':1,'processed':1,'apis':{'first':{'status':'doc-fixed'}}}))
    up = tmp_path/'v2'/'mir_eval'
    (up/'source').mkdir(parents=True)
    summary = {'identity': {'baseline_sha256':e.file_sha(roots['A2']/'docs/eval/A2/comprehension.json'), 'protocol':policy()},
               'apis': {'first': {'status':'stuck'}}}
    (up/'source/summary.json').write_text(json.dumps(summary))
    repair = ['fix-docs','--from-results','docs/eval/A2/comprehension.json','--doc-rounds','5','--doc-stuck','2','--retry-rounds','0','--deep-dive-first']
    fresh = ['comprehension','--max-fix-rounds','0','--doc','aideal','--doc-scope','relevant']
    jobs = [{'id':'mir_eval_B2_repair','command':repair}, {'id':'mir_eval_B2_zero','command':fresh,'environment_inventory':'env.txt','cwd':str(roots['B2'])}]
    (up/'b2_watchdog.yaml').write_text(yaml.safe_dump({'jobs':jobs}))
    (up/'b2_watchdog.state.json').write_text(json.dumps({'jobs':{j['id']:{'status':'succeeded'} for j in jobs}}))
    return tmp_path, up


def test_source_provider_retry_does_not_block_this_repositories_B2(admitted):
    parent, up = admitted
    assert e.inspect('mir_eval',parent,up.parent)['names'] == ['first']
    path = up/'source/summary.json'
    state = json.loads(path.read_text())
    state['apis']['first']['status'] = 'provider_blocked'
    path.write_text(json.dumps(state))
    ready, blocked = e.admission(parent,up.parent)
    assert 'mir_eval' in ready and not blocked
    from .source_retry import needed
    assert needed(ready['mir_eval'])


def test_completed_native_file_does_not_override_running_B2_worker(admitted):
    parent, up = admitted
    path = up/'b2_watchdog.state.json'
    state = json.loads(path.read_text())
    state['jobs']['mir_eval_B2_zero']['status'] = 'running'
    path.write_text(json.dumps(state))
    with pytest.raises(ValueError, match='not all succeeded'):
        e.inspect('mir_eval',parent,up.parent)


def test_changed_A2_inherited_result_rejected(admitted):
    parent, up = admitted
    (parent/'GRAIL_mir_eval_B2/project/docs/eval/A2/comprehension.json').write_text('{}')
    with pytest.raises(ValueError, match='inherit'):
        e.inspect('mir_eval',parent,up.parent)


def test_scheduler_runs_ready_repo_even_when_another_is_pending(tmp_path, monkeypatch):
    import sys
    from contextlib import contextmanager
    from . import __main__ as controller
    class ObservedWait(Exception):
        pass
    # Scheduling is independent of the immutable historical registration receipt.
    monkeypatch.setattr(controller.stage, 'registered', lambda: {})
    monkeypatch.setattr(controller, 'admission', lambda *args: ({'mir_eval': {}}, {'tslearn': 'A2 incomplete'}))
    monkeypatch.setattr(controller.time, 'sleep', lambda *args: (_ for _ in ()).throw(ObservedWait()))
    monkeypatch.setattr(controller.report, 'publish', lambda *args: None)
    called = []
    monkeypatch.setattr(controller.stage, 'prepare', lambda *args: {'apis': {'fn': {'status': 'pending'}}, 'statuses': {}})
    monkeypatch.setattr(controller.stage, 'one', lambda *args: called.append('mir_eval') or False)
    monkeypatch.setattr(controller.stage, 'compare', lambda *args: {})
    monkeypatch.setattr(controller.source_retry, 'needed', lambda *args: False)
    @contextmanager
    def admitted_slot(*args):
        yield True
    monkeypatch.setattr(controller, 'slot', admitted_slot)
    monkeypatch.setattr(sys, 'argv', ['post_b2', '--workspace-parent', str(tmp_path),
        '--upstream', str(tmp_path/'v2'), '--out', str(tmp_path/'v3'), '--work', str(tmp_path/'private'),
        '--admit-until', '2099-09-09T10:15:00-07:00', '--watch'])
    with pytest.raises(ObservedWait):
        controller.main()
    assert called == ['mir_eval']
    assert json.loads((tmp_path/'v3/scheduler_completion.json').read_text())['repositories']['tslearn'] == 'A2 incomplete'


def test_shared_admission_reserves_native_capacity_and_excludes_second_worker(tmp_path, monkeypatch):
    from .admission import slot, native_reservation
    monkeypatch.setenv('AIDEAL_GOOGLE_RECOVERY_ADMISSION_LOCK', str(tmp_path/'gate.lock'))
    monkeypatch.setenv('AIDEAL_GOOGLE_RATE_STATE', str(tmp_path/'rate.txt'))
    monkeypatch.setenv('AIDEAL_GOOGLE_MIN_INTERVAL_S', '3')
    upstream = tmp_path/'v2'
    assert native_reservation(upstream) == 6
    with slot(upstream, 'too early') as ok:
        assert not ok
    (upstream/'mir_eval').mkdir(parents=True)
    (upstream/'mir_eval/b2_watchdog.state.json').write_text(json.dumps({'jobs': {'B2': {'status':'succeeded'}}}))
    assert native_reservation(upstream) == 5
    with slot(upstream, 'first') as ok:
        assert ok
        with slot(upstream, 'second') as second:
            assert not second
    with slot(upstream, 'after release') as ok:
        assert ok
