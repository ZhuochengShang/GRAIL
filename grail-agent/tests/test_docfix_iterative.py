"""Iterative deep-dive docfix loop: control-flow tests with mocked LLM +
harness. Covers: pass-on-round-k keeps the final draft; all-rounds-fail
reverts to the original entry; no-improvement early stop; draft carried
across rounds; per-round trail recorded with understanding flags."""

import json
import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import aideal.docfix as docfix  # noqa: E402
import aideal.llm as llm  # noqa: E402
import aideal.doc_checks as doc_checks  # noqa: E402
from aideal.config import AidealConfig, ModelSpec  # noqa: E402


README = """## API Test: `foo`

Original entry body for foo.

```scala
val x = obj.foo(1)
```

## API Test: `bar`

bar body.
"""


def _cfg(tmp_path) -> AidealConfig:
    readme = tmp_path / "docs" / "LLM_readme.md"
    readme.parent.mkdir(parents=True)
    readme.write_text(README, encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "Lib.scala").write_text(
        "class Lib {\n  def foo(x: Int): Int = x\n}\n", encoding="utf-8")
    return AidealConfig(
        root=tmp_path, project_name="t", language="Scala",
        source_globs=["src/**/*.scala"],
        public_def_regex=r"def\s+([a-zA-Z][A-Za-z0-9_]*)",
        exclude_names=[], visibility={}, test_globs=[], surface_filter="all",
        llm_readme=readme, original_readme=None, original_readme_files=[],
        notes_to_self=tmp_path / "docs" / "notes.md",
        integration_tasks=tmp_path / "configs" / "t.yaml",
        aliases_file=tmp_path / "aliases" / "a.json",
        error_log=tmp_path / "logs" / "error_log.jsonl",
        registry={"m": ModelSpec(provider="x", model="m")},
        roles={"author": "m", "audience": "m", "fixer": "m"},
        runtime_target="local", runtime={}, required_sections=["Goal"],
        comprehension_apis_sampled=5,
        comprehension={"execute": {"auto_report": False}}, puzzle={}, raw={},
    )


class Script:
    """Programmable stand-ins for the LLM and the comprehension harness."""

    def __init__(self, diagnoses, rewrites, retry_outcomes):
        self.diagnoses = list(diagnoses)      # per diagnose call
        self.rewrites = list(rewrites)        # per rewrite call
        self.retries = list(retry_outcomes)   # per retry: (status, cat, err)
        self.rewrite_inputs = []              # entry_body seen by rewrite

    def invoke_text(self, spec, system, user):
        # prompts.load is patched to return (template_name, repr(kwargs)) —
        # route on the template name, capture the rewrite's entry_body input.
        if system.endswith("docfix_diagnose"):
            return self.diagnoses.pop(0) if self.diagnoses else "diag"
        self.rewrite_inputs.append(user)
        return self.rewrites.pop(0) if self.rewrites else "rewrite"

    def comprehension_check(self, cfg, api=None, execute=True,
                            max_fix_rounds=0, timeout_s=None, **kw):
        self.retry_calls = getattr(self, "retry_calls", [])
        self.retry_calls.append({"api": api, "max_fix_rounds": max_fix_rounds, **kw})
        if getattr(self, "on_retry", None):
            self.on_retry()
        status, cat, err = self.retries.pop(0)
        return {"metrics": {api: {"status": status, "error_category": cat}},
                "details": {api: (f"fail [{cat}]: {err}" if status != "pass"
                                  else "pass")}}


@pytest.fixture()
def patched(monkeypatch):
    def _apply(script: Script):
        monkeypatch.setattr(llm, "invoke_text", script.invoke_text)
        monkeypatch.setattr(llm, "usage_snapshot",
                            lambda: {"calls": 0, "input_tokens": 0,
                                     "output_tokens": 0, "by_model": {}})
        monkeypatch.setattr(llm, "usage_delta",
                            lambda b: {"calls": 1, "input_tokens": 10,
                                       "output_tokens": 5, "by_model": {}})
        monkeypatch.setattr(doc_checks, "comprehension_check",
                            script.comprehension_check)
        monkeypatch.setattr(doc_checks, "_owner_map", lambda cfg: {})
        monkeypatch.setattr(doc_checks, "_receiver_hint", lambda n, o: "")
        import aideal.profile as profile
        monkeypatch.setattr(profile, "require_profile", lambda cfg: None)
        import aideal.prompts as prompts
        monkeypatch.setattr(prompts, "load",
                            lambda cfg, name, **kw: (name, repr(kw)))
        monkeypatch.setattr(docfix, "_type_context", lambda cfg, n: "(types)")
        monkeypatch.setattr(docfix, "_source_window",
                            lambda cfg, n: ("// src", "(none)"))
    return _apply


