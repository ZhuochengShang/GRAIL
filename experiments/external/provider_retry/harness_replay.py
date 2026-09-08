"""Matched directory-setup diagnostic for three saved mir_eval B2 snippets.

The snippet bytes and input files stay unchanged. Only the isolated output
directory's existence changes between control and correction. No Gemini calls.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time

from .transport import sha


def replay(project,out):
    project,out=project.resolve(),out.resolve()
    out.mkdir(parents=True,exist_ok=False)
    native=json.loads((project/'docs/eval/B2/comprehension.json').read_text())
    results=[]
    for api in ['load_key','load_tempo','load_wav']:
        detail=native['details'][api]
        original=Path(detail['scala_file']).read_text()
        old=str(project/'.aideal_exec/B2/output')
        if old not in original or not detail.get('code'):
            raise ValueError('Native script binding missing')
        normalize=lambda s:'\n'.join(line.strip() for line in s.strip().splitlines())
        if normalize(detail['code']) not in normalize(original):
            raise ValueError('Saved native code does not match retained script')
        snippet=original.split('# TODO API_TEST_START',1)[1].split('# TODO API_TEST_END',1)[0]
        for variant in ['control_missing_directory','corrected_directory_created']:
            case=out/api/variant;case.mkdir(parents=True)
            output=case/'output'
            script=original.replace(old,str(output))
            assert script.split('# TODO API_TEST_START',1)[1].split('# TODO API_TEST_END',1)[0]==snippet
            if variant=='corrected_directory_created':output.mkdir()
            test=case/'api_test.py';test.write_text(script)
            env=dict(os.environ,PYTHONPATH=str(project/'source'),MPLBACKEND='Agg',
                     OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
            started=time.monotonic()
            proc=subprocess.run([str(project/'source/.venv/bin/python'),str(test)],
                                cwd=case,env=env,text=True,capture_output=True,timeout=60)
            result={'api':api,'variant':variant,'native_status':native['metrics'][api]['status'],
                    'exit_code':proc.returncode,'wall_s':time.monotonic()-started,
                    'stdout':proc.stdout,'stderr':proc.stderr,
                    'snippet_sha256':sha(snippet.encode()),'script_sha256':sha(script.encode()),
                    'native_script_sha256':sha(original.encode()),
                    'accepted':proc.returncode==0 and '__DONE__' in proc.stdout and '__CHECK__' in proc.stdout}
            (case/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result)
    (out/'summary.json').write_text(json.dumps({'scope':'Three B2 APIs only; no native score changes; same snippet, isolated output directory correction only','results':results},indent=2)+'\n')
    return [{'api':r['api'],'variant':r['variant'],'exit_code':r['exit_code'],'accepted':r['accepted']} for r in results]


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args();print(json.dumps(replay(a.project,a.out),indent=2))
