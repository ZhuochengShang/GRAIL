## API Test: `pairwise_distances`

### Signature
```python
def pairwise_distances(X, Y=None, metric='euclidean')
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:177_

### Goal
Computes the pairwise distance matrix between two sets of data using a specified metric, implemented specifically as a PyTorch backend helper to enable automatic differentiation.

### Parameters
- `X`: The first set of data (typically a PyTorch tensor).
- `Y`, default `None`: The second set of data (typically a PyTorch tensor). If `None`, the pairwise distances are computed between the elements of `X` itself.
- `metric`, default `'euclidean'`: A string representing the distance metric to use for the computation.

### Input
Callers must provide PyTorch tensors for `X` (and optionally `Y`). To compute gradients, the input tensors must have `requires_grad=True`. While `tslearn` generally expects 3D arrays `(n_ts, max_sz, d)` for time-series estimators, this low-level backend helper typically operates on 2D tensors `(n_samples, n_features)` mirroring `scikit-learn`'s `pairwise_distances` utility.

### Output
Returns `unspecified` — A PyTorch tensor representing the pairwise distance matrix between the elements of `X` and `Y`. If `X` has shape `(N, ...)` and `Y` has shape `(M, ...)`, the output is an `(N, M)` tensor. If inputs require gradients, the output tensor will be attached to a computation graph.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import pairwise_distances

# Inferred from signature (no verbatim example provided in context)
X = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
Y = torch.tensor([[1.0, 2.0]])

# Compute pairwise euclidean distances
dist_matrix = pairwise_distances(X, Y, metric='euclidean')

assert dist_matrix.shape == (2, 1), "Distance matrix should be of shape (N, M)"
print(dist_matrix)
```

### LLM Instruction Prompt
- When calling `pairwise_distances` from the PyTorch backend, ensure inputs are PyTorch tensors, not NumPy arrays.
- If gradient computation is required, ensure the input tensors are instantiated with `requires_grad=True`.
- Do not invent unsupported metric strings; stick to standard metrics like `'euclidean'` unless otherwise specified.

### Prompt Snippet
```text
Use `tslearn.backend.pytorch_backend.pairwise_distances` to compute a differentiable distance matrix between two PyTorch tensors. Ensure inputs are tensors and specify `metric='euclidean'`.
```

### Common Failure Modes
- **Missing PyTorch Dependency:** Fails with an `ImportError` if the `pytorch` package is not installed locally, as this function resides in the PyTorch backend module.
- **Type Mismatch:** Passing NumPy arrays or standard Python lists instead of PyTorch tensors may cause backend tensor operations to fail.
- **Shape Mismatch:** Providing `X` and `Y` with incompatible feature dimensions (e.g., different sizes in the last dimension) will result in a PyTorch broadcasting or matrix operation error.
- **Unsupported Metric:** Passing an unrecognized string to `metric` will cause a `ValueError` or `NotImplementedError` during the distance calculation.

### Fix Code Hint
```python
# FIX: Ensure inputs are PyTorch tensors before passing to the PyTorch backend helper
import torch
from tslearn.backend.pytorch_backend import pairwise_distances

X_tensor = torch.as_tensor(X, dtype=torch.float32)
Y_tensor = torch.as_tensor(Y, dtype=torch.float32) if Y is not None else None

distances = pairwise_distances(X_tensor, Y_tensor, metric='euclidean')
```