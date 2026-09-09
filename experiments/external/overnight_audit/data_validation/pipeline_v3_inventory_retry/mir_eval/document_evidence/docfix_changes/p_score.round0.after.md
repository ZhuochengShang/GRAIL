## API Test: `p_score`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def p_score(reference_beats, estimated_beats, p_score_threshold=0.2)
```

### Goal
Compute McKinney's P-score, a standard user-facing evaluation metric based on the autocorrelation of reference and estimated beat times.

### Parameters
- `reference_beats`: `np.ndarray` (1D, float) — Reference beat times in seconds. Must contain more than 1 element to yield a non-zero score.
- `estimated_beats`: `np.ndarray` (1D, float) — Query beat times in seconds. Must contain more than 1 element to yield a non-zero score.
- `p_score_threshold`: `float`, default `0.2` — Multiplier used to determine the evaluation window size, calculated as `p_score_threshold * np.median(inter_annotation_intervals)`.

### Input
1D numpy arrays of floats representing timestamps in seconds. If preprocessing with `mir_eval.beat.trim_beats` (which removes beats before 5 seconds), ensure the input arrays contain at least two beats after the 5-second mark.

### Output
`float` — McKinney's P-score (correlation). Explicitly returns `0.0` if either `reference_beats` or `estimated_beats` contains 1 or fewer elements.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Create dummy beat arrays with times > 5s to survive trim_beats if used,
# and with > 1 element to survive the size check in p_score.
ref_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])
est_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])

# Compute McKinney's P-score directly
score = mir_eval.beat.p_score(ref_beats, est_beats)
```

### LLM Instruction Prompt
To compute McKinney's P-score, pass 1D numpy arrays of float timestamps (in seconds) to `mir_eval.beat.p_score`. If preprocessing with `mir_eval.beat.trim_beats`, ensure the arrays contain at least two beats after 5.0 seconds, as `p_score` explicitly returns `0.0` if either input array has 1 or fewer elements.

### Prompt Snippet
```text
Use mir_eval.beat.p_score(ref_beats, est_beats) to compute McKinney's P-score. Inputs must be 1D numpy arrays of floats. Ensure arrays have >1 element (especially after applying trim_beats, which removes beats < 5s), otherwise the function returns 0.0.
```

### Common Failure Modes
- Providing dummy beat arrays with timestamps under 5 seconds, which are decimated to 1 or 0 elements when passed through `mir_eval.beat.trim_beats`, causing `p_score` to explicitly return `0.0` and failing perfect-score assertions.
- Passing arrays with 1 or fewer elements directly, which triggers a warning and returns `0.0`.
- Passing file paths (strings or `pathlib.Path`) directly to `p_score` instead of loading them into 1D numpy arrays of floats first.

### Fix Code Hint
```python
# BAD: Dummy beats < 5s get removed by trim_beats, leaving <= 1 element and returning 0.0
# ref_beats = np.array([1.0, 2.0, 3.0])
# est_beats = np.array([1.0, 2.0, 3.0])
# score = mir_eval.beat.p_score(mir_eval.beat.trim_beats(ref_beats), mir_eval.beat.trim_beats(est_beats))

# GOOD: Provide at least two beats > 5s to survive trimming and size checks
import numpy as np
import mir_eval

ref_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])
est_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])
score = mir_eval.beat.p_score(mir_eval.beat.trim_beats(ref_beats), mir_eval.beat.trim_beats(est_beats))
```