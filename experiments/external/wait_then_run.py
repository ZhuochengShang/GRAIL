#!/usr/bin/env python3
"""Wait for a durable watchdog job to succeed, then exec another command."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import time


def read_status(path: Path, job_id: str) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "not-created"
    return str((data.get("jobs") or {}).get(job_id, {}).get("status") or "not-created")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--job", required=True)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required after --")
    while True:
        status = read_status(args.state.resolve(), args.job)
        if status == "succeeded":
            print(f"prerequisite {args.job} succeeded; starting queued command", flush=True)
            os.execvpe(command[0], command, dict(os.environ))
        print(f"waiting for prerequisite {args.job}: status={status}", flush=True)
        time.sleep(max(1, args.poll_seconds))


if __name__ == "__main__":
    sys.exit(main())
