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


def _allowed_members_from_config(cfg: AidealConfig | None = None) -> set[str]:
    raw_docfix = ((cfg.raw or {}).get("docfix") if cfg else None) or {}
    categories = raw_docfix.get("allowed_member_categories", ["language_core"])
    out: set[str] = set()
    for cat in categories:
        out.update(_ALLOWED_MEMBER_CATEGORIES.get(cat, set()))
    out.update(raw_docfix.get("allowed_members", []))
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
              "SparkContext", "SparkSession", "DataFrame"}


def _type_context(cfg: AidealConfig, name: str, max_types: int = 4,
                  lines_per_type: int = 35) -> str:
    """DEEP-DIVE context: the definitions of the RECEIVER/PARAMETER/RETURN
    types in `name`'s canonical signature, located across the WHOLE codebase —
    Scala AND Java sources. This is what the wrong-receiver / unknown-member /
    Java-defined-type failure classes need and a single def window cannot
    show. Generic: works from cfg.source_globs, no project names hardcoded."""
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
    pats = {t: re.compile(rf"\b(?:case\s+class|abstract\s+class|class|trait|object|interface|enum)\s+{t}\b")
            for t in types}
    found: dict[str, str] = {}
    globs = list(cfg.source_globs) + [g.replace(".scala", ".java") for g in cfg.source_globs]
    for g in globs:
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
                    kind = "JAVA" if p.endswith(".java") else "Scala"
                    found[t] = f"// type {t} ({kind}-defined) — {rel}:{ln + 1}\n{seg}"
    return "\n\n".join(found.get(t, f"// type {t}: definition NOT found in sources")
                       for t in types)


