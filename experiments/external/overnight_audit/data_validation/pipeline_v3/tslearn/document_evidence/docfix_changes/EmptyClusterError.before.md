## API Test: `EmptyClusterError`

### Signature
```python
class EmptyClusterError(Exception)
```
_Source: tslearn/tslearn/clustering/utils.py:17_

### Goal
An exception class raised when a cluster loses all its assigned time-series samples during the execution of a clustering algorithm.

### Parameters
_None._

### Input
As a standard Python exception subclass, it accepts standard `Exception` arguments (such as a string error message) when instantiated, though no custom parameters are defined by the API.

### Output
Returns `unspecified` — An exception object that inherits from Python's built-in `Exception`, which can be raised or caught during time-series clustering workflows.

### Valid Call Patterns
```python
from tslearn.clustering.utils import EmptyClusterError

# Example inferred from the signature (not verified by existing tests)
try:
    # Simulate the exception being raised internally by a tslearn clustering estimator
    raise EmptyClusterError("A cluster became empty during iteration.")
except EmptyClusterError as e:
    assert isinstance(e, Exception)
    print(f"Successfully caught: {type(e).__name__}")
```

### LLM Instruction Prompt
- When writing robust time-series clustering pipelines or custom `tslearn`-compatible clustering estimators, catch `EmptyClusterError` to gracefully handle edge cases where a cluster centroid loses all its assigned time series. If implementing a custom clusterer, raise this exception when an empty cluster is detected.

### Prompt Snippet
```text
Catch `tslearn.clustering.utils.EmptyClusterError` to handle unstable clustering iterations where a cluster becomes empty, often due to `n_clusters` being too high.
```

### Common Failure Modes
- **Unhandled Exception on Fit:** An unhandled `EmptyClusterError` crashing a training pipeline. This typically occurs when `n_clusters` is set too high relative to the dataset size, or when using a poor centroid initialization strategy that leaves some centroids stranded far from the data.

### Fix Code Hint
```python
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering.utils import EmptyClusterError

try:
    # Attempt to fit the model
    model = TimeSeriesKMeans(n_clusters=10, metric="dtw")
    model.fit(X_scaled)
except EmptyClusterError:
    # Fallback strategy: reduce the number of clusters or change initialization
    print("Empty cluster encountered. Falling back to fewer clusters.")
    model = TimeSeriesKMeans(n_clusters=3, metric="dtw")
    model.fit(X_scaled)
```