def _entry(text):
    return "## API Test: `foo`\n\n" + text + "\n\n```scala\nval y = obj.foo(2)\nprintln(y)\n```"


def test_pass_on_second_round_keeps_final_draft(tmp_path, patched):
    cfg = _cfg(tmp_path)
    s = Script(
        diagnoses=["ROOT CAUSE:\nwrong receiver\n", "ROOT CAUSE:\nmissing import\n"],
        rewrites=[_entry("draft v1"), _entry("draft v2")],
        retry_outcomes=[("fail", "compile", "error: not found: value spark"),
                        ("pass", None, "")],
    )
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=5, doc_stuck=2,
                             retry_rounds=0)
    r = rep["apis"]["foo"]
    assert r["status"] == "doc-fixed"
    assert r["rounds_used"] == 2
    assert [d["retry_status"] for d in r["doc_rounds"]] == ["fail", "pass"]
    # round 2's rewrite saw round 1's DRAFT, not the original entry
    assert "draft v1" in s.rewrite_inputs[1]
    # the final draft is KEPT in the catalog
    assert "draft v2" in cfg.llm_readme.read_text()
    assert "Original entry body for foo" not in cfg.llm_readme.read_text()
    assert (cfg.llm_readme.parent / "docfix_changes" / "foo.before.md").exists()


def test_all_rounds_fail_reverts_original(tmp_path, patched):
    cfg = _cfg(tmp_path)
    s = Script(
        diagnoses=[f"ROOT CAUSE:\ncause {i}\n" for i in range(3)],
        rewrites=[_entry(f"draft {i}") for i in range(3)],
        retry_outcomes=[("fail", "compile", f"error: e{i}") for i in range(3)],
    )
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=3, doc_stuck=0,
                             retry_rounds=0)
    r = rep["apis"]["foo"]
    assert r["status"].startswith("still-failing")
    assert r["rounds_used"] == 3
    text = cfg.llm_readme.read_text()
    assert "Original entry body for foo" in text       # reverted
    assert "draft" not in text.split("## API Test: `bar`")[0]


def test_no_improvement_early_stop(tmp_path, patched):
    cfg = _cfg(tmp_path)
    same_diag = "ROOT CAUSE:\nsame cause forever\n"
    s = Script(
        diagnoses=[same_diag] * 5,
        rewrites=[_entry(f"draft {i}") for i in range(5)],
        retry_outcomes=[("fail", "compile", "error: identical failure")] * 5,
    )
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=5, doc_stuck=2,
                             retry_rounds=0)
    r = rep["apis"]["foo"]
    # r0: diagnosis counts as changed (first) but error same as baseline sig?
    # baseline had no recorded error -> first round counts as progressed;
    # afterwards nothing changes -> stop after 2 stagnant rounds, well before 5.
    assert r["rounds_used"] < 5
    assert r["status"].startswith("still-failing")
    assert "no-improvement" in r["status"]
    flags = [(d.get("diagnosis_changed"), d.get("error_progressed"))
             for d in r["doc_rounds"]]
    assert flags[-1] == (False, False)


def test_not_testable_stops_immediately(tmp_path, patched):
    cfg = _cfg(tmp_path)
    s = Script(
        diagnoses=["VERDICT: NOT-TESTABLE — protected[pkg], external harness "
                   "cannot call it"],
        rewrites=[], retry_outcomes=[],
    )
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=5, retry_rounds=0)
    r = rep["apis"]["foo"]
    assert r["status"].startswith("not-testable")
    assert r["rounds_used"] == 1
    assert "Original entry body for foo" in cfg.llm_readme.read_text()


def _cfg_orig(tmp_path):
    """Config whose catalog is EMPTY and whose original readme exists —
    the original-readme arm."""
    cfg = _cfg(tmp_path)
    cfg.llm_readme.write_text("", encoding="utf-8")
    orig = tmp_path / "README.md"
    orig.write_text("# Lib\nUse foo to frobnicate.", encoding="utf-8")
    cfg.original_readme_files = [orig]
    return cfg


def test_create_missing_creates_entry_on_pass(tmp_path, patched):
    cfg = _cfg_orig(tmp_path)
    s = Script(diagnoses=["ROOT CAUSE:\nno doc at all\n"],
               rewrites=[_entry("created entry v1")],
               retry_outcomes=[("pass", None, "")])
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=None, from_results=None,
                             doc_rounds=3, retry_rounds=0, create_missing=True,
                             max_apis=None)
    # no failures in log -> no targets; instead drive via explicit apis
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=3, retry_rounds=0,
                             create_missing=True)
    # apis= path filters on entries; foo absent -> goes to missing -> created
    r = rep["apis"].get("foo")
    assert r is not None and r["status"] == "doc-created"
    text = cfg.llm_readme.read_text()
    assert "created entry v1" in text
    # round-0 diagnosis/rewrite saw the ORIGINAL readme as the current doc
    assert "frobnicate" in s.rewrite_inputs[0]


