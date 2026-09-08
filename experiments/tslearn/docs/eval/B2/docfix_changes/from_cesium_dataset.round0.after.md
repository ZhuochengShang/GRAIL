## API Test: `from_cesium_dataset`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def from_cesium_dataset(X)
```

### Goal
Convert a dataset formatted for the `cesium` library into a standard `tslearn` 3D NumPy array. This is a user-facing ingestion bridge included in the main user-facing denominator.

### Parameters
- `X`: A `list` of `cesium.time_series.TimeSeries` objects.

### Input
A list of `cesium.time_series.TimeSeries` objects. 
*Note:* `cesium` is an optional external dependency.

### Output
A 3D `numpy.ndarray` of shape `(n_ts, max_sz, d)`, where `n_ts` is the number of time series, `max_sz` is the maximum length, and `d` is the dimensionality. Shorter time series are padded with `numpy.nan` at the end.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import from_cesium_dataset

try:
    # Attempt to use the function; it will raise ImportError if cesium is missing
    from_cesium_dataset([])
except ImportError as e:
    assert "cesium is not installed" in str(e)
else:
    # If cesium is installed, test the actual conversion
    from cesium.time_series import TimeSeries
    
    cesium_ds = [TimeSeries(m=np.array([1.0, 2.0, 3.0, 4.0]))]
    tslearn_arr = from_cesium_dataset(cesium_ds)
    
    assert tslearn_arr.shape == (1, 4, 1)
```

### LLM Instruction Prompt
When testing `from_cesium_dataset`, you MUST wrap the call in a `try...except ImportError` block. `cesium` is an optional external dependency, and calling this function in environments where it is missing will deterministically raise an `ImportError`. Catch this error and assert `"cesium is not installed" in str(e)` to ensure graceful test execution.

### Prompt Snippet
`tslearn.utils.from_cesium_dataset(X)` converts a list of `cesium.time_series.TimeSeries` to a 3D `tslearn` array. `cesium` is optional; calls must be wrapped in `try...except ImportError` to handle missing dependencies gracefully in test environments.

### Common Failure Modes
- **`[fail/infra] missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`** This happens when the test harness executes the code in an environment without the optional `cesium` dependency, and the script fails to catch the deterministic `ImportError` raised by `from_cesium_dataset`.
- **`ValueError`**: Raised if `X` is not a `list` or if any element is not exactly of type `cesium.time_series.TimeSeries`.

### Fix Code Hint
```python
# WRONG: Crashes test environments where optional 'cesium' is missing
from tslearn.utils import from_cesium_dataset
tslearn_arr = from_cesium_dataset(cesium_ds)

# CORRECT: Gracefully handles missing dependency
from tslearn.utils import from_cesium_dataset
try:
    from_cesium_dataset([])
except ImportError as e:
    assert "cesium is not installed" in str(e)
else:
    from cesium.time_series import TimeSeries
    import numpy as np
    cesium_ds = [TimeSeries(m=np.array([1.0, 2.0, 3.0, 4.0]))]
    tslearn_arr = from_cesium_dataset(cesium_ds)
    assert tslearn_arr.shape == (1, 4, 1)
```