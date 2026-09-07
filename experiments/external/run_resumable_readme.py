#!/usr/bin/env python3
"""Choose AIDEAL README --force or --resume from its durable state."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from aideal.config import load_config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--limit", default="0")
    parser.add_argument("--role", action="append", default=[])
    args = parser.parse_args()
    cfg = load_config(args.config)
    state = cfg.root / ".aideal_exec/readme_generation_state.json"
    mode = "--resume" if state.is_file() and cfg.llm_readme.is_file() else "--force"
    command = [
        sys.executable, "-m", "aideal.cli", "--config", str(args.config),
        "readme", "--generate", "--limit", str(args.limit), mode,
    ]
    for role in args.role:
        command.extend(["--role", role])
    os.execvpe(command[0], command, dict(os.environ))
    return 127


if __name__ == "__main__":
    raise SystemExit(main())