def test_create_missing_removes_entry_on_all_fail(tmp_path, patched):
    cfg = _cfg_orig(tmp_path)
    s = Script(diagnoses=[f"ROOT CAUSE:\ncause {i}\n" for i in range(2)],
               rewrites=[_entry(f"created draft {i}") for i in range(2)],
               retry_outcomes=[("fail", "compile", f"error: e{i}") for i in range(2)])
    patched(s)
    rep = docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=2, doc_stuck=0,
                             retry_rounds=0, create_missing=True)
    r = rep["apis"]["foo"]
    assert r["status"].startswith("still-failing")
    assert "created draft" not in cfg.llm_readme.read_text()   # reverted to ABSENT


def test_guard_allows_repo_called_members(tmp_path, patched):
    """The general allowlist: a member the target repo ITSELF calls is
    accepted without any curated category; a never-called member is rejected."""
    cfg = _cfg(tmp_path)
    # the repo's own code calls .frobnicate(...) somewhere
    (tmp_path / "src" / "Uses.scala").write_text(
        "object Uses {\n  def run(): Unit = { thing.frobnicate(1) }\n}\n",
        encoding="utf-8")
    allowed = docfix._allowed_members_from_config(cfg)
    assert "frobnicate" in allowed          # mined from repo sources
    fab = docfix._fabricated_members(
        "```scala\nx.frobnicate(1)\nx.zorblify(2)\n```",
        surface={"foo"}, api_name="foo", allowed_members=allowed)
    assert fab == ["zorblify"]              # never called anywhere -> rejected


def test_guard_yaml_categories_override_python_fallback(tmp_path, patched):
    cfg = _cfg(tmp_path)
    cfg.raw["docfix"] = {
        "allow_repo_called_members": False,
        "allowed_member_categories": ["language_core", "mystuff"],
        "member_categories": {"language_core": ["onlyThis"],
                              "mystuff": ["customCall"]},
    }
    allowed = docfix._allowed_members_from_config(cfg)
    assert {"onlyThis", "customCall"} <= allowed
    # YAML definition REPLACES the hardcoded language_core fallback
    assert "mkString" not in allowed


def test_retry_is_zero_rounds_and_carries_doc_context(tmp_path, patched):
    """2x2 invariants at the docfix retry: 0 snippet-fix rounds, and the
    doc_source/full_doc/manifest of the ARM flow through to every retry."""
    cfg = _cfg(tmp_path)
    s = Script(diagnoses=["ROOT CAUSE:\nx\n"], rewrites=[_entry("d1")],
               retry_outcomes=[("pass", None, "")])
    patched(s)
    docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=5, retry_rounds=0,
                       doc_source="original+aideal", full_doc=True,
                       manifest="docs/api_manifest_shared.json")
    call = s.retry_calls[0]
    assert call["max_fix_rounds"] == 0
    assert call["doc_source"] == "original+aideal"
    assert call["full_doc"] is True
    assert call["manifest"] == "docs/api_manifest_shared.json"


def test_per_round_live_persistence(tmp_path, patched):
    """Reviewer finding #4: the ACTIVE api's rounds must be in the JSON report
    while the loop is still running — checked from INSIDE round 2's retry."""
    import json as _json
    cfg = _cfg(tmp_path)
    report = tmp_path / "docfix_report.json"
    seen = []
    s = Script(diagnoses=[f"ROOT CAUSE:\nc{i}\n" for i in range(2)],
               rewrites=[_entry(f"d{i}") for i in range(2)],
               retry_outcomes=[("fail", "compile", "error: e0"), ("pass", None, "")])

    def peek():
        if report.exists():
            seen.append(_json.loads(report.read_text()))
    s.on_retry = peek
    patched(s)
    docfix.doc_fix_run(cfg, apis=["foo"], doc_rounds=3, retry_rounds=0,
                       report_path=report)
    mid = seen[-1]["apis"].get("foo")   # during round 2's retry
    assert mid is not None and mid["status"] == "in-progress"
    assert len(mid["doc_rounds"]) == 1 and mid["doc_rounds"][0]["round"] == 0
    final = _json.loads(report.read_text())["apis"]["foo"]
    assert final["status"] == "doc-fixed" and len(final["doc_rounds"]) == 2
