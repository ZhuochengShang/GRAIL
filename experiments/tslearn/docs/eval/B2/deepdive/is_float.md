# Deep-dive: `is_float`

model: google:gemini-3.1-pro-preview · tokens in=2,854 out=2,526 · wall 21s · 2026-09-08 15:38

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** ADVANCED/LOW-LEVEL. This is a backend abstraction helper used primarily by library developers or advanced users writing custom, backend-agnostic time-series metrics.
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. The method is accessed via a backend instance, which must first be explicitly constructed using `tslearn.backend.instantiate_backend`.

**L1 PURPOSE**
The `is_float` API is a backend-agnostic helper method used to verify whether a given scalar value (such as the output of a distance computation or alignment score) is a floating-point type recognized by the currently active computational backend (e.g., NumPy or PyTorch). It sits in the backend abstraction layer, allowing `tslearn` algorithms to validate scalar types without hardcoding backend-specific type checks.

**L2 CONTRACT**
- **Receiver:** A backend instance (e.g., `NumPyBackend`), obtained by calling `tslearn.backend.instantiate_backend(backend_name)` or passing an array to it.
- **Parameters:** 
  - `x` (Any): The object to be evaluated.
- **Return Value:** `bool`. Returns `True` if the object is a scalar floating-point type recognized by the backend, and `False` otherwise.
- **Visibility:** Public (part of the public backend API).
- **Thread-safety/Laziness:** Thread-safe as it performs a pure, stateless type check.

**L3 MECHANICS**
- In the NumPy backend (`tslearn/tslearn/backend/numpy_backend.py:106`), `is_float` is implemented as a `@staticmethod`.
- It delegates directly to Python's built-in `isinstance` function, checking if the input `x` is an instance of either `numpy.floating` or Python's native `float` (`isinstance(x, (_np.floating, float))`).
- **Crucial Distinction:** It evaluates the type of the *object itself*, not the `dtype` of an array. Passing a NumPy `ndarray` (even one containing floats) will return `False` because an `ndarray` is not a subclass of `numpy.floating` or `float`.

**L4 CORRECT MINIMAL USAGE**
```python
from tslearn.backend import instantiate_backend
import numpy as np

# 1. Explicitly construct the low-level backend receiver
backend = instantiate_backend("numpy")

# 2. Create a scalar float (simulating a distance metric output)
distance_score = np.float64(12.34)

# 3. Evaluate using the backend helper
result = backend.is_float(distance_score)

print(f"Correctness witness: {result}")
assert result is True, "Expected the backend to identify np.float64 as a float."

# Note: Arrays evaluate to False
array_val = np.array([1.0, 2.0])
assert backend.is_float(array_val) is False
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `res_float = backend.is_float(X)` where `X` was a balanced time-series dataset `ndarray` of floats.
- **Why it failed:** The test expected `is_float` to inspect the array's `dtype` and return `True` for a float array. However, as seen in `numpy_backend.py:107` (`return isinstance(x, (_np.floating, float))`), the method checks if the object *is* a scalar float. An `ndarray` is not an instance of `_np.floating` or `float`, causing the method to return `False` and triggering the `AssertionError`. The method is designed for scalars (like the `dtw_sakoe` distance in the real call site), not arrays.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - The exact class name in `numpy_backend.py` is inferred to be `NumPyBackend` based on standard naming conventions and the presence of `NumPyLinalg` below it, though the class definition line is cut off in the provided snippet.
  - The PyTorch implementation (`pytorch_backend.py:159`) is inferred to perform an equivalent scalar/0-d tensor type check for PyTorch float types.
- **Information needed for certainty:** The full source of `pytorch_backend.py` to confirm exactly how PyTorch tensors are evaluated (e.g., whether it checks `x.is_floating_point()` or `x.dtype`).
- **Confidence Scores:**
  - **L2 (Contract):** 9/10. The contract is clear from the NumPy source and real call sites, though PyTorch specifics are inferred.
  - **L3 (Mechanics):** 10/10. The NumPy mechanics are explicitly visible in the provided source code snippet.
  - **L4 (Usage):** 10/10. The usage pattern perfectly matches the real call site from `test_metrics.py` and correctly avoids the array-passing trap identified in the failure forensics.