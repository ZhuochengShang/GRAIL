#!/usr/bin/env python3
"""GRAIL demo agent — task-analyzed, section-by-section  text/Python -> RDPro Scala.

Five-step pipeline (replaces the old flat "one giant prompt -> one giant body"
design, which had no way to condition generation on the actual task):

  STEP 1 — ANALYZE
      One LLM call reads the task against the documented API surface's Goal
      lines only (cheap: ~200 one-liners, not the full 500K+ char readme) and
      returns which SECTIONS the job needs (LOAD_DATA/OUTPUT always; TYPE_CHECK/
      SPATIAL_CHECK/TRANSFORM/ANALYTICS only if the task needs them) plus a
      shortlist of candidate documented API names per section. Names not in the
      real API surface are dropped — this step routes, it never invents.

  STEP 2 — INPUTS
      Resolved deterministically from `comprehension.execute.sample_data`
      (same mechanism the rest of AIDEAL already uses) — never LLM-generated.
      Path vals are spliced into the scaffold outside the generated region, so
      LOAD_DATA only has to load them, never guess their names.

  STEP 3 — SECTIONS
      Each analyzed section is generated with a prompt grounded ONLY in the
      full LLM_readme entries for that section's shortlisted APIs — not a
      blind slice of the whole doc file (which, at 500K+ chars, meant most
      generations never saw the relevant entry at all).

  STEP 4 — FIX LOOP (per section)
      Each section is compiled+run on its own, appended to the sections
      already confirmed working (a syntactically-complete partial Scala body
      compiles fine even if the job doesn't do much yet). On failure, the real
      compiler/runtime error is fed back for up to `--rounds` retries before
      moving on.

  STEP 5 — LOG
      Every attempt (pass / fail / fixed) is appended to the SAME aideal
      ErrorLog (`logs/error_log.jsonl`) that `comprehension --execute` and
      `augment` use — this run's failures/fixes become part of AIDEAL's
      persistent, cross-session memory instead of a disposable local log.

Usage (unchanged from before):
    python demo_agent.py --text "Compute land-use % per Boston neighborhood ..." --execute --rounds 3
    python demo_agent.py --python ../../grail-agent/examples/python/zonal_stats_minmax.py --execute
    python demo_agent.py --text "..." --dry-run --show-code

`--execute` needs OPENAI_API_KEY and a working spark-submit; `--dry-run` stubs
both the analysis and the generation calls (a keyword heuristic replaces the
LLM for STEP 1, and STEP 3 returns a labeled placeholder per section) so the
five-step wiring is demonstrable with no key. Unlike the old dry-run, the stub
output now depends on the actual task text and the analyzed API picks, not a
single hardcoded zonal-stats scenario.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# AIDEAL backend modules (the agent reuses them; it never reimplements them).
from aideal.config import load_config
from aideal.error_log import ErrorLog, new_run_id
from aideal.notes_to_self import NotesToSelf
from aideal.alias_registry import AliasRegistry
from aideal.readme_agent import parse_readme
# Shared with the per-API comprehension loop so both converge the same way
# (single source of truth for the error-signature -> fix-hint mapping).
from aideal.fix_guide import FIX_GUIDE, classify  # noqa: F401  (FIX_GUIDE re-exported)


SECTION_ORDER = ["LOAD_DATA", "TYPE_CHECK", "SPATIAL_CHECK", "TRANSFORM", "ANALYTICS", "OUTPUT"]
ALWAYS_SECTIONS = {"LOAD_DATA", "OUTPUT"}
MAX_APIS_PER_SECTION = 4

# What each section is FOR — without this the model infers section meaning from
# the NAME alone and misfiles the main computation into a "check" section (e.g.
# `zonalStatsLocal`/`spatialJoin` landing in SPATIAL_CHECK, which should only
# hold lightweight precondition checks, not the task's actual answer).
SECTION_DESCRIPTIONS = {
    "LOAD_DATA":     "read raw inputs into typed RDDs. Loading only — no computation.",
    "TYPE_CHECK":    "verify pixel/attribute types BEFORE computing. Lightweight validation "
                     "only — do NOT put the main computation here.",
    "SPATIAL_CHECK": "verify CRS/alignment/extent compatibility BEFORE computing. Lightweight "
                     "validation only — do NOT put joins, zonal stats, or aggregation here.",
    "TRANSFORM":     "reshape/reproject/mask/convert data in preparation for the main computation.",
    "ANALYTICS":     "THE MAIN COMPUTATION that answers the task's actual question — joins, "
                     "zonal statistics, and aggregations belong HERE, not in TYPE_CHECK or "
                     "SPATIAL_CHECK.",
    "OUTPUT":        "write the final result to disk.",
}


def extract_errors(output: str, limit: int = 25) -> str:
    """Pull the actual compiler/runtime error lines out of the build output.
    The generic fix hint tells the model WHAT KIND of mistake it made; these lines
    tell it WHICH symbol on WHICH line — without them the repair loop regenerates
    near-identical code every round. Keeps scalac `file.scala:NN: error:` lines,
    `__RUN_ERR__` markers, and the summary; falls back to the output tail."""
    hits = [l.strip() for l in output.splitlines()
            if ".scala:" in l or "error:" in l.lower()
            or "__RUN_ERR__" in l or l.strip().lower().endswith(("errors found", "error found"))]
    if not hits:
        return (output or "").strip()[-1500:]
    return "\n".join(hits[:limit])


_VAL_DECL_RE = re.compile(r"\bval\s+(\w+)\s*[:=]")


def _declared_vars(body: str) -> set[str]:
    return set(_VAL_DECL_RE.findall(body or ""))


# --------------------------------------------------------------------------- #
# STEP 1 — ANALYZE: which sections, which candidate APIs, grounded in Goal lines.
# --------------------------------------------------------------------------- #
_KEYWORD_BUCKETS = {
    # bucket -> (task keywords, name/goal keywords to match against). Offline-only
    # heuristic (--dry-run has no LLM call); real runs use analyze_task()'s prompt.
    "join_agg":  (["join", "zonal", "raptor", "aggregat", "total", "sum",
                   "average", "mean", "count", "percent", "%"], ["raptor", "zonal", "join", "sum", "count", "aggregate"]),
    "transform": (["mask", "filter", "threshold", "convert", "subtract", "clip",
                   "reproject", "crop"], ["mappixels", "filterpixels", "overlay", "reproject", "mask"]),
    "csv_table": (["csv", "table", "attribute"], ["csv", "table"]),
    "vector":    (["polygon", "shapefile", "geojson", "vector", "boundary", "neighborhood"],
                  ["shapefile", "geojson", "feature", "vector"]),
    "raster":    (["raster", "geotiff", "pixel", "band", "tif"], ["geotiff", "raster", "pixel", "tile"]),
    "output":    (["csv", "geotiff", "geojson", "shapefile", "save", "write"],
                  ["save", "write"]),
}


def build_analysis_prompt(task: str, entries) -> tuple[str, str]:
    listing = "\n".join(f"- {e.name}: {e.goal}" for e in entries if e.goal) or \
              "\n".join(f"- {e.name}" for e in entries)
    section_defs = "\n".join(f"  {s}: {SECTION_DESCRIPTIONS[s]}" for s in SECTION_ORDER)
    system = (
        "You PLAN which parts of an RDPro Spark-Scala job a task needs — you do not "
        "write code. Sections, in required order, and what each one is FOR:\n"
        f"{section_defs}\n\n"
        "LOAD_DATA and OUTPUT are always required. Include TYPE_CHECK, SPATIAL_CHECK, "
        "TRANSFORM, and/or ANALYTICS ONLY if the task genuinely needs that KIND of step — "
        "most single-pass tasks (a join, an aggregate, a report) do NOT need a separate "
        "TYPE_CHECK or SPATIAL_CHECK; do not include a section just because it exists in "
        "the list. The task's main computation (a join, a zonal/spatial statistic, an "
        "aggregation) belongs in ANALYTICS — never in TYPE_CHECK or SPATIAL_CHECK, even if "
        "an API name sounds like it fits one of those better.\n\n"
        "First identify `primary_api`: the ONE documented API below that most directly "
        "answers what the task is asking for, chosen by what it actually DOES (per its "
        "goal text), not by how closely its name matches words in the task. Then, for each "
        f"included section, list up to {MAX_APIS_PER_SECTION} candidate API names FROM THE "
        "LIST BELOW ONLY — never invent a name not in the list. `primary_api` must also "
        "appear in whichever section's list it logically belongs to.\n\n"
        "Reply with JSON only, no prose, no markdown fences, exactly this shape:\n"
        '{"primary_api": "name", "sections": ["LOAD_DATA", "..."], '
        '"apis_by_section": {"LOAD_DATA": ["name1", "name2"]}}'
    )
    user = f"TASK:\n{task}\n\nDOCUMENTED APIs (name: goal):\n{listing}"
    return system, user


def _parse_and_validate_analysis(raw: str, entries) -> dict:
    """Keep the plan; drop any API name the model invented that isn't actually
    documented — this step routes to real docs, it must never smuggle a
    hallucinated name past the router and into a generation prompt as if it
    were real."""
    valid_names = {e.name for e in entries}
    try:
        start, end = raw.index("{"), raw.rindex("}") + 1
        parsed = json.loads(raw[start:end])
    except Exception:
        parsed = {}

    sections = [s for s in parsed.get("sections", []) if s in SECTION_ORDER]
    for req in ALWAYS_SECTIONS:
        if req not in sections:
            sections.append(req)
    sections = [s for s in SECTION_ORDER if s in sections]  # canonical order

    apis_by_section: dict[str, list[str]] = {}
    dropped: list[str] = []
    for sec, names in (parsed.get("apis_by_section", {}) or {}).items():
        if sec not in sections:
            continue
        kept = [n for n in names if n in valid_names]
        dropped += [n for n in names if n not in valid_names]
        if kept:
            apis_by_section[sec] = kept[:MAX_APIS_PER_SECTION]

    # `primary_api` exists specifically so the single best-matching operation
    # can't lose to lexical name-coincidence in the per-section split (e.g.
    # `raptorJoinFeature` losing to `spatialJoin`/`zonalStatsLocal` on name
    # resemblance alone). Force it into ANALYTICS (or TRANSFORM if ANALYTICS
    # wasn't included) so it can never be silently dropped.
    primary = parsed.get("primary_api", "")
    if primary and primary not in valid_names:
        dropped.append(primary)
        primary = ""
    if primary:
        target = "ANALYTICS" if "ANALYTICS" in sections else (
            "TRANSFORM" if "TRANSFORM" in sections else sections[-1])
        bucket = apis_by_section.setdefault(target, [])
        if primary not in bucket:
            bucket.insert(0, primary)
            apis_by_section[target] = bucket[:MAX_APIS_PER_SECTION + 1]  # +1: primary is guaranteed, not counted against the cap

    if not any(apis_by_section.get(s) for s in sections):
        # Analysis returned nothing usable -> don't silently ground sections on
        # nothing; fall back to the offline heuristic rather than proceeding blind.
        offline = _analyze_task_offline(parsed.get("_task", "") or "", entries)
        apis_by_section = offline["apis_by_section"]

    return {"sections": sections, "apis_by_section": apis_by_section,
            "primary_api": primary, "dropped_hallucinated": dropped}


def _analyze_task_offline(task: str, entries) -> dict:
    """No-LLM heuristic for --dry-run: match task keywords against each entry's
    name+goal text to pick section list and per-section candidates. Deliberately
    simple (this is the offline stub, not the real router) but genuinely reacts
    to the task text instead of returning one fixed scenario."""
    t = (task or "").lower()
    sections = ["LOAD_DATA"]
    if any(k in t for k in _KEYWORD_BUCKETS["join_agg"][0]):
        sections.append("ANALYTICS")
    if any(k in t for k in _KEYWORD_BUCKETS["transform"][0]):
        sections.append("TRANSFORM")
    sections.append("OUTPUT")
    sections = [s for s in SECTION_ORDER if s in sections]

    def matches_for(bucket_names: list[str]) -> list[str]:
        hits = []
        for e in entries:
            hay = (e.name + " " + (e.goal or "")).lower()
            if any(kw in hay for kw in bucket_names):
                hits.append(e.name)
        return hits

    apis_by_section: dict[str, list[str]] = {}
    for sec in sections:
        pool: list[str] = []
        for bucket, (task_kws, name_kws) in _KEYWORD_BUCKETS.items():
            if any(k in t for k in task_kws):
                pool += matches_for(name_kws)
        # de-dup, keep order
        seen = set()
        pool = [x for x in pool if not (x in seen or seen.add(x))]
        if pool:
            apis_by_section[sec] = pool[:MAX_APIS_PER_SECTION]
    return {"sections": sections, "apis_by_section": apis_by_section, "dropped_hallucinated": []}


def analyze_task(cfg, task: str, entries, dry_run: bool) -> dict:
    if dry_run:
        return _analyze_task_offline(task, entries)
    from aideal.llm import invoke_text
    system, user = build_analysis_prompt(task, entries)
    # Routing/ranking across 200+ candidates is a harder reasoning task than
    # per-section code generation — worth the stronger model even though
    # section generation itself stays on `author`.
    raw = invoke_text(cfg.model_for_role("audience"), system, user).strip()
    return _parse_and_validate_analysis(raw, entries)


# --------------------------------------------------------------------------- #
# STEP 3 — per-section grounding text, built ONLY from that section's picks.
# --------------------------------------------------------------------------- #
def section_grounding(entries, names: list[str]) -> str:
    by_name = {e.name: e for e in entries}
    bodies = [by_name[n].body for n in names if n in by_name]
    if not bodies:
        return ("(no documented API matched for this section — write the minimum "
                "necessary Scala, note any assumption as a `//` comment, and avoid "
                "inventing RDPro-specific calls not seen elsewhere in this prompt)")
    return "\n\n---\n\n".join(bodies)


def build_section_prompt(task: str, sec: str, section_doc_text: str, prior_body: str,
                         available_inputs: str, io_hints: str, round_hints: str) -> tuple[str, str]:
    system = (
        f"You write ONE section, `{sec}`, of a larger RDPro Spark-Scala job body — "
        "not the whole job. Output ONLY the Scala statements for this section: no "
        "markdown, no object/class wrapper, no imports (the scaffold provides them), "
        "no other sections. Use ONLY the documented API entries given below for this "
        "section; do not call any RDPro API that isn't shown here or in the code "
        "already written. Reuse variable names already defined in the code written so "
        "far — do not redeclare or reload them."
    )
    user = f"""TASK:
{task}

