from pathlib import Path

import yaml

from aideal.config import load_config
from aideal.readme_agent import find_or_create, parse_readme


def _config(tmp_path: Path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "api.py").write_text(
        'def alpha(x):\n    """Alpha."""\n    return x\n\n'
        'def beta(x):\n    """Beta."""\n    return x\n',
        encoding="utf-8",
    )
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "profile.yaml").write_text(
        "project:\n  name: resume-test\n  language: Python\n  description: test\n"
        "domain: testing\ntarget_users: [developers]\nuse_cases: [test APIs]\n",
        encoding="utf-8",
    )
    (tmp_path / "configs" / "aideal.yaml").write_text(yaml.safe_dump({
        "extends": ["python"],
        "project": {"name": "resume-test", "language": "Python"},
        "codebase": {"source_globs": ["pkg/**/*.py"], "surface_filter": "all"},
        "files": {
            "project_profile": "configs/profile.yaml",
            "llm_readme": "docs/LLM_readme.md",
        },
        "models": {
            "registry": {"fake": {"provider": "fake", "model": "fake"}},
            "roles": {"author": "fake", "audience": "fake"},
        },
    }), encoding="utf-8")
    return load_config(tmp_path / "configs" / "aideal.yaml")


def _entry(name: str) -> str:
    return (
        f"## API Test: `{name}`\n"
        "### Goal\n"
        f"generated-{name}\n"
        "### Prompt Snippet\n"
        f"Use {name}.\n"
    )


def test_readme_generation_resumes_only_incomplete_entries(tmp_path: Path, monkeypatch):
    cfg = _config(tmp_path)
    first_calls = []

    def interrupted(_model, _system, user):
        name = "alpha" if '"name": "alpha"' in user else "beta"
        first_calls.append(name)
        if name == "beta":
            raise TimeoutError("provider interrupted")
        return _entry(name)

    monkeypatch.setattr("aideal.llm.invoke_text", interrupted)
    first = find_or_create(cfg, generate=True, max_generated=0, force=True)
    assert first_calls == ["alpha", "beta"]
    assert first["generated_ok"] == 1
    assert first["fallback_to_skeleton"] == 1

    resumed_calls = []

    def resumed(_model, _system, user):
        name = "alpha" if '"name": "alpha"' in user else "beta"
        resumed_calls.append(name)
        return _entry(name)

    monkeypatch.setattr("aideal.llm.invoke_text", resumed)
    second = find_or_create(cfg, generate=True, max_generated=0, resume=True)
    assert resumed_calls == ["beta"]
    assert second["resumed_entries"] == 1
    assert second["newly_generated"] == 1
    assert second["generated_ok"] == 2
    assert second["fallback_to_skeleton"] == 0
    assert [e.name for e in parse_readme(cfg.llm_readme)] == ["alpha", "beta"]


def test_readme_resume_rejects_changed_inputs(tmp_path: Path, monkeypatch):
    cfg = _config(tmp_path)
    monkeypatch.setattr("aideal.llm.invoke_text", lambda _m, _s, u: (
        _entry("alpha" if '"name": "alpha"' in u else "beta")))
    find_or_create(cfg, generate=True, max_generated=0, force=True)
    (tmp_path / "pkg" / "api.py").write_text(
        (tmp_path / "pkg" / "api.py").read_text(encoding="utf-8")
        + "\ndef gamma(x):\n    return x\n",
        encoding="utf-8",
    )
    changed = load_config(tmp_path / "configs" / "aideal.yaml")
    try:
        find_or_create(changed, generate=True, max_generated=0, resume=True)
    except ValueError as exc:
        assert "fingerprint changed" in str(exc)
    else:
        raise AssertionError("changed source must invalidate README resume state")
