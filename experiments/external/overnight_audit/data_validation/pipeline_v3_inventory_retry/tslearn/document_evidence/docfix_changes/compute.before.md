## API Test: `compute`

### Signature
```python
def compute(self)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1111  (+1 more definition site/overload)_

_Source doc:_ Compute soft-DTW by dynamic programming. Returns ------- sdtw: float soft-DTW discrepancy.

### Goal
Compute the soft-DTW (Dynamic Time Warping) discrepancy between time series using dynamic programming.

### Parameters
- `self`: The instantiated Soft-DTW calculator object containing the initialized time-series data and metric hyperparameters (such as `gamma`).

### Input
This method takes no arguments other than `self`. The caller must have already instantiated the parent object with the necessary time-series data. As per `tslearn` conventions, the underlying time-series data provided to the object's constructor must be properly formatted (typically as 3D `numpy` arrays or PyTorch tensors of shape `(n_ts, max_sz, d)`).

### Output
Returns `unspecified` — A `float` representing the computed soft-DTW discrepancy score.

### Valid Call Patterns
```python
# Inferred from signature (not verified in provided examples)
# Assuming `soft_dtw_obj` is an already-instantiated Soft-DTW calculator object

sdtw_discrepancy = soft_dtw_obj.compute()
```

### LLM Instruction Prompt
- When calling `compute`, invoke it without any arguments on an already-initialized Soft-DTW object. Do not pass the time-series arrays or hyperparameters (like `gamma`) to `compute()`; these must be provided during the object's instantiation.

### Prompt Snippet
```text
# Compute the soft-DTW discrepancy using the pre-configured object
sdtw_score = soft_dtw_obj.compute()
```

### Common Failure Modes
- **Passing arguments to `compute`:** Providing time-series arrays directly to `compute(ts1, ts2)` will raise a `TypeError`, as the method only accepts `self`.
- **Unformatted underlying data:** If the parent object was initialized with raw lists instead of the strict `(n_ts, max_sz, d)` 3D array format required by `tslearn`, the computation will fail internally.

### Fix Code Hint
```python
# WRONG: Passing data directly to the compute method
# score = soft_dtw_obj.compute(ts1, ts2)

# RIGHT: Call compute without arguments (data is handled by the object's constructor)
score = soft_dtw_obj.compute()
```