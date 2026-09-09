"""Run only newly registered RDPro cells under shared supplemental admission."""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import threading
import time

from aideal.config import load_config
from aideal.doc_checks import comprehension_check
from aideal.docfix import doc_fix_run
from experiments.external.main_plan.worker import cohort
from experiments.external.post_b2.admission import slot
from experiments.external.recovery.engine import save
from experiments.external.recovery.validation import file_sha
from .feedback import feedback
from .report import read, render


def priority_ready(out):
    main = out.parent / 'main_plan_v5'
    return all(read(main/repo/'summary.json').get('complete') is True
               for repo in ('mir_eval', 'thumbnailator', 'tslearn'))


def verify(root):
    evidence = read(root/'docs/main_v5/build_identity.json')
    if not evidence.get('upstream_passed') or not evidence.get('smoke_passed'):
        raise ValueError('Pinned build, upstream tests and fixture smoke must pass before Gemini')
    for relative, expected in evidence['artifacts'].items():
        if file_sha(root/relative) != expected:
            raise ValueError('Built artifact changed: '+relative)
    for relative, expected in evidence['inputs'].items():
        if file_sha(root/relative) != expected:
            raise ValueError('Frozen baseline input changed: '+relative)


@contextmanager
def report_updates(root, out, action):
    stop = threading.Event()
    def update():
        while not stop.is_set():
            try:
                render(root, out, action)
            except Exception as exc:
                print('Passive report error: '+str(exc), flush=True)
            stop.wait(30)
    thread = threading.Thread(target=update, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop.set()
        thread.join()
        render(root, out, action)


def b2_project(root):
    target = root.parents[2]/'AIDEAL_rdpro_v5_B2/project'
    marker = target.parent/'initialized.json'
    if marker.exists():
        if read(marker)['A2_sha256'] != file_sha(root/'docs/main_v5/A2.json'):
            raise ValueError('B2 belongs to a different A2')
        return target
    if target.exists():
        raise ValueError('Incomplete B2 copy: inspect before resuming')
    shutil.copytree(root, target, symlinks=False,
                    ignore=shutil.ignore_patterns('.git', '.aideal_exec', '.aideal_recovery', 'logs'))
    baseline = read(root/'docs/main_v5/A2.json')
    failures = cohort(baseline)
    base = load_config(root/'configs/aideal.main_v5.yaml')
    ex = base.comprehension['execute']
    from aideal.error_log import ErrorLog
    log = ErrorLog(target/'logs/main_v5.jsonl')
    for name in failures:
        script = root/ex['work_dir']/('run_'+name)/ex['test_filename']
        if not script.exists():
            raise ValueError('Missing A2 failure script: '+name)
        code = script.read_text()
        begin, end = ex['region']
        code = code.split(begin,1)[1].split(end,1)[0]
        metric = baseline['metrics'][name]
        log.append(run_id=baseline['run']['run_id'], step='frozen-A2-failure',
            language='Scala', function=name, status='fail', round=0,
            error_category=metric.get('error_category'),
            error=(metric.get('error') or '').replace(str(root),str(target)),
            code=code.replace(str(root),str(target)),
            provenance_sha256=file_sha(root/'docs/main_v5/A2.json'),
            script_sha256=file_sha(script))
    save(marker, {'A2_sha256' : file_sha(root/'docs/main_v5/A2.json'),
                  'initial_readme_sha256': file_sha(root/'docs/main_v5/LLM_readme.md')})
    return target


def perform(action, root, out):
    current = root if action == 'A2' else b2_project(root)
    cfg = load_config(current/'configs/aideal.main_v5.yaml')
    if action != 'A2':
        label = 'docfix' if action == 'repair' else 'B2'
        cfg.comprehension['execute']['work_dir'] = '.aideal_exec/'+label
        cfg.comprehension['execute']['output_dir'] = '.aideal_exec/'+label+'/output'
        cfg.raw['comprehension'] = cfg.comprehension
    if action == 'repair':
        baseline = root/'docs/main_v5/A2.json'
        failures = cohort(read(baseline))
        dry = doc_fix_run(cfg, from_results=baseline, dry_run=True)
        if set(dry['targets']) != set(failures):
            raise ValueError('B2-2 cohort differs from frozen A2 failures')
        result = doc_fix_run(cfg, from_results=baseline, retry_rounds=0, timeout_s=600,
            report_path=current/'docs/main_v5/docfix.json', deep_dive_first=True,
            deep_dive_out='docs/main_v5/deepdive', doc_rounds=5, doc_stuck=2,
            doc_source='aideal', doc_scope='relevant', manifest='docs/main_v5/api_manifest.json')
        save(current/'docs/main_v5/docfix.json', result)
        return result
    result = comprehension_check(cfg, execute=True, show_code=True, doc_source='aideal',
        doc_scope='relevant', class_context=False, max_fix_rounds=0, resume=True,
        timeout_s=600, manifest='docs/main_v5/api_manifest.json')
    save(current/f'docs/main_v5/{action}.json', result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['A2', 'feedback', 'repair', 'B2'])
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--upstream', required=True, type=Path)
    args = p.parse_args()
    import fcntl
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out/'.worker.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        verify(args.root)
        with report_updates(args.root, args.out, args.action):
            while not priority_ready(args.out):
                save(args.out/'waiting.json', {'reason':'priority B2-1 work', 'epoch':time.time()})
                time.sleep(30)
            if args.action == 'feedback':
                folder = args.out/'feedback'
                folder.mkdir(exist_ok=True)
                result = feedback(args.root, folder, args.upstream)
            else:
                while True:
                    with slot(args.upstream, 'RDPro '+args.action) as admitted:
                        if admitted:
                            result = perform(args.action, args.root, args.out)
                            break
                    time.sleep(30)
        print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
