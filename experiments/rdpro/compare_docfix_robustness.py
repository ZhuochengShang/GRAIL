#!/usr/bin/env python3
"""Doc-repair ROBUSTNESS: rerun g1 on the fixed catalog, compare vs pre-docfix.

The persistence claim: an entry the doc-repair loop fixed should let a FRESH
full-surface run write passing code — not just pass once at retry. This diffs
a PRE-docfix comprehension run against a POST-docfix one on the SAME surface +
SAME audience model, and reports:
  - overall pass-rate delta,
  - for the doc-fixed APIs specifically: did they now pass on the clean run?
  - REGRESSIONS: APIs that passed before but fail now (a repair must never
    break a sibling — this is our PASS_TO_PASS gate),
  - GAINS beyond the fixed set (docs helping APIs that weren't even targeted).

Usage:
  python compare_docfix_robustness.py \
      --pre  results/bench/20260707_125142_g1_codex_flat.gpt-5.3-codex.json \
      --post docs/comprehension_run.post_docfix.json \
      --docfix docs/docfix_gemini_3_1_pro_from_g1.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def passset(path: str) -> tuple[dict, set, set]:
    m = json.loads(Path(path).read_text()).get("metrics", {})
    passed = {k for k, v in m.items() if v.get("status") == "pass"}
    failed = {k for k, v in m.items() if v.get("status") != "pass"}
    return m, passed, failed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre", required=True, help="pre-docfix g1 run JSON")
    ap.add_argument("--post", required=True, help="post-docfix g1 run JSON")
    ap.add_argument("--docfix", help="the docfix report (to name the fixed APIs)")
    args = ap.parse_args()

    mpre, pre_pass, pre_fail = passset(args.pre)
    mpost, post_pass, post_fail = passset(args.post)
    common = set(mpre) & set(mpost)

    fixed = set()
    if args.docfix:
        d = json.loads(Path(args.docfix).read_text())
        fixed = {k for k, v in d.get("apis", {}).items()
                 if v.get("status") == "doc-fixed"}

    gained = sorted((post_pass - pre_pass) & common)          # fail->pass
    regressed = sorted((pre_pass - post_pass) & common)        # pass->fail (BAD)
    fixed_now_pass = sorted(a for a in fixed if a in post_pass)
    fixed_still_fail = sorted(a for a in fixed if a in post_fail)

    print("== DOC-REPAIR ROBUSTNESS ==")
    print(f"pre  : {len(pre_pass)}/{len(mpre)} pass   ({args.pre.split('/')[-1]})")
    print(f"post : {len(post_pass)}/{len(mpost)} pass   ({args.post.split('/')[-1]})")
    print(f"delta: {len(post_pass)-len(pre_pass):+d} APIs on {len(common)} shared\n")

    if fixed:
        print(f"doc-fixed APIs that PERSIST on the clean run: "
              f"{len(fixed_now_pass)}/{len(fixed)}")
        print(f"  persisted: {fixed_now_pass}")
        if fixed_still_fail:
            print(f"  DID NOT persist (fixed at retry, fail fresh): {fixed_still_fail}")
        print()
    print(f"GAINS (fail->pass, {len(gained)}): {gained}")
    print(f"REGRESSIONS (pass->fail, {len(regressed)}): "
          f"{regressed or 'NONE — PASS_TO_PASS gate holds'}")
    if regressed:
        print("  ^ investigate: a repaired entry may have misled a sibling")


if __name__ == "__main__":
    main()
