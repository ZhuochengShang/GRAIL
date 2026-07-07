#!/usr/bin/env python3
"""
Convert each non-nodata raster pixel into a point feature carrying its value.

Single-machine reference implementation (rasterio). The GRAIL demo agent should
translate this to an RDPro job that reads the raster, emits pixel-center points
with the value as an attribute (pixelLocations / flatten), and saves GeoJSON.

Usage:
  python raster_to_points.py --raster ../fixtures/nldas_boston_30m.tif \
      --output-geojson pixels.geojson
"""
import argparse
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from shapely.geometry import Point


DEFAULT_RASTER = Path(__file__).resolve().parent.parent / "fixtures" / "nldas_boston_30m.tif"


def raster_to_points(raster_path: Path, output_geojson: Path) -> None:
    with rasterio.open(raster_path) as src:
        band = src.read(1).astype(np.float32)
        nodata = src.nodata
        transform = src.transform
        crs = src.crs

        valid = np.isfinite(band)
        if nodata is not None:
            valid &= band != nodata
        rows, cols = np.nonzero(valid)
        if rows.size == 0:
            raise ValueError("No valid (non-nodata) pixels in raster")

        # Pixel-center coordinates in the raster CRS.
        xs, ys = rasterio.transform.xy(transform, rows, cols, offset="center")
        values = band[rows, cols]

    gdf = gpd.GeoDataFrame(
        {"value": values},
        geometry=[Point(x, y) for x, y in zip(xs, ys)],
        crs=crs,
    )
    output_geojson.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(output_geojson, driver="GeoJSON")
    print(f"Wrote {len(gdf)} pixel points to {output_geojson}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Raster pixels -> point features (value attribute).")
    p.add_argument("--raster", type=Path, default=DEFAULT_RASTER)
    p.add_argument("--output-geojson", type=Path, default=Path("raster_points.geojson"))
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    raster_to_points(args.raster, args.output_geojson)
