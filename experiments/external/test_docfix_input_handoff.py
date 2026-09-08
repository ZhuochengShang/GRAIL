import json
from types import SimpleNamespace

import pytest

from experiments.external import docfix_input_handoff as h
from experiments.external.post_b2.test_post_b2 import result


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr(h, 'REPOSITORIES', {'mir_eval': ('GRAIL_mir_eval', 'project', 2)})
    roots = {c: tmp_path/f'GRAIL_mir_eval_{c}'/'project' for c in ('A2', 'B2')}
    native = result()
    for c, root in roots.items():
        path = root/'docs/eval/A2/comprehension.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(native))
    (roots['B2'].parent/'.git').write_text('test worktree')
    def config(path):
        root = roots['A2' if 'GRAIL_mir_eval_A2' in str(path) else 'B2']
        return SimpleNamespace(root=root, language='Python', error_log=root/'logs/B2/error_log.jsonl',
                               comprehension={'execute': {'work_dir': '.exec/A2', 'test_filename': 'test.py', 'region': ['BEGIN','END']}})
    monkeypatch.setattr(h, 'load_config', config)
    return tmp_path, roots


def test_handoff_seeds_A2_before_releasing_alias_and_preserves_append_log(setup):
    parent, roots = setup
    proof = h.prepare('mir_eval', parent)
    alias = roots['B2'].parent/'docs/eval'
    assert alias.resolve() == roots['B2']/'docs/eval'
    log = roots['B2']/'logs/B2/error_log.jsonl'
    rows = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]['function'] == 'first'
    assert proof['source_recovery_evidence_used'] is False
    with log.open('a') as f:
        f.write('{"function":"first","status":"fail","step":"later-validation"}\n')
    assert h.prepare('mir_eval', parent) == proof


def test_handoff_rejects_existing_output_namespace(setup):
    parent, roots = setup
    (roots['B2'].parent/'docs/eval').mkdir(parents=True)
    with pytest.raises(ValueError, match='existing CLI path'):
        h.prepare('mir_eval', parent)


def test_handoff_does_not_overwrite_existing_error_evidence(setup):
    parent, roots = setup
    log = roots['B2']/'logs/B2/error_log.jsonl'
    log.parent.mkdir(parents=True)
    log.write_text('other evidence')
    with pytest.raises(ValueError, match='refusing to overwrite'):
        h.prepare('mir_eval', parent)
    assert log.read_text() == 'other evidence'
    assert not (roots['B2'].parent/'docs/eval').exists()


def test_handoff_detects_changed_seed_prefix(setup):
    parent, roots = setup
    h.prepare('mir_eval', parent)
    (roots['B2']/'logs/B2/error_log.jsonl').write_text('changed')
    with pytest.raises(ValueError, match='prefix changed'):
        h.prepare('mir_eval', parent)
