"""Read separate native, document-validation and recovery evidence for drill-downs."""
from collections import Counter
from datetime import datetime
import hashlib
import difflib
import json
from pathlib import Path

from aideal.readme_agent import parse_readme
from .data import REPOS
from .review_notes import NOTES, evidence_key


class Reader:
    def __init__(self):
        self.sources = {}

    def read(self, path, *, optional=False, text=False):
        path = Path(path)
        if optional and not path.exists():
            return '' if text else None
        raw = path.read_bytes()
        self.sources[str(path)] = hashlib.sha256(raw).hexdigest()
        return raw.decode(errors='replace') if text else json.loads(raw)


def source_cases(reader, folder):
    summary = reader.read(folder / 'summary.json', optional=True)
    if summary is None:
        return {'summary': None, 'cases': {}}
    cases = {}
    for api, row in summary.get('apis', {}).items():
        path = folder / row['evidence_file'] if row.get('evidence_file') else None
        if path:
            cases[api] = reader.read(path, optional=True)
    return {'summary': summary, 'cases': cases}


def document_entries(reader, path):
    if not path.exists():
        return {}
    reader.read(path, text=True)
    return {entry.name: entry.body for entry in parse_readme(path)}


def saved_snippet(run, name):
    """Resumed rows can retain only a status string, not the original snippet."""
    detail = run.get('details', {}).get(name)
    return detail.get('code') if isinstance(detail, dict) else None


def derived(rows, doc):
    apis = (doc or {}).get('apis', {})
    rounds = [r for api in apis.values() for r in api.get('doc_rounds', [])]
    validation = Counter(r.get('retry_status', 'no validation outcome recorded') for r in rounds)
    retained = {name for name, row in apis.items() if row.get('status') == 'doc-fixed'}
    gained, lost, retained_failed = [], [], []
    paired = 0
    for row in rows:
        a2, b2 = (row['native'].get(c, {}).get('metric', {}) for c in ('A2', 'B2'))
        comparable = all(m.get('status') in ('pass', 'fail') and m.get('error_category') != 'llm-error' for m in (a2, b2))
        paired += int(comparable)
        if comparable and a2.get('status') == 'fail' and b2.get('status') == 'pass':
            gained.append(row['api'])
        if comparable and a2.get('status') == 'pass' and b2.get('status') == 'fail':
            lost.append(row['api'])
        if row['api'] in retained and b2.get('status') == 'fail' and b2.get('error_category') != 'llm-error':
            retained_failed.append(row['api'])
    return {'paired_A2_B2_outcomes': paired, 'document_round_records': len(rounds), 'validation_outcomes': dict(validation),
            'retained_entries': len(retained), 'A2_fail_B2_pass': gained,
            'A2_pass_B2_fail': lost, 'retained_entry_B2_fail': retained_failed}


