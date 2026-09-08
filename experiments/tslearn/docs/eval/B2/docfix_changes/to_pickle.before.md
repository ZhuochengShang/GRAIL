## API Test: `to_pickle`

### Signature
```python
def to_pickle(self, path)
```
_Source: tslearn/tslearn/bases/bases.py:307_

_Source doc:_ Save model to a pickle file. Parameters ---------- path : str Full file path.

### Goal
Serialize and save a `tslearn` time-series estimator or model to a file on disk using Python's pickle format.

### Parameters
- `self`: The `tslearn` model or estimator instance (e.g., a clustering, classification, or regression model) to be saved.
- `path`: A string representing the full file path where the pickled model will be written.

### Input
- **Preconditions:** The caller must have an instantiated `tslearn` model (fitted or unfitted) that inherits from the base classes providing this method. The provided `path` must be a valid, writable file path in the local filesystem.

### Output
Returns `unspecified` — typically `None`. The primary result is a side effect: a serialized `.pkl` file containing the model's state is written to the specified `path`.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.clustering import TimeSeriesKMeans

# Example inferred from the signature (not verified by existing tests)
model = TimeSeriesKMeans(n_clusters=2, random_state=42)

with tempfile.TemporaryDirectory() as tmpdir:
    filepath = os.path.join(tmpdir, "ts_model.pkl")
    
    # Call as an instance method
    model.to_pickle(filepath)
    
    assert os.path.exists(filepath)
    print(f"Model successfully saved to {filepath}")
```

### LLM Instruction Prompt
- Call `to_pickle` strictly as an instance method on a `tslearn` model object (e.g., `model.to_pickle("path/to/file.pkl")`), never as a standalone function.
- Ensure the `path` argument is a string representing a valid, writable file path.

### Prompt Snippet
```text
Save the trained `tslearn` model to disk using its built-in `to_pickle` method. Provide the full file path as a string.
```

### Common Failure Modes
- **Calling as a standalone function:** Attempting to call `tslearn.bases.to_pickle(model, path)` instead of `model.to_pickle(path)` will fail or cause import errors.
- **Invalid or read-only paths:** Providing a directory path instead of a file path, or a path where the user lacks write permissions, will raise an `OSError` or `PermissionError`.
- **Missing parent directories:** If the parent directories in the `path` do not exist, the underlying file open operation will fail with a `FileNotFoundError`.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function or missing parent directories
# to_pickle(model, "missing_dir/model.pkl")

# RIGHT: Call as an instance method and ensure the directory exists
import os
os.makedirs("saved_models", exist_ok=True)
model.to_pickle("saved_models/my_model.pkl")
```