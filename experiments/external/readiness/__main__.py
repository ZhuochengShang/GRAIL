"""Publish readiness reports or record explicit review decisions."""
import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import time

from experiments.external.audit_overnight import atomic, dump
from experiments.external.readiness.report import collect, publish
from experiments.external.readiness.review import history, record


@contextmanager
def locked(path, nonblocking=False):
    with path.open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0))
        yield


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-root', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    refresh = sub.add_parser('publish')
    refresh.add_argument('--watch', action='store_true')
    decision = sub.add_parser('review')
    decision.add_argument('--decision', type=Path, required=True)
    args = parser.parse_args()
    report = args.report_root.resolve()
    out = report/'data_validation/readiness'
    out.mkdir(parents=True, exist_ok=True)
    atomic(out/'.gitignore', 'observer.lock\npublish.lock\nheartbeat.json\nobserver.log\n')
    atomic(out/'WORKFLOW.md', Path(__file__).with_name('WORKFLOW.md').read_text())
    if args.command == 'review':
        payload = json.loads(args.decision.read_text())
        with locked(out/'publish.lock'):
            # Read fresh source ledgers, not a potentially stale generated card.
            _, cards, errors = collect(report)
            matches = [c for c in cards if c['id'] == payload.get('id')]
            if len(matches) != 1:
                raise ValueError(f'Suggestion is absent or evidence unavailable: {errors}')
            event = record(matches[0], history(out/'decisions.jsonl'), payload, out)
            publish(report)
        print(json.dumps({'recorded': event['action'], 'id': event['id']}))
        return
    with locked(out/'observer.lock', nonblocking=True):
        while True:
            try:
                with locked(out/'publish.lock'):
                    assessment, queue = publish(report)
                dump(out/'heartbeat.json', {'pid': os.getpid(), 'epoch': time.time(),
                    'status': 'ok' if not assessment['errors'] else 'partial_evidence', 'suggestions': len(queue['cards'])})
            except Exception as exc:
                dump(out/'heartbeat.json', {'pid': os.getpid(), 'epoch': time.time(), 'status': 'error', 'error': str(exc)})
                if not args.watch:
                    raise
            if not args.watch:
                return
            time.sleep(60)


if __name__ == '__main__':
    main()
