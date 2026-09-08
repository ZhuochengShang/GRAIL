# Deep-dive: `p_score`

model: google:gemini-3.1-pro-preview · tokens in=5,562 out=3,618 · wall 32s · 2026-09-08 01:43

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. This is a standard, public evaluation metric function in the `mir_eval.beat` module.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function takes standard 1D numpy arrays of floats (timestamps) and primitive types, requiring no complex object initialization.

**L1 PURPOSE**
The `p_score` API computes McKinney's P-score, an evaluation metric for beat tracking algorithms. It sits at the end of the evaluation data flow, taking preprocessed reference (ground truth) and estimated beat timestamps, converting them into impulse trains, and calculating their cross-correlation to return a single float score representing the accuracy of the estimated beats.

**L2 CONTRACT**
- **`reference_beats`**: `np.ndarray` (1D, float). Reference beat times in seconds. Must contain more than 1 element to yield a non-zero score.
- **`estimated_beats`**: `np.ndarray` (1D, float). Query/estimated beat times in seconds. Must contain more than 1 element to yield a non-zero score.
- **`p_score_threshold`**: `float`, default `0.2`. A multiplier used to determine the evaluation window size, calculated as `p_score_threshold * np.median(inter_annotation_intervals)`.
- **Returns**: `float`. McKinney's P-score (correlation). Returns `0.0` if either input array has 1 or fewer elements.
- **Visibility**: Public.
- **Thread-safety/Laziness**: Thread-safe (operates entirely on local variables and pure numpy functions without mutating the input arrays). Eagerly evaluated.

**L3 MECHANICS**
1. **Validation & Edge Cases:** Calls `validate(reference_beats, estimated_beats)` (line 358). It issues a `warnings.warn` if either array has exactly 1 element (lines 361-370). If either array has $\le 1$ element, it immediately returns `0.0` (lines 373-374).
2. **Quantization & Alignment:** Quantizes the beat timestamps to 10ms resolution (sampling rate = 100 Hz) (line 376). It shifts both beat sequences so that the absolute minimum timestamp across both arrays becomes zero (lines 378-380).
3. **Impulse Trains:** Creates zero-initialized arrays (`reference_train`, `estimated_train`) up to the maximum time index and places impulses (`1.0`) at the quantized beat indices (lines 382-391).
4. **Window Calculation:** Calculates the inter-annotation intervals of the reference beats using `np.diff`. The correlation window size is determined by `p_score_threshold * np.median(annotation_intervals)` (lines 394-395).
5. **Cross-Correlation:** Computes the full cross-correlation of the two impulse trains using `np.correlate(..., "full")` (line 397).
6. **Truncation & Scoring:** Truncates the correlation array to only include the valid lags within the calculated window size around the middle lag (lines 399-403). The final P-score is the sum of this truncated correlation divided by the maximum number of beats in either the reference or estimated sequence (lines 405-406).

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
import mir_eval

# Create dummy beat arrays with times > 5s to survive trim_beats if used,
# and with > 1 element to survive the size check in p_score.
ref_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])
est_beats = np.array([5.5, 6.0, 6.5, 7.0, 7.5])

# Compute McKinney's P-score directly
score = mir_eval.beat.p_score(ref_beats, est_beats)
assert score == 1.0
```

**L5 FAILURE FORENSICS**
- **`[fail/runtime] AssertionError: Expected perfect score to be 1.0, got 0.0`**: 
  This failure occurred because the test harness likely generated dummy beat events that were all less than 5 seconds (e.g., `[1.0, 2.0, 3.0]`). When passed through `mir_eval.beat.trim_beats(ref_events)` (as shown in the attempted code), all beats before 5 seconds were removed, resulting in arrays with 0 or 1 elements. At line 373 (`if estimated_beats.size <= 1 or reference_beats.size <= 1:`), `p_score` explicitly returns `0.0` for arrays with 1 or fewer elements. The test expected a perfect score of `1.0` because the original arrays were identical, but got `0.0` because they were decimated by the trimming preprocessing step.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** I inferred that `validate` checks that the inputs are 1D numpy arrays of floats, which is standard for `mir_eval` metrics.
- **INFERENCE:** I inferred that `trim_beats` removes beats before 5 seconds based on the documentation entry stating "crop out early beats (e.g., before 5 seconds)".
- **Confidence Score L2:** 10/10. The types, defaults, and return values are explicitly stated in the docstring and source code.
- **Confidence Score L3:** 10/10. The algorithm is clearly visible line-by-line in the provided source code, relying entirely on standard numpy operations.
- **Confidence Score L4:** 10/10. The minimal usage relies only on standard numpy arrays and the public API, deliberately avoiding the pitfall of short/early beat arrays that caused the recorded failure.