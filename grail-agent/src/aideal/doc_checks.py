"""The AIDEAL check pipeline over LLM_readme.md.

1. form_check          - every API entry has the required sections
2. comprehension_check - README UNIT TEST: given ONLY the doc entry, the
                         audience model must write correct code (no other
                         source); the author model grades it against the doc
3. completeness_check  - are all public functions covered by the readme?
4. puzzle_check        - integration: runs the application-provided puzzle
                         command (GRAIL's evaluator) with a fix loop that
                         injects notes_to_self + error log on retries

Failures feed the error log; repeated failures distill into notes_to_self.
Each check returns {"check", "passed", "score", "details"}.

AIDEAL never imports the application (GRAIL) — layering is one-way.
"""

from __future__ import annotations

import random
import re
import shlex
import subprocess

from .config import AidealConfig
from .error_log import ErrorLog, new_run_id
from .notes_to_self import NotesToSelf
from .readme_agent import parse_readme, public_api_surface, public_api_details


# ---------------------------------------------------------------------------
# 1. Form check (no LLM)
# ---------------------------------------------------------------------------

def form_check(cfg: AidealConfig) -> dict:
    inventory = parse_readme(cfg.llm_readme)
    failures: dict[str, list[str]] = {}
    for entry in inventory:
        missing = [
            req for req in cfg.required_sections
            if not any(re.search(rf"^### {re.escape(a)}\s*$", entry.body, re.MULTILINE)
                       for a in req.split("|"))
        ]
        if "TODO" in entry.body:
            missing.append("unfilled TODOs")  # a skeleton is not documentation
        if missing:
            failures[entry.name] = missing
    n = len(inventory)
    return {
        "check": "form",
        "passed": bool(n) and not failures,
        "score": round((n - len(failures)) / n, 3) if n else 0.0,
        "details": {"apis": n, "complete": n - len(failures), "missing_sections": failures},
    }


# ---------------------------------------------------------------------------
# 2. Comprehension check = README unit test
# ---------------------------------------------------------------------------

def _comprehension_inventory(cfg: AidealConfig, doc_source: str):
    """Build the list of ApiEntry to test, or return (None, error_dict)."""
    from .readme_agent import ApiEntry
    if doc_source == "original":
        if not cfg.original_readme_files:
            return None, {"check": "comprehension", "passed": False, "score": 0.0,
                          "details": {"error": "files.original_readme not configured or missing"}}
        text = cfg.original_readme_text(limit=12000)
        names = sorted(public_api_surface(cfg))
        return [ApiEntry(name=n, goal="", snippet="",
                         body=f"(Original project README — the only documentation available)\n"
                              f"{text}\n\nTarget function: `{n}`")
                for n in names], None
    inventory = [e for e in parse_readme(cfg.llm_readme) if "TODO" not in e.body]
    if not inventory:
        return None, {"check": "comprehension", "doc_source": doc_source, "passed": False,
                      "score": 0.0,
                      "details": {"error": "LLM_readme has no filled entries (skeleton TODOs "
                                           "don't count) - run `readme --generate` or fill them"}}
    return inventory, None


