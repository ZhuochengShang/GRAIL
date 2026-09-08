## API Test: `decision_function`

### Signature
```python
def decision_function(self, X)
```
_Source: tslearn/tslearn/svm/svm.py:352_

_Source doc:_ Evaluates the decision function for the samples in X. Parameters ---------- X : array-like of shape=(n_ts, sz, d) Time series dataset. Returns ------- ndarray of shape (n_samples, n_classes * (n_classes-1) / 2) Returns the decision function of the sample for each class in the model. If decision_function_shape='ovr', the shape is (n_samples, n_classes).

### Goal
Evaluates the decision function (e.g., the distance to the separating hyperplane) for each class in a fitted time-series support vector machine model.

### Parameters
- `self`: A fitted instance of a `tslearn` classifier that supports decision functions (e.g., `TimeSeriesSVC`).
- `X`: The time-series dataset to evaluate, formatted as a 3D array-like of shape `(n_ts, sz, d)`.

### Input
- `X` must be strictly formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. If starting from raw lists or variable-length sequences, it must be converted using `tslearn.utils.to_time_series_dataset` first.
- The estimator instance (`self`) must be fitted with training data before calling this method.

### Output
Returns `unspecified` — A `numpy.ndarray` representing the decision function scores for the samples in `X`. The shape is `(n_samples, n_classes * (n_classes-1) / 2)` by default, or `(n_samples, n_classes)` if the estimator was configured with `decision_function_shape='ovr'`. For binary classification, it typically returns a 1D array of shape `(n_samples,)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Prepare deterministic 3D time-series data (n_ts, max_sz, d)
X_train = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.5], [2.5], [3.5]], 
    [[8.0], [9.0], [10.0]], 
    [[8.5], [9.5], [10.5]]
])
y_train = np.array([0, 0, 1, 1])

# 2. Initialize and fit the classifier
clf = TimeSeriesSVC(kernel="euclidean")
clf.fit(X_train, y_train)

# 3. Evaluate the decision function on new 3D data
X_test = np.array([
    [[1.2], [2.2], [3.2]], 
    [[8.2], [9.2], [10.2]]
])
scores = clf.decision_function(X_test)

assert isinstance(scores, np.ndarray)
assert scores.shape[0] == X_test.shape[0]
print("Decision function scores:\n", scores)
```
_Note: This example is inferred from the signature and standard `tslearn` / `scikit-learn` conventions, as no verbatim example was found in the context._

### LLM Instruction Prompt
- Call `decision_function` as an instance method on a fitted classifier (like `TimeSeriesSVC`), never as a standalone function.
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists or variable-length sequences before passing them to this method.
- Do not call this method before calling `.fit()` on the estimator.

### Prompt Snippet
```text
# Evaluate the decision function on the test set
# Ensure X_test is a 3D array (n_ts, max_sz, d)
decision_scores = clf.decision_function(X_test)
```

### Common Failure Modes
- **`ValueError: Expected 3D array`**: Occurs if `X` is passed as a 1D or 2D array. `tslearn` strictly requires the `(n_ts, max_sz, d)` format.
- **`NotFittedError`**: Occurs if `decision_function` is called before the model has been fitted with `.fit()`.
- **`AttributeError`**: Occurs if attempting to call `decision_function` as a standalone function from the module rather than as a method on an instantiated estimator.

### Fix Code Hint
```python
# WRONG: Passing a 2D array or calling before fitting
# scores = clf.decision_function([[1, 2], [3, 4]])

# RIGHT: Convert to 3D array and ensure the model is fitted
from tslearn.utils import to_time_series_dataset

X_test_3d = to_time_series_dataset([[1, 2], [3, 4]])
# clf.fit(X_train_3d, y_train) # Must be called first
scores = clf.decision_function(X_test_3d)
```