"""2x2 experiment plumbing: full-document audience context, frozen manifest,
text-only original bundle, coverage sets (reviewer findings #1/#2/#5)."""

import json
import importlib.util
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aideal.config import AidealConfig, ModelSpec, _resolve_readme_sources  # noqa: E402
from aideal.doc_checks import (_comprehension_inventory,  # noqa: E402
                               _load_manifest, _shared_doc_text)
from aideal.readme_agent import api_coverage, _doc_code_mentions  # noqa: E402


def _cfg(tmp_path) -> AidealConfig:
    docs = tmp_path / "docs"; docs.mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "Lib.scala").write_text(
        "class Lib {\n  def foo(x: Int): Int = x\n  def bar(): Int = 1\n"
        "  def baz(): Int = 2\n}\n")
    big = ("# Big original doc\n\nUse `foo` like:\n\n```scala\nlib.foo(1)\n```\n\n"
           "Also bar() is handy.\n\n" + ("lorem ipsum " * 3000))   # >12K chars
    (tmp_path / "README.md").write_text(big)
    (docs / "LLM_readme.md").write_text(
        "## API Test: `foo`\n\nfoo entry.\n\n## API Test: `baz`\n\nbaz entry.\n")
    return AidealConfig(
        root=tmp_path, project_name="t", language="Scala",
        source_globs=["src/**/*.scala"],
        public_def_regex=r"def\s+([a-zA-Z][A-Za-z0-9_]*)",
        exclude_names=[], visibility={}, test_globs=[], surface_filter="all",
        llm_readme=docs / "LLM_readme.md",
        original_readme=tmp_path / "README.md",
        original_readme_files=[tmp_path / "README.md"],
        notes_to_self=docs / "notes.md",
        integration_tasks=tmp_path / "configs" / "t.yaml",
        aliases_file=tmp_path / "aliases" / "a.json",
        error_log=tmp_path / "logs" / "e.jsonl",
        registry={"m": ModelSpec(provider="x", model="m")},
        roles={"author": "m", "audience": "m"},
        runtime_target="local", runtime={}, required_sections=["Goal"],
        comprehension_apis_sampled=5, comprehension={}, puzzle={}, raw={},
    )


def test_bundle_is_text_only_and_deterministic(tmp_path):
    d = tmp_path / "doc"; d.mkdir()
    (d / "b.md").write_text("bee")
    (d / "a.md").write_text("ay")
    (d / "img.png").write_bytes(b"\x89PNG\r\n\x1a\nBINARY")
    (d / "chart.tiff").write_bytes(b"II*\x00BINARY")
    (d / "run.sh").write_text("#!/bin/sh")
    (tmp_path / "R.md").write_text("readme")
    files = _resolve_readme_sources(tmp_path, ["R.md", "doc"])
    names = [f.name for f in files]
    assert names == ["R.md", "a.md", "b.md"]          # sorted, text-only
    # explicit binary path is ALSO rejected
    files2 = _resolve_readme_sources(tmp_path, ["doc/img.png", "R.md"])
    assert [f.name for f in files2] == ["R.md"]


def test_full_doc_is_entire_document_untruncated(tmp_path):
    cfg = _cfg(tmp_path)
    inv, shared, err = _comprehension_inventory(cfg, "original", full_doc=True)
    assert err is None
    assert len(shared) > 12000                       # the old 12K cap is gone
    assert "lorem ipsum" in shared[-200:]            # tail survived
    assert all(e.body == "" for e in inv)            # no per-entry duplication


def test_full_doc_generated_is_whole_catalog(tmp_path):
    cfg = _cfg(tmp_path)
    inv, shared, err = _comprehension_inventory(cfg, "aideal", full_doc=True)
    assert err is None
    assert "foo entry." in shared and "baz entry." in shared   # ENTIRE readme


def test_relevant_scope_retrieves_only_api_sections_with_equal_cap(tmp_path):
    cfg = _cfg(tmp_path)
    cfg.comprehension = {"relevant_doc_chars": 180}
    cfg.original_readme_files[0].write_text(
        "# Intro\nGeneral material.\n\n## Foo\nCall `foo` using lib.foo(1).\n" +
        ("foo detail " * 30) +
        "\n## Unrelated\nOnly `baz` appears here.\n")
    inv_o, shared_o, err_o = _comprehension_inventory(
        cfg, "original", manifest=["foo"], doc_scope="relevant")
    inv_g, shared_g, err_g = _comprehension_inventory(
        cfg, "aideal", manifest=["foo"], doc_scope="relevant")
    assert err_o is err_g is None
    assert shared_o is shared_g is None
    assert "lib.foo(1)" in inv_o[0].body
    assert "Unrelated" not in inv_o[0].body
    assert "foo entry." in inv_g[0].body
    assert len(inv_o[0].body) <= 180 and len(inv_g[0].body) <= 180


