## API Test: `select_backend`

### Signature
```python
def select_backend(data)
```
_Source: tslearn/tslearn/backend/backend.py:31_

_Source doc:_ Select backend. Parameter --------- data : array-like or string or None Indicates the backend to choose. Optional, default equals None. Returns ------- backend : class The backend class. If data is a Numpy array or data equals 'numpy' or data is None, backend equals NumpyBackend(). If data is a PyTorch array or data equals 'pytorch', backend equals PytorchBackend().

### Goal
Selects and returns the appropriate computational backend instance (`NumpyBackend` or `PytorchBackend`) based on the provided data type or string identifier.

### Parameters
- `data`: An array-like object (e.g., NumPy array, PyTorch tensor), a string (`'numpy'`, `'pytorch'`), or `None` indicating which backend to choose. Defaults to `None`.

### Input
A valid time-series data object (NumPy array or PyTorch tensor), a string literal specifying the backend, or `None`. If a PyTorch tensor or `'pytorch'` is provided, the `pytorch` package must be installed locally in the environment.

### Output
Returns `unspecified` — represents the instantiated backend object (e.g., `NumpyBackend()` or `PytorchBackend()`) used for backend-agnostic metric computations and automatic differentiation.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import select_backend

# Example inferred from signature (not verified by existing tests)

# 1. Select backend using a string identifier
be_from_str = select_backend("numpy")

# 2. Select backend dynamically from a NumPy array
data_array = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])
be_from_data = select_backend(data_array)

# 3. Default fallback behavior
be_default = select_backend(None)

# Assert falsifiable property: all three should resolve to the same NumPy backend class
assert type(be_from_str) == type(be_from_data) == type(be_default), "Backend types diverged unexpectedly."

# Print correctness witness
print(f"Selected backend type: {type(be_from_str).__name__}")
```

### LLM Instruction Prompt
- When dynamically resolving the computational backend for time-series metrics, use `select_backend(data)`. 
- Pass the input array/tensor, a string (`"numpy"` or `"pytorch"`), or `None`. 
- Note that if PyTorch is requested, the environment must have `pytorch` installed. Unrecognized inputs or `None` will safely default to the NumPy backend.
- Do not expect a string return value; this function returns the actual backend class instance.

### Prompt Snippet
```text
from tslearn.backend import select_backend

# Auto-detect backend from data type or string
backend = select_backend(X_train)
# backend is now an instance of NumpyBackend() or PytorchBackend()
```

### Common Failure Modes
- **Missing Dependencies:** Requesting the PyTorch backend (`data='pytorch'` or passing a PyTorch tensor) in an environment where the `pytorch` package is not installed locally.
- **Type Misconceptions:** Assuming `select_backend` returns a string identifier; it returns a backend class instance (e.g., `NumpyBackend()`).
- **Unrecognized Strings:** Passing an unsupported string (e.g., `"tensorflow"`) will silently default to `NumpyBackend()` rather than raising a validation error.

### Fix Code Hint
```python
# Ensure safe fallback to numpy if pytorch is unavailable
try:
    import torch
    data = torch.tensor([[[1.0], [2.0]]], requires_grad=True)
    be = select_backend(data)
except ImportError:
    import numpy as np
    data = np.array([[[1.0], [2.0]]])
    be = select_backend("numpy")
```