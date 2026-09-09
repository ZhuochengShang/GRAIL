## API Test: `KNeighborsTimeSeriesMixin`

### Signature
```python
class KNeighborsTimeSeriesMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:28_

_Source doc:_ Mixin for k-neighbors searches on Time Series.

### Goal
Provides a mixin class for k-neighbors searches on time-series data, intended for developers building custom scikit-learn compatible time-series estimators.

### Parameters
_None._

### Input
As a mixin class, it does not take direct runtime data inputs upon instantiation. It expects to be inherited by an estimator class that processes time-series datasets strictly formatted as 3D `numpy` arrays with shape `(n_ts, max_sz, d)` (number of time series, maximum sequence length, and dimensions).

### Output
Returns `unspecified` — it is a class used for inheritance to provide k-neighbors search capabilities to derived estimator classes, rather than a function returning a data value.

### Valid Call Patterns
```python
from tslearn.neighbors import KNeighborsTimeSeriesMixin
from sklearn.base import BaseEstimator

# 1. Use as a base class for a custom time-series estimator (Inferred from signature)
class CustomTimeSeriesKNN(KNeighborsTimeSeriesMixin, BaseEstimator):
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

# Verify the mixin is properly inherited
estimator = CustomTimeSeriesKNN()
assert isinstance(estimator, KNeighborsTimeSeriesMixin)
print("Successfully inherited from KNeighborsTimeSeriesMixin.")
```

### LLM Instruction Prompt
- Do not instantiate `KNeighborsTimeSeriesMixin` directly. It is a mixin class designed to be used via multiple inheritance when creating custom time-series k-nearest neighbors estimators.
- Ensure that any custom estimator inheriting from this mixin enforces the `tslearn` strict 3D array format `(n_ts, max_sz, d)` for its `X` inputs during `fit` and `predict`/`kneighbors` calls.

### Prompt Snippet
```text
When building custom k-nearest neighbors models for time-series data in tslearn, inherit from `tslearn.neighbors.KNeighborsTimeSeriesMixin` alongside `sklearn.base.BaseEstimator`. Do not instantiate the mixin directly.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate `KNeighborsTimeSeriesMixin()` directly instead of using it as a base class for an estimator.
- **Incorrect Data Dimensions in Derived Classes:** Failing to format the input data as a 3D array `(n_ts, max_sz, d)` before passing it to the methods provided by the mixin, which will cause underlying distance computations (like DTW) to fail.

### Fix Code Hint
```python
# WRONG: Direct instantiation
# knn = KNeighborsTimeSeriesMixin()

# RIGHT: Inherit to build a custom estimator
from tslearn.neighbors import KNeighborsTimeSeriesMixin
from sklearn.base import BaseEstimator

class MyKNN(KNeighborsTimeSeriesMixin, BaseEstimator):
    pass
```