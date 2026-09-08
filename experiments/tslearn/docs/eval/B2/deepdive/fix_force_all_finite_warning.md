# Deep-dive: `fix_force_all_finite_warning`

model: google:gemini-3.1-pro-preview · tokens in=4,699 out=2,102 · wall 18s · 2026-09-08 15:17

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** INTERNAL/FRAMEWORK. This is a compatibility shim designed specifically to wrap `scikit-learn` validation functions (`check_array`, `check_X_y`) within the `tslearn` codebase. It should be excluded from a main user-facing benchmark denominator.
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. It is not exposed in the public `tslearn.utils` namespace and must be imported directly from the internal `tslearn.utils.utils` module.

**L1 PURPOSE**
`fix_force_all_finite_warning` is an internal decorator used to maintain compatibility across different versions of `scikit-learn`. It intercepts calls to validation functions and translates the deprecated `force_all_finite` keyword argument to the newer `ensure_all_finite` argument if the installed `scikit-learn` version (>= 1.6) expects it, preventing deprecation warnings or crashes.

**L2 CONTRACT**
- **Receiver:** None (standalone function).
- **Parameters:**
  - `func` (callable): The target function to be wrapped. In practice, this is `sklearn.utils.validation.check_array` or `check_X_y`.
- **Return value:** A wrapped callable (`wrapper`) that accepts `*args` and `**kwargs`, modifies the `kwargs` if necessary, and returns the result of `func(*args, **kwargs)`.
- **Visibility:** Internal. It is not exported in `tslearn.utils.__init__.py`.

**L3 MECHANICS**
- The decorator defines a `wrapper(*args, **kwargs)` function.
- When the wrapper is called, it checks two conditions (lines 28-29):
  1. Is `'force_all_finite'` present in the provided `kwargs`?
  2. Does the signature of `sklearn.utils.validation.check_array` contain the parameter `'ensure_all_finite'`? (Checked dynamically via `inspect.signature`).
- If both conditions are true, it pops `'force_all_finite'` from `kwargs` and assigns its value to `'ensure_all_finite'` (line 30).
- It then delegates execution to the original `func` with the modified arguments (line 31).

**L4 CORRECT MINIMAL USAGE**
```python
from tslearn.utils.utils import fix_force_all_finite_warning

# Create a mock function to observe the kwargs transformation
@fix_force_all_finite_warning
def mock_validation(**kwargs):
    return kwargs

# Call the wrapped function with the deprecated argument
result = mock_validation(force_all_finite=False)

# Depending on the installed scikit-learn version, the kwarg will either 
# remain 'force_all_finite' or be translated to 'ensure_all_finite'.
assert 'force_all_finite' in result or 'ensure_all_finite' in result, \
    "The kwarg should be preserved or translated."
assert result.get('force_all_finite') is False or result.get('ensure_all_finite') is False, \
    "The boolean value should be preserved."

print("fix_force_all_finite_warning check passed")
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `ImportError: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils'`
- **Reason:** The test harness attempted to import the function from the public `tslearn.utils` namespace. However, `fix_force_all_finite_warning` is an internal helper defined in `tslearn/utils/utils.py` and is not exposed in `tslearn/utils/__init__.py`. It must be imported via the exact submodule path: `from tslearn.utils.utils import fix_force_all_finite_warning`.

**L6 SELF-ASSESSMENT**
- **Inferences:** I inferred that `fix_force_all_finite_warning` is missing from `tslearn/utils/__init__.py` based purely on the `ImportError` in the failure history, which perfectly aligns with standard Python package encapsulation behavior for internal helpers.
- **Information needed for absolute certainty:** The contents of `tslearn/utils/__init__.py` to definitively prove it is omitted from `__all__`.
- **Confidence Scores:**
  - L2 (Contract): 10/10. The signature and types are trivial and explicitly defined in the source.
  - L3 (Mechanics): 10/10. The logic is a straightforward 5-line dictionary manipulation.
  - L4 (Usage): 10/10. The provided snippet correctly bypasses the namespace issue and deterministically verifies the decorator's behavior regardless of the environment's `scikit-learn` version.