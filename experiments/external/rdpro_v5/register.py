"""Register one isolated RDPro watchdog after successful preflight."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

import pyspark
import yaml

from experiments.external.recovery.engine import save
from .worker import verify


def register(root, out):
    verify(root)
    out.mkdir(parents=True, exist_ok=True)
    registration = root/'docs/main_v5'
    plan = registration/'study_watchdog.yaml'
    if plan.exists():
        raise ValueError('Existing registered plan: inspect and resume; never overwrite')
    inventory = registration/'environment.json'
    save(inventory, {'python':sys.version, 'executable':sys.executable,
        'spark':pyspark.__version__, 'spark_module':pyspark.__file__,
        'java_home':os.environ['JAVA_HOME'],
        'packages':sorted(set((d.metadata['Name'],d.version) for d in importlib.metadata.distributions()))})
    wt = root.parents[1]
    upstream = out.parent/'pipeline_v2'
    policy = wt/'experiments/external/rdpro_v5/protocol.yaml'
    jobs = []
    for action, deps, kind in [('A2', [], 'json_metrics_no_transient'),
        ('feedback', ['A2'], 'exit_zero'), ('repair', ['A2'], 'docfix'),
        ('B2', ['repair'], 'json_metrics_no_transient')]:
        jobs.append({'id':action, 'cwd':str(wt), 'branch':'aideal/rdpro-main-v5',
            'environment_inventory':str(inventory),
            'command':[sys.executable,'-m','experiments.external.rdpro_v5.worker',action,
                '--root',str(root),'--out',str(out),'--upstream',str(upstream)],
            'depends_on':deps, 'result':str(out/(action+'.invocation.json')),
            'complete':{'kind':kind}, 'max_restarts':0, 'max_runtime_seconds':1209600,
            'on_success':[[sys.executable,'-m','experiments.external.rdpro_v5.archive',
                           str(root),str(out),action]]})
    env = {'PYTHONPATH':str(wt/'grail-agent/src')+':'+str(wt),
        'JAVA_HOME':os.environ['JAVA_HOME'], 'SPARK_HOME':str(Path(pyspark.__file__).parent), 'SPARK_LOCAL_IP':'127.0.0.1',
        'AIDEAL_GOOGLE_RATE_STATE':'/tmp/aideal_google_rate_gate.txt',
        'AIDEAL_GOOGLE_MIN_INTERVAL_S':'3', 'AIDEAL_GOOGLE_REQUEST_TIMEOUT_S':'300',
        'AIDEAL_GOOGLE_MAX_RETRIES':'2', 'AIDEAL_RECOVERY_PROTOCOL':str(policy)}
    plan.write_text(yaml.safe_dump({'version':2,'max_parallel':1,
                                   'retry_delay_seconds':300,'env':env,'jobs':jobs},sort_keys=False))
    from experiments.external.run_condition_watchdog import Supervisor
    supervisor = Supervisor(plan)
    supervisor.preflight()
    save(registration/'registration.json', {'plan':str(plan),'out':str(out),
        'core_revision':subprocess.check_output(['git','-C',str(wt),'rev-parse','HEAD'],text=True).strip(),
        'scope':161, 'A1':'historical only; no newly matched control',
        'reuse':'generated README only; new A2 establishes both repair cohorts',
        'queue':'wait priority B2-1 summaries, then shared supplemental admission',
        'old_waiter':'preserved without changing its obsolete prerequisite',
        'deadline':'2026-09-09T11:00:00-07:00; completion not guaranteed'})
    return plan


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    print(register(args.root.resolve(),args.out.resolve()))
