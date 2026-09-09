"""Audit reuse against the independent-branch plan without launching experiments."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path

from experiments.external.recovery.compatibility import components
from experiments.external.study_dashboard.data import REPOS


def read(path, sources):
    raw = path.read_bytes()
    sources[str(path)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def normalized_execution(value):
    return {k: v for k, v in value.items() if k not in ('work_dir', 'output_dir')}


def priority(parent, repo, sources):
    prefix, rel = REPOS[repo]
    aroot, broot = (parent / f'{prefix}_{c}' / rel for c in ('A2', 'B2'))
    a2 = read(aroot / 'docs/eval/A2/comprehension.json', sources)
    b2 = read(broot / 'docs/eval/B2/comprehension.json', sources)
    inherited = read(broot / 'docs/eval/A2/comprehension.json', sources)
    doc = read(broot / 'docs/eval/B2/docfix.json', sources)
    a, am = components(a2)
    b, bm = components(b2)
    failures = sorted(n for n, m in a2['metrics'].items() if m['status'] == 'fail')
    checks = {'inherited_A2_exact': inherited == a2,
        'same_full_manifest': set(a2['metrics']) == set(b2['metrics']),
        'repair_targets_original_A2_failures': set(doc['apis']) == set(failures),
        'all_repair_targets_processed': doc['processed'] == len(failures),
        'source_informed': doc['deep_dive_first'] is True,
        'five_document_rounds_zero_snippet_validation': doc['doc_rounds'] == 5 and doc['retry_rounds'] == 0,
        'fresh_full_manifest_zero_fix': b2['run']['max_fix_rounds'] == 0 and
            b2['run']['api_count'] == b2['run']['manifest_api_count'] == len(a2['metrics']),
        'same_execution_contract_except_owned_paths': normalized_execution(a['execute_config']) == normalized_execution(b['execute_config'])}
    for key in ('source', 'fixtures', 'scaffold', 'models', 'interpreter', 'timeout_s',
                'class_context', 'doc_scope', 'manifest_sha256'):
        # Some schemas use timeout rather than timeout_s; compare both.
        checks['same_'+key] = a.get(key) == b.get(key)
    checks['same_timeout'] = a2['run']['timeout_s'] == b2['run']['timeout_s']
    checks['A2_B2_provider_resolved'] = all(m.get('error_category') != 'llm-error'
        for run in (a2, b2) for m in run['metrics'].values())
    return {'reuse_structural_checks_pass': all(checks.values()), 'checks': checks,
        'A2_N': len(a2['metrics']), 'A2_pass': sum(m['status']=='pass' for m in a2['metrics'].values()),
        'A2_failures': failures, 'B2_1': 'new feedback-only continuation required',
        'B2_2_retained_entries': doc['doc_fixed'],
        'B2_fresh_pass': sum(m['status']=='pass' for m in b2['metrics'].values()),
        'reviewed_migrations': {'A2': am, 'B2': bm},
        'limitations': ['Structural reuse is not certification of semantic validity or equal lifetime repair budget.',
            'Legacy document rounds are retained per invocation; restart history may exceed five lifetime rounds.',
            'Fresh isolated feedback repairs differ from historical shared output state.',
            'Matched clean-harness claims require a separate matched rerun of affected baseline and repair stages.']}


def rdpro(parent, sources):
    root = parent / 'GRAIL_rdpro_final_A2/experiments/rdpro/docs'
    a2 = read(root / 'comprehension_A2_generated_all.json', sources)
    fix = {}
    for label in ('shared88', 'complement83'):
        r = read(root / f'comprehension_A2_fix5_{label}.json', sources)
        fix[label] = {'N': len(r['metrics']), 'max_fix_rounds': r['run']['max_fix_rounds'],
            'round_zero_disagreements_with_A2': sum((m.get('pass_round') == 0) !=
                (a2['metrics'][n]['status'] == 'pass') for n, m in r['metrics'].items()),
            'pass': sum(m['status']=='pass' for m in r['metrics'].values()),
            'reuse_as_B2_1': False}
    docroot = parent / 'GRAIL/experiments/rdpro/docs'
    doc = read(docroot / 'docfix_B2_all171.completed.json', sources)
    fresh = read(docroot / 'comprehension_B2_final_all171.json', sources)
    return {'status': 'historical context only; no new RDPro execution registered',
        'A2_artifact_N': len(a2['metrics']), 'A2_native_pass': sum(m['status']=='pass' for m in a2['metrics'].values()),
        'B2_1_historical_fix5': fix,
        'B2_2': {'targets': doc['attempted'], 'processed': doc['processed'],
            'retained_entries': doc['doc_fixed'], 'deep_dive_first': doc['deep_dive_first'],
            'document_rounds': doc['doc_rounds'], 'validation_snippet_fixes': doc['retry_rounds'],
            'targets_equal_original_A2_failures': set(doc['apis']) == {n for n,m in a2['metrics'].items() if m['status']=='fail'}},
        'fresh': {'N': len(fresh['metrics']), 'native_pass': sum(m['status']=='pass' for m in fresh['metrics'].values()),
                  'snippet_fixes': fresh['run']['max_fix_rounds']},
        'limitations': ['171 generated entries include 10 extras beyond the validated 161 APIs.',
            'Older engine, Scala receiver hints and separate round-zero draws prevent exact new-protocol parity.',
            'Historical semantic-review counts and native counts remain separate.']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace-parent', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    sources = {}
    result = {'updated_at': datetime.now().astimezone().isoformat(),
        'protocol': 'aideal-independent-a2-branches-v5',
        'priority': {r: priority(args.workspace_parent, r, sources) for r in REPOS},
        'RDPro': rdpro(args.workspace_parent, sources), 'sources': sources}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise ValueError('preserve previous reuse audits; choose a new output file')
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({r: v['reuse_structural_checks_pass'] for r,v in result['priority'].items()}))


if __name__ == '__main__':
    main()
