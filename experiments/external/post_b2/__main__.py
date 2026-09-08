"""Low-priority, single-writer post-B2 queue with passive deadline reporting."""
import argparse
from datetime import datetime
import fcntl
import json
from pathlib import Path
import threading
import time

from experiments.external.recovery.engine import save
from .evidence import REPOSITORIES, TERMINAL, admission
from . import report, stage, source_retry
from .admission import slot


def isolated_paths(work, out, upstream, parent):
    paths = [Path(p).resolve() for p in (work, out, upstream)]
    for i, left in enumerate(paths):
        for right in paths[i + 1:]:
            if left == right or left in right.parents or right in left.parents:
                raise ValueError('work, output and upstream directories must be separate and non-nested')
    for prefix, relative, _ in REPOSITORIES.values():
        for cell in ('A1', 'A2', 'B2'):
            root = Path(parent).resolve() / f'{prefix}_{cell}'
            for path in paths[:2]:
                if root == path or root in path.parents or path in root.parents:
                    raise ValueError('extension writes overlap a native worktree')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--upstream', type=Path, required=True, help='existing pipeline_v2 report directory')
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--admit-until', required=True, help='ISO timestamp with UTC offset; no new APIs admitted later')
    parser.add_argument('--watch', action='store_true', help='enable automatic admission/execution; default is read-only preflight')
    args = parser.parse_args()
    cutoff = datetime.fromisoformat(args.admit_until)
    if cutoff.tzinfo is None:
        parser.error('--admit-until requires a timezone offset')
    isolated_paths(args.work, args.out, args.upstream, args.workspace_parent)
    stage.registered()
    if not args.watch:
        ready, blocked = admission(args.workspace_parent, args.upstream)
        print(json.dumps({'status': 'ready' if ready else 'waiting_repository',
                          'ready_repositories': list(ready), 'blocked': blocked,
                          'provider_calls': 0, 'native_writes': 0}, indent=2))
        return
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'observer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        status = {'state': 'waiting_repository', 'repositories': {}, 'max_parallel': 1,
                  'scheduling': 'independent repository admission; source retries do not depend on A1',
                  'admit_until': cutoff.isoformat(), 'source_implementation': stage.implementation()}
        stop = threading.Event()
        def observe():
            while not stop.is_set():
                try:
                    report.publish(args.out, args.upstream, args.workspace_parent, dict(status))
                except Exception as exc:
                    save(args.out / 'report_error.json', {'error': str(exc)})
                stop.wait(30)
        thread = threading.Thread(target=observe, name='passive-v3-report', daemon=True)
        thread.start()
        retry_file = args.out / 'source_retry_schedule.json'
        retry_after = json.loads(retry_file.read_text()) if retry_file.exists() else {}
        try:
            while True:
                if datetime.now(cutoff.tzinfo) >= cutoff:
                    status['state'] = 'deadline_admission_closed_partial_unless_all_terminal'
                    break
                ready, blocked = admission(args.workspace_parent, args.upstream)
                status['repositories'] = {repo: blocked.get(repo, 'priority complete') for repo in REPOSITORIES}
                if not ready:
                    status['state'] = 'waiting_repository'
                    time.sleep(30)
                    continue
                status['state'] = 'post_B2_recovery'
                terminal, progressed = not blocked, False
                for repo, info in ready.items():
                    if datetime.now(cutoff.tzinfo) >= cutoff:
                        terminal = False
                        break
                    out = args.out / repo
                    try:
                        state = stage.prepare(info, out)
                        with slot(args.upstream, f'{repo}:S_B2') as admitted:
                            if admitted:
                                progressed |= stage.one(info, args.work / repo, out, state)
                        save(out / 'comparison.json', stage.compare(info, state))
                        finished = all(row['status'] in TERMINAL for row in state['apis'].values())
                        terminal &= finished
                        status['repositories'][repo] = state['statuses']
                        if source_retry.needed(info):
                            terminal = False
                            if time.time() >= retry_after.get(repo, 0):
                                with slot(args.upstream, f'{repo}:S_A2_retry') as admitted:
                                    if admitted:
                                        try:
                                            result = source_retry.run(info, args.workspace_parent, args.upstream)
                                            status['repositories'][repo] = {'S_B2': state['statuses'], 'S_A2': result['statuses']}
                                            progressed = True
                                        except BlockingIOError:
                                            pass  # Original driver owns the source batch; no duplicate.
                                        finally:
                                            retry_after[repo] = time.time() + 300
                                            save(retry_file, retry_after)
                    except Exception as exc:
                        # A preflight/identity failure is evidence, never a new
                        # denominator or permission to bypass the gate.
                        terminal = False
                        status['repositories'][repo] = f'validation_blocked: {type(exc).__name__}: {exc}'
                        out.mkdir(parents=True, exist_ok=True)
                        save(out / 'blocker.json', {'error': status['repositories'][repo]})
                if terminal:
                    status['state'] = 'extension_settled_check_validation_blocks'
                    break
                if not progressed:
                    time.sleep(30)
        finally:
            stop.set()
            thread.join(timeout=60)
            if thread.is_alive():
                raise RuntimeError('report thread did not stop; preserve output ownership')
            report.publish(args.out, args.upstream, args.workspace_parent, status)
            save(args.out / 'scheduler_completion.json', status)


if __name__ == '__main__':
    main()
