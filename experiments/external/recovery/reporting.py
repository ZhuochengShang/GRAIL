"""Live v2 reporting; omitted B1 never masquerades as an unfinished experiment."""
from collections import Counter
from datetime import datetime
import html
import json
from pathlib import Path
import threading

from experiments.external.assertion_replay.evidence import collect
from .engine import save


def read(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def publish(repo, parent, prefix, relative, out):
    cells = {}
    for cell in ('A1', 'A2', 'B2'):
        root = parent / f'{prefix}_{cell}' / relative
        snapshot = collect(root, cell) if root.exists() else None
        if snapshot:
            rows = snapshot['rows']
            cells[cell] = {'state': 'native complete' if snapshot['complete'] else 'native partial',
                'api_outcomes': len(rows), 'pass': sum(r['status'] == 'pass' for r in rows.values()),
                'failures': dict(Counter(r.get('error_category') or 'unknown'
                    for r in rows.values() if r['status'] != 'pass')),
                'source_path': snapshot['source_path'], 'source_sha256': snapshot['source_sha256']}
        else:
            cells[cell] = {'state': 'pending native evidence'}
    source = read(out / 'source/summary.json')
    doc = read(parent / f'{prefix}_B2' / relative / 'docs/eval/B2/docfix.json')
    # Preserve native structures: document rounds are not code-fix rounds.
    state = {'protocol': 'aideal-a2-repair-v2', 'repo': repo,
        'updated_at': datetime.now().astimezone().isoformat(),
        'B1': 'omitted by user; original README has no repair loop',
        'cells': cells, 'source_recovery': source,
        'document_repair': {k: doc.get(k) for k in ('attempted', 'processed', 'blocked')},
        'interpretation': 'generation effect A2-A1; documentation transfer B2-A2; source recovery has a fixed A2-failure denominator'}
    save(out / 'live.json', state)
    rows = []
    for cell, value in cells.items():
        rows.append([cell, value['state'], str(value.get('pass', '—')),
                     str(value.get('api_outcomes', '—')), str(value.get('failures', {}))])
    text = ['# ' + repo + ' · A2-only repair pipeline', '', state['updated_at'], '',
        'A1 original README → zero fixes. A2 generated README → zero fixes.',
        'Frozen A2 failures → source-only snippet repair; independently → generated-README repair → fresh B2.',
        'Original-README repair (historical B1) is intentionally omitted.', '',
        '| Cell | State | Native pass | API outcomes | Failure categories |', '|---|---|---:|---:|---|']
    text += ['| ' + ' | '.join(row) + ' |' for row in rows]
    text += ['', 'Source recovery by new code-fix round: ' + str(source.get('native_recovery_by_round', 'pending')),
        'Source statuses: ' + str(source.get('statuses', 'pending')),
        'Document repair: ' + str(state['document_repair']), '',
        '[Source round details](source/REPORT.md) · [Machine-readable live evidence](live.json)', '',
        'A2 is round zero; at most five new snippet proposals; stuck threshold two. '
        'B2 has at most five document rewrite rounds and a fresh zero-code-fix full-manifest evaluation.',
        'Provider events, native acceptance, independent replay and semantic validation are separate. '
        'A passing generated assertion is not by itself independent proof of correctness.']
    (out / 'STATUS.md').write_text('\n'.join(text) + '\n')
    table = ''.join('<tr>' + ''.join('<td>' + html.escape(x) + '</td>' for x in row) + '</tr>' for row in rows)
    bars = ''.join(f'<tr><td>{n}</td><td>{count}</td></tr>'
                   for n, count in source.get('native_recovery_by_round', {}).items())
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AIDEAL A2 repair</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 24px;background:#f4f7fa;color:#19324b}table{border-collapse:collapse;background:white;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #ddd}.flow{display:flex;gap:16px;flex-wrap:wrap}article{background:white;padding:20px;border-radius:12px;border-top:5px solid #007e87;flex:1;min-width:220px}aside{padding:20px;background:#fff0d7;margin:20px 0}a{color:#006978}</style>
<h1>__REPO__ · A2-only repair</h1><p>__DATE__</p><div class="flow"><article><b>A1 · Control</b><p>Original README<br>Zero code fixes<br>No document repair</p></article><article><b>A2 · Baseline</b><p>Generated README<br>Zero code fixes<br>Freeze failure cohort</p></article><article><b>A2 → Source recovery</b><p>Source diagnosis + snippet fixes<br>Rounds 1–5, stuck at 2<br>README stays frozen</p></article><article><b>A2 → B2</b><p>Source-informed README rewrites<br>Up to 5 document rounds<br>Fresh reader; zero code fixes</p></article></div>
<aside>Historical B1 is omitted, not pending. Native source recovery and B2 fresh-reader transfer measure different outcomes. Independent assertion/data/API review is still required.</aside>
<h2>Native results</h2><table><tr><th>Cell</th><th>State</th><th>Pass</th><th>API outcomes</th><th>Failures</th></tr>__ROWS__</table>
<h2>Cumulative native source recovery by round</h2><table><tr><th>New code round</th><th>Recovered A2 failures</th></tr>__BARS__</table>
<p><a href="STATUS.md">Status memo</a> · <a href="source/REPORT.md">Per-API round histories</a> · <a href="live.json">Evidence JSON</a> · <a href="../../assertion_replay/REPLAY.html">Independent Thumbnailator replay</a></p></html>'''
    page = page.replace('__REPO__', html.escape(repo)).replace('__DATE__', state['updated_at'])
    (out / 'REPORT.html').write_text(page.replace('__ROWS__', table).replace('__BARS__', bars))


def start(repo, setup, prefix, relative, out):
    stop = threading.Event()
    def loop():
        while not stop.is_set():
            try:
                publish(repo, setup.parent, prefix, relative, out)
            except Exception as exc:
                save(out / 'report_error.json', {'error': str(exc)})
            stop.wait(30)
    thread = threading.Thread(target=loop, name='passive-v2-report', daemon=True)
    thread.start()
    return stop, thread
