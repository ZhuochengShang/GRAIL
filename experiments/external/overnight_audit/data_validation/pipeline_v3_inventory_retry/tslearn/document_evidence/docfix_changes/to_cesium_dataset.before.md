## API Test: `to_cesium_dataset`

### Signature
```python
def to_cesium_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:655_

_Source doc:_ Transform a tslearn-compatible dataset into a cesium dataset. Parameters ---------- X: array, shape = (n_ts, sz, d), where n_ts=1 tslearn-formatted dataset to be cast to cesium format Returns ------- list of cesium TimeSeries cesium-formatted dataset (cf. `link <http://cesium-ml.org/docs/api/cesium.time_series.html#cesium.time_series.TimeSeries>`_) Examples -------- >>> tslearn_arr = numpy.random.randn(3, 16, 1) >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 3 >>> cesium_ds[0].measurement.shape (16,) >>> tslearn_arr = numpy.random.randn(3, 16, 2) >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 3 >>> cesium_ds[0].measurement.shape (2, 16) >>> tslearn_arr = [[1, 2, 3], [1, 2, 3, 4]] >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 2 >>> cesium_ds[0].measurement.shape (3,) Notes ----- Conversion from/to cesium format requires cesium to be installed.

### Goal
Transform a standard 3D `tslearn`-compatible time-series dataset into a list of `cesium` `TimeSeries` objects.

### Parameters
- `X`: A `tslearn`-formatted dataset (array-like of shape `(n_ts, sz, d)`) to be cast to `cesium` format.

### Input
- A 3D `numpy` array of shape `(n_ts, max_sz, d)` representing `n_ts` time series, each with up to `max_sz` time steps and `d` dimensions. It also accepts a list of lists for variable-length time series.
- **Precondition**: The external `cesium` package must be installed in the Python environment.

### Output
Returns `unspecified` — A list of `cesium.time_series.TimeSeries` objects representing the converted dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_cesium_dataset

try:
    import cesium
    
    # 2 time series, 3 time steps, 2 dimensions
    tslearn_arr = np.array([
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
    ])
    
    cesium_ds = to_cesium_dataset(tslearn_arr)
    
    assert len(cesium_ds) == 2
    # cesium transposes the measurements to (d, sz)
    assert cesium_ds[0].measurement.shape == (2, 3)
    print(f"Successfully converted {len(cesium_ds)} series to cesium format.")
    
except ImportError:
    print("cesium is not installed; skipping execution.")
```

### LLM Instruction Prompt
- Use `tslearn.utils.to_cesium_dataset(X)` to convert a 3D `(n_ts, max_sz, d)` `tslearn` time-series dataset into a list of `cesium.time_series.TimeSeries` objects.
- Ensure the `cesium` package is installed in the environment before calling this function, as it is a strict dependency for the conversion.
- Be aware that `cesium` transposes the dimensions: a `tslearn` series of shape `(sz, d)` becomes a `cesium` measurement of shape `(d, sz)` (or `(sz,)` if `d=1`).

### Prompt Snippet
```text
When integrating with cesium, convert your 3D tslearn array using `tslearn.utils.to_cesium_dataset(X)`. This requires the `cesium` package to be installed and will return a list of `cesium.time_series.TimeSeries` objects where the measurement arrays are transposed to `(d, sz)`.
```

### Common Failure Modes
- **Missing Dependency**: Raising an `ImportError` or `ModuleNotFoundError` if the `cesium` package is not installed in the Python environment.
- **Invalid Input Shape**: Passing a dataset that has not been properly formatted into a 3D array or a valid list of lists, causing parsing errors during the conversion.

### Fix Code Hint
```python
try:
    import cesium
    from tslearn.utils import to_cesium_dataset
    
    # Ensure X is a properly formatted tslearn dataset before conversion
    cesium_dataset = to_cesium_dataset(X)
except ImportError:
    print("The 'cesium' package is required for this conversion. Please install it.")
```