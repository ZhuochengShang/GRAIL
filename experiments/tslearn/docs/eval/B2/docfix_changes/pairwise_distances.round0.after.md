## API Test: `pairwise_distances`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
@staticmethod
def pairwise_distances(X, Y=None, metric="euclidean")
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:177_

### Goal
INTERNAL/FRAMEWORK API. Computes the pairwise distance matrix between two sets of PyTorch tensors. This is a low-level backend helper designed to abstract tensor operations for `tslearn` algorithms. It should be excluded from main user-facing benchmark denominators.

### Parameters
- `X`: A 2D PyTorch Tensor of shape `(n_samples_X, n_features)`.
- `Y`, default `None`: A 2D PyTorch Tensor of shape `(n_samples_Y, n_features)`. If `None`, defaults to `X`.
- `metric`, default `"euclidean"`: Distance metric string (supported: `"euclidean"`, `"sqeuclidean"`) or a callable accepting two 1D tensors and returning a scalar distance.

### Input
ADVANCED/LOW-LEVEL: Callers must explicitly construct and pass PyTorch tensors. The inputs `X` and `Y` must be 2D tensors `(n_samples, n_features)`.

### Output
A 2D PyTorch Tensor of shape `(n_samples_X, n_samples_Y)` containing the computed pairwise distances.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

# Construct minimal 2D tensors (n_samples, n_features)
X_tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]], dtype=torch.float32)
Y_tensor = torch.tensor([[1.0, 2.0]], dtype=torch.float32)

# Call the static method on the backend class
dist_matrix = PyTorchBackend.pairwise_distances(X_tensor, Y_tensor, metric='euclidean')

assert dist_matrix.shape == (2, 1), f"Expected shape (2, 1), got {dist_matrix.shape}"
assert torch.allclose(dist_matrix[0, 0], torch.tensor(0.0), atol=1e-5), "Distance between identical elements should be 0"

print(f"__CHECK__ pairwise_distances {dist_matrix.shape} {dist_matrix[0, 0].item():.4f}")
```

### LLM Instruction Prompt
- `pairwise_distances` is an internal `@staticmethod` of the `PyTorchBackend` class, not a module-level function.
- Import `PyTorchBackend` from `tslearn.backend.pytorch_backend` and invoke it as `PyTorchBackend.pairwise_distances(X, Y, metric)`.
- Ensure inputs are PyTorch tensors.

### Prompt Snippet
```text
Use `PyTorchBackend.pairwise_distances` from `tslearn.backend.pytorch_backend` to compute a distance matrix between two 2D PyTorch tensors.
```

### Common Failure Modes
- **ImportError / Module Attribute Error (The failure that just happened):** Attempting to import `pairwise_distances` directly from the module (`from tslearn.backend.pytorch_backend import pairwise_distances`) fails because it is a `@staticmethod` nested inside the `PyTorchBackend` class. It must be accessed via the class namespace.
- **INTERNAL/FRAMEWORK Misuse:** End-users should typically use `tslearn.metrics` or `sklearn.metrics`. This API is excluded from standard user-facing denominators.
- **Unsupported Metric:** Passing an unrecognized string (anything other than `"euclidean"` or `"sqeuclidean"`) raises a `ValueError`.
- **Type Mismatch:** Passing NumPy arrays instead of PyTorch tensors causes backend operations to fail.

### Fix Code Hint
```python
# WRONG: Attempting to import as a module-level function
from tslearn.backend.pytorch_backend import pairwise_distances
dist = pairwise_distances(X, Y)

# CORRECT: Import the backend class and call the static method
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend
dist = PyTorchBackend.pairwise_distances(X, Y, metric="euclidean")
```