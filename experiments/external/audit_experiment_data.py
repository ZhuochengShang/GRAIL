#!/usr/bin/env python3
"""Read-only audit of priority-study inputs and per-API test data evidence.

Never invokes a provider or runs a generated snippet. Output is owned by this
observer alone; the existing report observer can commit it with the package.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import fcntl
import glob
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import time

from aideal.config import load_config
from aideal.doc_checks import _execute_sample_data, _sha256_files
from aideal.readme_agent import public_api_surface
from experiments.external.audit_overnight import DEADLINE, atomic, dump, read_checkpoint, read_json


SPECS = {
    "mir_eval": ("GRAIL_mir_eval", "experiments/external/mir_eval", "source", 148,
                 "fe73b3533737814f83dbd9739f06e90f5f82f758"),
    "thumbnailator": ("GRAIL_thumbnailator", "experiments/external/thumbnailator", "source", 149,
                     "c9d99613878bbbf1f4d9369585b4cb5352c3b474"),
    "tslearn": ("GRAIL_tslearn_full235", "experiments/tslearn", "tslearn", 235,
                "f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                   stderr=subprocess.PIPE).strip()


def fixture_evidence(path: Path, source: Path) -> dict:
    row = {"path": str(path), "exists": path.is_file()}
    if not path.is_file():
        return row
    row.update(sha256=sha(path), bytes=path.stat().st_size)
    try:
        relative = path.resolve().relative_to(source.resolve())
        expected = git(source, "rev-parse", f"HEAD:{relative}")
        actual = git(source, "hash-object", str(path))
        row.update(upstream_path=str(relative), tracked_at_pinned_commit=True,
                   pinned_blob=expected, actual_blob=actual, matches_pinned_blob=expected == actual)
    except (ValueError, subprocess.CalledProcessError):
        row.update(tracked_at_pinned_commit=False, matches_pinned_blob=False)
    try:
        if path.suffix.lower() in (".png", ".jpg", ".jpeg"):
            from PIL import Image
            with Image.open(path) as image:
                row["decoded"] = {"format": image.format, "size": list(image.size), "mode": image.mode}
                image.verify()
        elif path.suffix == ".npz":
            import numpy as np
            with np.load(path, allow_pickle=False) as arrays:
                row["decoded"] = {key: {"shape": list(arrays[key].shape), "dtype": str(arrays[key].dtype)}
                                  for key in arrays.files}
        elif path.suffix.lower() in (".txt", ".lab", ".csv"):
            lines = [line for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")]
            row["decoded"] = {"data_lines": len(lines), "first_line_columns": len(lines[0].split()) if lines else 0}
    except Exception as exc:
        row["decode_error"] = f"{type(exc).__name__}: {exc}"
    return row


def snippet_evidence(code: str, name: str, region: list[str], bindings: dict, preamble: str) -> dict:
    if len(region) == 2 and region[0] in code and region[1] in code:
        body = code.split(region[0], 1)[1].split(region[1], 1)[0]
    else:
        return {"snippet_region_found": False, "semantic_validation": "unverified"}
    used = [key for key in bindings if key != "output_dir" and re.search(rf"\b{re.escape(key)}\b", body)]
    preloaded = re.findall(r"(?m)^\s*(?:\w+(?:<[^>]+>)?\s+)?(\w+)\s*=", preamble)
    return {
        "snippet_region_found": True,
        "configured_fixture_bindings_referenced": used,
        "preloaded_bindings_referenced": sorted({key for key in preloaded if re.search(rf"\b{re.escape(key)}\b", body)}),
        "target_name_call_visible": bool(re.search(rf"\b{re.escape(name)}\s*\(", body)),
        "assertion_text_visible": bool(re.search(r"\bassert\b|\brequire\s*\(|AssertionError|throw new", body)),
        "witness_text_visible": "__CHECK__" in body,
        "semantic_validation": "unverified: textual references do not prove executed API ownership, input suitability, or correct assertions",
    }


def inspect(base: Path, repo: str, cell: str, out: Path) -> dict:
    prefix, relative, source_name, count, commit = SPECS[repo]
    wt = base / f"{prefix}_{cell}"
    if not wt.exists():
        return {"status": "pending", "expected_apis": count}
    root = wt / relative
    suffix = "_full235" if repo == "tslearn" else ""
    config_path = root / f"configs/aideal_{cell}{suffix}.yaml"
    cfg = load_config(config_path)
    ex = cfg.comprehension["execute"]
    source = root / source_name
    manifest_path = root / "docs/eval/api_manifest.json"
    manifest = read_json(manifest_path)
    names = manifest.get("apis") or []
    freeze = base / (prefix + ("_freeze" if repo == "tslearn" else "_setup")) / relative
    frozen_manifest = freeze / "docs/eval/api_manifest.json"
    names_hash = hashlib.sha256("\n".join(names).encode()).hexdigest()
    failures, limitations = [], []
    frozen_cfg = load_config(freeze / f"configs/aideal_{cell}{suffix}.yaml")
    if cfg.raw != frozen_cfg.raw:
        failures.append("effective condition configuration differs from its frozen counterpart")
    if sha(root / "configs/project_profile.yaml") != sha(freeze / "configs/project_profile.yaml"):
        failures.append("project profile differs from frozen profile")
    if len(names) != count or len(set(names)) != count or sha(manifest_path) != sha(frozen_manifest):
        failures.append("manifest differs from frozen full surface")
    if sorted(public_api_surface(cfg, override_filter="all")) != names:
        failures.append("current discovered public API names differ from frozen manifest")
    actual_commit = git(source, "rev-parse", "HEAD")
    if actual_commit != commit:
        failures.append("upstream commit differs from pinned version")
    if git(source, "diff", "--name-only", "HEAD"):
        failures.append("tracked upstream files differ from pinned commit")
    tracked = set(git(source, "ls-files", "-z").split("\0"))
    source_files = [Path(p) for pattern in cfg.source_globs for p in glob.glob(str(root / pattern), recursive=True)]
    if any(str(path.resolve().relative_to(source.resolve())) not in tracked for path in source_files):
        failures.append("source discovery includes untracked source files")
    bindings, _, warnings = _execute_sample_data(cfg, ex)
    failures.extend(warnings)
    inputs = {key: fixture_evidence(Path(value.removeprefix("file://")), source)
              for key, value in bindings.items() if key != "output_dir"}
    for key, row in inputs.items():
        if not row.get("matches_pinned_blob"):
            failures.append(f"input {key} does not match a checked-in blob at the pinned source")
        if row.get("decode_error"):
            limitations.append(f"input {key}: {row['decode_error']}")
    scaffold = (root / ex["scaffold"]).resolve()
    frozen_scaffold = freeze / ex["scaffold"]
    if sha(scaffold) != sha(frozen_scaffold):
        failures.append("scaffold differs from frozen scaffold")
    output = Path(bindings["output_dir"].removeprefix("file://"))
    try:
        output.relative_to(wt)
    except ValueError:
        failures.append("output directory escapes its condition worktree")
    if not output.is_dir():
        limitations.append("supplied output directory does not currently exist; write APIs may fail before the target call")
    result_path = root / f"docs/eval/{cell}/comprehension.json"
    result = read_json(result_path)
    events, checkpoint_errors = read_checkpoint(root / ex["work_dir"] / "comprehension_progress.jsonl")
    failures.extend(checkpoint_errors)
    fingerprint = result.get("run", {}).get("experiment_fingerprint") or next(
        (e.get("experiment_fingerprint") for e in reversed(events)), None)
    metrics = result.get("metrics") or {e["name"]: e for e in events if e.get("experiment_fingerprint") == fingerprint}
    if set(metrics) - set(names):
        failures.append("observed metrics include names outside the manifest")
    comparisons = {}
    if result:
        run = result["run"]
        fp = run.get("fingerprint_components") or {}
        comparisons = {
            "manifest_names_hash": run.get("manifest_sha256") == names_hash,
            "source_contents": fp.get("source") == _sha256_files(source_files, root),
            "scaffold_contents": fp.get("scaffold") == _sha256_files([scaffold], root),
            "effective_execution_config": fp.get("execute_config") == ex,
            "document_treatment": result.get("doc_source") == {"A1": "original", "A2": "aideal", "B1": "original+aideal", "B2": "aideal"}[cell],
        }
        for key, ok in comparisons.items():
            if not ok:
                failures.append(f"completed result disagrees with current pinned {key}")
        # The old runner includes output_dir in its aggregate fixture hash.
        # Independently verify input bytes; never confuse outputs with inputs.
        comparisons["input_only_fixture_hash"] = _sha256_files(
            [Path(value.removeprefix("file://")) for key, value in bindings.items() if key != "output_dir"], root)
        comparisons["recorded_fixture_hash"] = fp.get("fixtures")
        if comparisons["input_only_fixture_hash"] != comparisons["recorded_fixture_hash"]:
            limitations.append("recorded fixture aggregate differs from input-only aggregate; the runner may include mutable output files")
    rows = []
    for name in names:
        row = {"api": name, "status": metrics.get(name, {}).get("status", "pending"),
               "declared_source": metrics.get(name, {}).get("source"), "semantic_validation": "unverified"}
        if "/" not in name and ".." not in name:
            script = root / ex["work_dir"] / f"run_{name}" / ex["test_filename"]
            if script.is_file():
                row.update(script=str(script), script_sha256=sha(script))
                row.update(snippet_evidence(script.read_text(), name, ex.get("region", []), bindings, str(ex.get("preamble", ""))))
        rows.append(row)
    report = {"status": "FAIL" if failures else "PASS_WITH_LIMITATIONS", "failures": failures,
              "limitations": limitations, "expected_apis": count, "manifest_file_sha256": sha(manifest_path),
              "manifest_ordered_names_sha256": names_hash, "upstream_commit": actual_commit,
              "config_path": str(config_path), "config_sha256": sha(config_path),
              "profile_sha256": sha(root / "configs/project_profile.yaml"), "scaffold_sha256": sha(scaffold),
              "preamble_sha256": hashlib.sha256(str(ex.get("preamble", "")).encode()).hexdigest(),
              "fixture_bindings": inputs, "output_directory": str(output), "result_comparisons": comparisons,
              "observed_statuses": dict(Counter(row["status"] for row in rows)), "api_test_evidence": rows}
    dump(out / repo / cell / "data_evidence.json", report)
    stream = io.StringIO()
    fields = ["api", "status", "declared_source", "script", "script_sha256", "target_name_call_visible",
              "configured_fixture_bindings_referenced", "preloaded_bindings_referenced", "assertion_text_visible",
              "witness_text_visible", "semantic_validation"]
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    atomic(out / repo / cell / "api_test_data.csv", stream.getvalue())
    return {k: v for k, v in report.items() if k != "api_test_evidence"}


def audit(base: Path, out: Path) -> None:
    checks = {}
    for repo in SPECS:
        checks[repo] = {}
        for cell in ("A1", "A2", "B1", "B2"):
            try:
                checks[repo][cell] = inspect(base, repo, cell, out)
            except Exception as exc:
                checks[repo][cell] = {"status": "ERROR", "failures": [f"{type(exc).__name__}: {exc}"]}
    lines = ["# Experiment data and API-test verification", "",
             "This checks pinned input identity and records test evidence. It does not certify every generated assertion or API/data pairing.", "",
             "| Repository | Cell | Input provenance check | Issues |", "|---|---|---|---|"]
    for repo, cells in checks.items():
        for cell, row in cells.items():
            issues = "; ".join(row.get("failures", []) + row.get("limitations", [])) or "none observed"
            lines.append(f"| {repo} | {cell} | {row['status']} | {issues.replace('|', '/')} |")
    lines += ["", "For each active cell, data_evidence.json lists absolute input paths, SHA-256, pinned Git blobs, "
              "decoded file metadata, manifest/config/profile/scaffold hashes, and completed-result consistency checks. "
              "api_test_data.csv covers every manifest API and records which supplied fixtures or preloaded values "
              "are referenced inside its generated snippet, plus target-call/assertion/witness text. "
              "Textual references are evidence for review, not proof of runtime dataflow or semantic correctness.", "",
              "Inputs are checked against pinned source blobs; generated outputs are recorded separately. "
              "Do not install dependencies, alter fixture contents, or fix assertions inside active measured conditions. "
              "Use separate diagnostic copies and retain native scores.", ""]
    dump(out / "summary.json", checks)
    atomic(out / "DATA_VALIDATION.md", "\n".join(lines))
    # A separate, authoritative index combines the existing result observer
    # with this input audit without restarting it or sharing its output files.
    result_status = read_json(out.parent / "status.json")
    release = {}
    index = ["# Wednesday result report with data checks", "",
             f"Deadline: {DEADLINE.isoformat()}. Values below come from recorded final results; pending cells are not filled with estimates.", "",
             "| Repository | A1 pass/total | A2 pass/total | B1 pass/total | B2 pass/total | Release decision |",
             "|---|---|---|---|---|---|"]
    for repo, cells in checks.items():
        final_cells = result_status.get("cells", {}).get(repo, {})
        input_ok = all(cells.get(c, {}).get("status") == "PASS_WITH_LIMITATIONS" for c in ("A1", "A2", "B1", "B2"))
        complete = all(final_cells.get(c, {}).get("status") == "complete" for c in ("A1", "A2", "B1", "B2"))
        report_path = out.parent / repo / "DETAILED_REPORT.md"
        report_valid = report_path.is_file() and "**Comparison status: VALID WITH RECORDED LIMITATIONS.**" in report_path.read_text()
        release[repo] = "COMPLETE_WITH_LIMITATIONS" if complete and input_ok and report_valid else "WITHHELD/PARTIAL"
        values = [f"{final_cells[c]['counts'].get('pass', 0)}/{final_cells[c]['expected']}"
                  if final_cells.get(c, {}).get("status") == "complete" else "pending"
                  for c in ("A1", "A2", "B1", "B2")]
        index.append("| " + " | ".join([repo, *values, release[repo]]) + " |")
    index += ["", "Release requires all four complete matched results, the result observer's validity checks, "
              "and matching input provenance for all four cells. COMPLETE_WITH_LIMITATIONS is not a claim that "
              "every generated assertion or API/data pairing has been independently verified.", "",
              "- [Data checks and per-API test-data evidence](data_validation/DATA_VALIDATION.md)",
              "- [Detailed outcomes, effects, failures and rounds](DETAILED_PRIORITY_REPORT.md)", ""]
    dump(out / "release_status.json", release)
    atomic(out.parent / "FINAL_REPORT_WITH_DATA_CHECKS.md", "\n".join(index))
    if time.time() >= DEADLINE.timestamp() - 15 * 60:
        import shutil
        destination = out.parent / "deadline_snapshot" / "data_validation"
        if not (destination / "captured.json").exists():
            shutil.copytree(out, destination, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("observer.*", "heartbeat.json"))
            shutil.copy2(out.parent / "FINAL_REPORT_WITH_DATA_CHECKS.md", destination.parent / "FINAL_REPORT_WITH_DATA_CHECKS.md")
            dump(destination / "captured.json", {"epoch": time.time(), "release": release})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-parent", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "observer.lock").open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            audit(args.workspace_parent.resolve(), args.out.resolve())
            atomic(args.out / "heartbeat.json", json.dumps({"epoch": time.time()}))
            if not args.watch:
                return
            time.sleep(60)


if __name__ == "__main__":
    main()
