# Comprehension baseline — 2026-07-06 (pre-regen, OLD catalog)

Raw JSON: `docs/comprehension_run.pre_regen.json` (run_id in `run.run_id`).
Condition: OLD LLM_readme (218 entries, generated 2026-07-01 from the
pre-dedup surface) + fixed harness. audience=fixer=openai:gpt-4o,
max_fix_rounds=3, timeout=300s, class_context=off.

## Headline

| metric | value |
|---|---|
| APIs executed | 218 (intended surface is now 205; 13 old-catalog extras) |
| pass | **60/218 = 27.5%** (score 0.287 excl. 9 infra) |
| pass @ round 0 | 57 |
| rescued by fix loop | **3** (of 158 initial failures → 1.9% rescue rate) |
| burned all 4 attempts | 150 APIs |
| failures | compile 129 · runtime 19 · infra 9 · no-correctness-check 1 |
| wall | 54.0 min, 0 timeouts (max single API 122.8s) |
| tokens | 1,459,315 in / 117,293 out (674 calls; ≈$5 at gpt-4o rates) |

## What the numbers say

1. **The fix loop with a same-model fixer is nearly worthless: 3/158
   rescued.** The model repeats its own mistake across rounds (e.g. `add`
   re-invented `accumulator.getSummary` 4×). This is the headroom the
   `gemini_maxfix` (different-model fixer) and `class_context=on` conditions
   are designed to attack.
2. **Compile errors dominate (129/158)** — wrong receiver/entry-point or
   invented members, the failure class the index-first catalogue targets.
3. **Demo-critical status (VLDB item 6):** pass — raptorJoin,
   raptorJoinFeature, geoTiff, shapefile, overlay, filterPixels, mapPixels
   (all @round0). FAIL — zonalStatsLocal (snippet called
   `String.getFileSystem`), spatialJoin (tried `new RDD(...)`),
   reshapeNN (invented `pixelWidth` param name), retile (runtime,
   unrecognized-format on fixture), saveAsGeoTiff (**environment, not doc**:
   `exec_out/output.tif/temp/0 not empty` — stale leftovers from the crashed
   07-01 run; clean `exec_out/` before runs).
4. Old-catalog run = the BEFORE arm. Next: `aideal readme --generate --force`
   (deduped 205 surface) → rerun comprehension → diff pass rate + tokens.

## Count funnel (2026-07-06) + run-to-run variance

| step | count | source |
|---|---|---|
| raw public def sites | 1,599 | `aideal api-surface` |
| raw public names | 820 | same (`this` excluded) |
| intent-selected (static, thr 5) | 205 | `aideal intent` |
| … LLM arm (stale, pre-cache-fix) | 274 | `intent_all_llm.json` — re-judges on next keyed run |
| selected def sites → canonical | 418 → 205 | `aideal dedup` (19 telescoping-subsumed) |
| catalog entries after full-forwarder collapse | **203** | dedup report |
| catalog ON DISK (old, 2026-07-01) | 218 entries | `LLM_readme.md` — stale by 15 |
| class catalogue | 78 class files | `docs/api/` (63★ verified · 117 grounded · 27 sibling · 11 guessed) |
| comprehension executed | 218 | old catalog |

**The remembered "64": the 2026-07-01 full run passed 64/218**
(RDPro_Comprehension_Analysis.pptx: "64 of 218 APIs passed", "50 of 64 on
first try") — that run USED the old catalog; the catalog-vs-no-catalog
comparison hasn't run yet (`--doc original` is the no-catalog arm).
Today's same-catalog rerun: 60/218. → free repeat-run variance estimate:
**±4 APIs ≈ ±2pp** on the full 218 (evidence for the sample-size knob).
Open sub-question: fix-loop rescues fell 14 (07-01) → 3 (today); candidates:
timeout 600→300, model drift, known-failures window content (`failures_for`
caps at 4 items, so prompt bloat is bounded). Worth one controlled re-run.
