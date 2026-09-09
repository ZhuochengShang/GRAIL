"""Passive RDPro status; native API outcomes, provider failures and repair rounds."""
from collections import Counter
from datetime import datetime
import html
import json
from pathlib import Path

from experiments.external.recovery.engine import save


def read(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def metrics(root, stage):
    result = read(root / f'docs/main_v5/{stage}.json')
    rows = result.get('metrics', {})
    if rows:
        return rows, 'Final artifact'
    ledger = root / f'.aideal_exec/{stage}/comprehension_progress.jsonl'
    rows = {}
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            name = row.get('api') or row.get('name')
            if name:
                rows[name] = row
    return rows, 'Checkpoint progress; not a completed evaluation'


def render(root, out, stage):
    out.mkdir(parents=True, exist_ok=True)
    b2root = root.parents[2] / 'AIDEAL_rdpro_v5_B2/project'
    tables, data = [], {'updated_at': datetime.now().astimezone().isoformat(), 'active_stage': stage}
    for label, current in [('A2', root), ('B2', b2root)]:
        rows, provenance = metrics(current, label)
        counts = Counter(('provider unresolved' if r.get('error_category') == 'llm-error'
                          else r.get('status', 'unknown')) for r in rows.values())
        data[label] = {'counts': dict(counts), 'recorded': len(rows), 'denominator': 161,
                       'provenance': provenance, 'apis': rows}
        tables.append(f'<tr><td>{label}</td><td>161</td><td>{len(rows)}</td><td>{counts["pass"]}</td><td>{counts["fail"]}</td><td>{counts["provider unresolved"]}</td></tr>')
    data['B2-1'] = read(out / 'feedback/summary.json')
    data['B2-2'] = read(b2root / 'docs/main_v5/docfix.json')
    save(out / 'status.json', data)
    detail = []
    for cell in ('A2', 'B2'):
        for name, row in data[cell]['apis'].items():
            detail.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in
                (cell, name, row.get('status'), row.get('error_category', ''), row.get('wall_s', ''), row.get('attempts', ''), row.get('error', '')) )+'</tr>')
    text = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="60"><title>RDPro matched main study</title><style>body{font:16px system-ui;margin:24px;background:#f4f7fc;color:#17263d}main{max-width:1200px;margin:auto}table{border-collapse:collapse;width:100%;background:white}td,th{padding:10px;border:1px solid #ccd5e0;text-align:left;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere}.scroll{overflow:auto}td:last-child{max-width:420px;overflow-wrap:anywhere}</style><main><h1>RDPro · new matched study</h1>'''
    text += '<p>Updated '+html.escape(data['updated_at'])+' · Stage: <strong>'+html.escape(stage)+'</strong></p>'
    text += '<p>A2 → independent B2-1 feedback snippet repairs / B2-2 source-informed README repairs → fresh B2. Five repair rounds maximum; stuck threshold two. Fresh A2 and B2 use zero snippet fixes.</p><p>Primary manifest: 161 validated public APIs (88 originally documented, 73 undocumented). Historical 171-entry scores remain separate. New native passes are not independent semantic validation.</p>'
    text += '<div class="scroll"><table><tr><th>Evaluation</th><th>APIs</th><th>Recorded</th><th>Pass</th><th>Execution failure</th><th>Provider unresolved</th></tr>'+''.join(tables)+'</table></div>'
    feedback = data['B2-1']
    text += '<h2>B2-1 · README + errors, snippet fixes</h2><pre>'+html.escape(json.dumps({k:feedback.get(k) for k in ('cohort_count','statuses','native_recovery_by_round','active_api')},indent=2))+'</pre>'
    doc = data['B2-2']
    text += '<h2>B2-2 · Source/tests + errors, README repairs</h2><pre>'+html.escape(json.dumps({k:doc.get(k) for k in ('attempted','processed','doc_fixed','blocked')},indent=2))+'</pre><p>Missing/null means no recorded outcome, not zero failures. Both branches start independently from the new frozen A2 failures.</p>'
    text += '<h2>Per-API outcomes and timing</h2><div class="scroll"><table><tr><th>Cell</th><th>API</th><th>Status</th><th>Category</th><th>Wall seconds</th><th>Attempts</th><th>Error</th></tr>'+''.join(detail)+'</table></div><p>Provider retries have a configured minimum 300-second cooldown; admission waits can make the observed interval longer; SDK attempts and snippet-fix rounds are distinct. Detailed attempt evidence remains in the linked stage files and feedback cases.</p></main>'
    (out/'index.html').write_text(text)
    return data
