"""Separate native, recovery, replay and protocol-audit evidence in HTML/JSON."""
from collections import Counter
from datetime import datetime
import html
import hashlib
import json
from pathlib import Path
import re

from experiments.external.recovery.engine import save
from experiments.external.recovery.validation import file_sha
from .evidence import REPOSITORIES


def optional(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def document_audit(root):
    """Append-only stderr exposes restart rounds that the latest JSON can hide."""
    folder = Path(root) / 'docs/eval/B2'
    doc = optional(folder / 'docfix.json')
    path = folder / 'docfix_command.json.stderr.log'
    text = path.read_text(errors='replace') if path.exists() else ''
    starts = re.findall(r'\[docfix \d+/\d+\] (.+?) round (\d+)/5: deep-dive', text)
    counts = Counter(api for api, _ in starts)
    outcomes = re.findall(r'\[docfix \d+/\d+\] (.+?) round (\d+): (PASS|fail)', text)
    completed = Counter(api for api, _, _ in outcomes)
    handoff = optional(folder / 'A2_INPUT_HANDOFF.json')
    seeded = False
    if handoff:
        try:
            log = Path(handoff['error_log']).read_bytes()
            seeded = hashlib.sha256(log[:handoff['seed_bytes']]).hexdigest() == handoff['seed_sha256']
        except (OSError, KeyError):
            pass
    return {'report_present': bool(doc), 'attempted': doc.get('attempted'),
            'A2_error_seed_prefix_verified': seeded,
            'seeded_failure_count': handoff.get('seeded_failures'),
            'processed': doc.get('processed'), 'doc_round_starts_in_append_log': dict(counts),
            'validation_outcomes_in_append_log': dict(completed),
            'apis_with_more_than_five_round_starts': [api for api, n in counts.items() if n > 5],
            'apis_with_more_than_five_validation_outcomes': [api for api, n in completed.items() if n > 5],
            'stderr_sha256': file_sha(path) if path.exists() else None,
            'source_report': str(folder / 'docfix.json'),
            'limitations': ['Five doc rounds are configured per API invocation; unfinished APIs can restart. '
                           'Actual attempts and provider retries must be audited from the append log.',
                           'A2 error-log seed binding is reported separately; retained legacy snippet associations remain qualified.',
                           'Document repair can include infrastructure failures; source recovery excludes them.']}


def publish(out, upstream, parent, status):
    out, upstream, parent = Path(out), Path(upstream), Path(parent)
    now = datetime.now().astimezone().isoformat()
    entries, audits, table = {}, {}, []
    for repo, (prefix, relative, _) in REPOSITORIES.items():
        native = optional(upstream / repo / 'live.json')
        source = optional(upstream / repo / 'source/summary.json')
        post = optional(out / repo / 'summary.json')
        comparison = optional(out / repo / 'comparison.json')
        entries[repo] = {'native_v2': native, 'S_A2': source, 'S_B2': post, 'comparison': comparison}
        audits[repo] = document_audit(parent / f'{prefix}_B2' / relative)
        for cell in ('A1', 'A2', 'B2'):
            row = native.get('cells', {}).get(cell, {})
            table.append([repo, cell, row.get('state', 'pending'),
                          str(row.get('pass', '—')), str(row.get('api_outcomes', '—'))])
        for label, data in [('S_A2', source), ('S_B2', post)]:
            rows = data.get('apis')
            n = len(rows) if rows is not None else '—'
            count = sum(r['status'] == 'recovered_native' for r in rows.values()) if rows is not None else '—'
            label_status = str(data.get('statuses') or status.get('repositories', {}).get(repo, 'pending'))
            table.append([repo, label, label_status, str(count), str(n)])
    payload = {'protocol': 'aideal-separated-recovery-v3', 'updated_at': now,
               'scheduler': status, 'repositories': entries, 'document_protocol_audit': audits,
               'interpretation': 'Native scores, conditional recovery and replay are separate. '
                   'No semantic certification, equal-cost causal estimate or retrospective preregistration.'}
    save(out / 'live.json', payload)
    lines = ['# AIDEAL: three separate stages', '', now, '',
             'A1/A2 are zero-fix controls. S_A2 repairs snippets from A2 failures. '
             'Independent README repair produces fresh zero-fix B2. S_B2 repairs only eligible B2 failures.', '',
             '| Repository | Measurement | State | Native pass/recovered | Denominator |',
             '|---|---|---|---:|---:|']
    lines += ['| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |' for row in table]
    lines += ['', 'Denominators: A1/A2/B2 use the full manifest; S_A2 and S_B2 use different frozen eligible-failure cohorts.',
              'The composite B2 + S_B2 endpoint is never reported as the native B2 score.', '',
              '[Exact protocol and diagram](PIPELINE_V3.md) · [Report template](REPORT_TEMPLATE_V3.md) · '
              '[Full evidence JSON](live.json) · [Data/API methods](../FINAL_REPORT_DATA_AND_API_METHODS.md) · '
              '[Independent assertion replay](../assertion_replay/REPLAY.html)', '',
              'Method limitations: single adaptive run; no equal-cost randomized comparison. '
              'Legacy document retries can restart an unfinished API; A2 error-log seed binding is audited per repository. '
              'See document_protocol_audit in JSON for observed round counts. Native passes still require semantic review.']
    (out / 'STATUS.md').write_text('\n'.join(lines) + '\n')
    body = ''.join('<tr>' + ''.join('<td>' + html.escape(str(x)) + '</td>' for x in row) + '</tr>' for row in table)
    blocks = ''.join('<article><h3>' + title + '</h3><p>' + text + '</p></article>' for title, text in [
        ('1 · S_A2', 'Frozen A2 failures → source/tests diagnosis → up to 5 snippet proposals. Generated README stays fixed.'),
        ('2 · README → B2', 'Independent A2 failure selection → up to 5 configured doc rounds → fresh full-manifest, zero-fix B2.'),
        ('3 · S_B2', 'Freeze eligible B2 failures → new source/tests diagnosis → up to 5 snippet proposals. Rewritten README stays fixed.')])
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
            'content="width=device-width,initial-scale=1"><title>AIDEAL separated stages</title><style>'
            'body{font:16px system-ui;max-width:1200px;margin:32px auto;padding:0 20px;color:#18394c;background:#f3f7fa}'
            '.flow{display:flex;gap:16px;flex-wrap:wrap}article{flex:1;min-width:240px;background:white;padding:18px;'
            'border-top:5px solid #087f86;border-radius:10px}table{border-collapse:collapse;width:100%;background:white}'
            'th,td{padding:12px;text-align:left;border-bottom:1px solid #cbd5dc}aside{background:#fff0d8;padding:18px;'
            'margin:20px 0}a{color:#006a73}.table{overflow:auto}</style></head><body><h1>AIDEAL · three separate stages</h1>'
            f'<p>{now}</p><p>A1: original README, zero fixes. A2: generated README, zero fixes. Original-README repair is omitted.</p>'
            f'<div class="flow">{blocks}</div><aside>S_A2 and S_B2 have different failure denominators. '
            'B2 remains a fresh-reader score; B2 + S_B2 is a separate composite. Native pass does not certify correctness.</aside>'
            '<h2>Live outcomes</h2><div class="table"><table><thead><tr><th>Repository</th><th>Measurement</th><th>State</th>'
            f'<th>Pass/recovered</th><th>Denominator</th></tr></thead><tbody>{body}</tbody></table></div>'
            '<h2>Method audit</h2><p>The existing document loop can restart unfinished APIs; actual round starts and validation '
            'outcomes are audited from append-only logs. A2 error-log seed hashes are checked per repository. '
            'This is an adaptively amended study, not a preregistered equal-cost trial.</p><p>'
            '<a href="PIPELINE_V3.md">Design and code map</a> · <a href="REPORT_TEMPLATE_V3.md">Detailed report template</a> · '
            '<a href="live.json">Evidence and round audit</a> · <a href="../assertion_replay/REPLAY.html">Independent replay</a>'
            '</p></body></html>')
    (out / 'REPORT.html').write_text(page)
