# Deep-dive: `inverse_transform`

model: google:gemini-3.1-pro-preview · tokens in=5,196 out=2,371 · wall 20s · 2026-09-08 15:36

---

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience:** USER-FACING
- **Testability:** TESTABLE FROM PUBLIC INPUTS

This is a standard scikit-learn-style transformer method intended for end users. It can be tested directly by instantiating the public `PiecewiseAggregateApproximation` class, fitting it on a time-series dataset, and calling `inverse_transform`.

### L1 PURPOSE
The `inverse_transform` method reconstructs a time-series dataset back to its original length from its compressed Piecewise Aggregate Approximation (PAA) representation. In the library's data flow, it acts as the decoder counterpart to `transform`, allowing users to project reduced-dimensionality time series back into the original feature space (typically by repeating the aggregated segment values) for visualization, distance computation, or downstream processing.

### L2 CONTRACT
- **Receiver (`self`):** An instance of `PiecewiseAggregateApproximation` (or a subclass like `SymbolicAggregateApproximation`). It must be obtained by instantiating the class (e.g., `PiecewiseAggregateApproximation(n_segments=...)`) and must be fitted (via `fit` or `fit_transform`) so that it knows the original time-series length.
- **Parameters:**
  - `X`: array-like of shape `(n_ts, sz_paa, d)`. A dataset of PAA-compressed time series. It allows `NaN` values and variable-length inputs (as indicated by `_more_tags`).
- **Returns:**
  - `numpy.ndarray` of shape `(n_ts, sz_original_ts, d)`. A dataset of reconstructed time series corresponding to the provided representation.
- **Visibility:** Public.
- **State/Side Effects:** Read-only on the receiver. It relies on the `_X_fit_dims_` attribute set during `fit`.

### L3 MECHANICS
1. **State Validation:** Calls `self._is_fitted()` (line 256) to ensure the transformer has been fitted. This guarantees that `self._X_fit_dims_` (which stores the original time-series dimensions) is available.
2. **Input Validation:** Passes `X` through `check_array(X, allow_nd=True, force_all_finite=False)` and `check_dims(X)` (lines 257-258) to ensure it is a properly formatted 3D time-series array.
3. **Delegation:** Delegates the actual mathematical reconstruction to the backend helper `inv_transform_paa(X, original_size=self._X_fit_dims_[1])` (line 259), which handles the upsampling/repetition of the PAA segments to match the original time-series length.

### L4 CORRECT MINIMAL USAGE
```python
import numpy as np
from tslearn.piecewise import PiecewiseAggregateApproximation

# Create a minimal dataset: 1 time series, 4 time steps, 1 dimension
X_original = np.array([[[1.0], [2.0], [3.0], [4.0]]])

# Instantiate and fit the transformer
paa = PiecewiseAggregateApproximation(n_segments=2)
X_paa = paa.fit_transform(X_original)

# Reconstruct the time series
X_reconstructed = paa.inverse_transform(X_paa)

# Verify the reconstruction
assert X_reconstructed.shape == (1, 4, 1)
# The first segment (1.0, 2.0) averages to 1.5, which is repeated twice
assert np.allclose(X_reconstructed[0, 0, 0], 1.5)
assert np.allclose(X_reconstructed[0, 1, 0], 1.5)

print("Inverse transform successful, shape:", X_reconstructed.shape)
```

### L5 FAILURE FORENSICS
- **Failed Attempt:** `ImportError: cannot import name 'PAA' from 'tslearn.piecewise'`
- **Why it failed:** The execution harness attempted to import a class named `PAA`, following the flawed documentation entry. As seen in the provided source (line 276, `class SymbolicAggregateApproximation(PiecewiseAggregateApproximation):`), the actual class name in `tslearn.piecewise` is `PiecewiseAggregateApproximation`. There is no alias named `PAA` exposed in this module.

### L6 SELF-ASSESSMENT
- **Inferences:** 
  - I inferred that `inv_transform_paa` reconstructs the series by repeating the segment values, which is standard PAA behavior and supported by the SAX doctest example (lines 323-336) showing repeated values like `0.67448975`.
- **Information needed for absolute certainty:** The exact implementation of `inv_transform_paa` to confirm how it handles edge cases where `sz_original_ts` is not perfectly divisible by `n_segments`.
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The signature, parameter types, and return types are explicitly documented in the docstring (lines 245-254).
  - **L3 (Mechanics):** 10/10. The method body is only four lines long and explicitly shows the validation and delegation steps.
  - **L4 (Usage):** 10/10. The usage snippet correctly imports the actual class name found in the source and follows standard scikit-learn API conventions.