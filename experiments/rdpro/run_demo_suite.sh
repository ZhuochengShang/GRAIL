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

# --- cases live in demo_cases.sh (shared with run_demo_stability.sh) ---
source ./demo_cases.sh

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
