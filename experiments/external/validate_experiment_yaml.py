#!/usr/bin/env python3
"""Static, zero-LLM gate for AIDEAL experiment knowledge and execution YAML."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from aideal.config import load_config
from aideal.doc_checks import _execute_sample_data
from aideal.profile import load_profile, missing_fields, profile_path
from aideal.readme_agent import public_api_details, public_api_surface


CELLS = ("A1", "A2", "B1", "B2")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(source: Path, *args: str) -> str:
    if not (source / ".git").exists():
        return ""
    proc = subprocess.run(
        ["git", "-C", str(source), *args], text=True,
        capture_output=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def validate(repo_root: Path, minimum: int, maximum: int) -> dict:
    base_path = repo_root / "configs/aideal.yaml"
    result = {"repository_root": str(repo_root), "errors": [], "warnings": []}
    if not base_path.exists():
        result["errors"].append(f"missing {base_path}")
        return result

    base = load_config(base_path)
    profile = load_profile(base)
    missing = missing_fields(profile)
    if missing:
        result["errors"].append(f"incomplete project profile: {missing}")
    if profile.get("project", {}).get("name") != base.project_name:
        result["errors"].append("profile project.name differs from effective config")
    if str(profile.get("project", {}).get("language", "")).lower() != base.language.lower():
        result["errors"].append("profile project.language differs from effective config")
    if not profile.get("role"):
        result["warnings"].append("profile role is empty")

    details = public_api_details(base)
    surface = sorted(public_api_surface(base))
    raw_names = sorted({row["name"] for row in details if row.get("visibility") == "public"})
    source_files = sorted({row["file"] for row in details})
    test_files = sorted({path for pattern in base.test_globs
                         for path in glob.glob(str(base.root / pattern), recursive=True)
                         if Path(path).is_file()})
    result.update({
        "project": base.project_name,
        "language": base.language,
        "profile": str(profile_path(base)),
        "profile_sha256": sha256(profile_path(base)) if profile_path(base).exists() else "",
        "domain": profile.get("domain", ""),
        "surface_filter": base.surface_filter,
        "surface_names": len(surface),
        "raw_public_names": len(raw_names),
        "definition_sites": len(details),
        "source_files": len(source_files),
        "test_files": len(test_files),
    })
    if base.surface_filter != "all":
        result["errors"].append(
            f"surface_filter={base.surface_filter!r}; full-surface protocol requires 'all'")
    if not minimum <= len(surface) <= maximum:
        result["errors"].append(
            f"surface has {len(surface)} names; deadline gate is {minimum}..{maximum}")
    if not test_files:
        result["errors"].append("no checked-in tests matched test_globs")
    if not base.original_readme_files:
        result["errors"].append("original knowledge bundle is empty")

    source = repo_root / "source"
    result["upstream"] = {
        "commit": git_value(source, "rev-parse", "HEAD"),
        "dirty": bool(git_value(source, "status", "--porcelain")),
    }

    work_dirs: dict[str, str] = {}
    output_dirs: dict[str, str] = {}
    configs = {}
    for cell in CELLS:
        path = repo_root / f"configs/aideal_{cell}.yaml"
        if not path.exists():
            result["errors"].append(f"missing condition config {path.name}")
            continue
        cfg = load_config(path)
        ex = cfg.comprehension.get("execute", {})
        sample_data, _, sample_warnings = _execute_sample_data(cfg, ex)
        scaffold = (cfg.root / str(ex.get("scaffold", ""))).resolve()
        configs[cell] = {
            "sha256": sha256(path),
            "work_dir": str(ex.get("work_dir", "")),
            "output_dir": str(ex.get("output_dir", "")),
            "scaffold": str(scaffold),
            "sample_data": sample_data,
            "sample_data_warnings": sample_warnings,
            "models": {role: (
                f"{cfg.model_for_role(role).provider}:{cfg.model_for_role(role).model}")
                for role in ("author", "audience", "fixer")},
        }
        if cfg.project_name != base.project_name or cfg.language != base.language:
            result["errors"].append(f"{cell} changes project identity")
        if not ex.get("command"):
            result["errors"].append(f"{cell} has no execution command")
        if not scaffold.is_file():
            result["errors"].append(f"{cell} scaffold missing: {scaffold}")
        if sample_warnings:
            result["errors"].extend(f"{cell}: {warning}" for warning in sample_warnings)
        work_dirs[cell] = str((cfg.root / str(ex.get("work_dir", ""))).resolve())
        output_dirs[cell] = str((cfg.root / str(ex.get("output_dir", ""))).resolve())
        if str(ex.get("output_dir", "")).startswith("/tmp/"):
            result["errors"].append(
                f"{cell} uses shared absolute output_dir {ex.get('output_dir')}")

    if len(set(work_dirs.values())) != len(work_dirs):
        result["errors"].append("condition work_dir values are not unique")
    if len(set(output_dirs.values())) != len(output_dirs):
        result["errors"].append("condition output_dir values are not unique")
    result["configs"] = configs
    result["ready"] = not result["errors"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_roots", nargs="+", type=Path)
    parser.add_argument("--min-api", type=int, default=50)
    parser.add_argument("--max-api", type=int, default=200)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = {"schema": 1, "repositories": [
        validate(path.resolve(), args.min_api, args.max_api)
        for path in args.repo_roots
    ]}
    report["ready"] = all(item["ready"] for item in report["repositories"])
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        tmp = args.out.with_suffix(args.out.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(args.out)
    print(text, end="")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
