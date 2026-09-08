## API Test: `predict_class_and_earliness`

### Signature
```python
def predict_class_and_earliness(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:399_

_Source doc:_ Provide predicted class as well as prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- X : array-like of shape (n_series, n_timestamps, n_features) Vector to be scored, where `n_series` is the number of time series, `n_timestamps` is the number of timestamps in the series and `n_features` is the number of features recorded at each timestamp. Returns ------- array, shape (n_series,) Predicted classes. array-like of shape (n_series, ) Prediction timestamps.

### Goal
Predict the class labels and the timestamps at which the early classification decision was made for a given time-series dataset.

### Parameters
- `self`: A fitted early classification estimator instance.
- `X`: The time-series dataset to be scored, formatted as a 3D array-like of shape `(n_series, n_timestamps, n_features)`.

### Input
- `X` must be a 3D array-like of shape `(n_series, n_timestamps, n_features)`. If your data is 1D or 2D, it must be reshaped or converted using `tslearn.utils.to_time_series_dataset` prior to calling this method.
- The estimator (`self`) must be fitted before calling this method.

### Output
Returns `unspecified` — A tuple containing two arrays:
1. `predicted_classes` (array of shape `(n_series,)`): The predicted class labels.
2. `prediction_timestamps` (array-like of shape `(n_series,)`): The timestamps at which the prediction was made.

### Valid Call Patterns
```python
# Example inferred from signature (exact estimator class not specified in context)
import numpy as np
from unittest.mock import Mock

# X must be a 3D array: (n_series, n_timestamps, n_features)
X_test = np.zeros((3, 10, 1))

# Mocking a fitted early classification estimator since the exact class is unknown
estimator = Mock()
estimator.predict_class_and_earliness.return_value = (
    np.array([0, 1, 0]), 
    np.array([2, 4, 3])
)

# Call the method
predicted_classes, prediction_timestamps = estimator.predict_class_and_earliness(X_test)

assert predicted_classes.shape == (3,)
assert prediction_timestamps.shape == (3,)
print(f"Predicted classes: {predicted_classes}")
print(f"Prediction timestamps: {prediction_timestamps}")
```

### LLM Instruction Prompt
- When calling `predict_class_and_earliness`, ensure the input `X` is strictly formatted as a 3D array `(n_series, n_timestamps, n_features)`.
- Expect a tuple of two arrays in return: the predicted classes and the timestamps of the early predictions.
- Call this method only on a fitted early classification estimator instance.

### Prompt Snippet
```text
Ensure `X` is a 3D array `(n_series, n_timestamps, n_features)`. `predict_class_and_earliness` returns a tuple `(predicted_classes, prediction_timestamps)`.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D array `(n_series, n_timestamps, n_features)`, which will cause shape mismatch errors.
- Calling the method on an unfitted estimator, resulting in a `NotFittedError`.
- Misinterpreting the return value as a single array rather than a tuple of two arrays, leading to unpacking errors.

### Fix Code Hint
```python
# Ensure X is 3D
if X.ndim == 2:
    X = X[:, :, np.newaxis]
elif X.ndim == 1:
    X = X[np.newaxis, :, np.newaxis]

# Unpack the tuple correctly
predicted_classes, prediction_timestamps = estimator.predict_class_and_earliness(X)
```