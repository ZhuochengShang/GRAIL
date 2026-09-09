"""Build a provenance-bearing view of current, historical and missing evidence."""
from collections import Counter
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

REPOS = {'mir_eval': ('GRAIL_mir_eval', 'experiments/external/mir_eval'),
         'Thumbnailator': ('GRAIL_thumbnailator', 'experiments/external/thumbnailator'),
         'tslearn': ('GRAIL_tslearn_full235', 'experiments/tslearn')}
DEADLINE = datetime(2026, 9, 9, 11, tzinfo=ZoneInfo('America/Los_Angeles'))


class Evidence:
    def __init__(self):
        self.sources = []

    def text(self, path):
        raw = Path(path).read_bytes()
        self.sources.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
                             'bytes': len(raw)})
        return raw.decode()

    def json(self, path):
        return json.loads(self.text(path))


def historical_tables(text):
    """Read explicit table numerators; never infer a new treatment from B labels."""
    raw, reviewed = [], []
    target = None
    for line in text.splitlines():
        if line.startswith('## Raw execution results'):
            target = raw
        elif line.startswith('### Final semantically verified rates'):
            target = reviewed
        elif line.startswith('#'):
            target = None
        if target is None or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if target is raw and len(cells) == 5 and re.match(r'\d+/\d+', cells[1]):
            fractions = [tuple(map(int, re.match(r'(\d+)/(\d+)', c).groups())) for c in cells[1:]]
            target.append({'stratum': cells[0], 'n': fractions[0][1], 'passes': [p for p, n in fractions]})
        elif target is reviewed and len(cells) == 6 and cells[1].isdigit():
            target.append({'stratum': cells[0], 'n': int(cells[1]),
                           'passes': [int(re.match(r'\d+', c).group()) for c in cells[2:]]})
    if len(raw) != 5 or len(reviewed) != 5:
        raise ValueError('Historical report table format changed; do not guess denominators')
    return {'raw': raw, 'reviewed': reviewed}


def check_cells(cells):
    for cell in cells:
        if sum(cell['statuses'].values()) != cell['n'] or cell['n'] > cell['expected']:
            raise ValueError('Native outcome totals do not reconcile with recorded/full denominators')


def collect(parent):
    parent = Path(parent).resolve()
    main = parent / 'GRAIL_rdpro_puzzle_aideal'
    audit = parent / 'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit'
    data = audit / 'data_validation'
    evidence = Evidence()
    operations = evidence.json(data / 'provider_operations_v4/summary.json')
    cells = operations['native_cells']
    check_cells(cells)
    timings = list(csv.DictReader(io.StringIO(evidence.text(data / 'provider_operations_v4/API_TIMINGS.csv'))))
    if len(timings) != operations['api_rows']:
        raise ValueError('Report snapshot changed during read; retry the next refresh')
    for row in timings:
        for key in ('latest_native_attempt_s', 'retained_attempt_total_s', 'last_provider_s', 'last_retry_interval_s'):
            row[key] = float(row[key]) if row.get(key) else None
        for key in ('retained_checkpoint_events', 'retained_504_events', 'retained_cooldown_deferrals'):
            row[key] = int(row[key]) if row.get(key) else 0
    repairs, recovery, timing_basis = [], [], []
    for repo, (prefix, relative) in REPOS.items():
        project = parent / f'{prefix}_B2' / relative
        doc = evidence.json(project / 'docs/eval/B2/docfix.json')
        rounds = Counter(r.get('rounds_used', len(r.get('doc_rounds', []))) for r in doc['apis'].values())
        repairs.append({'repository': repo, 'processed': doc['processed'], 'target': doc['attempted'],
                        'retained': doc['doc_fixed'], 'statuses': dict(Counter(r['status'] for r in doc['apis'].values())),
                        'round_histogram': dict(rounds),
                        'retained_wall_s': sum(r.get('wall_s', 0) for r in doc['apis'].values())})
        run = evidence.json(project / 'docs/eval/B2/comprehension.json')
        seconds = sum(r.get('wall_s', 0) for r in run['metrics'].values())
        timing_basis.append({'repository': repo, 'doc_hours': repairs[-1]['retained_wall_s']/3600,
                             'b2_hours': seconds/3600, 'scope': 'retained document API time + final native API time; not lifetime elapsed'})
        source = evidence.json(data / 'pipeline_v2' / repo.lower() / 'source/summary.json')
        retry = data / 'pipeline_v3_inventory_retry' / repo.lower() / 'summary.json'
        post = evidence.json(retry if retry.exists() else data / 'pipeline_v3' / repo.lower() / 'summary.json')
        for stage, record in [('S_A2', source), ('S_B2', post)]:
            # An active API can retain its previous blocked status until a new outcome is saved.
            recovery.append({'repository': repo, 'stage': stage, 'n': len(record['apis']),
                             'statuses': record['statuses'], 'active_api': record.get('active_api'),
                             'by_round': record.get('native_recovery_by_round', {}),
                             'apis': {name: {k: row.get(k) for k in ('status', 'code_fix_rounds', 'error')}
                                      for name, row in record['apis'].items()}})
    historical = historical_tables(evidence.text(main/'experiments/rdpro/docs/STRATIFIED_A1_A2_COMPARISON.md'))
    # Verify the shared-88 raw zero-round values against original result metrics.
    a1 = evidence.json(parent/'GRAIL_rdpro_final_A1/experiments/rdpro/docs/comprehension_A1_original.json')
    a2 = evidence.json(parent/'GRAIL_rdpro_final_A2/experiments/rdpro/docs/comprehension_A2_generated_all.json')
    shared = set(a1['metrics'])
    expected = historical['raw'][0]
    if len(shared) != expected['n'] or [sum(a1['metrics'][n]['status']=='pass' for n in shared),
        sum(a2['metrics'][n]['status']=='pass' for n in shared)] != expected['passes'][:2]:
        raise ValueError('RDPro shared table does not match retained native evidence')
    historical['note'] = ('Historical stratified study, not a v3 replication. Fix5 means snippet repair, '
        'not B1/B2 document repair. A1 undocumented zero is reconstructed from round zero of its fix5 run. '
        'Recorded semantic review is a separate evidence layer, not a fresh execution replay.')
    from .mdanalysis import current
    md, md_progress = current(parent, evidence)
    replay = evidence.json(data/'assertion_replay/summary.json')
    replay['cells'] = [r for r in replay['cells'] if r['cell'] != 'B1']
    now = datetime.now(DEADLINE.tzinfo)
    return {'updated_at': now.isoformat(), 'native_snapshot': operations['updated_at'],
            'deadline': DEADLINE.isoformat(), 'hours_remaining': (DEADLINE-now).total_seconds()/3600,
            'native': cells, 'repairs': repairs, 'recovery': recovery, 'timings': timings,
            'rdpro': historical, 'mdanalysis': md, 'mdanalysis_progress': md_progress, 'replay': replay,
            'timing_basis': timing_basis, 'sources': evidence.sources,
            'proposal': {'status': 'Proposed only; no ablation launched', 'recommended_repo': 'mir_eval',
                         'cohort': 13, 'fresh_eval_per_arm': 148, 'planning_hours': [4, 7],
                         'scope': 'paired error-only/source-informed pilot, one run per arm; no equivalence claim'}}
