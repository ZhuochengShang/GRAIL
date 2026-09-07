#!/usr/bin/env python3
"""Fail-closed validation for the corrected complete tslearn surface."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from aideal.config import load_config
from aideal.profile import load_profile, missing_fields
from aideal.readme_agent import parse_readme, public_api_details, public_api_surface


EXPECTED_SOURCE = "f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7"
EXPECTED_MANIFEST_SHA = "42dd31265d4fd753eab37f00ea636b5e06bdd2b2203e48be45dc0be6569b967f"
EXPECTED_ORDERED_SHA = "f32b60b9ce1415415e60f7ff285bde2efb0f62a6e0aaf33622590486fd8bf907"
EXPECTED_FIXTURE_SHA = "0de0b7fa727cfabaf8481552db2b95fcccd12e54b67058aea79ff05b483cf807"
EXPECTED_SCAFFOLD_SHA = "45d3de8bc5de86ea8814fa9350e2695f06945a6bcae6b23528feef97dd2f1c99"
CONDITIONS = ("A1", "A2", "B1", "B2")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(name: str) -> str:
    return name.split("[", 1)[0].strip("` ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=CONDITIONS)
    parser.add_argument("--require-readme", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    manifest_path = root / "docs/eval/api_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_names = manifest.get("apis") or []
    problems: list[str] = []
    checks: dict = {}

    if sha(manifest_path) != EXPECTED_MANIFEST_SHA:
        problems.append("manifest file hash differs from the frozen value")
    ordered_sha = hashlib.sha256("\n".join(manifest_names).encode()).hexdigest()
    if ordered_sha != EXPECTED_ORDERED_SHA:
        problems.append("ordered manifest-name hash differs")
    if len(manifest_names) != 235 or len(set(manifest_names)) != 235:
        problems.append("manifest must contain 235 unique names")

    source = root / "tslearn"
    proc = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"],
                          text=True, capture_output=True, check=False)
    source_commit = proc.stdout.strip()
    if proc.returncode or source_commit != EXPECTED_SOURCE:
        problems.append(f"source commit is {source_commit or 'unavailable'}")

    fixture = source / "tslearn/.cached_datasets/Trace.npz"
    if not fixture.is_file() or sha(fixture) != EXPECTED_FIXTURE_SHA:
        problems.append("Trace fixture missing or hash differs")

    scaffold = root / "docs/api_test_scaffold_full235.py"
    try:
        ast.parse(scaffold.read_text(encoding="utf-8"))
    except Exception as exc:
        problems.append(f"shared scaffold does not parse: {exc}")
    if not scaffold.is_file() or sha(scaffold) != EXPECTED_SCAFFOLD_SHA:
        problems.append("shared scaffold hash differs")

    tags = (args.condition,) if args.condition else CONDITIONS
    path_tuples = set()
    for tag in tags:
        cfg_path = root / f"configs/aideal_{tag}_full235.yaml"
        cfg = load_config(cfg_path)
        raw_names = sorted(public_api_surface(cfg, override_filter="all"))
        details = [row for row in public_api_details(cfg)
                   if row.get("visibility") == "public"]
        ex = cfg.comprehension.get("execute") or {}
        if raw_names != manifest_names:
            problems.append(f"{tag}: discovery differs from frozen manifest")
        if len(details) != 343:
            problems.append(f"{tag}: expected 343 definition sites, got {len(details)}")
        if cfg.surface_filter != "all":
            problems.append(f"{tag}: surface_filter is not all")
        if missing_fields(load_profile(cfg)):
            problems.append(f"{tag}: project profile is incomplete")
        if ex.get("scaffold") != "docs/api_test_scaffold_full235.py":
            problems.append(f"{tag}: does not use the shared scaffold")
        expected_work = f".aideal_exec/{tag}"
        expected_output = f".aideal_exec/{tag}/output"
        expected_log = (root / f"logs/eval/{tag}/error_log.jsonl").resolve()
        if ex.get("work_dir") != expected_work or ex.get("output_dir") != expected_output:
            problems.append(f"{tag}: work/output directory is not isolated")
        if cfg.error_log != expected_log:
            problems.append(f"{tag}: error log is not isolated")
        path_tuples.add((str(cfg.llm_readme), str(cfg.error_log),
                         ex.get("work_dir"), ex.get("output_dir")))
        if args.require_readme:
            if not cfg.llm_readme.is_file():
                problems.append(f"{tag}: generated/repaired README is missing")
            else:
                doc_names = [normalize(entry.name) for entry in parse_readme(cfg.llm_readme)]
                if len(doc_names) != 235 or set(doc_names) != set(manifest_names):
                    problems.append(
                        f"{tag}: README names differ: entries={len(doc_names)}, "
                        f"unique={len(set(doc_names))}")
        checks[tag] = {
            "config": str(cfg_path), "raw_names": len(raw_names),
            "definition_sites": len(details), "work_dir": ex.get("work_dir"),
            "output_dir": ex.get("output_dir"), "llm_readme": str(cfg.llm_readme),
        }
    if not args.condition and len(path_tuples) != 4:
        problems.append("condition state paths are not all unique")

    result = {
        "valid": not problems,
        "surface_names": len(manifest_names),
        "definition_sites": 343,
        "manifest_sha256": sha(manifest_path),
        "ordered_names_sha256": ordered_sha,
        "source_commit": source_commit,
        "checks": checks,
        "problems": problems,
    }
    print(json.dumps(result, indent=2))
    return 0 if not problems else 2


if __name__ == "__main__":
    sys.exit(main())
