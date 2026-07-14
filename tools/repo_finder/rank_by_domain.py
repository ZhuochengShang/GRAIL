#!/usr/bin/env python3
"""Group run_grail_domains.sh results BY DOMAIN, top N per domain (default 5).

Each result file is Lang_domain.json; the domain is the filename after the
language prefix. A repo found by several domain queries appears under each.
Writes results_grail/RANKED_BY_DOMAIN.md + .csv.
"""
from __future__ import annotations

import csv
import glob
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results_grail")
LANGS = {"Scala", "Python", "Java", "Go", "Rust", "C++", "JavaScript", "TypeScript"}


def main(top: int = 5) -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=top, help="repos per domain (default 5)")
    args = ap.parse_args()

    # domain -> {repo: record}
    by_domain: dict[str, dict[str, dict]] = defaultdict(dict)
    for f in glob.glob(os.path.join(RES, "*.json")):
        base = os.path.basename(f)[:-5]
        if base.upper() in ("RANKED", "RANKED_BY_DOMAIN"):
            continue
        lang, _, domain = base.partition("_")
        if lang not in LANGS:
            continue
        domain = domain.replace("-", " ")
        try:
            rows = json.load(open(f))
        except Exception:
            continue
        for r in rows:
            key = r.get("repo") or r.get("full_name")
            if not key:
                continue
            prev = by_domain[domain].get(key)
            if not prev or r.get("final_score", 0) > prev.get("final_score", 0):
                r = dict(r); r["_lang"] = lang
                by_domain[domain][key] = r

    md = ["# GRAIL candidates grouped BY DOMAIN (top 5 each)", "",
          f"{len(by_domain)} domains with ≥1 candidate. ✓ = R1/R4/R5/R7 quick-gates "
          "green (API 50–3000, tests, active, no blocker).", ""]
    csv_rows = [["domain", "rank", "repo", "language", "stars", "api", "final_score", "ready", "url"]]

    def ready(r):
        api = r.get("public_api_count", 0)
        return (50 <= api <= 3000 and r.get("has_tests") and r.get("source_active"))

    for domain in sorted(by_domain, key=lambda d: -max((x.get("final_score", 0)
                                                        for x in by_domain[d].values()), default=0)):
        repos = sorted(by_domain[domain].values(),
                       key=lambda r: -r.get("final_score", 0))[:args.top]
        md += [f"## {domain}  ({len(by_domain[domain])} found)", "",
               "| # | repo | lang | ★ | APIs | score | ready |",
               "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(repos, 1):
            md.append(f"| {i} | [{r.get('repo','?')}]({r.get('url','')}) | {r.get('_lang','?')} | "
                      f"{r.get('stars','?')} | {r.get('public_api_count','?')} | "
                      f"{r.get('final_score','?')} | {'✓' if ready(r) else '—'} |")
            csv_rows.append([domain, i, r.get("repo"), r.get("_lang"), r.get("stars"),
                             r.get("public_api_count"), r.get("final_score"),
                             "yes" if ready(r) else "no", r.get("url")])
        md.append("")
    open(os.path.join(RES, "RANKED_BY_DOMAIN.md"), "w").write("\n".join(md) + "\n")
    with open(os.path.join(RES, "RANKED_BY_DOMAIN.csv"), "w", newline="") as fh:
        csv.writer(fh).writerows(csv_rows)
    print("\n".join(md))
    print(f"wrote {RES}/RANKED_BY_DOMAIN.md and .csv  ({len(by_domain)} domains)")


if __name__ == "__main__":
    main()
