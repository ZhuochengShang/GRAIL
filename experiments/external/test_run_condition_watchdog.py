import json
from pathlib import Path
import sys

import yaml

from experiments.external.run_condition_watchdog import Supervisor, completion


def test_completion_rejects_transient_and_unfingerprinted_results(tmp_path):
    job = {"cwd": str(tmp_path), "complete": {"kind": "json_metrics_no_transient"}}
    result = tmp_path / "result.json.tmp"
    payload = {
        "run": {"api_count": 1, "fingerprint_components": {"schema": 2}},
        "metrics": {"api": {"status": "fail", "error_category": "llm-error"}},
    }
    result.write_text(json.dumps(payload))
    assert not completion(job, result, tmp_path)[0]
    payload["metrics"]["api"] = {"status": "fail", "error_category": "runtime"}
    result.write_text(json.dumps(payload))
    assert completion(job, result, tmp_path)[0]
    payload["run"].pop("fingerprint_components")
    result.write_text(json.dumps(payload))
    assert not completion(job, result, tmp_path)[0]


def test_generation_completion_requires_every_entry_without_fallback(tmp_path):
    job = {"cwd": str(tmp_path), "complete": {"kind": "readme_generation"}}
    result = tmp_path / "generation.json.tmp"
    result.write_text(json.dumps({
        "api_entries": 148, "generated_ok": 147, "fallback_to_skeleton": 1,
        "generation_fingerprint": "fingerprint",
    }))
    assert not completion(job, result, tmp_path)[0]
    result.write_text(json.dumps({
        "api_entries": 148, "generated_ok": 148, "fallback_to_skeleton": 0,
        "generation_fingerprint": "fingerprint",
    }))
    assert completion(job, result, tmp_path)[0]


def test_supervisor_runs_dependencies_and_persists_success(tmp_path):
    inventory = tmp_path / "environment.txt"
    inventory.write_text("python=test\n")
    payload = json.dumps({
        "run": {"api_count": 1, "fingerprint_components": {"schema": 2}},
        "metrics": {"api": {"status": "pass"}},
    })
    plan = {
        "max_parallel": 2,
        "retry_delay_seconds": 1,
        "jobs": [
            {
                "id": "baseline",
                "cwd": str(tmp_path),
                "environment_inventory": str(inventory),
                "command": [sys.executable, "-c", f"print({payload!r})"],
                "result": "baseline.json",
                "complete": {"kind": "json_metrics_no_transient"},
            },
            {
                "id": "repair",
                "depends_on": ["baseline"],
                "cwd": str(tmp_path),
                "environment_inventory": str(inventory),
                "command": [sys.executable, "-c", "print('done')"],
                "result": "repair.log",
                "complete": {"kind": "exit_zero"},
            },
        ],
    }
    plan_path = tmp_path / "plan.yaml"
    plan_path.write_text(yaml.safe_dump(plan, sort_keys=False))
    supervisor = Supervisor(plan_path)
    assert supervisor.run() == 0
    state = json.loads(plan_path.with_suffix(".state.json").read_text())
    assert state["status"] == "succeeded"
    assert state["jobs"]["baseline"]["status"] == "succeeded"
    assert state["jobs"]["repair"]["status"] == "succeeded"
    assert (tmp_path / "baseline.json").is_file()
