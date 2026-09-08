import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from . import compatibility as c
from .driver import b2_jobs
from .engine import policy
from .runner import isolated_config


def test_registered_protocol_excludes_original_repairs_and_other_cells():
    p = policy()
    assert p['baseline_cells'] == ['A2'] and p['modes'] == ['source']
    assert p['original_document_repair'] is False
    assert (p['max_code_fix_rounds'], p['stuck_rounds']) == (5, 2)


def test_schema3_checks_all_seven_engine_files(tmp_path):
    assert len(c.engine_files(tmp_path, 3)) == 7
    assert len(c.engine_files(tmp_path, 2)) == 5
    with pytest.raises(ValueError): c.engine_files(tmp_path, 99)


def test_migration_retains_historical_output_limit_but_rejects_changed_treatment(tmp_path):
    checkpoint = tmp_path/'comprehension_progress.jsonl'
    captured = tmp_path/'input_proof.json'
    captured.write_text('{}')
    legacy = {'schema': 2, 'engine': 'old', 'fixtures': 'old-output', 'doc_source': 'aideal'}
    current = {**legacy, 'schema': 3, 'engine': 'new', 'fixtures': 'inputs'}
    record = {'schema': 1, 'checkpoint': str(checkpoint), 'legacy_components': legacy,
              'legacy_fingerprint': c.fingerprint(legacy), 'current_components': current,
              'input_fixtures': 'inputs', 'selection_policy': 'reviewed', 'reason': 'reviewed',
              'captured_proof': str(captured),
              'captured_proof_sha256': hashlib.sha256(captured.read_bytes()).hexdigest()}
    checkpoint.with_name('checkpoint_compatibility.json').write_text(json.dumps(record))
    native = {**legacy, 'fixtures': 'later-output'}
    result = {'run': {'checkpoint': str(checkpoint), 'fingerprint_components': native,
                      'experiment_fingerprint': c.fingerprint(native)}}
    resolved, proof = c.components(result)
    assert resolved == current and proof['historical_output_aggregate_differs']
    native['doc_source'] = 'original'
    result['run']['experiment_fingerprint'] = c.fingerprint(native)
    with pytest.raises(ValueError, match='beyond mutable output'):
        c.components(result)


def test_new_driver_creates_only_A2_document_repair_and_fresh_B2(tmp_path):
    from experiments.external import run_external_2x2_pipeline as old
    relative = Path('experiments/external/mir_eval')
    a2, b2 = tmp_path/'A2', tmp_path/'B2'
    source_doc = a2/relative/'docs/eval/A2/LLM_readme.md'
    source_doc.parent.mkdir(parents=True)
    source_doc.write_text('frozen A2 document')
    source_doc.with_name('comprehension.json').write_text('{"baseline": "A2"}')
    inventory = b2/relative/'docs/eval/setup/environment_B2.txt'
    inventory.parent.mkdir(parents=True)
    inventory.write_text('existing runtime')
    module = SimpleNamespace(git=lambda *args: SimpleNamespace(stdout='source-sha'),
        ensure_worktree=lambda *args: b2, make_job=old.make_job, REPOS=old.REPOS)
    trees = {'A2': a2}
    jobs = b2_jobs('mir_eval', tmp_path/'setup', trees, module, relative)
    assert [job['id'] for job in jobs] == ['mir_eval_B2_repair', 'mir_eval_B2_zero']
    command = jobs[0]['command']
    assert command[command.index('--from-results') + 1] == 'docs/eval/A2/comprehension.json'
    assert '--create-missing' not in command
    assert jobs[1]['depends_on'] == ['mir_eval_B2_repair']
    assert (b2/relative/'docs/eval/B2/LLM_readme.md').read_text() == source_doc.read_text()


def test_deep_recovery_output_rebases_tslearn_import_without_mutating_baseline(tmp_path):
    from aideal.config import load_config
    path = tmp_path/'configs/aideal.yaml'
    path.parent.mkdir()
    path.write_text('project: {name: tslearn, language: Python}\ncomprehension:\n  execute:\n'
                    '    command: env PYTHONPATH=../../tslearn python {test_file}\n')
    cfg = load_config(path)
    recovered = isolated_config(cfg, tmp_path/'deep/round/attempt', 'prompt')
    assert '../../tslearn' in cfg.comprehension['execute']['command']
    assert str(tmp_path/'tslearn') in recovered.comprehension['execute']['command']
    assert recovered.comprehension['execute']['work_dir'] != cfg.comprehension['execute']['work_dir']


def test_completed_A2_starts_repair_without_waiting_for_A1(tmp_path, monkeypatch):
    import sys
    import threading
    from . import driver
    setup = tmp_path/'GRAIL_mir_eval_setup'
    setup.mkdir()
    for cell in ('A1', 'A2'):
        (tmp_path/f'GRAIL_mir_eval_{cell}').mkdir()
    baseline = tmp_path/'mir_eval_baselines_watchdog.yaml'
    baseline.write_text('existing plan')
    release = threading.Event()
    order = []
    class FakeSupervisor:
        def __init__(self, path):
            self.baseline = path == baseline
            self.state = {'jobs': {'mir_eval_A2_zero': {'status': 'succeeded'}}}
        def run(self):
            if self.baseline:
                assert release.wait(5), 'A2 recovery never started while A1 remained active'
            return 0
    monkeypatch.setattr(driver, 'Supervisor', FakeSupervisor)
    module = SimpleNamespace(REPOS={'mir_eval': {'freeze_branch': 'expected'}},
                             git=lambda *args: SimpleNamespace(stdout='expected'))
    monkeypatch.setattr(driver, 'adapter', lambda *args: module)
    def recover(*args, **kwargs):
        assert not release.is_set()
        order.append('source_from_A2')
        release.set()
        return {'apis': {}, 'statuses': {}}
    monkeypatch.setattr(driver, 'batch', recover)
    monkeypatch.setattr(driver, 'completed_cell', lambda repo, cell, *args: order.append(cell))
    def jobs(repo, setup, trees, *args):
        trees['B2'] = tmp_path/'B2'
        return [{'id': 'B2'}]
    monkeypatch.setattr(driver, 'b2_jobs', jobs)
    monkeypatch.setattr(driver, 'report', lambda *args: order.append('report'))
    reporter = SimpleNamespace(join=lambda **kwargs: None)
    monkeypatch.setattr(driver.reporting, 'start', lambda *args: (threading.Event(), reporter))
    monkeypatch.setattr(driver.reporting, 'publish', lambda *args: None)
    monkeypatch.setattr(sys, 'argv', ['driver', 'mir_eval', '--freeze-worktree', str(setup),
        '--work', str(tmp_path/'work'), '--out', str(tmp_path/'out')])
    driver.main()
    assert order == ['A2', 'source_from_A2', 'B2', 'A1', 'report']


def test_legacy_adapter_receives_string_git_paths(tmp_path):
    from .driver import completed_cell
    captured = []
    def commit(worktree, branch, message, paths):
        # The legacy command logger joins its argv without coercion.
        captured.append(' '.join(['git', 'add', '--', *paths]))
    module = SimpleNamespace(analyze=lambda *args: None, commit_push=commit)
    completed_cell('mir_eval', 'A2', tmp_path, module, Path('experiments/external/mir_eval'))
    assert captured and 'docs/eval/A2' in captured[0]
