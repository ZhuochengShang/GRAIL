## API Test: `predict_class_and_earliness`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def predict_class_and_earliness(self, X)
```

### Goal
Predict the class labels and the exact timestamps at which the early classification decision was made for a given time-series dataset.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: The time-series dataset to be scored, formatted as a 3D array-like of shape `(n_series, n_timestamps, n_features)`.

### Input
- `X` must be a 3D array-like of shape `(n_series, n_timestamps, n_features)`.
- The estimator (`self`) must be fitted before calling this method.
- **Crucial:** The estimator's underlying `base_classifier` must natively accept 3D arrays. If you provided a custom `base_classifier` during the estimator's construction, it must be a `tslearn` time-series classifier (like `TimeSeriesSVC`). Standard scikit-learn classifiers will fail here.

### Output
A tuple containing two NumPy arrays:
1. `predicted_classes`: A 1D array of shape `(n_series,)` containing the predicted class labels.
2. `prediction_timestamps`: A 1D array of shape `(n_series,)` containing the integer timestamps (lengths of the truncated series) at which the predictions were made.

### Valid Call Patterns
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
# Omit base_classifier to use the default 3D-compatible classifier
early_clf = NonMyopicEarlyClassifier(
    n_clusters=2, 
    cost_time_parameter=1e-3, 
    random_state=42
)
early_clf.fit(X_train, y_train)

# 3. Predict class and earliness
predicted_classes, prediction_timestamps = early_clf.predict_class_and_earliness(X_train)

assert predicted_classes.shape == (4,)
assert prediction_timestamps.shape == (4,)
print(f"__CHECK__ predict_class_and_earliness {predicted_classes.shape}, {prediction_timestamps.shape}")
```

### LLM Instruction Prompt
- When calling `predict_class_and_earliness`, ensure the input `X` is strictly formatted as a 3D array `(n_series, n_timestamps, n_features)`.
- Do not pass standard scikit-learn classifiers (like `DecisionTreeClassifier`) as the `base_classifier` when constructing the early classifier. `tslearn` passes 3D arrays to the base classifier during prediction, which standard scikit-learn estimators reject. Omit the `base_classifier` argument to use the default 3D-compatible classifier.
- Expect a tuple of two arrays in return: `(predicted_classes, prediction_timestamps)`.

### Prompt Snippet
```text
Ensure `X` is a 3D array `(n_series, n_timestamps, n_features)`. The estimator must use a 3D-compatible `base_classifier` (omit the argument to use the default; do not use standard sklearn classifiers). `predict_class_and_earliness` returns a tuple `(predicted_classes, prediction_timestamps)`.
```

### Common Failure Modes
- **`ValueError: Found array with dim 3, while dim <= 2 is required...`**: This occurs during prediction if you explicitly passed a standard scikit-learn classifier (e.g., `DecisionTreeClassifier`) as the `base_classifier` to the early classifier. `tslearn` passes 3D arrays to the base classifier, which standard scikit-learn estimators strictly reject.
- Passing a 1D or 2D array for `X` instead of the required 3D array `(n_series, n_timestamps, n_features)`, causing shape mismatch errors.
- Calling the method on an unfitted estimator, resulting in a `NotFittedError`.

### Fix Code Hint
```python
# WRONG: Standard sklearn classifiers fail on 3D arrays during prediction
from sklearn.tree import DecisionTreeClassifier
early_clf = NonMyopicEarlyClassifier(base_classifier=DecisionTreeClassifier())
early_clf.fit(X, y)
preds, times = early_clf.predict_class_and_earliness(X) # Crashes here

# CORRECT: Omit base_classifier to use the default 3D-compatible tslearn classifier
early_clf = NonMyopicEarlyClassifier(n_clusters=2, cost_time_parameter=1e-3)
early_clf.fit(X, y)
preds, times = early_clf.predict_class_and_earliness(X) # Succeeds
```