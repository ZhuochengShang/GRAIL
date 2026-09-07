"""Small resumable recovery state machine, independent of provider and language."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

POLICY = Path(__file__).with_name('protocol.yaml')


def policy():
    import yaml
    return yaml.safe_load(POLICY.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def recover(identity, initial, out, *, diagnose, attempt, max_rounds=5, stuck=2):
    """Callbacks must preserve their own artifacts before returning.

    `attempt(round, previous, diagnosis)` returns status/category/code/error and
    evidence paths. Provider errors are events, never credited code-fix rounds.
    A caller must hold the output lock and validate immutable inputs each time.
    """
    if not 1 <= max_rounds <= 5 or not 0 <= stuck <= max_rounds:
        raise ValueError('require 1..5 code rounds and 0..max_rounds stuck threshold; 0 disables')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / 'recovery.json'
    fingerprint = digest({'identity': identity, 'max_rounds': max_rounds,
                          'stuck': stuck, 'initial': initial})
    state = json.loads(path.read_text()) if path.exists() else {
        'fingerprint': fingerprint, 'identity': identity, 'initial': initial,
        'events': [], 'rounds': [], 'status': 'pending', 'diagnosis': None,
        'max_rounds': max_rounds, 'stuck_threshold': stuck, 'stop_reason': None,
        'semantic_validation': 'needs_independent_review', 'headline_credit': False}
    if state['fingerprint'] != fingerprint:
        raise ValueError('changed recovery inputs; use a new output namespace')
    if state['status'] in ('recovered_native', 'exhausted', 'stuck', 'infra_blocked'):
        return state
    save(path, state)
    if state['diagnosis'] is None:
        try:
            state['diagnosis'] = diagnose()
        except Exception as exc:
            state['events'].append({'stage': 'deep_dive', 'error': str(exc),
                                    'status': 'blocked'})
            state['status'] = 'blocked'
            save(path, state)
            return state
        save(path, state)
    previous = state['rounds'][-1] if state['rounds'] else initial
    for number in range(len(state['rounds']) + 1, max_rounds + 1):
        row = attempt(number, previous, state['diagnosis'])
        row = dict(row, code_fix_round=number)
        state['events'].append(row)
        if row.get('category') == 'llm-error':
            state['status'] = 'provider_blocked'
            save(path, state)
            return state
        state['rounds'].append(row)
        state['status'] = 'running'
        if row['status'] == 'pass':
            state['status'] = 'recovered_native'
        elif row.get('category') == 'infra':
            state['status'] = 'infra_blocked'
        elif stuck and len(state['rounds']) >= stuck:
            recent = state['rounds'][-stuck:]
            if len({(r.get('category'), r.get('error', '')[:160]) for r in recent}) == 1:
                state['status'] = 'stuck'
                state['stop_reason'] = f'{stuck} consecutive equal category/error-prefix observations'
        if state['status'] == 'running' and number == max_rounds:
            state['status'] = 'exhausted'
            state['stop_reason'] = f'code-fix budget {max_rounds} exhausted'
        save(path, state)
        if state['status'] != 'running':
            return state
        previous = row
    return state
