#!/usr/bin/env python3
"""Freeze and verify the complete visibility-correct MDAnalysis API surface."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

from aideal.config import load_config
from aideal.readme_agent import public_api_details, public_api_surface


EXPECTED_NAMES = 1032
EXPECTED_SITES = 1397
SOURCE_COMMIT = "81b8ef51e5bc1aa2824294ac6c52818c74975658"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True, text=True, capture_output=True,
    ).stdout.strip()


def build(config: Path) -> dict:
    cfg = load_config(config)
    names = sorted(public_api_surface(cfg, override_filter="all"))
    sites = sorted(
        (row for row in public_api_details(cfg) if row.get("visibility") == "public"),
        key=lambda row: (
            row.get("name", ""), row.get("file", ""), int(row.get("line", 0)),
            row.get("qualified_name", ""), row.get("signature", ""),
        ),
    )
    source = cfg.root / "mdanalysis"
    source_head = git_head(source)
    if source_head != SOURCE_COMMIT:
        raise RuntimeError(f"source HEAD {source_head}, expected {SOURCE_COMMIT}")
    if len(names) != EXPECTED_NAMES or len(sites) != EXPECTED_SITES:
        raise RuntimeError(
            f"surface drift: names={len(names)}/{EXPECTED_NAMES}, "
            f"sites={len(sites)}/{EXPECTED_SITES}"
        )
    by_name: dict[str, list[dict]] = {}
    for row in sites:
        by_name.setdefault(row["name"], []).append(row)
    # One manifest identity per bare public name.  When several public
    # definition sites share that name (for example overloaded methods or
    # same-named classes), the generated entry's factual primary signature is
    # the one with the most parameters; ties are deterministic.
    primary = {
        name: max(
            rows,
            key=lambda row: (
                len(row.get("params") or []),
                len(row.get("signature") or ""),
                str(row.get("file", "")),
                -int(row.get("line", 0)),
            ),
        )
        for name, rows in by_name.items()
    }
    compact_names = json.dumps(
        names, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    compact_sites = json.dumps(
        sites, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "schema": 1,
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "set": "complete_visibility_correct_public_name_surface",
        "visibility_policy": (
            "Python AST identities; public names exclude underscore-prefixed "
            "and function-local definitions"
        ),
        "deduplication_policy": (
            "one bare public name per manifest; duplicate definition sites are "
            "retained in provenance and the primary signature uses the most "
            "parameters, with deterministic tie-breaks"
        ),
        "project": "MDAnalysis",
        "project_version": "2.9.0",
        "source_commit": source_head,
        "extractor_repo_commit": git_head(cfg.root.parents[1]),
        "public_names": len(names),
        "definition_sites": len(sites),
        "name_order": "Unicode code-point ascending",
        "names_json_sha256": sha256_bytes(compact_names),
        # This is the exact algorithm recorded by comprehension result files.
        "comprehension_manifest_sha256": sha256_bytes(
            "\n".join(names).encode("utf-8")
        ),
        "public_definition_sites_sha256": sha256_bytes(compact_sites),
        "primary_definition_by_name": {
            name: {
                "qualified_name": row.get("qualified_name", ""),
                "file": row.get("file", ""),
                "line": row.get("line", 0),
                "parameter_count": len(row.get("params") or []),
                "signature": row.get("signature", ""),
            }
            for name, row in sorted(primary.items())
        },
        "config_sha256": sha256_bytes(config.read_bytes()),
        "apis": names,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("configs/aideal.full1032.yaml"))
    parser.add_argument("--output", type=Path, default=Path("docs/full_1032/api_manifest.json"))
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    record = build(args.config.resolve())
    output = args.output.resolve()
    if args.verify:
        saved = json.loads(output.read_text(encoding="utf-8"))
        # A timestamp is provenance, not surface identity.
        for key, value in record.items():
            if key != "frozen_at" and saved.get(key) != value:
                raise RuntimeError(f"manifest mismatch for {key}")
        print(json.dumps({
            "verified": True,
            "path": str(output),
            "public_names": record["public_names"],
            "definition_sites": record["definition_sites"],
            "comprehension_manifest_sha256": record["comprehension_manifest_sha256"],
        }, indent=2))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(output)
    print(json.dumps({
        "frozen": True,
        "path": str(output),
        "public_names": record["public_names"],
        "definition_sites": record["definition_sites"],
        "comprehension_manifest_sha256": record["comprehension_manifest_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
