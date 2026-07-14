"""Pure-logic tests for the intent-signal fixes (TODO item 1).

No LLM / Spark / project config needed.
Run: `python -m pytest tests/test_intent_dedup.py -q` or plain
`python tests/test_intent_dedup.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aideal.readme_agent import _doc_code_mentions, _subsume_overloads  # noqa: E402


def _rec(file, line, types, doc=""):
    return {"file": file, "line": line, "description": doc,
            "signature": f"def f({', '.join(types)})",
            "params": [{"name": f"p{i}", "type": t} for i, t in enumerate(types)]}


def test_telescoping_overloads_subsumed_longest_canonical():
    # foo(x) ⊂ foo(x,y) ⊂ foo(x,y,z) in ONE file -> one function; canonical is
    # the longest ("needed longest parameters"), both short forms subsumed by it.
    a = _rec("A.scala", 10, ["Int"])
    b = _rec("A.scala", 20, ["Int", "String"], doc="the base doc")
    c = _rec("A.scala", 30, ["Int", "String", "Boolean"])
    maximals, subsumed = _subsume_overloads([a, b, c])
    assert maximals == [c]
    assert {(s["line"], by["line"]) for s, by in subsumed} == {(10, 30), (20, 30)}


def test_cross_file_same_name_never_subsumed():
    # run(opts) in two unrelated classes: interface impls, not one function.
    a = _rec("A.scala", 5, ["Opts"])
    b = _rec("B.scala", 5, ["Opts", "SparkContext"])
    maximals, subsumed = _subsume_overloads([a, b])
    assert subsumed == [] and len(maximals) == 2
    assert maximals[0] is b  # longest still sorts first


def test_different_types_are_distinct_variants():
    # foo(Int) vs foo(String): same arity, different types -> both kept.
    a = _rec("A.scala", 1, ["Int"])
    b = _rec("A.scala", 2, ["String"])
    maximals, subsumed = _subsume_overloads([a, b])
    assert subsumed == [] and len(maximals) == 2


def test_zero_arg_form_subsumed_by_parametrized():
    a = _rec("A.scala", 1, [])
    b = _rec("A.scala", 2, ["Int"])
    maximals, subsumed = _subsume_overloads([a, b])
    assert maximals == [b] and subsumed[0][0] is a


def test_fabricated_members_flags_only_nonsurface_calls():
    from aideal.docfix import _fabricated_members
    entry = """## API Test: `addTile`
```scala
val r = rasterRDD.convolve(kernel)      // fabricated — not on surface
val ok = MetaData.retile(rdd, meta)     // real surface member
println("__CHECK__ addTile " + r.count())
require(r.count() > 0, "empty")
```
"""
    surface = {"retile", "addTile", "geoTiff"}
    assert _fabricated_members(entry, surface, "addTile") == ["convolve"]
    # entry that only uses surface + stdlib -> clean
    clean = "```scala\nval x = sc.geoTiff(p)\nprintln(x.count())\n```"
    assert _fabricated_members(clean, {"geoTiff"}, "geoTiff") == []


def test_fabricated_members_allows_ecosystem_helpers():
    from aideal.docfix import _ALLOWED_MEMBER_CATEGORIES, _fabricated_members
    entry = """## API Test: `area`
