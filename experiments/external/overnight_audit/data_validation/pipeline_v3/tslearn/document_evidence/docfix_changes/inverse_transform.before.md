## API Test: `inverse_transform`

### Signature
```python
def inverse_transform(self, X)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:242  (+2 more definition site/overload)_

_Source doc:_ Compute time series corresponding to given PAA representations. Parameters ---------- X : array-like of shape (n_ts, sz_paa, d) A dataset of PAA series. Returns ------- numpy.ndarray of shape (n_ts, sz_original_ts, d) A dataset of time series corresponding to the provided representation.

### Goal
Reconstruct a time-series dataset in its original dimensionality from its Piecewise Aggregate Approximation (PAA) or similar piecewise representation.

### Parameters
- `self`: A fitted instance of a piecewise transformer (e.g., `tslearn.piecewise.PAA`).
- `X`: An array-like dataset of piecewise representations of shape `(n_ts, sz_paa, d)`.

### Input
A 3D array-like of shape `(n_ts, sz_paa, d)` representing the compressed time series. The transformer instance must have been previously fitted on the original time series so it knows `sz_original_ts` (the original number of time steps).

### Output
Returns `numpy.ndarray` — A 3D array of shape `(n_ts, sz_original_ts, d)` representing the reconstructed time series, where each segment's compressed value is repeated to match the original time-series length.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PAA

# 1 time series, 4 time steps, 1 dimension
X_original = np.array([[[1.0], [2.0], [3.0], [4.0]]])
paa = PAA(n_segments=2)
X_paa = paa.fit_transform(X_original)

# Inferred from signature and docstring
X_reconstructed = paa.inverse_transform(X_paa)

assert X_reconstructed.shape == (1, 4, 1)
assert np.allclose(X_reconstructed[0, 0, 0], 1.5)  # Average of 1.0 and 2.0
print("Inverse transform successful, shape:", X_reconstructed.shape)
```

### LLM Instruction Prompt
- Call `inverse_transform` on a fitted piecewise transformer instance (like `PAA`).
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, sz_paa, d)`.
- Do not call this method on an unfitted transformer, as it requires the original time series length (`sz_original_ts`) to reconstruct the array properly.

### Prompt Snippet
```text
When reconstructing time series from PAA representations using `inverse_transform`, ensure the input is a 3D array of shape `(n_ts, sz_paa, d)` and the transformer instance has already been fitted to learn the original time series length.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D array `(n_ts, sz_paa, d)`.
- Calling `inverse_transform` on an unfitted transformer, resulting in an error because `sz_original_ts` is unknown.
- Passing an array with a different number of segments (`sz_paa`) than what the transformer was configured for (`n_segments`).

### Fix Code Hint
```python
# Ensure input is 3D and the transformer is fitted
from tslearn.utils import to_time_series_dataset

X_paa_3d = to_time_series_dataset(X_paa)
X_reconstructed = paa.inverse_transform(X_paa_3d)
```