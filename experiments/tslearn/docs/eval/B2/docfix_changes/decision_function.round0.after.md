## API Test: `decision_function`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def decision_function(self, X)
```

### Goal
Evaluates the decision function (e.g., distance to the separating hyperplane) for a set of time series using a fitted `TimeSeriesSVC` classifier. Included in the main user-facing denominator.

### Parameters
- `self`: A fitted instance of `tslearn.svm.TimeSeriesSVC`.
- `X`: The time-series dataset to evaluate, formatted as a 3D array-like of shape `(n_ts, sz, d)`.

### Input
- `X` must be strictly formatted as a 3D `numpy` array of shape `(n_ts, sz, d)`.
- The estimator instance (`self`) must be instantiated with a valid kernel (e.g., `"gak"`, `"rbf"`, `"linear"`) and fitted with `.fit(X, y)` before calling this method. `TimeSeriesSVC` does not accept `"euclidean"` as a kernel.

### Output
Returns a `numpy.ndarray` representing the decision function scores. For binary classification, it returns a 1D array of shape `(n_samples,)`, not a 2D array. For multi-class classification, the shape is `(n_samples, n_classes * (n_classes-1) / 2)` by default, or `(n_samples, n_classes)` if configured with `decision_function_shape='ovr'`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

X_train = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.5], [2.5], [3.5]], 
    [[8.0], [9.0], [10.0]], 
    [[8.5], [9.5], [10.5]]
])
y_train = np.array([0, 0, 1, 1])

clf = TimeSeriesSVC(kernel="gak")
clf.fit(X_train, y_train)

X_test = np.array([
    [[1.2], [2.2], [3.2]], 
    [[8.2], [9.2], [10.2]]
])
scores = clf.decision_function(X_test)

assert isinstance(scores, np.ndarray)
assert scores.shape == (2,)
```

### LLM Instruction Prompt
- Instantiate `TimeSeriesSVC` with a valid kernel like `"gak"` (Global Alignment Kernel) or standard `sklearn` kernels like `"rbf"` or `"linear"`. Never use `"euclidean"`.
- Call `.fit(X_train, y_train)` on the estimator before calling `decision_function`.
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, sz, d)`.
- Expect a 1D array of shape `(n_samples,)` when evaluating binary classification tasks.

### Prompt Snippet
```python
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X_train, y_train)
decision_scores = clf.decision_function(X_test)
```

### Common Failure Modes
- **`InvalidParameterError` (Invalid Kernel)**: Occurs if instantiating `TimeSeriesSVC(kernel="euclidean")`. `"euclidean"` is not a valid kernel string for SVMs. Valid options are `"gak"` or standard `sklearn.svm.SVC` kernels.
- **`NotFittedError`**: Occurs if `decision_function` is called before the model has been fitted with `.fit()`.
- **`ValueError: Expected 3D array`**: Occurs if `X` is passed as a 1D or 2D array. `tslearn` strictly requires the `(n_ts, sz, d)` format.

### Fix Code Hint
```python
# WRONG: Using an invalid kernel string like "euclidean"
# clf = TimeSeriesSVC(kernel="euclidean")
# clf.fit(X_train, y_train)
# scores = clf.decision_function(X_test)

# RIGHT: Use a valid kernel like "gak" and ensure the model is fitted
from tslearn.svm import TimeSeriesSVC

clf = TimeSeriesSVC(kernel="gak")
clf.fit(X_train, y_train)
scores = clf.decision_function(X_test)
```