#!/usr/bin/env python3
"""Conservative, language-aware audit of comprehension PASS snippets.

This is a post-run validator: it never changes raw execution results.  A pass
is auto-verified only when the intended API occurs in executable code, a
non-obviously-vacuous assertion is present, no success fallback is visible,
and any apparent Spark transformation is paired with a terminal action.
Ambiguous receiver names are sent to manual review rather than rejected.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SPARK_TRANSFORMS = re.compile(
    r"\.(?:map|flatMap|filter|join|repartition|partitionBy|mapValues|groupByKey)\s*(?:\{|\()"
)
SPARK_ACTIONS = re.compile(
    r"\.(?:count|collect|take|first|reduce|treeReduce|aggregate|foreach|save\w*)\s*\("
)
ASSERTION = re.compile(r"\b(?:assert|require)\s*\(")
BAD_ASSERTION = re.compile(
    r"\b(?:assert|require)\s*\(\s*false\b|"
    r"insufficient to (?:verify|test)|contract is insufficient",
    re.I,
)
FALLBACK = re.compile(
    r"fallback_failed|no_valid|could_not_verify|unable_to_verify|"
    r"println\s*\([^\n]*(?:fallback|failed)[^\n]*__CHECK__",
    re.I,
)


def _strip_comments(code: str) -> str:
    code = re.sub(r"/\*.*?\*/", " ", code, flags=re.S)
    return re.sub(r"//[^\n]*", " ", code)


def audit(name: str, metric: dict, detail, code_dir: Path | None) -> dict:
    if metric.get("status") != "pass":
        return {"status": "not_pass"}
    code = detail.get("code", "") if isinstance(detail, dict) else ""
    if not code and code_dir:
        p = code_dir / f"run_{name}" / "ApiTest.scala"
        if p.exists():
            code = p.read_text(encoding="utf-8", errors="ignore")
    executable = _strip_comments(code)
    target_called = bool(re.search(rf"(?:\.|\b){re.escape(name)}\s*(?:\(|\b)", executable))
    has_assertion = bool(ASSERTION.search(executable))
    bad_assertion = bool(BAD_ASSERTION.search(executable))
    fallback = bool(FALLBACK.search(executable))
    lazy_without_action = bool(SPARK_TRANSFORMS.search(executable) and
                               not SPARK_ACTIONS.search(executable))
    other_sites = int(metric.get("source_other_sites") or 0)
    owner = Path(str(metric.get("source") or "unknown").split(":", 1)[0]).stem
    owner_explicit = owner != "unknown" and bool(re.search(rf"\b{re.escape(owner)}\b", executable))
    reasons = []
    if not code:
        reasons.append("missing_code")
    if not target_called:
        reasons.append("target_not_called")
    if not has_assertion:
        reasons.append("no_assertion")
    if bad_assertion:
        reasons.append("obviously_invalid_assertion")
    if fallback:
        reasons.append("success_fallback")
    if lazy_without_action:
        reasons.append("lazy_spark_without_action")
    hard = bool(reasons)
    ambiguous = other_sites > 0 and not owner_explicit
    status = "rejected" if hard else "manual_review" if ambiguous else "auto_verified"
    return {
        "status": status,
        "reasons": reasons + (["ambiguous_receiver"] if ambiguous else []),
        "owner": owner,
        "source_other_sites": other_sites,
        "target_called": target_called,
        "has_assertion": has_assertion,
        "spark_action_required": bool(SPARK_TRANSFORMS.search(executable)),
        "spark_action_found": bool(SPARK_ACTIONS.search(executable)),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("result", type=Path)
    ap.add_argument("--code-dir", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--review", type=Path,
                    help="JSON manual-review decisions keyed by API name")
    ap.add_argument("--condition",
                    help="condition key within the manual-review JSON")
    args = ap.parse_args()
    data = json.loads(args.result.read_text(encoding="utf-8"))
    metrics, details = data["metrics"], data.get("details") or {}
    rows = {name: audit(name, metric, details.get(name), args.code_dir)
            for name, metric in metrics.items()}
    if args.review:
        if not args.condition:
            ap.error("--condition is required with --review")
        reviews = json.loads(args.review.read_text(encoding="utf-8"))[args.condition]
        unresolved = sorted(name for name, row in rows.items()
                            if row["status"] == "manual_review" and name not in reviews)
        if unresolved:
            raise ValueError(f"unresolved manual-review APIs: {', '.join(unresolved)}")
        for name, decision in reviews.items():
            if name not in rows or rows[name]["status"] == "not_pass":
                continue
            rows[name]["automatic_status"] = rows[name]["status"]
            rows[name]["status"] = decision["status"]
            rows[name]["review_reason"] = decision["reason"]
    counts = {}
    for row in rows.values():
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    payload = {
        "source_result": str(args.result),
        "raw_apis": len(metrics),
        "raw_passes": sum(m.get("status") == "pass" for m in metrics.values()),
        "audit_counts": counts,
        "apis": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("raw_apis", "raw_passes", "audit_counts")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
