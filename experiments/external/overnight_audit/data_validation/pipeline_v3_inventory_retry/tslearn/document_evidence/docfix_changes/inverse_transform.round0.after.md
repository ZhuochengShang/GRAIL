## API Test: `inverse_transform`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def inverse_transform(self, X)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:242_

### Goal
Reconstruct a time-series dataset back to its original length from its compressed Piecewise Aggregate Approximation (PAA) representation.

### Parameters
- `self`: A fitted instance of `tslearn.piecewise.PiecewiseAggregateApproximation` (or a subclass like `SymbolicAggregateApproximation`).
- `X`: An array-like dataset of piecewise representations of shape `(n_ts, sz_paa, d)`.

### Input
A 3D array-like of shape `(n_ts, sz_paa, d)` representing the compressed time series. The transformer instance must have been previously fitted (via `fit` or `fit_transform`) on the original time series so it has stored `_X_fit_dims_` (the original number of time steps).

### Output
Returns `numpy.ndarray` — A 3D array of shape `(n_ts, sz_original_ts, d)` representing the reconstructed time series, where each segment's compressed value is repeated to match the original time-series length.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PiecewiseAggregateApproximation

# Create a dummy dataset of 8 time series, 40 time steps, 1 dimension
X = np.arange(320).reshape(8, 40, 1)

# Instantiate and fit the correct transformer class
paa = PiecewiseAggregateApproximation(n_segments=10)
X_paa = paa.fit_transform(X)

# Reconstruct the time series
X_reconstructed = paa.inverse_transform(X_paa)

assert X_reconstructed.shape == (8, 40, 1)
print(f"__CHECK__ inverse_transform {X_reconstructed.shape}")
```

### LLM Instruction Prompt
- The correct class name is `PiecewiseAggregateApproximation`, not `PAA`. Import it strictly via `from tslearn.piecewise import PiecewiseAggregateApproximation`.
- Call `inverse_transform` only on a fitted instance of `PiecewiseAggregateApproximation` (or `SymbolicAggregateApproximation`).
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, sz_paa, d)`.

### Prompt Snippet
```text
When reconstructing time series from PAA representations using `inverse_transform`, you must use the `PiecewiseAggregateApproximation` class (there is no `PAA` alias). Ensure the input is a 3D array of shape `(n_ts, sz_paa, d)` and the transformer instance has already been fitted to learn the original time series length.
```

### Common Failure Modes
- `ImportError: cannot import name 'PAA' from 'tslearn.piecewise'`: Attempting to import a non-existent `PAA` alias. The actual class name is `PiecewiseAggregateApproximation`.
- `NotFittedError`: Calling `inverse_transform` on an unfitted transformer, resulting in an error because `sz_original_ts` (stored in `_X_fit_dims_`) is unknown.
- `ValueError`: Passing a 1D or 2D array instead of the required 3D array `(n_ts, sz_paa, d)`.

### Fix Code Hint
```python
# WRONG: Attempting to import a non-existent 'PAA' alias
from tslearn.piecewise import PAA
paa = PAA(n_segments=10)
X_reconstructed = paa.inverse_transform(X_paa)

# CORRECT: Use the full class name PiecewiseAggregateApproximation
from tslearn.piecewise import PiecewiseAggregateApproximation
paa = PiecewiseAggregateApproximation(n_segments=10)
X_paa = paa.fit_transform(X) # Must fit first
X_reconstructed = paa.inverse_transform(X_paa)
```