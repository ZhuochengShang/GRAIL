## API Test: `compute`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def compute(self)
```

### Goal
Execute the delayed computation graph for differentiable time-series metrics. Depending on the receiver, it calculates either a pairwise squared Euclidean distance matrix (`SquaredEuclidean`) or the Soft-DTW discrepancy via dynamic programming (`SoftDTW`). 
*Note: This is an ADVANCED/LOW-LEVEL internal framework helper API. It should be excluded from the main user-facing benchmark denominator, but is testable via explicit low-level construction.*

### Parameters
- `self`: An instance of `tslearn.metrics.softdtw_variants.SoftDTW` or `tslearn.metrics.softdtw_variants.SquaredEuclidean`.

### Input
Takes no arguments. The caller must explicitly construct the low-level receiver objects:
- For `SquaredEuclidean`, initialize with two time-series arrays `X` and `Y` of shape `(n_timestamps, n_features)`.
- For `SoftDTW`, initialize with `D` (which must be a precomputed distance matrix or an instance of `SquaredEuclidean`) and `gamma`. 
*Do not pass raw time series directly to `SoftDTW`.*

### Output
- For `SquaredEuclidean.compute()`: A 2D array-like of shape `(m, n)` containing the squared Euclidean distance matrix.
- For `SoftDTW.compute()`: A `float` representing the soft-DTW discrepancy score. (Calling this also mutates the object by populating `self.R_` and setting `self.computed = True`).

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.softdtw_variants import SoftDTW, SquaredEuclidean

# 1. Define two time series (shape: n_timestamps, n_features)
X = np.array([[1.0], [2.0], [3.0]])
Y = np.array([[1.0], [2.0], [4.0]])

# 2. Construct the low-level SquaredEuclidean helper
sq_euc = SquaredEuclidean(X, Y)

# 3. Construct the low-level SoftDTW helper using the SquaredEuclidean object
soft_dtw_obj = SoftDTW(D=sq_euc, gamma=1.0)

# 4. Compute the Soft-DTW discrepancy
sdtw_score = soft_dtw_obj.compute()

assert isinstance(sdtw_score, float)
print(f"__CHECK__ compute {sdtw_score:.4f}")
```

### LLM Instruction Prompt
To test `compute`, explicitly import and construct the low-level `SquaredEuclidean` and `SoftDTW` helpers from `tslearn.metrics.softdtw_variants`. Do not pass raw time series to `SoftDTW`; pass them to `SquaredEuclidean(X, Y)`, and pass that resulting object as `D` to `SoftDTW(D=..., gamma=...)`. Call `.compute()` on the resulting object.

### Prompt Snippet
```python
sq_euc = SquaredEuclidean(X, Y)
soft_dtw_obj = SoftDTW(D=sq_euc, gamma=1.0)
sdtw_score = soft_dtw_obj.compute()
```

### Common Failure Modes
- **Passing raw time series to SoftDTW:** Attempting to instantiate `SoftDTW(ts1=X, ts2=Y)` will fail. `SoftDTW` expects its first positional argument `D` to be a distance matrix or a helper object like `SquaredEuclidean`. It does not accept raw time series kwargs.
- **Direct user-facing usage:** Treating this ADVANCED/LOW-LEVEL API as a standard user-facing metric function. It requires explicit multi-step object construction and is intended for framework-internal use.

### Fix Code Hint
```python
# WRONG: Passing raw time series directly to SoftDTW
# sdtw = SoftDTW(ts1=X, ts2=Y, gamma=1.0)
# score = sdtw.compute()

# RIGHT: Wrap time series in SquaredEuclidean first
sq_euc = SquaredEuclidean(X, Y)
sdtw = SoftDTW(D=sq_euc, gamma=1.0)
score = sdtw.compute()
```