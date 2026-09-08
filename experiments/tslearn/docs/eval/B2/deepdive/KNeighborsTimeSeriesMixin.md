# Deep-dive: `KNeighborsTimeSeriesMixin`

model: google:gemini-3.1-pro-preview · tokens in=5,533 out=3,764 · wall 32s · 2026-09-08 14:37

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
INTERNAL/FRAMEWORK. TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION.
This is a mixin class designed to be inherited by public estimators (like `KNeighborsTimeSeries`). It is not exposed in the public `tslearn.neighbors` namespace (as evidenced by the import failure in the history). Testing it standalone requires defining a custom class that inherits from it and manually injecting the internal state (like `_X_fit`, `_d`, and `metric`) that a standard `fit()` method would normally populate. It should be excluded from user-facing benchmark denominators.

**L1 PURPOSE**
`KNeighborsTimeSeriesMixin` provides the core distance computation and neighbor-search logic for time-series k-nearest neighbors estimators. It sits between the public estimator interface and the low-level distance metrics (like DTW, Soft-DTW, SAX, or Euclidean), handling data reshaping, metric parameter extraction, distance matrix computation, and efficient sorting of the nearest neighbors.

**L2 CONTRACT**
- **Receiver**: A custom class inheriting from `KNeighborsTimeSeriesMixin`. To function, the instance must have specific attributes populated: `n_neighbors` (int), `metric` (str), `metric_params` (dict or None), `n_jobs` (int or None), `_X_fit` (3D numpy array), `_ts_fit` (3D numpy array or None), and `_d` (int, the feature dimension).
- **Parameters for `kneighbors`**:
  - `X` (array-like, shape `(n_ts, sz, d)`, optional): The query time series. If `None`, the method finds neighbors for each point in the fitted dataset (`self._X_fit`), ignoring the point itself.
  - `n_neighbors` (int, optional): Number of neighbors to retrieve. Defaults to `self.n_neighbors`.
  - `return_distance` (boolean, optional): If `True`, returns both distances and indices. If `False`, returns only indices. Defaults to `True`.
- **Returns**:
  - `dist` (numpy.ndarray): Array of distances to the nearest points (only if `return_distance=True`).
  - `ind` (numpy.ndarray): Array of indices of the nearest points in the fitted dataset.
- **Visibility**: Internal/Framework. Must be imported from `tslearn.neighbors.neighbors`.

**L3 MECHANICS**
- **Input Handling**: If `X` is not provided, it defaults to `self._X_fit` and sets a `self_neighbors` flag to ensure a point is not its own nearest neighbor. It reshapes 2D inputs to 3D using `self._d`.
- **Distance Computation**: 
  - If `self.metric` is a valid tslearn metric (e.g., `"dtw"`, `"softdtw"`), it delegates to `_precompute_cross_dist`, which extracts parameters via `_get_metric_params` and calls the corresponding C/Cython backend (e.g., `_cdist_dtw` at `tslearn/metrics.py`).
  - If `self.metric` is standard (e.g., `"euclidean"`), it flattens the arrays and delegates to `scipy.spatial.distance.cdist`.
- **Neighbor Selection**: It uses `numpy.argpartition` (O(n) complexity) to efficiently find the `kbin` smallest distances without fully sorting the matrix.
- **Refinement**: If `self_neighbors` is true, it slices off the first column (distance of 0 to itself). It then uses `numpy.argsort` to strictly sort the selected `kbin` neighbors by distance before returning them.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.neighbors.neighbors import KNeighborsTimeSeriesMixin

# 1. Define a minimal class inheriting from the mixin
class CustomKNN(KNeighborsTimeSeriesMixin):
    def __init__(self):
        # Inject the state normally populated by an estimator's __init__ and fit()
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
print(f"Nearest neighbor index: {ind[0, 0]}, distance: {dist[0, 0]:.2f}")
```

**L5 FAILURE FORENSICS**
- **Failed Attempt**: `cannot import name 'KNeighborsTimeSeriesMixin' from 'tslearn.neighbors'`
- **Why it failed**: The documentation entry incorrectly suggested `from tslearn.neighbors import KNeighborsTimeSeriesMixin`. Because this is an internal mixin, it is not exposed in the `__init__.py` of the `neighbors` module. It must be imported directly from the submodule via `from tslearn.neighbors.neighbors import KNeighborsTimeSeriesMixin`.

**L6 SELF-ASSESSMENT**
- **Inferences**: The exact list of attributes required on the receiver (`_X_fit`, `_d`, `metric`, etc.) was inferred by tracing the attribute accesses within the provided source code for `kneighbors` and `_precompute_cross_dist`.
- **Information needed for certainty**: Confirmation that no other hidden attributes are required by `TimeSeriesMixin` (the parent class) during standard execution, though the minimal usage proves the core logic works without them.
- **Confidence Scores**:
  - L2 (Contract): 9/10. The parameters and returns are explicitly documented in the docstring, but the required receiver state is implicit.
  - L3 (Mechanics): 10/10. The source code clearly shows the delegation to `scipy_cdist` or `_precompute_cross_dist` and the use of `argpartition`.
  - L4 (Minimal Usage): 10/10. The snippet successfully bypasses the missing `fit()` method by manually injecting the exact state the mixin expects.