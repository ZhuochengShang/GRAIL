# Deep-dive: `pairwise_distances`

model: google:gemini-3.1-pro-preview · tokens in=4,686 out=3,143 · wall 28s · 2026-09-08 15:49

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** INTERNAL/FRAMEWORK
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- **Explanation:** This API is a low-level backend helper designed to abstract tensor operations so that `tslearn` algorithms can run agnostically across NumPy and PyTorch. It is not meant to be called directly by end-users, who should instead use `tslearn.metrics` or `sklearn.metrics`. It is testable by explicitly importing the backend class (inferred as `PyTorchBackend`) and invoking the static method. It should be excluded from main user-facing benchmark denominators.

**L1 PURPOSE**
`pairwise_distances` is a backend-specific helper method in `tslearn`'s PyTorch backend. It computes the pairwise distance matrix between two collections of vectors (tensors) using PyTorch operations. By delegating to this method, `tslearn` estimators can compute distances on PyTorch tensors, preserving computation graphs for automatic differentiation and enabling GPU acceleration without hardcoding PyTorch dependencies in the core algorithmic logic.

**L2 CONTRACT**
- **Receiver:** The `PyTorchBackend` class (as a `@staticmethod`).
- **Parameters:**
  - `X` (PyTorch Tensor): A 2D tensor of shape `(n_samples_X, n_features)` representing the first collection of vectors.
  - `Y` (PyTorch Tensor, optional): A 2D tensor of shape `(n_samples_Y, n_features)`. Defaults to `None`, in which case it is treated as `Y = X`.
  - `metric` (str or callable, default `"euclidean"`): The distance metric to compute. Supported strings are `"euclidean"` and `"sqeuclidean"`. If a callable is provided, it must accept two 1D tensors and return a scalar distance.
- **Return Value:** A 2D PyTorch Tensor of shape `(n_samples_X, n_samples_Y)` containing the computed pairwise distances.
- **Visibility:** Internal/Framework (publicly accessible but intended for backend abstraction).
- **Thread-safety/Laziness:** Eagerly evaluated. Thread-safety depends on the underlying PyTorch `cdist` implementation and the GIL.

**L3 MECHANICS**
- The method first checks if `Y` is `None`; if so, it aliases `Y` to `X` (line 178-179).
- If `metric` is `"euclidean"`, it delegates directly to `_torch.cdist(X, Y)` (line 181).
- If `metric` is `"sqeuclidean"`, it computes `_torch.cdist(X, Y) ** 2` (line 183).
- If `metric` is a callable, it falls back to a slow, unvectorized nested loop. It initializes a zero matrix of shape `(X.shape[0], Y.shape[0])` and populates it by calling `metric(X[i, ...], Y[j, ...])` for every pair (lines 184-189).
- If `metric` is an unsupported string, it raises a `ValueError` (line 190).

**L4 CORRECT MINIMAL USAGE**
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

# Construct minimal 2D tensors (n_samples, n_features)
X = torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32)
Y = torch.tensor([[2.0, 2.0]], dtype=torch.float32)

# Call the static method on the backend class
dist_matrix = PyTorchBackend.pairwise_distances(X, Y, metric="euclidean")

assert dist_matrix.shape == (2, 1), f"Expected shape (2, 1), got {dist_matrix.shape}"
print("Pairwise distances:\n", dist_matrix)
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `cannot import name 'pairwise_distances' from 'tslearn.backend.pytorch_backend'`
- **Reason for Failure:** The harness attempted to import `pairwise_distances` as a module-level function (`from tslearn.backend.pytorch_backend import pairwise_distances`). However, as seen in the source snippet (lines 148-177), `pairwise_distances` is a `@staticmethod` nested inside a class (the backend class). It must be accessed via the class namespace (e.g., `PyTorchBackend.pairwise_distances`).

**L6 SELF-ASSESSMENT**
- **INFERENCE:** The class containing `pairwise_distances` is named `PyTorchBackend`. This is inferred from the file name `pytorch_backend.py`, the presence of nested/sibling classes like `PyTorchLinalg` (line 238), and standard `tslearn` backend architecture conventions.
- **INFERENCE:** The `_torch` module referenced in the source is the standard `torch` library, imported as `_torch` at the top of the module to avoid namespace pollution.
- **Confidence in L2 (Contract):** 9/10. The signature and types are clear from the source code and PyTorch conventions, though the exact class name requires inference.
- **Confidence in L3 (Mechanics):** 10/10. The mechanics are explicitly visible in the provided source code snippet.
- **Confidence in L4 (Minimal Usage):** 9/10. The usage is correct and deterministic, assuming the inferred class name `PyTorchBackend` is accurate.