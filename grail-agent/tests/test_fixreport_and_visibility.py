"""Unit tests: visibility fixes (container modifiers, prefix under anchored
regex), Python adapter primitives (docstring-below, pytest blocks, scaffold
indentation, error classification), and the fix-report analyses."""

import json
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aideal.config import AidealConfig, ModelSpec  # noqa: E402
from aideal.readme_agent import (_container_context, _doc_below_py,  # noqa: E402
                                 _is_public, _iter_test_blocks_py)
from aideal.doc_checks import _classify_error, _fill_scaffold  # noqa: E402
from aideal.fixreport import (compare_runs, cluster_failures,  # noqa: E402
                              error_signature, load_run)


# --- visibility ---------------------------------------------------------------

SCALA = textwrap.dedent("""\
    package p
    class Pub {
      def visible(x: Int): Int = x
      protected[raptor] def compress: Unit = {}
      override protected def hidden2(): Unit = {}
      private[davinci] def hidden3: Int = 1
    }
    private[raptor] object Helper {
      def insidePrivateObject(): Int = 1
    }
    object Open {
      def alsoVisible(): Int = 2
    }
""")

SCALA_MODEL = {"mode": "deny", "private": [r"\bprivate\b", r"\bprotected\b"]}


def _surface_of(text: str) -> dict:
    """name -> is_public using the same prefix rules _iter_defs applies."""
    import re
    lines = text.splitlines()
    ctx = _container_context(lines)
    pat = re.compile(r"def\s+([a-zA-Z][A-Za-z0-9_]*)")
    out = {}
    for i, line in enumerate(lines):
        for m in pat.finditer(line):
            prefix = line[:m.start(1)]
            if ctx[i]:
                prefix = ctx[i] + " " + prefix
            out[m.group(1)] = _is_public(m.group(1), prefix, SCALA_MODEL)
    return out


def test_container_and_modifier_visibility():
    s = _surface_of(SCALA)
    assert s["visible"] is True
    assert s["alsoVisible"] is True
    assert s["compress"] is False            # protected[raptor] on the def line
    assert s["hidden2"] is False             # override BEFORE protected (old regex leak)
    assert s["hidden3"] is False             # private[davinci]
    assert s["insidePrivateObject"] is False  # public def inside private[raptor] object


def test_anchored_regex_lookahead_is_not_trusted():
    # the historical bug: ^\s*(?!private|protected) backtracks and passes on
    # any INDENTED private def — prefix-based checking must catch it anyway
    s = _surface_of("  protected def leak(): Int = 1\n")
    assert s["leak"] is False


# --- python adapter primitives -------------------------------------------------

def test_doc_below_py_single_and_multiline():
    src = textwrap.dedent('''\
        def dtw(s1, s2):
            """Compute DTW between two series."""
            return 0

        def cdist(
            dataset1,
            dataset2=None,
        ):
            """Cross-similarity matrix.

            More detail here.
            """
            return 0
    ''').splitlines()
    assert _doc_below_py(src, 0) == "Compute DTW between two series."
    assert _doc_below_py(src, 4).startswith("Cross-similarity matrix.")
    assert "More detail" in _doc_below_py(src, 4)


def test_iter_test_blocks_py():
    src = textwrap.dedent("""\
        import numpy as np

        def test_dtw():
            path, dist = dtw_path(s1, s2)
            assert dist >= 0

        def helper():
            pass

        def test_kmeans():
            km = TimeSeriesKMeans(n_clusters=2).fit(X)
    """)
    blocks = dict(_iter_test_blocks_py(src))
    assert set(blocks) == {"test_dtw", "test_kmeans"}
    assert "dtw_path" in blocks["test_dtw"]
    assert "helper" not in blocks["test_kmeans"]


def test_fill_scaffold_indents_python_region():
    scaffold = "def run():\n    # TODO API_TEST_START\n    # TODO API_TEST_END\n"
    out = _fill_scaffold(scaffold, "x = 1\nprint(x)",
                         ["# TODO API_TEST_START", "# TODO API_TEST_END"], {})
    assert "\n    x = 1\n    print(x)\n    # TODO API_TEST_END" in out


def test_classify_error_python():
    cat, msg, _ = _classify_error("ModuleNotFoundError: No module named 'torch'",
                                  1, "__RUN_ERR__", language="Python")
    assert cat == "infra"
    cat, msg, loc = _classify_error(
        'Traceback ...\n  File "api_test.py", line 12\nSyntaxError: invalid syntax',
        1, "__RUN_ERR__", language="Python")
    assert cat == "compile" and "SyntaxError" in msg
    cat, msg, loc = _classify_error(
        '  File "/w/api_test.py", line 9, in run\n'
        "__RUN_ERR__ ValueError: bad shape", 1, "__RUN_ERR__", language="Python")
    assert cat == "runtime" and "ValueError" in msg and loc.endswith(":9")


# --- fix-report ----------------------------------------------------------------

def test_error_signature_masks_and_matches():
    a = error_signature("compile", "/u/x/ApiTest.scala:358: error: value area is not a member of IFeature")
    b = error_signature("compile", "/u/y/ApiTest.scala:412: error: value area is not a member of IFeature")
    assert a == b
    am = error_signature("compile", "error: value fooA is not a member of T", mask_names=True)
    bm = error_signature("compile", "error: value fooB is not a member of T", mask_names=True)
    assert am == bm


def _mk_run(tmp_path, name, rows):
    obj = {"check": "comprehension", "run": {"run_id": name},
           "metrics": {}, "details": {}}
    for api, (status, cat, err) in rows.items():
        obj["metrics"][api] = {"status": status, "attempts": 1,
                               "pass_round": 0 if status == "pass" else None,
                               "error_category": cat or None}
        obj["details"][api] = ("pass" if status == "pass"
                               else f"fail [{cat}]: {err}")
    p = tmp_path / f"{name}.json"
    p.write_text(json.dumps(obj))
    return p


def test_compare_runs_same_issue_vs_changed(tmp_path):
    base = _mk_run(tmp_path, "base", {
        "a": ("pass", None, ""),
        "b": ("fail", "compile", "error: not found: value spark"),
        "c": ("fail", "compile", "error: not found: value spark"),
        "d": ("fail", "runtime", "ValueError: x"),
    })
    run = _mk_run(tmp_path, "run", {
        "a": ("fail", "runtime", "boom"),                          # regressed
        "b": ("pass", None, ""),                                   # fixed
        "c": ("fail", "compile", "error: not found: value spark"),  # same issue
        "d": ("fail", "compile", "error: type mismatch"),           # changed issue
    })
    c = compare_runs(load_run(run), load_run(base))
    assert c["fixed"] == ["b"]
    assert c["regressed"] == ["a"]
    assert c["still_same_issue"] == ["c"]
    assert [x[0] for x in c["still_changed_issue"]] == ["d"]


def test_cluster_failures_groups_masked_names(tmp_path):
    run = _mk_run(tmp_path, "r", {
        "a": ("fail", "compile", "error: value fooA is not a member of T"),
        "b": ("fail", "compile", "error: value fooB is not a member of T"),
        "c": ("fail", "runtime", "ValueError: nope"),
    })
    cl = cluster_failures(load_run(run))
    assert cl[0]["count"] == 2 and set(cl[0]["apis"]) == {"a", "b"}
