# Deep-dive: `jacobian_product`

model: google:gemini-3.1-pro-preview · tokens in=3,310 out=3,850 · wall 33s · 2026-09-08 15:45

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** ADVANCED/LOW-LEVEL
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- **Explanation:** The `jacobian_product` method is not a standalone function; it is an instance method on a distance computation class (inferred as `SquaredEuclidean` from the constructor's docstring example). It is used internally during the backward pass of Soft-DTW barycenter computations to apply the chain rule. To test it, one must explicitly instantiate the `SquaredEuclidean` class with two time series, and then call `jacobian_product` with a gradient matrix `E`. It should be excluded from a main user-facing benchmark denominator, as typical users interact with high-level barycenter or metric functions rather than manually computing Jacobian-vector products.

**L1 PURPOSE**
The `jacobian_product` API computes the Jacobian-vector product for a squared Euclidean distance matrix. In the context of the library's data flow, it is used during the gradient descent optimization of Soft-DTW barycenters. It takes the gradient of the loss with respect to the pairwise distance matrix (represented by `E`, the expected alignment matrix) and propagates it backward to compute the gradient with respect to the input time series `X`.

**L2 CONTRACT**
- **Receiver:** An instance of `SquaredEuclidean` (located in `tslearn.metrics.softdtw_variants`), obtained by calling `SquaredEuclidean(X, Y)` where `X` and `Y` are time series arrays.
- **Parameters:**
  - `E`: array-like of shape `(m, n)`. Represents the gradient of the objective with respect to the `m x n` distance matrix (e.g., the soft alignment matrix).
- **Returns:**
  - `G`: array-like of shape `(m, d)`. The resulting gradient with respect to the first time series `X`, computed as the product of the Jacobian of the distance function and `E`.
- **Visibility:** Public method on a low-level helper class.
- **Thread-safety/Laziness:** Eagerly evaluated. Thread-safety depends on the underlying backend (NumPy/PyTorch) and the Numba JIT compilation.

**L3 MECHANICS**
- The method initializes a zero-filled array `G` with the same shape `(m, d)` and data type as the stored time series `self.X`, using the configured backend (`self.be`).
- It branches based on the backend configuration:
  - If the backend is NumPy (`self.be.is_numpy`), it delegates the computation to a Numba JIT-compiled helper `_njit_jacobian_product_sq_euc`, mutating `G` in place.
  - If a non-NumPy backend is used but `compute_with_backend` is `False`, it temporarily casts `X`, `Y`, `E`, and `G` to NumPy arrays, runs the Numba helper for speed, and casts `G` back to the original backend format.
  - If a non-NumPy backend is used and `compute_with_backend` is `True`, it delegates to a pure-backend helper `_jacobian_product_sq_euc`.
- It returns the populated gradient matrix `G`.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# Define two small time series
# X: shape (m=3, d=2)
X = np.array([[1.0, 2.0], 
              [3.0, 4.0], 
              [5.0, 6.0]])

# Y: shape (n=4, d=2)
Y = np.array([[1.0, 1.0], 
              [2.0, 2.0], 
              [3.0, 3.0], 
              [4.0, 4.0]])

# 1. Explicitly construct the low-level distance object
dist_obj = SquaredEuclidean(X, Y)

# 2. Define E, the gradient w.r.t the (m x n) distance matrix
# E: shape (m=3, n=4)
E = np.ones((3, 4))

# 3. Compute the Jacobian-vector product
G = dist_obj.jacobian_product(E)

assert G.shape == (3, 2), f"Expected shape (3, 2), got {G.shape}"
print("Jacobian product successfully computed. Shape:", G.shape)
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `[fail/infra] missing module/import: cannot import name 'squared_distance_profile' from 'tslearn.metrics'`
- **Why it failed:** This was primarily an infrastructure/environment failure where the `tslearn.metrics` module failed to initialize properly in the test harness. However, looking at the attempted code (`from tslearn.metrics.softdtw_variants import SoftDTW`), there was also a logical error: the author assumed `jacobian_product` was a method on the `SoftDTW` class. As shown in the real call sites (`D.jacobian_product(E)` where `D` is passed into `SoftDTW(D, gamma=gamma)`), the method actually belongs to the underlying distance object (e.g., `SquaredEuclidean`), not the `SoftDTW` solver itself.

**L6 SELF-ASSESSMENT**
- **Inferences:** The exact class name `SquaredEuclidean` was inferred from the `Examples` section of the `__init__` docstring provided in the context. The context did not explicitly print the `class SquaredEuclidean:` declaration line, but the example `SquaredEuclidean([1, 2, 2, 3], [1, 2, 3, 4]).compute()` makes this a near-certain deduction.
- **Information needed for absolute certainty:** The exact class definition line (e.g., `class SquaredEuclidean:`) to confirm the class name without relying on the docstring example.
- **Confidence Scores:**
  - **L2 (Contract):** 9/10. The shapes `(m, n)` and `(m, d)` are explicitly documented, though the receiver class name is inferred.
  - **L3 (Mechanics):** 10/10. The source code provided explicitly shows the backend branching and delegation logic.
  - **L4 (Usage):** 9/10. The snippet correctly aligns the shapes of `X`, `Y`, and `E` to satisfy the mathematical requirements of the Jacobian product, assuming the inferred class name is correct.