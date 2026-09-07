#!/usr/bin/env python3
"""Idempotent end-to-end A1/A2/B1/B2 pipeline for a frozen external repo."""

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

import yaml

from experiments.external.run_condition_watchdog import Supervisor


PYTHON = Path("/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python")
MAVEN = Path("/Users/clockorangezoe/Documents/EnvUtilities/apache-maven-3.9.4/bin/mvn")
JAVA8 = Path("/Library/Java/JavaVirtualMachines/jdk-1.8.jdk/Contents/Home")

REPOS = {
    "mir_eval": {
        "label": "mir_eval",
        "freeze_branch": "aideal/mir_eval-freeze",
        "commit": "fe73b3533737814f83dbd9739f06e90f5f82f758",
        "kind": "python",
    },
    "thumbnailator": {
        "label": "Thumbnailator",
        "freeze_branch": "aideal/thumbnailator-freeze",
        "commit": "c9d99613878bbbf1f4d9369585b4cb5352c3b474",
        "kind": "java",
    },
}


def run(command: list[str], cwd: Path, *, check: bool = True,
        env: dict | None = None) -> subprocess.CompletedProcess:
    print(f"[{time.strftime('%H:%M:%S')}] {cwd.name}: {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                          check=check, env=env)


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd, check=check)


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def generation_complete(path: Path) -> bool:
    data = read_json(path)
    expected = int(data.get("api_entries", 0) or 0)
    return (expected > 0 and data.get("generated_ok") == expected
            and data.get("fallback_to_skeleton") == 0
            and bool(data.get("generation_fingerprint")))


def wait_for_watchdog_job(state_path: Path, job_id: str) -> None:
    """Wait for a separately supervised prerequisite without duplicating it."""
    state_path = state_path.resolve()
    while True:
        data = read_json(state_path)
        row = (data.get("jobs") or {}).get(job_id) or {}
        status = row.get("status")
        if status == "succeeded":
            print(f"[{time.strftime('%H:%M:%S')}] prerequisite {job_id} succeeded",
                  flush=True)
            return
        print(
            f"[{time.strftime('%H:%M:%S')}] waiting for prerequisite "
            f"{job_id}: status={status or 'not-created'}",
            flush=True,
        )
        time.sleep(30)


def wait_for_generation(freeze: Path, repo: str) -> None:
    result = freeze / f"experiments/external/{repo}/docs/eval/A2/generation_result.json"
    plan = freeze / f"experiments/external/{repo}/docs/eval/A2/generation_watchdog.yaml"
    lock_path = plan.with_suffix(".watchdog.lock")
    while not generation_complete(result):
        # If the original generation supervisor itself died, acquire its lock
        # and resume the exact same plan. If it is alive, leave it alone.
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                pass
            else:
                if not plan.is_file():
                    raise FileNotFoundError(plan)
                print(f"[{time.strftime('%H:%M:%S')}] resuming stopped generation supervisor",
                      flush=True)
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
                supervisor = Supervisor(plan)
                if supervisor.run() != 0:
                    raise RuntimeError(f"generation watchdog failed: {plan}")
        print(f"[{time.strftime('%H:%M:%S')}] waiting for complete {repo} README", flush=True)
        time.sleep(30)


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


def ensure_source(setup: Path, worktree: Path, repo: str, meta: dict, cell: str) -> Path:
    rel = Path(f"experiments/external/{repo}/source")
    source = worktree / rel
    if not (source / ".git").exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--shared", str(setup / rel), str(source)], worktree)
        git(source, "checkout", "--detach", meta["commit"])
    actual = git(source, "rev-parse", "HEAD").stdout.strip()
    if actual != meta["commit"]:
        raise RuntimeError(f"{repo} {cell} source {actual}, expected {meta['commit']}")

    if meta["kind"] == "python":
        venv = source / ".venv"
        if not (venv / "bin/python").exists():
            run([str(PYTHON), "-m", "venv", "--system-site-packages", str(venv)], worktree)
            run([str(venv / "bin/pip"), "install", "--no-deps", "-e", str(source)], worktree)
            run([str(venv / "bin/pip"), "install", "pytest-cov", "pytest-mpl"], worktree)
        freeze_text = run([str(venv / "bin/pip"), "freeze"], worktree).stdout
        inventory = (
            f"cell={cell}\nupstream_commit={meta['commit']}\n"
            f"python={venv / 'bin/python'}\n" + freeze_text)
    else:
        jar = source / "target/thumbnailator-0.4.21.jar"
        if not jar.exists():
            env = dict(os.environ, JAVA_HOME=str(JAVA8))
            run([str(MAVEN), "-q", "package", "javadoc:javadoc"], source, env=env)
        inventory = (
            f"cell={cell}\nupstream_commit={meta['commit']}\nJAVA_HOME={JAVA8}\n"
            f"maven={MAVEN}\njar_sha256={hashlib.sha256(jar.read_bytes()).hexdigest()}\n")
    inventory_path = worktree / f"experiments/external/{repo}/docs/eval/setup/environment_{cell}.txt"
    write_text_atomic(inventory_path, inventory)
    return inventory_path


