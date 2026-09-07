"""No provider calls, subprocess execution, or writes to real experiments."""
import json
from pathlib import Path
from types import SimpleNamespace
import sys

import pytest

from .engine import recover
from .validation import eligible, validate


INITIAL = {'status': 'fail', 'category': 'runtime', 'code': 'old()', 'error': 'original'}


def outcome(status='fail', error='same'):
    return {'status': status, 'category': 'runtime' if status == 'fail' else None,
            'code': 'candidate()', 'error': error}


def test_resume_reuses_success_and_rejects_changed_identity(tmp_path):
    calls = []
    def attempt(n, previous, diagnosis):
        calls.append(n)
        return outcome('pass')
    state = recover({'source': 'one'}, INITIAL, tmp_path, diagnose=lambda: {}, attempt=attempt)
    assert state['status'] == 'recovered_native'
    assert state['headline_credit'] is False
    recover({'source': 'one'}, INITIAL, tmp_path, diagnose=lambda: {}, attempt=attempt)
    assert calls == [1]
    with pytest.raises(ValueError, match='changed recovery inputs'):
        recover({'source': 'two'}, INITIAL, tmp_path, diagnose=lambda: {}, attempt=attempt)
    assert calls == [1]


def test_provider_failure_does_not_consume_code_round_and_diagnosis_is_reused(tmp_path):
    attempts, diagnoses = [], []
    def diagnose():
        diagnoses.append(1)
        return {'report_text': 'source evidence'}
    def attempt(n, previous, diagnosis):
        attempts.append(n)
        return {**outcome(), 'category': 'llm-error'} if len(attempts) == 1 else outcome('pass')
    a = recover({}, INITIAL, tmp_path, diagnose=diagnose, attempt=attempt)
    assert a['status'] == 'provider_blocked' and not a['rounds']
    b = recover({}, INITIAL, tmp_path, diagnose=diagnose, attempt=attempt)
    assert b['status'] == 'recovered_native' and len(b['events']) == 2
    assert attempts == [1, 1] and diagnoses == [1]


def test_threshold_two_can_miss_a_third_round_recovery(tmp_path):
    def attempt(n, previous, diagnosis):
        return outcome('pass' if n == 3 else 'fail')
    two = recover({}, INITIAL, tmp_path/'two', diagnose=lambda: {}, attempt=attempt, stuck=2)
    three = recover({}, INITIAL, tmp_path/'three', diagnose=lambda: {}, attempt=attempt, stuck=3)
    assert two['status'] == 'stuck' and len(two['rounds']) == 2
    assert three['status'] == 'recovered_native' and len(three['rounds']) == 3
    assert '2 consecutive' in two['stop_reason']


def test_budget_and_infra_stop(tmp_path):
    a = recover({}, INITIAL, tmp_path/'budget', diagnose=lambda: {},
                attempt=lambda n, *args: outcome(error=str(n)), stuck=0)
    assert a['status'] == 'exhausted' and len(a['rounds']) == 5
    b = recover({}, INITIAL, tmp_path/'infra', diagnose=lambda: {},
                attempt=lambda *args: {**outcome(), 'category': 'infra'})
    assert b['status'] == 'infra_blocked' and len(b['rounds']) == 1


def baseline():
    return {'run': {'max_fix_rounds': 0, 'fingerprint_components': {'schema': 2}, 'api_count': 1},
            'metrics': {'target': {'status': 'fail', 'error_category': 'runtime'}}}


@pytest.mark.parametrize('change', ['provider', 'nonzero', 'partial', 'passed', 'infra'])
def test_rejects_ineligible_baseline(change):
    result = baseline()
    if change == 'provider': result['metrics']['target']['error_category'] = 'llm-error'
    if change == 'nonzero': result['run']['max_fix_rounds'] = 5
    if change == 'partial': result['run']['api_count'] = 2
    if change == 'passed': result['metrics']['target']['status'] = 'pass'
    if change == 'infra': result['metrics']['target']['error_category'] = 'infra'
    with pytest.raises(ValueError): eligible(result, 'target')


