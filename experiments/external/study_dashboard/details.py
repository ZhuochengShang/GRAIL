"""Publish detailed per-repository studies in a separate, read-only observer namespace."""
import argparse
from datetime import datetime
import fcntl
import html
import json
from pathlib import Path
import time

from .__main__ import atomic
from .details_data import priority, mdanalysis, Reader


def historical(parent, out):
    """Keep RDPro's historical treatment names and denominators explicit."""
    import mistune
    reader = Reader()
    report = reader.read(parent / 'GRAIL_rdpro_puzzle_aideal/experiments/rdpro/docs/STRATIFIED_A1_A2_COMPARISON.md', text=True)
    runs = {}
    paths = {'A1 zero / shared88': ('A1', 'comprehension_A1_original.json'),
             'A2 zero / artifact171': ('A2', 'comprehension_A2_generated_all.json'),
             'A1 fix5 / shared88': ('A1', 'comprehension_A1_fix5.json'),
             'A2 fix5 / shared88': ('A2', 'comprehension_A2_fix5_shared88.json')}
    for label, (cell, filename) in paths.items():
        runs[label] = reader.read(parent / f'GRAIL_rdpro_final_{cell}/experiments/rdpro/docs/{filename}')
    names = sorted(runs['A1 zero / shared88']['metrics'])
    rows = []
    for name in names:
        cells = []
        evidence = {}
        for label, run in runs.items():
            metric = run['metrics'].get(name, {})
            cells.append(f"<td>{html.escape(str(metric.get('status', 'missing')))}; pass round {metric.get('pass_round', '—')}; {metric.get('wall_s', '—')} s</td>")
            evidence[label] = {'metric': metric, 'details': run.get('details', {}).get(name)}
        rows.append('<tr><td><details><summary>'+html.escape(name)+'</summary><pre>'+html.escape(json.dumps(evidence, indent=2))+'</pre></details></td>'+''.join(cells)+'</tr>')
    style = Path(__file__).with_name('details.html').read_text().split('<style>', 1)[1].split('</style>', 1)[0]
    page = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RDPro historical study</title><style>{style}</style><main><header><h1>RDPro · historical study</h1><nav><a href="../index.html">Overview</a><a href="mir_eval.html">Current detailed studies</a></nav></header><section><p class="note">Historical A1/A2 zero-fix and five-snippet-fix experiments. These fix5 runs are not the current source-only recovery or document-repair/B2 treatment. The 171 generated entries include 10 extras outside the validated 161-API surface. No historical outcomes are inserted into the current treatment matrix.</p>'+mistune.html(report).replace('<table>', '<div class="scroll"><table>').replace('</table>', '</table></div>')+'</section><section><h2>Shared 88 APIs · raw native evidence</h2><p>Expand an API for recorded metrics, timing and retained snippet details. The semantic-review strata above are a separate layer.</p><div class="scroll"><table><thead><tr><th>API / evidence</th>'+''.join('<th>'+html.escape(label)+'</th>' for label in runs)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></section><section><details><summary>Source paths and hashes</summary><pre>'+html.escape(json.dumps(reader.sources, indent=2))+'</pre></details></section></main></html>'
    atomic(out / 'rdpro.html', page)


def publish(parent, out):
    # Consume the existing summary observer's coherent embedded snapshot.
    snapshot_path = out.parent / 'data.json'
    snapshot = json.loads(snapshot_path.read_text())
    coverage = json.loads(Path(__file__).with_name('coverage_cohorts.json').read_text())
    template = Path(__file__).with_name('details.html').read_text()
    result = {}
    for repo in ('mir_eval', 'Thumbnailator', 'tslearn', 'MDAnalysis'):
        data = mdanalysis(parent) if repo == 'MDAnalysis' else priority(parent, repo, snapshot, coverage)
        slug = repo.lower()
        data['native_snapshot_time'] = snapshot['native_snapshot']
        encoded = json.dumps(data, ensure_ascii=False)
        page = template.replace('__DATA__', encoded.replace('<', '\\u003c'))
        atomic(out / f'{slug}.json', encoded+'\n')
        atomic(out / f'{slug}.html', page)
        result[repo] = {'apis': data['expected'], **data['derived']}
    historical(parent, out)
    atomic(out / 'summary.json', json.dumps({'updated_at': datetime.now().astimezone().isoformat(),
                                           'studies': result}, indent=2)+'\n')
    atomic(out / 'heartbeat.json', json.dumps({'epoch': time.time(), 'status': 'ok'})+'\n')
    return {repo: {k: v for k, v in r.items() if not isinstance(v, list)} for repo, r in result.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--watch', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / 'details.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            try:
                print(json.dumps(publish(args.workspace_parent, args.out)), flush=True)
            except Exception as exc:
                atomic(args.out / 'heartbeat.json', json.dumps({'epoch': time.time(),
                    'status': 'error', 'error': f'{type(exc).__name__}: {exc}'})+'\n')
                if not args.watch:
                    raise
            if not args.watch:
                break
            time.sleep(60)


if __name__ == '__main__':
    main()
