# mir_eval A1 failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/docs/eval/A1/comprehension.json`
- Experiment fingerprint: `6f5bcaa71d6a868167732ff1b08ada63654abf63b2bc6f0777aae06911a1e74f`
- APIs: 148
- Failures: 71

## Failure categories

- `infra`: 5
- `no-correctness-check`: 1
- `runtime`: 64
- `unknown`: 1

## Per-function evidence

### `IntervalFormatter`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:478`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 375.5
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: IntervalFormatter.__init__() missing 2 required positional arguments: 'base' and 'ticks'`

### `absolute_error`

- Category: `runtime`
- Source definition: `source/mir_eval/alignment.py:115`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 392.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: absolute_error is not a documented public API in mir_eval and its contract cannot be verified.`

### `adjust_events`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:359`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 2 events, got 4`

### `bss_eval_images_framewise`

- Category: `unknown`
- Source definition: `source/mir_eval/separation.py:507`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 173.1
- Diagnosis: Unclassified failure; inspect the captured error, rounds, and source location.
- Error: `sers/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/separation.py:592: FutureWarning: mir_eval.separation.bss_eval_images
	Deprecated as of mir_eval version 0.8.
	It will be removed in mir_eval version 0.9.
  result = bss_eval_images(`

### `cemgil`

- Category: `runtime`
- Source definition: `source/mir_eval/beat.py:176`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError:`

### `compute_accuracy`

- Category: `runtime`
- Source definition: `source/mir_eval/multipitch.py:248`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 336.1
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: compute_accuracy() got an unexpected keyword argument 'ref_times'`

### `compute_err_score`

- Category: `runtime`
- Source definition: `source/mir_eval/multipitch.py:296`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 384.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documentation does not support any non-tautological oracle for compute_err_score, and its module location is undocumented.`

### `compute_num_true_positives`

- Category: `runtime`
- Source definition: `source/mir_eval/multipitch.py:206`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 389.3
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()`

### `constant_hop_timebase`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:195`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 315.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected length 5, got 6`

### `deprecated`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:946`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 386.8
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: deprecated() takes 0 positional arguments but 2 were given`

### `deviation`

- Category: `no-correctness-check`
- Source definition: `source/mir_eval/segment.py:252`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 600.9
- Diagnosis: Snippet ran but did not emit the required deterministic correctness witness.
- Error: `ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ deviation " + <witness>).`

### `directional_hamming_distance`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:1359`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.6
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: module 'mir_eval.segment' has no attribute 'directional_hamming_distance'`

### `encode`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:471`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 20.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected bass 2 for D:min, got 0`

### `establishment_FPR`

- Category: `runtime`
- Source definition: `source/mir_eval/pattern.py:238`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 343.3
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected establishment FPR of 0.0 for a perfect match, got (1.0, 1.0, 1.0)`

### `filter_kwargs`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:860`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 14.9
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: argument of type 'NoneType' is not iterable`

### `freq_to_voicing`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:157`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 8.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Output should be a numpy array`

### `hierarchy`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:498`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 30.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError:`

### `hz_to_midi`

- Category: `infra`
- Source definition: `source/mir_eval/util.py:913`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 381.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'hz2midi' from 'mir_eval.melody' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/melody.py)`

### `index_labels`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:14`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 24.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected a numpy array for indices`

### `intervals_to_samples`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:74`
- Reached codebase frames: `source/mir_eval/util.py:112`
- Attempts / wall seconds: 1 / 24.3
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: operands could not be broadcast together with shapes (20,) (3,)`

### `join`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:436`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 384.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract for 'join' is insufficient to verify the result.`

### `karaoke_perceptual_metric`

- Category: `infra`
- Source definition: `source/mir_eval/alignment.py:269`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 394.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'karaoke_perceptual_metric' from 'mir_eval.separation' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/separ`

### `labeled_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:312`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 26.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected texts to be added to the axes for labeled intervals`

### `load_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:206`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.0
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_intervals.txt'`

### `load_key`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:497`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.9
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_key.txt'`

