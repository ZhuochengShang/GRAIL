# Deep-dive: `set_weights`

model: google:gemini-3.1-pro-preview · tokens in=5,124 out=3,547 · wall 31s · 2026-09-08 15:54

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification**: USER-FACING
- **Testability**: NOT TESTABLE IN THIS HARNESS
- **Explanation**: The `set_weights` method is a public API intended for users to manually inspect or transfer weights in a `LearningShapelets` model. However, as evidenced by the failure history (`[fail/infra] missing module/import: No module named 'keras'`), the `tslearn.shapelets` module heavily depends on Keras/TensorFlow for its underlying neural network architecture. Because the execution harness lacks this dependency, the API cannot be successfully executed. It should be excluded from a main user-facing benchmark denominator that assumes a pure NumPy/SciPy/scikit-learn environment. A `try/except` block is provided below to gracefully bypass the missing dependency while demonstrating correct usage.

**L1 PURPOSE**
The `set_weights` method allows users to manually inject or update the neural network weights of a `LearningShapelets` estimator. It sits in the model manipulation and inspection flow, typically used after the model has been fitted (which constructs the architecture) to transfer weights, manually tweak shapelets, or restore a specific state.

**L2 CONTRACT**
- **Receiver**: A `LearningShapelets` instance. Obtained by instantiating `tslearn.shapelets.LearningShapelets(...)` and typically calling `.fit(X, y)` to initialize the underlying Keras model architecture.
- **Parameters**:
  - `weights` (`list` of `ndarray`): The weights to assign to the target layer or the entire model. The shapes of the arrays must exactly match the expected dimensions of the target layer.
  - `layer_name` (`str` or `None`, default `None`): The name of the specific layer to update. If `None`, all model weights are set. Valid layer names include `"shapelets_i_j"` (where `i` is the shapelet ID and `j` is the dimension) and `"classification"` (for the final classification layer).
- **Return Value**: Returns the result of the underlying Keras `set_weights` call (which is typically `None`). The operation mutates the estimator's internal neural network weights in place.
- **Visibility**: Public.
- **Thread-Safety/Laziness**: Not thread-safe (mutates internal Keras model state). Eagerly applied.

**L3 MECHANICS**
- **Algorithm/Delegation**: The method acts as a direct proxy to the underlying Keras model (`self.model_`). 
  - If `layer_name` is `None`, it delegates to `self.model_.set_weights(weights)` (line 901).
  - If `layer_name` is provided, it fetches the specific layer via `self.model_.get_layer(layer_name)` and delegates to its `set_weights(weights)` method (line 903).
- **State Mutated**: Modifies the internal weights of the Keras model stored in `self.model_`.
- **Failure Conditions**: 
  - Raises `AttributeError` or Keras-level errors if called before the model is built (e.g., before `.fit()`).
  - Raises a Keras `ValueError` if the shapes of the provided `weights` list do not match the expected shapes of the target layer.
  - Raises a Keras `ValueError` if `layer_name` is provided but does not exist in the model.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    from tslearn.utils import to_time_series_dataset
    
    # 1. Prepare minimal 3D time-series data (n_ts, max_sz, d)
    X = to_time_series_dataset([[1.0, 2.0, 3.0, 4.0], [3.0, 2.0, 1.0, 0.0]])
    y = [0, 1]
    
    # 2. Initialize and fit the model to build the underlying Keras architecture
    clf = LearningShapelets(n_shapelets_per_size={3: 1}, max_iter=1, random_state=0)
    clf.fit(X, y)
    
    # 3. Define new weights as a list of ndarrays
    weights_shapelet = [np.array([[[1.0], [2.0], [3.0]]])]
    
    # 4. Set the weights for the specific shapelet layer
    clf.set_weights(weights_shapelet, layer_name="shapelets_0")
    
    # 5. Verify the weights were updated
    np.testing.assert_allclose(
        clf.shapelets_as_time_series_[0], 
        np.array([[1.], [2.], [3.]])
    )
    print("Correctness witness: Weights successfully set.")

except ImportError as e:
    # Gracefully handle the missing Keras dependency in the test harness
    print(f"Correctness witness: Skipped due to missing dependency - {e}")
```

**L5 FAILURE FORENSICS**
- **`[fail/infra] missing module/import: No module named 'keras'`**: This failure occurred because `tslearn.shapelets.LearningShapelets` relies on Keras (and by extension, TensorFlow) to construct and train its neural network backend. The execution harness does not have `keras` installed, causing an `ImportError` or `ModuleNotFoundError` as soon as the module is imported or the estimator is instantiated.

**L6 SELF-ASSESSMENT**
- **Inferences**: 
  - I inferred that `self.model_` is a Keras model based on the method calls (`get_layer`, `set_weights`, `to_json`, `model_from_json` on lines 901-972) and the explicit failure history mentioning `keras`.
  - I inferred that the return value is effectively `None`, as that is the standard behavior of Keras's `set_weights` method, despite the source code using `return self.model_.set_weights(...)`.
- **Information needed for certainty**: Verification of the exact Keras/TensorFlow version requirements for `tslearn` to ensure the mock/try-except block perfectly aligns with the library's internal imports.
- **Confidence Scores**:
  - **L2 (Contract)**: 10/10. The parameters and types are explicitly defined in the docstring and source code.
  - **L3 (Mechanics)**: 10/10. The delegation logic is trivial and explicitly visible on lines 900-903.
  - **L4 (Usage)**: 9/10. The usage perfectly mirrors the provided docstring example, with a necessary `try/except` wrapper to handle the known infrastructure limitation.