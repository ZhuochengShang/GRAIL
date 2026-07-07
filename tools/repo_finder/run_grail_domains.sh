#!/bin/bash
# run_grail_domains.sh — find GRAIL external-target candidates OUTSIDE geospatial.
#
# GRAIL already covers geospatial (RDPro/beast, Sedona); the generalization
# repos must come from OTHER domains. Runs the finder once per domain query,
# with rubric R1–R7 filters (paper/repo_selection.md) and a geo-exclusion
# regex applied to name/description/topics.
#
# Usage:
#   export GITHUB_TOKEN=ghp_xxx        # never hardcode tokens in this file
#   ./run_grail_domains.sh             # Python + Scala + Java, all domains
#   LANGS="Scala" ./run_grail_domains.sh

set -u
: "${GITHUB_TOKEN:?export GITHUB_TOKEN first (do NOT hardcode it here)}"

SCRIPT="$(dirname "$0")/sedona_shape_repo_finder.py"
OUT="$(dirname "$0")/results_grail"
mkdir -p "$OUT"

# languages ordered by harness cost: Scala (adapter exists) > Python (needs
# the 2 signal fixes) > Java (visibility model exists, execution adapter new)
LANGS="${LANGS:-Scala Python Java}"

# non-geospatial domains where API complexity is high and LLM headroom likely
DOMAINS=(
  "bioinformatics"
  "genomics"
  "cheminformatics"
  "materials science"
  "molecular dynamics"
  "quantum computing"
  "signal processing"
  "control systems"
  "time series"
  "econometrics"
  "medical imaging"
  "units physical quantities"
  "constraint solver optimization"
  "stream processing"
)

# drop anything geospatial-shaped no matter which query surfaced it
EXCLUDE='geo|spatial|gis|raster|map|cartog|osm|satellite|earth observation'

for LANG in $LANGS; do
  for D in "${DOMAINS[@]}"; do
    TAG="$(echo "${LANG}_${D}" | tr ' ' '-')"
    echo "=== $LANG / $D ==="
    python3 "$SCRIPT" \
      --language "$LANG" \
      --query-extra "$D" \
      --min-stars 100 --max-stars 5000 --min-forks 10 \
      --pushed-after 2025-07-01 --src-months 6 \
      --min-api 50 --top 10 --pages 1 --per-page 20 \
      --exclude-regex "$EXCLUDE" \
      --csv "$OUT/${TAG}.csv" --json "$OUT/${TAG}.json"
    sleep 30   # be kind to the search rate limit
  done
done

echo "done — merge/rank: python3 - <<'EOF'
import json, glob
rows = {}
for f in glob.glob('$OUT/*.json'):
    for r in json.load(open(f)):
        rows[r['full_name']] = r
top = sorted(rows.values(), key=lambda r: -r.get('final_score', 0))[:40]
for r in top:
    print(f\"{r.get('final_score',0):6.1f}  {r['full_name']:45s} {r.get('stars','?'):>6}★  {(r.get('description') or '')[:70]}\")
EOF"
