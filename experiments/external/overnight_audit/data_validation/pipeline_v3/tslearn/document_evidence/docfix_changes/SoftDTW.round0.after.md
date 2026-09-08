## API Test: `SoftDTW`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class SoftDTW(D, gamma=1.0, be=None, compute_with_backend=False)
```

### Goal
ADVANCED/LOW-LEVEL algorithmic primitive encapsulating the stateful dynamic programming computation of the Soft-DTW discrepancy and its gradient. Note: Exclude from main user-facing denominator; users should typically use the `soft_dtw` function instead.

### Parameters
- `D`: `array-like` of shape `(m, n)` and dtype `float64`, OR an object with a `compute()` method. Represents the pairwise distances between the points of two time series.
- `gamma`: `float`, default `1.0`. Regularization parameter. Lower is less smoothed.
- `be`: Backend object, string, or `None`.
- `compute_with_backend`: `bool`, default `False`.

### Input
Requires explicit low-level construction. The caller must provide a precomputed 2D pairwise distance matrix `D` (e.g., squared Euclidean distances between points of two time series) to the constructor. `D` is caller-owned.

### Output
An instantiated `SoftDTW` object with two primary methods:
- `compute()`: Executes the forward pass, mutates internal state, and returns a `float` (the soft-DTW discrepancy).
- `grad()`: Executes the backward pass and returns an `array-like` of shape `(m, n)` (the gradient w.r.t `D`).

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import SoftDTW

# Construct a deterministic caller-owned pairwise distance matrix D for two time series
D = np.array([
    [0.0, 1.0, 4.0, 9.0],
    [1.0, 0.0, 1.0, 4.0],
    [4.0, 1.0, 0.0, 1.0]
], dtype=np.float64)

# Instantiate the low-level SoftDTW helper
sdtw = SoftDTW(D, gamma=1.0)

# Execute the forward pass
discrepancy = sdtw.compute()

# Execute the backward pass (gradient w.r.t D)
gradient = sdtw.grad()

assert gradient.shape == D.shape == (3, 4)
print(f"__CHECK__ SoftDTW discrepancy: {discrepancy:.4f}, gradient shape: {gradient.shape}")
```

### LLM Instruction Prompt
- Recognize `SoftDTW` as an ADVANCED/LOW-LEVEL class requiring a precomputed distance matrix `D` of shape `(m, n)`.
- Do not instantiate `SoftDTW` without arguments.
- You must call `compute()` before calling `grad()`.

### Prompt Snippet
```text
To use the low-level `SoftDTW` class, instantiate it with a 2D pairwise distance matrix `D`. Call `compute()` to get the discrepancy float, then `grad()` to get the `(m, n)` gradient array.
```

### Common Failure Modes
- **Missing required positional argument:** `TypeError: SoftDTW.__init__() missing 1 required positional argument: 'D'`. This happens if instantiated without arguments.
- **Calling `grad()` prematurely:** `ValueError: Needs to call compute() first.` if `grad()` is called before `compute()`.
- **Misunderstanding API audience:** Attempting to pass raw 3D time-series datasets directly to `SoftDTW`. It is an ADVANCED/LOW-LEVEL primitive requiring a 2D pairwise distance matrix (exclude from main user-facing denominator).

### Fix Code Hint
```python
# WRONG: Instantiating without arguments (causes TypeError)
sdtw = SoftDTW()

# CORRECT: Passing a precomputed 2D distance matrix D
import numpy as np
from tslearn.metrics import SoftDTW

D = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.float64)
sdtw = SoftDTW(D, gamma=1.0)
discrepancy = sdtw.compute()
gradient = sdtw.grad()
```