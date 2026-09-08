# Deep-dive: `get_early_predict_proba_generator`

model: google:gemini-3.1-pro-preview · tokens in=5,679 out=3,850 · wall 32s · 2026-09-08 15:29

---

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Classification:** USER-FACING
- **Testability:** TESTABLE FROM PUBLIC INPUTS
- **Explanation:** The API is a public method on an early classification estimator (e.g., `NonMyopicEarlyClassifier`). It is fully documented with user-facing examples and can be tested by instantiating the classifier, fitting it on a standard `tslearn` time-series dataset, and interacting with the returned generator using public NumPy arrays.

### L1 PURPOSE
The `get_early_predict_proba_generator` method creates a stateful Python generator designed for streaming early classification. It allows users to feed incoming time-series data step-by-step (or in chunks) as it becomes available. Instead of requiring the user to manually concatenate historical time steps for each prediction, the generator maintains the accumulated state internally and yields updated class probability estimates and the expected delay before an optimal prediction can be made.

### L2 CONTRACT
- **Receiver:** A fitted instance of an early classifier (e.g., `NonMyopicEarlyClassifier`). It must be fitted via `.fit(X, y)` so that `_X_fit_dims` and the underlying time-step classifiers are initialized.
- **Parameters:**
  - `n_ts`: `int` (default `1`). The number of independent time series that will be streamed and predicted simultaneously by the generator.
- **Returns:** A Python `generator` object.
  - **Interaction:** The user must send data to the generator using `gen.send(x)`.
  - **Input `x`:** An array-like object of shape `(n_ts, n_timestamps, n_features)` representing freshly acquired data. For step-by-step feeding, `n_timestamps` should be `1`.
  - **Yields:** A tuple `(probabilities, delays)`.
    - `probabilities`: A NumPy array of shape `(n_ts, n_classes)` containing the current class probability estimates. If the accumulated time series is shorter than the model's `min_t`, it returns `np.nan` for all classes.
    - `delays`: A NumPy array of shape `(n_ts,)` containing the estimated number of time steps to wait before an optimal prediction can be made.

### L3 MECHANICS
- **Initialization:** The method delegates to `self._get_early_predict_generator(n_ts, predict_proba=True)` (line 725).
- **Validation:** `_get_early_predict_generator` calls `check_is_fitted(self, '_X_fit_dims')` to ensure the model is trained (line 728).
- **Generator Priming:** It instantiates the generator via `self._generate_early_predictions` and calls `next(gen)` to advance it to the first `yield` statement, making it ready to receive data via `.send()` (lines 730-731).
- **State Management:** Inside `_generate_early_predictions`, an empty NumPy array `data` of shape `(n_ts, 0, n_features)` is initialized (line 735).
- **Streaming Loop:** The generator enters an infinite `while True:` loop. It yields the result of `self._early_predict(data, predict_proba=True)` and suspends. When `.send(incoming_timestamp)` is called, it resumes, appending the new data to the `data` array along `axis=1` (lines 737-741). If the append fails, it catches the `ValueError` and issues a `RuntimeWarning` (lines 742-743).
- **Prediction Logic:** `_early_predict` verifies that the accumulated length does not exceed the training length (`self._X_fit_dims[1]`), raising a `ValueError` if it does (line 748). It iterates over each time series, checking if its length is at least `self.min_t`. If not, it returns `np.nan`s. Otherwise, it delegates probability estimation to the specific sub-classifier trained for that exact length (`self.classifiers_[sz].predict_proba`) and calculates the delay via `np.argmin(self._expected_costs(ts))` (lines 754-767).

### L4 CORRECT MINIMAL USAGE
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare training data and fit the early classifier
# 4 samples, 4 time steps, 1 feature
dataset = to_time_series_dataset([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [4, 3, 2, 1]
])
y = [0, 0, 1, 1]

# Fit the model
model = NonMyopicEarlyClassifier(
    n_clusters=2, 
    lamb=1000.0, 
    cost_time_parameter=0.1, 
    random_state=0
)
model.fit(dataset, y)

# 2. Create the generator for 1 time series
gen = model.get_early_predict_proba_generator(n_ts=1)

# 3. Stream 2 timestamps one by one for a single time series
# Shape must be (n_ts, n_timestamps, n_features) -> (1, 1, 1)
incoming_timestamps = np.array([1, 2]).reshape(2, 1, 1, 1)

for x in incoming_timestamps:
    probas, delays = gen.send(x)
    
    # Assert the output shapes match the expected (n_ts, n_classes) and (n_ts,)
    assert probas.shape == (1, 2)
    assert delays.shape == (1,)

print(f"Final step probabilities: {probas.tolist()}, delay: {delays.tolist()}")
```

### L5 FAILURE FORENSICS
- **`AssertionError: Expected probas shape (1, 4), got (1, 3)`**
  - **Cause:** The test author hardcoded an assertion expecting the probability array to have 4 columns (classes), but the model was trained on a dataset that only contained 3 unique classes. Because `predict_proba` returns an array of shape `(n_ts, n_classes)`, the actual shape was `(1, 3)`.
  - **Resolution:** The assertion must dynamically match the number of unique classes in the training labels `y`, or the training data must be adjusted to contain exactly the number of classes the test expects.

### L6 SELF-ASSESSMENT
- **Inferences:** 
  - The specific class name `NonMyopicEarlyClassifier` is inferred as the primary implementer of this method based on the docstring examples, though the method itself is defined in a base or mixin context within `early_classification.py`.
  - The default value of `self.min_t` is assumed to be small enough (likely 1) that sending a single timestamp will trigger a valid prediction rather than returning NaNs, as demonstrated by the docstring output.
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The parameters, return types, and generator `.send()` mechanics are explicitly detailed in the docstring and source code.
  - **L3 (Mechanics):** 10/10. The internal delegation to `_generate_early_predictions` and `_early_predict` is fully visible in the provided source, including the exact array concatenation and validation logic.
  - **L4 (Minimal Usage):** 10/10. The snippet correctly initializes the required 3D array shapes and accurately reflects the stateful generator pattern required by the API.