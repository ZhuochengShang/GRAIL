# Deep-dive: `lcss_accumulated_matrix`

model: google:gemini-3.1-pro-preview · tokens in=6,338 out=3,056 · wall 38s · 2026-09-08 15:46

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as ADVANCED/LOW-LEVEL. It is a public-by-convention (no leading underscore) helper function that computes the dynamic programming table for the Longest Common Subsequence (LCSS) metric, but it is not exposed in the top-level `tslearn.metrics` namespace. It is intended for internal use by higher-level functions like `lcss` or for advanced users needing the raw alignment matrix. 

It is TESTABLE FROM PUBLIC INPUTS. The function can be executed standalone by importing it directly from its defining module (`tslearn.metrics.dtw_variants`) and passing standard NumPy arrays. It should be excluded from a main user-facing benchmark denominator since it is an internal implementation detail of the LCSS metric.

L1 PURPOSE
`lcss_accumulated_matrix` computes the dynamic programming accumulated cost matrix for the Longest Common Subsequence (LCSS) similarity between two time series. It sits at the lowest level of the LCSS computation pipeline, handling backend-specific (NumPy or PyTorch) operations, applying the bounding mask (e.g., Sakoe-Chiba or Itakura), and returning the full DP table used to derive the final LCSS score.

L2 CONTRACT
- **Receiver**: None (standalone function).
- **Parameters**:
  - `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
  - `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
  - `eps`: float. The matching threshold. Two points match if their Euclidean distance is less than or equal to `eps`.
  - `mask`: array-like, shape `(sz1, sz2)`. A boolean mask where unconsidered cells (e.g., outside a global constraint band) must have `False` values.
  - `be`: Backend object, string (`"numpy"`, `"pytorch"`), or `None` (default: `None`). Determines the execution backend. If `None`, it is inferred from the input arrays.
- **Returns**:
  - `acc_cost_mat`: array-like, shape `(sz1 + 1, sz2 + 1)`. The accumulated cost matrix representing the LCSS dynamic programming table. The type matches the selected backend.
- **Visibility**: Public by naming convention, but effectively internal/advanced as it is omitted from the `tslearn.metrics` `__init__.py` exports.
- **Thread-safety/Laziness**: Eagerly evaluated. Thread-safety depends on the underlying backend (NumPy/PyTorch) but is generally safe as it does not mutate global state.

L3 MECHANICS
- The function first resolves the backend using `instantiate_backend(be, s1, s2)` (line 2297).
- It normalizes `s1` and `s2` into 2D time series arrays and removes NaNs using `to_time_series(..., remove_nans=True, be=be)` (lines 2298-2299).
- It initializes an accumulated cost matrix of zeros with shape `(l1 + 1, l2 + 1)` using the backend's `full` method (line 2302).
- It iterates through the time series using a nested loop (`i` from 1 to `l1`, `j` from 1 to `l2`).
- For each cell, if `mask[i - 1, j - 1]` is true, it computes the squared Euclidean distance between the points. It delegates to `_njit_local_squared_dist` for NumPy or `_local_squared_dist` for other backends (lines 2307-2310).
- If the square root of the distance is `<= eps`, it registers a match: `acc_cost_mat[i][j] = 1 + acc_cost_mat[i - 1][j - 1]` (line 2312).
- Otherwise, it propagates the maximum previous subsequence length: `max(acc_cost_mat[i][j - 1], acc_cost_mat[i - 1][j])` (lines 2314-2316).
- It returns the populated matrix.

L4 CORRECT MINIMAL USAGE
```python
import numpy as np
# Must import from the specific submodule, as it is not exposed in tslearn.metrics
from tslearn.metrics.dtw_variants import lcss_accumulated_matrix

# 1D or 2D time series
s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])

# Matching threshold
eps = 0.5

# Mask must exactly match (len(s1), len(s2))
mask = np.ones((len(s1), len(s2)), dtype=bool)

# Compute the accumulated cost matrix
acc_mat = lcss_accumulated_matrix(s1, s2, eps=eps, mask=mask)

# The resulting matrix has shape (len(s1) + 1, len(s2) + 1)
assert acc_mat.shape == (len(s1) + 1, len(s2) + 1)
print("Accumulated Cost Matrix:\n", acc_mat)
```

L5 FAILURE FORENSICS
- **`ImportError: cannot import name 'lcss_accumulated_matrix' from 'tslearn.metrics'`**:
  This failed because the test harness attempted to import the function directly from `tslearn.metrics`. While the documentation entry implies it belongs to `tslearn.metrics`, the function is not exported in the `__init__.py` of the `metrics` module. It must be imported directly from its defining file: `tslearn.metrics.dtw_variants`.

L6 SELF-ASSESSMENT
- **Inferences**: I inferred that `lcss_accumulated_matrix` is not exported in `tslearn.metrics.__init__.py` based purely on the `ImportError` in the failure history.
- **Missing Information**: The exact contents of `tslearn/metrics/__init__.py` to definitively confirm the export omission.
- **Confidence Scores**:
  - L2 (Contract): 10/10. The signature, types, and docstrings are explicitly provided in the source.
  - L3 (Mechanics): 10/10. The source code for the function is fully provided and the logic is straightforward dynamic programming.
  - L4 (Usage): 10/10. The fix for the import error is clear, and the required shapes for `s1`, `s2`, and `mask` are explicitly enforced by the code.