## API Test: `iscomplex`

### Signature
```python
def iscomplex(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:153_

### Goal
Determines whether a given PyTorch tensor has a complex data type, acting as a low-level backend helper for `tslearn` metric computations.

### Parameters
- `x`: The input PyTorch tensor to be evaluated for a complex data type.

### Input
A PyTorch tensor (`torch.Tensor`). The environment must have PyTorch installed locally to use this backend-specific helper.

### Output
Returns `unspecified` (typically a boolean) — indicates whether the input tensor's data type is complex (e.g., `torch.complex64` or `torch.complex128`).

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import iscomplex

# Note: Call form inferred from signature as no verbatim examples exist
real_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
complex_tensor = torch.tensor([1.0+1j, 2.0+2j], dtype=torch.complex64)

is_real_cplx = iscomplex(real_tensor)
is_cplx_cplx = iscomplex(complex_tensor)

assert not is_real_cplx, "Real tensor should not be complex"
assert is_cplx_cplx, "Complex tensor should be complex"
print(f"Complex check passed. Real: {is_real_cplx}, Complex: {is_cplx_cplx}")
```

### LLM Instruction Prompt
- Use `iscomplex` from `tslearn.backend.pytorch_backend` to check if a PyTorch tensor is complex-valued when writing custom PyTorch-backend extensions for `tslearn`.
- Do not pass NumPy arrays or standard Python lists to this specific PyTorch backend helper; it strictly expects PyTorch tensors.
- Remember that this is a low-level backend function; general users should typically rely on the dynamic backend dispatcher (`instantiate_backend`) rather than calling this directly.

### Prompt Snippet
```text
When operating within the PyTorch backend of `tslearn`, use `tslearn.backend.pytorch_backend.iscomplex(x)` to verify if a tensor `x` has a complex data type. Ensure `x` is a `torch.Tensor`.
```

### Common Failure Modes
- **Type Errors:** Passing a NumPy array, standard Python list, or scalar instead of a PyTorch tensor, which will cause PyTorch-specific type checks or attribute accesses to fail.
- **Missing Dependencies:** Attempting to import or use this function in an environment where the `pytorch` package is not installed.

### Fix Code Hint
```python
# BAD: Passing a NumPy array to the PyTorch backend helper
# import numpy as np
# iscomplex(np.array([1.0+1j]))

# GOOD: Ensure the input is a PyTorch tensor
import torch
from tslearn.backend.pytorch_backend import iscomplex

tensor_input = torch.tensor([1.0+1j], dtype=torch.complex64)
result = iscomplex(tensor_input)
```