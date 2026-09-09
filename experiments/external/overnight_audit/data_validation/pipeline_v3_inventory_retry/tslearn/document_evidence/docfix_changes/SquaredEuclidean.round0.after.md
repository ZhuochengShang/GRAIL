## API Test: `SquaredEuclidean`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class SquaredEuclidean(X, Y, be=None, compute_with_backend=False)
```

### Goal
ADVANCED/LOW-LEVEL. Instantiate a stateful metric object that computes and stores the pairwise squared Euclidean distance matrix between two specific time series. This is an internal helper primarily used by `SoftDTW` and barycenter computations to manage distance matrices and their Jacobians.

### Parameters
- `X`: array-like, shape=(m, d). The first time series.
- `Y`: array-like, shape=(n, d). The second time series.
- `be`: Backend object, string, or `None`. Specifies the computational backend (e.g., NumPy, PyTorch).
- `compute_with_backend`: `bool`, default=`False`. If `False`, non-NumPy backends may temporarily convert to NumPy to accelerate computation via Numba.

### Input
Requires two time-series arrays (`X` and `Y`) passed directly to the constructor. As a low-level stateful object, it binds to a specific pair of inputs upon instantiation.

### Output
Returns an instantiated `SquaredEuclidean` object. Calling the `.compute()` method on this object returns an `(m, n)` array representing the pairwise squared Euclidean distance matrix. Calling `.jacobian_product(E)` returns an `(m, d)` array.

### Valid Call Patterns
```python
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# Instantiate the stateful metric object with two time series
metric = SquaredEuclidean([1, 2, 2, 3], [1, 2, 3, 4])

# Compute the pairwise squared Euclidean distance matrix
D = metric.compute()

assert D.shape == (4, 4)
assert D[0, 0] == 0.0
```

### LLM Instruction Prompt
Instantiate `SquaredEuclidean` by passing two time-series arrays (`X` and `Y`) as positional arguments. Call `.compute()` on the resulting object to get the distance matrix. Do not treat it as a stateless factory.

### Prompt Snippet
```python
from tslearn.metrics.softdtw_variants import SquaredEuclidean
metric = SquaredEuclidean([1, 2, 2, 3], [1, 2, 3, 4])
D = metric.compute()
```

### Common Failure Modes
- **ADVANCED/LOW-LEVEL API misuse:** Treating the class as a stateless metric factory.
- **Missing arguments:** `TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`. This occurs if the execution harness attempts to instantiate the class without arguments (`SquaredEuclidean()`).

### Fix Code Hint
```python
# WRONG: Instantiating without arguments (stateless factory assumption)
metric = SquaredEuclidean()
D = metric(X, Y)

# RIGHT: Passing arrays to the constructor and calling compute()
metric = SquaredEuclidean(X, Y)
D = metric.compute()
```