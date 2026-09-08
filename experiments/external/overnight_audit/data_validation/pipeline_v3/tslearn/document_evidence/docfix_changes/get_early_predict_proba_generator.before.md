## API Test: `get_early_predict_proba_generator`

### Signature
```python
def get_early_predict_proba_generator(self, n_ts=1)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:677_

_Source doc:_ Allows streaming incoming timestamps of a time series and retrieving current probability estimates as well as estimated delay before prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- n_ts: int (default 1) The number of time series that will be predicted by the generator Returns ------- generator Use the `send` method of the generator to stream timestamps as they become available and retrieve associated prediction probalities and delays. This method takes an array-like, shape (n_ts, n_timestamps, n_features), representing freshly aquired data for all timeseries as input. This new data is concatenated with previously sent data, if any, to output the predicted probability estimates and estimated delays before optimal prediction timestamps for all timeseries based all on available data (same output as :func:`~early_predict_proba`). Use n_timestamps = 1 for step by step feeding. Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=1000., ...                                  cost_time_parameter=.1, ...                                  random_state=0).fit(dataset, y) >>> incoming_timestamps = np.array([1, 2, 3, 3, 1, 2]).reshape(6, 1, 1, 1) >>> gen = model.get_early_predict_proba_generator() >>> for x in incoming_timestamps: ...     print(gen.send(x)) (array([[1., 0.]]), array([3])) (array([[1., 0.]]), array([2])) (array([[1., 0.]]), array([1])) (array([[0., 1.]]), array([0])) (array([[0., 1.]]), array([0])) (array([[0., 1.]]), array([0]))

### Goal
Creates a generator that accepts streaming time-series data points and yields current class probability estimates along with the estimated delay before an optimal prediction can be made.

### Parameters
- `self`: A fitted early classification model instance (e.g., `NonMyopicEarlyClassifier`).
- `n_ts`, default `1`: `int`. The number of time series that will be predicted simultaneously by the generator.

### Input
The method itself takes an integer `n_ts`. The returned generator's `.send()` method requires an array-like input of shape `(n_ts, n_timestamps, n_features)` representing freshly acquired data. For step-by-step feeding, `n_timestamps` should be `1`. The model must be fitted before calling this method.

### Output
Returns `generator` — A Python generator object. When fed data via `.send(x)`, it yields a tuple `(probabilities, delays)` where `probabilities` is an array of shape `(n_ts, n_classes)` and `delays` is an array of shape `(n_ts,)` representing the estimated number of time steps to wait before making a prediction.

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
import numpy as np

# 1. Prepare training data and fit the early classifier
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1]
])
y = [0, 0, 1, 1]

model = NonMyopicEarlyClassifier(
    n_clusters=2, 
    lamb=1000.0, 
    cost_time_parameter=0.1, 
    random_state=0
)
model.fit(dataset, y)

# 2. Create the generator for 1 time series
gen = model.get_early_predict_proba_generator(n_ts=1)

# 3. Stream 3 timestamps one by one for a single time series
incoming_timestamps = np.array([1, 2, 3]).reshape(3, 1, 1, 1)
for x in incoming_timestamps:
    probas, delays = gen.send(x)
    
    # Assert the output shapes match the expected (n_ts, n_classes) and (n_ts,)
    assert probas.shape == (1, 2)
    assert delays.shape == (1,)

print(f"Final step probabilities: {probas}, delay: {delays}")
```

### LLM Instruction Prompt
- Use `get_early_predict_proba_generator` on a fitted early classifier to stream incoming time-series data.
- Do not pass the time-series data to the method itself; pass the number of time series (`n_ts`).
- Feed new data to the returned generator using its `.send(x)` method.
- Ensure the data `x` sent to the generator is strictly formatted as a 3D array `(n_ts, n_timestamps, n_features)`.

### Prompt Snippet
```text
To stream data for early classification, call `gen = model.get_early_predict_proba_generator(n_ts=1)` on a fitted model. Then, iteratively feed new time steps using `probas, delays = gen.send(x)`, ensuring `x` is a 3D array of shape `(n_ts, n_timestamps, n_features)`.
```

### Common Failure Modes
- Sending data to the generator with a different `n_ts` than what it was initialized with.
- Sending 1D or 2D arrays to the generator instead of the required 3D array `(n_ts, n_timestamps, n_features)`.
- Calling the method on an unfitted early classification model.

### Fix Code Hint
```python
# Ensure the input to .send() is a 3D array matching the initialized n_ts
gen = model.get_early_predict_proba_generator(n_ts=1)

# Reshape a single new measurement to (n_ts=1, n_timestamps=1, n_features=1)
new_data_point = np.array([value]).reshape(1, 1, 1)
probas, delays = gen.send(new_data_point)
```