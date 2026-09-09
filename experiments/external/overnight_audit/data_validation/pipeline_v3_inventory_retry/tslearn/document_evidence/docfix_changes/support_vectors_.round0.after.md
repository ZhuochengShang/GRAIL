## API Test: `support_vectors_`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def support_vectors_(self)
```

### Goal
Retrieves the support vectors of a fitted time-series Support Vector Classifier (`TimeSeriesSVC`), returning them as a list of 3D time-series arrays (one array per class).

### Parameters
- `self`: A fitted instance of `tslearn.svm.TimeSeriesSVC`. (Note: Do not use `TimeSeriesSVR`, as its underlying scikit-learn backend lacks the `n_support_` attribute required by this property).

### Input
The `TimeSeriesSVC` estimator must have been successfully fitted on a 3D time-series dataset of shape `(n_ts, max_sz, d)` using `.fit(X, y)`. 

### Output
Returns a Python `list` of 3D `numpy.ndarray` objects. Each array in the list contains the support vectors for a specific class and has the shape `(n_SV_c, max_sz, d)`, where `n_SV_c` is the number of support vectors for that class.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Create a minimal 3D time-series dataset (n_ts, sz, d)
X = np.array([
    [[1.0]], [[2.0]], [[1.5]],  # Class 0
    [[8.0]], [[9.0]], [[8.5]]   # Class 1
])
y = np.array([0, 0, 0, 1, 1, 1])

# 2. Fit the TimeSeriesSVC
clf = TimeSeriesSVC(kernel="gak", random_state=42)
clf.fit(X, y)

# 3. Access the support_vectors_ property
sv = clf.support_vectors_

# 4. Verify the contract (it returns a list of arrays, not a single array)
assert isinstance(sv, list), "support_vectors_ should be a list"
assert len(sv) == 2, "Expected 2 classes"
assert isinstance(sv[0], np.ndarray), "Elements of the list should be numpy arrays"
assert sv[0].ndim == 3, "Each class's support vectors should be a 3D array"

print(f"__CHECK__ support_vectors_ list length {len(sv)}")
```

### LLM Instruction Prompt
- Access `support_vectors_` as a property (no parentheses) on a fitted `TimeSeriesSVC` instance.
- Expect the return value to be a Python `list` of 3D `numpy.ndarray` objects, not a single array.
- Iterate or index into the list to access the `(n_SV_c, max_sz, d)` support vectors for each specific class.
- Do not use this property on `TimeSeriesSVR`, as it will raise an `AttributeError`.

### Prompt Snippet
```text
Access `clf.support_vectors_` as a property on a fitted `tslearn.svm.TimeSeriesSVC` to retrieve a list of 3D numpy arrays, where each array contains the support vectors for a specific class.
```

### Common Failure Modes
- Assuming `support_vectors_` returns a single numpy array and attempting to access `.ndim` or `.shape` directly on the returned object, resulting in `AttributeError: 'list' object has no attribute 'ndim'` or `'shape'`.
- Attempting to access this property on a `TimeSeriesSVR` instance, which fails because the underlying scikit-learn SVR lacks the `n_support_` attribute.
- Accessing `support_vectors_` before calling `.fit()`, which raises a `NotFittedError`.

### Fix Code Hint
```python
# WRONG: Assuming a single array is returned
sv = clf.support_vectors_
print(sv.ndim) # AttributeError: 'list' object has no attribute 'ndim'

# CORRECT: Handling the list of arrays (one per class)
sv = clf.support_vectors_
assert isinstance(sv, list)
for class_idx, class_sv in enumerate(sv):
    print(f"Class {class_idx} support vectors shape: {class_sv.shape}")
```