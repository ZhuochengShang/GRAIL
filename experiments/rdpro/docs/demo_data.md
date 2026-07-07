# GRAIL demo data — real Boston datasets

Small, real, overlapping datasets so every demo test case returns non-empty
results across all four capability groups. Build them with:

```bash
cd experiments/rdpro
python prepare_demo_data.py                 # full Boston bbox, 500 points
# or scope tighter to the existing 2-neighborhood sample:
python prepare_demo_data.py --bbox -71.107 42.267 -71.033 42.342 --max-points 300
```

Everything lands in `grail-agent/examples/fixtures/`.

## What gets created & why

| File | Source (license) | Unlocks |
|------|------------------|---------|
| `boston_neighborhoods.geojson` / `.shp` | Analyze Boston — *BPDA Neighborhood Boundaries* (public open data) | all ~26 polygons instead of 2 → richer **vector ops** + zonal zones |
| `boston_311_points.csv` (`longitude,latitude,…`) | Analyze Boston — *311 Service Requests* (public open data) | **point ops**: spatial join (point-in-polygon), kNN, point histogram, point range-query |
| `boston_worldcover_10m.tif` | ESA WorldCover 2021 v200, clipped (CC BY 4.0) | **raster×vector zonal** with real land-cover **classes** → makes "land-use %" literal; also **raster pixel ops** |
| `nldas_boston_30m.tif` *(already present)* | — | continuous **raster pixel ops** (band math, threshold, reproject) |

WorldCover class codes: `10` tree, `20` shrub, `30` grass, `40` crop, `50` built-up,
`60` bare, `80` water, `90` wetland. Attribution: *© ESA WorldCover project 2021 /
Contains modified Copernicus Sentinel data*.

The prep script resolves the CKAN download URLs at run time (they rotate) and clips
the WorldCover COG with a windowed `/vsicurl` read, so only the Boston window (a few
MB) is fetched, not the full 3°×3° tile.

## Wiring into the demo

The demo binds one raster + one vector + one CSV (`raster_tif`, `vector_geojson`,
`table_csv`, `output_dir`). Pick a profile in
`configs/aideal.yaml → comprehension.execute.sample_data`:

**Land-use / zonal profile** (class raster + polygons + attribute CSV):
```yaml
sample_data:
  raster_tif: ../../grail-agent/examples/fixtures/boston_worldcover_10m.tif
  vector_shapefile: ../../grail-agent/examples/fixtures/boston_neighborhoods.shp
  table_csv: ../../grail-agent/examples/fixtures/boston_land_use_summary_sample.csv
```

**Point-ops profile** (points CSV as the table input):
```yaml
sample_data:
  raster_tif: ../../grail-agent/examples/fixtures/nldas_boston_30m.tif
  vector_shapefile: ../../grail-agent/examples/fixtures/boston_neighborhoods.shp
  table_csv: ../../grail-agent/examples/fixtures/boston_311_points.csv
```

(Use absolute paths if your `aideal.yaml` already does; confirm the neighborhood
zone field with `ogrinfo -so boston_neighborhoods.shp` — expected `name`.)

## New test cases the points data unlocks

Add these to `docs/demo_test_cases.md` (Group 5 — point ops) once the point-ops
profile is active:

```bash
# 5.1 point-in-polygon spatial join -> requests per neighborhood
python demo_agent.py --execute --text "Load the 311 points from the CSV (x=longitude, y=latitude), spatially join them to the Boston neighborhood polygons, and write the number of requests per neighborhood to CSV."   # spatialJoin

# 5.2 point density histogram
python demo_agent.py --execute --text "Load the 311 points and compute a uniform 2D spatial histogram of point counts over the Boston bounding box; save the grid counts to CSV."   # computePointHistogramSparse / uniformHistogramCount

# 5.3 range query on points
python demo_agent.py --execute --text "Return only the 311 points that fall inside the bounding box minx=-71.10 miny=42.30 maxx=-71.05 maxy=42.35 and save them as GeoJSON."   # rangeQuery

# 5.4 rasterize points
python demo_agent.py --execute --text "Rasterize the 311 points into a 100x100 count grid over the Boston extent and save the grid as a GeoTIFF."   # rasterizePoints
```

All four API names (`spatialJoin`, `computePointHistogramSparse`,
`uniformHistogramCount`, `rangeQuery`, `rasterizePoints`) are in `docs/LLM_readme.md`.