THIS SECTION: {sec}

=== DOCUMENTED APIs FOR THIS SECTION (your only source of truth for {sec}) ===
{section_doc_text}

=== AVAILABLE INPUTS (in-scope val names — use exactly these; only relevant in LOAD_DATA) ===
{available_inputs}

=== I/O HINTS ===
{io_hints}

=== CODE ALREADY WRITTEN (earlier sections — do not repeat; reuse its variable names) ===
{prior_body or '(nothing yet — this is the first section)'}
{round_hints}
Write ONLY the `{sec}` section's Scala statements now."""
    return system, user


def translate_section(cfg, system: str, user: str, dry_run: bool, sec: str,
                      attempt: int, candidates: list[str]) -> str:
    """STEP 3 generation call. dry_run stub now depends on THIS section's actual
    analyzed candidates, not a fixed scenario — attempt 0 deliberately calls an
    invented variant of the first candidate to exercise the fix loop generically
    for whatever task/section is actually in play; attempt >0 'fixes' it using
    the real candidate name (still a stub — no compiler truly validated it).

    Fences are stripped HERE, at the source, not later on the concatenated
    body. Stripping only after concatenating prior_body + this section's body
    is wrong: if this section comes back fenced (models do this despite being
    told not to), the fence-matching regex keeps only what's inside the fence
    and silently drops every earlier section's code sitting in front of it —
    a real bug this caused (`not found: value neighborhoods` for a value
    LOAD_DATA had already declared, because LOAD_DATA's text was discarded
    before the file was ever written)."""
    if dry_run:
        api = candidates[0] if candidates else f"{sec.lower()}Op"
        if attempt == 0:
            return f"// dry-run stub ({sec}, attempt {attempt})\nval _{sec.lower()}_bad = {api}NotReal(???)"
        return f"// dry-run stub ({sec}, attempt {attempt}, candidate={api})\n// val _{sec.lower()}_ok = {api}(...)"
    from aideal.llm import invoke_text
    from aideal.doc_checks import _strip_fences
    raw = invoke_text(cfg.model_for_role("author"), system, user).strip()
    return _strip_fences(raw)


