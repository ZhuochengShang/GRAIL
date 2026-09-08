## API Test: `TimeSeriesSVMMixin`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class TimeSeriesSVMMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/svm/svm.py:20_

### Goal
INTERNAL/FRAMEWORK API. Provides shared boilerplate and data-wrangling logic for SVM-based time-series estimators (like `TimeSeriesSVC`). It bridges 3D `tslearn` arrays to 2D `scikit-learn` SVMs by handling dimensionality reshaping, GAK precomputation, and proxying access to fitted SVM attributes. This should be excluded from the main user-facing benchmark denominator; it is testable ONLY with explicit low-level construction.

### Parameters
_None._ (Mixin class).

### Input
As an INTERNAL/FRAMEWORK mixin, it requires the inheriting subclass to define specific configuration attributes (`self.kernel`, `self.gamma`, `self.random_state`). 
- Its injected method `_preprocess_sklearn(X, y=None, fit_time=False)` takes 3D time-series arrays `(n_ts, max_sz, d)`. 
- Its delegation properties (`support_`, `dual_coef_`, `coef_`, `intercept_`) require `self.svm_estimator_` and `self._X_fit` to be set on the instance.

### Output
- `_preprocess_sklearn` returns a tuple `(sklearn_X, y, nb_features)` where `sklearn_X` is a 2D array (flattened time series or precomputed kernel matrix).
- Properties (`support_`, etc.) return the corresponding attributes from the underlying `scikit-learn` estimator injected into `self.svm_estimator_`.

### Valid Call Patterns
```python
import numpy as np
from sklearn.base import BaseEstimator
from tslearn.svm.svm import TimeSeriesSVMMixin

# 1. Define a mock estimator to host the mixin and provide required attributes
class MockSVM(BaseEstimator, TimeSeriesSVMMixin):
    def __init__(self):
        self.kernel = "rbf"
        self.gamma = 0.1
        self.random_state = 42

mock = MockSVM()
X = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])
y = np.array([0, 1])

# 2. Exercise the mixin's preprocessing logic (populates self._X_fit)
sklearn_X, y_out, nb_features = mock._preprocess_sklearn(X, y, fit_time=True)

# 3. Exercise property delegation by injecting a dummy underlying estimator
class DummyUnderlyingSVM:
    @property
    def support_(self):
        return np.array([0])

mock.svm_estimator_ = DummyUnderlyingSVM()

# _X_fit was set by _preprocess_sklearn(fit_time=True), satisfying check_is_fitted
support = mock.support_

assert sklearn_X.shape == (2, 2)  # Flattened from (2, 2, 1) to (2, 2)
assert nb_features == 1
assert mock.estimator_kernel_ == "rbf"
assert support[0] == 0
```

### LLM Instruction Prompt
`TimeSeriesSVMMixin` is an internal framework mixin. Do not test it with tautological `isinstance` checks. Test it by creating a mock subclass inheriting from `BaseEstimator` and `TimeSeriesSVMMixin`. Initialize `self.kernel`, `self.gamma`, and `self.random_state`. Call `_preprocess_sklearn(X, y, fit_time=True)` to exercise preprocessing and populate `self._X_fit`. Inject a dummy object into `self.svm_estimator_` to test property delegation (e.g., `support_`).

### Prompt Snippet
```text
Test the internal `TimeSeriesSVMMixin` by creating a mock subclass with `kernel`, `gamma`, and `random_state` attributes. Invoke `_preprocess_sklearn(X, y, fit_time=True)` and test property delegation by mocking `self.svm_estimator_`.
```

### Common Failure Modes
- **Empty Contract / Tautological Tests:** Failing to specify or invoke the mixin's actual methods, causing the generation of tautological `isinstance` checks or fabricated properties (like `support_vectors_time_series_`). You must explicitly invoke `_preprocess_sklearn` and delegation properties like `support_`.
- **Missing Subclass Attributes:** Calling `_preprocess_sklearn` without defining `self.kernel`, `self.gamma`, or `self.random_state` on the subclass, leading to `AttributeError`.
- **NotFittedError on Properties:** Accessing `support_` without first setting `self.svm_estimator_` and `self._X_fit` (which `check_is_fitted` requires).

### Fix Code Hint
```python
# WRONG: Tautological test that doesn't exercise the mixin's logic
class MockSVM(BaseEstimator, TimeSeriesSVMMixin): pass
mock = MockSVM()
assert isinstance(mock, TimeSeriesSVMMixin) # Fails to test behavior

# CORRECT: Provide required attributes and invoke injected methods
class MockSVM(BaseEstimator, TimeSeriesSVMMixin):
    def __init__(self):
        self.kernel = "rbf"
        self.gamma = 0.1
        self.random_state = 42

mock = MockSVM()
sklearn_X, y_out, nb_features = mock._preprocess_sklearn(X, y, fit_time=True)
```