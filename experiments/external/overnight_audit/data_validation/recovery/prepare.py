"""Read-only priority-study audit and recovery queue; no execution/provider calls."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from aideal.config import load_config
from experiments.external.audit_experiment_data import SPECS
from .engine import POLICY, save
from .validation import eligible, file_sha, prompt_file

CELLS = ('A1', 'A2', 'B1', 'B2')


def prepare(base, report):
    findings, queue = {}, []
    health = json.loads((report / 'data_validation/automation/health.json').read_text())
    data = json.loads((report / 'data_validation/summary.json').read_text())
    for repo, (prefix, relative, _, count, _) in SPECS.items():
        suffix = '_full235' if repo == 'tslearn' else ''
        frozen = base / (prefix + ('_freeze' if repo == 'tslearn' else '_setup')) / relative
        cells, specs = {}, {}
        for cell in CELLS:
            root = base / f'{prefix}_{cell}' / relative
            name = f'configs/aideal_{cell}{suffix}.yaml'
            cfg = load_config(frozen / name)
            ex = dict(cfg.comprehension['execute'])
            for key in ('work_dir', 'output_dir'):
                ex.pop(key, None)
            specs[cell] = {'execute': ex, 'roles': cfg.roles, 'registry': cfg.raw['models']['registry'],
                           'class_context': cfg.comprehension.get('class_context'),
                           'relevant_doc_chars': cfg.comprehension.get('relevant_doc_chars'),
                           'profile_sha256': file_sha(frozen / cfg.raw['files']['project_profile']),
                           'prompt_sha256': file_sha(prompt_file(cfg, 'comprehension_write_exec'))}
            row = {'configured_code_fix_rounds': ex.get('max_fix_rounds'),
                   'frozen_config': str(frozen / name), 'worker_exists': root.exists(),
                   'input_audit': data.get(repo, {}).get(cell, {}), 'final_complete': False}
            if root.exists():
                row['effective_matches_frozen'] = load_config(root / name).raw == cfg.raw
            result_path = root / f'docs/eval/{cell}/comprehension.json'
            ledger_path = report / repo / cell / 'ledger.json'
            if ledger_path.exists():
                ledger = json.loads(ledger_path.read_text())
                row['final_complete'] = ledger['status'] == 'complete'
                row['ledger_sha256'] = file_sha(ledger_path)
            if result_path.exists():
                result = json.loads(result_path.read_text())
                row['result_sha256'] = file_sha(result_path)
                row['recorded_timeout_s'] = result.get('run', {}).get('timeout_s')
                for api in result.get('metrics', {}):
                    try:
                        eligible(result, api)
                    except ValueError:
                        continue
                    for mode in ('feedback', 'source'):
                        queue.append({'repo': repo, 'cell': cell, 'api': api, 'mode': mode,
                            'baseline_result': str(result_path), 'result_sha256': row['result_sha256'],
                            'status': 'staged', 'requires': ['isolated equivalent config',
                                'complete priority reports', 'preflight and semantic review']})
            cells[cell] = row
        problems = []
        for cell in CELLS:
            if specs[cell] != specs['A1']:
                problems.append(f'{cell}: frozen non-document protocol differs from A1')
            if cells[cell].get('effective_matches_frozen') is False:
                problems.append(f'{cell}: worker effective config differs from freeze')
            if cells[cell]['configured_code_fix_rounds'] != 0:
                problems.append(f'{cell}: configured code fixes are not zero')
        findings[repo] = {'apis': count, 'configuration_consistent': not problems,
                          'problems': problems, 'cells': cells}
    return {'version': 'aideal-recovery-v1', 'generated_at': datetime.now(timezone.utc).isoformat(),
            'protocol_sha256': file_sha(POLICY), 'execution_started': False,
            'admission': 'staged_until_priority_reports_complete',
            'headline_comparison': 'partial; final validation still required',
            'path_conflicts': health['path_conflicts'], 'observer_errors': health['errors'],
            'health_generated_at': health['generated_at'], 'repositories': findings, 'queue': queue}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--report-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True,
                        help='new snapshot directory, outside running observer namespaces')
    args = parser.parse_args()
    value = prepare(args.workspace_parent.resolve(), args.report_root.resolve())
    args.out.mkdir(parents=True, exist_ok=False)
    save(args.out / 'protocol_audit_and_queue.json', value)
    print(json.dumps({'snapshot': str(args.out), 'queued_pairs': len(value['queue']) // 2,
                      'configuration_consistent': {r: v['configuration_consistent']
                          for r, v in value['repositories'].items()}}, indent=2))


if __name__ == '__main__':
    main()