# --------------------------------------------------------------------------- #
# STEP 2 (inputs) + STEP 4 (compile/run) — shared scaffold splicing/execution.
# --------------------------------------------------------------------------- #
def resolve_inputs(cfg):
    """STEP 2: deterministic, never LLM-generated. Reuses the same resolver the
    rest of AIDEAL uses, so this run sees exactly what `comprehension --execute`
    sees — no separate, possibly-inconsistent input-guessing logic."""
    from aideal.doc_checks import _execute_sample_data
    ex = (cfg.comprehension or {}).get("execute", {})
    sample_data, available_inputs, warnings = _execute_sample_data(cfg, ex)
    return sample_data, available_inputs, warnings, ex


def run_scala(cfg, ex: dict, scala_body: str, sample_data: dict, work: Path,
              dry_run: bool, attempt: int) -> tuple[bool, str]:
    """Splice the accumulated body into the scaffold + compile/run. Dry-run
    simulates a first-attempt failure then success so the repair loop is
    observable offline."""
    if dry_run:
        if attempt == 0:
            return False, "error: not found: value NotReal"
        return True, "__DONE__ object=GeoJob"
    import glob as _glob, os as _os, subprocess as _sp
    from aideal.doc_checks import _strip_fences
    scala_body = _strip_fences(scala_body, strip_imports=True)
    scaffold = Path((cfg.root / ex["scaffold"])).read_text(encoding="utf-8")
    bindings = "\n    ".join(f'val {k} = "{v}"' for k, v in sample_data.items())
    region = ex.get("region", ["// TODO API_TEST_START", "// TODO API_TEST_END"])
    scala = scaffold.replace("// AIDEAL_DATA_BINDINGS", bindings)
    head, _, rest = scala.partition(region[0])
    _, _, tail = rest.partition(region[1])
    scala = f"{head}{region[0]}\n{scala_body}\n{region[1]}{tail}"
    work.mkdir(parents=True, exist_ok=True)
    scala_file = work / "ApiTest.scala"; scala_file.write_text(scala, encoding="utf-8")
    root = cfg.root
    beast_jars = _glob.glob(str(root / ex["jars"])) if ex.get("jars") else []
    uber = (_glob.glob(str((root / ex.get("build_cwd", ".")) / ex["uberjar"]))
            if ex.get("uberjar") else [])
    try:
        import pyspark
        spark_jars = _glob.glob(_os.path.join(_os.path.dirname(pyspark.__file__), "jars", "*.jar"))
    except Exception:
        spark_jars = []
    classpath = ":".join(beast_jars + spark_jars + uber)
    jars = ",".join(beast_jars)
    pflag = ("--packages " + ",".join(ex["packages"])) if ex.get("packages") else ""
    rflag = ("--repositories " + ",".join(ex["repositories"])) if ex.get("repositories") else ""
    cmd = (ex["command"].replace("{scala_file}", str(scala_file)).replace("{jars}", jars)
           .replace("{classpath}", classpath).replace("{work}", str(work))
           .replace("{packages}", pflag).replace("{repositories}", rflag)
           .replace("{uberjar}", uber[0] if uber else ""))
    proc = _sp.run(cmd, shell=True, cwd=str(root), capture_output=True, text=True,
                   timeout=900, env=dict(_os.environ))
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    return (proc.returncode == 0 and "__DONE__" in out), out


