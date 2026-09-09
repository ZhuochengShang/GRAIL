## API Test: `lcss_accumulated_matrix`

### Signature
```python
def lcss_accumulated_matrix(s1, s2, eps, mask, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2270_

_Source doc:_ Compute the longest common subsequence similarity score between two time series. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) First time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Second time series. If shape is (sz2,), the time series is assumed to be univariate. eps : float Matching threshold. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- acc_cost_mat : array-like, shape=(sz1 + 1, sz2 + 1) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) similarity between two time series.

### Parameters
- `s1`: First time series, array-like of shape `(sz1, d)` or `(sz1,)`. If 1D, it is assumed to be univariate.
- `s2`: Second time series, array-like of shape `(sz2, d)` or `(sz2,)`. If 1D, it is assumed to be univariate.
- `eps`: Matching threshold (float). Points are considered matching if their distance is less than or equal to `eps`.
- `mask`: Boolean mask array of shape `(sz1, sz2)`. Unconsidered cells must have `False` values.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`). If `None`, the backend is automatically determined from the input arrays.

### Input
- `s1` and `s2` must be 1D or 2D arrays (time steps, dimensions). Unlike high-level estimators, these low-level metric helpers expect single time series, not 3D datasets.
- `eps` must be a numeric float value.
- `mask` must be a boolean array matching the lengths of `s1` and `s2` exactly (`shape=(len(s1), len(s2))`).
- If using PyTorch for automatic differentiation, `s1` and `s2` must be `torch.Tensor` objects with `requires_grad=True`.

### Output
Returns `unspecified` — An accumulated cost matrix of shape `(sz1 + 1, sz2 + 1)` representing the dynamic programming table for the LCSS alignment. The type (NumPy array or PyTorch tensor) matches the selected backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import lcss_accumulated_matrix

s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])
eps = 0.5
mask = np.ones((len(s1), len(s2)), dtype=bool)

# Inferred from signature
acc_mat = lcss_accumulated_matrix(s1, s2, eps=eps, mask=mask)

assert acc_mat.shape == (len(s1) + 1, len(s2) + 1)
print(acc_mat)
```

### LLM Instruction Prompt
- When calling `lcss_accumulated_matrix`, you MUST provide the `mask` argument, as it has no default value.
- Ensure `mask` is a boolean array of shape `(len(s1), len(s2))`.
- Pass single time series (1D or 2D arrays) to `s1` and `s2`, not 3D dataset arrays.
- The returned matrix will have dimensions `(len(s1) + 1, len(s2) + 1)`.

### Prompt Snippet
```text
Use `tslearn.metrics.lcss_accumulated_matrix(s1, s2, eps, mask)` to compute the LCSS dynamic programming table. `s1` and `s2` must be 1D or 2D arrays. `mask` is required and must be a boolean array of shape `(len(s1), len(s2))`. Returns a matrix of shape `(len(s1) + 1, len(s2) + 1)`.
```

### Common Failure Modes
- **Missing `mask` argument**: Failing to provide `mask` will raise a `TypeError` because it is a required positional argument.
- **Incorrect `mask` shape**: Providing a mask that does not exactly match `(len(s1), len(s2))` will cause a shape mismatch error during the dynamic programming computation.
- **Passing 3D arrays**: Passing a full dataset `(n_ts, max_sz, d)` instead of a single time series `(sz, d)` will result in incorrect distance calculations or broadcast errors.

### Fix Code Hint
```python
# FIX: Ensure inputs are single time series and create a properly shaped boolean mask
s1_single = X[0]  # shape (sz1, d)
s2_single = X[1]  # shape (sz2, d)
mask = np.ones((len(s1_single), len(s2_single)), dtype=bool)

acc_mat = lcss_accumulated_matrix(s1_single, s2_single, eps=0.5, mask=mask)
```