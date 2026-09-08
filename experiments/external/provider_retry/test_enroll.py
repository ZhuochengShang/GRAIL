import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from .enroll import enroll, BOOTSTRAP


def test_bootstrap_in_real_fresh_process_without_model_calls(tmp_path):
    src=tmp_path/'grail-agent/src';src.mkdir(parents=True)
    (src/'aideal').symlink_to(Path(__file__).parents[3]/'grail-agent/src/aideal',target_is_directory=True)
    config=tmp_path/'config.yaml';config.write_text('project: {name: test}\n')
    out=tmp_path/'events'
    result=enroll(tmp_path,config,out)
    env=dict(os.environ,PYTHONPATH=str(src))
    proc=subprocess.run([sys.executable,'-m','aideal.cli','--config',str(config),
                         'comprehension','--resume','--max-fix-rounds','0','--help'],
                        env=env,cwd=tmp_path,text=True,capture_output=True)
    assert proc.returncode==0,proc.stderr
    assert '[transport]' in proc.stderr
    records=[json.loads(line) for p in out.glob('*.jsonl') for line in p.read_text().splitlines()]
    assert [r['event'] for r in records]==['worker_enrolled']
    assert result['activation'].startswith('Next naturally')
    # A generated script/plain interpreter must not load the adapter.
    plain=subprocess.run([sys.executable,'-c','import sys; print("_aideal_transport_retry" in sys.modules)'],
                         cwd=tmp_path,env=env,text=True,capture_output=True)
    assert plain.stdout.strip()=='False'


def test_refuses_existing_bootstrap(tmp_path):
    src=tmp_path/'grail-agent/src/aideal';src.mkdir(parents=True)
    (src/'llm.py').write_text('original')
    (src.parent/'sitecustomize.py').write_text('existing customization')
    config=tmp_path/'config.yaml';config.write_text('')
    with pytest.raises(ValueError,match='overwrite'):
        enroll(tmp_path,config,tmp_path/'out')
    assert not (src.parent/'_aideal_transport_retry.py').exists()


def test_malformed_policy_prevents_intended_worker_but_not_plain_python(tmp_path):
    (tmp_path/'sitecustomize.py').write_text(BOOTSTRAP)
    (tmp_path/'aideal_transport_policy.json').write_text('{broken')
    env=dict(os.environ, PYTHONPATH=str(tmp_path))
    process=subprocess.run([sys.executable, '-c', 'print("WORKER EXECUTED")',
        'comprehension', '--resume', '--config', str(tmp_path/'config')],
        env=env, cwd=tmp_path, text=True, capture_output=True)
    assert process.returncode != 0 and 'WORKER EXECUTED' not in process.stdout
    assert 'bootstrap failed' in process.stderr
    plain=subprocess.run([sys.executable, '-c', 'print("plain")'],
        env=env, cwd=tmp_path, text=True, capture_output=True)
    assert plain.returncode == 0 and plain.stdout.strip() == 'plain'
