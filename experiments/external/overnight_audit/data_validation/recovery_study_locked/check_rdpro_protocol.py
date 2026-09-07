"""Read-only static parity check against the corrected RDPro runner.

Checks selected core function implementations and literal launch limits. It does
not execute drivers, certify completed artifacts, or compare unlike repositories'
datasets. Missing inputs or changed implementations fail closed.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import yaml

FUNCTIONS = {'docfix.py': ('doc_fix_run', '_diag_sig', '_err_sig'),
             'deepdive.py': ('deep_dive_run',),
             'doc_checks.py': ('_comprehension_execute',)}
FLAGS = {'--max-fix-rounds': '0', '--doc-rounds': '5', '--doc-stuck': '2',
         '--retry-rounds': '0', '--doc-scope': 'relevant'}


def functions(worktree):
    result = {}
    for filename, names in FUNCTIONS.items():
        path = worktree/'grail-agent/src/aideal'/filename
        tree = ast.parse(path.read_text())
        nodes = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name in names:
            result[name] = hashlib.sha256(ast.dump(nodes[name], include_attributes=False).encode()).hexdigest()
    return result


def launch_flags(paths):
    sequences = []
    for path in paths:
        if path.suffix == '.yaml':
            sequences += [j['command'] for j in yaml.safe_load(path.read_text())['jobs']]
        else:
            tree = ast.parse(path.read_text())
            sequences += [[n.value if isinstance(n, ast.Constant) else None for n in node.elts]
                          for node in ast.walk(tree) if isinstance(node, (ast.List, ast.Tuple))]
    found = {flag: sorted({str(s[i+1]) for s in sequences for i, v in enumerate(s[:-1])
                          if v == flag}) for flag in FLAGS}
    found['--deep-dive-first'] = any('--deep-dive-first' in s for s in sequences)
    ok = found['--deep-dive-first'] and all(found[k] == [v] for k, v in FLAGS.items())
    return {'matches_registered_limits': ok, 'observed': found,
            'inputs': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def inspect(base, main):
    reference = base/'GRAIL_rdpro_2x2_runner'
    expected = functions(reference)
    workers = ['GRAIL_mir_eval_A1', 'GRAIL_mir_eval_A2',
               'GRAIL_thumbnailator_A1', 'GRAIL_thumbnailator_A2',
               'GRAIL_tslearn_full235_A1', 'GRAIL_tslearn_full235_A2',
               'GRAIL_mir_eval_setup', 'GRAIL_thumbnailator_setup',
               'GRAIL_tslearn_full235_freeze', 'GRAIL_mdanalysis_full1032_freeze']
    rows = {n: functions(base/n) for n in workers}
    drivers = {
        'RDPro_corrected': [reference/'experiments/rdpro/run_rdpro_2x2_pipeline.py'],
        'mir_eval_and_thumbnailator': [main/'experiments/external/run_external_2x2_pipeline.py'],
        'tslearn': [base/'GRAIL_tslearn_full235_freeze/experiments/tslearn/run_full235_pipeline.py'],
        'MDAnalysis_queued': [base/'GRAIL_mdanalysis_full1032_freeze/experiments/mdanalysis/docs/full_1032/setup'/n
                             for n in ('baseline_watchdog.yaml', 'repair_watchdog.yaml')]}
    limits = {name: launch_flags(paths) for name, paths in drivers.items()}
    same = {name: row == expected for name, row in rows.items()}
    return {'checked_at': datetime.now(timezone.utc).isoformat(),
            'scope': 'static selected-function and launch-limit parity; final results still require validation',
            'reference': str(reference), 'reference_function_sha256': expected,
            'worker_function_sha256': rows, 'matches_corrected_rdpro': same,
            'launch_limits': limits, 'passed': all(same.values()) and
                all(v['matches_registered_limits'] for v in limits.values()),
            'historical_retained_rdpro': {n: functions(base/n) for n in
                ('GRAIL_rdpro_final_B1', 'GRAIL_rdpro_final_B2')}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main-worktree', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args.main_worktree.resolve().parent, args.main_worktree.resolve())
    with args.out.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'passed': result['passed'], 'out': str(args.out)}))
    raise SystemExit(0 if result['passed'] else 2)


if __name__ == '__main__':
    main()
