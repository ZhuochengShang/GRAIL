const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const COLORS = {pass:'#06796f',compile:'#315cbc',runtime:'#b34049',provider:'#ac4e13'};
const GROUPS = {'documentation-contradiction':'README contradicts the API','surface-accessibility':'External-accessibility mismatch','receiver-setup':'Incomplete receiver setup','audience-helper-error':'Invented helper / wrong receiver','input-and-test-assumption':'Input or test assumption'};
const findings = new Map(DATA.findings.map(row => [row.api, row]));
const decisions = {};
let ascending = true;
let currentRows = [];

function outcome(row, cell) {
    if (row[cell] === 'pass') return 'pass';
    return row[cell+'_category'] === 'llm-error' ? 'provider' : row[cell+'_category'];
}
function badge(status) {
    return `<span class="badge ${esc(status)}">${esc({pass:'Recorded pass',compile:'Compile error',runtime:'Runtime error',provider:'Provider unresolved'}[status] || status)}</span>`;
}
function download(name, contents, mime) {
    const url = URL.createObjectURL(new Blob([contents], {type:mime}));
    const a = document.createElement('a'); a.href=url; a.download=name; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function barRows(id, rows, denominator, color) {
    $(id).innerHTML = rows.map(r => `<div class="bar-row"><div class="bar-title"><span>${esc(r.label)}</span><strong>${esc(r.display ?? r.value)}</strong></div><div class="bar-track"><div class="bar-fill" style="width:${100*r.value/denominator}%;background:${color}"></div></div></div>`).join('');
}
function overview() {
    $('stamp').textContent = 'Evidence snapshot: '+new Date(DATA.generated_at).toLocaleString()+' · Browser local time · No automatic refresh';
    const c = DATA.counts;
    $('kpis').innerHTML = [[c.manifest,'API names in frozen manifest','Not all are externally callable'],[c.a2_pass,'A2 recorded passes','Correctness gate limitation'],[c.a2_compile,'A2 compile failures','Target API never executed'],[c.a2_runtime,'A2 runtime failures','May fail before target call']].map(([n,label,note]) => `<div class="kpi"><div class="label">${label}</div><strong>${n}</strong><small>${note}</small></div>`).join('');
    $('outcomes').innerHTML = ['a1','a2'].map(cell => {
        const counts = {};
        DATA.apis.forEach(r => {const key=outcome(r,cell); counts[key]=(counts[key]||0)+1;});
        return `<div class="stack-label"><span>${cell.toUpperCase()} · ${cell==='a1'?'Original documentation':'Generated documentation'}</span><span>${counts.pass || 0} / ${c.manifest} recorded pass</span></div><div class="stack">`+Object.entries(COLORS).map(([key,color]) => counts[key] ? `<span title="${key}: ${counts[key]}" style="width:${100*counts[key]/c.manifest}%;background:${color}">${counts[key]}</span>`:'').join('')+'</div>';
    }).join('');
    $('paired').innerHTML = [['both_pass','Pass in both'],['a1_only','Pass only in A1'],['a2_only','Pass only in A2'],['neither_pass','No pass in either']].map(([key,label]) => `<div><strong>${c.paired[key]}</strong><span>${label}</span></div>`).join('');
    const steps = [[149,'Recorded API attempts','Harness entered evaluation for every name','auto'],[149,'Generated tests','No provider failures in final A2 result','llm'],[135,'Compiled / started','14 tests stopped at compilation','auto'],[127,'Accepted by harness','8 runtime failures; assertions disabled','auto'],['?','Verified correctness','Target-call and effective-assertion evidence still required','human']];
    $('stages').innerHTML = steps.map(([n,label,note,kind],i) => `${i?'<b aria-hidden="true">→</b>':''}<div><span class="tag ${kind}">${kind==='llm'?'LLM':kind==='human'?'REVIEW NEEDED':'AUTOMATIC'}</span><span class="count">${n}</span><strong>${label}</strong><small>${note}</small></div>`).join('');
    barRows('groups', Object.entries(c.groups).sort((a,b)=>b[1]-a[1]).map(([key,n])=>({label:GROUPS[key],value:n,display:n+' / 22'})),22,'#7044a0');
    histogram(DATA.apis.map(r=>r.wall_s));
}
function histogram(values) {
    const bins = Array(8).fill(0);
    values.forEach(v => bins[Math.min(7,Math.floor(v/10))]++);
    const max = Math.max(...bins), left=45, top=25, height=180, width=470, step=width/8;
    let svg = `<svg viewBox="0 0 545 260" role="img" aria-label="Histogram of 149 A2 per-API wall durations"><title>A2 duration histogram</title><desc>${bins.map((n,i)=>`${i*10}${i===7?'+':'–'+(i+1)*10} seconds: ${n} APIs`).join('; ')}</desc>`;
    [0,0.5,1].forEach(f=>{const y=top+height-height*f;svg+=`<line x1="${left}" x2="525" y1="${y}" y2="${y}" stroke="#dbe3e3"/><text x="37" y="${y+4}" text-anchor="end" fill="#516372" font-size="10">${Math.round(max*f)}</text>`;});
    bins.forEach((n,i)=>{const h=n/max*height,x=left+i*step+5;svg+=`<rect x="${x}" y="${top+height-h}" width="${step-10}" height="${h}" fill="#06796f" rx="3"><title>${i*10}${i===7?'+':'–'+(i+1)*10}s: ${n} APIs</title></rect><text x="${x+(step-10)/2}" y="${top+height-h-7}" text-anchor="middle" font-size="11" fill="#182d3a">${n}</text><text x="${x+(step-10)/2}" y="223" text-anchor="middle" font-size="10" fill="#516372">${i*10}${i===7?'+':'–'+(i+1)*10}</text>`;});
    $('histogram').innerHTML = svg+'<text x="280" y="248" text-anchor="middle" font-size="11" fill="#516372">Recorded wall time (seconds)</text><text x="45" y="13" font-size="10" fill="#516372">API count</text></svg>';
}
function renderTable() {
    const query=$('search').value.toLowerCase().trim(), transition=$('transition').value, group=$('group').value;
    currentRows = DATA.apis.filter(r=>{
        if (query && !r.api.toLowerCase().includes(query)) return false;
        if (group && findings.get(r.api)?.group!==group) return false;
        return transition==='all' || (transition==='a2fail' && r.a2!=='pass') || (transition==='a1only' && r.a1==='pass' && r.a2!=='pass') || (transition==='a2only' && r.a2==='pass' && r.a1!=='pass') || (transition==='both' && r.a1==='pass' && r.a2==='pass');
    }).sort((a,b)=>(ascending?1:-1)*a.api.localeCompare(b.api));
    $('shown').textContent=`Showing ${currentRows.length} of ${DATA.apis.length} APIs. Overview charts remain the full snapshot.`;
    $('api-table').innerHTML=currentRows.map(r=>`<tr><td>${esc(r.api)}</td><td>${badge(outcome(r,'a1'))}</td><td>${badge(outcome(r,'a2'))}</td><td>${esc(GROUPS[findings.get(r.api)?.group] || 'No A2 failure reviewed')}</td><td><button data-api="${esc(r.api)}">Inspect</button></td></tr>`).join('');
}
function showDetail(api) {
    const r=DATA.apis.find(x=>x.api===api), f=findings.get(api), decision=decisions[api]||{};
    let body=`<div class="eyebrow">PER-API EVIDENCE</div><h2>${esc(api)}</h2><p>A1 ${badge(outcome(r,'a1'))} &nbsp; A2 ${badge(outcome(r,'a2'))}</p>`;
    if (f) {
        body+=`<p class="callout"><strong>${esc(GROUPS[f.group])}</strong><br>${esc(f.finding)}</p><h3>Proposed improvement</h3><p>${esc(f.proposal)}</p><p class="caption">${esc(f.confidence)}. ${esc(f.proposal_status)}.</p><p><strong>Input used:</strong> ${esc(f.input_data)}</p><div class="detail-grid"><div><h3>Native failure evidence</h3><pre>${esc(f.execution.stderr_tail)}</pre><h3>Generated test code</h3><pre>${esc(f.execution.code)}</pre><p class="caption">Some native failure snippets were truncated by the recorder. The retained source file was separately inspected where noted.</p></div><div><details><summary>Delivered generated README</summary><pre>${esc(f.document)}</pre></details>`;
        f.source_refs.forEach(ref=>{const s=DATA.source_evidence[ref];body+=`<details><summary>${esc(ref)}</summary><pre>${esc(s.excerpt)}</pre><p class="caption">${esc(s.path)}<br>SHA-256: ${esc(s.sha256)}</p></details>`;});
        if(f.retained_test) body+=`<details><summary>Retained complete generated test region</summary><p class="caption">Native-code prefix match after blank-line normalization: ${f.retained_test.blank_line_normalized_prefix_matches}. SHA-256 of retained file: ${esc(f.retained_test.sha256)}</p><pre>${esc(f.retained_test.code)}</pre></details>`;
        body+=`</div></div><label>Review decision <select id="decision"><option value="unreviewed">Unreviewed</option><option value="accept-for-isolated-revision">Accept for isolated revision</option><option value="revise">Request revision</option><option value="defer">Defer</option></select></label><p class="caption">Local review annotation only. Export JSON to keep it; no code or live experiment is changed.</p>`;
    } else body+=`<p class="alert">This is a native recorded pass, not a verified correctness result. Java assertions were disabled.</p><h3>Recorded generated code</h3><pre>${esc(r.code)}</pre>`;
    $('detail-body').innerHTML=body;
    if(f){$('decision').value=decision.status||'unreviewed';$('decision').addEventListener('change',e=>{decisions[api]={status:e.target.value,recorded_at:new Date().toISOString()};});}
    $('detail').showModal();
}
function provider() {
    $('timeout-stamp').textContent='Snapshot '+new Date(DATA.timeout.observed_at).toLocaleTimeString();
    barRows('timeouts',DATA.timeout.cells.map(r=>({label:r.cell.replace('_',' / '),value:r.timeout_pct,display:`${r.timeout_events}/${r.checkpoint_events} · ${r.timeout_pct}%`})),100,'#ac4e13');
    $('timeout-table').innerHTML=DATA.timeout.cells.map(r=>`<tr><td>${esc(r.cell)}</td><td>${r.checkpoint_events}</td><td>${r.timeout_events}</td><td>${r.provider_error_events}</td><td>${r.distinct_timeout_apis}</td><td>${r.fingerprint_groups}</td></tr>`).join('');
}
function actions() {
    const items=[['P0 · AIDEAL HARNESS','Make assertions effective','Use an assertion sentinel that must fail, enable Java assertions in a versioned harness, and preserve existing scores as historical evidence.','Evidence: three accepted tests contain unconditional assert false.'],['P0 · AIDEAL API SURFACE','Check external accessibility','Separate package-local helpers and abstract construction from direct public consumer calls. Review a corrected manifest before a new matched run.','Examples: clear, init, createOutputStream, ThumbnailMaker.'],['P1 · LIBRARY DOCUMENTATION','Compile every complete example','Use real factory methods, correct receiver types, actual exception boundaries, and null-safe sentinel handling.','Examples: Pipeline, getRenderingHints, getOutputFormat.'],['P1 · API / DOC DESIGN','Provide a valid starting object','Show supported factories, initialization order, required state, and a minimal observable postcondition. Consider clearer readiness diagnostics.','Examples: defaultResizerFactory and fitWithinDimenions.'],['P1 · DATA / TEST DESIGN','Validate the meaning of fixtures','Provide separate positive and absent-metadata fixtures. Distinguish malformed Exif from valid Exif with no orientation.','Diagnostic: original.jpg → null; orientation_6.jpg → orientation 6.'],['P1 · EXPERIMENT OPERATOR','Bound infrastructure failure costs','Keep shared pacing, total request deadlines, and explicit retry evidence. Review a consistent deadline policy for unresolved provider outcomes.','Do not turn a Gemini timeout into a library-function defect.']];
    $('actions').innerHTML=items.map(([p,title,desc,proof])=>`<article class="action"><span class="priority">${p}</span><h3>${title}</h3><p>${desc}</p><small>${proof}</small></article>`).join('');
}
function evidence() {
    $('fixtures').innerHTML=DATA.fixtures.map(f=>`<article class="fixture"><img src="${f.image}" alt="Thumbnailator ${esc(f.binding)} fixture preview"><div><strong>${esc(f.binding)}</strong><p>${esc(f.path)}<br>${esc(f.format)} · ${f.bytes.toLocaleString()} bytes</p><p>${f.binding==='exif_jpeg'?'Observed orientation: null. Not a positive EXIF-orientation fixture.':f.binding==='diagnostic_positive_control'?'Observed orientation: 6. Diagnostic control only; not substituted into the live run.':'Checked-in grid image fixture.'}</p><details><summary>File hash</summary><p>${f.sha256}</p></details></div></article>`).join('');
    $('diagnostics').textContent=DATA.diagnostics.results.slice(1).map((r,i)=>`Probe ${i+1} · exit ${r.exit_code}\n${r.stdout}${r.stderr}`).join('\n');
    $('provenance').textContent=JSON.stringify(DATA.provenance,null,2);
}
Object.entries(GROUPS).forEach(([key,label])=>{const option=document.createElement('option');option.value=key;option.textContent=label;$('group').append(option);});
['search','transition','group'].forEach(id=>$(id).addEventListener(id==='search'?'input':'change',renderTable));
$('reset').addEventListener('click',()=>{$('search').value='';$('transition').value='a2fail';$('group').value='';renderTable();});
$('sort').addEventListener('click',()=>{ascending=!ascending;renderTable();});
$('api-table').addEventListener('click',e=>{const button=e.target.closest('button[data-api]');if(button)showDetail(button.dataset.api);});
$('close').addEventListener('click',()=>$('detail').close());
$('export').addEventListener('click',()=>download('AIDEAL_evidence_review.json',JSON.stringify({...DATA,local_review_decisions:decisions},null,2),'application/json'));
$('csv').addEventListener('click',()=>{const cols=['api','a1','a1_category','a2','a2_category','wall_s'];const cell=v=>'"'+String(v??'').replace(/^[=+@-]/,"'$&").replace(/"/g,'""')+'"';download('AIDEAL_filtered_APIs.csv',[cols.join(','),...currentRows.map(r=>cols.map(c=>cell(r[c])).join(','))].join('\n'),'text/csv');});
overview();renderTable();provider();actions();evidence();