def comprehension_check(cfg: AidealConfig, sample: int | None = None, seed: int = 42,
                        doc_source: str = "aideal", execute: bool = False,
                        show_code: bool = False) -> dict:
    """Given only the documentation, the audience model writes code; the author
    model grades strictly against the doc. Failures go to the error log.

    doc_source:
      "aideal"   - per-API entries from LLM_readme.md (the AIDEAL format)
      "original" - the project's ORIGINAL readme as the only context, with
                   target functions sampled from the code surface. This is
                   the baseline condition for original-vs-AIDEAL comparisons.
    execute: if True, the audience snippet is compiled/run via the configured
             `comprehension.execute` command instead of being LLM-graded —
             real execution ground truth. Defaults to ALL documented APIs.
    """
    from .llm import invoke_text
    from .profile import require_profile
    from .prompts import load as load_prompt

    require_profile(cfg)  # user must have entered project/target-user/domain fields
    inventory, err = _comprehension_inventory(cfg, doc_source)
    if err:
        return err
    if execute:
        return _comprehension_execute(cfg, inventory, sample, seed, doc_source, show_code=show_code)
    k = len(inventory) if sample == 0 else (sample or cfg.comprehension_apis_sampled)
    if k < len(inventory):
        inventory = random.Random(seed).sample(inventory, k)

    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()
    per_api: dict[str, object] = {}
    passed_n = 0
    ex = cfg.comprehension.get("execute", {}) if cfg.comprehension else {}
    _sample_data, available_inputs = _execute_sample_data(cfg, ex)
    for entry in inventory:
        code = invoke_text(
            cfg.model_for_role("audience"),
            *load_prompt(cfg, "aideal/comprehension_write",
                         api_body=entry.body, api_name=entry.name,
                         available_inputs=available_inputs),
        )
        verdict = invoke_text(
            cfg.model_for_role("author"),
            *load_prompt(cfg, "aideal/comprehension_grade",
                         api_body=entry.body, code=code),
        )
        if verdict.strip().upper().startswith("PASS"):
            passed_n += 1
            per_api[entry.name] = {"status": "pass", "code": code.strip()} if show_code else "pass"
        else:
            reason = verdict.split(":", 1)[-1].strip()[:200]
            per_api[entry.name] = (
                {"status": "fail", "reason": reason, "code": code.strip()}
                if show_code else f"fail: {reason}"
            )
            log.append(run_id=run_id, step="readme-unit-test", language=cfg.language,
                       task=f"comprehension_{doc_source}", status="fail",
                       function=entry.name, error=reason, root_cause="",
                       suggested_fix_code="")
    n = len(inventory)
    return {
        "check": "comprehension",
        "doc_source": doc_source,
        "passed": bool(n) and passed_n == n,
        "score": round(passed_n / n, 3) if n else 0.0,
        "details": per_api,
    }


def _fill_scaffold(scaffold: str, snippet: str, region: list[str], placeholders: dict) -> str:
    """Insert the snippet into the scaffold's API-test region and substitute
    {{KEY}} placeholders (sample-data paths). Generic: region markers and
    placeholder keys all come from config, nothing GRAIL-specific is hardcoded."""
    text = scaffold
    if region and len(region) == 2 and region[0] in text and region[1] in text:
        pre, _, rest = text.partition(region[0])
        _, _, post = rest.partition(region[1])
        text = f"{pre}{region[0]}\n{snippet}\n{region[1]}{post}"
    else:                                  # no region markers: append the snippet
        text = text + "\n" + snippet
    for key, val in (placeholders or {}).items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def _strip_fences(text: str, *, strip_imports: bool = False) -> str:
    """Remove markdown code fences / language tags the model may emit despite
    instructions, so the snippet is pure code. When the scaffold owns imports,
    callers can also drop model-generated import lines to avoid stale/wrong
    imports shadowing curated scaffold imports."""
    t = text.strip()
    if "```" in t:
        # keep the content of the first fenced block if present, else strip fences
        import re as _re
        m = _re.search(r"```[a-zA-Z]*\n(.*?)```", t, _re.DOTALL)
        t = m.group(1) if m else t.replace("```scala", "").replace("```", "")
    if strip_imports:
        t = "\n".join(
            line for line in t.strip().splitlines()
            if not line.lstrip().startswith("import ")
        )
    return t.strip()


