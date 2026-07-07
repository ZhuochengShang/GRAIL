# Gemini Fix Comparison

Generated from local artifacts after the Gemini doc-fix run.

## Available result files

| Artifact | Meaning |
|---|---|
| `results/bench/20260706_173509_g1_gemini_flat.json` | g1: Gemini flat-catalog comprehension run |
| `docs/comprehension_run.json` | post-dedup comprehension run over 205 intended APIs |
| `docs/comprehension_fixall.json` | fix-all rerun over the failed subset, not a full all-API denominator |
| `docs/docfix_run.json` | Gemini source-aware doc-repair run; rewrites entries, accepts only if retry passes |
| `docs/LLM_readme.baseline_docfix_20260708.md` | baseline README before the accepted doc-fix batch, except `compress` was already repaired |
| `docs/LLM_readme.md` | current README after accepted doc repairs |

## Comprehension / fix comparison

| Condition | Executed | Scored | Pass | Score | Infra excluded | Mean attempts | Mean attempts among passes | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| g1 Gemini flat catalog | 218 | 207 | 90 | 43.5% | 11 | 2.83 | 1.49 | `--role audience=google:gemini-2.5-pro --max-fix-rounds 3` |
| post-dedup comprehension | 205 | 196 | 77 | 39.3% | 9 | 2.95 | 1.44 | full 205 intended API set |
| fix-all on failures | 128 | 119 | 7 | 5.9% | 9 | 5.08 | 3.57 | failed-subset run only; do not compare as full pass rate |

`docs/comprehension_fixall.json` is not a full-condition pass rate. It only reran the failed subset, so the useful number is the marginal recovery: 7 previously-failing APIs were recovered out of 119 scored failed-subset APIs.

## Gemini doc-fix result

`docs/docfix_run.json`:

| Metric | Value |
|---|---:|
| attempted | 117 |
| accepted doc fixes | 10 |
| fix rate | 8.5% |
| not testable | 11 |
| rewrite rejected | 35 |
| still failing / reverted | 61 |

Accepted doc fixes:

`addTile`, `area`, `findIntersections`, `isCW`, `isDefined`, `numFields`, `retainIndex`, `saveAsKML`, `sierpinski`, `trimLineSegment`.

The current README also contains earlier accepted repairs for:

`compress`, `computeForFeatures`, `config`, `createPartitions`, `createRingsForOccupiedPixels`.

Total current repaired markers: 15.

## README delta

| File | Chars | API entries | Repaired markers |
|---|---:|---:|---:|
| baseline docfix snapshot | 526,902 | 205 | 1 |
| current README | 530,445 | 205 | 15 |

Entry-level changed APIs: 14.

`addTile`, `area`, `computeForFeatures`, `config`, `createPartitions`, `createRingsForOccupiedPixels`, `findIntersections`, `isCW`, `isDefined`, `numFields`, `retainIndex`, `saveAsKML`, `sierpinski`, `trimLineSegment`.

Structural change pattern:

- The original generated entries used a uniform section layout: `Signature`, `Goal`, `Parameters`, `Input`, `Output`, `Valid Call Patterns`, `LLM Instruction Prompt`, `Prompt Snippet`, `Common Failure Modes`, `Fix Code Hint`.
- Repaired entries remove most static template sections and replace them with source-grounded usage instructions: `Goal`, `Valid Call Patterns|Valid Access Patterns`, `LLM Instruction Prompt`, `Prompt Snippet`, `Common Failure Modes`, `Fix Code Hint`.
- Repaired entries add `_Grounding: doc-repaired from source (docfix)._`.
- The current README is 3,543 characters longer than the baseline snapshot.
- 139 diff blocks changed, roughly 13 inserted lines, 30 deleted lines, and 580 replaced-line span.

## Missing fair comparison

There is not yet a saved result for "g4 after rewritten README". To compare it fairly against g1 and the original fix-all run, run a new comprehension/fix-all condition on the current `docs/LLM_readme.md` and save it separately.

Suggested command from `experiments/rdpro/`:

```bash
caffeinate -i aideal comprehension --execute --timeout 300 --rerun-failed \
  --role audience=google:gemini-2.5-pro \
  --role fixer=google:gemini-2.5-pro \
  --max-fix-rounds 99 \
  > docs/comprehension_fixall_after_docfix.json
```

Then compare:

- `results/bench/20260706_173509_g1_gemini_flat.json`
- `docs/comprehension_fixall.json`
- `docs/comprehension_fixall_after_docfix.json`

