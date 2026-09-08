## API Test: `cydist_1d_sax`

### Signature
```python
def cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:135_

_Source doc:_ Compute distance between 1d-SAX representations as defined in [1]_. Parameters ---------- sax1 : array-like, shape=(sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) 1d-SAX representation of a time series. sax2 : array-like, shape=(sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) 1d-SAX representation of another time series. breakpoints_avg_middle_ : array-like, ndim=1, dtype=float64 breakpoints_slope_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dist_1d_sax : float64 1d-SAX distance. Notes ----- Unlike SAX distance, 1d-SAX distance does not lower bound Euclidean distance between original time series. References ---------- .. [1] S. Malinowski, T. Guyet, R. Quiniou, R. Tavenard. 1d-SAX: a Novel Symbolic Representation for Time Series. IDA 2013.

### Goal
Compute the distance between two 1d-SAX (1-dimensional Symbolic Aggregate approXimation) representations of time series using a low-level Cython backend helper.

### Parameters
- `sax1`: array-like, shape=(sz, 2 * d). The 1d-SAX representation of the first time series.
- `sax2`: array-like, shape=(sz, 2 * d). The 1d-SAX representation of the second time series.
- `breakpoints_avg_middle_`: array-like, ndim=1. The middle values of the breakpoints for the average component.
- `breakpoints_slope_middle_`: array-like, ndim=1. The middle values of the breakpoints for the slope component.
- `original_size`: int. The length of the original time series before it was transformed into the 1d-SAX representation.

### Input
The caller must provide pre-computed 1d-SAX representations (`sax1` and `sax2`) as 2D NumPy arrays of shape `(sz, 2 * d)`, where `sz` is the number of segments and `d` is the dimensionality. The breakpoint arrays must be 1D NumPy arrays of type `float64`. The `original_size` must be an integer. Note that data types are platform-dependent (e.g., `float64` and `int64` on Linux/macOS, `float32` and `int32` on Windows), but standard NumPy arrays will typically be cast appropriately by Cython.

### Output
Returns `float64` — A scalar float representing the 1d-SAX distance between the two representations. Note that unlike standard SAX distance, this metric does not lower-bound the Euclidean distance between the original time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import cydist_1d_sax

# Example inferred from signature (not verified)
sz = 3
d = 1
# Create dummy 1d-SAX representations of shape (sz, 2 * d)
sax1 = np.zeros((sz, 2 * d), dtype=np.float64)
sax2 = np.ones((sz, 2 * d), dtype=np.float64)

# Create dummy breakpoint middle values
breakpoints_avg_middle = np.array([-0.5, 0.5], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

original_size = 15

dist = cydist_1d_sax(
    sax1, 
    sax2, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)

print(f"1d-SAX distance: {dist}")
assert isinstance(dist, float)
```

### LLM Instruction Prompt
- Use `cydist_1d_sax` only when you need to compute the distance between pre-computed 1d-SAX representations.
- Do not pass raw time-series data to this function; it expects the symbolic representations of shape `(sz, 2 * d)`.
- Ensure that `breakpoints_avg_middle_` and `breakpoints_slope_middle_` are strictly 1-dimensional arrays.
- Remember to pass the `original_size` of the time series as an integer, as it is required for the distance scaling.

### Prompt Snippet
```text
When calculating the distance between 1d-SAX representations, use `tslearn.metrics.cysax.cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)`. Ensure `sax1` and `sax2` are 2D arrays of shape `(sz, 2 * d)`, the breakpoints are 1D arrays, and `original_size` is an integer.
```

### Common Failure Modes
- Passing raw 3D time-series datasets `(n_ts, max_sz, d)` instead of the 2D 1d-SAX representations `(sz, 2 * d)`.
- Providing multi-dimensional arrays for the breakpoint parameters, which will cause Cython buffer shape errors.
- Forgetting to pass the `original_size` argument, resulting in a `TypeError` for missing required positional arguments.
- Shape mismatches between `sax1` and `sax2` (they must have the same number of segments and dimensions).

### Fix Code Hint
```python
# FIX: Ensure inputs are 2D SAX representations and breakpoints are 1D arrays
sax1 = np.asarray(sax1, dtype=np.float64)
sax2 = np.asarray(sax2, dtype=np.float64)
bp_avg = np.asarray(breakpoints_avg_middle_, dtype=np.float64).flatten()
bp_slope = np.asarray(breakpoints_slope_middle_, dtype=np.float64).flatten()

dist = cydist_1d_sax(sax1, sax2, bp_avg, bp_slope, int(original_size))
```