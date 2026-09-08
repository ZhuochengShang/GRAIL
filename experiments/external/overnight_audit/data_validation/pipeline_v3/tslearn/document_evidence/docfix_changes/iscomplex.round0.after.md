## API Test: `iscomplex`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
@staticmethod
def iscomplex(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:153_

### Goal
INTERNAL/FRAMEWORK. Determines whether a given input is a Python complex scalar or a PyTorch tensor with a complex data type. This is a low-level backend helper and should be excluded from the main user-facing benchmark denominator.

### Parameters
- `x`: A Python `complex` scalar or a PyTorch tensor (`torch.Tensor`) to evaluate. If not a `complex` scalar, it must possess a `dtype` attribute with an `is_complex` boolean property.

### Input
ADVANCED/LOW-LEVEL. Requires explicit low-level construction. The input must be a Python `complex` scalar or a `torch.Tensor`.

### Output
`bool`. Returns `True` if the input is complex-valued, `False` otherwise.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

real_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
complex_tensor = torch.tensor([1.0+1j, 2.0+2j], dtype=torch.complex64)

is_real_cplx = PyTorchBackend.iscomplex(real_tensor)
is_cplx_cplx = PyTorchBackend.iscomplex(complex_tensor)

assert is_real_cplx is False, "Real tensor should not be complex"
assert is_cplx_cplx is True, "Complex tensor should be complex"
print(f"__CHECK__ iscomplex {is_real_cplx}, {is_cplx_cplx}")
```

### LLM Instruction Prompt
When testing the internal `tslearn` PyTorch backend, access `iscomplex` as a static method on the `PyTorchBackend` class. Do not attempt to import it as a module-level function. Pass either a Python `complex` scalar or a `torch.Tensor`.

### Prompt Snippet
```text
Use `PyTorchBackend.iscomplex(x)` from `tslearn.backend.pytorch_backend` to check if a scalar or tensor is complex.
```

### Common Failure Modes
- **ImportError:** `cannot import name 'iscomplex' from 'tslearn.backend.pytorch_backend'`. This occurs because `iscomplex` is a `@staticmethod` nested inside the `PyTorchBackend` class, not a module-level function.
- **AttributeError:** Raising `'...' object has no attribute 'dtype'` if `x` is not a `complex` scalar and lacks a `dtype` attribute (e.g., standard Python `float`, `int`, or `list`).
- **Audience Misuse:** Attempting to use this INTERNAL/FRAMEWORK helper in standard user workflows instead of relying on high-level estimators or the generic backend dispatcher.

### Fix Code Hint
```python
# BAD: Attempting to import as a module-level function
from tslearn.backend.pytorch_backend import iscomplex
res = iscomplex(x)

# GOOD: Importing the class and calling the static method
from tslearn.backend.pytorch_backend import PyTorchBackend
res = PyTorchBackend.iscomplex(x)
```