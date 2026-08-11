from __future__ import annotations

import json
from pathlib import Path

import pytest

from aideal.puzzle_bank import (
    freeze_puzzle_plan,
    load_structured,
    validate_bank,
    verify_plan_inputs,
)


def _write_minimal_bank(root: Path) -> tuple[Path, Path, Path]:
    fixture = root / "fixture.tif"
    fixture.write_bytes(b"small-fixture")
    bank = root / "bank.yaml"
    bank.write_text(
        """\
schema_version: 1
bank_id: test
cases:
  - id: case_a
    modes: [composition, discovery]
    goal: compose a workflow
    user_prompt: solve the task
    apis: [loadRaster, writeRaster]
    datasets: [raster]
    output: {format: GeoTIFF, file: result.tif}
  - id: case_b
    modes: [composition]
    goal: another workflow
    apis: [loadRaster]
    datasets: [raster]
""",
        encoding="utf-8",
    )
    data = root / "data.yaml"
    data.write_text(
        """\
schema_version: 1
datasets:
  raster:
    path: fixture.tif
    kind: raster
    format: GeoTIFF
""",
        encoding="utf-8",
    )
    return bank, data, fixture


def test_freeze_plan_is_deterministic_and_hashes_inputs(tmp_path: Path) -> None:
    bank, data, fixture = _write_minimal_bank(tmp_path)
    first = freeze_puzzle_plan(
        root=tmp_path,
        bank_path=bank,
        sample_data_path=data,
        mode="composition",
        sample=1,
        seed=17,
        documented_apis={"loadRaster", "writeRaster"},
    )
    second = freeze_puzzle_plan(
        root=tmp_path,
        bank_path=bank,
        sample_data_path=data,
        mode="composition",
        sample=1,
        seed=17,
        documented_apis={"loadRaster", "writeRaster"},
    )
    assert first == second
    assert first["cases"][0]["datasets"][0]["sha256"]
    assert verify_plan_inputs(first) == []

    fixture.write_bytes(b"changed")
    assert "dataset hash changed" in verify_plan_inputs(first)[0]


def test_discovery_plan_filters_composition_only_cases(tmp_path: Path) -> None:
    bank, data, _ = _write_minimal_bank(tmp_path)
    plan = freeze_puzzle_plan(
        root=tmp_path,
        bank_path=bank,
        sample_data_path=data,
        mode="discovery",
        seed=42,
        documented_apis={"loadRaster", "writeRaster"},
    )
    assert plan["case_ids"] == ["case_a"]
    assert plan["cases"][0]["mode"] == "discovery"


def test_plan_hashes_optional_semantic_oracle(tmp_path: Path) -> None:
    bank, data, _ = _write_minimal_bank(tmp_path)
    oracle = tmp_path / "oracle.csv"
    oracle.write_text("value\n1\n", encoding="utf-8")
    text = bank.read_text(encoding="utf-8")
    bank.write_text(text.replace("    output: {format: GeoTIFF, file: result.tif}\n",
                                 "    output: {format: GeoTIFF, file: result.tif}\n"
                                 "    oracle: oracle.csv\n", 1), encoding="utf-8")
    plan = freeze_puzzle_plan(
        root=tmp_path,
        bank_path=bank,
        sample_data_path=data,
        mode="discovery",
        documented_apis={"loadRaster", "writeRaster"},
    )
    assert plan["cases"][0]["oracle"]["sha256"]
    oracle.write_text("value\n2\n", encoding="utf-8")
    assert "oracle hash changed" in verify_plan_inputs(plan)[0]


def test_bank_rejects_undocumented_api(tmp_path: Path) -> None:
    bank, data, _ = _write_minimal_bank(tmp_path)
    errors = validate_bank(
        load_structured(bank),
        load_structured(data),
        documented_apis={"loadRaster"},
    )
    assert "case_a: API is not documented: writeRaster" in errors
    with pytest.raises(ValueError, match="writeRaster"):
        freeze_puzzle_plan(
            root=tmp_path,
            bank_path=bank,
            sample_data_path=data,
            documented_apis={"loadRaster"},
        )


def test_checked_in_rdpro_bank_and_samples_freeze() -> None:
    repo = Path(__file__).resolve().parents[2]
    project = repo / "experiments" / "rdpro"
    bank = project / "configs" / "puzzle_test_bank.yaml"
    data = project / "configs" / "puzzle_sample_data.yaml"
    readme = (project / "docs" / "LLM_readme.md").read_text(encoding="utf-8")
    documented = {
        line.split("`")[1]
        for line in readme.splitlines()
        if line.startswith("## API Test: `")
    }
    plan = freeze_puzzle_plan(
        root=project,
        bank_path=bank,
        sample_data_path=data,
        documented_apis=documented,
    )
    assert len(plan["cases"]) == 5
    assert verify_plan_inputs(plan) == []
    assert all(case["datasets"] for case in plan["cases"])
