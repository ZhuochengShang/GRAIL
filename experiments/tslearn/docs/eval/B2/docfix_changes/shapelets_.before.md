## API Test: `shapelets_`

### Signature
```python
def shapelets_(self)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:441_

### Goal
Retrieves the collection of learned shapelet arrays from a fitted `LearningShapelets` model.

### Parameters
- `self`: A fitted `tslearn.shapelets.LearningShapelets` estimator instance.

### Input
- The estimator must have been successfully fitted using `.fit(X, y)` on a 3D time-series dataset of shape `(n_ts, max_sz, d)`.
- **Precondition**: `tslearn.shapelets` requires a deep learning backend (such as TensorFlow/Keras or PyTorch) to be installed in the environment.

### Output
Returns `unspecified` — A list of NumPy arrays. Each array represents a learned shapelet with shape `(shapelet_size, d)`, where `shapelet_size` corresponds to the sizes specified in `n_shapelets_per_size` during model initialization, and `d` is the dimensionality of the input time series.

### Valid Call Patterns
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    from tslearn.utils import to_time_series_dataset

    # 1. Prepare a 3D time-series dataset (n_ts, max_sz, d)
    X = to_time_series_dataset([[1.0, 2.0, 3.0, 4.0], [3.0, 2.0, 1.0, 0.0]])
    y = [0, 1]

    # 2. Initialize and fit the model
    clf = LearningShapelets(
        n_shapelets_per_size={2: 1}, 
        max_iter=1, 
        optimizer="sgd", 
        random_state=0
    )
    clf.fit(X, y)

    # 3. Access the learned shapelets property
    shapelets = clf.shapelets_

    # 4. Verify the output
    assert isinstance(shapelets, list)
    assert len(shapelets) == 1
    assert shapelets[0].shape == (2, 1)
    print(f"Successfully retrieved {len(shapelets)} shapelet(s) of shape {shapelets[0].shape}.")

except ImportError:
    print("Skipping execution: tslearn.shapelets requires a deep learning backend (e.g., TensorFlow/Keras).")
```

### LLM Instruction Prompt
- Access `shapelets_` as a property (without parentheses), following `scikit-learn` conventions for fitted attributes.
- Ensure the `LearningShapelets` model has been fitted with `.fit(X, y)` before accessing this property.
- Be aware that importing `tslearn.shapelets` will fail with an `ImportError` if a compatible deep learning backend is not installed.

### Prompt Snippet
```text
Access `shapelets_` as a property on a fitted `LearningShapelets` instance to retrieve the learned shapelets as a list of NumPy arrays. Do not call it as a function. Ensure `.fit(X, y)` has been called first.
```

### Common Failure Modes
- **Calling as a function**: Attempting to call `clf.shapelets_()` raises a `TypeError` because it evaluates to a list of arrays, which is not callable.
- **Accessing before fitting**: Accessing `clf.shapelets_` before calling `.fit(X, y)` raises an `AttributeError` or `NotFittedError`.
- **Missing Dependencies**: Attempting to use `LearningShapelets` without TensorFlow/Keras or PyTorch installed raises an `ImportError`.

### Fix Code Hint
```python
# WRONG: Calling as a function or accessing before fit
clf = LearningShapelets(n_shapelets_per_size={2: 1})
# shapelets = clf.shapelets_()  # TypeError: 'list' object is not callable

# RIGHT: Access as a property after fitting
clf.fit(X, y)
shapelets = clf.shapelets_  # Returns a list of NumPy arrays
```