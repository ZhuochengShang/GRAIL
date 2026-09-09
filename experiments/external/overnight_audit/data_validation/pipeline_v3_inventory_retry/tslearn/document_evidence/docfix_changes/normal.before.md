## API Test: `normal`

### Signature
```python
def normal(loc=0.0, scale=1.0, size=(1,))
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:250_

### Goal
Generates an array or tensor of random numbers drawn from a normal (Gaussian) distribution, utilizing the active computational backend (e.g., PyTorch or NumPy).

### Parameters
- `loc`, default `0.0`: The mean (center) of the normal distribution (numeric scalar).
- `scale`, default `1.0`: The standard deviation (spread) of the normal distribution (numeric scalar).
- `size`, default `(1,)`: The shape of the output array or tensor, provided as a tuple of integers.

### Input
Numeric scalars for `loc` and `scale`, and a tuple of integers for `size`. No specific preconditions other than valid dimensions.

### Output
Returns `unspecified` — A backend-specific data structure (e.g., a PyTorch `Tensor` or NumPy `ndarray`) of the specified `size`, populated with normally distributed random values.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")

# Call form inferred from signature and backend conventions
noise_array = be.normal(loc=0.0, scale=0.1, size=(2, 5, 1))

assert noise_array.shape == (2, 5, 1)
print("Generated normal array shape:", noise_array.shape)
```

### LLM Instruction Prompt
- Call `normal` via an instantiated backend object (e.g., `be.normal(...)`) to generate backend-native random arrays/tensors.
- Always provide `size` as a tuple of integers. To generate time-series data, use the standard `tslearn` 3D shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
To generate normally distributed random data in a backend-agnostic manner, instantiate a backend using `tslearn.backend.instantiate_backend` and call its `normal` method: `be.normal(loc=0.0, scale=1.0, size=(n_ts, max_sz, d))`.
```

### Common Failure Modes
- Calling `normal` as a top-level module function (e.g., `tslearn.normal()`) instead of accessing it through a backend instance.
- Passing a scalar instead of a tuple for `size`, which may cause PyTorch backend errors.
- Generating 1D or 2D data and passing it directly to `tslearn` estimators, which strictly require 3D `(n_ts, max_sz, d)` arrays.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend

# 1. Instantiate the backend
be = instantiate_backend("pytorch")

# 2. Call normal on the backend instance with a 3D size tuple
# (n_ts=5, max_sz=50, d=1)
random_ts = be.normal(loc=0.0, scale=1.0, size=(5, 50, 1))
```