# Deep-dive: `support_vectors_`

model: google:gemini-3.1-pro-preview · tokens in=4,858 out=3,778 · wall 34s · 2026-09-08 15:56

---

An analysis of the `support_vectors_` API in `tslearn.svm.svm`.

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
USER-FACING.
TESTABLE FROM PUBLIC INPUTS.

### L1 PURPOSE
The `support_vectors_` property retrieves the actual time-series support vectors retained by a fitted `TimeSeriesSVC` model. Because `tslearn` preprocesses 3D time-series data into 2D arrays for the underlying `scikit-learn` SVM backend, this property maps the backend's support vector indices back to the original 3D time-series training data, returning them in their original format.

### L2 CONTRACT
**Receiver:** A fitted instance of `TimeSeriesSVC`. (Note: While the documentation implies it might apply to `TimeSeriesSVR`, the implementation relies on `n_support_`, which is specific to classifiers in `scikit-learn`; calling this on an SVR would likely raise an `AttributeError`).

**Parameters:** None (accessed as a property).

**Return Value:** A Python `list` of 3D `numpy.ndarray` objects. Each array in the list contains the support vectors for a specific class and has the shape `(n_SV_c, sz, d)`, where `n_SV_c` is the number of support vectors for that class. 

**Visibility:** Public.

**Thread-Safety/Laziness:** Evaluated eagerly upon access. Not thread-safe if the underlying `_X_fit` or `svm_estimator_` is being mutated concurrently.

### L3 MECHANICS
1. **Validation:** Calls `check_is_fitted(self, '_X_fit')` to ensure the model has been trained and the original training data was retained (line 286).
2. **Initialization:** Creates an empty list `sv` to hold the support vectors (line 287).
3. **Iteration:** Iterates over the number of support vectors per class, which is stored in the underlying `scikit-learn` estimator's `n_support_` attribute (line 289).
4. **Slicing & Mapping:** For each class, it calculates the start and end indices, slices the underlying `support_` array to get the original training indices, and indexes `self._X_fit` to extract the corresponding 3D time series (lines 290-292).
5. **Return:** Appends each class's 3D array to the list and returns the list (lines 292-294).

### L4 CORRECT MINIMAL USAGE
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
assert isinstance(sv, list), f"Expected list, got {type(sv)}"
assert len(sv) == 2, f"Expected 2 classes, got {len(sv)}"
assert isinstance(sv[0], np.ndarray), "List elements should be numpy arrays"
assert sv[0].ndim == 3, "Each class's support vectors should be a 3D array"

print(f"Successfully retrieved support vectors for {len(sv)} classes.")
print(f"Class 0 support vectors shape: {sv[0].shape}")
print(f"Class 1 support vectors shape: {sv[1].shape}")
```

### L5 FAILURE FORENSICS
**Failed Attempt:**
```python
[fail/runtime] AttributeError: 'list' object has no attribute 'ndim'
```
**Why it failed:** The previous test relied on the provided documentation, which incorrectly stated that `support_vectors_` returns a single 3D `numpy` array. The test attempted to check `sv.ndim == 3`. However, the source code (lines 287-294) explicitly constructs and returns a Python `list` of arrays (`sv = [] ... sv.append(...) ... return sv`), with one array per class. A Python `list` does not have an `ndim` attribute, causing the crash.

### L6 SELF-ASSESSMENT
- **Inferences:** 
  - The class defining this property is inferred to be `TimeSeriesSVC` because the snippet cuts off the class declaration, but the `__init__` method (line 258) and the `n_iter_` warning (line 280) explicitly mention `TimeSeriesSVC`.
  - I inferred that this property would fail on `TimeSeriesSVR` because `scikit-learn`'s `SVR` does not have an `n_support_` attribute (which is used on line 289).
- **Information needed for certainty:** The full class declaration line above line 258 to absolutely confirm the class name and its inheritance hierarchy.
- **Confidence Scores:**
  - L2 (Contract): 10/10 — The return type is unambiguously a list of arrays based on the explicit `sv = []` and `sv.append()` logic in the source.
  - L3 (Mechanics): 10/10 — The loop and slicing logic mapping `scikit-learn` indices to `_X_fit` is completely visible in the provided snippet.
  - L4 (Minimal Usage): 10/10 — The usage snippet correctly sets up a 3D array, fits the model, and asserts the true return type, avoiding the documentation's error.