## API Test: `dtw_barycenter_averaging_one_init`

### Signature
```python
def dtw_barycenter_averaging_one_init(X, barycenter_size=None, init_barycenter=None, max_iter=30, tol=1e-05, weights=None, metric_params=None, verbose=False, n_jobs=None)
```
_Source: tslearn/tslearn/barycenters/dba.py:621_

_Source doc:_ DTW Barycenter Averaging (DBA) method estimated through Expectation-Maximization algorithm. DBA was originally presented in [1]_. This implementation is based on a idea from [2]_ (Majorize-Minimize Mean Algorithm). Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. barycenter_size : int or None (default: None) Size of the barycenter to generate. If None, the size of the barycenter is that of the data provided at fit time or that of the initial barycenter if specified. init_barycenter : array or None (default: None) Initial barycenter to start from for the optimization process. max_iter : int (default: 30) Number of iterations of the Expectation-Maximization optimization procedure. tol : float (default: 1e-5) Tolerance to use for early stopping: if the decrease in cost is lower than this value, the Expectation-Maximization procedure stops. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. metric_params: dict or None (default: None) DTW constraint parameters to be used. See :ref:`tslearn.metrics.dtw_path <fun-tslearn.metrics.dtw_path>` for a list of accepted parameters If None, no constraint is used for DTW computations. verbose : boolean (default: False) Whether to print information about the cost at each iteration or not. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. Returns ------- numpy.array of shape (barycenter_size, d) or (sz, d) if barycenter_size \ is None DBA barycenter of the provided time series dataset. float Associated inertia References ----------

### Goal
Computes the Dynamic Time Warping (DTW) Barycenter Averaging (DBA) for a time-series dataset using a single initialization of the Expectation-Maximization algorithm.

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
- `X` must be formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. Raw lists or 2D arrays must be converted using `tslearn.utils.to_time_series_dataset` before calling this function.
- `weights`, if provided, must be a 1D array of length `n_ts`.

### Output
Returns a tuple `(barycenter, inertia)` where `barycenter` is a 2D `numpy.ndarray` of shape `(barycenter_size, d)` representing the averaged time series, and `inertia` is a `float` representing the associated DTW cost.

### Valid Call Patterns
```python
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging_one_init
from tslearn.utils import to_time_series_dataset

# 1. Format data into the required 3D shape (n_ts, sz, d)
X = to_time_series_dataset([
    [1.0, 2.0, 3.0], 
    [1.0, 2.0, 2.0], 
    [2.0, 2.0, 3.0]
])

# 2. Compute the DBA barycenter and inertia (inferred from signature)
barycenter, inertia = dtw_barycenter_averaging_one_init(X, max_iter=10, tol=1e-4)

assert isinstance(barycenter, np.ndarray)
assert barycenter.shape == (3, 1)
assert isinstance(inertia, float)
print(f"Inertia: {inertia:.4f}")
```

### LLM Instruction Prompt
- When calling `dtw_barycenter_averaging_one_init`, ensure the input `X` is a 3D array of shape `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to enforce this.
- Always unpack the return value into two variables: `barycenter, inertia`.
- Keep `max_iter` small (e.g., 10-30) for fast execution in tests.

### Prompt Snippet
```text
Use `tslearn.barycenters.dtw_barycenter_averaging_one_init` to compute the DTW barycenter of a time-series dataset. Ensure the input is a 3D array `(n_ts, sz, d)` and unpack the returned tuple `(barycenter, inertia)`.
```

### Common Failure Modes
- Passing a 1D or 2D array for `X` instead of the required 3D array `(n_ts, sz, d)`, which causes shape mismatch errors during DTW computation.
- Failing to unpack the return value into two variables, leading to type errors when attempting to use the tuple as a numpy array.
- Providing `weights` that do not match the length of `X` (`n_ts`).

### Fix Code Hint
```python
# Ensure X is 3D
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X)

# Unpack the tuple
barycenter, inertia = dtw_barycenter_averaging_one_init(X_3d, max_iter=10)
```