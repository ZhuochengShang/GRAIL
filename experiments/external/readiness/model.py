"""Pure assessment and suggestion logic; no provider or process execution."""
from collections import Counter
import hashlib
import json

from experiments.external.automation.analysis import classify


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def assess(ledger, data, config):
    rows = ledger.get('rows', [])
    count = ledger.get('expected', 0)
    errors = list(ledger.get('errors', []))
    if len(rows) != count or count <= 0 or len({r['api'] for r in rows}) != count:
        errors.append('Missing, duplicate, or inconsistent API denominator')
    counts = Counter(r.get('status', 'pending') for r in rows)
    provider = sum(r.get('runner_category') == 'llm-error' for r in rows)
    complete = (ledger.get('status') == 'complete' and not errors and not provider
                and bool(ledger.get('fingerprint')) and counts['pass']+counts['fail'] == count)
    return {
        'status': 'invalid_evidence' if errors else 'complete_measurement' if complete else 'partial_measurement',
        'scope': 'documentation-conditioned API execution under the fixed harness',
        'denominator': count, 'counts': dict(counts), 'unresolved_provider_apis': provider,
        'final_raw_pass_percent': 100*counts['pass']/count if complete else None,
        'provisional_passes': counts['pass'],
        'fingerprint': ledger.get('fingerprint'), 'errors': errors,
        'dimensions': {
            'discovery': {'status': 'not_measured', 'reason': 'Target API is supplied; independent agent search is not tested.'},
            'setup_and_inputs': {'status': 'partial_evidence', 'fixture_audit': data.get('status', 'missing'),
                                 'config_audit': config.get('status', 'missing'),
                                 'limitations': data.get('limitations', []) + data.get('failures', []) + config.get('warnings', []),
                                 'reason': 'Prepared harness and fixture identity do not measure autonomous installation or per-API input suitability.'},
            'api_execution': {'status': 'measured' if complete else 'provisional',
                              'reason': 'Native execution and witness checks; not an independent semantic certificate.'},
            'workflow_completion': {'status': 'not_measured', 'reason': 'No held-out multi-API workflow benchmark is included.'},
            'verification_and_recovery': {'status': 'partial_evidence',
                                         'reason': 'Assertions, diagnostics and retry histories exist; independent oracle validity and agent recovery capability are not established.'}},
        'overall_readiness_score': None,
        'interpretation': 'These results describe a codebase-agent-task-environment combination, not universal codebase quality.'}


GUIDANCE = {
    'provider': ('execution_infrastructure', 'Investigate provider failures and recorded retry behavior',
                 'Check quota/cooldown and error histories; preserve existing retry policy and completed checkpoints.',
                 'Reattempt only compatible unresolved requests under authorized policy; report recovery separately from documentation benefit.'),
    'doc-wrong': ('documentation', 'Correct the documented behavior against pinned implementation',
                  'Prepare a targeted documentation diff using the recorded source discrepancy and an accurate executable example.',
                  'Verify the example independently, preserve upstream tests, and measure a fresh matched treatment; do not replace the native result.'),
    'doc-vague': ('documentation', 'Clarify the missing API constraint',
                  'Document the exact input schema, receiver, or constraint supported by the source review.',
                  'Validate an example and a boundary case, then re-evaluate under a versioned matched treatment.'),
    'doc-missing': ('documentation', 'Supply a missing discoverable API explanation',
                    'Confirm the canonical API and prepare a minimal entry with valid call and input requirements.',
                    'Check source alignment and independent example behavior before a fresh matched evaluation.'),
    'test/scaffold': ('harness_or_input', 'Resolve the reviewed harness or input barrier',
                      'Prepare an isolated diagnostic and a minimal harness/input proposal; retain any secondary input-format finding.',
                      'Run the same saved snippet in a separate diagnostic directory; any protocol fix requires a separately frozen comparison.'),
    'example-invalid': ('example_or_input', 'Replace the invalid example or fixture reference',
                        'Identify a checked-in, format-compatible fixture and prepare an example diff.',
                        'Verify pinned bytes, schema and meaningful output assertions; keep diagnostic and native outcomes distinct.'),
    'api-identity': ('api_discovery_or_call', 'Clarify the intended API owner and call',
                     'Check the canonical module/class/signature and prepare a documented call correction.',
                     'Verify runtime ownership in isolation and test a meaningful property; repeated bare names need owner-specific review.')}


def suggestion(repo, cell, row, ledger, input_row=None):
    category, confidence, next_check = classify(row)
    change_kind, title, action, validation = GUIDANCE.get(category, (
        'investigation', 'Investigate the observed API-use barrier', next_check,
        'Reproduce in an isolated diagnostic; establish input, call and assertion validity before attributing a documentation or code defect.'))
    evidence = {'fingerprint': ledger.get('fingerprint'), 'manifest_sha256': ledger.get('manifest_file_sha256'),
                'api': row['api'], 'status': row.get('status'), 'native_category': row.get('runner_category'),
                'error': row.get('error'), 'source': row.get('source'),
                'review_evidence': row.get('review_evidence'),
                'script_sha256': (input_row or {}).get('script_sha256')}
    # Retry counters change frequently; they are retained but do not invalidate
    # a proposal when the underlying evidence/signature/error is unchanged.
    return {'id': digest([repo, cell, row['api']])[:20], 'repository': repo, 'cell': cell, 'api': row['api'],
            'evidence_version': digest(evidence), 'evidence': evidence,
            'title': f'{row["api"]}: {title}', 'change_kind': change_kind,
            'candidate_category': category, 'confidence': confidence,
            'diagnosis': row.get('category_reason') if row.get('review_evidence') else next_check,
            'proposed_action': action, 'validation_criteria': validation,
            'expected_benefit': 'Hypothesis only; measure against the pinned baseline before claiming improvement.',
            'risks': ['Changing inputs, harness, prompts or code changes the protocol.',
                      'Source-informed review must not leak into the audience treatment.'],
            'attempts': row.get('checkpoint_attempts'), 'provider_error_attempts': row.get('provider_error_attempts'),
            'document_rounds': row.get('doc_rounds_used'), 'script': (input_row or {}).get('script'),
            'allowed_executors': ['human', 'agent'], 'default_execution': 'disabled',
            'priority': 'execution_blocker' if category == 'provider' else 'reviewed_barrier' if confidence == 'reviewed' else 'needs_diagnosis'}
