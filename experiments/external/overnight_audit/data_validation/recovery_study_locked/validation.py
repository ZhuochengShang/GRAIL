"""Fail closed on incomplete baselines, changed inputs, or shared write roots."""
from __future__ import annotations

import glob
import hashlib
from pathlib import Path

from aideal.doc_checks import (_comprehension_inventory, _execute_sample_data,
                               _load_manifest, _sha256_files)
from aideal.prompts import DEFAULT_PROMPTS, prompts_dir

from .engine import POLICY, digest, policy


def prompt_file(cfg, name):
    path = prompts_dir(cfg) / f'aideal/{name}.md'
    return path if path.exists() else DEFAULT_PROMPTS / f'aideal/{name}.md'


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def document_hash(cfg, doc, names, scope):
    entries, shared, error = _comprehension_inventory(
        cfg, doc, manifest=names, full_doc=scope == 'full', doc_scope=scope)
    if error:
        raise ValueError(f'document inventory unavailable: {error}')
    text = shared if shared is not None else '\n\0\n'.join(f'{e.name}\n{e.body}' for e in entries)
    return hashlib.sha256(text.encode()).hexdigest()


def eligible(result, api):
    run, metrics = result.get('run', {}), result.get('metrics', {})
    if (run.get('max_fix_rounds') != 0 or not run.get('fingerprint_components')
            or not metrics or run.get('api_count') != len(metrics)
            or any(m.get('status') not in ('pass', 'fail') or
                   m.get('error_category') == 'llm-error' for m in metrics.values())):
        raise ValueError('baseline must be a complete zero-round result without provider failures')
    row = metrics.get(api, {})
    if row.get('status') != 'fail' or row.get('error_category') not in policy()['eligible_categories']:
        raise ValueError('API is not an eligible baseline execution failure')
    return row


def validate(base, cfg, result, api, manifest):
    metric = eligible(result, api)
    if base.root == cfg.root or base.root in cfg.root.parents or cfg.root in base.root.parents:
        raise ValueError('recovery requires a separate, non-nested project copy/worktree')
    if cfg.raw != base.raw:
        raise ValueError('isolated config must be an exact effective-config copy; outputs are isolated by runner')
    run, fp = result['run'], result['run']['fingerprint_components']
    names = _load_manifest(base, manifest)
    if not names or set(names) != set(result['metrics']):
        raise ValueError('manifest identities differ from baseline')
    if _load_manifest(cfg, manifest) != names:
        raise ValueError('isolated manifest differs from baseline')
    if hashlib.sha256('\n'.join(names).encode()).hexdigest() != run['manifest_sha256']:
        raise ValueError('ordered manifest differs from baseline')
    doc, scope = result['doc_source'], run['doc_scope']
    if scope not in ('relevant', 'full'):
        raise ValueError('unsupported baseline document scope')
    base_ex = base.comprehension['execute']
    for label, current in [('baseline', base), ('isolated', cfg)]:
        ex = current.comprehension['execute']
        def normalized(value):
            return {k: v for k, v in value.items() if k not in ('work_dir', 'output_dir')}
        if normalized(ex) != normalized(fp['execute_config']):
            raise ValueError(f'{label}: execution config differs from recorded baseline')
        if ex.get('build'):
            raise ValueError('recovery requires an already built harness; build separately before freezing')
        paths = [Path(p) for g in current.source_globs
                 for p in glob.glob(str(current.root / g), recursive=True)]
        scaffold = current.root / ex['scaffold']
        bindings, _, _ = _execute_sample_data(current, ex)
        fixtures = [Path(p.removeprefix('file://')) for k, p in bindings.items() if k != 'output_dir']
        docs = [*current.original_readme_files]
        if current.llm_readme.exists():
            docs.append(current.llm_readme)
        if any(current.root not in p.resolve().parents for p in paths + fixtures + docs + [scaffold]):
            raise ValueError(f'{label}: source/document/fixture/scaffold escapes its project root')
        for key, actual in [('source', _sha256_files(paths, current.root)),
                            ('scaffold', _sha256_files([scaffold], current.root)),
                            ('fixtures', _sha256_files(fixtures, current.root))]:
            if actual != fp[key]:
                raise ValueError(f'{label}: {key} differs or historical fixture hash included outputs')
        if document_hash(current, doc, names, scope) != run['document_sha256']:
            raise ValueError(f'{label}: delivered documentation differs from baseline')
        for role in ('audience', 'fixer'):
            spec = current.model_for_role(role)
            if f'{spec.provider}:{spec.model}' != run['models'][role]:
                raise ValueError(f'{label}: {role} model differs from baseline')
        profile = current.root / current.raw['files']['project_profile']
        if file_sha(profile) != file_sha(base.root / base.raw['files']['project_profile']):
            raise ValueError('project profile differs between baseline and recovery')
    # This extension must use the same executable engine as the frozen cell.
    import aideal.doc_checks as native
    directory = Path(native.__file__).parent
    files = [directory / n for n in ('config.py', 'doc_checks.py', 'llm.py', 'prompts.py', 'readme_agent.py')]
    if _sha256_files(files, directory) != fp['engine']:
        raise ValueError('native engine differs from baseline; do not mix versions')
    prompts = {}
    for name in ('comprehension_write_exec', 'deep_dive'):
        prompts[name] = file_sha(prompt_file(base, name))
        if prompts[name] != file_sha(prompt_file(cfg, name)):
            raise ValueError(f'prompt differs between baseline and recovery: {name}')
    test_hashes = []
    for current in (base, cfg):
        tests = [Path(p) for g in current.test_globs
                 for p in glob.glob(str(current.root / g), recursive=True)]
        if any(current.root not in p.resolve().parents for p in tests):
            raise ValueError('source-context test files escape project root')
        test_hashes.append(_sha256_files(tests, current.root))
    if test_hashes[0] != test_hashes[1]:
        raise ValueError('upstream test context differs between baseline and isolated copy')
    script = base.root / base_ex['work_dir'] / f'run_{api}' / base_ex['test_filename']
    if not script.is_file():
        raise ValueError('full preserved failing script is missing; truncated error-log code is insufficient')
    # Verify checkpoint ownership. Historical result JSON does not bind the full
    # saved script's bytes; expose that remaining limitation in the identity.
    checkpoint = Path(run['checkpoint'])
    if checkpoint.parent.resolve() != (base.root / base_ex['work_dir']).resolve():
        raise ValueError('baseline checkpoint ownership differs from config')
    identity = {'baseline_fingerprint': run['experiment_fingerprint'],
                'baseline_result_sha256': digest(result), 'api': api,
                'script_sha256': file_sha(script), 'prompt_sha256': prompts,
                'current_effective_config_sha256': digest(cfg.raw),
                'current_profile_sha256': file_sha(cfg.root / cfg.raw['files']['project_profile']),
                'upstream_test_context': test_hashes[0],
                'context_engine': {n: file_sha(directory / n) for n in ('deepdive.py', 'docfix.py')},
                'protocol_sha256': file_sha(POLICY), 'source': fp['source'],
                'document_sha256': run['document_sha256'],
                'script_binding': 'current saved harness; not independently bound by baseline JSON'}
    initial = {'status': 'fail', 'category': metric['error_category'],
               'error': metric.get('error', ''), 'code': script.read_text()}
    return identity, initial
