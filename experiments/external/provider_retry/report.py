"""Passive, explicit execution status and per-API timing; no model calls."""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import fcntl
import html
import json
from pathlib import Path
import time

from experiments.external.assertion_replay.evidence import collect, digest
from .transport import atomic

REPOS=[('mir_eval','GRAIL_mir_eval','experiments/external/mir_eval'),
       ('Thumbnailator','GRAIL_thumbnailator','experiments/external/thumbnailator'),
       ('tslearn','GRAIL_tslearn_full235','experiments/tslearn')]


def lines(path):
    if not path.is_file():return []
    return [json.loads(line) for line in path.read_bytes().splitlines(keepends=True)
            if line.endswith(b'\n')]


def outcome(row):
    if row['status']=='pass':return 'Passed native checks'
    category=row.get('error_category')
    return {'llm-error':'Waiting for provider / retry', 'compile':'Compile failed',
            'runtime':'Execution failed', 'timeout':'Execution timed out',
            'infra':'Setup/import blocked','no-correctness-check':'Correctness check missing'}.get(
                category,'Other recorded failure')


def execution(row):
    category=row.get('error_category')
    if category=='llm-error':return 'No test code executed for this provider attempt'
    if category=='compile':return 'Compilation failed; generated test did not execute'
    if category=='infra':return 'Setup/import failed; target execution not established'
    detail=row.get('execution_evidence')
    if isinstance(detail,dict) and detail.get('exit_code') is not None:
        return f"Test process returned exit code {detail['exit_code']}; target reach not independently verified"
    if row['status']=='pass' or category in ('runtime','timeout','no-correctness-check'):
        return 'Test execution reported by native harness; detailed process evidence may be incomplete'
    return 'Execution not established from available evidence'


def provider_timing(events):
    starts={e['invocation_id']:e for e in events if e['event']=='invocation_start'}
    ends={e['invocation_id']:e for e in events if e['event'] in ('invocation_success','invocation_error')}
    history=[]
    for key,start in starts.items():
        end=ends.get(key,{})
        previous=start.get('previous_end_epoch')
        history.append({'id':key,'start_epoch':start['epoch'],'end_epoch':end.get('epoch'),
                        'provider_wall_s':end.get('wall_s'),
                        'since_previous_provider_end_s':start['epoch']-previous if previous else None,
                        'outcome':end.get('event','In flight or interrupted: no end recorded'),
                        'retry_after_epoch':end.get('retry_after'),
                        'policy_sha256':start['policy_sha256']})
    return sorted(history,key=lambda e:e['start_epoch'])


