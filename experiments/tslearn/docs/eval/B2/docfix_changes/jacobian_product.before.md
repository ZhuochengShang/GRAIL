## API Test: `jacobian_product`

### Signature
```python
def jacobian_product(self, E)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1218_

_Source doc:_ Compute the product between the Jacobian (a linear map from m x d to m x n) and a matrix E. Parameters ---------- E: array-like, shape=(m, n) Second time series. Returns ------- G: array-like, shape=(m, d) Product with Jacobian. ([m x d, m x n] * [m x n] = [m x d]).

### Goal
Computes the product between a Jacobian matrix (representing a linear map from `m x d` to `m x n`) and a matrix `E` of shape `(m, n)`.

### Parameters
- `self`: The instance of the undocumented class in `tslearn.metrics.softdtw_variants` that provides this method.
- `E`: array-like of shape `(m, n)`. Represents the second time series or a matrix to be multiplied with the Jacobian.

### Input
The caller must provide an instantiated object that implements this method, and an array-like `E` (e.g., a NumPy array) with exactly two dimensions `(m, n)`.

### Output
Returns `unspecified` — an array-like object `G` of shape `(m, d)` representing the product of the Jacobian and `E`.

### Valid Call Patterns
```python
from unittest.mock import Mock
import numpy as np

# Example inferred from signature (not verified).
# The exact tslearn class is unknown from the provided facts.
instance = Mock()
instance.jacobian_product.return_value = np.zeros((5, 3)) # shape (m, d)

# E must be a 2D array of shape (m, n)
E = np.zeros((5, 4)) 
G = instance.jacobian_product(E)

assert G.shape == (5, 3)
print("Call pattern demonstrated via mock.")
```

### LLM Instruction Prompt
- Call `jacobian_product(E)` as an instance method on the appropriate object from `tslearn.metrics.softdtw_variants`, never as a standalone function.
- Ensure the input `E` is a 2D array-like of shape `(m, n)`.
- Expect the output to be a 2D array-like of shape `(m, d)`.
- Note that the exact class implementing this method is not specified in the standard documentation context; if something is unknown, say so rather than guessing.

### Prompt Snippet
```text
# Call as an instance method on the appropriate object
G = instance.jacobian_product(E)
```

### Common Failure Modes
- Attempting to import and call `jacobian_product` as a standalone module-level function, which will raise an `ImportError` or `NameError`.
- Passing an `E` matrix with incorrect dimensions (e.g., a standard `tslearn` 3D time-series dataset `(n_ts, max_sz, d)` instead of the expected 2D `(m, n)` shape).

### Fix Code Hint
```python
# WRONG: Calling as a standalone function or passing a 3D array
# from tslearn.metrics.softdtw_variants import jacobian_product
# G = jacobian_product(E_3d)

# CORRECT: Calling on the appropriate instance with a 2D array
G = instance.jacobian_product(E_2d)
```