"""Offline review probes; temporary files only, no model or experiment calls.

These document current failure modes, not a passing robustness certification.
Run from the checkout with its existing interpreter and PYTHONPATH=grail-agent/src:.
"""
import argparse
from copy import deepcopy
from datetime import datetime
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace

from aideal.config import ModelSpec
from aideal.doc_checks import _classify_error_py, _comprehension_fingerprint_components
from aideal.prompts import load as load_prompt
from experiments.external.assertion_replay.evidence import collect
from experiments.external.post_b2.evidence import fingerprint, matched
from experiments.external.provider_retry.enroll import BOOTSTRAP


def run():
    findings = {}
    with tempfile.TemporaryDirectory(prefix='aideal_code_review_') as directory:
        root = Path(directory)
        project = root / 'fresh_project'
        checkpoint = project / '.aideal_exec/B2/comprehension_progress.jsonl'
        checkpoint.parent.mkdir(parents=True)
        checkpoint.write_text(json.dumps({'name': 'example', 'status': 'pass',
                                         'experiment_fingerprint': 'fresh'}) + '\n')
        findings['fresh_checkpoint_hidden'] = collect(project, 'B2') is None

        prompt = project / 'prompts/aideal/comprehension_write_exec.md'
        prompt.parent.mkdir(parents=True)
        prompt.write_text('SYSTEM:\nVersion one. {project_context}\nUSER:\n{api_body}')
        profile = project / 'profile.yaml'
        profile.write_text('role: reviewer one\n')
        scaffold = project / 'scaffold.py'
        scaffold.write_text('# fixed scaffold\n')
        cfg = SimpleNamespace(root=project, source_globs=[], project_name='toy',
                              language='Python', raw={'files': {'project_profile': 'profile.yaml'}},
                              model_for_role=lambda _: ModelSpec('google', 'same-model'))
        def identity():
            return _comprehension_fingerprint_components(
                cfg, ex={'command': 'python test.py'}, doc_source='aideal', doc_scope='relevant',
                max_fix_rounds=0, manifest_sha256='same-manifest', document_sha256='same-doc',
                scaffold_file=scaffold, sample_data={}, class_context=False, timeout=300)
        before = identity()
        delivered = load_prompt(cfg, 'aideal/comprehension_write_exec', api_body='same-doc')
        prompt.write_text('SYSTEM:\nVersion two. {project_context}\nUSER:\n{api_body}')
        findings['prompt_changes_without_native_fingerprint_change'] = (
            before == identity() and delivered != load_prompt(
                cfg, 'aideal/comprehension_write_exec', api_body='same-doc'))
        delivered = load_prompt(cfg, 'aideal/comprehension_write_exec', api_body='same-doc')
        profile.write_text('role: reviewer two\n')
        findings['profile_changes_without_native_fingerprint_change'] = (
            before == identity() and delivered != load_prompt(
                cfg, 'aideal/comprehension_write_exec', api_body='same-doc'))

        bootstrap = root / 'bootstrap'
        bootstrap.mkdir()
        (bootstrap / 'sitecustomize.py').write_text(BOOTSTRAP)
        (bootstrap / 'aideal_transport_policy.json').write_text('{invalid')
        proc = subprocess.run(
            [sys.executable, '-c', 'print("CLI_BODY_RAN")', '--config',
             str(bootstrap / 'config.yaml'), 'comprehension', '--resume',
             '--max-fix-rounds', '0'], cwd=bootstrap,
            env=dict(os.environ, PYTHONPATH=str(bootstrap)), capture_output=True,
            text=True, timeout=10)
        findings['malformed_policy_continues'] = {
            'reproduced': proc.returncode == 0 and 'CLI_BODY_RAN' in proc.stdout,
            'exit_code': proc.returncode, 'stdout': proc.stdout.strip(),
            'stderr': proc.stderr.strip()}

        marker = root / 'child_finished.txt'
        child = ('import time; from pathlib import Path; time.sleep(0.3); '
                 f'Path({str(marker)!r}).write_text("finished")')
        # The trailing shell command ensures the shell retains a distinct child.
        command = shlex.join([sys.executable, '-c', child]) + '; :'
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True, timeout=.05)
        except subprocess.TimeoutExpired:
            pass
        time.sleep(.5)  # Only this finite toy child; never touch experiment PIDs.
        findings['child_survives_shell_timeout'] = marker.exists()

    components = {key: key for key in
                  ('project', 'language', 'manifest_sha256', 'scaffold', 'source', 'fixtures', 'engine')}
    components.update(schema=3, doc_source='aideal', doc_scope='relevant', max_fix_rounds=0,
                      models={'audience': 'same', 'fixer': 'same'}, class_context=False,
                      timeout_s=600, document_sha256='document',
                      execute_config={'work_dir': 'work', 'output_dir': 'out', 'command': 'test'},
                      interpreter={'executable': '/python', 'version': 'same',
                                   'environment_sha256': 'inventory'})
    a2 = {'doc_source': 'aideal', 'run': {**components, 'api_count': 1,
          'fingerprint_components': components, 'experiment_fingerprint': fingerprint(components)},
          'metrics': {'example': {'status': 'pass'}}}
    b2 = deepcopy(a2)
    a2['run']['transport_policy'] = {'timeout': 600, 'attempts': 1}
    b2['run']['transport_policy'] = {'timeout': 300, 'attempts': 2}
    findings['matching_ignores_extra_transport_provenance'] = bool(matched(a2, b2, 1))
    findings['nonexistent_symbol_import_category'] = _classify_error_py(
        "ImportError: cannot import name 'squared_distance_profile' from 'tslearn.metrics'",
        1, '__ERROR__')[0]
    return {'timestamp': datetime.now().astimezone().isoformat(),
            'scope': 'Seven offline failure-mode probes; no provider/API experiment executed',
            'findings': findings}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = run()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
