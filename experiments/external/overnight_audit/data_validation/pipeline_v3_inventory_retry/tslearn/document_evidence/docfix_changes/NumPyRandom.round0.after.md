## API Test: `NumPyRandom`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class NumPyRandom
```
_Source: tslearn/tslearn/backend/numpy_backend.py:132_

### Goal
INTERNAL/FRAMEWORK backend-specific helper class that encapsulates random number generation utilities for the NumPy computational backend. Recommendation: exclude from the main user-facing benchmark denominator as it is a backend implementation detail.

### Parameters
_None._

### Input
No arguments are required to instantiate this class. As an INTERNAL/FRAMEWORK API, it is typically instantiated internally by the `NumPyBackend` to provide a unified random number generation interface, but it is testable with explicit low-level construction.

### Output
Returns an instance of `NumPyRandom`. The instance exposes `rand`, `randint`, and `randn` attributes, which are bound directly to `numpy.random.rand`, `numpy.random.randint`, and `numpy.random.randn`.

### Valid Call Patterns
```python
from tslearn.backend.numpy_backend import NumPyRandom
import numpy as np

# Instantiate the low-level backend helper
np_random = NumPyRandom()

# Exercise the bound methods (delegates to numpy.random)
rand_array = np_random.rand(2, 3)
randint_array = np_random.randint(0, 10, size=(4,))
randn_array = np_random.randn(2)

# Assert falsifiable properties of the generated outputs
assert isinstance(rand_array, np.ndarray), "Expected a NumPy array"
assert rand_array.shape == (2, 3), "Expected shape (2, 3)"
assert randint_array.shape == (4,), "Expected shape (4,)"
assert randn_array.shape == (2,), "Expected shape (2,)"

print(f"__CHECK__ NumPyRandom {rand_array.shape}")
```

### LLM Instruction Prompt
- Recognize this as an INTERNAL/FRAMEWORK class testable via low-level construction.
- Do not pass any arguments when instantiating `NumPyRandom`.
- To verify the instance, callers must invoke one of the bound methods (e.g., `np_random.rand(2, 3)`) and assert the shape or type of the returned NumPy array.
- The exact bound methods (`rand`, `randint`, `randn`) are a stable part of the class contract; do not omit them from verification.

### Prompt Snippet
```text
`NumPyRandom` is an internal backend helper taking no parameters. It binds `rand`, `randint`, and `randn` directly to `numpy.random`. Verify it by explicitly calling these methods and asserting the output shapes.
```

### Common Failure Modes
- **Omission of bound method verification:** Failing to assert falsifiable properties because the documentation previously omitted the bound methods and warned against assuming them. The test merely instantiated the class and stopped. Callers must exercise `rand`, `randint`, or `randn` to verify correctness.
- **Direct user workflow usage:** Treating this INTERNAL/FRAMEWORK class as a standard user-facing tool rather than a low-level backend implementation detail.
- **Passing arguments to the constructor:** The `NumPyRandom` class signature accepts no parameters. Passing seeds or dimensions during instantiation will raise a `TypeError`.

### Fix Code Hint
```python
# BAD: Instantiating the class but failing to verify the bound methods
# np_random = NumPyRandom()
# assert isinstance(np_random, NumPyRandom)

# GOOD: Instantiate and explicitly exercise the bound methods to assert falsifiable properties
from tslearn.backend.numpy_backend import NumPyRandom
import numpy as np

np_random = NumPyRandom()
rand_array = np_random.rand(2, 3)
assert rand_array.shape == (2, 3)
```