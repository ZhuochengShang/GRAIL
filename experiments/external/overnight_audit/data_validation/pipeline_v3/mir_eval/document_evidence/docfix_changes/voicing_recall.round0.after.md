## API Test: `voicing_recall`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def voicing_recall(ref_voicing, est_voicing)
```
_Source: source/mir_eval/melody.py:441_

### Goal
Compute the voicing recall rate (the fraction of voiced frames in a reference sequence correctly identified as voiced in an estimated sequence). This is a standard user-facing metric included in the main denominator.

### Parameters
- `ref_voicing`: 1D `numpy.ndarray` (boolean or numeric). Reference voicing indicator sequence.
- `est_voicing`: 1D `numpy.ndarray` (boolean or numeric). Estimated voicing indicator sequence.

### Input
Both inputs must be 1-dimensional `numpy.ndarray` objects of the exact same length. They can be constructed directly as boolean or numeric arrays (where values `> 0` indicate a voiced frame). Do not require the use of `mir_eval.melody.to_cent_voicing` to generate inputs; simple numpy arrays are sufficient and preferred for minimal testing.

### Output
A `float` representing the voicing recall rate. Returns `0.0` if either input array is empty. Returns `1` (as an integer) if there are no voiced frames in the reference array to avoid division by zero.

### Valid Call Patterns
```python
import numpy as np
import mir_eval

# Construct boolean or numeric numpy arrays directly, bypassing to_cent_voicing
ref_voicing = np.array([True, True, False, False])
est_voicing = np.array([True, False, True, False])

# Calculate voicing recall
recall = mir_eval.melody.voicing_recall(ref_voicing, est_voicing)
```

### LLM Instruction Prompt
Construct `ref_voicing` and `est_voicing` directly as 1D `numpy.ndarray` objects of the same length. Do not use `mir_eval.melody.to_cent_voicing` to generate inputs for tests. If computing expected values manually in tests, avoid using the bitwise AND operator (`&`) on the arrays, as they may be numeric (float) arrays which will raise a `TypeError`; use multiplication (`*`) or `np.logical_and` instead.

### Prompt Snippet
Pass equal-length 1D `numpy.ndarray` objects directly to `voicing_recall`. Bypass `to_cent_voicing`. Avoid bitwise `&` on arrays; use `*` or `np.logical_and`.

### Common Failure Modes
- Applying the bitwise AND operator (`&`) to voicing arrays (e.g., when manually computing expected values or using outputs from `to_cent_voicing`), which raises a `TypeError: ufunc 'bitwise_and' not supported` if the arrays are numeric (float).
- Unnecessarily using `to_cent_voicing` to generate inputs for simple tests, complicating the test setup and introducing float arrays where booleans were expected.
- Passing arrays of different lengths, which raises a `ValueError` during internal numpy multiplication.

### Fix Code Hint
```python
# Incorrect: Using to_cent_voicing and bitwise & which fails on float arrays
# ref_v, _, est_v, _ = mir_eval.melody.to_cent_voicing(t, ref_f, t, est_f)
# expected = (ref_v & est_v).sum() / ref_v.sum() # TypeError

# Correct: Pass simple numpy arrays directly and use * or np.logical_and for manual checks
ref_voicing = np.array([1.0, 1.0, 0.0, 0.0])
est_voicing = np.array([1.0, 0.0, 1.0, 0.0])
recall = mir_eval.melody.voicing_recall(ref_voicing, est_voicing)
```