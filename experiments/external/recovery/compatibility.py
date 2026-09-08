"""Resolve only previously reviewed bookkeeping/transport migrations."""
import hashlib
import json
from pathlib import Path

from aideal.checkpoint_compatibility import fingerprint, load_compatibility


def components(result):
    run = result['run']
    recorded = run['fingerprint_components']
    if recorded.get('schema') in (3, 4):
        return recorded, None
    path = Path(run['checkpoint']).with_name('checkpoint_compatibility.json')
    if not path.exists():
        return recorded, None
    proof = json.loads(path.read_text())
    current = proof['current_components']
    migration = load_compatibility(Path(run['checkpoint']), current)
    if not migration:
        raise ValueError('approved checkpoint migration is unavailable')
    captured = Path(proof['captured_proof'])
    if hashlib.sha256(captured.read_bytes()).hexdigest() != proof['captured_proof_sha256']:
        raise ValueError('migration input proof was changed')
    if fingerprint(recorded) != run['experiment_fingerprint']:
        raise ValueError('baseline fingerprint does not bind its recorded components')
    # A later schema-2 invocation can differ only by its mutable output aggregate.
    # Reuse the already reviewed input-only proof, explicitly retaining this limit.
    legacy = proof['legacy_components']
    if {k: v for k, v in recorded.items() if k != 'fixtures'} != {
            k: v for k, v in legacy.items() if k != 'fixtures'}:
        raise ValueError('baseline differs from reviewed migration beyond mutable output aggregate')
    migration['baseline_fingerprint'] = run['experiment_fingerprint']
    migration['historical_output_aggregate_differs'] = recorded['fixtures'] != legacy['fixtures']
    migration['limitation'] = ('Input bytes are checked against the reviewed input-only proof; '
        'historical output contents and runtime state are not reconstructed. '
        'This is a supplementary recovery result, not certification of baseline execution.')
    return current, migration


def engine_files(directory, schema):
    names = ['config.py', 'doc_checks.py', 'llm.py', 'prompts.py', 'readme_agent.py']
    if schema in (3, 4):
        names += ['checkpoint_compatibility.py', 'provider_deadline.py']
    elif schema != 2:
        raise ValueError('unsupported baseline fingerprint schema')
    if schema == 4:
        names += ['experiment_identity.py', 'profile.py', 'execution.py']
    return [directory / name for name in names]
