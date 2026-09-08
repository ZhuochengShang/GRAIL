## API Test: `NumPyBackend`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class NumPyBackend(object)
```

### Goal
ADVANCED/LOW-LEVEL. Instantiate the concrete NumPy computational backend used internally by `tslearn` to delegate array operations and metrics to CPU-based libraries. 
*Note: Exclude this API from the main user-facing denominator; standard users should rely on `tslearn.backend.instantiate_backend()` instead.*

### Parameters
_None._

### Input
No arguments are required. (ADVANCED/LOW-LEVEL API; the caller owns the instantiated backend object).

### Output
Returns an instance of `NumPyBackend` exposing standard NumPy, SciPy, and scikit-learn array operations and distance metrics as bound attributes.

### Valid Call Patterns
```python
from tslearn.backend.numpy_backend import NumPyBackend

backend = NumPyBackend()
X = backend.array([[1.0, 2.0], [3.0, 4.0]])
shape_X = backend.shape(X)

assert shape_X == (2, 2), f"Expected shape (2, 2), got {shape_X}"
print(f"__CHECK__ NumPyBackend {shape_X}")
```

### LLM Instruction Prompt
- Import `NumPyBackend` exactly from `tslearn.backend.numpy_backend`. It is not exposed in the `tslearn.backend` root namespace.
- Code examples must construct their own arrays (e.g., using `backend.array(...)`) rather than assuming the existence of pre-defined variables like `X`.
- Recognize this as an advanced/internal API.

### Prompt Snippet
```text
`tslearn.backend.numpy_backend.NumPyBackend()` creates the internal NumPy backend instance. It takes no arguments and must be imported from its exact module path, not the `tslearn.backend` root.
```

### Common Failure Modes
- **ImportError**: Failing with `cannot import name 'NumPyBackend' from 'tslearn.backend'`. The class is not hoisted to the root namespace and must be imported directly from `tslearn.backend.numpy_backend`.
- **NameError**: Failing because code examples reference an undefined variable `X` instead of constructing a test array explicitly with `backend.array(...)`.
- **Audience Mismatch**: Using this ADVANCED/LOW-LEVEL constructor in standard user workflows instead of the dynamic `instantiate_backend()` helper.

### Fix Code Hint
```python
# WRONG:
from tslearn.backend import NumPyBackend
backend = NumPyBackend()
shape_X = backend.shape(X)  # X is undefined

# CORRECT:
from tslearn.backend.numpy_backend import NumPyBackend
backend = NumPyBackend()
X = backend.array([[1.0, 2.0], [3.0, 4.0]])
shape_X = backend.shape(X)
```