```scala
val spark = SparkSession.builder().appName("x").master("local[*]").getOrCreate()
val geom = factory.createPoint(coord)
val arr = Array.fill[Double](2)(0.0)
val ok = !arr(0).isNaN && !arr(0).isInfinite
val angle = Math.toRadians(42.0)
val df = spark.read.format("geojson").load(path)
import spark.implicits._
val df2 = rdd.toDF()
val n = df.rdd.getNumPartitions
val px = tile.getPixelValueAsFloat(0, 0)
```
"""
    allowed = set().union(
        _ALLOWED_MEMBER_CATEGORIES["language_core"],
        _ALLOWED_MEMBER_CATEGORIES["spark"],
        _ALLOWED_MEMBER_CATEGORIES["geometry_common"],
        _ALLOWED_MEMBER_CATEGORIES["raster_common"],
    )
    assert _fabricated_members(entry, {"area"}, "area", allowed) == []


def test_replace_entry_text_swaps_one_section():
    from aideal.docfix import _replace_entry_text
    text = ("# Catalog\n\n## API Test: `foo`\n\nold foo body\n\n"
            "## API Test: `bar`\n\nbar body\n")
    out = _replace_entry_text(text, "foo", "## API Test: `foo`\n\nNEW foo body")
    assert "NEW foo body" in out and "old foo body" not in out
    assert "bar body" in out                      # neighbors untouched
    out2 = _replace_entry_text(text, "bar", "## API Test: `bar`\n\nNEW bar")
    assert out2.rstrip().endswith("NEW bar")      # last entry (EOF case)
    try:
        _replace_entry_text(text, "nope", "x"); raise AssertionError("should raise")
    except KeyError:
        pass


def test_failed_apis_from_results_targets_specific_run(tmp_path):
    from aideal.docfix import _failed_apis_from_results
    p = tmp_path / "g1.json"
    p.write_text("""{
      "metrics": {
        "okApi": {"status": "pass"},
        "badApi": {"status": "fail"},
        "missingApi": {"status": "fail"},
        "infraApi": {"status": "fail", "error_category": "infra"}
      }
    }""")
    targets, missing = _failed_apis_from_results(p, {"okApi", "badApi", "infraApi"})
    assert targets == ["badApi", "infraApi"]
    assert missing == ["missingApi"]


def test_write_report_creates_incremental_json(tmp_path):
    from aideal.docfix import _write_report
    p = tmp_path / "nested" / "docfix.json"
    _write_report(p, {"check": "fix-docs", "processed": 1})
    assert '"processed": 1' in p.read_text()


def test_codebase_frames_maps_only_repo_files():
    from aideal.doc_checks import _codebase_frames
    trace = """java.lang.IllegalArgumentException: boom
        at edu.ucr.cs.bdlab.raptor.ZonalStatistics$.zonalStatsLocal(ZonalStatistics.scala:164)
        at edu.ucr.cs.bdlab.raptor.RaptorJoin$.raptorJoinLocal(RaptorJoin.scala:88)
        at org.apache.spark.rdd.RDD.count(RDD.scala:1200)
        at GeoJob$.run(ApiTest.scala:368)
        at edu.ucr.cs.bdlab.raptor.ZonalStatistics$.zonalStatsLocal(ZonalStatistics.scala:164)"""
    idx = {"ZonalStatistics.scala": "beast/raptor/src/main/scala/.../ZonalStatistics.scala",
           "RaptorJoin.scala": "beast/raptor/src/main/scala/.../RaptorJoin.scala"}
    frames = _codebase_frames(trace, idx)
    # repo files kept (deduped), Spark internals + the snippet itself excluded
    assert frames == ["beast/raptor/src/main/scala/.../ZonalStatistics.scala:164",
                      "beast/raptor/src/main/scala/.../RaptorJoin.scala:88"], frames


def test_deprioritized_facade_loses_election():
    # Java facade has the LONGER signature and doc, but a deprioritize pattern
    # hands the canonical slot to the Scala mixin context.
    import re
    scala = _rec("raptor/RaptorMixin.scala", 10, ["String"], doc="scala doc")
    java = _rec("beast-spark/JavaSpatialSparkContext.scala", 5,
                ["String", "Int", "BeastOptions"], doc="java doc")
    pats = (re.compile(r"(^|/)Java[A-Z][^/]*\.scala$"),)
    maximals, _ = _subsume_overloads([scala, java], pats)
    assert maximals[0] is scala
    # without the pattern the longer facade wins
    maximals, _ = _subsume_overloads([scala, java])
    assert maximals[0] is java

DOCS = """# MyLib
To run the pipeline, close the file and write results. Read this first.
Use `raptorJoin` for raster-vector joins:
```scala
val r = sc.geoTiff[Float](path)
r.reshapeNN(meta)
```
Call zonalStats(features) in prose form.
"""


def test_english_words_in_prose_do_not_count():
    # 'run', 'close', 'write', 'this' appear only as English words -> no credit.
    # (Before the fix these matched \b<name>\b and earned mentioned_in_docs(+4);
    # on RDPro that selected `this` (score 7) and pushed run/close/write/read
    # over the threshold.)
    assert _doc_code_mentions(DOCS, {"run", "close", "write", "this"}) == set()


def test_backticks_fences_and_call_forms_count():
    out = _doc_code_mentions(
        DOCS, {"raptorJoin", "geoTiff", "reshapeNN", "zonalStats", "spatialFile"})
    assert out == {"raptorJoin", "geoTiff", "reshapeNN", "zonalStats"}, out


def test_empty_inputs():
    assert _doc_code_mentions("", {"x"}) == set()
    assert _doc_code_mentions("some text", set()) == set()


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for f in fns:
        f()
        print("ok ", f.__name__)
    print(f"\n{len(fns)} passed")
