# GRAIL demo agent — test cases

A menu of end-to-end tasks for `experiments/rdpro/demo_agent.py`.

> **Fixing the old canonical example.** `"Compute land-use % per Boston
> neighborhood ..."` (still referenced in `RUNBOOK.md`) was never finished as
> a sentence, and — more importantly — `raster_tif` is pinned to NLDAS, a
> **continuous-value climate raster** (temperature / precipitation / soil
> moisture), not a land-cover classification. There is no "land use" encoded
> in that raster to compute a percentage of, so every run against it has been
> guessing at an unanswerable task. The canonical example below is now
> literally Case 1.1 — a task that matches what the pinned raster actually
> contains. Genuine land-use % belongs to **Group 4** (CSV attribute join,
> using `table_csv`) until a real land-cover raster fixture (e.g. NLCD) is
> pinned for Group 1.

```bash
python demo_agent.py --execute --text "Using a raptor join between the raster and the Boston neighborhood polygons, compute the mean, minimum, and maximum pixel value for each neighborhood. Write one row per neighborhood (name, mean, min, max, pixel_count) to CSV in the output directory."
```

Every case runs against the pinned fixtures in `configs/aideal.yaml → comprehension.execute.sample_data`
(+ the auto-discovered fixtures folder), so the in-scope input vals are:

| val | fixture | what it is |
|-----|---------|------------|
| `raster_tif` | `nldas_boston_30m.tif` | Boston-region NLDAS raster, continuous float values (climate, not land-cover) |
| `vector_geojson` / `vector_shapefile` | `Boston_Neighborhood_Boundaries_sample_grail.*` | neighborhood polygons; zone field = `name` (e.g. Roxbury, Dorchester) |
| `table_csv` | `boston_land_use_*_sample.csv` | per-neighborhood land-use table; key column = `zone_name` |
| `output_dir` | `experiments/rdpro/exec_out` | where the job writes results |

Each case notes the **documented RDPro API(s)** it should drive (all names verified
against `docs/LLM_readme.md`) so a failed translation tells you which API's doc /
alias / error-log entry needs work. Run offline with `--dry-run`, or for real with
`--execute` (needs `OPENAI_API_KEY` + working `spark-submit`).

---

## Group 1 — Raster × Vector (raptor join / zonal stats) — core showcase

Closest to the canonical land-use example; exercises `raptorJoin`, `raptorJoinFeature`, `zonalStatsLocal`.

**1.1 — Zonal mean/min/max per neighborhood**
```bash
python demo_agent.py --execute --text "Using a raptor join between the raster and the Boston neighborhood polygons, compute the mean, minimum, and maximum pixel value for each neighborhood. Write one row per neighborhood (name, mean, min, max, pixel_count) to CSV in the output directory."
```
APIs: `raptorJoin` / `raptorJoinFeature`, `zonalStatsLocal`, `saveAsCSVPoints`. Out: per-neighborhood CSV.

**1.2 — Pixel count per zone + hottest neighborhood**
```bash
python demo_agent.py --execute --text "For each Boston neighborhood polygon, count how many raster pixels fall inside it and compute the average value, then report the single neighborhood with the highest average value."
```
APIs: `raptorJoinFeature` + aggregate/reduce. Out: one (name, avg) record.

**1.3 — Total raster value per zone**
```bash
python demo_agent.py --execute --text "Compute the sum of all raster pixel values that fall within each neighborhood polygon and save neighborhood name and total to CSV."
```
APIs: `raptorJoin` + sum. Out: per-neighborhood CSV.

## Group 2 — Raster-only (pixel math / reproject / filter)

Exercises `mapPixels`, `filterPixels`, `reproject`, `saveAsGeoTiff` — no vector input.

**2.1 — Per-pixel unit conversion (band math)**
```bash
python demo_agent.py --execute --text "Convert every raster pixel from Kelvin to Celsius by subtracting 273.15, and write the converted raster as a GeoTIFF to the output directory."
```
APIs: `mapPixels`, `saveAsGeoTiff`. (Parallels `examples/python/ndvi.py`.)

**2.2 — Reproject raster**
```bash
python demo_agent.py --execute --text "Reproject the raster to EPSG:4326 and save it as a GeoTIFF in the output directory."
```
APIs: `reproject` / `reprojectRDD`, `saveAsGeoTiff`.

**2.3 — Threshold mask**
```bash
python demo_agent.py --execute --text "Keep only raster pixels whose value is greater than 300, set all other pixels to nodata, and write the masked raster as a GeoTIFF."
```
APIs: `filterPixels`, `saveAsGeoTiff`. (Mirrors `examples/python/raster_threshold_mask.py`.)

**2.4 — Raster to points**
```bash
python demo_agent.py --execute --text "Convert every non-empty raster pixel into a point feature carrying its value as an attribute, and save the points as GeoJSON."
```
APIs: `pixelLocations` / `flatten`, `saveAsGeoJSON`. (Mirrors `examples/python/raster_to_points.py`.)

## Group 3 — Vector-only (measure / reproject / range query)

Exercises `area`, `rangeQuery`, `reprojectGeometry`, `saveAsShapefile` — no raster input.

