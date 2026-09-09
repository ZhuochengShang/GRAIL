## API Test: `fix_force_all_finite_warning`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def fix_force_all_finite_warning(func)
```

### Goal
INTERNAL/FRAMEWORK helper. Wraps a function to ensure compatibility with `scikit-learn` >= 1.6 by automatically translating the deprecated `force_all_finite` keyword argument to the newer `ensure_all_finite` equivalent during validation calls. Note: This is an internal compatibility shim and should be excluded from the main user-facing benchmark denominator.

### Parameters
- `func` (callable): The target function to be wrapped. In practice, this is typically `sklearn.utils.validation.check_array` or `check_X_y`.

### Input
INTERNAL/FRAMEWORK usage only. A callable function. When the wrapped function is executed, it expects keyword arguments (specifically `force_all_finite`).

### Output
A wrapped callable (`wrapper`) that accepts `*args` and `**kwargs`, intercepts and corrects the `force_all_finite` keyword argument if required by the installed `scikit-learn` version, and returns the result of `func(*args, **kwargs)`.

### Valid Call Patterns
```python
from tslearn.utils.utils import fix_force_all_finite_warning

@fix_force_all_finite_warning
def mock_validation(**kwargs):
    return kwargs

result = mock_validation(force_all_finite=False)

assert isinstance(result, dict), "Wrapped function should return the kwargs dictionary"
assert "force_all_finite" in result or "ensure_all_finite" in result, "Missing finite check kwarg in intercepted arguments"
assert any(v is False for v in result.values()), "The False value was not passed through by the decorator"

witness = "ensure_all_finite" if "ensure_all_finite" in result else "force_all_finite"
print(f"__CHECK__ fix_force_all_finite_warning {witness}={result[witness]}")
```

### LLM Instruction Prompt
To test the internal `fix_force_all_finite_warning` decorator, import it directly from `tslearn.utils.utils` (not `tslearn.utils`) and apply it to a mock function to verify it intercepts and translates the `force_all_finite` kwarg.

### Prompt Snippet
```text
Use `tslearn.utils.utils.fix_force_all_finite_warning` to decorate functions calling `scikit-learn` validation utilities. It is an internal helper and must be imported from the exact submodule, not the public namespace.
```

### Common Failure Modes
- **INTERNAL/FRAMEWORK API Import Error:** `ImportError: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils'`. The function is not exposed in the public `tslearn.utils` namespace and must be imported directly from `tslearn.utils.utils`.
- Passing a non-callable object to `fix_force_all_finite_warning`, which will raise a `TypeError` when the decorator attempts to wrap it.
- Assuming the decorator modifies positional arguments; it strictly intercepts the `force_all_finite` keyword argument.

### Fix Code Hint
```python
# WRONG: Attempting to import from the public namespace
from tslearn.utils import fix_force_all_finite_warning

# CORRECT: Importing from the internal submodule
from tslearn.utils.utils import fix_force_all_finite_warning

@fix_force_all_finite_warning
def my_check_array(*args, **kwargs):
    return kwargs
```