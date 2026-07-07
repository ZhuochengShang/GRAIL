#!/bin/bash
# restart_clean.sh — clean pipeline restart in the canonical order:
#   0. ARCHIVE prior evidence (error log, old catalog, old results) — never delete
#   1. reset error log + all run scratch (fresh memory: no known_failures replay)
#   2. remove-redundant surface artifacts (static: intent 205 -> dedup 203)
#   3. regenerate LLM_readme from the DEDUPED surface   (author model, OPENAI_API_KEY)
#   4. full comprehension on the deduped catalog        (audience model, default Gemini)
#   5. fix failures, max 15 rounds + stuck detector
#
# Usage:
#   export OPENAI_API_KEY=...  GOOGLE_API_KEY=...
#   caffeinate -i ./restart_clean.sh 2>&1 | tee restart_$(date +%H%M).log
#   AUDIENCE=openai:gpt-4o ./restart_clean.sh      # different audience model
set -euo pipefail
cd "$(dirname "$0")"
: "${OPENAI_API_KEY:?need OPENAI_API_KEY (author model for readme regen)}"
AUD="${AUDIENCE:-google:gemini-2.5-pro}"
case "$AUD" in google:*) : "${GOOGLE_API_KEY:?need GOOGLE_API_KEY for $AUD}";; esac
STAMP=$(date +%Y%m%d_%H%M%S)

echo "== 0. archive prior evidence -> archive/$STAMP/"
mkdir -p "archive/$STAMP"
for f in logs/error_log.jsonl docs/LLM_readme.md docs/comprehension_run.json \
         docs/intent_common.json .aideal_exec/comprehension_progress.jsonl; do
  [ -f "$f" ] && cp "$f" "archive/$STAMP/$(basename "$f")" || true
done
wc -c docs/LLM_readme.md | tee "archive/$STAMP/readme_size_before.txt" || true

echo "== 1. reset error log + run scratch"
: > logs/error_log.jsonl
rm -rf .aideal_exec exec_out/* docs/preamble.scala docs/io_hints.txt 2>/dev/null || true

echo "== 2. remove-redundant surface (static; expect 820 raw -> 205 -> 203 entries)"
aideal intent --all > docs/intent_all_nollm.json
python3 -c "import json;d=json.load(open('docs/intent_all_nollm.json'));print('  intent:',d['raw_surface'],'->',d['selected'])"
aideal dedup --out docs/dedup_report.json > /dev/null
python3 -c "import json;d=json.load(open('docs/dedup_report.json'));print('  dedup: catalog entries after aliasing:',d['catalog_entries_after_aliasing'],'| subsumed telescoping sites:',d['subsumed_overload_sites'])"
aideal scaffold --generate > /dev/null && echo "  scaffold regenerated (incl. raptor Java-type imports)"

echo "== 3. regenerate LLM_readme from the deduped surface (author model)"
aideal readme --generate --force --limit 0    # 0 = ALL entries (default is 10!)
echo -n "  catalog size: " && wc -c < docs/LLM_readme.md
ENTRIES=$(grep -c "^## API Test:" docs/LLM_readme.md)
echo "  entries: $ENTRIES"
if [ "$ENTRIES" -lt 150 ]; then
  echo "ABORT: catalog has only $ENTRIES entries (expected ~203) — refusing to burn the night on a partial catalog." >&2
  exit 1
fi

echo "== 4. full comprehension on the deduped catalog (audience=$AUD)"
aideal comprehension --execute --timeout 300 --role "audience=$AUD" \
  > docs/comprehension_run.json
python3 -c "
import json; d=json.load(open('docs/comprehension_run.json'))
m=list(d['metrics'].values()); p=sum(1 for r in m if r['status']=='pass')
print(f'  comprehension: {p}/{len(m)} pass ({p/len(m):.1%}) | wall {d[\"run\"][\"wall_s\"]/60:.0f} min')"

echo "== 5. fix failures (max 15 rounds, stuck detector on)"
aideal comprehension --execute --timeout 300 --role "audience=$AUD" \
  --rerun-failed --max-fix-rounds 15 > docs/comprehension_fixall.json
python3 -c "
import json; d=json.load(open('docs/comprehension_fixall.json'))
m=list(d['metrics'].values()); p=[r for r in m if r['status']=='pass']
att=[r['attempts'] for r in p]
print(f'  fix-all: {len(p)}/{len(m)} fixed | rounds-to-fix mean {sum(att)/len(att):.1f}' if p else f'  fix-all: 0/{len(m)} fixed')
print(f'  tokens in={sum(r[\"input_tokens\"] for r in m):,} out={sum(r[\"output_tokens\"] for r in m):,}')"

echo "== DONE. Artifacts: docs/comprehension_run.json (step 4), docs/comprehension_fixall.json (step 5),"
echo "   docs/dedup_report.json, archive/$STAMP/ (pre-restart evidence)."
