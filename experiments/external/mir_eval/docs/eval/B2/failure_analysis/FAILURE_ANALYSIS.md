# mir_eval B2 failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/docs/eval/B2/comprehension.json`
- Experiment fingerprint: `da987c338bb4e2b297e7758540d75da27a61508fd074d51cf725260f805260b6`
- APIs: 148
- Failures: 11

## Failure categories

- `runtime`: 11

## Per-function evidence

### `cemgil`

- Category: `runtime`
- Source definition: `source/mir_eval/beat.py:176`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected perfect score to be ~1.0, got 0.0`

### `hierarchy`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:498`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 8 patches, got 0`

### `load_key`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:497`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.0
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_key.txt'`

### `load_patterns`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:331`
- Reached codebase frames: `source/mir_eval/io.py:380; source/mir_eval/io.py:26`
- Attempts / wall seconds: 1 / 26.3
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/source/tests/data/pattern/reference.txt'`

### `load_ragged_time_series`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:594`
- Reached codebase frames: `source/mir_eval/io.py:669; source/mir_eval/io.py:671`
- Attempts / wall seconds: 1 / 21.7
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Couldn't convert value timestamp using float found at /var/folders/83/6ly5xs5j5ns3gmwbqgjqd7rw0000gn/T/tmp3up3srzm.csv:1:`

### `load_tempo`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:542`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.2
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_tempo.txt'`

### `load_wav`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:409`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 30.7
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_B2/experiments/external/mir_eval/.aideal_exec/B2/output/test_load.wav'`

### `piano_roll`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:873`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 39.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 4 patches for 4 intervals, got 0`

### `precision_recall_f1_overlap`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription_velocity.py:230`
- Reached codebase frames: `source/mir_eval/transcription.py:565; source/mir_eval/transcription.py:136`
- Attempts / wall seconds: 1 / 21.1
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Reference intervals and pitches have different lengths.`

### `ticker_pitch`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:1095`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 'A' in label for MIDI 69, got 440`

### `tmeasure`

- Category: `runtime`
- Source definition: `source/mir_eval/hierarchy.py:466`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 33.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected precision 1.0, got 0.0`
