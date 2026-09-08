import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from aideal.config import ModelSpec
from aideal.doc_checks import (
    _checkpoint_row_reusable,
    _comprehension_fingerprint_components,
)


def _digest(value: dict) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    ).encode()).hexdigest()


def _cfg(root: Path, audience: str = "gemini-2.5-pro"):
    models = {
        "audience": ModelSpec("google", audience),
        "fixer": ModelSpec("google", "gemini-2.5-pro"),
    }
    return SimpleNamespace(
        root=root, raw={},
        source_globs=["source/**/*.py"],
        project_name="fixture-project",
        language="Python",
        model_for_role=lambda role: models[role],
    )


def _components(root: Path, **overrides):
    args = {
        "cfg": _cfg(root),
        "ex": {"command": "python {test_file}", "sample_data": {"fixture": "data/a.txt"}},
        "doc_source": "aideal",
        "doc_scope": "relevant",
        "max_fix_rounds": 0,
        "manifest_sha256": "manifest",
        "document_sha256": "document",
        "scaffold_file": root / "scaffold.py",
        "sample_data": {"fixture": str(root / "data/a.txt")},
        "class_context": False,
        "timeout": 300,
    }
    args.update(overrides)
    return _comprehension_fingerprint_components(**args)


def test_fingerprint_changes_for_scaffold_source_fixture_command_and_model(tmp_path):
    (tmp_path / "source").mkdir()
    (tmp_path / "data").mkdir()
    (tmp_path / "source/api.py").write_text("def api(): pass\n")
    (tmp_path / "data/a.txt").write_text("fixture-v1\n")
    (tmp_path / "scaffold.py").write_text("# scaffold-v1\n")

    baseline = _digest(_components(tmp_path))

    (tmp_path / "scaffold.py").write_text("# scaffold-v2\n")
    assert _digest(_components(tmp_path)) != baseline
    (tmp_path / "scaffold.py").write_text("# scaffold-v1\n")

    (tmp_path / "source/api.py").write_text("def api(): return 1\n")
    assert _digest(_components(tmp_path)) != baseline
    (tmp_path / "source/api.py").write_text("def api(): pass\n")

    (tmp_path / "data/a.txt").write_text("fixture-v2\n")
    assert _digest(_components(tmp_path)) != baseline
    (tmp_path / "data/a.txt").write_text("fixture-v1\n")

    changed_command = _components(
        tmp_path, ex={"command": "python -I {test_file}",
                      "sample_data": {"fixture": "data/a.txt"}})
    assert _digest(changed_command) != baseline

    changed_model = _components(tmp_path, cfg=_cfg(tmp_path, "gemini-3-pro"))
    assert _digest(changed_model) != baseline


def test_fingerprint_changes_for_environment_manifest_and_document(tmp_path, monkeypatch):
    (tmp_path / "source").mkdir()
    (tmp_path / "data").mkdir()
    (tmp_path / "source/api.py").write_text("def api(): pass\n")
    (tmp_path / "data/a.txt").write_text("fixture\n")
    (tmp_path / "scaffold.py").write_text("# scaffold\n")

    monkeypatch.setenv("AIDEAL_ENV_FINGERPRINT", "environment-v1")
    baseline = _digest(_components(tmp_path))
    monkeypatch.setenv("AIDEAL_ENV_FINGERPRINT", "environment-v2")
    assert _digest(_components(tmp_path)) != baseline
    assert _digest(_components(tmp_path, manifest_sha256="other")) != baseline
    assert _digest(_components(tmp_path, document_sha256="other")) != baseline


def test_resume_retries_transient_provider_failures():
    assert _checkpoint_row_reusable(
        {"experiment_fingerprint": "same", "error_category": "runtime"}, "same")
    assert not _checkpoint_row_reusable(
        {"experiment_fingerprint": "same", "error_category": "llm-error"}, "same")
    assert not _checkpoint_row_reusable(
        {"experiment_fingerprint": "old", "error_category": "runtime"}, "same")


def test_outputs_do_not_change_fingerprint_but_uri_input_bytes_do(tmp_path):
    fixture = tmp_path / "input space.txt"
    fixture.write_text("original input")
    output = tmp_path / "out"
    bindings = {"fixture": fixture.as_uri(), "output_dir": str(output)}
    before = _components(tmp_path, sample_data=bindings)
    assert before["fixtures"]["file_count"] == 1
    output.mkdir()
    (output / "model.pkl").write_text("generated")
    assert _components(tmp_path, sample_data=bindings) == before
    (output / "model.pkl").write_text("rewritten")
    assert _components(tmp_path, sample_data=bindings) == before
    fixture.write_text("changed real input")
    assert _components(tmp_path, sample_data=bindings) != before
