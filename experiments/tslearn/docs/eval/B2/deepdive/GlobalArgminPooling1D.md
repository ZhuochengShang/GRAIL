# Deep-dive: `GlobalArgminPooling1D`

model: google:gemini-3.1-pro-preview · tokens in=5,476 out=4,063 · wall 33s · 2026-09-08 14:35

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as **INTERNAL/FRAMEWORK**. It is a custom neural network layer designed to be used inside `tslearn`'s shapelet-based deep learning models (e.g., `LearningShapelets`). While it is registered as serializable and technically public, end-users typically do not instantiate it directly unless they are constructing custom Keras architectures.

Standalone testability is classified as **NOT TESTABLE IN THIS HARNESS**. The failure history explicitly shows an infrastructure failure (`[fail/infra] missing module/import: No module named 'keras'`). This indicates that the test environment lacks the optional deep-learning dependencies (Keras/TensorFlow) required to even import the module containing this class. 

*Note:* Because this API is an internal neural network component and requires optional heavy dependencies that are not present in the environment, it should be excluded from a main user-facing benchmark denominator.

L1 PURPOSE
`GlobalArgminPooling1D` is a custom Keras neural network layer used within `tslearn`'s shapelet models. It performs a global argmin pooling operation over the temporal dimension (steps) of a 3D time-series tensor. In the context of shapelet learning, after computing the distances between a time series and a set of shapelets across all sliding windows, this layer is used to find the temporal index where the minimum distance (the best match) occurs for each shapelet feature.

L2 CONTRACT
- **Receiver**: An instance of `GlobalArgminPooling1D`, obtained by calling its constructor `GlobalArgminPooling1D(**kwargs)`.
- **Parameters (Constructor)**: Accepts standard Keras `Layer` keyword arguments (`**kwargs`).
- **Parameters (`call` method)**:
  - `inputs`: A 3D tensor of shape `(batch_size, steps, features)`.
  - `mask` (optional): A boolean tensor used to mask out padded timesteps.
- **Return Value**: A 2D tensor of shape `(batch_size, features)` containing the temporal indices (cast to `float`) of the minimum values along the `steps` axis.
- **Visibility**: Public (exported and decorated with `@register_keras_serializable()`).
- **Thread-safety/Laziness**: Inherits the execution properties of the underlying Keras backend. The layer itself is stateless after initialization.

L3 MECHANICS
- **Initialization**: The constructor calls `super().__init__(**kwargs)` and sets `self.input_spec = InputSpec(ndim=3)` to strictly enforce that inputs must be 3D tensors.
- **Shape Computation**: `compute_output_shape` calculates the output shape by dropping the temporal dimension (index 1), returning `(input_shape[0], input_shape[2])`.
- **Forward Pass (`call`)**: 
  - If a `mask` is provided, it computes the maximum value in the `inputs` tensor (`ops.max(inputs)`). It then uses `ops.where(mask, inputs, max_)` to replace masked (invalid) positions with this maximum value, ensuring that padded steps are never selected as the minimum.
  - It computes the argmin along the temporal axis (`ops.argmin(inputs, axis=1)`).
  - Finally, it casts the resulting integer indices to floats (`ops.cast(..., dtype=float)`) and returns them.
- **Delegation**: All tensor operations are delegated to an `ops` module (line 121-124), which acts as a backend-agnostic abstraction (likely Keras Core/Keras 3 `ops`).

L4 CORRECT MINIMAL USAGE
Because the test harness lacks the `keras` dependency required to import the module, this API cannot be executed in this environment. The following snippet demonstrates the correct standalone usage, wrapped in a `try-except` block to prevent the harness from crashing due to the known `ImportError`.

```python
import numpy as np

try:
    from tslearn.shapelets.shapelets import GlobalArgminPooling1D
    
    # 1. Prepare a 3D time-series tensor: (batch_size=1, steps=3, features=1)
    # Using the exact values from the documentation example
    x = np.array([5.0, 6.8, np.inf]).reshape(1, 3, 1)
    
    # 2. Instantiate the pooling layer
    layer = GlobalArgminPooling1D()
    
    # 3. Apply the layer to the 3D input
    output = layer(x)
    
    # 4. Convert the output tensor to a NumPy array for inspection
    output_np = np.array(output)
    
    # 5. Verify the contract
    assert output_np.shape == (1, 1), f"Expected shape (1, 1), got {output_np.shape}"
    assert output_np[0, 0] == 0.0, f"Expected argmin index 0.0, got {output_np[0, 0]}"
    print("GlobalArgminPooling1D correctly found argmin index.")

except ImportError as e:
    print(f"Skipping execution due to missing optional dependency: {e}")
```

L5 FAILURE FORENSICS
- **`[fail/infra] missing module/import: No module named 'keras'`**
  - **Why it failed**: The test environment does not have the `keras` library installed. `tslearn.shapelets.shapelets` relies on Keras for its neural network components (inheriting from `Layer` and using `@register_keras_serializable()`). 
  - **Source Line**: The failure occurs implicitly during the module import phase (e.g., `from tslearn.shapelets.shapelets import GlobalArgminPooling1D`), before any of the actual test code can be executed.

L6 SELF-ASSESSMENT
- **INFERENCE**: I inferred that `Layer`, `InputSpec`, and `register_keras_serializable` are imported from Keras, and that `ops` refers to the Keras backend operations module. This is heavily implied by the failure history and standard deep learning conventions.
- **NEEDED**: The exact import statements at the top of `tslearn/shapelets/shapelets.py` to definitively confirm the backend framework version (e.g., TensorFlow-Keras vs. Keras 3).
- **Confidence L2 (Contract)**: 9/10. The input/output shapes and types are explicitly documented in the docstring and enforced by the code.
- **Confidence L3 (Mechanics)**: 10/10. The logic in the `call` method is straightforward and fully visible in the provided source.
- **Confidence L4 (Usage)**: 9/10. The usage matches the provided docstring example perfectly, though its actual execution is blocked by the environment's missing dependencies.