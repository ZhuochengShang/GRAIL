## API Test: `KNeighborsTimeSeriesMixin`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class KNeighborsTimeSeriesMixin(TimeSeriesMixin)
```

### Goal
INTERNAL/FRAMEWORK. Provides core distance computation and neighbor-search logic for time-series k-nearest neighbors estimators. This is an internal mixin and should be excluded from standard user-facing benchmark denominators.

### Parameters
_For the mixin's `kneighbors` method:_
- `X` (array-like, shape `(n_ts, sz, d)`, optional): Query time series. If `None`, finds neighbors for each point in the fitted dataset.
- `n_neighbors` (int, optional): Number of neighbors to retrieve.
- `return_distance` (boolean, optional): If `True`, returns both distances and indices.

### Input
ADVANCED/LOW-LEVEL. The mixin is not intended for direct instantiation. It must be inherited by a custom estimator class. To execute its methods, the receiver instance must have caller-owned internal state manually populated (e.g., `self.metric`, `self.metric_params`, `self.n_jobs`, `self._ts_fit`, `self._X_fit`, `self._d`, and `self.n_neighbors`), which are normally injected during a standard `fit()` call.

### Output
- `kneighbors` returns a tuple `(dist, ind)` containing numpy arrays of distances and indices to the nearest points.
- `_precompute_cross_dist` returns a 2D numpy array distance matrix.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors.neighbors import KNeighborsTimeSeriesMixin

# 1. Define a minimal class inheriting from the internal mixin
class CustomKNN(KNeighborsTimeSeriesMixin):
    def __init__(self):
        # Inject the state normally populated by an estimator's fit()
        self.n_neighbors = 1
        self.metric = "euclidean"
        self.metric_params = None
        self.n_jobs = 1
        
        # Mock fitted dataset: 3 time series, length 1, dimension 1
        self._X_fit = np.array([[[0.0]], [[2.0]], [[4.0]]])
        self._ts_fit = self._X_fit
        self._d = 1

# 2. Instantiate and query
knn = CustomKNN()
X_query = np.array([[[2.1]]])

dist, ind = knn.kneighbors(X_query, n_neighbors=1)

assert ind[0, 0] == 1  # 2.1 is closest to 2.0 (which is at index 1)
assert np.isclose(dist[0, 0], 0.1)
print("__CHECK__ KNeighborsTimeSeriesMixin computed nearest neighbor index:", ind[0, 0])
```

### LLM Instruction Prompt
- `KNeighborsTimeSeriesMixin` is an internal framework class. It MUST be imported from `tslearn.neighbors.neighbors`, not `tslearn.neighbors`.
- Do not instantiate the mixin directly. It must be inherited by a custom class.
- To test the mixin's methods (like `kneighbors` or `_precompute_cross_dist`), the derived class must explicitly initialize internal state attributes (`self.metric`, `self.metric_params`, `self.n_jobs`, `self._ts_fit`, `self._X_fit`, `self._d`, `self.n_neighbors`) before calling them.

### Prompt Snippet
```text
To test the internal tslearn.neighbors.neighbors.KNeighborsTimeSeriesMixin, inherit it in a custom class and manually assign self.metric, self.metric_params, self.n_jobs, self._ts_fit, self._X_fit, and self._d before calling its methods.
```

### Common Failure Modes
- **Import Error (INTERNAL/FRAMEWORK):** Attempting `from tslearn.neighbors import KNeighborsTimeSeriesMixin` fails with an `ImportError` because it is an internal class not exposed in the module's `__init__.py`. It must be imported from the `tslearn.neighbors.neighbors` submodule.
- **Missing Internal State (ADVANCED/LOW-LEVEL):** Calling mixin methods on a derived class without manually populating `self.metric`, `self.n_jobs`, `self._ts_fit`, `self._X_fit`, and `self._d` raises an `AttributeError`.
- **Direct Instantiation:** Attempting to instantiate `KNeighborsTimeSeriesMixin()` directly instead of using it as a base class.

### Fix Code Hint
```python
# WRONG: Incorrect import and missing internal state
# from tslearn.neighbors import KNeighborsTimeSeriesMixin
# class MyKNN(KNeighborsTimeSeriesMixin): pass
# knn = MyKNN()
# knn.kneighbors(X) # Fails: missing self._X_fit, self.metric, etc.

# RIGHT: Correct submodule import and explicit state injection
from tslearn.neighbors.neighbors import KNeighborsTimeSeriesMixin
import numpy as np

class MyKNN(KNeighborsTimeSeriesMixin):
    def __init__(self):
        self.n_neighbors = 1
        self.metric = "dtw"
        self.metric_params = None
        self.n_jobs = 1
        self._X_fit = np.array([[[0.0]], [[2.0]]])
        self._ts_fit = self._X_fit
        self._d = 1
```