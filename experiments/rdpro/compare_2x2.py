#!/usr/bin/env python3
"""2x2 doc-effect table (Zoe's design, corrected 2026-07-13 per review):

            | 0 fix rounds (pass-or-not) | after 5-round deep-dive doc repair |
  original  | A1                         | B1                                 |
  generated | A2                         | B2                                 |

ALL FOUR cells are FINAL FULL comprehension runs (`--execute --full-doc on
--max-fix-rounds 0 --manifest <frozen>`): B-cells are fresh evaluations
against the repaired document, NOT a union of A-passes with per-API docfix
recoveries (every repair changes the shared full-document context, so only a
rerun is valid). The script refuses runs whose manifests/denominators differ.

Usage:
  python compare_2x2.py --a1 A1.json --a2 A2.json --b1 B1.json --b2 B2.json \
                        [-o docs/compare_2x2.md]
"""
import argparse
import json
from pathlib import Path


def load_run(p):
    d = json.loads(Path(p).read_text())
    m = {k: v for k, v in (d.get("metrics") or {}).items() if isinstance(v, dict)}
    run = d.get("run") or {}
    return {"path": str(p), "n": len(m),
            "names": set(m),
            "passed": {k for k, v in m.items() if v.get("status") == "pass"},
            "infra": {k for k, v in m.items()
                      if (v.get("error_category") or "") == "infra"},
            "full_doc": run.get("full_doc"), "doc_chars": run.get("doc_chars"),
            "manifest": run.get("manifest"),
            "max_fix_rounds": run.get("max_fix_rounds")}


def cell(run):
    n, p = run["n"], run["passed"]
    scored_n = n - len(run["infra"] - p)
    return {"pass": len(p), "n": n, "scored_n": scored_n,
            "pct": 100.0 * len(p) / n if n else 0.0,
            "spct": 100.0 * len(p) / scored_n if scored_n else 0.0,
            "set": p}


def fmt(c):
    return f"{c['pass']}/{c['n']} ({c['pct']:.1f}% raw · {c['spct']:.1f}% scored)"


def check_design(runs):
    """Guard the experiment invariants: one denominator, full-doc on,
    zero snippet-fix rounds — refuse to print a table over unlike cells."""
    problems = []
    names = [r["names"] for r in runs.values()]
    if any(nm != names[0] for nm in names[1:]):
        for a in runs:
            for b in runs:
                d = runs[a]["names"] ^ runs[b]["names"]
                if d:
                    problems.append(f"{a} vs {b}: {len(d)} differing APIs "
                                    f"(e.g. {sorted(d)[:5]})")
                    break
    for tag, r in runs.items():
        if r["full_doc"] is False:
            problems.append(f"{tag}: full_doc was OFF (audience did not get the entire doc)")
        if r["max_fix_rounds"] not in (0, None):
            problems.append(f"{tag}: max_fix_rounds={r['max_fix_rounds']} (must be 0)")
    return problems


def main():
    ap = argparse.ArgumentParser()
    for tag, hint in (("a1", "original doc, 0 rounds"),
                      ("a2", "generated doc, 0 rounds"),
                      ("b1", "FINAL rerun after doc repair, original arm (--doc original+aideal)"),
                      ("b2", "FINAL rerun after doc repair, generated arm")):
        ap.add_argument(f"--{tag}", required=True, help=f"comprehension run JSON: {hint}")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--force", action="store_true",
                    help="print the table even if design invariants fail")
    a = ap.parse_args()

    runs = {t: load_run(getattr(a, t)) for t in ("a1", "a2", "b1", "b2")}
    problems = check_design(runs)
    if problems and not a.force:
        print("DESIGN INVARIANTS VIOLATED — not a valid 2x2 (use --force to override):")
        for pr in problems:
            print(f"  - {pr}")
        raise SystemExit(2)

    A1, A2, B1, B2 = (cell(runs[t]) for t in ("a1", "a2", "b1", "b2"))
    L = ["# 2x2 doc-effect table", ""]
    if problems:
        L += ["**WARNING (--force): invariants violated:** "
              + "; ".join(problems), ""]
    dc = {t: runs[t]["doc_chars"] for t in runs}
    L += [f"_All cells: full-document audience context, 0 snippet-fix rounds, "
          f"frozen manifest ({runs['a1']['n']} APIs). Doc sizes (chars): "
          f"A1={dc['a1']:,} · A2={dc['a2']:,} · B1={dc['b1']:,} · B2={dc['b2']:,}_", "",
          "| doc \\\\ fix | 0 rounds | after deep-dive doc repair |",
          "|---|---|---|",
          f"| **original** | {fmt(A1)} | {fmt(B1)} |",
          f"| **generated** | {fmt(A2)} | {fmt(B2)} |",
          "", "## Effects (scored pp)", "",
          f"- **Generation effect (A2−A1):** {A2['spct'] - A1['spct']:+.1f} — authoring the doc, cold.",
          f"- **Repair effect on ORIGINAL (B1−A1):** {B1['spct'] - A1['spct']:+.1f} — bootstrapping entries from failures alone.",
          f"- **Repair effect on GENERATED (B2−A2):** {B2['spct'] - A2['spct']:+.1f} — repair on top of an authored doc.",
          f"- **Best vs floor (B2−A1):** {B2['spct'] - A1['spct']:+.1f} total.",
          f"- **Interaction:** repair helps "
          f"{'GENERATED more' if (B2['spct'] - A2['spct']) > (B1['spct'] - A1['spct']) else 'ORIGINAL more'} "
          f"({B2['spct'] - A2['spct']:+.1f} vs {B1['spct'] - A1['spct']:+.1f}).", ""]
    only_b2 = sorted(B2["set"] - B1["set"])
    only_b1 = sorted(B1["set"] - B2["set"])
    L += [f"APIs passing only in the generated column ({len(only_b2)}): "
          + ", ".join(f"`{x}`" for x in only_b2[:20]),
          f"APIs passing only in the original column ({len(only_b1)}): "
          + ", ".join(f"`{x}`" for x in only_b1[:20])]
    md = "\n".join(L) + "\n"
    print(md)
    if a.out:
        Path(a.out).write_text(md)
        print(f"[written {a.out}]")


if __name__ == "__main__":
    main()
