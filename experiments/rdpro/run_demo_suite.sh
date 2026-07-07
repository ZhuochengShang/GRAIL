#!/usr/bin/env bash
# GRAIL demo-agent regression suite.
# Runs every case in docs/demo_test_cases.md through demo_agent.py and tallies
# PASS/FAIL. Default mode is --dry-run (offline, stubs LLM+Spark); pass --execute
# to really compile + spark-submit (needs OPENAI_API_KEY + spark-submit).
#
# Usage:
#   ./run_demo_suite.sh                # dry-run all cases
#   ./run_demo_suite.sh --execute      # real translation + run
#   ./run_demo_suite.sh --execute --rounds 4
set -uo pipefail
cd "$(dirname "$0")"

# aideal package lives in grail-agent/src
export PYTHONPATH="$(cd ../../grail-agent/src && pwd):${PYTHONPATH:-}"

MODE="--dry-run"
EXTRA=()
for a in "$@"; do
  case "$a" in
    --execute) MODE="--execute" ;;
    *) EXTRA+=("$a") ;;
  esac
done

# --- cases: "id|kind|payload" -------------------------------------------------
TEXT_CASES=(
  "1.1 zonal-mean-min-max|Using a raptor join between the raster and the Boston neighborhood polygons, compute the mean, minimum, and maximum pixel value for each neighborhood. Write one row per neighborhood (name, mean, min, max, pixel_count) to CSV in the output directory."
  "1.2 hottest-neighborhood|For each Boston neighborhood polygon, count how many raster pixels fall inside it and compute the average value, then report the single neighborhood with the highest average value."
  "1.3 zonal-sum|Compute the sum of all raster pixel values that fall within each neighborhood polygon and save neighborhood name and total to CSV."
  "2.1 kelvin-to-celsius|Convert every raster pixel from Kelvin to Celsius by subtracting 273.15, and write the converted raster as a GeoTIFF to the output directory."
  "2.2 reproject-raster|Reproject the raster to EPSG:4326 and save it as a GeoTIFF in the output directory."
  "2.3 threshold-mask|Keep only raster pixels whose value is greater than 300, set all other pixels to nodata, and write the masked raster as a GeoTIFF."
  "2.4 raster-to-points|Convert every non-empty raster pixel into a point feature carrying its value as an attribute, and save the points as GeoJSON."
  "3.1 area-rank|Compute the area of each Boston neighborhood polygon and write neighborhood name and area to CSV, sorted by area descending."
  "3.2 range-query|Return only the neighborhood polygons that intersect the bounding box minx=-71.10, miny=42.30, maxx=-71.05, maxy=42.35, and save the matches as GeoJSON."
  "3.3 reproject-polygons|Reproject the Boston neighborhood polygons to EPSG:3857 and save them as a shapefile in the output directory."
  "4.1 csv-attribute-join|Load the land-use summary CSV, join it to the neighborhood polygons on the neighborhood name (CSV column zone_name = polygon field name), attach each polygon's dominant land-use label as an attribute, and save the enriched polygons as GeoJSON."
)
PY_CASES=(
  "P1 threshold-mask|../../grail-agent/examples/python/raster_threshold_mask.py"
  "P2 area-rank|../../grail-agent/examples/python/polygon_area_rank.py"
  "P3 range-query|../../grail-agent/examples/python/bbox_clip.py"
  "P4 raster-to-points|../../grail-agent/examples/python/raster_to_points.py"
  "P5 csv-join|../../grail-agent/examples/python/csv_join_polygons.py"
  "P6 zonal-minmax|../../grail-agent/examples/python/zonal_stats_minmax.py"
)

pass=0; fail=0; results=()
run_case() {
  local id="$1"; shift
  local out; out="$(python3 demo_agent.py "$MODE" "${EXTRA[@]}" "$@" 2>&1)"
  if grep -q "status=RUNNABLE" <<<"$out"; then
    results+=("PASS  $id"); pass=$((pass+1))
  else
    results+=("FAIL  $id"); fail=$((fail+1))
  fi
}

echo "=== GRAIL demo suite ($MODE) ==="
for c in "${TEXT_CASES[@]}"; do
  id="${c%%|*}"; payload="${c#*|}"
  echo "--- text  $id"
  run_case "$id" --text "$payload"
done
for c in "${PY_CASES[@]}"; do
  id="${c%%|*}"; payload="${c#*|}"
  echo "--- py    $id"
  run_case "$id" --python "$payload"
done

echo
echo "================ SUMMARY ($MODE) ================"
printf '%s\n' "${results[@]}"
echo "------------------------------------------------"
echo "PASS=$pass  FAIL=$fail  TOTAL=$((pass+fail))"
[ "$fail" -eq 0 ]
