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
- The estimator instance (`self`) must be instantiated with a valid kernel (e.g., `"gak"`, `"rbf"`, `"linear"`) and fitted with `.fit(X, y)` before calling this method. `"euclidean"` is strictly invalid and will cause an `InvalidParameterError`.

### Output
Returns a `numpy.ndarray` representing the decision function scores. For binary classification, it returns a 1D array of shape `(n_samples,)`. For multi-class classification, the default `decision_function_shape` is `'ovr'`, meaning the default return shape is `(n_samples, n_classes)`, not the OvO shape `(n_samples, n_classes * (n_classes-1) / 2)`.

### Valid Call Patterns
```python
import numpy
from tslearn.svm import TimeSeriesSVC

X = numpy.random.rand(8, 5, 2)
y = numpy.array([0, 1, 2, 3, 0, 1, 2, 3])

clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)

scores = clf.decision_function(X)
assert scores.shape == (8, 4)
```

### LLM Instruction Prompt
- Instantiate `TimeSeriesSVC` with a valid kernel like `"gak"`, `"rbf"`, or `"linear"`. Never use `"euclidean"`.
- Call `.fit(X, y)` on the estimator before calling `decision_function`.
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, sz, d)`.
- Expect a 1D array of shape `(n_samples,)` for binary classification, and `(n_samples, n_classes)` for multiclass classification because the default `decision_function_shape` is `'ovr'`.

### Prompt Snippet
```python
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)
scores = clf.decision_function(X)
```

### Common Failure Modes
- **`AssertionError` on output shape**: Occurs when assuming the default multiclass return shape is the OvO shape `(n_samples, n_classes * (n_classes-1) / 2)`. Modern scikit-learn defaults to `decision_function_shape='ovr'`, so the actual default shape is `(n_samples, n_classes)`.
- **`InvalidParameterError` (Invalid Kernel)**: Occurs if instantiating `TimeSeriesSVC(kernel="euclidean")`. `"euclidean"` is strictly invalid for SVMs. Valid options are `"gak"` or standard `sklearn.svm.SVC` kernels.
- **`NotFittedError`**: Occurs if `decision_function` is called before the model has been fitted with `.fit()`.
- **`ValueError: Expected 3D array`**: Occurs if `X` is passed as a 1D or 2D array. `tslearn` strictly requires the `(n_ts, sz, d)` format.

### Fix Code Hint
```python
# WRONG: Using an invalid kernel and assuming OvO shape for 4 classes
# clf = TimeSeriesSVC(kernel="euclidean")
# clf.fit(X, y)
# scores = clf.decision_function(X)
# assert scores.shape == (8, 6) # 4 * 3 / 2 = 6

# RIGHT: Use a valid kernel like "gak" and expect 'ovr' shape (n_samples, n_classes)
import numpy
from tslearn.svm import TimeSeriesSVC

clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)
scores = clf.decision_function(X)
assert scores.shape == (8, 4)
```