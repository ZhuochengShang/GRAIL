# Deep-dive: `inv_transform_1d_sax`

model: google:gemini-3.1-pro-preview · tokens in=4,063 out=5,159 · wall 39s · 2026-09-08 15:33

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** ADVANCED/LOW-LEVEL (or INTERNAL/FRAMEWORK). It is a low-level Numba JIT-compiled backend helper used internally by `tslearn.piecewise.OneD_SymbolicAggregateApproximation`.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function can be executed directly by passing appropriately shaped and typed NumPy arrays.

**L1 PURPOSE**
`inv_transform_1d_sax` is a low-level, Numba-compiled backend helper function that reconstructs an approximate time series from its 1d-SAX (1D Symbolic Aggregate approXimation) representation. It maps discrete symbols (representing segment averages and slopes) back to continuous time-domain values using precomputed breakpoint middle values, and evaluates the resulting linear equations to reconstruct the segments.

**L2 CONTRACT**
- `dataset_sax`: 3D NumPy array of shape `(n_ts, sz, 2 * d)`. Contains the integer indices (symbols) for the average and slope of each segment. **Note:** Despite the docstring claiming `dtype=float64` or `float32`, this array *must* be an integer type (e.g., `np.int64` or `np.int32`) because its values are used directly as array indices.
- `breakpoints_avg_middle_`: 1D NumPy array of floats (e.g., `np.float64`). The continuous values corresponding to each average symbol.
- `breakpoints_slope_middle_`: 1D NumPy array of floats (e.g., `np.float64`). The continuous values corresponding to each slope symbol.
- `original_size`: Integer. The length of the original time series to reconstruct.
- **Returns:** `dataset_out`, a 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `np.float64`, containing the reconstructed time series.
- **Visibility:** Publicly importable but intended as an internal backend helper.
- **Thread-safety/laziness:** Uses Numba's `prange` for parallel execution over the `n_ts` dimension, making it thread-safe and parallelized for batch processing.

**L3 MECHANICS**
- The function initializes an empty output array `dataset_out` of shape `(n_ts, original_size, d)` (line 212).
- It calculates the segment size `seg_sz = original_size // sz` (line 211).
- It iterates over each time series `i` in parallel using Numba's `prange` (line 214).
- For each segment `t`, it calculates the start index `t0` and the middle time point `t_middle` (lines 216-217).
- For each dimension `di`, it retrieves the average value `avg` from `breakpoints_avg_middle_` using the symbol at `dataset_sax[i, t, di]` (line 219).
- It retrieves the slope value `slope` from `breakpoints_slope_middle_` using the symbol at `dataset_sax[i, t, di + d]` (line 220).
- It reconstructs the segment by evaluating the linear equation `avg + slope * (tt - t_middle)` for each time step `tt` in the segment, storing the result in `dataset_out` (line 222).
- **Failure conditions:** Raises a Numba `TypingError` if `dataset_sax` is a float array (due to invalid array indexing). Raises `IndexError` if the symbols in `dataset_sax` exceed the bounds of the breakpoint arrays.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.metrics.cysax import inv_transform_1d_sax

# 1 time series, 2 segments, d=1 (so 2*d = 2 features per segment: avg and slope)
# Symbols MUST be integers to be used as indices in Numba, despite the docstring.
dataset_sax = np.array([[[0, 0], [1, 1]]], dtype=np.int64)

# Middle values for the bins
breakpoints_avg_middle = np.array([0.25, 0.75], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

# Target original length
original_size = 4

reconstructed = inv_transform_1d_sax(
    dataset_sax,
    breakpoints_avg_middle,
    breakpoints_slope_middle,
    original_size
)

assert reconstructed.shape == (1, 4, 1)
print(reconstructed)
```

**L5 FAILURE FORENSICS**
- The recorded failure `TypingError: Failed in nopython mode pipeline (step: nopython frontend)` occurred because the previous attempt followed the docstring's incorrect advice to use `dtype=np.float64` (or `np.float32`) for `dataset_sax`.
- In Numba's `nopython` mode, array indices must be integers. The source code uses `dataset_sax` values as indices: `breakpoints_avg_middle_[dataset_sax[i, t, di]]` (line 219). Passing a float array causes a type inference failure during compilation because Numba does not implicitly cast float array elements to integers for indexing.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** I inferred that the docstring is incorrect about `dataset_sax` being `float64`/`float32`, based on the Numba `TypingError` and the source code using it as an index.
- **INFERENCE:** I inferred that `check_array` in the calling code (`piecewise.py`) preserves integer dtypes (which it does in scikit-learn when `dtype="numeric"` or `None` is used), allowing the internal framework to pass integers to this function successfully.
- **Confidence in L2:** 9/10. The types are clear from the Numba constraints, despite the misleading docstring.
- **Confidence in L3:** 10/10. The algorithm is a straightforward linear reconstruction from averages and slopes, clearly visible in the source.
- **Confidence in L4:** 10/10. The minimal usage provides the correct integer types and shapes to satisfy Numba's strict typing.