# Deep-dive: `PatchingLayer`

model: google:gemini-3.1-pro-preview · tokens in=5,586 out=3,301 · wall 29s · 2026-09-08 14:49

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
This API is classified as **INTERNAL/FRAMEWORK**. It is a Keras `Layer` subclass designed specifically to format data internally for `tslearn`'s shapelet learning algorithms (e.g., `LearningShapelets`). It should be excluded from the main user-facing benchmark denominator.

Standalone testability is classified as **NOT TESTABLE IN THIS HARNESS**. The failure history explicitly shows that importing `PatchingLayer` or its module raises `ModuleNotFoundError: No module named 'keras'` (and similarly for `tensorflow`). Because `tslearn`'s shapelet module relies on Keras/TensorFlow as a hard dependency for its neural network layers (evident from `@register_keras_serializable()` and `class PatchingLayer(Layer)`), it cannot be instantiated or executed in an environment where these optional dependencies are missing.

**L1 PURPOSE**
`PatchingLayer` is a neural network layer used within `tslearn`'s shapelet-learning models to preprocess time-series data. It sits at the beginning of the shapelet distance computation graph, taking a batch of 3D time-series tensors and slicing them into sliding windows (patches) of a specific length. This transforms the temporal sequence into a 4D tensor of patches, which can then be compared against learned shapelet weights (e.g., via `LocalSquaredDistanceLayer`).

**L2 CONTRACT**
- **Receiver Type**: `PatchingLayer`, a subclass of Keras `Layer`.
- **Instantiation**: `PatchingLayer(shapelet_length: int, **kwargs)`
- **Parameters**:
  - `shapelet_length` (int): The length of the sliding window patches to extract from the time series.
  - `**kwargs`: Additional keyword arguments passed up to the Keras `Layer` base class (e.g., `name`, `dtype`).
- **Input**: A 3D tensor or NumPy array of shape `(batch_size, steps, features)`.
- **Return Value**: A 4D tensor of shape `(batch_size, steps - shapelet_length + 1, shapelet_length, features)`.
- **Visibility**: Publicly exported in `tslearn.shapelets`, but intended as an internal framework component.
- **Thread-safety/Laziness**: Inherits the thread-safety and execution semantics of a Keras `Layer` (e.g., eager execution or graph compilation depending on the backend).

**L3 MECHANICS**
- **Initialization**: Sets `self.shapelet_length` and defines `self.input_spec = InputSpec(ndim=3)` to enforce 3D inputs (tslearn/tslearn/shapelets/shapelets.py:138-141).
- **Shape Computation**: `compute_output_shape` calculates the number of valid sliding windows as `steps - shapelet_length + 1` (line 146).
- **Forward Pass (`call`)**: 
  1. Extracts the dynamic shape `(n_ts, sz, d)` using `ops.shape`.
  2. Flattens the time and feature dimensions using `ops.reshape(inputs, (n_ts, sz * d))`.
  3. Delegates to `ops.extract_sequences` to slice the flattened array into overlapping sequences of size `shapelet_length * d` with a stride of `d`.
  4. Reshapes the extracted sequences back into the 4D patch format `(n_ts, sz - shapelet_length + 1, shapelet_length, d)`.
- **Serialization**: `get_config` merges `shapelet_length` into the base layer's configuration dictionary to support Keras model saving/loading (line 160).

**L4 CORRECT MINIMAL USAGE**
Because the required `keras` dependency is missing from the harness environment, this API cannot be successfully executed here. The following snippet demonstrates the correct minimal usage that *would* execute in a properly configured environment, guarded by a `try/except` block to prevent harness crashes.

```python
import numpy as np

try:
    from tslearn.shapelets import PatchingLayer
    
    # 1. Instantiate the layer with a specific shapelet length
    layer = PatchingLayer(shapelet_length=3)
    
    # 2. Create a dummy 3D time-series batch: (batch_size=2, steps=10, features=1)
    X_np = np.zeros((2, 10, 1), dtype=np.float32)
    
    # 3. Pass the data through the layer
    out = layer(X_np)
    
    # 4. Verify the output shape: (batch_size, steps - shapelet_length + 1, shapelet_length, features)
    # (2, 10 - 3 + 1, 3, 1) -> (2, 8, 3, 1)
    assert out.shape == (2, 8, 3, 1)
    print(f"__CHECK__ PatchingLayer output shape: {out.shape}")

except ImportError as e:
    print(f"__CHECK__ Skipping execution due to missing optional dependency: {e}")
```

**L5 FAILURE FORENSICS**
- **Attempt 1 (`import tensorflow as tf`)**: Failed with `No module named 'tensorflow'`. The test environment does not have TensorFlow installed, which is an optional dependency for `tslearn` but a hard requirement for its shapelet neural network layers.
- **Attempt 2 (`from tslearn.shapelets import PatchingLayer`)**: Failed with `No module named 'keras'`. Even without explicitly importing TensorFlow, importing `PatchingLayer` triggers the evaluation of `@register_keras_serializable()` and `class PatchingLayer(Layer)`, which internally attempt to import Keras/TensorFlow base classes.

**L6 SELF-ASSESSMENT**
- **Inferences**: 
  - `ops` is inferred to be a backend abstraction layer within `tslearn` (likely wrapping TensorFlow, Keras, or NumPy operations) that provides functions like `extract_sequences` and `reshape`.
  - The missing `Layer` and `InputSpec` base classes are inferred to be standard Keras imports (`keras.layers.Layer`, `keras.layers.InputSpec`).
- **Information needed for certainty**: The exact implementation of `ops.extract_sequences` to confirm how strides and padding are handled at the backend level.
- **Confidence Scores**:
  - **L2 (Contract)**: 10/10. The input/output shapes and parameters are explicitly defined in the docstring and `compute_output_shape`.
  - **L3 (Mechanics)**: 9/10. The sequence of operations is clear from the `call` method, though the exact backend implementation of `ops` is abstracted.
  - **L4 (Usage)**: 9/10. The usage is syntactically and logically correct based on Keras layer conventions, though execution is blocked by environment constraints.