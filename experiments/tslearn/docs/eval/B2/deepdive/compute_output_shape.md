# Deep-dive: `compute_output_shape`

model: google:gemini-3.1-pro-preview · tokens in=4,929 out=4,080 · wall 35s · 2026-09-08 15:06

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** INTERNAL/FRAMEWORK
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- **Explanation:** `compute_output_shape` is a standard Keras framework method implemented by custom neural network layers (`GlobalMinPooling1D`, `GlobalArgminPooling1D`, `PatchingLayer`, `LocalSquaredDistanceLayer`) in `tslearn.shapelets`. It is not meant to be called directly by end-users; rather, it is invoked automatically by the Keras backend during model compilation to infer tensor dimensions. It can be tested standalone by explicitly instantiating the layer classes and passing a mock shape tuple, provided the optional `keras` dependency is installed. It should be excluded from main user-facing benchmark denominators.

**L1 PURPOSE**
`compute_output_shape` calculates the expected shape of a layer's output tensor given the shape of its input tensor. In the context of `tslearn`, it allows the underlying Keras backend to statically build the computational graph and allocate resources for the `LearningShapelets` model before any data is actually passed through the network.

**L2 CONTRACT**
- **Receiver:** An instance of one of the custom Keras layers defined in `tslearn.shapelets` (e.g., `GlobalMinPooling1D`, `GlobalArgminPooling1D`, `PatchingLayer`, or `LocalSquaredDistanceLayer`). These are obtained by calling their constructors, sometimes requiring specific hyperparameters (e.g., `PatchingLayer(shapelet_length=10)`).
- **Parameters:**
  - `input_shape` (tuple of ints or `None`): A tuple representing the dimensions of the input tensor. Typically, this is a 3D shape `(batch_size, steps, features)` or a 4D shape `(batch_size, patches, shapelet_length, features)`.
- **Return value:** A tuple of integers (or `None` for dynamic dimensions) representing the dimensions of the output tensor.
- **Visibility:** Public within the Keras framework contract, but conceptually internal to `tslearn`.
- **Thread-safety/Laziness:** Pure function; thread-safe and evaluates eagerly.

**L3 MECHANICS**
The method performs simple tuple arithmetic based on the layer's mathematical operation:
- **`GlobalMinPooling1D` & `GlobalArgminPooling1D`:** Returns `(input_shape[0], input_shape[2])` (line 87, 118). It drops the temporal/steps dimension (`input_shape[1]`) because the pooling operation aggregates over all time steps, leaving only the batch and feature dimensions.
- **`PatchingLayer`:** Returns `(input_shape[0], input_shape[1] - self.shapelet_length + 1, self.shapelet_length, input_shape[2])` (line 144). It calculates the number of valid sliding-window patches that can be extracted and inserts a new dimension for the shapelet length.
- **`LocalSquaredDistanceLayer`:** Returns `(input_shape[0], input_shape[1], self.nb_shapelets)` (line 227). It replaces the patch and feature dimensions with a single dimension representing the computed distances to each of the `nb_shapelets`.

**L4 CORRECT MINIMAL USAGE**
```python
try:
    from tslearn.shapelets.shapelets import (
        GlobalMinPooling1D,
        PatchingLayer,
        LocalSquaredDistanceLayer
    )
    
    # 1. GlobalMinPooling1D (Input: 3D -> Output: 2D)
    pool_layer = GlobalMinPooling1D()
    pool_out = pool_layer.compute_output_shape((16, 50, 1))
    assert pool_out == (16, 1), f"Expected (16, 1), got {pool_out}"
    
    # 2. PatchingLayer (Input: 3D -> Output: 4D)
    patch_layer = PatchingLayer(shapelet_length=10)
    patch_out = patch_layer.compute_output_shape((16, 50, 1))
    assert patch_out == (16, 41, 10, 1), f"Expected (16, 41, 10, 1), got {patch_out}"
    
    # 3. LocalSquaredDistanceLayer (Input: 4D -> Output: 3D)
    dist_layer = LocalSquaredDistanceLayer(nb_shapelets=5)
    dist_out = dist_layer.compute_output_shape((16, 41, 10, 1))
    assert dist_out == (16, 41, 5), f"Expected (16, 41, 5), got {dist_out}"
    
    print("compute_output_shape verified for all custom layers.")
except ImportError as e:
    # tslearn.shapelets has a soft dependency on keras/tensorflow
    print(f"Skipping execution due to missing optional dependency: {e}")
```

**L5 FAILURE FORENSICS**
The recorded failure `[fail/infra] missing module/import: No module named 'keras'` occurred for two reasons:
1. **Missing Dependency:** The test environment lacks the `keras` library, which is an optional dependency required to import `tslearn.shapelets.shapelets`.
2. **Incorrect Class Name:** The attempted code tried to instantiate `shp.GlobalMinPooling1DLayer()`. Looking at the provided source (line 66), the actual class name is `GlobalMinPooling1D` (without the `Layer` suffix).

**L6 SELF-ASSESSMENT**
- **INFERENCE:** I inferred that `keras` is an optional dependency based on the infrastructure failure and standard `tslearn` packaging practices. The try-except block in the usage example is a standard pattern for handling this in test harnesses.
- **INFERENCE:** I inferred the semantic meaning of the `input_shape` indices (batch size, steps, features) based on standard Keras conventions and the docstrings provided in the source (e.g., lines 69, 132).
- **Confidence in L2 (Contract):** 10/10. The contract is explicitly defined in the source code for each layer and strictly follows the Keras Layer API.
- **Confidence in L3 (Mechanics):** 10/10. The mechanics are simple tuple manipulations directly visible in the provided source code.
- **Confidence in L4 (Usage):** 9/10. The usage is correct for Keras layers, though actual execution depends entirely on the presence of the `keras` library in the environment, which is safely handled via the `ImportError` catch.