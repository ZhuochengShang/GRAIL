## API Test: `BaseModelPackage`

### Signature
```python
class BaseModelPackage(object)
```
_Source: tslearn/tslearn/bases/bases.py:78_

### Goal
Acts as a base class for model packaging and serialization within the `tslearn` library.

### Parameters
_None._

### Input
No inputs or preconditions are required to instantiate this base class.

### Output
Returns `unspecified` — an initialized instance of the `BaseModelPackage` object.

### Valid Call Patterns
```python
from tslearn.bases import BaseModelPackage

# Inferred from signature: instantiate the base class without arguments
model_package = BaseModelPackage()

# Verify instantiation
assert isinstance(model_package, BaseModelPackage)
print(f"Successfully instantiated: {type(model_package).__name__}")
```

### LLM Instruction Prompt
- When interacting with `BaseModelPackage`, do not pass any arguments to its constructor. 
- Recognize it as a base class for model packaging; do not invent serialization methods (like `.save()` or `.load()`) on this base class unless explicitly provided by a derived estimator's API facts.

### Prompt Snippet
```text
`BaseModelPackage` is a base class in `tslearn.bases`. It takes no arguments in its constructor (`BaseModelPackage()`). Do not invent or call undocumented serialization methods on it directly.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Because it inherits directly from `object` and defines no parameters, passing hyperparameters or data during instantiation will raise a `TypeError`.
- **Calling invented methods:** Assuming the presence of standard serialization methods (e.g., `to_json()`, `save()`) that are not explicitly listed in the API facts.

### Fix Code Hint
```python
# WRONG: model_package = BaseModelPackage(model=my_model)
# RIGHT:
model_package = BaseModelPackage()
```