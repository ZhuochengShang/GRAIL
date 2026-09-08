"""Render the dated review as a local HTML codebook using installed mistune."""
import ast
import hashlib
import html
from pathlib import Path
import re

import mistune

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'AIDEAL_PIPELINE_CODE_REVIEW_2026-09-08.md'


def diagram():
    boxes = [
        ('human', 370, 15, 'Human: research choices', 'Question, protocol, budget'),
        ('auto', 370, 100, 'Resolve and freeze inputs', 'YAML, source, manifest, fixtures'),
        ('llm', 40, 195, 'A1: original README', 'Audience writes tests; zero fixes'),
        ('llm', 700, 195, 'Generate README', 'Author uses source/test evidence'),
        ('llm', 700, 285, 'A2: generated README', 'Audience writes tests; zero fixes'),
        ('auto', 700, 375, 'Freeze completed A2', 'Keep eligible and excluded failures'),
        ('llm', 370, 475, 'S_A2: source recovery', 'One diagnosis; up to 5 new fixes'),
        ('llm', 700, 475, 'Independent README repair', 'A2 evidence; up to 5 doc rounds'),
        ('llm', 700, 570, 'B2: fresh full-manifest tests', 'Rewritten README; zero fixes'),
        ('llm', 700, 665, 'S_B2: source recovery', 'B2 failures; up to 5 new fixes'),
        ('auto', 40, 665, 'Evidence and readiness', 'Separate scores, replay and timings'),
        ('human', 40, 765, 'Human reviews improvements', 'Human/agent implements; reevaluate')]
    edges = [((510,75),(510,100)),((370,130),(180,195)),((650,130),(840,195)),
             ((840,255),(840,285)),((840,345),(840,375)),
             ((755,435),(510,475)),((840,435),(840,475)),
             ((840,535),(840,570)),((840,630),(840,665)),
             ((180,255),(180,665)),((370,505),(180,665)),
             ((700,600),(320,680)),((700,695),(320,695)),((180,725),(180,765))]
    out=['<svg viewBox="0 0 1060 845" role="img" aria-label="AIDEAL evidence flow with automatic, LLM and human stages">',
         '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#64748b"/></marker></defs>']
    for (x1,y1),(x2,y2) in edges:
        out.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>')
    for kind,x,y,title,subtitle in boxes:
        color={'human':'#fef3c7','auto':'#e0f2fe','llm':'#ede9fe'}[kind]
        out.append(f'<rect x="{x}" y="{y}" width="280" height="60" rx="10" fill="{color}" stroke="#94a3b8"/>')
        out.append(f'<text x="{x+140}" y="{y+24}" text-anchor="middle" font-size="15" font-weight="650">{html.escape(title)}</text>')
        out.append(f'<text x="{x+140}" y="{y+45}" text-anchor="middle" font-size="12">{html.escape(subtitle)}</text>')
    out.append('<path d="M650,505 L700,505" stroke="#64748b" stroke-dasharray="4" marker-end="url(#arrow)"/><text x="675" y="460" text-anchor="middle" font-size="11">scheduled after S_A2</text></svg>')
    return ''.join(out)


def render():
    source=SOURCE.read_text()
    links=re.findall(r'\]\(([^)]+)\)',source)
    references={}
    for target in links:
        match=re.fullmatch(r'(.+\.py):(\d+)',target)
        if match:
            path,line=match[1],int(match[2])
            references[target]=(path,line,'code-'+hashlib.sha256(target.encode()).hexdigest()[:12])
            source=source.replace(']('+target+')','](#'+references[target][2]+')')
    mermaid=re.search(r'```mermaid\n(.*?)```',source,re.S).group(0)
    source=source.replace(mermaid,'<div class="diagram">'+diagram()+'</div>\n\nBlue = automatic · Purple = LLM · Amber = human/review. Dotted edge = scheduling, not transfer of source-recovery answers.')
    body=mistune.create_markdown(escape=False,plugins=['table'])(source)
    snippets=[]
    for target,(relative,line,anchor) in references.items():
        path=ROOT/relative
        lines=path.read_text().splitlines()
        # Show the containing function/class, bounded to a readable excerpt.
        nodes=[n for n in ast.walk(ast.parse(path.read_text()))
               if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.lineno<=line<=n.end_lineno]
        node=min(nodes,key=lambda n:n.end_lineno-n.lineno) if nodes else None
        start=node.lineno if node and line-node.lineno<40 else max(1,line-6)
        end=min(node.end_lineno if node else line+36,start+55)
        text='\n'.join(f'{i:4d}  {lines[i-1]}' for i in range(start,min(end,len(lines))+1))
        label=f'{relative}:{line}'
        snippets.append(f'<details class="snippet" id="{anchor}"><summary>{html.escape(label)}</summary><p>Snapshot excerpt, lines {start}–{end}. <a href="{html.escape(relative)}">Open full source file</a></p><pre><code>{html.escape(text)}</code></pre></details>')
    css='''body{margin:0;background:#f5f7fb;color:#192b40;font:16px/1.65 system-ui}main{max-width:1120px;margin:auto;padding:32px}h1{font-size:2.2rem;line-height:1.2}h2{margin-top:3rem;border-top:1px solid #cbd5e1;padding-top:1.2rem}h3{color:#164e63}a{color:#075985}table{display:block;overflow:auto;border-collapse:collapse;margin:1.3rem 0;font-size:.92rem}td,th{padding:10px 14px;border:1px solid #d6dfe9;vertical-align:top}th{background:#e5edf5;text-align:left}pre{overflow:auto;background:#132438;color:#e2e8f0;padding:18px;border-radius:8px;font-size:13px;line-height:1.55}code{font-size:.9em}details{background:white;border:1px solid #cbd5e1;border-radius:8px;padding:14px;margin:12px 0}summary{cursor:pointer;font-weight:650;overflow-wrap:anywhere}.diagram{background:white;border-radius:14px;padding:10px;margin:22px 0}.diagram svg{width:100%;max-height:880px}input{padding:12px;font:inherit;width:calc(100% - 28px);border:1px solid #94a3b8;border-radius:6px}nav{display:flex;gap:20px;flex-wrap:wrap;background:#e0f2fe;padding:14px;border-radius:8px}.notice{background:#fff1d6;padding:16px;border-left:4px solid #b45309}@media print{main{padding:0}nav,input{display:none}pre{white-space:pre-wrap}details{break-inside:avoid}}'''
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AIDEAL pipeline and code review</title><style>'+css+'</style></head><body><main><nav><a href="'+SOURCE.name+'">Markdown version</a><a href="#codebook">Browse code excerpts</a><a href="experiments/external/code_review/evidence_20260908.json">Offline findings</a></nav><p class="notice">Dated review snapshot. Findings are open; no running experiment was modified. Code excerpts are for inspection, not an execution interface.</p>'+body+'<h2 id="codebook">Code excerpts in reading order</h2><label for="query">Filter files or code</label><input id="query" placeholder="e.g. recover, fingerprint, docfix"><div>'+''.join(snippets)+'</div></main><script>document.getElementById("query").addEventListener("input",function(){let q=this.value.toLowerCase();document.querySelectorAll(".snippet").forEach(e=>{e.hidden=!e.textContent.toLowerCase().includes(q)})});document.querySelectorAll("a[href^=\"#code-\"]").forEach(a=>a.addEventListener("click",()=>{let d=document.getElementById(a.hash.slice(1));if(d)d.open=true}));</script></body></html>'
    output=SOURCE.with_suffix('.html')
    output.write_text(page)
    print({'html':str(output),'code_excerpts':len(snippets)})


if __name__=='__main__':
    render()
