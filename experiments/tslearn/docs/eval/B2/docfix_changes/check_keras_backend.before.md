## API Test: `check_keras_backend`

### Signature
```python
def check_keras_backend()
```
_Source: tslearn/tslearn/backend/__init__.py:12_

_Source doc:_ Select a backend based on installed packages when none is explicitly selected.

### Goal
Select a backend based on installed packages when none is explicitly selected, typically checking the environment for Keras availability.

### Parameters
_None._

### Input
No input parameters are required. The function relies on the current Python environment and installed packages.

### Output
Returns `None` — the function performs an environment check and backend selection as a side effect rather than returning a backend instance.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
from tslearn.backend import check_keras_backend

def test_check_keras_backend():
    # Execute the backend check (takes no arguments)
    result = check_keras_backend()
    
    # Assert the function returns None as it operates via side effects
    assert result is None, f"Expected check_keras_backend to return None, got {type(result)}"
    print("check_keras_backend() executed successfully and returned None.")

test_check_keras_backend()
```

### LLM Instruction Prompt
- Call `check_keras_backend()` without any arguments to trigger backend selection based on installed packages.
- Do not expect a backend object to be returned; the function returns `None` and configures the environment internally.

### Prompt Snippet
```text
Use `tslearn.backend.check_keras_backend()` to check for installed packages and select a backend when none is explicitly selected. It takes no arguments and returns None.
```

### Common Failure Modes
- Passing arguments (like a backend string or tensor) to `check_keras_backend`, which takes no parameters.
- Attempting to assign the return value to a variable and use it as a backend instance (it returns `None`).

### Fix Code Hint
```python
# WRONG: backend = check_keras_backend("tensorflow")
# RIGHT: check_keras_backend()  # Returns None; configures backend via side effects
```