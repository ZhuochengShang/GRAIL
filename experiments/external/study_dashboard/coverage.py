"""Freeze original-document cohorts; live outcomes remain in the existing observer."""
import argparse
import copy
import hashlib
import inspect
import json
from pathlib import Path
import re

from aideal.config import load_config
from aideal.readme_agent import _doc_code_mentions, parse_readme
from .data import REPOS


def build(parent):
    records = []
    for repo, (prefix, relative) in REPOS.items():
        root = parent / f'{prefix}_A1' / relative
        suffix = '_full235' if repo == 'tslearn' else ''
        cfg = load_config(root / f'configs/aideal_A1{suffix}.yaml')
        a2 = load_config(parent / f'{prefix}_A2' / relative / f'configs/aideal_A2{suffix}.yaml')
        original_text, copied_text = cfg.original_readme_text(), a2.original_readme_text()
        manifest_path = root / 'docs/eval/api_manifest.json'
        saved_path = root / 'docs/eval/api_coverage.json'
        manifest = json.loads(manifest_path.read_text())['apis']
        names = set(manifest)
        patterns = cfg.raw.get('coverage', {}).get('documentation_call_patterns')
        # Only explicit README files in the YAML input list, not nested docs READMEs.
        configured = cfg.raw['files']['original_readme']
        configured = [configured] if isinstance(configured, str) else configured
        readmes = [cfg.root / item for item in configured
                   if re.fullmatch(r'readme(?:\..*)?', Path(item).name, re.I)
                   and (cfg.root / item).is_file()]
        narrow = copy.copy(cfg)
        narrow.original_readme_files = readmes
        readme = _doc_code_mentions(narrow.original_readme_text(), names, patterns)
        bundle = _doc_code_mentions(cfg.original_readme_text(), names, patterns)
        saved = json.loads(saved_path.read_text())
        if bundle != set(saved['original_documented_O']) or names != set(saved['surface_S']):
            raise ValueError(f'{repo}: frozen coverage/manifest drift; inspect rather than relabel')
        assert readme <= bundle <= names
        if bundle != _doc_code_mentions(copied_text, names, patterns):
            raise ValueError(f'{repo}: code-reference cohorts differ between original-doc copies')
        generated = {entry.name for entry in parse_readme(a2.llm_readme)} & names
        sources = [manifest_path, saved_path, *cfg.original_readme_files, a2.llm_readme]
        records.append({'repository': repo, 'manifest': manifest, 'readme': sorted(readme),
            'bundle': sorted(bundle), 'generated': sorted(generated),
            'original_bundles_byte_equal': original_text == copied_text,
            'original_bundle_text_sha256': hashlib.sha256(original_text.encode()).hexdigest(),
            'a2_original_bundle_text_sha256': hashlib.sha256(copied_text.encode()).hexdigest(),
            'cohort_match_between_copies': True,
            'readme_paths': [str(p) for p in readmes], 'bundle_files': len(cfg.original_readme_files),
            'sources': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in sources]})
    return {'method': 'Existing _doc_code_mentions detector: code/backtick/call-form references to frozen bare API names. Matches do not certify documentation completeness or qualified symbol ownership.',
            'detector_sha256': hashlib.sha256(inspect.getsource(_doc_code_mentions).encode()).hexdigest(),
            'records': records}


def embed(template, data):
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    block = '<script id="coverage-data" type="application/json">'+payload+'</script>'
    text = template.read_text()
    if '<script id="coverage-data"' in text:
        text = re.sub(r'<script id="coverage-data".*?</script>', lambda _: block, text, flags=re.S)
    else:
        text = text.replace('<script id="study-data"', block+'<script id="study-data"')
    temporary = template.with_suffix('.coverage.tmp')
    temporary.write_text(text)
    temporary.replace(template)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-parent', type=Path, required=True)
    parser.add_argument('--template', type=Path, default=Path(__file__).with_name('dashboard.html'))
    args = parser.parse_args()
    data = build(args.workspace_parent.resolve())
    args.template.with_name('coverage_cohorts.json').write_text(json.dumps(data, indent=2)+'\n')
    embed(args.template, data)
    print(json.dumps([{k: len(row[k]) for k in ('manifest','readme','bundle','generated')} |
                     {'repository': row['repository']} for row in data['records']], indent=2))
