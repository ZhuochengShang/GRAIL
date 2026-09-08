import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

import pytest

from aideal.execution import run_command, CleanupError
from aideal.doc_checks import _classify_error_py
from aideal.experiment_identity import extra_components, write_run_identity, digest_native
from aideal.config import load_config


def config(tmp_path):
    path = tmp_path / 'configs/aideal.yaml'
    path.parent.mkdir()
    path.write_text('project: {name: example, language: Python}\n')
    return load_config(path)


def test_prompt_profile_and_transport_changes_invalidate_identity(tmp_path, monkeypatch):
    cfg = config(tmp_path)
    original = extra_components(cfg)
    prompt = tmp_path / 'prompts/aideal/comprehension_write_exec.md'
    prompt.parent.mkdir(parents=True)
    prompt.write_text('SYSTEM: changed\nUSER: {api_body}\n')
    changed = extra_components(cfg)
    assert changed['prompt_contract'] != original['prompt_contract']
    profile = tmp_path / 'configs/project_profile.yaml'
    profile.write_text('role: changed\n')
    assert extra_components(cfg)['prompt_contract'] != changed['prompt_contract']
    monkeypatch.setenv('AIDEAL_GOOGLE_REQUEST_TIMEOUT_S', '600')
    monkeypatch.setenv('AIDEAL_GOOGLE_MAX_RETRIES', '1')
    assert extra_components(cfg)['transport_contract'] != original['transport_contract']


def test_published_identity_binds_components(tmp_path):
    parts = {'schema': 4, 'prompt_contract': {'profile': 'hash'}}
    path = tmp_path / 'run_identity.json'
    write_run_identity(path, parts)
    row = json.loads(path.read_text())
    assert row['experiment_fingerprint'] == digest_native(parts)


@pytest.mark.skipif(os.name != 'posix', reason='POSIX process-group implementation')
def test_timeout_kills_child_even_if_parent_shell_exits(tmp_path):
    marker = tmp_path / 'survived'
    child = f'import time; from pathlib import Path; time.sleep(.8); Path({str(marker)!r}).write_text("bad")'
    command = shlex.join([sys.executable, '-c', child]) + '; :'
    try:
        with pytest.raises(subprocess.TimeoutExpired) as caught:
            run_command(command, cwd=tmp_path, env=os.environ.copy(), timeout=.05)
    except CleanupError as error:
        if isinstance(error.__cause__, PermissionError):
            pytest.skip('Host denies process-group signals; real descendant cleanup remains unverified')
        raise
    assert caught.value.cleanup['shell_reaped']
    time.sleep(.9)
    assert not marker.exists()


def test_process_output_and_failure_exit_are_preserved(tmp_path):
    command = shlex.join([sys.executable, '-c', 'import sys; print("witness"); sys.exit(3)'])
    result = run_command(command, cwd=tmp_path, env=os.environ.copy(), timeout=5)
    assert result.returncode == 3 and result.stdout.strip() == 'witness'


def test_missing_symbol_is_not_excluded_as_missing_environment():
    assert _classify_error_py("ImportError: cannot import name 'missing' from 'installed'", 1, '')[0] == 'api-import'
    assert _classify_error_py("ModuleNotFoundError: No module named 'optional_dependency'", 1, '')[0] == 'infra'


def test_timeout_requests_both_group_signals_and_reaps(monkeypatch, tmp_path):
    from unittest.mock import Mock
    import signal
    proc = Mock(pid=42, returncode=-15)
    proc.communicate.side_effect = [subprocess.TimeoutExpired('test', 1), ('out', 'err')]
    monkeypatch.setattr(subprocess, 'Popen', Mock(return_value=proc))
    signals = Mock()
    monkeypatch.setattr(os, 'killpg', signals)
    with pytest.raises(subprocess.TimeoutExpired) as caught:
        run_command('test', cwd=tmp_path, env={}, timeout=1)
    assert [call.args for call in signals.call_args_list] == [(42, signal.SIGTERM), (42, signal.SIGKILL)]
    assert caught.value.cleanup['shell_reaped']
    assert caught.value.output == 'out'


def test_denied_cleanup_is_not_a_normal_api_failure(monkeypatch, tmp_path):
    from unittest.mock import Mock
    proc = Mock(pid=42, returncode=0)
    proc.communicate.side_effect = [subprocess.TimeoutExpired('test', 1), ('', '')]
    monkeypatch.setattr(subprocess, 'Popen', Mock(return_value=proc))
    monkeypatch.setattr(os, 'killpg', Mock(side_effect=PermissionError('denied')))
    with pytest.raises(CleanupError, match='do not resume'):
        run_command('test', cwd=tmp_path, env={}, timeout=1)
    with pytest.raises(CleanupError, match='execution blocked'):
        run_command('another test', cwd=tmp_path, env={}, timeout=1)
    assert subprocess.Popen.call_count == 1


def test_native_writer_lock_rejects_same_root_and_allows_isolation(tmp_path):
    from types import SimpleNamespace
    from aideal.execution import exclusive_work_dir
    cfg = SimpleNamespace(root=tmp_path, comprehension={'execute': {'work_dir': 'A2'}})
    other = SimpleNamespace(root=tmp_path, comprehension={'execute': {'work_dir': 'B2'}})
    calls = []
    @exclusive_work_dir
    def reader(config):
        calls.append(config)
    @exclusive_work_dir
    def owner(config):
        with pytest.raises(BlockingIOError):
            reader(config)
        reader(other)
    owner(cfg)
    assert calls == [other]
    reader(cfg)
    assert calls == [other, cfg]
    (tmp_path/'A2/.aideal_unreconciled_process.json').write_text('{}')
    with pytest.raises(CleanupError, match='before model work'):
        reader(cfg)
    assert len(calls) == 2
