## API Test: `to_pickle`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def to_pickle(self, path)
```

### Goal
Serialize a `tslearn` time-series estimator to disk. Note: This method extracts and saves the model's internal state as a dictionary, not as a standard pickled Python object.

### Parameters
- `self`: The `tslearn` model instance (e.g., `TimeSeriesKMeans`, `TimeSeriesSVC`) to be saved.
- `path` (`str`): Full file path where the pickled dictionary will be written.

### Input
- An instantiated `tslearn` model (fitted or unfitted).
- A valid, writable file path string. Parent directories must exist.

### Output
Returns `None`. Writes a `.pkl` file containing the model's state dictionary to the specified path using pickle protocol 2.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.clustering import TimeSeriesKMeans

model = TimeSeriesKMeans(n_clusters=2, random_state=42)

with tempfile.TemporaryDirectory() as tmpdir:
    filepath = os.path.join(tmpdir, "test_model.pkl")
    
    # Save the model
    model.to_pickle(filepath)
    assert os.path.exists(filepath)
    
    # Load the model using the class method, NOT standard pickle.load
    loaded_model = TimeSeriesKMeans.from_pickle(filepath)
    
    assert loaded_model.n_clusters == 2
```

### LLM Instruction Prompt
- Call `to_pickle` strictly as an instance method on a `tslearn` model object.
- CRITICAL: `to_pickle` serializes the model's internal state as a dictionary, not as a standard pickled Python object. To load a model saved with `to_pickle`, callers MUST use the corresponding `from_pickle` class method on the estimator (e.g., `TimeSeriesKMeans.from_pickle(path)`) rather than standard `pickle.load`.

### Prompt Snippet
```text
Save the trained `tslearn` model to disk using its built-in `to_pickle` method, and reload it using the estimator's symmetric `from_pickle` class method.
```

### Common Failure Modes
- **Deserializing with standard `pickle.load`:** Because `to_pickle` explicitly dumps a dictionary of the model's state rather than the object itself, using standard `pickle.load(open(path, 'rb'))` returns a standard Python `dict`. Attempting to access model attributes (like `.n_clusters`) on this dictionary will crash with `AttributeError: 'dict' object has no attribute 'n_clusters'`. Always use the symmetric `from_pickle` classmethod to reconstruct the object.
- **Missing parent directories:** The underlying file open operation will fail with a `FileNotFoundError` if the parent directories in the `path` do not exist.

### Fix Code Hint
```python
# WRONG: Loading with standard pickle returns a dict, causing AttributeErrors
# import pickle
# model.to_pickle("model.pkl")
# loaded = pickle.load(open("model.pkl", "rb"))
# print(loaded.n_clusters)  # AttributeError: 'dict' object has no attribute 'n_clusters'

# RIGHT: Load using the symmetric from_pickle class method
from tslearn.clustering import TimeSeriesKMeans
model.to_pickle("model.pkl")
loaded = TimeSeriesKMeans.from_pickle("model.pkl")
print(loaded.n_clusters)
```