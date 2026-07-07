#!/usr/bin/env python3
"""
Range query: keep only the polygons that intersect a bounding box.

Single-machine reference implementation (geopandas). The GRAIL demo agent should
translate this to an RDPro `rangeQuery` job that filters the vector RDD by a
query envelope and writes GeoJSON.

Usage:
  python bbox_clip.py --vector ../fixtures/Boston_Neighborhood_Boundaries_sample_grail.geojson \
      --bbox -71.10 42.30 -71.05 42.35 --output-geojson downtown.geojson
"""
import argparse
from pathlib import Path

import geopandas as gpd
from shapely.geometry import box


DEFAULT_VECTOR = (Path(__file__).resolve().parent.parent / "fixtures"
                  / "Boston_Neighborhood_Boundaries_sample_grail.geojson")


def bbox_clip(vector_path: Path, bbox, output_geojson: Path) -> None:
    minx, miny, maxx, maxy = bbox
    if minx >= maxx or miny >= maxy:
        raise ValueError(f"Empty bbox: min must be < max, got {bbox}")

    gdf = gpd.read_file(vector_path)
    if gdf.empty:
        raise ValueError(f"Vector layer has no features: {vector_path}")
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()

    query = box(minx, miny, maxx, maxy)
    hits = gdf[gdf.geometry.intersects(query)].copy()

    output_geojson.parent.mkdir(parents=True, exist_ok=True)
    if hits.empty:
        raise ValueError("No polygons intersect the bounding box")
    hits.to_file(output_geojson, driver="GeoJSON")
    print(f"{len(hits)}/{len(gdf)} polygons intersect the bbox; wrote {output_geojson}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Keep polygons intersecting a bounding box.")
    p.add_argument("--vector", type=Path, default=DEFAULT_VECTOR)
    p.add_argument("--bbox", type=float, nargs=4, metavar=("MINX", "MINY", "MAXX", "MAXY"),
                   required=True, help="Query window: minx miny maxx maxy (layer CRS units).")
    p.add_argument("--output-geojson", type=Path, default=Path("bbox_clip.geojson"))
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bbox_clip(args.vector, args.bbox, args.output_geojson)
