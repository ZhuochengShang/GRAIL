#!/usr/bin/env python3
"""Merge + rank all run_grail_domains.sh results into one GRAIL candidate table.

Dedups repos across domain queries, ranks by finder final_score, and flags
GRAIL rubric readiness (API surface, tests, docs, no AGENTS.md, active source).
Writes results_grail/RANKED.md + RANKED.csv. No args needed.
"""
from __future__ import annotations

import csv
import glob
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results_grail")


def load() -> dict:
    repos: dict[str, dict] = {}
    where: dict[str, set] = defaultdict(set)
    for f in glob.glob(os.path.join(RES, "*.json")):
        tag = os.path.basename(f)[:-5]           # Lang_domain
        lang, _, domain = tag.partition("_")
        try:
            rows = json.load(open(f))
        except Exception:
            continue
        for r in rows:
            key = r.get("repo") or r.get("full_name")
            if not key:
                continue
            where[key].add(f"{lang}:{domain.replace('-', ' ')}")
            prev = repos.get(key)
            if not prev or r.get("final_score", 0) > prev.get("final_score", 0):
                repos[key] = r
    for k, r in repos.items():
        r["_found_in"] = sorted(where[k])
    return repos


def rubric_flags(r: dict) -> tuple[bool, str]:
    """R1/R4/R5/R7 quick gates from finder fields (R2 stars already filtered,
    R3/R6 need local build + probe). Returns (looks_ready, notes)."""
    api = r.get("public_api_count", 0)
    notes = []
    ok = True
    if not (50 <= api <= 3000):
        ok = False; notes.append(f"API {api} out of 50-3000")
    if not r.get("has_tests"): ok = False; notes.append("no tests")
    if not r.get("has_docs"): notes.append("thin docs")
    if r.get("has_agents"): notes.append("has AGENTS.md (less headroom)")
    if not r.get("source_active"): ok = False; notes.append("stale source")
    return ok, "; ".join(notes) or "all quick-gates green"


def main(top_per_lang: int = 10) -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=top_per_lang,
                    help="candidates to keep PER LANGUAGE (default 10)")
    args = ap.parse_args()

    repos = load()
    if not repos:
        print(f"no results in {RES} — run run_grail_domains.sh first"); return
    by_lang: dict[str, list] = defaultdict(list)
    for r in repos.values():
        by_lang[r.get("language", "?")].append(r)

    md = ["# GRAIL external candidates — top per language, across varied non-geo domains", "",
          f"{len(repos)} unique repos total. Quick-gates = R1/R4/R5/R7 from finder fields; "
          "R3 (builds ≤30 min) + R6 (contamination probe) need local Stage-B/D.", ""]
    csv_rows = [["language", "rank", "repo", "stars", "api", "final_score",
                 "ready", "domain(s)", "url"]]
    # language order = harness cost
    for lang in sorted(by_lang, key=lambda l: {"Scala": 0, "Python": 1, "Java": 2}.get(l, 9)):
        ranked = sorted(by_lang[lang], key=lambda r: -r.get("final_score", 0))[:args.top]
        md += [f"## {lang} — top {len(ranked)}", "",
               "| # | repo | ★ | APIs | score | ready | domain(s) | note |",
               "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(ranked, 1):
            ok, notes = rubric_flags(r)
            doms = ", ".join(d.split(":")[1] for d in r.get("_found_in", []))[:45]
            md.append(f"| {i} | [{r.get('repo','?')}]({r.get('url','')}) | {r.get('stars','?')} | "
                      f"{r.get('public_api_count','?')} | {r.get('final_score','?')} | "
                      f"{'✓' if ok else '—'} | {doms} | {notes[:45]} |")
            csv_rows.append([lang, i, r.get("repo"), r.get("stars"),
                             r.get("public_api_count"), r.get("final_score"),
                             "yes" if ok else "no", doms, r.get("url")])
        md.append("")
    open(os.path.join(RES, "RANKED.md"), "w").write("\n".join(md) + "\n")
    with open(os.path.join(RES, "RANKED.csv"), "w", newline="") as f:
        csv.writer(f).writerows(csv_rows)
    print("\n".join(md))
    print(f"wrote {RES}/RANKED.md and RANKED.csv  ({len(repos)} repos, "
          f"top {args.top}/language)")


if __name__ == "__main__":
    main()
