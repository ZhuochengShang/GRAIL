## API Test: `check_keras_backend`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def check_keras_backend()
```

### Goal
INTERNAL/FRAMEWORK utility to configure the environment before importing Keras. It mutates `os.environ["KERAS_BACKEND"]` to the first available supported backend (`torch`, `tensorflow`, or `jax`). Note: This is an internal initialization helper and should be excluded from the main user-facing benchmark denominator.

### Parameters
_None._

### Input
No parameters. Operates on the global environment state (`os.environ`). As an INTERNAL/FRAMEWORK helper, it is not intended for direct end-user data pipelines.

### Output
Returns `None`. Operates entirely via side effects (mutating `os.environ["KERAS_BACKEND"]`) or raises an `ImportError` if no supported backend is installed.

### Valid Call Patterns
```python
import os
from tslearn.backend import check_keras_backend

original_backend = os.environ.get("KERAS_BACKEND")
if "KERAS_BACKEND" in os.environ:
    del os.environ["KERAS_BACKEND"]

try:
    check_keras_backend()
    selected = os.environ.get("KERAS_BACKEND")
    assert selected in ["torch", "tensorflow", "jax"], f"Unexpected backend: {selected}"
    print(f"__CHECK__ check_keras_backend set KERAS_BACKEND to {selected}")
except ImportError as e:
    assert str(e) == "No Keras backend installed"
    print("__CHECK__ check_keras_backend raised ImportError (no backends installed)")
finally:
    if original_backend is not None:
        os.environ["KERAS_BACKEND"] = original_backend
    elif "KERAS_BACKEND" in os.environ:
        del os.environ["KERAS_BACKEND"]
```

### LLM Instruction Prompt
Call `check_keras_backend()` without arguments. You MUST verify its side effect by checking `os.environ["KERAS_BACKEND"]` or catching `ImportError("No Keras backend installed")`. Do not just assert the return value is `None`. Ensure you restore the original environment state after the test.

### Prompt Snippet
```text
Use `tslearn.backend.check_keras_backend()` to initialize the Keras backend environment variable. Verify the side effect on `os.environ["KERAS_BACKEND"]` or catch `ImportError`.
```

### Common Failure Modes
- **Asserting `None` instead of verifying side effects:** The previous test failed because it only asserted `result is None`. The test harness rejects tests for side-effect-only functions that do not falsifiably verify the state change (mutating `os.environ`).
- **Failing to catch `ImportError`:** If no backends are installed in the test environment, the function raises `ImportError("No Keras backend installed")`. Tests must catch and validate this.
- **Polluting the environment:** Failing to save and restore the original `os.environ.get("KERAS_BACKEND")` state, which can break subsequent tests.
- **Misunderstanding audience:** Using this INTERNAL/FRAMEWORK API as if it were a standard user-facing model component.

### Fix Code Hint
```python
# WRONG: Asserts return value but ignores the actual work performed
result = check_keras_backend()
assert result is None

# RIGHT: Verifies the side effect on the environment
check_keras_backend()
assert os.environ["KERAS_BACKEND"] in ["torch", "tensorflow", "jax"]
```