# --------------------------------------------------------------------------- #
# STEP 4 + STEP 5 — per-section fix loop, logged to the shared error_log.
# --------------------------------------------------------------------------- #
def run_section(cfg, ex, task_id, task, sec, entries, candidates, sections_body: dict,
                sample_data, available_inputs, io_hints, log: ErrorLog, notes: NotesToSelf,
                run_id: str, work_root: Path, max_rounds: int, dry_run: bool, execute: bool,
                show_code: bool) -> tuple[bool, str]:
    prior_body = "\n\n".join(sections_body[s] for s in SECTION_ORDER if s in sections_body)
    section_doc_text = section_grounding(entries, candidates)
    round_hints = ""
    body = ""
    # Neither --execute nor --dry-run: generate text only, single attempt, no
    # compile, no fix loop (nothing to fix without running it). Matches the
    # original flat demo_agent's "(generated; --execute to run)" behavior.
    rounds_to_try = (1 + max_rounds) if (execute or dry_run) else 1
    for attempt in range(rounds_to_try):
        system, user = build_section_prompt(task, sec, section_doc_text, prior_body,
                                            available_inputs, io_hints, round_hints)
        body = translate_section(cfg, system, user, dry_run, sec, attempt, candidates)
        if not (execute or dry_run):
            print(f"  [{sec}] generated (pass --execute to compile+run)")
            return True, body
        full_body = prior_body + ("\n\n" if prior_body else "") + body
        ok, output = run_scala(cfg, ex, full_body, sample_data,
                               work_root / f"{sec.lower()}_a{attempt}", dry_run, attempt)

        # Correctness gate for OUTPUT: compiling+running isn't enough — a body
        # that just re-saves LOAD_DATA's raw input passes this check with the
        # task's actual answer never written anywhere. If OUTPUT references
        # NONE of the variables any earlier non-LOAD_DATA section declared,
        # treat it as a failure with a specific hint rather than a silent
        # compiling-but-wrong PASS.
        correctness_note = ""
        if ok and sec == "OUTPUT":
            computed_vars = set()
            for s in SECTION_ORDER:
                if s in ("LOAD_DATA", "OUTPUT") or s not in sections_body:
                    continue
                computed_vars |= _declared_vars(sections_body[s])
            if computed_vars and not any(re.search(rf"\b{re.escape(v)}\b", body) for v in computed_vars):
                ok = False
                correctness_note = (
                    f"OUTPUT does not reference any variable computed by an earlier "
                    f"section ({', '.join(sorted(computed_vars))}) — it looks like it "
                    f"is saving the raw LOAD_DATA input instead of the actual computed "
                    f"result. Save one of those variables, not the original input.")

        print(f"  [{sec}] attempt {attempt}: {'PASS' if ok else 'FAIL'}"
             + (" (compiled, but ignored the computed result)" if correctness_note else ""))
        if show_code:
            print(f"    --- generated body ({sec}, attempt {attempt}) ---")
            print("\n".join(f"      {l}" for l in body.splitlines()))
            if not ok:
                print(f"    --- errors ({sec}, attempt {attempt}) ---")
                print("\n".join(f"      {l}" for l in (correctness_note or extract_errors(output)).splitlines()))
        if ok:
            # STEP 5: log the outcome either way, so a section that took retries
            # is distinguishable (status=fixed) from one that passed cleanly.
            log.append(run_id=run_id, step="demo-section", language="Scala", task=task_id,
                       function=f"(job:{sec})", status=("fixed" if attempt > 0 else "pass"),
                       code=body.strip()[:1500])
            return True, body
        if correctness_note:
            cat, hint, err_block = "no-result-used", correctness_note, correctness_note
        else:
            cat, hint = classify(output)
            err_block = extract_errors(output)
        log.append(run_id=run_id, step="demo-section", language="Scala", task=task_id,
                   function=f"(job:{sec})", status="fail", error=err_block,
                   error_category=cat, suggested_fix_code=hint, code=body.strip()[:1500])
        notes.distill(log)
        round_hints = (f"\n=== FIX FOR LAST FAILURE ([{cat}]) ===\n{hint}\n"
                       f"\n=== ACTUAL COMPILER/RUNTIME ERRORS from your last attempt — "
                       f"fix THESE specific lines ===\n{err_block}\n")
    return False, body


