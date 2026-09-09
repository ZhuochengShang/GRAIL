## API Test: `to_cesium_dataset`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def to_cesium_dataset(X)
```

### Goal
Transform a standard 3D `tslearn`-compatible time-series dataset into a list of `cesium` `TimeSeries` objects. 

### Parameters
- `X`: Array-like of shape `(n_ts, sz, d)`. The `tslearn`-formatted dataset to be converted. Accepts any format parsable by `tslearn.utils.check_dataset`.

### Input
- A 3D `numpy` array of shape `(n_ts, max_sz, d)` representing `n_ts` time series, each with up to `max_sz` time steps and `d` dimensions.

### Output
- A `list` of `cesium.time_series.TimeSeries` objects representing the converted dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_cesium_dataset

# Create a standard tslearn dataset: 3 time series, 16 time steps, 1 dimension
X = np.random.randn(3, 16, 1)

try:
    # Attempt conversion
    cesium_ds = to_cesium_dataset(X)
    
    # If cesium is installed, verify the output
    assert len(cesium_ds) == 3
    print(f"__CHECK__ to_cesium_dataset {len(cesium_ds)}")
    
except ImportError as e:
    # In environments without cesium (like the test harness), this is the expected behavior
    assert "cesium is not installed" in str(e)
    print("__CHECK__ to_cesium_dataset (cesium not installed)")
```

### LLM Instruction Prompt
- Use `tslearn.utils.to_cesium_dataset(X)` to convert a 3D `(n_ts, max_sz, d)` `tslearn` time-series dataset into a list of `cesium.time_series.TimeSeries` objects.
- The function requires the external `cesium` package to be installed. If `cesium` is not installed, calling this function will immediately raise an `ImportError`.
- Test snippets and robust integrations MUST wrap the call in a `try...except ImportError` block to gracefully handle environments where `cesium` is missing.

### Prompt Snippet
```text
When integrating with cesium, convert your 3D tslearn array using `tslearn.utils.to_cesium_dataset(X)`. Because `cesium` is an optional dependency, you must wrap the function call in a `try...except ImportError` block to prevent crashes in environments where it is not installed.
```

### Common Failure Modes
- **`[fail/infra] missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`**: This fails when the test environment lacks the `cesium` package and the script calls `to_cesium_dataset(X)` without catching the resulting `ImportError`. The function explicitly raises a custom `ImportError` if `cesium.time_series` cannot be imported.

### Fix Code Hint
**WRONG:**
```python
from tslearn.utils import to_cesium_dataset
# Crashes with ImportError if cesium is not installed
cesium_ds = to_cesium_dataset(X)
```

**CORRECT:**
```python
from tslearn.utils import to_cesium_dataset
try:
    cesium_ds = to_cesium_dataset(X)
    # Process cesium_ds...
except ImportError as e:
    assert "cesium is not installed" in str(e)
    print("Skipped: cesium dependency missing.")
```