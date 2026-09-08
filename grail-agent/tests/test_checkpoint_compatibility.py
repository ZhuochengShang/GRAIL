import json
import pytest
from aideal.checkpoint_compatibility import fingerprint, load_compatibility


def test_compatibility_is_bound_to_exact_inputs_and_engine(tmp_path):
    checkpoint = tmp_path / "comprehension_progress.jsonl"
    old = {"schema": 2, "engine": "old", "fixtures": "outputs+inputs", "models": "same"}
    current = dict(old, schema=3, engine="new", fixtures="inputs")
    record = dict(schema=1, checkpoint=str(checkpoint), current_components=current,
                  legacy_components=old, legacy_fingerprint=fingerprint(old),
                  input_fixtures="inputs", selection_policy="latest reproducible", reason="reviewed fix")
    path = tmp_path / "checkpoint_compatibility.json"
    path.write_text(json.dumps(record))
    assert load_compatibility(checkpoint, current)["legacy_fingerprint"] == fingerprint(old)
    assert load_compatibility(checkpoint, dict(current, models="changed")) == {}
    assert load_compatibility(checkpoint, dict(current, engine="unreviewed")) == {}
    with pytest.raises(ValueError, match="scope mismatch"):
        load_compatibility(tmp_path / "another.jsonl", current)
    record["legacy_components"]["models"] = "different treatment"
    record["legacy_fingerprint"] = fingerprint(record["legacy_components"])
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match="experimental inputs"):
        load_compatibility(checkpoint, current)


def test_no_implicit_legacy_reuse(tmp_path):
    assert load_compatibility(tmp_path / "comprehension_progress.jsonl", {}) == {}
