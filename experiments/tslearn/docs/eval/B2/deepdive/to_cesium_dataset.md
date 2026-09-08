# Deep-dive: `to_cesium_dataset`

model: google:gemini-3.1-pro-preview · tokens in=5,002 out=2,305 · wall 21s · 2026-09-08 15:57

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience**: USER-FACING. This is a public utility function designed for end-users to interoperate between `tslearn` and the `cesium` library.
- **Testability**: TESTABLE FROM PUBLIC INPUTS (with dependency handling). The function can be invoked with standard NumPy arrays, but because the `cesium` package is not installed in the test environment (as proven by the failure history), the test must explicitly catch the resulting `ImportError` to execute successfully in this harness.

**L1 PURPOSE**
The `to_cesium_dataset` API acts as an interoperability bridge, converting a standard `tslearn` time-series dataset (typically a 3D array of shape `(n_ts, sz, d)`) into a list of `cesium.time_series.TimeSeries` objects. It sits at the boundary of the library, allowing users to export data preprocessed or generated in `tslearn` for feature extraction or modeling in the `cesium` ecosystem.

**L2 CONTRACT**
- **Parameters**:
  - `X`: Array-like of shape `(n_ts, sz, d)`. The `tslearn`-formatted dataset to be converted. It accepts any format that `tslearn.utils.check_dataset` can parse (e.g., lists of lists, 2D arrays, 3D arrays).
- **Returns**:
  - A `list` of `cesium.time_series.TimeSeries` objects.
- **Exceptions**:
  - Raises `ImportError` if the `cesium` package is not installed in the Python environment.
- **Visibility**: Public.

**L3 MECHANICS**
- **Dependency Check**: The function first attempts to execute `from cesium.time_series import TimeSeries` (lines 694-695). If this fails, it intercepts the standard `ImportError` and raises a custom `ImportError` explaining that `cesium` must be installed (lines 697-698).
- **Validation**: It delegates to `check_dataset(X)` to normalize the input into a valid 3D `tslearn` array (line 700).
- **Backend Resolution**: It calls `instantiate_backend(X_)` to support both NumPy and PyTorch arrays (line 701).
- **Transformation**: It defines a nested helper `transpose_or_flatten(ts)` (lines 703-708). For each time series, if the dimensionality `d` is 1, it flattens the array to a 1D shape `(-1,)`. If `d > 1`, it transposes the array to shape `(d, sz)` to match `cesium`'s expected measurement format.
- **Construction**: It iterates over the normalized dataset `X_`, applying the helper and wrapping the result in a `TimeSeries(m=...)` object, returning the resulting list (line 710).

**L4 CORRECT MINIMAL USAGE**
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
    assert cesium_ds[0].measurement.shape == (16,)
    print("Successfully converted to cesium dataset.")
    
except ImportError as e:
    # In environments without cesium (like the test harness), this is the expected behavior
    assert "cesium is not installed" in str(e), f"Unexpected ImportError message: {e}"
    print("Caught expected ImportError due to missing cesium dependency.")
```

**L5 FAILURE FORENSICS**
- **`[fail/infra] missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`**:
  This failed because the test environment does not have the `cesium` package installed. When the test called `to_cesium_dataset(X)`, the function executed lines 694-698, caught the missing module error, and raised its custom `ImportError`. The test script did not wrap the call in a `try...except ImportError` block, causing the test to crash rather than gracefully acknowledging the missing optional dependency.

**L6 SELF-ASSESSMENT**
- **Inferences**: None. All claims are directly supported by the provided source code, docstrings, and failure history.
- **Confidence Score L2 (Contract)**: 10/10. The signature, parameters, and exceptions are explicitly defined in the docstring and the first few lines of the function.
- **Confidence Score L3 (Mechanics)**: 10/10. The internal logic is short, linear, and fully visible in the provided snippet.
- **Confidence Score L4 (Minimal Usage)**: 10/10. The usage snippet correctly handles the environmental constraint (missing `cesium`) proven by the failure history, ensuring it is deterministic and executable in the harness.