# Deep-dive: `decision_function`

model: google:gemini-3.1-pro-preview · tokens in=5,616 out=3,103 · wall 26s · 2026-09-08 15:09

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience:** USER-FACING. This is a standard scikit-learn-compatible estimator method used directly by end-users to evaluate the decision function (e.g., distance to the separating hyperplane) of a fitted Support Vector Machine classifier.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The method can be tested by instantiating a `TimeSeriesSVC`, fitting it on public in-memory NumPy arrays, and then calling `decision_function`.

L1 PURPOSE
The `decision_function` method evaluates the decision function for a given set of time series using a fitted `TimeSeriesSVC` model. In the library's data flow, it acts as a bridge between `tslearn`'s 3D time-series data format and the underlying `sklearn.svm.SVC` estimator, preprocessing the time series into a 2D format compatible with scikit-learn before delegating the actual mathematical computation to the scikit-learn backend.

L2 CONTRACT
- **Receiver:** A fitted instance of `tslearn.svm.TimeSeriesSVC`. It must be instantiated with a valid kernel (e.g., `"gak"`, `"rbf"`, `"linear"`) and fitted via `.fit(X, y)`.
- **Parameters:**
  - `X`: An array-like of shape `(n_ts, sz, d)` representing the time series dataset to evaluate.
- **Returns:** A `numpy.ndarray` containing the decision function scores. 
  - For binary classification, the shape is `(n_samples,)`.
  - For multi-class classification, the shape is `(n_samples, n_classes * (n_classes-1) / 2)` if `decision_function_shape='ovo'`, or `(n_samples, n_classes)` if `decision_function_shape='ovr'` (which is the default in modern scikit-learn).
- **Visibility:** Public.
- **Thread-safety/Laziness:** Eagerly evaluated. Thread-safety depends on the underlying `libsvm` implementation in scikit-learn, which may have limitations in multithreaded contexts if verbose output is enabled (as noted in the `TimeSeriesSVR` docstring).

L3 MECHANICS
- The method first calls `self._preprocess_sklearn(X, fit_time=False)` (line 367) to validate and reshape the 3D time-series array `X` into a 2D array (`sklearn_X`) that scikit-learn can process.
- It then delegates the computation to the underlying scikit-learn estimator by calling `self.svm_estimator_.decision_function(sklearn_X)` (line 368).
- **State Mutated:** None. The method is read-only with respect to the estimator's state.
- **Failure Conditions:** Raises `NotFittedError` if called before `.fit()`. Raises `ValueError` if `X` cannot be coerced into the expected 3D shape `(n_ts, sz, d)`.

L4 CORRECT MINIMAL USAGE
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Create a deterministic in-memory 3D time-series dataset (n_ts, sz, d)
X_train = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.5], [2.5], [3.5]], 
    [[8.0], [9.0], [10.0]], 
    [[8.5], [9.5], [10.5]]
])
# Binary classification targets
y_train = np.array([0, 0, 1, 1])

# 2. Instantiate and fit the classifier with a valid kernel
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X_train, y_train)

# 3. Evaluate the decision function
scores = clf.decision_function(X_train)

# 4. Verify the output shape for binary classification is (n_samples,)
assert isinstance(scores, np.ndarray)
assert scores.shape == (4,)
print("Decision function scores:", scores)
```

L5 FAILURE FORENSICS
- **Attempt 1 (`InvalidParameterError: The 'kernel' parameter of SVC must be a str... Got 'euclidean' instead`)**: 
  - **Why it failed:** The user instantiated `TimeSeriesSVC(kernel="euclidean")`. The underlying `sklearn.svm.SVC` does not support `"euclidean"` as a kernel string. `tslearn` supports `"gak"` or any standard scikit-learn kernel (`"rbf"`, `"linear"`, etc.).
  - **Source citation:** The failure originates during `.fit()` when `self.svm_estimator_` is initialized or fitted (around line 328), passing the invalid kernel down to scikit-learn.
- **Attempt 2 (`AssertionError: Expected shape (8, 6), got (8, 4)`)**:
  - **Why it failed:** The test logic assumed that for a 4-class problem, the decision function would return the One-vs-One (OvO) shape of `n_classes * (n_classes - 1) / 2`, which is `4 * 3 / 2 = 6`. However, modern scikit-learn defaults to `decision_function_shape='ovr'` (One-vs-Rest), which returns a shape of `(n_samples, n_classes)`, resulting in 4 columns.
  - **Source citation:** The docstring explicitly warns about this on lines 365-366: *"If decision_function_shape='ovr', the shape is (n_samples, n_classes)."* The test failed to account for the default `'ovr'` configuration.

L6 SELF-ASSESSMENT
- **Inferences:** 
  - I inferred that `TimeSeriesSVC` is the class containing this method, as the provided source snippet shows `TimeSeriesSVR` immediately following it, and the documentation entry explicitly names `TimeSeriesSVC`.
  - I inferred that the default `decision_function_shape` is `'ovr'` based on standard scikit-learn behavior and the specific numbers in the failed Attempt 2 (`(8, 4)` for 4 classes).
- **Information needed for certainty:** The exact class definition header for `TimeSeriesSVC` and its `__init__` method to confirm default parameter values (like `decision_function_shape`).
- **Confidence Scores:**
  - L2 (Contract): 10/10. The signature, parameters, and return types are explicitly documented in the provided source docstring.
  - L3 (Mechanics): 10/10. The method body is only two lines long and explicitly shows the delegation to `_preprocess_sklearn` and `svm_estimator_.decision_function`.
  - L4 (Minimal Usage): 10/10. The snippet uses standard NumPy arrays and the documented `"gak"` kernel, perfectly matching the required 3D shape and binary classification expectations.