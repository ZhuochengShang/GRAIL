#!/usr/bin/env python3
"""
Prepare small, REAL demo datasets for the GRAIL demo agent (Boston).

Fetches three public sources, trims each to a small Boston window, and drops the
results into grail-agent/examples/fixtures/ so the demo agent's test cases return
non-empty results across all four capability groups:

  1. Boston neighborhood polygons (all ~26)      -> vector ops + zonal zones
     Analyze Boston (CKAN): bpda-neighborhood-boundaries   [public open data]
  2. 311 service-request POINTS (lon/lat)         -> spatial join / kNN / point histogram
     Analyze Boston (CKAN): 311-service-requests           [public open data]
  3. ESA WorldCover 10 m land-cover CLASS raster  -> land-use % zonal (literal), pixel ops
     esa-worldcover S3 COG, clipped via /vsicurl          [CC BY 4.0]

Design notes:
  * CKAN resource URLs rotate, so we resolve them at run time from the package API
    instead of hard-coding them.
  * The WorldCover tile is a Cloud-Optimized GeoTIFF; `gdal_translate -projwin` over
    `/vsicurl/` downloads ONLY the Boston window (a few MB), not the 3x3-deg tile.
  * Every step is wrapped so a missing tool (gdal) or a network hiccup skips just
    that dataset rather than aborting the whole run.

Requires: internet, pandas; optional geopandas (geojson->shp) and GDAL CLI
(gdal_translate) for the land-cover clip.

Usage:
  python prepare_demo_data.py                 # full Boston bbox, 500 points
  python prepare_demo_data.py --max-points 300
  python prepare_demo_data.py --bbox -71.107 42.267 -71.033 42.342   # Roxbury+Dorchester only
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

# Repo layout: this file lives in experiments/rdpro/ ; fixtures are two levels up.
FIXTURES = (Path(__file__).resolve().parent.parent.parent
            / "grail-agent" / "examples" / "fixtures")
CKAN = "https://data.boston.gov/api/3/action/package_show?id={pkg}"
# ESA WorldCover 2021 v200, 3x3-deg tile whose SW corner is 42N, 72W -> covers Boston.
WORLDCOVER_TILE = ("https://esa-worldcover.s3.eu-central-1.amazonaws.com/"
                   "v200/2021/map/ESA_WorldCover_10m_2021_v200_N42W072_Map.tif")
# Full City-of-Boston land extent (lon/lat, EPSG:4326).
DEFAULT_BBOX = (-71.191, 42.227, -70.923, 42.397)


def _get(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "grail-demo-prep/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def ckan_resources(pkg: str) -> list[dict]:
    data = json.loads(_get(CKAN.format(pkg=pkg)))
    if not data.get("success"):
        raise RuntimeError(f"CKAN package_show failed for {pkg}")
    return data["result"]["resources"]


# --------------------------------------------------------------------------- #
def fetch_neighborhoods(out_dir: Path) -> None:
    print("[1/3] Boston neighborhood polygons ...")
    res = ckan_resources("bpda-neighborhood-boundaries")
    geo = [r for r in res if (r.get("format") or "").lower() == "geojson" and r.get("url")]
    if not geo:
        raise RuntimeError("no GeoJSON resource found in bpda-neighborhood-boundaries")
    dst = out_dir / "boston_neighborhoods.geojson"
    dst.write_bytes(_get(geo[0]["url"]))
    gj = json.loads(dst.read_text())
    props = list((gj["features"][0]["properties"]).keys()) if gj.get("features") else []
    print(f"      -> {dst.name}: {len(gj.get('features', []))} polygons; fields: {props}")
    # Best-effort shapefile copy (the config can bind either .geojson or .shp).
    try:
        import geopandas as gpd
        gpd.read_file(dst).to_file(out_dir / "boston_neighborhoods.shp")
        print(f"      -> boston_neighborhoods.shp (via geopandas)")
    except Exception as e:
        print(f"      (skipped .shp: {e}; use the .geojson binding)")


def fetch_311_points(out_dir: Path, bbox, max_points: int) -> None:
    print("[2/3] 311 service-request points ...")
    import pandas as pd
    res = ckan_resources("311-service-requests")
    csvs = [r for r in res if (r.get("format") or "").lower() == "csv" and r.get("url")]
    if not csvs:
        raise RuntimeError("no CSV resource found in 311-service-requests")

    def year_of(r):
        digits = "".join(c for c in (r.get("name") or "") if c.isdigit())
        return int(digits[:4]) if len(digits) >= 4 else 0
    latest = max(csvs, key=year_of)
    print(f"      source: {latest.get('name')}  (streaming + filtering to bbox)")

    minx, miny, maxx, maxy = bbox
    raw = io.BytesIO(_get(latest["url"], timeout=600))
    kept, chunks = [], pd.read_csv(raw, chunksize=50_000, low_memory=False)
    lat_col = lon_col = None
    for ch in chunks:
        if lat_col is None:
            cols = {c.lower(): c for c in ch.columns}
            lat_col = cols.get("latitude") or cols.get("lat") or cols.get("y")
            lon_col = cols.get("longitude") or cols.get("long") or cols.get("lon") or cols.get("x")
            if not (lat_col and lon_col):
                raise RuntimeError(f"no lat/lon columns in {list(ch.columns)[:20]}")
        ch = ch[[c for c in ch.columns]].copy()
        ch[lat_col] = pd.to_numeric(ch[lat_col], errors="coerce")
        ch[lon_col] = pd.to_numeric(ch[lon_col], errors="coerce")
        m = (ch[lon_col].between(minx, maxx) & ch[lat_col].between(miny, maxy))
        kept.append(ch[m])
        if sum(len(k) for k in kept) >= max_points * 4:
            break
    df = pd.concat(kept, ignore_index=True)
    if len(df) > max_points:
        df = df.sample(max_points, random_state=42).reset_index(drop=True)

    # Slim, RDPro-friendly point table: x=longitude, y=latitude + a couple attributes.
    keep_extra = [c for c in ("type", "reason", "case_status", "open_dt")
                  if c in {col.lower(): col for col in df.columns}]
    name_map = {col.lower(): col for col in df.columns}
    out = pd.DataFrame({"longitude": df[lon_col], "latitude": df[lat_col]})
    for c in keep_extra:
        out[c] = df[name_map[c]]
    dst = out_dir / "boston_311_points.csv"
    out.to_csv(dst, index=False)
    print(f"      -> {dst.name}: {len(out)} points (x=longitude, y=latitude), cols: {list(out.columns)}")


def clip_worldcover(out_dir: Path, bbox) -> None:
    print("[3/3] ESA WorldCover land-cover clip ...")
    if not shutil.which("gdal_translate"):
        print("      (skipped: gdal_translate not on PATH — install GDAL to build the class raster)")
        return
    minx, miny, maxx, maxy = bbox
    dst = out_dir / "boston_worldcover_10m.tif"
    cmd = [
        "gdal_translate",
        "--config", "GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR",
        "--config", "CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif",
        "-projwin", str(minx), str(maxy), str(maxx), str(miny),   # ulx uly lrx lry
        "-co", "COMPRESS=DEFLATE", "-co", "TILED=YES",
        f"/vsicurl/{WORLDCOVER_TILE}", str(dst),
    ]
    subprocess.run(cmd, check=True)
    print(f"      -> {dst.name} (10 m land-cover classes: 10=tree 50=built 80=water ...)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch + trim small real Boston demo datasets.")
    ap.add_argument("--bbox", type=float, nargs=4, default=list(DEFAULT_BBOX),
                    metavar=("MINX", "MINY", "MAXX", "MAXY"))
    ap.add_argument("--max-points", type=int, default=500)
    ap.add_argument("--out-dir", type=Path, default=FIXTURES)
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    print(f"fixtures dir: {a.out_dir}\nbbox: {tuple(a.bbox)}\n")

    ok, fail = [], []
    for name, fn in (("neighborhoods", lambda: fetch_neighborhoods(a.out_dir)),
                     ("311-points", lambda: fetch_311_points(a.out_dir, a.bbox, a.max_points)),
                     ("worldcover", lambda: clip_worldcover(a.out_dir, a.bbox))):
        try:
            fn(); ok.append(name)
        except Exception as e:
            fail.append(name); print(f"      !! {name} failed: {e}")
    print(f"\nDONE. ready: {ok}" + (f" | failed: {fail}" if fail else ""))
    print("Next: point the demo's sample_data at these files — see docs/demo_data.md.")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
