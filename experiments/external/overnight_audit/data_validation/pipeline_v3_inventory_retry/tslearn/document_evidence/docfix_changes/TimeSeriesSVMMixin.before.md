## API Test: `TimeSeriesSVMMixin`

### Signature
```python
class TimeSeriesSVMMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/svm/svm.py:20_

_Source doc:_ Time series mixin for SVM based estimators.

### Goal
Provides a mixin class for Support Vector Machine (SVM) based time-series estimators to ensure compatibility with `tslearn`'s 3D array data formats and `scikit-learn`'s API.

### Parameters
_None._

### Input
As a mixin class, it takes no runtime data inputs during initialization. It is intended to be inherited by custom SVM estimator classes. Methods provided by this mixin will expect time-series datasets to be strictly formatted as 3D `numpy` arrays of shape `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — acts as a base class providing SVM-specific time-series utility methods and attributes for derived estimators.

### Valid Call Patterns
```python
from tslearn.svm.svm import TimeSeriesSVMMixin
from sklearn.base import BaseEstimator

# Inferred from signature: Mixins are meant to be inherited, not instantiated directly.
class CustomTimeSeriesSVM(BaseEstimator, TimeSeriesSVMMixin):
    def __init__(self):
        pass

estimator = CustomTimeSeriesSVM()

assert isinstance(estimator, TimeSeriesSVMMixin), "Estimator should inherit from TimeSeriesSVMMixin"
print("Custom SVM estimator successfully inherited from TimeSeriesSVMMixin.")
```

### LLM Instruction Prompt
- Use `TimeSeriesSVMMixin` strictly as a base class (mixin) when creating custom SVM-based time-series estimators.
- Do not instantiate `TimeSeriesSVMMixin` directly.
- Ensure that any data passed to the resulting estimator's methods is formatted as a 3D `numpy` array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`.

### Prompt Snippet
```text
Use `TimeSeriesSVMMixin` as a base class for custom SVM time-series estimators. Do not instantiate it directly. Ensure input data to the derived estimator is a 3D array `(n_ts, max_sz, d)`.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate `TimeSeriesSVMMixin` directly rather than using it as a base class for an estimator.
- **Incorrect Data Dimensions:** Passing 1D or 2D arrays to the methods inherited from this mixin, which strictly require the `(n_ts, max_sz, d)` 3D array format.

### Fix Code Hint
```python
# Inherit from the mixin rather than instantiating it
class MySVM(BaseEstimator, TimeSeriesSVMMixin):
    pass

# Ensure data is 3D before passing to inherited methods
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
```