def test_original_plus_aideal_combines_both(tmp_path):
    cfg = _cfg(tmp_path)
    shared = _shared_doc_text(cfg, "original+aideal")
    assert "Big original doc" in shared and "foo entry." in shared


def test_manifest_gives_identical_denominator_across_sources(tmp_path):
    cfg = _cfg(tmp_path)
    mp = tmp_path / "docs" / "api_manifest_shared.json"
    mp.write_text(json.dumps({"apis": ["bar", "foo"]}))
    man = _load_manifest(cfg, str(mp))
    inv_o, _, _ = _comprehension_inventory(cfg, "original", manifest=man, full_doc=True)
    inv_g, _, _ = _comprehension_inventory(cfg, "aideal", manifest=man, full_doc=True)
    assert [e.name for e in inv_o] == [e.name for e in inv_g] == ["bar", "foo"]


def test_manifest_rejects_names_outside_surface(tmp_path):
    cfg = _cfg(tmp_path)
    mp = tmp_path / "docs" / "bad.json"
    mp.write_text(json.dumps({"apis": ["foo", "ghost"]}))
    with pytest.raises(ValueError, match="outside the configured public surface"):
        _load_manifest(cfg, str(mp))


def test_api_coverage_sets_and_shared_T(tmp_path):
    cfg = _cfg(tmp_path)
    cov = api_coverage(cfg)
    S = set(cov["surface_S"])
    assert S == {"foo", "bar", "baz"}
    # O: foo in code block/backticks, bar in call-form; 'lorem' words don't count
    assert set(cov["original_documented_O"]) == {"foo", "bar"}
    assert set(cov["generated_documented_G"]) == {"foo", "baz"}
    assert cov["shared_T"] == ["foo"]                 # S ∩ O ∩ G
    assert cov["coverage"]["shared_pct_of_S"] == round(100 / 3, 1)


def test_documented_api_syntax_is_project_configurable(tmp_path):
    cfg = _cfg(tmp_path)
    cfg.original_readme_files[0].write_text("Invoke the Rust-style `baz!` macro.")
    cfg.raw = {"coverage": {"documentation_call_patterns": [r"\b{name}!"]}}
    cov = api_coverage(cfg)
    assert cov["original_documented_O"] == ["baz"]


def test_code_mentions_do_not_span_markdown_fences_or_count_plain_prose():
    text = """The area is discussed in prose.
```scala
lib.foo(1)
```
Later we build an index and call a method.
"""
    assert _doc_code_mentions(text, {"foo", "area", "build", "call"}) == {"foo"}


def test_generic_prompts_do_not_embed_scala_or_rdpro_syntax():
    root = Path(__file__).resolve().parents[1] / "src" / "aideal" / "default_prompts" / "aideal"
    texts = "\n".join((root / name).read_text() for name in (
        "comprehension_write_exec.md", "docfix_diagnose.md",
        "docfix_rewrite.md", "deep_dive.md"))
    for forbidden in ("edu.ucr", "Scala AND Java", "classOf[", "require(n > 0",
                      'println("__CHECK__'):
        assert forbidden not in texts


def test_execution_prompt_rejects_tautological_correctness_checks():
    prompt = (Path(__file__).resolve().parents[1] / "src" / "aideal" /
              "default_prompts" / "aideal" / "comprehension_write_exec.md").read_text()
    assert "FALSIFIABLE" in prompt
    assert "TAUTOLOGIES" in prompt
    assert "Boolean value is either true or false" in prompt
    assert "count, size, offset, or index is merely non-negative" in prompt
    assert "deliberately fail the assertion" in prompt


def test_2x2_guard_requires_matching_scope_zero_rounds_and_hashes():
    script = Path(__file__).resolve().parents[2] / "experiments" / "rdpro" / "compare_2x2.py"
    spec = importlib.util.spec_from_file_location("compare_2x2", script)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    base = {"names": {"foo"}, "full_doc": False, "doc_scope": "relevant",
            "max_fix_rounds": 0,
            "manifest_sha256": "manifest", "document_sha256": "doc"}
    runs = {k: dict(base) for k in ("a1", "a2", "b1", "b2")}
    assert mod.check_design(runs) == []
    runs["a1"]["doc_scope"] = "full"
    runs["a2"]["max_fix_rounds"] = None
    runs["b1"]["manifest_sha256"] = None
    problems = mod.check_design(runs)
    assert any("scope" in p for p in problems)
    assert any("max_fix_rounds" in p for p in problems)
    assert any("manifest hash" in p for p in problems)
