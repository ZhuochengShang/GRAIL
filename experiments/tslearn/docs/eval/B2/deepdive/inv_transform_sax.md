# Deep-dive: `inv_transform_sax`

model: google:gemini-3.1-pro-preview · tokens in=5,682 out=6,389 · wall 52s · 2026-09-08 15:35

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification**: ADVANCED/LOW-LEVEL
- **Testability**: TESTABLE FROM PUBLIC INPUTS
- **Explanation**: This is a low-level, Numba-compiled (`@njit`) backend helper used internally by `tslearn`'s piecewise transformation classes (like `SymbolicAggregateApproximation`). It operates on primitive NumPy arrays and can be tested directly by providing appropriately shaped and typed arrays.

**L1 PURPOSE**
The `inv_transform_sax` function reconstructs a continuous time-series dataset from its discrete Symbolic Aggregate approXimation (SAX) representation. It maps the discrete SAX symbols (which act as bin indices) back to their corresponding continuous bin centers and repeats these values to expand the reduced SAX sequence back to the original time-series length.

**L2 CONTRACT**
- `dataset_sax`: A 3D NumPy array of shape `(n_ts, sz, d)`. **Crucially, this must be an integer type** (e.g., `np.int64` or `np.int32`) because it contains the indices of the SAX bins. *Note: The docstring incorrectly states `dtype=float64` or `float32`, which is a documentation error that causes compilation failures.*
- `breakpoints_middle_`: A 1D NumPy array of shape `(n_bins,)` and dtype `float64`. Contains the continuous values (bin centers) corresponding to each SAX symbol index.
- `original_size`: An integer representing the length of the original time series. It determines the expansion factor (`seg_sz = original_size // sz`). If `original_size` is not perfectly divisible by `sz`, the trailing elements of the reconstructed series will remain `0.0`.
- **Returns**: `dataset_out`, a 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `float64` containing the reconstructed time series.
- **Visibility**: Publicly accessible, but intended as an internal backend helper.
- **Thread-safety**: Safe and executes in parallel using Numba's `prange` if multiple time series (`n_ts > 1`) are provided.

**L3 MECHANICS**
- The function is JIT-compiled using Numba with `parallel=True` and `fastmath=True`.
- It calculates the segment size `seg_sz = original_size // sz` and initializes a zero-filled array `dataset_out` of shape `(n_ts, original_size, d)`.
- It iterates over each time series `i` (in parallel) and each SAX segment `t`.
- At line 100, it performs advanced indexing: `breakpoints_middle_[dataset_sax[i, t, :]]`. This looks up the continuous bin centers for all dimensions `d` simultaneously.
- It assigns this 1D array of size `d` to the 2D slice `dataset_out[i, t0 : t0 + seg_sz, :]` using NumPy/Numba broadcasting.
- **Mutates**: The locally created `dataset_out` array before returning it.
- **Raises**: `TypingError` during Numba compilation if `dataset_sax` is a float array. `IndexError` at runtime if any value in `dataset_sax` is out of bounds for `breakpoints_middle_`.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.metrics.cysax import inv_transform_sax

# 1 time series, SAX size 3, 1 dimension
# MUST be an integer type for Numba to use as indices, despite the docstring
dataset_sax = np.array([[[0], [1], [2]]], dtype=np.int64)

# 3 bins, so 3 middle breakpoints
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)

# Original size (e.g., 6, so each SAX symbol covers 2 time steps)
original_size = 6

# Execute the Numba-compiled function
dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, original_size)

# Verify the shape and the broadcasted reconstruction
assert dataset_out.shape == (1, 6, 1)
assert np.allclose(dataset_out[0, 0:2, 0], -0.5)
assert np.allclose(dataset_out[0, 2:4, 0], 0.0)
assert np.allclose(dataset_out[0, 4:6, 0], 0.5)

print("Reconstructed successfully:", dataset_out.flatten())
```

**L5 FAILURE FORENSICS**
- **Failure**: `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`
- **Cause**: The previous harness followed the incorrect docstring and passed `dataset_sax` as a float array (`dtype=float_type`). 
- **Source Citation**: At lines 100-102, the code executes `breakpoints_middle_[dataset_sax[i, t, :]]`. Numba strictly enforces that array indices must be integers. Attempting to index the 1D `breakpoints_middle_` array with a 1D slice of floats causes a type inference failure in Numba's frontend, aborting compilation. The fix is to pass `dataset_sax` as an integer array.

**L6 SELF-ASSESSMENT**
- **Inferences**: The assertion that the docstring is a copy-paste error or an artifact of scikit-learn's `check_array` default behavior is an inference, but the technical requirement for integer arrays is a hard constraint of Numba verified by the source code.
- **Information needed for certainty**: None. The Numba compilation rules and the provided source code definitively explain the failure and the required contract.
- **Confidence in L2 (Contract)**: 10/10. The types are strictly dictated by Numba's indexing rules, overriding the flawed docstring.
- **Confidence in L3 (Mechanics)**: 10/10. The array broadcasting and parallel loop mechanics are explicitly visible in the source.
- **Confidence in L4 (Minimal Usage)**: 10/10. The snippet correctly bypasses the documentation error by using `np.int64`, satisfying Numba's compiler and demonstrating the intended mathematical expansion.