"""Publish the agreed main-plan table, independently of legacy dashboard observers."""
import argparse
from datetime import datetime
import fcntl
import json
from pathlib import Path
import time

from experiments.external.study_dashboard.__main__ import atomic
from experiments.external.study_dashboard.details_data import Reader


def collect(root):
    reader = Reader()
    audit = reader.read(Path(__file__).with_name('REUSE_AUDIT_2026-09-08.json'))
    rows = []
    for slug in ('mir_eval', 'thumbnailator', 'tslearn', 'mdanalysis'):
        detail = reader.read(root.parent / f'study_dashboard_v1/details/{slug}.json')
        feedback = reader.read(root / slug / 'summary.json', optional=True)
        cases = {}
        for name, row in (feedback or {}).get('apis', {}).items():
            path = row.get('evidence_file')
            if path:
                cases[name] = reader.read(root / slug / path)
        native = {}
        for cell in ('A1', 'A2', 'B2'):
            metrics = [r['native'][cell]['metric'] for r in detail['rows']]
            native[cell] = {'recorded': sum(bool(m.get('status')) for m in metrics),
                'pass': sum(m.get('status') == 'pass' for m in metrics),
                'provider': sum(m.get('error_category') == 'llm-error' for m in metrics)}
        rows.append({'slug': slug, 'repository': detail['repository'], 'N': detail['expected'],
            'native': native, 'doc': detail['doc'], 'feedback': feedback, 'cases': cases,
            'detail_time': detail['updated_at'], 'validation': detail['derived']['validation_outcomes']})
    return {'updated_at': datetime.now().astimezone().isoformat(), 'rows': rows,
            'audit': audit, 'sources': reader.sources}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--out', type=Path, help='separate passive observer namespace')
    p.add_argument('--watch', action='store_true')
    args = p.parse_args()
    out = args.out or args.root / 'report'
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            try:
                data = collect(args.root)
                encoded = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
                page = Path(__file__).with_name('report.html').read_text().replace('__DATA__', encoded)
                atomic(out / 'data.json', json.dumps(data, ensure_ascii=False)+'\n')
                atomic(out / 'index.html', page)
                atomic(out / 'heartbeat.json', json.dumps({'epoch': time.time(), 'status': 'ok'}))
            except Exception as exc:
                atomic(out / 'heartbeat.json', json.dumps({'epoch': time.time(), 'status': 'error', 'error': str(exc)}))
                if not args.watch:
                    raise
            if not args.watch:
                break
            time.sleep(30)


if __name__ == '__main__':
    main()
