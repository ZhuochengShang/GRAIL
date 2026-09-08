"""Read-only admission and matched-treatment checks for the extension."""
from pathlib import Path
import json

import yaml

from experiments.external.recovery.compatibility import components, fingerprint
from experiments.external.recovery.engine import digest, policy
from experiments.external.recovery.validation import eligible, file_sha

REPOSITORIES = {'mir_eval': ('GRAIL_mir_eval', 'experiments/external/mir_eval', 148),
                'thumbnailator': ('GRAIL_thumbnailator', 'experiments/external/thumbnailator', 149),
                'tslearn': ('GRAIL_tslearn_full235', 'experiments/tslearn', 235)}
TERMINAL = {'recovered_native', 'stuck', 'exhausted', 'infra_blocked', 'preflight_blocked'}


def read(path):
    return json.loads(Path(path).read_text())


def complete(result, count):
    run, rows = result['run'], result['metrics']
    if (result['doc_source'] != 'aideal' or run['max_fix_rounds'] != 0
            or len(rows) != count or run['api_count'] != count
            or any(r.get('status') not in ('pass', 'fail') or
                   r.get('error_category') == 'llm-error' for r in rows.values())):
        raise ValueError('requires a complete generated-document zero-fix result without provider failures')
    if fingerprint(run['fingerprint_components']) != run['experiment_fingerprint']:
        raise ValueError('native fingerprint does not bind recorded components')


def matched(a2, b2, count):
    for result in (a2, b2):
        complete(result, count)
    if set(a2['metrics']) != set(b2['metrics']):
        raise ValueError('A2/B2 API identity sets differ')
    left, lm = components(a2)
    right, rm = components(b2)
    keys = ('project', 'language', 'doc_source', 'doc_scope', 'max_fix_rounds',
            'manifest_sha256', 'models', 'class_context', 'timeout_s',
            'scaffold', 'source', 'fixtures', 'engine')
    for key in keys:
        if left[key] != right[key]:
            raise ValueError(f'A2/B2 mismatch: {key}')
    normalize = lambda ex: {k: v for k, v in ex.items() if k not in ('work_dir', 'output_dir')}
    if normalize(left['execute_config']) != normalize(right['execute_config']):
        raise ValueError('A2/B2 execution policy differs')
    for key in ('executable', 'version'):
        if left['interpreter'][key] != right['interpreter'][key]:
            raise ValueError(f'A2/B2 interpreter differs: {key}')
    return {'A2_compatibility': lm, 'B2_compatibility': rm,
            'environment_inventory_hashes': [p['interpreter']['environment_sha256'] for p in (left, right)],
            'limitation': 'Inventory paths/cell labels can differ; runtime packages/imports are checked separately. '
                          'Historical script binding and baseline semantic validity remain qualified.'}


def cohort(result):
    names, exclusions = [], {}
    for name, row in result['metrics'].items():
        try:
            eligible(result, name)
            names.append(name)
        except ValueError as exc:
            if row['status'] != 'pass':
                exclusions[name] = str(exc)
    return names, exclusions


def command_option(command, flag, expected):
    if command.count(flag) != 1 or command[command.index(flag) + 1] != expected:
        raise ValueError(f'B2 command must declare {flag} {expected}')


def inspect(repo, parent, upstream):
    """Only succeeded B2 jobs and a settled A2 source pass permit admission."""
    prefix, relative, count = REPOSITORIES[repo]
    roots = {cell: Path(parent) / f'{prefix}_{cell}' / relative for cell in ('A2', 'B2')}
    files = {cell: root / f'docs/eval/{cell}/comprehension.json' for cell, root in roots.items()}
    a2, b2 = (read(files[cell]) for cell in ('A2', 'B2'))
    proof = matched(a2, b2, count)
    upstream = Path(upstream) / repo
    plan_path = upstream / 'b2_watchdog.yaml'
    plan = yaml.safe_load(plan_path.read_text())
    jobs = {job['id']: job for job in plan['jobs']}
    states = read(plan_path.with_suffix('.state.json'))['jobs']
    if not jobs or any(states.get(job, {}).get('status') != 'succeeded' for job in jobs):
        raise ValueError('priority B2 jobs have not all succeeded')
    repair, fresh = jobs[f'{repo}_B2_repair'], jobs[f'{repo}_B2_zero']
    for flag, value in [('--from-results', 'docs/eval/A2/comprehension.json'),
                        ('--doc-rounds', '5'), ('--doc-stuck', '2'), ('--retry-rounds', '0')]:
        command_option(repair['command'], flag, value)
    command_option(fresh['command'], '--max-fix-rounds', '0')
    command_option(fresh['command'], '--doc', 'aideal')
    command_option(fresh['command'], '--doc-scope', 'relevant')
    if '--deep-dive-first' not in repair['command'] or '--create-missing' in repair['command']:
        raise ValueError('unexpected generated-document repair treatment')
    inherited = roots['B2'] / 'docs/eval/A2/comprehension.json'
    if file_sha(inherited) != file_sha(files['A2']):
        raise ValueError('README repair did not inherit the frozen A2 result')
    doc = read(roots['B2'] / 'docs/eval/B2/docfix.json')
    if (doc.get('attempted') is None or doc.get('processed') != doc['attempted'] or doc.get('blocked')
            or any(str(r.get('status', '')).startswith(('in-progress', 'llm-error'))
                   for r in doc.get('apis', {}).values())):
        raise ValueError('document repair is incomplete')
    source = read(upstream / 'source/summary.json')
    if any(row.get('status') not in TERMINAL for row in source['apis'].values()):
        raise ValueError('A2 source work/retries still pending; preserve its provider capacity')
    if source.get('identity'):
        if (source['identity']['baseline_sha256'] != file_sha(files['A2'])
                or source['identity']['protocol'] != policy()):
            raise ValueError('A2 source policy or baseline identity differs')
        if set(source['apis']) != set(cohort(a2)[0]):
            raise ValueError('A2 source denominator differs from eligible A2 failures')
    elif not source.get('statuses', {}).get('preflight_blocked'):
        raise ValueError('missing A2 source identity without a recorded preflight block')
    names, exclusions = cohort(b2)
    suffix = '_full235' if repo == 'tslearn' else ''
    inventory = Path(fresh['environment_inventory'])
    if not inventory.is_absolute():
        inventory = Path(fresh['cwd']) / inventory
    return {'repo': repo, 'root': roots['B2'], 'config': roots['B2'] / f'configs/aideal_B2{suffix}.yaml',
            'A2': a2, 'B2': b2, 'files': files, 'source': source, 'inventory': inventory,
            'names': names, 'exclusions': exclusions, 'matched': proof,
            'identity': {'A2_sha256': file_sha(files['A2']), 'B2_sha256': file_sha(files['B2']),
                         'cohort_sha256': digest(names), 'b2_plan_sha256': file_sha(plan_path)}}


def admission(parent, upstream):
    ready, blocked = {}, {}
    for repo in REPOSITORIES:
        try:
            ready[repo] = inspect(repo, parent, upstream)
        except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
            blocked[repo] = f'{type(exc).__name__}: {exc}'
    return ready, blocked
