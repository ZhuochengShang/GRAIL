# Deep-dive: `LocalSquaredDistanceLayer`

model: google:gemini-3.1-pro-preview · tokens in=5,336 out=4,673 · wall 40s · 2026-09-08 14:40

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as INTERNAL/FRAMEWORK. It is a custom neural network layer (inheriting from a Keras `Layer`) designed specifically to be used inside the `LearningShapelets` estimator to compute distances between time-series patches and learned shapelets. It should be excluded from a main user-facing benchmark denominator because end-users are meant to interact with the `LearningShapelets` estimator, not its internal Keras layers.

This API is NOT TESTABLE IN THIS HARNESS. The failure history explicitly shows `No module named 'tensorflow'`. Because `LocalSquaredDistanceLayer` is a Keras layer (evidenced by `@register_keras_serializable()`, `build`, `call`, and `add_weight`), it fundamentally requires TensorFlow/Keras to be instantiated and executed. Without these optional dependencies installed in the test environment, the module cannot be exercised.

L1 PURPOSE
`LocalSquaredDistanceLayer` is a custom deep learning layer used within the `LearningShapelets` model. It sits in the forward pass of the shapelet transform, taking extracted local patches of a time series and computing their pairwise squared Euclidean distances against a set of learned shapelet weights. This allows the network to learn shapelets via gradient descent by backpropagating through the distance computation.

L2 CONTRACT
- **Receiver**: `LocalSquaredDistanceLayer`. Obtained by direct instantiation.
- **Parameters**:
  - `nb_shapelets` (int): The number of shapelets to learn. (Note: The current documentation incorrectly states this class takes no arguments).
  - `init` (str or callable, optional): The initializer for the shapelet weights. Defaults to `"uniform"` if `None`.
  - `**kwargs`: Additional keyword arguments passed to the base Keras `Layer` class (e.g., `name`).
- **Return Value**: When called, it returns a 3D tensor of shape `(batch_size, steps, nb_shapelets)` containing the squared distances.
- **Visibility**: Publicly exported and registered for Keras serialization, but functionally an internal framework component.
- **State/Laziness**: The layer is stateful; it initializes and holds trainable weights (`self.kernel`) when built.

L3 MECHANICS
- **Initialization**: Stores `nb_shapelets` and `initializer`. Sets `input_spec` to require a 4D tensor.
- **Building**: The `build` method (called automatically by Keras on the first forward pass) allocates a trainable weight matrix `self.kernel` of shape `(nb_shapelets, shapelet_length, features)` using `self.add_weight` (lines 189-194).
- **Masking**: `compute_mask` propagates invalidity by checking for finite values in the inputs.
- **Forward Pass (`call`)**:
  1. Replaces NaNs in the input `x` with 0 using `ops.nan_to_num`.
  2. Computes the squared Euclidean distance using the expansion $(x - y)^2 = x^2 + y^2 - 2xy$.
  3. $x^2$ is computed by squaring `x` and summing over the last two axes (`shapelet_length` and `features`).
  4. $y^2$ is computed by squaring `self.kernel` and summing over its last two axes.
  5. The cross-term $2xy$ is computed by reshaping both `x` and `self.kernel` into 2D matrices and performing a dot product (`ops.dot`).
  6. The final distance is normalized by dividing by `shapelet_size` (which is `input_shape[2]`).

L4 CORRECT MINIMAL USAGE
Because the environment lacks TensorFlow (as proven by the failure history), this API cannot be executed here. The following snippet demonstrates the correct usage wrapped in a guard to prevent infra failure.

```python
try:
    import numpy as np
    import tensorflow as tf
    from tslearn.shapelets.shapelets import LocalSquaredDistanceLayer

    # The current documentation is WRONG: it requires `nb_shapelets`.
    layer = LocalSquaredDistanceLayer(nb_shapelets=3, init="zeros")
    
    # Input shape: (batch_size, steps, shapelet_length, features)
    # e.g., 2 samples, 4 patches per sample, shapelet length 5, 1 feature
    dummy_input = tf.constant(np.ones((2, 4, 5, 1)), dtype=tf.float32)
    
    # Forward pass
    distances = layer(dummy_input)
    
    assert distances.shape == (2, 4, 3), f"Unexpected shape: {distances.shape}"
    print("Correctness witness: Layer executed successfully with TensorFlow.")

except ImportError as e:
    print(f"Correctness witness: Skipped due to missing optional dependency ({e})")
```

L5 FAILURE FORENSICS
- `[fail/infra] missing module/import: No module named 'tensorflow'`: The test harness attempted to `import tensorflow as tf`. `tslearn`'s shapelet module relies on Keras/TensorFlow for its neural network components. The test environment does not have TensorFlow installed, making this layer untestable.
- `[fail/doc-repair] round 0: rewrite fabricated members: convert_to_tensor, exit`: The LLM attempted to use `convert_to_tensor` (likely assuming `tf.convert_to_tensor` was available without importing TF, or trying to mock it) and failed. Furthermore, the LLM was misled by the severely incorrect documentation entry which stated: *"Instantiate `LocalSquaredDistanceLayer` without any arguments."* The source code explicitly requires `nb_shapelets` as a positional argument (line 179).

L6 SELF-ASSESSMENT
- **Inferences**: I inferred that `Layer` is `keras.layers.Layer` (or its Keras 3 equivalent) based on the `@register_keras_serializable()` decorator and standard Keras lifecycle methods (`build`, `call`, `compute_output_shape`, `add_weight`). I inferred that `ops` is a backend abstraction (like `keras.ops`) used by `tslearn` to support tensor operations.
- **Needs**: To be absolutely certain about the origin of `Layer` and `ops`, I would need to see the import statements at the top of `tslearn/shapelets/shapelets.py`.
- **Confidence Scores**:
  - L2 (Contract): 10/10. The signature and required arguments are explicitly defined in the provided source code.
  - L3 (Mechanics): 9/10. The mathematical expansion is clear from the source, though the exact implementation details of `ops.dot` depend on the unseen backend wrapper.
  - L4 (Usage): 9/10. The usage perfectly matches Keras layer conventions, though it cannot be verified dynamically due to the missing TensorFlow dependency.