def make_job(repo: str, worktree: Path, branch: str, cell: str,
             inventory: Path, *, repair: bool = False) -> dict:
    rel = f"experiments/external/{repo}"
    config = f"{rel}/configs/aideal_{cell}.yaml"
    manifest = "docs/eval/api_manifest.json"
    env = {"PYTHONPATH": str(worktree / "grail-agent/src")}
    if not repair:
        doc = {"A1": "original", "A2": "aideal",
               "B1": "original+aideal", "B2": "aideal"}[cell]
        command = [str(PYTHON), "-m", "aideal.cli", "--config", config,
                   "comprehension", "--execute", "--show-code", "--doc", doc,
                   "--doc-scope", "relevant", "--manifest", manifest,
                   "--max-fix-rounds", "0", "--resume", "--timeout", "600"]
        return {
            "id": f"{repo}_{cell}_zero", "cwd": str(worktree), "branch": branch,
            "environment_inventory": str(inventory.relative_to(worktree)), "env": env,
            "command": command, "result": f"{rel}/docs/eval/{cell}/comprehension.json",
            "complete": {"kind": "json_metrics_no_transient"},
            "max_runtime_seconds": 172800, "max_restarts": 0,
        }
    source_cell = "A1" if cell == "B1" else "A2"
    doc = "original+aideal" if cell == "B1" else "aideal"
    command = [str(PYTHON), "-m", "aideal.cli", "--config", config, "fix-docs",
               "--from-results", f"docs/eval/{source_cell}/comprehension.json",
               "--deep-dive-first", "--doc-rounds", "5", "--doc-stuck", "2",
               "--retry-rounds", "0", "--doc", doc, "--doc-scope", "relevant",
               "--manifest", manifest, "--report", f"docs/eval/{cell}/docfix.json",
               "--deep-dive-out", f"docs/eval/{cell}/deepdive", "--timeout", "600"]
    if cell == "B1":
        command.append("--create-missing")
    return {
        "id": f"{repo}_{cell}_repair", "cwd": str(worktree), "branch": branch,
        "environment_inventory": str(inventory.relative_to(worktree)), "env": env,
        "command": command, "result": f"{rel}/docs/eval/{cell}/docfix_command.json",
        "complete": {"kind": "docfix", "path": f"{rel}/docs/eval/{cell}/docfix.json"},
        "max_runtime_seconds": 259200, "max_restarts": 0,
    }


def run_plan(setup: Path, repo: str, name: str, jobs: list[dict]) -> None:
    plan_path = setup.parent / f"{repo}_{name}_watchdog.yaml"
    plan = {
        "version": 1, "max_parallel": 3, "retry_delay_seconds": 300,
        "env": {
            "AIDEAL_GOOGLE_MIN_INTERVAL_S": "3",
            "AIDEAL_GOOGLE_RATE_STATE": "/tmp/aideal_google_rate_gate.txt",
            "AIDEAL_GOOGLE_REQUEST_TIMEOUT_S": "300",
            "AIDEAL_GOOGLE_MAX_RETRIES": "2",
        },
        "jobs": jobs,
    }
    write_text_atomic(plan_path, yaml.safe_dump(plan, sort_keys=False))
    supervisor = Supervisor(plan_path)
    if supervisor.run() != 0:
        raise RuntimeError(f"watchdog plan failed: {plan_path}")


def analyze(worktree: Path, repo: str, cell: str) -> None:
    rel = f"experiments/external/{repo}"
    run([str(PYTHON), "experiments/external/analyze_failures.py",
         f"{rel}/docs/eval/{cell}/comprehension.json", "--out-dir",
         f"{rel}/docs/eval/{cell}/failure_analysis", "--label", f"{repo} {cell}"],
        worktree)


