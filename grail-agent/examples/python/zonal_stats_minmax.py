#!/usr/bin/env python3
"""
Zonal statistics (min, max, count) per polygon.
Supports single file, directory of files, and VRT-based merging.

Usage:
  # Single file, crop=True
  python zonal_stats_minmax.py --raster meris.tif --shapefile us_counties --zone-field NAME --output-csv out.csv --crop

  # Directory, crop=True
  python zonal_stats_minmax.py --raster treecover_us/ --shapefile us_counties --zone-field NAME --output-csv out.csv --crop

  # Directory, VRT merge per polygon (no double-counting on tile boundaries)
  python zonal_stats_minmax.py --raster LandsatTreecover/ --shapefile us_counties --zone-field NAME --output-csv out.csv --vrt
"""
import argparse, csv, os, subprocess, tempfile, warnings
from pathlib import Path
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask

NODATA_VALUES = {250, -9999, 32767, -32768}

def geometry_overlaps_raster(bounds, geometry) -> bool:
    minx, miny, maxx, maxy = geometry.bounds
    return not (maxx < bounds.left or minx > bounds.right or
                maxy < bounds.bottom or miny > bounds.top)

def raster_overlaps_geometry(raster_path: Path, geometry) -> bool:
    with rasterio.open(raster_path) as src:
        return geometry_overlaps_raster(src.bounds, geometry)

def extract_stats(band, nodata):
    if np.ma.isMaskedArray(band):
        data = band.data[~np.ma.getmaskarray(band)].astype(np.int32)
    else:
        data = band.flatten().astype(np.int32)
    if nodata is not None:
        data = data[data != int(nodata)]
    return data[~np.isin(data, list(NODATA_VALUES))]

def merge_stats(zone_stats, zone_key, data):
    if data.size == 0:
        return
    if zone_key not in zone_stats:
        zone_stats[zone_key] = [int(data.min()), int(data.max()), int(data.size)]
    else:
        s = zone_stats[zone_key]
        s[0] = min(s[0], int(data.min()))
        s[1] = max(s[1], int(data.max()))
        s[2] += int(data.size)

def run_multifile(raster_files, gdf, zone_field, crop):
    zone_stats = {}
    for i, rfile in enumerate(raster_files):
        print(f"[{i+1}/{len(raster_files)}] {rfile.name}")
        try:
            with rasterio.open(rfile) as src:
                nodata = src.nodata
                for feature_idx, row in gdf.iterrows():
                    zone_name = str(row[zone_field])
                    zone_key = (feature_idx, zone_name)
                    geom = row.geometry
                    if not geometry_overlaps_raster(src.bounds, geom):
                        continue
                    try:
                        out_img, _ = mask(src, [geom], crop=crop, filled=False)
                        data = extract_stats(out_img[0], nodata)
                        merge_stats(zone_stats, zone_key, data)
                    except Exception as e:
                        warnings.warn(f"Failed for {zone_name} in {rfile.name}: {e}")
        except Exception as e:
            warnings.warn(f"Failed to open {rfile.name}: {e}")
    return zone_stats

def run_vrt(raster_files, gdf, zone_field):
    """Build VRT per polygon from overlapping tiles — GDAL handles boundaries correctly."""
    zone_stats = {}
    total = len(gdf)
    for idx, (feature_idx, row) in enumerate(gdf.iterrows()):
        zone_name = str(row[zone_field])
        zone_key = (feature_idx, zone_name)
        geom = row.geometry
        if idx % 100 == 0:
            print(f"[{idx}/{total}] {zone_name}")
        overlapping = [
            str(rfile) for rfile in raster_files
            if raster_overlaps_geometry(rfile, geom)
        ]
        if not overlapping:
            continue
        vrt_fd, vrt_path = tempfile.mkstemp(suffix=".vrt")
        os.close(vrt_fd)
        try:
            subprocess.run(["gdalbuildvrt", vrt_path] + overlapping,
                           capture_output=True, text=True, check=True)
            with rasterio.open(vrt_path) as src:
                nodata = src.nodata
                geom_proj = gpd.GeoSeries([geom], crs=gdf.crs).to_crs(src.crs).iloc[0] \
                            if gdf.crs != src.crs else geom
                try:
                    out_img, _ = mask(src, [geom_proj], crop=True, filled=False)
                    data = extract_stats(out_img[0], nodata)
                    merge_stats(zone_stats, zone_key, data)
                except Exception as e:
                    warnings.warn(f"Failed mask for {zone_name}: {e}")
        except FileNotFoundError:
            raise RuntimeError("gdalbuildvrt was not found on PATH; install GDAL or avoid --vrt")
        except subprocess.CalledProcessError as e:
            warnings.warn(
                f"gdalbuildvrt failed for {zone_name}: {e.stderr.strip() or e}"
            )
        finally:
            if os.path.exists(vrt_path):
                os.unlink(vrt_path)
    return zone_stats

def zonal_stats(raster_path, shapefile_path, zone_field, output_csv, crop, use_vrt):
    raster_files = (
        sorted(p for p in raster_path.iterdir() if p.is_file() and p.suffix.lower() == ".tif")
        if raster_path.is_dir() else [raster_path]
    )
    print(f"Found {len(raster_files)} raster file(s)")
    if not raster_files:
        raise ValueError(f"No .tif files found in raster directory: {raster_path}")
    if not raster_path.is_dir() and not raster_path.exists():
        raise FileNotFoundError(f"Raster file not found: {raster_path}")

    with rasterio.open(raster_files[0]) as src:
        raster_crs = src.crs

    gdf = gpd.read_file(shapefile_path)
    if gdf.crs is None:
        raise ValueError("Input shapefile/vector layer has no CRS; define one before running zonal stats")
    if gdf.crs != raster_crs:
        gdf = gdf.to_crs(raster_crs)
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.reset_index(drop=True)
    if zone_field not in gdf.columns:
        raise ValueError(f"Field '{zone_field}' not found. Available: {list(gdf.columns)}")
    print(f"Loaded {len(gdf)} features")

    if use_vrt and raster_path.is_dir():
        print("Mode: VRT per polygon (correct boundary handling)")
        zone_stats = run_vrt(raster_files, gdf, zone_field)
    else:
        print(f"Mode: multifile, crop={crop}")
        zone_stats = run_multifile(raster_files, gdf, zone_field, crop)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["feature_id","zone_name","min","max","count"])
        writer.writeheader()
        for (feature_id, name), (mn, mx, cnt) in sorted(zone_stats.items()):
            writer.writerow({
                "feature_id": feature_id,
                "zone_name": name,
                "min": mn,
                "max": mx,
                "count": cnt,
            })
    print(f"Wrote {len(zone_stats)} rows to {output_csv}")

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--raster",     type=Path, required=True)
    p.add_argument("--shapefile",  type=Path, required=True)
    p.add_argument("--zone-field", default="NAME")
    p.add_argument("--output-csv", type=Path, default=Path("zonal_stats_out.csv"))
    p.add_argument("--crop", action="store_true", default=False)
    p.add_argument("--vrt",  action="store_true", default=False)
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.vrt and not args.raster.is_dir():
        raise ValueError("--vrt requires --raster to be a directory")
    zonal_stats(args.raster, args.shapefile, args.zone_field,
                args.output_csv, args.crop, args.vrt)
