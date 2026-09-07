import json

from experiments.external.wait_then_run import read_status


def test_read_status_handles_missing_and_completed(tmp_path):
    state = tmp_path / "state.json"
    assert read_status(state, "upstream") == "not-created"
    state.write_text(json.dumps({"jobs": {"upstream": {"status": "succeeded"}}}))
    assert read_status(state, "upstream") == "succeeded"


def test_read_status_handles_invalid_json(tmp_path):
    state = tmp_path / "state.json"
    state.write_text("partial")
    assert read_status(state, "upstream") == "not-created"
