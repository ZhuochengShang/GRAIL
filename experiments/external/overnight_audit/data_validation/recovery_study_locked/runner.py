"""Preflight or explicitly execute one isolated, versioned snippet recovery."""
from __future__ import annotations

import argparse
from copy import deepcopy
import fcntl
import json
from pathlib import Path
import sys

from aideal.config import load_config
from aideal.deepdive import deep_dive_run
from aideal.doc_checks import comprehension_check
from aideal.error_log import ErrorLog

from .engine import digest, policy, recover, save
from .validation import file_sha, prompt_file, validate


def isolated_config(cfg, out, prompt):
    cfg = deepcopy(cfg)
    cfg.error_log = out / 'error_log.jsonl'
    cfg.raw.setdefault('files', {})['prompts_dir'] = str(out / 'prompts')
    ex = cfg.comprehension['execute']
    ex['work_dir'] = str(out / 'work')
    ex['output_dir'] = str(out / 'output')
    cfg.raw['comprehension'] = cfg.comprehension
    # Every proposal uses the same fixer role, including its first attempt.
    spec = cfg.model_for_role('fixer')
    cfg.override_role('audience', f'{spec.provider}:{spec.model}')
    path = out / 'prompts/aideal/comprehension_write_exec.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt)
    return cfg


def run(cfg, base, result, api, mode, manifest, *, execute=False, max_rounds=5, stuck=2):
    if mode not in ('feedback', 'source'):
        raise ValueError('mode must be feedback or source')
    accepted = policy()
    if (max_rounds != accepted['max_code_fix_rounds'] or stuck != accepted['stuck_rounds']):
        raise ValueError('study limits are fixed at the protocol YAML values; alternatives require a separate protocol')
    if not 1 <= max_rounds <= 5 or not 0 <= stuck <= max_rounds:
        raise ValueError('require 1..5 code rounds and stuck threshold 0..max_rounds')
    identity, initial = validate(base, cfg, result, api, manifest)
    identity.update(mode=mode, max_code_fix_rounds=max_rounds, stuck_rounds=stuck,
                    runner_sha256=file_sha(Path(__file__)),
                    engine_sha256=file_sha(Path(__file__).with_name('engine.py')),
                    validation_sha256=file_sha(Path(__file__).with_name('validation.py')))
    if not execute:
        return {'status': 'preflight_passed', 'identity': identity,
                'admission': 'staged; run only after priority four-cell reports',
                'limitations': ['saved script association and runtime packages need review',
                                'passing generated assertions require independent semantic review']}
    expected = result['run']['fingerprint_components']['interpreter']
    if sys.version != expected['version'] or sys.executable != expected['executable']:
        raise ValueError('AIDEAL interpreter differs from baseline')
    import os
    # Retain the account-wide gate. Never invent a recovery-specific quota pool.
    if cfg.model_for_role('fixer').provider == 'google':
        if not os.environ.get('AIDEAL_GOOGLE_RATE_STATE') or float(os.environ.get('AIDEAL_GOOGLE_MIN_INTERVAL_S', '0')) < 3:
            raise ValueError('set the existing shared Google rate-state path and interval >=3s')
    if os.environ.get('AIDEAL_ENV_FINGERPRINT') != expected['environment_sha256']:
        raise ValueError('supply the validated baseline-compatible environment fingerprint')
    out = cfg.root / '.aideal_recovery' / digest(identity)
    if cfg.root not in out.resolve().parents:
        raise ValueError('recovery output escapes its isolated project root')
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        source_prompt = prompt_file(cfg, 'comprehension_write_exec').read_text()
        if mode == 'source':
            phrase = 'Use ONLY the documentation provided.'
            if phrase not in source_prompt:
                raise ValueError('custom prompt requires an explicit reviewed source-recovery adaptation')
            source_prompt = source_prompt.replace(phrase,
                'Use the documentation and the supplied source-grounded diagnosis. '
                'Treat its inferences as unverified; do not invent unavailable APIs.')
        source_prompt += ('\n\nRecovery boundary: repair the API-use snippet only. '
                          'Keep the fixtures, preloaded values, harness and library unchanged. '
                          'Do not weaken checks, bypass the target call, or replace an assertion '
                          'with a success print. Report success through the existing witness.\n')

        def diagnose():
            if mode == 'feedback':
                return {'mode': mode, 'report_text': '', 'llm_calls': 0}
            cached = out / 'diagnosis.json'
            if cached.exists():
                return json.loads(cached.read_text())
            dc = deepcopy(cfg)
            dc.error_log = out / 'diagnosis_error_log.jsonl'
            if not dc.error_log.exists():
                ErrorLog(dc.error_log).append(run_id=identity['baseline_fingerprint'],
                    step='recovery-baseline', language=cfg.language, task='API recovery',
                    status='fail', function=api, error_category=initial['category'],
                    error=initial['error'], code=initial['code'])
            from aideal.docfix import _source_window
            window, _ = _source_window(dc, api)
            if 'definition not found' in window:
                raise ValueError('canonical API source context unavailable')
            row = deep_dive_run(dc, api, out_dir=str(out / 'deepdive'), return_text=True)
            row['report_sha256'] = file_sha(row['report'])
            save(cached, row)
            return row

        def attempt(number, previous, diagnosis):
            folder = out / f'round_{number:02d}'
            folder.mkdir(exist_ok=True)
            # Preserve every provider attempt and script; never overwrite a round.
            existing = sorted(folder.glob('attempt_*/result.json'))
            if existing:
                row = json.loads(existing[-1].read_text())
                if row.get('category') != 'llm-error':
                    return row
            used = list(folder.glob('attempt_*'))
            invocation = folder / f'attempt_{len(used) + 1:04d}'
            current = isolated_config(cfg, invocation, source_prompt)
            ex = current.comprehension['execute']
            ex['exec_hints'] = (ex.get('exec_hints', '') + '\n\nPREVIOUS SAVED TEST:\n'
                + previous['code'] + '\nEXECUTION FAILURE:\n' + previous.get('error', '')
                + '\nSOURCE DIAGNOSIS:\n' + diagnosis.get('report_text', ''))
            native = comprehension_check(current, execute=True, show_code=True, api=api,
                doc_source=result['doc_source'], doc_scope=result['run']['doc_scope'],
                class_context=result['run']['class_context'], max_fix_rounds=0,
                timeout_s=result['run']['timeout_s'], resume=False, manifest=manifest)
            save(invocation / 'native_result.json', native)
            metric = native.get('metrics', {}).get(api)
            if not metric:
                raise ValueError(f'no native result for {api}; inspect {invocation}')
            script = Path(ex['work_dir']) / f'run_{api}' / ex['test_filename']
            row = {'status': metric['status'], 'category': metric.get('error_category'),
                   'error': metric.get('error', ''), 'code': script.read_text() if script.exists() else previous['code'],
                   'native_result': str(invocation / 'native_result.json'),
                   'script_sha256': file_sha(script) if script.exists() else None,
                   'wall_s': metric.get('wall_s'), 'llm_calls': metric.get('llm_calls'),
                   'input_tokens': metric.get('input_tokens'), 'output_tokens': metric.get('output_tokens')}
            # Unexpected changes invalidate this attempt instead of earning credit.
            validate(base, cfg, result, api, manifest)
            save(invocation / 'result.json', row)
            return row

        state = recover(identity, initial, out, diagnose=diagnose, attempt=attempt,
                        max_rounds=max_rounds, stuck=stuck)
        return {**state, 'report': str(out / 'recovery.json')}


def main():
    defaults = policy()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-config', required=True)
    parser.add_argument('--baseline-result', type=Path, required=True)
    parser.add_argument('--config', required=True, help='equivalent config in an isolated copy/worktree')
    parser.add_argument('--manifest', default='docs/eval/api_manifest.json')
    parser.add_argument('--api', required=True)
    parser.add_argument('--mode', choices=('feedback', 'source'), required=True)
    parser.add_argument('--execute', action='store_true', help='otherwise only inspect inputs; no model calls')
    parser.add_argument('--max-rounds', type=int, default=defaults['max_code_fix_rounds'])
    parser.add_argument('--stuck-rounds', type=int, default=defaults['stuck_rounds'],
                        help='must match the accepted protocol YAML value (2 for this study)')
    args = parser.parse_args()
    result = json.loads(args.baseline_result.read_text())
    print(json.dumps(run(load_config(args.config), load_config(args.baseline_config),
        result, args.api, args.mode, args.manifest, execute=args.execute,
        max_rounds=args.max_rounds, stuck=args.stuck_rounds), indent=2))


if __name__ == '__main__':
    main()
