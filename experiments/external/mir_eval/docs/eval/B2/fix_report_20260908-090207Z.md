# Fix-loop report — aideal_run_9t6ixhwq

_Generated 2026-09-08 02:49 by `aideal fix-report`._

- kind: **comprehension**  ·  run_id: `20260908-090207Z`  ·  models: audience=google:gemini-3.1-pro-preview, fixer=google:gemini-3.1-pro-preview
- pass **137/148** raw (92.6%)  ·  scored **137/148** (92.6%) after excluding 0 infra
- wall 0.79 h  ·  tokens in 366,141 / out 302,526 ·  llm calls 148  ·  max_fix_rounds 0
- pass-by-round: r0:137  ·  **0 rescued by the fix loop** (pass@0 = 137)

## Chronic failures across runs (5)

_Failed in ≥2 recorded runs with the same error signature at least twice — candidates for doc-repair with deep-dive, exclusion, or a harness/fixture fix rather than more snippet retries._

| API | runs failed | same-sig runs | distinct sigs | first seen |
|---|---|---|---|---|
| `load_key` | 4 | 2 | 3 |  |
| `load_patterns` | 4 | 2 | 3 |  |
| `load_tempo` | 4 | 2 | 3 |  |
| `load_wav` | 4 | 2 | 3 |  |
| `piano_roll` | 4 | 2 | 3 |  |

## Failure clusters (one issue, many APIs)

_Current failures grouped by normalized error signature (identifiers masked). Fixing the top cluster's root cause pays across all its APIs._

- **4x** [runtime] FileNotFoundError: [Errno 2] No such file or directory: <name>
  - `load_key`, `load_patterns`, `load_tempo`, `load_wav`
- **1x** [runtime] AssertionError: Expected perfect score to be ~1.0, got 0.0
  - `cemgil`
- **1x** [runtime] AssertionError: Expected 8 patches, got 0
  - `hierarchy`
- **1x** [runtime] ValueError: Couldn't convert value <name> using float found at /var/folders/83/6ly5xs5j5ns3gmwbqgjqd7rw0000gn/T/tmp3up3srzm.csv:<n>:
  - `load_ragged_time_series`
- **1x** [runtime] AssertionError: Expected 4 patches for 4 intervals, got 0
  - `piano_roll`
- **1x** [runtime] ValueError: Reference intervals and pitches have different lengths.
  - `precision_recall_f1_overlap`
- **1x** [runtime] AssertionError: Expected <name> in label for MIDI 69, got <num>
  - `ticker_pitch`
- **1x** [runtime] AssertionError: Expected precision 1.0, got 0.0
  - `tmeasure`

## Why each API fails (11 failing)

### `cemgil` — runtime

- canonical source: `source/mir_eval/beat.py:176`
- last error: AssertionError: Expected perfect score to be ~1.0, got 0.0
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected perfect score to be ~1.0, got 0.0

### `hierarchy` — runtime

- canonical source: `source/mir_eval/display.py:498`
- last error: AssertionError: Expected 8 patches, got 0
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected 8 patches, got 0

### `load_key` — runtime

- canonical source: `source/mir_eval/io.py:497`
- last error: FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_key.txt'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/externa

### `load_patterns` — runtime

- canonical source: `source/mir_eval/io.py:331` · reached: `source/mir_eval/io.py:380`, `source/mir_eval/io.py:26`
- last error: FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/tests/data/pattern/reference.txt'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/externa

### `load_ragged_time_series` — runtime

- canonical source: `source/mir_eval/io.py:594` · reached: `source/mir_eval/io.py:669`, `source/mir_eval/io.py:671`
- last error: ValueError: Couldn't convert value timestamp using float found at /var/folders/83/6ly5xs5j5ns3gmwbqgjqd7rw0000gn/T/tmp3up3srzm.csv:1:
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] ValueError: Couldn't convert value timestamp using float found at /var/folders/83/6ly5xs5j5ns3gmwbqgjqd7rw0000gn/T/tmp3up3srzm.csv:1:

### `load_tempo` — runtime

- canonical source: `source/mir_eval/io.py:542`
- last error: FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_tempo.txt'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/externa

### `load_wav` — runtime

- canonical source: `source/mir_eval/io.py:409`
- last error: FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_load.wav'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/externa

### `piano_roll` — runtime

- canonical source: `source/mir_eval/display.py:873`
- last error: AssertionError: Expected 4 patches for 4 intervals, got 0
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected 4 patches for 4 intervals, got 0

### `precision_recall_f1_overlap` — runtime

- canonical source: `source/mir_eval/transcription_velocity.py:230` · reached: `source/mir_eval/transcription.py:565`, `source/mir_eval/transcription.py:136`
- last error: ValueError: Reference intervals and pitches have different lengths.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] ValueError: Reference intervals and pitches have different lengths.

### `ticker_pitch` — runtime

- canonical source: `source/mir_eval/display.py:1095`
- last error: AssertionError: Expected 'A' in label for MIDI 69, got 440
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected 'A' in label for MIDI 69, got 440

### `tmeasure` — runtime

- canonical source: `source/mir_eval/hierarchy.py:466`
- last error: AssertionError: Expected precision 1.0, got 0.0
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected precision 1.0, got 0.0