# --------------------------------------------------------------------------- #
# Reusable entry point: one full run of the 5-step pipeline for one task.
# Used by main() (single CLI run) and by run_test_suite.py (batch runs) so
# both share identical logic — no risk of the two drifting apart.
# --------------------------------------------------------------------------- #
def run_task(cfg, task: str, task_id: str, out_path: Path, rounds: int,
            dry_run: bool, execute: bool, show_code: bool) -> dict:
    """Run the full 5-step pipeline for one task. `task_id` distinguishes this
    run's error_log/work-dir entries from other tasks sharing the same shared
    log file (important once a batch of test cases runs against one project).
    Returns a structured result — never raises for an ordinary pipeline failure
    (unresolved sections are a normal outcome, reflected in `status`)."""
    run_id = new_run_id()
    work_root = cfg.root / ".aideal_demo" / task_id
    if dry_run:
        work_root.mkdir(parents=True, exist_ok=True)
        log = ErrorLog(work_root / "error_log.jsonl")   # dry-run stays local, never touches shared state
        notes = NotesToSelf(work_root / "notes_to_self.md")
    else:
        log = ErrorLog(cfg.error_log)
        notes = NotesToSelf(cfg.notes_to_self)

    entries = [e for e in parse_readme(cfg.llm_readme) if "TODO" not in e.body]
    if not entries:
        return {"task_id": task_id, "status": "error",
                "error": "LLM_readme.md has no filled entries — run `aideal readme --generate` first"}

    # STEP 1
    analysis = analyze_task(cfg, task, entries, dry_run)
    print(f"[analyze] primary_api={analysis.get('primary_api') or '(none identified)'}")
    print(f"[analyze] sections={analysis['sections']}")
    for sec in analysis["sections"]:
        print(f"  {sec}: {analysis['apis_by_section'].get(sec, [])}")
    if analysis.get("dropped_hallucinated"):
        print(f"[analyze] dropped non-documented names the model invented: "
              f"{analysis['dropped_hallucinated']}")

    # STEP 2
    sample_data, available_inputs, sd_warnings, ex = resolve_inputs(cfg)
    print(f"[inputs] resolved {len(sample_data)} bindings deterministically (no LLM):")
    print("\n".join(f"  {l}" for l in available_inputs.splitlines()))
    if sd_warnings:
        for w in sd_warnings:
            print(f"  WARNING: {w}")
    if not ex.get("scaffold") and execute:
        return {"task_id": task_id, "status": "error",
                "error": "comprehension.execute.scaffold not configured"}

    try:
        from aideal.doc_checks import _resolve_io_hints
        io_hints = _resolve_io_hints(cfg, ex, sample_data) or "(none)"
    except Exception:
        io_hints = "(none)"

    # STEPS 3-5, per section
    sections_body: dict[str, str] = {}
    all_ok = True
    failed_section = None
    for sec in analysis["sections"]:
        candidates = analysis["apis_by_section"].get(sec, [])
        print(f"\n=== SECTION {sec} (candidates: {candidates or '(none matched)'}) ===")
        ok, body = run_section(cfg, ex, task_id, task, sec, entries, candidates, sections_body,
                               sample_data, available_inputs, io_hints, log, notes, run_id,
                               work_root, rounds, dry_run, execute, show_code)
        sections_body[sec] = body
        if not ok:
            all_ok = False
            failed_section = sec
            print(f"[result] SECTION {sec} unresolved after {rounds} fix attempts — stopping here.")
            break

    final_body = "\n\n".join(f"// SECTION {s}\n{sections_body[s]}"
                             for s in SECTION_ORDER if s in sections_body)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(final_body + "\n", encoding="utf-8")

    proposals = log.suggest_aliases()
    print(f"\n[result] status={'RUNNABLE' if all_ok else 'unresolved'} | scala -> {out_path}")
    if proposals:
        print("[alias proposals mined from failures]:",
              ", ".join(f"{p['proposed_alias']}(x{p['evidence_count']})" for p in proposals[:6]))
    print(f"[error log] {log.path}  (feeds aideal notes-distill / alias-suggest)")

    return {
        "task_id": task_id,
        "status": "RUNNABLE" if all_ok else "unresolved",
        "primary_api": analysis.get("primary_api") or "",
        "sections": analysis["sections"],
        "apis_by_section": analysis["apis_by_section"],
        "failed_section": failed_section,
        "scala_path": str(out_path),
        "alias_proposals": [p["proposed_alias"] for p in proposals[:6]],
    }


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="GRAIL demo agent: text/Python -> RDPro Scala (sectioned)")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="natural-language task")
    src.add_argument("--python", help="path to a Python script to translate")
    ap.add_argument("--config", default="configs/aideal.yaml")
    ap.add_argument("--rounds", type=int, default=3,
                    help="max fix attempts PER SECTION (each section gets its own budget)")
    ap.add_argument("--out", default="docs/demo_generated.scala")
    ap.add_argument("--execute", action="store_true", help="really compile + spark-submit")
    ap.add_argument("--dry-run", action="store_true", help="offline: stub LLM + runner")
    ap.add_argument("--show-code", action="store_true",
                    help="print the generated body + raw errors for every section attempt")
    a = ap.parse_args()

    cfg = load_config(a.config)
    task = a.text or (f"Translate this Python workflow to RDPro Scala:\n\n"
                      f"{Path(a.python).read_text(encoding='utf-8')}")
    out_path = (cfg.root / ".aideal_demo" / "cli" / "demo_generated.scala") if a.dry_run else (cfg.root / a.out)
    result = run_task(cfg, task, "cli", out_path, a.rounds, a.dry_run, a.execute, a.show_code)
    if result["status"] == "error":
        print(f"[error] {result['error']}", file=sys.stderr)
        return 2
    return 0 if result["status"] == "RUNNABLE" else 1


if __name__ == "__main__":
    sys.exit(main())