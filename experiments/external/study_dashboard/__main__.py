"""Publish an offline HTML/JSON dashboard; optional passive 60-second refresh."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import time

from .data import collect


def atomic(path, text):
    temporary = path.with_name(path.name + f'.{os.getpid()}.tmp')
    temporary.write_text(text)
    temporary.replace(path)


def publish(parent, out):
    data = collect(parent)
    embedded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    page = Path(__file__).with_name('dashboard.html').read_text().replace('__STUDY_DATA__', embedded).replace(
        '__LESSONS__', Path(__file__).with_name('lessons.html').read_text())
    atomic(out/'data.json', json.dumps(data, indent=2)+'\n')
    atomic(out/'index.html', page)
    atomic(out/'heartbeat.json', json.dumps({'epoch': time.time(), 'pid': os.getpid(), 'status': 'ok',
                                          'updated_at': data['updated_at']})+'\n')
    return data['updated_at']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out/'dashboard.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            try:
                print(publish(args.workspace_parent, args.out), flush=True)
            except Exception as exc:
                atomic(args.out/'heartbeat.json', json.dumps({'epoch': time.time(), 'pid': os.getpid(),
                    'status': 'error', 'error': f'{type(exc).__name__}: {exc}'})+'\n')
                if not args.watch:
                    raise
            if not args.watch:
                break
            time.sleep(60)


if __name__ == '__main__':
    main()
