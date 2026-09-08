"""Passive, timestamped failure evidence capture; no runner/provider imports."""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

MAIN = Path('/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_rdpro_puzzle_aideal')
PARENT = MAIN.parent
AUDIT = PARENT / 'GRAIL_overnight_evidence_audit'
BASE = AUDIT / 'experiments/external/overnight_audit/data_validation'
sys.path.insert(0, str(MAIN))
from experiments.external.assertion_replay.evidence import collect, digest

started = datetime.now().astimezone().isoformat()
OUT = BASE / 'failure_snapshots' / datetime.now().strftime('%Y-%m-%d_%H%M%S')
OUT.mkdir(parents=True, exist_ok=False)
def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str) + '\n')

index, cells = [], []
for repo, prefix, relative in [('mir_eval', 'GRAIL_mir_eval', 'experiments/external/mir_eval'),
                               ('thumbnailator', 'GRAIL_thumbnailator', 'experiments/external/thumbnailator'),
                               ('tslearn', 'GRAIL_tslearn_full235', 'experiments/tslearn')]:
    for cell in ['A1', 'A2', 'B2']:
        project = PARENT / f'{prefix}_{cell}' / relative
        evidence = collect(project, cell)
        if not evidence:
            continue
        observed = datetime.now().astimezone().isoformat()
        failed = {n: r for n, r in evidence['rows'].items() if r['status'] != 'pass'}
        folder = OUT / repo / cell
        folder.mkdir(parents=True)
        # Preserve the collected observation, even when an active writer appends later.
        save(folder / 'native_failures.json', dict(evidence, rows=failed, observed_at=observed,
             total_observed_rows=len(evidence['rows'])))
        journal = project / f'.aideal_exec/{cell}/comprehension_progress.jsonl'
        if journal.exists():
            raw = journal.read_bytes()
            events = []
            for line in raw.splitlines(keepends=True):
                if line.endswith(b'\n'):
                    event = json.loads(line)
                    if event.get('name') in failed:
                        events.append(event)
            save(folder / 'checkpoint_history.json', {'source': str(journal), 'sha256': digest(raw),
                 'observed_at': datetime.now().astimezone().isoformat(),
                 'note': 'All retained fingerprint groups; not all are compatible. Event count is not SDK attempt count.',
                 'events': events})
        for name, row in failed.items():
            case = folder / ('api_' + digest(name)[:16])
            case.mkdir()
            detail = row.get('execution_evidence')
            detail = detail if isinstance(detail, dict) else {}
            inspection = {'name': name, 'native_row': row, 'retained_binding': 'unavailable'}
            code = detail.get('code', '')
            if code:
                (case / 'recorded_snippet.txt').write_text(code)
            # Never attach old snippets to provider failures that produced no code.
            if row.get('error_category') == 'llm-error':
                inspection['retained_binding'] = 'provider_failure_no_execution_code_attached'
            else:
                candidates = [project / f'.aideal_exec/{cell}/run_{name}' / filename
                              for filename in ['api_test.py', 'ApiTest.java']]
                if detail.get('scala_file'):
                    candidates.insert(0, Path(detail['scala_file']))
                for path in candidates:
                    if path.is_file() and path.resolve().is_relative_to(project.resolve()):
                        raw = path.read_bytes()
                        source = raw.decode(errors='replace')
                        # Weak prefix binding explicitly does not certify full historical identity.
                        norm = lambda text: '\n'.join(line.strip() for line in text.strip().splitlines())
                        binding = ('recorded_code_prefix_present' if code and norm(code) in norm(source)
                                   else 'mismatch_do_not_replay' if code else 'unbound_legacy_do_not_certify')
                        inspection.update(retained_binding=binding, retained_path=str(path),
                                          retained_sha256=digest(raw))
                        (case / ('retained_' + path.name + '.txt')).write_bytes(raw)
                        break
            source = row.get('source', '')
            match = re.match(r'^(.*):(\d+)$', source)
            if match:
                path, line = project / match[1], int(match[2])
                if path.is_file() and path.resolve().is_relative_to(project.resolve()):
                    raw = path.read_bytes()
                    lines = raw.decode(errors='replace').splitlines()
                    lo, hi = max(1, line-15), min(len(lines), line+140)
                    (case / 'source_window.txt').write_text('\n'.join(f'{i}: {lines[i-1]}' for i in range(lo, hi+1))+'\n')
                    inspection['source_window'] = {'path': str(path), 'full_file_sha256': digest(raw),
                                                   'first_line': lo, 'last_line': hi,
                                                   'other_sites': row.get('source_other_sites', 0)}
            save(case / 'evidence.json', inspection)
            index.append({'repository': repo, 'cell': cell, 'api': name,
                          'native_category': row.get('error_category'), 'error': row.get('error'),
                          'wall_s': row.get('wall_s'), 'attempts_field': row.get('attempts'),
                          'binding': inspection['retained_binding'],
                          'evidence': str((case / 'evidence.json').relative_to(OUT))})
        cells.append({'repository': repo, 'cell': cell, 'complete': evidence['complete'],
                      'observed': len(evidence['rows']), 'failures': len(failed),
                      'categories': dict(Counter(r.get('error_category') for r in failed.values()))})

# Save contemporaneous source-recovery records separately; never merge with native outcomes.
for version in ['pipeline_v2', 'pipeline_v3']:
    for repo in ['mir_eval', 'thumbnailator', 'tslearn']:
        root = BASE / version / repo
        if version == 'pipeline_v2':
            root = root / 'source'
        for path in [root / 'summary.json', *sorted((root / 'cases').glob('*.json'))]:
            if path.is_file():
                raw = path.read_bytes()
                target = OUT / 'recovery_observations' / path.relative_to(BASE)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
for name in ['PROVIDER_504_EVIDENCE.json', 'PROVIDER_504_DIAGNOSIS.md']:
    path = BASE / 'pipeline_v3' / name
    if path.is_file():
        (OUT / name).write_bytes(path.read_bytes())
save(OUT / 'summary.json', {'started_at': started, 'finished_at': datetime.now().astimezone().isoformat(),
     'scope': 'Latest compatible native non-pass rows; one row per repo/cell/API name, not distinct functions across cells.',
     'total': len(index), 'categories': dict(Counter(r['native_category'] for r in index)), 'cells': cells})
with (OUT / 'FAILED_FUNCTIONS.csv').open('w') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(index[0]))
    writer.writeheader()
    writer.writerows(index)
save(OUT / 'FAILED_FUNCTIONS.json', index)
(OUT / 'capture.py').write_bytes(Path(__file__).read_bytes())
print(OUT)
print(json.dumps({'total': len(index), 'cells': cells}, indent=2))