def test_rejects_shared_worktree_before_reading_sources(tmp_path):
    cfg = SimpleNamespace(root=tmp_path)
    with pytest.raises(ValueError, match='separate'):
        validate(cfg, cfg, baseline(), 'target', 'manifest.json')


def test_study_runner_rejects_unmatched_threshold_before_any_input_or_model_call():
    from .runner import run
    with pytest.raises(ValueError, match='study limits are fixed'):
        run(None, None, {}, 'target', 'source', 'manifest.json', execute=True, stuck=3)


@pytest.mark.parametrize('threshold,expected', [('2', True), ('3', False)])
def test_static_parity_check_detects_changed_limit_without_importing_driver(tmp_path, threshold, expected):
    from experiments.external.check_rdpro_protocol import launch_flags
    path = tmp_path/'driver.py'
    path.write_text('raise RuntimeError("must never execute this driver")\ncommand = '
        + repr(['--max-fix-rounds', '0', '--doc-rounds', '5', '--doc-stuck', threshold,
                '--retry-rounds', '0', '--doc-scope', 'relevant', '--deep-dive-first']))
    assert launch_flags([path])['matches_registered_limits'] is expected


@pytest.mark.parametrize('changed', [None, 'source/target.py', 'fixture.txt', 'scaffold.py', 'doc.md'])
def test_file_identity_gate(tmp_path, monkeypatch, changed):
    from . import validation as v
    from aideal.doc_checks import _sha256_files
    import aideal.doc_checks
    import hashlib
    configs = []
    ex = {'work_dir': 'work', 'test_filename': 'api_test.py', 'scaffold': 'scaffold.py'}
    for label in ('base', 'isolated'):
        root = tmp_path/label
        for path, content in {'source/target.py': 'def target(): pass', 'tests/test.py': 'target()',
                'fixture.txt': '1 2', 'scaffold.py': 'scaffold', 'doc.md': 'documentation',
                'profile.yaml': 'project: test', 'manifest.json': '["target"]',
                'work/run_target/api_test.py': 'target()'}.items():
            dest = root/path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content)
        configs.append(SimpleNamespace(root=root, raw={'files': {'project_profile': 'profile.yaml'}},
            comprehension={'execute': ex}, source_globs=['source/*.py'], test_globs=['tests/*.py'],
            original_readme_files=[], llm_readme=root/'doc.md',
            model_for_role=lambda role: SimpleNamespace(provider='mock', model='fixed')))
    base, cfg = configs
    monkeypatch.setattr(v, '_load_manifest', lambda c, name: json.loads((c.root/name).read_text()))
    monkeypatch.setattr(v, '_execute_sample_data', lambda c, e: (
        {'fixture': str(c.root/'fixture.txt')}, '', []))
    monkeypatch.setattr(v, 'document_hash', lambda c, *args: v.file_sha(c.llm_readme))
    result = baseline()
    result['doc_source'] = 'aideal'
    directory = Path(aideal.doc_checks.__file__).parent
    result['run'].update(manifest_sha256=hashlib.sha256(b'target').hexdigest(),
        document_sha256=v.file_sha(base.llm_readme), doc_scope='relevant',
        experiment_fingerprint='frozen', checkpoint=str(base.root/'work/comprehension_progress.jsonl'),
        models={'audience': 'mock:fixed', 'fixer': 'mock:fixed'})
    fp = result['run']['fingerprint_components']
    fp.update(execute_config=ex,
        source=_sha256_files([base.root/'source/target.py'], base.root),
        scaffold=_sha256_files([base.root/'scaffold.py'], base.root),
        fixtures=_sha256_files([base.root/'fixture.txt'], base.root),
        engine=_sha256_files([directory/n for n in ('config.py','doc_checks.py','llm.py',
                                                     'prompts.py','readme_agent.py')], directory))
    if changed:
        (cfg.root/changed).write_text('changed input')
        with pytest.raises(ValueError, match='differs'):
            validate(base, cfg, result, 'target', 'manifest.json')
    else:
        identity, initial = validate(base, cfg, result, 'target', 'manifest.json')
        assert identity['baseline_fingerprint'] == 'frozen' and initial['code'] == 'target()'


