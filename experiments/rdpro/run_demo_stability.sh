#!/usr/bin/env bash
# VLDB demo stability protocol (TODO.md workstream 6):
# run every demo case N times, mark each case STABLE / FLAKY / BROKEN, and
# freeze the STABLE set as the live-demo script.
#
# Usage:
#   ./run_demo_stability.sh                     # N=5, --execute, all cases
#   ./run_demo_stability.sh -n 3 --dry-run      # quick offline shakeout
#   ./run_demo_stability.sh 1.1 2.3             # only these case ids
#
# Output: results/demo_stability_<stamp>.md (+ .json) — per-case pass counts,
# verdicts, and the failing output tails under results/demo_stability_logs/.
# Exit code 0 only when every selected case is STABLE (CI-able).
set -uo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$(cd ../../grail-agent/src && pwd):${PYTHONPATH:-}"
source ./demo_cases.sh

N=5
MODE="--execute"
ONLY=()
while [ $# -gt 0 ]; do
  case "$1" in
    -n) N="$2"; shift 2 ;;
    --dry-run) MODE="--dry-run"; shift ;;
    --execute) MODE="--execute"; shift ;;
    *) ONLY+=("$1"); shift ;;
  esac
done

STAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p results/demo_stability_logs
MD="results/demo_stability_${STAMP}.md"
JSON="results/demo_stability_${STAMP}.json"

selected() {  # case id in the ONLY filter (empty filter = everything)
  [ ${#ONLY[@]} -eq 0 ] && return 0
  local id="$1"
  for o in "${ONLY[@]}"; do [[ "$id" == "$o"* ]] && return 0; done
  return 1
}

declare -a ROWS_MD ROWS_JSON
total_cases=0; stable=0; flaky=0; broken=0

run_matrix() {           # $1=kind(text|python) $2=id $3=payload
  local kind="$1" id="$2" payload="$3" pass=0
  for k in $(seq 1 "$N"); do
    local log="results/demo_stability_logs/$(echo "$id" | tr ' /' '__')_run${k}.log"
    if [ "$kind" = "text" ]; then
      out="$(python3 demo_agent.py "$MODE" --text "$payload" 2>&1)"
    else
      out="$(python3 demo_agent.py "$MODE" --python "$payload" 2>&1)"
    fi
    if grep -q "status=RUNNABLE" <<<"$out"; then
      pass=$((pass+1))
      echo "  $id run $k/$N: PASS"
    else
      printf '%s\n' "$out" | tail -60 > "$log"
      echo "  $id run $k/$N: FAIL  (tail -> $log)"
    fi
  done
  local verdict
  if   [ "$pass" -eq "$N" ]; then verdict="STABLE"; stable=$((stable+1))
  elif [ "$pass" -eq 0 ];   then verdict="BROKEN"; broken=$((broken+1))
  else                            verdict="FLAKY";  flaky=$((flaky+1)); fi
  total_cases=$((total_cases+1))
  ROWS_MD+=("| $id | $pass/$N | **$verdict** |")
  ROWS_JSON+=("{\"id\": \"$id\", \"pass\": $pass, \"n\": $N, \"verdict\": \"$verdict\"}")
}

echo "=== demo stability: N=$N per case, mode=$MODE ==="
for c in "${TEXT_CASES[@]}"; do
  id="${c%%|*}"; payload="${c#*|}"
  selected "$id" || continue
  echo "--- text  $id"
  run_matrix text "$id" "$payload"
done
for c in "${PY_CASES[@]}"; do
  id="${c%%|*}"; payload="${c#*|}"
  selected "$id" || continue
  echo "--- py    $id"
  run_matrix python "$id" "$payload"
done

{
  echo "# Demo stability — ${STAMP} (N=${N}, ${MODE})"
  echo
  echo "STABLE = ${N}/${N} pass (live-demo safe) · FLAKY = intermittent (pre-bake"
  echo "a cached output, demo only with fallback) · BROKEN = 0/${N} (fix or cut)."
  echo
  echo "| case | pass | verdict |"
  echo "|---|---|---|"
  printf '%s\n' "${ROWS_MD[@]}"
  echo
  echo "totals: ${stable} stable · ${flaky} flaky · ${broken} broken of ${total_cases}"
  echo
  echo "Failing output tails: results/demo_stability_logs/"
} > "$MD"
printf '{"stamp": "%s", "n": %s, "mode": "%s", "cases": [%s]}\n' \
  "$STAMP" "$N" "$MODE" "$(IFS=,; echo "${ROWS_JSON[*]}")" > "$JSON"

echo
cat "$MD"
[ $((flaky+broken)) -eq 0 ]
