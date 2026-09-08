"""One resumable B2-failure case using the unchanged A2 source-recovery engine."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import shutil
import time

import yaml
from aideal.config import load_config

from experiments.external.recovery.batch import environment
from experiments.external.recovery.engine import digest, save
from experiments.external.recovery.runner import run
from experiments.external.recovery.snapshot import freeze, runtime_environment
from experiments.external.recovery.validation import file_sha
from .evidence import TERMINAL, cohort

POLICY = Path(__file__).with_name('protocol.yaml')


def implementation():
    """Bind the adapter and the unchanged source policy/implementation at registration."""
    recovery = Path(__file__).parent.parent / 'recovery'
    return {f'recovery/{name}': file_sha(recovery / name) for name in
            ('runner.py', 'engine.py', 'validation.py', 'compatibility.py', 'snapshot.py', 'protocol.yaml')}


def registered():
    record = yaml.safe_load(POLICY.read_text())
    if record['source_implementation'] != implementation():
        raise ValueError('source-recovery implementation changed after v3 registration')
    return record


def prepare(info, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    protocol = registered()
    identity = {**info['identity'], 'protocol_sha256': file_sha(POLICY),
                'adapter': {p.name: file_sha(p) for p in Path(__file__).parent.glob('*.py')}}
    path = out / 'summary.json'
    if path.exists():
        state = json.loads(path.read_text())
        if state['identity'] != identity:
            raise ValueError('post-B2 inputs changed; preserve results and use a new namespace')
        return state
    for cell in ('A2', 'B2'):
        save(out / f'{cell}_frozen.json', info[cell])
    # Keep the actual rewritten document and repair records in the report
    # snapshot, rather than relying only on absolute live-worktree links.
    native = info['root'] / 'docs/eval/B2'
    bundle = out / 'document_evidence'
    bundle.mkdir(exist_ok=True)
    for name in ('LLM_readme.md', 'docfix.json', 'docfix_command.json.stderr.log'):
        path = native / name
        if path.exists():
            shutil.copy2(path, bundle / name)
    if (native / 'docfix_changes').exists():
        shutil.copytree(native / 'docfix_changes', bundle / 'docfix_changes', dirs_exist_ok=True)
    state = {'protocol': protocol['version'], 'stage': 'S_B2', 'baseline_cell': 'B2',
             'repo': info['repo'], 'identity': identity, 'matched_inputs': info['matched'],
             'baseline_result': str(info['files']['B2']), 'exclusions': info['exclusions'],
             'apis': {name: {'status': 'pending'} for name in info['names']},
             'headline_credit': False, 'semantic_validation': 'needs_independent_review'}
    publish(out, state)
    return state


def publish(out, state):
    state['updated_at'] = datetime.now().astimezone().isoformat()
    state['statuses'] = dict(Counter(row['status'] for row in state['apis'].values()))
    state['native_recovery_by_round'] = {str(n): sum(
        row['status'] == 'recovered_native' and row.get('code_fix_rounds', 6) <= n
        for row in state['apis'].values()) for n in range(6)}
    state['observed_code_proposal_totals'] = {
        key: sum(row.get(key) or 0 for row in state['apis'].values())
        for key in ('code_fix_rounds', 'provider_events', 'diagnostic_block_events',
                    'wall_s', 'llm_calls', 'input_tokens', 'output_tokens')}
    save(Path(out) / 'summary.json', state)


def one(info, work, out, state, *, execute=True):
    """Return after at most one API; other repositories can then make progress."""
    pending = [name for name, row in state['apis'].items()
               if row['status'] not in TERMINAL and row.get('retry_after', 0) <= time.time()]
    if not pending:
        return False
    name = pending[0]
    state['active_api'] = name
    publish(out, state)
    try:
        base = load_config(info['config'])
        root = freeze(base, info['B2'], Path(work))
        cfg = load_config(root / 'configs' / info['config'].name)
        # B2 job inventories can be cell-specific or inherited from the frozen
        # controller. Select only an existing file with the recorded hash.
        import os
        expected = info['B2']['run']['fingerprint_components']['interpreter']['environment_sha256']
        choices = [info['inventory'], *sorted((base.root / 'docs/eval/setup').glob('environment_*.txt')),
                   Path(os.environ.get('AIDEAL_RECOVERY_ENV_INVENTORY', '/nonexistent'))]
        inventory = next((p for p in choices if p.is_file() and file_sha(p) == expected), None)
        if inventory is None:
            raise ValueError('no inventory binds the B2 runtime fingerprint')
        with environment(dict(os.environ, AIDEAL_RECOVERY_ENV_INVENTORY=str(inventory))):
            env, runtime = runtime_environment(base, cfg, info['B2'], info['repo'])
        save(Path(out) / 'runtime.json', runtime)
        preflight = run(cfg, base, info['B2'], name, 'source', 'docs/eval/api_manifest.json', execute=False)
        same_source_treatment(info['source'], preflight['identity'])
        # Same runner, prompts, stopping rule and native engine as S_A2. No
        # S_A2 code/diagnosis is supplied: round zero and context come from B2.
        with environment(env):
            row = run(cfg, base, info['B2'], name, 'source', 'docs/eval/api_manifest.json', execute=execute)
        for cell in ('A2', 'B2'):
            if file_sha(info['files'][cell]) != info['identity'][f'{cell}_sha256']:
                raise ValueError(f'{cell} native evidence changed during recovery')
        record = {'status': row['status'], 'code_fix_rounds': len(row.get('rounds', [])),
                  'provider_events': sum(e.get('category') == 'llm-error' for e in row.get('events', [])),
                  'diagnostic_block_events': sum(e.get('stage') == 'deep_dive' for e in row.get('events', [])),
                  'stop_reason': row.get('stop_reason'), 'identity': row.get('identity')}
        for key in ('wall_s', 'llm_calls', 'input_tokens', 'output_tokens'):
            record[key] = sum(r.get(key) or 0 for r in row.get('rounds', []))
        record['cost_scope'] = 'recorded code proposals only; diagnosis/provider evidence retained separately'
        record['retry_after'] = time.time() + 300 if row['status'] in ('provider_blocked', 'blocked') else 0
        case = Path(out) / 'cases' / (digest(name) + '.json')
        case.parent.mkdir(exist_ok=True)
        save(case, {**row, 'stage': 'S_B2', 'baseline_cell': 'B2'})
        record['evidence_file'] = str(case.relative_to(out))
        state['apis'][name] = record
        state['snapshot'] = str(root)
    except Exception as exc:
        state['apis'][name] = {'status': 'preflight_blocked', 'error': f'{type(exc).__name__}: {exc}',
                              'credit': False}
    finally:
        state.pop('active_api', None)
        publish(out, state)
    return True


def same_source_treatment(source, current):
    keys = ('mode', 'max_code_fix_rounds', 'stuck_rounds', 'runner_sha256', 'engine_sha256',
            'validation_sha256', 'compatibility_adapter_sha256', 'protocol_sha256',
            'prompt_sha256', 'context_engine')
    for row in source['apis'].values():
        prior = row.get('identity')
        if prior and any(prior[key] != current[key] for key in keys):
            raise ValueError('S_A2/S_B2 source prompt, engine or stopping policy differs')


def compare(info, state):
    """Paired descriptive endpoints; never replace the native B2 score."""
    a2, b2, source = info['A2']['metrics'], info['B2']['metrics'], info['source']['apis']
    source_names = set(cohort(info['A2'])[0])
    recovered = {name for name, row in state['apis'].items() if row['status'] == 'recovered_native'}
    rows = {}
    for name in a2:
        rows[name] = {'A2': a2[name]['status'], 'S_A2': source.get(name, {}).get('status',
                      'not_measured' if name in source_names else 'not_in_cohort'),
                      'B2': b2[name]['status'], 'S_B2': state['apis'].get(name, {}).get('status', 'not_in_cohort'),
                      'B2_regression': a2[name]['status'] == 'pass' and b2[name]['status'] != 'pass',
                      'S_A2_rounds': source.get(name, {}).get('code_fix_rounds'),
                      'S_B2_rounds': state['apis'].get(name, {}).get('code_fix_rounds')}
    return {'schema': 1, 'protocol': state['protocol'], 'identity': state['identity'],
            'full_manifest_N': len(a2), 'F_A2': len(source_names), 'F_B2': len(state['apis']),
            'B2_native_pass': sum(row['status'] == 'pass' for row in b2.values()),
            'S_B2_recovered': len(recovered),
            'B2_plus_S_B2_composite_native_pass': sum(row['status'] == 'pass' for row in b2.values()) + len(recovered),
            'on_F_A2': {'S_A2_recovered': sum(row.get('status') == 'recovered_native' for row in source.values()),
                        'B2_pass': sum(b2[n]['status'] == 'pass' for n in source_names),
                        'B2_plus_S_B2_pass': sum(b2[n]['status'] == 'pass' or n in recovered for n in source_names)},
            'apis': rows, 'interpretation': 'Paired descriptive outcomes on F_A2; conditional recovery on F_B2. '
                'Composite is not a fresh-reader score or an equal-cost causal effect. Native acceptance is not semantic certification.'}
