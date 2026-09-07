# mir_eval — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `IntervalFormatter`

### Signature
```python
class IntervalFormatter(Formatter)
```
_Source: source/mir_eval/display.py:478_

_Source doc:_ Ticker formatter for labeled interval plots. Parameters ---------- base : array-like of int The base positions of each label ticks : array-like of string The labels for the ticks

### Goal
A matplotlib ticker formatter used to label interval plots (such as segment or chord annotations) by mapping integer base positions to specific string labels.

### Parameters
_None._

### Input
When instantiating the class, the caller must provide the arguments defined in the source documentation:
*   `base`: An array-like of integers representing the base positions of each label on the axis.
*   `ticks`: An array-like of strings representing the text labels for the corresponding ticks.
*   **Preconditions:** As a display utility, any plotting script using this formatter must be run in a headless environment (e.g., using the `Agg` backend) if executed in an automated test suite, without requiring network or audio-device access.

### Output
Returns `unspecified` — An instance of `IntervalFormatter` (inheriting from matplotlib's `Formatter`) that can be applied to a matplotlib `Axis` object (e.g., via `ax.yaxis.set_major_formatter()`) to format its tick labels.

### Valid Call Patterns
```python
import matplotlib
matplotlib.use('Agg')  # Enforce headless display constraint
import matplotlib.pyplot as plt
import mir_eval.display

# Inferred from signature and source doc (not verified by test suite)
base_positions = [0, 1, 2]
tick_labels = ['Verse', 'Chorus', 'Bridge']

# Instantiate the formatter
formatter = mir_eval.display.IntervalFormatter(base=base_positions, ticks=tick_labels)

# Apply to a matplotlib axis
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
```

### LLM Instruction Prompt
- When generating plots for labeled intervals (like structural segments or chords) using `mir_eval.display`, use `IntervalFormatter` to map integer axis positions to their corresponding string labels.
- Always configure matplotlib to use a headless backend (e.g., `matplotlib.use('Agg')`) before importing `pyplot` or `mir_eval.display` to comply with the project's headless display constraints.
- Ensure the `base` (array of ints) and `ticks` (array of strings) arguments are provided and correspond to one another.

### Prompt Snippet
```text
Use `mir_eval.display.IntervalFormatter(base, ticks)` to format matplotlib axes for interval plots. `base` is an array-like of integer positions, and `ticks` is an array-like of string labels. Apply it using `ax.yaxis.set_major_formatter(formatter)`. Ensure matplotlib is set to a headless backend like 'Agg' for tests.
```

### Common Failure Modes
- **Headless Environment Violation:** Failing to set a headless matplotlib backend (like `Agg`) before plotting, causing the script to crash in CI/CD environments without a display server.
- **Mismatched Array Lengths:** Providing a `base` array and a `ticks` array of different lengths, which will cause alignment or indexing errors when matplotlib attempts to resolve the tick labels.
- **Invalid Base Types:** Passing non-integer values to `base` when the formatter expects an array-like of `int` for the base positions.

### Fix Code Hint
```python
import matplotlib
# FIX: Always set headless backend before importing pyplot or mir_eval.display
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mir_eval.display

# FIX: Ensure base and ticks are the same length and base contains integers
base_ints = [10, 20, 30]
label_strs = ['A', 'B', 'C']
formatter = mir_eval.display.IntervalFormatter(base=base_ints, ticks=label_strs)
```

## API Test: `InvalidChordException`

### Signature
```python
class InvalidChordException(Exception)
```
_Source: source/mir_eval/chord.py:113_

_Source doc:_ Exception class for suspect / invalid chord labels

### Goal
An exception class raised to indicate that a provided chord label is suspect, malformed, or contains an invalid chord quality during music-information-retrieval evaluation.

### Parameters
_None._ (Standard Python `Exception` arguments apply, such as the error message string).

### Input
Typically instantiated with a string message describing the invalid chord label. It is raised internally by `mir_eval.chord` functions when chord labels fail strict regular expression validation or contain qualities not restricted to the valid `chord.QUALITIES`.

### Output
Returns `unspecified` — an instance of `InvalidChordException` representing an error state during chord parsing, encoding, or evaluation.

### Valid Call Patterns
```python
import mir_eval

# Note: This example is inferred from the signature (not verified by an existing test).
try:
    # Example of a hypothetical operation that might trigger the exception
    # if an invalid chord label (e.g., failing regex validation) is encountered.
    raise mir_eval.chord.InvalidChordException("Invalid chord label: 'Xmaj7'")
except mir_eval.chord.InvalidChordException as e:
    print(f"Caught an invalid chord: {e}")
```

### LLM Instruction Prompt
- When evaluating chord annotations or encoding chords using `mir_eval.chord`, anticipate and catch `InvalidChordException` to gracefully handle dirty or non-standard chord labels. Chord validation uses strict regular expressions and restricts invalid chord types from `chord.QUALITIES`.

### Prompt Snippet
```text
`mir_eval.chord.InvalidChordException` is an Exception raised for suspect or invalid chord labels. Catch this exception when parsing repository-format chord annotations to prevent pipeline crashes on labels that fail regex validation or fall outside `chord.QUALITIES`.
```

### Common Failure Modes
- **Crashing on uncleaned data:** Processing raw, uncleaned repository-format chord annotations without a `try...except` block, causing the evaluation pipeline to crash when a non-standard or ambiguous chord label is encountered.
- **Invalid chord qualities:** Passing chord strings that contain qualities not recognized by `mir_eval`'s internal `chord.QUALITIES` list.

### Fix Code Hint
```python
import mir_eval

def safe_encode_chord(chord_label):
    try:
        # Attempt to process the chord label
        return mir_eval.chord.encode(chord_label)
    except mir_eval.chord.InvalidChordException as e:
        # Handle the suspect/invalid chord label gracefully
        print(f"Skipping invalid chord '{chord_label}': {e}")
        return None
```

## API Test: `absolute_error`

### Signature
```python
def absolute_error(reference_timestamps, estimated_timestamps)
```
_Source: source/mir_eval/alignment.py:115_

_Source doc:_ Compute the absolute deviations between estimated and reference timestamps, and then returns the median and average over all events Examples -------- >>> reference_timestamps = mir_eval.io.load_events('reference.txt') >>> estimated_timestamps = mir_eval.io.load_events('estimated.txt') >>> mae, aae = mir_eval.align.absolute_error(reference_onsets, estimated_timestamps) Parameters ---------- reference_timestamps : np.ndarray reference timestamps, in seconds estimated_timestamps : np.ndarray estimated timestamps, in seconds Returns ------- mae : float Median absolute error aae: float Average absolute error

### Goal
Compute the absolute deviations between estimated and reference timestamps for alignment evaluation, returning both the median and average errors across all events.

### Parameters
- `reference_timestamps`: `np.ndarray` — The ground truth reference timestamps, measured in seconds.
- `estimated_timestamps`: `np.ndarray` — The estimated timestamps to evaluate, measured in seconds.

### Input
Both inputs must be 1-dimensional `np.ndarray` objects containing timestamps in seconds. These are typically parsed from repository-format text files using `mir_eval.io.load_events()`. The arrays should be pre-matched or of equal length so that element-wise absolute deviation can be computed.

### Output
Returns `unspecified` — A tuple of two floats: `(mae, aae)`. `mae` represents the Median Absolute Error, and `aae` represents the Average Absolute Error.

### Valid Call Patterns
```python
# Inferred from the source docstring example
import mir_eval

reference_timestamps = mir_eval.io.load_events('reference.txt')
estimated_timestamps = mir_eval.io.load_events('estimated.txt')

# Compute the median and average absolute errors
mae, aae = mir_eval.alignment.absolute_error(reference_timestamps, estimated_timestamps)
```

### LLM Instruction Prompt
- When evaluating alignment timestamps, use `mir_eval.alignment.absolute_error(reference_timestamps, estimated_timestamps)`.
- Ensure both inputs are `np.ndarray` objects containing timestamps in seconds.
- Unpack the return value into two float variables representing the median absolute error (MAE) and average absolute error (AAE), in that exact order.
- Use `mir_eval.io.load_events()` to load the timestamp arrays from text files before passing them to this function.

### Prompt Snippet
```text
mir_eval.alignment.absolute_error(reference_timestamps, estimated_timestamps)
Computes absolute deviations between estimated and reference timestamps.
Inputs: Two np.ndarray objects of timestamps in seconds.
Returns: Tuple of (mae: float, aae: float) for Median and Average Absolute Error.
```

### Common Failure Modes
- Passing 2D interval arrays (e.g., `[start, end]`) instead of 1D timestamp arrays. `absolute_error` expects 1D arrays of discrete events.
- Passing raw file paths or file objects directly to the function instead of loading them into `np.ndarray` objects first using `mir_eval.io.load_events()`.
- Passing arrays of mismatched lengths, which will cause element-wise numpy operations to fail. Events must be matched or aligned prior to computing the absolute error.

### Fix Code Hint
```python
# INCORRECT: Passing file paths directly
# mae, aae = mir_eval.alignment.absolute_error('ref.txt', 'est.txt')

# CORRECT: Load events into numpy arrays first
import mir_eval
ref_times = mir_eval.io.load_events('ref.txt')
est_times = mir_eval.io.load_events('est.txt')

# Ensure arrays are matched in length before calling if necessary
# (e.g., using mir_eval.util.match_events)

mae, aae = mir_eval.alignment.absolute_error(ref_times, est_times)
```

## API Test: `adjust_events`

### Signature
```python
def adjust_events(events, labels=None, t_min=0.0, t_max=None, label_prefix='__')
```
_Source: source/mir_eval/util.py:359_

_Source doc:_ Adjust the given list of event times to span the range ``[t_min, t_max]``. Any event times outside of the specified range will be removed. If the times do not span ``[t_min, t_max]``, additional events will be added with the prefix ``label_prefix``. Parameters ---------- events : np.ndarray Array of event times (seconds) labels : list or None List of labels (Default value = None) t_min : float or None Minimum valid event time. (Default value = 0.0) t_max : float or None Maximum valid event time. (Default value = None) label_prefix : str Prefix string to use for synthetic labels (Default value = '__') Returns ------- new_times : np.ndarray Event times corrected to the given range.

### Goal
Adjust a sequence of event timestamps (and optionally their corresponding labels) to strictly span a specified time range `[t_min, t_max]`, trimming out-of-bounds events and padding with synthetic boundary events if necessary.

### Parameters
- `events`: A 1D `np.ndarray` of event times in seconds.
- `labels`, default `None`: A `list` of string labels corresponding to the `events`, or `None` if no labels are used.
- `t_min`, default `0.0`: A `float` representing the minimum valid event time, or `None`.
- `t_max`, default `None`: A `float` representing the maximum valid event time, or `None`.
- `label_prefix`, default `'__'`: A `str` prefix used to generate synthetic labels (e.g., `"__T_MIN"`, `"__T_MAX"`) when boundary events are added.

### Input
The caller must provide a 1D numpy array of numerical timestamps for `events`. If `labels` is provided, it must be a list of exactly the same length as the `events` array. `t_min` and `t_max` should be numerical bounds (typically floats) defining the valid time range.

### Output
Returns `unspecified` — The return signature depends on the `labels` argument. If `labels` is `None`, it returns a single `np.ndarray` of the adjusted event times. If `labels` is provided, it returns a tuple `(new_events, new_labels)`, where `new_events` is the adjusted `np.ndarray` of times and `new_labels` is the adjusted `list` of labels (including any synthetic boundary labels like `"__T_MIN"`).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Pattern 1: Adjusting events and labels together
events = np.arange(1, 11, dtype=float)
labels = [str(n) for n in range(10)]
new_e, new_l = mir_eval.util.adjust_events(events, labels, 0.0, 11.0)

# Pattern 2: Adjusting only events (labels=None)
events_only = np.array([1.5, 2.5, 12.0])
new_e_only = mir_eval.util.adjust_events(events_only, t_min=0.0, t_max=10.0)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.adjust_events`, you MUST handle the return value conditionally based on the `labels` argument. Despite the source docstring only mentioning `new_times`, the function returns a tuple `(new_events, new_labels)` if `labels` is passed as a list. If `labels` is `None` or omitted, it returns only `new_events`. Ensure `events` is a numpy array, not a standard Python list.

### Prompt Snippet
```text
mir_eval.util.adjust_events returns a tuple `(new_events, new_labels)` if the `labels` argument is provided. If `labels` is None, it returns just `new_events`. Always pass `events` as a numpy array.
```

### Common Failure Modes
- **ValueError (Too many values to unpack):** Occurs if the caller attempts to unpack `new_e, new_l = adjust_events(events)` without passing the `labels` argument.
- **TypeError (Cannot unpack non-iterable):** Occurs if the caller attempts to unpack `new_e, new_l` when `labels` is explicitly set to `None`.
- **Length Mismatch:** Passing a `labels` list that has a different length than the `events` array will cause indexing errors during the adjustment process.

### Fix Code Hint
```python
# WRONG: Unpacking two values when labels is not provided
new_e, new_l = mir_eval.util.adjust_events(events, t_min=0.0, t_max=10.0)

# RIGHT: Assign to a single variable when labels=None
new_e = mir_eval.util.adjust_events(events, t_min=0.0, t_max=10.0)

# RIGHT: Unpack two values when labels is provided
new_e, new_l = mir_eval.util.adjust_events(events, labels=my_labels, t_min=0.0, t_max=10.0)
```

## API Test: `adjust_intervals`

### Signature
```python
def adjust_intervals(intervals, labels=None, t_min=0.0, t_max=None, start_label='__T_MIN', end_label='__T_MAX')
```
_Source: source/mir_eval/util.py:261_

_Source doc:_ Adjust a list of time intervals to span the range ``[t_min, t_max]``. Any intervals lying completely outside the specified range will be removed. Any intervals lying partially outside the specified range will be cropped. If the specified range exceeds the span of the provided data in either direction, additional intervals will be appended.  If an interval is appended at the beginning, it will be given the label ``start_label``; if an interval is appended at the end, it will be given the label ``end_label``. Parameters ---------- intervals : np.ndarray, shape=(n_events, 2) Array of interval start and end-times labels : list, len=n_events or None List of labels (Default value = None) t_min : float or None Minimum interval start time. (Default value = 0.0) t_max : float or None Maximum interval end time. (Default value = None) start_label : str or float or int Label to give any intervals appended at the beginning (Default value = '__T_MIN') end_label : str or float or int Label to give any intervals appended at the end (Default value = '__T_MAX') Returns ------- new_intervals : np.ndarray Intervals spanning ``[t_min, t_max]`` new_labels : list List of labels for ``new_labels``

### Goal
Adjust a list of time intervals (and optionally their labels) to strictly span a specified time range `[t_min, t_max]` by cropping overlapping intervals, removing out-of-bounds intervals, and appending new intervals to fill gaps at the boundaries.

### Parameters
- `intervals`: A 2D numpy array of shape `(n_events, 2)` representing the start and end times of the events.
- `labels`, default `None`: A list of length `n_events` containing the labels corresponding to each interval.
- `t_min`, default `0.0`: A float (or `None`) specifying the minimum interval start time.
- `t_max`, default `None`: A float (or `None`) specifying the maximum interval end time.
- `start_label`, default `'__T_MIN'`: A string, float, or int to assign as the label for any interval appended at the beginning of the sequence.
- `end_label`, default `'__T_MAX'`: A string, float, or int to assign as the label for any interval appended at the end of the sequence.

### Input
The caller must provide `intervals` as a 2-dimensional numpy array of shape `(n_events, 2)`. If `labels` are provided, they must be passed as a Python list whose length exactly matches the number of rows in `intervals` (`n_events`). `t_min` and `t_max` should be numeric values (floats) defining the target boundary.

### Output
Returns `unspecified` — A tuple of two elements: `(new_intervals, new_labels)`. `new_intervals` is a numpy array of shape `(m_events, 2)` containing the adjusted intervals spanning `[t_min, t_max]`. `new_labels` is a list of length `m_events` containing the corresponding labels (including any newly appended `start_label` or `end_label`).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# INFERRED FROM SIGNATURE (no verified example provided in context)
intervals = np.array([[1.0, 3.0], [4.0, 6.0]])
labels = ['chord_A', 'chord_B']

# Adjust intervals to span exactly 0.0 to 10.0
new_intervals, new_labels = mir_eval.util.adjust_intervals(
    intervals, 
    labels=labels, 
    t_min=0.0, 
    t_max=10.0, 
    start_label='N', 
    end_label='N'
)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.adjust_intervals`, ensure `intervals` is a `(n, 2)` numpy array, not a flat list or 1D array.
- If passing `labels`, ensure it is a list of exactly the same length as the number of intervals.
- Always unpack the return value into two variables `(new_intervals, new_labels)`, even if `labels` was passed as `None` (in which case `new_labels` will be a list of `None`s or default labels).

### Prompt Snippet
```text
`mir_eval.util.adjust_intervals(intervals, labels=None, t_min=0.0, t_max=None, start_label='__T_MIN', end_label='__T_MAX')`
Adjusts time intervals to span `[t_min, t_max]`. `intervals` must be a `(n, 2)` numpy array. Returns a tuple `(new_intervals, new_labels)`.
```

### Common Failure Modes
- Passing a standard Python list of lists for `intervals` instead of a numpy array, which may cause shape-checking or numpy-specific operations to fail.
- Passing a `labels` list that does not match the `n_events` dimension of `intervals`, leading to a length mismatch error.
- Forgetting to unpack the return value, resulting in a tuple being mistakenly passed to downstream metric functions that expect a numpy array of intervals.

### Fix Code Hint
```python
# BAD: Forgetting to unpack the return value or passing a raw list
adjusted = mir_eval.util.adjust_intervals([[1, 2], [3, 4]], t_max=5.0)
# adjusted is a tuple, which will break downstream functions

# GOOD: Convert to numpy array and unpack the tuple
intervals_arr = np.array([[1.0, 2.0], [3.0, 4.0]])
new_intervals, new_labels = mir_eval.util.adjust_intervals(intervals_arr, t_max=5.0)
```

## API Test: `ari`

### Signature
```python
def ari(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1)
```
_Source: source/mir_eval/segment.py:589_

_Source doc:_ Compute the Adjusted Rand Index (ARI) for frame clustering segmentation evaluation. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> # Trim or pad the estimate to match reference timing >>> (ref_intervals, ...  ref_labels) = mir_eval.util.adjust_intervals(ref_intervals, ...                                               ref_labels, ...                                               t_min=0) >>> (est_intervals, ...  est_labels) = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()) >>> ari_score = mir_eval.structure.ari(ref_intervals, ref_labels, ...                                    est_intervals, est_labels) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. reference_labels : list, shape=(n,) reference segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_labels : list, shape=(m,) estimated segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. frame_size : float > 0 length (in seconds) of frames for clustering (Default value = 0.1) Returns ------- ari_score : float > 0 Adjusted Rand index between segmentations.

### Goal
Compute the Adjusted Rand Index (ARI) to evaluate frame clustering segmentation by comparing reference and estimated segment intervals and their corresponding labels.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` representing the start and end times of the ground-truth reference segments.
- `reference_labels`: `list` of shape `(n,)` containing the ground-truth labels corresponding to the reference intervals.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` representing the start and end times of the estimated segments.
- `estimated_labels`: `list` of shape `(m,)` containing the predicted labels corresponding to the estimated intervals.
- `frame_size`, default `0.1`: A `float > 0` specifying the length (in seconds) of the frames used for clustering.

### Input
Inputs are typically loaded from repository-format annotation files using `mir_eval.io.load_labeled_intervals`. 
**Preconditions:** The estimated intervals must be trimmed or padded to exactly match the reference timing (e.g., using `mir_eval.util.adjust_intervals` with `t_min=0` and `t_max=ref_intervals.max()`) before being passed to `ari`. The `frame_size` must be strictly greater than 0.

### Output
Returns `unspecified` — A `float > 0` representing the Adjusted Rand Index (ARI) score between the reference and estimated segmentations.

### Valid Call Patterns
```python
import mir_eval

# Example inferred from the source docstring
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Precondition: Trim or pad the estimate to match reference timing
(ref_intervals, ref_labels) = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
(est_intervals, est_labels) = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)

# Compute the Adjusted Rand Index (ARI)
# Note: The docstring references mir_eval.structure.ari, which is an alias for mir_eval.segment.ari
ari_score = mir_eval.segment.ari(
    ref_intervals, ref_labels, est_intervals, est_labels, frame_size=0.1
)
```

### LLM Instruction Prompt
- When calling `mir_eval.segment.ari` (or `mir_eval.structure.ari`), you MUST first align the estimated intervals to the reference intervals' time span using `mir_eval.util.adjust_intervals`. Failure to trim or pad the estimates to match the reference timing will result in an evaluation error. Ensure `frame_size` is strictly greater than 0.

### Prompt Snippet
```text
mir_eval.segment.ari requires estimated intervals to be temporally aligned with reference intervals. Always preprocess inputs using `mir_eval.util.adjust_intervals(est_intervals, est_labels, t_min=0, t_max=ref_intervals.max())` before computing the ARI score.
```

### Common Failure Modes
- **Unaligned Time Spans:** Passing estimated intervals that cover a different total duration than the reference intervals without first adjusting them via `mir_eval.util.adjust_intervals`.
- **Invalid Frame Size:** Providing a `frame_size` that is less than or equal to 0.
- **Shape Mismatch:** Providing an intervals array of shape `(n, 2)` but a labels list of a different length `(m,)`.

### Fix Code Hint
```python
# FIX: Ensure estimated intervals match the reference duration before calling ari
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)
ari_score = mir_eval.segment.ari(ref_intervals, ref_labels, est_intervals, est_labels)
```

## API Test: `average_overlap_ratio`

### Signature
```python
def average_overlap_ratio(ref_intervals, est_intervals, matching)
```
_Source: source/mir_eval/transcription.py:591_

_Source doc:_ Compute the Average Overlap Ratio between a reference and estimated note transcription. Given a reference and corresponding estimated note, their overlap ratio (OR) is defined as the ratio between the duration of the time segment in which the two notes overlap and the time segment spanned by the two notes combined (earliest onset to latest offset): >>> OR = ((min(ref_offset, est_offset) - max(ref_onset, est_onset)) / ...     (max(ref_offset, est_offset) - min(ref_onset, est_onset))) The Average Overlap Ratio (AOR) is given by the mean OR computed over all matching reference and estimated notes. The metric goes from 0 (worst) to 1 (best). Note: this function assumes the matching of reference and estimated notes (see :func:`match_notes`) has already been performed and is provided by the ``matching`` parameter. Furthermore, it is highly recommended to validate the intervals (see :func:`validate_intervals`) before calling this function, otherwise it is possible (though unlikely) for this function to attempt a divide-by-zero operation. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) matching : list of tuples A list of matched reference and estimated notes. ``matching[i] == (i, j)`` where reference note ``i`` matches estimated note ``j``. Returns ------- avg_overlap_ratio : float The computed Average Overlap Ratio score

### Goal
Compute the Average Overlap Ratio (AOR) between a reference and estimated note transcription by averaging the overlap ratios of pre-matched note pairs.

### Parameters
- `ref_intervals`: `np.ndarray`, shape=(n,2). Array of reference note time intervals (onset and offset times in seconds).
- `est_intervals`: `np.ndarray`, shape=(m,2). Array of estimated note time intervals (onset and offset times in seconds).
- `matching`: `list` of `tuple`. A list of matched reference and estimated notes, where `matching[i] == (i, j)` indicates that reference note `i` matches estimated note `j`.

### Input
Numpy arrays of shape `(n, 2)` and `(m, 2)` representing the time intervals, and a list of tuples representing the index mapping of matched notes. 
**Preconditions:** 
1. The matching of reference and estimated notes must already be performed (e.g., via `mir_eval.transcription.match_notes`) and passed into the `matching` parameter.
2. Intervals should be validated (e.g., via `mir_eval.util.validate_intervals`) before calling this function to ensure that no interval has an onset greater than or equal to its offset, which would cause a divide-by-zero operation.

### Output
Returns `unspecified` — `float`. The computed Average Overlap Ratio score, ranging from 0.0 (worst) to 1.0 (best).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Inferred from signature and project context
ref_intervals = np.array([[0.5, 1.5], [2.0, 3.0]])
est_intervals = np.array([[0.6, 1.4], [1.9, 3.1]])
matching = [(0, 0), (1, 1)]

# Compute the Average Overlap Ratio
aor_score = mir_eval.transcription.average_overlap_ratio(
    ref_intervals, 
    est_intervals, 
    matching
)
```

### LLM Instruction Prompt
- Do not use `average_overlap_ratio` to discover note matches; it only scores pairs that have already been matched. You must provide the `matching` list explicitly.
- Always validate `ref_intervals` and `est_intervals` before calling this function to guarantee that `onset < offset` for all notes, preventing divide-by-zero errors.
- Ensure `ref_intervals` and `est_intervals` are `(n, 2)` and `(m, 2)` numpy arrays, not 1D arrays of boundaries or raw event timestamps.

### Prompt Snippet
```text
mir_eval.transcription.average_overlap_ratio(ref_intervals, est_intervals, matching) computes the mean overlap ratio for pre-matched notes. Preconditions: `matching` must be a list of `(ref_idx, est_idx)` tuples (e.g., from `match_notes`). Intervals must be validated `(n, 2)` arrays to prevent divide-by-zero. Returns a float between 0 and 1.
```

### Common Failure Modes
- **Divide-by-zero Warning/Error**: Occurs if an interval is invalid (e.g., onset equals offset), causing the combined duration denominator to be zero.
- **IndexError**: Occurs if the tuples in `matching` contain indices that are out of bounds for the provided `ref_intervals` or `est_intervals` arrays.
- **ValueError / Shape Mismatch**: Occurs if `ref_intervals` or `est_intervals` are passed as 1D arrays instead of `(n, 2)` arrays.

### Fix Code Hint
```python
# Ensure intervals are valid to prevent divide-by-zero
mir_eval.util.validate_intervals(ref_intervals)
mir_eval.util.validate_intervals(est_intervals)

# Obtain matching first (example using a hypothetical match_notes call)
# matching = mir_eval.transcription.match_notes(ref_intervals, ref_pitches, est_intervals, est_pitches)

aor = mir_eval.transcription.average_overlap_ratio(ref_intervals, est_intervals, matching)
```

## API Test: `boundaries_to_intervals`

### Signature
```python
def boundaries_to_intervals(boundaries)
```
_Source: source/mir_eval/util.py:239_

_Source doc:_ Convert an array of event times into intervals Parameters ---------- boundaries : list-like List-like of event times.  These are assumed to be unique timestamps in ascending order. Returns ------- intervals : np.ndarray, shape=(n_intervals, 2) Start and end time for each interval

### Goal
Convert a 1D sequence of sequential event timestamps into a 2D array of start and end times representing continuous intervals.

### Parameters
- `boundaries`: A list-like sequence of event times (timestamps).

### Input
A 1D list or numpy array of numerical timestamps. 
**Preconditions:** 
- The timestamps must be unique.
- The timestamps must be sorted in strictly ascending order.
- **Compatibility Rule:** Do not pass a `labels` argument; it is no longer supported by this function.

### Output
Returns `np.ndarray` — A 2D numpy array of shape `(n_intervals, 2)` containing the start and end time for each interval, where `n_intervals` is `len(boundaries) - 1`.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Basic usage from the test suite
boundaries = np.arange(10)
intervals = mir_eval.util.boundaries_to_intervals(boundaries)
# intervals is now a (9, 2) array where each row is [i, i+1]
```

### LLM Instruction Prompt
- Pass exactly one argument: a 1D list-like of unique, ascending timestamps.
- NEVER pass a `labels` argument to `boundaries_to_intervals`, as it has been removed from the API.
- Ensure the input array has at least two elements to form a valid interval.
- Expect a 2D numpy array of shape `(N-1, 2)` in return, which can be directly passed to MIR evaluation metrics requiring interval arrays (e.g., `mir_eval.segment.evaluate`).

### Prompt Snippet
```text
mir_eval.util.boundaries_to_intervals(boundaries)
Converts a 1D list-like of unique, ascending timestamps into a 2D numpy array of shape (N-1, 2) representing [start, end] intervals. Do not pass a `labels` argument (it is deprecated/removed).
```

### Common Failure Modes
- **TypeError from `labels` argument:** Attempting to pass `labels` as a second positional or keyword argument will crash, as the signature only accepts `boundaries`.
- **Invalid intervals (negative or zero duration):** Passing unsorted boundaries or duplicate timestamps violates the precondition, resulting in intervals where the end time is less than or equal to the start time.
- **IndexError/ValueError:** Passing an array with fewer than 2 boundaries, making it impossible to construct an interval of shape `(n_intervals, 2)`.

### Fix Code Hint
```python
# BAD: Passing unsorted boundaries or using the removed `labels` argument
# intervals = mir_eval.util.boundaries_to_intervals(boundaries, labels=my_labels)

# GOOD: Ensure boundaries are unique and sorted, and handle labels separately
boundaries = np.unique(boundaries) # Sorts and removes duplicates
intervals = mir_eval.util.boundaries_to_intervals(boundaries)
```

## API Test: `bss_eval_images`

### Signature
```python
def bss_eval_images(reference_sources, estimated_sources, compute_permutation=True)
```
_Source: source/mir_eval/separation.py:372_

_Source doc:_ Compute the bss_eval_images function from the BSS_EVAL Matlab toolbox. Ordering and measurement of the separation quality for estimated source signals in terms of filtered true source, interference and artifacts. This method also provides the ISR measure. The decomposition allows a time-invariant filter distortion of length 512, as described in Section III.B of [#vincent2006performance]_. Passing ``False`` for ``compute_permutation`` will improve the computation performance of the evaluation; however, it is not always appropriate and is not the way that the BSS_EVAL Matlab toolbox computes bss_eval_images. Examples -------- >>> # reference_sources[n] should be an ndarray of samples of the >>> # n'th reference source >>> # estimated_sources[n] should be the same for the n'th estimated >>> # source >>> (sdr, isr, sir, sar, ...  perm) = mir_eval.separation.bss_eval_images(reference_sources, ...                                               estimated_sources) Parameters ---------- reference_sources : np.ndarray, shape=(nsrc, nsampl, nchan) matrix containing true sources estimated_sources : np.ndarray, shape=(nsrc, nsampl, nchan) matrix containing estimated sources compute_permutation : bool, optional compute permutation of estimate/source combinations (True by default) Returns ------- sdr : np.ndarray, shape=(nsrc,) vector of Signal to Distortion Ratios (SDR) isr : np.ndarray, shape=(nsrc,) vector of source Image to Spatial distortion Ratios (ISR) sir : np.ndarray, shape=(nsrc,) vector of Source to Interference Ratios (SIR) sar : np.ndarray, shape=(nsrc,) vector of Sources to Artifacts Ratios (SAR) perm : np.ndarray, shape=(nsrc,) vector containing the best ordering of estimated sources in the mean SIR sense (estimated source number ``perm[j]`` corresponds to true source number ``j``).  Note: ``perm`` will be ``(1,2,...,nsrc)`` if ``compute_permutation`` is ``False``. References ---------- .. [#] Emmanuel Vincent, Shoko Araki, Fabian J. Theis, Guido Nolte, Pau Bofill, Hiroshi Sawada, Alexey Ozerov, B. Vikrham Gowreesunker, Dominik Lutter and Ngoc Q.K. Duong, "The Signal Separation Evaluation Campaign (2007-2010): Achievements and remaining challenges", Signal Processing, 92, pp. 1928-1936, 2012.

### Goal
Compute the BSS_EVAL metrics (SDR, ISR, SIR, SAR, and permutation) to evaluate the separation quality of estimated multi-channel audio source signals against true reference sources.

### Parameters
- `reference_sources`: A 3-dimensional `np.ndarray` of shape `(nsrc, nsampl, nchan)` containing the true reference source signals.
- `estimated_sources`: A 3-dimensional `np.ndarray` of shape `(nsrc, nsampl, nchan)` containing the estimated source signals.
- `compute_permutation`, default `True`: A boolean indicating whether to compute the best ordering of estimate/source combinations. Passing `False` improves performance but deviates from standard BSS_EVAL behavior.

### Input
- Both inputs must be 3-dimensional numpy arrays representing multi-channel audio, where `nsrc` is the number of sources, `nsampl` is the number of samples, and `nchan` is the number of channels.
- **Precondition:** The number of sources (`nsrc`) must match exactly between `reference_sources` and `estimated_sources`.
- **Precondition:** Neither the reference nor the estimated sources can be completely silent (all zeros).
- **Deprecation Note:** The `mir_eval.separation` module is deprecated.

### Output
Returns `unspecified` — A tuple of 5 `np.ndarray`s, each of shape `(nsrc,)`: `(sdr, isr, sir, sar, perm)`. 
- `sdr`: Signal to Distortion Ratios.
- `isr`: Image to Spatial distortion Ratios.
- `sir`: Source to Interference Ratios.
- `sar`: Sources to Artifacts Ratios.
- `perm`: The best ordering of estimated sources (if `compute_permutation=False`, this defaults to `(1, 2, ..., nsrc)`).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example inferred from test suite and source doc
nsrc, nsampl, nchan = 2, 100, 2
ref_sources = np.random.random_sample((nsrc, nsampl, nchan))
est_sources = np.random.random_sample((nsrc, nsampl, nchan))

(sdr, isr, sir, sar, perm) = mir_eval.separation.bss_eval_images(
    ref_sources, 
    est_sources
)
```

### LLM Instruction Prompt
- When calling `mir_eval.separation.bss_eval_images`, ensure both inputs are 3-dimensional numpy arrays of shape `(nsrc, nsampl, nchan)`.
- Verify that the number of sources (`nsrc`) matches between the reference and estimated arrays.
- Ensure that no source in either array is completely silent (all zeros), as this will raise a `ValueError`.
- Expect a 5-tuple of 1D numpy arrays as the return value.
- Note that the `mir_eval.separation` module is deprecated.

### Prompt Snippet
```text
When evaluating multi-channel source separation using `mir_eval.separation.bss_eval_images`, provide 3D numpy arrays of shape `(nsrc, nsampl, nchan)`. Ensure the number of sources matches and no source is completely silent (all zeros) to avoid a ValueError. The function returns a 5-tuple: (sdr, isr, sir, sar, perm). Note that the separation module is deprecated.
```

### Common Failure Modes
- **Silent Sources:** Passing an array where one or more sources are completely silent (e.g., `np.zeros((1, 100, 2))`) raises a `ValueError`.
- **Mismatched Source Counts:** Passing reference and estimated arrays with a different number of sources (`nsrc`) raises a `ValueError`.
- **Empty Inputs:** Passing empty arrays triggers a `UserWarning` ("reference_sources is empty" / "estimated_sources is empty") and returns empty arrays.
- **Incorrect Dimensionality:** Passing 2D arrays (mono audio) instead of 3D arrays will cause shape mismatch errors. For mono audio, use `bss_eval_sources` instead.

### Fix Code Hint
```python
# Ensure inputs are 3D (nsrc, nsampl, nchan) and have matching source counts
if reference_sources.shape[0] != estimated_sources.shape[0]:
    raise ValueError("Number of reference and estimated sources must match.")

# Ensure no source is completely silent
if not np.any(reference_sources) or not np.any(estimated_sources):
    raise ValueError("Sources cannot be completely silent.")

sdr, isr, sir, sar, perm = mir_eval.separation.bss_eval_images(
    reference_sources, 
    estimated_sources
)
```

## API Test: `bss_eval_images_framewise`

### Signature
```python
def bss_eval_images_framewise(reference_sources, estimated_sources, window=30 * 44100, hop=15 * 44100, compute_permutation=False)
```
_Source: source/mir_eval/separation.py:507_

_Source doc:_ Framewise computation of bss_eval_images Please be aware that this function does not compute permutations (by default) on the possible relations between ``reference_sources`` and ``estimated_sources`` due to the dangers of a changing permutation. Therefore (by default), it assumes that ``reference_sources[i]`` corresponds to ``estimated_sources[i]``. To enable computing permutations please set ``compute_permutation`` to be ``True`` and check that the returned ``perm`` is identical for all windows. NOTE: if ``reference_sources`` and ``estimated_sources`` would be evaluated using only a single window or are shorter than the window length, the result of ``bss_eval_images`` called on ``reference_sources`` and ``estimated_sources`` (with the ``compute_permutation`` parameter passed to ``bss_eval_images``) is returned Examples -------- >>> # reference_sources[n] should be an ndarray of samples of the >>> # n'th reference source >>> # estimated_sources[n] should be the same for the n'th estimated >>> # source >>> (sdr, isr, sir, sar, ...  perm) = mir_eval.separation.bss_eval_images_framewise( reference_sources, ...      estimated_sources, window, ....     hop) Parameters ---------- reference_sources : np.ndarray, shape=(nsrc, nsampl, nchan) matrix containing true sources (must have the same shape as ``estimated_sources``) estimated_sources : np.ndarray, shape=(nsrc, nsampl, nchan) matrix containing estimated sources (must have the same shape as ``reference_sources``) window : int Window length for framewise evaluation hop : int Hop size for framewise evaluation compute_permutation : bool, optional compute permutation of estimate/source combinations for all windows (False by default) Returns ------- sdr : np.ndarray, shape=(nsrc, nframes) vector of Signal to Distortion Ratios (SDR) isr : np.ndarray, shape=(nsrc, nframes) vector of source Image to Spatial distortion Ratios (ISR) sir : np.ndarray, shape=(nsrc, nframes) vector of Source to Interference Ratios (SIR) sar : np.ndarray, shape=(nsrc, nframes) vector of Sources to Artifacts Ratios (SAR) perm : np.ndarray, shape=(nsrc, nframes) vector containing the best ordering of estimated sources in the mean SIR sense (estimated source number perm[j] corresponds to true source number j) Note: perm will be range(nsrc) for all windows if compute_permutation

### Goal
Computes framewise source separation evaluation metrics (SDR, ISR, SIR, SAR) over sliding windows for multi-channel audio sources.

### Parameters
- `reference_sources`: `np.ndarray` of shape `(nsrc, nsampl, nchan)` containing the true reference sources. Must have the exact same shape as `estimated_sources`.
- `estimated_sources`: `np.ndarray` of shape `(nsrc, nsampl, nchan)` containing the estimated sources. Must have the exact same shape as `reference_sources`.
- `window`, default `30 * 44100`: `int` representing the window length in samples for the framewise evaluation.
- `hop`, default `15 * 44100`: `int` representing the hop size in samples for the framewise evaluation.
- `compute_permutation`, default `False`: `bool` indicating whether to compute the optimal permutation of estimate/source combinations for all windows.

### Input
The caller must provide two 3-dimensional numpy arrays representing multi-channel audio data: `(number_of_sources, number_of_samples, number_of_channels)`. Both arrays must have identical shapes. 
**Preconditions:** 
- The `mir_eval.separation` module is deprecated and slated for removal.
- Sources cannot be completely silent (arrays of all zeros); doing so will raise a `ValueError`.
- If the inputs are shorter than the window length, the function falls back to computing the standard `bss_eval_images` over a single window.

### Output
Returns `unspecified` — A tuple of 5 `np.ndarray`s, each of shape `(nsrc, nframes)`:
1. `sdr`: Signal to Distortion Ratios (SDR)
2. `isr`: source Image to Spatial distortion Ratios (ISR)
3. `sir`: Source to Interference Ratios (SIR)
4. `sar`: Sources to Artifacts Ratios (SAR)
5. `perm`: The best ordering of estimated sources in the mean SIR sense. If `compute_permutation` is `False`, this will simply be `range(nsrc)` for all windows.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example derived from the test suite
ref_sources = np.random.random_sample((2, 1000, 2))
est_sources = np.random.random_sample((2, 1000, 2))

# Compute framewise metrics with a window of 40 samples and hop of 20 samples
sdr, isr, sir, sar, perm = mir_eval.separation.bss_eval_images_framewise(
    ref_sources, est_sources, 40, 20
)
```

### LLM Instruction Prompt
- Ensure `reference_sources` and `estimated_sources` are 3D numpy arrays `(nsrc, nsampl, nchan)` of the exact same shape.
- Do not pass silent sources (arrays of all zeros), as this raises a `ValueError`.
- Be aware that `mir_eval.separation` is deprecated.
- By default, permutations are not computed. If `compute_permutation=True` is used, verify that the returned `perm` is identical across all windows.

### Prompt Snippet
```text
Use `mir_eval.separation.bss_eval_images_framewise(ref, est, window, hop)` to compute framewise SDR, ISR, SIR, and SAR for multi-channel audio. Both inputs must be 3D numpy arrays `(nsrc, nsampl, nchan)` of identical shape. Do not pass silent (all-zero) sources. Note that the separation module is deprecated.
```

### Common Failure Modes
- **Silent Sources**: Passing a reference or estimated source that is entirely zeros raises a `ValueError`.
- **Shape Mismatch**: Passing `reference_sources` and `estimated_sources` with different shapes raises a `ValueError`.
- **Empty Inputs**: Passing empty arrays (e.g., `np.array([])`) raises a `UserWarning` ("reference_sources is empty") and returns empty arrays.
- **Dimensionality Errors**: Passing 2D arrays (single-channel sources) to this function, which expects 3D arrays `(nsrc, nsampl, nchan)`. For single-channel data, use `bss_eval_sources_framewise` instead.

### Fix Code Hint
```python
# Ensure inputs are 3D arrays (sources, samples, channels)
if ref_sources.ndim == 2:
    # If single channel, add a channel dimension or use bss_eval_sources_framewise
    ref_sources = ref_sources[:, :, np.newaxis]
    est_sources = est_sources[:, :, np.newaxis]

# Check for silent sources to prevent ValueError
if not np.any(ref_sources) or not np.any(est_sources):
    raise ValueError("Sources cannot be completely silent.")

sdr, isr, sir, sar, perm = mir_eval.separation.bss_eval_images_framewise(
    ref_sources, est_sources, window=30*44100, hop=15*44100
)
```

## API Test: `bss_eval_sources`

### Signature
```python
def bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)
```
_Source: source/mir_eval/separation.py:149_

_Source doc:_ Ordering and measurement of the separation quality for estimated source signals in terms of filtered true source, interference and artifacts. The decomposition allows a time-invariant filter distortion of length 512, as described in Section III.B of [#vincent2006performance]_. Passing ``False`` for ``compute_permutation`` will improve the computation performance of the evaluation; however, it is not always appropriate and is not the way that the BSS_EVAL Matlab toolbox computes bss_eval_sources. Examples -------- >>> # reference_sources[n] should be an ndarray of samples of the >>> # n'th reference source >>> # estimated_sources[n] should be the same for the n'th estimated >>> # source >>> (sdr, sir, sar, ...  perm) = mir_eval.separation.bss_eval_sources(reference_sources, ...                                               estimated_sources) Parameters ---------- reference_sources : np.ndarray, shape=(nsrc, nsampl) matrix containing true sources (must have same shape as estimated_sources) estimated_sources : np.ndarray, shape=(nsrc, nsampl) matrix containing estimated sources (must have same shape as reference_sources) compute_permutation : bool, optional compute permutation of estimate/source combinations (True by default) Returns ------- sdr : np.ndarray, shape=(nsrc,) vector of Signal to Distortion Ratios (SDR) sir : np.ndarray, shape=(nsrc,) vector of Source to Interference Ratios (SIR) sar : np.ndarray, shape=(nsrc,) vector of Sources to Artifacts Ratios (SAR) perm : np.ndarray, shape=(nsrc,) vector containing the best ordering of estimated sources in the mean SIR sense (estimated source number ``perm[j]`` corresponds to true source number ``j``). Note: ``perm`` will be ``[0, 1, ..., nsrc-1]`` if ``compute_permutation`` is ``False``. References ---------- .. [#] Emmanuel Vincent, Shoko Araki, Fabian J. Theis, Guido Nolte, Pau Bofill, Hiroshi Sawada, Alexey Ozerov, B. Vikrham Gowreesunker, Dominik Lutter and Ngoc Q.K. Duong, "The Signal Separation Evaluation Campaign (2007-2010): Achievements and remaining challenges", Signal Processing, 92, pp. 1928-1936, 2012.

### Goal
Computes the Signal to Distortion Ratio (SDR), Source to Interference Ratio (SIR), and Sources to Artifacts Ratio (SAR) to evaluate the quality of estimated audio source separation against reference sources.

### Parameters
- `reference_sources`: `np.ndarray` of shape `(nsrc, nsampl)`. A 2D matrix containing the true reference source signals. Must have the exact same shape as `estimated_sources`.
- `estimated_sources`: `np.ndarray` of shape `(nsrc, nsampl)`. A 2D matrix containing the estimated source signals. Must have the exact same shape as `reference_sources`.
- `compute_permutation`, default `True`: `bool`. If `True`, computes the best permutation of estimate/source combinations. Passing `False` improves computation performance but deviates from the standard BSS_EVAL Matlab toolbox behavior.

### Input
Both inputs must be 2D numpy arrays of shape `(n_sources, n_samples)` representing the audio signals. They must have identical shapes. Neither array can contain a completely silent (all-zero) source row, as this violates the metric's mathematical preconditions. *Note: The `mir_eval.separation` module is deprecated.*

### Output
Returns `unspecified` — A tuple of four 1D `np.ndarray` objects, each of shape `(nsrc,)`:
1. `sdr`: Vector of Signal to Distortion Ratios.
2. `sir`: Vector of Source to Interference Ratios.
3. `sar`: Vector of Sources to Artifacts Ratios.
4. `perm`: Vector containing the best ordering of estimated sources in the mean SIR sense (estimated source number `perm[j]` corresponds to true source number `j`). If `compute_permutation` is `False`, this will simply be `[0, 1, ..., nsrc-1]`.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example with 2 sources, 100 samples each
reference_sources = np.random.random_sample((2, 100))
estimated_sources = np.random.random_sample((2, 100))

(sdr, sir, sar, perm) = mir_eval.separation.bss_eval_sources(
    reference_sources, 
    estimated_sources
)
```

### LLM Instruction Prompt
- Ensure `reference_sources` and `estimated_sources` are 2D numpy arrays of shape `(n_sources, n_samples)`.
- Verify that both arrays have the exact same shape before calling.
- Check that no individual source (row) in either array is completely silent (all zeros), as this will raise a `ValueError`.
- Be aware that the `mir_eval.separation` module is deprecated.

### Prompt Snippet
```text
When evaluating source separation with `mir_eval.separation.bss_eval_sources`, ensure both inputs are 2D numpy arrays of shape `(n_sources, n_samples)` and have identical shapes. You must verify that no source row is completely silent (all zeros) to avoid a `ValueError`. The function returns a tuple of four arrays: `(sdr, sir, sar, perm)`.
```

### Common Failure Modes
- **Silent Sources**: Passing a matrix where one or more sources (rows) are completely silent (all zeros) will raise a `ValueError`.
- **Shape Mismatch**: Passing `reference_sources` and `estimated_sources` with different shapes (e.g., different number of sources or different lengths) will raise a `ValueError`.
- **Empty Inputs**: Passing empty arrays (e.g., `np.array([])`) will trigger a `UserWarning` ("reference_sources is empty" / "estimated_sources is empty") and return empty arrays.

### Fix Code Hint
```python
# FIX: Ensure inputs are 2D, have the same shape, and contain no all-zero rows
if reference_sources.shape != estimated_sources.shape:
    raise ValueError("Reference and estimated sources must have the same shape.")

if np.any(np.all(reference_sources == 0, axis=1)) or np.any(np.all(estimated_sources == 0, axis=1)):
    raise ValueError("Cannot evaluate separation: one or more sources are completely silent.")

sdr, sir, sar, perm = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources)
```

## API Test: `bss_eval_sources_framewise`

### Signature
```python
def bss_eval_sources_framewise(reference_sources, estimated_sources, window=30 * 44100, hop=15 * 44100, compute_permutation=False)
```
_Source: source/mir_eval/separation.py:260_

_Source doc:_ Framewise computation of bss_eval_sources Please be aware that this function does not compute permutations (by default) on the possible relations between reference_sources and estimated_sources due to the dangers of a changing permutation. Therefore (by default), it assumes that ``reference_sources[i]`` corresponds to ``estimated_sources[i]``. To enable computing permutations please set ``compute_permutation`` to be ``True`` and check that the returned ``perm`` is identical for all windows. NOTE: if ``reference_sources`` and ``estimated_sources`` would be evaluated using only a single window or are shorter than the window length, the result of :func:`mir_eval.separation.bss_eval_sources` called on ``reference_sources`` and ``estimated_sources`` (with the ``compute_permutation`` parameter passed to :func:`mir_eval.separation.bss_eval_sources`) is returned. Examples -------- >>> # reference_sources[n] should be an ndarray of samples of the >>> # n'th reference source >>> # estimated_sources[n] should be the same for the n'th estimated >>> # source >>> (sdr, sir, sar, ...  perm) = mir_eval.separation.bss_eval_sources_framewise( reference_sources, ...      estimated_sources) Parameters ---------- reference_sources : np.ndarray, shape=(nsrc, nsampl) matrix containing true sources (must have the same shape as ``estimated_sources``) estimated_sources : np.ndarray, shape=(nsrc, nsampl) matrix containing estimated sources (must have the same shape as ``reference_sources``) window : int, optional Window length for framewise evaluation (default value is 30s at a sample rate of 44.1kHz) hop : int, optional Hop size for framewise evaluation (default value is 15s at a sample rate of 44.1kHz) compute_permutation : bool, optional compute permutation of estimate/source combinations for all windows (False by default) Returns ------- sdr : np.ndarray, shape=(nsrc, nframes) vector of Signal to Distortion Ratios (SDR) sir : np.ndarray, shape=(nsrc, nframes) vector of Source to Interference Ratios (SIR) sar : np.ndarray, shape=(nsrc, nframes) vector of Sources to Artifacts Ratios (SAR) perm : np.ndarray, shape=(nsrc, nframes) vector containing the best ordering of estimated sources in the mean SIR sense (estimated source number ``perm[j]`` corresponds to true source number ``j``).  Note: ``perm`` will be ``range(nsrc)`` for all windows if ``compute_permutation`` is ``False``

### Goal
Computes the framewise Blind Source Separation (BSS) evaluation metrics (SDR, SIR, SAR, and permutation) over sliding windows of the input audio sources.

### Parameters
- `reference_sources`: `np.ndarray` of shape `(nsrc, nsampl)` containing the true audio sources. Must have the exact same shape as `estimated_sources`.
- `estimated_sources`: `np.ndarray` of shape `(nsrc, nsampl)` containing the estimated audio sources. Must have the exact same shape as `reference_sources`.
- `window`, default `30 * 44100`: `int`, the window length in samples for the framewise evaluation (default is 30 seconds at a 44.1kHz sample rate).
- `hop`, default `15 * 44100`: `int`, the hop size in samples for the framewise evaluation (default is 15 seconds at a 44.1kHz sample rate).
- `compute_permutation`, default `False`: `bool`, whether to compute the optimal permutation of estimate/source combinations for all windows.

### Input
- Both `reference_sources` and `estimated_sources` must be 2-dimensional numpy arrays of shape `(nsrc, nsampl)`.
- The arrays must not contain completely silent sources (i.e., a source row consisting entirely of zeros), as this will raise a `ValueError`.
- **Deprecation Warning:** The `mir_eval.separation` module is deprecated.
- If the input arrays are shorter than the window length, the function falls back to computing the non-framewise `mir_eval.separation.bss_eval_sources`.

### Output
Returns `unspecified` — A tuple of four `np.ndarray` objects, each of shape `(nsrc, nframes)`:
1. `sdr`: Signal to Distortion Ratios (SDR).
2. `sir`: Source to Interference Ratios (SIR).
3. `sar`: Sources to Artifacts Ratios (SAR).
4. `perm`: The best ordering of estimated sources in the mean SIR sense. If `compute_permutation` is `False`, this will simply be `range(nsrc)` for all windows.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example 1: Using default window and hop sizes
ref_sources = np.random.random_sample((2, 44100 * 60))
est_sources = np.random.random_sample((2, 44100 * 60))
(sdr, sir, sar, perm) = mir_eval.separation.bss_eval_sources_framewise(
    ref_sources, 
    est_sources
)

# Example 2: Specifying custom window and hop sizes (from test suite)
ref_sources_short = np.random.random_sample((2, 100))
est_sources_short = np.random.random_sample((2, 100))
(sdr, sir, sar, perm) = mir_eval.separation.bss_eval_sources_framewise(
    ref_sources_short, 
    est_sources_short, 
    40, 
    20
)
```

### LLM Instruction Prompt
- Ensure `reference_sources` and `estimated_sources` are numpy arrays with the exact same shape `(nsrc, nsampl)`.
- Do not pass completely silent sources (arrays of all zeros) to this function, as it will raise a `ValueError`.
- Be aware that `mir_eval.separation` is deprecated.
- By default, permutations are not computed (`compute_permutation=False`). If you set `compute_permutation=True`, you must verify that the returned `perm` array is identical across all windows to avoid the dangers of a changing permutation.

### Prompt Snippet
```text
Evaluate the source separation framewise using `mir_eval.separation.bss_eval_sources_framewise`. Ensure the reference and estimated source arrays have identical shapes and do not contain any completely silent tracks. Use a window of 40 samples and a hop of 20 samples.
```

### Common Failure Modes
- **`ValueError`**: Raised if `reference_sources` and `estimated_sources` have mismatched shapes (e.g., `ref_sources[:2]` vs `est_sources[1:]`).
- **`ValueError`**: Raised if any of the sources in the reference or estimated arrays are completely silent (e.g., `np.zeros(100)`).
- **`UserWarning`**: Raised if the input arrays are empty (`np.array([])`), which will also cause the metric to return empty arrays.

### Fix Code Hint
```python
# Ensure shapes match exactly
if reference_sources.shape != estimated_sources.shape:
    raise ValueError("Reference and estimated sources must have the same shape.")

# Ensure no source is completely silent
if np.any(np.all(reference_sources == 0, axis=1)) or np.any(np.all(estimated_sources == 0, axis=1)):
    raise ValueError("Input sources cannot be completely silent.")

sdr, sir, sar, perm = mir_eval.separation.bss_eval_sources_framewise(
    reference_sources, 
    estimated_sources, 
    window=40, 
    hop=20
)
```

## API Test: `cemgil`

### Signature
```python
def cemgil(reference_beats, estimated_beats, cemgil_sigma=0.04)
```
_Source: source/mir_eval/beat.py:176_

_Source doc:_ Cemgil's score, computes a gaussian error of each estimated beat. Compares against the original beat times and all metrical variations. Examples -------- >>> reference_beats = mir_eval.io.load_events('reference.txt') >>> reference_beats = mir_eval.beat.trim_beats(reference_beats) >>> estimated_beats = mir_eval.io.load_events('estimated.txt') >>> estimated_beats = mir_eval.beat.trim_beats(estimated_beats) >>> cemgil_score, cemgil_max = mir_eval.beat.cemgil(reference_beats, estimated_beats) Parameters ---------- reference_beats : np.ndarray reference beat times, in seconds estimated_beats : np.ndarray query beat times, in seconds cemgil_sigma : float Sigma parameter of gaussian error windows (Default value = 0.04) Returns ------- cemgil_score : float Cemgil's score for the original reference beats cemgil_max : float The best Cemgil score for all metrical variations

### Goal
Computes Cemgil's score for beat tracking evaluation by calculating a Gaussian error for each estimated beat against the original reference beat times and all metrical variations.

### Parameters
- `reference_beats`: `np.ndarray` representing the ground truth reference beat times, in seconds.
- `estimated_beats`: `np.ndarray` representing the estimated (query) beat times, in seconds.
- `cemgil_sigma`, default `0.04`: `float` representing the sigma parameter of the Gaussian error windows.

### Input
1D numpy arrays containing beat timestamps in seconds. In standard MIR evaluation workflows, these are typically loaded from repository-format text files using `mir_eval.io.load_events` and must be preprocessed using `mir_eval.beat.trim_beats` to remove early events (e.g., before 5 seconds) prior to evaluation.

### Output
Returns `unspecified` — A tuple of two `float` values: `(cemgil_score, cemgil_max)`. `cemgil_score` is Cemgil's score for the original reference beats, and `cemgil_max` is the best Cemgil score across all metrical variations.

### Valid Call Patterns
```python
# Inferred from source documentation
import mir_eval

reference_beats = mir_eval.io.load_events('reference.txt')
reference_beats = mir_eval.beat.trim_beats(reference_beats)

estimated_beats = mir_eval.io.load_events('estimated.txt')
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)

cemgil_score, cemgil_max = mir_eval.beat.cemgil(reference_beats, estimated_beats)
```

### LLM Instruction Prompt
- When evaluating beat tracking using `mir_eval.beat.cemgil`, ensure inputs are 1D numpy arrays of timestamps in seconds. Always preprocess the beat arrays with `mir_eval.beat.trim_beats` before evaluation to adhere to standard MIR practices. Expect a tuple of two floats `(cemgil_score, cemgil_max)` in return, and unpack them accordingly.

### Prompt Snippet
```text
Use `mir_eval.beat.cemgil(reference_beats, estimated_beats)` to compute Cemgil's score. Inputs must be 1D numpy arrays of beat times in seconds. Preprocess inputs with `mir_eval.beat.trim_beats` first. It returns a tuple: `(cemgil_score, cemgil_max)`.
```

### Common Failure Modes
- Failing to trim early beats (e.g., the first 5 seconds), which violates standard MIR evaluation preconditions and skews the resulting score.
- Passing multi-dimensional arrays or non-numeric data instead of 1D numpy arrays of timestamps in seconds.
- Unpacking only a single value from the function, resulting in a `ValueError`, as it strictly returns a tuple of two floats.

### Fix Code Hint
```python
# Ensure beats are loaded as 1D arrays and trimmed before calling cemgil
ref_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('ref.txt'))
est_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('est.txt'))

# Unpack both the score and the max score for metrical variations
cemgil_score, cemgil_max = mir_eval.beat.cemgil(ref_beats, est_beats)
```

## API Test: `chords`

### Signature
```python
def chords(chord_labels, intervals, fs, **kwargs)
def chords(intervals, labels, base=None, height=None, text=False, text_kw=None, ax=None, cmap='fifths', pattern=True, **kwargs)
```
_Source: source/mir_eval/display.py:1160  (+1 more definition site/overload)_

_Source doc:_ Plot a chord annotation as a set of disjoint rectangles with semantically meaningful colors. Parameters ---------- intervals : np.ndarray, shape=(n, 2) segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. labels : list, shape=(n,) reference chord labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. base : number The vertical position of the base of the rectangles. By default, this will be the bottom of the plot. height : number The height of the rectangles. By default, this will be the top of the plot (minus ``base``). .. note:: If either `base` or `height` are provided, both must be provided. text : bool If true, each segment's label is displayed in its upper-left corner text_kw : dict If ``text == True``, the properties of the text object can be specified here. See ``matplotlib.pyplot.Text`` for valid parameters ax : matplotlib.pyplot.axes An axis handle on which to draw the segmentation. If none is provided, a new set of axes is created. cmap : {'pitch', 'fifths'} The color map to use for the chord display. If 'pitch', the colors will cycle chromatically (C, C#, D, ...) If 'fifths', the colors will cycle through the circle of fifths (C, G, D, ...). In both cases, major qualities (identified by a natural third) and suspended chords (sus2, sus4) will receive a bright color, and minor qualities (identified by a flat third) will receive a darker color. Other Qualities which are neither major nor minor will receive a light color. No-chord ('N') or out-of-gamut ('X') symbols will be colored gray. pattern : bool If `True`, segments will be filled with a hatch pattern corresponding to the chord quality as described below: - Major: no hatch - Minor: no hatch - Suspended 2nd: horizontal hatch - Suspended 4th: vertical hatch - Augmented: cross hatch - Diminished: dot hatch - Major 7th: forward slash hatch - Minor Major 7th: forward slash hatch - Dominant 7th: backward slash hatch - Minor 7th: backward slash hatch - Half-diminished 7th: dot and forward slash hatch - Diminished 7th: dot and backward slash hatch - Major 6th: cross hatch - Minor 6th: cross hatch **kwargs Additional keyword arguments to pass to ``matplotlib.axes.Axes.axvspan``. Returns -------

### Goal
`chords` provides two distinct functionalities depending on the submodule: `mir_eval.display.chords` plots a chord annotation as a set of disjoint rectangles with semantically meaningful colors and hatch patterns, while `mir_eval.sonify.chords` synthesizes chord annotations into an audio signal for evaluation by ear.

### Parameters
- `intervals`: `np.ndarray`, shape=(n, 2). Segment intervals in seconds, typically returned by `mir_eval.io.load_labeled_intervals`. (Note: For `sonify.chords`, this is the second positional argument).
- `labels`: `list`, shape=(n,). Reference chord labels corresponding to the intervals. (Note: For `sonify.chords`, this is the first positional argument `chord_labels`).
- `base`, default `None`: `number`. The vertical position of the base of the rectangles. By default, the bottom of the plot.
- `height`, default `None`: `number`. The height of the rectangles. By default, the top of the plot (minus `base`).
- `text`, default `False`: `bool`. If True, each segment's label is displayed in its upper-left corner.
- `text_kw`, default `None`: `dict`. Properties for the text object if `text == True` (passed to `matplotlib.pyplot.Text`).
- `ax`, default `None`: `matplotlib.pyplot.axes`. An axis handle on which to draw the segmentation. If None, a new set of axes is created.
- `cmap`, default `'fifths'`: `str`. The color map to use for the chord display. 'pitch' cycles chromatically, 'fifths' cycles through the circle of fifths.
- `pattern`, default `True`: `bool`. If True, segments are filled with a hatch pattern corresponding to the chord quality (e.g., major, minor, suspended).
- `**kwargs`: Additional keyword arguments. For `display.chords`, passed to `matplotlib.axes.Axes.axvspan`. For `sonify.chords`, passed directly through to `mir_eval.sonify.time_frequency` (e.g., `length` in samples).

### Input
- **For `display.chords`**: `intervals` (n, 2) numpy array of start/end times in seconds, and `labels` list of string chord labels (e.g., "C:maj", "N", "X"). If `base` or `height` is provided, both must be provided.
- **For `sonify.chords`**: `chord_labels` (list of strings), `intervals` (n, 2) numpy array, and `fs` (int) sampling rate.
- Chord labels must follow standard syntax (e.g., "C:maj", "D:min7", "N" for no-chord, "X" for out-of-gamut). Validation uses regular expressions and restricts invalid chord types from `chord.QUALITIES`.

### Output
Returns `unspecified` — For `display.chords`, it modifies the matplotlib axes in place and returns nothing (or unspecified artists). For `sonify.chords`, it returns a 1D numpy array representing the synthesized audio signal.

### Valid Call Patterns
```python
import mir_eval
import matplotlib.pyplot as plt
import numpy as np

intervals = np.array([[0.0, 2.0], [2.0, 4.0]])
labels = ["C:maj", "G:maj"]

# 1. Display chords (intervals first)
fig, ax = plt.subplots()
mir_eval.display.chords(intervals, labels, ax=ax, cmap="fifths", pattern=True)

# 2. Sonify chords (labels first)
fs = 44100
signal = mir_eval.sonify.chords(labels, intervals, fs, length=fs * 5)
```

### LLM Instruction Prompt
- Differentiate between `mir_eval.display.chords` and `mir_eval.sonify.chords`.
- For `display.chords`, pass `intervals` first, then `labels`. If specifying `base` or `height`, both must be provided. Keep display tests headless.
- For `sonify.chords`, pass `chord_labels` first, then `intervals`, then `fs`.
- Ensure chord labels are valid strings (e.g., "C:maj", "N").
- `sonify.chords` passes `**kwargs` to `time_frequency`, so `length` can be specified in samples.

### Prompt Snippet
```text
`mir_eval.display.chords(intervals, labels, ...)` plots chord annotations. `mir_eval.sonify.chords(chord_labels, intervals, fs, **kwargs)` synthesizes them into audio. Note the argument order difference: display takes intervals first, sonify takes labels first. For display, if `base` or `height` are provided, both must be provided.
```

### Common Failure Modes
- **Argument Order Mismatch**: Passing `intervals` first to `sonify.chords` or `labels` first to `display.chords`.
- **Missing Base/Height Pair**: Providing `base` without `height` (or vice versa) in `display.chords` raises an error.
- **Invalid Chord Labels**: Using invalid chord qualities that are not in `mir_eval.chord.QUALITIES` or failing regular expression validation.
- **GUI Errors in CI**: Running display functions in environments without a headless matplotlib backend configured, causing GUI errors.

### Fix Code Hint
```python
# FIX: Ensure both base and height are provided together for display
mir_eval.display.chords(intervals, labels, base=0, height=1)

# FIX: Note the argument order difference for sonify (labels first)
signal = mir_eval.sonify.chords(labels, intervals, fs=44100)
```

## API Test: `chroma`

### Signature
```python
def chroma(chromagram, times, fs, **kwargs)
```
_Source: source/mir_eval/sonify.py:320_

_Source doc:_ Reverse synthesis of a chromagram (semitone matrix) Parameters ---------- chromagram : np.ndarray, shape=(12, times.shape[0]) Chromagram matrix, where each row represents a semitone [C->Bb] i.e., ``chromagram[3, j]`` is the magnitude of D# from ``times[j]`` to ``times[j + 1]`` times : np.ndarray, shape=(len(chord_labels),) or (len(chord_labels), 2) Either the start time of each column in the chromagram, or the time interval corresponding to each column. fs : int Sampling rate to synthesize audio data at **kwargs Additional keyword arguments to pass to :func:`mir_eval.sonify.time_frequency` Returns ------- output : np.ndarray Synthesized chromagram

### Goal
Performs reverse synthesis of a chromagram (semitone matrix) into an audio signal for "evaluation by ear".

### Parameters
- `chromagram`: A 2D `np.ndarray` of shape `(12, times.shape[0])` representing the chromagram matrix, where each row corresponds to a semitone from C to Bb.
- `times`: A 1D or 2D `np.ndarray` of shape `(N,)` or `(N, 2)` representing either the start time of each column in the chromagram, or the time interval corresponding to each column.
- `fs`: An `int` specifying the sampling rate at which to synthesize the audio data.
- `**kwargs`: Additional keyword arguments (such as `length`) that are passed directly through to `mir_eval.sonify.time_frequency`.

### Input
The caller must provide a 12-row numpy array for the `chromagram` and a matching numpy array for `times` where the number of columns in `chromagram` equals the length of `times`. Because `chroma` delegates to `mir_eval.sonify.time_frequency`, any negative amplitudes in the `chromagram` will not be sonified. 

### Output
Returns `unspecified` — A 1D `np.ndarray` containing the synthesized audio signal.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

fs = 44100
# 12 rows for semitones, 1000 time steps
chromagram = np.random.standard_normal((12, 1000))
times = np.linspace(0, 10, 1000)

# Basic reverse synthesis
signal = mir_eval.sonify.chroma(chromagram, times, fs)

# Passing kwargs through to time_frequency (e.g., specifying exact output length)
signal_padded = mir_eval.sonify.chroma(
    chromagram, 
    times, 
    fs, 
    length=fs * 11
)
```

### LLM Instruction Prompt
- Ensure `chromagram` is a 2D numpy array with exactly 12 rows.
- Ensure the second dimension of `chromagram` matches the first dimension of `times`.
- Remember that `**kwargs` are passed directly to `mir_eval.sonify.time_frequency`. You can use this to pass parameters like `length`.
- Do not attempt to sonify negative amplitudes, as the underlying `time_frequency` function ignores them. Ensure chromagram magnitudes are non-negative for accurate sonification.
- Do not include code that attempts to play the audio through an audio device; output the array only.

### Prompt Snippet
```text
When calling `mir_eval.sonify.chroma(chromagram, times, fs, **kwargs)`, ensure `chromagram` has shape `(12, len(times))`. Pass non-negative magnitudes, as the underlying `time_frequency` function does not sonify negative amplitudes. You can pass `length` via `**kwargs` to control the exact sample length of the output array.
```

### Common Failure Modes
- **Shape Mismatch**: Providing a `chromagram` where `chromagram.shape[1] != times.shape[0]`, causing alignment errors during synthesis.
- **Invalid Chromagram Dimensions**: Providing a `chromagram` with a number of rows other than 12.
- **Silent Output for Negative Values**: Passing a chromagram with negative magnitudes and expecting them to be sonified (they are ignored by the underlying `time_frequency` function).
- **Audio Device Access**: Attempting to play the returned array using an audio library in a headless/restricted environment.

### Fix Code Hint
```python
# Ensure chromagram has 12 rows and matches the length of times
if chromagram.shape[0] != 12:
    raise ValueError("Chromagram must have exactly 12 rows.")
if chromagram.shape[1] != len(times):
    raise ValueError("Chromagram columns must match the length of times.")

# Ensure non-negative magnitudes for proper sonification
chromagram_positive = np.maximum(0, chromagram)

signal = mir_eval.sonify.chroma(chromagram_positive, times, fs)
```

## API Test: `clicks`

### Signature
```python
def clicks(times, fs, click=None, length=None)
```
_Source: source/mir_eval/sonify.py:15_

_Source doc:_ Return a signal with the signal 'click' placed at each specified time Parameters ---------- times : np.ndarray times to place clicks, in seconds fs : int desired sampling rate of the output signal click : np.ndarray click signal, defaults to a 1 kHz blip length : int desired number of samples in the output signal, defaults to ``times.max()*fs + click.shape[0] + 1`` Returns ------- click_signal : np.ndarray Synthesized click signal

### Goal
Synthesize an audio signal containing a short click or blip at specified time locations, useful for sonifying events like beats or onsets for auditory evaluation.

### Parameters
- `times`: `np.ndarray` of times to place clicks, measured in seconds.
- `fs`: `int` representing the desired sampling rate of the output audio signal.
- `click`, default `None`: `np.ndarray` representing the custom click signal waveform to place at each time; if `None`, defaults to a 1 kHz blip.
- `length`, default `None`: `int` representing the desired total number of samples in the output signal; if `None`, it is inferred as `times.max() * fs + click.shape[0] + 1` and cast to an integer.

### Input
The caller must provide `times` as a 1D numpy array of timestamps in seconds (not sample indices). `fs` must be an integer representing the sampling frequency. If a custom `click` is provided, it must be a 1D numpy array of audio samples. If `length` is explicitly provided, it should be an integer. 

### Output
Returns `unspecified` — A 1D `np.ndarray` representing the synthesized audio signal with clicks placed at the requested timestamps.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Assume `times` is a numpy array of event times in seconds and `fs` is an integer (e.g., 44100)
# 1. Basic usage with default 1 kHz blip and inferred length
click_signal = mir_eval.sonify.clicks(times, fs)

# 2. Specifying an exact output length in samples
click_signal = mir_eval.sonify.clicks(times, fs, length=1000)

# 3. Providing a custom click signal (e.g., an array of zeros or a custom waveform)
custom_click = np.zeros(1000)
click_signal = mir_eval.sonify.clicks(times, fs, click=custom_click)
```

### LLM Instruction Prompt
- When sonifying events (like beats or onsets) for evaluation by ear, use `mir_eval.sonify.clicks(times, fs)`.
- Ensure `times` is provided in seconds, not sample indices.
- Do not attempt to play the audio directly using audio-device access in test environments; only generate the `np.ndarray` in memory.
- Remember that `mir_eval.sonify.clicks` automatically casts its inferred length to an integer, but if you pass `length` explicitly, ensure it is an integer.

### Prompt Snippet
```text
`mir_eval.sonify.clicks(times, fs, click=None, length=None)` synthesizes an audio array with a click at each time in `times` (in seconds). `fs` is the integer sample rate. `click` defaults to a 1 kHz blip. The inferred length is cast to an integer automatically. Returns a 1D `np.ndarray`.
```

### Common Failure Modes
- Passing sample indices instead of seconds for the `times` array, resulting in an output array that is massively oversized and causes memory errors.
- Passing a floating-point value for `length`, which may cause indexing or array-creation type errors.
- Attempting to sonify negative amplitudes or invalid time values (e.g., `NaN`s) without filtering them first.

### Fix Code Hint
```python
# BAD: Passing sample indices instead of seconds
# click_signal = mir_eval.sonify.clicks(sample_indices, fs=44100)

# GOOD: Convert sample indices to seconds before calling clicks
times_in_seconds = sample_indices / 44100.0
click_signal = mir_eval.sonify.clicks(times_in_seconds, fs=44100)

# GOOD: Explicitly casting length to integer if derived from a float calculation
total_duration_sec = 5.5
click_signal = mir_eval.sonify.clicks(times_in_seconds, fs=44100, length=int(total_duration_sec * 44100))
```

## API Test: `compute_accuracy`

### Signature
```python
def compute_accuracy(true_positives, n_ref, n_est)
```
_Source: source/mir_eval/multipitch.py:248_

_Source doc:_ Compute accuracy metrics. Parameters ---------- true_positives : np.ndarray Array containing the number of true positives at each time point. n_ref : np.ndarray Array containing the number of reference frequencies at each time point. n_est : np.ndarray Array containing the number of estimate frequencies at each time point. Returns ------- precision : float ``sum(true_positives)/sum(n_est)`` recall : float ``sum(true_positives)/sum(n_ref)`` acc : float ``sum(true_positives)/sum(n_est + n_ref - true_positives)``

### Goal
Compute precision, recall, and accuracy metrics for multipitch estimation based on frame-level counts of true positives, reference frequencies, and estimated frequencies.

### Parameters
- `true_positives`: A `np.ndarray` containing the number of correctly estimated pitches (true positives) at each time point/frame.
- `n_ref`: A `np.ndarray` containing the total number of ground-truth reference frequencies at each time point/frame.
- `n_est`: A `np.ndarray` containing the total number of estimated frequencies at each time point/frame.

### Input
Three 1-dimensional NumPy arrays of equal length representing frame-level integer counts. The arrays must be aligned such that the $i$-th element of each array corresponds to the same time point in the audio signal.

### Output
Returns `unspecified` — A tuple of three `float` values representing the evaluation metrics: `(precision, recall, accuracy)`. 
*   **Precision:** `sum(true_positives) / sum(n_est)`
*   **Recall:** `sum(true_positives) / sum(n_ref)`
*   **Accuracy:** `sum(true_positives) / sum(n_est + n_ref - true_positives)`

### Valid Call Patterns
```python
import numpy as np
import mir_eval

true_positives = np.array([1, 0, 0, 3, 2])
n_ref = np.array([2, 0, 1, 3, 2])
n_est = np.array([1, 0, 2, 3, 2])

(
    actual_precision,
    actual_recall,
    actual_accuracy,
) = mir_eval.multipitch.compute_accuracy(true_positives, n_ref, n_est)
```

### LLM Instruction Prompt
- When evaluating multipitch accuracy, call `mir_eval.multipitch.compute_accuracy(true_positives, n_ref, n_est)` using three equal-length 1D NumPy arrays containing the frame-wise counts. Unpack the returned tuple into three variables: precision, recall, and accuracy.

### Prompt Snippet
```text
Use `mir_eval.multipitch.compute_accuracy(true_positives, n_ref, n_est)` to calculate precision, recall, and accuracy from 1D NumPy arrays of frame-level counts. It returns a tuple of three floats: `(precision, recall, accuracy)`.
```

### Common Failure Modes
- Passing arrays of mismatched lengths, which violates the assumption that the counts correspond to aligned time points.
- Passing raw lists instead of `np.ndarray` objects, which may cause issues if the internal implementation relies on NumPy array operations.
- Passing arrays where `true_positives` exceeds `n_ref` or `n_est` at a given time point, which is mathematically invalid for these metrics.

### Fix Code Hint
```python
# Ensure all inputs are NumPy arrays of the exact same shape
true_positives = np.asarray(true_positives)
n_ref = np.asarray(n_ref)
n_est = np.asarray(n_est)

if not (true_positives.shape == n_ref.shape == n_est.shape):
    raise ValueError("All input arrays must have the same shape.")

precision, recall, accuracy = mir_eval.multipitch.compute_accuracy(
    true_positives, n_ref, n_est
)
```

## API Test: `compute_err_score`

### Signature
```python
def compute_err_score(true_positives, n_ref, n_est)
```
_Source: source/mir_eval/multipitch.py:296_

_Source doc:_ Compute error score metrics. Parameters ---------- true_positives : np.ndarray Array containing the number of true positives at each time point. n_ref : np.ndarray Array containing the number of reference frequencies at each time point. n_est : np.ndarray Array containing the number of estimate frequencies at each time point. Returns ------- e_sub : float Substitution error e_miss : float Miss error e_fa : float False alarm error e_tot : float Total error

### Goal
Compute substitution, miss, false alarm, and total error score metrics for multipitch estimation across evaluated time points.

### Parameters
- `true_positives`: `np.ndarray` — Array containing the number of true positives at each time point.
- `n_ref`: `np.ndarray` — Array containing the number of reference frequencies at each time point.
- `n_est`: `np.ndarray` — Array containing the number of estimate frequencies at each time point.

### Input
Three parallel, equal-length 1-dimensional `np.ndarray` objects containing non-negative numeric counts for each evaluated time frame. 

### Output
Returns `unspecified` — A tuple of four `float` values: `(e_sub, e_miss, e_fa, e_tot)`, representing the Substitution error, Miss error, False alarm error, and Total error, respectively.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

true_positives = np.array([1, 0, 0, 3, 2])
n_ref = np.array([2, 0, 1, 3, 2])
n_est = np.array([1, 0, 2, 3, 2])

(
    actual_esub,
    actual_emiss,
    actual_efa,
    actual_etot,
) = mir_eval.multipitch.compute_err_score(true_positives, n_ref, n_est)
```

### LLM Instruction Prompt
- When evaluating multipitch error scores, call `mir_eval.multipitch.compute_err_score(true_positives, n_ref, n_est)` using three equal-length 1D numpy arrays representing counts per time frame. Unpack the result into exactly four variables: substitution error, miss error, false alarm error, and total error.

### Prompt Snippet
```text
`mir_eval.multipitch.compute_err_score(true_positives, n_ref, n_est)` takes three equal-length 1D numpy arrays of counts and returns a tuple of 4 floats: `(e_sub, e_miss, e_fa, e_tot)`.
```

### Common Failure Modes
- Providing arrays of mismatched lengths, which will cause broadcasting or alignment errors during metric computation.
- Providing raw Python lists instead of `np.ndarray` objects, which may fail if the internal implementation relies on NumPy array operations (like vectorized arithmetic).
- Unpacking the return value into the wrong number of variables (it strictly returns 4 floats).

### Fix Code Hint
```python
# Ensure inputs are NumPy arrays of the exact same shape before calling
true_positives = np.asarray(true_positives)
n_ref = np.asarray(n_ref)
n_est = np.asarray(n_est)

assert true_positives.shape == n_ref.shape == n_est.shape, "Input arrays must have the same length."

e_sub, e_miss, e_fa, e_tot = mir_eval.multipitch.compute_err_score(true_positives, n_ref, n_est)
```

## API Test: `compute_num_freqs`

### Signature
```python
def compute_num_freqs(frequencies)
```
_Source: source/mir_eval/multipitch.py:190_

_Source doc:_ Compute the number of frequencies for each time point. Parameters ---------- frequencies : list of np.ndarray Frequency values Returns ------- num_freqs : np.ndarray Number of frequencies at each time point.

### Goal
Compute the count of active frequencies (pitch values) at each individual time frame for a multipitch estimation or reference sequence.

### Parameters
- `frequencies`: A list of 1D `np.ndarray` objects, where each array contains the frequency values (typically in Hz) present at a specific time point.

### Input
The caller must provide a Python `list` where each element corresponds to a single time frame. Because multipitch data has a variable number of pitches per frame, the elements must be 1D `numpy.ndarray` objects rather than a single dense 2D matrix. Frames with no active frequencies (unvoiced or silent frames) must be represented by empty numpy arrays (e.g., `np.array([])`).

### Output
Returns `unspecified` — A 1D `np.ndarray` of integers, where each integer represents the number of frequencies present at the corresponding time point in the input list.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Variable number of frequencies per time point, including an empty frame
frequencies = [
    np.array([256.0]),
    np.array([]),
    np.array([362.03867196751236, 128.0, 512.0]),
    np.array([300.0, 512.0]),
]

# Returns np.array([1, 0, 3, 2])
num_freqs = mir_eval.multipitch.compute_num_freqs(frequencies)
```

### LLM Instruction Prompt
- Call `mir_eval.multipitch.compute_num_freqs(frequencies)` to get an array of frequency counts per frame.
- Do NOT pass a 2D numpy array or a dense matrix; the input must be a Python `list` of 1D `np.ndarray` objects to accommodate the variable number of pitches per frame.
- Represent unvoiced/silent frames as empty numpy arrays (`np.array([])`), not as `None` or arrays containing `0.0` or `NaN`.

### Prompt Snippet
```text
mir_eval.multipitch.compute_num_freqs(frequencies) computes the number of active frequencies per time point. `frequencies` must be a list of 1D np.ndarray objects (one array per time frame). Unvoiced frames should be empty arrays. Returns a 1D np.ndarray of integer counts.
```

### Common Failure Modes
- **Passing a 2D numpy array**: Because the number of pitches varies per frame, multipitch data cannot be natively represented as a rectangular 2D array without padding. Passing a padded 2D array will result in incorrect counts (padding values will be counted as frequencies).
- **Passing a list of lists**: The function expects a list of `np.ndarray` objects. Passing a list of standard Python lists may cause attribute errors if the internal implementation relies on numpy array properties.
- **Using `None` for empty frames**: Passing `None` instead of `np.array([])` for frames with zero frequencies will cause iteration or length-checking errors.

### Fix Code Hint
```python
# BAD: Passing a list of lists or containing None
# frequencies = [[256.0], None, [128.0, 512.0]]
# num_freqs = mir_eval.multipitch.compute_num_freqs(frequencies)

# GOOD: Convert to a list of numpy arrays, replacing None with empty arrays
import numpy as np
raw_frequencies = [[256.0], None, [128.0, 512.0]]
frequencies = [np.array(f) if f is not None else np.array([]) for f in raw_frequencies]
num_freqs = mir_eval.multipitch.compute_num_freqs(frequencies)
```

## API Test: `compute_num_true_positives`

### Signature
```python
def compute_num_true_positives(ref_freqs, est_freqs, window=0.5, chroma=False)
```
_Source: source/mir_eval/multipitch.py:206_

_Source doc:_ Compute the number of true positives in an estimate given a reference. A frequency is correct if it is within a quartertone of the correct frequency. Parameters ---------- ref_freqs : list of np.ndarray reference frequencies (MIDI) est_freqs : list of np.ndarray estimated frequencies (MIDI) window : float Window size, in semitones chroma : bool If True, computes distances modulo n. If True, ``ref_freqs`` and ``est_freqs`` should be wrapped modulo n. Returns ------- true_positives : np.ndarray Array the same length as ref_freqs containing the number of true positives.

### Goal
Compute the number of correctly estimated pitches (true positives) per frame for a multipitch estimation task, based on a specified semitone tolerance window.

### Parameters
- `ref_freqs`: A list of 1D `np.ndarray` objects containing the reference (ground truth) frequencies in the MIDI pitch scale for each frame.
- `est_freqs`: A list of 1D `np.ndarray` objects containing the estimated frequencies in the MIDI pitch scale for each frame.
- `window`, default `0.5`: A float representing the tolerance window size in semitones. The default of 0.5 corresponds to a quartertone.
- `chroma`, default `False`: A boolean flag. If `True`, distances are computed modulo 12 (pitch class). If `True`, the caller must ensure `ref_freqs` and `est_freqs` are already wrapped modulo 12.

### Input
The caller must provide two lists of equal length, where each element is a 1D numpy array representing the active pitches in a single time frame. 
**Preconditions:** 
1. Frequencies must be converted to the MIDI pitch scale before being passed to this function (not raw Hz).
2. If `chroma=True` is used, the caller is responsible for wrapping the input arrays modulo 12 prior to calling the function.
3. Empty frames should be represented by empty numpy arrays (`np.array([])`), not `None`.

### Output
Returns `unspecified` — A 1D `np.ndarray` of integers, with the exact same length as `ref_freqs`, where each element contains the count of true positive pitch matches for that specific frame.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Standard multipitch true positives (MIDI pitch scale)
ref_freqs = [
    np.array([96.0, 100.0]),
    np.array([]),
    np.array([102.0, 84.0, 108.0])
]
est_freqs = [
    np.array([96.0]),
    np.array([]),
    np.array([102.0, 84.0, 108.0])
]
tp_counts = mir_eval.multipitch.compute_num_true_positives(ref_freqs, est_freqs)

# Chroma (pitch class) true positives with pre-wrapped modulo 12 inputs
ref_freqs_chroma = [
    np.array([0.0, 1.5]),
    np.array([5.1, 6.0, 11.0])
]
est_freqs_chroma = [
    np.array([0.0]),
    np.array([5.1, 6.0, 11.0])
]
tp_chroma_counts = mir_eval.multipitch.compute_num_true_positives(
    ref_freqs_chroma, est_freqs_chroma, chroma=True
)
```

### LLM Instruction Prompt
- When evaluating multipitch true positives using `mir_eval.multipitch.compute_num_true_positives`, ensure inputs are lists of `np.ndarray` (not raw lists of lists) and that the values are in the MIDI pitch scale, not Hz.
- If evaluating chroma/pitch-class accuracy (`chroma=True`), you MUST pre-wrap the input arrays modulo 12 before passing them to the function.
- Represent silent/empty frames as `np.array([])`.

### Prompt Snippet
```text
Ensure that the multipitch arrays passed to `compute_num_true_positives` are converted to MIDI pitch scale. If `chroma=True` is specified, you must manually wrap the frequencies modulo 12 beforehand. Use `np.array([])` for frames with no active pitches.
```

### Common Failure Modes
- **Hz instead of MIDI**: Passing frequencies in Hertz. The function assumes the values are in semitones (MIDI pitch) to apply the default `0.5` semitone window.
- **Unwrapped Chroma Inputs**: Setting `chroma=True` but passing standard MIDI pitches (e.g., `60.0`). The function expects inputs to already be wrapped modulo 12 (e.g., `0.0` for C) when this flag is active.
- **Raw Python Lists**: Passing lists of lists (e.g., `[[60.0], []]`) instead of lists of numpy arrays. This will cause attribute errors when the function attempts numpy operations on the inner elements.
- **Mismatched Frame Counts**: Passing `ref_freqs` and `est_freqs` lists of different lengths.

### Fix Code Hint
```python
# FIX: Convert Hz to MIDI and ensure inner elements are numpy arrays
ref_midi = [mir_eval.util.hz_to_midi(np.array(f)) if len(f) else np.array([]) for f in ref_hz]
est_midi = [mir_eval.util.hz_to_midi(np.array(f)) if len(f) else np.array([]) for f in est_hz]

# FIX: If using chroma=True, wrap modulo 12
if use_chroma:
    ref_midi = [np.mod(f, 12) for f in ref_midi]
    est_midi = [np.mod(f, 12) for f in est_midi]

tp_counts = mir_eval.multipitch.compute_num_true_positives(
    ref_midi, est_midi, chroma=use_chroma
)
```

## API Test: `constant_hop_timebase`

### Signature
```python
def constant_hop_timebase(hop, end_time)
```
_Source: source/mir_eval/melody.py:195_

_Source doc:_ Generate a time series from 0 to ``end_time`` with times spaced ``hop`` apart Parameters ---------- hop : float Spacing of samples in the time series end_time : float Time series will span ``[0, end_time]`` Returns ------- times : np.ndarray Generated timebase

### Goal
Generate a uniformly spaced time series array starting from 0 up to a specified end time, typically used to establish a common time grid for resampling and evaluating melody contours.

### Parameters
- `hop`: float — Spacing of samples in the time series (the time step or hop size).
- `end_time`: float — The upper bound for the time series; the generated times will span `[0, end_time]`.

### Input
Two numeric values (floats). `hop` must be a strictly positive value to ensure valid spacing, and `end_time` must be a positive value representing the maximum time limit (e.g., the duration of the audio or annotation). 

### Output
Returns `unspecified` — A 1-dimensional `np.ndarray` of floats representing the generated timebase (e.g., `[0.0, hop, 2*hop, ...]`), stopping at or before `end_time`.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

hop = 0.1
end_time = 0.35
# Generates array([0.0, 0.1, 0.2, 0.3])
res_times = mir_eval.melody.constant_hop_timebase(hop, end_time)
```

### LLM Instruction Prompt
When generating a uniform time grid for melody evaluation or resampling in `mir_eval`, use `mir_eval.melody.constant_hop_timebase(hop, end_time)`. Do not invent a `start_time` parameter; the timebase always implicitly starts at 0. Ensure both arguments are floats and that `hop` is strictly positive.

### Prompt Snippet
```text
mir_eval.melody.constant_hop_timebase(hop: float, end_time: float) -> np.ndarray
Generates a 1D numpy array time series from 0 to `end_time` with times spaced `hop` apart. Used for standardizing time grids in MIR melody evaluation.
```

### Common Failure Modes
- Providing a negative or zero `hop` value, which makes timebase generation impossible and will cause underlying array-generation routines to fail.
- Providing an `end_time` less than 0, which will result in an empty array.
- Attempting to pass a `start_time` argument (the function strictly takes exactly two arguments and always starts at 0).

### Fix Code Hint
```python
# Ensure hop is strictly positive and end_time is valid before calling
if hop <= 0:
    raise ValueError("hop must be strictly positive")
if end_time < 0:
    end_time = 0.0

times = mir_eval.melody.constant_hop_timebase(hop, end_time)
```

## API Test: `continuity`

### Signature
```python
def continuity(reference_beats, estimated_beats, continuity_phase_threshold=0.175, continuity_period_threshold=0.175)
```
_Source: source/mir_eval/beat.py:409_

_Source doc:_ Get metrics based on how much of the estimated beat sequence is continually correct. Examples -------- >>> reference_beats = mir_eval.io.load_events('reference.txt') >>> reference_beats = mir_eval.beat.trim_beats(reference_beats) >>> estimated_beats = mir_eval.io.load_events('estimated.txt') >>> estimated_beats = mir_eval.beat.trim_beats(estimated_beats) >>> CMLc, CMLt, AMLc, AMLt = mir_eval.beat.continuity(reference_beats, estimated_beats) Parameters ---------- reference_beats : np.ndarray reference beat times, in seconds estimated_beats : np.ndarray query beat times, in seconds continuity_phase_threshold : float Allowable ratio of how far is the estimated beat can be from the reference beat (Default value = 0.175) continuity_period_threshold : float Allowable distance between the inter-beat-interval and the inter-annotation-interval (Default value = 0.175) Returns ------- CMLc : float Correct metric level, continuous accuracy CMLt : float Correct metric level, total accuracy (continuity not required) AMLc : float Any metric level, continuous accuracy AMLt : float Any metric level, total accuracy (continuity not required)

### Goal
Compute beat tracking continuity metrics (Correct Metric Level and Any Metric Level) based on how much of the estimated beat sequence is continually correct.

### Parameters
- `reference_beats`: `np.ndarray` — Reference (ground truth) beat times, in seconds.
- `estimated_beats`: `np.ndarray` — Estimated (query) beat times, in seconds.
- `continuity_phase_threshold`, default `0.175`: `float` — Allowable ratio of how far the estimated beat can be from the reference beat.
- `continuity_period_threshold`, default `0.175`: `float` — Allowable distance between the inter-beat-interval and the inter-annotation-interval.

### Input
1D numpy arrays of beat times in seconds. Typically, these are loaded from repository-format text files using `mir_eval.io.load_events`. As a standard preprocessing step in MIR evaluation, both reference and estimated beats should usually be trimmed (e.g., cropping out beats before 5 seconds) using `mir_eval.beat.trim_beats` before being passed to this function.

### Output
Returns `unspecified` — A tuple of four `float` values representing the continuity scores:
1. `CMLc`: Correct metric level, continuous accuracy.
2. `CMLt`: Correct metric level, total accuracy (continuity not required).
3. `AMLc`: Any metric level, continuous accuracy.
4. `AMLt`: Any metric level, total accuracy (continuity not required).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example 1: Standard usage with file loading and trimming
reference_beats = mir_eval.io.load_events('reference.txt')
reference_beats = mir_eval.beat.trim_beats(reference_beats)
estimated_beats = mir_eval.io.load_events('estimated.txt')
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)

CMLc, CMLt, AMLc, AMLt = mir_eval.beat.continuity(reference_beats, estimated_beats)

# Example 2: Direct usage with numpy arrays (edge case with few beats)
ref_array = np.array([6.0, 6.0])
est_array = np.array([6.0, 7.0])
cmlc, cmlt, amlc, amlt = mir_eval.beat.continuity(ref_array, est_array)
```

### LLM Instruction Prompt
- When evaluating beat tracking continuity, always pass 1D `np.ndarray` objects containing beat times in seconds.
- Remember to unpack the return value into exactly four variables: `CMLc, CMLt, AMLc, AMLt`.
- Apply `mir_eval.beat.trim_beats()` to both the reference and estimated beat arrays before calling `continuity` to ensure standard MIR evaluation preprocessing (cropping early events) is respected.
- Be aware that special-case logic exists for inputs with very few beats, which will deterministically return `0.0` for the metrics.

### Prompt Snippet
```text
`mir_eval.beat.continuity(reference_beats, estimated_beats, continuity_phase_threshold=0.175, continuity_period_threshold=0.175)`
Computes beat tracking continuity metrics. Expects 1D numpy arrays of beat times in seconds (typically preprocessed with `mir_eval.beat.trim_beats`). Returns a tuple of four floats: (CMLc, CMLt, AMLc, AMLt).
```

### Common Failure Modes
- **Missing Preprocessing:** Failing to trim early beats (e.g., the first 5 seconds) using `mir_eval.beat.trim_beats`, leading to scores that do not match standard MIR evaluation baselines.
- **Incorrect Unpacking:** Attempting to assign the result to a single variable or a dictionary (like the high-level `evaluate()` function returns) instead of unpacking the four specific float values.
- **Invalid Input Types:** Passing raw Python lists instead of `np.ndarray` objects, which may cause issues with underlying numpy vectorized operations.

### Fix Code Hint
```python
# Incorrect: Missing trimming and incorrect unpacking
# scores = mir_eval.beat.continuity(ref_list, est_list)

# Correct: Load, trim, and unpack 4 floats
import mir_eval
ref_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('ref.txt'))
est_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('est.txt'))
CMLc, CMLt, AMLc, AMLt = mir_eval.beat.continuity(ref_beats, est_beats)
```

## API Test: `deprecated`

### Signature
```python
def deprecated(*, version, version_removed)
```
_Source: source/mir_eval/util.py:946_

_Source doc:_ Mark a function as deprecated. Using the decorated (old) function will result in a warning.

### Goal
Mark a function as deprecated within the library, ensuring that any subsequent calls to the decorated function emit a warning to the user.

### Parameters
- `version`: The version string indicating when the function was first marked as deprecated.
- `version_removed`: The version string indicating the future release when the function is slated for removal (e.g., `"0.9"`, as is the case for the deprecated `mir_eval.io.load_wav`).

### Input
The function to be decorated. The decorator itself requires `version` and `version_removed` to be passed strictly as keyword arguments due to the `*` in the signature.

### Output
Returns `unspecified` — A wrapped callable (decorator) that executes the original function but triggers a deprecation warning first.

### Valid Call Patterns
```python
# Note: This example is inferred from the signature (not verified).
import mir_eval.util

@mir_eval.util.deprecated(version="0.8", version_removed="0.9")
def load_wav(path):
    # Legacy function implementation slated for removal
    pass
```

### LLM Instruction Prompt
- When deprecating legacy functions (such as old I/O routines or functions in the deprecated `mir_eval.separation` module), use the `@deprecated` decorator. You MUST pass `version` and `version_removed` as keyword arguments because the signature enforces keyword-only arguments via `*`.

### Prompt Snippet
```text
`mir_eval.util.deprecated(*, version, version_removed)` is a decorator to mark functions as deprecated. Both arguments are required and must be passed as keywords. Calling the decorated function will emit a warning.
```

### Common Failure Modes
- **Positional Arguments:** Passing `version` and `version_removed` as positional arguments. Because the signature is `(*, version, version_removed)`, positional arguments will raise a `TypeError`.
- **Missing Arguments:** Failing to provide either `version` or `version_removed`, both of which are required keyword arguments.

### Fix Code Hint
```python
# BAD: Positional arguments will raise a TypeError
@mir_eval.util.deprecated("0.8", "0.9")
def old_func():
    pass

# GOOD: Keyword arguments are required by the signature
@mir_eval.util.deprecated(version="0.8", version_removed="0.9")
def old_func():
    pass
```

## API Test: `detection`

### Signature
```python
def detection(reference_tempi, reference_weight, estimated_tempi, tol=0.08)
def detection(reference_intervals, estimated_intervals, window=0.5, beta=1.0, trim=False)
```
_Source: source/mir_eval/segment.py:168  (+1 more definition site/overload)_

_Source doc:_ Boundary detection hit-rate. A hit is counted whenever an reference boundary is within ``window`` of a estimated boundary.  Note that each boundary is matched at most once: this is achieved by computing the size of a maximal matching between reference and estimated boundary points, subject to the window constraint. Examples -------- >>> ref_intervals, _ = mir_eval.io.load_labeled_intervals('ref.lab') >>> est_intervals, _ = mir_eval.io.load_labeled_intervals('est.lab') >>> # With 0.5s windowing >>> P05, R05, F05 = mir_eval.segment.detection(ref_intervals, ...                                            est_intervals, ...                                            window=0.5) >>> # With 3s windowing >>> P3, R3, F3 = mir_eval.segment.detection(ref_intervals, ...                                         est_intervals, ...                                         window=3) >>> # Ignoring hits for the beginning and end of track >>> P, R, F = mir_eval.segment.detection(ref_intervals, ...                                      est_intervals, ...                                      window=0.5, ...                                      trim=True) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. window : float > 0 size of the window of 'correctness' around ground-truth beats (in seconds) (Default value = 0.5) beta : float > 0 weighting constant for F-measure. (Default value = 1.0) trim : boolean if ``True``, the first and last boundary times are ignored. Typically, these denote start (0) and end-markers. (Default value = False) Returns ------- precision : float precision of estimated predictions recall : float recall of reference reference boundaries f_measure : float F-measure (weighted harmonic mean of ``precision`` and ``recall``)

### Goal
Computes the boundary detection hit-rate (precision, recall, and F-measure) by finding a maximal matching between estimated and reference segment boundaries within a specified time window.

### Parameters
- `reference_intervals`: `np.ndarray`, shape `(n, 2)`. The ground-truth reference segment intervals (start and end times in seconds).
- `estimated_intervals`: `np.ndarray`, shape `(m, 2)`. The estimated segment intervals to be evaluated.
- `window`, default `0.5`: `float > 0`. The size of the tolerance window (in seconds) around ground-truth boundaries for an estimation to be considered a correct hit.
- `beta`, default `1.0`: `float > 0`. The weighting constant used when calculating the F-measure.
- `trim`, default `False`: `boolean`. If `True`, the first and last boundary times (typically the 0 start-marker and the end-marker) are ignored during evaluation.

### Input
The caller must provide two 2D numpy arrays of shape `(n, 2)` and `(m, 2)` representing time intervals. These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_intervals` or `mir_eval.io.load_labeled_intervals`. If either array is empty, the function will issue a `UserWarning` and return `0` for all metrics. 

*(Note: An overload exists for tempo evaluation at `mir_eval.tempo.detection(reference_tempi, reference_weight, estimated_tempi, tol=0.08)` which expects 1D arrays of tempi and a reference weight float).*

### Output
Returns `unspecified` — A tuple of three floats: `(precision, recall, f_measure)`. `precision` is the accuracy of the estimated predictions, `recall` is the hit-rate of the reference boundaries, and `f_measure` is their weighted harmonic mean.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Standard segment boundary detection (from test suite)
correct_intervals = np.array([[0, 1], [1, 2]])
precision, recall, f_measure = mir_eval.segment.detection(
    correct_intervals, 
    correct_intervals
)

# 2. Segment boundary detection with trimming and custom window
ref_intervals = np.array([[0.0, 1.5], [1.5, 3.0]])
est_intervals = np.array([[0.0, 1.4], [1.4, 3.0]])
p, r, f = mir_eval.segment.detection(
    ref_intervals,
    est_intervals,
    window=0.5,
    trim=True
)
```

### LLM Instruction Prompt
- When evaluating segment boundaries, use `mir_eval.segment.detection(reference_intervals, estimated_intervals)`. 
- Ensure the inputs are `(n, 2)` numpy arrays representing `[start, end]` times in seconds. 
- Unpack the return value into exactly three variables: `precision, recall, f_measure`.
- If you need to ignore the start and end markers of the track, pass `trim=True`.
- Be aware that passing empty interval arrays (e.g., `np.zeros((0, 2))`) is permitted but will trigger a `UserWarning` ("Reference/Estimated intervals are empty") and return `0` for all metrics.

### Prompt Snippet
```text
Evaluate the estimated segment boundaries against the reference boundaries using a 0.5-second window. Ignore the start and end markers. Return the precision, recall, and F-measure.
```

### Common Failure Modes
- **Empty Interval Arrays**: Passing `np.zeros((0, 2))` triggers a `UserWarning` (`"Reference intervals are empty"` or `"Estimated intervals are empty"`) and returns `0` or `NaN` depending on the exact inputs.
- **Incorrect Array Shape**: Passing 1D arrays of boundary timestamps instead of `(n, 2)` interval arrays. The function expects intervals, not raw boundary points.
- **Unpacking Errors**: Failing to unpack the returned tuple into three distinct variables (`precision, recall, f_measure`).

### Fix Code Hint
```python
# BAD: Passing 1D boundary arrays directly
# p, r, f = mir_eval.segment.detection(ref_boundaries, est_boundaries)

# GOOD: Convert boundaries to intervals first, then evaluate
ref_intervals = mir_eval.util.boundaries_to_intervals(ref_boundaries)
est_intervals = mir_eval.util.boundaries_to_intervals(est_boundaries)
precision, recall, f_measure = mir_eval.segment.detection(ref_intervals, est_intervals, trim=True)
```

## API Test: `deviation`

### Signature
```python
def deviation(reference_intervals, estimated_intervals, trim=False)
```
_Source: source/mir_eval/segment.py:252_

_Source doc:_ Compute the median deviations between reference and estimated boundary times. Examples -------- >>> ref_intervals, _ = mir_eval.io.load_labeled_intervals('ref.lab') >>> est_intervals, _ = mir_eval.io.load_labeled_intervals('est.lab') >>> r_to_e, e_to_r = mir_eval.boundary.deviation(ref_intervals, ...                                              est_intervals) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. trim : boolean if ``True``, the first and last intervals are ignored. Typically, these denote start (0.0) and end-of-track markers. (Default value = False) Returns ------- reference_to_estimated : float median time from each reference boundary to the closest estimated boundary estimated_to_reference : float median time from each estimated boundary to the closest reference boundary

### Goal
Compute the median time deviations from reference segment boundaries to the closest estimated boundaries, and vice versa, to evaluate segmentation accuracy.

### Parameters
- `reference_intervals`: A 2D `np.ndarray` of shape `(n, 2)` representing the ground-truth segment start and end times in seconds.
- `estimated_intervals`: A 2D `np.ndarray` of shape `(m, 2)` representing the predicted segment start and end times in seconds.
- `trim`, default `False`: A boolean flag. If `True`, the first and last interval boundaries (typically the 0.0 start marker and the end-of-track marker) are ignored during the deviation calculation.

### Input
The caller must provide two 2D numpy arrays of shape `(n, 2)` and `(m, 2)` containing time intervals. These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_intervals` or `mir_eval.io.load_labeled_intervals`. If you only have a 1D array of boundary events, they must be converted to intervals first (e.g., using `mir_eval.util.boundaries_to_intervals`).

### Output
Returns `unspecified` — A tuple of two `float` values: `(reference_to_estimated, estimated_to_reference)`. The first float is the median time from each reference boundary to the closest estimated boundary. The second float is the median time from each estimated boundary to the closest reference boundary.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# From the project's test suite
correct_intervals = np.array([[0, 1], [1, 2]])
assert np.allclose(
    mir_eval.segment.deviation(correct_intervals, correct_intervals), 0
)

# Standard unpacking pattern
ref_intervals = np.array([[0.0, 1.5], [1.5, 3.0]])
est_intervals = np.array([[0.0, 1.4], [1.4, 3.0]])
r_to_e, e_to_r = mir_eval.segment.deviation(ref_intervals, est_intervals, trim=True)
```

### LLM Instruction Prompt
- When evaluating segment boundaries using `mir_eval.segment.deviation`, you MUST pass 2D numpy arrays of shape `(n, 2)` for intervals, not 1D arrays of boundary times.
- Expect a tuple of two floats in return `(ref_to_est, est_to_ref)`, representing the median deviations in both directions.
- Set `trim=True` if you need to exclude the start (0.0) and end-of-track markers from the evaluation.

### Prompt Snippet
```text
To evaluate segmentation boundary accuracy, use `mir_eval.segment.deviation(ref_intervals, est_intervals)`. Ensure inputs are `(n, 2)` numpy arrays of intervals. The function returns two floats: the median deviation from reference to estimated boundaries, and from estimated to reference boundaries. Use `trim=True` to ignore the first and last boundaries.
```

### Common Failure Modes
- **ValueError (Shape mismatch):** Passing 1D arrays of boundary timestamps instead of the required `(n, 2)` interval arrays.
- **ValueError (Too many values to unpack):** Expecting a single float return value or a dictionary of metrics (like the `evaluate()` functions return) instead of the specific two-float tuple `(r_to_e, e_to_r)`.
- **Including Track Ends Unintentionally:** Forgetting to set `trim=True` when the evaluation protocol dictates that the trivial start (0.0s) and end-of-audio boundaries should not artificially lower the median deviation score.

### Fix Code Hint
```python
# BAD: Passing 1D boundary arrays directly
# boundaries = np.array([0.0, 1.5, 3.0])
# dev = mir_eval.segment.deviation(boundaries, boundaries)

# GOOD: Convert boundaries to intervals first, and unpack the two return values
boundaries = np.array([0.0, 1.5, 3.0])
intervals = mir_eval.util.boundaries_to_intervals(boundaries)
r_to_e, e_to_r = mir_eval.segment.deviation(intervals, intervals, trim=True)
```

## API Test: `directional_hamming_distance`

### Signature
```python
def directional_hamming_distance(reference_intervals, estimated_intervals)
```
_Source: source/mir_eval/chord.py:1359_

_Source doc:_ Compute the directional hamming distance between reference and estimated intervals as defined by [#harte2010towards]_ and used for MIREX 'OverSeg', 'UnderSeg' and 'MeanSeg' measures. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> overseg = 1 - mir_eval.chord.directional_hamming_distance( ...     ref_intervals, est_intervals) >>> underseg = 1 - mir_eval.chord.directional_hamming_distance( ...     est_intervals, ref_intervals) >>> seg = min(overseg, underseg) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2), dtype=float Reference chord intervals to score against. estimated_intervals : np.ndarray, shape=(m, 2), dtype=float Estimated chord intervals to score against. Returns ------- directional hamming distance : float directional hamming distance between reference intervals and estimated intervals.

### Goal
Compute the directional Hamming distance between reference and estimated chord intervals, commonly used to calculate MIREX 'OverSeg', 'UnderSeg', and 'MeanSeg' segmentation metrics.

### Parameters
- `reference_intervals`: `np.ndarray`, shape=(n, 2), dtype=float. Reference chord intervals (start and end times in seconds) to score against.
- `estimated_intervals`: `np.ndarray`, shape=(m, 2), dtype=float. Estimated chord intervals (start and end times in seconds) to score against.

### Input
Two 2D numpy arrays of shape `(n, 2)` and `(m, 2)` representing time intervals `[start, end]`. The intervals must be strictly non-overlapping. Typically, these are loaded from repository-format annotation files using `mir_eval.io.load_labeled_intervals`.

### Output
Returns `unspecified` — A `float` representing the directional Hamming distance between the reference intervals and estimated intervals.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

ref_ivs = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
est_ivs = np.array([[0.0, 0.9], [0.9, 1.8], [1.8, 2.5]])

# Compute directional hamming distance (reference to estimated)
dhd_ref_to_est = mir_eval.chord.directional_hamming_distance(ref_ivs, est_ivs)

# Compute directional hamming distance (estimated to reference)
dhd_est_to_ref = mir_eval.chord.directional_hamming_distance(est_ivs, ref_ivs)

# Calculate MIREX segmentation metrics
overseg = 1 - dhd_ref_to_est
underseg = 1 - dhd_est_to_ref
seg = min(overseg, underseg)
```

### LLM Instruction Prompt
- Use `mir_eval.chord.directional_hamming_distance(reference_intervals, estimated_intervals)` to compute the directional Hamming distance for chord segmentation evaluation.
- Ensure both inputs are `(n, 2)` numpy arrays of floats representing `[start, end]` times.
- **Precondition:** Intervals must not overlap. Overlapping intervals will raise a `ValueError`.
- To compute the 'OverSeg' metric, use `1 - directional_hamming_distance(ref, est)`. To compute 'UnderSeg', reverse the arguments: `1 - directional_hamming_distance(est, ref)`.

### Prompt Snippet
```text
When evaluating chord segmentation, use `mir_eval.chord.directional_hamming_distance(ref_intervals, est_intervals)`. Ensure intervals are non-overlapping `(n, 2)` float arrays. Calculate OverSeg as `1 - dhd(ref, est)` and UnderSeg as `1 - dhd(est, ref)`.
```

### Common Failure Modes
- **Overlapping Intervals:** Passing intervals that overlap (e.g., `[[0.0, 1.0], [0.9, 2.0]]`) violates the function's preconditions and will raise a `ValueError`.
- **Incorrect Array Shapes:** Passing 1D arrays or arrays not of shape `(n, 2)` will cause indexing errors or validation failures.
- **Incorrect Argument Order for Metrics:** Confusing the order of `reference_intervals` and `estimated_intervals` will swap the OverSeg and UnderSeg results, as the distance is directional (asymmetric).

### Fix Code Hint
```python
# If intervals overlap, they must be corrected before calling
ivs_overlap = np.array([[0.0, 1.0], [0.9, 2.0]])

try:
    mir_eval.chord.directional_hamming_distance(ivs_overlap, est_ivs)
except ValueError as e:
    # Handle the ValueError raised by overlapping intervals
    print("Intervals must be strictly non-overlapping.")
```

## API Test: `encode`

### Signature
```python
def encode(chord_label, reduce_extended_chords=False, strict_bass_intervals=False)
```
_Source: source/mir_eval/chord.py:471_

_Source doc:_ Translate a chord label to numerical representations for evaluation. Parameters ---------- chord_label : str Chord label to encode. reduce_extended_chords : bool Whether to map the upper voicings of extended chords (9's, 11's, 13's) to semitone extensions. (Default value = False) strict_bass_intervals : bool Whether to require that the bass scale degree is present in the chord. (Default value = False) Returns ------- root_number : int Absolute semitone of the chord's root. semitone_bitmap : np.ndarray, dtype=int 12-dim vector of relative semitones in the chord spelling. bass_number : int Relative semitone of the chord's bass note, e.g. 0=root, 7=fifth, etc.

### Goal
Translate a string chord label into numerical representations (root absolute semitone, 12-dimensional relative semitone bitmap, and relative bass semitone) for evaluation.

### Parameters
- `chord_label`: A string representing the chord label to encode (e.g., `"C:maj"`, `"G:dim(4)/6"`).
- `reduce_extended_chords`, default `False`: A boolean indicating whether to map the upper voicings of extended chords (9's, 11's, 13's) to semitone extensions.
- `strict_bass_intervals`, default `False`: A boolean indicating whether to require that the bass scale degree is explicitly present in the chord's spelling.

### Input
A string representing a chord label. The label must be valid according to `mir_eval`'s regular expressions and use valid chord qualities from `chord.QUALITIES`. If `strict_bass_intervals` is set to `True`, any bass note specified (e.g., via inversion or slash notation) must be explicitly named as an extension in the chord spelling.

### Output
Returns `unspecified` — A 3-tuple `(root_number, semitone_bitmap, bass_number)` where:
1. `root_number` is an `int` representing the absolute semitone of the chord's root.
2. `semitone_bitmap` is a 12-dimensional `np.ndarray` of type `int` representing the relative semitones in the chord spelling.
3. `bass_number` is an `int` representing the relative semitone of the chord's bass note (e.g., 0=root, 7=fifth).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Standard encoding
root, intervals, bass = mir_eval.chord.encode(
    "C:maj7", reduce_extended_chords=False, strict_bass_intervals=False
)

# Encoding with strict bass intervals and reduced extended chords
root, intervals, bass = mir_eval.chord.encode(
    "A:min9", reduce_extended_chords=True, strict_bass_intervals=True
)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.encode`, expect a 3-tuple return value `(root, intervals, bass)`. Ensure the `chord_label` is a valid string. If `strict_bass_intervals=True` is used, ensure that any bass note specified in the label (e.g., after a slash `/`) is explicitly included in the chord's extensions, otherwise the function will fail.

### Prompt Snippet
```text
Use `mir_eval.chord.encode(chord_label, reduce_extended_chords=False, strict_bass_intervals=False)` to parse chord strings into numerical representations. It returns a tuple: `(root_number, semitone_bitmap, bass_number)`. If `strict_bass_intervals` is True, non-chord bass notes must be explicitly named as extensions.
```

### Common Failure Modes
- **Strict Bass Interval Violation:** Setting `strict_bass_intervals=True` but providing a chord label where the bass note is not part of the chord spelling (e.g., `"G:dim(4)/6"`). Non-chord bass notes *must* be explicitly named as extensions when this flag is active.
- **Invalid Chord Quality:** Passing a chord label that fails the regular expression validation or uses an unknown quality not present in `chord.QUALITIES`.

### Fix Code Hint
```python
# If strict_bass_intervals=True, ensure the bass note is in the chord spelling.
# This will fail: mir_eval.chord.encode("G:dim(4)/6", strict_bass_intervals=True)
# Instead, either set strict_bass_intervals=False or fix the chord label to include the extension.
root, intervals, bass = mir_eval.chord.encode(
    "G:dim(4)/6",
    reduce_extended_chords=False,
    strict_bass_intervals=False  # Set to False to allow non-chord bass notes
)
```

## API Test: `encode_many`

### Signature
```python
def encode_many(chord_labels, reduce_extended_chords=False)
```
_Source: source/mir_eval/chord.py:523_

_Source doc:_ Translate a set of chord labels to numerical representations for sane evaluation. Parameters ---------- chord_labels : list Set of chord labels to encode. reduce_extended_chords : bool Whether to map the upper voicings of extended chords (9's, 11's, 13's) to semitone extensions. (Default value = False) Returns ------- root_number : np.ndarray, dtype=int Absolute semitone of the chord's root. interval_bitmap : np.ndarray, dtype=int 12-dim vector of relative semitones in the given chord quality. bass_number : np.ndarray, dtype=int Relative semitones of the chord's bass notes.

### Goal
Translate a list of string chord labels into numerical representations (root semitone, interval bitmap, and bass semitone) for standardized MIR evaluation.

### Parameters
- `chord_labels`: A list of strings representing the set of chord labels to encode (e.g., `["C:min", "N", "B:maj/5"]`).
- `reduce_extended_chords`, default `False`: A boolean indicating whether to map the upper voicings of extended chords (9's, 11's, 13's) to semitone extensions.

### Input
The caller must provide a list of string chord labels formatted according to standard MIR chord syntax. The chord strings must pass internal regular expression validation and use valid chord qualities defined in `mir_eval.chord.QUALITIES`. The "no chord" label is represented by the string `"N"`.

### Output
Returns a tuple of three `np.ndarray` objects (all `dtype=int`): `(root_number, interval_bitmap, bass_number)`. 
- `root_number`: 1D array of the absolute semitones of the chords' roots (0-11, or -1 for "N").
- `interval_bitmap`: 2D array where each row is a 12-dimensional binary vector of relative semitones present in the given chord quality.
- `bass_number`: 1D array of the relative semitones of the chords' bass notes (or -1 for "N").

### Valid Call Patterns
```python
import mir_eval
import numpy as np

labels = ["B:maj(*1,*3)/5", "B:maj(*1,*3)/5", "N", "C:min", "C:min"]
roots, intervals, basses = mir_eval.chord.encode_many(labels)

# roots will be array([11, 11, -1, 0, 0])
# basses will be array([7, 7, -1, 0, 0])
```

### LLM Instruction Prompt
- When evaluating chord sequences, use `mir_eval.chord.encode_many` to batch-convert string labels into numeric arrays. Pass a list of strings, not a single string. Expect a 3-tuple of numpy arrays in return: `(roots, intervals, basses)`. Ensure chord labels strictly follow MIR syntax; invalid qualities will fail validation.

### Prompt Snippet
```text
mir_eval.chord.encode_many(chord_labels: list[str], reduce_extended_chords: bool = False) -> tuple[np.ndarray, np.ndarray, np.ndarray]
Batch encodes MIR chord strings into (root_number, interval_bitmap, bass_number) integer arrays. "N" yields -1 roots/basses and all-zero bitmaps.
```

### Common Failure Modes
- **Passing a single string:** Providing a single string like `"C:maj"` instead of a list `["C:maj"]` will cause iteration errors or incorrect character-by-character parsing.
- **Invalid chord syntax:** Passing malformed chords or qualities not present in `mir_eval.chord.QUALITIES` will fail the internal regular expression validation.
- **Unpacking errors:** Failing to unpack the returned 3-tuple into exactly three variables (`roots, intervals, basses`).

### Fix Code Hint
```python
# BAD: Passing a single string and failing to unpack the 3-tuple
encoded = mir_eval.chord.encode_many("C:min")

# GOOD: Passing a list of strings and unpacking the tuple
roots, intervals, basses = mir_eval.chord.encode_many(["C:min"])
```

## API Test: `establishment_FPR`

### Signature
```python
def establishment_FPR(reference_patterns, estimated_patterns, similarity_metric='cardinality_score')
```
_Source: source/mir_eval/pattern.py:238_

_Source doc:_ Compute the establishment F1 Score, Precision and Recall. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> F, P, R = mir_eval.pattern.establishment_FPR(ref_patterns, ...                                              est_patterns) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format similarity_metric : str A string representing the metric to be used when computing the similarity matrix. Accepted values: - "cardinality_score": Count of the intersection between occurrences. (Default value = "cardinality_score") Returns ------- f_measure : float The establishment F1 Score precision : float The establishment Precision recall : float The establishment Recall

### Goal
Compute the establishment F1 Score, Precision, and Recall for musical pattern discovery evaluation.

### Parameters
- `reference_patterns`: `list` — The reference (ground truth) patterns in the format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: `list` — The estimated patterns to evaluate, in the same format as the reference patterns.
- `similarity_metric`, default `'cardinality_score'`: `str` — A string representing the metric to be used when computing the similarity matrix. Accepted values include `"cardinality_score"` (which counts the intersection between occurrences).

### Input
The caller must provide in-memory lists of reference and estimated patterns. These are typically parsed from repository-format text files using `mir_eval.io.load_patterns()`. Do not pass raw file paths or unparsed text directly to this function.

### Output
Returns `unspecified` — A tuple of three `float` values: `(f_measure, precision, recall)` representing the establishment F1 Score, the establishment Precision, and the establishment Recall, respectively.

### Valid Call Patterns
```python
import mir_eval

# Call form inferred from source documentation
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

f_measure, precision, recall = mir_eval.pattern.establishment_FPR(
    ref_patterns, 
    est_patterns, 
    similarity_metric="cardinality_score"
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery with `mir_eval.pattern.establishment_FPR`, always load the pattern text files using `mir_eval.io.load_patterns()` first. Do not pass file paths directly to the metric function. Expect a tuple of three floats `(F, P, R)` to be returned.

### Prompt Snippet
```text
Use `mir_eval.pattern.establishment_FPR(reference_patterns, estimated_patterns)` to compute the establishment F1 Score, Precision, and Recall. Ensure inputs are lists of patterns parsed via `mir_eval.io.load_patterns()`. The function returns a tuple of three floats: `(f_measure, precision, recall)`.
```

### Common Failure Modes
- **Passing file paths instead of parsed lists**: Providing string file paths directly to `establishment_FPR` will cause a failure. The function expects lists of pattern data.
- **Invalid similarity metric**: Passing an unsupported string to `similarity_metric` (only `"cardinality_score"` is explicitly documented as accepted) will result in an error during the similarity matrix computation.

### Fix Code Hint
```python
# BAD: Passing file paths directly
# F, P, R = mir_eval.pattern.establishment_FPR("ref.txt", "est.txt")

# GOOD: Parse the files into lists first
import mir_eval
ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
F, P, R = mir_eval.pattern.establishment_FPR(ref_patterns, est_patterns)
```

## API Test: `evaluate`

### Signature
```python
def evaluate(reference_sources, estimated_sources, **kwargs)
def evaluate(ref_intervals, ref_pitches, est_intervals, est_pitches, **kwargs)
def evaluate(ref_time, ref_freqs, est_time, est_freqs, **kwargs)
def evaluate(ref_intervals, ref_labels, est_intervals, est_labels, **kwargs)
def evaluate(reference_onsets, estimated_onsets, **kwargs)
def evaluate(reference_timestamps, estimated_timestamps, **kwargs)
def evaluate(reference_key, estimated_key, allow_descending_fifths=False, **kwargs)
def evaluate(ref_time, ref_freq, est_time, est_freq, est_voicing=None, ref_reward=None, **kwargs)
def evaluate(ref_patterns, est_patterns, **kwargs)
def evaluate(ref_intervals_hier, ref_labels_hier, est_intervals_hier, est_labels_hier, **kwargs)
def evaluate(reference_tempi, reference_weight, estimated_tempi, **kwargs)
def evaluate(ref_intervals, ref_pitches, ref_velocities, est_intervals, est_pitches, est_velocities, **kwargs)
def evaluate(reference_beats, estimated_beats, **kwargs)
```

### Goal
Compute an entire suite of task-specific evaluation metrics for a music information retrieval (MIR) task (such as melody extraction, beat tracking, or alignment) by comparing an estimated prediction against a ground-truth reference.

### Parameters
- `ref_time`: `np.ndarray` — Time of each reference frequency value (for melody evaluation).
- `ref_freq`: `np.ndarray` — Array of reference frequency values (for melody evaluation).
- `est_time`: `np.ndarray` — Time of each estimated frequency value.
- `est_freq`: `np.ndarray` — Array of estimated frequency values.
- `est_voicing`, default `None`: `np.ndarray` — Estimate voicing confidence. If `None`, voicing is inferred from `est_freq`: frames with frequency <= 0.0 are considered "unvoiced", and frames with frequency > 0.0 are considered "voiced".
- `ref_reward`, default `None`: `np.ndarray` — Reference pitch estimation reward. If `None`, all frames are weighted equally.
- `**kwargs`: Additional keyword arguments which will be passed to the appropriate underlying metric or preprocessing functions.

### Input
Callers must provide in-memory data structures (typically `numpy.ndarray` objects) representing the reference and estimated annotations. Data should be loaded from repository-format files using the `mir_eval.io` submodule (e.g., `mir_eval.io.load_time_series` for melody, `mir_eval.io.load_events` for beats). 
**Preconditions:** 
- For `mir_eval.melody.evaluate`, passing incomplete files is permitted but will issue a warning.
- For `mir_eval.tempo.evaluate`, one reference tempo and both estimate tempi are allowed to be zero, and zero tolerance is permitted (though it will issue a warning).
- For `mir_eval.transcription_velocity.evaluate`, the evaluation returns 0 when there is no overlap.

### Output
Returns `unspecified` — A Python dictionary (`dict`) of scores, where the key is the metric name (`str`) and the value is the numerical score achieved (`float`).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Melody evaluation (from source documentation)
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')
melody_scores = mir_eval.melody.evaluate(ref_time, ref_freq, est_time, est_freq)

# 2. Beat evaluation (from test suite)
reference_beats = np.array([0.5, 1.0, 1.5, 2.0])
estimated_beats = np.array([0.52, 1.05, 1.5, 2.01])
beat_scores = mir_eval.beat.evaluate(reference_beats, estimated_beats)

# 3. Alignment evaluation (from test suite)
reference_alignments = np.array([[0.0, 1.0], [1.0, 2.0]])
estimated_alignments = np.array([[0.0, 0.9], [0.9, 2.1]])
alignment_scores = mir_eval.alignment.evaluate(reference_alignments, estimated_alignments)
```

### LLM Instruction Prompt
- Always call `evaluate` via its specific task submodule (e.g., `mir_eval.melody.evaluate`, `mir_eval.beat.evaluate`). Never call a bare `evaluate()`.
- Do not pass file paths directly to `evaluate`. Always load the data first using the appropriate `mir_eval.io` function (like `mir_eval.io.load_time_series` or `mir_eval.io.load_events`).
- Expect a dictionary of metric names to float scores as the return value. Do not invent metric names; iterate over the returned dictionary keys.

### Prompt Snippet
```text
To evaluate MIR tasks, load your reference and estimated annotations using `mir_eval.io`, then pass the resulting numpy arrays to the task-specific evaluate function, such as `mir_eval.melody.evaluate(ref_time, ref_freq, est_time, est_freq)`. It returns a dictionary mapping metric names to float scores.
```

### Common Failure Modes
- **Calling a bare function:** Attempting to call `mir_eval.evaluate(...)` instead of the submodule-specific function like `mir_eval.melody.evaluate(...)`.
- **Passing file paths instead of arrays:** Providing string file paths directly to `evaluate` instead of parsing them first with `mir_eval.io` functions.
- **Mismatched array lengths:** Providing a `ref_time` array that has a different length than the `ref_freq` array.
- **Incomplete files in melody evaluation:** Providing incomplete time series data to `mir_eval.melody.evaluate` will succeed but trigger a warning.

### Fix Code Hint
```python
# BAD: Passing file paths directly to a bare evaluate function
# scores = evaluate('ref.txt', 'est.txt')

# GOOD: Load data using mir_eval.io and call the submodule's evaluate
import mir_eval
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')
scores = mir_eval.melody.evaluate(ref_time, ref_freq, est_time, est_freq)
```

## API Test: `events`

### Signature
```python
def events(times, labels=None, base=None, height=None, ax=None, text_kw=None, prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:543_

### Goal
Plot event times (such as beats or onsets) as a set of vertical lines on a matplotlib axis for visual inspection of MIR annotations.

### Parameters
- `times`: `np.ndarray`, shape=(n,). The event times in seconds, typically in the format returned by `mir_eval.io.load_events` or `mir_eval.io.load_labeled_events`.
- `labels`, default `None`: `list`, shape=(n,). Optional individual event labels corresponding to each time, in the format returned by `mir_eval.io.load_labeled_events`.
- `base`, default `None`: `number`. The vertical position of the base of the line. By default, this will be the bottom of the plot.
- `height`, default `None`: `number`. The height of the lines. By default, this will be the top of the plot (minus `base`).
- `ax`, default `None`: `matplotlib.pyplot.axes`. An axis handle on which to draw the events. If none is provided, a new set of axes is created.
- `text_kw`, default `None`: `dict`. If `labels` is provided, the properties of the text objects can be specified here (valid parameters for `matplotlib.pyplot.Text`).
- `prop_cycle`, default `None`: `cycle.Cycler`. An optional property cycle object to specify style properties. If not provided, the default property cycler will be retrieved from matplotlib.
- `**kwargs`: Additional keyword arguments to pass directly to `matplotlib.pyplot.vlines` (e.g., `label="reference"` for a legend).

### Input
- `times` must be a 1D numpy array of numerical event times.
- If `labels` is provided, it must be a list of the same length as `times`.
- **Precondition:** If either `base` or `height` is provided, **both** must be provided.
- Display tests must be kept headless without network or audio-device access.

### Output
Returns `unspecified` — A `matplotlib.pyplot.axes._subplots.AxesSubplot` handle to the (possibly constructed) plot axes containing the plotted vertical lines.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval

plt.figure()

# Load event data
beats_ref = mir_eval.io.load_events("data/beat/ref00.txt")[:30]
beats_est = mir_eval.io.load_events("data/beat/est00.txt")[:30]

# Plot both with legend labels (passed via **kwargs to vlines)
mir_eval.display.events(beats_ref, label="reference")
mir_eval.display.events(beats_est, label="estimate")
plt.legend(loc="upper right")

# Plot events with individual event labels
labels = list("abcdefghijklmnop")[:len(beats_ref)]
mir_eval.display.events(beats_ref, labels=labels)
```

### LLM Instruction Prompt
- When calling `mir_eval.display.events`, ensure `times` is a 1D numpy array.
- If you need to set the vertical bounds of the lines, you MUST provide both `base` and `height`; providing only one will cause an error.
- Distinguish between the `labels` parameter (a list of strings annotating each individual event line) and the `label` kwarg (a single string passed to `vlines` to label the entire collection of lines in a `plt.legend()`).
- Always keep display tests headless; do not invoke `plt.show()` in automated environments.

### Prompt Snippet
```text
Plot the reference and estimated beats on the same axis using `mir_eval.display.events`. Add a legend to distinguish them. Ensure the test remains headless and does not block execution.
```

### Common Failure Modes
- **Missing paired arguments:** Providing `base` without `height` (or vice versa) violates the function's preconditions and will fail.
- **Mismatched labels length:** Passing a `labels` list that does not match the length of the `times` array.
- **Blocking execution:** Calling `plt.show()` in an automated test environment, which violates the headless constraint and causes the test suite to hang.

### Fix Code Hint
```python
# BAD: Providing base without height
# mir_eval.display.events(beats, base=0)

# GOOD: Providing both base and height
mir_eval.display.events(beats, base=0, height=1)

# BAD: Confusing `labels` (individual annotations) with `label` (legend entry)
# mir_eval.display.events(beats, labels="reference")

# GOOD: Using `label` kwarg for the legend
mir_eval.display.events(beats, label="reference")
```

## API Test: `f_measure`

### Signature
```python
def f_measure(reference_onsets, estimated_onsets, window=0.05)
def f_measure(precision, recall, beta=1.0)
def f_measure(reference_beats, estimated_beats, f_measure_threshold=0.07)
```
_Source: source/mir_eval/onset.py:55  (+2 more definition site/overload)_

_Source doc:_ Compute the F-measure of correct vs incorrectly predicted onsets. "Correctness" is determined over a small window. Examples -------- >>> reference_onsets = mir_eval.io.load_events('reference.txt') >>> estimated_onsets = mir_eval.io.load_events('estimated.txt') >>> F, P, R = mir_eval.onset.f_measure(reference_onsets, ...                                    estimated_onsets) Parameters ---------- reference_onsets : np.ndarray reference onset locations, in seconds estimated_onsets : np.ndarray estimated onset locations, in seconds window : float Window size, in seconds (Default value = .05) Returns ------- f_measure : float 2*precision*recall/(precision + recall) precision : float (# true positives)/(# true positives + # false positives) recall : float (# true positives)/(# true positives + # false negatives)

### Goal
Compute the F-measure (along with precision and recall) of correct versus incorrectly predicted events (such as onsets or beats) by matching them within a specified tolerance window.

### Parameters
- `reference_onsets`: `np.ndarray` representing the ground truth reference onset locations, in seconds.
- `estimated_onsets`: `np.ndarray` representing the estimated onset locations to be evaluated, in seconds.
- `window`, default `0.05`: `float` representing the tolerance window size in seconds. An estimated event is considered correct if it falls within this window of a reference event.

### Input
The caller must provide 1D numpy arrays of event times in seconds. If reading from repository-format text files, the data must first be parsed using `mir_eval.io.load_events()`. 
**Preconditions:** 
- Arrays can be empty, but passing an empty array for either reference or estimated events will issue a `UserWarning` (e.g., `"Reference onsets are empty."`) and result in a score of `0`.
- For beat evaluation (`mir_eval.beat.f_measure`), it is a common preprocessing step to first crop out early events using `mir_eval.beat.trim_beats()`.

### Output
Returns `unspecified` — Depending on the submodule called, the return format differs:
- `mir_eval.onset.f_measure` returns a 3-tuple of floats: `(f_measure, precision, recall)`.
- `mir_eval.beat.f_measure` returns a single float: `f_score`.
- `mir_eval.util.f_measure` (the precision/recall overload) returns a single float: `f_measure`.

### Valid Call Patterns
```python
import mir_eval
import numpy as np
import warnings

# 1. Onset evaluation (returns a 3-tuple)
onsets = np.arange(10, dtype=float)
f_measure, precision, recall = mir_eval.onset.f_measure(onsets, onsets)

# 2. Handling empty arrays (issues a warning, returns 0s)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    f_measure, precision, recall = mir_eval.onset.f_measure(np.array([]), np.array([]))

# 3. Beat evaluation overload (returns a single float)
reference_beats = mir_eval.io.load_events('reference.txt')
estimated_beats = mir_eval.io.load_events('estimated.txt')
reference_beats = mir_eval.beat.trim_beats(reference_beats)
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)
f_score = mir_eval.beat.f_measure(reference_beats, estimated_beats)
```

### LLM Instruction Prompt
- When evaluating onsets or beats, ensure you use the correct submodule (`mir_eval.onset.f_measure` vs `mir_eval.beat.f_measure`) and unpack the return values accordingly. `onset` returns a 3-tuple `(f_measure, precision, recall)`, whereas `beat` returns a single `f_score`.
- Never pass file paths directly to `f_measure`. Always load them first using `mir_eval.io.load_events()`.
- Be prepared to handle or suppress `UserWarning`s if there is a possibility that the input arrays are empty.

### Prompt Snippet
```text
To compute the F-measure for MIR events, use `mir_eval.onset.f_measure(ref, est, window=0.05)` which returns `(f_measure, precision, recall)`, or `mir_eval.beat.f_measure(ref, est, f_measure_threshold=0.07)` which returns a single `f_score`. Inputs must be 1D numpy arrays of times in seconds (loaded via `mir_eval.io.load_events`). Empty arrays will trigger a UserWarning and return 0.
```

### Common Failure Modes
- **Unpacking Errors:** Attempting to assign the result of `mir_eval.onset.f_measure` to a single variable and treating it as a float (it is a tuple), or trying to unpack `mir_eval.beat.f_measure` into three variables (it is a single float).
- **Type Errors:** Passing string file paths directly to the function instead of parsing them into numpy arrays first.
- **Uncaught Warnings:** Failing test suites because empty arrays trigger a `UserWarning` ("Reference onsets are empty." or "Estimated onsets are empty.") that is not caught or suppressed.

### Fix Code Hint
```python
# Incorrect: Passing file paths directly
# f_score = mir_eval.beat.f_measure('ref.txt', 'est.txt')

# Correct: Load events first
ref_beats = mir_eval.io.load_events('ref.txt')
est_beats = mir_eval.io.load_events('est.txt')
f_score = mir_eval.beat.f_measure(ref_beats, est_beats)

# Incorrect: Wrong unpacking for onset
# f_score = mir_eval.onset.f_measure(ref_onsets, est_onsets)

# Correct: Unpack the 3-tuple for onset
f_score, precision, recall = mir_eval.onset.f_measure(ref_onsets, est_onsets)
```

## API Test: `filter_kwargs`

### Signature
```python
def filter_kwargs(_function, *args, **kwargs)
```
_Source: source/mir_eval/util.py:860_

_Source doc:_ Given a function and args and keyword args to pass to it, call the function but using only the keyword arguments which it accepts.  This is equivalent to redefining the function with an additional ``**kwargs`` to accept slop keyword args. If the target function already accepts ``**kwargs`` parameters, no filtering is performed. Parameters ---------- _function : callable Function to call.  Can take in any number of args or kwargs *args **kwargs Arguments and keyword arguments to _function.

### Goal
Safely execute a target function by passing along positional arguments and only the specific keyword arguments that the target function's signature explicitly accepts, discarding any excess "slop" keyword arguments.

### Parameters
- `_function`: The target callable (function or method) to execute.
- `*args`: Positional arguments to pass directly through to `_function` without modification.
- `**kwargs`: A collection of keyword arguments. These will be inspected against `_function`'s signature and filtered so that only valid keyword arguments are passed.

### Input
The caller must provide a valid Python callable for `_function`. The `*args` must satisfy the target function's required positional parameters. The `**kwargs` can contain any arbitrary keys; however, if `_function` does not natively accept `**kwargs`, any keys in `**kwargs` that do not match `_function`'s named parameters will be silently dropped before invocation.

### Output
Returns `unspecified` — The return value of the executed `_function` after it is called with the provided `*args` and the filtered subset of `**kwargs`.

### Valid Call Patterns
```python
import mir_eval.util

def dummy_metric(reference, estimated, tolerance=0.5):
    return tolerance

# INFERRED FROM SIGNATURE (No exact test suite example provided)
# 'extra_param' will be filtered out, preventing a TypeError
result = mir_eval.util.filter_kwargs(
    dummy_metric, 
    [1.0, 2.0], 
    [1.0, 2.1], 
    tolerance=0.1, 
    extra_param="ignore_me"
)
```

### LLM Instruction Prompt
- When passing a broad dictionary of configuration parameters (e.g., when chaining sonification kwargs like passing `**kwargs` from `sonify.chroma` to `sonify.time_frequency`), use `mir_eval.util.filter_kwargs(target_func, *args, **kwargs)` to prevent `TypeError: got an unexpected keyword argument`.
- Do not rely on `filter_kwargs` to filter positional `*args`; it only inspects and filters keyword arguments.
- Ensure all required arguments for the target function are still provided, as `filter_kwargs` does not supply missing required parameters.

### Prompt Snippet
```text
Use `mir_eval.util.filter_kwargs(_function, *args, **kwargs)` to safely call a function with a dictionary of kwargs that might contain unsupported keys. It automatically drops invalid kwargs unless the target function natively accepts `**kwargs`.
```

### Common Failure Modes
- **Positional Argument Overflow:** Passing too many positional `*args` to a function that does not accept them. `filter_kwargs` only filters keyword arguments, so excess positional arguments will still raise a `TypeError`.
- **Missing Required Arguments:** Relying on `filter_kwargs` but failing to provide the required positional or keyword arguments that `_function` strictly needs to execute.
- **Non-Callable Target:** Passing a non-callable object (like a string or array) as `_function`, which will raise a `TypeError` when the utility attempts to inspect and call it.

### Fix Code Hint
```python
# BAD: filter_kwargs does not filter positional arguments, this will raise TypeError if my_func takes 1 arg
# mir_eval.util.filter_kwargs(my_func, arg1, arg2, kwarg1="val")

# GOOD: Pass required positional args, and let filter_kwargs handle the messy kwargs dictionary
kwargs_dict = {"tolerance": 0.5, "invalid_slop": True}
result = mir_eval.util.filter_kwargs(my_func, arg1, **kwargs_dict)
```

## API Test: `first_n_target_proportion_R`

### Signature
```python
def first_n_target_proportion_R(reference_patterns, estimated_patterns, n=5)
```
_Source: source/mir_eval/pattern.py:554_

_Source doc:_ First n target proportion establishment recall metric. This metric is similar is similar to the establishment FPR score, but it only takes into account the first n estimated patterns and it only outputs the Recall value of it. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> R = mir_eval.pattern.first_n_target_proportion_R( ...                                 ref_patterns, est_patterns, n=5) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format n : int Number of patterns to consider from the estimated results, in the order they appear in the matrix. (Default value = 5) Returns ------- recall : float The first n target proportion Recall.

### Goal
Computes the first *n* target proportion establishment recall metric for pattern discovery, evaluating only the top *n* estimated patterns against the reference patterns.

### Parameters
- `reference_patterns`: A `list` of reference (ground truth) patterns in the format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: A `list` of estimated patterns in the same format.
- `n`, default `5`: An `int` specifying the number of patterns to consider from the estimated results, in the order they appear in the matrix.

### Input
The caller must provide reference and estimated pattern data as lists. These lists must be parsed from repository-format text files using the `mir_eval.io.load_patterns()` utility function prior to calling this metric. 

### Output
Returns `unspecified` — A `float` representing the first *n* target proportion Recall score.

### Valid Call Patterns
```python
import mir_eval

# Load patterns from repository-format text files
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

# Compute the recall metric for the first 5 patterns
R = mir_eval.pattern.first_n_target_proportion_R(
    ref_patterns, 
    est_patterns, 
    n=5
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery with `first_n_target_proportion_R`, always parse the input text files using `mir_eval.io.load_patterns()` first. Do not pass file paths or raw file descriptors directly to the metric function. Ensure `n` is passed as an integer if overriding the default of 5.

### Prompt Snippet
```text
`mir_eval.pattern.first_n_target_proportion_R(reference_patterns, estimated_patterns, n=5)` computes the establishment recall metric considering only the first `n` estimated patterns. Inputs must be lists loaded via `mir_eval.io.load_patterns()`. Returns a float representing the recall score.
```

### Common Failure Modes
- Passing string file paths or `pathlib.Path` objects directly to `first_n_target_proportion_R` instead of the parsed pattern lists.
- Passing raw, unparsed text data read directly from a file without using `mir_eval.io.load_patterns()`.

### Fix Code Hint
```python
# INCORRECT: Passing file paths directly
# R = mir_eval.pattern.first_n_target_proportion_R("ref.txt", "est.txt")

# CORRECT: Load patterns first using mir_eval.io
import mir_eval
ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
R = mir_eval.pattern.first_n_target_proportion_R(ref_patterns, est_patterns, n=5)
```

## API Test: `first_n_three_layer_P`

### Signature
```python
def first_n_three_layer_P(reference_patterns, estimated_patterns, n=5)
```
_Source: source/mir_eval/pattern.py:509_

_Source doc:_ First n three-layer precision. This metric is basically the same as the three-layer FPR but it is only applied to the first n estimated patterns, and it only returns the precision. In MIREX and typically, n = 5. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> P = mir_eval.pattern.first_n_three_layer_P(ref_patterns, ...                                            est_patterns, n=5) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format n : int Number of patterns to consider from the estimated results, in the order they appear in the matrix (Default value = 5) Returns ------- precision : float The first n three-layer Precision

### Goal
Computes the three-layer precision metric restricted to the first *n* estimated musical patterns, commonly used in MIREX pattern discovery evaluation.

### Parameters
- `reference_patterns`: A list of reference (ground truth) patterns in the format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: A list of estimated patterns in the same format as the reference patterns.
- `n`, default `5`: An integer specifying the number of patterns to consider from the estimated results, evaluated in the order they appear.

### Input
The caller must provide reference and estimated patterns as parsed Python lists, not raw file paths. These lists must be loaded from repository-format text files using `mir_eval.io.load_patterns()`. 

### Output
Returns `unspecified` — A float representing the first *n* three-layer precision score.

### Valid Call Patterns
```python
import mir_eval

# Example derived from the authoritative source documentation
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

precision = mir_eval.pattern.first_n_three_layer_P(
    ref_patterns, 
    est_patterns, 
    n=5
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery using `first_n_three_layer_P`, you MUST first parse the text files into lists using `mir_eval.io.load_patterns()`. Do not pass file paths directly to the metric function. Leave `n=5` unless a different threshold is explicitly requested, as 5 is the MIREX standard.

### Prompt Snippet
```text
mir_eval.pattern.first_n_three_layer_P requires lists of patterns, not file paths. Parse your text files with `mir_eval.io.load_patterns(filepath)` before passing them to the metric.
```

### Common Failure Modes
- **Passing file paths instead of lists**: Providing string file paths directly to `first_n_three_layer_P` will cause a failure, as the function expects the in-memory list structures returned by the I/O module.
- **Incorrect pattern format**: Manually constructing the pattern lists incorrectly instead of relying on `mir_eval.io.load_patterns()` to guarantee the expected internal format.

### Fix Code Hint
```python
# BAD: Passing file paths directly
# p = mir_eval.pattern.first_n_three_layer_P("ref.txt", "est.txt")

# GOOD: Loading patterns first
ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
p = mir_eval.pattern.first_n_three_layer_P(ref_patterns, est_patterns, n=5)
```

## API Test: `freq_to_voicing`

### Signature
```python
def freq_to_voicing(frequencies, voicing=None)
```
_Source: source/mir_eval/melody.py:157_

_Source doc:_ Convert from an array of frequency values to frequency array + voice/unvoiced array Parameters ---------- frequencies : np.ndarray Array of frequencies.  A frequency <= 0 indicates "unvoiced". voicing : np.ndarray Array of voicing values. (Default value = None) Default None, which means the voicing is inferred from `frequencies`: - frames with frequency <= 0.0 are considered "unvoiced" - frames with frequency > 0.0 are considered "voiced" If specified, `voicing` is used as the voicing array, but frequencies with value 0 are forced to have 0 voicing. - Voicing inferred by negative frequency values is ignored. Returns ------- frequencies : np.ndarray Array of frequencies, all >= 0. voiced : np.ndarray Array of voicings between 0 and 1, same length as frequencies, which indicates voiced or unvoiced

### Goal
Converts an array of melody frequency values into a strictly non-negative frequency array and a corresponding voicing array, handling negative frequencies as unvoiced indicators.

### Parameters
- `frequencies`: `np.ndarray` of frequency values in Hz. A frequency `<= 0` indicates an "unvoiced" frame.
- `voicing`, default `None`: `np.ndarray` of voicing values. If `None`, voicing is inferred directly from `frequencies` (values `<= 0.0` become unvoiced `0`, values `> 0.0` become voiced `1`). If specified, this array is used, but any frame where the frequency is exactly `0` is forced to have a voicing of `0`.

### Input
The caller must provide a NumPy array of numeric frequency values. If the optional `voicing` array is provided, it must be a NumPy array of the same length as `frequencies`, containing values between 0 and 1. 

### Output
Returns `unspecified` — A tuple of two `np.ndarray` objects: `(frequencies, voiced)`. The returned `frequencies` array contains strictly non-negative values (negative inputs are converted to their absolute positive values). The `voiced` array contains values between 0 and 1 indicating the voiced or unvoiced status of each frame, matching the length of the input.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Pattern 1: Inferring voicing from negative/zero frequencies
hz = np.array([0.0, 100.0, -132.0])
res_hz, res_voicing = mir_eval.melody.freq_to_voicing(hz)
# res_hz is [0.0, 100.0, 132.0]
# res_voicing is [0, 1, 0]

# Pattern 2: Providing an explicit voicing array
hz = np.array([0.0, 100.0, -132.0, 0.0, 131.0])
voicing = np.array([0.8, 0.0, 1.0, 0.0, 0.5])
res_hz, res_voicing = mir_eval.melody.freq_to_voicing(hz, voicing=voicing)
# res_hz is [0.0, 100.0, 132.0, 0.0, 131.0]
# res_voicing is [0.0, 0.0, 1.0, 0.0, 0.5]
```

### LLM Instruction Prompt
- When evaluating melody extraction outputs where unvoiced frames are denoted by negative frequencies, use `mir_eval.melody.freq_to_voicing(frequencies)` to separate the data into a non-negative frequency array and a voicing indicator array. 
- Always unpack the returned tuple into two variables: `frequencies, voicing`.
- Remember that if you pass an explicit `voicing` array, any frequency that is exactly `0` will strictly force the output voicing for that frame to `0`, overriding the provided array.

### Prompt Snippet
```text
Use `mir_eval.melody.freq_to_voicing(frequencies, voicing=None)` to normalize melody arrays. It returns a tuple `(frequencies, voiced)`. Negative frequencies are converted to positive with a voicing of 0.
```

### Common Failure Modes
- **Failing to unpack the tuple:** Assigning the result to a single variable instead of unpacking it into `res_hz, res_voicing`.
- **Assuming negative frequencies remain negative:** The function returns the absolute (positive) values for frequencies that were originally negative.
- **Assuming custom voicing overrides a frequency of 0:** If `voicing` is provided, a frequency of exactly `0` will still force the resulting voicing to `0` for that frame, regardless of the value in the `voicing` array.

### Fix Code Hint
```python
# WRONG: Assigning to a single variable
normalized_data = mir_eval.melody.freq_to_voicing(hz)

# RIGHT: Unpacking the tuple into frequencies and voicing arrays
res_hz, res_voicing = mir_eval.melody.freq_to_voicing(hz)
```

## API Test: `frequencies_to_midi`

### Signature
```python
def frequencies_to_midi(frequencies, ref_frequency=440.0)
```
_Source: source/mir_eval/multipitch.py:155_

_Source doc:_ Convert frequencies to continuous MIDI values. Parameters ---------- frequencies : list of np.ndarray Original frequency values ref_frequency : float reference frequency in Hz. Returns ------- frequencies_midi : list of np.ndarray Continuous MIDI frequency values.

### Goal
Convert a sequence of multipitch frequency arrays (in Hz) into continuous MIDI pitch values.

### Parameters
- `frequencies`: A list of `np.ndarray` objects containing the original frequency values in Hz for each time frame.
- `ref_frequency`, default `440.0`: A float representing the reference tuning frequency in Hz (where 440.0 Hz corresponds to MIDI note 69).

### Input
The caller must provide a list of NumPy arrays, where each array represents the frequencies present at a specific time frame. Because this is a multipitch evaluation utility, frames can have zero, one, or multiple frequencies. Frames with no active pitches (unvoiced frames) must be represented by empty NumPy arrays (`np.array([])`).

### Output
Returns `unspecified` — A list of `np.ndarray` objects of the same shape and length as the input, containing the converted continuous (fractional) MIDI pitch values.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

frequencies = [
    np.array([440.0]),
    np.array([]), # Unvoiced frame
    np.array([220.0, 660.0, 512.0]), # Multiple pitches
    np.array([300.0, 512.0]),
]

# Convert to continuous MIDI values
actual_midi = mir_eval.multipitch.frequencies_to_midi(frequencies)
```

### LLM Instruction Prompt
- When calling `mir_eval.multipitch.frequencies_to_midi`, the `frequencies` argument MUST be a list of `np.ndarray` objects, not a single flat array or a list of floats.
- Represent unvoiced frames (frames with no pitches) as empty NumPy arrays (`np.array([])`), not as `None` or empty Python lists.
- Call the function using its fully qualified path: `mir_eval.multipitch.frequencies_to_midi(...)`.

### Prompt Snippet
```text
To convert multipitch frequency data to MIDI pitches in `mir_eval`, use `mir_eval.multipitch.frequencies_to_midi(frequencies)`. Ensure the input is a list of `np.ndarray` objects (one array per time frame), using empty arrays (`np.array([])`) for frames with no active pitches.
```

### Common Failure Modes
- **Passing a flat list or single array**: Providing `[440.0, 220.0]` or `np.array([440.0, 220.0])` instead of a list of arrays. The function expects a list where each element corresponds to a time frame.
- **Using `None` for unvoiced frames**: Passing `[np.array([440.0]), None]` will cause iteration or math errors. Unvoiced frames must be `np.array([])`.
- **Calling without the submodule**: Attempting to call `mir_eval.frequencies_to_midi(...)` instead of `mir_eval.multipitch.frequencies_to_midi(...)`.

### Fix Code Hint
```python
# WRONG: Passing a flat list of floats or a single 1D array
# midi = mir_eval.multipitch.frequencies_to_midi([440.0, 220.0])

# RIGHT: Passing a list of np.ndarray objects (one array per frame)
midi = mir_eval.multipitch.frequencies_to_midi([
    np.array([440.0]), 
    np.array([220.0])
])

# RIGHT: Handling unvoiced frames with empty arrays
midi_with_unvoiced = mir_eval.multipitch.frequencies_to_midi([
    np.array([440.0]), 
    np.array([])
])
```

## API Test: `generate_labels`

### Signature
```python
def generate_labels(items, prefix='__')
```
_Source: source/mir_eval/util.py:53_

_Source doc:_ Given an array of items (e.g. events, intervals), create a synthetic label for each event of the form '(label prefix)(item number)' Parameters ---------- items : list-like A list or array of events or intervals prefix : str This prefix will be prepended to all synthetically generated labels (Default value = '__') Returns ------- labels : list of str Synthetically generated labels

### Goal
Generates a list of synthetic string labels for a sequence of items (such as audio events or intervals) by appending an item index to a specified prefix.

### Parameters
- `items`: A list-like collection (e.g., a list or numpy array) of events or intervals.
- `prefix`, default `'__'`: A string that will be prepended to the generated item number for all synthetic labels.

### Input
An iterable or list-like object representing the data points to be labeled. This is typically a 1D numpy array of event timestamps or a 2D numpy array of `[start, end]` intervals loaded via `mir_eval.io`. The length of this collection dictates the number of labels generated.

### Output
Returns `unspecified` — A Python list of strings containing the synthetically generated labels, formatted as `"{prefix}{index}"` (e.g., `['__0', '__1', '__2']`).

### Valid Call Patterns
```python
# Note: Call pattern inferred from signature and source path (mir_eval.util)
import mir_eval
import numpy as np

# Example with intervals
intervals = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
labels = mir_eval.util.generate_labels(intervals, prefix='segment_')
# labels == ['segment_0', 'segment_1', 'segment_2']
```

### LLM Instruction Prompt
- When evaluating MIR tasks that require label arrays (such as segment or chord evaluation) but the input data only provides timestamps or intervals, use `mir_eval.util.generate_labels(items, prefix)` to create deterministic, synthetic labels. Ensure the `items` argument is a list-like object.

### Prompt Snippet
```text
mir_eval.util.generate_labels(items, prefix='__') creates a list of synthetic string labels for each item in a list-like array of events or intervals, formatted as '(prefix)(index)'. Useful for generating dummy labels for metric evaluations.
```

### Common Failure Modes
- Passing a scalar (e.g., a single float) or `None` instead of a list-like object for `items`, which will cause iteration or length-checking errors.
- Passing an empty list or array, which will validly return an empty list of labels but might cause downstream metric evaluation functions to fail if they require at least one event/interval.

### Fix Code Hint
```python
# Ensure items is a valid list or numpy array before passing it to generate_labels
if items is not None and hasattr(items, '__len__'):
    labels = mir_eval.util.generate_labels(items, prefix='event_')
else:
    raise ValueError("items must be a list-like array of events or intervals")
```

## API Test: `goto`

### Signature
```python
def goto(reference_beats, estimated_beats, goto_threshold=0.35, goto_mu=0.2, goto_sigma=0.2)
```
_Source: source/mir_eval/beat.py:229_

_Source doc:_ Calculate Goto's score, a binary 1 or 0 depending on some specific heuristic criteria Examples -------- >>> reference_beats = mir_eval.io.load_events('reference.txt') >>> reference_beats = mir_eval.beat.trim_beats(reference_beats) >>> estimated_beats = mir_eval.io.load_events('estimated.txt') >>> estimated_beats = mir_eval.beat.trim_beats(estimated_beats) >>> goto_score = mir_eval.beat.goto(reference_beats, estimated_beats) Parameters ---------- reference_beats : np.ndarray reference beat times, in seconds estimated_beats : np.ndarray query beat times, in seconds goto_threshold : float Threshold of beat error for a beat to be "correct" (Default value = 0.35) goto_mu : float The mean of the beat errors in the continuously correct track must be less than this (Default value = 0.2) goto_sigma : float The std of the beat errors in the continuously correct track must be less than this (Default value = 0.2) Returns ------- goto_score : float Either 1.0 or 0.0 if some specific criteria are met

### Goal
Calculate Goto's score, a binary metric evaluating beat tracking accuracy based on heuristic criteria for a continuously correct track.

### Parameters
- `reference_beats`: `np.ndarray` — Reference (ground truth) beat times, in seconds.
- `estimated_beats`: `np.ndarray` — Estimated (query) beat times, in seconds.
- `goto_threshold`, default `0.35`: `float` — Threshold of beat error for a beat to be considered "correct".
- `goto_mu`, default `0.2`: `float` — The maximum allowed mean of the beat errors in the continuously correct track.
- `goto_sigma`, default `0.2`: `float` — The maximum allowed standard deviation of the beat errors in the continuously correct track.

### Input
1D numpy arrays containing beat timestamps in seconds. In standard MIR evaluation workflows, these arrays are typically loaded from repository-format text files using `mir_eval.io.load_events()` and preprocessed using `mir_eval.beat.trim_beats()` to crop out early events (e.g., beats before 5 seconds) prior to evaluation.

### Output
Returns `unspecified` — A `float` value of either `1.0` or `0.0`, indicating whether the estimated beats meet Goto's specific heuristic criteria for correctness.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example 1: From the project's test suite using deterministic in-memory arrays
reference_beats = np.arange(100)
estimated_beats = np.append(np.arange(80), np.arange(80, 100) + 0.2)
goto_score = mir_eval.beat.goto(reference_beats, estimated_beats)
assert goto_score == 1.0

# Example 2: Standard workflow with I/O and preprocessing (from source doc)
# reference_beats = mir_eval.io.load_events('reference.txt')
# reference_beats = mir_eval.beat.trim_beats(reference_beats)
# estimated_beats = mir_eval.io.load_events('estimated.txt')
# estimated_beats = mir_eval.beat.trim_beats(estimated_beats)
# goto_score = mir_eval.beat.goto(reference_beats, estimated_beats)
```

### LLM Instruction Prompt
- When evaluating beat tracking using `mir_eval.beat.goto`, ensure the inputs are 1D numpy arrays of timestamps in seconds.
- Always preprocess the raw loaded events with `mir_eval.beat.trim_beats()` before passing them to `goto()` to adhere to standard MIR evaluation practices (cropping early beats).
- Expect a binary `float` return value (`1.0` or `0.0`), not a continuous score or a dictionary.

### Prompt Snippet
```text
Use `mir_eval.beat.goto(reference_beats, estimated_beats)` to compute Goto's score. Both arguments must be 1D numpy arrays of beat times in seconds. Remember to apply `mir_eval.beat.trim_beats()` to both arrays before evaluation to remove early events. The function returns a float (1.0 or 0.0).
```

### Common Failure Modes
- Passing raw lists instead of `np.ndarray` objects.
- Failing to trim the first 5 seconds of beats using `mir_eval.beat.trim_beats()`, which can skew the heuristic evaluation by including unstable early beat estimates.
- Expecting a continuous score between 0.0 and 1.0; `goto` is strictly binary (1.0 or 0.0).

### Fix Code Hint
```python
import mir_eval

# Load events from text files
ref_beats = mir_eval.io.load_events('reference.txt')
est_beats = mir_eval.io.load_events('estimated.txt')

# Precondition: Trim early beats (typically first 5 seconds)
ref_beats_trimmed = mir_eval.beat.trim_beats(ref_beats)
est_beats_trimmed = mir_eval.beat.trim_beats(est_beats)

# Compute Goto's score
score = mir_eval.beat.goto(ref_beats_trimmed, est_beats_trimmed)
```

## API Test: `has_kwargs`

### Signature
```python
def has_kwargs(function)
```
_Source: source/mir_eval/util.py:838_

_Source doc:_ Determine whether a function has ``**kwargs``. Parameters ---------- function : callable The function to test Returns ------- True if function accepts arbitrary keyword arguments. False otherwise.

### Goal
Determine whether a given callable function accepts arbitrary keyword arguments (`**kwargs`).

### Parameters
- `function`: A Python callable (such as a function or method) to be inspected.

### Input
A valid Python callable object. The function can have any signature (positional arguments, default arguments, `*args`, or `**kwargs`). 

### Output
Returns `unspecified` — A boolean value: `True` if the provided function accepts arbitrary keyword arguments (`**kwargs`), and `False` otherwise.

### Valid Call Patterns
```python
import mir_eval

def function_without_kwargs(a, b=5, *args):
    return None

def function_with_kwargs(a, **kwargs):
    return None

# Returns False
mir_eval.util.has_kwargs(function_without_kwargs)

# Returns True
mir_eval.util.has_kwargs(function_with_kwargs)
```

### LLM Instruction Prompt
- Use `mir_eval.util.has_kwargs(function)` to programmatically inspect a callable's signature.
- Remember that it strictly checks for `**kwargs` (arbitrary keyword arguments); it will return `False` for functions that only have standard default keyword arguments (e.g., `def f(x=1):`) or arbitrary positional arguments (`*args`).
- Ensure the argument passed is the callable itself, not the evaluated result of the callable.

### Prompt Snippet
```text
To check if a function accepts arbitrary keyword arguments in mir_eval, use `mir_eval.util.has_kwargs(func)`. It returns True if the function signature includes `**kwargs`, and False for standard positional, default, or `*args` signatures.
```

### Common Failure Modes
- **Passing a non-callable object**: Passing a string, integer, or the evaluated result of a function (e.g., `has_kwargs(my_func())` instead of `has_kwargs(my_func)`) will cause an inspection failure or `TypeError`.
- **Confusing default arguments with `**kwargs`**: Assuming `has_kwargs` returns `True` for functions with default arguments like `def f(a=5):`. It only returns `True` for actual `**kwargs` catch-alls.

### Fix Code Hint
```python
# INCORRECT: Passing the result of a function call or a non-callable
# result = mir_eval.util.has_kwargs(my_function())

# CORRECT: Pass the callable object directly
result = mir_eval.util.has_kwargs(my_function)
```

## API Test: `hierarchy`

### Signature
```python
def hierarchy(intervals_hier, labels_hier, levels=None, ax=None, **kwargs)
```
_Source: source/mir_eval/display.py:498_

_Source doc:_ Plot a hierarchical segmentation Parameters ---------- intervals_hier : list of np.ndarray A list of segmentation intervals.  Each element should be an n-by-2 array of segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. Segmentations should be ordered by increasing specificity. labels_hier : list of list-like A list of segmentation labels.  Each element should be a list of labels for the corresponding element in `intervals_hier`. levels : list of string Each element ``levels[i]`` is a label for the ```i`` th segmentation. This is used in the legend to denote the levels in a segment hierarchy. ax : matplotlib.pyplot.axes An axis handle on which to draw the intervals. If none is provided, a new set of axes is created. **kwargs Additional keyword arguments to `labeled_intervals`. Returns ------- ax : matplotlib.pyplot.axes._subplots.AxesSubplot A handle to the (possibly constructed) plot axes

### Goal
Plot a hierarchical segmentation of audio or music, displaying multiple levels of segment intervals and their corresponding labels on a matplotlib axis.

### Parameters
- `intervals_hier`: A list of segmentation intervals. Each element must be an n-by-2 numpy array of segment intervals (start and end times). The list should be ordered by increasing specificity.
- `labels_hier`: A list of list-like objects containing segmentation labels. Each element is a list of labels corresponding to the intervals in the matching element of `intervals_hier`.
- `levels`, default `None`: A list of strings where the *i*-th element is a label for the *i*-th segmentation level. This is used to denote the hierarchy levels in the plot legend.
- `ax`, default `None`: An existing `matplotlib.pyplot.axes` handle on which to draw the intervals. If `None`, a new set of axes is created.
- `**kwargs`: Additional keyword arguments passed through to the underlying `labeled_intervals` plotting function.

### Input
The caller must provide lists of intervals and labels, typically loaded from repository-format annotation files (e.g., `.lab` files) using `mir_eval.io.load_labeled_intervals`. The intervals must be n-by-2 numpy arrays. The segmentations in the lists must be ordered by increasing specificity (e.g., from coarse large-scale structure to fine-grained small-scale structure). If this function is used in an automated test suite, the environment must be configured to keep display tests headless without network or audio-device access.

### Output
Returns `unspecified` — A `matplotlib.pyplot.axes._subplots.AxesSubplot` handle to the (possibly newly constructed) plot axes containing the drawn hierarchical intervals.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval
from mir_eval.io import load_labeled_intervals

# Configure headless plotting for tests
plt.switch_backend('Agg')
plt.figure()

# Load hierarchical segment data (e.g., coarse and fine annotations)
int0, lab0 = load_labeled_intervals("data/hierarchy/ref00.lab")
int1, lab1 = load_labeled_intervals("data/hierarchy/ref01.lab")

# Plot reference and estimate with a common label set
ax = mir_eval.display.hierarchy(
    [int0, int1], 
    [lab0, lab1], 
    levels=["Large", "Small"]
)

plt.legend(loc="upper right")
```

### LLM Instruction Prompt
- When calling `mir_eval.display.hierarchy`, ensure `intervals_hier` is a *list* of n-by-2 numpy arrays and `labels_hier` is a *list* of label lists. 
- Order the lists by increasing specificity. 
- If generating tests, ensure matplotlib is configured to run headlessly (e.g., using the `Agg` backend) to satisfy project constraints.

### Prompt Snippet
```text
`mir_eval.display.hierarchy(intervals_hier, labels_hier, levels=None, ax=None, **kwargs)` plots hierarchical segmentations. `intervals_hier` must be a list of n-by-2 numpy arrays ordered by increasing specificity, and `labels_hier` must be a corresponding list of label lists. Returns a matplotlib AxesSubplot.
```

### Common Failure Modes
- Passing a single n-by-2 numpy array instead of a *list* of arrays for `intervals_hier`.
- Mismatched list lengths between `intervals_hier` and `labels_hier`.
- Ordering the hierarchy incorrectly (must be increasing specificity, not decreasing).
- Running display code in a CI environment without a headless backend configured, causing matplotlib to attempt to open a window and crash.

### Fix Code Hint
```python
# WRONG: Passing single arrays directly
# mir_eval.display.hierarchy(int0, lab0)

# RIGHT: Wrapping single levels in lists, though typically multiple levels are passed
mir_eval.display.hierarchy([int0], [lab0])

# RIGHT: Passing multiple levels ordered by increasing specificity
mir_eval.display.hierarchy([coarse_intervals, fine_intervals], [coarse_labels, fine_labels])
```

## API Test: `hz2cents`

### Signature
```python
def hz2cents(freq_hz, base_frequency=10.0)
```
_Source: source/mir_eval/melody.py:138_

_Source doc:_ Convert an array of frequency values in Hz to cents. 0 values are left in place. Parameters ---------- freq_hz : np.ndarray Array of frequencies in Hz. base_frequency : float Base frequency for conversion. (Default value = 10.0)

### Goal
Converts an array of frequency values in Hertz to cents relative to a base frequency, safely preserving `0.0` values (typically representing unvoiced frames).

### Parameters
- `freq_hz`: `np.ndarray` representing an array of frequencies in Hz.
- `base_frequency`, default `10.0`: `float` representing the base frequency in Hz used for the cents conversion.

### Input
A NumPy array of frequency values (`np.ndarray`). Unvoiced or silent frames should be represented as exactly `0.0`, as the function explicitly checks for and leaves `0` values in place to avoid logarithmic math errors.

### Output
Returns `unspecified` — A NumPy array (`np.ndarray`) of the same shape as `freq_hz`, containing the converted frequency values in cents.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# 0.0 values are safely preserved as 0.0
hz = np.array([0.0, 10.0, 5.0, 320.0, 1420.31238974231])
cents = mir_eval.melody.hz2cents(hz)
```

### LLM Instruction Prompt
- When converting melody or pitch contours from Hz to cents using `mir_eval.melody.hz2cents`, ensure the input is a NumPy array. Represent unvoiced/silent frames as exactly `0.0` Hz, as the function explicitly preserves `0.0` values to avoid math domain errors. Do not invent a `mir_eval.hz2cents` root import; it must be accessed via the `mir_eval.melody` submodule.

### Prompt Snippet
```text
mir_eval.melody.hz2cents(freq_hz, base_frequency=10.0): Converts a NumPy array of frequencies in Hz to cents. 0.0 Hz values (unvoiced frames) are safely left as 0.0.
```

### Common Failure Modes
- **Incorrect Import Path**: Attempting to call `mir_eval.hz2cents()` directly instead of `mir_eval.melody.hz2cents()`.
- **Using `NaN` or Negative Values for Unvoiced Frames**: Passing `np.nan` or negative numbers to represent unvoiced frames instead of `0.0`. The function specifically targets `0` for safe handling; other non-positive values will trigger logarithmic math warnings or propagate `NaN`s.

### Fix Code Hint
```python
import numpy as np
import mir_eval

# If your unvoiced frames are represented as NaN, convert them to 0.0 first
freq_hz = np.array([np.nan, 440.0, 880.0])
freq_hz = np.nan_to_num(freq_hz, nan=0.0)

# Now safely convert to cents
cents = mir_eval.melody.hz2cents(freq_hz)
```

## API Test: `hz_to_midi`

### Signature
```python
def hz_to_midi(freqs)
```
_Source: source/mir_eval/util.py:913_

_Source doc:_ Convert Hz to MIDI numbers Parameters ---------- freqs : number or ndarray Frequency/frequencies in Hz Returns ------- midi : number or ndarray MIDI note numbers corresponding to input frequencies. Note that these may be fractional.

### Goal
Convert acoustic frequencies in Hertz (Hz) to their corresponding MIDI note numbers.

### Parameters
- `freqs`: A numeric value or NumPy `ndarray` representing the frequency or frequencies in Hz.

### Input
A single number (float or int) or a NumPy `ndarray` of numeric frequency values in Hz. If loading from a text file, the data must be parsed into numeric types or arrays before being passed to this function.

### Output
Returns `unspecified` — A numeric value or NumPy `ndarray` representing the MIDI note numbers corresponding to the input frequencies. Note that these values may be fractional (e.g., for microtonal pitches or frequencies that do not perfectly align with standard equal-tempered MIDI notes).

### Valid Call Patterns
```python
import mir_eval
import matplotlib.pyplot as plt

# Example derived from the project's test suite
ref_t, ref_p = mir_eval.io.load_valued_intervals("data/transcription/ref04.txt")
est_t, est_p = mir_eval.io.load_valued_intervals("data/transcription/est04.txt")

# Convert Hz arrays to MIDI note numbers
ref_midi = mir_eval.util.hz_to_midi(ref_p)
est_midi = mir_eval.util.hz_to_midi(est_p)

# The fractional MIDI values can be passed directly to display functions
mir_eval.display.piano_roll(ref_t, midi=ref_midi, label="Reference", alpha=0.5)
```

### LLM Instruction Prompt
- When converting frequencies (Hz) to MIDI note numbers for evaluation or display (such as `mir_eval.display.piano_roll`), use `mir_eval.util.hz_to_midi(freqs)`. Do not assume the output will be integers; the function returns fractional MIDI note numbers to preserve exact pitch information.

### Prompt Snippet
```text
Use `mir_eval.util.hz_to_midi(freqs)` to convert an array of frequencies in Hz to MIDI note numbers. The output may contain fractional values, which are fully supported by `mir_eval.display` functions.
```

### Common Failure Modes
- **Assuming integer outputs:** Callers might expect strict integer MIDI note numbers and fail if they use the output as array indices without rounding/casting. The output is fractional.
- **Passing unparsed strings:** Passing raw string arrays from custom file readers instead of numeric NumPy arrays.
- **Incorrect module namespace:** Attempting to call `mir_eval.hz_to_midi` instead of the correct `mir_eval.util.hz_to_midi`.

### Fix Code Hint
```python
# Incorrect: assuming integer output for indexing or strict MIDI processing
midi_notes = mir_eval.util.hz_to_midi(freqs)
# note_counts[midi_notes] += 1  # This will raise an IndexError/TypeError

# Correct: round and cast to integer if strict MIDI note integers are required downstream
midi_notes_int = np.round(mir_eval.util.hz_to_midi(freqs)).astype(int)

# Correct: pass fractional MIDI directly to mir_eval display functions
mir_eval.display.piano_roll(times, midi=mir_eval.util.hz_to_midi(freqs))
```

## API Test: `index_labels`

### Signature
```python
def index_labels(labels, case_sensitive=False)
```
_Source: source/mir_eval/util.py:14_

_Source doc:_ Convert a list of string identifiers into numerical indices. Parameters ---------- labels : list of strings, shape=(n,) A list of annotations, e.g., segment or chord labels from an annotation file. case_sensitive : bool Set to True to enable case-sensitive label indexing (Default value = False) Returns ------- indices : list, shape=(n,) Numerical representation of ``labels`` index_to_label : dict Mapping to convert numerical indices back to labels. ``labels[i] == index_to_label[indices[i]]``

### Goal
Convert a list of string identifiers (such as segment or chord labels) into numerical indices and provide a reverse-mapping dictionary.

### Parameters
- `labels`: A list of strings, shape=(n,), representing a sequence of annotations (e.g., segment or chord labels loaded from an annotation file).
- `case_sensitive`, default `False`: A boolean flag. Set to `True` to enable case-sensitive label indexing (treating "Chorus" and "chorus" as distinct labels).

### Input
A list or 1D array of string annotations, typically parsed from a repository-format text file using `mir_eval.io` routines. If `case_sensitive` is `False` (the default), the elements must support case-conversion operations (i.e., they must be strings).

### Output
Returns `unspecified` — A tuple containing two elements:
1. `indices`: A list of shape `(n,)` containing the numerical representation of the input `labels`.
2. `index_to_label`: A dictionary mapping the numerical indices back to the original string labels, such that `labels[i] == index_to_label[indices[i]]`.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
import mir_eval

labels = ["verse", "chorus", "Verse", "bridge"]
# By default, case_sensitive=False, so "verse" and "Verse" receive the same index
indices, index_to_label = mir_eval.util.index_labels(labels)

# With case sensitivity enabled
strict_indices, strict_mapping = mir_eval.util.index_labels(labels, case_sensitive=True)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.index_labels`, you MUST unpack the two return values: the list of numerical indices and the index-to-label mapping dictionary.
- Ensure the `labels` input is a sequence of strings.
- Use `case_sensitive=True` if the evaluation requires distinguishing between identically spelled labels with different capitalization.

### Prompt Snippet
```text
`mir_eval.util.index_labels(labels, case_sensitive=False)`: Converts a list of string identifiers (shape=(n,)) into numerical indices. Returns a tuple `(indices, index_to_label)` where `indices` is the numerical list and `index_to_label` is a dict mapping indices back to strings.
```

### Common Failure Modes
- **Failing to unpack the return value**: Assigning the result to a single variable and attempting to use it as a list of indices will cause type errors, as the function returns a tuple of `(list, dict)`.
- **Passing non-string elements**: Providing a list of integers or mixed types when `case_sensitive=False` may cause an `AttributeError` if the function attempts to normalize the casing of non-string objects.

### Fix Code Hint
```python
# WRONG: Assigning to a single variable
# indices = mir_eval.util.index_labels(labels)

# CORRECT: Unpack both the indices and the mapping dictionary, ensuring inputs are strings
string_labels = [str(label) for label in labels]
indices, index_to_label = mir_eval.util.index_labels(string_labels, case_sensitive=False)
```

## API Test: `information_gain`

### Signature
```python
def information_gain(reference_beats, estimated_beats, bins=41)
```
_Source: source/mir_eval/beat.py:585_

_Source doc:_ Get the information gain - K-L divergence of the beat error histogram to a uniform histogram Examples -------- >>> reference_beats = mir_eval.io.load_events('reference.txt') >>> reference_beats = mir_eval.beat.trim_beats(reference_beats) >>> estimated_beats = mir_eval.io.load_events('estimated.txt') >>> estimated_beats = mir_eval.beat.trim_beats(estimated_beats) >>> information_gain = mir_eval.beat.information_gain(reference_beats, estimated_beats) Parameters ---------- reference_beats : np.ndarray reference beat times, in seconds estimated_beats : np.ndarray query beat times, in seconds bins : int Number of bins in the beat error histogram (Default value = 41) Returns ------- information_gain_score : float Entropy of beat error histogram

### Goal
Computes the information gain (Kullback-Leibler divergence) of the beat error histogram compared to a uniform histogram to evaluate beat tracking accuracy.

### Parameters
- `reference_beats`: A 1D `np.ndarray` of reference (ground truth) beat times, measured in seconds.
- `estimated_beats`: A 1D `np.ndarray` of estimated (query) beat times, measured in seconds.
- `bins`, default `41`: An `int` specifying the number of bins to use in the beat error histogram.

### Input
1D numpy arrays of beat timestamps in seconds. It is a standard precondition in `mir_eval` to preprocess these arrays by cropping out early beats (typically those before 5 seconds) using `mir_eval.beat.trim_beats` prior to evaluation. Data is typically loaded from repository-format text files using `mir_eval.io.load_events`.

### Output
Returns `unspecified` — A `float` representing the information gain score (the entropy of the beat error histogram).

### Valid Call Patterns
```python
import mir_eval

# Example derived from the source documentation
reference_beats = mir_eval.io.load_events('reference.txt')
reference_beats = mir_eval.beat.trim_beats(reference_beats)

estimated_beats = mir_eval.io.load_events('estimated.txt')
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)

information_gain_score = mir_eval.beat.information_gain(reference_beats, estimated_beats)
```

### LLM Instruction Prompt
- When evaluating beat tracking with `mir_eval.beat.information_gain`, ensure inputs are 1D numpy arrays of timestamps in seconds. Always preprocess both reference and estimated beats using `mir_eval.beat.trim_beats` before computing the metric to remove early events. Do not invent dictionary keys or assume this function returns a dictionary; it returns a single `float`.

### Prompt Snippet
```text
`mir_eval.beat.information_gain(reference_beats, estimated_beats, bins=41)` computes the K-L divergence of the beat error histogram to a uniform histogram. Inputs must be 1D numpy arrays of beat times in seconds, typically preprocessed with `mir_eval.beat.trim_beats`. Returns a float.
```

### Common Failure Modes
- **Missing Preprocessing:** Failing to call `mir_eval.beat.trim_beats` on the inputs, which includes early beats in the evaluation and skews the metric.
- **Incorrect Data Types:** Passing raw file paths or unparsed strings instead of `np.ndarray` objects. Files must first be parsed using `mir_eval.io.load_events`.
- **Multi-dimensional Arrays:** Passing 2D arrays (e.g., intervals) instead of 1D arrays of discrete beat timestamps.

### Fix Code Hint
```python
# FIX: Load events and trim early beats before calculating information gain
ref_beats = mir_eval.io.load_events("reference_beats.txt")
est_beats = mir_eval.io.load_events("estimated_beats.txt")

# Trim beats (removes beats before 5s by default)
ref_beats_trimmed = mir_eval.beat.trim_beats(ref_beats)
est_beats_trimmed = mir_eval.beat.trim_beats(est_beats)

# Compute metric
score = mir_eval.beat.information_gain(ref_beats_trimmed, est_beats_trimmed)
```

## API Test: `interpolate_intervals`

### Signature
```python
def interpolate_intervals(intervals, labels, time_points, fill_value=None)
```
_Source: source/mir_eval/util.py:118_

_Source doc:_ Assign labels to a set of points in time given a set of intervals. Time points that do not lie within an interval are mapped to `fill_value`. Parameters ---------- intervals : np.ndarray, shape=(n, 2) An array of time intervals, as returned by :func:`mir_eval.io.load_intervals()`. The ``i`` th interval spans time ``intervals[i, 0]`` to ``intervals[i, 1]``. Intervals are assumed to be disjoint. labels : list, shape=(n,) The annotation for each interval time_points : array_like, shape=(m,) Points in time to assign labels.  These must be in non-decreasing order. fill_value : type(labels[0]) Object to use for the label with out-of-range time points. (Default value = None) Returns ------- aligned_labels : list Labels corresponding to the given time points. Raises ------ ValueError If `time_points` is not in non-decreasing order.

### Goal
Assign labels to a sequence of time points based on a set of disjoint time intervals, mapping out-of-range or gap points to a specified fill value.

### Parameters
- `intervals`: An `np.ndarray` of shape `(n, 2)` representing time intervals, where the `i`th interval spans from `intervals[i, 0]` to `intervals[i, 1]`.
- `labels`: A `list` of shape `(n,)` containing the annotation corresponding to each interval.
- `time_points`: An `array_like` of shape `(m,)` representing the points in time to assign labels.
- `fill_value`, default `None`: The object to use for the label when a time point falls outside of all provided intervals (e.g., in gaps or out of bounds). Typically matches the type of the elements in `labels`.

### Input
- `intervals` must be disjoint (non-overlapping).
- `time_points` must be sorted in non-decreasing order.
- Gaps between intervals are explicitly supported by the function and will be mapped to `fill_value`.

### Output
Returns `unspecified` — A `list` of length `m` containing the aligned labels corresponding to each time point in `time_points`.

### Valid Call Patterns
```python
import numpy as np
from mir_eval import util

labels = ["a", "b", "c"]
# Intervals with gaps between them
intervals = np.array([[0.5, 1.0], [1.5, 2.0], [2.5, 3.0]])
time_points = [0.0, 0.75, 1.25, 1.75, 2.25, 2.75, 3.5]

# Interpolate with gaps, using "N" as the fill_value
aligned_labels = util.interpolate_intervals(intervals, labels, time_points, "N")
# aligned_labels == ["N", "a", "N", "b", "N", "c", "N"]
```

### LLM Instruction Prompt
- When using `mir_eval.util.interpolate_intervals`, you MUST ensure that `time_points` is sorted in non-decreasing order before calling the function.
- Ensure `intervals` are disjoint; overlapping intervals violate the function's preconditions.
- Gaps between intervals are supported and will be filled with `fill_value`.

### Prompt Snippet
```text
mir_eval.util.interpolate_intervals(intervals, labels, time_points, fill_value=None): Assigns labels to time_points based on disjoint intervals. time_points MUST be sorted in non-decreasing order. Gaps are filled with fill_value.
```

### Common Failure Modes
- Passing unsorted `time_points` raises a `ValueError`.
- Passing overlapping intervals leads to undefined behavior, as the function assumes intervals are disjoint.

### Fix Code Hint
```python
# Sort time_points to ensure they are in non-decreasing order before interpolating
time_points = np.sort(time_points)
aligned_labels = util.interpolate_intervals(intervals, labels, time_points, fill_value="None")
```

## API Test: `intersect_files`

### Signature
```python
def intersect_files(flist1, flist2)
```
_Source: source/mir_eval/util.py:427_

_Source doc:_ Return the intersection of two sets of filepaths, based on the file name (after the final '/') and ignoring the file extension. Examples -------- >>> flist1 = ['/a/b/abc.lab', '/c/d/123.lab', '/e/f/xyz.lab'] >>> flist2 = ['/g/h/xyz.npy', '/i/j/123.txt', '/k/l/456.lab'] >>> sublist1, sublist2 = mir_eval.util.intersect_files(flist1, flist2) >>> print sublist1 ['/e/f/xyz.lab', '/c/d/123.lab'] >>> print sublist2 ['/g/h/xyz.npy', '/i/j/123.txt'] Parameters ---------- flist1 : list first list of filepaths flist2 : list second list of filepaths Returns ------- sublist1 : list subset of filepaths with matching stems from ``flist1`` sublist2 : list corresponding filepaths from ``flist2``

### Goal
Finds the intersection of two lists of file paths by matching their base file names (stems) while ignoring directories and file extensions, which is useful for pairing reference and estimated annotation files for batch evaluation.

### Parameters
- `flist1`: First list of filepaths (strings), typically representing reference (ground truth) files.
- `flist2`: Second list of filepaths (strings), typically representing estimated (system output) files.

### Input
Two lists of strings representing file paths. The paths can reside in different directories and possess different file extensions (e.g., `.lab` vs `.npy`). The function relies on string parsing (specifically looking for the final `/` and ignoring the extension) to extract the file stem for matching.

### Output
Returns `unspecified` — A tuple of two lists: `(sublist1, sublist2)`. `sublist1` contains the subset of original filepaths from `flist1` that have a matching stem in `flist2`. `sublist2` contains the corresponding original filepaths from `flist2`.

### Valid Call Patterns
```python
from mir_eval import util

flist1 = ["/a/b/abc.lab", "/c/d/123.lab", "/e/f/xyz.lab"]
flist2 = ["/g/h/xyz.npy", "/i/j/123.txt", "/k/l/456.lab"]
sublist1, sublist2 = util.intersect_files(flist1, flist2)

assert sublist1 == ["/e/f/xyz.lab", "/c/d/123.lab"]
assert sublist2 == ["/g/h/xyz.npy", "/i/j/123.txt"]
```

### LLM Instruction Prompt
- When preparing batches of reference and estimated MIR annotation files for evaluation, use `mir_eval.util.intersect_files(flist1, flist2)` to align them. You MUST unpack the return value into two separate variables, as the function returns a tuple of two lists containing the filtered original paths, not a single list of stems. Pass lists of strings, as the internal logic parses paths based on the `/` character.

### Prompt Snippet
```text
Use `mir_eval.util.intersect_files(ref_files, est_files)` to pair annotation files by their filename stems, ignoring directories and extensions. Unpack the result into two lists: `matched_refs, matched_ests = ...`.
```

### Common Failure Modes
- **Assigning to a single variable:** Assuming the function returns a single list of intersected stems or a single list of tuples, resulting in a tuple-unpacking error or logic bugs downstream.
- **Passing `pathlib.Path` objects:** While `mir_eval.io` functions often accept `os.PathLike` objects, `intersect_files` explicitly documents parsing based on the string character `/`. Passing `Path` objects (especially on Windows where the separator is `\`) may fail to match stems correctly. Always pass lists of strings.
- **Assuming order preservation:** The output lists are not guaranteed to maintain the original sorting order of `flist1` or `flist2`, though the elements at index `i` in `sublist1` and `sublist2` will correctly correspond to the same stem.

### Fix Code Hint
```python
# WRONG: Assigning to a single variable or passing Path objects
matched_files = mir_eval.util.intersect_files(path_list_1, path_list_2)

# RIGHT: Unpacking into two lists and ensuring inputs are strings
str_list_1 = [str(p) for p in path_list_1]
str_list_2 = [str(p) for p in path_list_2]
matched_refs, matched_ests = mir_eval.util.intersect_files(str_list_1, str_list_2)
```

## API Test: `intervals_to_boundaries`

### Signature
```python
def intervals_to_boundaries(intervals, q=5)
```
_Source: source/mir_eval/util.py:221_

_Source doc:_ Convert interval times into boundaries. Parameters ---------- intervals : np.ndarray, shape=(n_events, 2) Array of interval start and end-times q : int Number of decimals to round to. (Default value = 5) Returns ------- boundaries : np.ndarray Interval boundary times, including the end of the final interval

### Goal
Convert a sequence of interval start and end times into a single 1D array of boundary times.

### Parameters
- `intervals`: A 2D numpy array (`np.ndarray`) of shape `(n_events, 2)` representing the start and end times of each interval.
- `q`, default `5`: An integer (`int`) specifying the number of decimal places to round the resulting boundary times to.

### Input
A 2D numpy array of numeric time values (typically in seconds) with exactly two columns (start and end times). The caller must ensure the input is a valid numpy array of shape `(n_events, 2)`.

### Output
Returns `unspecified` — A 1D numpy array (`np.ndarray`) containing the interval boundary times, rounded to `q` decimals, including the end time of the final interval.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
import numpy as np
import mir_eval

intervals = np.array([[0.0, 1.0], [1.0, 2.5], [2.5, 4.0]])
boundaries = mir_eval.util.intervals_to_boundaries(intervals, q=5)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.intervals_to_boundaries`, ensure the `intervals` argument is a 2D numpy array of shape `(n_events, 2)`. The function will return a 1D array of boundaries rounded to `q` decimal places (default 5). Do not pass 1D arrays or unstructured lists.

### Prompt Snippet
```text
mir_eval.util.intervals_to_boundaries(intervals, q=5): Converts an (n_events, 2) numpy array of interval start and end times into a 1D array of boundary times, rounding to `q` decimals.
```

### Common Failure Modes
- Passing a 1D array or a flat list instead of a 2D numpy array of shape `(n_events, 2)`, causing shape mismatch errors during processing.
- Passing non-numeric data types that cannot be rounded using numpy operations.

### Fix Code Hint
```python
# Ensure intervals is a 2D numpy array with 2 columns before calling
import numpy as np
import mir_eval

intervals = np.asarray(raw_intervals, dtype=float)
if intervals.ndim == 1 and intervals.size % 2 == 0:
    intervals = intervals.reshape(-1, 2)

boundaries = mir_eval.util.intervals_to_boundaries(intervals)
```

## API Test: `intervals_to_durations`

### Signature
```python
def intervals_to_durations(intervals)
```
_Source: source/mir_eval/util.py:892_

_Source doc:_ Convert an array of n intervals to their n durations. Parameters ---------- intervals : np.ndarray, shape=(n, 2) An array of time intervals, as returned by :func:`mir_eval.io.load_intervals()`. The ``i`` th interval spans time ``intervals[i, 0]`` to ``intervals[i, 1]``. Returns ------- durations : np.ndarray, shape=(n,) Array of the duration of each interval.

### Goal
Convert an array of $n$ time intervals into an array of their corresponding $n$ durations for music information retrieval evaluation.

### Parameters
- `intervals`: A 2D numpy array of shape `(n, 2)` representing time intervals, where the $i$-th interval spans from `intervals[i, 0]` to `intervals[i, 1]`.

### Input
A numpy array of shape `(n, 2)` containing numeric time values (typically seconds). This is commonly the output of `mir_eval.io.load_intervals()`. The start time of each interval should be less than or equal to its end time to ensure non-negative durations.

### Output
Returns `unspecified` — A 1D numpy array of shape `(n,)` containing the computed duration of each interval.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Inferred from signature (not verified)
intervals = np.array([[0.0, 1.5], [1.5, 4.0], [4.0, 5.5]])
durations = mir_eval.util.intervals_to_durations(intervals)
```

### LLM Instruction Prompt
- When calculating durations from time intervals in `mir_eval`, use `mir_eval.util.intervals_to_durations(intervals)`. Ensure the input is a 2D numpy array of shape `(n, 2)`.

### Prompt Snippet
```text
Use `mir_eval.util.intervals_to_durations(intervals)` to convert an `(n, 2)` numpy array of start and end times into an `(n,)` array of durations.
```

### Common Failure Modes
- Passing a 1D array or a standard Python list instead of a 2D `(n, 2)` numpy array, causing shape mismatch errors.
- Passing intervals where the start time is greater than the end time (`intervals[i, 0] > intervals[i, 1]`), which will silently produce negative durations that may violate preconditions of downstream metric evaluations.

### Fix Code Hint
```python
import numpy as np
import mir_eval

# Ensure intervals is a 2D numpy array of shape (n, 2)
intervals = np.asarray(raw_intervals)
if intervals.ndim == 1 and intervals.shape[0] == 2:
    intervals = intervals.reshape(1, 2)

durations = mir_eval.util.intervals_to_durations(intervals)
```

## API Test: `intervals_to_samples`

### Signature
```python
def intervals_to_samples(intervals, labels, offset=0, sample_size=0.1, fill_value=None)
```
_Source: source/mir_eval/util.py:74_

_Source doc:_ Convert an array of labeled time intervals to annotated samples. Parameters ---------- intervals : np.ndarray, shape=(n, d) An array of time intervals, as returned by :func:`mir_eval.io.load_intervals()` or :func:`mir_eval.io.load_labeled_intervals()`. The ``i`` th interval spans time ``intervals[i, 0]`` to ``intervals[i, 1]``. labels : list, shape=(n,) The annotation for each interval offset : float > 0 Phase offset of the sampled time grid (in seconds) (Default value = 0) sample_size : float > 0 duration of each sample to be generated (in seconds) (Default value = 0.1) fill_value : type(labels[0]) Object to use for the label with out-of-range time points. (Default value = None) Returns ------- sample_times : list list of sample times sample_labels : list array of labels for each generated sample Notes ----- Intervals will be rounded down to the nearest multiple of ``sample_size``.

### Goal
Convert an array of continuous, labeled time intervals (such as chords or segments) into a sequence of discrete, uniformly spaced annotated samples on a time grid.

### Parameters
- `intervals`: A 2D `np.ndarray` of shape `(n, d)` (typically `d=2`) representing time intervals in seconds, where the `i`th interval spans from `intervals[i, 0]` to `intervals[i, 1]`.
- `labels`: A `list` of shape `(n,)` containing the annotation corresponding to each interval.
- `offset`, default `0`: A float `> 0` representing the phase offset of the sampled time grid in seconds.
- `sample_size`, default `0.1`: A float `> 0` representing the duration of each generated sample (the step size of the grid) in seconds.
- `fill_value`, default `None`: An object (ideally of the same type as the elements in `labels`) to use as the label for sampled time points that fall outside the provided intervals.

### Input
The caller must provide `intervals` as a 2D numpy array and `labels` as a Python list of the same length `n`. These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_labeled_intervals()`. The `offset` and `sample_size` must be positive floats. Note that intervals will be rounded down to the nearest multiple of `sample_size`.

### Output
Returns `unspecified` — A tuple containing two lists: `(sample_times, sample_labels)`. `sample_times` is a list of the generated sample times in seconds, and `sample_labels` is a list of the corresponding labels at each sampled time.

### Valid Call Patterns
```python
import numpy as np
from mir_eval import util

labels = list("abc")
# Create intervals: [0.0, 1.0], [1.0, 2.0], [2.0, 3.0]
intervals = np.array([(n, n + 1.0) for n in range(len(labels))])

# Sample the intervals at 0.5s steps with no offset
sample_times, sample_labels = util.intervals_to_samples(
    intervals, labels, offset=0, sample_size=0.5, fill_value="N"
)
# sample_times == [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
# sample_labels == ["a", "a", "b", "b", "c", "c"]
```

### LLM Instruction Prompt
- When calling `mir_eval.util.intervals_to_samples`, ensure `intervals` is a 2D `numpy.ndarray` and `labels` is a `list`. Do not pass a list of lists for `intervals`.
- Ensure `intervals` and `labels` have the exact same length `n`.
- Provide a `fill_value` that matches the data type of the items in `labels` (e.g., a string like `"N"` or `"No Chord"` if `labels` contains strings) to handle out-of-range time points gracefully.

### Prompt Snippet
```text
Use `mir_eval.util.intervals_to_samples` to convert the loaded continuous intervals and labels into a discrete time series. Use a `sample_size` of 0.1 seconds and set `fill_value` to a string indicating silence or no-event. Ensure the intervals are passed as a numpy array.
```

### Common Failure Modes
- Passing a standard Python list instead of a `numpy.ndarray` for `intervals`, which can cause indexing errors since the function expects `intervals[i, 0]`.
- Providing `intervals` and `labels` of different lengths, leading to alignment errors or `IndexError`.
- Passing negative values for `offset` or `sample_size`.
- Forgetting that the function returns a tuple of two lists, and attempting to assign the result to a single variable without unpacking, leading to downstream type errors.

### Fix Code Hint
```python
# BAD: Passing a list of lists for intervals
# times, labs = util.intervals_to_samples([[0, 1], [1, 2]], ["A", "B"])

# GOOD: Convert intervals to a numpy array first and unpack the tuple
intervals_arr = np.array([[0.0, 1.0], [1.0, 2.0]])
labels_list = ["A", "B"]
sample_times, sample_labels = util.intervals_to_samples(
    intervals_arr, 
    labels_list, 
    sample_size=0.1, 
    fill_value="None"
)
```

## API Test: `join`

### Signature
```python
def join(chord_root, quality='', extensions=None, bass='')
```
_Source: source/mir_eval/chord.py:436_

_Source doc:_ Join the parts of a chord into a complete chord label. Parameters ---------- chord_root : str Root pitch class of the chord, e.g. 'C', 'Eb' quality : str Quality of the chord, e.g. 'maj', 'hdim7' (Default value = '') extensions : list Any added or absent scaled degrees for this chord, e.g. ['4', '\*3'] (Default value = None) bass : str Scale degree of the bass note, e.g. '5'. (Default value = '') Returns ------- chord_label : str A complete chord label.

### Goal
Reconstruct a complete chord label string from its constituent parts (root, quality, extensions, and bass) for music information retrieval chord evaluation tasks.

### Parameters
- `chord_root`: The root pitch class of the chord as a string (e.g., `'C'`, `'Eb'`).
- `quality`, default `''`: The quality of the chord as a string (e.g., `'maj'`, `'hdim7'`).
- `extensions`, default `None`: A list of strings representing any added or absent scale degrees for this chord (e.g., `['4', '*3']`).
- `bass`, default `''`: The scale degree of the bass note as a string (e.g., `'5'`).

### Input
The caller must provide string representations for the root, quality, and bass, and a list of strings for extensions. The inputs should correspond to valid chord components as used in MIR chord annotations. Note that `mir_eval` chord validation uses regular expressions and restricts invalid chord types from `chord.QUALITIES`.

### Output
Returns `unspecified` — A single string representing the complete, formatted chord label (e.g., `'C:maj(7,9)/5'`).

### Valid Call Patterns
```python
import mir_eval

# Using positional arguments (as demonstrated in the test suite via *split)
label = mir_eval.chord.join('C', 'maj', ['7', '9'], '5')

# Using keyword arguments for clarity when omitting optional components
label_simple = mir_eval.chord.join(chord_root='Eb', quality='hdim7')
```

### LLM Instruction Prompt
When calling `mir_eval.chord.join`, ensure `chord_root` is a valid pitch class string. Pass `extensions` as a list of strings (or `None`), not a single string. Use keyword arguments for clarity if omitting intermediate optional parameters. Ensure the provided `quality` is a valid MIR chord quality recognized by `mir_eval.chord.QUALITIES`.

### Prompt Snippet
```text
mir_eval.chord.join requires `extensions` to be a list of strings (e.g., ['7']), not a bare string. Ensure `quality` strings conform to valid MIR chord qualities.
```

### Common Failure Modes
- Passing a bare string instead of a list of strings for the `extensions` parameter, which will cause formatting errors when the function attempts to iterate or join the extensions.
- Providing invalid chord qualities that violate `mir_eval.chord` validation rules (which restrict invalid chord types from `chord.QUALITIES`).
- Relying on implicit parameter ordering without passing all intermediate arguments (e.g., passing the bass note as the third argument instead of the fourth).

### Fix Code Hint
```python
# BAD: Passing a string for extensions or skipping intermediate arguments
# label = mir_eval.chord.join('C', 'maj', '7') 

# GOOD: Passing a list for extensions
label = mir_eval.chord.join('C', 'maj', extensions=['7'])

# GOOD: Using keyword arguments to safely skip extensions
label = mir_eval.chord.join('C', 'maj', bass='3')
```

## API Test: `karaoke_perceptual_metric`

### Signature
```python
def karaoke_perceptual_metric(reference_timestamps, estimated_timestamps)
```
_Source: source/mir_eval/alignment.py:269_

_Source doc:_ Metric based on human synchronicity perception as measured in the paper "User-centered evaluation of lyrics to audio alignment" [#lizemasclef2021] The parameters of this function were tuned on data collected through a user Karaoke-like experiment It reflects human judgment of how "synchronous" lyrics and audio stimuli are perceived in that setup. Beware that this metric is non-symmetrical and by construction it is also not equal to 1 at 0. Examples -------- >>> reference_timestamps = mir_eval.io.load_events('reference.txt') >>> estimated_timestamps = mir_eval.io.load_events('estimated.txt') >>> score = mir_eval.align.karaoke_perceptual_metric(reference_onsets, estimated_timestamps) Parameters ---------- reference_timestamps : np.ndarray reference timestamps, in seconds estimated_timestamps : np.ndarray estimated timestamps, in seconds Returns ------- perceptual_score : float Perceptual score, averaged over all timestamps

### Goal
Computes a perceptual score for lyrics-to-audio alignment based on human synchronicity perception from a Karaoke-like experiment.

### Parameters
- `reference_timestamps`: `np.ndarray` — The ground truth reference timestamps, in seconds.
- `estimated_timestamps`: `np.ndarray` — The estimated timestamps to evaluate, in seconds.

### Input
Both inputs must be 1D numpy arrays containing event timestamps in seconds. These are typically loaded from repository-format text files using `mir_eval.io.load_events()`. 

### Output
Returns `unspecified` — A `float` representing the perceptual score, averaged over all timestamps. Note that by construction, this metric is non-symmetrical and does not equal 1.0 at 0 error.

### Valid Call Patterns
```python
import mir_eval

# Inferred from source documentation example (corrected for typos and module path)
reference_timestamps = mir_eval.io.load_events('reference.txt')
estimated_timestamps = mir_eval.io.load_events('estimated.txt')

score = mir_eval.alignment.karaoke_perceptual_metric(
    reference_timestamps, 
    estimated_timestamps
)
```

### LLM Instruction Prompt
- When evaluating lyrics-to-audio alignment, use `mir_eval.alignment.karaoke_perceptual_metric`. 
- Always pass the reference timestamps as the first argument and estimated timestamps as the second, because the metric is explicitly non-symmetrical. 
- Ensure inputs are 1D numpy arrays of timestamps in seconds (events), not 2D arrays of intervals.
- Do not write assertions expecting the score to be exactly `1.0` for perfect alignment, as the metric does not equal 1 at 0 error by construction.

### Prompt Snippet
```text
`mir_eval.alignment.karaoke_perceptual_metric(reference_timestamps, estimated_timestamps)` computes a human-perception-based synchronicity score for lyrics alignment. The metric is non-symmetrical; pass ground truth first. Inputs must be 1D numpy arrays of timestamps in seconds.
```

### Common Failure Modes
- **Argument Swapping:** Reversing the `reference_timestamps` and `estimated_timestamps` arguments, which yields incorrect results due to the metric's non-symmetrical nature.
- **Passing Intervals Instead of Events:** Providing 2D interval arrays (start/end times) instead of 1D event timestamp arrays.
- **Strict Equality Assertions:** Assuming the metric returns exactly `1.0` for perfect alignment (0 error) in test suites.

### Fix Code Hint
```python
import mir_eval

# Load 1D event timestamps (not intervals)
ref_times = mir_eval.io.load_events('reference.txt')
est_times = mir_eval.io.load_events('estimated.txt')

# Correct argument order: reference first, estimate second
score = mir_eval.alignment.karaoke_perceptual_metric(ref_times, est_times)
```

## API Test: `labeled_intervals`

### Signature
```python
def labeled_intervals(intervals, labels, label_set=None, base=None, height=None, extend_labels=True, ax=None, tick=True, prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:312_

### Goal
Plot labeled intervals (such as chords or structural segments) on a matplotlib axis, displaying each unique label on its own horizontal row for visual inspection.

### Parameters
- `intervals`: `np.ndarray`, shape=(n, 2) — The segment start and end times in seconds, typically in the format returned by `mir_eval.io.load_labeled_intervals`.
- `labels`: `list`, shape=(n,) — The reference segment labels (e.g., chord names or segment letters) corresponding to each interval.
- `label_set`, default `None`: `list` — An ordered list of labels to determine the vertical plotting order. If not provided, it is inferred from `ax.get_yticklabels()` or defaults to the sorted set of unique values in `labels`.
- `base`, default `None`: `np.ndarray`, shape=(n,) — The vertical starting positions of each label. By default, labels are positioned at integers `np.arange(len(labels))`.
- `height`, default `None`: scalar or `np.ndarray`, shape=(n,) — The height for each plotted label block. If a scalar is provided, the same value is applied to all labels. Defaults to `1`.
- `extend_labels`, default `True`: `bool` — If `False`, only values in `labels` that also exist in `label_set` are shown. If `True`, all labels are shown, appending unknown labels to the top of the plot separated by a horizontal line.
- `ax`, default `None`: `matplotlib.pyplot.axes` — An existing matplotlib axis handle on which to draw the intervals. If `None`, a new set of axes is created.
- `tick`, default `True`: `bool` — If `True`, sets the tick positions and labels on the y-axis to match the label names.
- `prop_cycle`, default `None`: `cycle.Cycler` — An optional property cycle object to specify style properties (colors, etc.). If not provided, matplotlib's default property cycler is used.
- `**kwargs`: Additional keyword arguments to pass directly to `matplotlib.collection.PolyCollection` (e.g., `alpha`, `edgecolor`).

### Input
The caller must provide `intervals` as a 2D numpy array of shape `(n, 2)` and `labels` as a list of strings of length `n`. These are typically loaded from a repository-format annotation file using `mir_eval.io.load_labeled_intervals`. Because this is a display function, any automated testing or CI execution must be kept headless (e.g., by using `matplotlib.use('Agg')` before importing `pyplot`) and must not attempt to access display devices.

### Output
Returns `unspecified` — A `matplotlib.pyplot.axes._subplots.AxesSubplot` handle to the constructed or modified plot axes containing the labeled interval visualization.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval

# Pattern 1: Basic plotting on a new figure
intervals, labels = mir_eval.io.load_labeled_intervals("data/chord/ref01.lab")
mir_eval.display.labeled_intervals(intervals, labels)
fig = plt.gcf()

# Pattern 2: Plotting on an existing axis with strict label sets
intervals, labels = mir_eval.io.load_labeled_intervals("data/chord/ref01.lab")
ax = plt.axes()
ax.set_yticklabels([])
mir_eval.display.labeled_intervals(
    intervals, labels, label_set=[], extend_labels=False, ax=ax
)
```

### LLM Instruction Prompt
- When generating code to visualize labeled intervals (like chords or segments) using `mir_eval.display.labeled_intervals`, always load the data using `mir_eval.io.load_labeled_intervals` to ensure the `intervals` array is `(n, 2)` and `labels` is a list of length `n`.
- If writing tests or running in an automated environment, you MUST configure matplotlib to use a headless backend (e.g., `matplotlib.use('Agg')`) before creating plots to prevent display-device errors.
- Pass `extend_labels=False` if you want to strictly limit the visualization to a predefined `label_set`.

### Prompt Snippet
```text
Generate a headless Python script that loads chord annotations from 'chords.lab' using mir_eval and plots them using `mir_eval.display.labeled_intervals`. Save the resulting plot to 'chords_plot.png' without opening a GUI window.
```

### Common Failure Modes
- **Display Device Errors in CI**: Failing to set a headless matplotlib backend (like `Agg`) before calling the display function, causing the script to crash in environments without a window server.
- **Shape Mismatch**: Passing a 1D array for `intervals` or providing a `labels` list whose length does not match the number of rows in `intervals`.
- **Invalid Data Types**: Passing a raw string or file path directly to `labeled_intervals` instead of parsing it first with `mir_eval.io.load_labeled_intervals`.

### Fix Code Hint
```python
import matplotlib
matplotlib.use('Agg')  # Must be called before importing pyplot to ensure headless execution
import matplotlib.pyplot as plt
import mir_eval

# Correctly load the intervals (n, 2) and labels (n,)
intervals, labels = mir_eval.io.load_labeled_intervals('annotations.lab')

# Create the plot
fig, ax = plt.subplots()
mir_eval.display.labeled_intervals(intervals, labels, ax=ax)

# Save headlessly
fig.savefig('output.png')
plt.close(fig)
```

## API Test: `lmeasure`

### Signature
```python
def lmeasure(reference_intervals_hier, reference_labels_hier, estimated_intervals_hier, estimated_labels_hier, frame_size=0.1, beta=1.0)
```
_Source: source/mir_eval/hierarchy.py:548_

_Source doc:_ Compute the tree measures for hierarchical segment annotations. Parameters ---------- reference_intervals_hier : list of ndarray ``reference_intervals_hier[i]`` contains the segment intervals (in seconds) for the ``i`` th layer of the annotations.  Layers are ordered from top to bottom, so that the last list of intervals should be the most specific. reference_labels_hier : list of list of str ``reference_labels_hier[i]`` contains the segment labels for the ``i`` th layer of the annotations estimated_intervals_hier : list of ndarray estimated_labels_hier : list of ndarray Like ``reference_intervals_hier`` and ``reference_labels_hier`` but for the estimated annotation frame_size : float > 0 length (in seconds) of frames.  The frame size cannot be longer than the window. beta : float > 0 beta parameter for the F-measure. Returns ------- l_precision : number [0, 1] L-measure Precision l_recall : number [0, 1] L-measure Recall l_measure : number [0, 1] F-beta measure for ``(l_precision, l_recall)`` Raises ------ ValueError If either of the input hierarchies are inconsistent If the input hierarchies have different time durations If ``frame_size > window`` or ``frame_size <= 0``

### Goal
Compute the tree measures (L-measure precision, recall, and F-measure) for hierarchical segment annotations to evaluate music structure analysis systems.

### Parameters
- `reference_intervals_hier`: list of `numpy.ndarray`. Contains the segment intervals (in seconds) for each layer of the reference annotations. Layers must be ordered from top to bottom, where the last list of intervals is the most specific.
- `reference_labels_hier`: list of list of str. Contains the segment labels corresponding to each layer of the reference annotations.
- `estimated_intervals_hier`: list of `numpy.ndarray`. Contains the segment intervals (in seconds) for each layer of the estimated annotations, ordered top to bottom.
- `estimated_labels_hier`: list of list of str (or list of ndarray). Contains the segment labels corresponding to each layer of the estimated annotations.
- `frame_size`, default `0.1`: float > 0. The length (in seconds) of frames. Cannot be longer than the window.
- `beta`, default `1.0`: float > 0. The beta parameter used to weight precision vs. recall in the F-measure calculation.

### Input
- **Data Formats:** Interval hierarchies must be provided as a Python `list` of 2D `numpy.ndarray` objects (shape `(n, 2)` representing start and end times). Label hierarchies must be a `list` of `list` of strings.
- **Preconditions:** 
  - Both reference and estimated hierarchies must have the exact same total time duration.
  - Hierarchies must be consistent. If boundaries are missing from one layer to the next, a `UserWarning` is issued. If they are fundamentally inconsistent, a `ValueError` is raised.
  - `frame_size` must be strictly greater than `0` and less than or equal to the window size.

### Output
Returns `unspecified` — A tuple of three numbers in the range `[0, 1]`: `(l_precision, l_recall, l_measure)`, representing the L-measure Precision, L-measure Recall, and F-beta measure respectively.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Define reference hierarchy (2 layers)
ref_intervals = [
    np.asarray([[0, 30]]), 
    np.asarray([[0, 15], [15, 30]])
]
ref_labels = [["A"], ["a", "b"]]

# Define estimated hierarchy (1 layer)
est_intervals = [np.asarray([[0, 30]])]
est_labels = [["A"]]

# Compute L-measure scores
l_precision, l_recall, l_measure = mir_eval.hierarchy.lmeasure(
    ref_intervals, ref_labels, est_intervals, est_labels, frame_size=0.1
)
```

### LLM Instruction Prompt
- When calling `mir_eval.hierarchy.lmeasure`, ensure that the interval arguments are lists of `numpy.ndarray` objects, not raw Python lists of lists.
- Ensure that the total time duration (from the start of the first interval to the end of the last interval) is identical between the reference and estimated hierarchies.
- Order the layers in the lists from top (broadest segments) to bottom (most specific segments).

### Prompt Snippet
```text
Evaluate the hierarchical segmentation using `mir_eval.hierarchy.lmeasure`. Convert your interval lists to lists of `numpy.ndarray` first. Ensure the reference and estimated hierarchies span the exact same time duration to avoid a ValueError.
```

### Common Failure Modes
- **`ValueError: If the input hierarchies have different time durations`**: Occurs if the overall start or end times of the reference and estimated annotations do not match perfectly.
- **`ValueError: If either of the input hierarchies are inconsistent`**: Occurs if the segments within a hierarchy overlap improperly or do not form a valid tree structure.
- **`UserWarning: Segment hierarchy is inconsistent at level X`**: Issued if there are missing boundaries from one layer to the next (e.g., a child segment crosses a parent segment's boundary).
- **`ValueError: If frame_size > window or frame_size <= 0`**: Occurs if an invalid `frame_size` is provided.
- **`AttributeError` or `TypeError`**: Occurs if the interval lists contain raw Python lists instead of `numpy.ndarray` objects, as the internal functions expect numpy array methods.

### Fix Code Hint
```python
# FIX: Ensure intervals are numpy arrays and durations match
ref_intervals = [np.asarray(layer) for layer in raw_ref_intervals]
est_intervals = [np.asarray(layer) for layer in raw_est_intervals]

# Verify durations match before calling
ref_duration = ref_intervals[0][-1, 1] - ref_intervals[0][0, 0]
est_duration = est_intervals[0][-1, 1] - est_intervals[0][0, 0]
if ref_duration != est_duration:
    # Handle duration mismatch (e.g., by cropping or padding)
    pass

scores = mir_eval.hierarchy.lmeasure(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

## API Test: `load_delimited`

### Signature
```python
def load_delimited(filename, converters, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:32_

### Goal
Parse a delimited text file (such as MIR annotations, events, or intervals) into separate columns using specified type converters.

### Parameters
- `filename`: A string file path, `pathlib.Path` (or `os.PathLike`), or an open file descriptor containing the delimited data to be loaded.
- `converters`: A list of callable type converters (e.g., `[float, float, str]`) corresponding to the expected data type of each column in the file.
- `delimiter`, default `'\s+'`: A string or regular expression used to separate columns in the text file. Defaults to one or more whitespace characters.
- `comment`, default `'#'`: A string indicating the start of a comment line to be ignored during parsing. Can be set to `None` to disable comment parsing.

### Input
A text file or open file handle containing tabular data. The number of delimited columns in every non-comment row must exactly match the length of the `converters` list. The data in each column must be successfully castable by its corresponding callable in `converters`.

### Output
Returns `unspecified` — A tuple of 1D sequences (typically numpy arrays), where each element in the tuple represents a single column from the file, parsed and cast to the types specified by the `converters` list.

### Valid Call Patterns
```python
import mir_eval
import tempfile
import numpy as np

# Loading a file with a custom comment character and two integer columns
with tempfile.TemporaryFile("r+") as f:
    f.write("; some comment\n10 20\n30 50")
    f.seek(0)
    
    col1, col2 = mir_eval.io.load_delimited(f, [int, int], comment=";")
    
    assert np.allclose(col1, [10, 30])
    assert np.allclose(col2, [20, 50])
```

### LLM Instruction Prompt
- When calling `mir_eval.io.load_delimited`, you MUST provide a `converters` list with a length that exactly matches the number of columns in the target file.
- The function returns a tuple of columns, not a single 2D array or dataframe. Unpack the result accordingly (e.g., `intervals, labels = load_delimited(...)`).
- If the file uses a comment character other than `'#'`, specify it via the `comment` parameter. If the file contains no comments but uses `'#'` as valid data, pass `comment=None`.

### Prompt Snippet
```text
To load custom MIR annotation files, use `mir_eval.io.load_delimited(filename, converters=[float, float, str])`. It requires a list of callables matching the column count and returns a tuple of 1D arrays (one per column).
```

### Common Failure Modes
- **`IOError` / `OSError`**: Raised if `filename` is `None`, not a string, or not a valid file handle.
- **`ValueError` (Column Mismatch)**: Raised if a row in the file has a different number of columns than the length of the `converters` list.
- **`ValueError` (Conversion Failure)**: Raised if a value in the file cannot be cast by the corresponding callable in `converters` (e.g., trying to cast the string `"a"` with `int`).
- **`ValueError` (Comment Parsing)**: Raised if the file contains comments using a character different from the specified `comment` parameter, causing the parser to read the comment as data and fail conversion or column-count checks.

### Fix Code Hint
```python
# If you encounter a ValueError regarding column counts or conversion:
# 1. Verify the file doesn't have a header row that needs to be commented out.
# 2. Ensure the length of `converters` matches the exact number of delimited columns.
# 3. Check if the delimiter needs to be explicitly set (e.g., delimiter=',') instead of the default whitespace.
col1, col2, col3 = mir_eval.io.load_delimited(
    "annotations.txt", 
    converters=[float, float, str], 
    delimiter='\t', 
    comment='#'
)
```

## API Test: `load_events`

### Signature
```python
def load_events(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:123_

### Goal
Loads 1D event annotations (such as beat or onset timestamps) from a repository-format text file into a deterministic in-memory array for evaluation or display.

### Parameters
- `filename`: The path to the text file containing the events. Can be a string, an open file descriptor, or an `os.PathLike` object (such as `pathlib.Path`).
- `delimiter`, default `'\s+'`: The string or regular expression used to separate values in the file. Defaults to any whitespace.
- `comment`, default `'#'`: The character indicating the start of a comment line. Lines starting with this character will be ignored during parsing.

### Input
A readable text file containing event data (typically timestamps in seconds). The file must exist at the specified path and conform to the expected delimiter and comment structure. 

### Output
Returns `unspecified` — an array of event timestamps parsed from the file, ready to be passed into task-specific evaluation functions (e.g., `mir_eval.beat.evaluate`) or display functions.

### Valid Call Patterns
```python
import mir_eval

# Standard usage: loading reference and estimated events for evaluation
reference_beats = mir_eval.io.load_events('reference_beats.txt')
estimated_beats = mir_eval.io.load_events('estimated_beats.txt')
scores = mir_eval.beat.evaluate(reference_beats, estimated_beats)

# Loading a subset of events (as seen in the test suite)
beats_ref = mir_eval.io.load_events("data/beat/ref00.txt")[:30]
beats_est = mir_eval.io.load_events("data/beat/est00.txt")[:30]
```

### LLM Instruction Prompt
- Use `mir_eval.io.load_events` to read 1D event annotations (like beats or onsets) from text files.
- Pass the file path as a string, open file descriptor, or `pathlib.Path`.
- Do not invent parameters; only `filename`, `delimiter`, and `comment` are supported.
- If the file contains comments using a character other than `#`, explicitly pass the `comment` parameter.

### Prompt Snippet
```text
Use `mir_eval.io.load_events(filename)` to load event timestamps (e.g., beats, onsets) from a text file into an array for evaluation. It accepts strings or `pathlib.Path` objects.
```

### Common Failure Modes
- **File Not Found**: Passing a string or path to a file that does not exist on disk.
- **Format Mismatch**: Attempting to load a file with a different comment character without overriding the `comment` parameter, leading to parsing errors.
- **Multi-column Data**: Using `load_events` on files containing intervals (start/end times) or labeled events, which require different parsing logic than a simple 1D event list.

### Fix Code Hint
```python
import pathlib
import mir_eval

event_file = pathlib.Path("data/beat/ref00.txt")
# Ensure the file exists before attempting to load
if event_file.is_file():
    # Load events, overriding the comment character if necessary
    events = mir_eval.io.load_events(event_file, comment=';')
```

## API Test: `load_intervals`

### Signature
```python
def load_intervals(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:206_

### Goal
Load a sequence of time intervals (start and end times) from a repository-format text file or file descriptor into a numerical array for MIR evaluation.

### Parameters
- `filename`: A string path, `pathlib.Path`, `os.PathLike` object, or an open file descriptor pointing to a text file containing the interval data.
- `delimiter`, default `'\s+'`: A string or regular expression indicating how the start and end times are separated on each line. The default handles any arbitrary whitespace.
- `comment`, default `'#'`: A string character indicating the start of a comment. Any text following this character on a line will be ignored during parsing.

### Input
The caller must provide a text file or open file-like object where each non-comment line contains exactly two numeric values (a start time and an end time) separated by the specified `delimiter`. 
**Preconditions:** All interval durations must be strictly positive (i.e., the start time must be strictly less than the end time). If any interval is non-increasing (e.g., `10 9`), the function will still parse the data but will issue a `UserWarning`.

### Output
Returns `unspecified` — A 2-dimensional `numpy.ndarray` of shape `(N, 2)` containing the parsed start and end times as floats, where `N` is the number of intervals.

### Valid Call Patterns
```python
import mir_eval
import tempfile
import numpy as np
import warnings

# Example derived from the project's test suite
with tempfile.TemporaryFile("r+") as f:
    # Write valid intervals (start < end)
    f.write("0.0 1.5\n1.5 3.0\n3.0 4.5")
    f.seek(0)
    
    intervals = mir_eval.io.load_intervals(f)
    assert np.all(intervals == [[0.0, 1.5], [1.5, 3.0], [3.0, 4.5]])

# Example using a file path string (inferred from context)
# intervals = mir_eval.io.load_intervals('reference_intervals.txt')
```

### LLM Instruction Prompt
- When calling `mir_eval.io.load_intervals`, ensure the target file contains exactly two columns of numeric data per line.
- If generating or preprocessing the file beforehand, guarantee that all interval durations are strictly positive (`start < end`) to prevent `UserWarning`s about invalid interval durations.
- Pass an open file descriptor (in text mode) or a valid path string/`pathlib.Path`.

### Prompt Snippet
```text
Use `mir_eval.io.load_intervals(filename)` to load the segment boundaries. Ensure the text file has two columns (start and end times) separated by whitespace, and that all start times are strictly less than their corresponding end times to avoid warnings.
```

### Common Failure Modes
- **Non-positive durations:** Passing a file where a start time is greater than or equal to the end time (e.g., `10 9`) will trigger a `UserWarning: All interval durations must be strictly positive`.
- **Incorrect column count:** Providing a file with lines containing only one value or more than two values (that are not commented out) will cause parsing errors, as the function expects exactly an `(N, 2)` shape.
- **File Not Found:** Passing a string path to a non-existent file will raise a standard `FileNotFoundError`.

### Fix Code Hint
```python
# If you encounter a UserWarning about interval durations, filter or fix the data before evaluating:
with open("intervals.txt", "r+") as f:
    intervals = mir_eval.io.load_intervals(f)

# Ensure shape is (N, 2) and start < end
valid_mask = intervals[:, 0] < intervals[:, 1]
valid_intervals = intervals[valid_mask]
```

## API Test: `load_key`

### Signature
```python
def load_key(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:497_

### Goal
Loads key annotations (such as ground truth reference or estimated keys) from a repository-format text file for use in music information retrieval evaluation.

### Parameters
- `filename`: The path to the key annotation file. Can be a string file path, an open file descriptor, or an `os.PathLike` object (such as `pathlib.Path`).
- `delimiter`, default `'\s+'`: The string or regular expression used to separate columns in the text file. Defaults to any whitespace.
- `comment`, default `'#'`: The character or string indicating the start of a comment in the text file. Lines starting with this character are ignored during parsing.

### Input
A text file containing key annotations. The file format typically contains key labels, and the `mir_eval` key notation supports unknown or ambiguous keys and modes. The `filename` argument must point to a valid, accessible file or be a valid open file descriptor. 

### Output
Returns `unspecified` — The parsed key annotation data extracted from the file. (The exact return type is unspecified in the provided API facts, but it represents the key label(s) ready to be passed to `mir_eval.key.evaluate`).

### Valid Call Patterns
```python
import mir_eval

# INFERRED FROM SIGNATURE (No verified test-suite example provided)
# Load a reference key from a text file
ref_key = mir_eval.io.load_key('reference_key.txt')

# Load an estimated key with a custom delimiter and comment character
est_key = mir_eval.io.load_key('estimated_key.csv', delimiter=',', comment=';')
```

### LLM Instruction Prompt
- When evaluating key estimation tasks, use `mir_eval.io.load_key(filename)` to load the repository-format text annotations.
- Pass the file path as a string or `pathlib.Path`.
- Remember that `mir_eval` key notation supports unknown or ambiguous keys and modes; do not attempt to filter these out before loading unless specifically required by your preprocessing logic.
- If the annotation file uses a specific separator (e.g., commas), override the default whitespace delimiter using the `delimiter` keyword argument.

### Prompt Snippet
```text
`mir_eval.io.load_key(filename, delimiter='\s+', comment='#')` loads key annotations from a text file. `filename` can be a string path, `pathlib.Path`, or open file descriptor. It supports unknown/ambiguous keys and modes. Returns the parsed key data for use in `mir_eval.key.evaluate`.
```

### Common Failure Modes
- **FileNotFoundError:** Providing a string path to a file that does not exist.
- **Parsing Errors:** Using the default whitespace delimiter (`'\s+'`) on a file that is strictly comma-separated or tab-separated with spaces inside the labels, causing the key labels to be split incorrectly.
- **Binary File Error:** Attempting to pass an audio file (e.g., `.wav`) instead of a text-based annotation file. `mir_eval.io` routines expect text files containing events, intervals, or labels.

### Fix Code Hint
```python
import mir_eval
from pathlib import Path

key_file = Path("annotations/song_key.txt")
if key_file.exists():
    # Ensure the delimiter matches the file's actual format if it isn't whitespace-separated
    key_data = mir_eval.io.load_key(key_file, delimiter='\t')
```

## API Test: `load_labeled_events`

### Signature
```python
def load_labeled_events(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:162_

### Goal
Loads labeled events (such as timestamps and their corresponding frequencies or string labels) from a repository-format text file into memory for MIR evaluation.

### Parameters
- `filename`: The path to the text file containing the labeled events. Can be a string, an open file descriptor, or an `os.PathLike` (e.g., `pathlib.Path`) object.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate the time and label columns in the text file. Defaults to one or more whitespace characters.
- `comment`, default `'#'`: The character indicating the start of a comment line. Lines starting with this character will be ignored during parsing.

### Input
A text file where each non-comment line contains an event timestamp and a corresponding label (e.g., a pitch frequency or a chord name), separated by the specified `delimiter`. The file must exist and be readable. 

### Output
Returns `unspecified` — Based on test suite usage, it returns a two-element tuple containing the parsed data (e.g., `(times, labels)` or `(times, frequencies)`), where the first element represents the event timestamps and the second element represents the corresponding labels.

### Valid Call Patterns
```python
from mir_eval.io import load_labeled_events

# Load reference and estimated melody frequencies
ref_times, ref_freqs = load_labeled_events("data/melody/ref00.txt")
est_times, est_freqs = load_labeled_events("data/melody/est00.txt")
```

### LLM Instruction Prompt
- When loading labeled event data (like melody pitches or chord labels) from text files for `mir_eval` evaluation, use `load_labeled_events`.
- Always unpack the return value into two variables (e.g., `times, labels = load_labeled_events(...)`).
- If the file uses a specific separator (like commas), override the default `delimiter` parameter (e.g., `delimiter=','`).

### Prompt Snippet
```text
`mir_eval.io.load_labeled_events(filename, delimiter='\s+', comment='#')` parses a text file containing timestamps and labels, returning a tuple of `(times, labels)`. It accepts strings, file descriptors, or `pathlib.Path` objects.
```

### Common Failure Modes
- **File Not Found**: Passing a string path that does not exist on disk.
- **Delimiter Mismatch**: Relying on the default whitespace delimiter (`\s+`) when the file is actually comma-separated or tab-separated with spaces inside the labels, causing column parsing to fail or misalign.
- **Unpacking Errors**: Failing to unpack the returned tuple into exactly two variables (times and labels).

### Fix Code Hint
```python
import pathlib
from mir_eval.io import load_labeled_events

filepath = pathlib.Path("annotations.csv")
if filepath.exists():
    # Ensure the delimiter matches the file format (e.g., CSV)
    times, labels = load_labeled_events(filepath, delimiter=',')
```

## API Test: `load_labeled_intervals`

### Signature
```python
def load_labeled_intervals(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:248_

### Goal
Loads labeled time intervals (such as structural segments or chords) from a repository-format text file into memory for evaluation or display.

### Parameters
- `filename`: The path (as a string, `pathlib.Path`, or `os.PathLike` object) or an open file descriptor pointing to the text file to be loaded.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate the start time, end time, and label columns in the file. Defaults to any whitespace.
- `comment`, default `'#'`: The character that denotes a comment line. Lines starting with this character will be ignored during parsing.

### Input
A text file (or file-like object) where each non-comment line contains exactly three columns: a numeric start time, a numeric end time, and a string label, separated by the specified `delimiter`. 

### Output
Returns `unspecified` — A tuple of two elements: `(intervals, labels)`. `intervals` represents the parsed start and end times, and `labels` represents the corresponding text annotations for each interval.

### Valid Call Patterns
```python
# Load segment data using default whitespace delimiter
intervals, labels = load_labeled_intervals("data/segment/ref00.lab")

# Plot the loaded segments
mir_eval.display.segments(intervals, labels, text=True)
```

### LLM Instruction Prompt
- When loading MIR annotations that contain start times, end times, and text labels (like structural segments or chords), use `load_labeled_intervals`. Expect it to return a tuple of `(intervals, labels)`. Do not use this function for files that only contain timestamps without labels; use `load_events` or `load_intervals` instead.

### Prompt Snippet
```text
To evaluate segment boundaries and labels, first load the reference and estimated annotation files using `load_labeled_intervals`. This function parses text files into the `(intervals, labels)` tuple format required by `mir_eval.segment.evaluate`.
```

### Common Failure Modes
- Passing a file formatted with a specific delimiter (like a comma in a CSV) without overriding the default `delimiter='\s+'` parameter, resulting in parsing errors.
- Passing a file that contains only intervals (no labels) or only events (single timestamps), which will fail to unpack into the expected three columns.
- Passing a file path that does not exist or cannot be resolved.

### Fix Code Hint
```python
# INCORRECT: Fails to parse a comma-separated file properly
intervals, labels = load_labeled_intervals("annotations.csv")

# CORRECT: Override the delimiter for CSV files
intervals, labels = load_labeled_intervals("annotations.csv", delimiter=",")
```

## API Test: `load_patterns`

### Signature
```python
def load_patterns(filename)
```
_Source: source/mir_eval/io.py:331_

_Source doc:_ Load the patterns contained in the filename and puts them into a list of patterns, each pattern being a list of occurrence, and each occurrence being a list of (onset, midi) pairs. The input file must be formatted as described in MIREX 2013: http://www.music-ir.org/mirex/wiki/2013:Discovery_of_Repeated_Themes_%26_Sections Parameters ---------- filename : str or `os.Pathlike` The input file path containing the patterns of a given piece using the MIREX 2013 format. Returns ------- pattern_list : list The list of patterns, containing all their occurrences, using the following format:: onset_midi = (onset_time, midi_number) occurrence = [onset_midi1, ..., onset_midiO] pattern = [occurrence1, ..., occurrenceM] pattern_list = [pattern1, ..., patternN] where ``N`` is the number of patterns, ``M[i]`` is the number of occurrences of the ``i`` th pattern, and ``O[j]`` is the number of onsets in the ``j``'th occurrence.  E.g.:: occ1 = [(0.5, 67.0), (1.0, 67.0), (1.5, 67.0), (2.0, 64.0)] occ2 = [(4.5, 65.0), (5.0, 65.0), (5.5, 65.0), (6.0, 62.0)] pattern1 = [occ1, occ2] occ1 = [(10.5, 67.0), (11.0, 67.0), (11.5, 67.0), (12.0, 64.0), (12.5, 69.0), (13.0, 69.0), (13.5, 69.0), (14.0, 67.0), (14.5, 76.0), (15.0, 76.0), (15.5, 76.0), (16.0, 72.0)] occ2 = [(18.5, 67.0), (19.0, 67.0), (19.5, 67.0), (20.0, 62.0), (20.5, 69.0), (21.0, 69.0), (21.5, 69.0), (22.0, 67.0), (22.5, 77.0), (23.0, 77.0), (23.5, 77.0), (24.0, 74.0)] pattern2 = [occ1, occ2] pattern_list = [pattern1, pattern2]

### Goal
Load repeated musical themes and sections (patterns) from a MIREX 2013 formatted text file into a deeply nested Python list structure.

### Parameters
- `filename`: A `str` or `os.PathLike` object representing the input file path that contains the patterns of a given piece, formatted according to the MIREX 2013 specification.

### Input
The caller must provide a valid path to a local text file. The file's contents must strictly adhere to the MIREX 2013 "Discovery of Repeated Themes & Sections" format, which encodes patterns, their occurrences, and the specific onset times and MIDI note numbers that make up each occurrence.

### Output
Returns `unspecified` — A Python `list` of patterns. The structure is a three-level nested list: `pattern_list` contains patterns; each `pattern` contains occurrences; and each `occurrence` contains `(onset_time, midi_number)` tuples (where `onset_time` and `midi_number` are floats).

### Valid Call Patterns
```python
# Note: This example is inferred from the signature and project context (not verified by an existing test).
import mir_eval

# Load reference patterns from a MIREX 2013 formatted file
reference_patterns = mir_eval.io.load_patterns('reference_patterns.txt')

# Load estimated patterns
estimated_patterns = mir_eval.io.load_patterns('estimated_patterns.txt')

# These lists can then be passed to mir_eval.pattern.evaluate()
```

### LLM Instruction Prompt
- When calling `mir_eval.io.load_patterns`, ensure the target file exists locally and is formatted exactly to the MIREX 2013 specification.
- Expect the return value to be a deeply nested list (`list[list[list[tuple[float, float]]]]`), not a numpy array or a flat list of events.
- Do not attempt to pass audio files or standard event/interval text files to this function; it is strictly for the MIREX 2013 pattern discovery format.

### Prompt Snippet
```text
`mir_eval.io.load_patterns(filename)` parses a MIREX 2013 pattern discovery text file. It returns a nested list: `[pattern1, ..., patternN]`, where each pattern is a list of occurrences, and each occurrence is a list of `(onset_time, midi_number)` tuples.
```

### Common Failure Modes
- **Incorrect File Format:** Passing a standard comma-separated or tab-separated event/interval file (like those used for beats or segments) will cause parsing errors, as the function expects the specific MIREX 2013 pattern hierarchy.
- **File Not Found:** Passing a string path to a file that does not exist on disk will raise standard Python `FileNotFoundError` or `IOError` exceptions.
- **Type Errors on Output:** Assuming the output is a numpy array or a flat list of events and attempting to slice it or pass it to incompatible utility functions (like `mir_eval.util.match_events`).

### Fix Code Hint
```python
# WRONG: Assuming flat list or standard event format
patterns = mir_eval.io.load_patterns("beats.txt")
first_onset = patterns[0][0] # Will likely fail or yield a whole occurrence list

# CORRECT: Using a MIREX 2013 pattern file and handling the nested structure
patterns = mir_eval.io.load_patterns("mirex_patterns.txt")
# Access the first onset of the first occurrence of the first pattern
first_onset_time, first_midi = patterns[0][0][0]
```

## API Test: `load_ragged_time_series`

### Signature
```python
def load_ragged_time_series(filename, dtype=float, delimiter='\s+', header=False, comment='#')
```
_Source: source/mir_eval/io.py:594_

_Source doc:_ Load data from a delimited time series annotation file with a variable number of columns. This function assumes that column 0 contains time stamps and columns 1 through n contain values. n may be variable from time stamp to time stamp. Examples -------- >>> # Load a ragged list of tab-delimited multi-f0 midi notes >>> times, vals = load_ragged_time_series('multif0.txt', dtype=int, delimiter='\t') >>> # Load a raggled list of space delimited multi-f0 values with a header >>> times, vals = load_ragged_time_series('labeled_events.csv', header=True) Parameters ---------- filename : str or `os.Pathlike` Path to the annotation file dtype : function Data type to apply to values columns. delimiter : str Separator regular expression. By default, lines will be split by any amount of whitespace. header : bool Indicates whether a header row is present or not. By default, assumes no header is present. comment : str or None Comment regular expression. Any lines beginning with this string or pattern will be ignored. Setting to `None` disables comments. Returns ------- times : np.ndarray array of timestamps (float) values : list of np.ndarray list of arrays of corresponding values

### Goal
Load data from a delimited time-series annotation file where each timestamp can have a variable (ragged) number of associated values, commonly used for multipitch estimation ground truth or outputs.

### Parameters
- `filename`: A `str` or `os.PathLike` representing the path to the annotation file to be loaded.
- `dtype`, default `float`: A callable or type (e.g., `float`, `int`) applied to cast the parsed data in the values columns.
- `delimiter`, default `'\s+'`: A regular expression string used to separate columns. By default, lines are split by any amount of whitespace.
- `header`, default `False`: A boolean indicating whether a header row is present in the file. If `True`, the first row is skipped.
- `comment`, default `'#'`: A string or regular expression pattern. Any lines beginning with this pattern are ignored. Setting to `None` disables comment parsing.

### Input
A delimited text file (e.g., `.txt`, `.csv`) containing time-series data. The first column (column 0) must contain timestamps that can be parsed as floats. Subsequent columns (columns 1 through n) contain the values for that timestamp. The number of value columns can vary from row to row.

### Output
Returns `unspecified` — A tuple of `(times, values)` where `times` is a 1D `np.ndarray` of float timestamps, and `values` is a `list` of `np.ndarray`s containing the corresponding values for each timestamp.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval
from mir_eval.io import load_ragged_time_series

# Headless display test pattern from the test suite
plt.figure()
times, pitches = load_ragged_time_series("data/multipitch/est01.txt")

# Plot pitches on a frequency scale with unvoiced frames
mir_eval.display.multipitch(times, pitches, midi=False, unvoiced=True)
fig = plt.gcf()
```

### LLM Instruction Prompt
- When loading multipitch or variable-length event annotations from text files, use `load_ragged_time_series`. Remember that the returned `values` object is a Python `list` of 1D numpy arrays (because the number of elements per timestamp can vary), not a single 2D numpy array. Always set `header=True` if the file contains column names to avoid float-parsing errors on the first row.

### Prompt Snippet
```text
Use `mir_eval.io.load_ragged_time_series(filename, delimiter='\s+', header=False)` to parse text files where column 0 is a timestamp and columns 1..n are values (e.g., multipitch data). It returns `(times, values)` where `times` is a 1D array and `values` is a list of 1D numpy arrays.
```

### Common Failure Modes
- **ValueError on parsing**: Forgetting to set `header=True` when parsing a file with column names, causing the function to fail when it attempts to parse the header string as a float timestamp.
- **AttributeError on `values`**: Treating the returned `values` as a 2D numpy array (e.g., calling `pitches.shape`) instead of a list of arrays.
- **Incorrect Delimiter**: Relying on the default whitespace delimiter (`'\s+'`) when parsing strict comma-separated files that might contain empty columns, which requires `delimiter=','`.

### Fix Code Hint
```python
# BAD: Assuming values is a 2D array and failing to skip the header
times, pitches = load_ragged_time_series("labeled_events.csv", delimiter=",")
print(pitches.shape) # AttributeError: 'list' object has no attribute 'shape'

# GOOD: Skipping the header and handling the ragged list of arrays
times, pitches = load_ragged_time_series("labeled_events.csv", delimiter=",", header=True)
for t, p in zip(times, pitches):
    print(f"Time {t} has {len(p)} pitches")
```

## API Test: `load_tempo`

### Signature
```python
def load_tempo(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:542_

### Goal
Load tempo annotations (typically two tempo values and a relative weight) from a repository-format text file for use in reproducible tempo evaluation metrics.

### Parameters
- `filename`: The path to the text file containing tempo annotations. Can be a string, an open file descriptor, or a `pathlib.Path` / `os.PathLike` object.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate values within the file. Defaults to one or more whitespace characters.
- `comment`, default `'#'`: The character or string indicating the start of a comment line, which will be ignored during parsing.

### Input
- A text file (e.g., `.lab` or `.txt`) containing numeric tempo values and a weight. 
- The file format typically consists of two tempo values (e.g., in beats per minute) and a float representing the relative perceptual weight of the first tempo (between 0.0 and 1.0).
- **Preconditions:** The file must exist and be readable. Note that `mir_eval.tempo` evaluation allows one reference tempo and both estimate tempi to be zero, so files containing zero values are valid and supported.

### Output
Returns `unspecified` — A two-element tuple `(tempi, weight)`. Based on the test suite, `tempi` is a NumPy array of the parsed tempo values (e.g., `[60., 120.]`), and `weight` is a float representing the relative weight (e.g., `0.5`).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Load tempo annotations from a standard whitespace-separated lab file
tempi, weight = mir_eval.io.load_tempo("data/tempo/ref01.lab")

# Verify the loaded data (example based on test suite)
assert np.allclose(tempi, [60, 120])
assert weight == 0.5
```

### LLM Instruction Prompt
- When calling `mir_eval.io.load_tempo`, you MUST unpack the return value into exactly two variables: `tempi` and `weight`.
- Pass the `filename` as a string or `pathlib.Path`. Do not invent additional parameters.
- If the target file uses a non-whitespace separator (like a comma), explicitly provide the `delimiter` argument (e.g., `delimiter=','`).

### Prompt Snippet
```text
To load tempo annotations for MIR evaluation, use `tempi, weight = mir_eval.io.load_tempo(filepath)`. The function parses the text file, ignoring lines starting with `#`, and returns a NumPy array of tempo values alongside a float representing the relative weight of the first tempo.
```

### Common Failure Modes
- **Tuple Unpacking Error:** Assigning the result to a single variable (e.g., `data = load_tempo(...)`) and passing it directly to an evaluation function, which expects separate `tempi` and `weight` arguments.
- **Delimiter Mismatch:** Failing to specify the `delimiter` argument when reading a CSV file, causing the default whitespace regex (`\s+`) to fail to split the values.
- **File Not Found:** Passing a string path to a file that does not exist, raising a standard `FileNotFoundError`.

### Fix Code Hint
```python
# INCORRECT: Fails to unpack the tuple, causing downstream type errors
# estimated_tempi = mir_eval.io.load_tempo('estimated.txt')
# scores = mir_eval.tempo.evaluate(ref_tempi, ref_weight, estimated_tempi)

# CORRECT: Unpack into tempi and weight
est_tempi, est_weight = mir_eval.io.load_tempo('estimated.txt')
scores = mir_eval.tempo.evaluate(ref_tempi, ref_weight, est_tempi, est_weight)
```

## API Test: `load_time_series`

### Signature
```python
def load_time_series(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:293_

### Goal
Loads a time series (such as time and frequency pairs for melody evaluation) from a repository-format text file into memory.

### Parameters
- `filename`: The path to the text file containing the time series data. Can be a string, an open file descriptor, or a `pathlib.Path` (or `os.PathLike`) object.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate the time and value columns in each line of the file. Defaults to any whitespace.
- `comment`, default `'#'`: The character indicating the start of a comment. Lines beginning with this character will be ignored during parsing.

### Input
A text file where each valid (non-comment) line contains exactly two numeric values separated by the specified `delimiter`. The first column typically represents timestamps (in seconds) and the second column represents the corresponding series values (such as fundamental frequency in Hz). 

### Output
Returns `unspecified` — A tuple of two 1D numpy arrays, typically representing `(times, values)` (e.g., `ref_time, ref_freq`), parsed sequentially from the columns of the input text file.

### Valid Call Patterns
```python
import mir_eval
import glob

# Load reference time and frequency arrays from a text file
ref_file = sorted(glob.glob('reference_annotations/*.txt'))[0]
ref_time, ref_freq = mir_eval.io.load_time_series(ref_file)

# Load with a custom delimiter (e.g., comma-separated values)
est_time, est_freq = mir_eval.io.load_time_series('estimated.csv', delimiter=',')
```

### LLM Instruction Prompt
- When loading time-series annotations (like melody pitch contours) for `mir_eval` evaluation, use `mir_eval.io.load_time_series(filename)`.
- Always unpack the return value into exactly two variables (e.g., `time, freq = ...`).
- If the target file is not whitespace-delimited, explicitly pass the correct `delimiter` argument (e.g., `delimiter=','`).
- You may pass a string path or a `pathlib.Path` object as the `filename`.

### Prompt Snippet
```text
Use `mir_eval.io.load_time_series(filename)` to parse time-series text files. It returns a tuple of two arrays `(time, values)`. Specify `delimiter=','` if parsing a CSV instead of a whitespace-delimited file.
```

### Common Failure Modes
- **ValueError on Unpacking:** The file contains more or fewer than two columns per line, causing the internal parsing to fail when returning exactly two arrays.
- **Parsing Errors due to Delimiter:** The file uses commas or tabs, but the default whitespace delimiter (`'\s+'`) incorrectly splits or fails to split the columns.
- **FileNotFoundError:** The provided string or `pathlib.Path` does not point to an existing file on disk.

### Fix Code Hint
```python
# If a file is comma-separated, the default '\s+' delimiter will fail to parse the two columns.
# FIX: Provide the correct delimiter.
time_array, freq_array = mir_eval.io.load_time_series(
    filepath, 
    delimiter=',', 
    comment='#'
)
```

## API Test: `load_valued_intervals`

### Signature
```python
def load_valued_intervals(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:448_

### Goal
Load time intervals and their associated numerical values (such as transcription note events with start/end times and pitches) from a repository-format text file into deterministic in-memory arrays.

### Parameters
- `filename`: The path to the text file containing the valued intervals. Can be a string file path, an open file descriptor, or a `pathlib.Path` (or `os.PathLike`) object.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate columns in the text file. Defaults to any whitespace.
- `comment`, default `'#'`: The character indicating the start of a comment line. Lines starting with this character will be ignored during parsing.

### Input
A text file where each non-comment line represents an interval and its corresponding value, typically formatted with three columns: `start_time end_time value` (e.g., onset time, offset time, and pitch in Hz). The file must exist, be readable, and contain valid numeric data separated by the specified `delimiter`. 

### Output
Returns `unspecified` — A tuple of two elements, typically unpacked as `(intervals, values)`. `intervals` represents the parsed time boundaries (usually a 2D array of start and end times), and `values` represents the corresponding numerical values for each interval (such as frequencies in Hz).

### Valid Call Patterns
```python
from mir_eval.io import load_valued_intervals
import mir_eval.util

# Load reference and estimated transcription data
ref_t, ref_p = load_valued_intervals("data/transcription/ref04.txt")
est_t, est_p = load_valued_intervals("data/transcription/est04.txt")

# Values (ref_p, est_p) are often frequencies in Hz that can be converted to MIDI
ref_midi = mir_eval.util.hz_to_midi(ref_p)
```

### LLM Instruction Prompt
- When loading transcription or multipitch data containing both time intervals and associated values (like pitch), use `mir_eval.io.load_valued_intervals`.
- Always unpack the return value into exactly two variables: one for the intervals and one for the values (e.g., `intervals, values = load_valued_intervals(...)`).
- If the file uses a specific separator (like commas), explicitly pass the `delimiter` argument (e.g., `delimiter=','`).
- Pass the resulting `intervals` and `values` directly to evaluation metrics or display functions like `mir_eval.display.piano_roll`.

### Prompt Snippet
```text
Use `mir_eval.io.load_valued_intervals(filename)` to parse the transcription text file. Unpack the result into `ref_intervals, ref_pitches`. Convert the pitches to MIDI using `mir_eval.util.hz_to_midi` before passing them to the piano roll display.
```

### Common Failure Modes
- **ValueError (too many/too few values to unpack):** Failing to unpack the result into exactly two variables (e.g., assigning the result to a single variable without indexing, or trying to unpack into three variables).
- **Parsing Errors:** Providing a file that only contains timestamps (events) without a third value column, which will fail to parse as a valued interval. Use `mir_eval.io.load_events` or `mir_eval.io.load_intervals` instead for those formats.
- **Delimiter Mismatch:** Using the default whitespace delimiter (`'\s+'`) on a CSV file, causing the parser to read the entire line as a single string and fail numeric conversion.
- **FileNotFoundError:** Providing a string path to a file that does not exist in the checked-in test fixtures.

### Fix Code Hint
```python
# BAD: Fails to unpack the tuple, causing downstream type errors
data = load_valued_intervals("transcription.txt")
mir_eval.display.piano_roll(data, label="Reference")

# GOOD: Unpack into intervals and values
ref_intervals, ref_pitches = load_valued_intervals("transcription.txt")
mir_eval.display.piano_roll(ref_intervals, ref_pitches, label="Reference")
```

## API Test: `load_wav`

### Signature
```python
def load_wav(path, mono=True)
```
_Source: source/mir_eval/io.py:409_

_Source doc:_ Load a .wav file as a numpy array using ``scipy.io.wavfile``. .. warning:: This function is deprecatred in mir_eval 0.8.1 and will be removed in 0.9.0. We recommend using a dedicated audio IO library such as `soundfile` instead. Parameters ---------- path : str or `os.Pathlike` Path to a .wav file mono : bool If the provided .wav has more than one channel, it will be converted to mono if ``mono=True``. (Default value = True) Returns ------- audio_data : np.ndarray Array of audio samples, normalized to the range [-1., 1.] fs : int Sampling rate of the audio data

### Goal
Load a `.wav` file as a NumPy array using `scipy.io.wavfile` and normalize the audio samples to the range `[-1., 1.]`.

### Parameters
- `path`: `str` or `os.PathLike` representing the file path to a `.wav` file.
- `mono`, default `True`: `bool` flag indicating whether to convert the audio to mono if the provided `.wav` file has more than one channel.

### Input
A valid path to an existing `.wav` file on disk. Note the strict deprecation precondition: this function is deprecated in `mir_eval` 0.8.1 and slated for removal in 0.9.0. Callers are strongly recommended to use a dedicated audio I/O library like `soundfile` instead.

### Output
Returns `unspecified` — A tuple of `(audio_data, fs)` where `audio_data` is a `np.ndarray` of audio samples automatically normalized to the float range `[-1., 1.]`, and `fs` is an `int` representing the sampling rate of the audio data.

### Valid Call Patterns
```python
# From the project's test suite
x0, fs = load_wav("data/separation/ref05/0.wav")
x1, fs = load_wav("data/separation/ref05/1.wav")
x2, fs = load_wav("data/separation/ref05/2.wav")

mir_eval.display.separation([x0, x1, x2], fs=fs)
```

### LLM Instruction Prompt
- Warn the user that `mir_eval.io.load_wav` is deprecated (removed in v0.9.0) and recommend using `soundfile` instead.
- If `load_wav` must be used, ensure the LLM unpacks the returned tuple into `(audio_data, fs)`.
- Do not manually normalize the returned audio array, as `load_wav` already normalizes the samples to `[-1.0, 1.0]`.
- Do not manually mix down stereo files unless `mono=False` is explicitly passed, as the default behavior automatically converts multi-channel audio to mono.

### Prompt Snippet
```text
`mir_eval.io.load_wav(path)` is deprecated and removed in 0.9.0; prefer `soundfile.read(path)`. If used, it returns a tuple `(audio_data, fs)` with `audio_data` already normalized to [-1.0, 1.0] and converted to mono by default.
```

### Common Failure Modes
- **Version Incompatibility:** Calling this function in `mir_eval` versions >= 0.9.0 will result in an `AttributeError` or `ImportError` because the function has been removed.
- **Tuple Unpacking Error:** Forgetting to unpack the return value into two variables, leading to a tuple being passed into downstream functions (like `mir_eval.display.separation`) that expect a NumPy array.
- **Double Normalization:** Attempting to divide the returned array by `32768.0` (a common pattern for 16-bit PCM WAV files), which corrupts the data because `load_wav` already normalizes it to `[-1., 1.]`.

### Fix Code Hint
```python
# Deprecated usage (will fail in mir_eval >= 0.9.0):
# audio_data, fs = load_wav("audio.wav")

# Recommended alternative using soundfile:
import soundfile as sf
# soundfile.read also returns (audio_data, fs) and normalizes to [-1.0, 1.0] by default
audio_data, fs = sf.read("audio.wav")

# If mono conversion is needed with soundfile:
if audio_data.ndim > 1:
    audio_data = audio_data.mean(axis=1)
```

## API Test: `majmin`

### Signature
```python
def majmin(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1107_

### Goal
Compare estimated chord labels against reference chord labels using major-minor rules, ignoring chords with qualities outside of Major, minor, or no-chord.

### Parameters
- `reference_labels`: `list` (len=n) — A list of reference (ground truth) string chord labels to score against.
- `estimated_labels`: `list` (len=n) — A list of estimated string chord labels to score against.

### Input
Lists of string chord labels of equal length `n`. Because chord annotations typically span time intervals, the caller must first load the labeled intervals (e.g., via `mir_eval.io.load_labeled_intervals`), adjust the estimated intervals to match the reference boundaries (`mir_eval.util.adjust_intervals`), and merge them (`mir_eval.util.merge_labeled_intervals`) so that the reference and estimated labels align perfectly in time. Chord strings must be valid according to `mir_eval`'s regular expression validation and restricted to valid chord types from `chord.QUALITIES`.

### Output
Returns `unspecified` — A 1D `np.ndarray` of shape `(n,)` and dtype `float` containing the comparison scores. Scores are in the range `[0.0, 1.0]`. If a comparison is out of gamut (i.e., the chords have qualities outside Major/minor/no-chord), the score for that element is `-1`.

### Valid Call Patterns
```python
import mir_eval

# 1. Load intervals and labels
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# 2. Adjust estimated intervals to reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# 3. Merge intervals to perfectly align the label lists
(intervals, ref_labels_merged, est_labels_merged) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# 4. Compute majmin comparisons
comparisons = mir_eval.chord.majmin(ref_labels_merged, est_labels_merged)

# 5. (Optional) Compute weighted accuracy using durations
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chords with `mir_eval.chord.majmin`, you MUST ensure `reference_labels` and `estimated_labels` are lists of equal length. Do not pass raw, unaligned label lists directly from file loaders; you must first align them in time using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals`. Handle the `-1` return values appropriately (e.g., by passing the result to `mir_eval.chord.weighted_accuracy`), as `-1` indicates the chords were out of gamut and should be ignored, not penalized.

### Prompt Snippet
```text
mir_eval.chord.majmin(reference_labels, estimated_labels) compares pre-aligned chord label lists (len=n) using major-minor rules. Returns a float ndarray of scores in [0.0, 1.0], or -1 for out-of-gamut chords. Always align intervals with `mir_eval.util.merge_labeled_intervals` before calling.
```

### Common Failure Modes
- **Unaligned Lists**: Passing lists of different lengths. The function requires `len=n` for both inputs.
- **Missing Preprocessing**: Failing to adjust and merge the time intervals before extracting the labels for comparison, leading to mismatched chord comparisons.
- **Misinterpreting `-1`**: Treating `-1` as a mathematical penalty rather than an "ignored/out of gamut" flag.
- **Invalid Chord Syntax**: Passing invalid chord strings that fail the internal regular expression validation or contain qualities restricted from `chord.QUALITIES`.

### Fix Code Hint
```python
# BAD: Passing unaligned labels directly from IO
# comparisons = mir_eval.chord.majmin(ref_labels, est_labels)

# GOOD: Merge intervals first to guarantee equal-length, time-aligned label lists
intervals, ref_labels_aligned, est_labels_aligned = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.majmin(ref_labels_aligned, est_labels_aligned)
```

## API Test: `majmin_inv`

### Signature
```python
def majmin_inv(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1172_

_Source doc:_ Compare chords along major-minor rules, with inversions. Chords with qualities outside Major/minor/no-chord are ignored, and the bass note must exist in the triad (bass in [1, 3, 5]). Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.majmin_inv(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0], or -1 if the comparison is out of gamut.

### Goal
Compare estimated chord labels against reference chord labels using major-minor rules with inversions, ignoring chords outside the Major/minor/no-chord gamut and requiring the bass note to be part of the triad.

### Parameters
- `reference_labels`: A `list` of length `n` containing the reference (ground truth) chord label strings to score against.
- `estimated_labels`: A `list` of length `n` containing the estimated chord label strings to score against.

### Input
Both inputs must be lists of strings representing chord labels (e.g., `'C:maj'`, `'G:maj/3'`, `'N'`). The lists must be of the exact same length `n`. Because raw chord annotations typically have unaligned time intervals, callers must first align the reference and estimated labels into a common time grid using `mir_eval.util.merge_labeled_intervals` before passing them to this function. Chord strings must be valid according to `mir_eval`'s internal regular expression validation and restricted to valid chord types from `chord.QUALITIES`.

### Output
Returns `unspecified` — A 1D numpy array (`np.ndarray`) of shape `(n,)` and dtype `float` representing the comparison scores. Scores are in the range `[0.0, 1.0]`. If a comparison is out of gamut (i.e., the chord quality is outside Major/minor/no-chord, or the bass note is not 1, 3, or 5), the score for that segment will be `-1.0`.

### Valid Call Patterns
```python
import mir_eval

# 1. Load intervals and labels
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# 2. Adjust estimated intervals to match reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# 3. Merge into a common time grid (crucial for len=n requirement)
intervals, ref_labels_merged, est_labels_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# 4. Compute segment-wise comparisons
comparisons = mir_eval.chord.majmin_inv(ref_labels_merged, est_labels_merged)

# 5. Aggregate into a final weighted accuracy score
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chords with `mir_eval.chord.majmin_inv`, you MUST first align the reference and estimated intervals using `mir_eval.util.merge_labeled_intervals` to ensure the label lists are of identical length `n`.
- Do not pass raw intervals to `majmin_inv`; it only accepts the lists of string labels.
- To compute a final scalar metric from the returned array, pass the result along with the segment durations to `mir_eval.chord.weighted_accuracy`, which automatically handles the `-1.0` out-of-gamut values.

### Prompt Snippet
```text
mir_eval.chord.majmin_inv(reference_labels, estimated_labels) compares aligned chord label lists using major-minor rules with inversions. Inputs must be equal-length lists of strings, typically produced by `mir_eval.util.merge_labeled_intervals`. Returns a float ndarray of scores in [0.0, 1.0], or -1.0 for out-of-gamut chords. Aggregate the result using `mir_eval.chord.weighted_accuracy`.
```

### Common Failure Modes
- **Mismatched List Lengths:** Passing raw, unaligned label lists directly from `mir_eval.io.load_labeled_intervals` without merging them first.
- **Passing Intervals Instead of Labels:** Accidentally passing the `intervals` array instead of the `labels` list to the function.
- **Manual Aggregation Errors:** Attempting to compute the mean of the returned array directly using `numpy.mean()`, which incorrectly includes the `-1.0` out-of-gamut flags in the calculation instead of ignoring them.
- **Invalid Chord Syntax:** Providing chord strings that fail `mir_eval`'s regular expression validation.

### Fix Code Hint
```python
# BAD: Passing unaligned labels or calculating mean directly
# scores = mir_eval.chord.majmin_inv(ref_labels, est_labels)
# final_score = np.mean(scores)

# GOOD: Merge intervals first, then use weighted_accuracy
intervals, ref_merged, est_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.majmin_inv(ref_merged, est_merged)
durations = mir_eval.util.intervals_to_durations(intervals)
final_score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

## API Test: `match_events`

### Signature
```python
def match_events(ref, est, window, distance=None)
```
_Source: source/mir_eval/util.py:644_

_Source doc:_ Compute a maximum matching between reference and estimated event times, subject to a window constraint. Given two lists of event times ``ref`` and ``est``, we seek the largest set of correspondences ``(ref[i], est[j])`` such that ``distance(ref[i], est[j]) <= window``, and each ``ref[i]`` and ``est[j]`` is matched at most once. This is useful for computing precision/recall metrics in beat tracking, onset detection, and segmentation. Parameters ---------- ref : np.ndarray, shape=(n,) Array of reference values est : np.ndarray, shape=(m,) Array of estimated values window : float > 0 Size of the window. distance : function function that computes the outer distance of ref and est. By default uses ``|ref[i] - est[j]|`` Returns ------- matching : list of tuples A list of matched reference and event numbers. ``matching[i] == (i, j)`` where ``ref[i]`` matches ``est[j]``.

### Goal
Compute a maximum bipartite matching between reference and estimated event times (such as beats or onsets) subject to a maximum distance window constraint.

### Parameters
- `ref`: Array of reference values (e.g., ground truth event times in seconds), expected as a 1D `np.ndarray` of shape `(n,)` or an array-like list.
- `est`: Array of estimated values (e.g., predicted event times in seconds), expected as a 1D `np.ndarray` of shape `(m,)` or an array-like list.
- `window`: Size of the tolerance window (float > 0). Matches are only valid if the distance between the reference and estimated event is less than or equal to this value.
- `distance`, default `None`: A function that computes the outer distance matrix between `ref` and `est`. If `None`, it defaults to computing the absolute difference `|ref[i] - est[j]|`.

### Input
The caller must provide two 1D array-like sequences of numerical event times (typically floats representing seconds, often loaded via `mir_eval.io.load_events`). The `window` parameter must be a strictly positive float (e.g., `0.05` for a 50ms tolerance). If a custom `distance` function is provided, it must accept two 1D arrays and return a 2D outer distance matrix.

### Output
Returns `unspecified` — A list of tuples representing the matched reference and estimated event indices. Each tuple is formatted as `(i, j)`, meaning `ref[i]` matches `est[j]`. Each event index appears at most once in the matching.

### Valid Call Patterns
```python
import mir_eval

# Example 1: Default absolute distance matching
ref = [1.0, 2.0, 3.0]
est = [1.1, 6.0, 1.9, 5.0, 10.0]
matching = mir_eval.util.match_events(ref, est, 0.5)
# matching == [(0, 0), (1, 2)]

# Example 2: Matching with a custom distance function
ref_mod = [1.0, 2.0, 3.0, 11.9]
est_mod = [1.1, 6.0, 1.9, 5.0, 10.0, 0.0]
matching_custom = mir_eval.util.match_events(
    ref_mod, est_mod, 0.5, distance=mir_eval.util._outer_distance_mod_n
)
# matching_custom == [(0, 0), (1, 2), (3, 5)]
```

### LLM Instruction Prompt
- When evaluating precision, recall, or F-measure for 1D event detections (like beats, onsets, or segment boundaries), use `mir_eval.util.match_events(ref, est, window)` to compute the optimal 1-to-1 bipartite matching. Ensure the `window` argument is a positive float representing the maximum allowed distance (e.g., in seconds) for a valid match.

### Prompt Snippet
```text
To find the true positive matches between ground truth and predicted onsets within a 50ms tolerance, use `mir_eval.util.match_events(ref_onsets, est_onsets, 0.05)`. This returns a list of `(ref_index, est_index)` tuples, ensuring no event is matched more than once.
```

### Common Failure Modes
- Passing a negative or zero value for `window`, which violates the `float > 0` constraint.
- Passing multi-dimensional arrays instead of 1D arrays for `ref` or `est`.
- Providing a custom `distance` function that returns a 1D array instead of the required 2D outer distance matrix of shape `(n, m)`.
- Calling the function as a bare `match_events(...)` instead of the fully qualified `mir_eval.util.match_events(...)`.

### Fix Code Hint
```python
# Ensure inputs are 1D arrays and window is strictly positive
ref_events = mir_eval.io.load_events('reference.txt')
est_events = mir_eval.io.load_events('estimated.txt')

# 50ms window for onset matching
window_size = 0.05 
matches = mir_eval.util.match_events(ref_events, est_events, window_size)
```

## API Test: `match_note_offsets`

### Signature
```python
def match_note_offsets(ref_intervals, est_intervals, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False)
```
_Source: source/mir_eval/transcription.py:169_

### Goal
Compute a maximum matching between reference and estimated notes based exclusively on their offset times, ignoring onsets and pitches.

### Parameters
- `ref_intervals`: `np.ndarray` of shape `(n, 2)` representing the reference note time intervals (onset and offset times in seconds).
- `est_intervals`: `np.ndarray` of shape `(m, 2)` representing the estimated note time intervals (onset and offset times in seconds).
- `offset_ratio`, default `0.2`: `float > 0` representing the ratio of the reference note's duration used to define the offset tolerance (e.g., 0.2 means 20% of the reference note's duration).
- `offset_min_tolerance`, default `0.05`: `float > 0` representing the absolute minimum tolerance in seconds for offset matching (e.g., 0.05 means 50 ms). Used if the ratio-based tolerance is smaller than this value.
- `strict`, default `False`: `bool` indicating whether threshold checks for offset matching should be performed using strict inequality `<` (`True`) or non-strict inequality `<=` (`False`).

### Input
Two 2D numpy arrays of shape `(N, 2)` containing `[onset, offset]` time pairs. If your data includes pitches or velocities (e.g., shape `(N, 3)` loaded via `mir_eval.io.load_valued_intervals`), you must slice the arrays to include only the first two columns before passing them to this function.

### Output
Returns `unspecified` — A list of tuples `(i, j)` representing the matched notes, where `i` is the index of the reference note and `j` is the index of the estimated note. Every reference note is matched against at most one estimated note.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example deterministic in-memory arrays of shape (N, 2)
REF = np.array([[0.5, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 4.0]])
EST = np.array([[0.55, 1.05], [1.1, 1.9], [2.0, 3.0], [3.1, 4.05], [3.1, 3.99]])

ref_int = REF[:, :2]
est_int = EST[:, :2]

# Default matching (non-strict threshold checks)
matching = mir_eval.transcription.match_note_offsets(ref_int, est_int)

# Strict matching (strict inequality for threshold checks)
matching_strict = mir_eval.transcription.match_note_offsets(ref_int, est_int, strict=True)
```

### LLM Instruction Prompt
- When evaluating transcription offsets, call `mir_eval.transcription.match_note_offsets(ref_intervals, est_intervals)`.
- Ensure both `ref_intervals` and `est_intervals` are `np.ndarray` objects strictly of shape `(N, 2)`. Slice off any pitch or velocity columns (e.g., `intervals[:, :2]`) before passing them.
- Do not use this function if you need to match notes based on onsets or pitches; use `mir_eval.transcription.match_note_onsets` or `mir_eval.transcription.match_notes` instead, as the rules for matching onsets and offsets differ.

### Prompt Snippet
```text
mir_eval.transcription.match_note_offsets computes a maximum matching between reference and estimated notes using ONLY offset times. Inputs `ref_intervals` and `est_intervals` must be (N, 2) numpy arrays of [onset, offset] times. If your data has >2 columns, slice it: `data[:, :2]`. Returns a list of (ref_idx, est_idx) tuples.
```

### Common Failure Modes
- **Incorrect Array Shape**: Passing arrays of shape `(N, 3)` (which include pitch) directly to the function. The function expects exactly `(N, 2)` for intervals.
- **Using Lists Instead of Numpy Arrays**: Passing standard Python lists instead of `np.ndarray` objects, which will cause duration calculations (like `ref_intervals[:, 1] - ref_intervals[:, 0]`) to fail.
- **Misunderstanding the Scope**: Expecting this function to evaluate pitch or onset accuracy. It strictly evaluates offsets.

### Fix Code Hint
```python
# BAD: Passing (N, 3) arrays directly
# matching = mir_eval.transcription.match_note_offsets(ref_data, est_data)

# GOOD: Slice the arrays to (N, 2) to extract only the [onset, offset] intervals
ref_intervals = ref_data[:, :2]
est_intervals = est_data[:, :2]
matching = mir_eval.transcription.match_note_offsets(ref_intervals, est_intervals)
```

## API Test: `match_note_onsets`

### Signature
```python
def match_note_onsets(ref_intervals, est_intervals, onset_tolerance=0.05, strict=False)
```
_Source: source/mir_eval/transcription.py:262_

_Source doc:_ Compute a maximum matching between reference and estimated notes, only taking note onsets into account. Given two note sequences represented by ``ref_intervals`` and ``est_intervals`` (see :func:`mir_eval.io.load_valued_intervals`), we see the largest set of correspondences ``(i,j)`` such that the onset of reference note ``i`` is within ``onset_tolerance`` of the onset of estimated note ``j``. Every reference note is matched against at most one estimated note. Note there are separate functions :func:`match_note_offsets` and :func:`match_notes` for matching notes based on offsets only or based on onset, offset, and pitch, respectively. This is because the rules for matching note onsets and matching note offsets are different. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) onset_tolerance : float > 0 The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds. Default is 0.05 (50 ms). strict : bool If ``strict=False`` (the default), threshold checks for onset matching are performed using ``<=`` (less than or equal). If ``strict=True``, the threshold checks are performed using ``<`` (less than). Returns ------- matching : list of tuples A list of matched reference and estimated notes. ``matching[i] == (i, j)`` where reference note ``i`` matches estimated note ``j``.

### Goal
Compute a maximum bipartite matching between reference and estimated note events based exclusively on their onset times falling within a specified tolerance.

### Parameters
- `ref_intervals`: `np.ndarray` of shape `(n, 2)`. An array of reference note time intervals, where each row is `[onset_time, offset_time]` in seconds.
- `est_intervals`: `np.ndarray` of shape `(m, 2)`. An array of estimated note time intervals, where each row is `[onset_time, offset_time]` in seconds.
- `onset_tolerance`, default `0.05`: `float > 0`. The maximum allowed deviation (in seconds) between an estimated note's onset and a reference note's onset.
- `strict`, default `False`: `bool`. If `False`, the onset distance threshold check uses `<=` (less than or equal). If `True`, it uses `<` (strictly less than).

### Input
The caller must provide two 2D numpy arrays of shape `(n, 2)` and `(m, 2)` representing time intervals. Even though this function only evaluates onsets, it expects full `[onset, offset]` interval arrays. If your data includes pitches or velocities (e.g., shape `(n, 3)` or `(n, 4)` from `mir_eval.io.load_valued_intervals`), you must slice the array to pass only the first two columns (`[:, :2]`).

### Output
Returns `unspecified` — A `list` of `tuple`s representing the matched notes. Each tuple `(i, j)` indicates that the reference note at index `i` is matched to the estimated note at index `j`. Every reference note is matched against at most one estimated note.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Deterministic in-memory arrays of shape (n, 2)
ref_intervals = np.array([[0.5, 1.0], [1.5, 2.0], [2.5, 3.0]])
est_intervals = np.array([[0.52, 0.9], [1.48, 2.1], [2.6, 3.1]])

# Default matching (<= 50ms tolerance)
matching = mir_eval.transcription.match_note_onsets(ref_intervals, est_intervals)

# Strict matching (< 50ms tolerance)
strict_matching = mir_eval.transcription.match_note_onsets(
    ref_intervals, 
    est_intervals, 
    strict=True
)
```

### LLM Instruction Prompt
- When calling `mir_eval.transcription.match_note_onsets`, ensure the inputs are 2D numpy arrays of shape `(n, 2)` representing `[onset, offset]` intervals. Do not pass 1D arrays of just onsets, and do not pass arrays containing pitch/velocity columns. Slice your data `[:, :2]` if necessary. Remember this function matches *only* on onsets; use `match_notes` if pitch matching is also required.

### Prompt Snippet
```text
mir_eval.transcription.match_note_onsets(ref_intervals, est_intervals, onset_tolerance=0.05, strict=False)
Matches notes based ONLY on onsets. Inputs MUST be (n, 2) and (m, 2) numpy arrays of [onset, offset] intervals. Slice valued intervals (e.g., `data[:, :2]`) before passing. Returns a list of (ref_idx, est_idx) tuples.
```

### Common Failure Modes
- **Passing 1D arrays:** Providing a 1D array of onset times instead of a 2D `(n, 2)` array of intervals will cause indexing errors, as the function expects to read the first column of a 2D array.
- **Passing arrays with pitch/velocity data:** Providing arrays of shape `(n, 3)` or `(n, 4)` (often returned by `mir_eval.io` loaders) without slicing them down to `(n, 2)` will cause shape mismatch errors or unexpected behavior.
- **Using the wrong matching function:** Calling this function when pitch or offset matching is also desired. This function strictly ignores offsets and pitches.

### Fix Code Hint
```python
# If your loaded data contains pitches (e.g., shape (n, 3)):
# ref_data = mir_eval.io.load_valued_intervals('ref.txt')
# est_data = mir_eval.io.load_valued_intervals('est.txt')

# Slice the arrays to extract only the (n, 2) interval columns
ref_intervals = ref_data[0][:, :2]
est_intervals = est_data[0][:, :2]

matching = mir_eval.transcription.match_note_onsets(ref_intervals, est_intervals)
```

## API Test: `match_notes`

### Signature
```python
def match_notes(ref_intervals, ref_pitches, est_intervals, est_pitches, onset_tolerance=0.05, pitch_tolerance=50.0, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False)
def match_notes(ref_intervals, ref_pitches, ref_velocities, est_intervals, est_pitches, est_velocities, onset_tolerance=0.05, pitch_tolerance=50.0, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False, velocity_tolerance=0.1)
```
_Source: source/mir_eval/transcription_velocity.py:107  (+1 more definition site/overload)_

_Source doc:_ Match notes, taking note velocity into consideration. This function first calls :func:`mir_eval.transcription.match_notes` to match notes according to the supplied intervals, pitches, onset, offset, and pitch tolerances. The velocities of the matched notes are then used to estimate a slope and intercept which can rescale the estimated velocities so that they are as close as possible (in L2 sense) to their matched reference velocities. Velocities are then normalized to the range [0, 1]. A estimated note is then further only considered correct if its velocity is within ``velocity_tolerance`` of its matched (according to pitch and timing) reference note. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) ref_pitches : np.ndarray, shape=(n,) Array of reference pitch values in Hertz ref_velocities : np.ndarray, shape=(n,) Array of MIDI velocities (i.e. between 0 and 127) of reference notes est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) est_pitches : np.ndarray, shape=(m,) Array of estimated pitch values in Hertz est_velocities : np.ndarray, shape=(m,) Array of MIDI velocities (i.e. between 0 and 127) of estimated notes onset_tolerance : float > 0 The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds. Default is 0.05 (50 ms). pitch_tolerance : float > 0 The tolerance for an estimated note's pitch deviating from the reference note's pitch, in cents. Default is 50.0 (50 cents). offset_ratio : float > 0 or None The ratio of the reference note's duration used to define the offset_tolerance. Default is 0.2 (20%), meaning the ``offset_tolerance`` will equal the ``ref_duration * 0.2``, or 0.05 (50 ms), whichever is greater. If ``offset_ratio`` is set to ``None``, offsets are ignored in the matching. offset_min_tolerance : float > 0 The minimum tolerance for offset matching. See offset_ratio description for an explanation of how the offset tolerance is determined. Note: this parameter only influences the results if ``offset_ratio`` is not ``None``. strict : bool If ``strict=False`` (the default), threshold checks for onset, offset, and pitch matching are performed using ``<=`` (less than or equal). If ``strict=True``, the threshold checks are performed using ``<`` (less than). velocity_tolerance : float > 0 Estimated notes are considered correct if, after rescaling and normalization to [0, 1], they are within ``velocity_tolerance`` of a matched reference note. Returns ------- matching : list of tuples A list of matched reference and estimated notes. ``matching[i] == (i, j)`` where reference note ``i`` matches estimated note ``j``.

### Goal
Match estimated musical notes to reference notes based on onset, offset, pitch, and optionally velocity tolerances, returning a list of matched index pairs.

### Parameters
- `ref_intervals`: `np.ndarray` of shape `(n, 2)` representing reference note time intervals (onset and offset times in seconds).
- `ref_pitches`: `np.ndarray` of shape `(n,)` representing reference pitch values in Hertz.
- `ref_velocities`: `np.ndarray` of shape `(n,)` representing MIDI velocities (0 to 127) of reference notes (only present in the `transcription_velocity` overload).
- `est_intervals`: `np.ndarray` of shape `(m, 2)` representing estimated note time intervals (onset and offset times in seconds).
- `est_pitches`: `np.ndarray` of shape `(m,)` representing estimated pitch values in Hertz.
- `est_velocities`: `np.ndarray` of shape `(m,)` representing MIDI velocities (0 to 127) of estimated notes (only present in the `transcription_velocity` overload).
- `onset_tolerance`, default `0.05`: `float > 0` specifying the tolerance for an estimated note's onset deviating from the reference note's onset, in seconds.
- `pitch_tolerance`, default `50.0`: `float > 0` specifying the tolerance for an estimated note's pitch deviating from the reference note's pitch, in cents.
- `offset_ratio`, default `0.2`: `float > 0` or `None`. The ratio of the reference note's duration used to define the offset tolerance (e.g., 0.2 means 20% of the reference duration). If `None`, offsets are ignored in the matching.
- `offset_min_tolerance`, default `0.05`: `float > 0` specifying the minimum tolerance for offset matching in seconds. Only influences results if `offset_ratio` is not `None`.
- `strict`, default `False`: `bool`. If `False`, threshold checks for onset, offset, and pitch matching are performed using `<=` (less than or equal). If `True`, checks are performed using `<` (less than).
- `velocity_tolerance`, default `0.1`: `float > 0` specifying the tolerance for normalized velocity matching (only present in the `transcription_velocity` overload).

### Input
The caller must provide 2D numpy arrays of shape `(n, 2)` for intervals (in seconds) and 1D numpy arrays of shape `(n,)` for pitches (in Hertz). If using the velocity-aware overload, 1D numpy arrays of shape `(n,)` containing MIDI velocities (0-127) must also be provided.

### Output
Returns `list of tuples` — A list of matched reference and estimated notes, where `matching[i] == (i, j)` indicates that reference note `i` matches estimated note `j`.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example 1: Standard transcription matching (from test suite)
ref_int = np.array([[0.0, 1.0], [1.0, 2.0]])
ref_pitch = np.array([100.0, 200.0])
est_int = np.array([[0.05, 1.0], [1.0, 2.0]])
est_pitch = np.array([100.0, 200.0])

matching = mir_eval.transcription.match_notes(
    ref_int, ref_pitch, est_int, est_pitch
)

# Example 2: Ignoring offsets during matching (from test suite)
matching_no_offset = mir_eval.transcription.match_notes(
    ref_int, ref_pitch, est_int, est_pitch, offset_ratio=None
)

# Example 3: Strict matching using `<` instead of `<=` (from test suite)
matching_strict = mir_eval.transcription.match_notes(
    ref_int, ref_pitch, est_int, est_pitch, strict=True
)
```

### LLM Instruction Prompt
- Ensure `ref_intervals` and `est_intervals` are 2D numpy arrays of shape `(n, 2)`.
- Ensure `ref_pitches` and `est_pitches` are 1D numpy arrays in Hertz, not MIDI note numbers.
- To ignore offset matching entirely, explicitly pass `offset_ratio=None`.
- Use `mir_eval.transcription.match_notes` for standard matching and `mir_eval.transcription_velocity.match_notes` when velocities are included.
- Be aware that setting `strict=True` changes the threshold checks from `<=` to `<`, which may cause exact boundary matches to fail due to floating-point precision.

### Prompt Snippet
```text
When evaluating note transcriptions with `mir_eval.transcription.match_notes`, ensure pitches are in Hertz and intervals are `(n, 2)` numpy arrays. Pass `offset_ratio=None` if offset times should be ignored during matching.
```

### Common Failure Modes
- Passing pitches as MIDI note numbers instead of Hertz, causing all pitch matching to fail.
- Passing 1D arrays for intervals instead of `(n, 2)` arrays, resulting in shape mismatch errors.
- Using `strict=True` when exact boundary matches are expected, causing them to fail because the check uses `<` instead of `<=`.

### Fix Code Hint
```python
# Ensure intervals are 2D arrays of shape (n, 2)
ref_intervals = np.atleast_2d(ref_intervals)
if ref_intervals.shape[1] != 2:
    raise ValueError("Intervals must have shape (n, 2)")

# Ensure pitches are 1D arrays
ref_pitches = np.atleast_1d(ref_pitches)
```

## API Test: `merge_chord_intervals`

### Signature
```python
def merge_chord_intervals(intervals, labels)
```
_Source: source/mir_eval/chord.py:1490_

_Source doc:_ Merge consecutive chord intervals if they represent the same chord. Parameters ---------- intervals : np.ndarray, shape=(n, 2), dtype=float Chord intervals to be merged, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. labels : list, shape=(n,) Chord labels to be merged, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. Returns ------- merged_ivs : np.ndarray, shape=(k, 2), dtype=float Merged chord intervals, k <= n

### Goal
Merges consecutive chord intervals into a single continuous interval if their corresponding string labels represent the same chord.

### Parameters
- `intervals`: A 2D numpy array of shape `(n, 2)` and dtype `float` representing the start and end times of chord intervals.
- `labels`: A list of length `n` containing string chord labels corresponding to each interval.

### Input
The caller must provide an `(n, 2)` numeric array of intervals and a parallel list of `n` string labels. These inputs are typically obtained directly from repository-format annotation files using `mir_eval.io.load_labeled_intervals`. The intervals should be consecutive (the end time of one matches the start time of the next) for merging to occur across boundaries.

### Output
Returns `unspecified` — A numpy array of shape `(k, 2)` and dtype `float` containing the merged chord intervals, where `k <= n`. Note that this function returns *only* the merged intervals array, not the corresponding merged labels.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

def test_merge_chord_intervals():
    intervals = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3], [3.0, 4.0], [4.0, 5.0]])
    # "C:maj" and "C:(1,3,5)" represent the same chord and will be merged.
    labels = ["C:maj", "C:(1,3,5)", "A:maj", "A:maj7", "A:maj7/3"]
    
    merged_intervals = mir_eval.chord.merge_chord_intervals(intervals, labels)
    
    assert np.allclose(
        np.array([[0.0, 2.0], [2.0, 3], [3.0, 4.0], [4.0, 5.0]]),
        merged_intervals,
    )
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.merge_chord_intervals`, provide an `(n, 2)` numpy array of intervals and a list of `n` labels. 
- Do not attempt to unpack the return value into multiple variables (like `intervals, labels = ...`); the function strictly returns a single numpy array of the merged intervals.
- Use `mir_eval.io.load_labeled_intervals` to safely load and format the inputs from text files before passing them to this function.

### Prompt Snippet
```text
Use `mir_eval.chord.merge_chord_intervals(intervals, labels)` to combine consecutive identical chords. It returns only the `(k, 2)` merged intervals array. Ensure `intervals` is an `(n, 2)` float array and `labels` is a list of length `n`.
```

### Common Failure Modes
- **Tuple Unpacking Error:** Attempting to unpack the result into `merged_intervals, merged_labels`. The function only returns the intervals array.
- **Shape Mismatch:** Passing a 1D array for `intervals` instead of the required `(n, 2)` shape.
- **Length Mismatch:** Passing an `intervals` array and a `labels` list that have different lengths (i.e., `intervals.shape[0] != len(labels)`).

### Fix Code Hint
```python
# BAD: Expecting both intervals and labels to be returned
merged_ivs, merged_lbls = mir_eval.chord.merge_chord_intervals(intervals, labels)

# GOOD: Assigning the single returned array
merged_ivs = mir_eval.chord.merge_chord_intervals(intervals, labels)
```

## API Test: `merge_labeled_intervals`

### Signature
```python
def merge_labeled_intervals(x_intervals, x_labels, y_intervals, y_labels)
```
_Source: source/mir_eval/util.py:481_

_Source doc:_ Merge the time intervals of two sequences. Parameters ---------- x_intervals : np.ndarray Array of interval times (seconds) x_labels : list or None List of labels y_intervals : np.ndarray Array of interval times (seconds) y_labels : list or None List of labels Returns ------- new_intervals : np.ndarray New interval times of the merged sequences. new_x_labels : list New labels for the sequence ``x`` new_y_labels : list New labels for the sequence ``y``

### Goal
Merge two sequences of labeled time intervals into a single, finer-grained sequence of intervals, propagating the corresponding labels from both original sequences to the new boundaries.

### Parameters
- `x_intervals`: `np.ndarray` of shape `(n, 2)` representing the start and end times (in seconds) of the first sequence of intervals.
- `x_labels`: `list` or `None` containing the labels corresponding to each interval in `x_intervals`.
- `y_intervals`: `np.ndarray` of shape `(m, 2)` representing the start and end times (in seconds) of the second sequence of intervals.
- `y_labels`: `list` or `None` containing the labels corresponding to each interval in `y_intervals`.

### Input
The caller must provide two valid interval arrays (where the first column is strictly less than the second column). Both interval sequences must span the exact same total time range (i.e., `x_intervals[0, 0] == y_intervals[0, 0]` and `x_intervals[-1, 1] == y_intervals[-1, 1]`). The labels can be of any type (e.g., strings, integers) but must be provided as Python lists with lengths matching the number of rows in their respective interval arrays.

### Output
Returns a tuple `(new_intervals, new_x_labels, new_y_labels)` — `new_intervals` is an `np.ndarray` of the merged interval times (shape `(k, 2)`). `new_x_labels` and `new_y_labels` are lists of length `k` containing the propagated labels for the sequence `x` and sequence `y`, respectively.

### Valid Call Patterns
```python
import numpy as np
from mir_eval import util

x_intvs = np.array([[0.0, 0.44], [0.44, 2.537], [2.537, 4.511], [4.511, 6.409]])
x_labels = ["A", "B", "C", "D"]

y_intvs = np.array([[0.0, 0.464], [0.464, 2.415], [2.415, 4.737], [4.737, 6.409]])
y_labels = [0, 1, 2, 3]

new_intvs, new_x_labels, new_y_labels = util.merge_labeled_intervals(
    x_intvs, x_labels, y_intvs, y_labels
)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.merge_labeled_intervals`, you MUST ensure that both `x_intervals` and `y_intervals` cover the exact same global time span. If the start time of the first interval or the end time of the last interval differ between the two sequences, the function will raise a `ValueError`.
- Pass intervals as `numpy.ndarray` objects of shape `(N, 2)` and labels as standard Python `list` objects.

### Prompt Snippet
```text
Ensure that the reference and estimated interval arrays span the exact same duration before merging them. You can use `mir_eval.util.adjust_intervals` or manually crop the arrays so that `x_intervals[0, 0] == y_intervals[0, 0]` and `x_intervals[-1, 1] == y_intervals[-1, 1]`. Then call `mir_eval.util.merge_labeled_intervals(x_intervals, x_labels, y_intervals, y_labels)`.
```

### Common Failure Modes
- **Mismatched sequence spans:** Raising a `ValueError` because `x_intervals[-1, 1] != y_intervals[-1, 1]` (e.g., one sequence ends at 6.409s and the other ends at 10.0s).
- **Mismatched array shapes or lengths:** Providing a label list whose length does not match the number of rows in the corresponding interval array.
- **Invalid interval arrays:** Passing 1D arrays instead of 2D `(N, 2)` arrays for the intervals.

### Fix Code Hint
```python
# Check and force the end times to match if they are slightly off due to rounding
if not np.isclose(x_intervals[-1, 1], y_intervals[-1, 1]):
    common_end = min(x_intervals[-1, 1], y_intervals[-1, 1])
    x_intervals[-1, 1] = common_end
    y_intervals[-1, 1] = common_end

new_intvs, new_x_labels, new_y_labels = util.merge_labeled_intervals(
    x_intervals, x_labels, y_intervals, y_labels
)
```

## API Test: `metrics`

### Signature
```python
def metrics(ref_time, ref_freqs, est_time, est_freqs, **kwargs)
```
_Source: source/mir_eval/multipitch.py:348_

_Source doc:_ Compute multipitch metrics. All metrics are computed at the 'macro' level such that the frame true positive/false positive/false negative rates are summed across time and the metrics are computed on the combined values. Examples -------- >>> ref_time, ref_freqs = mir_eval.io.load_ragged_time_series( ...     'reference.txt') >>> est_time, est_freqs = mir_eval.io.load_ragged_time_series( ...     'estimated.txt') >>> metris_tuple = mir_eval.multipitch.metrics( ...     ref_time, ref_freqs, est_time, est_freqs) Parameters ---------- ref_time : np.ndarray Time of each reference frequency value ref_freqs : list of np.ndarray List of np.ndarrays of reference frequency values est_time : np.ndarray Time of each estimated frequency value est_freqs : list of np.ndarray List of np.ndarrays of estimate frequency values **kwargs Additional keyword arguments which will be passed to the appropriate metric or preprocessing functions. Returns ------- precision : float Precision (TP/(TP + FP)) recall : float Recall (TP/(TP + FN)) accuracy : float Accuracy (TP/(TP + FP + FN)) e_sub : float Substitution error e_miss : float Miss error e_fa : float False alarm error e_tot : float Total error precision_chroma : float Chroma precision recall_chroma : float Chroma recall accuracy_chroma : float Chroma accuracy e_sub_chroma : float Chroma substitution error e_miss_chroma : float Chroma miss error e_fa_chroma : float Chroma false alarm error e_tot_chroma : float Chroma total error

### Goal
Compute a comprehensive suite of multipitch evaluation metrics (precision, recall, accuracy, and various error rates, both standard and chroma-based) at the macro level across time frames.

### Parameters
- `ref_time`: A 1D `np.ndarray` representing the time (in seconds) of each reference frequency frame.
- `ref_freqs`: A `list` of `np.ndarray`s containing the reference frequency values (in Hz) present at each corresponding time frame.
- `est_time`: A 1D `np.ndarray` representing the time (in seconds) of each estimated frequency frame.
- `est_freqs`: A `list` of `np.ndarray`s containing the estimated frequency values (in Hz) present at each corresponding time frame.
- `**kwargs`: Additional keyword arguments passed to the underlying metric or preprocessing functions.

### Input
The caller must provide time arrays and corresponding ragged frequency arrays (lists of arrays, because the number of pitches can vary per time frame). These are typically loaded from repository-format text files using `mir_eval.io.load_ragged_time_series`. The lengths of `ref_time` and `ref_freqs` must match, as must the lengths of `est_time` and `est_freqs`.

### Output
Returns `unspecified` — A tuple of 14 `float` values representing the computed metrics in the following exact order: `precision`, `recall`, `accuracy`, `e_sub` (substitution error), `e_miss` (miss error), `e_fa` (false alarm error), `e_tot` (total error), `precision_chroma`, `recall_chroma`, `accuracy_chroma`, `e_sub_chroma`, `e_miss_chroma`, `e_fa_chroma`, and `e_tot_chroma`.

### Valid Call Patterns
```python
import mir_eval

# Load ragged time series data from text files
ref_time, ref_freqs = mir_eval.io.load_ragged_time_series('reference.txt')
est_time, est_freqs = mir_eval.io.load_ragged_time_series('estimated.txt')

# Compute the tuple of 14 multipitch metrics
metrics_tuple = mir_eval.multipitch.metrics(
    ref_time, ref_freqs, est_time, est_freqs
)
```

### LLM Instruction Prompt
- When evaluating multipitch data, use `mir_eval.io.load_ragged_time_series` to parse the text files into the required `list of np.ndarray` format for frequencies.
- Do not pass standard 2D numpy arrays for frequencies; multipitch data is inherently ragged (varying number of active pitches per frame).
- Note that `mir_eval.multipitch.metrics` returns a tuple of 14 floats, unlike the high-level `evaluate()` functions which return a dictionary. Unpack or index the tuple accordingly.

### Prompt Snippet
```text
Use `mir_eval.multipitch.metrics(ref_time, ref_freqs, est_time, est_freqs)` to compute multipitch accuracy. Ensure `ref_freqs` and `est_freqs` are lists of 1D numpy arrays (ragged arrays), ideally loaded via `mir_eval.io.load_ragged_time_series`. The function returns a 14-element tuple of floats.
```

### Common Failure Modes
- Passing a 2D `np.ndarray` for `ref_freqs` or `est_freqs` instead of a `list` of 1D `np.ndarray`s, which fails because multipitch frames have variable numbers of pitches.
- Mismatched lengths between the time array (`ref_time`) and the frequency list (`ref_freqs`).
- Attempting to access the return value as a dictionary by key (e.g., `result['Precision']`), which fails because this specific function returns a tuple of floats.

### Fix Code Hint
```python
# INCORRECT: Assuming frequencies can be loaded as a standard 2D array
# ref_data = np.loadtxt('reference.txt')
# ref_time, ref_freqs = ref_data[:, 0], ref_data[:, 1:]

# CORRECT: Use the built-in ragged time series loader
ref_time, ref_freqs = mir_eval.io.load_ragged_time_series('reference.txt')
est_time, est_freqs = mir_eval.io.load_ragged_time_series('estimated.txt')
metrics_tuple = mir_eval.multipitch.metrics(ref_time, ref_freqs, est_time, est_freqs)
precision = metrics_tuple[0]
```

## API Test: `midi_to_chroma`

### Signature
```python
def midi_to_chroma(frequencies_midi)
```
_Source: source/mir_eval/multipitch.py:173_

_Source doc:_ Wrap MIDI frequencies to a single octave (chroma). Parameters ---------- frequencies_midi : list of np.ndarray Continuous MIDI note frequency values. Returns ------- frequencies_chroma : list of np.ndarray Midi values wrapped to one octave.

### Goal
Wrap continuous MIDI note frequency values to a single octave (chroma representation) for multipitch evaluation.

### Parameters
- `frequencies_midi`: A list of `np.ndarray` objects containing continuous MIDI note frequency values (e.g., 69.0 for A4).

### Input
The caller must provide a list of 1-dimensional NumPy arrays, where each array corresponds to a specific time frame and contains the continuous MIDI note numbers active at that time. Empty arrays (`np.array([])`) are permitted and expected for frames where no pitches are active. The values must be in the MIDI pitch scale, not raw Hertz frequencies.

### Output
Returns `unspecified` — A list of `np.ndarray` objects of the same length and shape as the input, where the continuous MIDI values have been wrapped to a single octave (chroma).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

midi_frequencies = [
    np.array([69.0]),
    np.array([]),
    np.array([57.0, 76.01955000865388, 71.623683437704088]),
    np.array([62.369507723654657, 71.623683437704088]),
]
actual_chroma = mir_eval.multipitch.midi_to_chroma(midi_frequencies)
```

### LLM Instruction Prompt
- When calling `mir_eval.multipitch.midi_to_chroma`, ensure the input is a list of `np.ndarray` objects containing continuous MIDI note values, not raw Hz frequencies.
- Because multipitch data has a variable number of pitches per frame, the input must be a list of arrays (one array per time frame), not a single dense 2D array. Use empty arrays for silent frames.

### Prompt Snippet
```text
`mir_eval.multipitch.midi_to_chroma(frequencies_midi)` wraps a list of NumPy arrays containing continuous MIDI note values to a single octave (chroma). Input must be a list of arrays (one per frame).
```

### Common Failure Modes
- Passing raw Hertz frequencies instead of MIDI note numbers, resulting in incorrect chroma wrapping.
- Passing a single flat or dense 2D NumPy array instead of a list of 1D NumPy arrays, which violates the expected multipitch data structure.
- Passing a list of standard Python lists instead of a list of `np.ndarray` objects.

### Fix Code Hint
```python
# INCORRECT: Passing a flat array or raw Hz frequencies
# chroma = mir_eval.multipitch.midi_to_chroma(np.array([440.0, 880.0]))

# CORRECT: Pass a list of NumPy arrays containing MIDI note numbers
midi_frames = [
    np.array([69.0]), # A4
    np.array([])      # Silence
]
chroma = mir_eval.multipitch.midi_to_chroma(midi_frames)
```

## API Test: `midi_to_hz`

### Signature
```python
def midi_to_hz(midi)
```
_Source: source/mir_eval/util.py:930_

_Source doc:_ Convert MIDI numbers to Hz Parameters ---------- midi : number or ndarray MIDI notes Returns ------- freqs : number or ndarray Frequency/frequencies in Hz corresponding to `midi`

### Goal
Convert MIDI note numbers to their corresponding acoustic frequencies in Hertz (Hz).

### Parameters
- `midi`: A numeric scalar (integer or float) or a NumPy `ndarray` of numbers representing MIDI notes.

### Input
The caller must provide numeric data representing MIDI pitches. If providing multiple values simultaneously, the input should be a NumPy `ndarray` of numeric types (e.g., `float64`). 

### Output
Returns `unspecified` — A number or a NumPy `ndarray` containing the frequency or frequencies in Hz corresponding to the input `midi` values. The return type matches the shape and structure of the input (scalar for scalar input, array for array input).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example inferred from signature (not verified by test suite)
midi_scalar = 69.0
hz_scalar = mir_eval.util.midi_to_hz(midi_scalar)

# Example with a NumPy array
midi_array = np.array([60.0, 69.0, 72.0])
hz_array = mir_eval.util.midi_to_hz(midi_array)
```

### LLM Instruction Prompt
- When converting MIDI note numbers to frequencies in Hz, use `mir_eval.util.midi_to_hz(midi)`. The `midi` parameter accepts either a single scalar number or a NumPy `ndarray` of numbers. If processing a sequence of notes, ensure the input is cast to a NumPy array rather than a standard Python list to guarantee compatibility with vectorized mathematical operations.

### Prompt Snippet
```text
mir_eval.util.midi_to_hz(midi) converts MIDI note numbers to Hz. Accepts and returns a scalar number or a NumPy ndarray.
```

### Common Failure Modes
- Passing a standard Python `list` instead of a NumPy `ndarray`, which may cause `TypeError` or `AttributeError` if the internal implementation relies on NumPy's vectorized arithmetic operations.
- Passing string representations of numbers or note names (e.g., `"C4"`, `"60"`) instead of numeric types.

### Fix Code Hint
```python
# Convert standard lists to NumPy arrays before calling
midi_list = [60, 64, 67]
midi_array = np.array(midi_list, dtype=float)
frequencies = mir_eval.util.midi_to_hz(midi_array)
```

## API Test: `mirex`

### Signature
```python
def mirex(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1044_

_Source doc:_ Compare chords along MIREX rules. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.mirex(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Compare reference and estimated chord labels according to MIREX (Music Information Retrieval Evaluation eXchange) rules to produce an array of segment-level scores.

### Parameters
- `reference_labels`: A list of length `n` containing the reference (ground truth) chord labels as strings.
- `estimated_labels`: A list of length `n` containing the estimated (predicted) chord labels as strings.

### Input
Both inputs must be lists of strings of the exact same length `n`. The strings must be valid chord labels (they are validated using regular expressions and restricted to valid chord types from `mir_eval.chord.QUALITIES`). Because chord annotations typically span different time intervals, callers must first align the reference and estimated labels in time. This is done by loading the labeled intervals, adjusting the estimated boundaries to match the reference boundaries using `mir_eval.util.adjust_intervals`, and then merging them into a common time grid using `mir_eval.util.merge_labeled_intervals`.

### Output
Returns `unspecified` — A 1D numpy array (`np.ndarray`) of shape `(n,)` and dtype `float` containing the comparison scores for each aligned label pair. Scores are bounded in the range `[0.0, 1.0]`.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Deterministic in-memory arrays representing loaded interval data
ref_intervals = np.array([[0.0, 2.0], [2.0, 4.0]])
ref_labels = ['C:maj', 'G:maj']

est_intervals = np.array([[0.0, 1.5], [1.5, 4.0]])
est_labels = ['C:maj', 'G:7']

# 1. Adjust estimated intervals to match reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# 2. Merge intervals to create perfectly aligned label lists of equal length 'n'
intervals, merged_ref_labels, merged_est_labels = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# 3. Compute MIREX scores on the aligned label lists
comparisons = mir_eval.chord.mirex(merged_ref_labels, merged_est_labels)

# (Optional) Compute the final weighted accuracy using the merged interval durations
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.mirex`, you MUST provide two lists of strings of the exact same length. Do not pass raw, unaligned label lists directly if they come from different time segmentations. First, align the time intervals using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals` to generate matching label lists. Ensure all chord strings are valid according to `mir_eval.chord.QUALITIES`.

### Prompt Snippet
```text
Use `mir_eval.chord.mirex(reference_labels, estimated_labels)` to compute MIREX chord comparison scores. Both arguments must be lists of strings of equal length `n`. Pre-align the labels using `mir_eval.util.merge_labeled_intervals` before scoring. Returns a float numpy array of shape `(n,)` with scores in `[0.0, 1.0]`.
```

### Common Failure Modes
- **Unequal List Lengths:** Passing `reference_labels` and `estimated_labels` of different lengths because the caller skipped the `merge_labeled_intervals` alignment step.
- **Invalid Chord Syntax:** Passing chord strings that fail internal regular expression validation or contain qualities not present in `mir_eval.chord.QUALITIES`.
- **Passing Intervals Instead of Labels:** Accidentally passing the `(n, 2)` numpy arrays of time intervals instead of the 1D lists of string labels.

### Fix Code Hint
```python
# If labels are of different lengths or unaligned, merge them first:
intervals, aligned_ref_labels, aligned_est_labels = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
# Then pass the aligned string lists to mirex:
comparisons = mir_eval.chord.mirex(aligned_ref_labels, aligned_est_labels)
```

## API Test: `multipitch`

### Signature
```python
def multipitch(times, frequencies, midi=False, unvoiced=False, ax=None, prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:762_

_Source doc:_ Visualize multiple f0 measurements Parameters ---------- times : np.ndarray, shape=(n,) Sample times of frequencies frequencies : list of np.ndarray frequencies (in Hz) of the pitch measurements. Voicing is indicated by sign (positive for voiced, non-positive for non-voiced). `times` and `frequencies` should be in the format produced by :func:`mir_eval.io.load_ragged_time_series` midi : bool If `True`, plot on a MIDI-numbered vertical axis. Otherwise, plot on a linear frequency axis. unvoiced : bool If `True`, unvoiced pitches are plotted and indicated by transparency. Otherwise, unvoiced pitches are omitted from the display. ax : matplotlib.pyplot.axes An axis handle on which to draw the pitch contours. If none is provided, a new set of axes is created. prop_cycle : cycle.Cycler An optional property cycle object to specify style properties. If not provided, the default property cycler will be retrieved from matplotlib. **kwargs Additional keyword arguments to `plt.scatter`. Returns ------- ax : matplotlib.pyplot.axes._subplots.AxesSubplot A handle to the (possibly constructed) plot axes

### Goal
Visualize multiple fundamental frequency (f0) measurements (multipitch contours) over time on either a linear frequency or MIDI-numbered axis.

### Parameters
- `times`: `np.ndarray`, shape=(n,). Sample times of the frequencies.
- `frequencies`: `list` of `np.ndarray`. Frequencies (in Hz) of the pitch measurements. Voicing is indicated by sign (positive for voiced, non-positive for non-voiced).
- `midi`, default `False`: `bool`. If `True`, plots on a MIDI-numbered vertical axis. Otherwise, plots on a linear frequency axis.
- `unvoiced`, default `False`: `bool`. If `True`, unvoiced pitches are plotted and indicated by transparency. Otherwise, unvoiced pitches are omitted from the display.
- `ax`, default `None`: `matplotlib.pyplot.axes`. An axis handle on which to draw the pitch contours. If none is provided, a new set of axes is created.
- `prop_cycle`, default `None`: `cycle.Cycler`. An optional property cycle object to specify style properties. If not provided, the default property cycler will be retrieved from matplotlib.
- `**kwargs`: Additional keyword arguments passed directly to `matplotlib.pyplot.scatter`.

### Input
The caller must provide `times` as a 1D numpy array and `frequencies` as a list of 1D numpy arrays (a ragged time series). These inputs should strictly follow the format produced by `mir_eval.io.load_ragged_time_series`. Voicing must be indicated by the sign of the frequency values (positive for voiced, non-positive for unvoiced). For automated testing or agentic workflows, the matplotlib environment must be configured to run headlessly without network or audio-device access.

### Output
Returns `unspecified` — a `matplotlib.pyplot.axes._subplots.AxesSubplot` object representing the handle to the (possibly constructed) plot axes containing the scatter plot of the multipitch contours.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval
from mir_eval.io import load_ragged_time_series

# Ensure headless execution for automated environments
plt.switch_backend('Agg')

plt.figure()
times, pitches = load_ragged_time_series("data/multipitch/est01.txt")

# Plot pitches on a linear frequency scale, including unvoiced pitches
ax = mir_eval.display.multipitch(times, pitches, midi=False, unvoiced=True)

# Plot pitches on a linear frequency scale, omitting unvoiced pitches
plt.figure()
ax2 = mir_eval.display.multipitch(times, pitches, midi=False, unvoiced=False)
```

### LLM Instruction Prompt
- Always load multipitch data using `mir_eval.io.load_ragged_time_series` to guarantee that `times` and `frequencies` are in the required ragged format (a 1D array of times and a list of 1D arrays of frequencies).
- Do not pass a dense 2D numpy array for `frequencies`; it must be a list of arrays to handle polyphony correctly.
- Ensure that any generated display tests are kept headless (e.g., using `matplotlib.use('Agg')`) and do not attempt to access network or audio devices.
- Remember that voicing is determined by the sign of the frequency. If you want to visualize unvoiced pitches, you must pass `unvoiced=True`.

### Prompt Snippet
```text
mir_eval.display.multipitch visualizes multipitch contours. Inputs `times` (1D array) and `frequencies` (list of 1D arrays) MUST be in the ragged format produced by `mir_eval.io.load_ragged_time_series`. Voicing is indicated by sign. Keep display tests headless (e.g., `plt.switch_backend('Agg')`).
```

### Common Failure Modes
- **Incorrect Frequency Format:** Passing a dense 2D `np.ndarray` for `frequencies` instead of a `list` of `np.ndarray`s. The function expects a ragged time series because the number of simultaneous pitches varies per time frame.
- **Environment Blocking:** Failing to configure a headless matplotlib backend (like `Agg`) in CI/CD or agentic environments, causing the script to hang or crash when attempting to open a GUI window.
- **Missing Unvoiced Pitches:** Expecting unvoiced pitches to appear by default. They are omitted unless `unvoiced=True` is explicitly passed.
- **Incorrect Voicing Representation:** Representing unvoiced pitches with `NaN` or positive values instead of non-positive values (≤ 0), which breaks the internal sign-based voicing logic.

### Fix Code Hint
```python
import matplotlib
matplotlib.use('Agg') # Enforce headless mode
import matplotlib.pyplot as plt
import mir_eval

# Correctly load ragged time series data
times, frequencies = mir_eval.io.load_ragged_time_series("data/multipitch/est01.txt")

fig, ax = plt.subplots()
# Pass the ragged data and the axis handle
mir_eval.display.multipitch(times, frequencies, unvoiced=True, ax=ax)
```

## API Test: `mutual_information`

### Signature
```python
def mutual_information(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1)
```
_Source: source/mir_eval/segment.py:869_

_Source doc:_ Frame-clustering segmentation: mutual information metrics. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> # Trim or pad the estimate to match reference timing >>> (ref_intervals, ...  ref_labels) = mir_eval.util.adjust_intervals(ref_intervals, ...                                               ref_labels, ...                                               t_min=0) >>> (est_intervals, ...  est_labels) = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()) >>> mi, ami, nmi = mir_eval.structure.mutual_information(ref_intervals, ...                                                      ref_labels, ...                                                      est_intervals, ...                                                      est_labels) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. reference_labels : list, shape=(n,) reference segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_labels : list, shape=(m,) estimated segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. frame_size : float > 0 length (in seconds) of frames for clustering (Default value = 0.1) Returns ------- MI : float > 0 Mutual information between segmentations AMI : float Adjusted mutual information between segmentations. NMI : float > 0 Normalize mutual information between segmentations

### Goal
Computes frame-clustering segmentation mutual information metrics (Mutual Information, Adjusted Mutual Information, and Normalized Mutual Information) between reference and estimated segmentations.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` representing the reference segment start and end times in seconds.
- `reference_labels`: `list` of length `n` containing the reference segment labels corresponding to the intervals.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` representing the estimated segment start and end times in seconds.
- `estimated_labels`: `list` of length `m` containing the estimated segment labels corresponding to the intervals.
- `frame_size`, default `0.1`: A strictly positive `float` representing the length (in seconds) of the frames used for clustering the segmentations.

### Input
Intervals and labels are typically loaded from repository-format text files using `mir_eval.io.load_labeled_intervals`. The intervals must be 2D numpy arrays of shape `(n, 2)` and `(m, 2)`, and the labels must be lists of matching lengths. 
**Precondition:** The estimated intervals should be trimmed or padded to match the reference timing (e.g., using `mir_eval.util.adjust_intervals(..., t_min=0, t_max=ref_intervals.max())`) before calling this function, as mismatched total durations will skew the frame-clustering alignment.

### Output
Returns `unspecified` — A tuple of three floats `(MI, AMI, NMI)`:
1. `MI`: Mutual information between segmentations (float > 0).
2. `AMI`: Adjusted mutual information between segmentations (float).
3. `NMI`: Normalized mutual information between segmentations (float > 0).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Using deterministic in-memory arrays (from test suite)
reference_intervals = np.array([[0.0, 1.0], [1.0, 2.0]])
estimated_intervals = np.array([[0.0, 1.0], [1.0, 2.0]])
labels = ["a", "b"]

mi, ami, nmi = mir_eval.segment.mutual_information(
    reference_intervals, labels, estimated_intervals, labels
)

# 2. Using loaded and adjusted intervals (from source doc)
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# Trim or pad the estimate to match reference timing
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)

mi, ami, nmi = mir_eval.segment.mutual_information(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

### LLM Instruction Prompt
- When evaluating segmentation mutual information, always ensure the estimated intervals are adjusted to match the reference time span using `mir_eval.util.adjust_intervals` before calling `mir_eval.segment.mutual_information`.
- Pass intervals as `(n, 2)` numpy arrays and labels as standard Python lists.
- Do not pass a `frame_size` less than or equal to 0.

### Prompt Snippet
```text
Ensure that the estimated segmentation intervals are adjusted to the reference boundaries using `mir_eval.util.adjust_intervals` before computing `mir_eval.segment.mutual_information`. The function returns a tuple of three floats: (MI, AMI, NMI).
```

### Common Failure Modes
- **Mismatched Time Spans:** Failing to adjust the estimated intervals to match the reference `t_min` and `t_max`. This causes the frame clustering to misalign or evaluate over different total durations.
- **Shape Errors:** Passing 1D arrays for intervals instead of `(n, 2)` arrays, or passing labels lists that do not match the length of their respective intervals array.
- **Invalid Frame Size:** Passing `frame_size=0` or a negative value, which violates the `float > 0` constraint and causes division-by-zero or clustering errors.

### Fix Code Hint
```python
# FIX: Adjust intervals to ensure matching time spans before computing mutual information
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0.0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0.0, t_max=ref_intervals.max()
)
mi, ami, nmi = mir_eval.segment.mutual_information(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

## API Test: `nce`

### Signature
```python
def nce(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1, beta=1.0, marginal=False)
```
_Source: source/mir_eval/segment.py:960_

_Source doc:_ Frame-clustering segmentation: normalized conditional entropy Computes cross-entropy of cluster assignment, normalized by the max-entropy. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> # Trim or pad the estimate to match reference timing >>> (ref_intervals, ...  ref_labels) = mir_eval.util.adjust_intervals(ref_intervals, ...                                               ref_labels, ...                                               t_min=0) >>> (est_intervals, ...  est_labels) = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()) >>> S_over, S_under, S_F = mir_eval.structure.nce(ref_intervals, ...                                               ref_labels, ...                                               est_intervals, ...                                               est_labels) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. reference_labels : list, shape=(n,) reference segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_labels : list, shape=(m,) estimated segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. frame_size : float > 0 length (in seconds) of frames for clustering (Default value = 0.1) beta : float > 0 beta for F-measure (Default value = 1.0) marginal : bool If `False`, normalize conditional entropy by uniform entropy. If `True`, normalize conditional entropy by the marginal entropy. (Default value = False) Returns ------- S_over Over-clustering score: - For `marginal=False`, ``1 - H(y_est | y_ref) / log(|y_est|)`` - For `marginal=True`, ``1 - H(y_est | y_ref) / H(y_est)`` If `|y_est|==1`, then `S_over` will be 0. S_under

### Goal
Computes the normalized conditional entropy (cross-entropy of cluster assignment normalized by max-entropy) for frame-clustering segmentation evaluation.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` representing reference segment intervals, typically in the format returned by `mir_eval.io.load_labeled_intervals`.
- `reference_labels`: `list` of length `n` representing reference segment labels.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` representing estimated segment intervals.
- `estimated_labels`: `list` of length `m` representing estimated segment labels.
- `frame_size`, default `0.1`: `float > 0` representing the length (in seconds) of frames for clustering.
- `beta`, default `1.0`: `float > 0` representing the beta parameter for the F-measure calculation.
- `marginal`, default `False`: `bool` flag. If `False`, normalizes conditional entropy by uniform entropy. If `True`, normalizes by the marginal entropy.

### Input
The caller must provide reference and estimated intervals and labels, typically loaded from repository-format text files using `mir_eval.io.load_labeled_intervals`. As a strict precondition, the estimated intervals must be trimmed or padded to match the reference timing before calling this function (e.g., using `mir_eval.util.adjust_intervals`).

### Output
Returns `unspecified` — A tuple of three floats `(S_over, S_under, S_F)` representing the over-clustering score, the under-clustering score, and their F-measure. If the number of unique estimated labels is 1 (`|y_est|==1`), `S_over` will be 0.

### Valid Call Patterns
```python
import mir_eval

# Load intervals and labels
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# Precondition: Trim or pad the estimate to match reference timing
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)

# Compute Normalized Conditional Entropy
S_over, S_under, S_F = mir_eval.segment.nce(
    ref_intervals, 
    ref_labels, 
    est_intervals, 
    est_labels,
    marginal=True
)
```

### LLM Instruction Prompt
- When evaluating segmentation using `mir_eval.segment.nce`, you MUST align the time spans of the estimated and reference intervals first using `mir_eval.util.adjust_intervals`.
- Pass `marginal=True` if the evaluation requires normalizing the conditional entropy by the marginal entropy instead of the default uniform entropy.
- Ensure intervals are passed as `(n, 2)` numpy arrays and labels as lists.

### Prompt Snippet
```text
Ensure you preprocess the segmentation intervals with `mir_eval.util.adjust_intervals` to match the reference timing before calling `mir_eval.segment.nce`.
```

### Common Failure Modes
- Failing to align the start and end times of the reference and estimated intervals, leading to mismatched frame clustering bounds.
- Passing labels as numpy arrays instead of lists, or intervals as 1D arrays instead of `(n, 2)` shape arrays.
- Providing a `frame_size` or `beta` that is less than or equal to 0.

### Fix Code Hint
```python
# FIX: Ensure intervals are adjusted to the same time span before calling nce
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(ref_intervals, ref_labels, t_min=0)
est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, t_min=0, t_max=ref_intervals.max())
S_over, S_under, S_F = mir_eval.segment.nce(ref_intervals, ref_labels, est_intervals, est_labels)
```

## API Test: `occurrence_FPR`

### Signature
```python
def occurrence_FPR(reference_patterns, estimated_patterns, thres=0.75, similarity_metric='cardinality_score')
```
_Source: source/mir_eval/pattern.py:299_

_Source doc:_ Compute the occurrence F1 Score, Precision and Recall. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> F, P, R = mir_eval.pattern.occurrence_FPR(ref_patterns, ...                                           est_patterns) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format thres : float How similar two occurrences must be in order to be considered equal (Default value = .75) similarity_metric : str A string representing the metric to be used when computing the similarity matrix. Accepted values: - "cardinality_score": Count of the intersection between occurrences. (Default value = "cardinality_score") Returns ------- f_measure : float The occurrence F1 Score precision : float The occurrence Precision recall : float The occurrence Recall

### Goal
Compute the occurrence F1 Score, Precision, and Recall for pattern discovery evaluation in music information retrieval.

### Parameters
- `reference_patterns`: A list of ground truth reference patterns, strictly in the format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: A list of estimated patterns to evaluate, in the same format as `reference_patterns`.
- `thres`, default `0.75`: A float representing the threshold for how similar two occurrences must be in order to be considered equal.
- `similarity_metric`, default `'cardinality_score'`: A string representing the metric to be used when computing the similarity matrix. The only accepted value is `"cardinality_score"` (which counts the intersection between occurrences).

### Input
The caller must provide reference and estimated patterns that have been parsed into lists using `mir_eval.io.load_patterns()`. Do not pass raw file paths or unparsed text strings directly to this function.

### Output
Returns `unspecified` — A tuple of three floats `(f_measure, precision, recall)` representing the occurrence F1 Score, the occurrence Precision, and the occurrence Recall, respectively.

### Valid Call Patterns
```python
import mir_eval

# Load patterns from repository-format text files
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

# Compute occurrence F-measure, Precision, and Recall
F, P, R = mir_eval.pattern.occurrence_FPR(
    ref_patterns, 
    est_patterns, 
    thres=0.75, 
    similarity_metric='cardinality_score'
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery using `mir_eval.pattern.occurrence_FPR`, you MUST first load the pattern text files using `mir_eval.io.load_patterns()`.
- Do not pass file paths directly to `occurrence_FPR`.
- Expect a tuple of three floats `(F, P, R)` as the return value.
- Do not invent or use similarity metrics other than `"cardinality_score"`.

### Prompt Snippet
```text
mir_eval.pattern.occurrence_FPR(reference_patterns, estimated_patterns, thres=0.75, similarity_metric='cardinality_score')
Computes occurrence F1 Score, Precision, and Recall for MIR pattern discovery. Inputs must be lists loaded via `mir_eval.io.load_patterns()`. Returns a tuple of floats: (f_measure, precision, recall).
```

### Common Failure Modes
- **Passing file paths instead of lists**: Providing string file paths directly to `occurrence_FPR` will cause a failure. The function expects the parsed list structures returned by `mir_eval.io.load_patterns()`.
- **Invalid similarity metric**: Passing a string other than `"cardinality_score"` to `similarity_metric` is unsupported and will fail.
- **Unpacking errors**: Failing to unpack the return value into exactly three variables `(F, P, R)`.

### Fix Code Hint
```python
# INCORRECT: Passing file paths directly
# F, P, R = mir_eval.pattern.occurrence_FPR("ref.txt", "est.txt")

# CORRECT: Load patterns first
import mir_eval
ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
F, P, R = mir_eval.pattern.occurrence_FPR(ref_patterns, est_patterns)
```

## API Test: `offset_precision_recall_f1`

### Signature
```python
def offset_precision_recall_f1(ref_intervals, est_intervals, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False, beta=1.0)
```
_Source: source/mir_eval/transcription.py:705_

_Source doc:_ Compute the Precision, Recall and F-measure of note offsets: an estimated offset is considered correct if it is within +-50ms (or 20% of the ref note duration, which ever is greater) of a reference offset. Note that this metric completely ignores note onsets and note pitch. This means an estimated offset will be considered correct if it matches a reference offset, even if the offsets come from notes with completely different pitches (i.e. notes that would not match with :func:`match_notes`). Examples -------- >>> ref_intervals, _ = mir_eval.io.load_valued_intervals( ...     'reference.txt') >>> est_intervals, _ = mir_eval.io.load_valued_intervals( ...     'estimated.txt') >>> (offset_precision, ...  offset_recall, ...  offset_f_measure) = mir_eval.transcription.offset_precision_recall_f1( ...      ref_intervals, est_intervals) Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) offset_ratio : float > 0 or None The ratio of the reference note's duration used to define the offset_tolerance. Default is 0.2 (20%), meaning the ``offset_tolerance`` will equal the ``ref_duration * 0.2``, or ``offset_min_tolerance`` (0.05 by default, i.e. 50 ms), whichever is greater. offset_min_tolerance : float > 0 The minimum tolerance for offset matching. See ``offset_ratio`` description for an explanation of how the offset tolerance is determined. strict : bool If ``strict=False`` (the default), threshold checks for onset matching are performed using ``<=`` (less than or equal). If ``strict=True``, the threshold checks are performed using ``<`` (less than). beta : float > 0 Weighting factor for f-measure (default value = 1.0). Returns ------- precision : float The computed precision score recall : float The computed recall score f_measure : float The computed F-measure score

### Goal
Compute the precision, recall, and F-measure of note offsets by comparing estimated and reference intervals, completely ignoring note onsets and pitches.

### Parameters
- `ref_intervals`: `np.ndarray, shape=(n,2)` — Array of reference note time intervals (onset and offset times in seconds).
- `est_intervals`: `np.ndarray, shape=(m,2)` — Array of estimated note time intervals (onset and offset times in seconds).
- `offset_ratio`, default `0.2`: `float > 0 or None` — The ratio of the reference note's duration used to define the offset tolerance. Default is 20%.
- `offset_min_tolerance`, default `0.05`: `float > 0` — The minimum absolute tolerance for offset matching in seconds. Default is 50 ms.
- `strict`, default `False`: `bool` — If `False`, threshold checks for matching use `<=` (less than or equal). If `True`, checks use `<` (strictly less than).
- `beta`, default `1.0`: `float > 0` — Weighting factor for the F-measure calculation.

### Input
`ref_intervals` and `est_intervals` must be 2D numpy arrays of shape `(n, 2)` and `(m, 2)` respectively, representing `[onset, offset]` pairs. Empty arrays of shape `(0, 2)` are permitted; if one array is empty and the other is not, the function deterministically returns `(0.0, 0.0, 0.0)`. If your data includes pitches or velocities (e.g., shape `(n, 3)`), you must slice the array to pass only the first two columns.

### Output
Returns `unspecified` — A 3-tuple of floats `(precision, recall, f_measure)` representing the computed evaluation scores for the note offsets.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Standard evaluation using loaded or generated intervals
ref_intervals = np.array([[0.5, 1.2], [1.5, 2.5]])
est_intervals = np.array([[0.6, 1.22], [1.4, 2.45]])

precision, recall, f_measure = mir_eval.transcription.offset_precision_recall_f1(
    ref_intervals, est_intervals
)

# 2. Handling empty arrays gracefully
ref_empty = np.empty(shape=(0, 2))
est_intervals = np.array([[0.0, 1.0]])

precision, recall, f1 = mir_eval.transcription.offset_precision_recall_f1(
    ref_empty, est_intervals
)
assert (precision, recall, f1) == (0, 0, 0)
```

### LLM Instruction Prompt
- When evaluating transcription offsets independently of onsets and pitches, use `mir_eval.transcription.offset_precision_recall_f1`.
- Ensure inputs are strictly 2D numpy arrays of shape `(n, 2)` containing `[onset, offset]` times. Slice larger arrays (e.g., `intervals[:, :2]`) if they contain extra columns like pitch or velocity.
- Expect a 3-tuple of floats `(precision, recall, f_measure)` as the return value.
- Do not use this function if you need to evaluate pitch accuracy or onset accuracy; it explicitly ignores both.

### Prompt Snippet
```text
mir_eval.transcription.offset_precision_recall_f1(ref_intervals, est_intervals, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False, beta=1.0)
Computes Precision, Recall, and F-measure of note offsets. An estimated offset is correct if it is within +-50ms (or 20% of the ref note duration, whichever is greater) of a reference offset. Ignores onsets and pitches. Inputs must be (n, 2) numpy arrays of [onset, offset] times. Returns a tuple: (precision, recall, f_measure).
```

### Common Failure Modes
- **Incorrect Array Shape**: Passing 1D arrays or arrays with more than 2 columns (e.g., `[onset, offset, pitch]`) will cause shape mismatch errors.
- **Misunderstanding the Metric**: Assuming this metric evaluates full note correctness. It *only* evaluates offsets. An estimated offset will be considered correct if it matches a reference offset, even if the notes have completely different pitches or onsets.
- **Passing Lists Instead of Arrays**: While `mir_eval` sometimes coerces lists, passing native Python lists instead of `np.ndarray` can lead to unexpected behavior or attribute errors during internal numpy operations.

### Fix Code Hint
```python
# If your data includes pitches (e.g., shape (n, 3)), slice it before passing:
ref_intervals = REF_DATA[:, :2]
est_intervals = EST_DATA[:, :2]

precision, recall, f_measure = mir_eval.transcription.offset_precision_recall_f1(
    ref_intervals, est_intervals
)
```

## API Test: `onset_precision_recall_f1`

### Signature
```python
def onset_precision_recall_f1(ref_intervals, est_intervals, onset_tolerance=0.05, strict=False, beta=1.0)
```
_Source: source/mir_eval/transcription.py:643_

_Source doc:_ Compute the Precision, Recall and F-measure of note onsets: an estimated onset is considered correct if it is within +-50ms of a reference onset. Note that this metric completely ignores note offset and note pitch. This means an estimated onset will be considered correct if it matches a reference onset, even if the onsets come from notes with completely different pitches (i.e. notes that would not match with :func:`match_notes`). Examples -------- >>> ref_intervals, _ = mir_eval.io.load_valued_intervals( ...     'reference.txt') >>> est_intervals, _ = mir_eval.io.load_valued_intervals( ...     'estimated.txt') >>> (onset_precision, ...  onset_recall, ...  onset_f_measure) = mir_eval.transcription.onset_precision_recall_f1( ...      ref_intervals, est_intervals) Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) onset_tolerance : float > 0 The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds. Default is 0.05 (50 ms). strict : bool If ``strict=False`` (the default), threshold checks for onset matching are performed using ``<=`` (less than or equal). If ``strict=True``, the threshold checks are performed using ``<`` (less than). beta : float > 0 Weighting factor for f-measure (default value = 1.0). Returns ------- precision : float The computed precision score recall : float The computed recall score f_measure : float The computed F-measure score

### Goal
Compute the precision, recall, and F-measure scores for note onsets by matching estimated onsets to reference onsets within a time tolerance, completely ignoring note offsets and pitches.

### Parameters
- `ref_intervals`: `np.ndarray`, shape=(n,2). Array of reference notes time intervals (onset and offset times in seconds).
- `est_intervals`: `np.ndarray`, shape=(m,2). Array of estimated notes time intervals (onset and offset times in seconds).
- `onset_tolerance`, default `0.05`: `float > 0`. The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds. Default is 50 ms.
- `strict`, default `False`: `bool`. If `False`, threshold checks for onset matching use `<=` (less than or equal). If `True`, checks use `<` (less than).
- `beta`, default `1.0`: `float > 0`. Weighting factor for the F-measure calculation.

### Input
The caller must provide two 2-dimensional numpy arrays of shape `(n, 2)` and `(m, 2)` representing the reference and estimated time intervals. The first column of each array represents the onset times, and the second column represents the offset times. Even though this specific metric ignores offsets, the arrays must still be `(n, 2)` in shape. Empty arrays (shape `(0, 2)`) are permitted and will deterministically return `(0, 0, 0)`.

### Output
Returns `unspecified` — A tuple of three `float` values: `(precision, recall, f_measure)`. These represent the computed precision score, recall score, and F-measure score, respectively.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Standard evaluation using sliced interval arrays
ref_int = np.array([[0.5, 1.0], [1.5, 2.0]])
est_int = np.array([[0.52, 0.9], [1.6, 2.1]])

precision, recall, f_measure = mir_eval.transcription.onset_precision_recall_f1(
    ref_int, est_int
)

# 2. Handling empty estimations or references
ref_empty = np.empty(shape=(0, 2))
est_intervals = np.array([[0.0, 1.0]])

precision, recall, f1 = mir_eval.transcription.onset_precision_recall_f1(
    ref_empty, est_intervals
)
assert (precision, recall, f1) == (0, 0, 0)
```

### LLM Instruction Prompt
- When evaluating transcription or onset detection where pitch and offset are irrelevant, use `mir_eval.transcription.onset_precision_recall_f1`.
- Always pass 2D numpy arrays of shape `(n, 2)` for both `ref_intervals` and `est_intervals`. If your data includes pitches or velocities (e.g., shape `(n, 3)` or `(n, 4)`), slice the array to include only the first two columns (e.g., `data[:, :2]`) before passing it to this function.
- Do not invent a `mir_eval.onset.onset_precision_recall_f1` function; this metric lives in the `mir_eval.transcription` submodule.

### Prompt Snippet
```text
mir_eval.transcription.onset_precision_recall_f1(ref_intervals, est_intervals, onset_tolerance=0.05, strict=False, beta=1.0)
Computes Precision, Recall, and F-measure of note onsets. An estimated onset is correct if within +-50ms (default) of a reference onset. Ignores note offset and pitch. Inputs must be np.ndarrays of shape (n, 2) and (m, 2). Returns a tuple of floats: (precision, recall, f_measure).
```

### Common Failure Modes
- Passing 1D arrays of just onset times instead of 2D `(n, 2)` interval arrays. The function expects intervals, even though it only evaluates the first column (onsets).
- Passing arrays with more than 2 columns (e.g., intervals with appended pitch or velocity data).
- Calling the function from the wrong submodule (e.g., attempting `mir_eval.onset.onset_precision_recall_f1` instead of `mir_eval.transcription.onset_precision_recall_f1`).

### Fix Code Hint
```python
# If your data contains pitches (shape n, 3), slice it to (n, 2) first:
ref_intervals = REF_DATA[:, :2]
est_intervals = EST_DATA[:, :2]

precision, recall, f_measure = mir_eval.transcription.onset_precision_recall_f1(
    ref_intervals, est_intervals
)
```

## API Test: `overall_accuracy`

### Signature
```python
def overall_accuracy(ref_voicing, ref_cent, est_voicing, est_cent, cent_tolerance=50)
```
_Source: source/mir_eval/melody.py:691_

_Source doc:_ Compute the overall accuracy given two pitch (frequency) sequences in cents and matching voicing indicator sequences. The first pitch and voicing arrays are treated as the reference (truth), and the second two as the estimate (prediction).  All 4 sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> overall_accuracy = mir_eval.melody.overall_accuracy(ref_v, ref_c, ...                                                     est_v, est_c) Parameters ---------- ref_voicing : np.ndarray Reference voicing array. When this array is non-binary, it is treated as a 'reference reward', as in (Bittner & Bosch, 2019) ref_cent : np.ndarray Reference pitch sequence in cents est_voicing : np.ndarray Estimated voicing array est_cent : np.ndarray Estimate pitch sequence in cents cent_tolerance : float Maximum absolute deviation in cents for a frequency value to be considered correct (Default value = 50) Returns ------- overall_accuracy : float Overall accuracy, the total fraction of correctly estimates frames, where provides a correct frequency values (within cent_tolerance).

### Goal
Compute the overall accuracy of an estimated melody pitch sequence against a reference, defined as the total fraction of correctly estimated frames where the estimate provides a correct frequency value within a specified cent tolerance.

### Parameters
- `ref_voicing`: A 1D `np.ndarray` representing the reference voicing indicator sequence. If this array is non-binary, it is treated as a 'reference reward'.
- `ref_cent`: A 1D `np.ndarray` representing the reference pitch sequence, converted to cents.
- `est_voicing`: A 1D `np.ndarray` representing the estimated voicing indicator sequence.
- `est_cent`: A 1D `np.ndarray` representing the estimated pitch sequence, converted to cents.
- `cent_tolerance`, default `50`: A `float` representing the maximum absolute deviation in cents for a frequency value to be considered correct.

### Input
Four 1D numpy arrays (`ref_voicing`, `ref_cent`, `est_voicing`, `est_cent`) that must all be of the exact same length. The pitch arrays must be provided in cents, not Hertz. Callers typically use `mir_eval.melody.to_cent_voicing` to align raw time-series data onto a common time grid and convert frequencies to cents before calling this metric.

### Output
Returns `unspecified` — A `float` representing the overall accuracy score (the fraction of frames where the estimated pitch and voicing correctly match the reference within the `cent_tolerance`).

### Valid Call Patterns
```python
import mir_eval

# Example inferred from the source documentation
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')

# Precondition: Align times and convert frequencies to cents and voicing arrays
(ref_v, ref_c, est_v, est_c) = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

# Compute the metric
accuracy = mir_eval.melody.overall_accuracy(ref_v, ref_c, est_v, est_c)
```

### LLM Instruction Prompt
- When generating calls to `mir_eval.melody.overall_accuracy`, ensure that all four input arrays are of the exact same length and that pitch values are in cents. Do not pass raw time-frequency arrays (in seconds and Hz) directly to this function; route them through `mir_eval.melody.to_cent_voicing` first to satisfy the preconditions.

### Prompt Snippet
```text
Compute the overall melody accuracy for the estimated pitch sequence against the reference. Ensure you convert the raw time and frequency arrays into aligned cent and voicing arrays before computing the metric.
```

### Common Failure Modes
- `ValueError` due to mismatched array lengths between the reference and estimate sequences.
- Incorrect or near-zero accuracy scores caused by passing raw frequencies (Hz) instead of cents.
- Passing raw time arrays as arguments instead of the expected voicing indicator arrays.

### Fix Code Hint
```python
# INCORRECT: Passing raw time and frequency (Hz) arrays of potentially different lengths
# accuracy = mir_eval.melody.overall_accuracy(ref_time, ref_freq, est_time, est_freq)

# CORRECT: Convert to aligned cent and voicing arrays first
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)
accuracy = mir_eval.melody.overall_accuracy(ref_v, ref_c, est_v, est_c)
```

## API Test: `overseg`

### Signature
```python
def overseg(reference_intervals, estimated_intervals)
```
_Source: source/mir_eval/chord.py:1409_

_Source doc:_ Compute the MIREX 'OverSeg' score. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> score = mir_eval.chord.overseg(ref_intervals, est_intervals) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2), dtype=float Reference chord intervals to score against. estimated_intervals : np.ndarray, shape=(m, 2), dtype=float Estimated chord intervals to score against. Returns ------- oversegmentation score : float Comparison score, in [0.0, 1.0], where 1.0 means no oversegmentation.

### Goal
Compute the MIREX 'OverSeg' score to evaluate the oversegmentation of estimated chord intervals against reference chord intervals.

### Parameters
- `reference_intervals`: `np.ndarray, shape=(n, 2), dtype=float` representing the ground truth chord intervals to score against.
- `estimated_intervals`: `np.ndarray, shape=(m, 2), dtype=float` representing the predicted chord intervals to score against.

### Input
Two numpy arrays of shape `(n, 2)` and `(m, 2)` containing float values for the start and end times of the intervals. These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_labeled_intervals` and extracting the first element of the returned tuple.

### Output
Returns `unspecified` — A float comparison score in the range `[0.0, 1.0]`, where `1.0` indicates no oversegmentation.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example derived from the project's test suite
ref_ivs = np.array([[0.0, 2.0], [2.0, 2.5], [2.5, 3.2]])
est_ivs = np.array([[0.0, 3.0], [3.0, 3.5]])

score = mir_eval.chord.overseg(ref_ivs, est_ivs)
```

### LLM Instruction Prompt
- When evaluating chord oversegmentation, use `mir_eval.chord.overseg(reference_intervals, estimated_intervals)`. Ensure both inputs are `(n, 2)` float numpy arrays representing `[start_time, end_time]` intervals. Do not pass the chord labels to this function; it only requires the intervals.

### Prompt Snippet
```text
`mir_eval.chord.overseg(ref_ivs, est_ivs)` computes the MIREX OverSeg score (1.0 = no oversegmentation). Inputs must be `(n, 2)` float numpy arrays of intervals.
```

### Common Failure Modes
- Passing the full tuple `(intervals, labels)` returned by `mir_eval.io.load_labeled_intervals` instead of just the `intervals` array.
- Providing 1D arrays or arrays with shapes other than `(n, 2)`.
- Passing standard Python lists instead of `numpy.ndarray` objects with `dtype=float`.

### Fix Code Hint
```python
# Ensure inputs are strictly (n, 2) float numpy arrays
ref_intervals = np.asarray(ref_intervals, dtype=float).reshape(-1, 2)
est_intervals = np.asarray(est_intervals, dtype=float).reshape(-1, 2)
score = mir_eval.chord.overseg(ref_intervals, est_intervals)
```

## API Test: `p_score`

### Signature
```python
def p_score(reference_beats, estimated_beats, p_score_threshold=0.2)
```
_Source: source/mir_eval/beat.py:329_

_Source doc:_ Get McKinney's P-score. Based on the autocorrelation of the reference and estimated beats Examples -------- >>> reference_beats = mir_eval.io.load_events('reference.txt') >>> reference_beats = mir_eval.beat.trim_beats(reference_beats) >>> estimated_beats = mir_eval.io.load_events('estimated.txt') >>> estimated_beats = mir_eval.beat.trim_beats(estimated_beats) >>> p_score = mir_eval.beat.p_score(reference_beats, estimated_beats) Parameters ---------- reference_beats : np.ndarray reference beat times, in seconds estimated_beats : np.ndarray query beat times, in seconds p_score_threshold : float Window size will be ``p_score_threshold*np.median(inter_annotation_intervals)``, (Default value = 0.2) Returns ------- correlation : float McKinney's P-score

### Goal
Compute McKinney's P-score, an evaluation metric based on the autocorrelation of reference and estimated beat times.

### Parameters
- `reference_beats`: `np.ndarray` — Reference (ground truth) beat times, in seconds.
- `estimated_beats`: `np.ndarray` — Query (estimated) beat times, in seconds.
- `p_score_threshold`, default `0.2`: `float` — Multiplier used to determine the evaluation window size, which is calculated as `p_score_threshold * np.median(inter_annotation_intervals)`.

### Input
1D numpy arrays containing beat timestamps in seconds. Data is typically loaded from repository-format text files using `mir_eval.io.load_events`. It is a standard MIR evaluation precondition to crop out early beats (e.g., before 5 seconds) using `mir_eval.beat.trim_beats` prior to scoring.

### Output
Returns `unspecified` — A `float` representing McKinney's P-score (correlation).

### Valid Call Patterns
```python
import mir_eval

# Example derived from the source documentation
reference_beats = mir_eval.io.load_events('reference.txt')
reference_beats = mir_eval.beat.trim_beats(reference_beats)

estimated_beats = mir_eval.io.load_events('estimated.txt')
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)

p_score = mir_eval.beat.p_score(reference_beats, estimated_beats)
```

### LLM Instruction Prompt
- When evaluating beat tracking using McKinney's P-score, always load the reference and estimated beat text files using `mir_eval.io.load_events`, preprocess both arrays with `mir_eval.beat.trim_beats` to remove early events, and pass the resulting 1D numpy arrays to `mir_eval.beat.p_score`. Do not pass file paths directly to the metric function.

### Prompt Snippet
```text
Use mir_eval.beat.p_score(ref_beats, est_beats) to compute McKinney's P-score. Ensure inputs are 1D numpy arrays of timestamps in seconds, typically loaded via mir_eval.io.load_events and preprocessed with mir_eval.beat.trim_beats.
```

### Common Failure Modes
- Passing file paths (strings or `pathlib.Path`) directly to `p_score` instead of loading them into numpy arrays first.
- Forgetting to trim the first 5 seconds of beats using `mir_eval.beat.trim_beats`, which is a standard preprocessing step that prevents early, unstable beats from skewing the evaluation metric.
- Passing multi-dimensional arrays instead of 1D arrays of timestamps.

### Fix Code Hint
```python
# BAD: Passing file paths directly
# score = mir_eval.beat.p_score('ref.txt', 'est.txt')

# GOOD: Load events and trim early beats before scoring
ref_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('ref.txt'))
est_beats = mir_eval.beat.trim_beats(mir_eval.io.load_events('est.txt'))
score = mir_eval.beat.p_score(ref_beats, est_beats)
```

## API Test: `pairwise`

### Signature
```python
def pairwise(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1, beta=1.0)
```
_Source: source/mir_eval/segment.py:310_

_Source doc:_ Frame-clustering segmentation evaluation by pair-wise agreement. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> # Trim or pad the estimate to match reference timing >>> (ref_intervals, ...  ref_labels) = mir_eval.util.adjust_intervals(ref_intervals, ...                                               ref_labels, ...                                               t_min=0) >>> (est_intervals, ...  est_labels) = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()) >>> precision, recall, f = mir_eval.structure.pairwise(ref_intervals, ...                                                    ref_labels, ...                                                    est_intervals, ...                                                    est_labels) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. reference_labels : list, shape=(n,) reference segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_labels : list, shape=(m,) estimated segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. frame_size : float > 0 length (in seconds) of frames for clustering (Default value = 0.1) beta : float > 0 beta value for F-measure (Default value = 1.0) Returns ------- precision : float > 0 Precision of detecting whether frames belong in the same cluster recall : float > 0 Recall of detecting whether frames belong in the same cluster f : float > 0 F-measure of detecting whether frames belong in the same cluster

### Goal
Computes a frame-clustering segmentation evaluation by pair-wise agreement, measuring how accurately the estimated segments group frames into the same clusters as the reference segments.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)`. The reference segment start and end times (in seconds), typically loaded via `mir_eval.io.load_labeled_intervals`.
- `reference_labels`: `list` of length `n`. The reference segment labels corresponding to `reference_intervals`.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)`. The estimated segment start and end times (in seconds).
- `estimated_labels`: `list` of length `m`. The estimated segment labels corresponding to `estimated_intervals`.
- `frame_size`, default `0.1`: `float > 0`. The length (in seconds) of the frames used for clustering.
- `beta`, default `1.0`: `float > 0`. The beta weight value used when calculating the F-measure.

### Input
Callers must provide in-memory numpy arrays for intervals and lists for labels, typically parsed from repository-format text files using `mir_eval.io.load_labeled_intervals`. 
**Precondition:** The estimated intervals must be trimmed or padded to exactly match the reference timing span (e.g., using `mir_eval.util.adjust_intervals`) before calling `pairwise`.

### Output
Returns `tuple[float, float, float]` — A tuple containing `(precision, recall, f)`, where all values are floats > 0 representing the precision, recall, and F-measure of detecting whether frames belong in the same cluster.

### Valid Call Patterns
```python
import mir_eval

# Example derived from the source docstring
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# Precondition: Trim or pad the estimate to match reference timing
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)

# Compute pair-wise agreement metrics
precision, recall, f = mir_eval.segment.pairwise(
    ref_intervals, 
    ref_labels, 
    est_intervals, 
    est_labels,
    frame_size=0.1,
    beta=1.0
)
```

### LLM Instruction Prompt
- When evaluating segmentation with `pairwise`, you MUST preprocess the estimated intervals to match the reference intervals' time span using `mir_eval.util.adjust_intervals`.
- Do not pass raw file paths to `pairwise`; load them first using `mir_eval.io.load_labeled_intervals`.
- Ensure `reference_intervals` and `estimated_intervals` are 2D numpy arrays of shape `(n, 2)` and `(m, 2)`.

### Prompt Snippet
```text
Load the reference and estimated labeled intervals from 'ref.txt' and 'est.txt'. Adjust the estimated intervals so their time span matches the reference intervals (starting at 0 and ending at the reference's max time). Then, compute the pair-wise agreement metrics using `mir_eval.segment.pairwise`.
```

### Common Failure Modes
- **Timing Mismatch:** Failing to align the start and end times of the estimated intervals with the reference intervals, which causes frame-clustering logic to compare mismatched time spans or throw out-of-bounds errors.
- **Incorrect Data Types:** Passing file paths (strings) instead of the loaded `np.ndarray` and `list` objects.
- **Shape Errors:** Passing 1D arrays for intervals instead of the required `(n, 2)` shape.

### Fix Code Hint
```python
# FIX: Ensure estimated intervals are adjusted to the reference boundaries before calling pairwise
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(ref_intervals, ref_labels, t_min=0)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)
precision, recall, f = mir_eval.segment.pairwise(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

## API Test: `percentage_correct`

### Signature
```python
def percentage_correct(reference_timestamps, estimated_timestamps, window=0.3)
```
_Source: source/mir_eval/alignment.py:144_

_Source doc:_ Compute the percentage of correctly predicted timestamps. A timestamp is predicted correctly if its position doesn't deviate more than the window parameter from the ground truth timestamp. Examples -------- >>> reference_timestamps = mir_eval.io.load_events('reference.txt') >>> estimated_timestamps = mir_eval.io.load_events('estimated.txt') >>> pc = mir_eval.align.percentage_correct(reference_onsets, estimated_timestamps, window=0.2) Parameters ---------- reference_timestamps : np.ndarray reference timestamps, in seconds estimated_timestamps : np.ndarray estimated timestamps, in seconds window : float Window size, in seconds (Default value = .3) Returns ------- pc : float Percentage of correct timestamps

### Goal
Compute the percentage of correctly predicted timestamps by checking if each estimated event falls within a specified time tolerance window of a ground truth reference event.

### Parameters
- `reference_timestamps`: `np.ndarray` of ground truth reference timestamps, measured in seconds.
- `estimated_timestamps`: `np.ndarray` of estimated timestamps to be evaluated, measured in seconds.
- `window`, default `0.3`: A `float` representing the tolerance window size in seconds. An estimated timestamp is considered correct if its absolute deviation from the reference is less than or equal to this value.

### Input
Both `reference_timestamps` and `estimated_timestamps` must be 1-dimensional numpy arrays of time events in seconds. These are typically loaded from repository-format text files using `mir_eval.io.load_events()`. 

### Output
Returns `unspecified` — A `float` representing the percentage of correctly predicted timestamps.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Inferred from signature and source docstring
reference_timestamps = np.array([1.0, 2.0, 3.0, 4.0])
estimated_timestamps = np.array([1.05, 2.1, 3.4, 4.01])

# Compute percentage of correct timestamps with a 0.2 second tolerance window
pc = mir_eval.alignment.percentage_correct(
    reference_timestamps, 
    estimated_timestamps, 
    window=0.2
)
```

### LLM Instruction Prompt
- Pass 1D numpy arrays of timestamps (in seconds) for both reference and estimated inputs.
- Use `mir_eval.io.load_events()` to load timestamps from text files before passing them to this function.
- Note the module path: use `mir_eval.alignment.percentage_correct` (the official docstring contains a typo referencing `mir_eval.align`, but the correct task submodule is `mir_eval.alignment`).
- Adjust the `window` parameter (default 0.3s) if a different tolerance is required by the specific MIR evaluation task.

### Prompt Snippet
```text
When evaluating timestamp predictions (like alignments), use `mir_eval.alignment.percentage_correct(reference_timestamps, estimated_timestamps, window=0.3)`. Both inputs must be 1D numpy arrays of timestamps in seconds.
```

### Common Failure Modes
- **Module Name Typo:** Attempting to call `mir_eval.align.percentage_correct(...)` as shown in the source docstring example. The correct submodule name is `mir_eval.alignment`.
- **Passing Intervals Instead of Events:** Passing 2D arrays of intervals (e.g., `[[start, end], ...]`) instead of 1D arrays of timestamps. If you have intervals, you must extract the relevant boundaries first.
- **Type Errors:** Passing raw Python lists instead of `np.ndarray`. While numpy operations sometimes implicitly cast lists, strict scientific Python APIs expect numpy arrays.

### Fix Code Hint
```python
import mir_eval

# 1. Load 1D event arrays from text files
ref_events = mir_eval.io.load_events('reference.txt')
est_events = mir_eval.io.load_events('estimated.txt')

# 2. Call the function using the correct submodule name (alignment, not align)
score = mir_eval.alignment.percentage_correct(
    ref_events, 
    est_events, 
    window=0.2
)
```

## API Test: `percentage_correct_segments`

### Signature
```python
def percentage_correct_segments(reference_timestamps, estimated_timestamps, duration: Optional[float]=None)
```
_Source: source/mir_eval/alignment.py:175_

### Goal
Calculate the percentage of correct segments (PCS) metric by constructing segments from timestamp vectors and computing their overlap relative to the total duration.

### Parameters
- `reference_timestamps`: A numpy array of reference (ground truth) timestamps, in seconds.
- `estimated_timestamps`: A numpy array of estimated (predicted) timestamps, in seconds.
- `duration` (`Optional[float]`), default `None`: The total duration of the audio in seconds. WARNING: Providing this parameter fundamentally changes how the metric is computed and which segment boundaries are created.

### Input
`reference_timestamps` and `estimated_timestamps` must be numpy arrays of timestamps in seconds. These are typically loaded from repository-format text files using `mir_eval.io.load_events()`. If `duration` is provided, it must be a float representing the total audio duration. 

### Output
Returns `unspecified` — A float representing the percentage of time where the ground truth and predicted segments overlap.

### Valid Call Patterns
```python
# Inferred from the source docstring, adapting the submodule name to match the context's `mir_eval.alignment`
import mir_eval

reference_timestamps = mir_eval.io.load_events('reference.txt')
estimated_timestamps = mir_eval.io.load_events('estimated.txt')

# Default behavior (MIREX 2020 variant)
pcs_mirex = mir_eval.alignment.percentage_correct_segments(
    reference_timestamps, 
    estimated_timestamps
)

# Strict boundary behavior (Fujihara 2011 variant)
pcs_strict = mir_eval.alignment.percentage_correct_segments(
    reference_timestamps, 
    estimated_timestamps, 
    duration=180.5
)
```

### LLM Instruction Prompt
- When calling `percentage_correct_segments`, you MUST decide whether to pass the `duration` parameter based on the desired evaluation strictness.
- If `duration` is `None` (default), the computation follows the MIREX lyrics alignment challenge 2020. Segments are created strictly between the provided timestamps `(t1, t2), ... (tN-1, tN)`. This variant is invariant to how long the eventless beginning and end parts of the audio are.
- If `duration` is provided, the computation follows the original Fujihara 2011 paper. Segments are created from the start and end of the track: `(0, t1), (t1, t2), ... (tN, duration)`. This variant punishes cases where the first estimated timestamp is too early or the last is too late.
- Ensure inputs are numpy arrays of timestamps in seconds.

### Prompt Snippet
```text
Calculate the percentage of correct segments (PCS) for the alignment task. Use the strict Fujihara 2011 variant by passing the total audio duration to the metric function so that early/late boundary estimates are properly penalized.
```

### Common Failure Modes
- **Unexpected Metric Behavior**: Failing to explicitly choose the `duration` parameter strategy. Omitting it when strict boundary evaluation is desired will artificially inflate scores by ignoring the eventless beginning and end parts of the audio.
- **Submodule Naming**: Attempting to call `mir_eval.align.percentage_correct_segments` (as written in the legacy docstring) instead of the actual task submodule `mir_eval.alignment.percentage_correct_segments`.
- **Incorrect Input Types**: Passing raw lists instead of numpy arrays, or passing interval arrays `(start, end)` instead of 1D timestamp event arrays.

### Fix Code Hint
```python
# FIX: Ensure the correct submodule `alignment` is used and timestamps are loaded as 1D event arrays.
import mir_eval

# Load 1D timestamp arrays (not intervals)
ref_times = mir_eval.io.load_events('reference.txt')
est_times = mir_eval.io.load_events('estimated.txt')

# Pass duration to penalize boundary errors (Fujihara 2011 variant)
score = mir_eval.alignment.percentage_correct_segments(ref_times, est_times, duration=210.0)
```

## API Test: `piano_roll`

### Signature
```python
def piano_roll(intervals, pitches=None, midi=None, ax=None, **kwargs)
```
_Source: source/mir_eval/display.py:873_

_Source doc:_ Plot a quantized piano roll as intervals Parameters ---------- intervals : np.ndarray, shape=(n, 2) timing intervals for notes pitches : np.ndarray, shape=(n,), optional pitches of notes (in Hz). midi : np.ndarray, shape=(n,), optional pitches of notes (in MIDI numbers). At least one of ``pitches`` or ``midi`` must be provided. ax : matplotlib.pyplot.axes An axis handle on which to draw the intervals. If none is provided, a new set of axes is created. **kwargs Additional keyword arguments to :func:`labeled_intervals`. Returns ------- ax : matplotlib.pyplot.axes._subplots.AxesSubplot A handle to the (possibly constructed) plot axes

### Goal
Plot a quantized piano roll representation of musical notes as intervals on a matplotlib axis.

### Parameters
- `intervals`: `np.ndarray` of shape `(n, 2)` representing the timing intervals (start and end times) for notes.
- `pitches`, default `None`: `np.ndarray` of shape `(n,)` representing the optional pitches of notes in Hz.
- `midi`, default `None`: `np.ndarray` of shape `(n,)` representing the optional pitches of notes in MIDI numbers.
- `ax`, default `None`: `matplotlib.pyplot.axes` handle on which to draw the intervals. If none is provided, a new set of axes is created.
- `**kwargs`: Additional keyword arguments (such as `label`, `alpha`, or `facecolor`) passed through to the underlying `labeled_intervals` function.

### Input
The caller must provide an `(n, 2)` numpy array of time intervals and an `(n,)` numpy array of corresponding pitch values. **Precondition:** At least one of `pitches` (Hz) or `midi` (MIDI note numbers) MUST be provided. If generating plots in an automated test environment, the matplotlib backend must be configured to run headlessly without network or audio-device access.

### Output
Returns `matplotlib.pyplot.axes._subplots.AxesSubplot` — A handle to the matplotlib axes containing the constructed piano roll plot.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval

# Pattern 1: Plotting using Hz pitches
plt.figure()
mir_eval.display.piano_roll(ref_t, ref_p, label="Reference", alpha=0.5)
mir_eval.display.piano_roll(est_t, est_p, label="Estimate", alpha=0.5, facecolor="r")
plt.legend(loc="upper right")

# Pattern 2: Plotting using MIDI numbers
plt.figure()
ref_midi = mir_eval.util.hz_to_midi(ref_p)
est_midi = mir_eval.util.hz_to_midi(est_p)
mir_eval.display.piano_roll(ref_t, midi=ref_midi, label="Reference", alpha=0.5)
mir_eval.display.piano_roll(est_t, midi=est_midi, label="Estimate", alpha=0.5, facecolor="r")
plt.legend(loc="upper right")
```

### LLM Instruction Prompt
- Call `mir_eval.display.piano_roll` to visualize transcription or multipitch outputs.
- You MUST provide `intervals` and at least one of `pitches` (in Hz) or `midi` (in MIDI numbers). Do not leave both pitch arguments as `None`.
- Pass standard matplotlib styling arguments (like `alpha`, `facecolor`, `label`) via `**kwargs` to differentiate reference and estimated annotations on the same plot.
- Ensure any generated display tests are kept headless.

### Prompt Snippet
```text
When visualizing note events with `mir_eval.display.piano_roll(intervals, pitches=None, midi=None, ax=None, **kwargs)`, you must supply an `(n, 2)` array of intervals and an `(n,)` array for either `pitches` (Hz) or `midi` (MIDI numbers). At least one pitch representation is required. Use `**kwargs` for matplotlib styling (e.g., `alpha=0.5`, `facecolor="r"`).
```

### Common Failure Modes
- **Missing Pitch Data**: Calling the function with only `intervals` and leaving both `pitches` and `midi` as `None` will violate the precondition and fail.
- **Shape Mismatch**: Providing an `intervals` array that is not `(n, 2)` or a pitch/midi array that does not match the length `n` of the intervals.
- **GUI/Display Errors in CI**: Executing the plot function in a headless test environment without properly configuring matplotlib's non-interactive backend (e.g., `Agg`).

### Fix Code Hint
```python
# BAD: Missing pitch/midi data
# mir_eval.display.piano_roll(intervals)

# GOOD: Provide either pitches (Hz) or midi (MIDI numbers)
import matplotlib
matplotlib.use("Agg") # Ensure headless execution for tests
import matplotlib.pyplot as plt
import mir_eval

fig, ax = plt.subplots()
# Using pitches in Hz
mir_eval.display.piano_roll(intervals, pitches=hz_pitches, ax=ax, label="Reference", alpha=0.5)
# OR using MIDI numbers
mir_eval.display.piano_roll(intervals, midi=midi_pitches, ax=ax, label="Estimate", facecolor="r", alpha=0.5)
```

## API Test: `pitch`

### Signature
```python
def pitch(times, frequencies, midi=False, unvoiced=False, ax=None, prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:659_

_Source doc:_ Visualize pitch contours Parameters ---------- times : np.ndarray, shape=(n,) Sample times of frequencies frequencies : np.ndarray, shape=(n,) frequencies (in Hz) of the pitch contours. Voicing is indicated by sign (positive for voiced, non-positive for non-voiced). midi : bool If `True`, plot on a MIDI-numbered vertical axis. Otherwise, plot on a linear frequency axis. unvoiced : bool If `True`, unvoiced pitch contours are plotted and indicated by transparency. Otherwise, unvoiced pitch contours are omitted from the display. ax : matplotlib.pyplot.axes An axis handle on which to draw the pitch contours. If none is provided, a new set of axes is created. prop_cycle : cycle.Cycler An optional property cycle object to specify style properties. If not provided, the default property cycler will be retrieved from matplotlib. **kwargs Additional keyword arguments to `matplotlib.pyplot.plot`. Returns ------- ax : matplotlib.pyplot.axes._subplots.AxesSubplot A handle to the (possibly constructed) plot axes

### Goal
Visualize pitch contours (such as melody or fundamental frequency over time) on either a linear frequency (Hz) or MIDI-numbered vertical axis.

### Parameters
- `times`: `np.ndarray`, shape=(n,). Sample times corresponding to the frequencies.
- `frequencies`: `np.ndarray`, shape=(n,). Frequencies (in Hz) of the pitch contours. Voicing is indicated by sign (positive for voiced, non-positive or zero for non-voiced).
- `midi`, default `False`: `bool`. If `True`, plots the frequencies on a MIDI-numbered vertical axis. Otherwise, plots on a linear frequency axis.
- `unvoiced`, default `False`: `bool`. If `True`, unvoiced pitch contours are plotted and indicated by transparency. Otherwise, unvoiced pitch contours are omitted from the display.
- `ax`, default `None`: `matplotlib.pyplot.axes`. An axis handle on which to draw the pitch contours. If none is provided, a new set of axes is created.
- `prop_cycle`, default `None`: `cycle.Cycler`. An optional property cycle object to specify style properties. If not provided, the default property cycler will be retrieved from matplotlib.
- `**kwargs`: Additional keyword arguments passed directly to `matplotlib.pyplot.plot` (e.g., `label="Reference"`, `color="blue"`).

### Input
The caller must provide 1D numpy arrays for `times` and `frequencies` of identical length `n`. `frequencies` must be provided in Hertz (Hz), even if `midi=True` is specified (the function handles the conversion internally). Voicing information must be encoded in the sign of the `frequencies` array: positive values are voiced, and non-positive values (<= 0) are unvoiced. If running in an automated test environment, the matplotlib backend must be configured to run headlessly.

### Output
Returns `matplotlib.pyplot.axes._subplots.AxesSubplot` — A handle to the matplotlib axes containing the constructed pitch contour plot.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval

# Example 1: Plotting reference and estimate on a Hz scale with unvoiced frames
plt.figure()
mir_eval.display.pitch(ref_times, ref_freqs, unvoiced=True, label="Reference")
mir_eval.display.pitch(est_times, est_freqs, unvoiced=True, label="Estimate")
plt.legend(loc="upper left")

# Example 2: Plotting on a MIDI scale with note tickers
plt.figure()
mir_eval.display.pitch(times, freqs, midi=True)
mir_eval.display.ticker_notes()
```

### LLM Instruction Prompt
- When visualizing melody or pitch contours using `mir_eval.display.pitch`, ensure the input `frequencies` array is in Hz, not MIDI pitch, even if `midi=True` is requested.
- Encode unvoiced frames as negative values or zeros in the `frequencies` array.
- Pass `unvoiced=True` if you want unvoiced frames to be visible (they will be rendered with transparency).
- Pass `**kwargs` like `label` to differentiate multiple contours on the same plot.
- Always configure matplotlib to use a headless backend (e.g., `Agg`) when generating plots in automated tests to prevent CI hangs.

### Prompt Snippet
```text
Plot the estimated and reference pitch contours on a MIDI axis using `mir_eval.display.pitch`. Include unvoiced frames and label the plots. Ensure the test runs headlessly.
```

### Common Failure Modes
- **Pre-converting to MIDI**: Passing frequencies that have already been converted to MIDI values when `midi=True`. The function expects Hz and will apply its own math, resulting in incorrect scaling.
- **Shape Mismatch**: Providing `times` and `frequencies` arrays of different lengths, which will cause `matplotlib.pyplot.plot` to raise a `ValueError`.
- **Blocking CI Environments**: Failing to set a headless backend (like `Agg`) before importing `pyplot` in test suites, causing the test to hang waiting for a display server.
- **Missing Voicing Information**: Passing `NaN` or omitting unvoiced frames entirely from the arrays instead of using non-positive values, which breaks the continuous time alignment expected by the plotting logic.

### Fix Code Hint
```python
import matplotlib
matplotlib.use('Agg')  # Ensure headless display for tests
import matplotlib.pyplot as plt
import mir_eval
import numpy as np

# Ensure arrays are 1D and match in length
times = np.asarray(times).flatten()
frequencies = np.asarray(frequencies).flatten()
assert len(times) == len(frequencies), "Times and frequencies must have the same length."

fig, ax = plt.subplots()
# Frequencies must be in Hz; midi=True handles the visual conversion
ax_handle = mir_eval.display.pitch(
    times, 
    frequencies, 
    midi=True, 
    unvoiced=True, 
    ax=ax, 
    label="Estimated Pitch"
)
mir_eval.display.ticker_notes() # Optional: add note names to the Y-axis
```

## API Test: `pitch_class_to_semitone`

### Signature
```python
def pitch_class_to_semitone(pitch_class)
```
_Source: source/mir_eval/chord.py:142_

_Source doc:_ Convert a pitch class to semitone. Parameters ---------- pitch_class : str Spelling of a given pitch class, e.g. 'C#', 'Gbb' Returns ------- semitone : int Semitone value of the pitch class.

### Goal
Converts a string representation of a musical pitch class into its corresponding integer semitone value.

### Parameters
- `pitch_class`: A string representing the spelling of a given pitch class (e.g., 'C#', 'Gbb').

### Input
A string containing a valid musical pitch class spelling. The input must represent a pitch class only and should not contain octave information (e.g., use 'C#', not 'C#4').

### Output
Returns `unspecified` — An integer representing the semitone value of the provided pitch class.

### Valid Call Patterns
```python
import mir_eval

pitch = 'C#'
semitone = mir_eval.chord.pitch_class_to_semitone(pitch)
```

### LLM Instruction Prompt
- Always pass a string representing a valid pitch class spelling (e.g., 'C#', 'Gbb') to `mir_eval.chord.pitch_class_to_semitone`.
- Do not include octave numbers in the string; this function expects pitch classes, not absolute pitches.
- Ensure the receiver is fully qualified as `mir_eval.chord.pitch_class_to_semitone`.

### Prompt Snippet
```text
# Convert a pitch class string to an integer semitone
semitone_val = mir_eval.chord.pitch_class_to_semitone('Gbb')
```

### Common Failure Modes
- Passing a pitch string that includes an octave number (e.g., 'C#4' instead of 'C#'), which will fail to parse as a valid pitch class.
- Passing an invalid, malformed, or unrecognized accidental spelling.
- Passing a non-string type (e.g., an integer or float) instead of the expected string spelling.

### Fix Code Hint
```python
# BAD: Includes octave information
# semitone = mir_eval.chord.pitch_class_to_semitone('C#4')

# GOOD: Pitch class only
semitone = mir_eval.chord.pitch_class_to_semitone('C#')
```

## API Test: `pitch_contour`

### Signature
```python
def pitch_contour(times, frequencies, fs, amplitudes=None, function=np.sin, length=None, kind='linear')
```
_Source: source/mir_eval/sonify.py:247_

_Source doc:_ Sonify a pitch contour. Parameters ---------- times : np.ndarray time indices for each frequency measurement, in seconds frequencies : np.ndarray frequency measurements, in Hz. Non-positive measurements or NaNs will be interpreted as un-voiced samples. fs : int desired sampling rate of the output signal amplitudes : np.ndarray amplitude measurements, nonnegative defaults to ``np.ones((length,))`` function : function function to use to synthesize notes, should be 2π-periodic length : int desired number of samples in the output signal, defaults to ``max(times)*fs`` kind : str Interpolation mode for the frequency and amplitude values. See: ``scipy.interpolate.interp1d`` for valid settings. Returns ------- output : np.ndarray synthesized version of the pitch contour

### Goal
Synthesize a pitch contour (time and frequency measurements) into an audio signal array for "evaluation by ear".

### Parameters
- `times`: `np.ndarray` of time indices for each frequency measurement, in seconds.
- `frequencies`: `np.ndarray` of frequency measurements, in Hz. Non-positive measurements or NaNs are natively interpreted as un-voiced (silent) samples.
- `fs`: `int` representing the desired sampling rate of the output audio signal.
- `amplitudes`, default `None`: `np.ndarray` of nonnegative amplitude measurements. If `None`, defaults to an array of ones (`np.ones((length,))`).
- `function`, default `np.sin`: A 2π-periodic function used to synthesize the notes.
- `length`, default `None`: `int` representing the desired number of samples in the output signal. If `None`, defaults to `max(times) * fs`.
- `kind`, default `'linear'`: `str` specifying the interpolation mode for the frequency and amplitude values. Accepts valid settings for `scipy.interpolate.interp1d`.

### Input
Callers must provide `times` and `frequencies` as parallel 1D `np.ndarray` objects. `frequencies` can safely contain `np.nan` or non-positive values (<= 0) to represent unvoiced regions; these do not need to be filtered out prior to calling. If `amplitudes` is provided, it must be a nonnegative `np.ndarray` matching the length of the inputs. `fs` and `length` (if provided) must be integers.

### Output
Returns `unspecified` — A 1D `np.ndarray` containing the synthesized audio signal of the pitch contour.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

fs = 8000
# Generate 5 seconds of time indices
times = np.linspace(0, 5, num=5 * fs, endpoint=True)

# Generate a 440 Hz tone with some unvoiced (negative) segments
freqs = np.full(len(times), 440.0)
freqs[1000:2000] *= -1  # Unvoiced segment

# 1. Basic sonification (infers duration)
audio_out = mir_eval.sonify.pitch_contour(times, freqs, fs)

# 2. Sonification with explicit length and amplitudes
amps = np.linspace(0, 1, num=5 * fs, endpoint=True)
audio_fade = mir_eval.sonify.pitch_contour(times, freqs, fs, length=fs * 7, amplitudes=amps)
```

### LLM Instruction Prompt
- Always pass `times` and `frequencies` as `np.ndarray` objects.
- Do not manually filter out `np.nan` or `<= 0` values from the `frequencies` array; `mir_eval.sonify.pitch_contour` natively handles these as unvoiced samples.
- If specifying `amplitudes`, ensure the array contains strictly nonnegative values.
- If specifying `length`, ensure it is cast to an integer (e.g., `int(duration * fs)`).

### Prompt Snippet
```text
Use `mir_eval.sonify.pitch_contour(times, frequencies, fs)` to synthesize the estimated pitch contour into an audio array. The `frequencies` array may contain NaNs or zeros for unvoiced frames; pass them directly without filtering. Ensure `fs` is an integer.
```

### Common Failure Modes
- Passing lists instead of `np.ndarray` for `times` or `frequencies`, which can cause internal numpy operations to fail.
- Providing negative values in the `amplitudes` array (amplitudes must be nonnegative).
- Passing a float for `length` or `fs`, which can cause indexing or array-initialization errors.
- Mismatched array lengths between `times`, `frequencies`, and `amplitudes`.

### Fix Code Hint
```python
# Ensure inputs are numpy arrays and length is an integer
times_arr = np.asarray(times)
freqs_arr = np.asarray(frequencies)
amps_arr = np.asarray(amplitudes) if amplitudes is not None else None

# Unvoiced frames (NaN or <= 0) are handled automatically
audio = mir_eval.sonify.pitch_contour(
    times_arr, 
    freqs_arr, 
    fs=44100, 
    amplitudes=amps_arr,
    length=int(max(times_arr) * 44100)
)
```

## API Test: `precision_recall_f1_overlap`

### Signature
```python
def precision_recall_f1_overlap(ref_intervals, ref_pitches, est_intervals, est_pitches, onset_tolerance=0.05, pitch_tolerance=50.0, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False, beta=1.0)
def precision_recall_f1_overlap(ref_intervals, ref_pitches, ref_velocities, est_intervals, est_pitches, est_velocities, onset_tolerance=0.05, pitch_tolerance=50.0, offset_ratio=0.2, offset_min_tolerance=0.05, strict=False, velocity_tolerance=0.1, beta=1.0)
```
_Source: source/mir_eval/transcription_velocity.py:230  (+1 more definition site/overload)_

_Source doc:_ Compute the Precision, Recall and F-measure of correct vs incorrectly transcribed notes, and the Average Overlap Ratio for correctly transcribed notes (see :func:`mir_eval.transcription.average_overlap_ratio`). "Correctness" is determined based on note onset, velocity, pitch and (optionally) offset. An estimated note is considered correct if 1. Its onset is within ``onset_tolerance`` (default +-50ms) of a reference note 2. Its pitch (F0) is within +/- ``pitch_tolerance`` (default one quarter tone, 50 cents) of the corresponding reference note 3. Its velocity, after normalizing reference velocities to the range [0, 1] and globally rescaling estimated velocities to minimize L2 distance between matched reference notes, is within ``velocity_tolerance`` (default 0.1) the corresponding reference note 4. If ``offset_ratio`` is ``None``, note offsets are ignored in the comparison. Otherwise, on top of the above requirements, a correct returned note is required to have an offset value within `offset_ratio`` (default 20%) of the reference note's duration around the reference note's offset, or within ``offset_min_tolerance`` (default 50 ms), whichever is larger. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) ref_pitches : np.ndarray, shape=(n,) Array of reference pitch values in Hertz ref_velocities : np.ndarray, shape=(n,) Array of MIDI velocities (i.e. between 0 and 127) of reference notes est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) est_pitches : np.ndarray, shape=(m,) Array of estimated pitch values in Hertz est_velocities : np.ndarray, shape=(n,) Array of MIDI velocities (i.e. between 0 and 127) of estimated notes onset_tolerance : float > 0 The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds. Default is 0.05 (50 ms). pitch_tolerance : float > 0 The tolerance for an estimated note's pitch deviating from the reference note's pitch, in cents. Default is 50.0 (50 cents). offset_ratio : float > 0 or None The ratio of the reference note's duration used to define the offset_tolerance. Default is 0.2 (20%), meaning the ``offset_tolerance`` will equal the ``ref_duration * 0.2``, or ``offset_min_tolerance`` (0.05 by default, i.e. 50 ms), whichever is greater. If ``offset_ratio`` is set to ``None``, offsets are ignored in the evaluation. offset_min_tolerance : float > 0 The minimum tolerance for offset matching. See ``offset_ratio`` description for an explanation of how the offset tolerance is determined. Note: this parameter only influences the results if ``offset_ratio`` is not ``None``. strict : bool If ``strict=False`` (the default), threshold checks for onset, offset, and pitch matching are performed using ``<=`` (less than or equal). If ``strict=True``, the threshold checks are performed using ``<`` (less than). velocity_tolerance : float > 0 Estimated notes are considered correct if, after rescaling and

### Goal
Compute the Precision, Recall, F-measure, and Average Overlap Ratio of estimated transcribed notes against reference notes based on onset, pitch, (optionally) offset, and (optionally) velocity matching.

### Parameters
- `ref_intervals`: `np.ndarray, shape=(n,2)` — Array of reference notes time intervals (onset and offset times in seconds).
- `ref_pitches`: `np.ndarray, shape=(n,)` — Array of reference pitch values in Hertz.
- `ref_velocities`: `np.ndarray, shape=(n,)` — Array of MIDI velocities (between 0 and 127) of reference notes. *(Only present in the `transcription_velocity` overload).*
- `est_intervals`: `np.ndarray, shape=(m,2)` — Array of estimated notes time intervals (onset and offset times in seconds).
- `est_pitches`: `np.ndarray, shape=(m,)` — Array of estimated pitch values in Hertz.
- `est_velocities`: `np.ndarray` — Array of MIDI velocities (between 0 and 127) of estimated notes. *(Only present in the `transcription_velocity` overload).*
- `onset_tolerance`, default `0.05`: `float > 0` — The tolerance for an estimated note's onset deviating from the reference note's onset, in seconds.
- `pitch_tolerance`, default `50.0`: `float > 0` — The tolerance for an estimated note's pitch deviating from the reference note's pitch, in cents.
- `offset_ratio`, default `0.2`: `float > 0` or `None` — The ratio of the reference note's duration used to define the offset tolerance. If `None`, offsets are ignored in the evaluation.
- `offset_min_tolerance`, default `0.05`: `float > 0` — The minimum tolerance for offset matching in seconds.
- `strict`, default `False`: `bool` — If `False`, threshold checks use `<=`. If `True`, threshold checks use `<`.
- `velocity_tolerance`, default `0.1`: `float > 0` — Tolerance for velocity matching after normalizing and rescaling. *(Only present in the `transcription_velocity` overload).*
- `beta`, default `1.0`: `float` — The beta parameter for the F-measure computation (weighting of precision vs. recall).

### Input
The caller must provide deterministic, in-memory numpy arrays for intervals and pitches (and velocities, if using the velocity-aware overload). 
- Intervals must be 2D arrays of shape `(n, 2)` representing `[onset, offset]` in seconds.
- Pitches must be 1D arrays of shape `(n,)` in Hertz.
- Empty arrays are explicitly supported (e.g., `np.empty(shape=(0, 2))` for intervals and `np.array([])` for pitches); the evaluation will safely return `0` for the metrics when there is no overlap or when inputs are empty.

### Output
Returns `unspecified` — A 4-tuple of floats representing `(precision, recall, f_measure, avg_overlap_ratio)`.

### Valid Call Patterns
```python
# Standard transcription evaluation (without velocities)
(
    precision,
    recall,
    f_measure,
    avg_overlap_ratio,
) = mir_eval.transcription.precision_recall_f1_overlap(
    ref_int, ref_pitch, est_int, est_pitch
)

# Transcription evaluation ignoring note offsets
(
    precision,
    recall,
    f_measure,
    avg_overlap_ratio,
) = mir_eval.transcription.precision_recall_f1_overlap(
    ref_int, ref_pitch, est_int, est_pitch, offset_ratio=None
)
```

### LLM Instruction Prompt
- When evaluating transcription accuracy, use `mir_eval.transcription.precision_recall_f1_overlap` for standard onset/offset/pitch matching, and `mir_eval.transcription_velocity.precision_recall_f1_overlap` if MIDI velocities are also being evaluated.
- Always unpack the return value into exactly four variables: `precision, recall, f_measure, avg_overlap_ratio`.
- To evaluate transcription without requiring note offsets to match, explicitly pass `offset_ratio=None`.
- Ensure inputs are numpy arrays; do not pass raw Python lists.

### Prompt Snippet
```text
Evaluate the estimated transcription against the reference transcription using `mir_eval`. The arrays `ref_intervals`, `ref_pitches`, `est_intervals`, and `est_pitches` are already loaded. Compute the precision, recall, F1-score, and average overlap ratio, ignoring note offsets.
```

### Common Failure Modes
- **Signature Mismatch:** Passing velocity arrays to `mir_eval.transcription.precision_recall_f1_overlap` instead of `mir_eval.transcription_velocity.precision_recall_f1_overlap`. The standard transcription module does not accept velocity arguments.
- **Unpacking Errors:** Failing to unpack the 4-tuple return value, leading to `ValueError: too many values to unpack` if expecting only 3 values (Precision, Recall, F1).
- **List Inputs:** Passing standard Python lists instead of `np.ndarray` objects, which can cause shape-attribute or array-operation failures internally.
- **Shape Mismatches:** Providing a 1D array for intervals instead of a 2D array of shape `(n, 2)`, or providing pitch arrays whose length does not match the number of intervals.

### Fix Code Hint
```python
# BAD: Expecting 3 return values or passing lists
p, r, f = mir_eval.transcription.precision_recall_f1_overlap(list_ref_int, list_ref_pitch, list_est_int, list_est_pitch)

# GOOD: Unpacking 4 values and ensuring numpy arrays
ref_int = np.array(list_ref_int)
ref_pitch = np.array(list_ref_pitch)
est_int = np.array(list_est_int)
est_pitch = np.array(list_est_pitch)

precision, recall, f_measure, avg_overlap = mir_eval.transcription.precision_recall_f1_overlap(
    ref_int, ref_pitch, est_int, est_pitch
)
```

## API Test: `quality_to_bitmap`

### Signature
```python
def quality_to_bitmap(quality)
```
_Source: source/mir_eval/chord.py:276_

_Source doc:_ Return the bitmap for a given quality. Parameters ---------- quality : str Chord quality name. Returns ------- bitmap : np.ndarray Bitmap representation of this quality (12-dim).

### Goal
Convert a string representing a musical chord quality (e.g., "maj") into a 12-dimensional binary numpy array (bitmap) indicating the active semitones relative to the chord's root.

### Parameters
- `quality`: A string representing the chord quality name (e.g., `"maj"`, `"min"`).

### Input
The caller must provide a string representing a valid chord quality. The string must exactly match one of the predefined valid qualities restricted by `mir_eval.chord.QUALITIES`. Do not pass full chord labels (e.g., `"C:maj"`), only the quality component.

### Output
Returns `unspecified` — A 12-dimensional `np.ndarray` bitmap representation of the chord quality, where `1` indicates an active semitone interval relative to the root and `0` indicates an inactive semitone.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Convert a major chord quality to its 12-dimensional bitmap
bitmap = mir_eval.chord.quality_to_bitmap("maj")

# The resulting bitmap for "maj" is:
# np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.quality_to_bitmap`, ensure the `quality` argument is a valid string present in `mir_eval.chord.QUALITIES`. Do not pass full chord labels (like `"C:maj"`), only the quality part (like `"maj"`). Expect a 12-element numpy array in return.

### Prompt Snippet
```text
mir_eval.chord.quality_to_bitmap(quality: str) -> np.ndarray
Converts a chord quality string (e.g., "maj") into a 12-dim binary numpy array.
```

### Common Failure Modes
- **Invalid Quality String:** Passing a quality string that is not in the predefined `mir_eval.chord.QUALITIES` list will raise an exception.
- **Passing Full Chord Labels:** Passing a complete chord string (e.g., `"C:maj"`) instead of just the quality (`"maj"`) will fail validation.

### Fix Code Hint
```python
# WRONG: Passing a full chord label
# bitmap = mir_eval.chord.quality_to_bitmap("C:maj")

# CORRECT: Extract or pass only the quality string
chord_label = "C:maj"
quality = chord_label.split(":")[1] if ":" in chord_label else "maj"
bitmap = mir_eval.chord.quality_to_bitmap(quality)
```

## API Test: `rand_index`

### Signature
```python
def rand_index(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1, beta=1.0)
```
_Source: source/mir_eval/segment.py:413_

### Goal
Computes the (non-adjusted) Rand index to evaluate the similarity between reference and estimated musical segmentations by clustering frames.

### Parameters
- `reference_intervals`: `np.ndarray, shape=(n, 2)` — Reference segment intervals, typically in the format returned by `mir_eval.io.load_labeled_intervals`.
- `reference_labels`: `list, shape=(n,)` — Reference segment labels corresponding to the reference intervals.
- `estimated_intervals`: `np.ndarray, shape=(m, 2)` — Estimated segment intervals, typically in the format returned by `mir_eval.io.load_labeled_intervals`.
- `estimated_labels`: `list, shape=(m,)` — Estimated segment labels corresponding to the estimated intervals.
- `frame_size`, default `0.1`: `float > 0` — Length (in seconds) of the frames used for clustering.
- `beta`, default `1.0`: `float > 0` — Beta value used for the F-measure calculation.

### Input
The caller must provide reference and estimated intervals as `(n, 2)` numpy arrays and their corresponding labels as lists. These are typically loaded from repository-format text files using `mir_eval.io.load_labeled_intervals`. 
**Precondition:** The estimated intervals must be adjusted to match the reference timing before evaluation. This is typically done using `mir_eval.util.adjust_intervals` to trim or pad the estimate so that its `t_min` and `t_max` align with the reference.

### Output
Returns `unspecified` — A `float > 0` representing the computed Rand index score.

### Valid Call Patterns
```python
import mir_eval

# Load reference and estimated intervals and labels
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Trim or pad the estimate to match reference timing
(ref_intervals, ref_labels) = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
(est_intervals, est_labels) = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)

# Compute the Rand index
rand_index_score = mir_eval.structure.rand_index(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

### LLM Instruction Prompt
- When evaluating segment or structure outputs using `rand_index`, you MUST first load the data using `mir_eval.io.load_labeled_intervals`. 
- You MUST preprocess the intervals using `mir_eval.util.adjust_intervals` to ensure the estimated intervals match the reference timing (e.g., setting `t_min=0` and `t_max=ref_intervals.max()`) before passing them to `mir_eval.structure.rand_index`.
- Do not pass raw file paths directly to the metric function.

### Prompt Snippet
```text
Load the reference and estimated labeled intervals from 'ref.lab' and 'est.lab'. Adjust the intervals so the estimate matches the reference timing (starting at 0 and ending at the reference's max time). Then, compute the Rand index using `mir_eval.structure.rand_index`.
```

### Common Failure Modes
- **Unadjusted Timing:** Failing to call `mir_eval.util.adjust_intervals` on the estimated intervals, leading to mismatched durations between the reference and estimate during frame clustering.
- **Passing File Paths:** Passing string file paths directly to `rand_index` instead of the parsed `np.ndarray` and `list` objects returned by `mir_eval.io.load_labeled_intervals`.
- **Invalid Hyperparameters:** Providing a `frame_size` or `beta` that is less than or equal to 0.

### Fix Code Hint
```python
# INCORRECT: Passing unadjusted intervals or raw file paths
# score = mir_eval.structure.rand_index('ref.lab', 'est.lab')

# CORRECT: Load and adjust intervals first
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

ref_intervals, ref_labels = mir_eval.util.adjust_intervals(ref_intervals, ref_labels, t_min=0)
est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, t_min=0, t_max=ref_intervals.max())

score = mir_eval.structure.rand_index(ref_intervals, ref_labels, est_intervals, est_labels)
```

## API Test: `raw_chroma_accuracy`

### Signature
```python
def raw_chroma_accuracy(ref_voicing, ref_cent, est_voicing, est_cent, cent_tolerance=50)
```
_Source: source/mir_eval/melody.py:622_

_Source doc:_ Compute the raw chroma accuracy given two pitch (frequency) sequences in cents and matching voicing indicator sequences. The first pitch and voicing arrays are treated as the reference (truth), and the second two as the estimate (prediction).  All 4 sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> raw_chroma = mir_eval.melody.raw_chroma_accuracy(ref_v, ref_c, ...                                                  est_v, est_c) Parameters ---------- ref_voicing : np.ndarray Reference voicing array. When this array is non-binary, it is treated as a 'reference reward', as in (Bittner & Bosch, 2019) ref_cent : np.ndarray Reference pitch sequence in cents est_voicing : np.ndarray Estimated voicing array est_cent : np.ndarray Estimate pitch sequence in cents cent_tolerance : float Maximum absolute deviation in cents for a frequency value to be considered correct (Default value = 50) Returns ------- raw_chroma : float Raw chroma accuracy, the fraction of voiced frames in ref_cent for which est_cent provides a correct frequency values (within cent_tolerance cents), ignoring octave errors

### Goal
Compute the raw chroma accuracy between reference and estimated pitch sequences, measuring the fraction of correctly estimated voiced frames while ignoring octave errors.

### Parameters
- `ref_voicing`: `np.ndarray` — Reference voicing indicator array. If this array is non-binary, it is treated as a 'reference reward'.
- `ref_cent`: `np.ndarray` — Reference pitch sequence, measured in cents.
- `est_voicing`: `np.ndarray` — Estimated voicing indicator array.
- `est_cent`: `np.ndarray` — Estimated pitch sequence, measured in cents.
- `cent_tolerance`, default `50`: `float` — Maximum absolute deviation in cents for an estimated frequency value to be considered correct.

### Input
Four NumPy arrays (`ref_voicing`, `ref_cent`, `est_voicing`, `est_cent`) that must all be of the exact same length. The pitch arrays must be provided in cents, not Hertz. Typically, these arrays are generated by loading time-series data (e.g., via `mir_eval.io.load_time_series`) and preprocessing them with `mir_eval.melody.to_cent_voicing` to ensure they are aligned to the same time grid and converted to cents.

### Output
Returns `unspecified` — A `float` representing the raw chroma accuracy score. This is the fraction of voiced frames in the reference sequence for which the estimated sequence provides a correct frequency value (within `cent_tolerance` cents), ignoring octave errors.

### Valid Call Patterns
```python
# Example inferred from the source documentation
import mir_eval

# Assuming ref_time, ref_freq, est_time, est_freq are already loaded via mir_eval.io.load_time_series
(ref_v, ref_c, est_v, est_c) = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

raw_chroma = mir_eval.melody.raw_chroma_accuracy(
    ref_voicing=ref_v, 
    ref_cent=ref_c, 
    est_voicing=est_v, 
    est_cent=est_c, 
    cent_tolerance=50
)
```

### LLM Instruction Prompt
- When calling `mir_eval.melody.raw_chroma_accuracy`, you MUST ensure all four input arrays (`ref_voicing`, `ref_cent`, `est_voicing`, `est_cent`) are exactly the same length.
- Do not pass raw frequency values in Hertz. You MUST convert frequencies to cents and align the time grids first, typically by using `mir_eval.melody.to_cent_voicing(ref_time, ref_freq, est_time, est_freq)`.

### Prompt Snippet
```text
Use `mir_eval.melody.raw_chroma_accuracy` to evaluate the melody extraction. Remember to convert your Hz frequencies to cents and align the reference and estimate arrays to the same length using `mir_eval.melody.to_cent_voicing` before passing them to the metric.
```

### Common Failure Modes
- **Mismatched Array Lengths**: Passing reference and estimate arrays of different lengths will cause a failure. They must be aligned to the same time grid.
- **Passing Frequencies in Hertz**: Passing raw Hz values instead of cents will result in wildly incorrect accuracy scores, as the `cent_tolerance` (default 50) expects a logarithmic cent scale.
- **Missing Voicing Arrays**: Attempting to pass only the pitch arrays without the corresponding voicing indicator arrays.

### Fix Code Hint
```python
# WRONG: Passing unaligned Hz frequencies directly
# raw_chroma = mir_eval.melody.raw_chroma_accuracy(ref_voicing, ref_freq_hz, est_voicing, est_freq_hz)

# CORRECT: Align and convert to cents first
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq_hz, est_time, est_freq_hz
)
raw_chroma = mir_eval.melody.raw_chroma_accuracy(ref_v, ref_c, est_v, est_c)
```

## API Test: `raw_pitch_accuracy`

### Signature
```python
def raw_pitch_accuracy(ref_voicing, ref_cent, est_voicing, est_cent, cent_tolerance=50)
```
_Source: source/mir_eval/melody.py:554_

_Source doc:_ Compute the raw pitch accuracy given two pitch (frequency) sequences in cents and matching voicing indicator sequences. The first pitch and voicing arrays are treated as the reference (truth), and the second two as the estimate (prediction).  All 4 sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> raw_pitch = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c, ...                                                est_v, est_c) Parameters ---------- ref_voicing : np.ndarray Reference voicing array. When this array is non-binary, it is treated as a 'reference reward', as in (Bittner & Bosch, 2019) ref_cent : np.ndarray Reference pitch sequence in cents est_voicing : np.ndarray Estimated voicing array est_cent : np.ndarray Estimate pitch sequence in cents cent_tolerance : float Maximum absolute deviation in cents for a frequency value to be considered correct (Default value = 50) Returns ------- raw_pitch : float Raw pitch accuracy, the fraction of voiced frames in ref_cent for which est_cent provides a correct frequency values (within cent_tolerance cents).

### Goal
Compute the raw pitch accuracy metric, which measures the fraction of voiced frames in a reference melody where the estimated pitch is within a specified tolerance (in cents) of the ground truth.

### Parameters
- `ref_voicing`: Reference voicing array (`np.ndarray`). When this array is non-binary, it is treated as a 'reference reward'.
- `ref_cent`: Reference pitch sequence in cents (`np.ndarray`).
- `est_voicing`: Estimated voicing array (`np.ndarray`).
- `est_cent`: Estimated pitch sequence in cents (`np.ndarray`).
- `cent_tolerance`, default `50`: Maximum absolute deviation in cents for a frequency value to be considered correct (`float`).

### Input
Four `np.ndarray` sequences (`ref_voicing`, `ref_cent`, `est_voicing`, `est_cent`) that **must all be of the exact same length**. The pitch arrays must be provided in cents, not Hertz. Typically, these aligned arrays are generated from raw time-frequency series using `mir_eval.melody.to_cent_voicing`.

### Output
Returns `unspecified` — A `float` representing the raw pitch accuracy score (the fraction of voiced frames in `ref_cent` for which `est_cent` provides a correct frequency value within `cent_tolerance` cents).

### Valid Call Patterns
```python
import mir_eval

# Example inferred from source documentation
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')

# Precondition: Align times and convert Hz to cents and voicing arrays
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

# Compute the metric
raw_pitch = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c, est_v, est_c)
```

### LLM Instruction Prompt
- When calling `mir_eval.melody.raw_pitch_accuracy`, you MUST ensure all four input arrays (`ref_voicing`, `ref_cent`, `est_voicing`, `est_cent`) are exactly the same length. Do not pass raw Hz frequencies or unaligned time series; pitches must be converted to cents and aligned to a common time grid first, typically by passing the raw time/frequency arrays through `mir_eval.melody.to_cent_voicing`.

### Prompt Snippet
```text
mir_eval.melody.raw_pitch_accuracy(ref_voicing, ref_cent, est_voicing, est_cent, cent_tolerance=50)
Computes raw pitch accuracy. Inputs MUST be same-length numpy arrays. Pitches MUST be in cents, not Hz. Use mir_eval.melody.to_cent_voicing to prepare inputs from raw time/frequency series.
```

### Common Failure Modes
- **Mismatched array lengths**: Passing reference and estimation arrays that have not been resampled/aligned to the same time grid. All four arrays must be identical in length.
- **Passing Hz instead of cents**: Passing raw frequency values directly from `load_time_series` without converting them to cents, resulting in wildly inaccurate accuracy scores.
- **Missing voicing arrays**: Attempting to pass only the pitch arrays. The function strictly requires the voicing indicator arrays as the first and third arguments.

### Fix Code Hint
```python
# WRONG: Passing raw time/frequency arrays directly or mismatched lengths
# raw_pitch = mir_eval.melody.raw_pitch_accuracy(ref_freq, est_freq)

# CORRECT: Use to_cent_voicing to align lengths and convert Hz to cents
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)
raw_pitch = mir_eval.melody.raw_pitch_accuracy(ref_v, ref_c, est_v, est_c)
```

## API Test: `reduce_extended_quality`

### Signature
```python
def reduce_extended_quality(quality)
```
_Source: source/mir_eval/chord.py:319_

_Source doc:_ Map an extended chord quality to a simpler one, moving upper voices to a set of scale degree extensions. Parameters ---------- quality : str Extended chord quality to reduce. Returns ------- base_quality : str New chord quality. extensions : set Scale degrees extensions for the quality.

### Goal
Map an extended chord quality string to a simpler base quality, extracting the upper voices into a set of scale degree extensions for standardized chord evaluation.

### Parameters
- `quality`: A string representing the extended chord quality to reduce (e.g., "maj9", "min11").

### Input
A string representing a valid extended chord quality. The input must be the quality portion of the chord only (not including the root note). The quality string must conform to `mir_eval`'s chord regular expressions and be valid within the restricted `chord.QUALITIES` definitions.

### Output
Returns `unspecified` — A two-element tuple `(base_quality, extensions)` where `base_quality` is a `str` representing the simplified chord quality, and `extensions` is a `set` of strings representing the scale degree extensions extracted from the original quality.

### Valid Call Patterns
```python
# Note: Call form inferred from signature and project context (not verified by test suite)
import mir_eval

quality_str = "maj9"
base_quality, extensions = mir_eval.chord.reduce_extended_quality(quality_str)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.reduce_extended_quality`, pass a single string representing the chord quality (without the root note).
- Expect a tuple of `(str, set)` in return, representing the base quality and the set of scale degree extensions.
- Ensure the input string is a valid chord quality recognized by `mir_eval`'s chord validation regex.

### Prompt Snippet
```text
# Reduce an extended chord quality to its base and extensions
base_quality, extensions = mir_eval.chord.reduce_extended_quality("min11")
```

### Common Failure Modes
- **Passing a full chord string:** Providing "C:maj9" instead of "maj9" will fail or produce incorrect results, as the function expects only the quality portion of the chord.
- **Passing invalid qualities:** Providing a quality string that violates `mir_eval`'s restricted `chord.QUALITIES` or regex validation rules.
- **Type errors:** Passing a non-string type (e.g., `None` or a list) to the `quality` parameter.

### Fix Code Hint
```python
# Incorrect: Passing the full chord string including the root
# base, ext = mir_eval.chord.reduce_extended_quality("G:maj7")

# Correct: Pass only the quality string
chord_label = "G:maj7"
root, quality = chord_label.split(":") # Simplified split for example
base, ext = mir_eval.chord.reduce_extended_quality(quality)
```

## API Test: `register_colormap`

### Signature
```python
def register_colormap(name, cmap)
```
_Source: source/mir_eval/display.py:117_

_Source doc:_ Handle changes to matplotlib colormap interface in 3.6.

### Goal
Register a custom matplotlib colormap safely, providing a compatibility layer for changes introduced to the colormap registry interface in matplotlib 3.6.

### Parameters
- `name`: The string identifier to assign to the registered colormap.
- `cmap`: The matplotlib `Colormap` instance (e.g., `ListedColormap` or `LinearSegmentedColormap`) to be registered.

### Input
The caller must provide a valid string name and an instantiated matplotlib `Colormap` object. Because this function interacts with `matplotlib`, the environment must have `matplotlib` (version 2 or higher) installed. 

### Output
Returns `unspecified` — this function operates via side effects, registering the provided colormap globally within matplotlib's internal colormap registry so it can be referenced by `name` in subsequent plotting calls.

### Valid Call Patterns
```python
import mir_eval.display
from matplotlib.colors import ListedColormap

# INFERRED FROM SIGNATURE (No verbatim examples provided in context)
custom_cmap = ListedColormap(['#000000', '#FFFFFF'])
mir_eval.display.register_colormap('binary_custom', custom_cmap)
```

### LLM Instruction Prompt
- When generating code that registers custom colormaps for `mir_eval.display` visualizations, always use `mir_eval.display.register_colormap(name, cmap)` instead of matplotlib's native `matplotlib.cm.register_cmap` or `matplotlib.colormaps.register`. This ensures compatibility across different matplotlib versions (specifically handling the API changes in matplotlib 3.6). Keep display tests headless and do not invoke `plt.show()`.

### Prompt Snippet
```text
Use `mir_eval.display.register_colormap(name, cmap)` to register matplotlib colormaps safely across matplotlib versions (>=2.0, including 3.6+ changes). Do not use `matplotlib.colormaps.register` directly when working within mir_eval's display module.
```

### Common Failure Modes
- **Passing an uninstantiated colormap class**: Providing a class like `ListedColormap` instead of an instance `ListedColormap([...])` will cause matplotlib registry errors.
- **Environment missing matplotlib**: While `mir_eval` core dependencies are `scipy`, `numpy`, and `decorator`, the `display` submodule requires `matplotlib`. Calling this without matplotlib installed will fail.
- **Violating headless constraints**: Attempting to test the registered colormap by opening a windowed plot (e.g., `plt.show()`) in a headless CI environment.

### Fix Code Hint
```python
# WRONG: Passing a raw list or uninstantiated class
# mir_eval.display.register_colormap('my_cmap', ['red', 'blue'])

# CORRECT: Instantiate a matplotlib Colormap object first
from matplotlib.colors import ListedColormap
my_cmap = ListedColormap(['red', 'blue'])
mir_eval.display.register_colormap('my_cmap', my_cmap)
```

## API Test: `resample_melody_series`

### Signature
```python
def resample_melody_series(times, frequencies, voicing, times_new, kind='linear')
```
_Source: source/mir_eval/melody.py:220_

_Source doc:_ Resamples frequency and voicing time series to a new timescale. Maintains any zero ("unvoiced") values in frequencies. If ``times`` and ``times_new`` are equivalent, no resampling will be performed. Parameters ---------- times : np.ndarray Times of each frequency value frequencies : np.ndarray Array of frequency values, >= 0 voicing : np.ndarray Array which indicates voiced or unvoiced. This array may be binary or have continuous values between 0 and 1. times_new : np.ndarray Times to resample frequency and voicing sequences to kind : str kind parameter to pass to scipy.interpolate.interp1d. (Default value = 'linear') Returns ------- frequencies_resampled : np.ndarray Frequency array resampled to new timebase voicing_resampled : np.ndarray Voicing array resampled to new timebase

### Goal
Resamples a melody's frequency and voicing time series to a new timescale, carefully maintaining zero values that represent unvoiced frames.

### Parameters
- `times`: `np.ndarray` of original timestamps (in seconds) corresponding to each frequency value.
- `frequencies`: `np.ndarray` of frequency values (>= 0), where 0 typically indicates an unvoiced frame.
- `voicing`: `np.ndarray` indicating voiced or unvoiced status. This array may be binary (0 or 1) or contain continuous values between 0 and 1.
- `times_new`: `np.ndarray` of the target timestamps to resample the frequency and voicing sequences to.
- `kind`, default `'linear'`: `str` specifying the interpolation method to pass to `scipy.interpolate.interp1d`.

### Input
Four 1D `np.ndarray` objects. `times`, `frequencies`, and `voicing` must all have the exact same length. `times` and `times_new` should be monotonically increasing time sequences. If `times` and `times_new` are identical, the function optimizes by returning the original arrays without performing interpolation.

### Output
Returns `unspecified` — A tuple of two `np.ndarray` objects: `(frequencies_resampled, voicing_resampled)`. The first array contains the frequencies interpolated to the new timebase, and the second contains the interpolated voicing values.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example with a zero transition and binary voicing
times = np.arange(4) / 35.0
cents = np.array([2.0, 0.0, -1.0, 1.0])
voicing = np.array([1, 0, 1, 1])
times_new = np.linspace(0, 0.08, 9)

res_cents, res_voicing = mir_eval.melody.resample_melody_series(
    times, cents, voicing, times_new
)

# Example with continuous voicing
voicing_continuous = np.array([0.8, 0.0, 0.2, 1.0])
res_cents_cont, res_voicing_cont = mir_eval.melody.resample_melody_series(
    times, cents, voicing_continuous, times_new
)
```

### LLM Instruction Prompt
- When evaluating melody extraction systems, use `mir_eval.melody.resample_melody_series` to align an estimated pitch trajectory to the reference's time grid (or vice versa) before computing metrics. 
- Do not attempt to manually interpolate the arrays using `scipy` or `numpy`, as `resample_melody_series` contains domain-specific logic to prevent zero-valued ("unvoiced") frames from being smeared into adjacent voiced frames during interpolation.
- Expect a tuple of two arrays `(frequencies, voicing)` as the return value.

### Prompt Snippet
```text
To align melody sequences with different timebases for comparison, use `mir_eval.melody.resample_melody_series(times, frequencies, voicing, times_new)`. It returns a tuple `(frequencies_resampled, voicing_resampled)` and safely handles zero-valued unvoiced frames without interpolation artifacts.
```

### Common Failure Modes
- **Mismatched Array Lengths**: Passing `times`, `frequencies`, and `voicing` arrays of different lengths will cause a failure when the internal interpolation function attempts to map them.
- **Extrapolation Errors**: Providing a `times_new` array with timestamps that fall significantly outside the bounds of the original `times` array may cause `scipy.interpolate.interp1d` to raise a `ValueError` (if bounds errors are triggered).
- **Non-NumPy Inputs**: Passing standard Python lists instead of `np.ndarray` objects may lead to unexpected behavior or attribute errors during array operations.

### Fix Code Hint
```python
# Ensure all inputs are NumPy arrays and that the source arrays match in length
times = np.asarray(times)
frequencies = np.asarray(frequencies)
voicing = np.asarray(voicing)
times_new = np.asarray(times_new)

if not (len(times) == len(frequencies) == len(voicing)):
    raise ValueError("times, frequencies, and voicing must have the same length.")

res_freqs, res_voicing = mir_eval.melody.resample_melody_series(
    times, frequencies, voicing, times_new
)
```

## API Test: `resample_multipitch`

### Signature
```python
def resample_multipitch(times, frequencies, target_times)
```
_Source: source/mir_eval/multipitch.py:101_

_Source doc:_ Resamples multipitch time series to a new timescale using nearest neighbor interpolation. Values in ``target_times`` outside the range of ``times`` return no pitch estimate. Parameters ---------- times : np.ndarray Array of time stamps frequencies : list of np.ndarray List of np.ndarrays of frequency values target_times : np.ndarray Array of target time stamps Returns ------- frequencies_resampled : list of numpy arrays Frequency list of lists resampled to new timebase

### Goal
Resamples a multipitch time series (where each timestamp can have zero, one, or multiple fundamental frequencies) to a new set of target timestamps using nearest-neighbor interpolation.

### Parameters
- `times`: A 1D `np.ndarray` of original time stamps (typically in seconds).
- `frequencies`: A `list` of `np.ndarray` objects, where each array contains the frequency values (in Hz) corresponding to the same index in `times`.
- `target_times`: A 1D `np.ndarray` of target time stamps to which the multipitch data should be resampled.

### Input
The caller must provide 1D numpy arrays for `times` and `target_times`. `frequencies` must be a list of 1D numpy arrays (not a 2D array, as multipitch frames can have a variable number of active pitches). The length of `times` must match the length of `frequencies`. Empty arrays and lists are permitted; if `times` and `frequencies` are empty, the function will return empty pitch estimates for all `target_times`.

### Output
Returns `unspecified` — A list of 1D numpy arrays (`frequencies_resampled`) representing the frequency values resampled to the new timebase. Any values in `target_times` that fall outside the minimum and maximum range of `times` will return an empty array (no pitch estimate).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

times = np.array([0.00, 0.01, 0.02, 0.03])
freqs = [
    np.array([200.0]),
    np.array([]),
    np.array([300.0, 400.0, 500.0]),
    np.array([300.0, 500.0]),
]
target_times = np.array([0.001, 0.002, 0.01, 0.029, 0.05])

# Resample the multipitch data to the target_times
actual_freqs = mir_eval.multipitch.resample_multipitch(times, freqs, target_times)
```

### LLM Instruction Prompt
- When calling `mir_eval.multipitch.resample_multipitch`, ensure that `frequencies` is formatted as a list of 1D numpy arrays, not a 2D numpy array or a list of standard Python lists.
- Be aware that nearest-neighbor interpolation is used.
- Do not attempt to extrapolate; target times outside the bounds of the original `times` array will deterministically result in empty arrays (`np.array([])`).

### Prompt Snippet
```text
Ensure the multipitch frequencies are passed as a list of numpy arrays. Use `mir_eval.multipitch.resample_multipitch(times, frequencies, target_times)` to align the estimated multipitch series to the reference timebase before evaluation.
```

### Common Failure Modes
- Passing a 2D numpy array for `frequencies` instead of a list of 1D arrays. Because multipitch data has a variable number of pitches per frame, a 2D array implies uniform padding which `mir_eval` does not expect here.
- Passing standard Python lists of floats inside the `frequencies` list instead of numpy arrays, which can cause downstream numpy operations to fail.
- Mismatched lengths between the `times` array and the `frequencies` list.

### Fix Code Hint
```python
# If frequencies is a list of lists, convert the inner lists to numpy arrays first:
frequencies_formatted = [np.array(f, dtype=float) for f in raw_frequencies]

# Then call the resampling function
resampled_freqs = mir_eval.multipitch.resample_multipitch(
    times=times_array, 
    frequencies=frequencies_formatted, 
    target_times=target_times_array
)
```

## API Test: `root`

### Signature
```python
def root(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1000_

_Source doc:_ Compare chords according to roots. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.root(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0], or -1 if the comparison is out of gamut.

### Goal
Compare estimated chord labels against reference chord labels strictly based on their root notes, ignoring chord quality or extensions.

### Parameters
- `reference_labels`: A list of length `n` containing the reference (ground truth) string chord labels to score against.
- `estimated_labels`: A list of length `n` containing the estimated string chord labels to evaluate.

### Input
The caller must provide two lists of string chord labels of identical length `n`. Typically, these labels are parsed from repository-format `.lab` files using `mir_eval.io.load_labeled_intervals`. Because raw annotation files often have mismatched timestamps, the intervals and labels must first be aligned and merged using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals` before passing the labels to this function. Chord strings are validated using regular expressions, and invalid chord types are restricted from `chord.QUALITIES`.

### Output
Returns `unspecified` — An `np.ndarray` of shape `(n,)` and dtype `float` containing the comparison scores. Scores are `1.0` for a correct root match, `0.0` for an incorrect match, or `-1.0` if the comparison is out of gamut (e.g., comparing against a "no chord" label when not applicable).

### Valid Call Patterns
```python
import mir_eval

# Example adapted from the source documentation
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Adjust estimated intervals to match the reference time boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# Merge intervals to create a common time grid with aligned labels
(intervals, ref_labels, est_labels) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# Compute root comparison scores
comparisons = mir_eval.chord.root(ref_labels, est_labels)

# Calculate final weighted accuracy using the durations of the merged intervals
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chord roots using `mir_eval.chord.root`, you MUST ensure `reference_labels` and `estimated_labels` are lists of the exact same length. Do not pass raw, unaligned labels directly from `load_labeled_intervals`. Always preprocess the intervals and labels using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals` first. The output is an array of scores per segment, which should typically be aggregated using `mir_eval.chord.weighted_accuracy(comparisons, durations)`.

### Prompt Snippet
```text
mir_eval.chord.root requires aligned label lists of equal length `n`. Preprocess with `mir_eval.util.merge_labeled_intervals` before calling. Returns an array of float scores (1.0, 0.0, or -1.0).
```

### Common Failure Modes
- **Length Mismatch:** Passing `reference_labels` and `estimated_labels` of different lengths because the user skipped the `merge_labeled_intervals` alignment step.
- **Invalid Chord Strings:** Passing malformed chord strings that fail the internal regular expression validation or contain qualities not present in `chord.QUALITIES`.
- **Passing Intervals Instead of Labels:** Accidentally passing the `intervals` numpy array instead of the `labels` list to the function.

### Fix Code Hint
```python
# If you encounter a length mismatch error, ensure you merge the intervals first:
intervals, ref_labels_aligned, est_labels_aligned = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
# Then pass the aligned labels to the metric:
comparisons = mir_eval.chord.root(ref_labels_aligned, est_labels_aligned)
```

## API Test: `rotate_bitmap_to_root`

### Signature
```python
def rotate_bitmap_to_root(bitmap, chord_root)
```
_Source: source/mir_eval/chord.py:559_

_Source doc:_ Circularly shift a relative bitmap to its absolute pitch classes. For clarity, the best explanation is an example. Given 'G:Maj', the root and quality map are as follows:: root=5 quality=[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]  # Relative chord shape After rotating to the root, the resulting bitmap becomes:: abs_quality = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]  # G, B, and D Parameters ---------- bitmap : np.ndarray, shape=(12,) Bitmap of active notes, relative to the given root. chord_root : int Absolute pitch class number. Returns ------- bitmap : np.ndarray, shape=(12,) Absolute bitmap of active pitch classes.

### Goal
Circularly shifts a 12-element relative pitch class bitmap (representing a chord's quality) to its absolute pitch classes based on the given absolute chord root.

### Parameters
- `bitmap`: `np.ndarray`, shape=(12,). A bitmap of active notes, relative to the given root (e.g., `[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]` for a major triad).
- `chord_root`: `int`. The absolute pitch class number of the chord's root (e.g., `5` for G).

### Input
The caller must provide a 1-dimensional numpy array of exactly 12 elements representing the relative chord shape, and an integer representing the absolute pitch class root (typically 0-11). Because the internal implementation uses tuple indexing, `bitmap` must be a valid numpy array, not a standard Python list.

### Output
Returns `unspecified` — A numpy array (`np.ndarray`) of shape `(12,)` representing the absolute bitmap of active pitch classes (e.g., `[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1]` for G Major).

### Valid Call Patterns
```python
# Inferred from signature and project context (not verified by existing tests)
import numpy as np
import mir_eval

relative_quality = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
chord_root = 5  # G

absolute_bitmap = mir_eval.chord.rotate_bitmap_to_root(relative_quality, chord_root)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.rotate_bitmap_to_root`, ensure the `bitmap` argument is explicitly cast to a numpy array of shape `(12,)`. Do not pass a standard Python list, as the function relies on tuple indexing which will fail on lists.
- Ensure `chord_root` is provided as an integer.

### Prompt Snippet
```text
`mir_eval.chord.rotate_bitmap_to_root(bitmap, chord_root)` circularly shifts a relative 12-element chord quality bitmap to its absolute pitch classes. `bitmap` must be a numpy array of shape (12,) (due to internal tuple indexing) and `chord_root` must be an integer representing the absolute pitch class.
```

### Common Failure Modes
- **TypeError due to list input**: Passing a standard Python list instead of a `np.ndarray` for `bitmap` will cause a `TypeError` because the function uses tuple indexing internally, which lists do not support.
- **ValueError due to incorrect shape**: Passing a numpy array that does not have exactly 12 elements (representing the 12 semitones).
- **TypeError due to float root**: Passing a float instead of an integer for `chord_root` may cause indexing or shifting errors.

### Fix Code Hint
```python
# Ensure the bitmap is a numpy array before passing it to the function
bitmap_array = np.array(relative_bitmap_list, dtype=int)
root_int = int(chord_root)
absolute_bitmap = mir_eval.chord.rotate_bitmap_to_root(bitmap_array, root_int)
```

## API Test: `rotate_bitmaps_to_roots`

### Signature
```python
def rotate_bitmaps_to_roots(bitmaps, roots)
```
_Source: source/mir_eval/chord.py:594_

_Source doc:_ Circularly shift a relative bitmaps to absolute pitch classes. See :func:`rotate_bitmap_to_root` for more information. Parameters ---------- bitmaps : np.ndarray, shape=(N, 12) Bitmap of active notes, relative to the given root. roots : np.ndarray, shape=(N,) Absolute pitch class number. Returns ------- bitmap : np.ndarray, shape=(N, 12) Absolute bitmaps of active pitch classes.

### Goal
Circularly shift an array of relative chord bitmaps to absolute pitch classes based on their corresponding root notes.

### Parameters
- `bitmaps`: `np.ndarray, shape=(N, 12)` (or array-like) representing the bitmaps of active notes, relative to the given roots.
- `roots`: `np.ndarray, shape=(N,)` (or array-like) representing the absolute pitch class numbers corresponding to each bitmap.

### Input
The caller must provide a sequence of `N` relative bitmaps (where each bitmap is a 12-dimensional array or list representing the 12 semitones) and a sequence of `N` root pitch classes (integers). These can be passed as numpy arrays or standard Python lists (as demonstrated in the test suite).

### Output
Returns `unspecified` — A numpy array of shape `(N, 12)` containing the absolute bitmaps of active pitch classes.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example derived from the project's test suite
bitmap = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0] # Example relative major triad
root = 0 # Example root pitch class (C)
expected_bitmap = [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

ans = mir_eval.chord.rotate_bitmaps_to_roots([bitmap], [root])
assert np.all(ans == [expected_bitmap])
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.rotate_bitmaps_to_roots`, ensure the inputs are aligned in size `N`. The `bitmaps` argument must be an `(N, 12)` array-like structure, and `roots` must be an `(N,)` array-like structure of pitch class integers.

### Prompt Snippet
```text
mir_eval.chord.rotate_bitmaps_to_roots(bitmaps, roots): Circularly shifts an (N, 12) array of relative chord bitmaps to absolute pitch classes using an (N,) array of root pitch class integers.
```

### Common Failure Modes
- Providing `bitmaps` and `roots` with mismatched `N` dimensions (e.g., passing 10 bitmaps but only 9 roots).
- Providing bitmaps that do not have exactly 12 elements per row, violating the `(N, 12)` shape requirement for pitch classes.
- Passing non-integer values for `roots`, which cannot be used as valid shift amounts for pitch classes.

### Fix Code Hint
```python
# Ensure inputs are properly shaped numpy arrays before calling
bitmaps_arr = np.atleast_2d(bitmaps)
roots_arr = np.atleast_1d(roots)

if bitmaps_arr.shape[0] != roots_arr.shape[0]:
    raise ValueError("Number of bitmaps must match number of roots.")
if bitmaps_arr.shape[1] != 12:
    raise ValueError("Each bitmap must have exactly 12 elements.")

ans = mir_eval.chord.rotate_bitmaps_to_roots(bitmaps_arr, roots_arr)
```

## API Test: `scale_degree_to_bitmap`

### Signature
```python
def scale_degree_to_bitmap(scale_degree, modulo=False, length=BITMAP_LENGTH)
```
_Source: source/mir_eval/chord.py:211_

_Source doc:_ Create a bitmap representation of a scale degree. Note that values in the bitmap may be negative, indicating that the semitone is to be removed. Parameters ---------- scale_degree : str Spelling of a relative scale degree, e.g. 'b3', '7', '#5' modulo : bool, default=True If a scale degree exceeds the length of the bit-vector, modulo the scale degree back into the bit-vector; otherwise it is discarded. length : int, default=12 Length of the bit-vector to produce Returns ------- bitmap : np.ndarray, in [-1, 0, 1], len=`length` Bitmap representation of this scale degree.

### Goal
Create a bit-vector (bitmap) representation of a relative musical scale degree, where values can be negative to indicate that a semitone should be removed.

### Parameters
- `scale_degree`: A string representing the spelling of a relative scale degree (e.g., `'b3'`, `'7'`, `'#5'`).
- `modulo`, default `False`: A boolean flag. If `True`, a scale degree that exceeds the length of the bit-vector is wrapped (modulo) back into the vector; if `False`, it is discarded. *(Note: While the docstring mentions `default=True`, the actual Python signature defaults to `False`.)*
- `length`, default `BITMAP_LENGTH`: An integer specifying the length of the bit-vector to produce (typically 12 for a standard chromatic scale).

### Input
The caller must provide a valid string for the `scale_degree`. According to project compatibility rules, callers **must explicitly provide** the `modulo` and `length` arguments when calling this function, rather than relying on the implicit defaults.

### Output
Returns `unspecified` — A 1D `np.ndarray` of length `length` containing integer values in `[-1, 0, 1]`. This array represents the bitmap of the scale degree, where a `-1` indicates a semitone to be removed.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Explicitly providing modulo and length as required by project rules
degree_str = 'b3'
bitmap = mir_eval.chord.scale_degree_to_bitmap(degree_str, modulo=True, length=12)

# The output is a numpy array that can be checked for specific values
assert isinstance(bitmap, np.ndarray)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.scale_degree_to_bitmap`, you MUST explicitly pass the `modulo` and `length` arguments as keyword arguments. Do not rely on their default values.
- Ensure `scale_degree` is passed as a string (e.g., `'b3'`, `'#5'`).
- Be aware that the returned bitmap is not strictly binary; it contains values in `[-1, 0, 1]`, where `-1` denotes a removed semitone.

### Prompt Snippet
```text
Generate a bitmap for the scale degree '#5' using mir_eval.chord.scale_degree_to_bitmap. You must explicitly provide the `modulo` and `length` arguments (e.g., modulo=True, length=12) as required by the library's usage patterns.
```

### Common Failure Modes
- **Missing Explicit Arguments**: Relying on the default values for `modulo` or `length` violates the project's type-selection rules and can lead to unexpected behavior or test failures.
- **Incorrect Input Type**: Passing an integer (e.g., `3`) instead of a string (e.g., `'3'`) for the `scale_degree` parameter.
- **Misinterpreting the Output**: Assuming the returned numpy array is strictly boolean or binary `[0, 1]`. The array can contain `-1` values which will break logic that expects standard binary masks.

### Fix Code Hint
```python
# BAD: Relying on defaults and passing an integer
# bitmap = mir_eval.chord.scale_degree_to_bitmap(7)

# GOOD: Passing a string and explicitly defining modulo and length
bitmap = mir_eval.chord.scale_degree_to_bitmap('7', modulo=False, length=12)
```

## API Test: `scale_degree_to_semitone`

### Signature
```python
def scale_degree_to_semitone(scale_degree)
```
_Source: source/mir_eval/chord.py:175_

_Source doc:_ Convert a scale degree to semitone. Parameters ---------- scale_degree : str Spelling of a relative scale degree, e.g. 'b3', '7', '#5' Returns ------- semitone : int Relative semitone of the scale degree, wrapped to a single octave Raises ------ InvalidChordException if `scale_degree` is invalid.

### Goal
Convert a string spelling of a relative musical scale degree into its corresponding integer semitone offset within a single octave.

### Parameters
- `scale_degree`: A string representing the spelling of a relative scale degree (e.g., `'b3'`, `'7'`, `'#5'`).

### Input
A string containing a valid musical scale degree notation. The string must use standard accidentals (`'b'` for flat, `'#'` for sharp) preceding the degree number.

### Output
Returns `unspecified` — An integer representing the relative semitone of the scale degree, wrapped to a single octave.

### Valid Call Patterns
```python
import mir_eval

# Convert a flat third to its semitone integer
semitone_b3 = mir_eval.chord.scale_degree_to_semitone('b3')

# Convert a sharp fifth to its semitone integer
semitone_sharp5 = mir_eval.chord.scale_degree_to_semitone('#5')
```

### LLM Instruction Prompt
- Use `mir_eval.chord.scale_degree_to_semitone(scale_degree)` to map a string scale degree to an integer semitone. The input must be a valid string spelling (e.g., `'b3'`, `'#5'`). You must handle or prevent `InvalidChordException` if the input string might be malformed or invalid.

### Prompt Snippet
```text
mir_eval.chord.scale_degree_to_semitone(scale_degree: str) -> int: Converts a scale degree string (e.g., 'b3', '7') to a semitone integer wrapped to a single octave. Raises InvalidChordException on invalid input.
```

### Common Failure Modes
- Raising `InvalidChordException` because the `scale_degree` string is invalid, malformed, or uses non-standard accidentals (e.g., passing `'flat3'` instead of `'b3'`).
- Passing an integer (e.g., `3`) instead of the required string representation (e.g., `'3'`).

### Fix Code Hint
```python
import mir_eval

degree_str = "b3"
try:
    semitone = mir_eval.chord.scale_degree_to_semitone(degree_str)
except mir_eval.chord.InvalidChordException:
    # Fallback or error handling for invalid scale degree spelling
    semitone = None
```

## API Test: `seg`

### Signature
```python
def seg(reference_intervals, estimated_intervals)
```
_Source: source/mir_eval/chord.py:1461_

_Source doc:_ Compute the MIREX 'MeanSeg' score. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> score = mir_eval.chord.seg(ref_intervals, est_intervals) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2), dtype=float Reference chord intervals to score against. estimated_intervals : np.ndarray, shape=(m, 2), dtype=float Estimated chord intervals to score against. Returns ------- segmentation score : float Comparison score, in [0.0, 1.0], where 1.0 means perfect segmentation.

### Goal
Compute the MIREX "MeanSeg" score to evaluate how well estimated chord segmentation intervals align with reference ground-truth intervals.

### Parameters
- `reference_intervals`: A 2D numpy array of shape `(n, 2)` and `dtype=float` representing the reference chord intervals (start and end times) to score against.
- `estimated_intervals`: A 2D numpy array of shape `(m, 2)` and `dtype=float` representing the estimated chord intervals (start and end times) to score against.

### Input
Both inputs must be 2D numpy arrays of shape `(N, 2)` containing float values that represent the start and end times of audio segments (e.g., chords). These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_labeled_intervals()`. Because `load_labeled_intervals` returns a tuple of `(intervals, labels)`, you must unpack the tuple and pass only the `intervals` array to this function.

### Output
Returns `unspecified` — A `float` representing the segmentation comparison score in the range `[0.0, 1.0]`, where `1.0` indicates perfect segmentation.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Pattern 1: Using deterministic in-memory arrays
ref_ivs = np.array([[0.0, 2.0], [2.0, 2.5], [2.5, 3.2]])
est_ivs = np.array([[0.0, 3.0], [3.0, 3.5]])
score = mir_eval.chord.seg(ref_ivs, est_ivs)

# Pattern 2: Loading from repository-format annotation files
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')
score = mir_eval.chord.seg(ref_intervals, est_intervals)
```

### LLM Instruction Prompt
- When evaluating chord segmentation using `mir_eval.chord.seg`, ensure that both inputs are `(n, 2)` float numpy arrays representing intervals. Do not pass the string labels. If loading data using `mir_eval.io.load_labeled_intervals`, you must unpack the returned `(intervals, labels)` tuple and pass only the `intervals` to `seg`.

### Prompt Snippet
```text
To compute the MIREX MeanSeg score for chord segmentation, use `mir_eval.chord.seg(reference_intervals, estimated_intervals)`. Ensure inputs are `(n, 2)` float numpy arrays. If loading from files via `mir_eval.io.load_labeled_intervals`, unpack the tuple and pass only the intervals, discarding the labels.
```

### Common Failure Modes
- **Passing labels instead of intervals**: Passing the raw output of `mir_eval.io.load_labeled_intervals()` directly into `seg` without unpacking it. This passes a tuple `(intervals, labels)` where a numpy array is expected, causing a `TypeError` or `ValueError`.
- **Incorrect array shape**: Passing 1D arrays of boundaries instead of `(n, 2)` interval pairs. If you have boundaries, they must first be converted using `mir_eval.util.boundaries_to_intervals`.

### Fix Code Hint
```python
# BAD: Passing the tuple directly from the IO function
ref_data = mir_eval.io.load_labeled_intervals('ref.lab')
est_data = mir_eval.io.load_labeled_intervals('est.lab')
score = mir_eval.chord.seg(ref_data, est_data)  # Fails

# GOOD: Unpack the tuple and pass only the intervals
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')
score = mir_eval.chord.seg(ref_intervals, est_intervals)
```

## API Test: `segments`

### Signature
```python
def segments(intervals, labels, base=None, height=None, text=False, text_kw=None, ax=None, prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:180_

### Goal
Plot a music or audio segmentation as a set of disjoint rectangles on a matplotlib axis for visual inspection.

### Parameters
- `intervals`: `np.ndarray` of shape `(n, 2)` representing segment start and end times, typically loaded via `mir_eval.io.load_intervals` or `mir_eval.io.load_labeled_intervals`.
- `labels`: `list` of length `n` containing the reference segment labels corresponding to the `intervals`.
- `base`, default `None`: `number` representing the vertical position of the base of the rectangles. If provided, `height` must also be provided. Defaults to the bottom of the plot.
- `height`, default `None`: `number` representing the height of the rectangles. If provided, `base` must also be provided. Defaults to the top of the plot (minus `base`).
- `text`, default `False`: `bool` indicating whether to display each segment's label in its upper-left corner.
- `text_kw`, default `None`: `dict` of properties to pass to `matplotlib.pyplot.Text` if `text == True`.
- `ax`, default `None`: `matplotlib.pyplot.axes` handle on which to draw the segmentation. If `None`, a new set of axes is created.
- `prop_cycle`, default `None`: `cycle.Cycler` object to specify style properties. If not provided, the default property cycler is retrieved from matplotlib.
- `**kwargs`: Additional keyword arguments to pass directly to `matplotlib.patches.Rectangle`.

### Input
The caller must provide an `(n, 2)` numpy array of intervals and a list of `n` labels. These are typically obtained by parsing a repository-format annotation file using `mir_eval.io.load_labeled_intervals`. 
**Preconditions:** 
- If specifying custom vertical bounds, both `base` and `height` must be provided together; providing only one is invalid.
- For automated testing or reproducible metric evaluations, display tests must be kept headless (do not invoke interactive GUI windows or require network/audio-device access).

### Output
Returns `unspecified` — A `matplotlib.pyplot.axes._subplots.AxesSubplot` handle to the (possibly constructed) plot axes containing the drawn segmentation rectangles.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval
from mir_eval.io import load_labeled_intervals

# Example 1: Plotting segments without text labels
plt.figure()
intervals, labels = load_labeled_intervals("data/segment/ref00.lab")
ax = mir_eval.display.segments(intervals, labels, text=False)
plt.legend(loc="upper right")

# Example 2: Plotting segments with text labels enabled
plt.figure()
intervals, labels = load_labeled_intervals("data/segment/ref00.lab")
ax = mir_eval.display.segments(intervals, labels, text=True)
```

### LLM Instruction Prompt
- When plotting segmentations using `mir_eval.display.segments`, ensure that the `intervals` array has shape `(n, 2)` and matches the length of the `labels` list. 
- If you need to customize the vertical placement of the rectangles, you MUST provide both `base` and `height` arguments; providing only one will cause an error. 
- Always keep display tests headless (e.g., do not call `plt.show()` in automated test environments).

### Prompt Snippet
```text
Plot the loaded segmentation intervals and labels using `mir_eval.display.segments`. Enable text labels on the rectangles and set the base to 0 and height to 1. Ensure the plot is generated headlessly.
```

### Common Failure Modes
- **Missing `base` or `height`:** Providing `base` without `height` (or vice versa) violates the function's preconditions.
- **Mismatched dimensions:** Passing an `intervals` array that does not have shape `(n, 2)` or a `labels` list that does not have exactly `n` elements.
- **Interactive plotting in tests:** Failing to keep the display test headless, causing the test suite to hang or crash in CI environments without a display server.

### Fix Code Hint
```python
# BAD: Providing base without height
# ax = mir_eval.display.segments(intervals, labels, base=0)

# GOOD: Providing both base and height
ax = mir_eval.display.segments(intervals, labels, base=0, height=1)

# GOOD: Providing neither (uses plot defaults)
ax = mir_eval.display.segments(intervals, labels)
```

## API Test: `separation`

### Signature
```python
def separation(sources, fs=22050, labels=None, alpha=0.75, ax=None, rasterized=True, edgecolors='None', shading='gouraud', prop_cycle=None, **kwargs)
```
_Source: source/mir_eval/display.py:923_

_Source doc:_ Source-separation visualization Parameters ---------- sources : np.ndarray, shape=(nsrc, nsampl) A list of waveform buffers corresponding to each source fs : number > 0 The sampling rate labels : list of strings An optional list of descriptors corresponding to each source alpha : float in [0, 1] Maximum alpha (opacity) of spectrogram values. ax : matplotlib.pyplot.axes An axis handle on which to draw the spectrograms. If none is provided, a new set of axes is created. rasterized : bool If `True`, the spectrogram is rasterized. edgecolors : str or None The color of the edges of the spectrogram patches. Set to "None" (default) to disable edge coloring. shading : str The shading method to use for the spectrogram. See `matplotlib.pyplot.pcolormesh` for valid options. prop_cycle : cycle.Cycler An optional property cycle object to specify colors for each signal. If not provided, the default property cycler will be retrieved from matplotlib. **kwargs Additional keyword arguments to ``scipy.signal.spectrogram`` Returns ------- ax The axis handle for this plot

### Goal
Visualizes source-separation outputs by plotting overlaid spectrograms of multiple waveform buffers on a matplotlib axis.

### Parameters
- `sources`: `np.ndarray` of shape `(nsrc, nsampl)` or a list of 1D arrays. A list of waveform buffers corresponding to each separated audio source.
- `fs`, default `22050`: `number > 0`. The sampling rate of the audio sources.
- `labels`, default `None`: A list of strings providing optional descriptors corresponding to each source, useful for generating a legend.
- `alpha`, default `0.75`: `float` in `[0, 1]`. The maximum alpha (opacity) of the spectrogram values.
- `ax`, default `None`: `matplotlib.pyplot.axes`. An axis handle on which to draw the spectrograms. If none is provided, a new set of axes is created.
- `rasterized`, default `True`: `bool`. If `True`, the spectrogram is rasterized to optimize rendering performance and file size.
- `edgecolors`, default `'None'`: `str` or `None`. The color of the edges of the spectrogram patches. Set to `"None"` to disable edge coloring.
- `shading`, default `'gouraud'`: `str`. The shading method to use for the spectrogram (see `matplotlib.pyplot.pcolormesh` for valid options).
- `prop_cycle`, default `None`: `cycle.Cycler`. An optional property cycle object to specify colors for each signal. If not provided, matplotlib's default property cycler is used.
- `**kwargs`: Additional keyword arguments passed directly to `scipy.signal.spectrogram`.

### Input
The caller must provide the audio sources as either a 2D numpy array of shape `(nsrc, nsampl)` or a list of 1D numpy arrays representing the waveforms. The sampling rate `fs` must be strictly greater than 0. If `labels` are provided, the length of the list must exactly match the number of sources (`nsrc`). Because `mir_eval.io.load_wav` is deprecated, callers should generate deterministic in-memory arrays for testing or use standard external libraries (like `scipy.io.wavfile`) to load audio.

### Output
Returns `unspecified` — Returns the `matplotlib.pyplot.axes` handle (`ax`) containing the plotted spectrograms.

### Valid Call Patterns
```python
import numpy as np
import matplotlib.pyplot as plt
import mir_eval

# Generate deterministic in-memory arrays for headless testing
fs = 22050
t = np.linspace(0, 1, fs)
x0 = np.sin(2 * np.pi * 440 * t)
x1 = np.sin(2 * np.pi * 880 * t)
x2 = np.sin(2 * np.pi * 1320 * t)

plt.figure()
# Call the display function
ax = mir_eval.display.separation(
    sources=[x0, x1, x2], 
    fs=fs, 
    labels=["Source 1", "Source 2", "Source 3"]
)
plt.legend(loc="upper right")
```

### LLM Instruction Prompt
- When testing `mir_eval.display.separation`, always use deterministic in-memory numpy arrays (e.g., sine waves) rather than attempting to load audio files from disk, and ensure the test environment is headless (no network or audio-device access).
- Do not use `mir_eval.io.load_wav` to load audio, as it is deprecated and slated for removal.
- Ensure the `fs` parameter is strictly greater than 0.
- If providing `labels`, ensure the number of labels matches the number of waveform buffers in `sources`.

### Prompt Snippet
```text
Use `mir_eval.display.separation(sources, fs=22050, labels=None, ...)` to plot overlaid spectrograms of separated audio sources. Pass a list of 1D numpy arrays or a 2D array `(nsrc, nsampl)` as `sources`. For tests, use deterministic in-memory arrays and a headless matplotlib environment. Do not use the deprecated `mir_eval.io.load_wav`.
```

### Common Failure Modes
- **Deprecated Audio Loading**: Using `mir_eval.io.load_wav` to load the source files, which will trigger deprecation warnings or fail in newer versions.
- **Mismatched Labels**: Passing a `labels` list that has a different length than the `sources` list, causing a mismatch when applying the property cycle or generating the legend.
- **Invalid Sampling Rate**: Passing `fs=0` or a negative number, which violates the `number > 0` precondition and causes `scipy.signal.spectrogram` to fail.
- **Display Side Effects**: Failing to use a headless matplotlib backend in CI environments, causing the test to crash when attempting to open a window.

### Fix Code Hint
```python
# BAD: Using deprecated load_wav and failing to configure headless mode
# x0, fs = mir_eval.io.load_wav("0.wav")
# mir_eval.display.separation([x0], fs=fs)

# GOOD: Using deterministic arrays for testing in a headless environment
import matplotlib
matplotlib.use('Agg') # Ensure headless backend
import matplotlib.pyplot as plt
import numpy as np
import mir_eval

fs = 22050
x0 = np.sin(2 * np.pi * 440 * np.linspace(0, 1, fs))
fig, ax = plt.subplots()
mir_eval.display.separation([x0], fs=fs, ax=ax, labels=["Sine 440Hz"])
```

## API Test: `sevenths`

### Signature
```python
def sevenths(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1236_

_Source doc:_ Compare chords along MIREX 'sevenths' rules. Chords with qualities outside [maj, maj7, 7, min, min7, N] are ignored. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.sevenths(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0], or -1 if the comparison is out of gamut.

### Goal
Compare reference and estimated chord labels according to the MIREX 'sevenths' rules, scoring matches while ignoring chords with qualities outside of major, major 7th, dominant 7th, minor, minor 7th, and "no chord" (N).

### Parameters
- `reference_labels`: `list` (len=n) — A list of string reference chord labels (ground truth) to score against.
- `estimated_labels`: `list` (len=n) — A list of string estimated chord labels to evaluate.

### Input
The caller must provide two lists of string chord labels of identical length `n`. Because raw chord annotations typically occur over unaligned time intervals, the caller must first preprocess the data by loading the labeled intervals, adjusting the estimated intervals to the reference boundaries (using `mir_eval.util.adjust_intervals`), and merging them into a common time grid (using `mir_eval.util.merge_labeled_intervals`). Chord validation uses regular expressions and restricts invalid chord types from `chord.QUALITIES`.

### Output
Returns `unspecified` (documented as `np.ndarray`, shape=(n,), dtype=float) — An array of comparison scores where each element is in `[0.0, 1.0]` representing the accuracy of the match, or `-1.0` if the reference chord is out of gamut (i.e., its quality is not one of `[maj, maj7, 7, min, min7, N]`) and should be ignored in downstream metric aggregation.

### Valid Call Patterns
```python
import mir_eval

# 1. Load intervals and labels
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# 2. Adjust estimated intervals to reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# 3. Merge into a common time grid
intervals, ref_labels_merged, est_labels_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# 4. Compute sevenths comparisons
comparisons = mir_eval.chord.sevenths(ref_labels_merged, est_labels_merged)

# 5. Aggregate into a final weighted accuracy score
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chord estimations using `mir_eval.chord.sevenths`, you MUST first align the reference and estimated labels to a common time grid using `mir_eval.util.merge_labeled_intervals`.
- Pass the resulting aligned string lists to `sevenths(reference_labels, estimated_labels)`.
- Do not aggregate the resulting array with standard `numpy.mean()`; you must use `mir_eval.chord.weighted_accuracy(comparisons, durations)` to correctly weight the scores by interval duration and properly ignore the `-1` out-of-gamut values.

### Prompt Snippet
```text
To score chords using MIREX 'sevenths' rules, align the intervals using `mir_eval.util.merge_labeled_intervals`, pass the aligned label lists to `mir_eval.chord.sevenths(ref_labels, est_labels)`, and aggregate the returned array using `mir_eval.chord.weighted_accuracy(comparisons, durations)` to handle durations and -1 (out-of-gamut) scores.
```

### Common Failure Modes
- **Unaligned Inputs**: Passing raw label lists of different lengths directly from `load_labeled_intervals` without merging them first. This will cause a length mismatch error.
- **Incorrect Aggregation**: Using `np.mean(comparisons)` instead of `mir_eval.chord.weighted_accuracy`. This fails to account for chord durations and incorrectly includes `-1` (out-of-gamut) flags as negative scores in the average.
- **Passing Intervals Instead of Labels**: Accidentally passing the `intervals` array instead of the `labels` list to the function.

### Fix Code Hint
```python
# BAD: Unaligned labels and incorrect aggregation
# comparisons = mir_eval.chord.sevenths(ref_labels, est_labels)
# score = np.mean(comparisons)

# GOOD: Merge intervals first, then use weighted_accuracy
intervals, ref_labels_merged, est_labels_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.sevenths(ref_labels_merged, est_labels_merged)
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

## API Test: `sevenths_inv`

### Signature
```python
def sevenths_inv(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:1295_

_Source doc:_ Compare chords along MIREX 'sevenths' rules. Chords with qualities outside [maj, maj7, 7, min, min7, N] are ignored. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.sevenths_inv(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0], or -1 if the comparison is out of gamut.

### Goal
Compare estimated chord labels against reference chord labels using the MIREX 'sevenths' rules (which evaluate seventh chords and their inversions), ignoring chord qualities outside of a specific gamut.

### Parameters
- `reference_labels`: `list`, len=n. Reference chord labels (ground truth) to score against.
- `estimated_labels`: `list`, len=n. Estimated chord labels (predictions) to score against.

### Input
The caller must provide two equal-length lists of string chord labels (e.g., `['C:maj', 'G:7/3', 'N']`). Chord validation uses regular expressions and restricts invalid chord types from `chord.QUALITIES`. Because chord annotations typically span time intervals, the raw reference and estimated labels must first be aligned and merged into a common time grid (usually via `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals`) before being passed to this function.

### Output
Returns `np.ndarray, shape=(n,), dtype=float` — an array of comparison scores where each element is in `[0.0, 1.0]`. If a reference chord's quality falls outside the allowed gamut (`[maj, maj7, 7, min, min7, N]`), the comparison is considered out of gamut and the function returns `-1.0` for that index.

### Valid Call Patterns
```python
import mir_eval

# Deterministic in-memory arrays of aligned chord labels
ref_labels = ['C:maj', 'G:7', 'A:min7', 'N']
est_labels = ['C:maj', 'G:7/3', 'A:min', 'N']

# Compute the sevenths_inv comparison scores
comparisons = mir_eval.chord.sevenths_inv(ref_labels, est_labels)

# Typically followed by computing the weighted accuracy using interval durations
# score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chords with `mir_eval.chord.sevenths_inv`, ensure `reference_labels` and `estimated_labels` are equal-length lists of strings.
- Do not pass raw, unaligned interval labels directly to this function; they must be merged onto a common time grid using `mir_eval.util.merge_labeled_intervals` first.
- Be aware that this metric ignores chords with qualities outside `[maj, maj7, 7, min, min7, N]`, returning `-1.0` for those indices.
- To get a final scalar metric, pass the resulting comparison array and the corresponding interval durations to `mir_eval.chord.weighted_accuracy`.

### Prompt Snippet
```text
Use `mir_eval.chord.sevenths_inv(ref_labels, est_labels)` to compute MIREX 'sevenths' chord scores (including inversions). Inputs must be equal-length lists of string labels that have already been aligned to a common time grid. The function returns a numpy array of scores in [0.0, 1.0], or -1.0 for out-of-gamut chords.
```

### Common Failure Modes
- Passing lists of unequal lengths, which occurs if the user forgets to merge the reference and estimated intervals onto a common time grid.
- Passing invalid chord strings that fail `mir_eval`'s internal regular expression validation.
- Passing raw interval arrays (e.g., `[[0.0, 1.5], [1.5, 3.0]]`) instead of the string label lists.

### Fix Code Hint
```python
# FIX: Align and merge intervals before scoring
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, ref_intervals.min(),
    ref_intervals.max(), mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

intervals, ref_labels_merged, est_labels_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# Now it is safe to call sevenths_inv
comparisons = mir_eval.chord.sevenths_inv(ref_labels_merged, est_labels_merged)
```

## API Test: `sort_labeled_intervals`

### Signature
```python
def sort_labeled_intervals(intervals, labels=None)
```
_Source: source/mir_eval/util.py:171_

_Source doc:_ Sort intervals, and optionally, their corresponding labels according to start time. Parameters ---------- intervals : np.ndarray, shape=(n, 2) The input intervals labels : list, optional Labels for each interval Returns ------- intervals_sorted or (intervals_sorted, labels_sorted) Labels are only returned if provided as input

### Goal
Sorts a set of time intervals, and optionally their corresponding labels, chronologically according to their start times.

### Parameters
- `intervals`: `np.ndarray, shape=(n, 2)` — The input intervals, typically representing start and end times in seconds.
- `labels`, default `None`: `list, optional` — A list of labels corresponding to each interval.

### Input
The caller must provide `intervals` as a 2-dimensional numpy array of shape `(n, 2)`. If the optional `labels` argument is provided, it must be a list of length `n` containing the corresponding label for each interval in the array.

### Output
Returns `unspecified` — The function dynamically returns either a single value or a tuple based on the input arguments. If `labels` is `None`, it returns `intervals_sorted` (a numpy array of the sorted intervals). If `labels` is provided, it returns a tuple `(intervals_sorted, labels_sorted)` containing both the sorted intervals array and the sorted labels list.

### Valid Call Patterns
```python
# Pattern 1: Sorting intervals and labels together
xs, ls = mir_eval.util.sort_labeled_intervals(x, labels)

# Pattern 2: Sorting only intervals
xs = mir_eval.util.sort_labeled_intervals(x)
```

### LLM Instruction Prompt
- When calling `mir_eval.util.sort_labeled_intervals`, you must adjust your return value unpacking based on whether the `labels` argument is provided. If `labels` is passed, unpack two variables `(intervals_sorted, labels_sorted)`. If `labels` is omitted or `None`, assign the result to a single variable `intervals_sorted`. Ensure the input `intervals` is an `(n, 2)` numpy array.

### Prompt Snippet
```text
`mir_eval.util.sort_labeled_intervals(intervals, labels=None)` returns `intervals_sorted` if `labels` is None, or `(intervals_sorted, labels_sorted)` if `labels` is provided. Ensure `intervals` is an `(n, 2)` np.ndarray.
```

### Common Failure Modes
- **Unpacking Error (ValueError):** Attempting to unpack two values when `labels` is not provided, or assigning to a single variable when `labels` is provided, causing a tuple to be unexpectedly assigned to the intervals variable.
- **Shape Mismatch:** Passing a 1-dimensional array or an array with a shape other than `(n, 2)` for the `intervals` parameter.
- **Length Mismatch:** Providing a `labels` list whose length does not match the number of rows `n` in the `intervals` array.

### Fix Code Hint
```python
# WRONG: Unpacking two values when labels is not provided
# xs, ls = mir_eval.util.sort_labeled_intervals(x)

# CORRECT: Assign to a single variable when sorting only intervals
xs = mir_eval.util.sort_labeled_intervals(x)

# CORRECT: Unpack two variables when labels are provided
xs, ls = mir_eval.util.sort_labeled_intervals(x, labels)
```

## API Test: `split`

### Signature
```python
def split(chord_label, reduce_extended_chords=False)
```
_Source: source/mir_eval/chord.py:361_

_Source doc:_ Parse a chord label into its four constituent parts: - root - quality shorthand - scale degrees - bass Note: Chords lacking quality AND interval information are major. - If a quality is specified, it is returned. - If an interval is specified WITHOUT a quality, the quality field is empty. Some examples:: 'C' -> ['C', 'maj', {}, '1'] 'G#:min(*b3,*5)/5' -> ['G#', 'min', {'*b3', '*5'}, '5'] 'A:(3)/6' -> ['A', '', {'3'}, '6'] Parameters ---------- chord_label : str A chord label. reduce_extended_chords : bool Whether to map the upper voicings of extended chords (9's, 11's, 13's) to semitone extensions. (Default value = False) Returns ------- chord_parts : list Split version of the chord label.

### Goal
Parse a string-based chord label into its four constituent parts (root, quality shorthand, scale degrees, and bass) for music information retrieval evaluation.

### Parameters
- `chord_label`: A string representing a chord label to be parsed (e.g., `'C'`, `'G#:min(*b3,*5)/5'`).
- `reduce_extended_chords`, default `False`: A boolean indicating whether to map the upper voicings of extended chords (such as 9's, 11's, and 13's) to semitone extensions.

### Input
The caller must provide a valid chord label string. The chord label must conform to `mir_eval`'s expected regular expressions and use valid chord types restricted by `chord.QUALITIES`. 

### Output
Returns `unspecified` — A Python list containing exactly four elements representing the split version of the chord label: `[root (str), quality (str), scale_degrees (set), bass (str)]`.

### Valid Call Patterns
```python
import mir_eval

# Default split
chord_parts = mir_eval.chord.split('G#:min(*b3,*5)/5')

# Split with extended chords reduced
reduced_parts = mir_eval.chord.split('C:maj9', reduce_extended_chords=True)
```

### LLM Instruction Prompt
- When parsing chord labels in `mir_eval`, use `mir_eval.chord.split(chord_label)`. Remember that chords lacking both quality and interval information default to a `'maj'` quality. If an interval is specified without a quality, the quality field in the returned list will be an empty string `''`, not `None`. The scale degrees are returned as a Python `set`, not a list.

### Prompt Snippet
```text
Use `mir_eval.chord.split(chord_label, reduce_extended_chords=False)` to parse a chord label into a 4-element list: `[root, quality, scale_degrees, bass]`.
```

### Common Failure Modes
- Passing an invalid chord label that fails the internal regular expression validation or uses a quality not present in `chord.QUALITIES`.
- Assuming the quality field will be `None` instead of an empty string `''` when an interval is specified without a quality (e.g., `'A:(3)/6'`).
- Assuming the scale degrees part is a list; it is a set of strings (e.g., `{'*b3', '*5'}`).
- Attempting to unpack the result into fewer or more than four variables.

### Fix Code Hint
```python
# Ensure the chord label is a valid string before splitting
label = 'A:(3)/6'
root, quality, scale_degrees, bass = mir_eval.chord.split(label)

# Note: quality will be '' (empty string), not None
# Note: scale_degrees will be a set: {'3'}
```

## API Test: `split_key_string`

### Signature
```python
def split_key_string(key)
```
_Source: source/mir_eval/key.py:93_

_Source doc:_ Split a key string (of the form, e.g. ``'C# major'``), into a tuple of ``(key, mode)`` where ``key`` is is an integer representing the semitone distance from C. Parameters ---------- key : str String representing a key. Returns ------- key : int Number of semitones above C. mode : str String representing the mode.

### Goal
Parses a musical key string (e.g., `'C# major'`) into a tuple containing its root pitch class as an integer (semitones above C) and its mode as a string.

### Parameters
- `key`: A string representing a musical key and its mode.

### Input
A string containing a musical key notation (e.g., `'C major'`, `'F# minor'`). As per the project's compatibility rules, the key notation parser also supports unknown or ambiguous keys and modes.

### Output
Returns `unspecified` — A two-element tuple `(key, mode)` where `key` is an `int` representing the number of semitones above C (e.g., C=0, C#=1) and `mode` is a `str` representing the mode (e.g., `'major'`).

### Valid Call Patterns
```python
import mir_eval

# Note: Call form inferred from signature and source documentation
root_pitch, mode = mir_eval.key.split_key_string('C# major')
```

### LLM Instruction Prompt
- When calling `mir_eval.key.split_key_string`, provide a single string representing a musical key. 
- Expect a tuple of `(int, str)` in return, where the integer is the 0-indexed semitone distance from C. 
- Remember that `mir_eval` supports unknown or ambiguous keys and modes, so handle the returned mode string dynamically rather than strictly assuming only `'major'` or `'minor'`.

### Prompt Snippet
```text
Extract the root pitch class and mode from a key annotation string using mir_eval.key.split_key_string.
```

### Common Failure Modes
- Passing a non-string value (such as an integer or `None`), which will cause string parsing exceptions.
- Assuming the returned `key` is a string (like `'C#'`); it is always converted to an integer representing the semitone distance from C.

### Fix Code Hint
```python
# BAD: Passing an unparsed or non-string object
# pitch, mode = mir_eval.key.split_key_string(0)

# GOOD: Passing a properly formatted key string
pitch, mode = mir_eval.key.split_key_string('Eb minor')
```

## API Test: `standard_FPR`

### Signature
```python
def standard_FPR(reference_patterns, estimated_patterns, tol=1e-05)
```
_Source: source/mir_eval/pattern.py:171_

_Source doc:_ Compute the standard F1 Score, Precision and Recall. This metric checks if the prototype patterns of the reference match possible translated patterns in the prototype patterns of the estimations. Since the sizes of these prototypes must be equal, this metric is quite restrictive and it tends to be 0 in most of 2013 MIREX results. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> F, P, R = mir_eval.pattern.standard_FPR(ref_patterns, est_patterns) Parameters ---------- reference_patterns : list The reference patterns using the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format tol : float Tolerance level when comparing reference against estimation. Default parameter is the one found in the original matlab code by Tom Tom Collins used for MIREX 2013. (Default value = 1e-5) Returns ------- f_measure : float The standard F1 Score precision : float The standard Precision recall : float The standard Recall

### Goal
Compute the standard F1 Score, Precision, and Recall for pattern discovery by checking if reference prototype patterns match translated estimated prototype patterns of the exact same size.

### Parameters
- `reference_patterns`: A list of reference patterns, strictly in the parsed format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: A list of estimated patterns in the same parsed format as the reference patterns.
- `tol`, default `1e-05`: A float representing the tolerance level when comparing the reference against the estimation (defaults to the MIREX 2013 standard).

### Input
The caller must provide reference and estimated patterns as lists of parsed pattern data, not as raw file paths. These lists should be generated by reading repository-format text files using `mir_eval.io.load_patterns()`. Note that this metric is highly restrictive: the sizes of the prototype patterns must be exactly equal to register a match.

### Output
Returns `unspecified` — A tuple of three floats `(f_measure, precision, recall)` representing the standard F1 Score, standard Precision, and standard Recall, respectively.

### Valid Call Patterns
```python
import mir_eval

# Inferred from source documentation
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")
f_measure, precision, recall = mir_eval.pattern.standard_FPR(ref_patterns, est_patterns)
```

### LLM Instruction Prompt
- When evaluating pattern discovery with `mir_eval.pattern.standard_FPR`, you MUST first load the pattern text files using `mir_eval.io.load_patterns()`. Do not pass file paths directly to the metric function.
- Be aware that this metric is highly restrictive and requires exact size matches between prototype patterns; it is normal for it to return `0.0` for all three values on many datasets (as seen in MIREX 2013).
- Unpack the return value into exactly three variables: F-measure, Precision, and Recall.

### Prompt Snippet
```text
To evaluate pattern discovery using the standard FPR metric, load both reference and estimated patterns using `mir_eval.io.load_patterns()` and pass the resulting lists to `mir_eval.pattern.standard_FPR(ref_patterns, est_patterns)`. It returns a tuple of three floats: `(f_measure, precision, recall)`.
```

### Common Failure Modes
- **Passing file paths instead of parsed lists:** Providing string paths directly to `standard_FPR` will fail. The inputs must be pre-processed via `mir_eval.io.load_patterns()`.
- **Unexpected zero scores:** Users or tests might assume the metric is broken if it returns `(0.0, 0.0, 0.0)`. This is a known behavior of `standard_FPR` due to its strict requirement that prototype pattern sizes must be exactly equal to match.

### Fix Code Hint
```python
# Incorrect: Passing file paths directly to the metric
# f, p, r = mir_eval.pattern.standard_FPR("reference.txt", "estimated.txt")

# Correct: Parse the files into lists first
import mir_eval
ref_patterns = mir_eval.io.load_patterns("reference.txt")
est_patterns = mir_eval.io.load_patterns("estimated.txt")
f, p, r = mir_eval.pattern.standard_FPR(ref_patterns, est_patterns)
```

## API Test: `tetrads`

### Signature
```python
def tetrads(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:905_

_Source doc:_ Compare chords along tetrad (root & full quality) relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.tetrads(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Compare estimated chord labels against reference chord labels based on tetrad (root and full quality) relationships.

### Parameters
- `reference_labels`: `list` of length `n`. Reference chord labels (strings) to score against.
- `estimated_labels`: `list` of length `n`. Estimated chord labels (strings) to score against.

### Input
Two equal-length lists of chord label strings. The labels must be valid chord strings (validated internally via regular expressions and restricted to valid chord types from `chord.QUALITIES`). Because raw annotations often have mismatched timestamps, the lists must typically be aligned in time using `mir_eval.util.merge_labeled_intervals` before being passed to this function.

### Output
Returns `unspecified` — an `np.ndarray` of shape `(n,)` and `dtype=float` containing comparison scores in the range [0.0, 1.0] for each aligned chord pair.

### Valid Call Patterns
```python
import mir_eval

# Assuming ref_labels and est_labels are already aligned lists of strings
comparisons = mir_eval.chord.tetrads(ref_labels, est_labels)

# To compute a final weighted accuracy score:
# score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chord tetrads, always align the reference and estimated intervals first using `mir_eval.util.merge_labeled_intervals` to produce equal-length label lists. 
- Pass these aligned lists of strings to `mir_eval.chord.tetrads`. 
- To compute a final scalar metric, pass the resulting comparison array and the merged durations to `mir_eval.chord.weighted_accuracy`.
- Ensure chord strings are valid according to `mir_eval`'s regular expressions and `chord.QUALITIES`.

### Prompt Snippet
```text
`mir_eval.chord.tetrads(reference_labels, estimated_labels)` compares aligned chord labels along tetrad relationships. Inputs must be equal-length lists of valid chord strings. Use `mir_eval.util.merge_labeled_intervals` to align intervals before scoring. Returns an array of float scores in [0.0, 1.0].
```

### Common Failure Modes
- Providing unaligned lists of different lengths (e.g., passing raw loaded labels without merging them first).
- Passing invalid chord strings that fail `mir_eval`'s regular expression validation or are not present in `chord.QUALITIES`.
- Passing interval arrays (timestamps) instead of the label lists.

### Fix Code Hint
```python
# Align intervals and labels before calling tetrads
(intervals, ref_labels_aligned, est_labels_aligned) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.tetrads(ref_labels_aligned, est_labels_aligned)
```

## API Test: `tetrads_inv`

### Signature
```python
def tetrads_inv(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:952_

_Source doc:_ Compare chords along tetrad (root, full quality, & bass) relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.tetrads_inv(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Compare estimated and reference chord labels based on their tetrad (root, full quality, and bass) relationships, returning an array of item-wise scores.

### Parameters
- `reference_labels`: A list of length `n` containing the ground-truth reference chord labels (strings) to score against.
- `estimated_labels`: A list of length `n` containing the estimated chord labels (strings) to be evaluated.

### Input
- Both inputs must be lists of string chord labels (e.g., `'C:maj7/3'`, `'N'`, `'X'`).
- The lists must be of identical length `n`.
- The labels are typically obtained by loading `.lab` files via `mir_eval.io.load_labeled_intervals` and must be aligned to a common time grid using `mir_eval.util.merge_labeled_intervals` before being passed to this function.
- Chord strings must be valid according to `mir_eval`'s internal regular expressions and restricted to valid chord types from `chord.QUALITIES`. Unknown chords (`"X"`) and no-chord (`"N"`) are handled but may be marked as not comparable depending on the metric.

### Output
Returns `unspecified` — A 1-dimensional `np.ndarray` of floats with shape `(n,)`. Each element represents the comparison score between the reference and estimated chord at that index, bounded in the range `[0.0, 1.0]`.

### Valid Call Patterns
```python
import mir_eval

# 1. Standard workflow: Load, adjust, merge, and score
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Adjust estimated intervals to match reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# Merge intervals to create a common time grid
(intervals, aligned_ref_labels, aligned_est_labels) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# Compute tetrads_inv scores
comparisons = mir_eval.chord.tetrads_inv(aligned_ref_labels, aligned_est_labels)

# (Optional) Compute weighted accuracy using durations
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chords with `mir_eval.chord.tetrads_inv`, you MUST align the reference and estimated intervals first using `mir_eval.util.merge_labeled_intervals`. Never pass raw, unaligned label lists directly from file loading, as they will likely have mismatched lengths and misaligned time boundaries. Pass only the resulting aligned label lists.

### Prompt Snippet
```text
`mir_eval.chord.tetrads_inv(reference_labels, estimated_labels)` requires two lists of string chord labels of identical length. Always preprocess raw intervals and labels using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals` to ensure the labels correspond to the same segmented time grid before calling this metric.
```

### Common Failure Modes
- **Length Mismatch:** Passing `reference_labels` and `estimated_labels` of different lengths (e.g., directly after loading from files with different numbers of chord events) will cause a failure or meaningless results.
- **Invalid Chord Syntax:** Passing strings that do not conform to standard MIR chord syntax (e.g., failing the internal regex or not existing in `chord.QUALITIES`) will cause validation errors.
- **Passing Intervals:** Accidentally passing the `intervals` array instead of the `labels` list to the function.

### Fix Code Hint
```python
# BAD: Passing unaligned labels directly
# scores = mir_eval.chord.tetrads_inv(ref_labels, est_labels)

# GOOD: Merge intervals first to guarantee identical lengths and aligned segments
intervals, aligned_ref, aligned_est = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
scores = mir_eval.chord.tetrads_inv(aligned_ref, aligned_est)
```

## API Test: `thirds`

### Signature
```python
def thirds(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:715_

_Source doc:_ Compare chords along root & third relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.thirds(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Compare reference and estimated chord labels based on their root and third interval relationships.

### Parameters
- `reference_labels`: A list of length `n` containing the reference (ground truth) chord labels as strings.
- `estimated_labels`: A list of length `n` containing the estimated chord labels as strings to score against the reference.

### Input
Two lists of string chord labels of equal length `n`. The labels must be valid chord strings recognized by `mir_eval`'s regular expressions (restricted to valid chord types from `chord.QUALITIES`, plus 'N' for no chord and 'X' for unknown). Typically, these lists are prepared by loading labeled intervals and merging them using `mir_eval.util.merge_labeled_intervals` so that the reference and estimated labels are perfectly aligned in time.

### Output
Returns `unspecified` — A 1-dimensional NumPy array (`np.ndarray`) of shape `(n,)` and `dtype=float` containing the comparison scores. Each score is in the range [0.0, 1.0].

### Valid Call Patterns
```python
import mir_eval

# Example using pre-aligned label lists
ref_labels = ['C:maj', 'G:maj', 'N', 'X']
est_labels = ['C:maj', 'G:min', 'N', 'N']
comparisons = mir_eval.chord.thirds(ref_labels, est_labels)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.thirds`, ensure that `reference_labels` and `estimated_labels` are lists of strings of the exact same length. 
- The labels must be valid chord strings (e.g., 'C:maj', 'N'). 
- Do not pass raw time intervals to this function; it only accepts the label lists. If evaluating over time, you must first align the reference and estimated intervals using `mir_eval.util.merge_labeled_intervals`.

### Prompt Snippet
```text
To evaluate chord estimations using the root and third relationship metric, use `mir_eval.chord.thirds(reference_labels, estimated_labels)`. Both arguments must be lists of string chord labels of equal length. Ensure intervals are merged and aligned beforehand.
```

### Common Failure Modes
- Providing lists of different lengths (e.g., unaligned reference and estimated labels).
- Passing invalid chord strings that fail `mir_eval`'s regex validation or are not in `chord.QUALITIES`.
- Passing interval arrays (e.g., `[[0.0, 1.0], ...]`) instead of the label lists.

### Fix Code Hint
```python
# WRONG: Passing intervals or unaligned labels
# scores = mir_eval.chord.thirds(ref_intervals, est_intervals)

# CORRECT: Merge intervals first to align labels, then score
(intervals, ref_labels_merged, est_labels_merged) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.thirds(ref_labels_merged, est_labels_merged)
```

## API Test: `thirds_inv`

### Signature
```python
def thirds_inv(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:762_

_Source doc:_ Score chords along root, third, & bass relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.thirds_inv(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Score estimated chord labels against reference chord labels based on their root, third, and bass relationships.

### Parameters
- `reference_labels`: A list of length `n` containing the reference (ground truth) chord labels as strings.
- `estimated_labels`: A list of length `n` containing the estimated chord labels as strings to score against the reference.

### Input
The caller must provide two lists of string chord labels of exactly the same length `n`. Because raw annotation files often contain unaligned time intervals, the labels must first be aligned and merged (typically using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals`) before being passed to this function. The chord strings must be valid according to `mir_eval`'s internal regular expressions and restricted to valid qualities in `chord.QUALITIES`.

### Output
Returns `unspecified` — A 1D numpy array (`np.ndarray`) of shape `(n,)` and `dtype=float` containing the comparison scores for each aligned label pair. Each score is in the range `[0.0, 1.0]`.

### Valid Call Patterns
```python
import mir_eval

# Assuming ref_intervals, ref_labels, est_intervals, est_labels are already loaded
# 1. Adjust intervals to a common time base
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, ref_intervals.min(),
    ref_intervals.max(), mir_eval.chord.NO_CHORD,
    mir_eval.chord.NO_CHORD
)

# 2. Merge into a single set of intervals with aligned labels
intervals, ref_labels_merged, est_labels_merged = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# 3. Compute the thirds_inv comparisons
comparisons = mir_eval.chord.thirds_inv(ref_labels_merged, est_labels_merged)

# 4. (Optional) Compute the final weighted accuracy score
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When evaluating chord metrics using `mir_eval.chord.thirds_inv`, NEVER pass raw, unaligned label lists directly from file loaders.
- ALWAYS align the reference and estimated labels first using `mir_eval.util.adjust_intervals` and `mir_eval.util.merge_labeled_intervals` to ensure both lists have the exact same length `n`.
- `thirds_inv` returns an array of item-wise comparison scores, NOT a single scalar metric. To get the final evaluation score, pass the resulting array and the interval durations to `mir_eval.chord.weighted_accuracy`.
- Be aware that certain chord labels like "X" (unknown) and "N" (no chord) have specific non-comparable behaviors.

### Prompt Snippet
```text
`mir_eval.chord.thirds_inv(reference_labels, estimated_labels)` scores root, third, and bass relationships. Inputs must be lists of strings of equal length `n`, typically pre-aligned using `mir_eval.util.merge_labeled_intervals`. It returns an `(n,)` float numpy array of scores in [0.0, 1.0]. Pass this array to `mir_eval.chord.weighted_accuracy` to compute the final scalar metric.
```

### Common Failure Modes
- **Length Mismatch:** Passing `reference_labels` and `estimated_labels` of different lengths because the user skipped the `merge_labeled_intervals` alignment step.
- **Invalid Chord Syntax:** Passing chord strings that fail `mir_eval`'s strict regular expression validation or use qualities not found in `chord.QUALITIES`.
- **Type Error:** Passing the `intervals` (numpy arrays of floats) instead of the `labels` (lists of strings) to the function.
- **Misinterpreting Output:** Expecting a single float score instead of an array of item-wise comparisons.

### Fix Code Hint
```python
# BAD: Passing unaligned labels directly
# scores = mir_eval.chord.thirds_inv(ref_labels, est_labels)

# GOOD: Align intervals and labels first, then score and weight
intervals, aligned_ref, aligned_est = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
comparisons = mir_eval.chord.thirds_inv(aligned_ref, aligned_est)
durations = mir_eval.util.intervals_to_durations(intervals)
final_score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

## API Test: `three_layer_FPR`

### Signature
```python
def three_layer_FPR(reference_patterns, estimated_patterns)
```
_Source: source/mir_eval/pattern.py:382_

_Source doc:_ Three Layer F1 Score, Precision and Recall. As described by Meridith. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> F, P, R = mir_eval.pattern.three_layer_FPR(ref_patterns, ...                                            est_patterns) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format Returns ------- f_measure : float The three-layer F1 Score precision : float The three-layer Precision recall : float The three-layer Recall

### Goal
Computes the three-layer F1 score, precision, and recall for musical pattern discovery evaluation, as described by Meredith.

### Parameters
- `reference_patterns`: `list` — The ground truth reference patterns, formatted as a list of patterns.
- `estimated_patterns`: `list` — The estimated patterns to evaluate, provided in the exact same format as `reference_patterns`.

### Input
Both inputs must be lists of patterns in memory. Callers should use `mir_eval.io.load_patterns(file_path)` to parse standard repository-format pattern text files into the correct list structures required by this function. Do not pass raw file paths or unparsed strings.

### Output
Returns `unspecified` — A tuple of three `float` values: `(f_measure, precision, recall)`, representing the three-layer F1 Score, three-layer Precision, and three-layer Recall, respectively.

### Valid Call Patterns
```python
import mir_eval

# Example inferred from source documentation
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

f_measure, precision, recall = mir_eval.pattern.three_layer_FPR(
    ref_patterns, 
    est_patterns
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery using `mir_eval.pattern.three_layer_FPR`, always ensure the inputs are lists of patterns parsed by `mir_eval.io.load_patterns()`, not raw file paths or strings. Unpack the result into three variables: F-measure, Precision, and Recall.

### Prompt Snippet
```text
`mir_eval.pattern.three_layer_FPR(reference_patterns, estimated_patterns)` computes Meredith's three-layer F1, Precision, and Recall for pattern discovery. Inputs must be lists returned by `mir_eval.io.load_patterns()`. Returns a tuple of floats: `(f_measure, precision, recall)`.
```

### Common Failure Modes
- Passing file paths (strings or `pathlib.Path`) directly to `three_layer_FPR` instead of parsing them first with `mir_eval.io.load_patterns()`.
- Failing to unpack the returned tuple into three separate float variables, leading to tuple-unpacking `ValueError`s or type errors downstream.

### Fix Code Hint
```python
# WRONG: Passing file paths directly
# F, P, R = mir_eval.pattern.three_layer_FPR("ref.txt", "est.txt")

# RIGHT: Load patterns first using mir_eval.io
import mir_eval

ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
f_measure, precision, recall = mir_eval.pattern.three_layer_FPR(ref_patterns, est_patterns)
```

## API Test: `ticker_notes`

### Signature
```python
def ticker_notes(ax=None)
```
_Source: source/mir_eval/display.py:1077_

_Source doc:_ Set the y-axis of the given axes to MIDI notes Parameters ---------- ax : matplotlib.pyplot.axes The axes handle to apply the ticker. By default, uses the current axes handle.

### Goal
Modifies the y-axis of a matplotlib plot to display formatted MIDI note names (e.g., C4, D#4) instead of raw numerical values.

### Parameters
- `ax`, default `None`: A `matplotlib.pyplot.axes` object representing the axes handle to apply the ticker to. If `None`, it defaults to using the current active axes handle.

### Input
An active matplotlib figure or axes where the y-axis data corresponds to MIDI note numbers. This is typically prepared by calling plotting functions like `mir_eval.display.pitch` or `mir_eval.display.multipitch` with the argument `midi=True`. 

### Output
Returns `unspecified` — modifies the provided or current matplotlib axes in-place and returns `None`.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval
from mir_eval.io import load_labeled_events

plt.figure()
times, freqs = load_labeled_events("data/melody/ref00.txt")

# Plot pitches on a midi scale with note tickers
mir_eval.display.pitch(times, freqs, midi=True)
mir_eval.display.ticker_notes()
fig = plt.gcf()
```

### LLM Instruction Prompt
- When plotting pitch or multipitch data, if the y-axis represents MIDI note numbers, call `mir_eval.display.ticker_notes(ax=None)` to format the y-axis ticks as musical note names. 
- Do not assign a return value, as the function modifies the axes in-place and returns `None`. 
- Ensure matplotlib is configured for headless operation (e.g., using the `Agg` backend) if generating plots in an automated or test environment, as network and audio-device access are prohibited.

### Prompt Snippet
```text
mir_eval.display.ticker_notes(ax=None): Formats the y-axis of a matplotlib plot to show MIDI note names. Call after plotting pitches with midi=True. Modifies axes in-place (returns None).
```

### Common Failure Modes
- Applying the ticker to a plot where the y-axis represents raw frequencies in Hz rather than MIDI note numbers, resulting in completely incorrect note labels.
- Attempting to assign the result of `ticker_notes()` to a variable and using it later (it returns `None`).
- Violating the headless constraint by allowing matplotlib to open an interactive display window during automated testing.

### Fix Code Hint
```python
# Ensure the plot uses the MIDI scale before applying the ticker
mir_eval.display.pitch(times, freqs, midi=True)
# Call ticker_notes without assigning its return value
mir_eval.display.ticker_notes() 
```

## API Test: `ticker_pitch`

### Signature
```python
def ticker_pitch(ax=None)
```
_Source: source/mir_eval/display.py:1095_

_Source doc:_ Set the y-axis of the given axes to MIDI frequencies Parameters ---------- ax : matplotlib.pyplot.axes The axes handle to apply the ticker. By default, uses the current axes handle.

### Goal
Set the y-axis of a matplotlib plot to display musical note names corresponding to MIDI frequencies.

### Parameters
- `ax`, default `None`: A `matplotlib.pyplot.axes` object representing the axes handle to apply the ticker to; if `None`, it defaults to the current active axes handle.

### Input
A matplotlib axes object (either passed explicitly or implicitly via the current active figure) that has been plotted with pitch data on a MIDI scale. This is typically preceded by a call to a display function like `mir_eval.display.pitch(..., midi=True)`. In automated testing environments, the matplotlib backend must be configured for headless execution (e.g., using the `Agg` backend) without network or audio-device access.

### Output
Returns `unspecified` — modifies the provided or current matplotlib axes in place by updating its y-axis formatter to display MIDI note names.

### Valid Call Patterns
```python
import matplotlib.pyplot as plt
import mir_eval

plt.figure()
# Assuming `times` and `freqs` are loaded arrays of pitch data
mir_eval.display.pitch(times, freqs, midi=True)
mir_eval.display.ticker_pitch()
fig = plt.gcf()
```

### LLM Instruction Prompt
- When visualizing pitch or melody data, use `mir_eval.display.ticker_pitch()` to format the y-axis with human-readable musical note names.
- You MUST ensure the plotted data is on a MIDI scale (e.g., by passing `midi=True` to `mir_eval.display.pitch`) before applying this ticker, otherwise the note labels will be incorrect.
- If generating code for tests, you MUST configure matplotlib to run headlessly (e.g., `matplotlib.use('Agg')`) to satisfy environment constraints.

### Prompt Snippet
```text
To format the y-axis of a pitch plot with musical note names, call `mir_eval.display.ticker_pitch()`. Ensure the underlying plot uses a MIDI scale (e.g., `mir_eval.display.pitch(times, freqs, midi=True)`). For test environments, configure matplotlib for headless execution.
```

### Common Failure Modes
- **Mismatched Scales:** Applying `ticker_pitch()` to an axis where the data was plotted in Hertz (Hz) instead of MIDI note numbers. This results in nonsensical note labels because the ticker assumes the y-values are MIDI pitches.
- **Environment Errors:** Failing to set a headless backend (like `Agg`) in CI or test environments, causing matplotlib to crash when attempting to open a display window.

### Fix Code Hint
```python
import matplotlib
matplotlib.use('Agg')  # Required for headless test environments
import matplotlib.pyplot as plt
import mir_eval

plt.figure()
# Ensure midi=True is passed so the y-axis values align with the ticker's expectations
mir_eval.display.pitch(times, freqs, midi=True)
mir_eval.display.ticker_pitch()
```

## API Test: `time_frequency`

### Signature
```python
def time_frequency(gram, frequencies, times, fs, function=np.sin, length=None, n_dec=1, threshold=0.01)
```
_Source: source/mir_eval/sonify.py:64_

_Source doc:_ Reverse synthesis of a time-frequency representation of a signal Parameters ---------- gram : np.ndarray ``gram[n, m]`` is the magnitude of ``frequencies[n]`` from ``times[m]`` to ``times[m + 1]`` Non-positive magnitudes are interpreted as silence. frequencies : np.ndarray array of size ``gram.shape[0]`` denoting the frequency (in Hz) of each row of gram times : np.ndarray, shape= ``(gram.shape[1],)`` or ``(gram.shape[1], 2)`` Either the start time (in seconds) of each column in the gram, or the time interval (in seconds) corresponding to each column. fs : int desired sampling rate of the output signal function : function function to use to synthesize notes, should be 2π-periodic length : int desired number of samples in the output signal, defaults to ``times[-1]*fs`` n_dec : int the number of decimals used to approximate each sonfied frequency. Defaults to 1 decimal place. Higher precision will be slower. threshold : float optimizes synthesis to only occur for frequencies that have a linear magnitude of at least one element in gram above the given threshold. Returns ------- output : np.ndarray synthesized version of the piano roll

### Goal
Performs reverse synthesis of a time-frequency representation (such as a spectrogram or piano roll) into a 1D audio signal for "evaluation by ear".

### Parameters
- `gram`: `np.ndarray` representing the magnitude of frequencies over time. `gram[n, m]` is the magnitude of `frequencies[n]` at the time step corresponding to `times[m]`. Non-positive magnitudes are interpreted as silence.
- `frequencies`: `np.ndarray` of size `gram.shape[0]` denoting the frequency (in Hz) of each row in `gram`.
- `times`: `np.ndarray` of shape `(gram.shape[1],)` or `(gram.shape[1], 2)`. Represents either the start time (in seconds) of each column in the gram, or the `[start, end]` time interval (in seconds) corresponding to each column.
- `fs`: `int` specifying the desired sampling rate of the output audio signal.
- `function`, default `np.sin`: A 2π-periodic function used as the oscillator to synthesize notes.
- `length`, default `None`: `int` specifying the desired number of samples in the output signal. If `None`, defaults to `times[-1] * fs`.
- `n_dec`, default `1`: `int` specifying the number of decimals used to approximate each sonified frequency. Higher precision yields more accurate pitches but will be slower to compute.
- `threshold`, default `0.01`: `float` that optimizes synthesis by only processing frequencies that have a linear magnitude of at least one element in `gram` above this threshold.

### Input
The caller must provide aligned numpy arrays for `gram`, `frequencies`, and `times`. 
- `gram` must be a 2D array.
- `frequencies` must be a 1D array matching the number of rows in `gram`.
- `times` must match the number of columns in `gram` and can be either 1D (start times) or 2D (intervals). Single-interval inputs (e.g., `times` of shape `(1, 2)`) are explicitly supported.
- **Preconditions:** Negative amplitudes in `gram` are not sonified (they are treated as silence). `fs` and `length` (if provided) should be integers.

### Output
Returns `unspecified` — A 1D `np.ndarray` containing the synthesized audio signal (the sonified version of the piano roll or time-frequency representation).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

fs = 8000

# 1. Synthesize a time-frequency representation using 1D start times
signal = mir_eval.sonify.time_frequency(
    np.random.standard_normal((100, 1000)),
    np.arange(1, 101),
    np.linspace(0, 10, 1000),
    fs,
)

# 2. Synthesize with a specific output length
signal_custom_length = mir_eval.sonify.time_frequency(
    np.random.standard_normal((100, 1000)),
    np.arange(1, 101),
    np.linspace(0, 10, 1000),
    fs,
    length=fs * 11,
)

# 3. Synthesize a single interval (e.g., a single note) using 2D intervals
single_note_signal = mir_eval.sonify.time_frequency(
    np.ones((1, 1)),
    np.array([60]),
    np.array([[0, 1]]),
    fs,
)
```

### LLM Instruction Prompt
- Ensure the dimensions of `gram` strictly match `(len(frequencies), len(times))`.
- Pass `times` as either a 1D array of start times or a 2D array of `[start, end]` intervals. Single-interval inputs are valid.
- Remember that negative amplitudes in `gram` are ignored (treated as silence).
- If specifying `length`, ensure it is cast to an integer (e.g., `int(fs * duration)`).
- Do not attempt to pass `**kwargs` directly unless wrapping this function (e.g., `mir_eval.sonify.chroma` and `mir_eval.sonify.chords` pass `**kwargs` through to this function).

### Prompt Snippet
```text
Synthesize the given piano roll `gram` (shape 88x100) into an audio signal using `mir_eval.sonify.time_frequency`. The frequencies are provided in `midi_freqs` (length 88) and the start times in `frame_times` (length 100). Use a sampling rate of 44100 and ensure the output length is exactly 441000 samples.
```

### Common Failure Modes
- **Shape Mismatch:** Providing a `gram` array whose shape does not match `(frequencies.shape[0], times.shape[0])`.
- **Type Errors on Length:** Passing a float to `length` (e.g., `length=fs * 5.5`) instead of an integer, which can cause indexing or array initialization errors internally.
- **Invalid Oscillator Function:** Passing a `function` that is not 2π-periodic, resulting in phase discontinuities or incorrect synthesis.

### Fix Code Hint
```python
# Incorrect: length might be a float, and shapes might be misaligned
# signal = mir_eval.sonify.time_frequency(gram, freqs, times, fs, length=fs * duration)

# Correct: Ensure length is an integer and shapes align
assert gram.shape == (len(freqs), len(times)), "gram shape must match (len(freqs), len(times))"
signal = mir_eval.sonify.time_frequency(
    gram, 
    freqs, 
    times, 
    fs, 
    length=int(fs * duration)
)
```

## API Test: `tmeasure`

### Signature
```python
def tmeasure(reference_intervals_hier, estimated_intervals_hier, transitive=False, window=15.0, frame_size=0.1, beta=1.0)
```
_Source: source/mir_eval/hierarchy.py:466_

_Source doc:_ Compute the tree measures for hierarchical segment annotations. Parameters ---------- reference_intervals_hier : list of ndarray ``reference_intervals_hier[i]`` contains the segment intervals (in seconds) for the ``i`` th layer of the annotations.  Layers are ordered from top to bottom, so that the last list of intervals should be the most specific. estimated_intervals_hier : list of ndarray Like ``reference_intervals_hier`` but for the estimated annotation transitive : bool whether to compute the t-measures using transitivity or not. window : float > 0 size of the window (in seconds).  For each query frame q, result frames are only counted within q +- window. frame_size : float > 0 length (in seconds) of frames.  The frame size cannot be longer than the window. beta : float > 0 beta parameter for the F-measure. Returns ------- t_precision : number [0, 1] T-measure Precision t_recall : number [0, 1] T-measure Recall t_measure : number [0, 1] F-beta measure for ``(t_precision, t_recall)`` Raises ------ ValueError If either of the input hierarchies are inconsistent If the input hierarchies have different time durations If ``frame_size > window`` or ``frame_size <= 0``

### Goal
Compute the tree measures (T-measure precision, recall, and F-measure) for hierarchical segment annotations to evaluate structural music segmentation.

### Parameters
- `reference_intervals_hier`: A list of `np.ndarray`. `reference_intervals_hier[i]` contains the segment intervals (in seconds) for the `i`th layer of the ground truth annotations. Layers must be ordered from top to bottom (the last list of intervals is the most specific/granular).
- `estimated_intervals_hier`: A list of `np.ndarray`. Formatted identically to `reference_intervals_hier`, representing the estimated hierarchical annotations.
- `transitive`, default `False`: A boolean indicating whether to compute the t-measures using transitivity.
- `window`, default `15.0`: A strictly positive float representing the size of the window (in seconds). For each query frame `q`, result frames are only counted within `q ± window`.
- `frame_size`, default `0.1`: A strictly positive float representing the length (in seconds) of frames. Cannot be longer than the `window`.
- `beta`, default `1.0`: A strictly positive float representing the beta parameter for the F-measure calculation.

### Input
The caller must provide two lists of 2D numpy arrays (shape `(n, 2)`), where each array represents a layer of intervals `[start_time, end_time]`. 
Preconditions:
1. Both hierarchies must be consistent (e.g., boundaries should not be missing from one layer to the next).
2. Both the reference and estimated hierarchies must cover the exact same total time duration.
3. `frame_size` must be strictly greater than `0` and less than or equal to `window`.

### Output
Returns `unspecified` — A tuple of three floats `(t_precision, t_recall, t_measure)`, where each value is a number in the range `[0, 1]` representing the T-measure Precision, T-measure Recall, and F-beta measure, respectively.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Define a 2-level reference hierarchy and a 1-level estimate
ref = [
    np.array([[0.0, 30.0]]), 
    np.array([[0.0, 15.0], [15.0, 30.0]])
]
est = [
    np.array([[0.0, 30.0]])
]

# Compute tree measures
t_precision, t_recall, t_measure = mir_eval.hierarchy.tmeasure(
    ref, est, window=15.0, frame_size=0.1
)
```

### LLM Instruction Prompt
- When calling `mir_eval.hierarchy.tmeasure`, ensure that both `reference_intervals_hier` and `estimated_intervals_hier` are lists of `numpy.ndarray` objects, not raw Python lists of lists.
- You must verify that the total time duration (from the start of the first interval to the end of the last interval) is identical for both the reference and the estimate.
- Ensure `frame_size` is strictly positive and does not exceed `window`.
- Expect a tuple of three floats to be returned.

### Prompt Snippet
```text
Use `mir_eval.hierarchy.tmeasure(ref_hier, est_hier)` to evaluate the hierarchical segmentation. Ensure `ref_hier` and `est_hier` are lists of `np.ndarray` and have the exact same total duration. The function returns a tuple: `(t_precision, t_recall, t_measure)`.
```

### Common Failure Modes
- **`ValueError: Input hierarchies have different time durations`**: Occurs if the overall start and end times of the reference and estimated hierarchies do not match exactly.
- **`ValueError: frame_size > window or frame_size <= 0`**: Occurs if the frame size is invalid relative to the window size.
- **`ValueError: Input hierarchies are inconsistent`**: Occurs if the hierarchical structure is malformed.
- **`UserWarning: Segment hierarchy is inconsistent at level X`**: Emitted if there are missing boundaries from one layer to the next (e.g., a child segment crosses a parent segment's boundary).
- **`AttributeError` or `TypeError`**: Occurs if the inputs are passed as standard Python lists instead of lists of `numpy.ndarray`.

### Fix Code Hint
```python
# Convert raw lists to lists of numpy arrays
ref_hier = [np.asarray(layer) for layer in raw_ref_hier]
est_hier = [np.asarray(layer) for layer in raw_est_hier]

# Ensure durations match before calling
if ref_hier[0][-1, 1] != est_hier[0][-1, 1]:
    # Handle duration mismatch (e.g., by cropping or padding)
    pass

t_precision, t_recall, t_measure = mir_eval.hierarchy.tmeasure(
    ref_hier, est_hier, window=15.0, frame_size=0.1
)
```

## API Test: `to_cent_voicing`

### Signature
```python
def to_cent_voicing(ref_time, ref_freq, est_time, est_freq, est_voicing=None, ref_reward=None, base_frequency=10.0, hop=None, kind='linear')
```
_Source: source/mir_eval/melody.py:316_

_Source doc:_ Convert reference and estimated time/frequency (Hz) annotations to sampled frequency (cent)/voicing arrays. A zero frequency indicates "unvoiced". If est_voicing is not provided, a negative frequency indicates: "Predicted as unvoiced, but if it's voiced, this is the frequency estimate". If it is provided, negative frequency values are ignored, and the voicing from est_voicing is directly used. Parameters ---------- ref_time : np.ndarray Time of each reference frequency value ref_freq : np.ndarray Array of reference frequency values est_time : np.ndarray Time of each estimated frequency value est_freq : np.ndarray Array of estimated frequency values est_voicing : np.ndarray Estimate voicing confidence. Default None, which means the voicing is inferred from est_freq: - frames with frequency <= 0.0 are considered "unvoiced" - frames with frequency > 0.0 are considered "voiced" ref_reward : np.ndarray Reference voicing reward. Default None, which means all frames are weighted equally. base_frequency : float Base frequency in Hz for conversion to cents (Default value = 10.) hop : float Hop size, in seconds, to resample, default None which means use ref_time kind : str kind parameter to pass to scipy.interpolate.interp1d. (Default value = 'linear') Returns ------- ref_voicing : np.ndarray Resampled reference voicing array ref_cent : np.ndarray Resampled reference frequency (cent) array est_voicing : np.ndarray Resampled estimated voicing array est_cent : np.ndarray Resampled estimated frequency (cent) array

### Goal
Convert reference and estimated melody time/frequency (Hz) annotations into resampled, aligned frequency (in cents) and boolean voicing arrays for evaluation.

### Parameters
- `ref_time`: `np.ndarray` — Time of each reference frequency value, in seconds.
- `ref_freq`: `np.ndarray` — Array of reference frequency values, in Hz.
- `est_time`: `np.ndarray` — Time of each estimated frequency value, in seconds.
- `est_freq`: `np.ndarray` — Array of estimated frequency values, in Hz.
- `est_voicing`, default `None`: `np.ndarray` — Estimated voicing confidence. If `None`, voicing is inferred from `est_freq` (<= 0.0 is unvoiced, > 0.0 is voiced).
- `ref_reward`, default `None`: `np.ndarray` — Reference voicing reward. If `None`, all frames are weighted equally.
- `base_frequency`, default `10.0`: `float` — Base frequency in Hz used for the conversion to cents.
- `hop`, default `None`: `float` — Hop size, in seconds, to resample the arrays. If `None`, it defaults to using `ref_time` as the time grid.
- `kind`, default `'linear'`: `str` — The interpolation kind parameter to pass to `scipy.interpolate.interp1d`.

### Input
Four 1D numpy arrays representing the time series of the reference and estimated melodies. `ref_time` must match the length of `ref_freq`, and `est_time` must match the length of `est_freq`. Frequencies must be in Hz. 
A frequency of `0.0` indicates an "unvoiced" frame. If `est_voicing` is not provided, negative frequencies in `est_freq` are treated as unvoiced frames that carry a latent pitch estimate (e.g., "Predicted as unvoiced, but if it's voiced, this is the frequency estimate"). If `est_voicing` is provided, negative frequencies are ignored and the explicit voicing array is used.

### Output
Returns `unspecified` — A tuple of four 1D `np.ndarray` objects: `(ref_voicing, ref_cent, est_voicing, est_cent)`. The voicing arrays represent whether a frame is voiced (typically boolean or confidence values), and the cent arrays represent the resampled frequencies converted to cents relative to the `base_frequency`. Note: If the time series does not start at 0.0, a 0.0 frame is automatically prepended to the output arrays.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Load time series from repository-format text files
ref_time, ref_freq = mir_eval.io.load_time_series('reference_melody.txt')
est_time, est_freq = mir_eval.io.load_time_series('estimated_melody.txt')

# Convert to cents and voicing arrays
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

# Using deterministic in-memory arrays
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    np.array([1.0, 2.0]),
    np.array([440.0, 442.0]),
    np.array([1.0, 2.0]),
    np.array([441.0, 443.0])
)
```

### LLM Instruction Prompt
- When evaluating melody extraction, use `mir_eval.melody.to_cent_voicing` to align and convert raw Hz-based time series into the cent and voicing arrays required by lower-level metric functions.
- Do not manually filter out negative frequencies in the estimate before calling this function; `to_cent_voicing` specifically uses negative frequencies to infer latent pitch estimates for unvoiced frames unless an explicit `est_voicing` array is provided.
- Always pass 1D numpy arrays. Use `mir_eval.io.load_time_series` to safely parse standard MIR text files into the required `(time, frequency)` arrays.

### Prompt Snippet
```text
Use `mir_eval.melody.to_cent_voicing(ref_time, ref_freq, est_time, est_freq)` to preprocess the loaded melody annotations. It returns a tuple of `(ref_voicing, ref_cent, est_voicing, est_cent)` which you can then pass to individual metric functions.
```

### Common Failure Modes
- Passing mismatched array lengths (e.g., `ref_time` and `ref_freq` have different shapes).
- Passing an invalid string to `kind` that `scipy.interpolate.interp1d` does not support (e.g., typos like `'liner'`).
- Passing multi-dimensional arrays instead of 1D arrays.
- Stripping negative frequencies from `est_freq` manually, which destroys the latent pitch estimates that `mir_eval` uses for certain continuous pitch metrics.

### Fix Code Hint
```python
# Ensure data is loaded correctly as 1D arrays
ref_time, ref_freq = mir_eval.io.load_time_series(ref_file)
est_time, est_freq = mir_eval.io.load_time_series(est_file)

# Call the function using the mir_eval.melody namespace
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)
```

## API Test: `triads`

### Signature
```python
def triads(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:810_

_Source doc:_ Compare chords along triad (root & quality to #5) relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.triads(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- comparison_scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Compare estimated and reference chord labels based on their triad relationships (evaluating root and quality up to the augmented fifth).

### Parameters
- `reference_labels`: `list` of length `n` — Reference chord labels (strings) to score against.
- `estimated_labels`: `list` of length `n` — Estimated chord labels (strings) to score against.

### Input
Two equal-length lists of string chord labels. The labels must be valid chord strings recognized by `mir_eval`'s regular expressions (e.g., `'C:maj'`, `'N'` for no chord, `'X'` for unknown). Crucially, the labels must be pre-aligned to the same time intervals; you cannot pass raw, unaligned labels directly from file loading.

### Output
Returns `unspecified` — A 1D numpy array (`np.ndarray`) of shape `(n,)` and `dtype=float` containing comparison scores in the range `[0.0, 1.0]`. Each element represents the triad similarity between the reference and estimated chord at that index.

### Valid Call Patterns
```python
import mir_eval

# 1. Direct call with pre-aligned labels (from test suite)
ref_labels = ['C:maj', 'G:maj', 'N']
est_labels = ['C:maj', 'G:min', 'N']
comparisons = mir_eval.chord.triads(ref_labels, est_labels)

# 2. Full pipeline with interval merging (from source doc)
(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Adjust and merge intervals to ensure equal-length, aligned label lists
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, ref_intervals.min(),
    ref_intervals.max(), mir_eval.chord.NO_CHORD,
    mir_eval.chord.NO_CHORD
)
(intervals, ref_labels_merged, est_labels_merged) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# Compute triad comparisons on the merged labels
comparisons = mir_eval.chord.triads(ref_labels_merged, est_labels_merged)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.triads`, ensure that `reference_labels` and `estimated_labels` are equal-length lists of strings that have been pre-aligned to the exact same time intervals. 
- Do not pass raw labels directly from `mir_eval.io.load_labeled_intervals` without first merging them using `mir_eval.util.merge_labeled_intervals`. 
- Note that `"X"` (unknown) and `"N"` (no chord) are not comparable to each other.

### Prompt Snippet
```text
Compare the estimated chords against the reference chords using the triads metric. Ensure you merge the labeled intervals first so the label lists are aligned and of equal length before passing them to `mir_eval.chord.triads`.
```

### Common Failure Modes
- **Length mismatch:** Passing `reference_labels` and `estimated_labels` of different lengths because they were loaded directly from files without interval merging.
- **Invalid chord strings:** Passing chord strings that do not conform to `mir_eval`'s expected regular expressions or `chord.QUALITIES`.
- **Comparing uncomparable labels:** Attempting to compare `"X"` (unknown chord) directly with `"N"` (no chord) without proper handling, as they are not comparable.

### Fix Code Hint
```python
# FIX: Align intervals and labels before scoring to prevent length mismatches
(intervals, ref_labels_merged, est_labels_merged) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
# Now pass the merged, equal-length lists to triads
comparisons = mir_eval.chord.triads(ref_labels_merged, est_labels_merged)
```

## API Test: `triads_inv`

### Signature
```python
def triads_inv(reference_labels, estimated_labels)
```
_Source: source/mir_eval/chord.py:857_

_Source doc:_ Score chords along triad (root, quality to #5, & bass) relationships. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> comparisons = mir_eval.chord.triads_inv(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- reference_labels : list, len=n Reference chord labels to score against. estimated_labels : list, len=n Estimated chord labels to score against. Returns ------- scores : np.ndarray, shape=(n,), dtype=float Comparison scores, in [0.0, 1.0]

### Goal
Score estimated chord labels against reference chord labels based on triad relationships (evaluating the root, quality up to the augmented 5th, and the bass note).

### Parameters
- `reference_labels`: `list` of length `n`. Reference chord labels (strings) to score against.
- `estimated_labels`: `list` of length `n`. Estimated chord labels (strings) to score against.

### Input
Two equal-length lists of string chord labels (e.g., `['C:maj', 'N', 'X']`). 
**Preconditions:** 
1. The lists must be of the exact same length `n`. 
2. The labels must be valid chord strings recognized by `mir_eval`'s regular expressions and restricted to valid chord types from `chord.QUALITIES`. 
3. Because chord annotations typically span different time intervals, the raw labels must first be aligned and merged (e.g., using `mir_eval.util.merge_labeled_intervals`) before being passed to this metric.

### Output
Returns `unspecified` — an `np.ndarray` of shape `(n,)` and dtype `float` containing the comparison scores for each aligned chord pair. Values are in the range `[0.0, 1.0]`.

### Valid Call Patterns
```python
# Standard workflow: load, adjust, merge, compare, and score
import mir_eval

(ref_intervals, ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab')
(est_intervals, est_labels) = mir_eval.io.load_labeled_intervals('est.lab')

# Adjust estimated intervals to match reference boundaries
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, 
    ref_intervals.min(), ref_intervals.max(), 
    mir_eval.chord.NO_CHORD, mir_eval.chord.NO_CHORD
)

# Merge intervals so labels are perfectly aligned in time
(intervals, ref_labels_merged, est_labels_merged) = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)

# Compute the triad inversion comparisons
comparisons = mir_eval.chord.triads_inv(ref_labels_merged, est_labels_merged)

# (Optional) Compute the final weighted accuracy using the segment durations
durations = mir_eval.util.intervals_to_durations(intervals)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.triads_inv`, ensure both `reference_labels` and `estimated_labels` are equal-length lists of strings. Do not pass raw, unaligned labels directly if they correspond to different time intervals; you must use `mir_eval.util.merge_labeled_intervals` first to align the time segments. Ensure chord strings are valid according to `mir_eval`'s chord syntax.

### Prompt Snippet
```text
`mir_eval.chord.triads_inv(reference_labels, estimated_labels)` scores chord triads (root, quality, bass). Inputs must be equal-length lists of valid chord strings. Always align intervals with `mir_eval.util.merge_labeled_intervals` before passing the resulting label lists to this function. Returns a 1D numpy array of float scores in [0.0, 1.0].
```

### Common Failure Modes
- **Length Mismatch:** Passing the raw `ref_labels` and `est_labels` directly from `load_labeled_intervals` without merging them first. This raises an error because the lists will likely have different lengths.
- **Invalid Chord Syntax:** Passing strings that fail `mir_eval`'s internal regular expression validation or contain qualities not in `chord.QUALITIES`.
- **Passing Intervals Instead of Labels:** Accidentally passing the `intervals` array instead of the `labels` list to the function.

### Fix Code Hint
```python
# BAD: Passing unaligned labels directly
# scores = mir_eval.chord.triads_inv(ref_labels, est_labels)

# GOOD: Merge intervals first to guarantee equal-length, time-aligned label lists
intervals, ref_labels_aligned, est_labels_aligned = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
scores = mir_eval.chord.triads_inv(ref_labels_aligned, est_labels_aligned)
```

## API Test: `trim_beats`

### Signature
```python
def trim_beats(beats, min_beat_time=5.0)
```
_Source: source/mir_eval/beat.py:56_

_Source doc:_ Remove beats before min_beat_time.  A common preprocessing step. Parameters ---------- beats : np.ndarray Array of beat times in seconds. min_beat_time : float Minimum beat time to allow (Default value = 5.) Returns ------- beats_trimmed : np.ndarray Trimmed beat array.

### Goal
Remove beat events that occur before a specified minimum time (typically 5.0 seconds) as a standard preprocessing step in beat tracking evaluation.

### Parameters
- `beats`: A 1D `np.ndarray` of beat times in seconds.
- `min_beat_time`, default `5.0`: A `float` representing the minimum beat time to allow. Any beats occurring strictly before this timestamp are removed.

### Input
A 1D numpy array of non-negative float values representing beat timestamps in seconds. In standard workflows, this array is typically loaded from a repository-format text file using `mir_eval.io.load_events()`.

### Output
Returns `unspecified` — A 1D `np.ndarray` containing the trimmed beat times, retaining only the events that occur at or after `min_beat_time`.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Using in-memory numpy arrays (from test suite)
dummy_beats = np.arange(10, dtype=np.float64)
expected_beats = mir_eval.beat.trim_beats(dummy_beats)

# 2. Standard preprocessing workflow (from project context)
reference_beats = mir_eval.io.load_events('reference_beats.txt')
estimated_beats = mir_eval.io.load_events('estimated_beats.txt')

# Crop out beats before 5s, a common preprocessing step
reference_beats = mir_eval.beat.trim_beats(reference_beats)
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)
```

### LLM Instruction Prompt
- When evaluating beat tracking with `mir_eval.beat`, always apply `mir_eval.beat.trim_beats` to BOTH the reference and estimated beat arrays before computing metrics (like `f_measure` or `pscore`). This is a standard MIR preprocessing step to ignore the first 5 seconds of audio.
- Ensure the input is a 1D numpy array of timestamps in seconds, not a 2D array of intervals.

### Prompt Snippet
```text
Before computing beat evaluation metrics, preprocess both the reference and estimated beat arrays using `mir_eval.beat.trim_beats(beats)` to remove the first 5 seconds of events. This ensures standard, reproducible metric evaluations.
```

### Common Failure Modes
- **Asymmetric trimming:** Forgetting to trim *both* the reference and estimated beat arrays, leading to mismatched evaluation windows and heavily penalized metric scores.
- **Incorrect input shape:** Passing a 2D array of intervals (e.g., `[[start, end], ...]`) instead of a 1D array of discrete event timestamps. `trim_beats` expects 1D event arrays.
- **Passing raw file paths:** Passing a string file path directly to `trim_beats`. The file must first be parsed into a numpy array using `mir_eval.io.load_events()`.

### Fix Code Hint
```python
# Incorrect: Evaluating without trimming, or trimming only one array
# f_measure = mir_eval.beat.f_measure(ref_beats, est_beats)

# Correct: Ensure both reference and estimated beats are trimmed before evaluation
ref_beats_trimmed = mir_eval.beat.trim_beats(ref_beats)
est_beats_trimmed = mir_eval.beat.trim_beats(est_beats)
f_measure = mir_eval.beat.f_measure(ref_beats_trimmed, est_beats_trimmed)
```

## API Test: `underseg`

### Signature
```python
def underseg(reference_intervals, estimated_intervals)
```
_Source: source/mir_eval/chord.py:1435_

_Source doc:_ Compute the MIREX 'UnderSeg' score. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> score = mir_eval.chord.underseg(ref_intervals, est_intervals) Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2), dtype=float Reference chord intervals to score against. estimated_intervals : np.ndarray, shape=(m, 2), dtype=float Estimated chord intervals to score against. Returns ------- undersegmentation score : float Comparison score, in [0.0, 1.0], where 1.0 means no undersegmentation.

### Goal
Compute the MIREX 'UnderSeg' score to evaluate the undersegmentation of estimated chord intervals compared to reference ground-truth intervals.

### Parameters
- `reference_intervals`: `np.ndarray, shape=(n, 2), dtype=float` — Reference chord intervals (start and end times in seconds) to score against.
- `estimated_intervals`: `np.ndarray, shape=(m, 2), dtype=float` — Estimated chord intervals (start and end times in seconds) to score against.

### Input
Two 2D numpy arrays of floats, each with exactly two columns representing the start and end times of chord segments. These arrays are typically obtained by parsing repository-format annotation files (like `.lab` files) using `mir_eval.io.load_labeled_intervals(filepath)` and extracting the first element of the returned tuple.

### Output
Returns `unspecified` — A `float` representing the comparison score in the range `[0.0, 1.0]`, where `1.0` means no undersegmentation.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Example using deterministic in-memory arrays (from the test suite)
ref_ivs = np.array([[0.0, 2.0], [2.0, 2.5], [2.5, 3.2]])
est_ivs = np.array([[0.0, 3.0], [3.0, 3.5]])

# Compute the undersegmentation score
score = mir_eval.chord.underseg(ref_ivs, est_ivs)
```

### LLM Instruction Prompt
- When evaluating chord segmentation using `mir_eval.chord.underseg`, ensure both `reference_intervals` and `estimated_intervals` are `(n, 2)` numpy arrays of floats. Do not pass file paths directly to this function; parse them first using `mir_eval.io.load_labeled_intervals`.

### Prompt Snippet
```text
`mir_eval.chord.underseg(reference_intervals, estimated_intervals)` computes the MIREX UnderSeg score (float in [0.0, 1.0], 1.0 = no undersegmentation) given two `(n, 2)` float ndarrays of start/end times.
```

### Common Failure Modes
- Passing raw file paths (strings or `pathlib.Path`) instead of parsed numpy arrays.
- Passing 1D arrays or arrays with a second dimension other than 2 (e.g., `(n, 3)`).
- Passing the full tuple returned by `mir_eval.io.load_labeled_intervals` instead of just the intervals array.

### Fix Code Hint
```python
# FIX: Parse the files to extract the (n, 2) interval arrays before scoring
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('ref.lab')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('est.lab')

# Pass only the interval arrays to underseg
score = mir_eval.chord.underseg(ref_intervals, est_intervals)
```

## API Test: `validate`

### Signature
```python
def validate(reference_sources, estimated_sources)
def validate(ref_intervals, ref_pitches, est_intervals, est_pitches)
def validate(ref_time, ref_freqs, est_time, est_freqs)
def validate(reference_labels, estimated_labels)
def validate(reference_onsets, estimated_onsets)
def validate(reference_timestamps: np.ndarray, estimated_timestamps: np.ndarray)
def validate(reference_key, estimated_key)
def validate(ref_voicing, ref_cent, est_voicing, est_cent)
def validate(reference_patterns, estimated_patterns)
def validate(reference_tempi, reference_weight, estimated_tempi)
def validate(ref_intervals, ref_pitches, ref_velocities, est_intervals, est_pitches, est_velocities)
def validate(reference_beats, estimated_beats)
```
_Source: source/mir_eval/transcription_velocity.py:62  (+11 more definition site/overload)_

_Source doc:_ Check that the input annotations have valid time intervals, pitches, and velocities, and throws helpful errors if not. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) ref_pitches : np.ndarray, shape=(n,) Array of reference pitch values in Hertz ref_velocities : np.ndarray, shape=(n,) Array of MIDI velocities (i.e. between 0 and 127) of reference notes est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times) est_pitches : np.ndarray, shape=(m,) Array of estimated pitch values in Hertz est_velocities : np.ndarray, shape=(m,) Array of MIDI velocities (i.e. between 0 and 127) of estimated notes

### Goal
Checks that the input annotations (such as time intervals, pitches, and velocities) are valid and well-formed for the specific MIR evaluation task, raising helpful errors or warnings if they are not.

### Parameters
- `ref_intervals`: `np.ndarray`, shape=(n,2) — Array of reference notes time intervals (onset and offset times).
- `ref_pitches`: `np.ndarray`, shape=(n,) — Array of reference pitch values in Hertz.
- `ref_velocities`: `np.ndarray`, shape=(n,) — Array of MIDI velocities (i.e. between 0 and 127) of reference notes.
- `est_intervals`: `np.ndarray`, shape=(m,2) — Array of estimated notes time intervals (onset and offset times).
- `est_pitches`: `np.ndarray`, shape=(m,) — Array of estimated pitch values in Hertz.
- `est_velocities`: `np.ndarray`, shape=(m,) — Array of MIDI velocities (i.e. between 0 and 127) of estimated notes.

### Input
The caller must provide reference and estimated annotations corresponding to the specific task submodule being used (e.g., `mir_eval.transcription`, `mir_eval.chord`, `mir_eval.tempo`). 
- For transcription and velocity tasks, inputs must be numpy arrays where intervals are strictly shape `(n, 2)` and `(m, 2)`, and pitches/velocities are 1D arrays of matching lengths `(n,)` and `(m,)`.
- Pitches must be valid frequencies in Hertz.
- Velocities must be valid MIDI velocities (between 0 and 127).
- For chord validation, inputs can be lists of string labels.
- Preconditions: Empty annotations are permitted but will issue a `UserWarning`. In tasks requiring 1:1 correspondence (like chord label comparison), passing arrays/lists of different lengths will raise a `ValueError`.

### Output
Returns `None` (unspecified) — This function acts as an assertion step. It returns nothing on success and raises exceptions (`ValueError`) or issues warnings (`UserWarning`) if the inputs violate task-specific formatting rules.

### Valid Call Patterns
```python
import mir_eval
import numpy as np
import pytest

# 1. Validating transcription inputs (from test suite)
ref_int = np.array([[0, 1]])
ref_pitch = np.array([440.0])
est_pitch = np.array([440.0])
# Validates intervals and pitches for transcription
mir_eval.transcription.validate(ref_int, ref_pitch, ref_int, est_pitch)

# 2. Validating chord inputs (from test suite, demonstrating warnings/errors)
with pytest.warns(UserWarning):
    # Triggers warnings for empty reference and estimated labels
    mir_eval.chord.validate([], [])

with pytest.raises(ValueError):
    # Throws ValueError on different-length labels
    mir_eval.chord.validate([], ["C"])
```

### LLM Instruction Prompt
- When preparing data for `mir_eval` evaluation, use the task-specific `validate` function (e.g., `mir_eval.transcription_velocity.validate` or `mir_eval.chord.validate`) to assert that inputs are correctly shaped and typed.
- Ensure interval arrays are strictly shape `(n, 2)`, and that 1D arrays for pitches and velocities match the length `n` of their corresponding intervals.
- Be prepared to catch `UserWarning` if passing empty annotations, and `ValueError` if passing mismatched lengths to tasks that require aligned arrays.

### Prompt Snippet
```text
Use `mir_eval.<task>.validate(...)` to verify annotation formats before evaluation. Ensure intervals are `(n, 2)` numpy arrays, pitches are in Hz, and velocities are MIDI values (0-127). Handle `UserWarning` for empty arrays and `ValueError` for mismatched lengths.
```

### Common Failure Modes
- **Mismatched Array Lengths:** Passing `ref_intervals` of length `n` but `ref_pitches` or `ref_velocities` of a different length will fail validation.
- **Mismatched Reference/Estimate Lengths (Task Specific):** In tasks like chord evaluation, passing a reference list and an estimate list of different lengths raises a `ValueError`.
- **Empty Annotations:** Passing empty lists or arrays (e.g., `[]`) is technically allowed by some validators but will issue a `UserWarning` ("Estimated labels are empty" / "Reference labels are empty").
- **Invalid Values:** Passing velocities outside the 0-127 MIDI range, or intervals where the onset time is greater than the offset time.

### Fix Code Hint
```python
# Ensure intervals are 2D and match the length of pitches/velocities
if ref_intervals.ndim == 1:
    ref_intervals = ref_intervals.reshape(-1, 2)

assert len(ref_intervals) == len(ref_pitches) == len(ref_velocities), \
    "Reference arrays must have the same number of events."

# Suppress warnings if empty annotations are expected in your pipeline
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    mir_eval.transcription_velocity.validate(
        ref_intervals, ref_pitches, ref_velocities,
        est_intervals, est_pitches, est_velocities
    )
```

## API Test: `validate_boundary`

### Signature
```python
def validate_boundary(reference_intervals, estimated_intervals, trim)
```
_Source: source/mir_eval/segment.py:86_

_Source doc:_ Check that the input annotations to a segment boundary estimation metric (i.e. one that only takes in segment intervals) look like valid segment times, and throws helpful errors if not. Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_intervals` or :func:`mir_eval.io.load_labeled_intervals`. trim : bool will the start and end events be trimmed?

### Goal
Validates that reference and estimated segment intervals are correctly formatted for segment boundary estimation metrics, raising helpful errors if they are invalid.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` representing the ground truth segment start and end times in seconds.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` representing the predicted segment start and end times in seconds.
- `trim`: `bool` indicating whether the start and end events will be trimmed during the metric evaluation.

### Input
The caller must provide two numpy arrays of shape `(N, 2)` containing numeric time intervals (start and end times). These are typically obtained by parsing repository-format annotation files using `mir_eval.io.load_intervals` or `mir_eval.io.load_labeled_intervals`. The `trim` parameter must be a boolean.

### Output
Returns `unspecified` — this function acts as an assertion mechanism and returns nothing (`None`). It is called for its side effect of raising exceptions if the input arrays are malformed, have incorrect dimensions, or contain invalid time intervals.

### Valid Call Patterns
```python
# INFERRED FROM SIGNATURE (No exact test/README example provided)
import mir_eval

# Load intervals from repository-format files
ref_intervals, _ = mir_eval.io.load_labeled_intervals('reference.txt')
est_intervals, _ = mir_eval.io.load_labeled_intervals('estimated.txt')

# Validate the boundaries before computing custom metrics
mir_eval.segment.validate_boundary(ref_intervals, est_intervals, trim=True)
```

### LLM Instruction Prompt
- When implementing reproducible segment boundary evaluations, always call `mir_eval.segment.validate_boundary` before passing intervals to custom metric logic to ensure the inputs are valid `(n, 2)` numpy arrays.
- Do not assign the output of this function to a variable, as it returns `None` and is used purely for its validation side-effects (raising errors on invalid data).
- Ensure inputs are loaded via `mir_eval.io` helpers rather than manually constructed lists to guarantee correct numpy array shapes and types.

### Prompt Snippet
```text
Validate segment boundary annotations using `mir_eval.segment.validate_boundary(reference_intervals, estimated_intervals, trim)`. It takes `(n, 2)` numpy arrays of start/end times (typically loaded via `mir_eval.io.load_intervals`) and a boolean `trim` flag. It returns nothing but raises errors if the intervals are malformed.
```

### Common Failure Modes
- Passing standard Python lists instead of `np.ndarray` objects, which may lack the `.shape` attribute expected by the validation logic.
- Passing 1D arrays of timestamps instead of `(n, 2)` interval arrays. If you have 1D boundary events, they must first be converted to intervals using `mir_eval.util.boundaries_to_intervals`.
- Providing intervals where the start time is greater than or equal to the end time, which violates valid segment time constraints.

### Fix Code Hint
```python
# If you have 1D boundary events, convert them to (n, 2) intervals first
ref_intervals = mir_eval.util.boundaries_to_intervals(ref_boundaries)
est_intervals = mir_eval.util.boundaries_to_intervals(est_boundaries)

# Now they can be safely validated
mir_eval.segment.validate_boundary(ref_intervals, est_intervals, trim=False)
```

## API Test: `validate_chord_label`

### Signature
```python
def validate_chord_label(chord_label)
```
_Source: source/mir_eval/chord.py:348_

_Source doc:_ Test for well-formedness of a chord label. Parameters ---------- chord_label : str Chord label to validate.

### Goal
Test a chord label string for well-formedness according to the library's regular expressions and allowed chord qualities.

### Parameters
- `chord_label`: A string representing the chord label to validate.

### Input
A string representing a chord annotation (e.g., `'C:maj'`, `'N'`). The chord label must conform to the expected syntax, and its quality must not be restricted from the allowed `chord.QUALITIES`.

### Output
Returns `unspecified` — returns `None` if the chord label is well-formed. If the label is invalid, the function raises an exception.

### Valid Call Patterns
```python
import mir_eval

# Validates silently if the label is well-formed
label = "C:maj"
mir_eval.chord.validate_chord_label(label)
```

### LLM Instruction Prompt
- Use `mir_eval.chord.validate_chord_label` to assert the well-formedness of a chord label string before further processing.
- Do not expect a boolean return value; the function returns `None` on success and raises an exception on failure.
- Ensure that generated or parsed chord labels use valid qualities defined in `chord.QUALITIES` and match the library's expected regular expression syntax.

### Prompt Snippet
```text
When parsing chord annotations for `mir_eval`, validate each label using `mir_eval.chord.validate_chord_label(label)`. Since it raises an exception on malformed inputs (such as qualities missing from `chord.QUALITIES`), wrap the call in a try-except block if you need to filter out or log invalid chords from a raw dataset.
```

### Common Failure Modes
- Passing a chord label with an unrecognized or restricted quality that is not permitted by `chord.QUALITIES`.
- Passing a string that fails the internal regular expression parsing (e.g., malformed root notes or invalid bass inversion syntax).
- Passing a non-string argument, which will fail string-specific operations during validation.

### Fix Code Hint
```python
import mir_eval

def filter_valid_chords(chord_labels):
    valid_chords = []
    for label in chord_labels:
        try:
            mir_eval.chord.validate_chord_label(label)
            valid_chords.append(label)
        except Exception as e:
            print(f"Skipping invalid chord '{label}': {e}")
    return valid_chords
```

## API Test: `validate_events`

### Signature
```python
def validate_events(events, max_time=30000.0)
```
_Source: source/mir_eval/util.py:763_

_Source doc:_ Check that a 1-d event location ndarray is well-formed, and raises errors if not. Parameters ---------- events : np.ndarray, shape=(n,) Array of event times max_time : float If an event is found above this time, a ValueError will be raised. (Default value = 30000.)

### Goal
Check that a 1-dimensional numpy array of event times (such as beats or onsets) is well-formed and does not exceed a specified maximum time limit.

### Parameters
- `events`: A 1-dimensional numpy array (`np.ndarray`, shape `(n,)`) representing event times (typically in seconds).
- `max_time`, default `30000.0`: A float representing the maximum allowed time for any event in the array. If any event exceeds this value, a `ValueError` is raised.

### Input
The caller must provide a 1-dimensional numpy array of numerical event times. These are typically loaded from repository-format text files using `mir_eval.io.load_events`. 
Preconditions: 
- The array must be strictly 1-dimensional.
- No value in the array can be greater than `max_time`.

### Output
Returns `None` — The function does not return a value on success; it acts as an assertion and raises an error if the input array is malformed or violates the time constraints.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example 1: Standard validation using default max_time
events = np.array([0.5, 1.2, 2.0, 3.5])
mir_eval.util.validate_events(events)

# Example 2: Validation with a custom maximum time limit
mir_eval.util.validate_events(events, max_time=600.0)
```

### LLM Instruction Prompt
- Use `mir_eval.util.validate_events(events, max_time)` to assert that a 1-D array of event times is well-formed before passing it to custom evaluation logic.
- Do not use this for interval data (shape `(n, 2)`); it strictly requires 1-D event arrays (shape `(n,)`).
- Be prepared to handle a `ValueError` if the events exceed the `max_time` threshold.

### Prompt Snippet
```text
`mir_eval.util.validate_events(events, max_time=30000.0)` verifies that `events` is a 1-D numpy array of event times and raises a ValueError if any event exceeds `max_time`. Use this to validate loaded event annotations (like beats or onsets) before processing.
```

### Common Failure Modes
- **Passing interval data instead of events:** Providing a 2-D array of intervals (e.g., shape `(n, 2)`) will fail because the function strictly expects a 1-D array of shape `(n,)`.
- **Exceeding `max_time`:** Passing an array where one or more event times are greater than `max_time` (default 30000.0) will raise a `ValueError`.
- **Passing unparsed text or lists:** Failing to parse file inputs into a numerical numpy array (e.g., passing raw strings or standard Python lists instead of using `mir_eval.io.load_events` or `np.array`) may cause type or shape validation errors.

### Fix Code Hint
```python
# If you have intervals but need to validate events, you might be using the wrong validation function.
# If you have events that might exceed max_time, filter them first or increase max_time:
valid_events = events[events <= custom_max_time]
mir_eval.util.validate_events(valid_events, max_time=custom_max_time)
```

## API Test: `validate_frequencies`

### Signature
```python
def validate_frequencies(frequencies, max_freq, min_freq, allow_negatives=False)
```
_Source: source/mir_eval/util.py:794_

_Source doc:_ Check that a 1-d frequency ndarray is well-formed, and raises errors if not. Parameters ---------- frequencies : np.ndarray, shape=(n,) Array of frequency values max_freq : float If a frequency is found above this pitch, a ValueError will be raised. (Default value = 5000.) min_freq : float If a frequency is found below this pitch, a ValueError will be raised. (Default value = 20.) allow_negatives : bool Whether or not to allow negative frequency values.

### Goal
Validates that a 1-dimensional NumPy array of frequency values is well-formed and falls within specified pitch boundaries for music information retrieval tasks.

### Parameters
- `frequencies`: A 1-dimensional NumPy array (`np.ndarray`, shape=(n,)) containing numeric frequency values.
- `max_freq`: A `float` representing the maximum allowed frequency. If any frequency in the array is found above this value, a `ValueError` is raised. Note: Despite the source docstring mentioning a default, it is a required positional argument in the signature.
- `min_freq`: A `float` representing the minimum allowed frequency. If any frequency in the array is found below this value, a `ValueError` is raised. Note: Despite the source docstring mentioning a default, it is a required positional argument in the signature.
- `allow_negatives`, default `False`: A `bool` indicating whether or not to allow negative frequency values in the array.

### Input
The caller must provide a 1-dimensional NumPy array of numeric frequency values (e.g., in Hertz). The array must not contain values outside the `[min_freq, max_freq]` range unless `allow_negatives` is `True` and the values are negative. 

### Output
Returns `unspecified` — This function does not return a value (returns `None`). It acts as an assertion, raising a `ValueError` if the input array is malformed or contains out-of-bounds frequencies.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example 1: Standard validation (compiles and passes based on test suite)
freqs = np.array([440.0, 880.0, 1000.0])
mir_eval.util.validate_frequencies(freqs, 5000, 20, allow_negatives=False)

# Example 2: Allowing negative frequencies (compiles and passes based on test suite)
freqs_with_neg = np.array([-440.0, 880.0])
mir_eval.util.validate_frequencies(freqs_with_neg, 5000, 20, allow_negatives=True)
```

### LLM Instruction Prompt
- When validating frequency arrays in `mir_eval`, use `mir_eval.util.validate_frequencies`.
- You MUST explicitly pass `max_freq` and `min_freq` as positional arguments; they do not have default values in the function signature.
- Ensure the input `frequencies` is a 1-dimensional `np.ndarray`.
- Be prepared to handle a `ValueError` if the frequencies exceed the specified bounds or if negative values are present when `allow_negatives=False`.

### Prompt Snippet
```text
Validate 1-D frequency arrays using `mir_eval.util.validate_frequencies(frequencies, max_freq, min_freq)`. You must provide `max_freq` and `min_freq` explicitly. It raises a ValueError for out-of-bounds or unexpected negative values.
```

### Common Failure Modes
- **Missing Positional Arguments**: Failing to provide `max_freq` and `min_freq` because the docstring implies they have defaults, resulting in a `TypeError`.
- **Out of Bounds**: Passing an array with frequencies greater than `max_freq` or less than `min_freq` (when positive), which raises a `ValueError`.
- **Unexpected Negatives**: Passing an array with negative frequencies while `allow_negatives` is left as its default `False`, raising a `ValueError`.
- **Incorrect Array Shape**: Passing a 2-D array or a non-NumPy sequence, which violates the `shape=(n,)` precondition and raises an error.

### Fix Code Hint
```python
import mir_eval
import numpy as np

frequencies = np.array([10.0, 440.0, 6000.0])

# FIX: Clip or filter frequencies before validation, and explicitly provide max/min bounds
frequencies = np.clip(frequencies, 20.0, 5000.0)

try:
    # max_freq (5000) and min_freq (20) are explicitly provided
    mir_eval.util.validate_frequencies(frequencies, 5000, 20, allow_negatives=False)
except ValueError as e:
    print(f"Invalid frequencies detected: {e}")
```

## API Test: `validate_hier_intervals`

### Signature
```python
def validate_hier_intervals(intervals_hier)
```
_Source: source/mir_eval/hierarchy.py:431_

_Source doc:_ Validate a hierarchical segment annotation. Parameters ---------- intervals_hier : ordered list of segmentations Raises ------ ValueError If any segmentation does not span the full duration of the top-level segmentation. If any segmentation does not start at 0.

### Goal
Validate a hierarchical segment annotation to ensure all levels of the hierarchy start at 0 and span the exact same total duration.

### Parameters
- `intervals_hier`: An ordered list of segmentations, where each segmentation is typically an array-like of shape `(n, 2)` containing `[start, end]` times in seconds for that level of the hierarchy.

### Input
The caller must provide a list of interval arrays representing different levels of a hierarchical segmentation. 
**Preconditions:** 
1. The first interval of every segmentation level must start at exactly `0`. 
2. The last interval of every segmentation level must end at the exact same time as the top-level segmentation (the first element in the list).

### Output
Returns `unspecified` — this function acts as an assertion/validation step and returns nothing (`None`). It raises a `ValueError` if the input fails validation.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# INFERRED FROM SIGNATURE (No exact test suite example provided)
top_level = np.array([[0.0, 10.0], [10.0, 20.0]])
sub_level = np.array([[0.0, 5.0], [5.0, 10.0], [10.0, 20.0]])
intervals_hier = [top_level, sub_level]

# Validates silently if preconditions are met
mir_eval.hierarchy.validate_hier_intervals(intervals_hier)
```

### LLM Instruction Prompt
- When calling `mir_eval.hierarchy.validate_hier_intervals`, ensure the input is an ordered list of interval arrays. You MUST verify that every level in the hierarchy starts at `0.0` and that the final end time of every level exactly matches the final end time of the top-level segmentation. Do not pass raw file paths; parse them into interval arrays first.

### Prompt Snippet
```text
`mir_eval.hierarchy.validate_hier_intervals(intervals_hier)` validates hierarchical segmentations. `intervals_hier` is a list of `(n, 2)` interval arrays. Raises ValueError if any level does not start at 0 or does not end at the same time as the top level.
```

### Common Failure Modes
- **Non-zero start time:** Passing a segmentation level where the first event starts at a value greater than `0` (raises `ValueError`).
- **Mismatched durations:** Passing a segmentation level whose final end time differs from the top-level segmentation's final end time, often caused by floating-point inaccuracies or unaligned annotations (raises `ValueError`).

### Fix Code Hint
```python
# Ensure all levels start at 0 and end at the same max duration before validation
if intervals_hier:
    max_duration = intervals_hier[0][-1, 1]
    for level in intervals_hier:
        if level[0, 0] != 0.0:
            level[0, 0] = 0.0
        if level[-1, 1] != max_duration:
            level[-1, 1] = max_duration

mir_eval.hierarchy.validate_hier_intervals(intervals_hier)
```

## API Test: `validate_intervals`

### Signature
```python
def validate_intervals(ref_intervals, est_intervals)
def validate_intervals(intervals)
```
_Source: source/mir_eval/transcription.py:147  (+1 more definition site/overload)_

_Source doc:_ Check that the input annotations to a metric look like time intervals, and throws helpful errors if not. Parameters ---------- ref_intervals : np.ndarray, shape=(n,2) Array of reference notes time intervals (onset and offset times) est_intervals : np.ndarray, shape=(m,2) Array of estimated notes time intervals (onset and offset times)

### Goal
Validates that input annotations to a metric are properly formatted time intervals (onset and offset times), raising helpful errors if they are malformed.

### Parameters
- `ref_intervals`: `np.ndarray, shape=(n,2)` representing reference note time intervals (onset and offset times).
- `est_intervals`: `np.ndarray, shape=(m,2)` representing estimated note time intervals (onset and offset times).

### Input
Numpy arrays of shape `(n, 2)` containing numeric time values (typically in seconds). The first column must represent onset times and the second column must represent offset times. The function supports a single-argument overload for checking one array, or a two-argument signature for checking both reference and estimated intervals simultaneously.

### Output
Returns `unspecified` — The function returns nothing (`None`); it is used purely for its side effect of raising exceptions if the validation fails.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Single-argument overload (from test suite)
intervals = np.array([[0.0, 1.0], [1.0, 2.5]])
mir_eval.util.validate_intervals(intervals)

# 2. Two-argument overload (inferred from signature)
ref_intervals = np.array([[0.0, 1.0], [1.5, 2.0]])
est_intervals = np.array([[0.1, 1.1], [1.4, 2.1]])
mir_eval.transcription.validate_intervals(ref_intervals, est_intervals)
```

### LLM Instruction Prompt
- When writing evaluation code or custom metrics using `mir_eval`, use `validate_intervals` to assert that interval arrays are valid `(n, 2)` numpy arrays of onset and offset times. Use the single-argument overload `mir_eval.util.validate_intervals(intervals)` for individual arrays, or the two-argument signature for reference and estimate pairs. Do not expect a return value.

### Prompt Snippet
```text
mir_eval.util.validate_intervals(intervals) # Validates shape=(n,2) onset/offset time arrays, raises ValueError if malformed
```

### Common Failure Modes
- Passing 1D arrays (e.g., `[0.0, 1.0]`) instead of 2D arrays (e.g., `[[0.0, 1.0]]`).
- Passing arrays with more or fewer than 2 columns (e.g., shape `(n, 3)`).
- Passing standard Python lists instead of `np.ndarray`.
- Passing intervals where the onset time is greater than or equal to the offset time (invalid time intervals).

### Fix Code Hint
```python
# Ensure intervals are 2D numpy arrays of shape (n, 2) before validation
intervals = np.asarray(intervals, dtype=float)
if intervals.ndim == 1 and len(intervals) == 2:
    intervals = intervals.reshape(1, 2)

# Validate
mir_eval.util.validate_intervals(intervals)
```

## API Test: `validate_key`

### Signature
```python
def validate_key(key)
```
_Source: source/mir_eval/key.py:47_

_Source doc:_ Check that a key is well-formatted, e.g. in the form ``'C# major'``. The Key can be 'X' if it is not possible to categorize the Key and mode can be 'other' if it can't be categorized as major or minor. Parameters ---------- key : str Key to verify

### Goal
Validates that a musical key string is well-formatted according to `mir_eval` conventions (e.g., `'C# major'`), supporting unknown keys or ambiguous modes.

### Parameters
- `key`: A string representing the musical key to verify.

### Input
A string containing the key notation. 
**Preconditions:** 
- The string must typically be formatted as a pitch class followed by a space and a mode (e.g., `'C# major'`).
- If the key cannot be categorized at all, the string must be exactly `'X'`.
- If the pitch is known but the mode cannot be categorized as major or minor, the mode must be `'other'` (e.g., `'C other'`).

### Output
Returns `unspecified` (typically `None`). This function acts as a validator and will raise an exception if the provided key string is malformed.

### Valid Call Patterns
```python
import mir_eval

# Note: Call pattern inferred from signature and source documentation
mir_eval.key.validate_key('C# major')

# Validating an unknown key
mir_eval.key.validate_key('X')

# Validating a key with an ambiguous mode
mir_eval.key.validate_key('F other')
```

### LLM Instruction Prompt
- When calling `mir_eval.key.validate_key`, ensure the input is a string formatted strictly as `<Pitch> <mode>` (e.g., `'C# major'`). 
- Use `'X'` if the key is completely unknown.
- Use the mode `'other'` if the key is known but the mode is neither major nor minor. 
- Do not assign the result to a variable, as the function returns `None` and is used purely for its side effect of raising an exception on invalid input.

### Prompt Snippet
```text
Validate that a key string matches mir_eval format requirements:
mir_eval.key.validate_key(key_string)
```

### Common Failure Modes
- Passing a key string without a mode (e.g., `'C#'` instead of `'C# major'`), which will fail validation unless the string is exactly `'X'`.
- Passing an unrecognized mode (modes should be major, minor, or other).
- Passing non-string types (e.g., `None` or custom objects) instead of a formatted string.

### Fix Code Hint
```python
# BAD: Missing mode
# mir_eval.key.validate_key('C#')

# GOOD: Include the mode separated by a space
mir_eval.key.validate_key('C# major')

# GOOD: Use 'X' for completely unknown keys
mir_eval.key.validate_key('X')
```

## API Test: `validate_structure`

### Signature
```python
def validate_structure(reference_intervals, reference_labels, estimated_intervals, estimated_labels)
```
_Source: source/mir_eval/segment.py:121_

_Source doc:_ Check that the input annotations to a structure estimation metric (i.e. one that takes in both segment boundaries and their labels) look like valid segment times and labels, and throws helpful errors if not. Parameters ---------- reference_intervals : np.ndarray, shape=(n, 2) reference segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. reference_labels : list, shape=(n,) reference segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_intervals : np.ndarray, shape=(m, 2) estimated segment intervals, in the format returned by :func:`mir_eval.io.load_labeled_intervals`. estimated_labels : list, shape=(m,) estimated segment labels, in the format returned by :func:`mir_eval.io.load_labeled_intervals`.

### Goal
Validates that reference and estimated segment intervals and labels are correctly formatted for structure estimation metrics, raising helpful errors if they are malformed.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` — The ground truth segment intervals (start and end times in seconds).
- `reference_labels`: `list` of length `n` — The ground truth segment labels corresponding to `reference_intervals`.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` — The predicted segment intervals (start and end times in seconds).
- `estimated_labels`: `list` of length `m` — The predicted segment labels corresponding to `estimated_intervals`.

### Input
The caller must provide in-memory numpy arrays for intervals and Python lists for labels. The number of reference intervals must exactly match the number of reference labels (`n`), and the number of estimated intervals must exactly match the number of estimated labels (`m`). These inputs are typically produced by `mir_eval.io.load_labeled_intervals`.

### Output
Returns `None` — acts purely as an assertion/validation step that raises exceptions if the inputs violate expected shapes, types, or matching lengths.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Note: Call form inferred from signature (not verified by test suite)
ref_intervals = np.array([[0.0, 2.0], [2.0, 5.0]])
ref_labels = ['A', 'B']
est_intervals = np.array([[0.0, 2.5], [2.5, 5.0]])
est_labels = ['A', 'B']

mir_eval.segment.validate_structure(
    ref_intervals, 
    ref_labels, 
    est_intervals, 
    est_labels
)
```

### LLM Instruction Prompt
- When preparing inputs for custom structure estimation metrics in `mir_eval`, always call `mir_eval.segment.validate_structure` first to ensure the intervals are `(n, 2)` numpy arrays and the labels are lists of matching lengths. Do not pass raw file paths to this function; load them first using `mir_eval.io.load_labeled_intervals`.

### Prompt Snippet
```text
Use `mir_eval.segment.validate_structure(ref_intervals, ref_labels, est_intervals, est_labels)` to assert that segment boundaries and labels are valid before computing structure metrics. Intervals must be `(n, 2)` numpy arrays and labels must be lists of length `n`.
```

### Common Failure Modes
- Passing 1D arrays or flat lists for intervals instead of `(n, 2)` shaped numpy arrays.
- Mismatched lengths between an interval array and its corresponding label list (e.g., `len(reference_intervals) != len(reference_labels)`).
- Passing file paths (strings) instead of the loaded array/list data.
- Passing `None` for labels when evaluating a metric that strictly requires structural labels.

### Fix Code Hint
```python
# FIX: Load the data properly using mir_eval.io before validating
ref_intervals, ref_labels = mir_eval.io.load_labeled_intervals('reference.txt')
est_intervals, est_labels = mir_eval.io.load_labeled_intervals('estimated.txt')

# Now validation will succeed
mir_eval.segment.validate_structure(
    ref_intervals, ref_labels, 
    est_intervals, est_labels
)
```

## API Test: `validate_tempi`

### Signature
```python
def validate_tempi(tempi, reference=True)
```
_Source: source/mir_eval/tempo.py:29_

_Source doc:_ Check that there are two non-negative tempi. For a reference value, at least one tempo has to be greater than zero. Parameters ---------- tempi : np.ndarray length-2 array of tempo, in bpm reference : bool indicates a reference value

### Goal
Validates that a given array of two tempo values (in beats per minute) meets the non-negative constraints required for tempo evaluation, ensuring at least one reference tempo is greater than zero.

### Parameters
- `tempi`: A length-2 `np.ndarray` of tempo values, measured in beats per minute (bpm).
- `reference`, default `True`: A boolean flag indicating whether the `tempi` array represents reference (ground truth) values (`True`) or estimated values (`False`).

### Input
The caller must provide a numpy array containing exactly two numerical values. Both values must be non-negative. If `reference=True`, at least one of the two values must be strictly greater than zero. If `reference=False`, the evaluation allows both estimate tempi to be zero.

### Output
Returns `unspecified` — acts as a validation step that raises an exception if the constraints are not met, otherwise returning nothing (implicitly `None`).

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Inferred from signature (no verified test example available)
reference_tempi = np.array([120.0, 60.0])
mir_eval.tempo.validate_tempi(reference_tempi, reference=True)

estimated_tempi = np.array([0.0, 0.0])
mir_eval.tempo.validate_tempi(estimated_tempi, reference=False)
```

### LLM Instruction Prompt
- When calling `mir_eval.tempo.validate_tempi`, ensure `tempi` is a length-2 `np.ndarray` of non-negative numbers.
- Set `reference=True` for ground truth data (which requires at least one tempo > 0) and `reference=False` for estimates (which allows both tempi to be 0).

### Prompt Snippet
```text
Validate tempo arrays using `mir_eval.tempo.validate_tempi(tempi, reference=True)`. The `tempi` input must be a length-2 numpy array of non-negative bpm values. If `reference` is True, at least one value must be > 0. If False, both can be 0.
```

### Common Failure Modes
- Providing an array with a length other than 2 (e.g., a single tempo value instead of a pair).
- Providing negative tempo values.
- Providing a reference array (`reference=True`) where both tempo values are exactly `0.0`.
- Passing standard Python lists instead of `np.ndarray`, which may fail if the internal validation relies on numpy-specific attributes like `.shape`.

### Fix Code Hint
```python
import numpy as np
import mir_eval

def safe_validate_tempi(tempi_list, is_reference):
    # Ensure tempi is a length-2 numpy array
    tempi = np.array(tempi_list, dtype=float)
    if tempi.size != 2:
        raise ValueError("Tempi array must have exactly two elements.")
    
    # Ensure non-negative values
    tempi = np.maximum(tempi, 0.0)
    
    # Validate using mir_eval
    mir_eval.tempo.validate_tempi(tempi, reference=is_reference)
    return tempi
```

## API Test: `validate_voicing`

### Signature
```python
def validate_voicing(ref_voicing, est_voicing)
```
_Source: source/mir_eval/melody.py:77_

_Source doc:_ Check that voicing inputs to a metric are in the correct format. Parameters ---------- ref_voicing : np.ndarray Reference voicing array est_voicing : np.ndarray Estimated voicing array

### Goal
Validates that reference and estimated voicing arrays (which indicate whether a pitch/melody is present at a given time frame) are in the correct `numpy.ndarray` format before computing evaluation metrics.

### Parameters
- `ref_voicing`: `np.ndarray` representing the ground-truth reference voicing array.
- `est_voicing`: `np.ndarray` representing the estimated voicing array.

### Input
Both inputs must be `numpy.ndarray` objects. They typically contain binary or boolean values indicating the presence (voiced) or absence (unvoiced) of a melody or pitch at corresponding time frames. 

### Output
Returns `unspecified` — the function acts as an assertion/validation step (returning `None` on success) and raises an error if the inputs are not valid numpy arrays.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
import numpy as np
import mir_eval.melody

ref_voicing = np.array([1, 1, 0, 1])
est_voicing = np.array([1, 0, 0, 1])

mir_eval.melody.validate_voicing(ref_voicing, est_voicing)
```

### LLM Instruction Prompt
- Always ensure `ref_voicing` and `est_voicing` are `numpy.ndarray` objects before passing them to `validate_voicing`. Do not pass raw Python lists.
- Use this function as a precondition check before computing custom melody metrics to guarantee reproducible and correct metric evaluations.

### Prompt Snippet
```text
mir_eval.melody.validate_voicing(ref_voicing, est_voicing)
```

### Common Failure Modes
- Passing standard Python `list` objects instead of `numpy.ndarray`s, which will fail the format check.
- Passing arrays of mismatched shapes or dimensions (e.g., 2D arrays instead of 1D arrays), which violates the expected metric input format.

### Fix Code Hint
```python
# Convert lists to numpy arrays before validation
ref_voicing_arr = np.array(ref_voicing_list)
est_voicing_arr = np.array(est_voicing_list)
mir_eval.melody.validate_voicing(ref_voicing_arr, est_voicing_arr)
```

## API Test: `vmeasure`

### Signature
```python
def vmeasure(reference_intervals, reference_labels, estimated_intervals, estimated_labels, frame_size=0.1, beta=1.0)
```
_Source: source/mir_eval/segment.py:1100_

### Goal
Computes the V-measure (cross-entropy of cluster assignment normalized by marginal entropy) for frame-clustering segmentation evaluation, which is equivalent to calling `nce(..., marginal=True)`.

### Parameters
- `reference_intervals`: `np.ndarray` of shape `(n, 2)` representing the ground-truth segment start and end times in seconds.
- `reference_labels`: `list` of length `n` containing the ground-truth segment labels.
- `estimated_intervals`: `np.ndarray` of shape `(m, 2)` representing the estimated segment start and end times in seconds.
- `estimated_labels`: `list` of length `m` containing the estimated segment labels.
- `frame_size`, default `0.1`: `float > 0` representing the length (in seconds) of frames used for clustering.
- `beta`, default `1.0`: `float > 0` representing the weight parameter for the F-measure calculation.

### Input
Intervals must be `(n, 2)` numpy arrays and labels must be lists, typically loaded from repository-format files using `mir_eval.io.load_labeled_intervals`. 
**Precondition:** The estimated intervals must be trimmed or padded to match the reference timing exactly. You must use `mir_eval.util.adjust_intervals` to align the start (`t_min`) and end (`t_max`) times of the estimates to the reference before calling this metric.

### Output
Returns `unspecified` — A tuple of three floats: `(V_precision, V_recall, V_F)`.
*   `V_precision`: The over-clustering score (`1 - H(y_est | y_ref) / H(y_est)`). Returns `0` if `|y_est| == 1`.
*   `V_recall`: The under-clustering score (`1 - H(y_ref | y_est) / H(y_ref)`). Returns `0` if `|y_ref| == 1`.
*   `V_F`: The V-measure (the F-measure combining precision and recall using `beta`).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# Example inferred from signature and docstring
ref_intervals = np.array([[0.0, 2.0], [2.0, 5.0]])
ref_labels = ['A', 'B']
est_intervals = np.array([[0.0, 2.5], [2.5, 5.5]])
est_labels = ['A', 'C']

# Precondition: Trim or pad the estimate to match reference timing
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0.0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0.0, t_max=ref_intervals.max()
)

V_precision, V_recall, V_F = mir_eval.segment.vmeasure(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

### LLM Instruction Prompt
- When calling `mir_eval.segment.vmeasure`, you MUST first align the estimated intervals to the reference intervals' time boundaries using `mir_eval.util.adjust_intervals(est_intervals, est_labels, t_min=0, t_max=ref_intervals.max())`.
- Ensure `reference_intervals` and `estimated_intervals` are `(n, 2)` numpy arrays, not 1D arrays or lists.
- Expect a 3-tuple of floats `(V_precision, V_recall, V_F)` as the return value.

### Prompt Snippet
```text
mir_eval.segment.vmeasure requires matching total durations. Always preprocess inputs:
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(ref_intervals, ref_labels, t_min=0)
est_intervals, est_labels = mir_eval.util.adjust_intervals(est_intervals, est_labels, t_min=0, t_max=ref_intervals.max())
v_prec, v_rec, v_f = mir_eval.segment.vmeasure(ref_intervals, ref_labels, est_intervals, est_labels)
```

### Common Failure Modes
- **Mismatched Durations**: Failing to adjust the estimated intervals to match the reference `t_max` will cause the frame clustering to misalign or raise an error.
- **Invalid Interval Shapes**: Passing 1D arrays or lists instead of `(n, 2)` numpy arrays for the interval arguments.
- **Invalid Parameters**: Passing `frame_size <= 0` or `beta <= 0` violates the mathematical requirements of the metric.

### Fix Code Hint
```python
# FIX: Align the estimated intervals to the reference boundaries before evaluation
ref_intervals, ref_labels = mir_eval.util.adjust_intervals(
    ref_intervals, ref_labels, t_min=0
)
est_intervals, est_labels = mir_eval.util.adjust_intervals(
    est_intervals, est_labels, t_min=0, t_max=ref_intervals.max()
)
V_precision, V_recall, V_F = mir_eval.segment.vmeasure(
    ref_intervals, ref_labels, est_intervals, est_labels
)
```

## API Test: `voicing_false_alarm`

### Signature
```python
def voicing_false_alarm(ref_voicing, est_voicing)
```
_Source: source/mir_eval/melody.py:478_

_Source doc:_ Compute the voicing false alarm rates given two voicing indicator sequences, one as reference (truth) and the other as the estimate (prediction).  The sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> false_alarm = mir_eval.melody.voicing_false_alarm(ref_v, est_v) Parameters ---------- ref_voicing : np.ndarray Reference boolean voicing array est_voicing : np.ndarray Estimated boolean voicing array Returns ------- vx_false_alarm : float Voicing false alarm rate, the fraction of unvoiced frames in ref indicated as voiced in est

### Goal
Compute the voicing false alarm rate, representing the fraction of unvoiced frames in a reference melody annotation that are incorrectly predicted as voiced by an estimation system.

### Parameters
- `ref_voicing`: `np.ndarray` — Reference boolean voicing array (ground truth).
- `est_voicing`: `np.ndarray` — Estimated boolean voicing array (prediction).

### Input
Two 1-dimensional numpy arrays of boolean values indicating whether a frame is voiced (`True`) or unvoiced (`False`). Both arrays **must** be of the exact same length and aligned to the same time grid. These are typically obtained by preprocessing raw time-frequency data using `mir_eval.melody.to_cent_voicing`.

### Output
Returns `unspecified` — A `float` representing the voicing false alarm rate. This is calculated as the fraction of unvoiced frames in the reference array that are incorrectly indicated as voiced in the estimated array.

### Valid Call Patterns
```python
import mir_eval

# Example inferred from source documentation
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')

# Precondition: Align time grids and extract boolean voicing arrays
(ref_v, ref_c, est_v, est_c) = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

# Compute the false alarm rate
false_alarm = mir_eval.melody.voicing_false_alarm(ref_v, est_v)
```

### LLM Instruction Prompt
- When evaluating melody extraction, never pass raw frequency arrays or unaligned time series to `voicing_false_alarm`. You must first convert the time and frequency series into aligned boolean voicing arrays of identical length, typically using `mir_eval.melody.to_cent_voicing`.

### Prompt Snippet
```text
`mir_eval.melody.voicing_false_alarm` requires two boolean numpy arrays of the exact same length. Use `mir_eval.melody.to_cent_voicing` to align raw time/frequency series into matching boolean voicing arrays before calling this metric.
```

### Common Failure Modes
- **Mismatched Array Lengths**: Passing `ref_voicing` and `est_voicing` arrays of different lengths, which violates the metric's preconditions.
- **Raw Frequencies Instead of Booleans**: Passing the raw frequency arrays (floats) instead of the boolean voicing indicators.
- **Unaligned Time Grids**: Attempting to compare voicing arrays that were sampled at different time steps without resampling them to a common time grid first.

### Fix Code Hint
```python
# FIX: Use to_cent_voicing to ensure arrays are boolean, aligned, and of equal length
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)
false_alarm_rate = mir_eval.melody.voicing_false_alarm(ref_v, est_v)
```

## API Test: `voicing_measures`

### Signature
```python
def voicing_measures(ref_voicing, est_voicing)
```
_Source: source/mir_eval/melody.py:515_

_Source doc:_ Compute the voicing recall and false alarm rates given two voicing indicator sequences, one as reference (truth) and the other as the estimate (prediction).  The sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> recall, false_alarm = mir_eval.melody.voicing_measures(ref_v, ...                                                        est_v) Parameters ---------- ref_voicing : np.ndarray Reference boolean voicing array est_voicing : np.ndarray Estimated boolean voicing array Returns ------- vx_recall : float Voicing recall rate, the fraction of voiced frames in ref indicated as voiced in est vx_false_alarm : float Voicing false alarm rate, the fraction of unvoiced frames in ref indicated as voiced in est

### Goal
Compute the voicing recall and false alarm rates by comparing an estimated boolean voicing indicator sequence against a reference ground-truth sequence.

### Parameters
- `ref_voicing`: `np.ndarray` — Reference boolean voicing array indicating ground-truth voiced frames.
- `est_voicing`: `np.ndarray` — Estimated boolean voicing array indicating predicted voiced frames.

### Input
Two 1-dimensional numpy arrays of boolean (or binary numeric) values. The sequences **must** be of the exact same length. These arrays are typically obtained by aligning and converting raw time-frequency series using `mir_eval.melody.to_cent_voicing`.

### Output
Returns `unspecified` — A tuple of two floats: `(vx_recall, vx_false_alarm)`. `vx_recall` is the voicing recall rate (the fraction of voiced frames in the reference correctly indicated as voiced in the estimate). `vx_false_alarm` is the voicing false alarm rate (the fraction of unvoiced frames in the reference incorrectly indicated as voiced in the estimate).

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Standard usage (derived from source docstring)
ref_v = np.array([True, True, False, False])
est_v = np.array([True, False, True, False])
recall, false_alarm = mir_eval.melody.voicing_measures(ref_v, est_v)

# 2. Edge case: Empty arrays (from test suite)
# Note: This will issue UserWarnings and return (0.0, 0.0)
score = mir_eval.melody.voicing_measures(np.array([]), np.array([]))

# 3. Edge case: Unvoiced estimate (from test suite)
# Note: This will issue a UserWarning for the estimated melody
recall, false_alarm = mir_eval.melody.voicing_measures(np.ones(10), np.zeros(10))
```

### LLM Instruction Prompt
- Ensure `ref_voicing` and `est_voicing` are 1D numpy arrays of the exact same length.
- Expect a tuple of two floats `(vx_recall, vx_false_alarm)` to be returned.
- Be aware that passing empty arrays or arrays containing no voiced frames (all `False` or `0`) is permitted but will trigger `UserWarning`s (e.g., "Reference melody has no voiced frames.") and will result in a metric score of `0.0`.

### Prompt Snippet
```text
When evaluating melody extraction voicing, use `mir_eval.melody.voicing_measures(ref_voicing, est_voicing)`. Both arguments must be 1D numpy arrays of the same length containing boolean or binary indicators. It returns a tuple of floats `(vx_recall, vx_false_alarm)`. If either array is empty or lacks voiced frames, the function issues a UserWarning and returns 0 for the affected metric.
```

### Common Failure Modes
- **Mismatched Array Lengths**: Passing arrays of different lengths will cause the evaluation to fail. They must be aligned first (e.g., via `mir_eval.melody.to_cent_voicing`).
- **Empty or Unvoiced Arrays**: Passing empty arrays (`np.array([])`) or arrays with only unvoiced frames (`np.zeros(10)`) does not raise an exception, but it triggers multiple `UserWarning`s and returns `0.0` for the metrics.

### Fix Code Hint
```python
# Ensure arrays are the same length before calling the metric
if len(ref_voicing) != len(est_voicing):
    raise ValueError("Voicing arrays must be of the same length.")

import warnings
# Optionally suppress warnings if empty/unvoiced arrays are expected in your pipeline
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    recall, false_alarm = mir_eval.melody.voicing_measures(ref_voicing, est_voicing)
```

## API Test: `voicing_recall`

### Signature
```python
def voicing_recall(ref_voicing, est_voicing)
```
_Source: source/mir_eval/melody.py:441_

_Source doc:_ Compute the voicing recall given two voicing indicator sequences, one as reference (truth) and the other as the estimate (prediction).  The sequences must be of the same length. Examples -------- >>> ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt') >>> est_time, est_freq = mir_eval.io.load_time_series('est.txt') >>> (ref_v, ref_c, ...  est_v, est_c) = mir_eval.melody.to_cent_voicing(ref_time, ...                                                  ref_freq, ...                                                  est_time, ...                                                  est_freq) >>> recall = mir_eval.melody.voicing_recall(ref_v, est_v) Parameters ---------- ref_voicing : np.ndarray Reference boolean voicing array est_voicing : np.ndarray Estimated boolean voicing array Returns ------- vx_recall : float Voicing recall rate, the fraction of voiced frames in ref indicated as voiced in est

### Goal
Compute the voicing recall rate, which is the fraction of voiced frames in a reference melody sequence that are correctly identified as voiced in an estimated sequence.

### Parameters
- `ref_voicing`: Reference boolean voicing array (ground truth).
- `est_voicing`: Estimated boolean voicing array (prediction).

### Input
Both inputs must be 1-dimensional boolean `np.ndarray` objects of the exact same length. Typically, these are generated by preprocessing raw frequency time series using `mir_eval.melody.to_cent_voicing` to align the time grids and extract boolean voicing indicators.

### Output
Returns `unspecified` — A `float` representing the voicing recall rate (the fraction of voiced frames in the reference array that are indicated as voiced in the estimated array).

### Valid Call Patterns
```python
import mir_eval

# Example inferred from the source documentation
ref_time, ref_freq = mir_eval.io.load_time_series('ref.txt')
est_time, est_freq = mir_eval.io.load_time_series('est.txt')

# Preprocess to get equal-length boolean voicing arrays
(ref_v, ref_c, est_v, est_c) = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)

recall = mir_eval.melody.voicing_recall(ref_v, est_v)
```

### LLM Instruction Prompt
- When calling `mir_eval.melody.voicing_recall`, ensure both `ref_voicing` and `est_voicing` are boolean numpy arrays of the exact same length. Do not pass raw frequency arrays directly; use `mir_eval.melody.to_cent_voicing` to align the time grids and extract the boolean voicing indicators first.

### Prompt Snippet
```text
Ensure `ref_voicing` and `est_voicing` are equal-length boolean numpy arrays. Preprocess raw time/frequency series with `mir_eval.melody.to_cent_voicing` before calling `voicing_recall`.
```

### Common Failure Modes
- Passing arrays of different lengths (the sequences must be of the same length).
- Passing raw frequency values (floats) instead of boolean voicing indicators.
- Failing to align the reference and estimated time grids before evaluation.

### Fix Code Hint
```python
# Incorrect: passing raw frequencies or unaligned arrays
# recall = mir_eval.melody.voicing_recall(ref_freq, est_freq)

# Correct: align and convert to boolean voicing arrays first
ref_v, ref_c, est_v, est_c = mir_eval.melody.to_cent_voicing(
    ref_time, ref_freq, est_time, est_freq
)
recall = mir_eval.melody.voicing_recall(ref_v, est_v)
```

## API Test: `weighted_accuracy`

### Signature
```python
def weighted_accuracy(comparisons, weights)
```
_Source: source/mir_eval/chord.py:647_

_Source doc:_ Compute the weighted accuracy of a list of chord comparisons. Examples -------- >>> (ref_intervals, ...  ref_labels) = mir_eval.io.load_labeled_intervals('ref.lab') >>> (est_intervals, ...  est_labels) = mir_eval.io.load_labeled_intervals('est.lab') >>> est_intervals, est_labels = mir_eval.util.adjust_intervals( ...     est_intervals, est_labels, ref_intervals.min(), ...     ref_intervals.max(), mir_eval.chord.NO_CHORD, ...     mir_eval.chord.NO_CHORD) >>> (intervals, ...  ref_labels, ...  est_labels) = mir_eval.util.merge_labeled_intervals( ...      ref_intervals, ref_labels, est_intervals, est_labels) >>> durations = mir_eval.util.intervals_to_durations(intervals) >>> # Here, we're using the "thirds" function to compare labels >>> # but any of the comparison functions would work. >>> comparisons = mir_eval.chord.thirds(ref_labels, est_labels) >>> score = mir_eval.chord.weighted_accuracy(comparisons, durations) Parameters ---------- comparisons : np.ndarray List of chord comparison scores, in [0, 1] or -1 weights : np.ndarray Weights (not necessarily normalized) for each comparison. This can be a list of interval durations Returns ------- score : float Weighted accuracy

### Goal
Compute the weighted accuracy of a list of chord comparison scores, typically weighted by the duration of each evaluated chord segment.

### Parameters
- `comparisons`: `np.ndarray` — A 1D numpy array of chord comparison scores, typically containing values in the range `[0, 1]` or `-1` (where `-1` often denotes comparisons to be ignored).
- `weights`: `np.ndarray` — A 1D numpy array of weights for each comparison. These do not need to be normalized and typically represent the time duration of each evaluated interval.

### Input
Both `comparisons` and `weights` must be 1-dimensional numpy arrays of the exact same length. The `weights` array must contain only non-negative values. Typically, `comparisons` are generated by a chord comparison function (like `mir_eval.chord.thirds`) and `weights` are generated by `mir_eval.util.intervals_to_durations(intervals)`.

### Output
Returns `unspecified` — A `float` representing the final weighted accuracy score.

### Valid Call Patterns
```python
import mir_eval
import numpy as np

# 1. Basic usage with pre-computed arrays (from test suite)
comparisons = np.array([1, 1, 1])
weights = np.array([1, 1, 1])
score = mir_eval.chord.weighted_accuracy(comparisons, weights)

# 2. Full evaluation pipeline (from source documentation)
# Assume ref_intervals, ref_labels, est_intervals, est_labels are loaded
intervals, ref_labels, est_labels = mir_eval.util.merge_labeled_intervals(
    ref_intervals, ref_labels, est_intervals, est_labels
)
durations = mir_eval.util.intervals_to_durations(intervals)
comparisons = mir_eval.chord.thirds(ref_labels, est_labels)
score = mir_eval.chord.weighted_accuracy(comparisons, durations)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.weighted_accuracy`, ensure that `comparisons` and `weights` are numpy arrays of identical length.
- Validate that `weights` contains no negative values before calling, as this will raise a `ValueError`.
- Be aware that if all weights are zero, the function will issue a `UserWarning` ("No nonzero weights, returning 0") and return `0.0`.

### Prompt Snippet
```text
`mir_eval.chord.weighted_accuracy(comparisons, weights)` computes the weighted accuracy of chord scores. Both arguments must be 1D numpy arrays of the same length. `weights` must be non-negative. Mismatched lengths or negative weights raise `ValueError`. All-zero weights return 0.0 and issue a `UserWarning`.
```

### Common Failure Modes
- **Mismatched Array Lengths**: Passing `comparisons` and `weights` arrays of different lengths raises a `ValueError`.
- **Negative Weights**: Passing a `weights` array containing any negative values raises a `ValueError`.
- **Zero Weights Warning**: Passing a `weights` array where all elements are `0` will trigger a `UserWarning` and return a score of `0`.

### Fix Code Hint
```python
# Ensure arrays are numpy arrays of the same length
comparisons = np.asarray(comparisons)
weights = np.asarray(weights)

if len(comparisons) != len(weights):
    raise ValueError("comparisons and weights must have the same length.")

# Ensure no negative weights
if np.any(weights < 0):
    raise ValueError("Weights must be non-negative.")

score = mir_eval.chord.weighted_accuracy(comparisons, weights)
```

## API Test: `weighted_score`

### Signature
```python
def weighted_score(reference_key, estimated_key, allow_descending_fifths=False)
```
_Source: source/mir_eval/key.py:117_

_Source doc:_ Compute a heuristic score which is weighted according to the relationship of the reference and estimated key, as follows: +------------------------------------------------------+-------+ | Relationship                                         | Score | +------------------------------------------------------+-------+ | Same key and mode                                    | 1.0   | +------------------------------------------------------+-------+ | Estimated key is a perfect fifth above reference key | 0.5   | +------------------------------------------------------+-------+ | Relative major/minor (same key signature)            | 0.3   | +------------------------------------------------------+-------+ | Parallel major/minor (same key)                      | 0.2   | +------------------------------------------------------+-------+ | Other                                                | 0.0   | +------------------------------------------------------+-------+ When specifying allow_descending_fifths=True, the scoring changes so that keys that are a perfect fifth above or below the reference key score 0.5 points. This is consistent with the scoring used for MIREX since 2017. In the future, the default behaviour will change to use the new method by default. Examples -------- >>> ref_key = mir_eval.io.load_key('ref.txt') >>> est_key = mir_eval.io.load_key('est.txt') >>> score = mir_eval.key.weighted_score(ref_key, est_key, ...                                     allow_descending_fifths=True) Parameters ---------- reference_key : str Reference key string. estimated_key : str Estimated key string. allow_descending_fifths : bool Specifies whether to score descending fifth errors or not. Returns ------- score : float Score representing how closely related the keys are.

### Goal
Compute a heuristic accuracy score between a reference key and an estimated key based on their harmonic relationship.

### Parameters
- `reference_key`: A string representing the ground-truth reference key (e.g., loaded via `mir_eval.io.load_key`).
- `estimated_key`: A string representing the estimated key to be evaluated.
- `allow_descending_fifths`, default `False`: A boolean specifying whether to score descending fifth errors (a perfect fifth below the reference key) as 0.5 points. Setting this to `True` is consistent with the MIREX scoring standard used since 2017.

### Input
The caller must provide valid key strings for both the reference and the estimate. The key notation supports unknown or ambiguous keys and modes. Typically, these strings are parsed from repository-format text files using `mir_eval.io.load_key()`.

### Output
Returns `unspecified` — A `float` score representing how closely related the keys are. The score is `1.0` for the same key and mode, `0.5` for a perfect fifth above (and below, if `allow_descending_fifths=True`), `0.3` for relative major/minor, `0.2` for parallel major/minor, and `0.0` for any other relationship.

### Valid Call Patterns
```python
import mir_eval

# Example 1: Loading from files and using MIREX 2017+ scoring
ref_key = mir_eval.io.load_key('ref.txt')
est_key = mir_eval.io.load_key('est.txt')
score = mir_eval.key.weighted_score(
    ref_key, 
    est_key, 
    allow_descending_fifths=True
)

# Example 2: Direct string evaluation (from test suite)
good_key = "C major"
score = mir_eval.key.weighted_score(good_key, good_key)
assert score == 1.0
```

### LLM Instruction Prompt
- When evaluating key estimation, always consider setting `allow_descending_fifths=True` to comply with modern (MIREX 2017+) evaluation standards, as the default `False` penalizes descending fifths with a score of 0.0 instead of 0.5.
- Ensure that the inputs are valid key strings; passing malformed or unrecognized key strings will raise a `ValueError`.

### Prompt Snippet
```text
Use `mir_eval.key.weighted_score(ref_key, est_key, allow_descending_fifths=True)` to compute the heuristic key score. Ensure both inputs are valid key strings, as invalid formats will raise a ValueError.
```

### Common Failure Modes
- **`ValueError` on invalid keys**: Passing a malformed or unrecognized key string (e.g., `bad_key` in the test suite) to either `reference_key` or `estimated_key` will raise a `ValueError`.
- **Unexpected 0.0 scores for descending fifths**: Forgetting to pass `allow_descending_fifths=True` will cause estimates that are a perfect fifth below the reference key to receive a score of `0.0` instead of the expected `0.5` used in modern MIR evaluations.

### Fix Code Hint
```python
import mir_eval

ref_key = "C major"
est_key = "F major" # Perfect fifth below

try:
    # Use allow_descending_fifths=True for MIREX 2017+ compatibility
    score = mir_eval.key.weighted_score(
        ref_key, 
        est_key, 
        allow_descending_fifths=True
    )
except ValueError as e:
    print(f"Evaluation failed due to invalid key format: {e}")
```