def publish(parent,out):
    out.mkdir(parents=True,exist_ok=True)
    details=out/'api_details';details.mkdir(exist_ok=True)
    rows,cells,recoveries,rollout=[],[],[],[]
    for repo,prefix,relative in REPOS:
        for cell in ['A1','A2','B2']:
            worktree=parent/(prefix+'_'+cell);project=worktree/relative
            evidence=collect(project,cell)
            if evidence is None:
                cells.append({'repository':repo,'cell':cell,'state':'Not started / no native results',
                              'n':0,'statuses':{}})
                continue
            native=evidence['rows'];fps={r['experiment_fingerprint'] for r in native.values()}
            history=defaultdict(list)
            for r in lines(project/f'.aideal_exec/{cell}/comprehension_progress.jsonl'):
                if r.get('experiment_fingerprint') in fps:history[r['name']].append(r)
            transport=defaultdict(list)
            enrolled=[]
            for p in sorted((worktree/'.aideal_exec/provider_transport_v2').glob('events-*.jsonl')):
                for event in lines(p):
                    if event.get('event')=='worker_enrolled':enrolled.append(event['pid'])
                    if event.get('api'):transport[event['api']].append(event)
            if (worktree/'grail-agent/src/aideal_transport_policy.json').exists():
                rollout.append({'repository':repo,'cell':cell,'observed_enrolled_worker_pids':enrolled,
                                'state':'New transport observed in worker logs' if enrolled else
                                'Installed; awaiting next natural worker start'})
            statuses=Counter(outcome(r) for r in native.values())
            wait=statuses.get('Waiting for provider / retry',0)
            cells.append({'repository':repo,'cell':cell,'n':len(native),'statuses':dict(statuses),
                          'state':f'{wait} provider cases unresolved' if wait else
                          'Native evaluation finished (failures still count)' if evidence['complete'] else
                          'Awaiting final artifact; no provider failures in collected rows'})
            for api,n in native.items():
                h=history[api];events=transport[api];timing=provider_timing(events)
                path=details/f'{digest([repo,cell,api])[:20]}.json'
                latest=n.get('wall_s')
                item={'repository':repo,'cell':cell,'api':api,'outcome':outcome(n),
                      'test_execution':execution(n),'target_api_reached':'Not independently verified',
                      'latest_native_attempt_s':latest,
                      'retained_checkpoint_events':len(h),
                      'retained_attempt_total_s':round(sum(r.get('wall_s',0) or 0 for r in h),3) if h else None,
                      'retained_504_events':sum('504' in str(r.get('error','')) for r in h),
                      'historical_idle_retry_s':None,
                      'measured_provider_invocations':len(timing),
                      'last_provider_s':timing[-1].get('provider_wall_s') if timing else None,
                      'last_retry_interval_s':timing[-1].get('since_previous_provider_end_s') if timing else None,
                      'next_provider_retry_epoch':timing[-1].get('retry_after_epoch') if timing else None,
                      'transport_policy':timing[-1]['policy_sha256'] if timing else 'Historical/uninstrumented',
                      'error':n.get('error',''),'details':str(path.relative_to(out))}
                atomic(path,{'summary':item,'native_row':n,'source_path':evidence['source_path'],
                             'source_sha256':evidence['source_sha256'],'checkpoint_events':h,
                             'provider_timing':timing,'transport_events':events,
                             'timing_note':'Native wall_s includes generation and test work for that attempt, not cumulative lifetime duration. Checkpoint events lack timestamps: historical idle waits cannot be reconstructed. New retry intervals include scheduler/admission delays. Missing provider end means in flight or interrupted, never success.'})
                rows.append(item)
        audit=parent/'GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation'
        for stage,p in [('A2 source fixes',audit/'pipeline_v2'/repo.lower()/'source/summary.json'),
                        ('Post-B2 source fixes',audit/'pipeline_v3'/repo.lower()/'summary.json')]:
            if p.is_file():
                d=json.loads(p.read_text())
                recoveries.append({'repository':repo,'stage':stage,'statuses':d.get('statuses',{}),
                                   'cohort':len(d.get('apis',{})),
                                   'apis':{n:{k:r.get(k) for k in ['status','code_fix_rounds','provider_events']}
                                           for n,r in d.get('apis',{}).items()}})
    now=datetime.now().astimezone().isoformat()
    atomic(out/'summary.json',{'updated_at':now,'native_cells':cells,'separate_recovery':recoveries,'transport_rollout':rollout,
                             'api_rows':len(rows),'B1':'Omitted: no original-document repair'})
    tmp=out/'API_TIMINGS.csv.tmp'
    with tmp.open('w') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    tmp.replace(out/'API_TIMINGS.csv')
    labels=['Passed native checks','Compile failed','Execution failed','Setup/import blocked','Waiting for provider / retry']
    header='| Repository | Cell | State | Pass | Compile fail | Execution fail | Setup/import | Provider pending | Other/timeout |\n|---|---|---|---:|---:|---:|---:|---:|---:|'
    table=[header]+['| '+ ' | '.join([c['repository'],c['cell'],c['state']]+[str(c['statuses'].get(k,0)) for k in labels]+[str(sum(v for k,v in c['statuses'].items() if k not in labels))])+' |' for c in cells]
    text=['# Execution status and API timing', '',now,'',
          '**No single “partial” label:** each unresolved case has an explicit reason. A finished evaluation can contain real failures. A provider failure is not executed code. A running test does not prove the target API was reached.','',*table,'',
          'Other failures/timeouts, if present, remain explicit in summary.json and the full API table. B1 is intentionally omitted. MDAnalysis, Sedona and RDPro reruns are deferred.','',
          '[Searchable dashboard](REPORT.html) · [Every API timing (CSV)](API_TIMINGS.csv) · [Machine-readable status](summary.json)','',
          'Timing: latest_native_attempt_s is one recorded generation-plus-test attempt, not lifetime duration. retained_attempt_total_s sums retained checkpoint events only. Provider transport duration is measured separately for instrumented retries. last_retry_interval_s is the interval from a previous provider end to the next provider start, including queue/cooldown. Blank historical timing means unavailable, not zero.','',
          'New workers may use the explicitly registered 600s × 1 transport and output-directory setup amendment. Existing workers finish under their previous settings. Each instrumented request records policy/adapter hashes; native fingerprints alone do not distinguish transport revisions. Source and README repairs remain separate from these operational corrections.','',
          '## Separate source-recovery progress','']
    for r in recoveries:text.append(f"- {r['repository']} / {r['stage']}: {r['statuses']}; cohort {r['cohort']} APIs.")
    text.extend(['','## Transport rollout',''])
    for r in rollout:text.append(f"- {r['repository']} {r['cell']}: {r['state']}; observed workers {r['observed_enrolled_worker_pids']}.")
    atomic_text(out/'STATUS.md','\n'.join(text)+'\n')
    columns=['repository','cell','api','outcome','latest_native_attempt_s','retained_checkpoint_events',
             'retained_attempt_total_s','retained_504_events','last_provider_s','last_retry_interval_s']
    headings=['Repository','Cell','API','Outcome','Latest attempt (s)','Checkpoint records','Sum recorded time (s)',
              'Recorded 504s','Latest provider time (s)','Retry interval (s)']
    rendered=[]
    for r in rows:
        values=[html.escape(str(r[k])) if r[k] is not None else 'Not recorded' for k in columns]
        values[2]=f'<a href="{r["details"]}">{values[2]}</a>'
        rendered.append('<tr>'+''.join('<td>'+v+'</td>' for v in values)+'</tr>')
    cards=[]
    for c in cells:
        passed=c['statuses'].get('Passed native checks',0);total=c['n']
        status_list='<br>'.join(f'{html.escape(k)}: {v}' for k,v in c['statuses'].items())
        cards.append(f'<article><b>{html.escape(c["repository"])} {c["cell"]}</b><p>{passed}/{total} passed native checks</p><progress value="{passed}" max="{total or 1}"></progress><p>{html.escape(c["state"])}</p><small>{status_list}</small></article>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AIDEAL execution and timing</title>
<style>body{font:16px system-ui;margin:2rem;color:#16263b;background:#f4f7fb}h1{font-size:1.7rem}a{color:#1457a5}.cards{display:flex;flex-wrap:wrap;gap:1rem}article{background:white;padding:1rem;border:1px solid #ccd5e0;border-radius:8px;width:240px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:9px;border-bottom:1px solid #dce3ec;text-align:left}th{position:sticky;top:0;background:#18324d;color:white}input{padding:12px;width:70%;margin:1rem 0}.scroll{overflow:auto;max-height:70vh}progress{width:100%}.note{background:#fff1c9;padding:1rem;line-height:1.5}</style>
<h1>AIDEAL: what actually finished?</h1><p>UPDATED</p><p class="note">Pass = native harness accepted the generated test. Compile failure = no test execution. Provider pending = no usable model response for that attempt. Setup/import failures do not establish that the target API ran. No independent semantic correctness claim is made.</p>
<div class="cards">CARDS</div><p><a href="API_TIMINGS.csv">Download every API and timing</a> · <a href="STATUS.md">Protocol and status notes</a></p><p>Latest attempt includes generation and test work. Sum covers retained attempts only. Retry interval includes queue/cooldown. “Not recorded” means missing evidence, never zero. Source fixes are separate from these scores.</p>
<label for="filter">Filter by repository, cell, API or outcome</label><br><input id="filter" placeholder="e.g. tslearn, compute, Waiting for provider"><div class="scroll"><table><thead><tr>HEADINGS</tr></thead><tbody>ROWS</tbody></table></div>
<script>document.getElementById('filter').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));});</script></html>'''
    page=page.replace('UPDATED',html.escape(now)).replace('CARDS',''.join(cards)).replace('HEADINGS',''.join('<th>'+h+'</th>' for h in headings)).replace('ROWS',''.join(rendered))
    atomic_text(out/'REPORT.html',page)
    return {'updated_at':now,'api_rows':len(rows),'cells':cells}


def atomic_text(path,text):
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(text);tmp.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--watch',action='store_true')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    with (args.out/'report.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        while True:
            print(json.dumps(publish(args.workspace_parent,args.out)),flush=True)
            if not args.watch:break
            time.sleep(60)


if __name__=='__main__':main()
