## API Test: `uniform`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def uniform(low=0.0, high=1.0, size=(1,), dtype=None)
```

### Goal
ADVANCED/LOW-LEVEL: Generates a tensor of uniformly distributed random numbers within a specified range `[low, high)`. This is an internal backend-specific helper method in `tslearn`'s PyTorch backend abstraction and should be excluded from the main user-facing denominator.

### Parameters
- `low` (float, default `0.0`): The lower bound (inclusive) of the uniform distribution.
- `high` (float, default `1.0`): The upper bound (exclusive) of the uniform distribution. Must be strictly greater than `low`.
- `size` (int or iterable of ints, default `(1,)`): The shape of the output tensor. If a scalar is provided, it is automatically converted to a 1-tuple.
- `dtype` (torch.dtype or None, default `None`): The desired data type of the output tensor. If `None`, uses the PyTorch default.

### Input
ADVANCED/LOW-LEVEL: Scalar bounds and a tuple (or scalar) for the desired shape. The PyTorch backend must be instantiated first via `tslearn.backend.instantiate_backend("pytorch")`, and the method must be accessed via the `random` attribute of the backend instance.

### Output
Returns a PyTorch `Tensor` of shape `size` containing random values sampled from the uniform distribution `[low, high)`.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

# Instantiate the PyTorch backend
be = instantiate_backend("pytorch")

# Access the uniform method via the backend's random module
arr = be.random.uniform(low=-2.0, high=5.0, size=(3, 4, 5))

assert arr.shape == (3, 4, 5), f"Expected shape (3, 4, 5), got {arr.shape}"
assert (arr >= -2.0).all() and (arr < 5.0).all(), "Values are out of the specified uniform bounds"

print(f"__CHECK__ uniform {arr.shape}")
```

### LLM Instruction Prompt
- When generating random uniform tensors within a backend-agnostic function using `tslearn`, access `uniform` via the `random` attribute on the instantiated backend object (e.g., `be.random.uniform()`). Do not call it directly on the backend object.

### Prompt Snippet
```text
from tslearn.backend import instantiate_backend

be = instantiate_backend("pytorch")
X_random = be.random.uniform(low=-1.0, high=1.0, size=(10, 50, 1))
```

### Common Failure Modes
- ADVANCED/LOW-LEVEL: This API is an internal backend helper and should be excluded from the main user-facing denominator.
- Calling `uniform` directly on the backend instance (`be.uniform(...)`). In the `tslearn` backend architecture, random generation methods are encapsulated within a nested class and must be accessed via the `random` attribute (`be.random.uniform(...)`).
- Using the NumPy backend when expecting the PyTorch-specific implementation. The PyTorch backend must be instantiated via `instantiate_backend("pytorch")`.
- Providing a `low` value that is greater than or equal to `high`, which raises a `ValueError("Upper bound must be higher than lower bound")`.

### Fix Code Hint
```python
# BAD: Calling uniform directly on the backend object
# from tslearn.backend import instantiate_backend
# be = instantiate_backend("pytorch")
# arr = be.uniform(low=-2.0, high=5.0, size=(3, 4, 5))

# GOOD: Access uniform via the random attribute of the instantiated backend
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
arr = be.random.uniform(low=-2.0, high=5.0, size=(3, 4, 5))
```