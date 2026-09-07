"""Observe existing evidence. Never start experiments, run snippets, or call LLMs."""
from __future__ import annotations

import argparse
from datetime import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import time

import yaml
from aideal.config import load_config, DEFAULTS_PATH, _resolve_adapter
from aideal.doc_checks import _execute_sample_data
from experiments.external.audit_experiment_data import SPECS
from experiments.external.audit_overnight import atomic, dump, DEADLINE

from experiments.external.automation.analysis import forecast, classify, overlaps
from experiments.external.automation.contracts import lint_python

CELLS = ('A1', 'A2', 'B1', 'B2')


def read(path):
    # Malformed/missing evidence is surfaced by the caller, never interpreted
    # as a successful empty result.
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def redact(value):
    if isinstance(value, dict):
        return {k: '[REDACTED]' if any(s in k.lower() for s in
                ('api_key', 'password', 'secret', 'authorization', 'access_token'))
                else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def bundle(base, repo, cell, out):
    prefix, relative, _, _, _ = SPECS[repo]
    wt = base / f'{prefix}_{cell}'
    if not wt.exists():
        return {'status': 'pending'}, []
    root = wt / relative
    suffix = '_full235' if repo == 'tslearn' else ''
    path = root / f'configs/aideal_{cell}{suffix}.yaml'
    cfg = load_config(path)
    ex = cfg.comprehension['execute']
    frozen_root = base / (prefix + ('_freeze' if repo == 'tslearn' else '_setup')) / relative
    frozen = load_config(frozen_root / path.relative_to(root))
    profile = root / cfg.raw['files']['project_profile']
    frozen_profile = frozen_root / frozen.raw['files']['project_profile']
    bindings, _, warnings = _execute_sample_data(cfg, ex)
    # Record the actual loader's direct layers; do not invent recursive extends
    # semantics that the current configuration loader does not implement.
    layers = [DEFAULTS_PATH]
    raw = yaml.safe_load(path.read_text())
    for name in raw.get('extends', []):
        layer = _resolve_adapter(name, path.parent)
        if layer is None:
            warnings.append(f'unresolved direct config layer: {name}')
        else:
            layers.append(layer)
    layers.append(path)
    owner = f'{repo}/{cell}'
    owned = [(owner, (root / str(p)).resolve()) for p in
             (ex['work_dir'], bindings['output_dir'], cfg.llm_readme, cfg.error_log)]
    if any(wt.resolve() not in p.parents for _, p in owned):
        warnings.append('mutable path escapes its condition worktree')
    inventory = root / f'docs/eval/setup/environment_{cell}.txt'
    if inventory.is_file():
        atomic(out / repo / cell / 'environment_inventory.txt', inventory.read_text())
    evidence_path = out.parent / repo / cell / 'data_evidence.json'
    evidence = read(evidence_path) if evidence_path.exists() else {}
    script_checks = []
    for row in evidence.get('api_test_evidence', []):
        script = Path(row.get('script', ''))
        source = str(row.get('declared_source') or '').split(':')[0]
        if script.suffix != '.py' or not script.is_file() or not source.endswith('.py'):
            continue
        parts = Path(source).with_suffix('').parts
        # Remove checkout prefix, retain module namespace. Repeated method names
        # remain only candidate identities until owner-specific review.
        target = '.'.join((*parts[1:], row['api']))
        code = script.read_text()
        script_checks.append({'api': row['api'], 'script': str(script),
                              'sha256': hashlib.sha256(code.encode()).hexdigest(),
                              **lint_python(code, target)})
    dump(out / repo / cell / 'python_assertion_review.json', script_checks)
    result = {'status': 'checked', 'root': str(root), 'config': str(path),
              'config_layers': [{'path': str(p), 'sha256': sha(p)} for p in layers],
              'effective_config_sha256': hashlib.sha256(json.dumps(cfg.raw, sort_keys=True).encode()).hexdigest(),
              'effective_matches_frozen': cfg.raw == frozen.raw,
              'effective_profile': str(profile), 'profile_sha256': sha(profile),
              'profile_matches_frozen': sha(profile) == sha(frozen_profile),
              'execution_command': ex.get('command'), 'bindings': bindings,
              'fixture_identity_evidence': evidence.get('fixture_bindings', {}),
              'inventory': {'path': str(inventory), 'sha256': sha(inventory) if inventory.exists() else None,
                            'scope': 'recorded per-cell inventory, not fresh attestation of all imports'},
              'warnings': warnings}
    if warnings or not result['effective_matches_frozen'] or not result['profile_matches_frozen']:
        result['status'] = 'needs_review'
    atomic(out / repo / cell / 'resolved_config.yaml', yaml.safe_dump(redact(cfg.raw), sort_keys=False))
    dump(out / repo / cell / 'config_bundle.json', result)
    return result, owned


def observe(base, report, out):
    now = time.time()
    forecasts, configs, queue, owners, errors = {}, {}, [], [], []
    for repo in SPECS:
        forecasts[repo], configs[repo] = {}, {}
        for cell in CELLS:
            try:
                ledger_path = report / repo / cell / 'ledger.json'
                ledger = read(ledger_path)
                forecasts[repo][cell] = forecast(ledger)
                forecasts[repo][cell]['ledger_sha256'] = sha(ledger_path)
                for row in ledger['rows']:
                    if row.get('status') != 'fail':
                        continue
                    category, confidence, next_check = classify(row)
                    queue.append({'repository': repo, 'cell': cell, 'api': row['api'],
                                  'candidate_category': category, 'confidence': confidence,
                                  'next_check': next_check, 'native_category': row.get('runner_category'),
                                  'existing_review_category': row.get('primary_category'),
                                  'error': row.get('error'), 'source': row.get('source'),
                                  'checkpoint_attempts': row.get('checkpoint_attempts'),
                                  'provider_error_attempts': row.get('provider_error_attempts'),
                                  'doc_rounds_used': row.get('doc_rounds_used'),
                                  'fingerprint': ledger.get('fingerprint'),
                                  'ledger_sha256': forecasts[repo][cell]['ledger_sha256'],
                                  'decision': 'reviewed evidence retained' if confidence == 'reviewed' else 'candidate only; native score unchanged'})
                configs[repo][cell], paths = bundle(base, repo, cell, out)
                owners.extend(paths)
            except Exception as exc:
                errors.append(f'{repo}/{cell}: {type(exc).__name__}: {exc}')
    conflicts = overlaps(owners)
    heartbeat = {}
    for name, path in [('results', report/'heartbeat.json'), ('data', out.parent/'heartbeat.json')]:
        try:
            row = read(path)
            epoch = row.get('epoch') or datetime.fromisoformat(row['time']).timestamp()
            heartbeat[name] = {'age_seconds': round(now-epoch, 1), 'stale': now-epoch > 180}
        except Exception as exc:
            heartbeat[name] = {'stale': True, 'error': str(exc)}
    full_complete = all(forecasts.get(r, {}).get(c, {}).get('state') == 'complete' for r in SPECS for c in CELLS)
    health = {'generated_at': datetime.now(DEADLINE.tzinfo).isoformat(),
              'hours_to_deadline': (DEADLINE.timestamp()-now)/3600,
              'upstream_observers': heartbeat, 'errors': errors, 'path_conflicts': conflicts,
              'measurement_cells_complete': full_complete,
              'full_pipeline_eta': None,
              'full_pipeline_eta_reason': 'Generation, document repair, and post-treatment validation lack a complete observed timing model; cell estimates must not be presented as total completion forecasts.'}
    health['deadline_risks'] = [f'{r}/{c}: {f["state"]}' for r, cells in forecasts.items() for c, f in cells.items()
                                if f.get('state') == 'stalled_no_recent_terminal_outcomes' or
                                (f.get('hours') and f['hours']['likely'] > max(0,health['hours_to_deadline']))]
    dump(out/'deadline_forecast.json', forecasts)
    dump(out/'failure_review_queue.json', queue)
    dump(out/'health.json', health)
    dump(out/'config_bundles.json', configs)
    # A bounded progress history supports observed throughput without relying
    # on file mtime as an API event timestamp or mixing experiment fingerprints.
    history_path = out/'progress_history.json'
    history = read(history_path) if history_path.exists() else []
    history.append({'epoch': now, 'cells': {f'{r}/{c}': {'remaining': f.get('remaining_apis'),
                    'ledger_sha256': f.get('ledger_sha256')} for r, cells in forecasts.items() for c, f in cells.items()}})
    dump(history_path, history[-2880:])
    lines = ['# Automation status and deadline forecast', '',
             f"Updated: {health['generated_at']}. Hours to Wednesday 11 AM: {health['hours_to_deadline']:.2f}.", '',
             '**Whole-pipeline completion time remains unverified.** Estimates below cover remaining comprehension only; generation, document repair, and final validation are additional. Scenarios are not confidence intervals.', '',
             '| Repository/cell | Remaining APIs | State | Optimistic / likely / conservative hours |', '|---|---:|---|---|']
    for repo, cells in forecasts.items():
        for cell, f in cells.items():
            hrs = f.get('hours')
            values = ' / '.join(f'{hrs[k]:.2f}' for k in ('optimistic','likely','conservative')) if hrs else 'unknown'
            lines.append(f"| {repo}/{cell} | {f['remaining_apis']} | {f['state']} | {values} |")
    lines += ['', f'Failure review queue: {len(queue)} entries. Mutable cross-condition path conflicts: {len(conflicts)}.',
              'Deadline risks: ' + ('; '.join(health['deadline_risks']) or 'No estimated comprehension stage exceeds available time; unmeasured stages still prevent a whole-pipeline assurance.'),
              f'Observation errors: {len(errors)}. Observer health: `{json.dumps(heartbeat)}`.', '',
              '- [Failure review queue](failure_review_queue.json): suggested causes, evidence, confidence, attempts and repair rounds.',
              '- [Resolved configuration bundles](config_bundles.json): actual profile, direct YAML layers, fixture bindings and recorded environments.',
              '- Each populated Python cell also has `python_assertion_review.json`: AST call candidates, missing assertions, and trivial checks. This never executes snippets or certifies their semantics.',
              '- [Health and path ownership](health.json)',
              '- [Data and API-test methods](../FINAL_REPORT_DATA_AND_API_METHODS.md)',
              '- [Measured results and release decisions](../../FINAL_REPORT_WITH_DATA_CHECKS.md)', '',
              'No generated test, experiment command, provider request, scoring mutation, or job restart is performed by this observer.', '']
    atomic(out/'AUTOMATION_STATUS.md', '\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--report-root', type=Path, required=True)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    report = args.report_root.resolve()
    out = report/'data_validation/automation'
    out.mkdir(parents=True, exist_ok=True)
    with (out/'observer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        atomic(out/'.gitignore', 'observer.lock\nobserver.log\nheartbeat.json\n')
        while True:
            try:
                observe(args.workspace_parent.resolve(), report, out)
                dump(out/'heartbeat.json', {'pid': os.getpid(), 'epoch': time.time(), 'status': 'ok'})
            except Exception as exc:
                dump(out/'heartbeat.json', {'pid': os.getpid(), 'epoch': time.time(), 'status': 'error', 'error': str(exc)})
                if not args.watch:
                    raise
            if not args.watch:
                return
            time.sleep(60)


if __name__ == '__main__':
    main()