def priority(parent, repo, native_snapshot, coverage):
    reader = Reader()
    prefix, relative = REPOS[repo]
    audit = parent / 'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation'
    roots = {c: parent / f'{prefix}_{c}' / relative for c in ('A1', 'A2', 'B2')}
    runs = {c: reader.read(root / f'docs/eval/{c}/comprehension.json', optional=True)
            for c, root in roots.items()}
    doc = reader.read(roots['B2'] / 'docs/eval/B2/docfix.json')
    sa = source_cases(reader, audit / 'pipeline_v2' / repo.lower() / 'source')
    sb_dir = audit / 'pipeline_v3_inventory_retry' / repo.lower()
    sb = source_cases(reader, sb_dir if (sb_dir / 'summary.json').exists()
                      else audit / 'pipeline_v3' / repo.lower())
    documents = {c: document_entries(reader, roots[c] / f'docs/eval/{c}/LLM_readme.md')
                 for c in ('A2', 'B2')}
    cohort = next(r for r in coverage['records'] if r['repository'] == repo)
    rows = []
    timings = {(r['cell'], r['api']): r for r in native_snapshot['timings'] if r['repository'] == repo}
    for name in cohort['manifest']:
        native = {}
        for cell in roots:
            timing = timings.get((cell, name))
            record = reader.read(audit / 'provider_operations_v4' / timing['details']) if timing else None
            run = runs[cell] or {}
            bound = bool(record and record.get('source_sha256') == reader.sources.get(record.get('source_path')))
            native[cell] = {'metric': record.get('native_row', {}) if record else {},
                'timing': timing, 'attempt_evidence': record,
                'saved_snippet': saved_snippet(run, name) if bound else None,
                'snippet_binding': 'bound to recorded source artifact' if bound else 'not bound to current row; not substituted from another run'}
        repair = doc.get('apis', {}).get(name)
        reports = {}
        for round_record in (repair or {}).get('doc_rounds', []):
            report = (round_record.get('deep_dive') or {}).get('report')
            if report and report not in reports:
                reports[report] = reader.read(report, optional=True, text=True)
        rows.append({'api': name, 'native': native, 'repair': repair,
            'readme_before': documents['A2'].get(name), 'readme_after': documents['B2'].get(name),
            'readme_diff': '\n'.join(difflib.unified_diff(documents['A2'].get(name, '').splitlines(), documents['B2'].get(name, '').splitlines(), fromfile='A2 generated entry', tofile='B2 repaired entry', lineterm='')),
            'deep_dive_reports': reports,
            'S_A2': sa['cases'].get(name) or (sa['summary'] or {}).get('apis', {}).get(name),
            'S_B2': sb['cases'].get(name) or (sb['summary'] or {}).get('apis', {}).get(name)})
    bindings = reader.read(Path(__file__).with_name('review_bindings.json'))
    for row in rows:
        note = NOTES.get(repo, {}).get(row['api'])
        if note:
            row['review'] = {'category': note[0], 'finding': note[1], 'suggestion': note[2],
                'evidence_matches_review': bindings[repo][row['api']] == evidence_key(row),
                'scope': 'Inspection of retained evidence; no new replay or source modification'}
    replay = reader.read(audit / 'assertion_replay/summary.json') if repo == 'Thumbnailator' else None
    return {'repository': repo, 'scope': 'Current separated-stage study', 'expected': len(rows),
        'updated_at': datetime.now().astimezone().isoformat(), 'rows': rows,
        'doc': {k: v for k, v in doc.items() if k != 'apis'},
        'source_summaries': {'S_A2': sa['summary'], 'S_B2': sb['summary']},
        'run_contracts': {c: (run or {}).get('run') for c, run in runs.items()},
        'coverage': cohort, 'derived': derived(rows, doc), 'sources': reader.sources, 'assertion_replay': replay,
        'limitations': ['Native acceptance is not independent semantic certification.',
            'Historical document-round diagnosis/error fields may be excerpts; missing intermediate README versions and timings are not reconstructed.',
            'A retained deep-dive file can have been overwritten by a later round; its current bytes are not certified as every referenced round’s original text.',
            'Provider attempts, document rounds and snippet-fix rounds are separate counters. Retained histories may not cover all earlier attempts.']}


def mdanalysis(parent):
    reader = Reader()
    out = parent / 'AIDEAL_mdanalysis_v4'
    registration = reader.read(out / 'registration.json')
    state = reader.read(out / 'study_watchdog.state.json')
    roots = {c: Path(r['root']) for c, r in registration['cells'].items()}
    manifest = reader.read(roots['A2'] / 'docs/full_1032/api_manifest.json')['apis']
    runs, metrics = {}, {}
    for cell, root in roots.items():
        run = reader.read(root / f'docs/full_1032/{cell}/comprehension.json', optional=True)
        runs[cell] = run or {}
        metrics[cell] = (run or {}).get('metrics', {})
        checkpoint = root / f'.aideal_exec/full_1032/{cell}/comprehension_progress.jsonl'
        if not run and checkpoint.exists():
            lines = reader.read(checkpoint, text=True).splitlines()
            events = []
            for i, line in enumerate(lines):
                try:
                    events.append(json.loads(line))
                except ValueError:
                    if i != len(lines)-1:
                        raise
            if len({r.get('experiment_fingerprint') for r in events}) > 1:
                raise ValueError('MDAnalysis checkpoint identities differ')
            metrics[cell] = {r['name']: r for r in events}
    doc = reader.read(roots['B2'] / 'docs/full_1032/B2/docfix.json', optional=True)
    source = {stage: source_cases(reader, out / stage) for stage in ('S_A2', 'S_B2')}
    documents = {c: document_entries(reader, roots[c] / f'docs/full_1032/{c}/LLM_readme.md')
                 for c in ('A2', 'B2')}
    rows = [{'api': name, 'native': {c: {'metric': metrics[c].get(name, {}),
             'saved_snippet': saved_snippet(runs[c], name),
             'snippet_binding': 'final result details if available'} for c in roots},
             'repair': (doc or {}).get('apis', {}).get(name),
             'readme_before': documents['A2'].get(name), 'readme_after': documents['B2'].get(name),
             **{s: source[s]['cases'].get(name) or (source[s]['summary'] or {}).get('apis', {}).get(name)
                for s in source}} for name in manifest]
    return {'repository': 'MDAnalysis', 'scope': 'Isolated full1032 v4 continuation',
        'expected': 1032, 'updated_at': datetime.now().astimezone().isoformat(), 'rows': rows,
        'doc': {k: v for k, v in (doc or {}).items() if k != 'apis'},
        'source_summaries': {s: source[s]['summary'] for s in source},
        'run_contracts': {c: r.get('run') for c, r in runs.items()},
        'derived': derived(rows, doc), 'sources': reader.sources, 'jobs': state,
        'limitations': ['Missing outcomes and pending stages are not failures or zero success rates.',
                        'MDAnalysis v4 is not an exact historical v3 replication.']}
