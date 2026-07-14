#!/bin/bash
# fixer_bench.sh — FIXER-model ablation on the doc-repair routing (fix-docs).
#
# Design: AUDIENCE is FIXED (default google:gemini-2.5-pro) so retry round-0
# snippets are written identically across arms; only the DIAGNOSE + REWRITE +
# fix-round model varies. Target set FROZEN to the codex-g1 failure list
# (matches the current codex-authored catalog), so every arm attacks the SAME
# failures. One arm per invocation of `aideal fix-docs`, sequential.
#
# Arms (models overridable via env; verify availability first:
#   gemini -> `python bench_check.py --list`;  ollama -> `ollama list`):
#   A cloud strong : google:${FIXER_A:-gemini-3.1-pro-preview-customtools}
#   B cloud cheap  : google:${FIXER_B:-gemini-3.5-flash}
#   C local strong : ollama:${FIXER_C:-qwen2.5-coder:32b}
#   D local small  : ollama:${FIXER_D:-qwen2.5-coder:7b}
#
# Usage:
#   export GOOGLE_API_KEY=...            # ollama arms need `ollama serve` running
#   ./fixer_bench.sh                     # all arms
#   ARMS="B D" ./fixer_bench.sh          # subset
#   AIDEAL_OLLAMA_NUM_CTX=16384 is the default context for local models.
set -euo pipefail
cd "$(dirname "$0")"
FROM="results/bench/20260707_125142_g1_codex_flat.gpt-5.3-codex.json"
AUD="${AUDIENCE:-google:gemini-2.5-pro}"
ARMS="${ARMS:-A B C D}"

declare -A FIXER=(
  [A]="google:${FIXER_A:-gemini-3.1-pro-preview-customtools}"
  [B]="google:${FIXER_B:-gemini-3.5-flash}"
  [C]="ollama:${FIXER_C:-qwen2.5-coder:32b}"
  [D]="ollama:${FIXER_D:-qwen2.5-coder:7b}"
)

for arm in $ARMS; do
  fx="${FIXER[$arm]}"
  tag=$(echo "$fx" | tr ':/' '--')
  echo "== fixer arm $arm: $fx  (audience=$AUD, targets frozen to codex-g1 fails)"
  caffeinate -i aideal fix-docs \
    --from-results "$FROM" \
    --timeout 300 --retry-rounds 5 \
    --role "audience=$AUD" --role "fixer=$fx" \
    --report "docs/docfix_fixerbench_${tag}.json" || echo "arm $arm stopped (see report)"
done

echo "== summary =="
python3 - <<'EOF'
import glob, json
for f in sorted(glob.glob("docs/docfix_fixerbench_*.json")):
    d = json.load(open(f))
    print(f"{f.split('/')[-1]:55s} model={d.get('model','?'):40s} "
          f"fixed={d.get('doc_fixed')}/{d.get('processed', d.get('attempted'))} "
          f"outcomes={d.get('outcomes')}")
EOF
