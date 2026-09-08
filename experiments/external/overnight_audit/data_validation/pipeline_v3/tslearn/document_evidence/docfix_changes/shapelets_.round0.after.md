## API Test: `shapelets_`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
@property
def shapelets_(self)
```

### Goal
Retrieves the raw, learned shapelet arrays from a fitted `LearningShapelets` model.

### Parameters
- `self`: A fitted `tslearn.shapelets.LearningShapelets` estimator instance.

### Input
- The estimator must have been successfully fitted using `.fit(X, y)` on a 3D time-series dataset of shape `(n_ts, max_sz, d)`.
- **Precondition**: `tslearn.shapelets` requires an optional deep learning backend (like `keras` or `tensorflow`); any code using it must wrap the import in a `try...except ImportError` block to avoid crashing in environments without these dependencies.

### Output
Returns a 1D NumPy array of `dtype=object` containing the individual shapelet arrays (NOT a Python list). Each element in this array is a NumPy array representing a single learned shapelet of shape `(shapelet_size, d)`, where `shapelet_size` corresponds to the sizes specified in `n_shapelets_per_size` during model initialization, and `d` is the dimensionality of the input time series.

### Valid Call Patterns
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    
    # Prepare a minimal 3D time-series dataset (n_ts, max_sz, d)
    X = np.array([
        [[1.0], [2.0], [3.0], [4.0]], 
        [[3.0], [2.0], [1.0], [0.0]]
    ])
    y = np.array([0, 1])
    
    # Initialize and fit the model
    clf = LearningShapelets(
        n_shapelets_per_size={2: 1}, 
        max_iter=1, 
        optimizer="sgd", 
        random_state=0
    )
    clf.fit(X, y)
    
    # Access the learned shapelets property
    shapelets = clf.shapelets_
    
    # Verify the output contract
    assert isinstance(shapelets, np.ndarray), "Expected a NumPy array"
    assert shapelets.dtype == object, "Expected dtype to be object"
    assert len(shapelets) == 1, "Expected exactly 1 shapelet"
    assert shapelets[0].shape == (2, 1), "Expected shapelet shape to be (2, 1)"
    
    print(f"Successfully retrieved {len(shapelets)} shapelet(s) of shape {shapelets[0].shape}.")

except ImportError as e:
    print(f"Skipping execution: tslearn.shapelets requires a deep learning backend. Details: {e}")
```

### LLM Instruction Prompt
- Wrap the import of `tslearn.shapelets` in a `try...except ImportError` block to handle environments missing the required deep learning backend (e.g., Keras/TensorFlow).
- Ensure the `LearningShapelets` model has been fitted with `.fit(X, y)` before accessing this property.
- Access `shapelets_` as a property (without parentheses), following `scikit-learn` conventions for fitted attributes.
- Expect a 1D NumPy array of `dtype=object`, not a Python list.

### Prompt Snippet
```text
Access `shapelets_` as a property on a fitted `LearningShapelets` instance to retrieve the learned shapelets as a 1D NumPy array of `dtype=object`. Do not call it as a function. Ensure `.fit(X, y)` has been called first. Wrap the import in `try...except ImportError` to handle missing deep learning backends.
```

### Common Failure Modes
- **`[fail/infra] missing module/import: No module named 'keras'`**: Executing `from tslearn.shapelets import LearningShapelets` at the top level without a `try...except ImportError` block crashes in environments lacking a deep learning backend.
- **Type mismatch assumption**: Assuming `shapelets_` returns a Python list. It explicitly allocates and returns a 1D NumPy array of `dtype=object`.
- **Calling as a function**: Attempting to call `clf.shapelets_()` raises a `TypeError` because it evaluates to a NumPy array, which is not callable.
- **Accessing before fitting**: Accessing `clf.shapelets_` before calling `.fit(X, y)` raises `sklearn.exceptions.NotFittedError`.

### Fix Code Hint
```python
# WRONG: Unprotected import, calling as a function, and assuming a list return type
from tslearn.shapelets import LearningShapelets
clf = LearningShapelets(n_shapelets_per_size={2: 1})
clf.fit(X, y)
shapelets = clf.shapelets_() # TypeError: 'numpy.ndarray' object is not callable
assert isinstance(shapelets, list) # AssertionError

# RIGHT: Protected import, property access, and expecting an object array
try:
    from tslearn.shapelets import LearningShapelets
    clf = LearningShapelets(n_shapelets_per_size={2: 1})
    clf.fit(X, y)
    shapelets = clf.shapelets_  # Returns a 1D NumPy array of dtype=object
    assert isinstance(shapelets, np.ndarray) and shapelets.dtype == object
except ImportError:
    pass
```