**3.1 — Area per polygon, ranked**
```bash
python demo_agent.py --execute --text "Compute the area of each Boston neighborhood polygon and write neighborhood name and area to CSV, sorted by area descending."
```
APIs: `geojsonFile`/`shapefile`, `area`, `saveAsCSVPoints`. (Mirrors `examples/python/polygon_area_rank.py`.)

**3.2 — Range query by bounding box**
```bash
python demo_agent.py --execute --text "Return only the neighborhood polygons that intersect the bounding box minx=-71.10, miny=42.30, maxx=-71.05, maxy=42.35, and save the matches as GeoJSON."
```
APIs: `rangeQuery`, `saveAsGeoJSON`. (Mirrors `examples/python/bbox_clip.py`.)

**3.3 — Reproject polygons**
```bash
python demo_agent.py --execute --text "Reproject the Boston neighborhood polygons to EPSG:3857 and save them as a shapefile in the output directory."
```
APIs: `reprojectGeometry` / `reproject`, `saveAsShapefile`.

## Group 4 — Vector × Table (attribute join)

Exercises the CSV reader + attribute join — uses `table_csv` + `vector_geojson`. This is
where genuine "land-use %" belongs, since `table_csv` is the only fixture that actually
encodes land-use categories.

**4.1 — Join land-use table onto polygons**
```bash
python demo_agent.py --execute --text "Load the land-use summary CSV, join it to the neighborhood polygons on the neighborhood name (CSV column zone_name = polygon field name), attach each polygon's dominant land-use label as an attribute, and save the enriched polygons as GeoJSON."
```
APIs: `readCSVPoint`/table read, join, `saveAsGeoJSON`. (Mirrors `examples/python/csv_join_polygons.py`.)

---

## Python-script cases (`--python`)

Same tasks fed as single-machine Python for the agent to translate (tests the
Python→Scala path, not just NL→Scala). Existing scripts plus the five new ones:

```bash
# existing
python demo_agent.py --execute --python ../../grail-agent/examples/python/zonal_stats_minmax.py
python demo_agent.py --execute --python ../../grail-agent/examples/python/nlcd_clip_zonal.py
python demo_agent.py --execute --python ../../grail-agent/examples/python/ndvi.py

# new (each a distinct RDPro capability)
python demo_agent.py --execute --python ../../grail-agent/examples/python/raster_threshold_mask.py   # filterPixels
python demo_agent.py --execute --python ../../grail-agent/examples/python/polygon_area_rank.py        # area
python demo_agent.py --execute --python ../../grail-agent/examples/python/bbox_clip.py                # rangeQuery
python demo_agent.py --execute --python ../../grail-agent/examples/python/raster_to_points.py         # pixelLocations
python demo_agent.py --execute --python ../../grail-agent/examples/python/csv_join_polygons.py        # attribute join
```

## Running the whole suite at once

`run_test_suite.py` parses this file directly (the numbered cases above, and
optionally the `--python` cases) and runs each through the same 5-step
pipeline as a single `demo_agent.py` invocation — so this doc and the runner
can never drift apart; there's no separately-maintained case list.

```bash
python run_test_suite.py --dry-run                    # offline sanity check, no key/cluster needed
python run_test_suite.py --execute                     # real run, ALL numbered cases
python run_test_suite.py --execute --group 1            # just Group 1 (1.1, 1.2, 1.3)
python run_test_suite.py --execute --only 1.1,2.1,4.1   # a hand-picked subset
python run_test_suite.py --execute --include-python     # also run the --python cases
python run_test_suite.py --execute --show-code          # print each section's generated code + errors live
```

**Where to look afterward** (default `results/`, next to `docs/` and `logs/`):
- `results/<id>_<slug>.scala` — the generated Scala for that case (sections concatenated in order,
  even if it stopped partway through — the file shows exactly how far it got)
- `results/<id>_<slug>.json` — structured result: `status` (`RUNNABLE`/`unresolved`/`error`),
  `primary_api`, `sections`, `apis_by_section`, `failed_section` if any, `scala_path`
- `results/SUMMARY.md` — one table across every case in the run: id, title, status, primary_api,
  failed_section, scala filename — the fastest way to see what passed without opening each file

Every attempt across every case still logs to the same `logs/error_log.jsonl` `comprehension
--execute` and `augment` use, tagged with that case's id as the `task` field — so `aideal
alias-suggest` / `aideal notes-distill` pick up patterns across the whole suite, not just one run.

## How to read a single run

- `--dry-run` stubs the LLM + Spark to show the analyze → sections → log wiring offline.
- On `--execute`, watch `[analyze] primary_api=...` and `[SECTION ...] attempt N: PASS/FAIL`;
  failures append to `logs/error_log.jsonl` with a category + fix hint, get distilled into
  `docs/notes_to_self.md`, and are replayed into the next attempt for that section.
- `[alias proposals mined from failures]` shows hallucinated names worth adding as aliases.

A case that keeps failing on the same API is a signal that that API's `LLM_readme`
entry, alias, or I/O hint is the weak spot — which is the whole point of the harness.