# Deep-dive: `compute`

model: google:gemini-3.1-pro-preview · tokens in=5,272 out=3,958 · wall 31s · 2026-09-08 15:04

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
- Classification: ADVANCED/LOW-LEVEL
- Testability: TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- Explanation: The `compute` method belongs to internal helper classes (`SoftDTW` and `SquaredEuclidean`) defined in `tslearn.metrics.softdtw_variants`. These classes are used as building blocks for higher-level functions like `soft_dtw_alignment` and barycenter computations. They are not meant to be instantiated directly by typical end-users, but they can be constructed explicitly by passing time-series arrays to `SquaredEuclidean` and then passing the resulting object (or a precomputed distance matrix) to `SoftDTW`. This API should be excluded from a main user-facing benchmark denominator.

L1 PURPOSE
The `compute` method executes the core mathematical operations for differentiable time-series metrics. Depending on the receiver object, it either calculates the pairwise squared Euclidean distance matrix between two time series (`SquaredEuclidean.compute()`) or executes the dynamic programming algorithm to find the Soft-DTW discrepancy (`SoftDTW.compute()`). It acts as the delayed execution step in a computation graph, allowing backend-specific (NumPy, PyTorch) acceleration and memory allocation to be deferred until explicitly requested.

L2 CONTRACT
- Receiver: An instance of `SquaredEuclidean` or `SoftDTW`.
  - `SquaredEuclidean` is obtained via `SquaredEuclidean(X, Y, be=None, compute_with_backend=False)` where `X` and `Y` are array-like time series.
  - `SoftDTW` is obtained via `SoftDTW(D, gamma=1.0, be=None, compute_with_backend=False)` where `D` is a distance matrix or an object with a `compute()` method (like `SquaredEuclidean`).
- Parameters: None (takes only `self`).
- Return value: 
  - For `SquaredEuclidean`: A 2D array-like of shape `(m, n)` containing the squared Euclidean distance matrix.
  - For `SoftDTW`: A `float` representing the soft-DTW discrepancy score.
- State Mutation: `SoftDTW.compute()` mutates the object by populating `self.R_` (the accumulated cost matrix of shape `(m+2, n+2)`) and setting the boolean flag `self.computed = True`. `SquaredEuclidean.compute()` is stateless.
- Visibility: Public, though primarily intended for framework-internal use.

L3 MECHANICS
- `SquaredEuclidean.compute()`: Delegates directly to the active backend's `pairwise_euclidean_distances(self.X, self.Y)` and squares the result (line 1216).
- `SoftDTW.compute()`: 
  1. Retrieves the dimensions `m, n` of the distance matrix `self.D`.
  2. Checks the active backend. If it is NumPy, it delegates to a Numba-compiled fast path `_njit_soft_dtw(self.D, self.R_, gamma=self.gamma)` (line 1122).
  3. If a non-NumPy backend is used but `compute_with_backend` is `False`, it temporarily casts the inputs to NumPy, runs the Numba fast path, and casts the result back to the original backend (lines 1123-1129).
  4. If `compute_with_backend` is `True`, it delegates to the pure-backend implementation `_soft_dtw` (line 1131).
  5. Sets `self.computed = True` (required before calling `grad()`) and returns the final accumulated cost at `self.R_[m, n]`.

L4 CORRECT MINIMAL USAGE
```python
import numpy as np
from tslearn.metrics.softdtw_variants import SquaredEuclidean
from tslearn.metrics import SoftDTW

# 1. Define two small time series (shape: n_timestamps, n_features)
X = np.array([[1.0], [2.0], [2.0], [3.0]])
Y = np.array([[1.0], [2.0], [3.0], [4.0]])

# 2. Construct the low-level SquaredEuclidean helper
sq_euc = SquaredEuclidean(X, Y)

# 3. Compute the distance matrix
D_matrix = sq_euc.compute()
assert D_matrix.shape == (4, 4)
print("Squared Euclidean Distance Matrix:\n", D_matrix)

# 4. Construct the low-level SoftDTW helper using the SquaredEuclidean object
sdtw = SoftDTW(D=sq_euc, gamma=1.0)

# 5. Compute the Soft-DTW discrepancy
sdtw_score = sdtw.compute()
assert isinstance(sdtw_score, float)
print(f"\nSoft-DTW Score: {sdtw_score}")
```

L5 FAILURE FORENSICS
- Failed Attempt: `SoftDTW(ts1=s1, ts2=s2, gamma=1.0)` followed by `soft_dtw_obj.compute()`
- Reason for Failure: The user attempted to instantiate `SoftDTW` by passing raw time series `ts1` and `ts2` directly to its constructor. As seen in the source at line 1096 (`if hasattr(D, "compute"): self.D = D.compute()`), `SoftDTW` expects its first positional argument `D` to be a precomputed distance matrix or a helper object that generates one (like `SquaredEuclidean`). It does not accept `ts1` and `ts2` kwargs. The correct approach is to wrap the time series in `SquaredEuclidean` first, as demonstrated in the `barycenters/softdtw.py` call site.

L6 SELF-ASSESSMENT
- INFERENCE: The exact class name `SoftDTW` is inferred from the failure history and the call site in `barycenters/softdtw.py:28`, as its `class SoftDTW:` declaration is just above the provided source snippet (line 1081 is inside its docstring).
- INFERENCE: The import path `tslearn.metrics.softdtw_variants` for `SquaredEuclidean` is inferred from the file path provided in the context.
- Confidence L2: 10/10. The source code clearly shows the return types, state mutations (`self.R_`, `self.computed`), and constructor parameters.
- Confidence L3: 10/10. The source code explicitly shows the delegation to `_njit_soft_dtw` and `pairwise_euclidean_distances`.
- Confidence L4: 10/10. The usage perfectly mirrors the exact call sites provided in the context (specifically `barycenters/softdtw.py:27-29`).