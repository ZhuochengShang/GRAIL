# Fix-loop report — aideal_run_pgcqa5is

_Generated 2026-09-07 01:39 by `aideal fix-report`._

- kind: **comprehension**  ·  run_id: `20260907-083814Z`  ·  models: audience=google:gemini-3.1-pro-preview, fixer=google:gemini-3.1-pro-preview
- pass **135/148** raw (91.2%)  ·  scored **135/148** (91.2%) after excluding 0 infra
- wall 0.02 h  ·  tokens in 2,696 / out 6,918 ·  llm calls 1  ·  max_fix_rounds 0
- pass-by-round: r0:135  ·  **0 rescued by the fix loop** (pass@0 = 135)

## Failure clusters (one issue, many APIs)

_Current failures grouped by normalized error signature (identifiers masked). Fixing the top cluster's root cause pays across all its APIs._

- **13x** [runtime] resumed: fail
  - `deprecated`, `first_n_three_layer_P`, `load_key`, `load_patterns`, `load_ragged_time_series`, `load_tempo`, `load_valued_intervals`, `load_wav`, `p_score`, `piano_roll`, `reduce_extended_quality`, `ticker_pitch`, `voicing_recall`

## Why each API fails (13 failing)

### `deprecated` — runtime

- canonical source: `source/mir_eval/util.py:946`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `first_n_three_layer_P` — runtime

- canonical source: `source/mir_eval/pattern.py:509`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_key` — runtime

- canonical source: `source/mir_eval/io.py:497`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_patterns` — runtime

- canonical source: `source/mir_eval/io.py:331` · reached: `source/mir_eval/io.py:380`, `source/mir_eval/io.py:26`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_ragged_time_series` — runtime

- canonical source: `source/mir_eval/io.py:594` · reached: `source/mir_eval/io.py:669`, `source/mir_eval/io.py:671`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_tempo` — runtime

- canonical source: `source/mir_eval/io.py:542`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_valued_intervals` — runtime

- canonical source: `source/mir_eval/io.py:448`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_wav` — runtime

- canonical source: `source/mir_eval/io.py:409`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `p_score` — runtime

- canonical source: `source/mir_eval/beat.py:329`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `piano_roll` — runtime

- canonical source: `source/mir_eval/display.py:873`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `reduce_extended_quality` — runtime

- canonical source: `source/mir_eval/chord.py:319`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `ticker_pitch` — runtime

- canonical source: `source/mir_eval/display.py:1095`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `voicing_recall` — runtime

- canonical source: `source/mir_eval/melody.py:441`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)
