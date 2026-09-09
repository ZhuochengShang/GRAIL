## API Test: `uniform`

### Signature
```python
def uniform(low=0.0, high=1.0, size=(1,), dtype=None)
```

### Goal
Generates an array or tensor of uniformly distributed random numbers within a specified range, using the active computational backend (NumPy or PyTorch).

### Parameters
- `low`, default `0.0`: The lower bound (inclusive) of the uniform distribution.
- `high`, default `1.0`: The upper bound (exclusive) of the uniform distribution.
- `size`, default `(1,)`: A tuple specifying the shape of the output array or tensor.
- `dtype`, default `None`: The desired data type of the output (e.g., `numpy.float64` or `torch.float64`). If `None`, defaults to the backend's standard float type.

### Input
Scalar bounds and a tuple for the desired shape. The backend must be instantiated first via `tslearn.backend.instantiate_backend`.

### Output
Returns `unspecified` — A backend-specific array or tensor (NumPy `ndarray` or PyTorch `Tensor`) containing random values sampled from the uniform distribution `[low, high)`.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")

# Call inferred from signature (not verified)
random_tensor = be.uniform(low=-0.5, high=0.5, size=(10, 5, 1))
assert random_tensor.shape == (10, 5, 1)
print(random_tensor.shape)
```

### LLM Instruction Prompt
- When generating random time-series data or initializing weights within a backend-agnostic function, use `be.uniform()` on the instantiated backend object rather than hardcoding `numpy.random.uniform` or `torch.rand`.

### Prompt Snippet
```text
from tslearn.backend import instantiate_backend

# Generate a random 3D time-series dataset using the PyTorch backend
be = instantiate_backend("pytorch")
X_random = be.uniform(low=-1.0, high=1.0, size=(10, 50, 1))
```

### Common Failure Modes
- Calling `uniform` directly as a module-level function instead of as a method on an instantiated backend object.
- Passing a scalar instead of a tuple for the `size` parameter, which may cause shape resolution errors in some backends.
- Requesting a `dtype` that is incompatible with the active backend (e.g., passing a PyTorch dtype to the NumPy backend).

### Fix Code Hint
```python
# BAD: Calling uniform directly or using incompatible dtypes
# import tslearn.backend as backend
# arr = backend.uniform(size=10)

# GOOD: Instantiate the backend and pass a tuple for size
from tslearn.backend import instantiate_backend
be = instantiate_backend("numpy")
arr = be.uniform(low=0.0, high=1.0, size=(10,))
```