#!/usr/bin/env python3
"""Gemini experiment suite — all stages run Gemini as the coding model.

Stages (run in this order; each = one `aideal comprehension --execute` process,
results land in results/bench/<ts>_<stage>.json, aggregate with
`python bench_conditions.py --table`):

  g1_gemini_flat   ONE LARGE README: flat LLM_readme.md entries, class_context
                   off, fix rounds 3 — Gemini's counterpart of the gpt-4o
                   baseline (60-64/218).
  g2_gemini_index  WITH CATALOG/INDEX: --class-context on — each API's entry is
                   prefixed with its catalogue class header (receiver + a
                   verified sibling call pattern from docs/api + readme index).
  g3_gemini_dedup  OPTIONAL, REDUNDANCY-REMOVED: same as g1 but AFTER
                   `aideal readme --generate --force` regenerated the catalog
                   from the deduped 205-name surface (203 entries). The suite
                   refuses to run g3 while the on-disk catalog still has the
                   old 218 entries. (Regen uses the author model -> needs
                   OPENAI_API_KEY once.)
  g4_gemini_fixall FIX-ALL: --rerun-failed picks every function whose
                   MOST-RECENT error_log outcome is fail (i.e. the failures of
                   whichever stage you ran last) and lets Gemini fix with
                   --max-fix-rounds 99. Reports: how many got fixed, total fix
                   rounds, tokens spent — per API and total.

Env:  GOOGLE_API_KEY (required)
      BENCH_GEMINI_MODEL (default gemini-2.5-pro — set to an id from
      `python bench_check.py --list`)
Usage:
  python gemini_suite.py --stages g1                 # one stage
  python gemini_suite.py --stages g1,g4              # flat run, then fix-all on its failures
  python gemini_suite.py --stages g2,g4
  python gemini_suite.py --stages g3 --allow-regen-check-skip   # only if you know why
  python gemini_suite.py --dry-run --stages g1,g2,g3,g4
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
GEMINI = os.environ.get("BENCH_GEMINI_MODEL", "gemini-2.5-pro")
AIDEAL = os.environ.get("AIDEAL_BIN") or shutil.which("aideal") or str(Path(sys.executable).with_name("aideal"))
ROLE = ["--role", f"audience=google:{GEMINI}"]   # fixer falls back to audience -> Gemini fixes too
BASE = [AIDEAL, "comprehension", "--execute", "--timeout", "300", *ROLE]

STAGES: dict[str, list[str]] = {
    "g1": [*BASE, "--max-fix-rounds", "3"],
    "g2": [*BASE, "--max-fix-rounds", "3", "--class-context", "on"],
    "g3": [*BASE, "--max-fix-rounds", "3"],                    # + regen gate below
    # g4 cap: evidence from the 2026-07-07 run — every fixable API fixed in
    # ≤12 rounds; unfixable ones repeated one error to the 100-round cap
    # (addTile: 368K output tokens). The in-loop STUCK detector (3 identical
    # errors -> stop) now ends those early; the cap is a backstop.
    # Override: BENCH_G4_ROUNDS=99 for the literal "no matter how many rounds".
    "g4": [*BASE, "--rerun-failed", "--max-fix-rounds",
           os.environ.get("BENCH_G4_ROUNDS", "15")],
}
_MODEL_TAG = re.sub(r"[^A-Za-z0-9.]+", "-", GEMINI)   # results keyed per model:
NAMES = {k: f"{v}.{_MODEL_TAG}" for k, v in {       # pro and flash runs coexist
    "g1": "g1_gemini_flat", "g2": "g2_gemini_index",
    "g3": "g3_gemini_dedup", "g4": "g4_gemini_fixall"}.items()}


def catalog_entries() -> int:
    txt = (HERE / "docs" / "LLM_readme.md").read_text(encoding="utf-8", errors="ignore")
    return len(re.findall(r"^## API Test:", txt, re.M))


def preflight() -> None:
    """One tiny Gemini call through the SAME path the harness uses — abort the
    whole suite on a bad key/model instead of burning 218 llm-error rows."""
    sys.path.insert(0, str(HERE.parents[1] / "grail-agent" / "src"))
    from aideal.config import ModelSpec
    from aideal.llm import invoke_text
    out = invoke_text(ModelSpec(provider="google", model=GEMINI),
                      "Reply with exactly: OK", "ping")
    print(f"preflight google:{GEMINI} -> {out.strip()[:20]!r}", file=sys.stderr)


def run(stage: str, dry: bool) -> None:
    cmd = STAGES[stage]
    if dry:
        print(f"{NAMES[stage]:18} {' '.join(cmd)}")
        return
    if stage == "g3":
        n = catalog_entries()
        if n > 210:   # old pre-dedup catalog has 218; regenerated one ~203
            print(f"[g3] REFUSING: catalog on disk has {n} entries (pre-dedup). "
                  f"Run `aideal readme --generate --force` first (needs OPENAI_API_KEY), "
                  f"then rerun g3.", file=sys.stderr)
            return
    # stale writer temp dirs (exec_out/output.tif/temp/...) fail
    # saveAsGeoTiff-style APIs with "Directory not empty" — env noise, not doc
    # quality. Clean the snippet-output scratch before every stage.
    exec_out = HERE / "exec_out"
    if exec_out.exists():
        for child in exec_out.iterdir():
            shutil.rmtree(child, ignore_errors=True) if child.is_dir() else child.unlink(missing_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    dest = OUT / f"{ts}_{NAMES[stage]}.json"
    print(f"[{NAMES[stage]}] {' '.join(cmd)}", file=sys.stderr)
    # stdout (final JSON) captured; stderr INHERITED so the per-API
    # `[api] round N: PASS/FAIL` progress streams live to your terminal.
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
    m = payload.get("metrics", {})
    ok = sum(1 for v in m.values() if v["status"] == "pass")
    print(f"[{NAMES[stage]}] {ok}/{len(m)} pass -> {dest.name}", file=sys.stderr)
    if stage == "g4":
        rows = list(m.values())
        fixed = [r for r in rows if r["status"] == "pass"]
        print("\n== g4 FIX-ALL SUMMARY (Gemini, rounds cap 99) ==")
        print(f"failures attempted : {len(rows)}")
        print(f"fixed              : {len(fixed)} ({len(fixed)/len(rows):.1%})" if rows else "-")
        print(f"total fix rounds   : {sum(r['attempts'] for r in rows)}")
        if fixed:
            att = sorted(r["attempts"] for r in fixed)
            print(f"rounds to fix      : mean {sum(att)/len(att):.1f}, median {att[len(att)//2]}, max {att[-1]}")
        print(f"tokens             : in={sum(r['input_tokens'] for r in rows)} "
              f"out={sum(r['output_tokens'] for r in rows)}")
        print(f"still failing      : {sorted(k for k, v in m.items() if v['status'] != 'pass')[:20]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stages", default="g1", help="comma list from: g1,g2,g3,g4 (order respected)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    stages = [s.strip() for s in args.stages.split(",")]
    for s in stages:
        if s not in STAGES:
            print(f"unknown stage '{s}' (have: g1,g2,g3,g4)"); return 2
    if args.dry_run:
        for s in stages:
            run(s, dry=True)
        return 0
    if not os.environ.get("GOOGLE_API_KEY"):
        print("GOOGLE_API_KEY not set"); return 2
    preflight()
    for s in stages:
        run(s, dry=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
