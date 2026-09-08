# Deep-dive: `piano_roll`

model: google:gemini-3.1-pro-preview · tokens in=5,241 out=3,120 · wall 30s · 2026-09-08 01:51

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. The API is exposed in `mir_eval.display`, has a detailed public docstring, and is used directly in the repository's test suite to visualize evaluation data.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function requires only standard `numpy` arrays for intervals and pitches/MIDI, and optionally a `matplotlib` axis, all of which can be constructed directly without internal library state.

**L1 PURPOSE**
The `piano_roll` function provides a visualization utility at the end of the evaluation data flow. It takes musical note events (defined by time intervals and pitches) and plots them as a quantized piano roll on a matplotlib axis, which is standard for inspecting transcription or multipitch estimation outputs.

**L2 CONTRACT**
- **Parameters:**
  - `intervals`: `np.ndarray` of shape `(n, 2)`. The start and end times (in seconds) for `n` notes.
  - `pitches`: `np.ndarray` of shape `(n,)`, optional. The frequencies of the notes in Hz.
  - `midi`: `np.ndarray` of shape `(n,)`, optional. The pitches of the notes in MIDI numbers.
  - `ax`: `matplotlib.pyplot.axes`, optional. The axis handle on which to draw. If `None`, a new set of axes is created by underlying helpers.
  - `**kwargs`: Additional keyword arguments (e.g., `label`, `alpha`, `facecolor`) passed through to `labeled_intervals`.
- **Preconditions:** At least one of `pitches` or `midi` MUST be provided. If both are `None`, a `ValueError` is raised.
- **Returns:** `matplotlib.pyplot.axes._subplots.AxesSubplot`. A handle to the matplotlib axes containing the plot.
- **Visibility:** Public.
- **Thread-safety/Laziness:** Not thread-safe if modifying a shared matplotlib figure/axis (standard matplotlib limitation). Eager execution.

**L3 MECHANICS**
1. **Input Validation:** The function checks if `midi` is `None`. If so, it checks if `pitches` is `None` and raises a `ValueError` if both are missing (lines 901-903).
2. **Conversion:** If `midi` is not provided, it converts the `pitches` array from Hz to MIDI numbers using `hz_to_midi(pitches)` (line 905).
3. **Quantization & Delegation:** It defines a valid MIDI scale as integers from 0 to 127 (`scale = np.arange(128)`). It then rounds the `midi` array to the nearest integer, casts it to `int`, and delegates the actual drawing to `labeled_intervals` (lines 907-915). It passes the rounded MIDI numbers as the labels and restricts the allowed labels to `label_set=scale`.
4. **Formatting:** It sets the y-axis minor ticks to appear at every integer (semitone) using `MultipleLocator(1)` (line 918).
5. **Return:** It returns the modified axis `ax`.

**L4 CORRECT MINIMAL USAGE**
```python
import matplotlib
matplotlib.use("Agg")  # Ensure headless execution
import matplotlib.pyplot as plt
import mir_eval
import numpy as np

# 1. Define public inputs
intervals = np.array([[0.0, 0.5], [0.5, 1.0]])
pitches_hz = np.array([440.0, 880.0]) # A4 and A5

# 2. Create axis
fig, ax = plt.subplots()

# 3. Call API
ax_out = mir_eval.display.piano_roll(
    intervals=intervals, 
    pitches=pitches_hz, 
    ax=ax, 
    facecolor="blue", 
    alpha=0.7
)
```

**L5 FAILURE FORENSICS**
- `[fail/runtime] AssertionError: Expected 4 patches for 4 intervals, got 0`
  **Why it failed:** The test asserted that 4 matplotlib patches were drawn, but 0 were found. In `piano_roll`, the drawing is delegated to `labeled_intervals` with `label_set=np.arange(128)` (lines 907-911). If the provided `ref_freqs` contained unvoiced frames (e.g., `0.0` Hz) or frequencies that map to MIDI notes outside the 0-127 range, `hz_to_midi` would produce `-inf` or out-of-bounds values. When rounded and cast to `int`, these labels do not exist in `label_set=np.arange(128)`. Consequently, `labeled_intervals` filters them out and draws nothing. The attempted code likely passed unvoiced or invalid frequencies without filtering them first.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - I inferred that `labeled_intervals` filters out or ignores intervals whose corresponding label is not present in `label_set`. This is highly probable based on the parameter name `label_set=scale` and the specific failure mode (0 patches drawn), but the source code for `labeled_intervals` is not provided in the context.
  - I inferred that the failed test attempt passed 0 Hz or out-of-bounds frequencies, causing the out-of-bounds MIDI quantization.
- **Information needed for certainty:** The source code of `labeled_intervals` to confirm exactly how it handles labels missing from `label_set`.
- **Confidence Scores:**
  - **L2 (Contract): 10/10.** The parameters, types, and return values are explicitly defined in the docstring and enforced in the source code.
  - **L3 (Mechanics): 10/10.** The entire function body is provided, making the step-by-step execution completely transparent.
  - **L4 (Minimal Usage): 10/10.** The function relies only on standard `numpy` and `matplotlib` objects, making the minimal usage snippet robust and self-contained.