## API Test: `PyTorchRandom`

### Signature
```python
class PyTorchRandom
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:243_

### Goal
Provides a PyTorch-specific random number generator interface for the `tslearn` backend system, mirroring NumPy's random utilities.

### Parameters
_None._

### Input
No arguments are required for instantiation. The environment must have `torch` installed to use PyTorch backend components.

### Output
Returns `unspecified` — an instance of `PyTorchRandom` that serves as a random number generation namespace or utility for the PyTorch backend.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchRandom

# Inferred from signature (not verified)
rng = PyTorchRandom()

assert isinstance(rng, PyTorchRandom)
print("PyTorchRandom instantiated successfully.")
```

### LLM Instruction Prompt
- Use `PyTorchRandom` to access random number generation capabilities specifically tied to the PyTorch backend in `tslearn`.
- Do not pass any arguments to the constructor, as it takes no parameters.
- Ensure `torch` is installed in the environment before interacting with PyTorch backend helpers.
- Do not invent or call undocumented methods on the resulting instance.

### Prompt Snippet
```text
When working with the PyTorch backend in `tslearn`, use `PyTorchRandom()` to instantiate the backend-specific random number generator. It requires no initialization arguments.
```

### Common Failure Modes
- **Passing arguments to the constructor**: `PyTorchRandom` takes no parameters. Providing arguments will raise a `TypeError`.
- **Missing PyTorch dependency**: Attempting to import or use this class without `torch` installed will result in an `ImportError`.

### Fix Code Hint
```python
# Correct instantiation with no arguments
from tslearn.backend.pytorch_backend import PyTorchRandom

try:
    rng = PyTorchRandom()
except TypeError as e:
    print(f"Failed to instantiate: {e}")
```