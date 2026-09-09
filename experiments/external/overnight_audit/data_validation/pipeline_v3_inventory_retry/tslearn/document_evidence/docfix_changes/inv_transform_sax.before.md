## API Test: `inv_transform_sax`

### Signature
```python
def inv_transform_sax(dataset_sax, breakpoints_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:78_

_Source doc:_ Compute time series corresponding to given SAX representations. Parameters ---------- dataset_sax : array-like, shape=(n_ts, sz, d), dtype=float64 (Linux and MacOS) or float32 (Windows) A dataset of SAX series. breakpoints_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dataset_out : array-like, shape=(n_ts, original_size, d), dtype=float64

### Goal
Computes the inverse transformation of a Symbolic Aggregate approXimation (SAX) representation, reconstructing a continuous time-series dataset of the original length from the discrete SAX symbols.

### Parameters
- `dataset_sax`: A 3D array-like of shape `(n_ts, sz, d)` containing the SAX representations of the time series (typically bin indices represented as floats).
- `breakpoints_middle_`: A 1D array-like of `float64` representing the middle values of the SAX bins, used to map the discrete symbols back to continuous values.
- `original_size`: An integer specifying the length of the original time series before it was reduced to length `sz`.

### Input
- `dataset_sax` must be a 3D numpy array of shape `(n_ts, sz, d)`. Due to Cython bindings, it expects `float64` on Linux/macOS and `float32` on Windows.
- `breakpoints_middle_` must be a 1D numpy array of `float64`.
- `original_size` must be an integer (`int64` on Linux/macOS, `int32` on Windows).

### Output
Returns `dataset_out` — A 3D numpy array of shape `(n_ts, original_size, d)` and dtype `float64` containing the reconstructed time series, where the SAX values are mapped to their bin centers and repeated to match the `original_size`.

### Valid Call Patterns
```python
import sys
import numpy as np
from tslearn.metrics.cysax import inv_transform_sax

# Platform-specific types for Cython memoryviews
float_type = np.float32 if sys.platform == "win32" else np.float64
int_type = np.int32 if sys.platform == "win32" else np.int64

# 1 time series, SAX size 3, 1 dimension
dataset_sax = np.array([[[0.0], [1.0], [2.0]]], dtype=float_type)
# 3 bins, so 3 middle breakpoints
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
original_size = int_type(6)

# Inferred from signature
dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, original_size)

assert dataset_out.shape == (1, 6, 1)
print("Reconstructed shape:", dataset_out.shape)
```

### LLM Instruction Prompt
- Always import `inv_transform_sax` from `tslearn.metrics.cysax`.
- Ensure `dataset_sax` is strictly a 3D array `(n_ts, sz, d)`. If you have 2D data, use `np.expand_dims` to add the feature dimension.
- Be mindful of the Cython dtype constraints: `dataset_sax` expects `float64` on Linux/macOS and `float32` on Windows. `original_size` expects `int64` on Linux/macOS and `int32` on Windows.
- `breakpoints_middle_` must be a 1D array of `float64`.

### Prompt Snippet
```text
When calling `inv_transform_sax`, ensure the input `dataset_sax` is a 3D array of shape `(n_ts, sz, d)`. The function requires `breakpoints_middle_` as a 1D array to map SAX indices back to continuous values, and `original_size` to determine the length of the output time series. Account for platform-specific Cython types (float32/int32 on Windows, float64/int64 elsewhere).
```

### Common Failure Modes
- **Dimensionality Error**: Passing a 2D array `(n_ts, sz)` for `dataset_sax` instead of the required 3D array `(n_ts, sz, d)`.
- **Cython Type Error**: Passing integers or the wrong float precision for `dataset_sax` or `original_size`, which can cause a Cython memoryview `ValueError` on different operating systems.
- **Shape Mismatch**: Providing a `breakpoints_middle_` array that is not 1D.

### Fix Code Hint
```python
import sys
import numpy as np

# Adjust dtype based on platform to satisfy Cython memoryviews
float_type = np.float32 if sys.platform == "win32" else np.float64
int_type = np.int32 if sys.platform == "win32" else np.int64

dataset_sax = np.asarray(dataset_sax, dtype=float_type)
if dataset_sax.ndim == 2:
    dataset_sax = np.expand_dims(dataset_sax, axis=-1)

breakpoints_middle = np.asarray(breakpoints_middle, dtype=np.float64)
original_size = int_type(original_size)
```