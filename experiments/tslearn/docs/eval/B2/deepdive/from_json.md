# Deep-dive: `from_json`

model: google:gemini-3.1-pro-preview · tokens in=3,095 out=2,975 · wall 23s · 2026-09-08 15:19

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
USER-FACING. TESTABLE FROM PUBLIC INPUTS.
This is a public class method intended for end-users to deserialize trained time-series machine learning models from disk. It can be tested using public estimator classes (like `TimeSeriesKMeans`) and standard NumPy arrays.

**L1 PURPOSE**
The `from_json` class method deserializes and instantiates a `tslearn` machine learning model from a JSON file. It sits at the end of the model persistence data flow, reversing the effects of `to_json` by reading the JSON payload, reconstructing NumPy arrays from nested lists, and re-populating the estimator's hyperparameters and learned weights.

**L2 CONTRACT**
- **Receiver (`cls`)**: A class object inheriting from the `tslearn` base model class (e.g., `TimeSeriesKMeans`). Obtained by referencing the class directly.
- **`path`**: `str`. The full file path to a valid JSON file previously created by the corresponding `to_json` method of the same model class.
- **Returns**: An instance of the receiver class (`Model instance`). The returned object will have its hyperparameters and fitted attributes (e.g., `cluster_centers_`) fully restored.
- **Visibility**: Public.
- **Thread-safety/Laziness**: Eagerly reads from disk and allocates memory for the model parameters. Not thread-safe if another process is concurrently writing to the target file.

**L3 MECHANICS**
1. **File I/O**: Opens the file at `path` in read mode and parses it into a Python dictionary using `json.load` (line 287).
2. **String Normalization**: Delegates to `cls._byte2string(model)` to recursively convert any lingering byte strings into standard strings (line 288).
3. **Array Reconstruction**: Iterates through the `model_params` and `hyper_params` dictionaries. If a parameter is a `list`, it attempts to cast it to a NumPy array (`np.array(param)`). 
4. **Jagged Array Fallback**: If the resulting array has an `object` dtype (line 297) or if `np.array` raises a `ValueError` (line 301) due to jagged dimensions, it falls back to creating a list of individual NumPy arrays (`[np.array(p) for p in param]`).
5. **Instantiation**: Delegates to `cls._organize_model(cls, model)` (line 305), which handles the actual instantiation of the class and the assignment of the reconstructed parameters to the object's `__dict__`.

**L4 CORRECT MINIMAL USAGE**
```python
import os
import tempfile
import numpy as np
from tslearn.clustering import TimeSeriesKMeans

# 1. Create and fit a model on deterministic data
model = TimeSeriesKMeans(n_clusters=2, max_iter=2, random_state=42)
X = np.zeros((10, 5, 1))
X[5:] = 1.0  # Create two distinct constant time-series clusters
model.fit(X)

with tempfile.TemporaryDirectory() as tmpdir:
    model_path = os.path.join(tmpdir, "model.json")
    
    # 2. Serialize the fitted model to JSON
    model.to_json(model_path)
    
    # 3. Target API: Deserialize the model using the class method
    loaded_model = TimeSeriesKMeans.from_json(model_path)
    
    # 4. Verify correctness
    assert isinstance(loaded_model, TimeSeriesKMeans)
    assert loaded_model.n_clusters == 2
    assert hasattr(loaded_model, "cluster_centers_")
    assert loaded_model.cluster_centers_.shape == (2, 5, 1)
    print("Model successfully loaded from JSON.")
```

**L5 FAILURE FORENSICS**
- **Failed Attempt**: `NotFittedError: This TimeSeriesKMeans instance is not fitted yet.`
- **Why it failed**: The execution harness attempted to call `model.to_json(model_path)` on a freshly initialized `TimeSeriesKMeans` instance that had not yet been trained via `.fit()`. In `tslearn`, `to_json` delegates to `self._to_dict()` (line 269), which internally enforces scikit-learn's `check_is_fitted` constraint. Because the model was unfitted, serialization failed before `from_json` could even be invoked.

**L6 SELF-ASSESSMENT**
- **Inferences**: 
  - I inferred that `_to_dict()` enforces `check_is_fitted`, which explains the `NotFittedError` during the `to_json` setup step in the failed attempt.
  - I inferred that `TimeSeriesKMeans` inherits from the base class defining this method, as it is the standard clustering estimator in `tslearn` and was used in the harness history.
- **Information needed for certainty**: The exact implementation of `_to_dict()` and `_organize_model()` to confirm the exact mechanism of the `NotFittedError` and the final object instantiation.
- **Confidence Scores**:
  - L2 (Contract): 10/10. The signature and return types are explicitly defined in the docstring and source code.
  - L3 (Mechanics): 10/10. The source code provided for `from_json` explicitly shows the JSON loading, array reconstruction, and jagged array fallback logic.
  - L4 (Minimal Usage): 10/10. The snippet correctly fits the model before serialization, avoiding the exact `NotFittedError` that trapped the previous harness attempt.