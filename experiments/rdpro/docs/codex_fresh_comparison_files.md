# Codex Fresh README Comparison Files

This file tracks the clean Codex condition:

1. keep the current Gemini doc-fixed README,
2. regenerate `docs/LLM_readme.md` from scratch using Codex as the author,
3. run Codex g1 comprehension,
4. run Codex g4 fix-all on the Codex g1 failures,
5. compare against the archived Gemini-fixed README and earlier Gemini results.

## Preserved Gemini-fixed state

Archive directory:

`docs/codex_fresh_archives/20260707_115728/`

Files:

- `LLM_readme.gemini_docfix.md` — current Gemini-fixed README before Codex regeneration.
- `docfix_run.gemini.json` — Gemini source-aware doc-fix report.
- `error_log.before_codex.jsonl` — full pre-Codex error log.

The active files were reset for a clean Codex condition:

- `logs/error_log.jsonl` — truncated to 0 lines.
- `.aideal_exec/comprehension_progress.jsonl` — removed.

## Run Codex Fresh README

Run from `experiments/rdpro/`:

```bash
export BENCH_CODEX_MODEL=gpt-5.3-codex

caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/aideal \
  readme --generate --limit 0 --force \
  --role author=codex:$BENCH_CODEX_MODEL \
  > docs/readme_generate_codex_fresh.json

cp docs/LLM_readme.md docs/LLM_readme.codex_fresh.md
wc -c docs/LLM_readme.codex_fresh.md \
  docs/codex_fresh_archives/20260707_115728/LLM_readme.gemini_docfix.md
```

## Run Codex g1

```bash
caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g1
```

The result is written to:

`results/bench/<timestamp>_g1_codex_flat.gpt-5.3-codex.json`

## Run Codex g4

Run g4 only after g1 finishes. It uses the clean `logs/error_log.jsonl` from the Codex g1 run.

```bash
export BENCH_G4_ROUNDS=15

caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g4
```

The result is written to:

`results/bench/<timestamp>_g4_codex_fixall.gpt-5.3-codex.json`

For the literal long fix-all condition:

```bash
export BENCH_G4_ROUNDS=99
```

## Aggregate Table

```bash
/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  bench_conditions.py --table \
  > docs/backend_comparison_table_after_codex.txt
```

## Files To Check For Comparison

### README comparison

- `docs/codex_fresh_archives/20260707_115728/LLM_readme.gemini_docfix.md`
- `docs/LLM_readme.codex_fresh.md`
- `docs/readme_generate_codex_fresh.json`

Suggested checks:

```bash
diff -u docs/codex_fresh_archives/20260707_115728/LLM_readme.gemini_docfix.md \
  docs/LLM_readme.codex_fresh.md \
  > docs/diff_gemini_docfix_vs_codex_fresh_readme.patch

grep -c '^## API Test:' docs/LLM_readme.codex_fresh.md
grep -c 'doc-repaired from source' docs/LLM_readme.codex_fresh.md
wc -c docs/codex_fresh_archives/20260707_115728/LLM_readme.gemini_docfix.md \
  docs/LLM_readme.codex_fresh.md
```

### Performance comparison

- `results/bench/20260706_173509_g1_gemini_flat.json`
- `results/bench/<timestamp>_g1_codex_flat.gpt-5.3-codex.json`
- `results/bench/<timestamp>_g4_codex_fixall.gpt-5.3-codex.json`
- `docs/backend_comparison_table_after_codex.txt`

Optional earlier local outputs:

- `docs/comprehension_run.json`
- `docs/comprehension_fixall.json`
- `docs/docfix_run.json`
- `docs/gemini_fix_comparison.md`

### Error/failure analysis

- `logs/error_log.jsonl` — clean Codex g1/g4 failure log after the run.
- `docs/codex_fresh_archives/20260707_115728/error_log.before_codex.jsonl` — previous Gemini/older mixed log.
- `docs/still_failing_reverted_errors.md` — previous docfix reverted-error summary.

## Why Same README vs Fresh README Are Different Experiments

Using the same README for `openai`, `codex`, and `gemini` isolates the coding model: each backend receives identical documentation and the measured difference is mostly model behavior.

Regenerating the README with Codex changes the condition. It tests the full pipeline with Codex as the documentation author plus Codex as the coding audience/fixer. That is useful, but it should be reported separately from the same-README model comparison.

