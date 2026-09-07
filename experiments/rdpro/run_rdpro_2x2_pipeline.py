#!/usr/bin/env python3
"""Prepare and supervise the protocol-valid RDPro A1/A2/B1/B2 experiment.

The public commands are deliberately split:

* ``plan`` is read-only;
* ``prepare`` creates isolated branches/worktrees and a watchdog plan, but
  never invokes an LLM;
* ``run`` requires ``--confirm-paid-llm`` and resumes the generated plan.

The watchdog provides process-level restart recovery. AIDEAL comprehension and
docfix provide per-API checkpoints, so restarting this coordinator does not
repeat completed Gemini work under the same experiment fingerprint.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import yaml


GEOAI = Path("/Users/clockorangezoe/Documents/phd_projects/code/geoAI")
RUNNER = GEOAI / "GRAIL_rdpro_2x2_runner"
HISTORICAL_A1 = GEOAI / "GRAIL_rdpro_A1"
PYTHON = Path("/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python")
MAVEN = Path("/Users/clockorangezoe/Documents/EnvUtilities/apache-maven-3.9.4/bin/mvn")
JAVA8 = Path("/Library/Java/JavaVirtualMachines/jdk-1.8.jdk/Contents/Home")

BEAST_REVISION = "547f7f912131a8032f6b5d26991415a5faf05cef"
MANIFEST_SHA256 = "1dc1f1c758ae9829c2654e853899603f12f1d7174afdfeffd9edd1f29dde14e1"
MANIFEST_COUNT = 88
A1_DOCUMENT_SHA256 = "f64779c18f593613644e8628cba19469d1b618b9cfb7ce039d6376075a3dfc67"
A2_DOCUMENT_SHA256 = "8963aef19580d73d341661917fe480c2f72babfc56718507b6bf483d47ea89fe"
A1_START = "153aa994efdea0ac4428be378ef4da62e0b9e80d"
A2_START = "092bef5e4dff275f8de5b328b469012eaef902c0"
RATE_STATE = "/tmp/aideal_rdpro_google_rate_gate.txt"

CELLS = {
    "A1": {
        "branch": "aideal/rdpro-final-a1-shared88",
        "path": GEOAI / "GRAIL_rdpro_final_A1",
        "start": A1_START,
        "doc": "original",
    },
    "A2": {
        "branch": "aideal/rdpro-final-a2-shared88",
        "path": GEOAI / "GRAIL_rdpro_final_A2",
        "start": A2_START,
        "doc": "aideal",
    },
    "B1": {
        "branch": "aideal/rdpro-final-b1-shared88",
        "path": GEOAI / "GRAIL_rdpro_final_B1",
        "start": A1_START,
        "doc": "original+aideal",
    },
    "B2": {
        "branch": "aideal/rdpro-final-b2-shared88",
        "path": GEOAI / "GRAIL_rdpro_final_B2",
        "start": A2_START,
        "doc": "aideal",
    },
}

FIXTURE_HASHES = {
    "../../../GRAIL/grail-agent/examples/fixtures/nldas_boston_30m.tif":
        "d1583296084ff5511743f4b3c0cf6307313e436410771503e42e097c94e8f407",
    "../../../GRAIL/grail-agent/examples/fixtures/Boston_Neighborhood_Boundaries_sample_grail.shp":
        "2595d72266b1b3decdb8989e679d093996240cf4b891b3c09f37d9372a6a6cd6",
    "../../../GRAIL/grail-agent/examples/fixtures/Boston_Neighborhood_Boundaries_sample_grail.dbf":
        "9ce6ca2e7cd0f94cf68b3cdf676071a22d402bea980cb5997354afd08bd41b47",
    "../../../GRAIL/grail-agent/examples/fixtures/Boston_Neighborhood_Boundaries_sample_grail.shx":
        "ed102bdd96060de98de2d6039aae78b0a00805d5d680947f2bd4ddcd03e0bd6b",
    "../../../GRAIL/grail-agent/examples/fixtures/Boston_Neighborhood_Boundaries_sample_grail.prj":
        "a02a27b1d1982c8516d83398e85a3c8b1aef1713c13ef4d84d7bde17430c07c4",
    "beast/raptor/src/test/resources/rasters/MYD11A1.A2002185.h09v06.006.2015146150958.hdf":
        "95f00c649b46985e51d13695e7c20fadf0ea6269cd50f8f163db2dba4dfbe2d0",
}


def run(command: list[str], cwd: Path, *, check: bool = True,
        env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    print(f"[{time.strftime('%H:%M:%S')}] {cwd.name}: {' '.join(command)}", flush=True)
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                          check=check, env=env)


def git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return run(["git", *args], cwd, check=check)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, value: dict) -> None:
    atomic_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_hash(names: list[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def validate_manifest(path: Path) -> dict:
    data = load_json(path)
    names = data.get("apis") or []
    if len(names) != MANIFEST_COUNT or len(set(names)) != MANIFEST_COUNT:
        raise RuntimeError(f"manifest needs 88 unique APIs, found {len(names)}/{len(set(names))}")
    actual = manifest_hash(names)
    if actual != MANIFEST_SHA256:
        raise RuntimeError(f"manifest inventory hash {actual}, expected {MANIFEST_SHA256}")
    return data


def validate_result(path: Path, expected_doc: str) -> dict:
    data = load_json(path)
    run_row = data.get("run") or {}
    coverage = data.get("coverage") or {}
    metrics = data.get("metrics") or {}
    executed = int(run_row.get("api_count") or coverage.get("executed") or 0)
    manifested = int(run_row.get("manifest_api_count")
                     or (run_row.get("manifest") or {}).get("apis") or executed)
    errors = []
    if data.get("check") != "comprehension" or data.get("mode") != "execute":
        errors.append("not an execution-grounded comprehension result")
    if data.get("doc_source") != expected_doc:
        errors.append(f"doc_source={data.get('doc_source')!r}, expected {expected_doc!r}")
    if executed != MANIFEST_COUNT or manifested != MANIFEST_COUNT:
        errors.append(f"API counts executed/manifest={executed}/{manifested}, expected 88/88")
    if len(metrics) != MANIFEST_COUNT:
        errors.append(f"metrics={len(metrics)}, expected 88")
    if run_row.get("manifest_sha256") != MANIFEST_SHA256:
        errors.append(f"manifest_sha256={run_row.get('manifest_sha256')!r}")
    if run_row.get("doc_scope") != "relevant":
        errors.append(f"doc_scope={run_row.get('doc_scope')!r}, expected 'relevant'")
    if int(run_row.get("max_fix_rounds", -1)) != 0:
        errors.append(f"max_fix_rounds={run_row.get('max_fix_rounds')!r}, expected 0")
    if data.get("sample_data_warnings"):
        errors.append(f"sample_data_warnings={data['sample_data_warnings']!r}")
    transient = sorted(name for name, row in metrics.items()
                       if row.get("error_category") == "llm-error")
    if transient:
        errors.append(f"transient LLM failures remain: {transient}")
    if errors:
        raise RuntimeError(f"invalid result {path}: " + "; ".join(errors))
    return data


def relevant_document_hash(worktree: Path, doc_source: str) -> str:
    """Reproduce the exact document hash used by comprehension, without an LLM."""
    agent_src = str(RUNNER / "grail-agent/src")
    if agent_src not in sys.path:
        sys.path.insert(0, agent_src)
    from aideal.config import load_config
    from aideal.doc_checks import _comprehension_inventory

    cfg = load_config(worktree / "experiments/rdpro/configs/aideal.yaml")
    names = validate_manifest(
        worktree / "experiments/rdpro/docs/api_manifest_shared.json")["apis"]
    inventory, shared, error = _comprehension_inventory(
        cfg, doc_source, manifest=names, full_doc=False, doc_scope="relevant")
    if error or shared is not None:
        raise RuntimeError(f"could not build relevant document inventory: {error}")
    payload = "\n\0\n".join(f"{entry.name}\n{entry.body}" for entry in inventory)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ensure_worktree(branch: str, path: Path, start: str) -> None:
    if path.exists():
        if not (path / ".git").exists():
            raise RuntimeError(f"refusing existing non-worktree path: {path}")
        actual = git(path, "branch", "--show-current").stdout.strip()
        if actual != branch:
            raise RuntimeError(f"{path} is branch {actual!r}, expected {branch!r}")
        return
    exists = git(RUNNER, "show-ref", "--verify", "--quiet",
                 f"refs/heads/{branch}", check=False).returncode == 0
    command = ["git", "worktree", "add"]
    if not exists:
        command.extend(["-b", branch])
    command.extend([str(path), branch if exists else start])
    run(command, RUNNER)


def corrected_config_text() -> str:
    source = RUNNER / "experiments/rdpro/configs/aideal.yaml"
    text = source.read_text(encoding="utf-8")
    replacements = {
        "- /Users/clockorangezoe/Documents/phd_projects/code/geoAI/RDPro/README.md":
            '- "beast/README.md"',
        "- /Users/clockorangezoe/Documents/phd_projects/code/geoAI/RDPro/doc":
            '- "beast/doc"',
        "../../../GRAIL_rdpro_A1/experiments/rdpro/beast/raptor/src/test/resources/rasters/"
        "MYD11A1.A2002185.h09v06.006.2015146150958.hdf":
            "beast/raptor/src/test/resources/rasters/"
            "MYD11A1.A2002185.h09v06.006.2015146150958.hdf",
    }
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"runner config no longer contains expected text: {old}")
        text = text.replace(old, new)
    return text


def ensure_beast(worktree: Path) -> Path:
    source = worktree / "experiments/rdpro/beast"
    seed = HISTORICAL_A1 / "experiments/rdpro/beast"
    if not (seed / ".git").exists():
        raise FileNotFoundError(f"pinned local Beast seed missing: {seed}")
    if not (source / ".git").exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--no-hardlinks", str(seed), str(source)], worktree)
        git(source, "checkout", "--detach", BEAST_REVISION)
    actual = git(source, "rev-parse", "HEAD").stdout.strip()
    if actual != BEAST_REVISION:
        raise RuntimeError(f"{source} is {actual}, expected {BEAST_REVISION}")
    dirty = git(source, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty:
        raise RuntimeError(f"pinned Beast source has tracked changes: {dirty}")
    return source


def validate_fixtures(worktree: Path) -> dict[str, str]:
    root = worktree / "experiments/rdpro"
    found = {}
    for relative, expected in FIXTURE_HASHES.items():
        path = (root / relative).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"fixture missing: {path}")
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"fixture hash mismatch: {path}: {actual} != {expected}")
        found[str(path)] = actual
    return found


def environment_inventory(cell: str, worktree: Path, fixtures: dict[str, str]) -> Path:
    out = worktree / f"experiments/rdpro/docs/eval/setup/environment_{cell}.json"
    data = {
        "cell": cell,
        "branch": CELLS[cell]["branch"],
        "worktree": str(worktree),
        "runner_commit": git(RUNNER, "rev-parse", "HEAD").stdout.strip(),
        "beast_revision": BEAST_REVISION,
        "beast_release": "beast-0.10.1",
        "manifest_api_count": MANIFEST_COUNT,
        "manifest_inventory_sha256": MANIFEST_SHA256,
        "doc_scope": "relevant",
        "final_snippet_fix_rounds": 0,
        "python": str(PYTHON),
        "maven": str(MAVEN),
        "java_home": str(JAVA8),
        "fixtures": fixtures,
    }
    atomic_json(out, data)
    return out


def prepare(plan_path: Path) -> Path:
    validate_manifest(HISTORICAL_A1 / "experiments/rdpro/docs/api_manifest_shared.json")
    validate_result(HISTORICAL_A1 / "experiments/rdpro/docs/comprehension_A1_original.json",
                    "original")
    for required in (PYTHON, MAVEN, JAVA8):
        if not required.exists():
            raise FileNotFoundError(required)
    config_text = corrected_config_text()
    for cell, meta in CELLS.items():
        worktree = meta["path"]
        ensure_worktree(meta["branch"], worktree, meta["start"])
        if git(worktree, "status", "--porcelain").stdout.strip():
            # A prior coordinator run is allowed; any unrelated dirt is not.
            changed = git(worktree, "status", "--porcelain").stdout.splitlines()
            if any("experiments/rdpro/" not in line for line in changed):
                raise RuntimeError(f"unrelated changes in {worktree}: {changed}")
        atomic_text(worktree / "experiments/rdpro/configs/aideal.yaml", config_text)
        shutil.copy2(RUNNER / "experiments/rdpro/configs/project_profile.yaml",
                     worktree / "experiments/rdpro/configs/project_profile.yaml")
        shutil.copy2(HISTORICAL_A1 / "experiments/rdpro/docs/api_manifest_shared.json",
                     worktree / "experiments/rdpro/docs/api_manifest_shared.json")
        ensure_beast(worktree)
        fixtures = validate_fixtures(worktree)
        environment_inventory(cell, worktree, fixtures)
        if cell in {"A1", "B1"}:
            actual_doc = relevant_document_hash(worktree, "original")
            if actual_doc != A1_DOCUMENT_SHA256:
                raise RuntimeError(
                    f"{cell} original relevant-document hash {actual_doc}, "
                    f"expected historical A1 {A1_DOCUMENT_SHA256}")
        if cell in {"A2", "B2"}:
            actual_doc = relevant_document_hash(worktree, "aideal")
            if actual_doc != A2_DOCUMENT_SHA256:
                raise RuntimeError(
                    f"{cell} generated relevant-document hash {actual_doc}, "
                    f"expected frozen A2 {A2_DOCUMENT_SHA256}")
    plan = build_plan()
    atomic_text(plan_path, yaml.safe_dump(plan, sort_keys=False, width=120))
    print(json.dumps({"prepared": True, "plan": str(plan_path),
                      "cells": {c: {"branch": m["branch"], "path": str(m["path"])}
                                for c, m in CELLS.items()}}, indent=2))
    return plan_path


def base_job(cell: str, suffix: str, command: list[str], result: str,
             *, depends: list[str] | None = None, completion: dict | None = None,
             max_restarts: int = 3, max_runtime: int = 172800) -> dict:
    worktree = CELLS[cell]["path"]
    return {
        "id": f"rdpro_{cell.lower()}_{suffix}",
        "cwd": str(worktree),
        "branch": CELLS[cell]["branch"],
        "environment_inventory":
            f"experiments/rdpro/docs/eval/setup/environment_{cell}.json",
        "env": {"PYTHONPATH": str(RUNNER / "grail-agent/src")},
        "command": command,
        "result": result,
        "complete": completion or {"kind": "exit_zero"},
        "depends_on": depends or [],
        "max_runtime_seconds": max_runtime,
        "max_restarts": max_restarts,
    }


def self_command(*args: str) -> list[str]:
    return [str(PYTHON), str(Path(__file__).resolve()), "internal", *args]


def comprehension_job(cell: str, depends: list[str]) -> dict:
    doc = CELLS[cell]["doc"]
    result = f"experiments/rdpro/docs/eval/{cell}/comprehension.json"
    command = [
        str(PYTHON), "-m", "aideal.cli", "--config",
        "experiments/rdpro/configs/aideal.yaml", "comprehension", "--execute",
        "--show-code", "--doc", doc, "--doc-scope", "relevant", "--full-doc", "off",
        "--manifest", "docs/api_manifest_shared.json", "--max-fix-rounds", "0",
        "--resume", "--timeout", "600",
    ]
    return base_job(cell, "zero", command, result, depends=depends,
                    completion={"kind": "json_metrics_no_transient"},
                    max_restarts=24, max_runtime=172800)


def docfix_job(cell: str, depends: list[str]) -> dict:
    source_cell = "A1" if cell == "B1" else "A2"
    report = f"experiments/rdpro/docs/eval/{cell}/docfix.json"
    command = [
        str(PYTHON), "-m", "aideal.cli", "--config",
        "experiments/rdpro/configs/aideal.yaml", "fix-docs", "--from-results",
        f"experiments/rdpro/docs/eval/{source_cell}/comprehension.json", "--deep-dive-first",
        "--doc-rounds", "5", "--doc-stuck", "2", "--retry-rounds", "0",
        "--doc", CELLS[cell]["doc"], "--doc-scope", "relevant", "--full-doc", "off",
        "--manifest", "docs/api_manifest_shared.json", "--report",
        f"experiments/rdpro/docs/eval/{cell}/docfix.json", "--deep-dive-out",
        f"experiments/rdpro/docs/eval/{cell}/deepdive", "--timeout", "600",
    ]
    if cell == "B1":
        command.append("--create-missing")
    return base_job(cell, "repair", command, report, depends=depends,
                    completion={"kind": "docfix", "path": report},
                    max_restarts=24, max_runtime=259200)


def build_plan() -> dict:
    jobs = []
    for cell in CELLS:
        jobs.append(base_job(cell, "p2p_before",
                             self_command("p2p", cell, "before"),
                             f"experiments/rdpro/docs/eval/{cell}/PASS_TO_PASS_BEFORE.json",
                             max_restarts=3, max_runtime=7200))

    jobs.append(base_job("A1", "import", self_command("import-a1"),
                         "experiments/rdpro/docs/eval/A1/import.json",
                         depends=["rdpro_a1_p2p_before"]))
    jobs.append(base_job("A1", "baseline_checkpoint",
                         self_command("checkpoint", "A1", "baseline",
                                      "Save validated RDPro A1 shared-88 baseline"),
                         "experiments/rdpro/docs/eval/A1/baseline_checkpoint.json",
                         depends=["rdpro_a1_import"]))
    jobs.append(base_job("A1", "analyze", self_command("analyze", "A1"),
                         "experiments/rdpro/docs/eval/A1/failure_analysis/summary.json",
                         depends=["rdpro_a1_baseline_checkpoint"]))
    jobs.append(base_job("A1", "p2p_after", self_command("p2p", "A1", "after"),
                         "experiments/rdpro/docs/eval/A1/PASS_TO_PASS_AFTER.json",
                         depends=["rdpro_a1_analyze"], max_runtime=7200))
    jobs.append(base_job("A1", "finalize", self_command("finalize", "A1"),
                         "experiments/rdpro/docs/eval/A1/finalized.json",
                         depends=["rdpro_a1_p2p_after"]))

    jobs.append(comprehension_job("A2", ["rdpro_a2_p2p_before"]))
    jobs.append(base_job("A2", "baseline_checkpoint",
                         self_command("checkpoint", "A2", "baseline",
                                      "Save fresh RDPro A2 shared-88 baseline"),
                         "experiments/rdpro/docs/eval/A2/baseline_checkpoint.json",
                         depends=["rdpro_a2_zero"]))
    jobs.append(base_job("A2", "analyze", self_command("analyze", "A2"),
                         "experiments/rdpro/docs/eval/A2/failure_analysis/summary.json",
                         depends=["rdpro_a2_baseline_checkpoint"]))
    jobs.append(base_job("A2", "p2p_after", self_command("p2p", "A2", "after"),
                         "experiments/rdpro/docs/eval/A2/PASS_TO_PASS_AFTER.json",
                         depends=["rdpro_a2_analyze"], max_runtime=7200))
    jobs.append(base_job("A2", "finalize", self_command("finalize", "A2"),
                         "experiments/rdpro/docs/eval/A2/finalized.json",
                         depends=["rdpro_a2_p2p_after"]))

    jobs.append(base_job("B1", "clean", self_command("prepare-b1"),
                         "experiments/rdpro/docs/eval/B1/precondition.json",
                         depends=["rdpro_b1_p2p_before", "rdpro_a1_import"]))
    jobs.append(docfix_job("B1", ["rdpro_b1_clean"]))
    jobs.append(base_job("B1", "repair_checkpoint",
                         self_command("checkpoint", "B1", "repair",
                                      "RDPro B1 repair checkpoint"),
                         "experiments/rdpro/docs/eval/B1/repair_checkpoint.json",
                         depends=["rdpro_b1_repair"]))
    jobs.append(comprehension_job("B1", ["rdpro_b1_repair_checkpoint"]))
    jobs.append(base_job("B1", "analyze", self_command("analyze", "B1"),
                         "experiments/rdpro/docs/eval/B1/failure_analysis/summary.json",
                         depends=["rdpro_b1_zero"]))
    jobs.append(base_job("B1", "p2p_after", self_command("p2p", "B1", "after"),
                         "experiments/rdpro/docs/eval/B1/PASS_TO_PASS_AFTER.json",
                         depends=["rdpro_b1_analyze"], max_runtime=7200))
    jobs.append(base_job("B1", "finalize", self_command("finalize", "B1"),
                         "experiments/rdpro/docs/eval/B1/finalized.json",
                         depends=["rdpro_b1_p2p_after"]))

    jobs.append(base_job("B2", "sync", self_command("sync-a2"),
                         "experiments/rdpro/docs/eval/B2/baseline_import.json",
                         depends=["rdpro_b2_p2p_before", "rdpro_a2_baseline_checkpoint"]))
    jobs.append(docfix_job("B2", ["rdpro_b2_sync"]))
    jobs.append(base_job("B2", "repair_checkpoint",
                         self_command("checkpoint", "B2", "repair",
                                      "RDPro B2 repair checkpoint"),
                         "experiments/rdpro/docs/eval/B2/repair_checkpoint.json",
                         depends=["rdpro_b2_repair"]))
    jobs.append(comprehension_job("B2", ["rdpro_b2_repair_checkpoint"]))
    jobs.append(base_job("B2", "analyze", self_command("analyze", "B2"),
                         "experiments/rdpro/docs/eval/B2/failure_analysis/summary.json",
                         depends=["rdpro_b2_zero"]))
    jobs.append(base_job("B2", "p2p_after", self_command("p2p", "B2", "after"),
                         "experiments/rdpro/docs/eval/B2/PASS_TO_PASS_AFTER.json",
                         depends=["rdpro_b2_analyze"], max_runtime=7200))
    jobs.append(base_job("B2", "finalize", self_command("finalize", "B2"),
                         "experiments/rdpro/docs/eval/B2/finalized.json",
                         depends=["rdpro_b2_p2p_after"]))

    return {
        "version": 1,
        "max_parallel": 2,
        "retry_delay_seconds": 300,
        "env": {
            "AIDEAL_GOOGLE_MIN_INTERVAL_S": "4",
            "AIDEAL_GOOGLE_RATE_STATE": RATE_STATE,
            "AIDEAL_GOOGLE_REQUEST_TIMEOUT_S": "300",
            "AIDEAL_GOOGLE_MAX_RETRIES": "8",
            "PYTHONUNBUFFERED": "1",
        },
        "jobs": jobs,
    }


def emit_result(value: dict) -> int:
    print(json.dumps(value, indent=2, ensure_ascii=False))
    return 0


def internal_p2p(cell: str, phase: str) -> int:
    worktree = CELLS[cell]["path"]
    source = worktree / "experiments/rdpro/beast"
    revision_before = git(source, "rev-parse", "HEAD").stdout.strip()
    dirty_before = git(source, "status", "--porcelain", "--untracked-files=no").stdout.strip()
    if revision_before != BEAST_REVISION or dirty_before:
        raise RuntimeError(f"invalid Beast source before PASS_TO_PASS: {revision_before} {dirty_before}")
    command = [str(MAVEN), "-q", "package" if phase == "before" else "test"]
    env = dict(os.environ, JAVA_HOME=str(JAVA8))
    started = time.time()
    proc = run(command, source, check=False, env=env)
    log_path = worktree / f"experiments/rdpro/docs/eval/{cell}/PASS_TO_PASS_{phase.upper()}.log"
    atomic_text(log_path, proc.stdout + "\n" + proc.stderr)
    jars = sorted(source.glob("target/beast-uber-*.jar"))
    dist_jars = sorted(source.glob("target/beast-0.10.1-bin/beast-0.10.1/lib/*.jar"))
    result = {
        "check": "PASS_TO_PASS",
        "cell": cell,
        "phase": phase,
        "command": command,
        "exit_code": proc.returncode,
        "wall_s": round(time.time() - started, 1),
        "beast_revision": revision_before,
        "tracked_source_clean_before": not bool(dirty_before),
        "tracked_source_clean_after": not bool(git(
            source, "status", "--porcelain", "--untracked-files=no").stdout.strip()),
        "uberjars": {str(path.relative_to(source)): sha256(path) for path in jars},
        "distribution_jar_count": len(dist_jars),
        "log": str(log_path.relative_to(worktree)),
    }
    target = worktree / f"experiments/rdpro/docs/eval/{cell}/PASS_TO_PASS_{phase.upper()}.json"
    atomic_json(target, result)
    print(json.dumps(result, indent=2))
    if proc.returncode or not result["tracked_source_clean_after"]:
        return proc.returncode or 1
    if phase == "before" and (not jars or not dist_jars):
        return 1
    return 0


def internal_import_a1() -> int:
    worktree = CELLS["A1"]["path"]
    source = HISTORICAL_A1 / "experiments/rdpro/docs/comprehension_A1_original.json"
    validate_result(source, "original")
    target = worktree / "experiments/rdpro/docs/eval/A1/comprehension.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    provenance = {
        "cell": "A1", "mode": "validated historical reuse",
        "source": str(source), "source_sha256": sha256(source),
        "reason": "already protocol-valid: shared 88, relevant scope, zero snippet fixes",
    }
    atomic_json(target.parent / "import.json", provenance)
    return emit_result(provenance)


def internal_prepare_b1() -> int:
    worktree = CELLS["B1"]["path"]
    catalog = worktree / "experiments/rdpro/docs/LLM_readme.md"
    archive = worktree / "experiments/rdpro/docs/eval/B1/LLM_readme_precondition_archive.md"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if catalog.exists() and not archive.exists():
        shutil.copy2(catalog, archive)
    if catalog.exists():
        catalog.unlink()
    baseline = worktree / "experiments/rdpro/docs/eval/A1/comprehension.json"
    seed_error_log(worktree, baseline, "B1")
    result = {"cell": "B1", "catalog_absent": not catalog.exists(),
              "precondition": "original docs only; create_missing enabled",
              "archive": str(archive.relative_to(worktree)),
              "archive_sha256": sha256(archive) if archive.exists() else None}
    atomic_json(archive.parent / "precondition.json", result)
    return emit_result(result)


def internal_sync_a2() -> int:
    source = CELLS["A2"]["path"] / "experiments/rdpro/docs/eval/A2/comprehension.json"
    validate_result(source, "aideal")
    worktree = CELLS["B2"]["path"]
    target = worktree / "experiments/rdpro/docs/eval/A2/comprehension.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    a2_catalog = CELLS["A2"]["path"] / "experiments/rdpro/docs/LLM_readme.md"
    b2_catalog = worktree / "experiments/rdpro/docs/LLM_readme.md"
    if sha256(a2_catalog) != sha256(b2_catalog):
        raise RuntimeError("B2 frozen README differs from the exact A2 treatment")
    seed_error_log(worktree, target, "B2")
    result = {"cell": "B2", "baseline_cell": "A2", "source": str(source),
              "source_sha256": sha256(source), "target": str(target.relative_to(worktree))}
    out = worktree / "experiments/rdpro/docs/eval/B2/baseline_import.json"
    atomic_json(out, result)
    return emit_result(result)


def seed_error_log(worktree: Path, result_path: Path, cell: str) -> Path:
    """Replace mutable historical feedback with only the matched baseline failures.

    The prior log is archived first. This prevents a later five-round or
    different-denominator experiment from leaking hints into B1/B2 repair.
    """
    data = load_json(result_path)
    log_path = worktree / "experiments/rdpro/logs/error_log.jsonl"
    archive = worktree / f"experiments/rdpro/docs/eval/{cell}/historical_error_log_archive.jsonl"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists() and not archive.exists():
        shutil.copy2(log_path, archive)
    details = data.get("details") or {}
    rows = []
    for name, metric in sorted((data.get("metrics") or {}).items()):
        if metric.get("status") == "pass":
            continue
        detail = details.get(name) if isinstance(details.get(name), dict) else {}
        rows.append({
            "run_id": (data.get("run") or {}).get("run_id"),
            "step": "readme-exec-test",
            "language": "Scala",
            "task": f"matched_{cell}_repair_baseline",
            "status": "fail",
            "function": name,
            "error_category": metric.get("error_category") or detail.get("error_category") or "unknown",
            "error": metric.get("error") or detail.get("error") or "",
            "root_cause": metric.get("locus") or "",
            "code": detail.get("code") or "",
            "frames": metric.get("codebase_frames") or [],
            "round": 0,
            "provenance": str(result_path.relative_to(worktree)),
        })
    atomic_text(log_path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    return archive


def internal_analyze(cell: str) -> int:
    worktree = CELLS[cell]["path"]
    result = worktree / f"experiments/rdpro/docs/eval/{cell}/comprehension.json"
    validate_result(result, CELLS[cell]["doc"])
    out_dir = worktree / f"experiments/rdpro/docs/eval/{cell}/failure_analysis"
    command = [str(PYTHON), str(RUNNER / "experiments/external/analyze_failures.py"),
               str(result), "--out-dir", str(out_dir), "--label", f"RDPro {cell}"]
    proc = run(command, worktree)
    summary = json.loads(proc.stdout)
    atomic_json(out_dir / "summary.json", summary)
    return emit_result(summary)


def changed_paths(worktree: Path) -> list[str]:
    proc = git(worktree, "status", "--porcelain", "--untracked-files=all")
    paths = []
    for line in proc.stdout.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return paths


def checkpoint(cell: str, message: str) -> dict:
    worktree = CELLS[cell]["path"]
    allowed = ("experiments/rdpro/configs/aideal.yaml",
               "experiments/rdpro/configs/project_profile.yaml",
               "experiments/rdpro/docs/", "experiments/rdpro/logs/")
    bad = [path for path in changed_paths(worktree)
           if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if bad:
        raise RuntimeError(f"refusing to commit unrelated paths in {cell}: {bad}")
    git(worktree, "add", "--", "experiments/rdpro/configs/aideal.yaml",
        "experiments/rdpro/configs/project_profile.yaml", "experiments/rdpro/docs",
        "experiments/rdpro/logs/error_log.jsonl")
    committed = False
    if git(worktree, "diff", "--cached", "--quiet", check=False).returncode != 0:
        git(worktree, "commit", "-m", message)
        committed = True
    git(worktree, "push", "-u", "origin", CELLS[cell]["branch"])
    return {"cell": cell, "branch": CELLS[cell]["branch"],
            "commit": git(worktree, "rev-parse", "HEAD").stdout.strip(),
            "created_commit": committed, "pushed": True}


def internal_checkpoint(cell: str, stage: str, message: str) -> int:
    worktree = CELLS[cell]["path"]
    out = worktree / f"experiments/rdpro/docs/eval/{cell}/{stage}_checkpoint.json"
    # Write evidence before committing so it is part of the checkpoint itself.
    result = {"cell": cell, "status": "repair checkpoint complete",
              "branch": CELLS[cell]["branch"]}
    atomic_json(out, result)
    checkpoint(cell, message)
    return emit_result(result)


def internal_finalize(cell: str) -> int:
    worktree = CELLS[cell]["path"]
    result_path = worktree / f"experiments/rdpro/docs/eval/{cell}/comprehension.json"
    data = validate_result(result_path, CELLS[cell]["doc"])
    metrics = data["metrics"]
    categories = Counter((row.get("error_category") or "pass") for row in metrics.values())
    before = load_json(worktree / f"experiments/rdpro/docs/eval/{cell}/PASS_TO_PASS_BEFORE.json")
    after = load_json(worktree / f"experiments/rdpro/docs/eval/{cell}/PASS_TO_PASS_AFTER.json")
    if before.get("exit_code") != 0 or after.get("exit_code") != 0:
        raise RuntimeError(f"{cell} PASS_TO_PASS gate failed")
    memo = [
        f"# RDPro {cell} completion memo", "",
        f"- Branch: `{CELLS[cell]['branch']}`",
        f"- Beast commit: `{BEAST_REVISION}` (`beast-0.10.1`)",
        f"- Protocol: shared 88 APIs; `relevant` documentation; zero final snippet fixes",
        f"- Document arm: `{CELLS[cell]['doc']}`",
        f"- Score: `{data.get('score')}` ({sum(1 for row in metrics.values() if row.get('status') == 'pass')}/88 raw passes)",
        f"- Infrastructure exclusions: `{data.get('infra_excluded')}`",
        f"- Experiment fingerprint: `{(data.get('run') or {}).get('experiment_fingerprint')}`",
        f"- PASS_TO_PASS: before `{before.get('exit_code')}`, after `{after.get('exit_code')}`",
        "", "## Outcome counts", "",
    ]
    memo.extend(f"- `{name}`: {count}" for name, count in sorted(categories.items()))
    memo.extend(["", "## Detailed evidence", "",
                 "Per-function failures, generated code, source definition, runtime frames, and error text are in ",
                 f"`docs/eval/{cell}/failure_analysis/FAILURE_ANALYSIS.md` and its JSON/CSV companions.", ""])
    out_dir = worktree / f"experiments/rdpro/docs/eval/{cell}"
    atomic_text(out_dir / "CELL_MEMO.md", "\n".join(memo))
    provisional = {"cell": cell, "validated": True, "score": data.get("score"),
                   "manifest_api_count": 88, "manifest_sha256": MANIFEST_SHA256,
                   "doc_scope": "relevant", "max_fix_rounds": 0}
    atomic_json(out_dir / "finalized.json", provisional)
    checkpoint(cell, f"Complete protocol-valid RDPro {cell} shared-88 cell")
    print(json.dumps(provisional, indent=2))
    return 0


def run_watchdog(plan_path: Path, confirm: bool) -> int:
    if not confirm:
        raise SystemExit("refusing paid LLM execution without --confirm-paid-llm")
    command = [str(PYTHON), str(RUNNER / "experiments/external/run_condition_watchdog.py"),
               str(plan_path), "--keep-awake"]
    return subprocess.call(command, cwd=RUNNER)


def print_plan() -> int:
    plan = build_plan()
    print(yaml.safe_dump({
        "protocol": {"beast_revision": BEAST_REVISION, "manifest_count": MANIFEST_COUNT,
                     "manifest_sha256": MANIFEST_SHA256, "doc_scope": "relevant",
                     "final_snippet_fix_rounds": 0},
        "cells": {cell: {k: str(v) if isinstance(v, Path) else v for k, v in meta.items()}
                  for cell, meta in CELLS.items()},
        "job_order": {job["id"]: job.get("depends_on", []) for job in plan["jobs"]},
        "max_parallel": plan["max_parallel"],
        "paid_calls_started": False,
    }, sort_keys=False))
    return 0


def internal_main(args: argparse.Namespace) -> int:
    if args.action == "p2p":
        return internal_p2p(args.cell, args.phase)
    if args.action == "import-a1":
        return internal_import_a1()
    if args.action == "prepare-b1":
        return internal_prepare_b1()
    if args.action == "sync-a2":
        return internal_sync_a2()
    if args.action == "analyze":
        return internal_analyze(args.cell)
    if args.action == "checkpoint":
        return internal_checkpoint(args.cell, args.stage, args.message)
    if args.action == "finalize":
        return internal_finalize(args.cell)
    raise AssertionError(args.action)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan", help="print the read-only protocol and dependency graph")
    prep = sub.add_parser("prepare", help="create isolated workers; no LLM calls")
    prep.add_argument("--plan-out", type=Path,
                      default=RUNNER / ".aideal_exec/rdpro_2x2/watchdog.yaml")
    execute = sub.add_parser("run", help="resume the prepared paid experiment")
    execute.add_argument("--plan", type=Path,
                         default=RUNNER / ".aideal_exec/rdpro_2x2/watchdog.yaml")
    execute.add_argument("--confirm-paid-llm", action="store_true")

    internal = sub.add_parser("internal", help=argparse.SUPPRESS)
    actions = internal.add_subparsers(dest="action", required=True)
    p2p = actions.add_parser("p2p")
    p2p.add_argument("cell", choices=CELLS)
    p2p.add_argument("phase", choices=("before", "after"))
    actions.add_parser("import-a1")
    actions.add_parser("prepare-b1")
    actions.add_parser("sync-a2")
    analyze = actions.add_parser("analyze")
    analyze.add_argument("cell", choices=CELLS)
    checkpoint_parser = actions.add_parser("checkpoint")
    checkpoint_parser.add_argument("cell", choices=CELLS)
    checkpoint_parser.add_argument("stage", choices=("baseline", "repair"))
    checkpoint_parser.add_argument("message")
    finalize = actions.add_parser("finalize")
    finalize.add_argument("cell", choices=CELLS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "plan":
        return print_plan()
    if args.command == "prepare":
        prepare(args.plan_out.resolve())
        return 0
    if args.command == "run":
        if not args.plan.is_file():
            raise FileNotFoundError(f"prepare first; plan missing: {args.plan}")
        return run_watchdog(args.plan.resolve(), args.confirm_paid_llm)
    if args.command == "internal":
        return internal_main(args)
    raise AssertionError(args.command)


if __name__ == "__main__":
    sys.exit(main())
