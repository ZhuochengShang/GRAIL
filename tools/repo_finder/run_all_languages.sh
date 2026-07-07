#!/bin/bash
# run_all_languages.sh
# Runs sedona_shape_repo_finder.py for each language sequentially.
# Waits 60s between runs to let the GitHub rate limit reset.
# All output is logged to run_all.log as well as printed to screen.
#
# Usage:
#   chmod +x run_all_languages.sh
#   ./run_all_languages.sh
#
# Or with a custom token/top:
#   TOKEN=YOUR_TOKEN_HERE TOP=30 ./run_all_languages.sh

TOKEN="${TOKEN:-YOUR_TOKEN_HERE}"
TOP="${TOP:-20}"
SCRIPT="sedona_shape_repo_finder.py"
LOG="run_all.log"
OUT_DIR="results"
WAIT=60   # seconds between language runs

LANGUAGES=("Python" "Java" "Go" "Rust" "C++" "JavaScript" "TypeScript" "Scala")

mkdir -p "$OUT_DIR"
echo "" > "$LOG"

echo "======================================"
echo "  Sedona-shape finder — all languages"
echo "  Top: $TOP per language"
echo "  Output dir: $OUT_DIR/"
echo "  Log: $LOG"
echo "  Wait between runs: ${WAIT}s"
echo "======================================"
echo ""

TOTAL=${#LANGUAGES[@]}

for i in "${!LANGUAGES[@]}"; do
    LANG="${LANGUAGES[$i]}"
    NUM=$((i + 1))

    # Safe filename: replace + and spaces
    SAFE=$(echo "$LANG" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g')
    CSV="$OUT_DIR/${SAFE}.csv"
    JSON="$OUT_DIR/${SAFE}.json"

    echo "--------------------------------------"
    echo "[$NUM/$TOTAL] Language: $LANG"
    echo "  CSV  → $CSV"
    echo "  JSON → $JSON"
    echo "  Started: $(date '+%H:%M:%S')"
    echo "--------------------------------------"

    python "$SCRIPT" \
        --token "$TOKEN" \
        --language "$LANG" \
        --top "$TOP" \
        --csv "$CSV" \
        --json "$JSON" \
        2>&1 | tee -a "$LOG"

    EXIT=${PIPESTATUS[0]}
    if [ $EXIT -ne 0 ]; then
        echo "⚠️  $LANG exited with code $EXIT — check $LOG"
    else
        echo "✅ $LANG done → $CSV"
    fi

    # Wait between runs (skip after last language)
    if [ $NUM -lt $TOTAL ]; then
        echo ""
        echo "⏳ Waiting ${WAIT}s before next language..."
        sleep $WAIT
        echo ""
    fi
done

echo ""
echo "======================================"
echo "  All done! $(date '+%H:%M:%S')"
echo "  Results in: $OUT_DIR/"
ls -lh "$OUT_DIR/"
echo "======================================"

# Merge all CSVs into one combined file
COMBINED="$OUT_DIR/all_languages.csv"
HEADER_WRITTEN=0
> "$COMBINED"

for f in "$OUT_DIR"/*.csv; do
    [ "$f" = "$COMBINED" ] && continue
    if [ $HEADER_WRITTEN -eq 0 ]; then
        cat "$f" >> "$COMBINED"
        HEADER_WRITTEN=1
    else
        tail -n +2 "$f" >> "$COMBINED"   # skip header row
    fi
done

echo ""
echo "📋 Combined CSV: $COMBINED"
LINES=$(wc -l < "$COMBINED")
echo "   $(( LINES - 1 )) total candidates across all languages"
