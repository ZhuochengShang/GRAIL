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