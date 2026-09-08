"""Install a reviewed compatibility record before deploying the repaired engine.

Uses capture.py with the repaired engine on PYTHONPATH. Copies, never mutates,
the captured journal prefix. Does not launch or stop any experiment process.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capture import capture
from aideal.checkpoint_compatibility import load_compatibility


def install(before_path, output_path):
    before = json.loads(before_path.read_text())
    legacy = before["selected"]
    if not legacy:
        raise ValueError("No reproducible legacy group; migration refused")
    parts = legacy["components"]
    after = capture(before["config"], before["environment"],
                    parts["doc_source"], parts["timeout_s"])
    current = after["inputs_only"]["components"]
    if before["inputs_only"]["components"]["fixtures"] != current["fixtures"]:
        raise ValueError("Input fixtures changed since capture")
    checkpoint = Path(before["checkpoint"])
    raw = checkpoint.read_bytes()[:before["checkpoint_bytes"]]
    if hashlib.sha256(raw).hexdigest() != before["checkpoint_sha256"]:
        raise ValueError("Checkpoint prefix changed since capture")
    backup = checkpoint.with_name("checkpoint_before_repair_20260907.jsonl")
    with backup.open("xb") as f:
        f.write(raw)
    record = dict(schema=1, checkpoint=str(checkpoint), current_components=current,
                  legacy_components=parts, legacy_fingerprint=legacy["fingerprint"],
                  input_fixtures=current["fixtures"], selection_policy=before["selection_policy"],
                  reason="Reviewed schema-3 output-hash repair and bounded provider transport; model, prompts, scoring and logical fix budgets unchanged",
                  captured_proof=str(before_path.resolve()),
                  captured_proof_sha256=hashlib.sha256(before_path.read_bytes()).hexdigest(),
                  backup=str(backup), backup_sha256=hashlib.sha256(raw).hexdigest(),
                  implementation_commits=["2b69710", "985c8f3"],
                  limitation="Legacy checkpoint rows retain native metrics but may lack the original generated snippet; later files must not be attributed to those rows")
    sidecar = checkpoint.with_name("checkpoint_compatibility.json")
    # Validate before installation, in an isolated directory using its own scope.
    allowed = {"schema", "engine", "fixtures"}
    if {k: v for k, v in parts.items() if k not in allowed} != {
            k: v for k, v in current.items() if k not in allowed}:
        raise ValueError("Experimental inputs differ; migration refused")
    with sidecar.open("x") as f:
        json.dump(record, f, indent=2)
    assert load_compatibility(checkpoint, current)
    with output_path.open("x") as f:
        json.dump(record, f, indent=2)
    print(json.dumps({"record": str(output_path), "legacy": legacy["fingerprint"],
                      "installed": str(sidecar)}))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("before", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    install(a.before, a.output)
