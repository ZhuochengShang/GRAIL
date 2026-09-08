## API Test: `inv_transform_1d_sax`

### Signature
```python
def inv_transform_1d_sax(dataset_sax, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:189_

_Source doc:_ Compute time series corresponding to given 1d-SAX representations. Parameters ---------- dataset_sax : array-like, shape=(n_ts, sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) A dataset of SAX series. breakpoints_avg_middle_ : array-like, ndim=1, dtype=float64 breakpoints_slope_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dataset_out : array-like, shape=(n_ts, original_size, d), dtype=float64 A dataset of time series corresponding to the provided representation.

### Goal
Computes the inverse transformation of a 1d-SAX (1D Symbolic Aggregate approXimation) representation to reconstruct an approximation of the original time series using segment averages and slopes.

### Parameters
- `dataset_sax`: Array-like of shape `(n_ts, sz, 2 * d)`. The 1d-SAX representation of the dataset, where each segment contains both an average symbol and a slope symbol (hence `2 * d` features per segment).
- `breakpoints_avg_middle_`: 1D array-like of `float64`. The middle values of the bins used for the average breakpoints, used to map average symbols back to continuous values.
- `breakpoints_slope_middle_`: 1D array-like of `float64`. The middle values of the bins used for the slope breakpoints, used to map slope symbols back to continuous slopes.
- `original_size`: Integer (`int64` or `int32` depending on OS). The length of the original time series before it was reduced to `sz` segments.

### Input
The caller must provide a strictly 3D NumPy array for `dataset_sax` containing the SAX symbols (represented as floats), two 1D NumPy arrays containing the precomputed middle values of the SAX bins, and the target integer length of the reconstructed time series. 

### Output
Returns `array-like` — A 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `float64` representing the reconstructed time series approximations.

### Valid Call Patterns
```python
import numpy as np
# Inferred from signature and source path (tslearn/tslearn/metrics/cysax.py)
from tslearn.metrics.cysax import inv_transform_1d_sax

# 1 time series, 2 segments, d=1 (so 2*d = 2 features per segment: avg and slope)
# Symbols are represented as float indices
dataset_sax = np.array([[[0.0, 0.0], [1.0, 1.0]]], dtype=np.float64)

# Middle values for the bins (e.g., from a fitted OneD_SymbolicAggregateApproximation)
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

assert reconstructed.shape == (1, 4, 1)
print(reconstructed)
```

### LLM Instruction Prompt
- Use `inv_transform_1d_sax` to reconstruct time series from 1d-SAX representations.
- Ensure `dataset_sax` strictly follows the 3D shape `(n_ts, sz, 2 * d)`. The last dimension must be exactly twice the original dimensionality `d` because 1d-SAX stores both an average and a slope symbol for each segment.
- Provide the middle values of the breakpoints for both averages and slopes as 1D `float64` arrays.
- Pass the desired `original_size` as an integer.

### Prompt Snippet
```text
When reconstructing 1d-SAX representations in tslearn, use `tslearn.metrics.cysax.inv_transform_1d_sax`. Ensure the input SAX dataset is a 3D array of shape `(n_ts, sz, 2 * d)` and provide the 1D arrays for `breakpoints_avg_middle_` and `breakpoints_slope_middle_`.
```

### Common Failure Modes
- **Incorrect Last Dimension:** Passing a `dataset_sax` array where the last dimension is `d` instead of `2 * d`. 1d-SAX requires two values (average and slope) per original dimension.
- **Dimensionality Mismatch:** Passing a 2D array for `dataset_sax`. `tslearn` strictly requires the `(n_ts, sz, 2 * d)` 3D format.
- **Type Errors:** Passing integer arrays for `dataset_sax` on platforms where the Cython backend strictly expects `float64` (Linux/macOS) or `float32` (Windows). Always cast the SAX dataset to the appropriate float type before calling this low-level helper.

### Fix Code Hint
```python
# FIX: Ensure dataset_sax is 3D and cast to float64
dataset_sax = np.asarray(dataset_sax, dtype=np.float64)
if dataset_sax.ndim == 2:
    # Reshape (n_ts, sz * 2 * d) to (n_ts, sz, 2 * d) if flattened
    dataset_sax = dataset_sax.reshape(dataset_sax.shape[0], -1, 2 * d)

reconstructed = inv_transform_1d_sax(
    dataset_sax, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)
```