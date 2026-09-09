## API Test: `TsLearnTags`

### Signature
```python
class TsLearnTags(Tags)
```
_Source: tslearn/tslearn/bases/bases.py:29_

### Goal
Defines scikit-learn compatible estimator tags specific to `tslearn` models, indicating their capabilities (such as accepting 3D variable-length time-series data).

### Parameters
_None._

### Input
No input parameters are required to instantiate this class. It is typically used internally or by custom estimators to declare compatibility with `tslearn`'s strict `(n_ts, max_sz, d)` 3D array format and variable-length time-series handling.

### Output
Returns an instance of `TsLearnTags` (inheriting from `Tags`) representing the estimator's tag configuration. The exact internal tag dictionary structure is not specified in the provided facts.

### Valid Call Patterns
```python
# Inferred from the signature (no verified examples in the provided context)
from tslearn.bases.bases import TsLearnTags

# Instantiate the tags object
tags = TsLearnTags()

# Assert falsifiable property
assert isinstance(tags, TsLearnTags), "Failed to instantiate TsLearnTags"
print("TsLearnTags instantiated successfully.")
```

### LLM Instruction Prompt
- When creating custom `tslearn` estimators or inspecting `tslearn` base classes, use `TsLearnTags()` to generate or represent the appropriate scikit-learn compatible tags. Do not pass any arguments to the constructor.

### Prompt Snippet
```text
`TsLearnTags` is a base class/utility in `tslearn.bases.bases` used to define scikit-learn compatible estimator tags for time-series models. It takes no arguments upon instantiation: `tags = TsLearnTags()`.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Because `TsLearnTags` takes no parameters, providing arguments (e.g., trying to pass a dictionary of tags directly into the constructor) will raise a `TypeError`.

### Fix Code Hint
```python
# BAD: Attempting to pass arguments to the constructor
# tags = TsLearnTags({"allow_nan": True})

# GOOD: Instantiate without arguments
tags = TsLearnTags()
```