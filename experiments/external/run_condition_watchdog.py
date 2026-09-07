#!/usr/bin/env python3
"""Dependency-aware, crash-resuming supervisor for isolated AIDEAL worktrees.

The plan is YAML. Each job has its own cwd/worktree, command, durable result,
completion predicate, and optional post-success Git commands. The supervisor
may itself be restarted: succeeded jobs remain succeeded, interrupted jobs are
returned to pending, and AIDEAL's fingerprinted ``--resume`` checkpoint does
the per-API recovery.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import time

import yaml


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def command_list(value) -> list[str]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    if isinstance(value, str):
        return shlex.split(value)
    raise ValueError(f"command must be a string list, got {value!r}")


def result_path(job: dict, plan_dir: Path) -> Path:
    cwd = Path(job["cwd"])
    if not cwd.is_absolute():
        cwd = (plan_dir / cwd).resolve()
    result = Path(job.get("result", ".aideal_exec/watchdog.stdout"))
    return result if result.is_absolute() else cwd / result


def completion(job: dict, candidate: Path, plan_dir: Path) -> tuple[bool, str]:
    spec = job.get("complete", {"kind": "exit_zero"}) or {}
    kind = spec.get("kind", "exit_zero")
    target = Path(spec.get("path", candidate))
    if not target.is_absolute():
        cwd = Path(job["cwd"])
        if not cwd.is_absolute():
            cwd = (plan_dir / cwd).resolve()
        target = cwd / target
    if kind == "exit_zero":
        return True, "exit zero"
    if kind == "file_nonempty":
        ok = target.is_file() and target.stat().st_size > 0
        return ok, f"file_nonempty={ok}: {target}"
    data = load_json(target)
    if kind == "json_metrics_no_transient":
        metrics = data.get("metrics") or {}
        run = data.get("run") or {}
        expected = int(run.get("api_count", 0) or 0)
        transient = sorted(name for name, row in metrics.items()
                           if row.get("error_category") == "llm-error")
        fingerprinted = bool(run.get("fingerprint_components"))
        ok = expected > 0 and len(metrics) == expected and not transient and fingerprinted
        return ok, (f"metrics={len(metrics)}/{expected}, transient={len(transient)}, "
                    f"fingerprinted={fingerprinted}")
    if kind == "docfix":
        apis = data.get("apis") or {}
        unfinished = [name for name, row in apis.items()
                      if str(row.get("status", "")).startswith(("in-progress", "llm-error"))]
        attempted = data.get("attempted")
        processed = data.get("processed")
        ok = (attempted is not None and processed == attempted
              and not unfinished and not data.get("blocked"))
        return ok, (f"processed={processed}/{attempted}, unfinished={len(unfinished)}, "
                    f"blocked={bool(data.get('blocked'))}")
    raise ValueError(f"unknown completion kind {kind!r}")


class Supervisor:
    def __init__(self, plan_path: Path, state_path: Path | None = None):
        self.plan_path = plan_path.resolve()
        self.plan_bytes = self.plan_path.read_bytes()
        self.plan_sha = hashlib.sha256(self.plan_bytes).hexdigest()
        self.plan = yaml.safe_load(self.plan_bytes) or {}
        self.plan_dir = self.plan_path.parent
        self.state_path = (state_path or self.plan_path.with_suffix(".state.json")).resolve()
        self.log_path = self.state_path.with_suffix(".log")
        self.jobs = {job["id"]: job for job in self.plan.get("jobs", [])}
        if not self.jobs or len(self.jobs) != len(self.plan.get("jobs", [])):
            raise ValueError("plan jobs need unique non-empty ids")
        self.max_parallel = int(self.plan.get("max_parallel", 3))
        self.retry_delay = int(self.plan.get("retry_delay_seconds", 300))
        self.active: dict[str, dict] = {}
        self.stopping = False
        self.state = load_json(self.state_path)
        if self.state and self.state.get("plan_sha256") != self.plan_sha:
            raise RuntimeError(
                f"plan changed since {self.state_path}; use a new state path to avoid mixing runs")
        if not self.state:
            self.state = {"schema": 1, "plan": str(self.plan_path),
                          "plan_sha256": self.plan_sha, "jobs": {}}
        for job_id in self.jobs:
            row = self.state["jobs"].setdefault(
                job_id, {"status": "pending", "attempts": 0})
            if row.get("status") == "running":
                row["status"] = "pending"
                row["recovered_after_supervisor_restart"] = True
        self._save()

    def log(self, message: str) -> None:
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        print(line, flush=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")

    def _save(self) -> None:
        self.state["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        atomic_json(self.state_path, self.state)

    def cwd(self, job: dict) -> Path:
        path = Path(job["cwd"])
        return path.resolve() if path.is_absolute() else (self.plan_dir / path).resolve()

    def env(self, job: dict) -> dict[str, str]:
        env = dict(os.environ)
        shared = self.plan.get("env", {}) or {}
        env.update({str(k): str(v) for k, v in shared.items()})
        env.update({str(k): str(v) for k, v in (job.get("env", {}) or {}).items()})
        env.setdefault("AIDEAL_GOOGLE_MIN_INTERVAL_S", "3")
        env.setdefault("AIDEAL_GOOGLE_RATE_STATE", "/tmp/aideal_google_rate_gate.txt")
        env.setdefault("AIDEAL_GOOGLE_REQUEST_TIMEOUT_S", "300")
        env.setdefault("AIDEAL_GOOGLE_MAX_RETRIES", "2")
        env.setdefault("PYTHONUNBUFFERED", "1")
        if not env.get("AIDEAL_ENV_FINGERPRINT"):
            inventory = str(job.get("environment_inventory", ""))
            inventory_path = Path(inventory) if inventory else None
            if inventory_path and not inventory_path.is_absolute():
                inventory_path = self.cwd(job) / inventory_path
            if inventory_path and inventory_path.is_file():
                env["AIDEAL_ENV_FINGERPRINT"] = hashlib.sha256(
                    inventory_path.read_bytes()).hexdigest()
            else:
                raise RuntimeError(
                    f"{job['id']} needs environment_inventory or AIDEAL_ENV_FINGERPRINT")
        return env

    def preflight(self) -> None:
        for job_id, job in self.jobs.items():
            unknown = set(job.get("depends_on", [])) - set(self.jobs)
            if unknown:
                raise ValueError(f"{job_id} has unknown dependencies: {sorted(unknown)}")
            cwd = self.cwd(job)
            if not cwd.is_dir():
                raise FileNotFoundError(f"{job_id} cwd missing: {cwd}")
            expected_branch = job.get("branch")
            if expected_branch:
                proc = subprocess.run(
                    ["git", "-C", str(cwd), "branch", "--show-current"],
                    text=True, capture_output=True, check=False)
                actual = proc.stdout.strip()
                if actual != expected_branch:
                    raise RuntimeError(
                        f"{job_id} expected branch {expected_branch!r}, found {actual!r}")
            command_list(job["command"])
            self.env(job)

    def eligible(self, job_id: str, now: float) -> bool:
        row = self.state["jobs"][job_id]
        if row.get("status") not in {"pending", "retry"}:
            return False
        if float(row.get("retry_at", 0) or 0) > now:
            return False
        if any(self.state["jobs"][dep].get("status") != "succeeded"
               for dep in self.jobs[job_id].get("depends_on", [])):
            return False
        cwd = str(self.cwd(self.jobs[job_id]))
        return all(str(info["cwd"]) != cwd for info in self.active.values())

    def launch(self, job_id: str) -> None:
        job = self.jobs[job_id]
        cwd = self.cwd(job)
        final = result_path(job, self.plan_dir)
        final.parent.mkdir(parents=True, exist_ok=True)
        tmp = final.with_suffix(final.suffix + ".tmp")
        stderr = final.with_suffix(final.suffix + ".stderr.log")
        stdout_stream = tmp.open("w", encoding="utf-8")
        stderr_stream = stderr.open("a", encoding="utf-8")
        command = command_list(job["command"])
        proc = subprocess.Popen(
            command, cwd=cwd, env=self.env(job), text=True,
            stdout=stdout_stream, stderr=stderr_stream, start_new_session=True)
        row = self.state["jobs"][job_id]
        row.update({"status": "running", "pid": proc.pid,
                    "attempts": int(row.get("attempts", 0)) + 1,
                    "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "result": str(final)})
        self.active[job_id] = {
            "proc": proc, "cwd": cwd, "final": final, "tmp": tmp,
            "stdout": stdout_stream, "stderr": stderr_stream,
            "started": time.time(),
        }
        self.log(f"START {job_id} attempt={row['attempts']} pid={proc.pid}")
        self._save()

    def finish(self, job_id: str) -> None:
        info = self.active.pop(job_id)
        proc = info["proc"]
        info["stdout"].close()
        info["stderr"].close()
        row = self.state["jobs"][job_id]
        rc = proc.returncode
        ok, detail = (False, f"exit={rc}")
        if rc == 0:
            ok, detail = completion(self.jobs[job_id], info["tmp"], self.plan_dir)
        if ok:
            info["tmp"].replace(info["final"])
            try:
                for command in self.jobs[job_id].get("on_success", []) or []:
                    subprocess.run(command_list(command), cwd=info["cwd"],
                                   env=self.env(self.jobs[job_id]), check=True)
            except Exception as exc:
                ok, detail = False, f"post-success failed: {type(exc).__name__}: {exc}"
        if ok:
            row.update({"status": "succeeded", "finished_at": time.strftime(
                "%Y-%m-%d %H:%M:%S"), "detail": detail, "pid": None})
            self.log(f"DONE {job_id}: {detail}")
        else:
            max_restarts = int(self.jobs[job_id].get("max_restarts", 0) or 0)
            attempts = int(row.get("attempts", 0))
            terminal = max_restarts > 0 and attempts > max_restarts
            row.update({"status": "failed" if terminal else "retry",
                        "retry_at": time.time() + self.retry_delay,
                        "detail": detail, "pid": None})
            self.log(f"{'FAILED' if terminal else 'RETRY'} {job_id}: {detail}")
        self._save()

    def run(self) -> int:
        self.preflight()
        self.state["status"] = "running"
        self._save()
        while not self.stopping:
            now = time.time()
            for job_id, info in list(self.active.items()):
                max_runtime = int(self.jobs[job_id].get("max_runtime_seconds", 0) or 0)
                if max_runtime and now - info["started"] > max_runtime:
                    self.log(f"TIMEOUT {job_id}; terminating process group")
                    os.killpg(info["proc"].pid, signal.SIGTERM)
                if info["proc"].poll() is not None:
                    self.finish(job_id)
            for job_id in self.jobs:
                if len(self.active) >= self.max_parallel:
                    break
                if self.eligible(job_id, now):
                    self.launch(job_id)
            statuses = [row.get("status") for row in self.state["jobs"].values()]
            if statuses and all(status == "succeeded" for status in statuses):
                self.state["status"] = "succeeded"
                self._save()
                self.log("ALL JOBS SUCCEEDED")
                return 0
            if not self.active and not any(status in {"pending", "retry"} for status in statuses):
                self.state["status"] = "failed"
                self._save()
                return 1
            self.state["heartbeat_epoch"] = time.time()
            self._save()
            time.sleep(2)
        return 130

    def stop(self, *_args) -> None:
        self.stopping = True
        for info in self.active.values():
            try:
                os.killpg(info["proc"].pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        self.state["status"] = "interrupted"
        self._save()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--state", type=Path)
    parser.add_argument("--keep-awake", action="store_true")
    args = parser.parse_args()
    lock_path = args.plan.resolve().with_suffix(".watchdog.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = lock_path.open("a+")
    try:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another supervisor holds {lock_path}")
    supervisor = Supervisor(args.plan, args.state)
    signal.signal(signal.SIGINT, supervisor.stop)
    signal.signal(signal.SIGTERM, supervisor.stop)
    awake = None
    if args.keep_awake and shutil.which("caffeinate"):
        awake = subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])
    try:
        return supervisor.run()
    finally:
        if awake and awake.poll() is None:
            awake.terminate()


if __name__ == "__main__":
    sys.exit(main())
