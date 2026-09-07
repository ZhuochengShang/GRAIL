"""Pure forecast, failure-triage, and path-ownership calculations."""
import statistics


def forecast(ledger):
    """Empirical serial comprehension estimates, never a whole-pipeline ETA."""
    rows = ledger.get('rows', [])
    unresolved = sum(r.get('status') == 'pending' or r.get('runner_category') == 'llm-error' for r in rows)
    fp = ledger.get('fingerprint')
    events = [e for e in ledger.get('all_checkpoint_events', [])
              if fp and e.get('experiment_fingerprint') == fp]
    recent = events[-30:]
    seconds = [float(e['wall_s']) for e in recent if float(e.get('wall_s') or 0) > 0]
    terminal = sum(e.get('status') in ('pass', 'fail') and e.get('error_category') != 'llm-error' for e in recent)
    result = {'remaining_apis': unresolved, 'sample_attempts': len(recent),
              'recent_terminal_fraction': terminal / len(recent) if recent else None,
              'hours': None, 'scope': 'remaining zero-fix comprehension only',
              'excludes': ['generation', 'document repair/deep dives', 'future B-cell evaluations',
                           'post-treatment checks', 'future queue/cooldown delays'],
              'assumption': 'serial API attempts; recent latency and recovery fraction remain representative'}
    if ledger.get('status') == 'complete':
        result.update(state='complete', hours={'optimistic': 0, 'likely': 0, 'conservative': 0})
    elif not rows or len(seconds) < 5:
        result.update(state='insufficient_observations')
    elif terminal == 0:
        result.update(state='stalled_no_recent_terminal_outcomes')
    else:
        ordered = sorted(seconds)
        q = lambda p: ordered[round((len(ordered)-1)*p)]
        fraction = terminal / len(recent)
        # These are sensitivity scenarios, not statistical confidence bounds.
        result.update(state='estimated' if unresolved else 'awaiting_final_validation',
                      hours={'optimistic': unresolved*q(.25)/3600,
                             'likely': unresolved*statistics.mean(seconds)/fraction/3600,
                             'conservative': unresolved*max(q(.90), statistics.mean(seconds))/(fraction/2)/3600})
    return result


def classify(row):
    error = str(row.get('error') or '')
    if row.get('review_evidence'):
        return row.get('primary_category', 'unknown'), 'reviewed', row.get('category_reason', '')
    if row.get('runner_category') == 'llm-error':
        return 'provider', 'high', 'Recorded provider failure; preserve and retry under existing policy.'
    if 'cannot import name' in error or 'has no attribute' in error:
        return 'api-identity-or-version', 'medium', 'Verify intended owner and installed version; not proof of missing dependency.'
    if 'ModuleNotFoundError' in error:
        return 'dependency-or-invented-module', 'medium', 'Check actual package inventory and whether this module exists upstream.'
    if 'FileNotFound' in error or 'No such file' in error:
        return 'input-or-output-path', 'medium', 'Compare attempted path, file schema, and output-directory setup.'
    if 'AssertionError' in error:
        return 'assertion-or-behavior', 'medium', 'Compare expected value with pinned implementation; do not weaken the assertion.'
    if 'TypeError' in error or 'ValueError' in error:
        return 'input-contract-or-api-call', 'medium', 'Check signature, dtype, shape, units, and file format.'
    return 'unknown', 'low', 'Source, supplied document, and script review required.'


def overlaps(owners):
    conflicts = []
    for i, (a, p) in enumerate(owners):
        for b, q in owners[i+1:]:
            if a != b and (p == q or p in q.parents or q in p.parents):
                conflicts.append({'owner_a': a, 'path_a': str(p), 'owner_b': b, 'path_b': str(q)})
    return conflicts