def _execute_sample_data(cfg: AidealConfig, ex: dict) -> tuple[dict[str, str], str]:
    """Resolve configured sample-data bindings for prompts/scaffolds."""
    def _resolve(v):
        v = str(v)
        return str((cfg.root / v).resolve()) if (not v.startswith("/") and "/" in v) else v

    use_uri = ex.get("local_uris", True)

    def _as_uri(p):
        p = str(p)
        if "://" in p:
            return p
        return f"file://{p}" if (use_uri and p.startswith("/")) else p

    sample_data = {k: _as_uri(_resolve(v)) for k, v in (ex.get("sample_data", {}) or {}).items()}
    available_inputs = "\n".join(f"- {k} = {p}" for k, p in sample_data.items()) or "(none configured)"
    return sample_data, available_inputs


def _classify_error(merged: str, rc: int, error_marker: str) -> tuple[str, str, str]:
    """Return (category, message, locus) from the run output.
    category: compile | runtime | timeout | unknown; locus = the failing line/call."""
    import re as _re
    if rc == 124:
        return "timeout", "execution timed out", ""
    # runtime: the scaffold prints __RUN_ERR__ <Class>: <msg>
    if error_marker and error_marker in merged:
        line = next((l for l in merged.splitlines() if error_marker in l), "").strip()
        msg = line.split(error_marker, 1)[-1].strip()
        # first app stack frame = the failing call site
        frame = next((l.strip() for l in merged.splitlines()
                      if l.strip().startswith("at ") and ".scala" in l), "")
        return "runtime", msg or "runtime error", frame
    # compile: scalac prints `<file>.scala:NN: error: <msg>`
    cm = _re.search(r"^(.*\.scala:\d+: error: .*)$", merged, _re.MULTILINE)
    if cm:
        return "compile", cm.group(1).strip(), cm.group(1).split(":")[0:2] and cm.group(1).split(" error:")[0].strip()
    return "unknown", (merged.strip()[-300:] or f"exit {rc}"), ""


