"""Capture a hash-bound count of recorded provider failures, without API calls."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics


def capture(evidence_dir):
    cells = []
    for path in sorted(evidence_dir.glob("*_migration.json")):
        proof = json.loads(path.read_text())
        checkpoint = Path(proof["checkpoint"])
        raw = checkpoint.read_bytes()
        rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
        provider = [row for row in rows if row.get("error_category") == "llm-error"]
        timeouts = [row for row in provider if any(token in str(row.get("error", "")).lower()
                    for token in ("timeout", "timed out", "deadline_exceeded", "deadline expired", "wall deadline"))]
        terminal = [row for row in rows if row.get("error_category") != "llm-error"]
        def median(items):
            values = [row["wall_s"] for row in items if isinstance(row.get("wall_s"), (int, float))]
            return statistics.median(values) if values else None
        cells.append({"cell": path.stem.replace("_migration", ""),
                      "checkpoint": str(checkpoint), "checkpoint_sha256": hashlib.sha256(raw).hexdigest(),
                      "checkpoint_bytes": len(raw), "checkpoint_events": len(rows),
                      "provider_error_events": len(provider), "timeout_events": len(timeouts),
                      "timeout_pct": round(100*len(timeouts)/len(rows), 1),
                      "distinct_timeout_apis": len({r["name"] for r in timeouts}),
                      "fingerprint_groups": len({r["experiment_fingerprint"] for r in rows}),
                      "timeout_median_wall_s": median(timeouts), "terminal_median_wall_s": median(terminal)})
    return {"observed_at": datetime.now().astimezone().isoformat(),
            "unit": "Recorded per-API evaluation event, including repeated groups and watchdog retries; not SDK requests",
            "cells": cells, "limitations": ["SDK internal retries and failed-request tokens are unknown.",
            "Events lack individual timestamps; no reliable hourly outage rate is inferred.",
            "Timeouts are infrastructure evidence, not proof of a codebase defect."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(capture(args.evidence_dir), indent=2)+"\n")
