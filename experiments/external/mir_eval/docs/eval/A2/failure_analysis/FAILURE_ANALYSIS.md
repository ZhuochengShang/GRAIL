# mir_eval A2 zero-round failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/docs/eval/A2/comprehension.json`
- Experiment fingerprint: `ea2bfacf7be649de61c9ef34386a0c1981e61766f231e06367304ff9caa25571`
- APIs: 148
- Failures: 13

## Failure categories

- `runtime`: 13

## Per-function evidence

### `deprecated`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:946`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 8.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError:`

### `first_n_three_layer_P`

- Category: `runtime`
- Source definition: `source/mir_eval/pattern.py:509`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 32.1
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/.aideal_exec/A2/output/ref_pattern.txt'`

### `load_key`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:497`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 20.5
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/.aideal_exec/A2/output/test_key.txt'`

### `load_patterns`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:331`
- Reached codebase frames: `source/mir_eval/io.py:380; source/mir_eval/io.py:26`
- Attempts / wall seconds: 1 / 25.1
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/source/tests/data/pattern/reference.txt'`

### `load_ragged_time_series`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:594`
- Reached codebase frames: `source/mir_eval/io.py:669; source/mir_eval/io.py:671`
- Attempts / wall seconds: 1 / 20.6
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Couldn't convert value timestamp using float found at /var/folders/83/6ly5xs5j5ns3gmwbqgjqd7rw0000gn/T/tmppufke0_n.csv:1:`

### `load_tempo`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:542`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.1
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/.aideal_exec/A2/output/test_tempo.txt'`

### `load_valued_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:448`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.0
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/.aideal_exec/A2/output/test_valued_intervals.txt'`

### `load_wav`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:409`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 33.5
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A2/experiments/external/mir_eval/.aideal_exec/A2/output/test_load.wav'`

### `p_score`

- Category: `runtime`
- Source definition: `source/mir_eval/beat.py:329`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.4
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected perfect score to be 1.0, got 0.0`

### `piano_roll`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:873`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 40.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 4 patches for 4 intervals, got 0`

### `reduce_extended_quality`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:319`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 7.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected base quality 'maj', got maj7`

### `ticker_pitch`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:1095`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.4
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 'A' in formatted MIDI 69, got 440`

### `voicing_recall`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:441`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 14.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: ufunc 'bitwise_and' not supported for the input types, and the inputs could not be safely coerced to any supported types according to the casting rule ''safe''`
