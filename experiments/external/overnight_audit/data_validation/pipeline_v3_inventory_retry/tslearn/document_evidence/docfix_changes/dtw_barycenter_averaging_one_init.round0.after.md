## API Test: `dtw_barycenter_averaging_one_init`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def dtw_barycenter_averaging_one_init(X, barycenter_size=None, init_barycenter=None, max_iter=30, tol=1e-05, weights=None, metric_params=None, verbose=False, n_jobs=None)
```

### Goal
ADVANCED/LOW-LEVEL helper function. Computes the Dynamic Time Warping (DTW) Barycenter Averaging (DBA) for a time-series dataset using a single initialization of the Expectation-Maximization algorithm. Note: This should be excluded from the main user-facing denominator; standard users should use `dtw_barycenter_averaging` instead.

### Parameters
- `X`: array-like, shape `(n_ts, sz, d)`. The time-series dataset to average.
- `barycenter_size`, default `None`: int or None. The length of the generated barycenter. If `None`, defaults to the size of the data or the initial barycenter.
- `init_barycenter`, default `None`: array or None. The initial barycenter time series to start the optimization process.
- `max_iter`, default `30`: int. The maximum number of Expectation-Maximization iterations.
- `tol`, default `1e-05`: float. The tolerance for early stopping based on cost decrease.
- `weights`, default `None`: array or None. The weights for each time series in `X`. Must be the same length as `X`. If `None`, uniform weights are used.
- `metric_params`, default `None`: dict or None. DTW constraint parameters (e.g., `global_constraint`, `sakoe_chiba_radius`).
- `verbose`, default `False`: boolean. Whether to print cost information at each iteration.
- `n_jobs`, default `None`: int or None. The number of parallel jobs to run.

### Input
- ADVANCED/LOW-LEVEL API: Requires explicit low-level construction.
- `X` must be formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. Raw lists or 2D arrays must be converted using `tslearn.utils.to_time_series_dataset` before calling this function.
- `weights`, if provided, must be a 1D array of length `n_ts`.

### Output
Returns a tuple `(barycenter, inertia)` where `barycenter` is a 2D `numpy.ndarray` of shape `(barycenter_size, d)` representing the averaged time series, and `inertia` is a `float` representing the associated DTW cost.

### Valid Call Patterns
```python
import numpy as np
from tslearn.barycenters.dba import dtw_barycenter_averaging_one_init
from tslearn.utils import to_time_series_dataset

X = to_time_series_dataset([
    [1.0, 2.0, 3.0], 
    [1.0, 2.0, 2.0], 
    [2.0, 2.0, 3.0]
])

barycenter, inertia = dtw_barycenter_averaging_one_init(
    X=X, 
    max_iter=10, 
    tol=1e-4
)

assert barycenter.shape == (3, 1)
assert isinstance(inertia, float)
```

### LLM Instruction Prompt
- `dtw_barycenter_averaging_one_init` is an advanced helper and is not exposed in the `tslearn.barycenters` namespace. It must be imported directly from `tslearn.barycenters.dba`.
- Ensure the input `X` is a 3D array of shape `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to enforce this.
- Always unpack the return value into two variables: `barycenter, inertia`.

### Prompt Snippet
```text
Use `tslearn.barycenters.dba.dtw_barycenter_averaging_one_init` to compute the DTW barycenter of a time-series dataset for a single initialization. Ensure the input is a 3D array `(n_ts, sz, d)` and unpack the returned tuple `(barycenter, inertia)`.
```

### Common Failure Modes
- **ImportError (`cannot import name 'dtw_barycenter_averaging_one_init' from 'tslearn.barycenters'`)**: This is an ADVANCED/LOW-LEVEL helper and is excluded from the main user-facing denominator. It is not exposed in the package's `__init__.py` and must be imported directly from `tslearn.barycenters.dba`.
- Passing a 1D or 2D array for `X` instead of the required 3D array `(n_ts, sz, d)`, which causes shape mismatch errors during DTW computation.
- Failing to unpack the return value into two variables, leading to type errors when attempting to use the tuple as a numpy array.

### Fix Code Hint
```python
# WRONG
from tslearn.barycenters import dtw_barycenter_averaging_one_init
barycenter = dtw_barycenter_averaging_one_init(X, max_iter=10)

# CORRECT
from tslearn.barycenters.dba import dtw_barycenter_averaging_one_init
from tslearn.utils import to_time_series_dataset

X_3d = to_time_series_dataset(X)
barycenter, inertia = dtw_barycenter_averaging_one_init(X_3d, max_iter=10)
```