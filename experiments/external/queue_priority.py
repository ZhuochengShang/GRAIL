"""Hold one launch supervisor, preserving its children, until a study finishes."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def identity(pid):
    result = subprocess.run(['ps', '-p', str(pid), '-o', 'lstart=', '-o', 'command='],
                            text=True, capture_output=True, check=False)
    parts = result.stdout.strip().split(maxsplit=5)
    if result.returncode or len(parts) != 6:
        raise ValueError(f'Supervisor {pid} is absent; do not signal a replacement')
    return {'started': ' '.join(parts[:5]), 'command': parts[5]}


def save(path, data):
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data, indent=2)+'\n')
    tmp.replace(path)


def prerequisite_complete(policy):
    state = json.loads(Path(policy['prerequisite_state']).read_text())
    if state.get('plan_sha256') != policy['prerequisite_plan_sha256']:
        raise ValueError('Prerequisite plan changed; inspect before releasing the queue')
    return all(state.get('jobs', {}).get(job, {}).get('status') == 'succeeded'
               for job in policy['required_jobs'])


def signal_supervisor(policy, sig):
    pid = policy['supervisor_pid']
    if identity(pid) != policy['supervisor_identity']:
        raise ValueError('Supervisor identity changed; refusing to signal a reused PID')
    os.kill(pid, sig)  # Deliberately only this PID, never its process group/children.


def run(policy, out, execute=False):
    out.mkdir(parents=True, exist_ok=True)
    command = policy['supervisor_identity']['command']
    if ('run_condition_watchdog.py' not in command or policy['supervisor_plan'] not in command
            or not policy['required_jobs']):
        raise ValueError('Only an identified launch supervisor with nonempty prerequisites may be held')
    if identity(policy['supervisor_pid']) != policy['supervisor_identity']:
        raise ValueError('Supervisor identity does not match registration')
    ready = prerequisite_complete(policy)
    if not execute:
        return {'preflight': 'passed', 'prerequisite_complete': ready, 'children_untouched': True}
    cancelled = False
    def cancel(*_):
        nonlocal cancelled
        cancelled = True
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, cancel)
    state = {'policy': policy, 'children_untouched': True,
             'policy_sha256': hashlib.sha256(json.dumps(policy, sort_keys=True).encode()).hexdigest()}
    with (out/'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while not cancelled:
            ready = prerequisite_complete(policy)
            if ready:
                break
            signal_supervisor(policy, signal.SIGSTOP)
            state.update(status='holding_new_launches', epoch=time.time(),
                         reason='RDPro A2, feedback, README repair and fresh B2 before new MDAnalysis stages')
            save(out/'status.json', state)
            time.sleep(5)
        signal_supervisor(policy, signal.SIGCONT)
        state.update(status='released' if ready else 'cancelled_and_released', epoch=time.time())
        save(out/'status.json', state)
        return state


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(json.loads(args.policy.read_text()), args.out, args.execute)), flush=True)
