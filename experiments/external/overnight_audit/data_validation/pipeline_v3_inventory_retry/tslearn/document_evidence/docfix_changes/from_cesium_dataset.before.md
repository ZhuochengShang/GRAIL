## API Test: `from_cesium_dataset`

### Signature
```python
def from_cesium_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:713_

_Source doc:_ Transform a cesium-compatible dataset into a tslearn dataset. Parameters ---------- X: list of cesium TimeSeries cesium-formatted dataset (cf. `link <http://cesium-ml.org/docs/api/cesium.time_series.html#cesium.time_series.TimeSeries>`_) Returns ------- array, shape=(n_ts, sz, d) tslearn-formatted dataset. Examples -------- >>> from cesium.time_series import TimeSeries >>> cesium_ds = [TimeSeries(m=numpy.array([1, 2, 3, 4]))] >>> tslearn_arr = from_cesium_dataset(cesium_ds) >>> tslearn_arr.shape (1, 4, 1) >>> cesium_ds = [ ...     TimeSeries(m=numpy.array([[1, 2, 3, 4], ...                               [5, 6, 7, 8]])) ... ] >>> tslearn_arr = from_cesium_dataset(cesium_ds) >>> tslearn_arr.shape (1, 4, 2) Notes ----- Conversion from/to cesium format requires cesium to be installed.

### Goal
Transform a `cesium`-compatible dataset (a list of `cesium.time_series.TimeSeries` objects) into a strict 3D `tslearn` time-series dataset.

### Parameters
- `X`: A list of `cesium.time_series.TimeSeries` objects representing the dataset to be converted.

### Input
A list of `cesium` `TimeSeries` objects. 
**Precondition:** The external `cesium` package must be installed in the Python environment, as `tslearn` relies on it to parse the objects.

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the `tslearn`-formatted dataset, where `n_ts` is the number of time series, `max_sz` is the maximum number of measurements per time series, and `d` is the number of dimensions.

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

try:
    import cesium
    
    # Create a deterministic tslearn dataset
    n, sz, d = 2, 4, 1
    rng = np.random.RandomState(0)
    tslearn_dataset = rng.randn(n, sz, d)
    
    # Roundtrip: tslearn -> cesium -> tslearn
    cesium_ds = tslearn.utils.to_cesium_dataset(tslearn_dataset)
    recovered_dataset = tslearn.utils.from_cesium_dataset(cesium_ds)
    
    assert recovered_dataset.shape == (2, 4, 1)
    np.testing.assert_allclose(tslearn_dataset, recovered_dataset)
    print("Successfully converted from cesium dataset.")

except ImportError:
    print("cesium is not installed; skipping execution.")
```

### LLM Instruction Prompt
- When converting data from the `cesium` library to `tslearn`, use `tslearn.utils.from_cesium_dataset(X)`. Ensure `X` is a list of `cesium.time_series.TimeSeries` objects. Note that this function strictly requires the `cesium` package to be installed in the environment. The output will be a standard `tslearn` 3D NumPy array of shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
tslearn.utils.from_cesium_dataset(X) converts a list of cesium TimeSeries objects into a 3D tslearn NumPy array (n_ts, max_sz, d). Requires the `cesium` package to be installed.
```

### Common Failure Modes
- **`ImportError` or `ModuleNotFoundError`**: Occurs if the `cesium` package is not installed in the environment.
- **`AttributeError`**: Occurs if `X` is a standard Python list of lists or a raw NumPy array instead of a list of `cesium.time_series.TimeSeries` objects, as the function expects to access `cesium`-specific attributes (like `.m` or `.time`).

### Fix Code Hint
```python
# Ensure cesium is installed and imported, or handle the missing dependency gracefully
try:
    from cesium.time_series import TimeSeries
    import tslearn.utils
    
    # X must be a list of TimeSeries objects, not raw arrays
    cesium_ds = [TimeSeries(m=np.array([1, 2, 3, 4]))]
    tslearn_arr = tslearn.utils.from_cesium_dataset(cesium_ds)
except ImportError:
    print("Please install cesium to use from_cesium_dataset.")
```