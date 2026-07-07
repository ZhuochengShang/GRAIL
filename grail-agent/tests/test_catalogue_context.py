"""Pure-logic tests for the index-first catalogue read path.

Runs in-sandbox (no LLM/Spark): exercises _safe_filenames, _catalogue_model
(collision-safe grouping), and _class_context_body (receiver + verified-sibling
injection). Run: `python -m pytest tests/test_catalogue_context.py -q`
or plain `python tests/test_catalogue_context.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aideal.readme_agent import (  # noqa: E402
    ApiEntry, _safe_filenames, _catalogue_model, _class_context_body,
)


def _entry(name, goal="", pattern=""):
    body = f"## API Test: `{name}`\n\n### Goal\n{goal}\n"
    if pattern:
        body += f"\n### Valid Call Patterns\n```scala\n{pattern}\n```\n"
    return ApiEntry(name=name, goal=goal, snippet="", body=body)


def test_safe_filenames_no_collision_is_identity():
    # RDPro case: every simple name unique -> filename == sanitized label, unchanged.
    gk = {"a/b/Foo": "Foo", "a/b/Bar": "Bar", "c/Baz": "Baz"}
    out = _safe_filenames(gk)
    assert out == {"a/b/Foo": "Foo", "a/b/Bar": "Bar", "c/Baz": "Baz"}
    assert len(set(out.values())) == 3


def test_safe_filenames_collision_disambiguated():
    # General case: same simple name in two packages -> two DISTINCT files, no clobber.
    gk = {"pkg/one/Reader": "Reader", "pkg/two/Reader": "Reader"}
    out = _safe_filenames(gk)
    assert len(set(out.values())) == 2, out
    assert all("Reader" in v for v in out.values())


def test_catalogue_model_groups_by_file_collision_safe():
    entries = [_entry("readA"), _entry("readB")]
    tiers = {"readA": "verified", "readB": "grounded"}
    exec_status = {"readA": "pass", "readB": "fail"}
    class_of = {"readA": "Reader", "readB": "Reader"}          # SAME simple name...
    owner = {"readA": ("Reader", "instance"), "readB": ("Reader", "instance")}
    file_of = {"readA": "pkg/one/Reader.scala",               # ...DIFFERENT files
               "readB": "pkg/two/Reader.scala"}
    model = _catalogue_model(entries, tiers, exec_status, class_of, owner, file_of=file_of)
    assert len(model) == 2, "two distinct classes must not merge into one group"
    labels = sorted(m["label"] for m in model.values())
    assert labels == ["Reader", "Reader"]
    safes = {m["safe"] for m in model.values()}
    assert len(safes) == 2, f"per-class files must be unique, got {safes}"


def test_catalogue_model_ranks_primary_by_tier_then_exec():
    entries = [_entry("lo", goal="low"), _entry("hi", goal="high goal")]
    tiers = {"hi": "verified", "lo": "guessed"}
    exec_status = {"hi": "pass", "lo": ""}
    class_of = {"hi": "K", "lo": "K"}
    owner = {"hi": ("K", "static"), "lo": ("K", "static")}
    file_of = {"hi": "p/K.scala", "lo": "p/K.scala"}
    model = _catalogue_model(entries, tiers, exec_status, class_of, owner, file_of=file_of)
    (m,) = model.values()
    assert m["primary"] == "hi"                    # verified+pass beats guessed
    assert m["purpose"] == "high goal"             # purpose taken from primary's Goal
    assert m["kind"] == "static"


def test_class_context_injects_receiver_and_verified_sibling():
    target = _entry("mapPixels", goal="map over pixels")
    sibling = _entry("overlay", goal="overlay rasters",
                     pattern="val r = sc.geoTiff[Float](path); r.overlay(other)")
    entries = [target, sibling]
    tiers = {"overlay": "verified", "mapPixels": "grounded"}
    exec_status = {"overlay": "pass", "mapPixels": "fail"}
    class_of = {"overlay": "RasterOperationsLocal", "mapPixels": "RasterOperationsLocal"}
    owner = {"overlay": ("RasterOperationsLocal", "instance"),
             "mapPixels": ("RasterOperationsLocal", "instance")}
    file_of = {"overlay": "raptor/RasterOperationsLocal.scala",
               "mapPixels": "raptor/RasterOperationsLocal.scala"}
    model = _catalogue_model(entries, tiers, exec_status, class_of, owner, file_of=file_of)
    name_to_gkey = {x["name"]: g for g, m in model.items() for x in m["members"]}
    by_name = {e.name: e for e in entries}

    out = _class_context_body(target, model, name_to_gkey, by_name)
    assert "Class context" in out and "RasterOperationsLocal" in out
    assert "Obtaining the receiver" in out                     # receiver line present
    assert "sc.geoTiff[Float]" in out                          # verified sibling pattern injected
    assert "overlay" in out                                    # names the proven sibling
    assert target.body in out                                  # target's own doc preserved
    # ordering: class context comes BEFORE the target's own section
    assert out.index("Class context") < out.index("### Goal\nmap over pixels")


def test_class_context_noop_when_target_is_primary():
    # If the target IS the most-robust member, there is no better sibling to show;
    # still emit the receiver line, but do not inject a sibling pattern block.
    only = _entry("solo", goal="the one", pattern="val x = Solo(); x.solo()")
    entries = [only]
    model = _catalogue_model(entries, {"solo": "verified"}, {"solo": "pass"},
                             {"solo": "Solo"}, {"solo": ("Solo", "instance")},
                             file_of={"solo": "p/Solo.scala"})
    name_to_gkey = {x["name"]: g for g, m in model.items() for x in m["members"]}
    out = _class_context_body(only, model, name_to_gkey, {"solo": only})
    assert "Obtaining the receiver" in out
    assert "Proven setup from" not in out                      # no sibling block


def test_class_context_noop_when_class_unknown():
    orphan = _entry("ghost")
    out = _class_context_body(orphan, {}, {}, {"ghost": orphan})
    assert out == orphan.body                                  # unchanged fallback


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")
