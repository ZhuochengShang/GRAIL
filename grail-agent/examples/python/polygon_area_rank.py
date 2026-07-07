#!/usr/bin/env python3
"""
Compute the area of each polygon and rank neighborhoods largest-first.

Single-machine reference implementation (geopandas). The GRAIL demo agent should
translate this to an RDPro vector job (load polygons -> `area` -> save CSV).
Vector-only: touches the neighborhood polygons, no raster.

Usage:
  python polygon_area_rank.py --vector ../fixtures/Boston_Neighborhood_Boundaries_sample_grail.shp \
      --zone-field name --output-csv neighborhood_area.csv
"""
import argparse
from pathlib import Path

import geopandas as gpd

DEFAULT_VECTOR = (Path(__file__).resolve().parent.parent / "fixtures"
                  / "Boston_Neighborhood_Boundaries_sample_grail.shp")
# World Mollweide: an equal-area projection so polygon areas are meaningful (m^2).
EQUAL_AREA_CRS = "ESRI:54009"


def polygon_area_rank(vector_path: Path, zone_field: str, output_csv: Path) -> None:
    gdf = gpd.read_file(vector_path)
    if gdf.empty:
        raise ValueError(f"Vector layer has no features: {vector_path}")
    if zone_field not in gdf.columns:
        raise ValueError(f"Field '{zone_field}' not found. Available: {list(gdf.columns)}")
    if gdf.crs is None:
        raise ValueError("Vector layer has no CRS; define one before computing area")

    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()
    gdf["area_m2"] = gdf.to_crs(EQUAL_AREA_CRS).geometry.area
    ranked = (gdf[[zone_field, "area_m2"]]
              .sort_values("area_m2", ascending=False)
              .rename(columns={zone_field: "zone_name"}))

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(output_csv, index=False)
    print(f"Wrote {len(ranked)} ranked neighborhoods to {output_csv}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Area per polygon, ranked descending.")
    p.add_argument("--vector", type=Path, default=DEFAULT_VECTOR)
    p.add_argument("--zone-field", default="name")
    p.add_argument("--output-csv", type=Path, default=Path("neighborhood_area.csv"))
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    polygon_area_rank(args.vector, args.zone_field, args.output_csv)