### `load_labeled_events`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:162`
- Reached codebase frames: `source/mir_eval/io.py:193; source/mir_eval/io.py:98`
- Attempts / wall seconds: 1 / 10.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `ValueError: Expected 2 columns, got 1 at /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/tests/data/beat/ref00.txt:1:`

### `load_patterns`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:331`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 35.9
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_patterns.txt'`

### `load_tempo`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:542`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.6
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_tempo.txt'`

### `load_valued_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:448`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.1
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_valued_intervals.txt'`

### `load_wav`

- Category: `runtime`
- Source definition: `source/mir_eval/io.py:409`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.7
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/.aideal_exec/A1/output/test_load.wav'`

### `match_note_offsets`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription.py:169`
- Reached codebase frames: `source/mir_eval/transcription.py:233`
- Attempts / wall seconds: 1 / 20.4
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed`

### `match_note_onsets`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription.py:262`
- Reached codebase frames: `source/mir_eval/transcription.py:301`
- Attempts / wall seconds: 1 / 329.1
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()`

### `match_notes`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription_velocity.py:107`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 33.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 4 matches, got 3`

### `merge_chord_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:1490`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 387.4
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract for merge_chord_intervals is insufficient to verify the result.`

### `merge_labeled_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:481`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.6
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: merge_labeled_intervals() missing 2 required positional arguments: 'y_intervals' and 'y_labels'`

### `metrics`

- Category: `infra`
- Source definition: `source/mir_eval/multipitch.py:348`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'metrics' from 'mir_eval.beat' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/beat.py)`

### `midi_to_chroma`

- Category: `infra`
- Source definition: `source/mir_eval/multipitch.py:173`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 43.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'midi_to_chroma' from 'mir_eval.util' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/util.py)`

### `mirex`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:1044`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 20.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: mirex() takes 2 positional arguments but 4 were given`

### `mutual_information`

- Category: `runtime`
- Source definition: `source/mir_eval/segment.py:869`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 30.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `ValueError: too many values to unpack (expected 2)`

### `nce`

- Category: `runtime`
- Source definition: `source/mir_eval/segment.py:960`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 36.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected S_over to be 0.0 for identical inputs, got 1.0`

### `occurrence_FPR`

- Category: `runtime`
- Source definition: `source/mir_eval/pattern.py:299`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 39.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected occurrence FPR of 0.0 for identical patterns, got (1.0, 1.0, 1.0)`

### `offset_precision_recall_f1`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription.py:705`
- Reached codebase frames: `source/mir_eval/transcription.py:765; source/mir_eval/transcription.py:166; source/mir_eval/util.py:749`
- Attempts / wall seconds: 1 / 29.8
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Intervals should be n-by-2 numpy ndarray, but shape=(2,)`

### `onset_precision_recall_f1`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription.py:643`
- Reached codebase frames: `source/mir_eval/transcription.py:690; source/mir_eval/transcription.py:166; source/mir_eval/util.py:749`
- Attempts / wall seconds: 1 / 332.4
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Intervals should be n-by-2 numpy ndarray, but shape=(2,)`

### `overseg`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:1409`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 386.7
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AssertionError: The documented contract is insufficient to verify the result: The documented contract is insufficient to verify the result: overseg function not found in mir_eval.segment`

### `percentage_correct`

- Category: `runtime`
- Source definition: `source/mir_eval/alignment.py:144`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 379.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract for percentage_correct is insufficient to verify the result.`

### `percentage_correct_segments`

- Category: `runtime`
- Source definition: `source/mir_eval/alignment.py:175`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 372.7
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AssertionError: percentage_correct_segments not found in mir_eval.segment or contract unverifiable`

### `precision_recall_f1_overlap`

- Category: `runtime`
- Source definition: `source/mir_eval/transcription_velocity.py:230`
- Reached codebase frames: `source/mir_eval/transcription.py:565; source/mir_eval/transcription.py:136`
- Attempts / wall seconds: 1 / 24.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Reference intervals and pitches have different lengths.`

