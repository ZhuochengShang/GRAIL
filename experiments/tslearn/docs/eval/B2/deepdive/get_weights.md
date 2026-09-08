# Deep-dive: `get_weights`

model: google:gemini-3.1-pro-preview · tokens in=5,762 out=2,740 · wall 25s · 2026-09-08 15:31

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** USER-FACING
- **Testability:** TESTABLE FROM PUBLIC INPUTS (with dependency handling)
- **Explanation:** The `get_weights` method is a public API on the `LearningShapelets` estimator, intended for users to inspect the learned shapelets and classification weights. It is fully testable from public inputs by instantiating `LearningShapelets`, fitting it on a small dummy dataset, and calling the method. However, because `LearningShapelets` relies on Keras/TensorFlow (which the failure history shows is missing in the test harness), the test must gracefully catch the `ImportError` to be executable in this specific environment.

**L1 PURPOSE**
The `get_weights` method allows users to extract the learned parameters (weights) from the underlying neural network used by the `LearningShapelets` estimator. It sits at the end of the training data flow, providing a bridge between the high-level scikit-learn-compatible estimator and the low-level Keras model, enabling inspection of the discovered shapelets and the final classification layer.

**L2 CONTRACT**
- **Receiver:** A fitted `LearningShapelets` instance. Obtained by importing `tslearn.shapelets.LearningShapelets`, initializing it, and calling `.fit(X, y)`.
- **Parameters:**
  - `layer_name` (`str` or `None`, default: `None`): The name of the specific layer to retrieve weights for. If `None`, all model weights are returned. Valid layer names include `"classification"` and `"shapelets_i"` (where `i` is the shapelet size index).
- **Returns:** A `list` of `numpy.ndarray` objects containing the requested weights.
- **Visibility:** Public.
- **State/Side Effects:** Read-only; does not mutate the estimator's state.

**L3 MECHANICS**
- The method checks if `layer_name` is `None`.
- If `None`, it delegates directly to the underlying Keras model via `self.model_.get_weights()` (line 862).
- If a `layer_name` is provided, it retrieves the specific layer using `self.model_.get_layer(layer_name)` and then calls `.get_weights()` on that layer (line 864).
- It assumes `self.model_` has been constructed and compiled, which happens during the `.fit()` method. Calling this before `.fit()` will raise an `AttributeError` because `self.model_` will not exist.
- Passing a non-existent `layer_name` will cause the underlying Keras `get_layer` method to raise a `ValueError`.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    HAS_KERAS = True
except ImportError:
    HAS_KERAS = False

if HAS_KERAS:
    # 1. Prepare deterministic 3D time-series data (n_ts, max_sz, d)
    X = np.array([[[1.0], [2.0], [3.0], [4.0]], 
                  [[1.5], [2.5], [3.5], [4.5]], 
                  [[9.0], [8.0], [7.0], [6.0]]])
    y = np.array([0, 0, 1])

    # 2. Initialize and fit the estimator
    clf = LearningShapelets(n_shapelets_per_size={2: 2}, max_iter=1, random_state=42)
    clf.fit(X, y)

    # 3. Retrieve weights
    all_weights = clf.get_weights()
    cls_weights = clf.get_weights("classification")
    shp_weights = clf.get_weights("shapelets_0")

    # 4. Assert properties
    assert isinstance(all_weights, list), "Weights should be returned as a list."
    assert isinstance(cls_weights, list), "Classification weights should be a list."
    assert len(cls_weights) > 0, "Classification weights list should not be empty."

    print(f"Retrieved {len(all_weights)} total weight arrays.")
    print(f"Classification weights shape: {cls_weights[0].shape}")
else:
    print("Keras not installed; skipping test gracefully.")
```

**L5 FAILURE FORENSICS**
- **`[fail/infra] missing module/import: No module named 'keras'`**: This failure occurred because the test harness environment lacks the `keras` (or `tensorflow`) dependency. The `tslearn.shapelets` module heavily relies on Keras to build the neural network architecture for learning shapelets. When the test attempted to import `LearningShapelets`, the internal imports within `tslearn` failed, raising an `ImportError`. The fix is to conditionally skip the test logic if the dependency is missing, as demonstrated in L4.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - The class owning this method is `LearningShapelets`. This is heavily implied by the examples in the docstring (`clf = LearningShapelets(...)`) and the surrounding source code referencing shapelet-specific logic (`self._n_shapelet_sizes`).
  - The underlying `self.model_` is a Keras `Model` object, inferred from the method calls (`get_layer`, `get_weights`) and the failure history mentioning `keras`.
- **Information needed for certainty:** Confirmation of the exact Keras version supported (e.g., standalone `keras` vs `tensorflow.keras`), though the API surface used here (`get_weights`, `get_layer`) is stable across both.
- **Confidence Scores:**
  - **L2 (Contract): 10/10** - The docstring explicitly defines the parameters, types, and return values.
  - **L3 (Mechanics): 10/10** - The source code for the method is provided and consists of a simple conditional delegation to Keras.
  - **L4 (Minimal Usage): 9/10** - The usage is correct according to the API, but relies on a `try/except` block to bypass the infrastructure limitation (missing Keras) in the test harness.