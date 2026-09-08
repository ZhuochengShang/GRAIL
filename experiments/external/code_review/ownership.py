"""Read-only snapshot of declared writers and live supervisor evidence.

This is an audit of discovered plans, not an OS sandbox or a proof about every
open file. It never imports a provider, launches an experiment, or signals a PID.
"""
import argparse
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
import subprocess
import time

import yaml


def inspect(parent):
    main = parent / 'GRAIL_rdpro_puzzle_aideal'
    audit = parent / 'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation'
    paths = set(main.glob('experiments/external/*watchdog.state.json'))
    paths.update(parent.glob('*baselines_watchdog.state.json'))
    paths.update((parent/'GRAIL_tslearn_full235_freeze/experiments/tslearn/docs/eval/watchdogs').glob('*.state.json'))
    paths.update(audit.glob('pipeline_v*/**/*watchdog.state.json'))
    process = subprocess.run(['ps', '-axo', 'pid,ppid,lstart,etime,state,command'],
                             capture_output=True, text=True, check=True)
    lines = {int(line.split()[0]): line.strip() for line in process.stdout.splitlines()[1:] if line.strip()}
    jobs, problems, states = [], [], []
    owners = defaultdict(set)
    for path in sorted(paths):
        try:
            state = json.loads(path.read_text())
            plan_path = Path(state.get('plan') or str(path).replace('.state.json', '.yaml'))
            plan = yaml.safe_load(plan_path.read_text())
            specs = {j['id']: j for j in plan.get('jobs', [])}
            states.append({'path': str(path), 'status': state.get('status'),
                           'heartbeat_age_s': round(time.time()-state.get('heartbeat_epoch', 0), 1)})
            for name, row in state.get('jobs', {}).items():
                if row.get('status') != 'running':
                    continue
                spec = specs[name]
                cwd = Path(spec['cwd'])
                cwd = (plan_path.parent/cwd).resolve() if not cwd.is_absolute() else cwd.resolve()
                result = Path(spec.get('result', '.aideal_exec/watchdog.stdout'))
                result = result if result.is_absolute() else cwd/result
                pid = row.get('pid')
                env = {**plan.get('env', {}), **spec.get('env', {})}
                item = {'id': name, 'pid': pid, 'process_present': pid in lines,
                        'state': str(path), 'cwd': str(cwd), 'result': str(result),
                        'attempts': row.get('attempts'), 'started_at': row.get('started_at'),
                        'plan_rate_gate': env.get('AIDEAL_GOOGLE_RATE_STATE', '/tmp/aideal_google_rate_gate.txt'),
                        'plan_min_interval_s': env.get('AIDEAL_GOOGLE_MIN_INTERVAL_S', 3),
                        'declared_writes': [str(result), str(result)+'.tmp'],
                        'configured_inputs': {}, 'config': None}
                command = spec['command']
                if isinstance(command, list) and '--config' in command:
                    config = Path(command[command.index('--config')+1])
                    config = config if config.is_absolute() else cwd/config
                    from aideal.config import load_config
                    cfg = load_config(config)
                    item['config'] = str(config)
                    execute = cfg.comprehension.get('execute', {})
                    for key in ('work_dir', 'output_dir'):
                        if execute.get(key):
                            item['declared_writes'].append(str((cfg.root/execute[key]).resolve()))
                    for key, value in execute.get('sample_data', {}).items():
                        if isinstance(value, str):
                            item['configured_inputs'][key] = {'value': value,
                                'exists_relative_to_project': (cfg.root/value).exists()}
                    if 'fix-docs' in command:
                        item['declared_writes'].append(str(cfg.llm_readme.resolve()))
                for output in item['declared_writes']:
                    owners[str(Path(output).resolve())].add(str(pid))
                stderr = result.with_suffix(result.suffix+'.stderr.log')
                if stderr.exists():
                    with stderr.open('rb') as stream:
                        stream.seek(max(0, stderr.stat().st_size-1500))
                        item['stderr_tail'] = stream.read().decode(errors='replace')
                jobs.append(item)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append({'state': str(path), 'error': f'{type(exc).__name__}: {exc}'})
    collisions = []
    outputs = sorted(owners)
    for i, left in enumerate(outputs):
        for right in outputs[i:]:
            if (left == right or Path(left) in Path(right).parents) and len(owners[left] | owners[right]) > 1:
                collisions.append({'left': left, 'right': right, 'pids': sorted(owners[left] | owners[right])})
    return {'updated_at': datetime.now().astimezone().isoformat(), 'jobs': jobs, 'states': states,
            'declared_write_conflicts': collisions, 'inspection_errors': problems,
            'limitations': ['Only discovered supervisor plans are covered; arbitrary generated writes are not contained.',
                'PID presence alone is not process identity or proof of activity.',
                'Rate settings are declared plan/default values; inherited environment and account-wide usage are not observed.',
                'A sample_data value can be an output destination or literal; an absent path is not automatically a fixture defect.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    data = inspect(args.workspace_parent)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps({'updated_at': data['updated_at'], 'running_jobs': len(data['jobs']),
                      'conflicts': data['declared_write_conflicts'], 'errors': data['inspection_errors']}))


if __name__ == '__main__':
    main()
