from pathlib import Path

import yaml

from aideal.config import load_config
from aideal.doc_checks import _execute_sample_data
from aideal.readme_agent import (intended_api_llm, intent_scores,
                                 public_api_details, public_api_surface)


def test_python_qualified_identity_and_local_exclusion(tmp_path: Path):
    pkg = tmp_path / "src" / "sciencepkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "analysis.py").write_text(
        "def distance(x, y):\n"
        "    def local_helper():\n"
        "        return 0\n"
        "    return x - y\n\n"
        "class RMSD:\n"
        "    def run(self):\n"
        "        return 1\n\n"
        "class Contacts:\n"
        "    def run(self):\n"
        "        return 2\n\n"
        "class Mode(int): \"\"\"An integer mode.\"\"\"\n",
        encoding="utf-8",
    )
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "aideal.yaml").write_text(yaml.safe_dump({
        "extends": ["python"],
        "project": {"name": "sciencepkg", "language": "Python"},
        "codebase": {"source_globs": ["src/sciencepkg/**/*.py"]},
    }), encoding="utf-8")

    cfg = load_config(tmp_path / "configs" / "aideal.yaml")
    details = public_api_details(cfg)
    by_qualified = {d["qualified_name"]: d for d in details}
    assert "sciencepkg.analysis.distance" in by_qualified
    assert "sciencepkg.analysis.RMSD" in by_qualified
    assert "sciencepkg.analysis.RMSD.run" in by_qualified
    assert "sciencepkg.analysis.Contacts.run" in by_qualified
    assert by_qualified["sciencepkg.analysis.Mode"]["signature"] == "class Mode(int)"
    assert by_qualified["sciencepkg.analysis.Mode"]["params"] == []
    assert by_qualified["sciencepkg.analysis.Mode"]["returns"] == ""
    assert not any(d["name"] == "local_helper" for d in details)
    assert "local_helper" not in intent_scores(cfg)
    assert "local_helper" not in public_api_surface(cfg, override_filter="all")
    assert by_qualified["sciencepkg.analysis.RMSD.run"]["owner"] == "RMSD"
    assert by_qualified["sciencepkg.analysis.RMSD.run"]["definition_kind"] == "method"


def test_qualified_intent_keeps_same_bare_name_separate(tmp_path: Path, monkeypatch):
    pkg = tmp_path / "sciencepkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "ops.py").write_text(
        "class RMSD:\n    def run(self):\n        return 1\n\n"
        "class Contacts:\n    def run(self):\n        return 2\n",
        encoding="utf-8")
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "profile.yaml").write_text(
        "project:\n  name: x\n  language: Python\n  description: x\n"
        "target_users: [x]\nuse_cases: [x]\ndomain: x\n", encoding="utf-8")
    cfg_data = {
        "extends": ["python"], "project": {"name": "x", "language": "Python"},
        "codebase": {
            "source_globs": ["sciencepkg/**/*.py"],
            "intent": {"threshold": -100},
            "intended_api": {"identity": "qualified", "static_include_threshold": 999,
                             "static_exclude_threshold": -999, "batch_size": 25,
                             "cache": "docs/q.json"}},
        "files": {"project_profile": "configs/profile.yaml"},
        "models": {"registry": {"judge": {"provider": "fake", "model": "judge"}},
                   "roles": {"author": "judge"}},
    }
    (tmp_path / "configs" / "aideal.yaml").write_text(
        yaml.safe_dump(cfg_data), encoding="utf-8")
    cfg = load_config(tmp_path / "configs" / "aideal.yaml")

    def fake_invoke(_model, _system, user):
        assert "sciencepkg.ops.RMSD.run" in user
        assert "sciencepkg.ops.Contacts.run" in user
        return ('[{"name":"sciencepkg.ops.RMSD.run","decision":"include","reason":"yes"},'
                '{"name":"sciencepkg.ops.Contacts.run","decision":"exclude","reason":"no"}]')

    monkeypatch.setattr("aideal.llm.invoke_text", fake_invoke)
    selected, decisions = intended_api_llm(cfg)
    assert selected == {"sciencepkg.ops.RMSD.run"}
    assert decisions["sciencepkg.ops.Contacts.run"]["decision"] == "exclude"


def test_fixed_budget_preserves_capability_family_breadth(tmp_path: Path, monkeypatch):
    pkg = tmp_path / "sciencepkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "ops.py").write_text(
        "def distance():\n    return 1\n\n"
        "def distance_fast():\n    return 1\n\n"
        "def cluster():\n    return 1\n",
        encoding="utf-8")
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "profile.yaml").write_text(
        "project:\n  name: x\n  language: Python\n  description: x\n"
        "target_users: [x]\nuse_cases: [x]\ndomain: x\n", encoding="utf-8")
    (tmp_path / "configs" / "aideal.yaml").write_text(yaml.safe_dump({
        "extends": ["python"], "project": {"name": "x", "language": "Python"},
        "codebase": {"source_globs": ["sciencepkg/**/*.py"],
                     "intent": {"threshold": -100},
                     "intended_api": {
                         "identity": "qualified", "selection_limit": 2,
                         "static_include_threshold": 999,
                         "static_exclude_threshold": -999,
                         "cache": "docs/q.json"}},
        "files": {"project_profile": "configs/profile.yaml"},
        "models": {"registry": {"judge": {"provider": "fake", "model": "judge"}},
                   "roles": {"author": "judge"}},
    }), encoding="utf-8")
    cfg = load_config(tmp_path / "configs" / "aideal.yaml")

    def fake_invoke(_model, _system, _user):
        return """[
          {"name":"sciencepkg.ops.distance","decision":"include","capability_family":"geometry/distance","ratings":{"user_facing":3,"fixture_runnable":3,"oracle_strength":3,"domain_relevance":3},"reason":"core"},
          {"name":"sciencepkg.ops.distance_fast","decision":"include","capability_family":"geometry/distance","ratings":{"user_facing":3,"fixture_runnable":3,"oracle_strength":3,"domain_relevance":3},"reason":"variant"},
          {"name":"sciencepkg.ops.cluster","decision":"include","capability_family":"analysis/clustering","ratings":{"user_facing":2,"fixture_runnable":2,"oracle_strength":2,"domain_relevance":2},"reason":"distinct family"}
        ]"""

    monkeypatch.setattr("aideal.llm.invoke_text", fake_invoke)
    selected, decisions = intended_api_llm(cfg)
    assert len(selected) == 2
    assert "sciencepkg.ops.cluster" in selected
    assert len({decisions[n]["capability_family"] for n in selected}) == 2
    assert decisions["sciencepkg.ops.distance_fast"]["selected_in_budget"] is False


def test_package_resource_sample_data(tmp_path: Path):
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "aideal.yaml").write_text(yaml.safe_dump({
        "extends": ["python"],
        "project": {"name": "x", "language": "Python"},
        "codebase": {"source_globs": []},
    }), encoding="utf-8")
    cfg = load_config(tmp_path / "configs" / "aideal.yaml")
    data, _shown, warnings = _execute_sample_data(cfg, {
        "local_uris": False,
        "sample_data": {
            "fixture": {"package": "aideal", "resource": "__init__.py"},
        },
    })
    assert Path(data["fixture"]).name == "__init__.py"
    assert Path(data["fixture"]).is_file()
    assert not warnings