def doc_fix_run(cfg: AidealConfig, apis: list[str] | None = None,
                max_apis: int | None = None, retry_rounds: int = 2,
                timeout_s: int | None = None, dry_run: bool = False,
                from_results: str | Path | None = None,
                report_path: str | Path | None = None,
                deep_dive_first: bool = False,
                deep_dive_out: str = "docs/deepdive") -> dict:
    """Run the doc-repair routing over failed APIs. Returns a report dict."""
    from .llm import invoke_text, usage_snapshot, usage_delta
    from .prompts import load as load_prompt
    from .profile import require_profile
    from .readme_agent import parse_readme, _exec_status_map
    from .doc_checks import comprehension_check, _owner_map, _receiver_hint

    require_profile(cfg)
    entries = {e.name: e for e in parse_readme(cfg.llm_readme)}
    if apis:
        targets = [a for a in apis if a in entries]
        missing = [a for a in apis if a not in entries]
    elif from_results:
        targets, missing = _failed_apis_from_results(from_results, set(entries))
    else:
        failed = {fn for fn, s in _exec_status_map(cfg).items() if s == "fail"}
        targets = sorted(n for n in failed if n in entries)
        missing = []
    if max_apis:
        targets = targets[:max_apis]
    base_report = {"check": "fix-docs",
                   "target_source": str(from_results) if from_results else
                   ("explicit --api" if apis else "latest error_log failures"),
                   "deep_dive_first": deep_dive_first,
                   "attempted": len(targets),
                   "not_in_catalog": missing,
                   "apis": {}}
    if dry_run:
        out = {**base_report, "dry_run": True, "targets": targets}
        _write_report(report_path, out)
        return out

    log = ErrorLog(cfg.error_log)
    owner_map = _owner_map(cfg)
    from .readme_agent import public_api_surface
    raw_surface = public_api_surface(cfg, override_filter="all")
    allowed_members = _allowed_members_from_config(cfg)
    spec = cfg.model_for_role("fixer")   # senior engineer + doc rewriter
    prior = _read_report(report_path)
    if (prior and prior.get("target_source") == base_report["target_source"]
            and bool(prior.get("deep_dive_first")) == deep_dive_first):
        results: dict[str, dict] = dict(prior.get("apis") or {})
    else:
        results = {}
    fixed = sum(1 for v in results.values() if v.get("status") == "doc-fixed")
    import sys as _sys
    run_report = {**base_report, "model": f"{spec.provider}:{spec.model}",
                  "doc_fixed": fixed,
                  "fix_rate": round(fixed / len(targets), 3) if targets else None,
                  "outcomes": _outcomes(results),
                  "processed": len(results),
                  "resumed": bool(results)}
    _write_report(report_path, run_report)
    for i, name in enumerate(targets, 1):
        if name in results and not results[name].get("status", "").startswith("llm-error"):
            continue
        _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: diagnose -> rewrite -> retry\n")
        _sys.stderr.flush()
        t0 = time.time()
        u0 = usage_snapshot()
        # last failure evidence for THIS api
        rows = [r for r in log.entries()
                if r.get("function") == name and r.get("status") == "fail"]
        last = rows[-1] if rows else {}
        window, others = _source_window(cfg, name)
        deep_dive_report = "(not requested)"
        deep_dive_meta = None
        if deep_dive_first:
            try:
                from .deepdive import deep_dive_run
                dd = deep_dive_run(cfg, name, out_dir=deep_dive_out,
                                   context_only=False, return_text=True)
                deep_dive_report = (dd.get("report_text") or "")[:10000]
                deep_dive_meta = {k: v for k, v in dd.items() if k != "report_text"}
            except Exception as exc:
                results[name] = {"status": "llm-error (run stopped)",
                                 "phase": "deep-dive",
                                 "error_type": type(exc).__name__,
                                 "error": str(exc)[:1000],
                                 "wall_s": round(time.time() - t0, 1)}
                run_report.update({"doc_fixed": fixed,
                                   "fix_rate": round(fixed / len(targets), 3) if targets else None,
                                   "outcomes": _outcomes(results),
                                   "processed": len(results),
                                   "blocked": True,
                                   "blocked_api": name,
                                   "apis": results})
                _write_report(report_path, run_report)
                _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: DEEP-DIVE ERROR — "
                                  f"{type(exc).__name__}: {str(exc)[:160]}\n")
                return run_report
        # 2+3: locate + senior-engineer diagnosis against the real source
        try:
            diagnosis = invoke_text(spec, *load_prompt(
                cfg, "aideal/docfix_diagnose",
                api_name=name, source_window=window, other_sites=others,
                type_context=_type_context(cfg, name)[:7000],
                deep_dive_report=deep_dive_report,
                receiver=_receiver_hint(name, owner_map) or "(not resolved)",
                entry_body=entries[name].body[:6000],
                snippet=(last.get("code") or "(snippet not recorded)")[:2000],
                error=(last.get("error") or "(no recorded error)")[:1500],
                error_category=last.get("error_category", "unknown"),
                frames=", ".join(last.get("frames", []) or []) or "(none)",
                language_lower=cfg.language.lower()))
        except Exception as exc:
            results[name] = {"status": "llm-error (run stopped)",
                             "error_type": type(exc).__name__,
                             "error": str(exc)[:1000],
                             "wall_s": round(time.time() - t0, 1)}
            run_report.update({"doc_fixed": fixed,
                               "fix_rate": round(fixed / len(targets), 3) if targets else None,
                               "outcomes": _outcomes(results),
                               "processed": len(results),
                               "blocked": True,
                               "blocked_api": name,
                               "apis": results})
            _write_report(report_path, run_report)
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: LLM ERROR — "
                              f"{type(exc).__name__}: {str(exc)[:160]}\n")
            return run_report
        if diagnosis.strip().upper().startswith("VERDICT: NOT-TESTABLE"):
            results[name] = {"status": "not-testable (entry unchanged)",
                             "verdict": diagnosis.strip().splitlines()[0][:200],
                             "wall_s": round(time.time() - t0, 1),
                             "deep_dive": deep_dive_meta}
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: NOT-TESTABLE — skipped\n")
            run_report["apis"] = results
            run_report["processed"] = len(results)
            _write_report(report_path, run_report)
            continue
        # 4: rewrite the entry, folding the diagnosis in
        try:
            new_entry = invoke_text(spec, *load_prompt(
                cfg, "aideal/docfix_rewrite",
                api_name=name, diagnosis=diagnosis[:8000],
                deep_dive_report=deep_dive_report,
                source_window=window[:8000], entry_body=entries[name].body[:6000],
                required_sections=", ".join(cfg.required_sections)))
        except Exception as exc:
            results[name] = {"status": "llm-error (run stopped)",
                             "error_type": type(exc).__name__,
                             "error": str(exc)[:1000],
                             "diagnosis_head": diagnosis.strip()[:300],
                             "wall_s": round(time.time() - t0, 1)}
            run_report.update({"doc_fixed": fixed,
                               "fix_rate": round(fixed / len(targets), 3) if targets else None,
                               "outcomes": _outcomes(results),
                               "processed": len(results),
                               "blocked": True,
                               "blocked_api": name,
                               "apis": results})
            _write_report(report_path, run_report)
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: LLM ERROR — "
                              f"{type(exc).__name__}: {str(exc)[:160]}\n")
            return run_report
        new_entry = new_entry.strip()
        if not new_entry.startswith("## API Test:"):
            new_entry = f"## API Test: `{name}`\n\n" + new_entry
        # guard: reject rewrites that call members not on the RAW surface —
        # the observed failure mode where the diagnosis invents a plausible
        # cousin (`.convolve`, `.build`) and the retry dies on "not a member".
        fab = _fabricated_members(new_entry, raw_surface, name, allowed_members)
        if fab:
            results[name] = {"status": f"rewrite-rejected (fabricated members: {', '.join(fab[:4])})",
                             "diagnosis_head": diagnosis.strip()[:300],
                             "wall_s": round(time.time() - t0, 1),
                             "deep_dive": deep_dive_meta}
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: REJECTED — "
                              f"rewrite references nonexistent {fab[:3]}\n")
            log.append(step="doc-fix", language=cfg.language, task="docfix",
                       status="fail", function=name, error_category="doc-repair",
                       error=f"rewrite fabricated members: {', '.join(fab[:6])}")
            run_report["apis"] = results
            run_report["processed"] = len(results)
            _write_report(report_path, run_report)
            continue
        old_text = cfg.llm_readme.read_text(encoding="utf-8")
        try:
            cfg.llm_readme.write_text(
                _replace_entry_text(old_text, name, new_entry), encoding="utf-8")
        except KeyError:
            results[name] = {"status": "error", "note": "entry not found in readme"}
            continue
        # 5: re-run the comprehension test with the repaired entry
        retry = comprehension_check(cfg, api=name, execute=True,
                                    max_fix_rounds=retry_rounds,
                                    timeout_s=timeout_s)
        m = (retry.get("metrics") or {}).get(name, {})
        passed = m.get("status") == "pass"
        if passed:
            fixed += 1
            # audit trail: keep the exact before/after + diagnosis for every
            # ACCEPTED repair, so catalog evolution is diffable per entry.
            chg = cfg.llm_readme.parent / "docfix_changes"
            chg.mkdir(parents=True, exist_ok=True)
            (chg / f"{name}.before.md").write_text(entries[name].body, encoding="utf-8")
            (chg / f"{name}.after.md").write_text(new_entry, encoding="utf-8")
            (chg / f"{name}.diagnosis.txt").write_text(diagnosis, encoding="utf-8")
        else:
            # revert: never leave the catalog worse than we found it
            cfg.llm_readme.write_text(old_text, encoding="utf-8")
        _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: "
                          f"{'DOC-FIXED' if passed else 'still failing — entry reverted'}\n")
        _sys.stderr.flush()
        u = usage_delta(u0)
        results[name] = {
            "status": "doc-fixed" if passed else "still-failing (entry reverted)",
            "retry": m or retry.get("details", {}).get(name),
            "diagnosis_head": diagnosis.strip()[:300],
            "entry_chars": {"old": len(entries[name].body), "new": len(new_entry)},
            "wall_s": round(time.time() - t0, 1),
            "tokens": {"in": u["input_tokens"], "out": u["output_tokens"]},
            "deep_dive": deep_dive_meta,
        }
        log.append(step="doc-fix", language=cfg.language, task="docfix",
                   status="pass" if passed else "fail", function=name,
                   error_category="doc-repair",
                   error=("" if passed else "retry failed; entry reverted"),
                   suggested_fix_code=new_entry[:1200] if passed else "")
        run_report.update({
            "doc_fixed": fixed,
            "fix_rate": round(fixed / len(targets), 3) if targets else None,
            "outcomes": _outcomes(results),
            "processed": len(results),
            "apis": results,
        })
        _write_report(report_path, run_report)
    final = {"check": "fix-docs",
             "target_source": str(from_results) if from_results else
             ("explicit --api" if apis else "latest error_log failures"),
             "model": f"{spec.provider}:{spec.model}",
             "deep_dive_first": deep_dive_first,
             "attempted": len(targets), "doc_fixed": fixed,
             "fix_rate": round(fixed / len(targets), 3) if targets else None,
             "outcomes": _outcomes(results),
             "not_in_catalog": missing,
             "apis": results}
    _write_report(report_path, final)
    return final
