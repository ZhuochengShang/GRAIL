import hashlib
import json

import pytest

from experiments.rdpro import run_rdpro_2x2_pipeline as runner


def test_queued_paid_command_reuses_evidence_without_launch(tmp_path, monkeypatch, capsys):
    evidence = tmp_path / "result.json"
    evidence.write_text('{"metrics": {"api": {"status": "pass"}}}')
    policy = tmp_path / "experiments/rdpro/reuse_only_policy.json"
    policy.parent.mkdir(parents=True)
    policy.write_text(json.dumps({
        "paid_execution_allowed": False,
        "comparison_status": "PARTIAL",
        "evidence": [{"path": str(evidence),
                      "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest()}],
    }))
    monkeypatch.setattr(runner, "RUNNER", tmp_path)
    monkeypatch.setattr(runner.subprocess, "call", lambda *a, **k: pytest.fail("paid launch"))
    assert runner.run_watchdog(tmp_path / "unused.yaml", confirm=True) == 0
    assert json.loads(capsys.readouterr().out)["paid_calls_started"] is False
    evidence.write_text("changed")
    with pytest.raises(RuntimeError, match="changed or missing"):
        runner.run_watchdog(tmp_path / "unused.yaml", confirm=True)


def test_missing_policy_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "RUNNER", tmp_path)
    with pytest.raises(FileNotFoundError):
        runner.run_watchdog(tmp_path / "unused.yaml", confirm=True)
