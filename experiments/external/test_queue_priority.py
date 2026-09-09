import json
import signal

import pytest

from experiments.external import queue_priority as queue


def policy(tmp_path):
    state = tmp_path/'rdpro.state.json'
    state.write_text(json.dumps({'plan_sha256': 'frozen', 'jobs': {
        'A2': {'status': 'succeeded'}, 'feedback': {'status': 'succeeded'},
        'repair': {'status': 'succeeded'}, 'B2': {'status': 'pending'}}}))
    return {'supervisor_pid': 123, 'supervisor_identity': {
        'started': 'fixed', 'command': 'python run_condition_watchdog.py /md/plan.yaml'},
        'supervisor_plan': '/md/plan.yaml', 'prerequisite_state': str(state),
        'prerequisite_plan_sha256': 'frozen', 'required_jobs': ['A2', 'feedback', 'repair', 'B2']}


def test_release_requires_every_stage_and_matching_plan(tmp_path):
    p = policy(tmp_path)
    assert not queue.prerequisite_complete(p)
    state = json.loads(open(p['prerequisite_state']).read())
    state['jobs']['B2']['status'] = 'succeeded'
    open(p['prerequisite_state'], 'w').write(json.dumps(state))
    assert queue.prerequisite_complete(p)
    p['prerequisite_plan_sha256'] = 'changed'
    with pytest.raises(ValueError, match='plan changed'):
        queue.prerequisite_complete(p)


def test_signals_only_registered_supervisor_and_rejects_pid_reuse(tmp_path, monkeypatch):
    p = policy(tmp_path)
    sent = []
    monkeypatch.setattr(queue.os, 'kill', lambda *args: sent.append(args))
    monkeypatch.setattr(queue, 'identity', lambda pid: p['supervisor_identity'])
    queue.signal_supervisor(p, signal.SIGSTOP)
    assert sent == [(123, signal.SIGSTOP)]
    monkeypatch.setattr(queue, 'identity', lambda pid: {'started': 'new process'})
    with pytest.raises(ValueError, match='reused PID'):
        queue.signal_supervisor(p, signal.SIGCONT)
    assert len(sent) == 1


def test_preflight_does_not_signal(tmp_path, monkeypatch):
    p = policy(tmp_path)
    monkeypatch.setattr(queue, 'identity', lambda pid: p['supervisor_identity'])
    monkeypatch.setattr(queue.os, 'kill', lambda *args: pytest.fail('preflight signalled a process'))
    assert queue.run(p, tmp_path/'out')['preflight'] == 'passed'


def test_hold_then_automatic_resume(tmp_path, monkeypatch):
    p = policy(tmp_path)
    sent = []
    monkeypatch.setattr(queue, 'identity', lambda pid: p['supervisor_identity'])
    monkeypatch.setattr(queue.os, 'kill', lambda *args: sent.append(args))
    monkeypatch.setattr(queue.signal, 'signal', lambda *args: None)
    def finish(_):
        state = json.loads(open(p['prerequisite_state']).read())
        state['jobs']['B2']['status'] = 'succeeded'
        open(p['prerequisite_state'], 'w').write(json.dumps(state))
    monkeypatch.setattr(queue.time, 'sleep', finish)
    assert queue.run(p, tmp_path/'out', execute=True)['status'] == 'released'
    assert sent == [(123, signal.SIGSTOP), (123, signal.SIGCONT)]
