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
from .readme_agent import parse_readme, public_api_surface


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

def comprehension_check(cfg: AidealConfig, sample: int | None = None, seed: int = 42,
                        doc_source: str = "aideal") -> dict:
    """Given only the documentation, the audience model writes code; the author
    model grades strictly against the doc. Failures go to the error log.

    doc_source:
      "aideal"   - per-API entries from LLM_readme.md (the AIDEAL format)
      "original" - the project's ORIGINAL readme as the only context, with
                   target functions sampled from the code surface. This is
                   the baseline condition for original-vs-AIDEAL comparisons.
    """
    from .llm import invoke_text
    from .profile import require_profile
    from .prompts import load as load_prompt
    from .readme_agent import ApiEntry

    require_profile(cfg)  # user must have entered project/target-user/domain fields
    if doc_source == "original":
        original = cfg.original_readme
        if original is None or not original.exists():
            return {"check": "comprehension", "passed": False, "score": 0.0,
                    "details": {"error": "files.original_readme not configured or missing"}}
        text = original.read_text(encoding="utf-8", errors="ignore")[:12000]
        names = sorted(public_api_surface(cfg))
        inventory = [
            ApiEntry(name=n, goal="", snippet="",
                     body=f"(Original project README — the only documentation available)\n"
                          f"{text}\n\nTarget function: `{n}`")
            for n in names
        ]
    else:
        inventory = [e for e in parse_readme(cfg.llm_readme) if "TODO" not in e.body]
        if not inventory:
            return {"check": "comprehension", "doc_source": doc_source, "passed": False,
                    "score": 0.0,
                    "details": {"error": "LLM_readme has no filled entries (skeleton TODOs "
                                         "don't count) - run `readme --generate` or fill them"}}
    k = sample or cfg.comprehension_apis_sampled
    if k < len(inventory):
        inventory = random.Random(seed).sample(inventory, k)

    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()
    per_api: dict[str, str] = {}
    passed_n = 0
    for entry in inventory:
        code = invoke_text(
            cfg.model_for_role("audience"),
            *load_prompt(cfg, "aideal/comprehension_write",
                         api_body=entry.body, api_name=entry.name),
        )
        verdict = invoke_text(
            cfg.model_for_role("author"),
            *load_prompt(cfg, "aideal/comprehension_grade",
                         api_body=entry.body, code=code),
        )
        if verdict.strip().upper().startswith("PASS"):
            passed_n += 1
            per_api[entry.name] = "pass"
        else:
            reason = verdict.split(":", 1)[-1].strip()[:200]
            per_api[entry.name] = f"fail: {reason}"
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


# ---------------------------------------------------------------------------
# 3. Completeness check (no LLM)
# ---------------------------------------------------------------------------

def _normalize(name: str) -> str:
    return re.sub(r"\[.*\]$", "", name).strip("`")


def completeness_check(cfg: AidealConfig) -> dict:
    surface = public_api_surface(cfg)
    documented = {_normalize(e.name) for e in parse_readme(cfg.llm_readme)}
    undocumented = sorted(surface - documented)
    n = len(surface)
    return {
        "check": "completeness",
        "passed": not undocumented,
        "score": round((n - len(undocumented)) / n, 3) if n else 0.0,
        "details": {
            "public_functions": n,
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
