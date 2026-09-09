#!/usr/bin/env python3
"""Static, no-LLM validation for the MDAnalysis full-surface experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import yaml

from aideal.config import load_config
from aideal.doc_checks import _execute_sample_data, _sha256_files
from aideal.profile import load_profile, missing_fields
from aideal.readme_agent import public_api_details, public_api_surface


PYTHON = "/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python"
SOURCE_COMMIT = "81b8ef51e5bc1aa2824294ac6c52818c74975658"
EXPECTED_NAMES = 1032
EXPECTED_SITES = 1397
CELLS = ("A1", "A2", "B1", "B2")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    repo = args.root.resolve()
    exp = repo / "experiments/mdanalysis"
    source = exp / "mdanalysis"
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(git_head(source) == SOURCE_COMMIT, "pinned source commit mismatch")
    manifest_path = exp / "docs/full_1032/api_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("public_names") == EXPECTED_NAMES, "manifest public_names != 1032")
    require(manifest.get("definition_sites") == EXPECTED_SITES, "manifest sites != 1397")
    names = manifest.get("apis") or []
    require(len(names) == EXPECTED_NAMES and len(names) == len(set(names)),
            "manifest is not 1,032 unique names")
    require(names == sorted(names), "manifest order is not deterministic sorted order")
    newline_sha = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
    require(newline_sha == manifest.get("comprehension_manifest_sha256"),
            "manifest comprehension hash mismatch")
    primary = manifest.get("primary_definition_by_name") or {}
    require(set(primary) == set(names),
            "primary-definition map does not cover exactly the manifest names")

    # The un-suffixed file is a shared YAML layer, not a fifth experimental
    # condition.  Include only the four cell overlays in collision checks so
    # their deliberately distinct work/output directories are tested.
    config_paths = [exp / f"configs/aideal.full1032.{cell}.yaml" for cell in CELLS]
    configs = [load_config(path) for path in config_paths]
    work_dirs, output_dirs = [], []
    for path, cfg in zip(config_paths, configs):
        raw_names = sorted(public_api_surface(cfg, override_filter="all"))
        sites = [row for row in public_api_details(cfg) if row.get("visibility") == "public"]
        require(raw_names == names, f"{path.name}: surface differs from manifest")
        require(len(sites) == EXPECTED_SITES, f"{path.name}: definition-site drift")
        grouped = {}
        for row in sites:
            grouped.setdefault(row["name"], []).append(row)
        for name, rows in grouped.items():
            chosen = max(rows, key=lambda row: (
                len(row.get("params") or []), len(row.get("signature") or ""),
                str(row.get("file", "")), -int(row.get("line", 0))))
            saved = primary.get(name) or {}
            require(saved.get("file") == chosen.get("file")
                    and saved.get("line") == chosen.get("line")
                    and saved.get("parameter_count") == len(chosen.get("params") or []),
                    f"{path.name}: primary signature rule drift for {name}")
        require(cfg.surface_filter == "all", f"{path.name}: surface_filter is not all")
        require("class" in cfg.public_def_regex, f"{path.name}: Python class regex missing")
        execute = cfg.comprehension.get("execute") or {}
        command = execute.get("command", "")
        require("{root}/mdanalysis/.venv/bin/python" in command
                and "{root}/mdanalysis/package" in command,
                f"{path.name}: command not pinned to source/interpreter")
        _, _, warnings = _execute_sample_data(cfg, execute)
        require(not warnings, f"{path.name}: sample warnings: {warnings}")
        work_dirs.append(execute.get("work_dir"))
        output_dirs.append(execute.get("output_dir"))
        require(not missing_fields(load_profile(cfg)), f"{path.name}: incomplete profile")
    require(len(work_dirs) == len(set(work_dirs)), "condition work dirs collide")
    require(len(output_dirs) == len(set(output_dirs)), "condition output dirs collide")

    input_manifest = json.loads((exp / "docs/input_manifest.json").read_text())
    fixture_dir = source / "testsuite/MDAnalysisTests/data"
    fixture_files = sorted(p for p in fixture_dir.rglob("*") if p.is_file())
    require(len(fixture_files) == input_manifest["fixture_directory"]["files"],
            "fixture count mismatch")
    require(sum(p.stat().st_size for p in fixture_files)
            == input_manifest["fixture_directory"]["bytes"], "fixture bytes mismatch")
    for name, record in input_manifest["fixtures"].items():
        path = fixture_dir / name
        require(path.is_file(), f"missing fixture: {name}")
        require(path.stat().st_size == record["bytes"], f"fixture size mismatch: {name}")
        require(sha256(path) == record["sha256"], f"fixture hash mismatch: {name}")

    docs_hash = _sha256_files(configs[0].original_readme_files, configs[0].root)
    require(docs_hash["file_count"] == input_manifest["documentation_files"],
            "original documentation file count mismatch")
    require(docs_hash["sha256"] == input_manifest["documentation_sha256"],
            "original documentation bundle hash mismatch")
    hosted = exp / input_manifest["hosted_document_snapshot"]["path"]
    require(sha256(hosted) == input_manifest["hosted_document_snapshot"]["sha256"],
            "hosted-doc snapshot hash mismatch")

    plan_dir = exp / "docs/full_1032/setup"
    generation = yaml.safe_load((plan_dir / "generation_watchdog.yaml").read_text())
    baseline = yaml.safe_load((plan_dir / "baseline_watchdog.yaml").read_text())
    repair = yaml.safe_load((plan_dir / "repair_watchdog.yaml").read_text())
    require([j["id"] for j in generation["jobs"]]
            == ["mdanalysis_upstream_before", "mdanalysis_A2_generate"],
            "generation plan jobs/dependency order invalid")
    require(generation["jobs"][1].get("depends_on") == ["mdanalysis_upstream_before"],
            "generation must wait for upstream-before")
    require({j["id"] for j in baseline["jobs"]}
            == {"mdanalysis_A1_zero", "mdanalysis_A2_zero"}, "baseline plan cells invalid")
    repair_jobs = {j["id"]: j for j in repair["jobs"]}
    require(set(repair_jobs) == {"mdanalysis_B1_repair", "mdanalysis_B2_repair",
                                 "mdanalysis_B1_zero", "mdanalysis_B2_zero"},
            "repair plan cells invalid")
    b1_command = repair_jobs["mdanalysis_B1_repair"]["command"]
    b2_command = repair_jobs["mdanalysis_B2_repair"]["command"]
    require("--create-missing" in b1_command and "original+aideal" in b1_command,
            "B1 is not explicit original+create-missing")
    require("--create-missing" not in b2_command and "aideal" in b2_command,
            "B2 protocol invalid")
    for job in generation["jobs"] + baseline["jobs"] + repair["jobs"]:
        require(job.get("max_restarts") == 0, f"{job['id']}: not infinitely restartable")
    for cell in ("B1", "B2"):
        zero = repair_jobs[f"mdanalysis_{cell}_zero"]
        command = zero["command"]
        require(command[command.index("--max-fix-rounds") + 1] == "0",
                f"{cell}: final measurement is not zero-round")
        require("--resume" in command, f"{cell}: resume missing")

    for script in (
        "freeze_full_surface.py", "run_pass_to_pass.py", "compare_full_2x2.py",
        "run_full_2x2_pipeline.py", "validate_full_surface_setup.py",
    ):
        path = exp / script
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except SyntaxError as exc:
            errors.append(f"{script}: {exc}")

    result = {
        "valid": not errors,
        "errors": errors,
        "surface": {"public_names": len(names), "definition_sites": EXPECTED_SITES,
                    "manifest_sha256": newline_sha},
        "configs": len(configs),
        "fixtures": len(fixture_files),
        "original_document_files": docs_hash["file_count"],
        "plans": {"generation_jobs": len(generation["jobs"]),
                  "baseline_jobs": len(baseline["jobs"]),
                  "repair_jobs": len(repair["jobs"])},
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
