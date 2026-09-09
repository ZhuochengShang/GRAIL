## API Test: `SquaredEuclidean`

### Signature
```python
class SquaredEuclidean
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1176_

_Source doc:_ Squared Euclidean distance.

### Goal
Instantiate a metric object representing the squared Euclidean distance, typically used as a base point-wise metric for time-series alignment algorithms.

### Parameters
_None._

### Input
No arguments are required for instantiation.

### Output
Returns `unspecified` — an instance of the `SquaredEuclidean` class representing the distance metric.

### Valid Call Patterns
```python
# Inferred from signature (not verified by test suite or README examples)
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# Instantiate the metric object
metric = SquaredEuclidean()
```

### LLM Instruction Prompt
- Instantiate `SquaredEuclidean` without any arguments.
- Do not pass time-series arrays directly to the class constructor; it is a metric object factory, not a direct distance function.

### Prompt Snippet
```text
from tslearn.metrics.softdtw_variants import SquaredEuclidean
sq_euclidean_metric = SquaredEuclidean()
```

### Common Failure Modes
- **Passing arrays to the constructor:** Attempting to compute the distance by passing time-series arrays directly to `SquaredEuclidean(ts1, ts2)` will fail because the constructor takes no parameters.

### Fix Code Hint
```python
# WRONG: Passing arrays directly to the constructor
# dist = SquaredEuclidean(ts1, ts2)

# RIGHT: Instantiate the metric object without arguments
metric = SquaredEuclidean()
```