#!/usr/bin/env python3
"""Create per-function Markdown/CSV/JSON failure evidence from AIDEAL results."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
import json
from pathlib import Path
import re
import sys


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def diagnosis(category: str, error: str) -> str:
    text = error.lower()
    if category == "llm-error":
        return "Transient model-provider, quota, or network failure; retry under the same fingerprint."
    if category == "infra":
        return "Execution environment or optional dependency gap, not documentation quality."
    if category == "timeout":
        return "Generated call exceeded the execution bound; inspect input size and termination behavior."
    if category == "no-correctness-check":
        return "Snippet ran but did not emit the required deterministic correctness witness."
    if re.search(r"cannot find symbol|not found|nameerror|attributeerror|has no attribute", text):
        return "Wrong API owner/import/member name, or a symbol absent from the pinned version."
    if re.search(r"incompatible types|type mismatch|typeerror|cannot be converted", text):
        return "Signature, receiver, argument-type, or return-type mismatch."
    if re.search(r"no such file|filenotfound|does not exist|directory", text):
        return "Missing or incorrectly bound repository fixture/output directory."
    if re.search(r"zero.?division|divide by zero|periodic|box dimensions", text):
        return "Fixture lacks non-degenerate values or periodic-box metadata required by the API."
    if re.search(r"assert|expected|requirement failed|__check__", text):
        return "The call ran, but the generated semantic expectation/correctness assertion was wrong."
    if category == "compile":
        return "Generated code did not compile; inspect signature, ownership, imports, and language version."
    if category == "runtime":
        return "Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics."
    return "Unclassified failure; inspect the captured error, rounds, and source location."


def rows_for(result: dict) -> list[dict]:
    rows = []
    details = result.get("details") or {}
    for name, metric in sorted((result.get("metrics") or {}).items()):
        if metric.get("status") == "pass":
            continue
        detail = details.get(name) or {}
        if not isinstance(detail, dict):
            detail = {}
        rounds = detail.get("rounds") or []
        error = metric.get("error") or detail.get("error") or next((
            row.get("error", "") for row in reversed(rounds)
            if row.get("status") == "fail"), "")
        category = metric.get("error_category") or detail.get("error_category") or next((
            row.get("category", "") for row in reversed(rounds)
            if row.get("status") == "fail"), "unknown")
        frames = metric.get("codebase_frames") or []
        rows.append({
            "function": name,
            "status": metric.get("status", "fail"),
            "category": category,
            "diagnosis": diagnosis(category, error),
            "error": error,
            "locus": metric.get("locus") or "",
            "source": metric.get("source") or "",
            "codebase_frames": "; ".join(frames),
            "attempts": metric.get("attempts"),
            "wall_s": metric.get("wall_s"),
            "llm_calls": metric.get("llm_calls"),
            "input_tokens": metric.get("input_tokens"),
            "output_tokens": metric.get("output_tokens"),
            "rounds": rounds,
            "generated_code": detail.get("code", ""),
            "stdout_tail": detail.get("stdout_tail", ""),
            "stderr_tail": detail.get("stderr_tail", ""),
        })
    return rows


def write_report(result_path: Path, out_dir: Path, label: str) -> dict:
    result = load(result_path)
    rows = rows_for(result)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "failure_details.json"
    csv_path = out_dir / "failure_details.csv"
    md_path = out_dir / "FAILURE_ANALYSIS.md"
    json_path.write_text(json.dumps({
        "source_result": str(result_path),
        "run": result.get("run", {}),
        "failure_count": len(rows),
        "failures": rows,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    fields = ["function", "status", "category", "diagnosis", "error", "locus",
              "source", "codebase_frames", "attempts", "wall_s", "llm_calls",
              "input_tokens", "output_tokens"]
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["category"] for row in rows)
    run = result.get("run") or {}
    lines = [
        f"# {label} failure analysis", "",
        f"- Result: `{result_path}`",
        f"- Experiment fingerprint: `{run.get('experiment_fingerprint', '')}`",
        f"- APIs: {run.get('api_count')}",
        f"- Failures: {len(rows)}", "",
        "## Failure categories", "",
    ]
    lines.extend(f"- `{key}`: {value}" for key, value in sorted(counts.items()))
    lines.extend(["", "## Per-function evidence", ""])
    for row in rows:
        safe_error = str(row["error"]).replace("`", "'")[:1000] or "not captured"
        lines.extend([
            f"### `{row['function']}`", "",
            f"- Category: `{row['category']}`",
            f"- Source definition: `{row['source'] or 'not resolved'}`",
            f"- Reached codebase frames: `{row['codebase_frames'] or 'none'}`",
            f"- Attempts / wall seconds: {row['attempts']} / {row['wall_s']}",
            f"- Diagnosis: {row['diagnosis']}",
            f"- Error: `{safe_error}`",
            "",
        ])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {"label": label, "failures": len(rows), "markdown": str(md_path),
            "csv": str(csv_path), "json": str(json_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--label")
    args = parser.parse_args()
    summary = write_report(args.result.resolve(), args.out_dir.resolve(),
                           args.label or args.result.stem)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
