## API Test: `PyTorchRandom`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class PyTorchRandom
```

### Goal
INTERNAL/FRAMEWORK API. Provides a PyTorch-specific random number generator interface mirroring NumPy's random utilities for the `tslearn` backend system. Excluded from the main user-facing denominator; testable only via explicit low-level construction.

### Parameters
_None._ (The constructor takes no arguments).

### Input
Requires explicit low-level construction (`PyTorchRandom()`). 
Static methods accept standard distribution parameters:
- `normal(loc=0.0, scale=1.0, size=(1,))`
- `uniform(low=0.0, high=1.0, size=(1,), dtype=None)`

### Output
Returns a `PyTorchRandom` instance.
- Instance attributes `rand`, `randint`, and `randn` are bound directly to their `torch` equivalents.
- Static methods `normal` and `uniform` return `torch.Tensor` objects.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchRandom

# Explicit low-level construction
rng = PyTorchRandom()

# Test instance attributes bound to torch functions
rand_tensor = rng.rand(2, 2)
assert isinstance(rand_tensor, torch.Tensor)
assert rand_tensor.shape == (2, 2)

# Test static method: normal
norm_tensor = PyTorchRandom.normal(loc=5.0, scale=2.0, size=3)
assert isinstance(norm_tensor, torch.Tensor)
assert norm_tensor.shape == (3,)

# Test static method: uniform
unif_tensor = PyTorchRandom.uniform(low=10.0, high=20.0, size=(4, 1))
assert isinstance(unif_tensor, torch.Tensor)
assert unif_tensor.shape == (4, 1)
assert (unif_tensor >= 10.0).all() and (unif_tensor <= 20.0).all()

print("PyTorchRandom instantiated and methods verified successfully.")
```

### LLM Instruction Prompt
To test the internal `PyTorchRandom` framework API, instantiate it explicitly and exercise its methods to assert falsifiable properties. Use instance attributes (`rand`, `randint`, `randn`) or static methods (`normal`, `uniform`) to generate `torch.Tensor` objects and verify their shapes or bounds.

### Prompt Snippet
```text
`PyTorchRandom` is an internal framework class. Instantiate it with `PyTorchRandom()` and call its static methods `normal(loc, scale, size)` or `uniform(low, high, size)`, or use its instance attributes `rand`, `randint`, and `randn` (bound to `torch` functions) to generate tensors and assert their shapes.
```

### Common Failure Modes
- **AssertionError: The documented contract is insufficient to verify the result**: Failing to exercise the API. Merely instantiating the class without calling its methods (`normal`, `uniform`, `rand`, etc.) and asserting falsifiable properties (like tensor shapes or bounds) will fail the test harness.
- **INTERNAL/FRAMEWORK API misuse**: This is a low-level backend helper not intended for standard user workflows. It must be explicitly imported from `tslearn.backend.pytorch_backend`.
- **Invalid bounds in `uniform`**: Passing `low >= high` raises a `ValueError`.

### Fix Code Hint
```python
# WRONG: Instantiating without exercising methods (fails harness)
rng = PyTorchRandom()
assert isinstance(rng, PyTorchRandom)

# CORRECT: Exercise methods and assert falsifiable properties
rng = PyTorchRandom()
unif_tensor = rng.uniform(low=10.0, high=20.0, size=(4, 1))
assert unif_tensor.shape == (4, 1)
assert (unif_tensor >= 10.0).all() and (unif_tensor <= 20.0).all()
```