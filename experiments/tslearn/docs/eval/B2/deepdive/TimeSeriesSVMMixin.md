# Deep-dive: `TimeSeriesSVMMixin`

model: google:gemini-3.1-pro-preview · tokens in=6,286 out=4,952 · wall 34s · 2026-09-08 14:57

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** INTERNAL/FRAMEWORK. This is a mixin class designed to be inherited by `tslearn`'s SVM estimators (like `TimeSeriesSVC` and `TimeSeriesSVR`) to share boilerplate data-wrangling and property delegation. It should be excluded from the main user-facing benchmark denominator.
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. It cannot be instantiated or used directly. Testing it requires defining a mock subclass that inherits from `BaseEstimator` and `TimeSeriesSVMMixin`, provides a dummy `fit` method (required by scikit-learn's `check_is_fitted`), initializes required attributes (`kernel`, `gamma`, `random_state`), and injects a dummy `svm_estimator_`.

**L1 PURPOSE**
`TimeSeriesSVMMixin` provides shared data-wrangling logic and property delegation for SVM-based time-series estimators. It bridges 3D `tslearn` arrays to 2D `scikit-learn` SVMs by handling dimensionality reshaping, Global Alignment Kernel (GAK) precomputation, and proxying access to fitted SVM attributes (like `support_` and `coef_`).

**L2 CONTRACT**
- **Receiver:** A subclass inheriting from `TimeSeriesSVMMixin` and `sklearn.base.BaseEstimator`.
- **Method `_preprocess_sklearn(self, X, y=None, fit_time=False)`:**
  - `X` (array-like): 3D time-series dataset of shape `(n_ts, max_sz, d)`.
  - `y` (array-like, optional): Target values of shape `(n_ts,)`.
  - `fit_time` (bool, default=False): Whether the preprocessing is happening during the `fit` phase.
  - **Returns:** A tuple `(sklearn_X, y, nb_features)` where `sklearn_X` is a 2D array (either flattened time series or a precomputed kernel matrix), `y` is the validated target array, and `nb_features` is the feature dimension `d`.
- **Properties (`support_`, `dual_coef_`, `coef_`, `intercept_`):**
  - Require `self.svm_estimator_` and `self._X_fit` to be set, and the instance to have a `fit` method.
  - **Returns:** The corresponding attribute from the underlying `scikit-learn` estimator injected into `self.svm_estimator_`.
- **Visibility:** Internal/Framework.

**L3 MECHANICS**
- **Preprocessing (`_preprocess_sklearn`):** 
  1. Determines if NaNs are allowed based on whether `self.kernel` is in `VARIABLE_LENGTH_METRICS`.
  2. Validates `X` and `y` using `check_array` or `check_X_y`, then converts `X` to a 3D time-series dataset.
  3. If `fit_time=True`, it saves `self._X_fit`, computes `self.gamma_` (using `gamma_soft_dtw` if `gamma="auto"`), and saves `self.classes_`.
  4. If `fit_time=False`, it calls `check_is_fitted` and validates dimensions against `self._X_fit`.
  5. If `self.kernel` is `"gak"`, it sets `self.estimator_kernel_ = "precomputed"` and computes the GAK cross-similarity matrix using `_cdist_gak`. Otherwise, it flattens `X` to 2D using `to_sklearn_dataset`.
- **Property Delegation:** The properties call `check_is_fitted(self, ['svm_estimator_', '_X_fit'])` and then return the requested attribute from `self.svm_estimator_`.
- **Tags:** Overrides `_more_tags` and `__sklearn_tags__` to indicate support for variable-length data and disallow NaNs.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from sklearn.base import BaseEstimator
from tslearn.svm.svm import TimeSeriesSVMMixin

# 1. Define a mock estimator to host the mixin
class MockSVM(BaseEstimator, TimeSeriesSVMMixin):
    def __init__(self):
        self.kernel = "rbf"
        self.gamma = 0.1
        self.random_state = 42
        
    # Required by scikit-learn's check_is_fitted to recognize this as an estimator
    def fit(self, X, y=None):
        return self

class DummyUnderlyingSVM:
    @property
    def support_(self):
        return np.array([0, 1])

mock = MockSVM()
X = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])
y = np.array([0, 1])

# 2. Exercise the mixin's preprocessing logic (populates self._X_fit)
sklearn_X, y_out, nb_features = mock._preprocess_sklearn(X, y, fit_time=True)

# 3. Exercise property delegation by injecting a dummy underlying estimator
mock.svm_estimator_ = DummyUnderlyingSVM()

# _X_fit was set by _preprocess_sklearn, and fit() exists, satisfying check_is_fitted
support = mock.support_

assert sklearn_X.shape == (2, 2)  # Flattened from (2, 2, 1) to (2, 2)
assert nb_features == 1
assert mock.estimator_kernel_ == "rbf"
assert np.array_equal(support, np.array([0, 1]))
print("TimeSeriesSVMMixin successfully tested.")
```

**L5 FAILURE FORENSICS**
- **`AssertionError: The documented contract is insufficient...`**: The initial test attempt likely generated a tautological `isinstance(mock, TimeSeriesSVMMixin)` check without invoking any of the mixin's actual methods, failing the harness's requirement for a falsifiable behavioral assertion.
- **`TypeError: MockSVM() is not an estimator instance.`**: The test accessed `mock.support_` (or called `_preprocess_sklearn` with `fit_time=False`), which invokes `check_is_fitted(self, ...)`. In scikit-learn, `check_is_fitted` verifies that the object is an estimator by checking for the presence of a `fit` method. Because `MockSVM` inherited from `BaseEstimator` and `TimeSeriesSVMMixin` but did not define a `fit` method, `check_is_fitted` raised a `TypeError`.
- **`round 0: retry still failing`**: The doc-repair attempt failed to recognize the missing `fit` method requirement for `check_is_fitted`, so the generated code still raised the exact same `TypeError`.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** The exact reason for `TypeError: MockSVM() is not an estimator instance.` is inferred from scikit-learn's standard `check_is_fitted` behavior, which explicitly looks for a `fit` method on the instance to validate it as an estimator.
- **INFERENCE:** `VARIABLE_LENGTH_METRICS` contains `"gak"`, inferred from the assertion `assert self.kernel == "gak"` immediately following the check `if self.kernel in VARIABLE_LENGTH_METRICS:`.
- **Confidence in L2 (Contract):** 10/10. The contract is clearly defined by the source code signatures and property definitions.
- **Confidence in L3 (Mechanics):** 10/10. The mechanics are explicitly written in the provided `_preprocess_sklearn` and property methods.
- **Confidence in L4 (Minimal Usage):** 10/10. The minimal usage correctly mocks the required attributes, provides the missing `fit` method to satisfy `check_is_fitted`, and exercises both the preprocessing and property delegation.