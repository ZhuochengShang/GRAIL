## API Test: `deprecated`

### Signature
```python
def deprecated(*, version, version_removed)
```
_Source: source/mir_eval/util.py:946_

_Source doc:_ Mark a function as deprecated. Using the decorated (old) function will result in a warning.

### Goal
Mark a function as deprecated within the library, ensuring that any subsequent calls to the decorated function emit a warning to the user.

### Parameters
- `version`: The version string indicating when the function was first marked as deprecated.
- `version_removed`: The version string indicating the future release when the function is slated for removal (e.g., `"0.9"`, as is the case for the deprecated `mir_eval.io.load_wav`).

### Input
The function to be decorated. The decorator itself requires `version` and `version_removed` to be passed strictly as keyword arguments due to the `*` in the signature.

### Output
Returns `unspecified` — A wrapped callable (decorator) that executes the original function but triggers a deprecation warning first.

### Valid Call Patterns
```python
# Note: This example is inferred from the signature (not verified).
import mir_eval.util

@mir_eval.util.deprecated(version="0.8", version_removed="0.9")
def load_wav(path):
    # Legacy function implementation slated for removal
    pass
```

### LLM Instruction Prompt
- When deprecating legacy functions (such as old I/O routines or functions in the deprecated `mir_eval.separation` module), use the `@deprecated` decorator. You MUST pass `version` and `version_removed` as keyword arguments because the signature enforces keyword-only arguments via `*`.

### Prompt Snippet
```text
`mir_eval.util.deprecated(*, version, version_removed)` is a decorator to mark functions as deprecated. Both arguments are required and must be passed as keywords. Calling the decorated function will emit a warning.
```

### Common Failure Modes
- **Positional Arguments:** Passing `version` and `version_removed` as positional arguments. Because the signature is `(*, version, version_removed)`, positional arguments will raise a `TypeError`.
- **Missing Arguments:** Failing to provide either `version` or `version_removed`, both of which are required keyword arguments.

### Fix Code Hint
```python
# BAD: Positional arguments will raise a TypeError
@mir_eval.util.deprecated("0.8", "0.9")
def old_func():
    pass

# GOOD: Keyword arguments are required by the signature
@mir_eval.util.deprecated(version="0.8", version_removed="0.9")
def old_func():
    pass
```