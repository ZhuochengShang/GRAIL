# Deep-dive: `voicing_recall`

model: google:gemini-3.1-pro-preview · tokens in=5,213 out=5,745 · wall 352s · 2026-09-08 02:01

---

```markdown
L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience**: USER-FACING. This is a standard, public evaluation metric in the `mir_eval.melody` module used to evaluate melody extraction algorithms.
- **Testability**: TESTABLE FROM PUBLIC INPUTS. The function can be tested directly by passing standard boolean or numeric `numpy.ndarray` objects, without needing to invoke the problematic `to_cent_voicing` helper.

L1 PURPOSE
This API computes the voicing recall rate for melody extraction evaluation. It calculates the fraction of voiced frames in a reference (ground truth) sequence that are correctly identified as voiced in an estimated (predicted) sequence. It sits at the end of the evaluation data flow, typically consuming boolean arrays generated after raw frequency sequences have been aligned and thresholded.

L2 CONTRACT
- **`ref_voicing`**: `np.ndarray`. The reference voicing indicator sequence. Expected to be a boolean or numeric array where values `> 0` indicate a voiced frame.
- **`est_voicing`**: `np.ndarray`. The estimated voicing indicator sequence. Expected to be a boolean or numeric array of the exact same length as `ref_voicing`.
- **Returns**: `float` (or `int`). The voicing recall rate. Returns `0.0` if either input array is empty. Returns `1` (as an integer) if there are no voiced frames in the reference array.
- **Visibility**: Public.
- **Thread-safety/Laziness**: Thread-safe (pure function with no shared mutable state). Evaluates eagerly.

L3 MECHANICS
- **Empty Check**: The function first checks if either `ref_voicing.size == 0` or `est_voicing.size == 0`. If so, it immediately returns `0.0`.
- **Indicator Construction**: It creates `ref_indicator` by evaluating `ref_voicing > 0` and casting the resulting boolean array to `float`.
- **Zero-Division Prevention**: It checks if the sum of `ref_indicator` is `0` (meaning the reference has no voiced frames). If so, it returns `1` to avoid division by zero.
- **Calculation**: It computes the element-wise product of `est_voicing` and `ref_indicator` (which effectively masks out unvoiced reference frames), sums the result, and divides by the sum of `ref_indicator`.
- **Implicit Constraints**: The function relies on numpy broadcasting rules. It does not explicitly validate that the arrays are the same length; if they are different lengths, numpy will raise a `ValueError` during the multiplication step.

L4 CORRECT MINIMAL USAGE
```python
import numpy as np
import mir_eval

# Construct boolean numpy arrays directly, bypassing to_cent_voicing
ref_voicing = np.array([True, True, False, False])
est_voicing = np.array([True, False, True, False])

# Calculate voicing recall
recall = mir_eval.melody.voicing_recall(ref_voicing, est_voicing)

assert recall == 0.5
```

L5 FAILURE FORENSICS
- **Failed Attempt**: `TypeError: ufunc 'bitwise_and' not supported for the input types...`
- **Why it failed**: The failure did not occur inside `voicing_recall`. The attempted code called `mir_eval.melody.to_cent_voicing(times, ref_freqs, times, est_freqs)` to generate the inputs. The error `ufunc 'bitwise_and'` indicates the use of the `&` operator on incompatible types (like floats). This strongly implies that `to_cent_voicing` (or the harness's generation of the mock `freqs` arrays) executed an unparenthesized bitwise operation on float arrays (e.g., `freqs > 0 & freqs < 1000`, which evaluates as `0 & freqs`). 
- `voicing_recall` itself contains no bitwise operators and explicitly casts its internal indicator to `float`, using standard multiplication (`*`). The fix is to bypass `to_cent_voicing` and pass valid `np.ndarray` objects directly to `voicing_recall`.

L6 SELF-ASSESSMENT
- **INFERENCE**: The exact source of the `bitwise_and` error is inferred to be inside `to_cent_voicing` (or the harness setup), as `voicing_recall` contains no bitwise operators and the traceback points to a failure before `voicing_recall` could successfully execute.
- **INFERENCE**: The behavior of `to_cent_voicing` is inferred from standard MIR evaluation pipelines where it converts raw frequencies to cents and boolean voicing indicators.
- **Confidence in L2 (Contract)**: 10/10. The contract is clearly defined by the docstring and the simple arithmetic in the source.
- **Confidence in L3 (Mechanics)**: 10/10. The mechanics are fully visible in the 6 lines of source code.
- **Confidence in L4 (Minimal Usage)**: 10/10. The minimal usage directly exercises the function with valid numpy arrays, avoiding the problematic helper function entirely.
```