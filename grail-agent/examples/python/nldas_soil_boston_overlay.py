"""
NLDAS Soil Overlay -> 30 m Raster
=================================

Pipeline:
  1. Read the overlay boundary shapefile.
  2. Reproject the boundary to EPSG:4326.
  3. Build an approximate local 30 m grid in EPSG:4326.
  4. Reproject NLDAS directly to that 30 m grid with bilinear interpolation.
  5. Mask the output to the exact boundary geometry and write the GeoTIFF.
"""

from __future__ import annotations

from math import ceil, cos, radians
from pathlib import Path
from time import perf_counter

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from rasterio.warp import reproject
from shapely.ops import unary_union


# ---------------------------------------------------------------------------
# Paths — update if needed
# ---------------------------------------------------------------------------
NLDAS_PATH = (
    "/Users/clockorangezoe/Documents/phd_projects/code/baitsss_model_fieldsat/"
    "data/NLDAS2019_Geotiff_test/2019-09-23/"
    "NLDAS_FORA0125_H.A20190923.0000.002.tif"
)
BOUNDARY_PATH = (
    "/Users/clockorangezoe/Documents/phd_projects/data/Vector/cali_simplify/cali_simplify.shp"
)
OUTPUT_PATH = (
    "/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/python/"
    "nldas_soil_overlay_30m.tif"
)


# ---------------------------------------------------------------------------
# Grid configuration
# ---------------------------------------------------------------------------
TARGET_CRS = "EPSG:4326"
TARGET_RESOLUTION_M = 30.0
NODATA_VALUE = -9999.0


def _ensure_parent(path: str) -> None:
    Path(path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def _meters_to_degrees_lat(meters: float) -> float:
    return meters / 111_320.0


def _meters_to_degrees_lon(meters: float, latitude_deg: float) -> float:
    return meters / (111_320.0 * cos(radians(latitude_deg)))


def _build_target_grid(gdf_4326: gpd.GeoDataFrame) -> tuple[rasterio.Affine, int, int]:
    minx, miny, maxx, maxy = gdf_4326.total_bounds
    center_lat = (miny + maxy) / 2.0
    xres = _meters_to_degrees_lon(TARGET_RESOLUTION_M, center_lat)
    yres = _meters_to_degrees_lat(TARGET_RESOLUTION_M)
    width = max(1, int(ceil((maxx - minx) / xres)))
    height = max(1, int(ceil((maxy - miny) / yres)))
    transform = from_origin(minx, maxy, xres, yres)
    return transform, width, height


def _mask_to_geometry(
    array: np.ndarray,
    transform: rasterio.Affine,
    height: int,
    width: int,
    geometry,
    nodata: float,
) -> np.ndarray:
    mask = geometry_mask(
        [geometry],
        transform=transform,
        invert=True,
        out_shape=(height, width),
    )
    masked = array.copy()
    if masked.ndim == 3:
        masked[:, ~mask] = nodata
    else:
        masked[~mask] = nodata
    return masked


def main() -> None:
    total_start = perf_counter()

    print("Loading overlay boundary ...")
    t0 = perf_counter()
    boundary_gdf = gpd.read_file(BOUNDARY_PATH)
    if boundary_gdf.empty:
        raise ValueError("Boundary shapefile is empty.")

    boundary_4326 = boundary_gdf.to_crs(TARGET_CRS)
    boundary_union = unary_union(boundary_4326.geometry)
    transform, width, height = _build_target_grid(boundary_4326)

    print(f"  Target CRS      : {TARGET_CRS}")
    print(f"  Target shape    : {height} x {width}")
    print(f"  Target res      : approx {TARGET_RESOLUTION_M} m")
    print(f"  Boundary time   : {perf_counter() - t0:.2f} s")

    with rasterio.open(NLDAS_PATH) as src:
        t1 = perf_counter()
        src_nodata = src.nodata if src.nodata is not None else NODATA_VALUE
        dtype = np.float32

        dest = np.full((src.count, height, width), NODATA_VALUE, dtype=dtype)

        print(f"  Source CRS      : {src.crs}")
        print(f"  Source shape    : {src.height} x {src.width}")

        for band_idx in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, band_idx),
                destination=dest[band_idx - 1],
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=TARGET_CRS,
                src_nodata=src_nodata,
                dst_nodata=NODATA_VALUE,
                resampling=Resampling.bilinear,
            )
        print(f"  Reproject time  : {perf_counter() - t1:.2f} s")

        t2 = perf_counter()
        dest = _mask_to_geometry(
            dest,
            transform=transform,
            height=height,
            width=width,
            geometry=boundary_union,
            nodata=NODATA_VALUE,
        )
        print(f"  Mask time       : {perf_counter() - t2:.2f} s")

        profile = src.profile.copy()
        profile.update(
            crs=TARGET_CRS,
            transform=transform,
            width=width,
            height=height,
            count=src.count,
            dtype="float32",
            nodata=NODATA_VALUE,
        )

    t3 = perf_counter()
    _ensure_parent(OUTPUT_PATH)
    with rasterio.open(OUTPUT_PATH, "w", **profile) as dst:
        dst.write(dest)
    print(f"  Write time      : {perf_counter() - t3:.2f} s")

    print(f"Output written: {OUTPUT_PATH}")
    print(f"Total runtime: {perf_counter() - total_start:.2f} s")


if __name__ == "__main__":
    main()
