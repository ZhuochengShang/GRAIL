## API Test: `cdist_sax`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def cdist_sax(dataset1, breakpoints_avg, size_fitted, dataset2=None, n_jobs=None, verbose=0)
```

### Goal
Calculates a cross-similarity matrix of MINDIST distances between two datasets of already-discretized SAX-transformed time series (integer symbols).

### Parameters
- `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of SAX-transformed time series (represented as integer symbols).
- `breakpoints_avg`: 1D array-like. The breakpoints used to assign the SAX alphabet symbols.
- `size_fitted`: Integer. The original number of timesteps in the time series before they were discretized through SAX.
- `dataset2`, default `None`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`. The second dataset of SAX-transformed time series (integer symbols). If `None`, the self-similarity matrix of `dataset1` is returned.
- `n_jobs`, default `None`: Integer or `None`. The number of parallel jobs to run (`-1` uses all processors).
- `verbose`, default `0`: Integer. The verbosity level for progress messages.

### Input
Time-series datasets provided as array-like structures (lists or NumPy arrays) containing **integer SAX symbols**, NOT continuous floats.
**Crucial Precondition:** The original time series must have been normalized to zero mean and unit variance *before* being transformed into these SAX symbols. Do not pass continuous floats to this function, as they will be silently truncated to integers by the internal `dtype=int` cast.

### Output
A 2D NumPy array cross-similarity matrix of shape `(n_ts1, n_ts2)` containing the computed MINDIST distances.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# dataset1 must be already-discretized SAX symbols (integers)
dataset1 = np.array([[0, 0, 0], [3, 3, 3]])
breakpoints = np.array([-0.6745, 0.0, 0.6745])
size_fitted = 30

dists = tslearn.metrics.cdist_sax(
    dataset1=dataset1,
    breakpoints_avg=breakpoints,
    size_fitted=size_fitted
)

assert dists.shape == (2, 2)
print(f"Computed SAX MINDIST matrix:\n{dists}")
```

### LLM Instruction Prompt
- `dataset1` and `dataset2` MUST be the already-discretized SAX symbols (integers), NOT the normalized continuous time series.
- Do not pass continuous floats; they will be silently truncated to integers by `dtype=int`.
- The requirement for zero mean and unit variance applies to the original time series *before* they are transformed into SAX symbols, not to the inputs of this function.
- To test the function directly, bypass the SAX transformer and provide the integer symbols, breakpoints, and original size directly.

### Prompt Snippet
```text
Compute the SAX MINDIST distance matrix between `X_sax_symbols` and `Y_sax_symbols` (both containing integer symbols). Assume both datasets were derived from time series of original length 50 that were normalized to zero mean and unit variance before SAX transformation. Use the breakpoints array `sax_breakpoints`.
```

### Common Failure Modes
- **Transformer Kwarg Errors:** Attempting to dynamically generate SAX inputs using `tslearn.piecewise.SymbolicAggregateApproximation` but passing invalid keyword arguments (e.g., `TypeError: SymbolicAggregateApproximation.__init__() got an unexpected keyword argument 'alphabet_size'`). Bypass the transformer for direct testing.
- **Passing Continuous Floats:** Passing normalized continuous time series instead of integer SAX symbols. The function casts inputs via `dtype=int`, which silently truncates floats, leading to mathematically invalid distances without raising an error.
- **Missing Positional Arguments:** Failing to provide `breakpoints_avg` or `size_fitted`, which are required positional arguments.

### Fix Code Hint
```python
# WRONG: Passing continuous floats or dynamically generating with invalid kwargs
# dists = tslearn.metrics.cdist_sax(
#     X_normalized_floats,  # Silently truncated to int!
#     breakpoints_avg=my_breakpoints, 
#     size_fitted=50
# )

# CORRECT: Pass already-discretized SAX integer symbols directly
import numpy as np
import tslearn.metrics

X_sax_symbols = np.array([[0, 1, 2], [2, 1, 0]]) # Integers
my_breakpoints = np.array([-0.5, 0.0, 0.5])

dists = tslearn.metrics.cdist_sax(
    dataset1=X_sax_symbols, 
    breakpoints_avg=my_breakpoints, 
    size_fitted=50
)
```