def _comprehension_execute(cfg: AidealConfig, inventory, sample, seed, doc_source: str,
                           show_code: bool = False) -> dict:
    """Compile/run each API's audience snippet via the configured command.
    PASS = the program runs (success_marker present, exit 0). Real failures
    (compile/runtime) are logged with the actual error text."""
    import os
    import shlex
    import subprocess
    import tempfile
    from pathlib import Path
    from .llm import invoke_text
    from .prompts import load as load_prompt

    ex = cfg.comprehension.get("execute", {}) if cfg.comprehension else {}
    cmd_template = ex.get("command", "")
    scaffold_path = ex.get("scaffold", "")
    if not cmd_template or not scaffold_path:
        return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                "details": {"error": "configure comprehension.execute.{command,scaffold} in aideal.yaml"}}
    scaffold_file = (cfg.root / scaffold_path).resolve()
    if not scaffold_file.exists():
        return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                "details": {"error": f"scaffold not found: {scaffold_file}"}}
    scaffold = scaffold_file.read_text(encoding="utf-8", errors="ignore")
    region = ex.get("region", ["// TODO API_TEST_START", "// TODO API_TEST_END"])

    # Build the project's own uberjar ONCE, then run snippets against that single
    # jar (no hand-listed dependency jars). build runs in build_cwd; {uberjar}
    # in the command is replaced with the resolved jar path.
    import glob as _glob
    build_cwd = (cfg.root / ex.get("build_cwd", ".")).resolve()
    build_cmd = ex.get("build", "")
    build_info = None
    if build_cmd:
        try:
            bp = subprocess.run(shlex.split(build_cmd), cwd=build_cwd, capture_output=True,
                                text=True, timeout=int(ex.get("build_timeout_seconds", 1800) or 1800))
        except FileNotFoundError as e:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": f"build tool not found ({e.filename}). Install Maven on "
                                "PATH, or set comprehension.execute.build: '' and point `uberjar` "
                                "at a prebuilt jar."}}
        except subprocess.TimeoutExpired:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": "project build timed out"}}
        build_info = {"exit_code": bp.returncode, "stderr_tail": bp.stderr[-400:]}
        if bp.returncode != 0:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": "project build failed", "build": build_info}}
    uberjar = ""
    uber_list: list[str] = []
    if ex.get("uberjar"):
        uber_list = sorted(_glob.glob(str(build_cwd / ex["uberjar"])))
        uberjar = uber_list[-1] if uber_list else ""
    # A glob of a prebuilt distribution's lib/*.jar — comma-joined as {jars}
    # (spark-submit --jars), colon-joined into {classpath} (scalac) below.
    jars = ""
    beast_jars_list: list[str] = []
    if ex.get("jars"):
        jg = str(ex["jars"])
        beast_jars_list = sorted(_glob.glob(jg if jg.startswith("/") else str(cfg.root / jg)))
        if not beast_jars_list:
            return {"check": "comprehension", "mode": "execute", "passed": False, "score": 0.0,
                    "details": {"error": f"no jars matched comprehension.execute.jars: {jg}"}}
        jars = ",".join(beast_jars_list)

    # {classpath} for scalac (COLON-separated): Spark jars + beast jars + the
    # uber jar (the uber carries JTS/GeoTools types so generated snippets that
    # reference them still compile). Runtime deps come from --packages.
    spark_jars: list[str] = []
    try:
        import pyspark as _pyspark
        _sj = os.path.join(os.path.dirname(_pyspark.__file__), "jars")
        spark_jars = sorted(_glob.glob(os.path.join(_sj, "*.jar")))
    except Exception:
        pass
    classpath = ":".join(beast_jars_list + spark_jars + uber_list)

    def _resolve(v):
        v = str(v)
        return str((cfg.root / v).resolve()) if (not v.startswith("/") and "/" in v) else v

    # Typed sample-data catalog: name -> resolved path. Each becomes a `val` in
    # the scaffold; the model picks the one(s) matching the API's param types.
    sample_data, available_inputs = _execute_sample_data(cfg, ex)
    bindings = "\n    ".join(f'val {k} = "{p}"' for k, p in sample_data.items())
    # legacy {{KEY}} placeholders still supported
    placeholders = {k: _resolve(v) for k, v in (ex.get("placeholders", {}) or {}).items()}
    success_marker = ex.get("success_marker", "")
    error_marker = ex.get("error_marker", "")
    timeout = int(ex.get("timeout_seconds", 600) or 600)
    strip_snippet_imports = bool(ex.get("strip_snippet_imports", False))
    output_tail_chars = int(ex.get("output_tail_chars", 2000) or 2000)
    max_fix_rounds = int(ex.get("max_fix_rounds", 1) or 0)   # attempts = 1 + retries
    work_dir = (cfg.root / ex.get("work_dir", ".aideal_exec")).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    # Scope execution to user-facing, runnable APIs. Most of the public surface
    # is internal/utility defs (close, copy, compareTo, hasNext, ...) that aren't
    # standalone-runnable — completeness covers all of them; execution shouldn't.
    include = set(ex.get("include", []) or [])
    exclude = set(ex.get("exclude", []) or [])
    # Reproducible alternative to a hand-list: select by DEFINING CLASS. User-
    # facing ops live in entrypoint classes (the SparkContext/RasterRDD mixin and
    # the operation objects); internal helpers live in tile/reader/serializer
    # classes. Derived from the `file` of each API — no manual judgment.
    entry_classes = set(ex.get("entrypoint_classes", []) or [])
    if entry_classes and not include:
        import os as _os
        include = {d["name"] for d in public_api_details(cfg)
                   if d["visibility"] == "public"
                   and _os.path.basename(d["file"])[:-6] in entry_classes}
    if include:
        inventory = [e for e in inventory if e.name in include]
    if exclude:
        inventory = [e for e in inventory if e.name not in exclude]
    if sample and sample < len(inventory):
        inventory = random.Random(seed).sample(inventory, sample)

    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()
    task = f"comprehension_exec_{doc_source}"
    per_api: dict[str, object] = {}
    passed_n = 0
    for entry in inventory:
        work_api = work_dir / f"run_{entry.name}"
        (work_api / "classes").mkdir(parents=True, exist_ok=True)
        scala_file = work_api / "ApiTest.scala"
        cmd = (cmd_template.replace("{scala_file}", str(scala_file))
               .replace("{uberjar}", uberjar).replace("{jars}", jars)
               .replace("{classpath}", classpath).replace("{work}", str(work_api)))

        ran = False
        last = {}
        last_run = {"stdout": "", "stderr": "", "exit_code": None}
        for attempt in range(1 + max_fix_rounds):
            # pull prior failures for THIS api (accumulated across rounds/runs)
            known = log.failures_for(entry.name)
            snippet = _strip_fences(invoke_text(
                cfg.model_for_role("audience"),
                *load_prompt(cfg, "aideal/comprehension_write_exec",
                             api_body=entry.body, api_name=entry.name,
                             available_inputs=available_inputs,
                             known_failures=known or "(none yet)"),
            ), strip_imports=strip_snippet_imports)
            scala = _fill_scaffold(scaffold.replace("// AIDEAL_DATA_BINDINGS", bindings),
                                   snippet, region, placeholders)
            scala_file.write_text(scala, encoding="utf-8")
            try:
                # shell=True so the `scalac && jar && spark-submit` pipeline runs
                proc = subprocess.run(cmd, shell=True, cwd=work_dir, capture_output=True,
                                      text=True, timeout=timeout, env=dict(os.environ))
                out, err_out, rc = proc.stdout, proc.stderr, proc.returncode
            except subprocess.TimeoutExpired as e:
                out, err_out, rc = (e.stdout or ""), (e.stderr or "") + "\n[timeout]", 124
            last_run = {"stdout": out or "", "stderr": err_out or "", "exit_code": rc}
            merged = (out or "") + "\n" + (err_out or "")
            ran = (rc == 0) and (success_marker in merged if success_marker else True) \
                and not (error_marker and error_marker in merged)
            if ran:
                # if this took a retry, log the working snippet as the solution
                if attempt > 0 and last:
                    log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                               task=task, status="fixed", function=entry.name,
                               error_category=last.get("cat", ""), error=last.get("msg", ""),
                               root_cause=last.get("locus", ""), code=last.get("code", ""),
                               suggested_fix_code=snippet.strip()[:1000])
                break
            cat, msg, locus = _classify_error(merged, rc, error_marker)
            last = {"cat": cat, "msg": msg, "locus": locus, "code": snippet.strip()[:1000]}
            log.append(run_id=run_id, step="readme-exec-test", language=cfg.language,
                       task=task, status="fail", function=entry.name,
                       error_category=cat, error=msg, root_cause=locus,
                       code=snippet.strip()[:1000], suggested_fix_code="")
        if ran:
            passed_n += 1
            status = "pass" if not last else "pass (after fix)"
            per_api[entry.name] = (
                {"status": status, "code": snippet.strip(), "scala_file": str(scala_file),
                 "exit_code": last_run["exit_code"],
                 "stdout_tail": last_run["stdout"][-output_tail_chars:],
                 "stderr_tail": last_run["stderr"][-output_tail_chars:]}
                if show_code else status
            )
        else:
            status = f"fail [{last.get('cat','?')}]: {last.get('msg','')[:140]}"
            per_api[entry.name] = (
                {"status": "fail", "error_category": last.get("cat", ""),
                 "error": last.get("msg", ""), "code": last.get("code", ""),
                 "scala_file": str(scala_file), "exit_code": last_run["exit_code"],
                 "stdout_tail": last_run["stdout"][-output_tail_chars:],
                 "stderr_tail": last_run["stderr"][-output_tail_chars:]}
                if show_code else status
            )
    n = len(inventory)
    # Report all three denominators explicitly (no ambiguity):
    #   raw_surface       = every visible public def (regex surface)
    #   intended_surface  = surface_filter set (what gets documented)
    #   executed          = the runnable subset actually compiled/run here
    raw = public_api_surface(cfg, override_filter="all")
    intended = public_api_surface(cfg)
    covered = {e.name for e in inventory}
    return {
        "check": "comprehension",
        "mode": "execute",
        "doc_source": doc_source,
        "passed": bool(n) and passed_n == n,
        "score": round(passed_n / n, 3) if n else 0.0,
        "coverage": {
            "raw_surface": len(raw),
            "intended_surface": len(intended),
            "surface_filter": cfg.surface_filter,
            "executed": n,
            "untested_intended": sorted(intended - covered)[:20],
        },
        "details": per_api,
    }


