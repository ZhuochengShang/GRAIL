from __future__ import annotations

import json
from pathlib import Path

from rdpro_section_codegen.puzzle_eval import load_plan_puzzles


def _plan(tmp_path: Path, mode: str) -> Path:
    path = tmp_path / "plan.json"
    path.write_text(
        json.dumps({
            "schema_version": 1,
            "kind": "aideal_frozen_puzzle_plan",
            "mode": mode,
            "case_ids": ["case_a"],
            "cases": [{
                "id": "case_a",
                "mode": mode,
                "goal": "Compose the raster workflow.",
                "user_prompt": "Create the requested raster output.",
                "api_policy": "exact",
                "apis": [
                    {"name": "loadRaster", "stage": "load"},
                    {"name": "writeRaster", "stage": "output"},
                ],
                "datasets": [{
                    "id": "raster",
                    "uri": "file:///tmp/raster.tif",
                    "kind": "raster",
                    "format": "GeoTIFF",
                }],
                "output": {"format": "GeoTIFF", "file": "result.tif"},
            }],
        }),
        encoding="utf-8",
    )
    return path


def test_composition_plan_exposes_exact_api_names(tmp_path: Path) -> None:
    docs = tmp_path / "docs.md"
    docs.write_text(
        "## API Test: `loadRaster`\n### Goal\nload\n\n"
        "## API Test: `writeRaster`\n### Goal\nwrite\n",
        encoding="utf-8",
    )
    puzzles, _ = load_plan_puzzles(_plan(tmp_path, "composition"), docs)
    assert "`loadRaster`" in puzzles[0].task_text
    assert "`writeRaster`" in puzzles[0].task_text
    assert "{{OUTPUT_DIR}}/result.tif" in puzzles[0].task_text


def test_discovery_plan_hides_candidate_api_names_and_accepts_plain_docs(tmp_path: Path) -> None:
    docs = tmp_path / "original.md"
    docs.write_text("A plain original project guide with no AIDEAL headings.", encoding="utf-8")
    puzzles, _ = load_plan_puzzles(_plan(tmp_path, "discovery"), docs)
    prompt = puzzles[0].task_text
    assert "Create the requested raster output." in prompt
    assert "loadRaster" not in prompt
    assert "writeRaster" not in prompt
    assert puzzles[0].scoped_api_doc == docs.read_text(encoding="utf-8")
