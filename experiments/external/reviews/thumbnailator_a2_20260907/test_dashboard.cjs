// Behavioral checks without a browser: deliberately small DOM interface.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, 'AIDEAL_RESULTS_REVIEW.html'), 'utf8');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'review_data.json'), 'utf8'));
const elements = new Map();
const blobs = [];
class Element {
    constructor() { this.value=''; this.events={}; this.children=[]; this.textContent=''; }
    set innerHTML(value) {
        this.html=value;
        for (const match of value.matchAll(/id="([^"]+)"/g)) elements.set(match[1],new Element());
    }
    get innerHTML() { return this.html||''; }
    addEventListener(name,callback) { this.events[name]=callback; }
    append(child) { this.children.push(child); }
    click() { if (this.events.click) this.events.click({target:this}); }
    showModal() { this.open=true; }
    close() { this.open=false; }
}
for (const match of html.matchAll(/id="([^"]+)"/g)) elements.set(match[1],new Element());
elements.get('transition').value='a2fail';
const context=vm.createContext({DATA:data,Blob,Date,console,setTimeout:()=>0,
    URL:{createObjectURL:blob=>{blobs.push(blob);return 'blob:test';},revokeObjectURL:()=>{}},
    document:{getElementById:id=>{assert(elements.has(id),'Missing element '+id);return elements.get(id);},createElement:()=>new Element()}});
vm.runInContext(fs.readFileSync(path.join(__dirname,'dashboard.js'),'utf8'),context);
const count=()=> (elements.get('api-table').innerHTML.match(/<tr>/g)||[]).length;
assert.equal(count(),22);
elements.get('search').value='quality';context.renderTable();assert.equal(count(),1);
elements.get('reset').click();assert.equal(count(),22);
elements.get('group').value='documentation-contradiction';context.renderTable();assert.equal(count(),7);
elements.get('reset').click();elements.get('transition').value='all';context.renderTable();assert.equal(count(),149);
elements.get('transition').value='a1only';context.renderTable();assert.equal(count(),data.counts.paired.a1_only);
context.showDetail('getOutputFormat');assert(elements.get('detail').open);
assert.match(elements.get('detail-body').innerHTML,/ORIGINAL_FORMAT/);
elements.get('decision').events.change({target:{value:'defer'}});
elements.get('close').click();assert.equal(elements.get('detail').open,false);
elements.get('export').click();
elements.get('csv').click();
assert.equal(blobs.length,2);
assert(!/<script[^>]+src=|<link[^>]+href=|__DATA__|__SCRIPT__|__STYLE__/.test(html));
assert.equal(data.findings.length,22);
assert.equal(data.counts.a2_pass+data.counts.a2_compile+data.counts.a2_runtime,149);
assert.equal(Object.values(data.counts.paired).reduce((a,b)=>a+b,0),149);
assert.equal(data.assertion_false_passes.length,3);
Promise.all(blobs.map(blob=>blob.text())).then(([review,csv])=>{
    assert.equal(JSON.parse(review).local_review_decisions.getOutputFormat.status,'defer');
    assert.equal(csv.split('\n').length,data.counts.paired.a1_only+1);
    console.log('PASS: 22 findings, 149 APIs, filters, paired counts, inspector, local decisions, JSON/CSV exports, embedded assets. Visual browser rendering not tested.');
});
