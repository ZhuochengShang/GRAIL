## API Test: `deprecated`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def deprecated(*, version, version_removed)
```

### Goal
INTERNAL/FRAMEWORK utility. Exclude from main user-facing benchmark denominator. Used by library maintainers to mark legacy functions as deprecated, emitting a `FutureWarning` when the decorated function is called.

### Parameters
- `version` (str): The version string indicating when the function was first marked as deprecated. Must be passed as a keyword argument.
- `version_removed` (str): The version string indicating the future release when the function is slated for removal. Must be passed as a keyword argument.

### Input
INTERNAL/FRAMEWORK API. Takes a target callable (via decorator syntax). Requires `version` and `version_removed` to be passed strictly as keyword arguments due to the `*` in the signature.

### Output
Returns a wrapped callable (decorator) that emits a `FutureWarning` via the `warnings` module, then executes and returns the result of the original function.

### Valid Call Patterns
```python
import warnings
from mir_eval.util import deprecated

@deprecated(version="0.8", version_removed="0.9")
def dummy_func():
    return 42

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    # The function MUST be called to trigger the warning
    result = dummy_func()

assert result == 42
assert len(w) == 1
assert issubclass(w[-1].category, FutureWarning)
```

### LLM Instruction Prompt
When testing the internal `@deprecated` decorator, you must pass `version` and `version_removed` as keyword arguments. To verify it works, you must actually *call* the decorated function and catch the resulting `FutureWarning` (not `DeprecationWarning`) using the standard library `warnings` module.

### Prompt Snippet
`mir_eval.util.deprecated(*, version, version_removed)` is an internal decorator. Calling the decorated function emits a `FutureWarning` (not `DeprecationWarning`). Both arguments are keyword-only.

### Common Failure Modes
- **INTERNAL/FRAMEWORK API:** This is not a standard MIR evaluation metric; do not use it for evaluating audio tasks.
- **Wrong Warning Category:** Asserting the emitted warning is a `DeprecationWarning`. The decorator explicitly emits a `FutureWarning` (`category=FutureWarning`).
- **Not Calling the Function:** Assigning the function object to a variable (e.g., `result = dummy_func`) instead of calling it (`result = dummy_func()`). The warning is only emitted when the internal wrapper executes during a function call.
- **Positional Arguments:** Passing `version` and `version_removed` as positional arguments raises a `TypeError` due to the `*` in the signature.

### Fix Code Hint
```python
# BAD: Asserting DeprecationWarning or failing to call the function
@deprecated(version="0.8", version_removed="0.9")
def old_func(): 
    pass

with warnings.catch_warnings(record=True) as w:
    result = old_func  # Function not called! No warning emitted.
    # assert issubclass(w[-1].category, DeprecationWarning) # Wrong category!

# GOOD: Call the function and assert FutureWarning
@deprecated(version="0.8", version_removed="0.9")
def old_func(): 
    pass

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    result = old_func() # Function called
    assert issubclass(w[-1].category, FutureWarning)
```