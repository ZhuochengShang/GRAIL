## API Test: `PyTorchBackend`

### Signature
```python
class PyTorchBackend
class PyTorchBackend(object)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:29  (+1 more definition site/overload)_

### Goal
Instantiates the PyTorch backend utility class, which provides tensor operations and automatic differentiation capabilities for time-series metrics.

### Parameters
_None._

### Input
No arguments are required to instantiate the class. The local environment must have the `pytorch` package installed to successfully utilize this backend's methods.

### Output
Returns `unspecified` — an instance of the `PyTorchBackend` class, which acts as a namespace/utility object providing PyTorch-specific implementations of array and mathematical operations.

### Valid Call Patterns
```python
# Inferred from signature (not verified in existing tests)
from tslearn.backend import PyTorchBackend

# Instantiate the backend directly (takes no arguments)
pytorch_be = PyTorchBackend()

# Verify instantiation
assert pytorch_be.__class__.__name__ == "PyTorchBackend"
print(f"Successfully instantiated: {type(pytorch_be)}")
```

### LLM Instruction Prompt
- Call `PyTorchBackend()` with exactly zero arguments.
- Note that in typical `tslearn` workflows, users do not need to instantiate this class directly; instead, they should use `tslearn.backend.instantiate_backend(..., "pytorch")` or pass `be="pytorch"` directly to metric functions (like `soft_dtw`) to auto-resolve the backend.
- Ensure `torch` is installed in the environment before attempting to use PyTorch backend features, as it is a strict precondition for automatic differentiation.

### Prompt Snippet
```text
`tslearn.backend.PyTorchBackend()` initializes the PyTorch backend for automatic differentiation and gradient computation. It takes no arguments. Typically accessed dynamically via `instantiate_backend` or by passing `be="pytorch"` to metric functions.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Providing strings (like `"pytorch"`) or configuration dictionaries to `PyTorchBackend()` will raise a `TypeError` because the constructor takes no arguments.
- **Missing PyTorch dependency:** Attempting to use the backend's tensor operations when the `pytorch` package is not installed locally will result in `ImportError` or fallback behaviors.

### Fix Code Hint
```python
# Incorrect: Passing a string identifier to the constructor
# be = PyTorchBackend("pytorch")

# Correct: Instantiate with no arguments
from tslearn.backend import PyTorchBackend
be = PyTorchBackend()

# Alternative (Preferred for dynamic workflows):
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
```