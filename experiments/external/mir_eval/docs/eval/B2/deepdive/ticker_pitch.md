# Deep-dive: `ticker_pitch`

model: google:gemini-3.1-pro-preview · tokens in=4,882 out=3,136 · wall 27s · 2026-09-08 01:54

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
USER-FACING
TESTABLE FROM PUBLIC INPUTS

**L1 PURPOSE**
`ticker_pitch` is a display utility that configures the y-axis of a matplotlib plot to display frequencies in Hertz (Hz) when the underlying plotted data is in MIDI note numbers. It allows users to plot pitch data on a linear MIDI scale (which visually represents logarithmic frequency, matching human pitch perception) while retaining physically meaningful Hz labels on the axis.

**L2 CONTRACT**
- **Receiver**: None (standalone function).
- **Parameters**:
  - `ax` (`matplotlib.pyplot.axes`, optional): The axes handle to apply the ticker to. If `None`, it defaults to the current active axes handle (resolved internally).
- **Returns**: None. The function mutates the provided or current axes in place.
- **Visibility**: Public.

**L3 MECHANICS**
The function resolves the target axes by calling the internal `__get_axes(ax=ax)` (line 1104). It then mutates the y-axis of the resolved axes by setting its major formatter to `FMT_MIDI_HZ` (line 1106). `FMT_MIDI_HZ` is a matplotlib `FuncFormatter` instantiated with the internal `__ticker_midi_hz` function (line 1111). When matplotlib draws the ticks, `__ticker_midi_hz` interprets the y-axis values as MIDI note numbers and converts them to Hz using `midi_to_hz(x)`, formatting the result as a general float string (`"{...:g}"`) (lines 1068-1074).

**L4 CORRECT MINIMAL USAGE**
```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mir_eval.display

fig, ax = plt.subplots()
# Plot pitch data on a MIDI scale (e.g., MIDI 69 = 440 Hz)
ax.plot([0, 1, 2], [69, 70, 71])

# Apply the ticker to format the y-axis labels as Hz (e.g., 440, 466.164, 493.883)
mir_eval.display.ticker_pitch(ax)
```

**L5 FAILURE FORENSICS**
- `[fail/runtime] AssertionError: Expected 'A' in formatted MIDI 69, got 440`: The test author was misled by the provided documentation, which incorrectly claimed `ticker_pitch` formats the y-axis with "human-readable musical note names". In reality, `ticker_pitch` sets the formatter to `FMT_MIDI_HZ` (line 1106), which converts MIDI numbers to Hz (e.g., 69 to 440). The function for note names is actually `ticker_notes` (line 1077).
- `[fail/doc-repair] round 0: rewrite fabricated members: get_major_formatter, use`: The test attempted to extract the formatter using `ax.yaxis.get_m...` (likely `get_major_formatter()`) to test its output directly, but the code snippet was incomplete or used methods the harness considered fabricated/unauthorized.

**L6 SELF-ASSESSMENT**
- INFERENCE: I infer that `midi_to_hz` is imported from `mir_eval.util` or similar, as it is not defined in the provided snippet but used in `__ticker_midi_hz`.
- INFERENCE: I infer that `__get_axes` returns a tuple where the first element is the axes object, based on `ax, _ = __get_axes(ax=ax)`.
- Confidence Score L2: 10/10 - The parameter and return type are explicitly clear from the docstring and source code.
- Confidence Score L3: 10/10 - The delegation to `FMT_MIDI_HZ` and `__ticker_midi_hz` is fully visible in the provided source.
- Confidence Score L4: 10/10 - The minimal usage correctly sets up a headless matplotlib plot, plots MIDI data, and applies the ticker, avoiding the documentation's confusion.