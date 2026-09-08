# Deep-dive: `early_predict_proba`

model: google:gemini-3.1-pro-preview · tokens in=5,925 out=2,933 · wall 24s · 2026-09-08 15:11

---

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience:** USER-FACING
- **Testability:** TESTABLE FROM PUBLIC INPUTS
- **Explanation:** The API is a public method (`early_predict_proba`) on early classification estimators (like `NonMyopicEarlyClassifier`). It is intended for end-users to obtain probability estimates and prediction delays on incomplete time series. It can be tested directly by instantiating a public estimator, fitting it on a small dataset, and passing a truncated dataset to the method.

### L1 PURPOSE
The `early_predict_proba` method computes class probability estimates and the estimated delay before an optimal prediction can be made for a dataset of incomplete time series. In the context of early classification, it allows a user to feed partial time series (observed up to time $t$) into a fitted model to see both the current confidence distribution across classes and how many more time steps the model estimates it needs to make a definitive prediction.

### L2 CONTRACT
- **Receiver:** A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`). It must be fitted so that attributes like `_X_fit_dims` and `__n_classes_` are populated.
- **Parameters:**
  - `X`: Array-like of shape `(n_series, t, n_features)`. A dataset of incomplete time series observed up to time `t`. `t` must be less than or equal to the maximum sequence length seen during training.
- **Returns:** A tuple of two array-likes:
  - `probabilities`: Array of shape `(n_series, n_classes)` containing the probability estimates for each class, ordered as in `self.classes_`. If `t < self.min_t`, the probabilities for that series will be `NaN`.
  - `delays`: Array of shape `(n_series,)` containing the estimated delays (in number of timestamps) before an optimal prediction timestamp is reached.
- **Visibility:** Public.
- **Side Effects / Thread Safety:** The method does not mutate the estimator's state. It is thread-safe for concurrent predictions provided the underlying base classifier's prediction methods are thread-safe.

### L3 MECHANICS
1. **Validation:** The method first checks if the estimator is fitted by verifying the existence of `_X_fit_dims` (via `check_is_fitted` at line 621).
2. **Formatting:** It validates `X` using `check_array` and `check_dims` (ensuring the number of features matches the training data), and converts it to a standard 3D time series dataset using `to_time_series_dataset` (lines 622-624).
3. **Delegation:** It delegates the actual computation to the internal `_early_predict` method, passing `predict_proba=True` (line 625).
4. **Internal Logic (`_early_predict`):**
   - It checks if the incoming time series has more timestamps than the training data (`X.shape[1] > self._X_fit_dims[1]`). If so, it raises a `ValueError` (line 748).
   - It iterates over each time series in `X`. If the length of the valid (non-NaN) time series is less than `self.min_t`, it appends a default prediction of `NaN`s of length `self.__n_classes_` (lines 752-759).
   - (INFERENCE based on standard early classification logic): For series of sufficient length, it uses the underlying base classifier and cost functions to compute the probabilities and the expected delay.

### L4 CORRECT MINIMAL USAGE
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
import numpy as np

# 1. Prepare full-length training data (4 series, 4 timestamps, 1 feature)
X_train = to_time_series_dataset([
    [1.0, 2.0, 3.0, 4.0],
    [1.1, 2.1, 3.1, 4.1],
    [4.0, 3.0, 2.0, 1.0],
    [4.1, 3.1, 2.1, 1.1]
])
y_train = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    min_t=2,
    lamb=1000.0,
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(X_train, y_train)

# 3. Predict probabilities on incomplete time series (first 2 timestamps)
X_incomplete = X_train[:, :2, :]
probas, delays = model.early_predict_proba(X_incomplete)

# 4. Verify outputs
assert probas.shape == (4, 2), f"Expected shape (4, 2), got {probas.shape}"
assert delays.shape == (4,), f"Expected shape (4,), got {delays.shape}"
print("Probabilities:\n", probas)
print("Delays:\n", delays)
```

### L5 FAILURE FORENSICS
- **`AssertionError: Expected probabilities shape (8, 4), got (8, 3)`**
  - **Cause:** The test author asserted that the returned probability matrix would have 4 columns (representing 4 classes), but the model returned a matrix with 3 columns.
  - **Reasoning:** The number of columns in the probability matrix is strictly determined by `self.__n_classes_` (the number of unique classes discovered in `y` during `fit`). The test likely provided a training dataset `y` that only contained 3 distinct classes, causing the model to fit for 3 classes. When `early_predict_proba` delegated to `_early_predict`, it correctly returned an `(8, 3)` array, violating the hardcoded `(8, 4)` assertion.

### L6 SELF-ASSESSMENT
- **Inferences:**
  - The exact internal computation of probabilities and delays inside `_early_predict` beyond the `min_t` check is inferred, as the provided source cuts off at line 759.
  - The existence of `self.__n_classes_` is inferred to be set during `fit` based on standard scikit-learn/tslearn conventions and its usage at line 752.
- **Information needed for certainty:** The complete source code of `_early_predict` to see exactly how the base classifier is invoked to generate the probabilities and delays.
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The signature, return types, and shapes are explicitly documented in the docstring and confirmed by the return statement and failure history.
  - **L3 (Mechanics):** 9/10. The validation and delegation steps are fully visible. The exact mathematical computation of the delay is hidden in the truncated `_early_predict` method, but the structural mechanics are clear.
  - **L4 (Minimal Usage):** 10/10. The snippet uses standard public APIs, correctly formats the 3D input, fits the model, and unpacks the tuple exactly as required by the contract.