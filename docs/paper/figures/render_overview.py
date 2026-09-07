from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/paper/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(18,12),dpi=160)
fig.patch.set_facecolor('#F5F7FB'); ax.set_facecolor('#F5F7FB')
ax.set_xlim(0,1800); ax.set_ylim(1200,0); ax.axis('off')
C={'ink':'#18253B','muted':'#53647B','line':'#8D9BB0','D':'#087F8C','L':'#7050BB','H':'#AE6215','O':'#385D9F'}
def txt(x,y,s,size=13,color='ink',weight='normal',ha='left'):
 return ax.text(x,y,s,fontsize=size,color=C.get(color,color),fontweight=weight,ha=ha,va='top',linespacing=1.30)
def rect(x,y,w,h,color='white',edge='#DDE4EF',r=16):
 p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',facecolor=color,edgecolor=edge,linewidth=1.2);ax.add_patch(p);return p
def badge(x,y,mode):
 rect(x,y,54,27,C[mode],C[mode],8);txt(x+27,y+4,mode,10,'white','bold','center')
def arrow(a,b,color='line',dashed=False,curve=0):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=15,linewidth=1.6,color=C[color],linestyle='--' if dashed else '-',connectionstyle=f'arc3,rad={curve}'))
def card(x,y,w,h,title,body,mode,code=None):
 rect(x,y,w,h);badge(x+16,y+15,mode);txt(x+82,y+17,title,10.8 if w < 330 else 13,weight='bold');txt(x+18,y+58,body,11,'muted')
 if code:txt(x+18,y+h-30,code,9.4,'muted')

txt(55,30,'AIDEAL',34,weight='bold')
txt(310,38,'Evidence-backed agent readiness',26,weight='bold')
txt(57,91,'Measure API use  →  explain barriers  →  review improvements  →  re-evaluate',16,'muted')
for x,m,label in [(57,'D','Deterministic automation'),(415,'L','LLM generation / diagnosis'),(825,'H','Human decision'),(1132,'O','Operator agent + tools')]:
 badge(x,140,m);txt(x+66,143,label,12)

txt(60,212,'01  FREEZE THE EXPERIMENT',12,'D','bold')
txt(425,212,'02  MEASURE THE DOCUMENTATION TREATMENTS',12,'L','bold')
txt(1140,212,'03  INTERPRET THE EVIDENCE',12,'D','bold')
card(55,252,305,160,'Define scope','Repositories, API surface,\nresearch question and budget','H','profile.require_profile()')
card(55,443,305,240,'Pin inputs + protocol','Source + public API manifest\nYAML + profile + prompts\nFixtures + dependencies\nScaffold + execution command','D','config.load_config()')
arrow((207,414),(207,440))

rect(410,252,680,431,'#EEF0FA','#D9DCEE')
txt(435,270,'Same frozen API inventory and harness',13,'muted','bold')
card(435,311,303,141,'A1 · Original docs','Audience LLM writes a test;\ncompiler / runtime executes it.','L','_comprehension_execute()')
card(762,311,303,141,'A2 · Generated docs','Author creates documentation;\naudience test is executed.','L','find_or_create() + execute')
card(435,514,303,141,'B1 · Repaired original','Fresh tests after document\ndiagnosis and repair.','L','doc_fix_run() + execute')
card(762,514,303,141,'B2 · Repaired generated','Fresh tests after document\ndiagnosis and repair.','L','doc_fix_run() + execute')
arrow((586,453),(586,509),'L');arrow((913,453),(913,509),'L')
txt(602,468,'repair',10,'L');txt(930,468,'repair',10,'L')
arrow((363,560),(407,560),'D');arrow((1093,466),(1134,466),'D')

card(1138,252,606,139,'Preserve execution evidence','Results, saved tests, failure categories, provider attempts,\ndocument rounds, configuration and input provenance','D','audit_overnight.summarize() · audit_experiment_data.inspect()')
card(1138,420,606,140,'Assess observed readiness','API execution is measured; other capabilities are\npartial or unmeasured. No invented overall score.','D','readiness.model.assess()')
card(1138,573,606,110,'Build reviewable suggestions','Evidence + diagnosis + proposed action + validation criteria','D','readiness.model.suggestion()')
arrow((1441,393),(1441,417));arrow((1441,562),(1441,570))

rect(55,713,1689,82,'#E6F3F4','#CCE5E7')
badge(72,733,'D');txt(139,733,'Autonomous operations',13,'D','bold')
txt(410,733,'Watchdogs • compatible checkpoints • separate mutable outputs • provider-start coordination',12,'D')
txt(139,765,'Zero code-fix rounds in final cells. Document repair: up to 5 rounds, with a 2-stuck-round stop.',11,'muted')

txt(60,832,'04  HUMAN-REVIEWED IMPROVEMENT LOOP',12,'H','bold')
card(55,871,382,149,'Propose a concrete plan','Human or operator agent prepares\na scoped change and validation plan.','O','review action: propose')
card(491,871,382,149,'Approve + assign','Human reviews the plan and\nchooses a human or agent executor.','H','review action: approve_plan')
card(927,871,382,149,'Implement + validate','Assigned executor works in isolation;\nsubmits change and comparison evidence.','O','review action: submit_result')
card(1363,871,382,149,'Review the result','Human accepts or requests changes.\nBenefit needs matched re-evaluation.','H','review action: accept_result')
for x in [438,874,1310]:arrow((x,943),(x+49,943),'H')
ax.plot([1678,1780,1780,32,32,55],[686,686,852,852,943,943],color=C['line'],linewidth=1.3,linestyle='--')
arrow((32,943),(53,943))
txt(60,1050,'What is implemented',12,weight='bold')
txt(60,1078,'Executable API study + evidence reporting + review records. Approval does not launch an agent or merge changes.',12,'muted')
txt(60,1118,'What still needs separate validation',12,weight='bold')
txt(60,1146,'Input / oracle correctness • independent discovery and setup • held-out workflows • full transport-level quota admission',12,'muted')
fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
for ext in ['svg','pdf','png']:
 fig.savefig(OUT/f'AIDEAL_OVERVIEW.{ext}',facecolor=fig.get_facecolor(),dpi=160)
print('Saved SVG, PDF and PNG overview')
