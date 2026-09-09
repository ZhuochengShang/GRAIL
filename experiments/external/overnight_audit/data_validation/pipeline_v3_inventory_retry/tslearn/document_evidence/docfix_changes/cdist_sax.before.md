## API Test: `cdist_sax`

### Signature
```python
def cdist_sax(dataset1, breakpoints_avg, size_fitted, dataset2=None, n_jobs=None, verbose=0)
```
_Source: tslearn/tslearn/metrics/sax.py:10_

_Source doc:_ Calculates a matrix of distances (MINDIST) on SAX-transformed data, as presented in [1]_. It is important to note that this function expects the timeseries in dataset1 and dataset2 to be normalized to each have zero mean and unit variance. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz1, d) or (n_ts1, sz1) or (sz1,) A dataset of time series. If shape is (n_ts1, sz1), the dataset is composed of univariate time series. If shape is (sz1,), the dataset is composed of a unique univariate time series. breakpoints_avg : array-like, ndim=1 The breakpoints used to assign the alphabet symbols. size_fitted: int The original timesteps in the timeseries, before discretizing through SAX. dataset2 : None or array-like, shape=(n_ts2, sz2, d) or (n_ts2, sz2) or (sz2,) (default: None) Another dataset of time series. If `None`, self-similarity of `dataset1` is returned. If shape is (n_ts2, sz2), the dataset is composed of univariate time series. If shape is (sz2,), the dataset is composed of a unique univariate time series. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. verbose : int, optional (default=0) The verbosity level: if non zero, progress messages are printed. Above 50, the output is sent to stdout. The frequency of the messages increases with the verbosity level. If it more than 10, all iterations are reported. `Glossary <https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation>`__ for more details. Returns ------- cdist : array-like, shape=(n_ts1, n_ts2) Cross-similarity matrix. References ---------- .. [1] Lin, Jessica, et al. "Experiencing SAX: a novel symbolic representation of time series." Data Mining and knowledge discovery 15.2 (2007): 107-144.

### Goal
Calculates a cross-similarity matrix of MINDIST distances between two datasets of SAX-transformed time series.

### Parameters
- `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of time series.
- `breakpoints_avg`: 1D array-like. The breakpoints used to assign the SAX alphabet symbols.
- `size_fitted`: Integer. The original number of timesteps in the time series before they were discretized through SAX.
- `dataset2`, default `None`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`. The second dataset of time series. If `None`, the self-similarity matrix of `dataset1` is returned.
- `n_jobs`, default `None`: Integer or `None`. The number of parallel jobs to run (`-1` uses all processors).
- `verbose`, default `0`: Integer. The verbosity level for progress messages.

### Input
Time-series datasets provided as array-like structures (lists or NumPy arrays). 
**Crucial Precondition:** The time series in `dataset1` and `dataset2` MUST be normalized to have zero mean and unit variance before being passed to this function (e.g., using `tslearn.preprocessing.TimeSeriesScalerMeanVariance`). The function mathematically assumes this normalization for the MINDIST calculation.

### Output
Returns `unspecified` — A 2D array-like cross-similarity matrix of shape `(n_ts1, n_ts2)` containing the computed MINDIST distances between the time series in `dataset1` and `dataset2`.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# Note: Inputs here are assumed to be already normalized (zero mean, unit variance)
expected = np.array([[0, 1], [1, 0]])
dists = tslearn.metrics.cdist_sax(
    [[-1, 0, 1], [1, 0, 1]],
    [-0.5, 0., 0.5],
    3,
    dataset2=[[-1, 0, 1], [1, 0, 1]],
)

np.testing.assert_equal(dists, expected)
print(f"Computed SAX MINDIST matrix:\n{dists}")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.cdist_sax`, you MUST ensure the input time series (`dataset1` and `dataset2`) are normalized to zero mean and unit variance.
- You must provide the 1D array of `breakpoints_avg` and the integer `size_fitted` (the original length of the time series before SAX discretization) as positional arguments.
- If computing pairwise distances between two different datasets, pass the second dataset to the `dataset2` keyword argument.

### Prompt Snippet
```text
Compute the SAX MINDIST distance matrix between `X_sax` and `Y_sax`. Assume both datasets were derived from time series of original length 50 that were normalized to zero mean and unit variance. Use the breakpoints array `sax_breakpoints`.
```

### Common Failure Modes
- **Unnormalized Data:** Passing raw time series that do not have zero mean and unit variance. The function will execute, but the resulting MINDIST distances will be mathematically invalid.
- **Missing Positional Arguments:** Failing to provide `breakpoints_avg` or `size_fitted`, which are required positional arguments without defaults.
- **Incorrect Breakpoints Shape:** Passing a 2D array for `breakpoints_avg` instead of the required 1D array.

### Fix Code Hint
```python
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import tslearn.metrics

# Ensure data is normalized before SAX transformation and distance computation
scaler = TimeSeriesScalerMeanVariance()
X_normalized = scaler.fit_transform(X_raw)
Y_normalized = scaler.fit_transform(Y_raw)

# Compute distances using the normalized data representations
dists = tslearn.metrics.cdist_sax(
    X_normalized, 
    breakpoints_avg=my_breakpoints, 
    size_fitted=X_raw.shape[1], 
    dataset2=Y_normalized
)
```