from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys

from aideal.config import ModelSpec
from aideal import llm


def test_google_rate_gate_waits_and_persists(monkeypatch, tmp_path: Path):
    state = tmp_path / "gate.txt"
    state.write_text("100.0\n", encoding="utf-8")
    clock = iter([101.0, 105.0])
    sleeps = []
    monkeypatch.setenv("AIDEAL_GOOGLE_MIN_INTERVAL_S", "4")
    monkeypatch.setenv("AIDEAL_GOOGLE_RATE_STATE", str(state))
    monkeypatch.setattr(llm.time, "time", lambda: next(clock))
    monkeypatch.setattr(llm.time, "sleep", sleeps.append)

    llm._wait_for_provider_slot(ModelSpec(provider="google", model="gemini"))

    assert sleeps == [3.0]
    assert state.read_text(encoding="utf-8") == "105.000000000\n"


def test_rate_gate_ignores_other_providers(monkeypatch, tmp_path: Path):
    state = tmp_path / "gate.txt"
    monkeypatch.setenv("AIDEAL_GOOGLE_MIN_INTERVAL_S", "4")
    monkeypatch.setenv("AIDEAL_GOOGLE_RATE_STATE", str(state))

    llm._wait_for_provider_slot(ModelSpec(provider="openai", model="x"))

    assert not state.exists()


def test_shared_rate_gate_serializes_concurrent_processes(tmp_path: Path):
    # Exercise the actual file lock with a private gate; no provider requests.
    command = [sys.executable, "-c", "from aideal import llm; "
               "from aideal.config import ModelSpec; import time; "
               "llm._wait_for_provider_slot(ModelSpec(provider='google', model='test')); "
               "print(time.time(), flush=True)"]
    env = dict(os.environ, AIDEAL_GOOGLE_MIN_INTERVAL_S="0.15",
               AIDEAL_GOOGLE_RATE_STATE=str(tmp_path / "shared-rate.txt"))
    workers = [subprocess.Popen(command, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True) for _ in range(4)]
    starts = []
    for worker in workers:
        stdout, stderr = worker.communicate(timeout=15)
        assert worker.returncode == 0, stderr
        starts.append(float(stdout.strip()))
    starts.sort()
    assert all(right - left >= 0.12 for left, right in zip(starts, starts[1:]))
