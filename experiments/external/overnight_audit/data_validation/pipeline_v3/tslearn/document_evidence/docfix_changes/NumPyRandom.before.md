## API Test: `NumPyRandom`

### Signature
```python
class NumPyRandom
```
_Source: tslearn/tslearn/backend/numpy_backend.py:132_

### Goal
A backend-specific helper class that encapsulates random number generation utilities for the NumPy computational backend in `tslearn`.

### Parameters
_None._

### Input
No arguments are required to instantiate this class. It is typically instantiated internally by the `NumPyBackend` to provide a unified random number generation interface.

### Output
Returns `unspecified` — an instance of the `NumPyRandom` class. (Note: Specific random generation methods attached to this class are not detailed in the provided API facts).

### Valid Call Patterns
```python
# Inferred from signature (no verbatim examples provided in context)
from tslearn.backend.numpy_backend import NumPyRandom

# Instantiate the NumPy random helper
np_random = NumPyRandom()

# Verify the instance type
assert isinstance(np_random, NumPyRandom), "Failed to instantiate NumPyRandom"
print(f"Successfully instantiated: {type(np_random).__name__}")
```

### LLM Instruction Prompt
- Do not pass any arguments when instantiating `NumPyRandom`.
- Recognize that this is a low-level backend helper class. In standard `tslearn` workflows, users typically do not instantiate this directly; instead, they access random utilities via the `.random` attribute of an instantiated backend object (e.g., from `instantiate_backend()`).
- Do not invent or assume specific method signatures on this class without verifying them against the active backend's capabilities.

### Prompt Snippet
```text
When working with tslearn's backend system, `NumPyRandom` is the class responsible for random operations under the NumPy backend. It takes no initialization parameters. Instantiate it directly via `NumPyRandom()` if explicitly required for low-level backend extensions.
```

### Common Failure Modes
- **Passing arguments to the constructor:** The `NumPyRandom` class signature accepts no parameters. Passing seeds or dimensions during instantiation will raise a `TypeError`.
- **Assuming PyTorch compatibility:** This class is strictly for the NumPy backend. If the active backend is PyTorch (e.g., for automatic differentiation with `soft_dtw`), the equivalent `PyTorchRandom` should be used instead.

### Fix Code Hint
```python
# BAD: Passing a seed or shape to the constructor
# rng = NumPyRandom(seed=42)

# GOOD: Instantiate without arguments (seeding is handled by backend methods, not the constructor)
from tslearn.backend.numpy_backend import NumPyRandom
rng = NumPyRandom()
```