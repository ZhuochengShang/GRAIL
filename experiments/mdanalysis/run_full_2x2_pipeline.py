#!/usr/bin/env python3
"""Unattended, restart-safe MDAnalysis full-surface A1/A2/B1/B2 pipeline."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from experiments.external.run_condition_watchdog import Supervisor


PYTHON = Path("/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python")
SOURCE_COMMIT = "81b8ef51e5bc1aa2824294ac6c52818c74975658"
FREEZE_BRANCH = "aideal/mdanalysis-full1032-freeze"
CELLS = ("A1", "A2", "B1", "B2")


def run(command: list[str], cwd: Path, *, check: bool = True,
        env: dict | None = None) -> subprocess.CompletedProcess:
    print(f"[{time.strftime('%H:%M:%S')}] {cwd.name}: {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=cwd, env=env, text=True,
                          capture_output=True, check=check)


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd, check=check)


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def commit_push(worktree: Path, branch: str, message: str, paths: list[str]) -> None:
    existing = [path for path in paths if (worktree / path).exists()]
    if existing:
        git(worktree, "add", "--", *existing)
        if git(worktree, "diff", "--cached", "--quiet", check=False).returncode != 0:
            git(worktree, "commit", "-m", message)
    git(worktree, "push", "-u", "origin", branch)


def ensure_worktree(freeze: Path, branch: str, path: Path, start: str) -> Path:
    if path.is_dir() and (path / ".git").exists():
        actual = git(path, "branch", "--show-current").stdout.strip()
        if actual != branch:
            raise RuntimeError(f"{path} is {actual}, expected {branch}")
        return path
    exists = git(freeze, "show-ref", "--verify", "--quiet",
                 f"refs/heads/{branch}", check=False).returncode == 0
    command = ["git", "worktree", "add"]
    if not exists:
        command.extend(["-b", branch])
    command.extend([str(path), branch if exists else start])
    run(command, freeze)
    return path


def ensure_source(seed: Path, worktree: Path, cell: str, build_tools: Path) -> Path:
    rel = Path("experiments/mdanalysis/mdanalysis")
    source = worktree / rel
    if not (source / ".git").exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--shared", str(seed), str(source)], worktree)
        git(source, "checkout", "--detach", SOURCE_COMMIT)
    actual = git(source, "rev-parse", "HEAD").stdout.strip()
    if actual != SOURCE_COMMIT:
        raise RuntimeError(f"{cell} source {actual}, expected {SOURCE_COMMIT}")

    venv_python = source / ".venv/bin/python"
    if not venv_python.is_file():
        run([str(PYTHON), "-m", "venv", "--system-site-packages", str(source / ".venv")],
            worktree)
    # The release source contains generated C that targets newer NumPy headers.
    # Re-Cythonize with the pinned 3.0.12 build tool copied during freeze setup,
    # then compile an editable build against this environment's NumPy.
    if not any((source / "package/MDAnalysis/lib").glob("_cutil*.so")):
        if not (build_tools / "Cython").is_dir():
            raise RuntimeError(f"missing offline Cython 3.0.12 build tools: {build_tools}")
        build_env = dict(os.environ, PYTHONPATH=str(build_tools))
        run([
            str(source / ".venv/bin/pip"), "install", "--no-build-isolation",
            "--no-deps", "-e", str(source / "package"),
        ], worktree, env=build_env)
    env = dict(os.environ, PYTHONPATH=f"{source / 'package'}:{source / 'testsuite'}")
    versions = run([
        str(venv_python), "-c",
        "import sys,MDAnalysis,MDAnalysisTests; "
        "print(sys.executable); print(MDAnalysis.__version__); "
        "print(MDAnalysis.__file__); print(MDAnalysisTests.__version__)",
    ], worktree, env=env).stdout
    if str(source / "package") not in versions:
        raise RuntimeError(f"{cell} runtime did not import the pinned editable source")
    freeze = run([str(venv_python), "-m", "pip", "freeze"], worktree, env=env).stdout
    inventory = (
        f"cell={cell}\nsource_commit={SOURCE_COMMIT}\n"
        f"source={source}\nversions:\n{versions}\npip_freeze:\n{freeze}"
    )
    inventory_path = (
        worktree / f"experiments/mdanalysis/docs/full_1032/setup/environment_{cell}.txt"
    )
    atomic_text(inventory_path, inventory)
    return inventory_path


def generation_complete(freeze: Path) -> bool:
    base = freeze / "experiments/mdanalysis/docs/full_1032/A2"
    result = read_json(base / "generation_result.json")
    state = read_json(freeze / "experiments/mdanalysis/.aideal_exec/readme_generation_state.json")
    return (
        result.get("api_entries") == 1032
        and result.get("generated_ok") == 1032
        and result.get("fallback_to_skeleton") == 0
        and bool(result.get("generation_fingerprint"))
        and state.get("target_count") == 1032
        and state.get("completed_count") == 1032
        and state.get("complete") is True
    )


def run_supervised(plan: Path) -> None:
    supervisor = Supervisor(plan)
    if supervisor.run() != 0:
        raise RuntimeError(f"watchdog failed: {plan}")


def wait_for_generation(freeze: Path) -> None:
    plan = freeze / "experiments/mdanalysis/docs/full_1032/setup/generation_watchdog.yaml"
    lock_path = plan.with_suffix(".watchdog.lock")
    while not generation_complete(freeze):
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                pass
            else:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
                run_supervised(plan)
        if not generation_complete(freeze):
            print("waiting for complete 1,032-entry README", flush=True)
            time.sleep(30)


def validate_generated_readme(freeze: Path) -> None:
    env = dict(os.environ, PYTHONPATH=str(freeze / "grail-agent/src"))
    code = (
        "import json; from pathlib import Path; "
        "from aideal.config import load_config; from aideal.readme_agent import parse_readme; "
        "c=load_config('experiments/mdanalysis/configs/aideal.full1032.A2.yaml'); "
        "m=json.loads(Path('experiments/mdanalysis/docs/full_1032/api_manifest.json').read_text()); "
        "e=parse_readme(c.llm_readme); assert [x.name for x in e]==m['apis']; "
        "assert all('TODO' not in x.body for x in e); print(len(e))"
    )
    run([str(PYTHON), "-c", code], freeze, env=env)


def analyze(worktree: Path, cell: str) -> None:
    rel = f"experiments/mdanalysis/docs/full_1032/{cell}"
    run([
        str(PYTHON), "experiments/external/analyze_failures.py",
        f"{rel}/comprehension.json", "--out-dir", f"{rel}/failure_analysis",
        "--label", f"MDAnalysis full-1032 {cell}",
    ], worktree)


def upstream_after(worktree: Path, cell: str) -> None:
    baseline = worktree / (
        "experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.json"
    )
    command = [
        str(PYTHON), "experiments/mdanalysis/run_pass_to_pass.py",
        "--experiment-root", "experiments/mdanalysis", "--phase", "after",
        "--cell", cell, "--out-dir", f"experiments/mdanalysis/docs/full_1032/{cell}",
        "--baseline", str(baseline),
    ]
    run(command, worktree)


def copy_result(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def wait_for_priority_repositories(priority_dir: Path) -> None:
    required = {"mir_eval": "mir_eval_complete_2x2",
                "thumbnailator": "thumbnailator_complete_2x2",
                "tslearn": "tslearn_complete_full235"}
    while True:
        pending = [repo for repo, job in required.items()
                   if (read_json(priority_dir / f"{repo}_pipeline_watchdog.state.json")
                       .get("jobs", {}).get(job, {}).get("status")) != "succeeded"]
        if not pending:
            return
        print(f"MDAnalysis deferred behind priority repositories: {', '.join(pending)}", flush=True)
        time.sleep(30)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-worktree", required=True, type=Path)
    parser.add_argument("--source-seed", required=True, type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    if not args.prepare_only:
        # Priority repositories are now admitted concurrently. The old outer
        # waiter checks tslearn only; retain it and add the full admission gate
        # here, before any MDAnalysis build, test, or paid generation starts.
        priority_dir = Path(__file__).resolve().parents[2].parent / "GRAIL_rdpro_puzzle_aideal/experiments/external"
        wait_for_priority_repositories(priority_dir)
    freeze = args.freeze_worktree.resolve()
    seed = args.source_seed.resolve()
    if git(freeze, "branch", "--show-current").stdout.strip() != FREEZE_BRANCH:
        raise RuntimeError(f"freeze worktree must be {FREEZE_BRANCH}")

    build_tools = freeze / "experiments/mdanalysis/.aideal_build_tools"
    ensure_source(seed, freeze, "freeze", build_tools)
    env = dict(os.environ, PYTHONPATH=str(freeze / "grail-agent/src"))
    run([
        str(PYTHON), "experiments/mdanalysis/validate_full_surface_setup.py",
        "--root", str(freeze),
    ], freeze, env=env)
    if args.prepare_only:
        print("static preparation complete; no LLM was started", flush=True)
        return 0

    wait_for_generation(freeze)
    validate_generated_readme(freeze)
    state = freeze / "experiments/mdanalysis/.aideal_exec/readme_generation_state.json"
    snapshot = freeze / "experiments/mdanalysis/docs/full_1032/A2/readme_generation_state.json"
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(state, snapshot)
    commit_push(
        freeze, FREEZE_BRANCH, "Freeze MDAnalysis full-1032 generated README",
        ["experiments/mdanalysis/docs/full_1032/A2",
         "experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.json",
         "experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.md",
         "experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.xml",
         "experiments/mdanalysis/docs/full_1032/setup/PASS_TO_PASS_BEFORE.log"],
    )
    freeze_head = git(freeze, "rev-parse", "HEAD").stdout.strip()
    parent = freeze.parent
    worktrees: dict[str, Path] = {}

    for cell in ("A1", "A2"):
        branch = f"aideal/mdanalysis-full1032-{cell}"
        wt = ensure_worktree(freeze, branch, parent / f"GRAIL_mdanalysis_full1032_{cell}", freeze_head)
        ensure_source(seed, wt, cell, build_tools)
        worktrees[cell] = wt
    run_supervised(
        freeze / "experiments/mdanalysis/docs/full_1032/setup/baseline_watchdog.yaml"
    )
    for cell in ("A1", "A2"):
        wt = worktrees[cell]
        analyze(wt, cell)
        commit_push(
            wt, f"aideal/mdanalysis-full1032-{cell}",
            f"Complete MDAnalysis full-1032 {cell} zero-round evaluation",
            [f"experiments/mdanalysis/docs/full_1032/{cell}",
             f"experiments/mdanalysis/logs/full_1032/{cell}",
             f"experiments/mdanalysis/docs/full_1032/setup/environment_{cell}.txt"],
        )

    for cell, parent_cell in (("B1", "A1"), ("B2", "A2")):
        start = git(worktrees[parent_cell], "rev-parse", "HEAD").stdout.strip()
        branch = f"aideal/mdanalysis-full1032-{cell}"
        wt = ensure_worktree(freeze, branch, parent / f"GRAIL_mdanalysis_full1032_{cell}", start)
        ensure_source(seed, wt, cell, build_tools)
        worktrees[cell] = wt
        if cell == "B2":
            source_doc = wt / "experiments/mdanalysis/docs/full_1032/A2/LLM_readme.md"
            target_doc = wt / "experiments/mdanalysis/docs/full_1032/B2/LLM_readme.md"
            if not target_doc.exists():
                target_doc.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_doc, target_doc)

    run_supervised(
        freeze / "experiments/mdanalysis/docs/full_1032/setup/repair_watchdog.yaml"
    )
    for cell in ("B1", "B2"):
        wt = worktrees[cell]
        analyze(wt, cell)
        upstream_after(wt, cell)
        commit_push(
            wt, f"aideal/mdanalysis-full1032-{cell}",
            f"Complete MDAnalysis full-1032 {cell} repaired evaluation",
            [f"experiments/mdanalysis/docs/full_1032/{cell}",
             f"experiments/mdanalysis/logs/full_1032/{cell}",
             f"experiments/mdanalysis/docs/full_1032/setup/environment_{cell}.txt"],
        )

    analysis_branch = "aideal/mdanalysis-full1032-analysis"
    analysis = ensure_worktree(
        freeze, analysis_branch, parent / "GRAIL_mdanalysis_full1032_analysis", freeze_head
    )
    combined = analysis / "experiments/mdanalysis/docs/full_1032/combined"
    for cell in CELLS:
        copy_result(
            worktrees[cell] / f"experiments/mdanalysis/docs/full_1032/{cell}/comprehension.json",
            combined / f"{cell}.json",
        )
    run([
        str(PYTHON), "experiments/mdanalysis/compare_full_2x2.py",
        "--a1", str(combined / "A1.json"), "--a2", str(combined / "A2.json"),
        "--b1", str(combined / "B1.json"), "--b2", str(combined / "B2.json"),
        "--manifest", "experiments/mdanalysis/docs/full_1032/api_manifest.json",
        "--out-dir", str(combined),
    ], analysis)
    commit_push(
        analysis, analysis_branch, "Compare MDAnalysis full-1032 A1/A2/B1/B2",
        ["experiments/mdanalysis/docs/full_1032/combined"],
    )
    print("MDAnalysis full-1032 A1/A2/B1/B2 complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
