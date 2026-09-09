## API Test: `from_pickle`

### Signature
```python
def from_pickle(cls, path)
```
_Source: tslearn/tslearn/bases/bases.py:321_

_Source doc:_ Load model from a pickle file. Parameters ---------- path : str Full path to file. Returns ------- Model instance

### Goal
Load a serialized `tslearn` model instance from a pickle file on disk.

### Parameters
- `cls`: The class of the model being loaded (implicitly passed when called as a class method on a `tslearn` estimator).
- `path`: A string representing the full path to the pickle file to load.

### Input
A valid file path string pointing to a pickle file that contains a serialized `tslearn` model.

### Output
Returns `unspecified` — A deserialized instance of the model class.

### Valid Call Patterns
```python
import os
import pickle
from tslearn.clustering import TimeSeriesKMeans

# Setup: create a dummy pickle file containing a model
model = TimeSeriesKMeans(n_clusters=2)
with open("dummy_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Inferred from signature: call as a class method on the estimator
loaded_model = TimeSeriesKMeans.from_pickle("dummy_model.pkl")

assert isinstance(loaded_model, TimeSeriesKMeans)
print("Successfully loaded:", type(loaded_model).__name__)

# Teardown
os.remove("dummy_model.pkl")
```

### LLM Instruction Prompt
- Call `from_pickle` as a class method on the specific `tslearn` estimator class you wish to load (e.g., `TimeSeriesKMeans.from_pickle(path)`).
- Do not call it as a standalone module-level function.
- Provide a valid string path to an existing pickle file.

### Prompt Snippet
```text
Call `from_pickle` as a class method on the specific `tslearn` estimator class (e.g., `TimeSeriesKMeans.from_pickle("model.pkl")`). Do not call it as a standalone function. Ensure the file path exists and contains a valid pickled model.
```

### Common Failure Modes
- Calling `from_pickle` as a standalone module-level function instead of a class method on an estimator class, resulting in a `NameError` or missing `cls` argument.
- `FileNotFoundError` if the provided `path` does not exist.
- `AttributeError` or `TypeError` if the pickle file contains an object incompatible with the calling class or if the environment lacks the dependencies required to unpickle the object.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function
# model = from_pickle("model.pkl")

# RIGHT: Calling as a class method on the target estimator class
from tslearn.clustering import TimeSeriesKMeans
model = TimeSeriesKMeans.from_pickle("model.pkl")
```