#!/usr/bin/env python3
"""Validate and compare MDAnalysis A1/A2/B1/B2 on the frozen full surface."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path


EXCLUDED = {"infra", "llm-error"}
EXPECTED_DOC = {
    "A1": "original",
    "A2": "aideal",
    "B1": "original+aideal",
    "B2": "aideal",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("check") != "comprehension" or not isinstance(value.get("metrics"), dict):
        raise ValueError(f"not a comprehension result: {path}")
    return value


def stable_components(result: dict) -> dict:
    fp = (result.get("run") or {}).get("fingerprint_components") or {}
    return {
        key: fp.get(key) for key in
        ("schema", "project", "language", "manifest_sha256", "models",
         "scaffold", "source", "fixtures", "engine", "interpreter")
    }


def state(metric: dict) -> str:
    if metric.get("status") == "pass":
        return "pass"
    if metric.get("error_category") in EXCLUDED:
        return "excluded"
    return "fail"


def transition(left: str, right: str) -> str:
    if "excluded" in (left, right):
        return "excluded"
    if left == right == "pass":
        return "both-pass"
    if left == right == "fail":
        return "both-fail"
    return "improvement" if left == "fail" else "regression"


def validate(arms: dict[str, dict], manifest: dict) -> list[str]:
    names = manifest.get("apis") or []
    if len(names) != 1032 or manifest.get("public_names") != 1032:
        raise ValueError("full manifest must contain exactly 1,032 public names")
    expected_order = tuple(names)
    first_stable = None
    for arm, result in arms.items():
        run = result.get("run") or {}
        if result.get("doc_source") != EXPECTED_DOC[arm]:
            raise ValueError(f"{arm}: wrong doc source {result.get('doc_source')!r}")
        if tuple(result["metrics"]) != expected_order:
            raise ValueError(f"{arm}: metric order/set differs from frozen manifest")
        if run.get("api_count") != 1032 or run.get("manifest_api_count") != 1032:
            raise ValueError(f"{arm}: incomplete denominator")
        if run.get("manifest_sha256") != manifest.get("comprehension_manifest_sha256"):
            raise ValueError(f"{arm}: manifest hash differs")
        if run.get("max_fix_rounds") != 0 or run.get("doc_scope") != "relevant":
            raise ValueError(f"{arm}: final result is not relevant-scope zero-round")
        if result.get("sample_data_warnings"):
            raise ValueError(f"{arm}: sample-data warnings present")
        stable = stable_components(result)
        if first_stable is None:
            first_stable = stable
        elif stable != first_stable:
            raise ValueError(f"{arm}: source/fixture/model/engine environment drift")
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    for arm in EXPECTED_DOC:
        parser.add_argument(f"--{arm.lower()}", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    arms = {arm: load(getattr(args, arm.lower())) for arm in EXPECTED_DOC}
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    names = validate(arms, manifest)

    pairs = (("A1", "A2"), ("A1", "B1"), ("A2", "B2"), ("B1", "B2"))
    rows = []
    for name in names:
        row = {"api": name}
        for arm, result in arms.items():
            metric = result["metrics"][name]
            row[f"{arm}_state"] = state(metric)
            row[f"{arm}_category"] = str(metric.get("error_category") or "")
        for left, right in pairs:
            row[f"{left}_to_{right}"] = transition(
                row[f"{left}_state"], row[f"{right}_state"]
            )
        rows.append(row)

    out = args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / "per_api_transitions.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "manifest_sha256": manifest["comprehension_manifest_sha256"],
        "apis": len(names),
        "arms": {
            arm: dict(Counter(state(m) for m in result["metrics"].values()))
            for arm, result in arms.items()
        },
        "transitions": {
            f"{left}_to_{right}": dict(Counter(
                row[f"{left}_to_{right}"] for row in rows
            )) for left, right in pairs
        },
    }
    (out / "comparison.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# MDAnalysis full-surface A1/A2/B1/B2 comparison", "",
        f"Frozen denominator: **{len(names)}** public API names.", "",
        "## Arms", "",
        "| Arm | Pass | Fail | Excluded infra/provider |",
        "|---|---:|---:|---:|",
    ]
    for arm in EXPECTED_DOC:
        counts = Counter(state(m) for m in arms[arm]["metrics"].values())
        lines.append(f"| {arm} | {counts['pass']} | {counts['fail']} | {counts['excluded']} |")
    for left, right in pairs:
        counts = summary["transitions"][f"{left}_to_{right}"]
        lines.extend([
            "", f"## {left} → {right}", "",
            f"- Fail→pass: {counts.get('improvement', 0)}",
            f"- Pass→fail: {counts.get('regression', 0)}",
            f"- Both pass: {counts.get('both-pass', 0)}",
            f"- Both fail: {counts.get('both-fail', 0)}",
            f"- Excluded: {counts.get('excluded', 0)}",
        ])
    (out / "COMPARISON.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
