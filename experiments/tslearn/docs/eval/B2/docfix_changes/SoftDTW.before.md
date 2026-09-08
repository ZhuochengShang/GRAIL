## API Test: `SoftDTW`

### Signature
```python
class SoftDTW
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1068_

_Source doc:_ Soft Dynamic Time Warping

### Goal
Represents the Soft Dynamic Time Warping (Soft-DTW) metric class, used for computing differentiable alignments between time series.

### Parameters
_None._

### Input
No initialization parameters are documented in the authoritative API facts. If used as a PyTorch `autograd.Function` or similar backend helper, inputs to its methods (if any) are unknown.

### Output
Returns `unspecified` — an instance of the `SoftDTW` class.

### Valid Call Patterns
```python
from tslearn.metrics import SoftDTW

# Inferred from signature (no verified examples available)
def test_soft_dtw_instantiation():
    soft_dtw_instance = SoftDTW()
    assert isinstance(soft_dtw_instance, SoftDTW)
    print(f"Successfully instantiated: {type(soft_dtw_instance).__name__}")

test_soft_dtw_instantiation()
```

### LLM Instruction Prompt
- Do not invent initialization parameters for the `SoftDTW` class; the API facts list an empty parameter signature (`params: []`).
- Do not confuse the `SoftDTW` class with the `soft_dtw` function (which computes the metric and accepts arguments like `gamma` and `compute_with_backend`).
- Import `SoftDTW` explicitly from `tslearn.metrics`.

### Prompt Snippet
```text
When referencing the Soft-DTW class directly, use `SoftDTW()` without arguments as no parameters are documented. For computing the metric, prefer the `soft_dtw` function instead.
```

### Common Failure Modes
- **Inventing parameters:** Passing arguments (like `gamma` or `dataset`) to the `SoftDTW` class constructor will likely cause a `TypeError` since no parameters are defined in the signature.
- **Confusing class and function:** Attempting to use `SoftDTW` as a drop-in replacement for the `soft_dtw` function to compute distances directly on 3D `(n_ts, max_sz, d)` arrays.

### Fix Code Hint
```python
from tslearn.metrics import SoftDTW

# Instantiate the class exactly as defined by the signature (no arguments)
soft_dtw_metric = SoftDTW()
```