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


#: methods snippets legitimately call that are NOT part of the library surface
_STDLIB_OK = {
    "println", "print", "require", "assert", "format", "mkString", "toString",
    "map", "flatMap", "filter", "foreach", "collect", "count", "take", "first",
    "reduce", "fold", "foldLeft", "sum", "min", "max", "size", "length",
    "nonEmpty", "isEmpty", "head", "headOption", "last", "getOrElse", "get",
    "exists", "forall", "contains", "indexOf", "sortBy", "sorted", "zip",
    "zipWithIndex", "toArray", "toList", "toSeq", "toSet", "toMap", "distinct",
    "sliding", "grouped", "apply", "update", "close", "cache", "persist",
    "coalesce", "repartition", "keys", "values", "trim", "split", "replace",
    "startsWith", "endsWith", "toDouble", "toInt", "toLong", "toFloat", "abs",
    "floor", "ceil", "round", "find", "getPath", "getName", "getClass", "asInstanceOf",
    "isInstanceOf", "mkdirs", "exists", "listFiles", "delete", "getConstructor",
    "newInstance", "getFileSystem", "resolve",
}


def _fabricated_members(entry_md: str, surface: set[str], api_name: str) -> list[str]:
    """Member calls `.name(` inside the entry's code blocks that are neither on
    the library's RAW surface, nor stdlib/collection methods, nor the API
    itself — i.e. likely HALLUCINATED members (`.convolve`, `.build`, …)."""
    code = "\n".join(re.findall(r"```.*?\n(.*?)```", entry_md, re.S))
    called = set(re.findall(r"\.([a-z]\w+)\s*\(", code))
    return sorted(called - surface - _STDLIB_OK - {api_name})


def doc_fix_run(cfg: AidealConfig, apis: list[str] | None = None,
                max_apis: int | None = None, retry_rounds: int = 2,
                timeout_s: int | None = None, dry_run: bool = False) -> dict:
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
    else:
        failed = {fn for fn, s in _exec_status_map(cfg).items() if s == "fail"}
        targets = sorted(n for n in failed if n in entries)
        missing = []
    if max_apis:
        targets = targets[:max_apis]
    if dry_run:
        return {"check": "fix-docs", "dry_run": True, "targets": targets,
                "not_in_catalog": missing}

    log = ErrorLog(cfg.error_log)
    owner_map = _owner_map(cfg)
    from .readme_agent import public_api_surface
    raw_surface = public_api_surface(cfg, override_filter="all")
    spec = cfg.model_for_role("fixer")   # senior engineer + doc rewriter
    results: dict[str, dict] = {}
    fixed = 0
    import sys as _sys
    for i, name in enumerate(targets, 1):
        _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: diagnose -> rewrite -> retry\n")
        _sys.stderr.flush()
        t0 = time.time()
        u0 = usage_snapshot()
        # last failure evidence for THIS api
        rows = [r for r in log.entries()
                if r.get("function") == name and r.get("status") == "fail"]
        last = rows[-1] if rows else {}
        window, others = _source_window(cfg, name)
        # 2+3: locate + senior-engineer diagnosis against the real source
        diagnosis = invoke_text(spec, *load_prompt(
            cfg, "aideal/docfix_diagnose",
            api_name=name, source_window=window, other_sites=others,
            receiver=_receiver_hint(name, owner_map) or "(not resolved)",
            entry_body=entries[name].body[:6000],
            snippet=(last.get("code") or "(snippet not recorded)")[:2000],
            error=(last.get("error") or "(no recorded error)")[:1500],
            error_category=last.get("error_category", "unknown"),
            frames=", ".join(last.get("frames", []) or []) or "(none)",
            language_lower=cfg.language.lower()))
        if diagnosis.strip().upper().startswith("VERDICT: NOT-TESTABLE"):
            results[name] = {"status": "not-testable (entry unchanged)",
                             "verdict": diagnosis.strip().splitlines()[0][:200],
                             "wall_s": round(time.time() - t0, 1)}
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: NOT-TESTABLE — skipped\n")
            continue
        # 4: rewrite the entry, folding the diagnosis in
        new_entry = invoke_text(spec, *load_prompt(
            cfg, "aideal/docfix_rewrite",
            api_name=name, diagnosis=diagnosis[:8000],
            source_window=window[:8000], entry_body=entries[name].body[:6000],
            required_sections=", ".join(cfg.required_sections)))
        new_entry = new_entry.strip()
        if not new_entry.startswith("## API Test:"):
            new_entry = f"## API Test: `{name}`\n\n" + new_entry
        # guard: reject rewrites that call members not on the RAW surface —
        # the observed failure mode where the diagnosis invents a plausible
        # cousin (`.convolve`, `.build`) and the retry dies on "not a member".
        fab = _fabricated_members(new_entry, raw_surface, name)
        if fab:
            results[name] = {"status": f"rewrite-rejected (fabricated members: {', '.join(fab[:4])})",
                             "diagnosis_head": diagnosis.strip()[:300],
                             "wall_s": round(time.time() - t0, 1)}
            _sys.stderr.write(f"[docfix {i}/{len(targets)}] {name}: REJECTED — "
                              f"rewrite references nonexistent {fab[:3]}\n")
            log.append(step="doc-fix", language=cfg.language, task="docfix",
                       status="fail", function=name, error_category="doc-repair",
                       error=f"rewrite fabricated members: {', '.join(fab[:6])}")
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
        }
        log.append(step="doc-fix", language=cfg.language, task="docfix",
                   status="pass" if passed else "fail", function=name,
                   error_category="doc-repair",
                   error=("" if passed else "retry failed; entry reverted"),
                   suggested_fix_code=new_entry[:1200] if passed else "")
    from collections import Counter
    outcome = Counter(v["status"].split(" ")[0] for v in results.values())
    return {"check": "fix-docs",
            "model": f"{spec.provider}:{spec.model}",
            "attempted": len(targets), "doc_fixed": fixed,
            "fix_rate": round(fixed / len(targets), 3) if targets else None,
            "outcomes": dict(outcome),
            "not_in_catalog": missing,
            "apis": results}
