# Codex 5.3 vs Gemini README Comparison

Comparison date: 2026-07-07

## Files

- Codex fresh README: `docs/LLM_readme.codex_fresh.md`
- Gemini reference README: `docs/LLM_readme.baseline_docfix_20260708.md`

Note: the Gemini reference is the best same-surface snapshot available in this worktree. It has one early docfix marker, so treat it as Gemini-generated plus one accepted repair, not a perfectly pristine Gemini-only artifact.

## Quantitative Summary

| Metric | Codex 5.3 fresh | Gemini reference | Difference |
|---|---:|---:|---:|
| API entries | 205 | 205 | 0 |
| Missing API names | 0 | 0 | same surface |
| Characters | 675,824 | 526,902 | Codex +148,922 (+28.3%) |
| Median entry length | 3,219 chars | 2,499 chars | Codex +720 |
| Code blocks | 879 | 820 | Codex +59 |
| Bullet items | 2,696 | 1,145 | Codex +1,551 |
| Docfix markers | 0 | 1 | Codex is fresh/no docfix |
| Mean full-entry text similarity | 0.296 | n/a | low, large rewrites |
| Median full-entry text similarity | 0.296 | n/a | low, large rewrites |
| Mean valid-call-pattern similarity | 0.571 | n/a | moderate |
| Median valid-call-pattern similarity | 0.544 | n/a | moderate |

## Main Difference

Codex did not just paraphrase Gemini. It regenerated almost every entry in a more instruction-heavy style:

- More receiver-qualified instructions, e.g. telling the LLM to call `accumulator.add(f)` instead of bare `add(f)`.
- More negative guidance, e.g. "do not expect a return value", "do not call without receiver", "trigger a Spark action".
- More stepwise bullets inside `LLM Instruction Prompt` and `Common Failure Modes`.
- Slightly more executable-looking snippets, but this needs g1/g4 to prove whether they actually compile/pass.

Gemini is shorter and often more descriptive. It tends to explain what the API means, while Codex more often explains how an LLM should call it.

## Same Structure

Both files keep the same top-level schema:

- `Signature`
- `Goal`
- `Parameters`
- `Input`
- `Output`
- `Valid Call Patterns`
- `LLM Instruction Prompt`
- `Prompt Snippet`
- `Common Failure Modes`
- `Fix Code Hint`

The API surface is identical: 205 common API names, no Codex-only names, no Gemini-only names.

## Largest Codex Expansions

| API | Codex chars | Gemini chars | Delta |
|---|---:|---:|---:|
| `run` | 5,385 | 2,836 | +2,549 |
| `createPartitioner` | 5,940 | 3,921 | +2,019 |
| `getFeatureReaderClass` | 4,040 | 2,165 | +1,875 |
| `using` | 3,941 | 2,122 | +1,819 |
| `partitionBy` | 4,412 | 2,603 | +1,809 |
| `sridToCRS` | 4,282 | 2,543 | +1,739 |
| `rangeQuery` | 4,927 | 3,307 | +1,620 |
| `createPartitions` | 4,115 | 2,499 | +1,616 |
| `visualize` | 3,353 | 1,742 | +1,611 |
| `partitionFeatures` | 4,588 | 3,082 | +1,506 |

## APIs Where Codex Is Shorter

| API | Codex chars | Gemini chars | Delta |
|---|---:|---:|---:|
| `compress` | 2,456 | 2,936 | -480 |
| `plotImage` | 3,917 | 4,089 | -172 |
| `saveAsCSVPoints` | 3,537 | 3,708 | -171 |
| `zonalStatsLocal` | 3,935 | 4,045 | -110 |
| `buildIndex` | 2,879 | 2,933 | -54 |
| `eulerHistogramSize` | 3,049 | 3,067 | -18 |

## Interpretation For Experiments

This comparison says Codex produces a denser, more operational README, but not necessarily a more correct one. The correct test is the active g1/g4 run:

- If Codex g1 improves over Gemini g1, the extra operational detail helped initial comprehension.
- If Codex g1 is similar but g4 improves, Codex may be better as fixer than as README author.
- If Codex remains near Gemini, the blocker is probably not prose style alone; it is missing structured codebase facts such as receiver type, imports, fixture variables, known passing sibling, and forbidden call patterns.

The next comparison table should use:

- `results/bench/*g1_codex_flat.gpt-5.3-codex.json`
- `results/bench/*g4_codex_fixall.gpt-5.3-codex.json`
- `docs/backend_comparison_table_after_codex_5_3.txt`
- `logs/error_log.jsonl`

