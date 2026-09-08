# Deep-dive: `cydist_1d_sax`

model: google:gemini-3.1-pro-preview · tokens in=4,947 out=3,693 · wall 30s · 2026-09-08 15:06

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** ADVANCED/LOW-LEVEL
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- **Explanation:** `cydist_1d_sax` is a Numba JIT-compiled backend helper function (`@njit`) located in `tslearn.metrics.cysax`. It is not meant for direct end-user consumption but is delegated to by higher-level estimator methods (e.g., in `tslearn.piecewise`). It is testable standalone, but requires explicit construction of low-level 1d-SAX symbolic representations and breakpoint arrays with specific shapes and types. It should be excluded from main user-facing benchmark denominators.

**L1 PURPOSE**
This API computes the distance between two 1d-SAX (1-dimensional Symbolic Aggregate approXimation) representations of time series. It sits at the bottom of the library's data flow, acting as a high-performance, parallelized Cython/Numba backend helper to calculate distances for piecewise symbolic representations without needing to fully reconstruct the original time series in Python space.

**L2 CONTRACT**
- **`sax1`**: Array-like, shape `(sz, 2 * d)`. Represents the 1d-SAX symbols for the first time series. **Crucial Note:** Despite the docstring claiming `dtype=float64`, this array *must* contain integer types (e.g., `np.int64` or `np.int32`) because its values are used directly as indices to look up breakpoints.
- **`sax2`**: Array-like, shape `(sz, 2 * d)`. Represents the 1d-SAX symbols for the second time series. Must also be of integer type.
- **`breakpoints_avg_middle_`**: Array-like, 1-dimensional, `dtype=float64`. Contains the middle values of the bins used to discretize the segment averages.
- **`breakpoints_slope_middle_`**: Array-like, 1-dimensional, `dtype=float64`. Contains the middle values of the bins used to discretize the segment slopes.
- **`original_size`**: Integer (`int64` or `int32`). The length of the original time series before it was reduced to `sz` segments.
- **Returns**: `float64`. The computed 1d-SAX distance.
- **Visibility**: Publicly importable but functionally internal/advanced.
- **Thread-safety/Laziness**: Thread-safe and eagerly evaluated. It uses Numba's `prange` for parallel execution across segments.

**L3 MECHANICS**
1. **Validation & Setup:** The function asserts that `sax1` and `sax2` have identical shapes (`sz == sax2.shape[0]` and `d_1d_sax == sax2.shape[1]`). It calculates the original dimensionality `d = d_1d_sax // 2` and the segment size `seg_sz = original_size // sz` (lines 167-170).
2. **Parallel Iteration:** It iterates over the `sz` segments in parallel using Numba's `prange` (line 172).
3. **Symbol Lookup:** For each segment `t` and dimension `di`, it uses the integer symbols in `sax1` and `sax2` to index into `breakpoints_avg_middle_` and `breakpoints_slope_middle_` (lines 176-179). The first `d` columns store average symbols; the next `d` columns store slope symbols.
4. **Distance Accumulation:** It reconstructs the linear trend for each point `tt` in the segment using the formula `avg + slope * (tt - t_middle)`. It computes the squared difference between the two reconstructed trends and accumulates it into a running sum `s` (lines 180-183).
5. **Return:** It returns the square root of the accumulated sum `s` (line 184).

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.metrics.cysax import cydist_1d_sax

# Number of segments (sz) and original dimensions (d)
sz = 3
d = 1

# 1d-SAX representations require shape (sz, 2 * d)
# WARNING: Must be integers to be used as array indices in Numba, 
# overriding the incorrect docstring that suggests float64.
sax1 = np.zeros((sz, 2 * d), dtype=np.int64)
sax2 = np.ones((sz, 2 * d), dtype=np.int64)

# Breakpoints must be 1D float arrays. 
# We need at least 2 elements since sax2 contains the index '1'.
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

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`
- **Why it failed:** The previous attempt followed the docstring literally and created `sax1` and `sax2` as `np.float64` arrays. At line 176 (`avg1 = breakpoints_avg_middle_[sax1[t, di]]`), the code attempts to use a value from `sax1` as an array index. Numba's `nopython` mode strictly forbids indexing arrays with floating-point numbers, resulting in a `TypingError` during compilation. The docstring is factually incorrect regarding the required `dtype` for `sax1` and `sax2`.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - The exact cause of the Numba `TypingError` was inferred by cross-referencing the failed attempt's use of `np.float64` with the source code's use of those arrays as indices (lines 176-179).
- **Information needed for certainty:** Confirmation from the `tslearn` maintainers on whether the docstring's mention of `float64` is a legacy artifact from before Numba strictness, or if the upstream caller (`piecewise.py`) actually passes floats that Numba used to silently cast to ints in older versions.
- **Confidence Scores:**
  - **L2 (Contract):** 9/10. High confidence, though overriding the official docstring's type signature requires a slight leap of faith based on Numba's mechanical constraints.
  - **L3 (Mechanics):** 10/10. The mathematical reconstruction and parallel accumulation are explicitly visible in the provided source.
  - **L4 (Minimal Usage):** 10/10. The provided snippet corrects the typing error and satisfies all shape and bounds requirements for the Numba compiler.