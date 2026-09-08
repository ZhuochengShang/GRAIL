# Deep-dive: `SquaredEuclidean`

model: google:gemini-3.1-pro-preview · tokens in=4,460 out=2,806 · wall 23s · 2026-09-08 14:54

---

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
ADVANCED/LOW-LEVEL
TESTABLE FROM PUBLIC INPUTS

This API is a low-level helper class primarily used internally by `SoftDTW` and soft-DTW barycenter computations to manage pairwise distance matrices and their Jacobians. However, it is exposed publicly, documented with an interactive example, and can be instantiated directly from public inputs (time-series arrays).

### L1 PURPOSE
`SquaredEuclidean` is a stateful metric object that computes and stores the pairwise squared Euclidean distance matrix between two time series, $X$ and $Y$. It sits at the base of the `SoftDTW` algorithm's data flow, providing both the forward distance matrix computation and the backward Jacobian product required for gradient-based optimization (e.g., in barycenter computation).

### L2 CONTRACT
**Constructor:**
`SquaredEuclidean(X, Y, be=None, compute_with_backend=False)`
- `X`: array-like, shape=(m, d). The first time series.
- `Y`: array-like, shape=(n, d). The second time series.
- `be`: Backend object, string, or `None`. Specifies the computational backend (e.g., NumPy, PyTorch).
- `compute_with_backend`: `bool`, default=`False`. If `True` and a non-NumPy backend is used, computations remain in that backend. If `False`, it may convert to NumPy to accelerate computation via Numba.

**Methods:**
- `compute()`: Returns `D`, an array-like of shape `(m, n)` representing the pairwise squared Euclidean distance matrix.
- `jacobian_product(E)`: Takes `E`, an array-like of shape `(m, n)`. Returns `G`, an array-like of shape `(m, d)`, representing the product of the Jacobian (a linear map from $m \times d$ to $m \times n$) and the matrix $E$.

### L3 MECHANICS
- **Initialization:** The constructor resolves the backend using `instantiate_backend(be, X, Y)`. It then formats `X` and `Y` into standard time-series shapes using `to_time_series` and casts them to `float64` in the selected backend (lines 1203-1206).
- **Distance Computation (`compute`):** Delegates directly to the backend's `pairwise_euclidean_distances(self.X, self.Y)` and squares the result (line 1216).
- **Jacobian Product (`jacobian_product`):** Allocates a zero matrix `G` of shape `(m, d)`. Depending on the backend and the `compute_with_backend` flag, it delegates the actual math to either `_njit_jacobian_product_sq_euc` (a Numba JIT-compiled function for NumPy arrays) or `_jacobian_product_sq_euc` (for other backends). If `compute_with_backend` is `False` but a non-NumPy backend is used, it temporarily casts the inputs to NumPy, runs the JIT function, and casts the result back (lines 1235-1248).

### L4 CORRECT MINIMAL USAGE
```python
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# Instantiate the metric object with two time series
# (1D arrays are automatically reshaped to (n, 1) by to_time_series)
metric = SquaredEuclidean([1, 2, 2, 3], [1, 2, 3, 4])

# Compute the pairwise squared Euclidean distance matrix
D = metric.compute()

# Verify the shape (m=4, n=4) and a known distance value
assert D.shape == (4, 4)
assert D[0, 0] == 0.0  # (1 - 1)^2 == 0

print("Distance matrix computed successfully:")
print(D)
```

### L5 FAILURE FORENSICS
- **`TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`**
  - **Why it failed:** The execution harness attempted to instantiate the class without arguments (`metric = SquaredEuclidean()`).
  - **Source citation:** Line 1178 (`def __init__(self, X, Y, be=None, compute_with_backend=False):`) explicitly requires `X` and `Y` as positional arguments.
  - **Context:** The provided "CURRENT DOCUMENTATION ENTRY" is entirely hallucinated and dangerously incorrect. It claims the constructor takes no parameters and explicitly warns *against* passing arrays to it. The source code and the docstring example (line 1197: `SquaredEuclidean([1, 2, 2, 3], [1, 2, 3, 4]).compute()`) prove that the arrays must be passed at instantiation.

### L6 SELF-ASSESSMENT
- **Inferences:** The exact mathematical operations inside `_njit_jacobian_product_sq_euc` are inferred to be the standard chain-rule derivatives for squared Euclidean distance, as the implementation of that specific helper is not included in the snippet.
- **Confidence Scores:**
  - **L2 (Contract): 10/10** - The constructor signature, types, and method signatures are fully visible in the provided source code.
  - **L3 (Mechanics): 10/10** - The delegation to backend methods and JIT helpers is explicitly written in the `compute` and `jacobian_product` methods.
  - **L4 (Usage): 10/10** - The usage exactly mirrors the verified docstring example provided in the source code.