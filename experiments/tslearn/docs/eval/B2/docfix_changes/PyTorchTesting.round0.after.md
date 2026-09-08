## API Test: `PyTorchTesting`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class PyTorchTesting()
```

### Goal
INTERNAL/FRAMEWORK. Provides a low-level backend-specific utility class that abstracts PyTorch tensor equality and closeness checks for `tslearn`'s internal test suites. It is not intended for end-user time-series modeling workflows and should be excluded from main user-facing benchmark denominators.

### Parameters
None. The `__init__` method takes no arguments.

### Input
INTERNAL/FRAMEWORK API. Instantiation requires no inputs. To exercise the instance, callers must provide standard `torch.tensor` objects to its bound methods.

### Output
Returns a caller-owned instance of `PyTorchTesting` exposing two callable attributes:
- `assert_allclose`: Maps to `torch.allclose` (takes two tensors, returns a boolean).
- `assert_equal`: Maps to `torch.testing.assert_close` (takes two tensors, raises `AssertionError` if tensors are not close, returns `None` otherwise).

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchTesting

# Instantiate the testing utility (caller-owned)
tester = PyTorchTesting()

# Create dummy tensors for testing
t1 = torch.tensor([1.0, 2.0, 3.0])
t2 = torch.tensor([1.0, 2.0, 3.0])

# assert_allclose returns a boolean
is_close = tester.assert_allclose(t1, t2)
assert is_close is True, "Tensors should be allclose"

# assert_equal raises an AssertionError if not close, returns None otherwise
tester.assert_equal(t1, t2)

print(f"__CHECK__ PyTorchTesting {type(tester).__name__}")
```

### LLM Instruction Prompt
- Recognize this is an INTERNAL/FRAMEWORK API testable only with explicit low-level construction.
- Import `torch` and `tslearn.backend.pytorch_backend.PyTorchTesting`.
- Instantiate `PyTorchTesting` without arguments.
- Create dummy PyTorch tensors.
- Verify the object's behavior by passing the tensors to `tester.assert_allclose` (asserting it returns `True`) and `tester.assert_equal`.

### Prompt Snippet
```text
To verify the PyTorchTesting internal helper, instantiate it and use its bound PyTorch methods:
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchTesting
tester = PyTorchTesting()
t1 = torch.tensor([1.0, 2.0])
assert tester.assert_allclose(t1, t1) is True
tester.assert_equal(t1, t1)
```
```

### Common Failure Modes
- **`AssertionError: The documented contract is insufficient to verify the result.`**: This failure previously occurred because the prompt explicitly instructed the generator *not* to use specific testing methods, hiding the fact that `assert_allclose` and `assert_equal` are bound during `__init__`. The generator must use these methods to verify a falsifiable property.
- **INTERNAL/FRAMEWORK Misuse**: Attempting to use this class for standard time-series modeling workflows. It is strictly an internal backend abstraction.
- **Missing PyTorch dependency**: The local environment must have `torch` installed to import and create the required tensor inputs.

### Fix Code Hint
```python
# BAD: Instantiating without verifying bound methods (insufficient contract)
tester = PyTorchTesting()
assert isinstance(tester, PyTorchTesting)

# GOOD: Verify the bound PyTorch methods using dummy tensors
import torch
from tslearn.backend.pytorch_backend import PyTorchTesting

tester = PyTorchTesting()
t1 = torch.tensor([1.0, 2.0])
assert tester.assert_allclose(t1, t1) is True
tester.assert_equal(t1, t1)
```