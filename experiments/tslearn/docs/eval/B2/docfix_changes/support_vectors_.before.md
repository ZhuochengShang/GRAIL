## API Test: `support_vectors_`

### Signature
```python
def support_vectors_(self)
```
_Source: tslearn/tslearn/svm/svm.py:285  (+1 more definition site/overload)_

### Goal
Retrieves the support vectors of a fitted time-series Support Vector Machine (SVM) model, formatted as a 3D time-series array.

### Parameters
- `self`: A fitted instance of a `tslearn` SVM estimator (e.g., `tslearn.svm.TimeSeriesSVC` or `tslearn.svm.TimeSeriesSVR`).

### Input
The estimator must have been successfully fitted on a 3D time-series dataset of shape `(n_ts, max_sz, d)` using `.fit(X, y)`. 

### Output
Returns `unspecified` — A 3D `numpy` array of shape `(n_SV, max_sz, d)` containing the support vectors retained by the model, where `n_SV` is the number of support vectors.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data
X = to_time_series_dataset([[1.0, 2.0], [1.0, 4.0], [9.0, 8.0], [8.0, 9.0]])
y = [0, 0, 1, 1]

# 2. Fit the SVM classifier
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)

# 3. Access the support_vectors_ property (inferred from signature and scikit-learn conventions)
sv = clf.support_vectors_

assert isinstance(sv, np.ndarray)
assert sv.ndim == 3
print(f"Support vectors shape: {sv.shape}")
```

### LLM Instruction Prompt
- Access `support_vectors_` as a property on a fitted `TimeSeriesSVC` or `TimeSeriesSVR` instance. Do not call it as a method (no parentheses).
- Ensure the model is fitted before accessing this property.
- Expect the returned support vectors to be in the strict 3D `tslearn` format `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
Access `support_vectors_` as a property (without parentheses) on a fitted `tslearn.svm.TimeSeriesSVC` or `TimeSeriesSVR` instance to retrieve the support vectors as a 3D numpy array.
```

### Common Failure Modes
- Accessing `support_vectors_` before calling `.fit()`, which raises an `AttributeError` or `NotFittedError`.
- Calling it as a method `clf.support_vectors_()` instead of accessing it as a property `clf.support_vectors_`, which raises a `TypeError` (e.g., `'numpy.ndarray' object is not callable`).
- Fitting the model with 2D data instead of the required 3D `(n_ts, max_sz, d)` format, causing `.fit()` to fail before the property can be accessed.

### Fix Code Hint
```python
# Ensure data is 3D before fitting
X_3d = to_time_series_dataset(X)
clf.fit(X_3d, y)

# Access as a property, not a method
sv = clf.support_vectors_
```