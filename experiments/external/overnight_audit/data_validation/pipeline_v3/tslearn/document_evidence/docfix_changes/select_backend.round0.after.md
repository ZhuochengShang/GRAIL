## API Test: `select_backend`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def select_backend(data)
```

### Goal
ADVANCED/LOW-LEVEL. Determines and instantiates the correct computational backend class (`NumPyBackend` or `PyTorchBackend`) based on the provided data or string identifier. This is a low-level utility used primarily by the framework's internal dispatch system. *Note: Exclude from the main user-facing denominator; include only in advanced/internal testing buckets.*

### Parameters
- `data` (array-like, string, or `None`): The input used to deduce the backend. Can be a literal string (e.g., `"numpy"`, `"pytorch"`), an actual array/tensor object, or `None`. Defaults to `None`.

### Input
ADVANCED/LOW-LEVEL. A valid time-series data object (NumPy array or PyTorch tensor), a string literal specifying the backend, or `None`. Evaluated eagerly using a permissive duck-typing string-matching heuristic (checks if the substring `"torch"` is present in the lowercase string representation of the data and its type).

### Output
Returns an instantiated object of either `NumPyBackend` or `PyTorchBackend`. 
*Correction:* The official docstring contains a typo (`NumpyBackend` / `PytorchBackend`), but the actual returned classes use specific capitalization: `NumPyBackend` (capital 'P') and `PyTorchBackend` (capital 'T').

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import select_backend

X = np.array([1, 2, 3])
be_from_data = select_backend(X)
be_from_str = select_backend("numpy")
be_default = select_backend(None)

# Assert falsifiable property: all three should resolve to the same NumPy backend class
assert type(be_from_data).__name__ == "NumPyBackend", f"Expected NumPyBackend, got {type(be_from_data).__name__}"
assert type(be_from_data) == type(be_from_str) == type(be_default), "Backend types diverged unexpectedly."

# Print correctness witness
print(f"__CHECK__ select_backend {type(be_from_data).__name__}")
```

### LLM Instruction Prompt
- Use `select_backend(data)` to dynamically resolve the computational backend.
- Pass an array/tensor, a string (`"numpy"` or `"pytorch"`), or `None`.
- **CRITICAL:** The returned backend class for NumPy is exactly named `NumPyBackend` (with a capital 'P'), not `NumpyBackend`.
- **CRITICAL:** The returned backend class for PyTorch is exactly named `PyTorchBackend` (with a capital 'T'), not `PytorchBackend`.
- Unrecognized inputs or `None` safely default to `NumPyBackend`.

### Prompt Snippet
```python
from tslearn.backend import select_backend

# Auto-detect backend from data type or string
backend = select_backend("numpy")
# backend is now an instance of NumPyBackend() (note the capital 'P')
```

### Common Failure Modes
- **ADVANCED/LOW-LEVEL API:** This is an internal/advanced helper. Do not present it as a standard user workflow.
- **Incorrect Class Name Assertion:** `AssertionError: Expected NumpyBackend, got NumPyBackend`. The documentation docstring loosely refers to `NumpyBackend()` and `PytorchBackend()`, but the actual instantiated classes are `NumPyBackend` and `PyTorchBackend`. Asserting against the lowercase 'p' or 't' will fail.
- **Unrecognized Strings:** Passing an unsupported string (e.g., `"tensorflow"`) will silently default to `NumPyBackend()` rather than raising a validation error because the heuristic only looks for the substring `"torch"`.

### Fix Code Hint
```python
# WRONG: Relying on the docstring typo
backend = select_backend("numpy")
assert type(backend).__name__ == "NumpyBackend"

# CORRECT: Using the actual class name instantiated by the source
backend = select_backend("numpy")
assert type(backend).__name__ == "NumPyBackend"
```