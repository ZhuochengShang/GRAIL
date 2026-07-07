#!/usr/bin/env python3
"""Backend micro-benchmark driver — TODO items 3 + 5 (quantified comparisons).

Conditions (model IDs via env so no code edit per run):
  openai_chat    audience = config default (openai chat-completions), default fix loop
  codex_api      audience = codex:$BENCH_CODEX_MODEL  (OpenAI Responses/Codex endpoint)
  gemini_maxfix  fixer = google:$BENCH_GEMINI_MODEL, --max-fix-rounds 99
                 ("let gemini fix as much as possible, no matter the rounds")
  no_fix         --max-fix-rounds 0  (single-shot baseline: the value of the fix loop)

Each condition runs `aideal comprehension --execute` as ONE clean process; the
per-API metrics block (status, attempts, pass_round, wall_s, provider-reported
tokens, per-model split) is saved to results/bench/<ts>_<condition>.json.

Usage:
  python bench_conditions.py --list
  python bench_conditions.py --dry-run              # print the exact commands
  python bench_conditions.py                        # all conditions, ALL documented APIs
  python bench_conditions.py --only no_fix,gemini_maxfix --sample 10
  python bench_conditions.py --table                # aggregate results/bench/*.json

Env: OPENAI_API_KEY always; GOOGLE_API_KEY for gemini_maxfix;
     BENCH_CODEX_MODEL (default gpt-5.1-codex-max), BENCH_GEMINI_MODEL
     (default gemini-2.5-pro) — set to the model IDs your accounts offer.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "bench"
AIDEAL = os.environ.get("AIDEAL_BIN") or shutil.which("aideal") or str(Path(sys.executable).with_name("aideal"))

CODEX = os.environ.get("BENCH_CODEX_MODEL", "gpt-5.1-codex-max")
GEMINI = os.environ.get("BENCH_GEMINI_MODEL", "gemini-2.5-pro")

CONDITIONS: dict[str, dict] = {
    "openai_chat":   {"args": [], "needs": ["OPENAI_API_KEY"]},
    "codex_api":     {"args": ["--role", f"audience=codex:{CODEX}"],
                      "needs": ["OPENAI_API_KEY"]},
    "gemini_maxfix": {"args": ["--role", f"fixer=google:{GEMINI}",
                               "--max-fix-rounds", "99"],
                      "needs": ["OPENAI_API_KEY", "GOOGLE_API_KEY"]},
    "no_fix":        {"args": ["--max-fix-rounds", "0"],
                      "needs": ["OPENAI_API_KEY"]},
}


def run_condition(name: str, sample: int | None, dry: bool) -> None:
    cond = CONDITIONS[name]
    cmd = [AIDEAL, "comprehension", "--execute", *cond["args"]]
    if sample is not None:
        cmd += ["--sample", str(sample)]
    if dry:
        print(" ".join(cmd))
        return
    missing = [k for k in cond["needs"] if not os.environ.get(k)]
    if missing:
        print(f"[{name}] SKIP — missing env: {', '.join(missing)}", file=sys.stderr)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    dest = OUT / f"{ts}_{name}.json"
    print(f"[{name}] running: {' '.join(cmd)}", file=sys.stderr)
    # stdout (final JSON) captured; stderr INHERITED -> live per-API progress.
    proc = subprocess.run(cmd, cwd=HERE, stdout=subprocess.PIPE, text=True)
    if proc.returncode != 0 and not (proc.stdout or "").strip():
        print(f"[{name}] FAILED rc={proc.returncode} (see progress above)", file=sys.stderr)
        return
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"[{name}] non-JSON output, saving raw", file=sys.stderr)
        dest.with_suffix(".raw.txt").write_text(proc.stdout or "")
        return
    payload["_condition"] = name
    payload["_cmd"] = " ".join(cmd)
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    m = payload.get("metrics", {})
    ok = sum(1 for v in m.values() if v["status"] == "pass")
    print(f"[{name}] done: {ok}/{len(m)} pass -> {dest.name}", file=sys.stderr)


def _agg(rows: list[dict]) -> dict:
    n = len(rows)
    passed = [r for r in rows if r["status"] == "pass"]
    at0 = [r for r in passed if r.get("pass_round") == 0]
    return {
        "n": n,
        "pass_rate": round(len(passed) / n, 3) if n else 0.0,
        "pass_at_round0": round(len(at0) / n, 3) if n else 0.0,
        "mean_attempts": round(sum(r["attempts"] for r in rows) / n, 2) if n else 0.0,
        "mean_attempts_to_pass": round(sum(r["attempts"] for r in passed) / len(passed), 2)
                                 if passed else None,
        "input_tokens": sum(r.get("input_tokens", 0) for r in rows),
        "output_tokens": sum(r.get("output_tokens", 0) for r in rows),
        "wall_s": round(sum(r.get("wall_s", 0) for r in rows), 1),
    }


def _prices() -> dict:
    """Optional $ pricing: results/bench/prices.json maps a model-id SUBSTRING
    to [input_$_per_M, output_$_per_M], e.g.
      {"gpt-4o": [2.5, 10], "gemini-2.5-pro": [1.25, 10], "gemini-2.5-flash": [0.3, 2.5]}
    Fill from the providers' CURRENT pricing pages — not shipped hardcoded so
    the numbers can't silently go stale."""
    p = OUT / "prices.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except Exception:
        return {}


