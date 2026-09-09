## API Test: `EmptyClusterError`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class EmptyClusterError(Exception):
    def __init__(self, message="")
```

### Goal
An exception class raised when a cluster loses all its assigned time-series samples during the execution of a clustering algorithm.

### Parameters
- `message` (str, optional): A custom string providing additional context about the error. Defaults to `""`.

### Input
A string message providing context for the empty cluster failure.

### Output
An instance of `EmptyClusterError` inheriting from Python's built-in `Exception`.

### Valid Call Patterns
```python
from tslearn.clustering.utils import EmptyClusterError

try:
    raise EmptyClusterError("Test empty cluster")
except EmptyClusterError as e:
    assert isinstance(e, Exception), "EmptyClusterError should inherit from Exception"
    assert str(e) == "Cluster assignments lead to at least one empty cluster (Test empty cluster)"
    print(f"__CHECK__ EmptyClusterError {type(e).__name__}")
```

### LLM Instruction Prompt
Catch `tslearn.clustering.utils.EmptyClusterError` to handle unstable clustering iterations where a cluster becomes empty. Note that `EmptyClusterError` overrides `__str__` to prepend the hardcoded string `"Cluster assignments lead to at least one empty cluster"`. If a custom message is provided during instantiation, it is appended to the string representation in parentheses as a suffix (e.g., `"Cluster assignments lead to at least one empty cluster (my message)"`).

### Prompt Snippet
```text
`EmptyClusterError` overrides `__str__` to prepend `"Cluster assignments lead to at least one empty cluster"`. Custom messages are appended in parentheses.
```

### Common Failure Modes
- **String Representation Mismatch:** Asserting that `str(e)` exactly matches the passed message. The class overrides `__str__` to prepend `"Cluster assignments lead to at least one empty cluster"` and formats the custom message as a suffix in parentheses.
- **Unhandled Exception on Fit:** An unhandled `EmptyClusterError` crashing a training pipeline. This typically occurs when `n_clusters` is set too high relative to the dataset size.

### Fix Code Hint
```python
# WRONG: Assuming str(e) exactly matches the passed message
try:
    raise EmptyClusterError("Test empty cluster")
except EmptyClusterError as e:
    assert str(e) == "Test empty cluster"

# CORRECT: Accounting for the overridden __str__ formatting
try:
    raise EmptyClusterError("Test empty cluster")
except EmptyClusterError as e:
    assert str(e) == "Cluster assignments lead to at least one empty cluster (Test empty cluster)"
```