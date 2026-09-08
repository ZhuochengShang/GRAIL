# Deep-dive: `deprecated`

model: google:gemini-3.1-pro-preview · tokens in=2,743 out=2,464 · wall 25s · 2026-09-08 01:23

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
INTERNAL/FRAMEWORK. This API is a utility intended for library maintainers to manage the lifecycle of the library's public surface, rather than a tool for end-users to evaluate music information retrieval tasks. It should be excluded from a main user-facing benchmark denominator.
TESTABLE FROM PUBLIC INPUTS. The decorator can be applied to any arbitrary dummy function in a test harness and its effects (warnings) can be observed using standard Python library tools.

**L1 PURPOSE**
The `deprecated` function is a decorator factory used to mark legacy functions within the `mir_eval` library as deprecated. It intercepts calls to the decorated function, emits a standardized `FutureWarning` indicating when the function was deprecated and when it will be removed, and then proceeds to execute the original function.

**L2 CONTRACT**
- **Parameters:**
  - `version` (str): The version string indicating when the function was first marked as deprecated. Must be passed as a keyword argument.
  - `version_removed` (str): The version string indicating the future release when the function is slated for removal. Must be passed as a keyword argument.
- **Returns:** 
  - A decorator function that wraps a target callable.
- **Side Effects:** 
  - When the decorated function is invoked, it emits a `FutureWarning` via the `warnings` module.

**L3 MECHANICS**
The `deprecated` function defines an internal `__wrapper(func, *args, **kwargs)` function. When the decorated function is called, `__wrapper` executes first. It constructs a warning message containing the target function's module (`func.__module__`), name (`func.__name__`), the `version`, and the `version_removed`. It calls `warnings.warn` with `category=FutureWarning` and `stacklevel=3` (to ensure the warning points to the user's call site rather than the internals of the decorator). After emitting the warning, it delegates execution to the original function via `func(*args, **kwargs)` and returns its result. The decorator itself is constructed by passing `__wrapper` to an external `decorator` utility (likely from the `decorator` package, which preserves function signatures).

**L4 CORRECT MINIMAL USAGE**
```python
import warnings
from mir_eval.util import deprecated

# Apply the decorator using keyword arguments as required by the signature
@deprecated(version="0.8", version_removed="0.9")
def dummy_func():
    return 42

# Catch the warning to verify the decorator works without polluting stdout
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    
    # The function MUST be called to trigger the warning
    result = dummy_func()
    
    assert result == 42
    assert len(w) == 1
    assert issubclass(w[-1].category, FutureWarning)
    assert "Deprecated as of mir_eval version 0.8" in str(w[-1].message)
```

**L5 FAILURE FORENSICS**
The recorded failed attempt failed with an `AssertionError` because it never actually invoked the decorated function. The code executed `result = dummy_func` (assigning the function object to a variable) instead of `result = dummy_func()` (calling the function). Because the function was not called, the internal `__wrapper` was never executed, and no `FutureWarning` was emitted. Any subsequent assertions in the hidden test harness (such as `assert len(w) > 0`) would have failed, raising the `AssertionError`.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** I inferred that the `decorator` function called on line 962 comes from the external `decorator` library (a common dependency in scientific Python) based on the signature of `__wrapper`, which takes `func` as its first argument.
- **INFERENCE:** I inferred that the `AssertionError` in the failed attempt was caused by an unshown assertion checking the contents of the `warnings.catch_warnings` list `w`, which was empty because the function was not called.
- **Confidence in L2 (Contract):** 10/10. The signature strictly enforces keyword arguments via `*`, and the return behavior is clear from the source.
- **Confidence in L3 (Mechanics):** 10/10. The internal logic, including the specific `stacklevel` and warning category, is explicitly visible in the provided source code.
- **Confidence in L4 (Minimal Usage):** 10/10. The snippet correctly applies the decorator, invokes the function, and safely catches the resulting warning.