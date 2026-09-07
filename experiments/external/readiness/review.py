"""Append-only review decisions; no implementation, merging or rescoring."""
import json
from datetime import datetime, timezone
from pathlib import Path

from experiments.external.readiness.model import digest


def history(path):
    if not path.exists():
        return []
    # Corrupt decisions fail closed instead of silently erasing approvals.
    events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    previous = None
    for event in events:
        if event.get('previous_event') != previous:
            raise ValueError('Review decision chain is inconsistent')
        previous = digest(event)
    return events


def state(card, events):
    relevant = [e for e in events if e['id'] == card['id']]
    current = [e for e in relevant if e['evidence_version'] == card['evidence_version']]
    if not current:
        return {'status': 'stale_review' if relevant else 'open', 'events': []}
    status, plan, executor, result = 'open', None, None, None
    for event in current:
        action = event['action']
        if action == 'propose':
            status, plan, executor, result = 'proposed', event['plan'], None, None
        elif action == 'approve_plan':
            status, executor = 'approved_for_implementation', event['executor']
        elif action == 'submit_result':
            status, result = 'awaiting_result_review', event['result']
        else:
            status = {'defer': 'deferred', 'reject': 'rejected', 'request_changes': 'changes_requested',
                      'accept_result': 'accepted_by_reviewer'}[action]
    return {'status': status, 'plan': plan, 'executor': executor, 'result': result, 'events': current}


def validate(card, events, decision):
    if decision.get('evidence_version') != card['evidence_version']:
        raise ValueError('Stale evidence version: inspect the current suggestion again')
    if not decision.get('actor') or decision.get('actor_type') not in ('human', 'agent') or not decision.get('note'):
        raise ValueError('An actor, actor_type (human/agent), and review note are required')
    action = decision.get('action')
    current = state(card, events)
    status = current['status']
    if action == 'propose':
        plan = decision.get('plan', {})
        if any(not plan.get(k) for k in ('summary', 'files', 'validation', 'risks', 'isolation')):
            raise ValueError('A concrete plan needs summary, files, validation, risks, and isolation')
        if not isinstance(plan['files'], list) or not all(isinstance(x, str) for x in plan['files']):
            raise ValueError('Plan files must be a list of paths to review')
    elif action == 'approve_plan':
        if status != 'proposed' or decision['actor_type'] != 'human' or decision.get('executor') not in ('human', 'agent'):
            raise ValueError('Human review of a concrete proposal and a human/agent executor are required')
    elif action == 'submit_result':
        if status != 'approved_for_implementation' or decision['actor_type'] != current['executor']:
            raise ValueError('Only the assigned executor can submit work under the approved plan')
        result = decision.get('result', {})
        if result.get('validation_status') != 'passed' or any(not result.get(k) for k in ('change', 'validation', 'comparison')):
            raise ValueError('Submission requires change, validation and before/after comparison artifacts plus declared passed validation')
    elif action == 'accept_result':
        if status != 'awaiting_result_review' or decision['actor_type'] != 'human':
            raise ValueError('Human review of submitted validation evidence is required to accept a result')
    elif action not in ('defer', 'reject', 'request_changes'):
        raise ValueError(f'Unknown review action: {action}')
    return current


def record(card, events, decision, directory):
    """Caller holds the publisher/review lock. Bind decisions to exact evidence."""
    validate(card, events, decision)
    fields = ('action', 'actor', 'actor_type', 'note', 'plan', 'executor', 'result')
    event = {k: decision[k] for k in fields if k in decision}
    if event['action'] == 'submit_result':
        result = dict(event['result'])
        for kind in ('change', 'validation', 'comparison'):
            original = Path(result[kind]).resolve()
            contents = original.read_bytes()
            import hashlib
            checksum = hashlib.sha256(contents).hexdigest()
            dest = directory/'artifacts'/checksum
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                with dest.open('xb') as stream:
                    stream.write(contents)
            result[kind] = {'original_path': str(original), 'sha256': checksum,
                            'snapshot': f'artifacts/{checksum}'}
        event['result'] = result
    event.update(id=card['id'], evidence_version=card['evidence_version'],
                 recorded_at=datetime.now(timezone.utc).isoformat(), previous_event=digest(events[-1]) if events else None)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/'decisions.jsonl').open('a') as stream:
        stream.write(json.dumps(event, sort_keys=True)+'\n')
        stream.flush()
        import os
        os.fsync(stream.fileno())
    return event
