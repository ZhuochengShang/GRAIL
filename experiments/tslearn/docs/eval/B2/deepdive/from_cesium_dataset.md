# Deep-dive: `from_cesium_dataset`

model: google:gemini-3.1-pro-preview · tokens in=4,076 out=2,852 · wall 22s · 2026-09-08 15:18

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. This is a public utility function designed to help users integrate `tslearn` with the `cesium` time-series machine learning library.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function can be invoked directly with public inputs. However, because the `cesium` package is an optional dependency and is not installed in the test environment (as evidenced by the failure history), the test must gracefully catch the deterministic `ImportError` raised by the function.

**L1 PURPOSE**
The `from_cesium_dataset` API converts a dataset formatted for the `cesium` library (a list of `cesium.time_series.TimeSeries` objects) into a standard `tslearn` 3D NumPy array of shape `(n_ts, max_sz, d)`. It acts as an ingestion bridge, allowing users to apply `tslearn`'s distance metrics, clustering, and classification algorithms to data that was loaded or preprocessed using `cesium`.

**L2 CONTRACT**
- **Parameters:**
  - `X`: A `list` of `cesium.time_series.TimeSeries` objects.
- **Returns:** 
  - A 3D `numpy.ndarray` of shape `(n_ts, max_sz, d)`, where `n_ts` is the number of time series in `X`, `max_sz` is the maximum length among all time series, and `d` is the dimensionality. Shorter time series are padded with `numpy.nan` at the end.
- **Exceptions:**
  - Raises `ImportError` if the `cesium` package is not installed in the Python environment.
  - Raises `ValueError` if `X` is not a `list` or if any element in `X` is not exactly of type `cesium.time_series.TimeSeries`.

**L3 MECHANICS**
1. **Dependency Check:** The function first attempts to import `TimeSeries` from `cesium.time_series`. If it fails, it immediately raises an `ImportError` (lines 746-750).
2. **Type Validation:** It checks that `X` is a list and that every element's type is exactly `TimeSeries`. If not, it raises a `ValueError` (lines 772-775).
3. **Per-Series Formatting:** It iterates over each `TimeSeries` object in `X` using a nested helper function `format_to_tslearn(ts)`:
   - It attempts to sort the time series chronologically by calling `ts.sort()`. If `cesium` raises a `ValueError`, it catches it, issues a `UserWarning`, and assumes the data is already sorted (lines 753-758).
   - It normalizes the measurement data shape. If `ts.measurement` is 1D, it reshapes it to `(1, -1)` (lines 759-762).
   - It determines the dimensionality `d` and the maximum length `max_sz` across all dimensions for this specific time series (lines 763-764).
   - It allocates an empty NumPy array filled with `numpy.nan` of shape `(max_sz, d)` and copies the measurement data into it, dimension by dimension (lines 765-769).
4. **Dataset Aggregation:** It collects the formatted 2D arrays into a list and delegates to `to_time_series_dataset(dataset=dataset)` to pad them to the global maximum length and stack them into a single 3D array (line 777).

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.utils import from_cesium_dataset

try:
    # Attempt to import cesium to see if we can run the happy path
    from cesium.time_series import TimeSeries
    
    # Create a mock cesium dataset
    cesium_ds = [TimeSeries(m=np.array([1.0, 2.0, 3.0, 4.0]))]
    
    # Convert to tslearn format
    tslearn_arr = from_cesium_dataset(cesium_ds)
    
    assert tslearn_arr.shape == (1, 4, 1)
    print("Successfully converted cesium dataset.")

except ImportError:
    # cesium is not installed in this environment; verify the graceful failure
    try:
        from_cesium_dataset([])
        assert False, "Expected ImportError was not raised."
    except ImportError as e:
        assert "cesium is not installed" in str(e)
        print("Correctly raised ImportError for missing cesium dependency.")
```

**L5 FAILURE FORENSICS**
- **`[fail/infra] missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`**
  This failure occurred because the test harness executed the code in an environment where the optional `cesium` dependency was not installed. The attempted code called `to_cesium_dataset` and `from_cesium_dataset` without wrapping them in a `try...except ImportError` block. Consequently, the explicit `ImportError` raised at `tslearn/tslearn/utils/cast.py:749` crashed the test script.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** I inferred that `to_time_series_dataset` (called on line 777) handles the final padding across different time series to form the 3D array, as this is standard `tslearn` behavior, though the implementation of `to_time_series_dataset` is not provided in the context.
- **Confidence in L2 (Contract):** 10/10. The parameters, return types, and exceptions are explicitly visible and validated in the provided source code.
- **Confidence in L3 (Mechanics):** 10/10. The entire algorithm, including the nested helper function and error handling, is fully contained in the provided source snippet.
- **Confidence in L4 (Minimal Usage):** 10/10. The minimal usage correctly handles the missing dependency, which is the only robust way to make it pass in an arbitrary or constrained test harness.