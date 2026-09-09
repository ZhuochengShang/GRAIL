"""Publish a read-only documentation-style audit; never launch experiment work."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re

from aideal.config import load_config
from .data import REPOS


def fingerprint(path, parent):
    if not path.is_file():
        return {'path': str(path.relative_to(parent)), 'available': False}
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    return {'path': str(path.relative_to(parent)), 'available': True,
            'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
            'lines': len(text.splitlines()),
            'api_entry_headings': len(re.findall(r'^## API Test:', text, re.M)),
            'headings_sample': re.findall(r'^#{2,3} (.+)$', text, re.M)[:12]}


def collect(parent):
    here = Path(__file__).parent
    observations = json.loads((here / 'documentation_styles.json').read_text())
    coverage = json.loads((here / 'coverage_cohorts.json').read_text())
    cohorts = {r['repository']: r for r in coverage['records']}
    specs = {}
    for name, (prefix, relative) in REPOS.items():
        suffix = '_full235' if name == 'tslearn' else ''
        roots = {c: parent / f'{prefix}_{c}' / relative for c in ('A1', 'A2', 'B2')}
        specs[name] = (roots['A1'] / f'configs/aideal_A1{suffix}.yaml',
                       roots['A2'] / 'docs/eval/A2/LLM_readme.md',
                       roots['B2'] / 'docs/eval/B2/LLM_readme.md')
    md = json.loads((parent / 'AIDEAL_mdanalysis_v4/registration.json').read_text())['cells']
    md_roots = {c: parent / Path(v['worktree']).name / Path(v['root']).relative_to(v['worktree'])
                for c, v in md.items()}
    specs['MDAnalysis'] = (md_roots['A1'] / 'configs/aideal.full1032.A1.yaml',
        md_roots['A2'] / 'docs/full_1032/A2/LLM_readme.md',
        md_roots['B2'] / 'docs/full_1032/B2/LLM_readme.md')
    rd = parent / 'GRAIL_rdpro_main_v5/experiments/rdpro'
    specs['RDPro'] = (rd / 'configs/aideal.main_v5.yaml',
                      rd / 'docs/main_v5/LLM_readme.md', None)
    for name, row in observations.items():
        row['repository'] = name
        if name not in specs:
            continue
        config, generated, repaired = specs[name]
        cfg = load_config(config)
        inputs = cfg.raw['files']['original_readme']
        inputs = [inputs] if isinstance(inputs, str) else inputs
        row['configured_original_inputs'] = inputs
        row['config'] = fingerprint(config, parent)
        row['bundle_file_count'] = len(cfg.original_readme_files)
        row['bundle_text_sha256'] = hashlib.sha256(cfg.original_readme_text().encode()).hexdigest()
        row['original_readmes'] = [fingerprint(cfg.root / p, parent) for p in inputs
                                  if re.fullmatch(r'readme(?:\..*)?', Path(p).name, re.I)]
        row['generated'] = fingerprint(generated, parent)
        row['repaired'] = fingerprint(repaired, parent) if repaired else {
            'available': False, 'note': 'New RDPro v5 repair not yet available; historical B2 is a different study.'}
        if name in cohorts:
            cohort = cohorts[name]
            if row['bundle_text_sha256'] != cohort['original_bundle_text_sha256']:
                raise ValueError(f'{name}: original bundle drift; review before publishing coverage')
            row['references'] = {key: len(cohort[key]) for key in ('manifest', 'readme', 'bundle', 'generated')}
        else:
            row['references'] = None  # Do not infer root coverage from historical bundle counts.
    return {'snapshot_utc': datetime.now(timezone.utc).isoformat(),
            'method': coverage['method'], 'records': list(observations.values())}


def render(data):
    esc = html.escape
    intro = ('Compare the root README, the configured original documentation bundle, the generated A2 README, '
             'and the repaired README used by fresh B2. These are descriptive observations, not causal style scores. '
             'The A1 bundle is available for selection by the harness; it is not necessarily included in full in every prompt.')
    sections = []
    for r in data['records']:
        refs = r.get('references')
        coverage = (f"Root README: {refs['readme']}/{refs['manifest']}; full original bundle: "
                    f"{refs['bundle']}/{refs['manifest']}; A2 parsed entries: {refs['generated']}/{refs['manifest']}."
                    if refs else 'Comparable root/bundle reference counts not audited in this snapshot.')
        rows = ''.join(f'<tr><th scope="row">{label}</th><td>{esc(r[key])}</td></tr>' for key, label in
                       [('structure', 'Structure'), ('example', 'Representative example'), ('data', 'Data guidance'),
                        ('strength', 'Useful features'), ('barrier', 'Limits'), ('check', 'Evidence to inspect')])
        files = ''.join('<tr><th scope="row">'+label+'</th><td>'+esc(
            f"{f['bytes']:,} bytes · {f['lines']:,} lines · {f['api_entry_headings']} API-entry headings"
            if f.get('available') else f.get('note', 'Not available at snapshot'))+'</td></tr>'
            for label, f in [('Generated A2 file snapshot', r.get('generated', {})), ('Repaired for fresh B2', r.get('repaired', {}))])
        originals = r.get('original_readmes', [])
        if originals:
            files = '<tr><th scope="row">Root README size</th><td>'+esc('; '.join(
                f"{f['bytes']:,} bytes · {f['lines']:,} lines" for f in originals if f['available']))+'</td></tr>'+files
        sections.append(f'<section id="{esc(r["repository"].lower().replace(" ", "-"))}"><h2>{esc(r["repository"])}</h2>'
            f'<p class="label">{esc(r["style"])}</p><table>{rows}{files}</table><p><b>Reference audit:</b> {esc(coverage)}</p>'
            '<details><summary>Configured inputs, source hashes and snapshot measurements</summary><pre>'+
            esc(json.dumps(r, indent=2))+'</pre></details></section>')
    return ('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>AIDEAL · README style comparison</title><style>*{box-sizing:border-box}body{margin:0;background:#f2f5f8;'
        'color:#18314a;font:16px/1.55 system-ui;overflow-wrap:anywhere}main{max-width:1100px;margin:auto;padding:20px}'
        'header,section{padding:22px;border-radius:12px;margin-bottom:20px;background:white}header{background:#18314a;color:white}'
        'a{color:#176b92}header a{color:white}table{width:100%;border-collapse:collapse}td,th{padding:10px;text-align:left;'
        'vertical-align:top;border-bottom:1px solid #dce5ec}th{width:25%}.label{font-weight:650;color:#126777}'
        'pre{white-space:pre-wrap;max-height:450px;overflow:auto;font-size:12px}summary{cursor:pointer}nav a{display:inline-block;'
        'margin-right:14px}@media(max-width:600px){main{padding:10px}header,section{padding:14px}td,th{display:block;width:100%}}</style>'
        '<main><header><h1>Original README styles across repositories</h1><p>'+esc(intro)+'</p><p>Snapshot: '+esc(data['snapshot_utc'])+
        '</p><nav><a href="../study_dashboard_v1/index.html">Study dashboard</a><a href="../main_plan_v5/live/index.html">Live main plan</a>'
        '<a href="comparison.json">Download evidence JSON</a></nav></header><section><h2>How to read this comparison</h2>'
        '<p>Generated documents use repeated API Test sections: signatures, goals, parameters, input/output, call patterns and further guidance. '
        'Repair changes selected entries within that structure. More sections or longer text do not establish correct advice.</p>'
        '<p>'+esc(data['method'])+'</p><p>MDAnalysis documents can still be evolving; file presence and heading counts do not certify completion. '
        'RDPro v5 and historical RDPro must remain separate. Apache Sedona is deferred.</p>'
        '<p>To relate style to outcomes, use matched API cohorts and list A1-only/A2-only passes, exact delivered fragments, errors and target-call evidence. '
        'Separate documentation contradictions, audience mistakes, data/receiver setup, API-surface defects, provider errors and harness limitations. '
        'A controlled style-only ablation has not been run.</p></section>'+''.join(sections)+'</main></html>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = collect(args.workspace_parent.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    for name, text in [('comparison.json', json.dumps(data, indent=2)+'\n'), ('index.html', render(data))]:
        tmp = args.output / (name + '.tmp')
        tmp.write_text(text)
        tmp.replace(args.output / name)
    print(json.dumps({'output': str(args.output), 'repositories': len(data['records']), 'snapshot_utc': data['snapshot_utc']}))
