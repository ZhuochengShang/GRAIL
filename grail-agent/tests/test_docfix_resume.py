import json
import pytest

import aideal.docfix as docfix
import aideal.llm as llm
from aideal.repair_journal import RepairJournal
from test_docfix_iterative import _cfg, _entry, Script, patched


def test_validation_provider_retry_reuses_completed_rewrite(tmp_path, patched):
    cfg = _cfg(tmp_path)
    script = Script(['diagnosis'], [_entry('saved rewrite')],
                    [('fail', 'llm-error', '504'), ('pass', None, '')])
    patched(script)
    args = dict(apis=['foo'], doc_rounds=5, retry_rounds=0, report_path=tmp_path/'report.json')
    first = docfix.doc_fix_run(cfg, **args)
    assert first['blocked']
    second = docfix.doc_fix_run(cfg, **args)
    assert second['apis']['foo']['status'] == 'doc-fixed'
    assert second['apis']['foo']['rounds_used'] == 1
    assert len(script.rewrite_inputs) == 1 and len(script.retry_calls) == 2


def test_restart_preserves_round_budget_and_true_original(tmp_path, patched, monkeypatch):
    cfg = _cfg(tmp_path)
    original = cfg.llm_readme.read_text()
    script = Script(['first diagnosis'], [_entry('first draft')], [('fail', 'runtime', 'one')])
    patched(script)
    invoke = script.invoke_text
    count = 0
    def fail_second_diagnosis(spec, system, user):
        nonlocal count
        if system.endswith('docfix_diagnose'):
            count += 1
            if count == 2:
                raise TimeoutError('provider deadline')
        return invoke(spec, system, user)
    monkeypatch.setattr(llm, 'invoke_text', fail_second_diagnosis)
    args = dict(apis=['foo'], doc_rounds=2, doc_stuck=0, retry_rounds=0, report_path=tmp_path/'report.json')
    assert docfix.doc_fix_run(cfg, **args)['blocked']
    second = Script(['second diagnosis'], [_entry('second draft')], [('fail', 'runtime', 'two')])
    patched(second)
    row = docfix.doc_fix_run(cfg, **args)['apis']['foo']
    assert row['rounds_used'] == 2
    assert len(second.rewrite_inputs) == 1 and 'first draft' in second.rewrite_inputs[0]
    assert cfg.llm_readme.read_text().strip() == original.strip()


def test_crash_after_saved_validation_does_not_repeat_model_or_execution(tmp_path, patched, monkeypatch):
    cfg = _cfg(tmp_path)
    script = Script(['diagnosis'], [_entry('saved')], [('pass', None, '')])
    patched(script)
    args = dict(apis=['foo'], doc_rounds=5, retry_rounds=0, report_path=tmp_path/'report.json')
    checkpoint = RepairJournal.checkpoint
    def crash(*args):
        raise RuntimeError('simulated interruption after durable validation')
    monkeypatch.setattr(RepairJournal, 'checkpoint', crash)
    with pytest.raises(RuntimeError, match='simulated'):
        docfix.doc_fix_run(cfg, **args)
    monkeypatch.setattr(RepairJournal, 'checkpoint', checkpoint)
    row = docfix.doc_fix_run(cfg, **args)['apis']['foo']
    assert row['status'] == 'doc-fixed' and row['rounds_used'] == 1
    assert len(script.retry_calls) == len(script.rewrite_inputs) == 1


def test_ambiguous_phase_never_silently_issues_second_call(tmp_path):
    path = tmp_path/'state.json'
    journal = RepairJournal(path, 'identity', {})
    class Crash(BaseException):
        pass
    with pytest.raises(Crash):
        journal.phase(0, 'rewrite', lambda: (_ for _ in ()).throw(Crash()))
    resumed = RepairJournal(path, 'identity', {})
    with pytest.raises(RuntimeError, match='unacknowledged'):
        resumed.phase(0, 'rewrite', lambda: pytest.fail('must not call provider'))
    assert len(json.loads(path.read_text())['phases']['0:rewrite']['attempts']) == 1
