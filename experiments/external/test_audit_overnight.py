import json

from experiments.external.audit_overnight import primary_category, read_checkpoint, summarize


def event(name="api", fingerprint="new", status="pass", category=None):
    return {"name": name, "experiment_fingerprint": fingerprint, "status": status,
            "error_category": category, "checkpoint_line": 1, "llm_calls": 1}


def test_fingerprints_and_provider_attempts_are_not_mixed_with_repairs():
    events = [event(fingerprint="old"), event(status="fail", category="llm-error"), event()]
    repair = {"apis": {"api": {"rounds_used": 2, "doc_rounds": [{"round": 0}, {"round": 1}]}}}
    report = summarize(["api", "pending"], events, {}, repair)
    assert report["status"] == "partial"
    assert report["counts"] == {"pass": 1, "pending": 1}
    row = report["rows"][0]
    assert row["checkpoint_attempts"] == 2
    assert row["provider_error_attempts"] == 1
    assert row["doc_rounds_used"] == 2
    assert row["provider_internal_retries"] is None
    assert len(report["all_checkpoint_events"]) == 3


def test_complete_requires_exact_denominator_zero_rounds_and_no_provider_errors():
    final = {"run": {"api_count": 1, "max_fix_rounds": 0, "experiment_fingerprint": "new",
                     "fingerprint_components": {"schema": 2}}, "metrics": {"api": event()}}
    assert summarize(["api"], [], final, {})["status"] == "complete"
    final["metrics"]["api"] = event(status="fail", category="llm-error")
    assert summarize(["api"], [], final, {})["status"] == "partial"
    final["metrics"]["api"] = event()
    final["run"]["max_fix_rounds"] = 5
    assert summarize(["api"], [], final, {})["status"] == "partial"


def test_partial_jsonl_write_is_ignored_but_corrupt_complete_line_is_reported(tmp_path):
    path = tmp_path / "checkpoint.jsonl"
    path.write_text(json.dumps(event()) + '\n{"name":')
    rows, errors = read_checkpoint(path)
    assert len(rows) == 1 and not errors
    path.write_text('broken\n' + json.dumps(event()) + '\n')
    rows, errors = read_checkpoint(path)
    assert len(rows) == 1 and len(errors) == 1


def test_output_directory_failure_is_secondary_harness_diagnosis():
    metric = event(status="fail", category="runtime")
    metric["error"] = "FileNotFoundError: /tmp/project/output/test_key.txt"
    detail = {"code": 'with open(key_file, "w") as f: f.write("C:maj")'}
    assert primary_category(metric, detail)[0] == "test/scaffold"
    assert metric["error_category"] == "runtime"
    metric["error"] = "AssertionError: wrong expected score"
    assert primary_category(metric, detail)[0] == "unknown"
