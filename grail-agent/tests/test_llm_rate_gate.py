from __future__ import annotations

from pathlib import Path

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