### `raw_chroma_accuracy`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:622`
- Reached codebase frames: `source/mir_eval/melody.py:666; source/mir_eval/melody.py:104`
- Attempts / wall seconds: 1 / 35.3
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Voicing arrays must be between 0 and 1.`

### `raw_pitch_accuracy`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:554`
- Reached codebase frames: `source/mir_eval/melody.py:595; source/mir_eval/melody.py:104`
- Attempts / wall seconds: 1 / 31.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Voicing arrays must be between 0 and 1.`

### `reduce_extended_quality`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:319`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 378.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 'C:maj7', got ('C:maj9', set())`

### `register_colormap`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:117`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 337.6
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: register_colormap() missing 2 required positional arguments: 'name' and 'cmap'`

### `rotate_bitmap_to_root`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:559`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], got [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]`

### `rotate_bitmaps_to_roots`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:594`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Rotated bitmaps should match`

### `seg`

- Category: `infra`
- Source definition: `source/mir_eval/chord.py:1461`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 383.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'seg' from 'mir_eval' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mir_eval_A1/experiments/external/mir_eval/source/mir_eval/__init__.py)`

### `segments`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:180`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.3
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 4 text labels to be plotted, got 0`

### `split_key_string`

- Category: `runtime`
- Source definition: `source/mir_eval/key.py:93`
- Reached codebase frames: `source/mir_eval/key.py:111`
- Attempts / wall seconds: 1 / 14.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `ValueError: not enough values to unpack (expected 2, got 1)`

### `standard_FPR`

- Category: `runtime`
- Source definition: `source/mir_eval/pattern.py:171`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 35.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected FPR 0.0 for identical patterns, got (1.0, 1.0, 1.0)`

### `tetrads_inv`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:952`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 39.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: tetrads_inv() takes 2 positional arguments but 4 were given`

### `thirds`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:715`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.4
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `NameError: name 'chord_estimate_file' is not defined`

### `ticker_notes`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:1077`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 33.8
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: cannot unpack non-iterable NoneType object`

### `ticker_pitch`

- Category: `runtime`
- Source definition: `source/mir_eval/display.py:1095`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 24.3
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: ticker_pitch() takes from 0 to 1 positional arguments but 2 were given`

### `tmeasure`

- Category: `runtime`
- Source definition: `source/mir_eval/hierarchy.py:466`
- Reached codebase frames: `source/mir_eval/hierarchy.py:523`
- Attempts / wall seconds: 1 / 22.3
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: '>' not supported between instances of 'float' and 'list'`

### `to_cent_voicing`

- Category: `runtime`
- Source definition: `source/mir_eval/melody.py:316`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 25.6
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: to_cent_voicing() missing 2 required positional arguments: 'est_time' and 'est_freq'`

### `underseg`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:1435`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 403.5
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: module 'mir_eval.segment' has no attribute 'underseg'`

### `validate_boundary`

- Category: `runtime`
- Source definition: `source/mir_eval/segment.py:86`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 359.4
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: validate_boundary() missing 2 required positional arguments: 'estimated_intervals' and 'trim'`

### `validate_chord_label`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:348`
- Reached codebase frames: `source/mir_eval/chord.py:357`
- Attempts / wall seconds: 1 / 12.1
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `InvalidChordException: Invalid chord label: InvalidChordLabel`

### `validate_frequencies`

- Category: `runtime`
- Source definition: `source/mir_eval/util.py:794`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 27.3
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: validate_frequencies() missing 2 required positional arguments: 'max_freq' and 'min_freq'`

### `validate_hier_intervals`

- Category: `runtime`
- Source definition: `source/mir_eval/hierarchy.py:431`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 16.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: validate_hier_intervals only raises on invalid input and returns None; documented contract is insufficient to verify the result`

### `validate_structure`

- Category: `runtime`
- Source definition: `source/mir_eval/segment.py:121`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 342.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: validate_structure should pass for valid intervals and labels`

### `validate_tempi`

- Category: `runtime`
- Source definition: `source/mir_eval/tempo.py:29`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result.`

### `weighted_accuracy`

- Category: `runtime`
- Source definition: `source/mir_eval/chord.py:647`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 16.0
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: module 'mir_eval.key' has no attribute 'weighted_accuracy'`
