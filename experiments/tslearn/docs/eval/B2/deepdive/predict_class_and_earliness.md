# Deep-dive: `predict_class_and_earliness`

model: google:gemini-3.1-pro-preview · tokens in=5,199 out=4,408 · wall 32s · 2026-09-08 15:50

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
USER-FACING. TESTABLE FROM PUBLIC INPUTS.

**L1 PURPOSE**
The `predict_class_and_earliness` method is a core inference API in `tslearn`'s early classification module. It evaluates a set of time series and returns both the predicted class labels and the exact timestamps at which the model gathered enough information to make those decisions, allowing users to analyze the trade-off between classification accuracy and how early the prediction is made.

**L2 CONTRACT**
- **Receiver**: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- **Parameters**:
  - `X`: Array-like of shape `(n_series, n_timestamps, n_features)`. The time-series dataset to be scored.
- **Returns**: A tuple of two NumPy arrays:
  - `predicted_classes`: A 1D array of shape `(n_series,)` containing the predicted class labels.
  - `prediction_timestamps`: A 1D array of shape `(n_series,)` containing the integer timestamps (lengths of the truncated series) at which the predictions were made.
- **Visibility**: Public.
- **State/Side Effects**: Read-only; does not mutate the estimator.

**L3 MECHANICS**
- The method first validates the input `X` using `check_array(allow_nd=True)`.
- It verifies that the estimator has been fitted by checking for the `_X_fit_dims` attribute via `check_is_fitted`.
- It ensures the feature dimensionality of `X` matches the training data using `check_dims(check_n_features_only=True)`.
- It initializes two empty lists: `y_pred` and `time_prediction`.
- It iterates over each time series `X[i]` in the dataset.
- For each series, it delegates to the internal method `_predict_single_series(X[i])`.
  - Inside `_predict_single_series` (lines 375-377), it determines the optimal stopping time `t` by calling `self._get_prediction_time(Xi)`.
  - It then slices the series up to time `t` (`Xi[:t]`), wraps it in a list to maintain the 3D shape `(1, t, n_features)`, and passes it to the specific base classifier trained for length `t`: `self.classifiers_[t].predict([Xi[:t]])[0]`.
- The resulting class and timestamp are appended to the lists, which are finally converted to NumPy arrays and returned.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.utils import to_time_series_dataset

# 1. Create a minimal 3D time-series dataset (n_series, n_timestamps, n_features)
X_train = to_time_series_dataset([
    [1.0, 2.0, 3.0, 4.0],
    [1.0, 2.0, 3.0, 4.0],
    [4.0, 3.0, 2.0, 1.0],
    [4.0, 3.0, 2.0, 1.0]
])
y_train = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
# Using parameters inferred from the provided docstring examples
model = NonMyopicEarlyClassifier(n_clusters=2, cost_time_parameter=0.1)
model.fit(X_train, y_train)

# 3. Predict class and earliness
preds, pred_times = model.predict_class_and_earliness(X_train)

assert preds.shape == (4,)
assert pred_times.shape == (4,)
print(f"Predicted classes: {preds}")
print(f"Prediction timestamps: {pred_times}")
```

**L5 FAILURE FORENSICS**
- **`ValueError: Found array with dim 3, while dim <= 2 is required by DecisionTreeClassifier.`**
  This failure occurred because the user explicitly passed a standard scikit-learn `DecisionTreeClassifier` as the `base_classifier` to the early classifier. As seen on line 376 (`self.classifiers_[t].predict([Xi[:t]])[0]`), `tslearn` passes a 3D array `(1, t, n_features)` to the base classifier's `predict` method. Standard scikit-learn classifiers strictly expect 2D arrays `(n_samples, n_features)`. To fix this, the base classifier must be a time-series-compatible estimator from `tslearn` (which natively handles 3D arrays), or the user should rely on the default base classifier provided by the early classification model.

**L6 SELF-ASSESSMENT**
- **INFERENCE**: I inferred that `predict_class_and_earliness` is a method of a base class or directly on `NonMyopicEarlyClassifier`, based on the `early_classification_cost` docstring example and the failure history.
- **INFERENCE**: I inferred that `NonMyopicEarlyClassifier` can be instantiated without explicitly providing a `base_classifier` and will default to a 3D-compatible time-series classifier, avoiding the dimensionality error seen in the failure logs.
- **Confidence in L2 (Contract)**: 10/10. The signature, parameters, and return types are explicitly documented in the provided source.
- **Confidence in L3 (Mechanics)**: 10/10. The source code for the method and its immediate delegates (`_predict_single_series`) is fully visible and straightforward.
- **Confidence in L4 (Usage)**: 9/10. The usage pattern is standard for scikit-learn/tslearn estimators, though the exact default behavior of `NonMyopicEarlyClassifier`'s constructor relies slightly on standard library conventions.