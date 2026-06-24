#!/usr/bin/env bash
# Compile + spark-submit the smoke test (the proven path; not spark-shell -i).
# Run from experiments/rdpro:  bash docs/run_smoke.sh
set -euo pipefail

REPO=https://repo.osgeo.org/repository/geotools-releases/,https://repo.osgeo.org/repository/release/
PKGS=org.locationtech.jts:jts-core:1.19.0,org.geotools:gt-referencing:26.1,org.geotools:gt-epsg-hsql:26.1,org.geotools:gt-geotiff:26.1,org.geotools:gt-coverage:26.1,it.geosolutions.imageio-ext:imageio-ext-tiff:1.4.14

LIB=beast/target/beast-0.10.1-bin/beast-0.10.1/lib
[ -d "$LIB" ] || { echo "ERROR: beast lib not found: $LIB (build beast or fix the path)"; exit 1; }

# Spark jars come from the pyspark install (needed on the COMPILE classpath)
SPARK_JARS_DIR="$(python -c 'import pyspark,os; print(os.path.join(os.path.dirname(pyspark.__file__),"jars"))')"

WORK=.aideal_exec
mkdir -p "$WORK/classes"

# scalac classpath: COLON-separated, must include Spark + beast jars
COMPILE_CP="$(ls "$LIB"/*.jar "$SPARK_JARS_DIR"/*.jar | paste -sd: -)"
# spark-submit --jars: COMMA-separated beast jars (Spark is already on its classpath)
SUBMIT_JARS="$(ls "$LIB"/*.jar | paste -sd, -)"

echo ">> compiling (scalac, colon classpath)..."
scalac -classpath "$COMPILE_CP" -d "$WORK/classes" docs/smoke_test.scala

echo ">> packaging..."
( cd "$WORK/classes" && jar cf ../app.jar . )

echo ">> submitting..."
spark-submit --master "local[*]" --class GeoJobMain \
  --repositories "$REPO" --packages "$PKGS" \
  --jars "$SUBMIT_JARS" "$WORK/app.jar"
