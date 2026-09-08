## API Test: `lcss_accumulated_matrix`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def lcss_accumulated_matrix(s1, s2, eps, mask, be=None)
```

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) similarity between two time series. Note: This is an ADVANCED/LOW-LEVEL internal helper excluded from the main user-facing benchmark denominator. It is not exported in the main `tslearn.metrics` namespace and must be imported directly from its defining module.

### Parameters
- `s1`: First time series, array-like of shape `(sz1, d)` or `(sz1,)`. If 1D, it is assumed to be univariate.
- `s2`: Second time series, array-like of shape `(sz2, d)` or `(sz2,)`. If 1D, it is assumed to be univariate.
- `eps`: Matching threshold (float). Points are considered matching if their distance is less than or equal to `eps`.
- `mask`: Boolean mask array of shape `(sz1, sz2)`. Unconsidered cells must have `False` values.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`). If `None`, the backend is automatically determined from the input arrays.

### Input
- As an ADVANCED/LOW-LEVEL helper, it expects single time series (1D or 2D arrays), not 3D datasets.
- `eps` must be a numeric float value.
- `mask` must be a boolean array matching the lengths of `s1` and `s2` exactly (`shape=(len(s1), len(s2))`).

### Output
- `acc_cost_mat`: An accumulated cost matrix of shape `(sz1 + 1, sz2 + 1)` representing the dynamic programming table for the LCSS alignment. The type (NumPy array or PyTorch tensor) matches the selected backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import lcss_accumulated_matrix

s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])
eps = 0.5
mask = np.ones((len(s1), len(s2)), dtype=bool)

acc_mat = lcss_accumulated_matrix(s1, s2, eps=eps, mask=mask)

expected_shape = (len(s1) + 1, len(s2) + 1)
assert acc_mat.shape == expected_shape, f"Expected shape {expected_shape}, got {acc_mat.shape}"

print(f"__CHECK__ lcss_accumulated_matrix {acc_mat.shape} {acc_mat[-1, -1]}")
```

### LLM Instruction Prompt
- `lcss_accumulated_matrix` is an advanced/low-level helper and is not exported in the main `tslearn.metrics` namespace. You MUST import it directly using `from tslearn.metrics.dtw_variants import lcss_accumulated_matrix`.
- You MUST provide the `mask` argument, as it has no default value. Ensure `mask` is a boolean array of shape `(len(s1), len(s2))`.
- Pass single time series (1D or 2D arrays) to `s1` and `s2`, not 3D dataset arrays.

### Prompt Snippet
```text
Use `tslearn.metrics.dtw_variants.lcss_accumulated_matrix(s1, s2, eps, mask)` to compute the LCSS dynamic programming table. This is a low-level helper requiring direct import. `mask` is required and must be a boolean array of shape `(len(s1), len(s2))`. Returns a matrix of shape `(len(s1) + 1, len(s2) + 1)`.
```

### Common Failure Modes
- **`ImportError: cannot import name 'lcss_accumulated_matrix' from 'tslearn.metrics'`**: This fails because the API is an ADVANCED/LOW-LEVEL helper omitted from the `tslearn.metrics.__init__.py` exports. It must be imported directly from `tslearn.metrics.dtw_variants`.
- **Missing `mask` argument**: Failing to provide `mask` will raise a `TypeError` because it is a required positional argument.
- **Incorrect `mask` shape**: Providing a mask that does not exactly match `(len(s1), len(s2))` will cause a shape mismatch error during the dynamic programming computation.

### Fix Code Hint
```python
# WRONG: Fails with ImportError
from tslearn.metrics import lcss_accumulated_matrix
acc_mat = lcss_accumulated_matrix(s1, s2, eps=0.5)

# CORRECT: Import from the defining module and provide the required mask
from tslearn.metrics.dtw_variants import lcss_accumulated_matrix
mask = np.ones((len(s1), len(s2)), dtype=bool)
acc_mat = lcss_accumulated_matrix(s1, s2, eps=0.5, mask=mask)
```