#!/usr/bin/env python3
"""Unattended, crash-resumable tslearn full-surface A1/A2/B1/B2 pipeline.

The script creates one Git worktree per cell, preserves every historical
tslearn worktree, rate-limits Gemini across processes, validates all 235 names,
runs upstream tests before/after treatment, writes per-function failure
analysis, and commits/pushes a cell only after its completion gates pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import yaml

from experiments.external.run_condition_watchdog import Supervisor


PYTHON = Path("/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python")
SOURCE_COMMIT = "f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7"
FREEZE_BRANCH = "aideal/tslearn-full235-freeze"
BRANCHES = {cell: f"aideal/tslearn-full235-{cell}" for cell in ("A1", "A2", "B1", "B2")}
WORKTREE_NAMES = {cell: f"GRAIL_tslearn_full235_{cell}" for cell in BRANCHES}
REL = Path("experiments/tslearn")


def run(command: list[str], cwd: Path, *, check: bool = True,
        env: dict | None = None) -> subprocess.CompletedProcess:
    print(f"[{time.strftime('%H:%M:%S')}] {cwd.name}: {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                          check=check, env=env)


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd, check=check)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_worktree(setup: Path, cell: str, start: str) -> Path:
    branch = BRANCHES[cell]
    path = setup.parent / WORKTREE_NAMES[cell]
    if path.is_dir() and (path / ".git").exists():
        actual = git(path, "branch", "--show-current").stdout.strip()
        if actual != branch:
            raise RuntimeError(f"{path} is {actual}, expected {branch}")
        return path
    exists = git(setup, "show-ref", "--verify", "--quiet",
                 f"refs/heads/{branch}", check=False).returncode == 0
    command = ["git", "worktree", "add"]
    if not exists:
        command.extend(["-b", branch])
    command.extend([str(path), branch if exists else start])
    run(command, setup)
    return path


def ensure_source(setup: Path, worktree: Path) -> Path:
    source = worktree / REL / "tslearn"
    setup_source = setup / REL / "tslearn"
    if not (source / ".git").exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--shared", str(setup_source), str(source)], worktree)
        git(source, "checkout", "--detach", SOURCE_COMMIT)
    actual = git(source, "rev-parse", "HEAD").stdout.strip()
    if actual != SOURCE_COMMIT:
        raise RuntimeError(f"{worktree.name}: source {actual}, expected {SOURCE_COMMIT}")
    if not (source / "tslearn/.cached_datasets/Trace.npz").is_file():
        raise RuntimeError(f"{worktree.name}: repository Trace fixture missing")
    return source


def environment_inventory(worktree: Path, cell: str, source: Path) -> Path:
    env = dict(os.environ, PYTHONPATH=str(source), MPLBACKEND="Agg",
               PYTHONHASHSEED="0", NUMBA_THREADING_LAYER="workqueue",
               NUMBA_NUM_THREADS="1", OMP_NUM_THREADS="1",
               OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    versions = run([str(PYTHON), "-c",
                    "import sys,numpy,scipy,sklearn,numba,tslearn; "
                    "print('python='+sys.version.replace('\\n',' ')); "
                    "print('executable='+sys.executable); "
                    "print('tslearn='+tslearn.__version__); "
                    "print('tslearn_file='+tslearn.__file__); "
                    "print('numpy='+numpy.__version__); print('scipy='+scipy.__version__); "
                    "print('sklearn='+sklearn.__version__); print('numba='+numba.__version__)"],
                   worktree, env=env).stdout
    packages = run([str(PYTHON), "-m", "pip", "freeze"], worktree).stdout
    manifest = worktree / REL / "docs/eval/api_manifest.json"
    scaffold = worktree / REL / "docs/api_test_scaffold_full235.py"
    fixture = source / "tslearn/.cached_datasets/Trace.npz"
    config = worktree / REL / f"configs/aideal_{cell}_full235.yaml"
    text = (
        f"cell={cell}\nsource_commit={SOURCE_COMMIT}\n"
        f"source_tree={git(source, 'rev-parse', 'HEAD^{tree}').stdout.strip()}\n"
        f"manifest_sha256={sha(manifest)}\nscaffold_sha256={sha(scaffold)}\n"
        f"config_sha256={sha(config)}\nfixture_sha256={sha(fixture)}\n"
        f"PYTHONPATH={source}\nNUMBA_THREADING_LAYER=workqueue\nthreads=1\n"
        f"{versions}\n[pip-freeze]\n{packages}")
    path = worktree / REL / f"docs/eval/setup/environment_{cell}.txt"
    atomic_text(path, text)
    return path


def upstream_tests(worktree: Path, cell: str, stage: str, source: Path) -> Path:
    env = dict(os.environ, PYTHONPATH=str(source), MPLBACKEND="Agg",
               PYTHONHASHSEED="0", NUMBA_THREADING_LAYER="workqueue",
               NUMBA_NUM_THREADS="1", OMP_NUM_THREADS="1",
               OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    started = time.time()
    proc = run([str(PYTHON), "-m", "pytest", "-q"], source,
               check=False, env=env)
    combined = proc.stdout + proc.stderr
    path = worktree / REL / f"docs/eval/{cell}/PASS_TO_PASS_{stage.upper()}.md"
    text = (
        f"# tslearn PASS_TO_PASS {stage} {cell}\n\n"
        f"- Exit code: {proc.returncode}\n"
        f"- Source commit: `{SOURCE_COMMIT}`\n"
        f"- Python: `{PYTHON}`\n"
        f"- Duration seconds: {time.time() - started:.1f}\n"
        f"- Output SHA-256: `{hashlib.sha256(combined.encode()).hexdigest()}`\n\n"
        f"```text\n{combined[-20000:]}\n```\n")
    atomic_text(path, text)
    if proc.returncode != 0:
        raise RuntimeError(f"tslearn upstream tests failed {stage} {cell}")
    return path


def validate(worktree: Path, *, cell: str | None = None,
             require_readme: bool = False) -> None:
    command = [str(PYTHON), str(REL / "validate_full235.py")]
    if cell:
        command.extend(["--condition", cell])
    if require_readme:
        command.append("--require-readme")
    env = dict(os.environ, PYTHONPATH=str(worktree / "grail-agent/src"))
    proc = run(command, worktree, check=False, env=env)
    if proc.returncode:
        raise RuntimeError(proc.stdout + proc.stderr)


def commit_push(worktree: Path, branch: str, message: str, paths: list[Path]) -> None:
    existing = [str(path) for path in paths if (worktree / path).exists()]
    if existing:
        git(worktree, "add", "--", *existing)
        if git(worktree, "diff", "--cached", "--quiet", check=False).returncode != 0:
            git(worktree, "commit", "-m", message)
    git(worktree, "push", "-u", "origin", branch)


def common_job(worktree: Path, cell: str, inventory: Path) -> dict:
    return {
        "cwd": str(worktree), "branch": BRANCHES[cell],
        "environment_inventory": str(inventory.relative_to(worktree)),
        "env": {"PYTHONPATH": str(worktree / "grail-agent/src")},
        "max_restarts": 0,
    }


def generation_job(worktree: Path, inventory: Path) -> dict:
    job = common_job(worktree, "A2", inventory)
    job.update({
        "id": "tslearn_A2_generate",
        "command": [str(PYTHON), "experiments/external/run_resumable_readme.py",
                    "--config", "experiments/tslearn/configs/aideal_A2_full235.yaml",
                    "--limit", "0"],
        "result": "experiments/tslearn/docs/eval/A2/generation_result.json",
        "complete": {"kind": "readme_generation"},
        "max_runtime_seconds": 172800,
    })
    return job


def validation_job(worktree: Path, inventory: Path) -> dict:
    job = common_job(worktree, "A2", inventory)
    job.update({
        "id": "tslearn_A2_validate_readme",
        "depends_on": ["tslearn_A2_generate"],
        "command": [str(PYTHON), "experiments/tslearn/validate_full235.py",
                    "--condition", "A2", "--require-readme"],
        "result": "experiments/tslearn/docs/eval/A2/static_validation.json",
        "complete": {"kind": "file_nonempty"},
        "max_runtime_seconds": 1800,
    })
    return job


def comprehension_job(worktree: Path, cell: str, inventory: Path,
                      depends_on: list[str] | None = None) -> dict:
    job = common_job(worktree, cell, inventory)
    doc = {"A1": "original", "A2": "aideal",
           "B1": "original+aideal", "B2": "aideal"}[cell]
    job.update({
        "id": f"tslearn_{cell}_zero",
        "depends_on": depends_on or [],
        "command": [str(PYTHON), "-m", "aideal.cli", "--config",
                    f"experiments/tslearn/configs/aideal_{cell}_full235.yaml",
                    "comprehension", "--execute", "--show-code", "--doc", doc,
                    "--doc-scope", "relevant", "--manifest",
                    "docs/eval/api_manifest.json", "--max-fix-rounds", "0",
                    "--resume", "--timeout", "300"],
        "result": f"experiments/tslearn/docs/eval/{cell}/comprehension.json",
        "complete": {"kind": "json_metrics_no_transient"},
        "max_runtime_seconds": 172800,
    })
    return job


def repair_job(worktree: Path, cell: str, inventory: Path) -> dict:
    job = common_job(worktree, cell, inventory)
    source_cell = "A1" if cell == "B1" else "A2"
    doc = "original+aideal" if cell == "B1" else "aideal"
    command = [str(PYTHON), "-m", "aideal.cli", "--config",
               f"experiments/tslearn/configs/aideal_{cell}_full235.yaml",
               "fix-docs", "--from-results",
               f"docs/eval/{source_cell}/comprehension.json",
               "--deep-dive-first", "--doc-rounds", "5", "--doc-stuck", "2",
               "--retry-rounds", "0", "--doc", doc, "--doc-scope", "relevant",
               "--manifest", "docs/eval/api_manifest.json", "--report",
               f"docs/eval/{cell}/docfix.json", "--deep-dive-out",
               f"docs/eval/{cell}/deepdive", "--timeout", "300"]
    if cell == "B1":
        command.append("--create-missing")
    job.update({
        "id": f"tslearn_{cell}_repair", "command": command,
        "result": f"experiments/tslearn/docs/eval/{cell}/docfix_command.json",
        "complete": {"kind": "docfix",
                     "path": f"experiments/tslearn/docs/eval/{cell}/docfix.json"},
        "max_runtime_seconds": 259200,
    })
    return job


def write_plan(setup: Path, name: str, jobs: list[dict]) -> Path:
    path = setup / REL / f"docs/eval/watchdogs/{name}.yaml"
    plan = {
        "version": 1,
        "max_parallel": 2,
        "retry_delay_seconds": 300,
        "env": {
            "AIDEAL_GOOGLE_MIN_INTERVAL_S": "3",
            "AIDEAL_GOOGLE_RATE_STATE": "/tmp/aideal_google_rate_gate.txt",
            "AIDEAL_GOOGLE_REQUEST_TIMEOUT_S": "300",
            "AIDEAL_GOOGLE_MAX_RETRIES": "2",
            "PYTHONUNBUFFERED": "1",
        },
        "jobs": jobs,
    }
    atomic_text(path, yaml.safe_dump(plan, sort_keys=False))
    return path


def run_plan(path: Path, *, execute: bool) -> None:
    supervisor = Supervisor(path)
    supervisor.preflight()
    if execute and supervisor.run() != 0:
        raise RuntimeError(f"watchdog failed: {path}")


def analyze(worktree: Path, cell: str) -> None:
    run([str(PYTHON), "experiments/external/analyze_failures.py",
         f"experiments/tslearn/docs/eval/{cell}/comprehension.json",
         "--out-dir", f"experiments/tslearn/docs/eval/{cell}/failure_analysis",
         "--label", f"tslearn full235 {cell}"], worktree)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-worktree", type=Path, default=Path.cwd())
    parser.add_argument("--prepare-only", action="store_true",
                        help="create A1/A2 worktrees, run non-LLM preflights, and validate YAML")
    args = parser.parse_args()
    setup = args.freeze_worktree.resolve()
    if git(setup, "branch", "--show-current").stdout.strip() != FREEZE_BRANCH:
        raise RuntimeError(f"freeze worktree must be {FREEZE_BRANCH}")
    validate(setup)
    freeze_head = git(setup, "rev-parse", "HEAD").stdout.strip()

    worktrees: dict[str, Path] = {}
    inventories: dict[str, Path] = {}
    for cell in ("A1", "A2"):
        wt = ensure_worktree(setup, cell, freeze_head)
        source = ensure_source(setup, wt)
        validate(wt)
        inventories[cell] = environment_inventory(wt, cell, source)
        worktrees[cell] = wt
        pre = wt / REL / f"docs/eval/{cell}/PASS_TO_PASS_BEFORE.md"
        if not pre.is_file():
            upstream_tests(wt, cell, "before", source)

    baseline_plan = write_plan(setup, "full235_baselines", [
        comprehension_job(worktrees["A1"], "A1", inventories["A1"]),
        generation_job(worktrees["A2"], inventories["A2"]),
        validation_job(worktrees["A2"], inventories["A2"]),
        comprehension_job(worktrees["A2"], "A2", inventories["A2"],
                          ["tslearn_A2_validate_readme"]),
    ])
    run_plan(baseline_plan, execute=not args.prepare_only)
    if args.prepare_only:
        print(f"prepared without Gemini: {baseline_plan}")
        return 0

    for cell in ("A1", "A2"):
        analyze(worktrees[cell], cell)
        paths = [REL / f"docs/eval/{cell}", REL / f"logs/eval/{cell}",
                 REL / f"docs/eval/setup/environment_{cell}.txt"]
        commit_push(worktrees[cell], BRANCHES[cell],
                    f"Complete tslearn full235 {cell}", paths)

    for cell, parent_cell in (("B1", "A1"), ("B2", "A2")):
        start = git(worktrees[parent_cell], "rev-parse", "HEAD").stdout.strip()
        wt = ensure_worktree(setup, cell, start)
        source = ensure_source(setup, wt)
        worktrees[cell] = wt
        inventories[cell] = environment_inventory(wt, cell, source)
        if cell == "B2":
            source_doc = wt / REL / "docs/eval/A2/LLM_readme.md"
            target_doc = wt / REL / "docs/eval/B2/LLM_readme.md"
            if not target_doc.exists():
                target_doc.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_doc, target_doc)

    repair_jobs = []
    for cell in ("B1", "B2"):
        repair_jobs.append(repair_job(worktrees[cell], cell, inventories[cell]))
        repair_jobs.append(comprehension_job(
            worktrees[cell], cell, inventories[cell], [f"tslearn_{cell}_repair"]))
    repair_plan = write_plan(setup, "full235_repairs", repair_jobs)
    run_plan(repair_plan, execute=True)

    for cell in ("B1", "B2"):
        analyze(worktrees[cell], cell)
        upstream_tests(worktrees[cell], cell, "after", ensure_source(setup, worktrees[cell]))
        paths = [REL / f"docs/eval/{cell}", REL / f"logs/eval/{cell}",
                 REL / f"docs/eval/setup/environment_{cell}.txt"]
        commit_push(worktrees[cell], BRANCHES[cell],
                    f"Complete tslearn full235 {cell}", paths)

    comparison = setup / REL / "docs/eval/compare_2x2.md"
    run([str(PYTHON), "experiments/rdpro/compare_2x2.py",
         "--a1", str(worktrees["A1"] / REL / "docs/eval/A1/comprehension.json"),
         "--a2", str(worktrees["A2"] / REL / "docs/eval/A2/comprehension.json"),
         "--b1", str(worktrees["B1"] / REL / "docs/eval/B1/comprehension.json"),
         "--b2", str(worktrees["B2"] / REL / "docs/eval/B2/comprehension.json"),
         "--out", str(comparison)], setup)
    commit_push(setup, FREEZE_BRANCH, "Record tslearn full235 final 2x2",
                [REL / "docs/eval/compare_2x2.md", REL / "docs/eval/watchdogs"])
    print("tslearn full235 A1/A2/B1/B2 complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