def _cost(by_model: dict, prices: dict) -> float | None:
    if not prices or not by_model:
        return None
    total, matched = 0.0, False
    for mk, mv in by_model.items():
        for sub, (pi, po) in prices.items():
            if sub in mk:
                total += mv["input_tokens"] / 1e6 * pi + mv["output_tokens"] / 1e6 * po
                matched = True
                break
    return round(total, 2) if matched else None


def table() -> None:
    files = sorted(OUT.glob("*_*.json"))
    if not files:
        print(f"no results in {OUT} — run conditions first")
        return
    prices = _prices()
    # keep the LATEST file per condition
    latest: dict[str, Path] = {}
    for f in files:
        cond = "_".join(f.stem.split("_")[2:])
        latest[cond] = f
    hdr = ("condition", "n", "pass", "pass@0", "att/api", "att/pass",
           "tok_in", "tok_out", "wall_s", "cost$", "audience", "fixer", "max_fix")
    print(("%-34s %4s %6s %7s %8s %9s %9s %8s %8s %6s  %-24s %-24s %s") % hdr)
    for cond, f in sorted(latest.items()):
        d = json.loads(f.read_text())
        rows = list(d.get("metrics", {}).values())
        a = _agg(rows)
        run = d.get("run", {})
        models = run.get("models", {})
        cost = _cost((run.get("usage", {}) or {}).get("by_model", {}), prices)
        print("%-34s %4d %6.3f %7.3f %8.2f %9s %9d %8d %8.1f %6s  %-24s %-24s %s" % (
            cond, a["n"], a["pass_rate"], a["pass_at_round0"], a["mean_attempts"],
            a["mean_attempts_to_pass"] if a["mean_attempts_to_pass"] is not None else "-",
            a["input_tokens"], a["output_tokens"], a["wall_s"],
            cost if cost is not None else "-",
            models.get("audience", "?"), models.get("fixer", "?"),
            run.get("max_fix_rounds", "?")))
    if not prices:
        print("\n(no $ column: create results/bench/prices.json — see _prices() docstring "
              "for the format; fill rates from the providers' current pricing pages)")
    print("\nper-model token split (latest run per condition):")
    for cond, f in sorted(latest.items()):
        d = json.loads(f.read_text())
        bym = (d.get("run", {}).get("usage", {}) or {}).get("by_model", {})
        for mk, mv in bym.items():
            print("  %-14s %-34s calls=%-4d in=%-8d out=%d" % (
                cond, mk, mv["calls"], mv["input_tokens"], mv["output_tokens"]))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default=None, help="comma-separated condition names")
    ap.add_argument("--sample", type=int, default=None,
                    help="APIs per condition (default: ALL documented APIs)")
    ap.add_argument("--dry-run", action="store_true", help="print commands, don't run")
    ap.add_argument("--list", action="store_true", help="list conditions")
    ap.add_argument("--table", action="store_true", help="aggregate saved results")
    args = ap.parse_args()
    if args.list:
        for k, v in CONDITIONS.items():
            print(f"{k:14} aideal comprehension --execute {' '.join(v['args'])}")
        return 0
    if args.table:
        table()
        return 0
    names = (args.only.split(",") if args.only else list(CONDITIONS))
    for name in names:
        if name.strip() not in CONDITIONS:
            print(f"unknown condition '{name}' (have: {', '.join(CONDITIONS)})", file=sys.stderr)
            return 2
    for name in names:
        run_condition(name.strip(), args.sample, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
