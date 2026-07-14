"""Doc-repair fix routing — fix the DOCUMENTATION, not just the snippet.

The classic fix loop rewrites the failing snippet with the error pasted back
(same doc, new guess); measured rescue rates are low and stuck loops common.
This routing treats the failure as evidence about the DOC and repairs it:

  1. take a FAILED function (most-recent fail in the error log),
  2. locate its canonical definition in the codebase and read the REAL source,
  3. senior-engineer LLM pass diagnoses the root cause against that source,
  4. rewrite that API's LLM_readme entry, folding the diagnosis in,
  5. re-run the comprehension test for that API with the repaired entry.

Entry policy: KEEP the repaired entry if the retry passes; REVERT it if the
retry still fails (the catalog only ever gets monotonically better). Every
step's tokens and outcome are recorded. CLI: `aideal fix-docs`.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from .config import AidealConfig
from .error_log import ErrorLog


def _replace_entry_text(text: str, name: str, new_entry: str) -> str:
    """Replace the `## API Test: `name`` section (up to the next entry or EOF).
    Pure function so it is unit-testable. Raises KeyError if absent."""
    pat = re.compile(rf"(?ms)^## API Test: `{re.escape(name)}`.*?(?=^## API Test: `|\Z)")
    if not pat.search(text):
        raise KeyError(name)
    repl = new_entry.rstrip() + "\n\n"
    return pat.sub(lambda _m: repl, text, count=1)


def _insert_entry_text(text: str, new_entry: str) -> str:
    """Append a brand-new `## API Test:` entry at the end of the catalog.
    Used by create-missing mode (original-readme arm: the doc-repair loop
    WRITES the entry that never existed)."""
    return (text.rstrip() + "\n\n" if text.strip() else "") + new_entry.rstrip() + "\n\n"


def _remove_entry_text(text: str, name: str) -> str:
    """Delete an entry created by this run (all-rounds-fail in create-missing
    mode reverts to ABSENT, keeping the catalog exactly as found)."""
    pat = re.compile(rf"(?ms)^## API Test: `{re.escape(name)}`.*?(?=^## API Test: `|\Z)")
    return pat.sub("", text, count=1)


def _source_window(cfg: AidealConfig, name: str, before: int = 15, after: int = 80) -> tuple[str, str]:
    """(window_text, other_sites_note) for the CANONICAL definition of `name`
    — the same election dedup/readme use (subsumption + deprioritized paths)."""
    from .readme_agent import public_api_details, _subsume_overloads, _dedup_deprioritize
    recs = [d for d in public_api_details(cfg)
            if d["visibility"] == "public" and d["name"] == name]
    if not recs:
        return "(definition not found on the public surface)", "(none)"
    maximals, _ = _subsume_overloads(recs, _dedup_deprioritize(cfg))
    canon = maximals[0]
    path = cfg.root / canon["file"]
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    lo = max(0, canon["line"] - 1 - before)
    hi = min(len(lines), canon["line"] - 1 + after)
    numbered = "\n".join(f"{i+1:5d} | {lines[i]}" for i in range(lo, hi))
    window = f"// {canon['file']}:{canon['line']}\n{numbered}"
    others = [f"{d['file']}:{d['line']}" for d in recs if d is not canon]
    return window, (", ".join(others[:6]) or "(none)")


# LEGACY FALLBACK ONLY (2026-07-13): category CONTENTS now live in the YAML
# layers (defaults.yaml / adapters / project file, under
# docfix.member_categories) and the DEFAULT evidence source is the repo's own
# call vocabulary (_repo_called_members). This dict answers only for configs
# that name a category without defining it anywhere in YAML.
_ALLOWED_MEMBER_CATEGORIES = {
    # Language/library calls that are normal in snippets and should not be
    # confused with the target project API surface.
    "language_core": {
        "println", "print", "require", "assert", "format", "mkString", "toString",
        "map", "flatMap", "filter", "foreach", "collect", "count", "take", "first",
        "reduce", "fold", "foldLeft", "sum", "min", "max", "size", "length",
        "nonEmpty", "isEmpty", "head", "headOption", "last", "getOrElse", "get",
        "exists", "forall", "contains", "indexOf", "sortBy", "sorted", "zip",
        "zipWithIndex", "toArray", "toList", "toSeq", "toSet", "toMap", "distinct",
        "sliding", "grouped", "apply", "update", "close", "cache", "persist",
        "coalesce", "repartition", "keys", "values", "trim", "split", "replace",
        "startsWith", "endsWith", "toDouble", "toInt", "toLong", "toFloat", "abs",
        "floor", "ceil", "round", "find", "getPath", "getName", "getClass",
        "asInstanceOf", "isInstanceOf", "mkdirs", "listFiles", "delete",
        "getConstructor", "newInstance", "getFileSystem", "resolve",
        "isNaN", "isInfinite", "isFinite", "toRadians", "toDegrees", "sqrt",
        "pow", "sin", "cos", "tan", "atan2", "fill", "range", "empty", "ofDim",
    },
    "spark": {
        "builder", "appName", "master", "config", "getOrCreate", "sparkContext",
        "createDataFrame", "load", "save", "mode", "option", "options", "select",
        "where", "withColumn", "as", "show", "registerTempTable", "toDF", "toDS",
        "rdd", "schema", "printSchema", "parallelize", "textFile", "wholeTextFiles",
        "broadcast", "longAccumulator", "doubleAccumulator", "setLogLevel",
        "getNumPartitions", "partitions", "partitioner", "saveAsTextFile",
    },
    "geometry_common": {
        "createPoint", "createLineString", "createPolygon", "createMultiPolygon",
        "createGeometryCollection", "createLinearRing", "setSRID", "getSRID",
        "getCoordinate", "getCoordinates", "getEnvelopeInternal", "getArea",
        "getLength", "intersects", "contains", "covers", "within", "touches",
        "buffer", "union", "intersection", "difference", "getX", "getY",
        "decode", "encode",
    },
    "raster_common": {
        "getPixelValueAsFloat", "getPixelValueAsDouble",
        "getPixelValueAsInt", "getPixelValueAsLong",
    },
    # Python/numpy/sklearn ecosystem members that are normal in snippets and
    # must not be mistaken for fabricated project APIs (python adapter).
    "python_core": {
        "fit", "predict", "transform", "fit_transform", "fit_predict",
        "score", "ravel", "reshape", "astype", "tolist", "copy", "mean",
        "sum", "std", "var", "argmin", "argmax", "cumsum", "squeeze",
        "flatten", "array", "asarray", "zeros", "ones", "arange", "linspace",
        "allclose", "isclose", "seed", "rand", "randn", "randint",
        "normal", "shuffle", "append", "extend", "join", "format", "items",
        "keys", "values", "get", "strip", "lower", "upper", "round",
        "set_params", "get_params",
    },
}


_MEMBER_CALL_RE = re.compile(r"\.([a-zA-Z_]\w*)\s*\(")


def _repo_called_members(cfg: AidealConfig, max_files: int = 4000) -> set[str]:
    """EVIDENCE-BASED allowlist (the general mechanism, 2026-07-13): every
    member name the target codebase ITSELF calls in its sources/tests is
    legitimate vocabulary for this ecosystem — `.map`, `.fit`, `.getOrCreate`,
    `.createPoint` all appear in real repo code, so no hand-curated
    language/ecosystem/domain list is needed per codebase. A rewrite calling a
    member the repo has never called anywhere is exactly the hallucination
    class the guard exists to reject. Existence is name-level (like the guard
    itself); wrong-receiver misuse is still caught by the execution retry."""
    import glob as _glob
    out: set[str] = set()
    seen = 0
    for g in list(cfg.source_globs) + list(cfg.test_globs or []):
        for path in _glob.glob(str(cfg.root / g), recursive=True):
            if seen >= max_files:
                return out
            seen += 1
            try:
                text = Path(path).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            out.update(_MEMBER_CALL_RE.findall(text))
    return out


def _allowed_members_from_config(cfg: AidealConfig | None = None) -> set[str]:
    """Allowed-member vocabulary for the fabricated-member guard, from three
    layers (most general first):

      1. docfix.allow_repo_called_members (default TRUE): members mined from
         the target repo's own sources/tests — codebase-agnostic, no curation.
      2. docfix.member_categories (YAML, deep-merged defaults <- adapter <-
         project): named sets whose CONTENTS live in config layers, e.g.
         language_core in defaults.yaml, spark in the scala-spark adapter,
         geometry/raster sets in the rdpro project file. The Python
         _ALLOWED_MEMBER_CATEGORIES dict remains only as a fallback for
         configs that name a category without defining it.
      3. docfix.allowed_members: plain per-project extra names.
    """
    raw_docfix = ((cfg.raw or {}).get("docfix") if cfg else None) or {}
    categories = raw_docfix.get("allowed_member_categories", ["language_core"])
    yaml_cats = raw_docfix.get("member_categories", {}) or {}
    out: set[str] = set()
    for cat in categories:
        defined = yaml_cats.get(cat)
        out.update(defined if defined is not None
                   else _ALLOWED_MEMBER_CATEGORIES.get(cat, set()))
    out.update(raw_docfix.get("allowed_members", []))
    if cfg is not None and raw_docfix.get("allow_repo_called_members", True):
        out |= _repo_called_members(cfg)
    return out


def _fabricated_members(entry_md: str, surface: set[str], api_name: str,
                        allowed_members: set[str] | None = None) -> list[str]:
    """Member calls `.name(` inside the entry's code blocks that are neither on
    the library's RAW surface, nor configured ecosystem/language methods, nor
    the API itself — i.e. likely hallucinated project members (`.convolve`, …)."""
    code = "\n".join(re.findall(r"```.*?\n(.*?)```", entry_md, re.S))
    called = set(re.findall(r"\.([a-z]\w+)\s*\(", code))
    allowed = allowed_members if allowed_members is not None else _allowed_members_from_config()
    return sorted(called - surface - allowed - {api_name})


def _failed_apis_from_results(path: str | Path, entries: set[str]) -> tuple[list[str], list[str]]:
    """Return failed API names from a comprehension/bench result JSON.

    This freezes docfix to a specific baseline run (e.g. g1) instead of whatever
    the mutable error log currently says after later g4/docfix experiments.
    """
    p = Path(path)
    obj = json.loads(p.read_text(encoding="utf-8"))
    metrics = obj.get("metrics") or {}
    failed = sorted(n for n, m in metrics.items()
                    if isinstance(m, dict) and m.get("status") == "fail")
    return [n for n in failed if n in entries], [n for n in failed if n not in entries]


def _write_report(path: str | Path | None, report: dict) -> None:
    if not path:
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                 encoding="utf-8")


def _read_report(path: str | Path | None) -> dict | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _outcomes(results: dict[str, dict]) -> dict[str, int]:
    from collections import Counter
    return dict(Counter(v.get("status", "unknown").split(" ")[0]
                        for v in results.values()))


_TYPE_SKIP = {"String", "Int", "Long", "Float", "Double", "Boolean", "Unit",
              "Array", "Option", "Some", "None", "Seq", "List", "Map", "Set",
              "Class", "Any", "AnyRef", "AnyVal", "T", "K", "V", "ClassTag",
              "Iterator", "Iterable", "Tuple2", "Tuple3", "RDD", "JavaRDD",
              "SparkContext", "SparkSession", "DataFrame", "NoneType", "True", "False"}


def _type_context(cfg: AidealConfig, name: str, max_types: int = 4,
                  lines_per_type: int = 35) -> str:
    """Definitions of receiver/parameter/return types found in configured source.

    This intentionally follows ``source_globs`` rather than assuming a language
    pair.  The declaration pattern covers common class/type constructs; projects
    with unusual syntax still get an explicit "not found" instead of a fabricated
    definition.
    """
    import glob as _glob
    from .readme_agent import public_api_details, _subsume_overloads, _dedup_deprioritize
    recs = [d for d in public_api_details(cfg)
            if d["visibility"] == "public" and d["name"] == name]
    if not recs:
        return "(no public definition found)"
    canon = _subsume_overloads(recs, _dedup_deprioritize(cfg))[0][0]
    sig = " ".join([canon.get("signature") or "", canon.get("returns") or ""] +
                   [p.get("type") or "" for p in canon.get("params", [])])
    types = [t for t in dict.fromkeys(re.findall(r"\b([A-Z][A-Za-z0-9]{2,})\b", sig))
             if t not in _TYPE_SKIP][:max_types]
    if not types:
        return "(signature uses only primitive/collection types)"
    pats = {t: re.compile(rf"\b(?:case\s+class|abstract\s+class|class|trait|object|"
                              rf"interface|enum|struct|record|type)\s+{t}\b")
            for t in types}
    found: dict[str, str] = {}
    extra_globs = (((cfg.raw or {}).get("codebase") or {})
                   .get("type_context_globs") or [])
    for g in dict.fromkeys([*cfg.source_globs, *extra_globs]):
        if len(found) == len(types):
            break
        for p in _glob.glob(str(cfg.root / g), recursive=True):
            if len(found) == len(types):
                break
            try:
                text = Path(p).read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for t, pat in pats.items():
                if t in found:
                    continue
                m = pat.search(text)
                if m:
                    lines = text.splitlines()
                    ln = text[:m.start()].count("\n")
                    seg = "\n".join(lines[ln:ln + lines_per_type])
                    rel = str(Path(p).relative_to(cfg.root))
                    suffix = Path(p).suffix.lstrip(".") or cfg.language
                    found[t] = f"// type {t} ({suffix} source) — {rel}:{ln + 1}\n{seg}"
    return "\n\n".join(found.get(t, f"// type {t}: definition NOT found in sources")
                       for t in types)


def _err_sig(category: str, message: str) -> str:
    """Normalized error signature (shared with fixreport) for progress checks."""
    from .fixreport import error_signature
    return error_signature(category or "", message or "")


def _diag_sig(diagnosis: str) -> str:
    """Signature of a diagnosis: the ROOT CAUSE section, whitespace-normalized.
    Used for the per-round 'did understanding improve?' check — an unchanged
    root cause means the deep dive learned nothing new this round."""
    m = re.search(r"ROOT CAUSE:(.*?)(?:\n[A-Z][A-Z ]+:|\Z)", diagnosis, re.S)
    core = (m.group(1) if m else diagnosis)
    return " ".join(core.split()).lower()[:400]


def doc_fix_run(cfg: AidealConfig, apis: list[str] | None = None,
                max_apis: int | None = None, retry_rounds: int = 2,
                timeout_s: int | None = None, dry_run: bool = False,
                from_results: str | Path | None = None,
                report_path: str | Path | None = None,
                deep_dive_first: bool = False,
                deep_dive_out: str = "docs/deepdive",
                doc_rounds: int = 1,
                doc_stuck: int = 2,
                create_missing: bool = False,
                doc_source: str = "aideal",
                full_doc: bool | None = None,
                doc_scope: str | None = None,
                manifest: str | None = None) -> dict:
    """Doc-repair routing over failed APIs. Returns a report dict.

    doc_rounds=1 → the classic single pass (diagnose → rewrite → retry).
    doc_rounds>1 → ITERATIVE deep-dive repair (2026-07-13 design): per API,
    up to N rounds of

        deep-dive (fresh, sees the newest failure + current draft)
        → diagnose → rewrite entry → run the API against the NEW doc
          (retry_rounds snippet fixes; 0 = clean pass-or-not doc measurement)

    with a per-round UNDERSTANDING CHECK: `diagnosis_changed` (root-cause text
    moved vs previous round) and `error_progressed` (the failure signature
    changed after the rewrite). If NEITHER improves for `doc_stuck`
    consecutive rounds, the API stops early — rounds must earn themselves.
    The draft entry is kept across rounds so each round builds on the last;
    the catalog is only left changed if the API finally PASSES (all-rounds
    fail → revert to the original entry: monotonically non-worse).
    After every round the incremental JSON report AND the readable
    fix-report markdown are refreshed, so the log is checkable mid-run."""
    from .llm import invoke_text, usage_snapshot, usage_delta
    from .prompts import load as load_prompt
    from .profile import require_profile
    from .readme_agent import parse_readme, _exec_status_map
    from .doc_checks import comprehension_check, _owner_map, _receiver_hint

    require_profile(cfg)
    entries = {e.name: e for e in parse_readme(cfg.llm_readme)} \
        if cfg.llm_readme.exists() else {}
    if apis:
        targets = [a for a in apis if a in entries]
        missing = [a for a in apis if a not in entries]
    elif from_results:
        targets, missing = _failed_apis_from_results(from_results, set(entries))
    else:
        failed = {fn for fn, s in _exec_status_map(cfg).items() if s == "fail"}
        targets = sorted(n for n in failed if n in entries)
        missing = []
    if create_missing and missing:
        # ORIGINAL-README ARM: no catalog entry exists — the loop CREATES one.
        # Round-0 "current doc" = the original README excerpt the audience saw.
        targets = sorted(set(targets) | set(missing))
        missing = []
    if max_apis:
        targets = targets[:max_apis]
    base_report = {"check": "fix-docs",
                   "target_source": str(from_results) if from_results else
                   ("explicit --api" if apis else "latest error_log failures"),
                   "deep_dive_first": deep_dive_first,
                   "doc_rounds": doc_rounds,
                   "retry_rounds": retry_rounds,
                   "create_missing": create_missing,
                   "retry_doc_source": doc_source,
                   "retry_full_doc": full_doc,
                   "retry_doc_scope": doc_scope,
                   "manifest": manifest,
                   "attempted": len(targets),
                   "not_in_catalog": missing,
                   "apis": {}}
    if dry_run:
        out = {**base_report, "dry_run": True, "targets": targets}
        _write_report(report_path, out)
        return out

    raw_docfix = (cfg.raw or {}).get("docfix", {}) or {}
    ctx_chars = int(raw_docfix.get("context_chars", 12000))

    def _clip(text: str, n: int | None = None) -> str:
        # In full-document experimental mode, repair must receive the same
        # documentation exposure as the audience. Outside that mode, projects
        # can cap context; context_chars=0 also explicitly means unlimited.
        n = (0 if full_doc else ctx_chars) if n is None else n
        t = text or ""
        return t if not n or len(t) <= n else t[:n] + f"\n[... truncated at {n} chars — full text in repo]"

    log = ErrorLog(cfg.error_log)
    owner_map = _owner_map(cfg)
    from .readme_agent import public_api_surface
    raw_surface = public_api_surface(cfg, override_filter="all")
    allowed_members = _allowed_members_from_config(cfg)
    spec = cfg.model_for_role("fixer")   # senior engineer + doc rewriter
    prior = _read_report(report_path)
    if (prior and prior.get("target_source") == base_report["target_source"]
            and bool(prior.get("deep_dive_first")) == deep_dive_first
            and prior.get("doc_rounds", 1) == doc_rounds):
        results: dict[str, dict] = dict(prior.get("apis") or {})
    else:
        results = {}
    fixed = sum(1 for v in results.values()
                if v.get("status") in ("doc-fixed", "doc-created"))
    import sys as _sys

    def _flush(blocked_api: str | None = None):
        run_report = {**base_report, "model": f"{spec.provider}:{spec.model}",
                      "doc_fixed": fixed,
                      "fix_rate": round(fixed / len(targets), 3) if targets else None,
                      "outcomes": _outcomes(results),
                      "processed": len(results),
                      "apis": results}
        if blocked_api:
            run_report["blocked"] = True
            run_report["blocked_api"] = blocked_api
        _write_report(report_path, run_report)
        try:                       # readable log refreshed EVERY flush (per round)
            from .fixreport import auto_report
            auto_report(cfg, run_report)
        except Exception:
            pass
        return run_report

    _flush()
    for i, name in enumerate(targets, 1):
        if name in results and not results[name].get("status", "").startswith(
                ("llm-error", "in-progress")):
            continue
        t0 = time.time()
        u0 = usage_snapshot()
        created = name not in entries
        if created:
            # What the audience actually read. Full-doc mode deliberately keeps
            # the entire bundle here; legacy mode may use the configured cap.
            original_body = ("(No catalog entry exists. The audience read the "
                             "ORIGINAL project documentation"
                             + (" IN FULL (full-doc mode)" if full_doc else "")
                             + "; content below.)\n"
                             + _clip(cfg.original_readme_text(limit=None))
                             + f"\n\nTarget function: `{name}`")
        else:
            original_body = entries[name].body
        window, others = _source_window(cfg, name)
        type_ctx = _type_context(cfg, name)[:7000]
        receiver = _receiver_hint(name, owner_map) or "(not resolved)"
        # newest failure evidence for round 0
        rows = [r for r in log.entries()
                if r.get("function") == name and r.get("status") == "fail"]
        last = rows[-1] if rows else {}
        cur_error = (last.get("error") or "(no recorded error)")[:1500]
        cur_cat = last.get("error_category", "unknown")
        cur_snippet = (last.get("code") or "(snippet not recorded)")[:2000]
        cur_frames = ", ".join(last.get("frames", []) or []) or "(none)"
        current_body = original_body          # draft carried across rounds
        prev_err_sig = _err_sig(cur_cat, cur_error)
        prev_diag_sig = None
        stagnant = 0
        rounds_trail: list[dict] = []
        passed = False
        outcome = None            # set on early terminal verdicts
        for rnd in range(doc_rounds):
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name} round {rnd + 1}/"
                              f"{doc_rounds}: deep-dive -> diagnose -> rewrite -> run\n")
            _sys.stderr.flush()
            rrec: dict = {"round": rnd}
            # -- 1. deep-dive: fresh each round; sees the CURRENT draft (readme
            #       already holds it) and the newest failures (error log grows
            #       with every retry), so understanding can actually deepen.
            deep_dive_report = "(not requested)"
            if deep_dive_first:
                try:
                    from .deepdive import deep_dive_run
                    dd = deep_dive_run(cfg, name, out_dir=deep_dive_out,
                                       context_only=False, return_text=True)
                    deep_dive_report = (dd.get("report_text") or "")[:10000]
                    rrec["deep_dive"] = {k: v for k, v in dd.items()
                                         if k in ("tokens", "wall_s", "report")}
                except Exception as exc:
                    results[name] = {"status": "llm-error (run stopped)",
                                     "phase": f"deep-dive round {rnd}",
                                     "error_type": type(exc).__name__,
                                     "error": str(exc)[:1000],
                                     "doc_rounds_done": rounds_trail,
                                     "wall_s": round(time.time() - t0, 1)}
                    return _flush(blocked_api=name)
            # -- 2. diagnose against real source + current failure
            try:
                diagnosis = invoke_text(spec, *load_prompt(
                    cfg, "aideal/docfix_diagnose",
                    api_name=name, source_window=window, other_sites=others,
                    type_context=type_ctx,
                    deep_dive_report=deep_dive_report,
                    receiver=receiver,
                    entry_body=_clip(current_body),
                    snippet=cur_snippet,
                    error=cur_error,
                    error_category=cur_cat,
                    frames=cur_frames,
                    language_lower=cfg.language.lower()))
            except Exception as exc:
                results[name] = {"status": "llm-error (run stopped)",
                                 "phase": f"diagnose round {rnd}",
                                 "error_type": type(exc).__name__,
                                 "error": str(exc)[:1000],
                                 "doc_rounds_done": rounds_trail,
                                 "wall_s": round(time.time() - t0, 1)}
                return _flush(blocked_api=name)
            dsig = _diag_sig(diagnosis)
            rrec["diagnosis_head"] = diagnosis.strip()[:300]
            rrec["diagnosis_changed"] = (prev_diag_sig is None
                                         or dsig != prev_diag_sig)
            prev_diag_sig = dsig
            if diagnosis.strip().upper().startswith("VERDICT: NOT-TESTABLE"):
                outcome = "not-testable (entry unchanged)"
                rrec["outcome"] = "not-testable"
                rounds_trail.append(rrec)
                _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: NOT-TESTABLE — stopped\n")
                break
            # -- 3. rewrite the entry, folding diagnosis in
            try:
                new_entry = invoke_text(spec, *load_prompt(
                    cfg, "aideal/docfix_rewrite",
                    api_name=name, diagnosis=diagnosis[:8000],
                    deep_dive_report=deep_dive_report,
                    source_window=window[:8000],
                    entry_body=_clip(current_body),
                    required_sections=", ".join(cfg.required_sections)))
            except Exception as exc:
                results[name] = {"status": "llm-error (run stopped)",
                                 "phase": f"rewrite round {rnd}",
                                 "error_type": type(exc).__name__,
                                 "error": str(exc)[:1000],
                                 "doc_rounds_done": rounds_trail,
                                 "wall_s": round(time.time() - t0, 1)}
                return _flush(blocked_api=name)
            new_entry = new_entry.strip()
            if not new_entry.startswith("## API Test:"):
                new_entry = f"## API Test: `{name}`\n\n" + new_entry
            fab = _fabricated_members(new_entry, raw_surface, name, allowed_members)
            if fab:
                rrec["outcome"] = f"rewrite-rejected (fabricated: {', '.join(fab[:4])})"
                rounds_trail.append(rrec)
                results[name] = {"status": "in-progress",
                                 "rounds_used": len(rounds_trail),
                                 "doc_rounds": rounds_trail}
                log.append(step="doc-fix", language=cfg.language, task="docfix",
                           status="fail", function=name, error_category="doc-repair",
                           error=f"round {rnd}: rewrite fabricated members: {', '.join(fab[:6])}",
                           round=rnd)
                _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name} round {rnd + 1}: "
                                  f"REJECTED (fabricated {fab[:3]})\n")
                _flush()
                # a rejected rewrite is not progress; count toward stagnation
                stagnant += 1
                if doc_stuck and stagnant >= doc_stuck:
                    outcome = "still-failing (no-improvement stop)"
                    break
                continue
            current_body = new_entry             # next round builds on this draft
            rrec["entry_chars"] = {"old": len(original_body), "new": len(new_entry)}
            # -- 4. put the draft in the catalog and RUN the api against it
            readme_text = (cfg.llm_readme.read_text(encoding="utf-8")
                           if cfg.llm_readme.exists() else "")
            try:
                cfg.llm_readme.write_text(
                    _replace_entry_text(readme_text, name, new_entry), encoding="utf-8")
            except KeyError:
                if created:                       # first accepted rewrite: INSERT
                    cfg.llm_readme.parent.mkdir(parents=True, exist_ok=True)
                    cfg.llm_readme.write_text(
                        _insert_entry_text(readme_text, new_entry), encoding="utf-8")
                else:
                    results[name] = {"status": "error", "note": "entry not found in readme",
                                     "doc_rounds_done": rounds_trail}
                    break
            retry = comprehension_check(cfg, api=name, execute=True,
                                        max_fix_rounds=retry_rounds,
                                        timeout_s=timeout_s,
                                        doc_source=doc_source,
                                        full_doc=full_doc,
                                        doc_scope=doc_scope,
                                        manifest=manifest)
            m = (retry.get("metrics") or {}).get(name, {}) or {}
            rrec["retry_status"] = m.get("status", "fail")
            rrec["error_category"] = m.get("error_category")
            det = (retry.get("details") or {}).get(name)
            err_text = ""
            if isinstance(det, dict):
                err_text = det.get("error", "") or ""
            elif isinstance(det, str):
                err_text = det
            new_sig = _err_sig(m.get("error_category") or "", err_text)
            rrec["error_head"] = err_text[:200]
            rrec["error_progressed"] = (m.get("status") == "pass"
                                        or new_sig != prev_err_sig)
            passed = m.get("status") == "pass"
            rounds_trail.append(rrec)
            # LIVE per-round persistence: the ACTIVE api's rounds are in the
            # JSON/markdown report from the moment they happen (finding #4) —
            # finalized (status/tokens) when the api completes; resume re-runs
            # any api left "in-progress" by a kill.
            results[name] = {"status": "in-progress",
                             "rounds_used": len(rounds_trail),
                             "doc_rounds": rounds_trail}
            _sys.stderr.write(
                f"[docfix {i}/{len(targets)}] {name} round {rnd + 1}: "
                f"{'PASS' if passed else 'fail'}  "
                f"(diagnosis {'changed' if rrec['diagnosis_changed'] else 'UNCHANGED'}, "
                f"error {'progressed' if rrec['error_progressed'] else 'SAME'})\n")
            _sys.stderr.flush()
            log.append(step="doc-fix", language=cfg.language, task="docfix",
                       status="pass" if passed else "fail", function=name,
                       error_category="doc-repair",
                       error="" if passed else f"round {rnd}: retry still failing",
                       round=rnd)
            # audit trail per round (before/after/diagnosis diffable per round)
            chg = cfg.llm_readme.parent / "docfix_changes"
            chg.mkdir(parents=True, exist_ok=True)
            tag = f"{name}.round{rnd}"
            (chg / f"{tag}.diagnosis.txt").write_text(diagnosis, encoding="utf-8")
            (chg / f"{tag}.after.md").write_text(new_entry, encoding="utf-8")
            _flush()
            if passed:
                break
            # understanding check: neither a new diagnosis nor a moved error
            # means this loop is not learning — stop before burning rounds.
            if rrec["diagnosis_changed"] or rrec["error_progressed"]:
                stagnant = 0
            else:
                stagnant += 1
                if doc_stuck and stagnant >= doc_stuck:
                    outcome = "still-failing (no-improvement stop)"
                    _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: "
                                      f"STOPPED — no improvement {stagnant}x\n")
                    break
            # feed this round's failure into the next round's diagnosis
            cur_error = err_text[:1500] or cur_error
            cur_cat = m.get("error_category") or cur_cat
            prev_err_sig = new_sig
            # deep dive next round sees the draft (already in the readme)
        # ---- finalize this API ----
        if passed:
            fixed += 1
            chg = cfg.llm_readme.parent / "docfix_changes"
            chg.mkdir(parents=True, exist_ok=True)
            (chg / f"{name}.before.md").write_text(
                original_body if not created else "(no entry existed — created by doc-repair)",
                encoding="utf-8")
            status = "doc-created" if created else "doc-fixed"
        else:
            # revert: the catalog is only ever monotonically non-worse.
            # created entries revert to ABSENT; existing ones to the original.
            if cfg.llm_readme.exists():
                readme_text = cfg.llm_readme.read_text(encoding="utf-8")
                try:
                    cfg.llm_readme.write_text(
                        _remove_entry_text(readme_text, name) if created else
                        _replace_entry_text(readme_text, name, original_body),
                        encoding="utf-8")
                except KeyError:
                    pass
            status = outcome or "still-failing (entry reverted)"
        u = usage_delta(u0)
        results[name] = {
            "status": status,
            "rounds_used": len(rounds_trail),
            "doc_rounds": rounds_trail,
            "diagnosis_head": rounds_trail[-1].get("diagnosis_head", "") if rounds_trail else "",
            "entry_chars": ({"old": len(original_body),
                             "new": rounds_trail[-1]["entry_chars"]["new"]}
                            if rounds_trail and "entry_chars" in rounds_trail[-1] else None),
            "wall_s": round(time.time() - t0, 1),
            "tokens": {"in": u["input_tokens"], "out": u["output_tokens"]},
        }
        _flush()
    final = _flush()
    final["not_in_catalog"] = missing
    _write_report(report_path, final)
    return final
