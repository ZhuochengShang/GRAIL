## API Test: `PyTorchBackend`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class PyTorchBackend(object)
```

### Goal
Instantiates the PyTorch backend utility class. **INTERNAL/FRAMEWORK API**: This is an internal infrastructure component and should be excluded from the main user-facing benchmark denominator. It is testable only with explicit low-level construction.

### Parameters
_None._

### Input
**INTERNAL/FRAMEWORK API**: No arguments are required. The caller must ensure `torch` is installed in the environment; otherwise, instantiation will unconditionally raise a `ValueError`.

### Output
An instance of `PyTorchBackend` providing PyTorch-specific implementations of array operations (e.g., `array`, `is_array`) and mapping `torch` data types (e.g., `float32`).

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

# Explicit low-level construction from the internal module
be = PyTorchBackend()

# Exercise the backend's array creation and type checking
data = [1.0, 2.0, 3.0]
tensor = be.array(data, dtype=be.float32)

# Assert falsifiable properties
assert be.backend_string == "pytorch", "Expected backend string to be 'pytorch'"
assert be.is_array(tensor), "Expected the created object to be recognized as a tensor"

# Print correctness witness
print(f"__CHECK__ PyTorchBackend {tensor.shape}")
```

### LLM Instruction Prompt
- Import `PyTorchBackend` directly from `tslearn.backend.pytorch_backend`, NOT `tslearn.backend`.
- Call `PyTorchBackend()` with exactly zero arguments.
- Use `be.array()` to create a tensor and `be.is_array()` to verify it, rather than relying on undefined variables or unverified methods.
- Ensure `import torch` is included.

### Prompt Snippet
```text
`tslearn.backend.pytorch_backend.PyTorchBackend()` is an internal framework class for PyTorch tensor operations. It takes no arguments. It is not exposed in `tslearn.backend` and must be imported from its specific submodule. Raises ValueError if `torch` is not installed.
```

### Common Failure Modes
- **INTERNAL/FRAMEWORK API Import Error:** Attempting `from tslearn.backend import PyTorchBackend` fails with `ImportError` because it is not exposed in the package root's `__init__.py`. It must be imported from `tslearn.backend.pytorch_backend`.
- **Undefined Variables / Unverified Methods:** Relying on undefined variables (like `s1`) or unverified methods instead of using the explicitly defined `array` and `is_array` methods.
- **Missing PyTorch Dependency:** Instantiating the class when `torch` is not installed raises a `ValueError`.

### Fix Code Hint
```python
# Incorrect: Importing from the public namespace and using undefined variables
# from tslearn.backend import PyTorchBackend
# be = PyTorchBackend()
# tensor = be.array(s1)

# Correct: Importing from the internal submodule and using defined methods
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

be = PyTorchBackend()
tensor = be.array([1.0, 2.0, 3.0], dtype=be.float32)
assert be.is_array(tensor)
```