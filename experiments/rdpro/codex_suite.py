#!/usr/bin/env python3
"""Codex experiment suite — g1/g4 using OpenAI Responses/Codex models.

Stages mirror `gemini_suite.py`, but use `--role audience=codex:$BENCH_CODEX_MODEL`.

  g1_codex_flat    ONE LARGE README: flat LLM_readme.md entries, class_context
                   off, fix rounds 3.
  g4_codex_fixall  FIX-ALL: --rerun-failed picks every function whose most
                   recent error_log outcome is fail and lets the same Codex
                   model fix with --max-fix-rounds N.

Env:
  OPENAI_API_KEY required.
  BENCH_CODEX_MODEL defaults to gpt-5.3-codex.
  BENCH_G4_ROUNDS defaults to 15; set 99 for the literal fix-as-much-as-possible run.

Usage:
  python codex_suite.py --dry-run --stages g1,g4
  caffeinate -i python codex_suite.py --stages g1,g4
  python bench_conditions.py --table
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "bench"
CODEX = os.environ.get("BENCH_CODEX_MODEL", "gpt-5.3-codex")
AIDEAL = os.environ.get("AIDEAL_BIN") or shutil.which("aideal") or str(Path(sys.executable).with_name("aideal"))
ROLE = ["--role", f"audience=codex:{CODEX}"]
BASE = [AIDEAL, "comprehension", "--execute", "--timeout", "300", *ROLE]

STAGES: dict[str, list[str]] = {
    "g1": [*BASE, "--max-fix-rounds", "3"],
    "g4": [*BASE, "--rerun-failed", "--max-fix-rounds",
           os.environ.get("BENCH_G4_ROUNDS", "15")],
}

_MODEL_TAG = re.sub(r"[^A-Za-z0-9.]+", "-", CODEX)
NAMES = {
    "g1": f"g1_codex_flat.{_MODEL_TAG}",
    "g4": f"g4_codex_fixall.{_MODEL_TAG}",
}


def preflight() -> None:
    sys.path.insert(0, str(HERE.parents[1] / "grail-agent" / "src"))
    from aideal.config import ModelSpec
    from aideal.llm import invoke_text

    out = invoke_text(ModelSpec(provider="codex", model=CODEX),
                      "Reply with exactly: OK", "ping")
    print(f"preflight codex:{CODEX} -> {out.strip()[:20]!r}", file=sys.stderr)


def clean_exec_out() -> None:
    exec_out = HERE / "exec_out"
    if not exec_out.exists():
        return
    for child in exec_out.iterdir():
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink(missing_ok=True)


def run(stage: str, dry: bool) -> None:
    cmd = STAGES[stage]
    if dry:
        print(f"{NAMES[stage]:24} {' '.join(cmd)}")
        return
    clean_exec_out()
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{time.strftime('%Y%m%d_%H%M%S')}_{NAMES[stage]}.json"
    print(f"[{NAMES[stage]}] {' '.join(cmd)}", file=sys.stderr)
    proc = subprocess.run(cmd, cwd=HERE, stdout=subprocess.PIPE, text=True)
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        dest.with_suffix(".raw.txt").write_text(proc.stdout or "")
        print(f"[{NAMES[stage]}] non-JSON output saved (rc={proc.returncode})", file=sys.stderr)
        return
    payload["_condition"] = NAMES[stage]
    payload["_cmd"] = " ".join(cmd)
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    metrics = payload.get("metrics", {})
    ok = sum(1 for v in metrics.values() if v.get("status") == "pass")
    print(f"[{NAMES[stage]}] {ok}/{len(metrics)} pass -> {dest.name}", file=sys.stderr)
    if stage == "g4":
        rows = list(metrics.values())
        fixed = [r for r in rows if r.get("status") == "pass"]
        print("\n== g4 FIX-ALL SUMMARY (Codex) ==")
        print(f"failures attempted : {len(rows)}")
        print(f"fixed              : {len(fixed)} ({len(fixed)/len(rows):.1%})" if rows else "-")
        print(f"total fix rounds   : {sum(r.get('attempts', 0) for r in rows)}")
        print(f"tokens             : in={sum(r.get('input_tokens', 0) for r in rows)} "
              f"out={sum(r.get('output_tokens', 0) for r in rows)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stages", default="g1", help="comma list from: g1,g4")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    stages = [s.strip() for s in args.stages.split(",")]
    for s in stages:
        if s not in STAGES:
            print(f"unknown stage '{s}' (have: g1,g4)")
            return 2
    if args.dry_run:
        for s in stages:
            run(s, dry=True)
        return 0
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set")
        return 2
    preflight()
    for s in stages:
        run(s, dry=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