def upstream_after(worktree: Path, repo: str, meta: dict, cell: str) -> None:
    source = worktree / f"experiments/external/{repo}/source"
    if meta["kind"] == "python":
        proc = run(["../.venv/bin/python", "-m", "pytest", "-q"], source / "tests",
                   check=False, env=dict(os.environ, MPLBACKEND="Agg",
                                         OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"))
    else:
        proc = run([str(MAVEN), "-q", "test"], source, check=False,
                   env=dict(os.environ, JAVA_HOME=str(JAVA8)))
    text = (f"# {repo} PASS_TO_PASS after {cell}\n\n- Exit code: {proc.returncode}\n"
            f"- Source: `{meta['commit']}`\n\n```text\n"
            f"{(proc.stdout + proc.stderr)[-12000:]}\n```\n")
    out = worktree / f"experiments/external/{repo}/docs/eval/{cell}/PASS_TO_PASS_AFTER.md"
    write_text_atomic(out, text)
    if proc.returncode != 0:
        raise RuntimeError(f"{repo} upstream tests failed after {cell}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", choices=sorted(REPOS))
    parser.add_argument("--freeze-worktree", required=True, type=Path)
    parser.add_argument("--wait-for-watchdog-state", type=Path)
    parser.add_argument("--wait-for-job")
    args = parser.parse_args()
    if bool(args.wait_for_watchdog_state) != bool(args.wait_for_job):
        parser.error("--wait-for-watchdog-state and --wait-for-job are required together")
    repo = args.repo
    meta = REPOS[repo]
    setup = args.freeze_worktree.resolve()
    if args.wait_for_watchdog_state:
        wait_for_watchdog_job(args.wait_for_watchdog_state, args.wait_for_job)
    if git(setup, "branch", "--show-current").stdout.strip() != meta["freeze_branch"]:
        raise RuntimeError(f"freeze worktree must be {meta['freeze_branch']}")

    wait_for_generation(setup, repo)
    rel = f"experiments/external/{repo}"
    state = setup / f"{rel}/.aideal_exec/readme_generation_state.json"
    if state.exists():
        snapshot = setup / f"{rel}/docs/eval/A2/readme_generation_state.json"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(state, snapshot)
    commit_push(setup, meta["freeze_branch"], f"Freeze {meta['label']} generated README",
                [f"{rel}/docs/eval/A2"])
    freeze_head = git(setup, "rev-parse", "HEAD").stdout.strip()
    parent = setup.parent

    worktrees = {}
    inventories = {}
    for cell in ("A1", "A2"):
        branch = f"aideal/{repo}-{cell}"
        wt = ensure_worktree(setup, branch, parent / f"GRAIL_{repo}_{cell}", freeze_head)
        worktrees[cell] = wt
        inventories[cell] = ensure_source(setup, wt, repo, meta, cell)
    run_plan(setup, repo, "baselines", [
        make_job(repo, worktrees[cell], f"aideal/{repo}-{cell}", cell, inventories[cell])
        for cell in ("A1", "A2")])
    for cell in ("A1", "A2"):
        analyze(worktrees[cell], repo, cell)
        commit_push(worktrees[cell], f"aideal/{repo}-{cell}",
                    f"Complete {meta['label']} {cell} zero-round evaluation",
                    [f"{rel}/docs/eval/{cell}", f"{rel}/logs/{cell}",
                     f"{rel}/docs/eval/setup/environment_{cell}.txt"])

    for cell, parent_cell in (("B1", "A1"), ("B2", "A2")):
        start = git(worktrees[parent_cell], "rev-parse", "HEAD").stdout.strip()
        branch = f"aideal/{repo}-{cell}"
        wt = ensure_worktree(setup, branch, parent / f"GRAIL_{repo}_{cell}", start)
        worktrees[cell] = wt
        inventories[cell] = ensure_source(setup, wt, repo, meta, cell)
        if cell == "B2":
            source_doc = wt / f"{rel}/docs/eval/A2/LLM_readme.md"
            target_doc = wt / f"{rel}/docs/eval/B2/LLM_readme.md"
            target_doc.parent.mkdir(parents=True, exist_ok=True)
            if not target_doc.exists():
                shutil.copy2(source_doc, target_doc)

    repair_jobs = [
        make_job(repo, worktrees[cell], f"aideal/{repo}-{cell}", cell,
                 inventories[cell], repair=True)
        for cell in ("B1", "B2")]
    zero_jobs = []
    for cell in ("B1", "B2"):
        job = make_job(repo, worktrees[cell], f"aideal/{repo}-{cell}", cell,
                       inventories[cell])
        job["depends_on"] = [f"{repo}_{cell}_repair"]
        zero_jobs.append(job)
    run_plan(setup, repo, "repairs", repair_jobs + zero_jobs)
    for cell in ("B1", "B2"):
        analyze(worktrees[cell], repo, cell)
        upstream_after(worktrees[cell], repo, meta, cell)
        commit_push(worktrees[cell], f"aideal/{repo}-{cell}",
                    f"Complete {meta['label']} {cell} repaired evaluation",
                    [f"{rel}/docs/eval/{cell}", f"{rel}/logs/{cell}",
                     f"{rel}/docs/eval/setup/environment_{cell}.txt"])
    print(f"{repo}: complete A1/A2/B1/B2", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
