#!/usr/bin/env python3
"""
Attribute-join a CSV table to polygons and write the enriched polygons.

Single-machine reference implementation (pandas + geopandas). The GRAIL demo
agent should translate this to an RDPro job that reads the CSV table + the
vector layer, joins on a shared key, and saves the enriched features as GeoJSON.
Touches all three inputs' spirit (table + vector), no raster.

Usage:
  python csv_join_polygons.py \
      --vector ../fixtures/Boston_Neighborhood_Boundaries_sample_grail.geojson \
      --csv ../fixtures/boston_land_use_summary_sample.csv \
      --vector-key name --csv-key zone_name \
      --output-geojson neighborhoods_landuse.geojson
"""
import argparse
from pathlib import Path

import geopandas as gpd
import pandas as pd

FIX = Path(__file__).resolve().parent.parent / "fixtures"
DEFAULT_VECTOR = FIX / "Boston_Neighborhood_Boundaries_sample_grail.geojson"
DEFAULT_CSV = FIX / "boston_land_use_summary_sample.csv"
# Columns from the summary CSV to attach to each polygon.
ATTACH_COLS = ["dominant_label", "dominant_pct", "pct_developed", "pct_forest"]


def csv_join_polygons(vector_path: Path, csv_path: Path, vector_key: str,
                      csv_key: str, output_geojson: Path) -> None:
    gdf = gpd.read_file(vector_path)
    if vector_key not in gdf.columns:
        raise ValueError(f"Vector key '{vector_key}' not found. Available: {list(gdf.columns)}")

    table = pd.read_csv(csv_path)
    if csv_key not in table.columns:
        raise ValueError(f"CSV key '{csv_key}' not found. Available: {list(table.columns)}")
    keep = [csv_key] + [c for c in ATTACH_COLS if c in table.columns]
    table = table[keep]

    merged = gdf.merge(table, how="left", left_on=vector_key, right_on=csv_key)
    if csv_key != vector_key and csv_key in merged.columns:
        merged = merged.drop(columns=[csv_key])
    unmatched = int(merged["dominant_label"].isna().sum()) if "dominant_label" in merged else 0

    output_geojson.parent.mkdir(parents=True, exist_ok=True)
    merged.to_file(output_geojson, driver="GeoJSON")
    print(f"Joined {len(merged)} polygons ({unmatched} without a CSV match); wrote {output_geojson}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Join a CSV table onto polygons by a shared key.")
    p.add_argument("--vector", type=Path, default=DEFAULT_VECTOR)
    p.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    p.add_argument("--vector-key", default="name")
    p.add_argument("--csv-key", default="zone_name")
    p.add_argument("--output-geojson", type=Path, default=Path("polygons_joined.geojson"))
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    csv_join_polygons(args.vector, args.csv, args.vector_key, args.csv_key, args.output_geojson)
