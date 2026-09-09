"""Bind the completed historical RDPro stages to their native source files."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def collect(parent):
    paths = {
        'A1': 'GRAIL_rdpro_final_A1/experiments/rdpro/docs/comprehension_A1_original.json',
        'A2': 'GRAIL_rdpro_final_A2/experiments/rdpro/docs/comprehension_A2_generated_all.json',
        'repair': 'GRAIL/experiments/rdpro/docs/docfix_B2_all171.completed.json',
        'B2': 'GRAIL/experiments/rdpro/docs/comprehension_B2_final_all171.json'}
    result = {'sources': []}
    for cell, relative in paths.items():
        raw = (parent / relative).read_bytes()
        data = json.loads(raw)
        result['sources'].append({'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()})
        result[cell] = ({k: data[k] for k in ('attempted', 'processed', 'doc_fixed')} if cell == 'repair'
                        else {'N': len(data['metrics']),
                              'pass': sum(m['status'] == 'pass' for m in data['metrics'].values())})
    if [result[c]['N'] for c in ('A1', 'A2', 'B2')] != [88, 171, 171]:
        raise ValueError('Historical scope changed; inspect the artifacts before publishing')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    args = parser.parse_args()
    data = collect(args.workspace_parent)
    template = Path(__file__).with_name('dashboard.html')
    block = '<script id="stage-history-data" type="application/json">'+json.dumps(data).replace('<', '\\u003c')+'</script>'
    text = template.read_text()
    text = re.sub(r'<script id="stage-history-data".*?</script>', '', text, flags=re.S)
    text = text.replace('<script id="study-data"', block+'<script id="study-data"', 1)
    tmp = template.with_suffix('.stage.tmp')
    tmp.write_text(text)
    tmp.replace(template)
    print(json.dumps({k: v for k, v in data.items() if k != 'sources'}))
