# Deep-dive: `GlobalMinPooling1D`

model: google:gemini-3.1-pro-preview · tokens in=5,587 out=4,221 · wall 35s · 2026-09-08 14:36

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** ADVANCED/LOW-LEVEL
- **Testability:** NOT TESTABLE IN THIS HARNESS
- **Explanation:** `GlobalMinPooling1D` is a custom neural network layer used for building shapelet-based models. The failure history explicitly shows `[fail/infra] missing module/import: No module named 'keras'`, indicating that the required Keras/TensorFlow backend is not installed in the test environment. Because the class inherits from a Keras `Layer` (which is evaluated at import time), it cannot be instantiated or executed in this harness without catching the `ImportError`. It should be excluded from the main user-facing benchmark denominator as it is a backend-specific framework component rather than a standalone time-series algorithm.

**L1 PURPOSE**
`GlobalMinPooling1D` is a custom Keras neural network layer designed to perform global minimum pooling over the temporal dimension (steps) of a 3D time-series tensor. In the context of `tslearn`'s shapelet learning, it is used to aggregate the pairwise distances between local time-series patches and learned shapelets, extracting the minimum distance (the best match) across all sliding windows for each shapelet.

**L2 CONTRACT**
- **Receiver:** A Keras `Layer` instance, obtained by calling `GlobalMinPooling1D(**kwargs)`.
- **Parameters:**
  - `**kwargs`: Standard Keras layer keyword arguments (e.g., `name`, `dtype`, `trainable`).
- **Call Arguments:**
  - `inputs`: A 3D tensor of shape `(batch_size, steps, features)` representing the input time series or distance sequences.
  - `mask` (optional): A boolean tensor of the same spatial dimensions indicating valid time steps.
- **Return Value:** A 2D tensor of shape `(batch_size, features)` containing the minimum values across the `steps` dimension (axis 1).
- **Visibility:** Public (exported as part of the shapelets module), but primarily intended for internal use or advanced users building custom Keras models.
- **Thread-safety/Laziness:** Inherits Keras layer semantics; execution is deferred when building symbolic graphs, or eager if running eagerly.

**L3 MECHANICS**
- The layer specifies its input requirements via `self.input_spec = InputSpec(ndim=3)` (line 84).
- `compute_output_shape` (line 86) calculates the output shape by dropping the middle dimension (steps), returning `(input_shape[0], input_shape[2])`.
- In `call` (line 89), if a `mask` is provided, it computes the maximum value of the entire `inputs` tensor using `ops.max(inputs)`. It then uses `ops.where(mask, inputs, max_)` to replace masked-out (invalid) steps with this maximum value, ensuring they are never selected as the minimum.
- Finally, it delegates to `ops.min(inputs, axis=1)` to compute the minimum across the temporal dimension.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np

# We must wrap the import in a try-except block because Keras is a soft 
# dependency in tslearn and is known to be missing in this harness.
try:
    from tslearn.shapelets.shapelets import GlobalMinPooling1D
    HAS_KERAS = True
except ImportError:
    HAS_KERAS = False

if HAS_KERAS:
    # 1. Prepare a 3D input tensor (batch_size=1, steps=3, features=1)
    x = np.array([5.0, 6.8, 10.0]).reshape(1, 3, 1)
    
    # 2. Instantiate the pooling layer
    pool_layer = GlobalMinPooling1D()
    
    # 3. Apply the layer to the temporal data
    output = pool_layer(x)
    
    # 4. Convert output to NumPy array for inspection
    if hasattr(output, "numpy"):
        output_np = output.numpy()
    else:
        output_np = np.asarray(output)
        
    assert output_np.shape == (1, 1)
    assert output_np[0, 0] == 5.0
    print("GlobalMinPooling1D output:", output_np)
else:
    print("Keras is not installed; skipping execution.")
```

**L5 FAILURE FORENSICS**
- **Failure 1:** `[fail/infra] missing module/import: No module named 'keras'`
  - **Reason:** The test environment lacks the `keras` library, which is a soft dependency for `tslearn.shapelets`. The import `from tslearn.shapelets.shapelets import GlobalMinPooling1D` fails immediately because the module internally imports Keras components (like `Layer` and `InputSpec`) to define the class inheritance.

**L6 SELF-ASSESSMENT**
- **Inferences:**
  - `ops` refers to Keras backend operations (`keras.ops` in Keras 3 or a TensorFlow backend wrapper).
  - `Layer` and `InputSpec` are imported from Keras.
  - The layer is used specifically for aggregating patch distances in `LearningShapelets` (inferred from the domain and surrounding classes like `LocalSquaredDistanceLayer`).
- **Missing Info:** The exact imports at the top of `tslearn.shapelets.shapelets` (lines 1-35) to confirm exactly where `Layer`, `InputSpec`, and `ops` are imported from.
- **Confidence Scores:**
  - L2 (Contract): 9/10 - The contract is clearly defined by the Keras layer API and the provided source code, though the exact tensor types depend on the active backend.
  - L3 (Mechanics): 10/10 - The mechanics are explicitly visible in the `call` and `compute_output_shape` methods.
  - L4 (Usage): 9/10 - The usage snippet is standard Keras layer usage and handles the missing dependency gracefully.