## API Test: `early_predict_proba`

### Signature
```python
def early_predict_proba(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:600_

_Source doc:_ Provides probability estimates as well as estimated delays before prediction timestamps for a dataset of incomplete time series. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- X : array-like of shape (n_series, t, n_features) A dataset of incomplete time series observed up to time t Returns ------- array-like, shape (n_series, n_classes) Probabilities for each class in the model, where classes are ordered as they are in ``self.classes_``. array-like of shape (n_series,) Estimated delays before prediction timestamps.

### Goal
Computes class probability estimates and estimated delays before prediction timestamps for a dataset of incomplete time series using a fitted early classification estimator.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: An array-like dataset of incomplete time series observed up to time `t`, with shape `(n_series, t, n_features)`.

### Input
`X` must be a 3D array formatted via `tslearn.utils.to_time_series_dataset` representing incomplete time series (where the time dimension `t` is typically smaller than the full series length seen during training). The estimator (`self`) must be fitted first. If `t` is smaller than the estimator's configured `min_t`, the method will return `NaN` values.

### Output
Returns `unspecified` — A tuple of two array-likes: `(probabilities, delays)`. `probabilities` has shape `(n_series, n_classes)` containing the class probabilities ordered by `self.classes_`. `delays` has shape `(n_series,)` containing the estimated delays before prediction timestamps.

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
import numpy as np

# 1. Prepare full-length training data
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1]
])
y = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1, metric="euclidean"),
    min_t=2,
    lamb=1000.0,
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(dataset, y)

# 3. Predict probabilities on incomplete time series (e.g., first 3 timestamps)
incomplete_X = dataset[:, :3]
probas, delays = model.early_predict_proba(incomplete_X)

# 4. Verify outputs
assert probas.shape == (4, 2), "Expected probabilities shape (n_series, n_classes)"
assert delays.shape == (4,), "Expected delays shape (n_series,)"
print(f"Probabilities:\n{probas}\nDelays:\n{delays}")
```

### LLM Instruction Prompt
- When calling `early_predict_proba`, ensure the input `X` is strictly a 3D array `(n_series, t, n_features)` representing incomplete time series.
- Always unpack the return value into two variables (e.g., `probas, delays = model.early_predict_proba(X)`), as it returns both the probability estimates and the estimated delays.
- Ensure the time dimension `t` of the input `X` is at least the `min_t` parameter of the fitted model; otherwise, the returned arrays will contain `NaN` values.

### Prompt Snippet
```text
Use the fitted `NonMyopicEarlyClassifier` to predict probabilities and delays for the incomplete time series `X_incomplete`. Unpack the results into `probas` and `delays`.
```

### Common Failure Modes
- **Not unpacking the return value:** Assigning the result to a single variable and attempting to use it as a probability matrix, which fails because the method returns a tuple `(probabilities, delays)`.
- **Passing 2D arrays:** Providing a 2D array `(n_series, t)` instead of the required 3D array `(n_series, t, n_features)`, leading to shape mismatch errors.
- **Calling before `fit`:** Attempting to call `early_predict_proba` on an unfitted estimator, raising a `NotFittedError`.
- **Providing too few timestamps:** Passing an `X` where the time dimension `t` is less than the model's `min_t`, resulting in arrays filled with `np.nan` instead of valid probabilities and delays.

### Fix Code Hint
```python
# FIX: Ensure X is 3D and unpack the tuple return value
X_incomplete_3d = to_time_series_dataset(X_incomplete)
probas, delays = model.early_predict_proba(X_incomplete_3d)

# Check for NaNs if the series is too short
if np.isnan(probas).any():
    print("Warning: Input time series length is shorter than the model's min_t.")
```