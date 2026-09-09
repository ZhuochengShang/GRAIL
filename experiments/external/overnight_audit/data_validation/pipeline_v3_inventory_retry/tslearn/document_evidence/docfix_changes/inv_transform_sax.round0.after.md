## API Test: `inv_transform_sax`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def inv_transform_sax(dataset_sax, breakpoints_middle_, original_size)
```

### Goal
Reconstructs a continuous time-series dataset from its discrete Symbolic Aggregate approXimation (SAX) representation. 
*Note: This is an ADVANCED/LOW-LEVEL internal framework helper. It should generally be excluded from standard user-facing workflows, but is testable by providing appropriately typed primitive arrays.*

### Parameters
- `dataset_sax`: A 3D NumPy array of shape `(n_ts, sz, d)` containing the SAX bin indices. **Must be an integer type.**
- `breakpoints_middle_`: A 1D NumPy array of shape `(n_bins,)` and dtype `float64` containing the continuous bin centers.
- `original_size`: An integer representing the length of the original time series.

### Input
- `dataset_sax`: 3D NumPy array of shape `(n_ts, sz, d)`. **Crucially, this must be an integer type** (e.g., `np.int64` or `np.int32`). Ignore the source docstring's claim that it should be `float64` or `float32`; passing floats causes a Numba compilation failure.
- `breakpoints_middle_`: 1D NumPy array of `float64`.
- `original_size`: Integer.
- *Note: As an internal framework helper, inputs must be strictly formatted NumPy arrays.*

### Output
Returns `dataset_out` — A 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `float64` containing the reconstructed time series, where the SAX values are mapped to their bin centers and repeated to match the `original_size`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import inv_transform_sax

# dataset_sax MUST be an integer type for Numba indexing
dataset_sax = np.array([[[0], [1], [2]]], dtype=np.int64)
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
original_size = 6

dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, original_size)

assert dataset_out.shape == (1, 6, 1)
assert np.allclose(dataset_out[0, :, 0], [-0.5, -0.5, 0.0, 0.0, 0.5, 0.5])
```

### LLM Instruction Prompt
- Always import `inv_transform_sax` from `tslearn.metrics.cysax`.
- `dataset_sax` MUST be an integer array (e.g., `np.int64` or `np.int32`), not a float array, because it contains bin indices used for array indexing inside a Numba-compiled function. Ignore the docstring's claim that it should be `float64` or `float32`.
- `breakpoints_middle_` must be a 1D array of `float64`.
- `original_size` must be an integer.

### Prompt Snippet
```text
When calling the internal helper `inv_transform_sax`, ensure `dataset_sax` is a 3D integer array `(n_ts, sz, d)` (e.g., `np.int64`). Do not pass floats, as Numba uses these values as array indices. `breakpoints_middle_` must be a 1D `float64` array, and `original_size` must be an integer.
```

### Common Failure Modes
- **Numba TypingError (Float Indexing)**: Passing `dataset_sax` as a float array (`float64` or `float32`) causes `TypingError: Failed in nopython mode pipeline`. Numba strictly requires array indices to be integers. The source docstring is wrong; you must use integers.
- **Dimensionality Error**: Passing a 2D array `(n_ts, sz)` for `dataset_sax` instead of the required 3D array `(n_ts, sz, d)`.
- **IndexError**: Providing values in `dataset_sax` that are out of bounds for the `breakpoints_middle_` array.
- **Misuse of Internal API**: Attempting to use this ADVANCED/LOW-LEVEL internal framework helper as a standard preprocessing transformer instead of directly passing primitive NumPy arrays.

### Fix Code Hint
```python
# WRONG: Following the flawed docstring and using floats causes Numba TypingError
dataset_sax = np.array([[[0.0], [1.0], [2.0]]], dtype=np.float64)
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, 6)

# CORRECT: Use integer types because the array is used for indexing
dataset_sax = np.array([[[0], [1], [2]]], dtype=np.int64)
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, 6)
```