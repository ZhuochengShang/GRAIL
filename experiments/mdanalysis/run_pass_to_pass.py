#!/usr/bin/env python3
"""Run and compare the pinned upstream MDAnalysis suite before/after treatment."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


SOURCE_COMMIT = "81b8ef51e5bc1aa2824294ac6c52818c74975658"


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()


def junit_cases(path: Path) -> dict[str, str]:
    root = ET.parse(path).getroot()
    rows: dict[str, str] = {}
    for case in root.iter("testcase"):
        key = f"{case.get('classname', '')}::{case.get('name', '')}"
        if key in rows:
            raise RuntimeError(f"duplicate JUnit identity: {key}")
        status = "pass"
        if case.find("skipped") is not None:
            status = "skip"
        elif case.find("failure") is not None:
            status = "fail"
        elif case.find("error") is not None:
            status = "error"
        rows[key] = status
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment-root", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--phase", required=True, choices=["before", "after"])
    parser.add_argument("--cell", default="freeze")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = args.experiment_root.resolve()
    source = root / "mdanalysis"
    if git_head(source) != SOURCE_COMMIT:
        raise RuntimeError(f"{source} is not pinned to {SOURCE_COMMIT}")
    out = args.out_dir.resolve()
    python = source / ".venv/bin/python"
    if not python.is_file():
        raise RuntimeError(f"missing pinned editable runtime: {python}")
    prefix = f"PASS_TO_PASS_{args.phase.upper()}"
    junit = out / f"{prefix}.xml"
    log_path = out / f"{prefix}.log"
    result_path = out / f"{prefix}.json"
    command = [
        str(python), "-m", "pytest", "-q", "--disable-warnings",
        f"--junitxml={junit}", "testsuite/MDAnalysisTests",
    ]
    if args.dry_run:
        print(json.dumps({
            "dry_run": True, "cwd": str(source), "command": command,
            "source_commit": SOURCE_COMMIT,
        }, indent=2))
        return 0

    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "PYTHONPATH": f"{source / 'package'}:{source / 'testsuite'}",
        "MPLBACKEND": "Agg",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "PYTHONHASHSEED": "0",
    })
    started = time.time()
    proc = subprocess.run(command, cwd=source, env=env, text=True,
                          capture_output=True, check=False)
    atomic_text(log_path, proc.stdout + "\n" + proc.stderr)
    if not junit.is_file():
        raise RuntimeError(f"pytest did not create {junit}; exit={proc.returncode}")
    cases = junit_cases(junit)
    counts = dict(Counter(cases.values()))
    record: dict[str, object] = {
        "schema": 1,
        "phase": args.phase,
        "cell": args.cell,
        "source_commit": SOURCE_COMMIT,
        "python": str(python),
        "command": command,
        "exit_code": proc.returncode,
        "wall_s": round(time.time() - started, 1),
        "counts": counts,
        "case_count": len(cases),
        "cases_sha256": sha256_json(cases),
        "cases": cases,
        "log": str(log_path),
        "junit": str(junit),
    }
    ok = proc.returncode == 0 and not counts.get("fail") and not counts.get("error")
    if args.phase == "after":
        if not args.baseline:
            parser.error("--baseline is required for --phase after")
        baseline = json.loads(args.baseline.resolve().read_text(encoding="utf-8"))
        before = baseline.get("cases") or {}
        lost_passes = sorted(name for name, state in before.items()
                             if state == "pass" and cases.get(name) != "pass")
        changed = sorted(name for name in set(before) | set(cases)
                         if before.get(name) != cases.get(name))
        record["baseline"] = str(args.baseline.resolve())
        record["baseline_cases_sha256"] = baseline.get("cases_sha256")
        record["lost_passes"] = lost_passes
        record["changed_cases"] = changed
        record["pass_to_pass"] = not lost_passes
        ok = ok and not lost_passes
    record["passed"] = ok
    atomic_text(result_path, json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    lines = [
        f"# MDAnalysis PASS_TO_PASS {args.phase} — {args.cell}", "",
        f"- Source commit: `{SOURCE_COMMIT}`",
        f"- Exit code: `{proc.returncode}`",
        f"- Cases: `{len(cases)}`",
        f"- Counts: `{json.dumps(counts, sort_keys=True)}`",
        f"- Cases SHA-256: `{record['cases_sha256']}`",
        f"- PASS_TO_PASS: `{'PASS' if ok else 'FAIL'}`",
    ]
    if args.phase == "after":
        lines.extend([
            f"- Baseline: `{record['baseline']}`",
            f"- Lost prior passes: `{len(record['lost_passes'])}`",
            f"- Changed cases: `{len(record['changed_cases'])}`",
        ])
    atomic_text(out / f"{prefix}.md", "\n".join(lines) + "\n")
    print(json.dumps({
        "passed": ok, "result": str(result_path), "counts": counts,
        "case_count": len(cases),
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
