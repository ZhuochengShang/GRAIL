import hashlib
import json

import pytest
import yaml

from experiments.external import watchdog_adoption as a
from experiments.external.run_condition_watchdog import Supervisor


def process(pid, ppid=1, started='original', command='python driver.py'):
    return dict(pid=pid, ppid=ppid, started=started, command=command, state='S')


def test_adoption_tracks_detached_descendants_and_pid_reuse(monkeypatch):
    table = {10: process(10), 20: process(20, 10, command='python worker.py')}
    monkeypatch.setattr(a, 'process_table', lambda: table)
    proc = a.adopt({'pid': 10}, ['python', 'driver.py'])
    assert proc and len(proc.tracked) == 2
    table.pop(10)
    table[20]['ppid'] = 1
    assert proc.poll() is None  # parent died; independently sessioned child is alive
    table[20]['started'] = 'reused PID'
    assert proc.poll() == 255  # never invent a successful exit status


def test_adoption_fails_closed_on_wrong_identity_or_ps_error(monkeypatch):
    monkeypatch.setattr(a, 'process_table', lambda: {10: process(10, command='other')})
    with pytest.raises(RuntimeError, match='identity differs'):
        a.adopt({'pid': 10}, ['python', 'driver.py'])
    def denied():
        raise PermissionError('process inspection unavailable')
    monkeypatch.setattr(a, 'process_table', denied)
    with pytest.raises(PermissionError):
        a.adopt({'pid': 10}, ['python', 'driver.py'])


def test_supervisor_preserves_live_attempt_and_never_signals_adopted_job(tmp_path, monkeypatch):
    monkeypatch.setattr(a, 'process_table', lambda: {10: process(10)})
    path = tmp_path/'plan.yaml'
    path.write_text(yaml.safe_dump({'jobs': [{'id': 'job', 'cwd': str(tmp_path),
                                           'command': ['python', 'driver.py']}]}))
    path.with_suffix('.state.json').write_text(json.dumps({
        'plan_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'jobs': {'job': {'status': 'running', 'pid': 10, 'attempts': 4}}}))
    supervisor = Supervisor(path)
    assert supervisor.state['jobs']['job']['status'] == 'running'
    assert supervisor.state['jobs']['job']['attempts'] == 4
    assert not supervisor.eligible('job', 0)
    def forbidden(*args):
        pytest.fail('must not signal adopted worker')
    monkeypatch.setattr('os.killpg', forbidden)
    supervisor.stop()
    assert supervisor.state['jobs']['job']['status'] == 'running'


def test_supervisor_environment_is_stable_during_isolated_recovery(tmp_path, monkeypatch):
    monkeypatch.setenv('AIDEAL_ENV_FINGERPRINT', 'baseline-inventory')
    path = tmp_path/'plan.yaml'
    path.write_text(yaml.safe_dump({'jobs': [{'id': 'job', 'cwd': str(tmp_path),
                                           'command': ['python', 'driver.py']}]}))
    supervisor = Supervisor(path)
    monkeypatch.setenv('AIDEAL_ENV_FINGERPRINT', 'another-thread-recovery')
    assert supervisor.env(supervisor.jobs['job'])['AIDEAL_ENV_FINGERPRINT'] == 'baseline-inventory'