# ---------------------------------------------------------------------------
# 3. Completeness check (no LLM)
# ---------------------------------------------------------------------------

def _normalize(name: str) -> str:
    return re.sub(r"\[.*\]$", "", name).strip("`")


def completeness_check(cfg: AidealConfig) -> dict:
    surface = public_api_surface(cfg)                       # intended-API set
    raw = public_api_surface(cfg, override_filter="all")    # raw discovered surface
    documented = {_normalize(e.name) for e in parse_readme(cfg.llm_readme)}
    undocumented = sorted(surface - documented)
    n = len(surface)
    return {
        "check": "completeness",
        "passed": not undocumented,
        "score": round((n - len(undocumented)) / n, 3) if n else 0.0,
        "details": {
            "raw_surface": len(raw),               # every visible public def
            "intended_surface": n,                 # surface_filter set = denominator
            "surface_filter": cfg.surface_filter,
            "public_functions": n,                 # (= intended_surface; kept for back-compat)
            "documented": len(documented),
            "undocumented": undocumented,
            "orphan_doc_entries": sorted(documented - surface),
        },
    }


# ---------------------------------------------------------------------------
# 4. Puzzle check with fix loop
# ---------------------------------------------------------------------------

def puzzle_check(cfg: AidealConfig, dry_run: bool = False) -> dict:
    """Run the application-provided puzzle command. On failure, retry up to
    max_fix_rounds with notes_to_self + error log rendered to a hint file the
    runner can inject (passed via PUZZLE_HINTS env var)."""
    import os

    pz = cfg.puzzle
    cmd_template = pz.get("command", "")
    if not cmd_template:
        return {"check": "puzzle", "passed": False, "score": 0.0,
                "details": {"error": "no puzzle.command configured"}}
    cmd = cmd_template.format(
        llm_readme=cfg.llm_readme,
        n=pz.get("num_puzzles", 3),
        k=pz.get("num_functions", 5),
        seed=pz.get("seed", 42),
    )
    if dry_run:
        cmd += " --dry-run"

    notes = NotesToSelf(cfg.notes_to_self)
    log = ErrorLog(cfg.error_log)
    rounds = []
    max_rounds = 1 if dry_run else 1 + int(pz.get("max_fix_rounds", 0))
    for rnd in range(max_rounds):
        env = dict(os.environ)
        hints = "\n\n".join(x for x in (notes.to_prompt(), log.to_prompt()) if x)
        if hints:
            hint_path = cfg.error_log.parent / "puzzle_hints.txt"
            hint_path.parent.mkdir(parents=True, exist_ok=True)
            hint_path.write_text(hints, encoding="utf-8")
            env["PUZZLE_HINTS"] = str(hint_path)
        run_cwd = (cfg.root / pz.get("cwd", ".")).resolve()
        proc = subprocess.run(shlex.split(cmd), cwd=run_cwd,
                              capture_output=True, text=True, env=env)
        rounds.append({"round": rnd, "exit_code": proc.returncode,
                       "stdout_tail": proc.stdout[-500:]})
        if proc.returncode == 0:
            break
        notes.distill(log)  # consolidate before the next fix round
    ok = rounds[-1]["exit_code"] == 0
    return {"check": "puzzle", "passed": ok, "score": None,
            "details": {"command": cmd, "rounds": rounds}}
