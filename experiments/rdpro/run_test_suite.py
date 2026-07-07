#!/usr/bin/env python3
"""Batch runner for demo_test_cases.md.

Runs every (or a chosen subset of) test case through demo_agent.run_task(),
and writes ONE output Scala file + ONE JSON result per case, plus a combined
SUMMARY.md table — so every case's generated code and pass/fail status is
inspectable afterward without re-running anything.

demo_test_cases.md stays the single source of truth for case text: this
parses it directly rather than duplicating a hardcoded case list, so the
suite and the doc can never silently drift apart.

Usage (run from experiments/rdpro/, same as demo_agent.py):
    python run_test_suite.py --dry-run                        # offline, no key/cluster
    python run_test_suite.py --execute                        # real LLM + Spark, ALL cases
    python run_test_suite.py --execute --only 1.1,2.1,3.2      # just these case ids
    python run_test_suite.py --execute --group 1               # just Group 1 (1.1, 1.2, 1.3)
    python run_test_suite.py --execute --include-python        # also run the --python cases
    python run_test_suite.py --execute --rounds 2 --show-code

Output layout (default --out-dir results/):
    results/1.1_zonal_mean_min_max.scala   <- generated Scala for that case
    results/1.1_zonal_mean_min_max.json    <- structured result (status, sections, primary_api...)
    results/SUMMARY.md                     <- one table across every case run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from aideal.config import load_config
from demo_agent import run_task

CASE_RE = re.compile(
    r"\*\*(\d+\.\d+)\s*—\s*([^\*]+?)\*\*\s*\n```bash\n(.*?)```",
    re.DOTALL,
)
TEXT_ARG_RE = re.compile(r'--text\s+"([^"]*)"')
PY_CASE_RE = re.compile(
    r"^python demo_agent\.py --execute --python (\S+)(?:\s*#\s*(.*))?$",
    re.MULTILINE,
)


def parse_nl_cases(md_text: str) -> list[dict]:
    """Extract the numbered `**N.N — Title**` / ```bash ... --text "..."``` cases."""
    cases = []
    for m in CASE_RE.finditer(md_text):
        case_id, title, block = m.group(1), m.group(2).strip(), m.group(3)
        tm = TEXT_ARG_RE.search(block)
        if not tm:
            continue
        cases.append({"id": case_id, "title": title, "task": tm.group(1), "kind": "text"})
    return cases


def parse_python_cases(md_text: str) -> list[dict]:
    """Extract the `--python <path>  # comment` lines from the python-script block."""
    cases = []
    for i, m in enumerate(PY_CASE_RE.finditer(md_text), 1):
        path, comment = m.group(1), (m.group(2) or "").strip()
        cases.append({"id": f"py.{i}", "title": comment or Path(path).stem,
                     "python_path": path, "kind": "python"})
    return cases


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:40]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run every demo_test_cases.md case through the demo_agent pipeline")
    ap.add_argument("--cases-md", default="demo_test_cases.md")
    ap.add_argument("--config", default="configs/aideal.yaml")
    ap.add_argument("--out-dir", default="results")
    ap.add_argument("--only", default="", help="comma-separated case ids, e.g. 1.1,2.1")
    ap.add_argument("--group", default="", help="only run cases whose id is N.* (e.g. --group 1)")
    ap.add_argument("--include-python", action="store_true",
                    help="also run the --python cases (needs the referenced scripts to exist)")
    ap.add_argument("--rounds", type=int, default=3, help="max fix attempts per section")
    ap.add_argument("--execute", action="store_true", help="really compile + spark-submit")
    ap.add_argument("--dry-run", action="store_true", help="offline: stub LLM + runner")
    ap.add_argument("--show-code", action="store_true")
    a = ap.parse_args()

    cfg = load_config(a.config)
    md_path = Path(a.cases_md)
    if not md_path.is_absolute():
        md_path = cfg.root / md_path
    md_text = md_path.read_text(encoding="utf-8")

    cases = parse_nl_cases(md_text)
    if a.include_python:
        cases += parse_python_cases(md_text)

    if a.only:
        wanted = {x.strip() for x in a.only.split(",")}
        cases = [c for c in cases if c["id"] in wanted]
    elif a.group:
        cases = [c for c in cases if c["id"] == a.group or c["id"].startswith(a.group + ".")]

    if not cases:
        print(f"[error] no matching cases found in {md_path}", file=sys.stderr)
        return 2

    print(f"[suite] {len(cases)} case(s) parsed from {md_path.name}: "
          f"{', '.join(c['id'] for c in cases)}")

    out_dir = cfg.root / a.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for c in cases:
        case_slug = f"{c['id']}_{slug(c['title'])}"
        print(f"\n{'=' * 70}\nCASE {c['id']} — {c['title']}\n{'=' * 70}")

        if c["kind"] == "python":
            py_path = (cfg.root / c["python_path"]).resolve()
            if not py_path.exists():
                print(f"[skip] python script not found: {py_path}")
                results.append({"id": c["id"], "title": c["title"], "status": "skipped-missing-script"})
                continue
            task = f"Translate this Python workflow to RDPro Scala:\n\n{py_path.read_text(encoding='utf-8')}"
        else:
            task = c["task"]

        scala_out = out_dir / f"{case_slug}.scala"
        try:
            result = run_task(cfg, task, c["id"], scala_out, a.rounds, a.dry_run, a.execute, a.show_code)
        except Exception as e:
            print(f"[error] case {c['id']} raised {type(e).__name__}: {e}")
            result = {"task_id": c["id"], "status": "error", "error": f"{type(e).__name__}: {e}"}
        result["id"] = c["id"]
        result["title"] = c["title"]
        results.append(result)
        (out_dir / f"{case_slug}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    # --- summary table --------------------------------------------------- #
    n_ok = sum(1 for r in results if r.get("status") == "RUNNABLE")
    summary_lines = [
        "# Test suite results", "",
        f"{n_ok}/{len(results)} RUNNABLE"
        + (" (--dry-run, no real compile)" if a.dry_run else "" if a.execute else " (generate-only, no compile)"),
        "",
        "| id | title | status | primary_api | failed_section | scala |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        scala_name = Path(r["scala_path"]).name if r.get("scala_path") else "-"
        summary_lines.append(
            f"| {r.get('id', '?')} | {r.get('title', '')} | {r.get('status', '?')} | "
            f"{r.get('primary_api') or '-'} | {r.get('failed_section') or '-'} | `{scala_name}` |"
        )
    summary_path = out_dir / "SUMMARY.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"\n{'=' * 70}")
    print(f"[suite] {n_ok}/{len(results)} RUNNABLE")
    print(f"[suite] per-case Scala + JSON -> {out_dir}")
    print(f"[suite] summary table         -> {summary_path}")
    return 0 if n_ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
