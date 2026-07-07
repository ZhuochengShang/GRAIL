# Codex 5.3 Fresh README Experiment

Branch: `exp/run-codex-fresh-5.3`
Worktree: `GRAIL_exp_runner`

## State

Codex 5.3 generated a fresh full README:

- `docs/LLM_readme.md` — active README for this run
- `docs/LLM_readme.codex_fresh.md` — frozen copy of the Codex-generated README
- `docs/readme_generate_codex_fresh.json` — generation report

Checks at setup:

```text
API entries: 205
Docfix markers: 0
Generated ok: 205
Fallback skeletons: 0
```

The active error log and comprehension checkpoint were cleared before g1/g4:

- `logs/error_log.jsonl`
- `.aideal_exec/comprehension_progress.jsonl`

## Next Commands

Run from `experiments/rdpro/`.

### 1. Codex g1: flat entire README

```bash
export BENCH_CODEX_MODEL=gpt-5.3-codex

caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g1
```

Expected output:

`results/bench/<timestamp>_g1_codex_flat.gpt-5.3-codex.json`

### 2. Codex g4: fix the g1 failures

Run only after g1 finishes. g4 uses `--rerun-failed`, so it should see only the Codex g1 failures from the cleared log.

```bash
export BENCH_G4_ROUNDS=15

caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g4
```

Expected output:

`results/bench/<timestamp>_g4_codex_fixall.gpt-5.3-codex.json`

### 3. Aggregate

```bash
/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  bench_conditions.py --table \
  > docs/backend_comparison_table_after_codex_5_3.txt
```

## Files To Compare

Codex fresh README:

- `docs/LLM_readme.codex_fresh.md`
- `docs/readme_generate_codex_fresh.json`

Codex performance:

- `results/bench/*g1_codex_flat.gpt-5.3-codex.json`
- `results/bench/*g4_codex_fixall.gpt-5.3-codex.json`
- `docs/backend_comparison_table_after_codex_5_3.txt`
- `logs/error_log.jsonl`

Baseline references:

- `docs/gemini_fix_comparison.md`
- `results/bench/20260706_173509_g1_gemini_flat.json`
- `docs/comprehension_run.json`
- `docs/comprehension_fixall.json`

## Interpretation

This is not the same as the same-README backend comparison. This condition tests:

```text
Codex as README author + Codex as code-generating audience/fixer
```

The same-README comparison tests only the coding backend. Keep these two result families separate.
