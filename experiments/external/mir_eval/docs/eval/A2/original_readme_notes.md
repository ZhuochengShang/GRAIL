### 1. Project purpose
`mir_eval` is a scientific Python library designed for computing common heuristic accuracy scores for various music and audio information retrieval (MIR) and signal processing tasks. It provides a transparent, standardized, and straightforward methodology to evaluate MIR systems, ensuring reproducible metric evaluations for researchers and audio engineers.

### 2. Main workflows
The primary workflow involves loading reference (ground truth) and estimated annotations from repository-format files, optionally applying domain-specific preprocessing (such as cropping or trimming early events), and computing evaluation metrics. Users can either compute an entire suite of task-specific metrics at once using a submodule's `evaluate()` function, or compute individual metrics directly. Secondary workflows include sonifying annotations (synthesizing them into audio for "evaluation by ear") and generating visual plots of the annotations for inspection.

### 3. Important APIs and usage patterns
The library is structured into task-specific submodules and utility submodules. 
Task submodules include: `mir_eval.alignment`, `mir_eval.beat`, `mir_eval.chord`, `mir_eval.hierarchy`, `mir_eval.key`, `mir_eval.melody`, `mir_eval.multipitch`, `mir_eval.onset`, `mir_eval.pattern`, `mir_eval.segment`, `mir_eval.tempo`, `mir_eval.transcription`, and `mir_eval.transcription_velocity`.
Utility submodules include: `mir_eval.io` (for loading data), `mir_eval.util` (shared functionality), `mir_eval.sonify` (audio synthesis), and `mir_eval.display` (plotting).

The standard usage pattern for any task is to call `mir_eval.<task>.evaluate(reference, estimated)`. 
Specific exposed functions and usage patterns include:
*   `mir_eval.beat.trim_beats`
*   `mir_eval.beat.f_measure`
*   `mir_eval.beat.pscore`
*   `mir_eval.chord.encode`
*   `mir_eval.chord.rotate_bitmap_to_root`
*   `mir_eval.chord.scale_degree_to_bitmap`
*   `mir_eval.chord.tetrads`
*   `mir_eval.segment.nce`
*   `mir_eval.melody.resample_melody_series`
*   `mir_eval.display.multipitch`
*   `mir_eval.util.interpolate_intervals`
*   `mir_eval.util.match_events`
*   `mir_eval.util.boundaries_to_intervals`
*   `mir_eval.util.intervals_to_samples`
*   `mir_eval.sonify.time_frequency`
*   `mir_eval.sonify.clicks`
*   `mir_eval.sonify.pitch_contour`
*   `mir_eval.sonify.chroma`
*   `mir_eval.sonify.chords`

### 4. Inputs and file formats
The `mir_eval.io` routines handle loading task-specific data from common file formats (typically text files containing events, intervals, or labels). Functions like `mir_eval.io.load_events` and `mir_eval.io.load_tempo` accept file paths as strings, open file descriptors, or `pathlib.Path` (and generally `os.PathLike`) objects. The I/O methods also support reading comments within these files.

### 5. Outputs and generated artifacts
*   The `evaluate()` function in any task submodule returns a Python dictionary. The keys are the names of the computed metrics, and the values are the corresponding numerical scores achieved.
*   `mir_eval.sonify` functions output synthesized audio arrays (e.g., time-frequency representations, clicks, or pitch contours).
*   `mir_eval.display` functions output matplotlib plots (e.g., labeled interval formatters, multipitch displays).

### 6. Configuration and environment assumptions
*   **Supported runtime:** Python 3.10 (Python 2 support has been explicitly removed).
*   **Core dependencies:** `scipy`, `numpy`, and `decorator`.
*   **Display dependencies:** `matplotlib` (version 2 or higher is supported; side effects are isolated).
*   **Constraints:** Display tests must be kept headless without network or audio-device access.

### 7. Commands and examples

Installation via pip or conda:
```console
python -m pip install mir_eval
conda install -c conda-forge mir_eval
python setup.py install
```

Importing the library:
```python
import mir_eval
```

Evaluating beat tracking (computing all metrics):
```python
reference_beats = mir_eval.io.load_events('reference_beats.txt')
estimated_beats = mir_eval.io.load_events('estimated_beats.txt')
scores = mir_eval.beat.evaluate(reference_beats, estimated_beats)
```

Preprocessing data and computing a specific metric:
```python
reference_beats = mir_eval.io.load_events('reference_beats.txt')
estimated_beats = mir_eval.io.load_events('estimated_beats.txt')
# Crop out beats before 5s, a common preprocessing step
reference_beats = mir_eval.beat.trim_beats(reference_beats)
estimated_beats = mir_eval.beat.trim_beats(estimated_beats)
# Compute the F-measure metric and store it in f_measure
f_measure = mir_eval.beat.f_measure(reference_beats, estimated_beats)
```

### 8. Constraints, preconditions, compatibility rules, and type-selection rules
*   **Deprecations:** `mir_eval.io.load_wav` is deprecated and slated for removal in v0.9. The `mir_eval.separation` module (for source separation evaluation) is also deprecated.
*   **Preconditions for `mir_eval.melody.evaluate`:** Passing incomplete files to this function is permitted but will issue a warning.
*   **Preconditions for `mir_eval.tempo`:** The evaluation allows one reference tempo and both estimate tempi to be zero. Allowing zero tolerance in tempo is permitted but will issue a warning.
*   **Preconditions for `mir_eval.transcription_velocity`:** The evaluation returns 0 when there is no overlap.
*   **Type-selection and arguments:**
    *   `mir_eval.chord.encode` accepts a `STRICT_BASS_INTERVALS` argument.
    *   `mir_eval.chord.scale_degree_to_bitmap` requires `modulo` and `length` arguments.
    *   `mir_eval.segment.nce` accepts a `marginal` flag.
    *   `mir_eval.sonify.pitch_contour` accepts an `amplitude` parameter and supports `nan` values.
    *   `mir_eval.sonify.chroma` and `mir_eval.sonify.chords` pass `**kwargs` directly through to `mir_eval.sonify.time_frequency`.
    *   `mir_eval.util.boundaries_to_intervals` no longer supports a `labels` argument.
    *   `mir_eval.util.interpolate_intervals` supports gaps in the data.
    *   `mir_eval.display.multipitch` casts `n_voiced` to an integer.
    *   `mir_eval.sonify.clicks` casts its inferred length to an integer.
    *   `mir_eval.chord.rotate_bitmap_to_root` uses tuple indexing.
    *   Sparse matrices should use `toarray` instead of `todense`.
    *   `mir_eval.sonify.time_frequency` does not sonify negative amplitudes and supports single-interval inputs.
    *   Chord validation uses regular expressions and restricts invalid chord types from `chord.QUALITIES`.
    *   Key notation supports unknown or ambiguous keys and modes.

### 9. Facts to preserve in the final README
*   If `mir_eval` is used in a research project, users must cite the 2014 ISMIR paper by Colin Raffel et al., "mir_eval: A Transparent Implementation of Common MIR Metrics".
*   The package is distributed via PyPI (`pip install mir_eval`) and conda-forge (`conda install -c conda-forge mir_eval`).

### 10. Missing or weak documentation
*   The exact dictionary keys (metric names) returned by the `evaluate()` functions are not clearly documented in the high-level text.
*   The exact signatures, input types (e.g., numpy array shapes), and return types for most utility and sonification functions (like `sonify.time_frequency`, `util.match_events`) are not clearly documented.
*   The specific format of the text files parsed by `io.load_events` and `io.load_tempo` is not clearly documented.