## API Test: `normal`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def normal(loc=0.0, scale=1.0, size=(1,))
```

### Goal
INTERNAL-FRAMEWORK / ADVANCED: Generates a PyTorch tensor of random numbers drawn from a normal (Gaussian) distribution. This is a low-level backend helper nested inside the PyTorch backend implementation (`PyTorchRandom`). It is not meant for standard end-user workflows and should be excluded from main user-facing benchmarks.

### Parameters
- `loc`, default `0.0`: The mean (center) of the normal distribution (numeric scalar).
- `scale`, default `1.0`: The standard deviation (spread) of the normal distribution (numeric scalar).
- `size`, default `(1,)`: The shape of the output tensor (int or tuple of ints).

### Input
ADVANCED/LOW-LEVEL: Requires explicit low-level construction of the PyTorch backend. Numeric scalars for `loc` and `scale`, and an integer or tuple of integers for `size`.

### Output
A PyTorch `Tensor` of the specified `size`, populated with normally distributed random values.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

# Explicit low-level construction required
be = instantiate_backend("pytorch")

# Access via the backend's random namespace
noise_tensor = be.random.normal(loc=0.0, scale=0.1, size=(2, 5, 1))

assert noise_tensor.shape == (2, 5, 1)
print(f"__CHECK__ normal {noise_tensor.shape}")
```

### LLM Instruction Prompt
To test this internal framework helper, instantiate the PyTorch backend using `tslearn.backend.instantiate_backend("pytorch")`. You MUST access `normal` through the backend's `random` attribute (i.e., `be.random.normal(...)`), not directly on the backend object.

### Prompt Snippet
```text
For low-level backend testing, instantiate the PyTorch backend and call `normal` via its random namespace: `be = instantiate_backend("pytorch"); tensor = be.random.normal(loc=0.0, scale=1.0, size=(2, 5, 1))`.
```

### Common Failure Modes
- *AttributeError on backend:* Calling `normal` directly on the backend instance (`be.normal(...)`). It must be accessed via the `random` namespace (`be.random.normal(...)`).
- *Wrong backend instantiation:* Instantiating the `"numpy"` backend when testing this specific PyTorch implementation.
- *INTERNAL/FRAMEWORK API misuse:* Attempting to use this as a standard user-facing function without explicit low-level backend instantiation.

### Fix Code Hint
```python
# WRONG: Calling directly on the backend or using the wrong backend
be = instantiate_backend("numpy")
noise = be.normal(loc=0.0, scale=1.0, size=(2, 5, 1))

# CORRECT: Using the PyTorch backend and the random namespace
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
noise = be.random.normal(loc=0.0, scale=1.0, size=(2, 5, 1))
```