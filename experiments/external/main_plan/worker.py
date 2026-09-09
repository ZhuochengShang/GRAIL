"""One isolated feedback-only worker; preserve all A2 failures in its denominator."""
import argparse
from collections import Counter
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import time

from aideal.config import load_config
from experiments.external.post_b2.admission import slot
from experiments.external.recovery.batch import environment
from experiments.external.recovery.engine import digest, save
from experiments.external.recovery.runner import run
from experiments.external.recovery.snapshot import freeze, runtime_environment
from experiments.external.recovery.validation import file_sha

POLICY = Path(__file__).with_name('protocol.yaml')
TERMINAL = {'recovered_native', 'stuck', 'exhausted', 'infra_blocked', 'evidence_blocked'}


def cohort(result):
    metrics, run_info = result.get('metrics', {}), result.get('run', {})
    if (not metrics or run_info.get('api_count') != len(metrics)
            or run_info.get('manifest_api_count') != len(metrics)
            or run_info.get('max_fix_rounds') != 0
            or result.get('doc_source') != 'aideal'
            or any(r.get('status') not in ('pass', 'fail') or
                   r.get('error_category') == 'llm-error' for r in metrics.values())):
        raise ValueError('A2 must be complete, zero-fix and provider-resolved')
    return sorted(n for n, r in metrics.items() if r['status'] == 'fail')


def publish(out, state):
    state['updated_at'] = datetime.now().astimezone().isoformat()
    state['statuses'] = dict(Counter(r['status'] for r in state['apis'].values()))
    state['complete'] = all(r['status'] in TERMINAL for r in state['apis'].values())
    state['native_recovery_by_round'] = {str(i): sum(
        r['status'] == 'recovered_native' and r.get('code_fix_rounds', 6) <= i
        for r in state['apis'].values()) for i in range(6)}
    save(out / 'summary.json', state)


def prepare(config, result_path, repo, work, out, manifest):
    result = json.loads(result_path.read_text())
    names = cohort(result)
    base = load_config(config)
    identity = {'baseline_sha256': file_sha(result_path), 'protocol_sha256': file_sha(POLICY),
                'worker_sha256': file_sha(Path(__file__)), 'repo': repo, 'manifest': manifest}
    path = out / 'summary.json'
    state = json.loads(path.read_text()) if path.exists() else {
        'stage': 'B2-1', 'mode': 'feedback', 'identity': identity,
        'baseline_result': str(result_path), 'cohort_sha256': digest(names),
        'cohort_count': len(names), 'baseline_manifest_count': len(result['metrics']),
        'apis': {n: {'status': 'pending'} for n in names},
        'source_diagnosis_calls': 0, 'native_scores_unchanged': True,
        'limitations': ['Native acceptance is not independent semantic validation.',
            'All A2 failures remain in the denominator, including dependency and evidence blockers.',
            'Historical baseline output state and full snippet association may be unavailable.']}
    if state['identity'] != identity:
        raise ValueError('registered inputs changed; preserve this namespace and register a new one')
    root = freeze(base, result, work)
    cfg = load_config(root / 'configs' / config.name)
    expected = result['run']['fingerprint_components']['interpreter']['environment_sha256']
    candidates = list((base.root / 'docs/eval/setup').glob('environment_*.txt'))
    if os.environ.get('AIDEAL_RECOVERY_ENV_INVENTORY'):
        candidates.append(Path(os.environ['AIDEAL_RECOVERY_ENV_INVENTORY']))
    inventory = next((p for p in candidates if p.is_file() and file_sha(p) == expected), None)
    if inventory is None:
        raise ValueError('no recorded inventory matches A2; do not silently replace the environment')
    with environment(dict(os.environ, AIDEAL_RECOVERY_ENV_INVENTORY=str(inventory),
                          AIDEAL_RECOVERY_PROTOCOL=str(POLICY))):
        env, runtime = runtime_environment(base, cfg, result, repo)
    save(out / 'runtime.json', runtime)
    save(out / 'A2_frozen.json', result)
    state['snapshot'] = str(root)
    # All APIs are preflighted before the first paid call. Failures stay visible.
    with environment(env):
        for name in names:
            if state['apis'][name]['status'] != 'pending':
                continue
            try:
                proof = run(cfg, base, result, name, 'feedback', manifest, execute=False)
                state['apis'][name] = {'status': 'ready', 'preflight': proof['identity']}
            except ValueError as exc:
                state['apis'][name] = {'status': 'evidence_blocked', 'error': str(exc)}
    publish(out, state)
    return base, cfg, result, env, state


def execute_one(base, cfg, result, env, state, out, manifest, name):
    state['active_api'] = name
    publish(out, state)
    try:
        with environment(env):
            record = run(cfg, base, result, name, 'feedback', manifest, execute=True)
        if record.get('diagnosis', {}).get('report_text'):
            raise ValueError('feedback arm unexpectedly contains source diagnosis')
        evidence = out / 'cases' / (digest(name)+'.json')
        evidence.parent.mkdir(exist_ok=True)
        save(evidence, record)
        state['apis'][name] = {'status': record['status'], 'code_fix_rounds': len(record['rounds']),
            'evidence_file': str(evidence.relative_to(out)), 'stop_reason': record.get('stop_reason'),
            'retry_after': time.time()+300 if record['status'] not in TERMINAL else 0}
    except ValueError as exc:
        state['apis'][name] = {'status': 'evidence_blocked', 'error': str(exc)}
    finally:
        state.pop('active_api', None)
        publish(out, state)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--result', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--upstream', type=Path, required=True)
    p.add_argument('--manifest', default='docs/eval/api_manifest.json')
    p.add_argument('--execute', action='store_true')
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.execute:
            while not args.result.exists():
                save(args.out / 'waiting.json', {'status': 'waiting_for_own_A2', 'result': str(args.result),
                                                'epoch': time.time()})
                time.sleep(30)
        base, cfg, result, env, state = prepare(args.config, args.result, args.repo,
                                               args.work, args.out, args.manifest)
        if not args.execute:
            print(json.dumps({'preflight': state['statuses'], 'cohort': state['cohort_count']}))
            return
        while not state['complete']:
            names = [n for n, r in state['apis'].items() if r['status'] not in TERMINAL
                     and r.get('retry_after', 0) <= time.time()]
            for name in names:
                with environment(env), slot(args.upstream, f'B2-1 feedback {args.repo}/{name}') as admitted:
                    if not admitted:
                        break
                    if file_sha(args.result) != state['identity']['baseline_sha256']:
                        raise ValueError('A2 changed during execution; stop without replacing evidence')
                    execute_one(base, cfg, result, env, state, args.out, args.manifest, name)
            if not state['complete']:
                time.sleep(30)
        print(json.dumps({'complete': True, 'statuses': state['statuses']}), flush=True)


if __name__ == '__main__':
    main()
