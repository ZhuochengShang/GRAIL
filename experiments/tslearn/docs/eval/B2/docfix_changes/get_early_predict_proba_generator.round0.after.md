## API Test: `get_early_predict_proba_generator`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def get_early_predict_proba_generator(self, n_ts=1)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:677_

### Goal
Creates a generator that accepts streaming time-series data points and yields current class probability estimates along with the estimated delay before an optimal prediction can be made. 

**Note:** Do not use large or arbitrary datasets (like a global harness dataset) to test `NonMyopicEarlyClassifier`, as it trains a classifier per time step and may drop classes if samples are insufficient, causing shape mismatches. Fitting on long time series is also extremely slow.

### Parameters
- `self`: A fitted early classification model instance (e.g., `NonMyopicEarlyClassifier`).
- `n_ts`, default `1`: `int`. The number of time series that will be predicted simultaneously by the generator.

### Input
The method itself takes an integer `n_ts`. The returned generator's `.send()` method requires an array-like input of shape `(n_ts, n_timestamps, n_features)` representing freshly acquired data. For step-by-step feeding, `n_timestamps` should be `1`. The model must be fitted before calling this method. Always use a small, deterministic dummy dataset with a known number of classes to fit the model before testing the generator.

### Output
Returns `generator` — A Python generator object. When fed data via `.send(x)`, it yields a tuple `(probabilities, delays)` where `probabilities` is an array of shape `(n_ts, n_classes)` (where `n_classes` is the number of classes successfully fitted by the model) and `delays` is an array of shape `(n_ts,)` representing the estimated number of time steps to wait before making a prediction.

### Valid Call Patterns
```python
import numpy as np
from tslearn.early_classification import NonMyopicEarlyClassifier

# Always use a small, deterministic dummy dataset to avoid dropped classes and slow fitting
dataset = np.array([
    [[1], [2], [3], [4], [5], [6]],
    [[1], [2], [3], [4], [5], [6]],
    [[1], [2], [3], [4], [5], [6]],
    [[1], [2], [3], [3], [2], [1]],
    [[1], [2], [3], [3], [2], [1]],
    [[1], [2], [3], [3], [2], [1]],
    [[3], [2], [1], [1], [2], [3]],
    [[3], [2], [1], [1], [2], [3]]
])
y = np.array([0, 0, 0, 1, 1, 1, 0, 0])

model = NonMyopicEarlyClassifier(
    n_clusters=3, 
    lamb=1000.0, 
    cost_time_parameter=0.1, 
    random_state=0
)
model.fit(dataset, y)

gen = model.get_early_predict_proba_generator(n_ts=1)
incoming_timestamps = np.array([1, 2, 3]).reshape(3, 1, 1, 1)

for x in incoming_timestamps:
    probas, delays = gen.send(x)
    assert probas.shape == (1, 2)
    assert delays.shape == (1,)
```

### LLM Instruction Prompt
- Use `get_early_predict_proba_generator` on a fitted early classifier to stream incoming time-series data.
- Fit the model on a small, deterministic dummy dataset to prevent dropped classes and extremely slow execution times.
- Do not pass the time-series data to the method itself; pass the number of time series (`n_ts`).
- Feed new data to the returned generator using its `.send(x)` method.
- Ensure the data `x` sent to the generator is strictly formatted as a 3D array `(n_ts, n_timestamps, n_features)`.

### Prompt Snippet
```text
To stream data for early classification, fit the model on a small deterministic dataset, then call `gen = model.get_early_predict_proba_generator(n_ts=1)`. Iteratively feed new time steps using `probas, delays = gen.send(x)`, ensuring `x` is a 3D array of shape `(n_ts, n_timestamps, n_features)`. The `probas` shape will be `(n_ts, n_classes)`.
```

### Common Failure Modes
- Asserting that the probability array shape matches the number of classes in a large/arbitrary global dataset. `NonMyopicEarlyClassifier` trains a classifier per time step and may drop classes if samples are insufficient, resulting in a shape mismatch (e.g., `AssertionError: Expected probas shape (1, 4), got (1, 3)`).
- Fitting the model on long time series (e.g., 275 time steps), which is extremely slow and error-prone.
- Sending data to the generator with a different `n_ts` than what it was initialized with.
- Sending 1D or 2D arrays to the generator instead of the required 3D array `(n_ts, n_timestamps, n_features)`.
- Calling the method on an unfitted early classification model.

### Fix Code Hint
```python
# WRONG: Fitting on a large arbitrary dataset and asserting hardcoded global class counts
model.fit(large_global_dataset, global_y) # Slow, drops classes
gen = model.get_early_predict_proba_generator(n_ts=1)
probas, delays = gen.send(new_data)
assert probas.shape == (1, len(np.unique(global_y))) # Fails if classes were dropped

# CORRECT: Fit on a small, deterministic dummy dataset with a known number of classes
dataset = np.array([[[1], [2]], [[1], [2]], [[3], [4]], [[3], [4]]])
y = np.array([0, 0, 1, 1])
model.fit(dataset, y)
gen = model.get_early_predict_proba_generator(n_ts=1)
probas, delays = gen.send(np.array([1]).reshape(1, 1, 1))
assert probas.shape == (1, 2) # Matches successfully fitted classes
```