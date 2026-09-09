import json
from pathlib import Path
import pytest
from experiments.external.recovery.batch import batch, publish
from experiments.mdanalysis import study_worker


def test_source_rejects_original_baseline(tmp_path):
    with pytest.raises(ValueError, match='only generated-document'):
        batch(None, None, 'mdanalysis', tmp_path, tmp_path, baseline_cell='A1')


def test_post_b2_report_labels_its_actual_baseline(tmp_path):
    publish(tmp_path, {'baseline_cell': 'B2', 'apis': {}})
    assert 'B2 is round zero' in (tmp_path / 'REPORT.md').read_text()


def test_existing_repaired_readme_is_never_overwritten(tmp_path, monkeypatch):
    base, root, out = (tmp_path / name for name in ('A2', 'B2', 'out'))
    for folder, cell, text in [(base, 'A2', 'original generated'), (root, 'B2', 'repaired')]:
        p = folder / f'docs/full_1032/{cell}/LLM_readme.md'
        p.parent.mkdir(parents=True); p.write_text(text)
    monkeypatch.setattr('sys.argv', ['worker', 'copy-doc', '--root', str(root),
        '--baseline-root', str(base), '--out', str(out)])
    with pytest.raises(ValueError, match='refuse to overwrite'):
        study_worker.main()
    assert (root / 'docs/full_1032/B2/LLM_readme.md').read_text() == 'repaired'


def test_protocol_override_is_hashed_and_scoped(monkeypatch):
    from experiments.external.recovery.engine import policy, policy_path
    from experiments.external.recovery.validation import file_sha
    original = policy_path()
    selected = Path(__file__).with_name('protocol_v4.yaml')
    monkeypatch.setenv('AIDEAL_RECOVERY_PROTOCOL', str(selected))
    assert policy()['baseline_cells'] == ['A2', 'B2']
    assert (policy()['max_code_fix_rounds'], policy()['stuck_rounds']) == (5, 2)
    assert file_sha(policy_path()) != file_sha(original)
