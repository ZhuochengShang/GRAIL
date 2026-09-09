## API Test: `inv_transform_1d_sax`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def inv_transform_1d_sax(dataset_sax, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```

### Goal
Advanced/Internal low-level Numba JIT-compiled backend helper. Reconstructs an approximate time series from its 1d-SAX representation. *Note: This is an internal framework function; standard users should use `tslearn.piecewise.OneD_SymbolicAggregateApproximation.inverse_transform` instead.*

### Parameters
- `dataset_sax`: 3D NumPy array of shape `(n_ts, sz, 2 * d)`. Contains the integer indices (symbols) for the average and slope of each segment. **Must be an integer type (e.g., `np.int64` or `np.int32`)**, despite the original docstring incorrectly claiming `float64`.
- `breakpoints_avg_middle_`: 1D NumPy array of `float64`. Continuous values corresponding to each average symbol.
- `breakpoints_slope_middle_`: 1D NumPy array of `float64`. Continuous values corresponding to each slope symbol.
- `original_size`: Integer. The length of the original time series to reconstruct.

### Input
The caller must provide a strictly 3D NumPy array of integers for `dataset_sax` (used directly as array indices in Numba), two 1D `float64` NumPy arrays for the breakpoints, and the target integer length. As an internal/advanced API, the caller owns the construction of these low-level arrays.

### Output
Returns a 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `np.float64` containing the reconstructed time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import inv_transform_1d_sax

# Symbols MUST be integers to be used as indices in Numba, despite the docstring.
dataset_sax = np.array([[[0, 0], [1, 1]]], dtype=np.int64)

# Middle values for the bins
breakpoints_avg_middle = np.array([0.25, 0.75], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

# Target original length
original_size = 4

reconstructed = inv_transform_1d_sax(
    dataset_sax,
    breakpoints_avg_middle,
    breakpoints_slope_middle,
    original_size
)

expected_sum = 2.0
assert reconstructed.shape == (1, 4, 1)
assert np.isclose(reconstructed.sum(), expected_sum)
print(f"__CHECK__ inv_transform_1d_sax {reconstructed.shape} sum={reconstructed.sum():.1f}")
```

### LLM Instruction Prompt
When calling the internal helper `inv_transform_1d_sax`, you MUST pass `dataset_sax` as an integer array (e.g., `np.int64`), ignoring the official docstring's claim that it should be `float64`. Pass `breakpoints_avg_middle_` and `breakpoints_slope_middle_` as 1D `float64` arrays.

### Prompt Snippet
```text
For tslearn.metrics.cysax.inv_transform_1d_sax, `dataset_sax` MUST be an integer array (np.int64) because Numba uses it for array indexing. Do not use float64.
```

### Common Failure Modes
- **Numba TypingError (Float Indexing):** Passing a float array for `dataset_sax` causes a `TypingError: Failed in nopython mode pipeline` during compilation because Numba does not implicitly cast floats to integers for array indexing. The docstring's advice to use `float64` is incorrect.
- **IndexError:** Passing integer symbols in `dataset_sax` that exceed the bounds of the provided 1D breakpoint arrays.
- **Internal API Misuse:** Attempting to use this low-level helper for standard workflows instead of the public `OneD_SymbolicAggregateApproximation` estimator.

### Fix Code Hint
```python
# WRONG: Following the incorrect docstring causes a Numba TypingError
# dataset_sax = np.array([[[0.0, 0.0]]], dtype=np.float64)

# CORRECT: dataset_sax MUST be an integer type for Numba array indexing
dataset_sax = np.array([[[0, 0]]], dtype=np.int64)
reconstructed = inv_transform_1d_sax(
    dataset_sax,
    breakpoints_avg_middle,
    breakpoints_slope_middle,
    original_size
)
```