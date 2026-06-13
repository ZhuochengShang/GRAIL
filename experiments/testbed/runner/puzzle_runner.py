"""Puzzle runner for barelib (Python target — no Spark needed).

Samples N functions, asks the AUDIENCE model to compose them into one
program, EXECUTES the generated code against barelib, and scores it.

Two documentation modes (this is the measured variable):
  - LLM_readme exists  -> the model gets the doc entries (post-readme stages)
  - no readme          -> the model gets ONLY the raw source of the sampled
                          functions (stage-0 baseline)

Supports PUZZLE_HINTS (path to a hints file from notes_to_self / error log)
so the fix loop measurably changes generation.

Exit code: 0 if all puzzles pass, 1 otherwise (drives AIDEAL's fix loop).
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

TESTBED = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TESTBED))

from aideal.config import load_config           # noqa: E402
from aideal.error_log import ErrorLog, new_run_id  # noqa: E402
from aideal.llm import invoke_text               # noqa: E402
from aideal.readme_agent import parse_readme     # noqa: E402

import barelib                                   # noqa: E402


def inventory(api_doc: Path) -> list[dict]:
    """Each item: {name, context} where context is doc entry or raw source."""
    if api_doc.exists():
        return [{"name": re.sub(r"\[.*\]$", "", e.name), "context": e.body}
                for e in parse_readme(api_doc)]
    items = []
    for name in sorted(barelib.__dict__):
        fn = getattr(barelib, name)
        if callable(fn) and not name.startswith("_"):
            items.append({"name": name, "context": inspect.getsource(fn)})
    return items


def compose_prompt(funcs: list[dict], hints: str, mode: str) -> tuple[str, str]:
    system = (
        "You write Python code using the `barelib` library. Use ONLY the "
        f"{'documentation' if mode == 'readme' else 'source code'} provided — "
        "no other assumptions about the library. Output only code, no fences."
    )
    parts = [f"Reference ({mode}):"]
    parts += [f["context"] for f in funcs]
    names = ", ".join(f["name"] for f in funcs)
    parts.append(
        f"\nWrite one Python program that imports barelib and calls each of "
        f"these functions at least once in a coherent flow: {names}. "
        "Construct small inputs inline (grids are lists of equal-length "
        "lists). Print one line of evidence per function call. "
        "The program must run without errors."
    )
    if hints:
        parts.append("\n" + hints)
    return system, "\n\n".join(parts)


def extract_code(text: str) -> str:
    m = re.search(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


def run_code(code: str, workdir: Path, timeout: int = 20) -> dict:
    script = workdir / "candidate.py"
    script.write_text(code, encoding="utf-8")
    env = dict(os.environ, PYTHONPATH=str(TESTBED))
    try:
        proc = subprocess.run([sys.executable, str(script)], capture_output=True,
                              text=True, timeout=timeout, env=env)
        return {"exit": proc.returncode, "stdout": proc.stdout[-1000:],
                "stderr": proc.stderr[-1500:]}
    except subprocess.TimeoutExpired:
        return {"exit": -1, "stdout": "", "stderr": f"timeout {timeout}s"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(TESTBED / "configs/aideal.yaml"))
    p.add_argument("--api-doc", default=str(TESTBED / "docs/LLM_readme.md"))
    p.add_argument("--num-puzzles", type=int, default=5)
    p.add_argument("--num-functions", type=int, default=4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--tag", default="run")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    cfg = load_config(args.config)
    api_doc = Path(args.api_doc)
    inv = inventory(api_doc)
    mode = "readme" if api_doc.exists() else "source-only"
    rng = random.Random(args.seed)
    puzzles = [rng.sample(inv, min(args.num_functions, len(inv)))
               for _ in range(args.num_puzzles)]

    hints = ""
    hint_path = os.environ.get("PUZZLE_HINTS", "")
    if hint_path and Path(hint_path).exists():
        hints = Path(hint_path).read_text(encoding="utf-8")

    print(f"mode={mode} inventory={len(inv)} puzzles={len(puzzles)} "
          f"seed={args.seed} hints={'yes' if hints else 'no'}")
    if args.dry_run:
        for i, funcs in enumerate(puzzles):
            print(f"puzzle_{i:02d}: {[f['name'] for f in funcs]}")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    run_root = TESTBED / "outputs" / f"{args.tag}_{mode}_{stamp}"
    run_root.mkdir(parents=True, exist_ok=True)
    log = ErrorLog(cfg.error_log)
    run_id = new_run_id()

    results = []
    for i, funcs in enumerate(puzzles):
        pid = f"puzzle_{i:02d}"
        names = [f["name"] for f in funcs]
        pdir = run_root / pid
        pdir.mkdir(parents=True, exist_ok=True)
        raw = invoke_text(cfg.model_for_role("audience"),
                          *compose_prompt(funcs, hints, mode))
        code = extract_code(raw)
        r = run_code(code, pdir)
        called = [n for n in names if re.search(rf"\b{n}\s*\(", code)]
        ok = r["exit"] == 0 and len(called) == len(names)
        if not ok:
            log.append(run_id=run_id, step="puzzle", language="Python",
                       task=pid, status="fail",
                       function=(set(names) - set(called) or {names[0]}).pop(),
                       error=(r["stderr"].splitlines() or ["functions not all called"])[-1][:200],
                       root_cause=r["stderr"][-300:], suggested_fix_code="")
        results.append({"puzzle": pid, "functions": names, "called": called,
                        "exit": r["exit"], "pass": ok})
        print(f"{pid} {names} -> {'PASS' if ok else 'FAIL'}")

    passed = sum(1 for r in results if r["pass"])
    report = {"tag": args.tag, "mode": mode, "seed": args.seed,
              "readiness_score": round(passed / len(results), 3),
              "passed": passed, "total": len(results),
              "hints_used": bool(hints), "results": results}
    (run_root / "puzzle_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in
                      ("mode", "readiness_score", "passed", "total", "hints_used")}))
    print(f"report: {run_root / 'puzzle_report.json'}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
