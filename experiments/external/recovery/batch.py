"""A2-only source recovery: fixed denominator, sequential APIs, resumable rounds."""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path

from aideal.config import load_config
from .engine import digest, policy, save
from .runner import run
from .snapshot import freeze, runtime_environment
from .validation import eligible, file_sha


@contextmanager
def environment(values):
    old = dict(os.environ)
    os.environ.clear()
    os.environ.update(values)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old)


def publish(out, state):
    state['updated_at'] = datetime.now().astimezone().isoformat()
    state['native_recovery_by_round'] = {str(n): sum(
        r.get('status') == 'recovered_native' and r.get('code_fix_rounds', 6) <= n
        for r in state['apis'].values()) for n in range(6)}
    state['statuses'] = dict(Counter(r['status'] for r in state['apis'].values()))
    save(out / 'summary.json', state)
    text = ['# A2 source-only recovery', '',
        f"Updated: {state['updated_at']}", '',
        f"Fixed eligible-failure denominator: {len(state['apis'])}. A2 is round zero; five new proposals maximum; stuck threshold two.", '',
        '| API | Status | New code rounds | Evidence / blocker |', '|---|---|---:|---|']
    for api, row in state['apis'].items():
        reason = str(row.get('error') or row.get('report') or '').replace('|', '\\|').replace('\n', ' ')
        text.append(f"| {api} | {row['status']} | {row.get('code_fix_rounds', 0)} | {reason} |")
    text += ['', 'Native recovery does not certify the generated assertions. Semantic review remains required.',
             'B2 is a separate fresh-reader evaluation of the rewritten generated README. Original README repair is omitted.']
    (out / 'REPORT.md').write_text('\n'.join(text) + '\n')


def batch(baseline_config, result_path, repo, work, out, *, execute=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = json.loads(Path(result_path).read_text())
        if result.get('doc_source') != 'aideal':
            raise ValueError('recovery starts only from generated-README A2')
        names, exclusions = [], {}
        for name, row in result['metrics'].items():
            try:
                eligible(result, name)
                names.append(name)
            except ValueError as exc:
                if row.get('status') != 'pass':
                    exclusions[name] = str(exc)
        # Validate completeness even when no eligible failures exist.
        metrics, native_run = result['metrics'], result['run']
        if (native_run['max_fix_rounds'] != 0 or native_run['api_count'] != len(metrics)
            or any(r.get('status') not in ('pass', 'fail') or r.get('error_category') == 'llm-error'
                   for r in metrics.values())):
            raise ValueError('A2 remains partial or has provider failures')
        identity = {'protocol': policy(), 'baseline_sha256': file_sha(result_path), 'repo': repo}
        saved = out / 'summary.json'
        state = json.loads(saved.read_text()) if saved.exists() else {
            'identity': identity, 'baseline_result': str(result_path), 'baseline_cell': 'A2',
            'cohort_sha256': digest(names), 'exclusions': exclusions,
            'apis': {name: {'status': 'pending'} for name in names},
            'semantic_validation': 'needs_independent_review', 'headline_credit': False}
        if state['identity'] != identity:
            raise ValueError('A2/protocol changed; use a new result namespace')
        base = load_config(baseline_config)
        root = freeze(base, result, Path(work))
        cfg = load_config(root / 'configs' / Path(baseline_config).name)
        env, runtime = runtime_environment(base, cfg, result, repo)
        save(out / 'runtime.json', runtime)
        state['snapshot'] = str(root)
        publish(out, state)
        for name in names:
            if state['apis'][name]['status'] in ('recovered_native', 'stuck', 'exhausted', 'infra_blocked'):
                continue
            try:
                with environment(env):
                    row = run(cfg, base, result, name, 'source', 'docs/eval/api_manifest.json', execute=execute)
                state['apis'][name] = {'status': row['status'], 'report': row.get('report'),
                    'code_fix_rounds': len(row.get('rounds', [])),
                    'provider_events': sum(e.get('category') == 'llm-error' for e in row.get('events', [])),
                    'identity': row.get('identity'), 'stop_reason': row.get('stop_reason')}
                if row.get('report'):
                    # Keep full round code/error/diagnosis evidence in the deadline
                    # package as well as the private resumable execution directory.
                    evidence = out / 'cases' / (digest(name) + '.json')
                    evidence.parent.mkdir(exist_ok=True)
                    save(evidence, row)
                    state['apis'][name]['evidence_file'] = str(evidence.relative_to(out))
            except Exception as exc:
                state['apis'][name] = {'status': 'preflight_blocked', 'error': f'{type(exc).__name__}: {exc}'}
            publish(out, state)
        return state
