## API Test: `jacobian_product`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def jacobian_product(self, E)
```

### Goal
ADVANCED/LOW-LEVEL. Computes the Jacobian-vector product for a squared Euclidean distance matrix. Used internally during the backward pass of Soft-DTW barycenter computations to apply the chain rule. This is an internal helper and should be excluded from main user-facing benchmark denominators.

### Parameters
- `self`: An instance of `SquaredEuclidean` (from `tslearn.metrics.softdtw_variants`), initialized with two time series `X` (shape `m x d`) and `Y` (shape `n x d`).
- `E`: array-like of shape `(m, n)`. Represents the gradient of the objective with respect to the `m x n` distance matrix (e.g., the soft alignment matrix).

### Input
ADVANCED/LOW-LEVEL. Requires explicit low-level construction. The caller must instantiate `tslearn.metrics.softdtw_variants.SquaredEuclidean(X, Y)` where `X` and `Y` are 2D arrays of shape `(m, d)` and `(n, d)`. The input `E` must be a 2D array of shape `(m, n)`.

### Output
`G`: array-like of shape `(m, d)`. The resulting gradient with respect to the first time series `X`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# X has shape (m=3, d=2)
X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
# Y has shape (n=4, d=2)
Y = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]])

# Instantiate the low-level distance object
dist_obj = SquaredEuclidean(X, Y)

# E is the gradient w.r.t the (m x n) distance matrix
E = np.ones((3, 4))

# Compute the Jacobian-vector product
G = dist_obj.jacobian_product(E)

assert G.shape == (3, 2)
```

### LLM Instruction Prompt
- Recognize this is an ADVANCED/LOW-LEVEL internal method.
- Do not call `jacobian_product` on `SoftDTW` or as a standalone function.
- Explicitly import and instantiate `SquaredEuclidean(X, Y)` from `tslearn.metrics.softdtw_variants`.
- Ensure `X` is `(m, d)`, `Y` is `(n, d)`, and `E` is `(m, n)`.

### Prompt Snippet
```python
dist_obj = SquaredEuclidean(X, Y)
G = dist_obj.jacobian_product(E)
```

### Common Failure Modes
- ADVANCED/LOW-LEVEL: Guessing the wrong owner class. A common failure is assuming `jacobian_product` belongs to the `SoftDTW` solver class or attempting to import non-existent helpers like `squared_distance_profile`. It strictly belongs to the underlying distance object `SquaredEuclidean`.
- Attempting to call it as a standalone module-level function.
- Passing an `E` matrix with incorrect dimensions (e.g., a standard `tslearn` 3D time-series dataset `(n_ts, max_sz, d)` instead of the expected 2D `(m, n)` shape).

### Fix Code Hint
```python
# WRONG: Assuming it belongs to SoftDTW or calling as a standalone function
# from tslearn.metrics.softdtw_variants import SoftDTW
# solver = SoftDTW(...)
# G = solver.jacobian_product(E)

# CORRECT: Instantiate SquaredEuclidean explicitly
from tslearn.metrics.softdtw_variants import SquaredEuclidean
dist_obj = SquaredEuclidean(X, Y) # X is (m, d), Y is (n, d)
G = dist_obj.jacobian_product(E)  # E is (m, n)
```