@pytest.mark.parametrize('mode', ['feedback', 'source'])
def test_native_adapter_preserves_round_scripts_and_baseline(tmp_path, monkeypatch, mode):
    from . import runner
    from aideal.config import load_config
    cfg_path = tmp_path/'configs/aideal.yaml'
    cfg_path.parent.mkdir()
    cfg_path.write_text('project: {name: test, language: Python}\n'
        'models:\n  registry: {mock: {provider: mock, model: fixed}}\n'
        '  roles: {audience: mock, fixer: mock}\n'
        'comprehension:\n  execute: {test_filename: api_test.py}\n')
    cfg = load_config(cfg_path)
    prompt = tmp_path/'original_prompt.md'
    original = 'SYSTEM: Use ONLY the documentation provided.\nUSER: {exec_hints}'
    prompt.write_text(original)
    monkeypatch.setattr(runner, 'validate', lambda *args: (
        {'api': 'target', 'baseline_fingerprint': 'base', 'baseline_result_sha256': 'result',
         'script_sha256': 'original'}, dict(INITIAL)))
    monkeypatch.setattr(runner, 'prompt_file', lambda *args: prompt)
    import aideal.docfix
    monkeypatch.setattr(aideal.docfix, '_source_window', lambda *args: ('def target(): pass', ''))
    diagnoses = []
    def deep_dive(current, api, out_dir, return_text):
        diagnoses.append(api)
        path = Path(out_dir)/'target.md'
        path.parent.mkdir(parents=True)
        path.write_text('grounded diagnosis')
        return {'report_text': 'grounded diagnosis', 'report': str(path)}
    monkeypatch.setattr(runner, 'deep_dive_run', deep_dive)
    monkeypatch.setenv('AIDEAL_ENV_FINGERPRINT', 'environment')
    result = {'doc_source': 'aideal', 'run': {'doc_scope': 'relevant', 'class_context': False,
        'timeout_s': 3, 'fingerprint_components': {'interpreter': {
            'version': sys.version, 'executable': sys.executable, 'environment_sha256': 'environment'}}}}
    calls = []
    def native(current, **kwargs):
        calls.append(current)
        ex = current.comprehension['execute']
        assert kwargs['max_fix_rounds'] == 0 and kwargs['resume'] is False
        actual_prompt = Path(current.raw['files']['prompts_dir'])/'aideal/comprehension_write_exec.md'
        assert ('source-grounded diagnosis' in actual_prompt.read_text()) == (mode == 'source')
        assert 'old()' in ex['exec_hints'] if len(calls) == 1 else 'round 1' in ex['exec_hints']
        script = Path(ex['work_dir'])/'run_target/api_test.py'
        script.parent.mkdir(parents=True)
        script.write_text(f'# round {len(calls)}\ntarget()')
        return {'metrics': {'target': {'status': 'pass' if len(calls) == 2 else 'fail',
            'error_category': None if len(calls) == 2 else 'runtime', 'error': 'first failure'}}}
    monkeypatch.setattr(runner, 'comprehension_check', native)
    report = runner.run(cfg, cfg, result, 'target', mode, 'manifest', execute=True)
    assert report['status'] == 'recovered_native'
    assert len(list(tmp_path.rglob('api_test.py'))) == 2
    assert prompt.read_text() == original
    assert cfg.comprehension['execute'].get('work_dir') != calls[0].comprehension['execute']['work_dir']
    saved = json.loads(Path(report['report']).read_text())
    assert len(saved['rounds']) == 2 and saved['headline_credit'] is False
    assert diagnoses == (['target'] if mode == 'source' else [])
