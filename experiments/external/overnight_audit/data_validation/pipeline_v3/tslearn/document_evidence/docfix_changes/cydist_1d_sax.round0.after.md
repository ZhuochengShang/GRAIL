## API Test: `cydist_1d_sax`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```

### Goal
Compute the distance between two 1d-SAX representations of time series. This is an ADVANCED/LOW-LEVEL Numba JIT-compiled backend helper function. It is not intended for standard end-user workflows and should be excluded from main user-facing benchmark denominators.

### Parameters
- `sax1`: array-like, shape `(sz, 2 * d)`. 1d-SAX symbols for the first time series. **Must be an integer type** (e.g., `np.int64`), overriding the incorrect official docstring.
- `sax2`: array-like, shape `(sz, 2 * d)`. 1d-SAX symbols for the second time series. **Must be an integer type**.
- `breakpoints_avg_middle_`: array-like, 1D, `float64`. Middle values of bins for segment averages.
- `breakpoints_slope_middle_`: array-like, 1D, `float64`. Middle values of bins for segment slopes.
- `original_size`: int. Length of the original time series.

### Input
The caller must explicitly construct low-level 1d-SAX symbolic representations (`sax1`, `sax2`) as 2D NumPy arrays of shape `(sz, 2 * d)`. Crucially, these arrays must contain integers (e.g., `np.int64`), not floats, because they are used directly as array indices to look up breakpoints. The breakpoint arrays must be 1D `float64` arrays with enough elements to be indexed by the maximum integer symbol present in `sax1` and `sax2`.

### Output
Returns `float64` — A scalar float representing the 1d-SAX distance.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import cydist_1d_sax

sz = 3
d = 1
# sax1 and sax2 must be integers because they are used as indices
sax1 = np.zeros((sz, 2 * d), dtype=np.int64)
sax2 = np.ones((sz, 2 * d), dtype=np.int64)

breakpoints_avg_middle = np.array([-0.5, 0.5], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

original_size = 15

dist_zero = cydist_1d_sax(
    sax1, 
    sax1, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)

dist_pos = cydist_1d_sax(
    sax1, 
    sax2, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)

assert dist_zero == 0.0
assert dist_pos > 0.0
print(f"__CHECK__ cydist_1d_sax {dist_zero} {dist_pos:.4f}")
```

### LLM Instruction Prompt
When calling `tslearn.metrics.cysax.cydist_1d_sax`, ignore the official docstring's claim that `sax1` and `sax2` should be `float64`. They MUST be integer arrays (e.g., `np.int64`) because Numba uses them as indices. Ensure breakpoint arrays are 1D floats and large enough to accommodate the maximum integer index in the SAX arrays.

### Prompt Snippet
```text
Use `tslearn.metrics.cysax.cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)` for low-level 1d-SAX distance. `sax1` and `sax2` MUST be `np.int64` arrays of shape `(sz, 2 * d)`, not floats, to avoid Numba TypingErrors during index lookups.
```

### Common Failure Modes
- **Numba `TypingError` (Failed in nopython mode pipeline):** Occurs if `sax1` or `sax2` are created as `float64` or `float32` (as incorrectly suggested by the official docstring). Numba strictly forbids indexing arrays with floating-point numbers.
- **IndexError / Out of Bounds:** Occurs if the integer symbols in `sax1` or `sax2` exceed the length of the provided 1D breakpoint arrays.
- **Misunderstanding API Scope:** Attempting to pass raw time-series data to this ADVANCED/LOW-LEVEL internal helper instead of pre-computed integer symbolic representations.

### Fix Code Hint
```python
# WRONG: Following the incorrect docstring causes a Numba TypingError
sax1 = np.zeros((sz, 2 * d), dtype=np.float64)
sax2 = np.ones((sz, 2 * d), dtype=np.float64)

# CORRECT: Use integers because the values are used as array indices
sax1 = np.zeros((sz, 2 * d), dtype=np.int64)
sax2 = np.ones((sz, 2 * d), dtype=np.int64)
```