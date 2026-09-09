## API Test: `NonMyopicEarlyClassifier`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class NonMyopicEarlyClassifier(TimeSeriesMixin, ClassifierMixin, BaseEstimator)
```

### Goal
A scikit-learn compatible, user-facing estimator for non-myopic early classification of time series. It predicts the class of an incoming time series as early as possible by balancing classification accuracy against a time-delay cost. Included in the main user-facing denominator.

### Parameters
*   `n_clusters` (int, default=2): Number of clusters to form during the internal clustering phase.
*   `base_classifier` (Estimator or None): Estimator instance to be cloned and used for classifications (defaults to 1NN with Euclidean metric if `None`).
*   `min_t` (int, default=1): Earliest time at which a classification can be performed.
*   `lamb` (float, default=1.0): Hyperparameter lambda used in the cost function to evaluate cluster probabilities.
*   `cost_time_parameter` (float, default=1.0): Parameter of the time cost function `f(time) = time * cost_time_parameter`.
*   `random_state` (int or None): Random state for reproducible clustering and data splitting.

### Input
**Training Data (`.fit(X, y)`):**
*   `X`: A 3D numpy array of shape `(n_ts, max_sz, d)` formatted using `tslearn.utils.to_time_series_dataset`. **CRITICAL:** The dataset must be large and distinct enough to guarantee that the internal `TimeSeriesKMeans` assigns at least 2 samples to every cluster, otherwise the internal stratified `train_test_split` will raise a `ValueError`.
*   `y`: A 1D array-like of shape `(n_ts,)` containing the target class labels.

### Output
Returns an instantiated `NonMyopicEarlyClassifier` object. After calling `.fit()`, use `.predict_class_and_earliness(X)` to obtain a tuple of `(predictions, prediction_times)`. Do not expect or handle `np.nan` outputs for short series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier

# Construct a dataset with highly distinct groups to guarantee 
# TimeSeriesKMeans creates clusters with >= 2 members each.
X_train = to_time_series_dataset([
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0]
])
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])

model = NonMyopicEarlyClassifier(
    n_clusters=2,
    min_t=1,
    lamb=1.0,
    cost_time_parameter=0.1,
    random_state=42
)

model.fit(X_train, y_train)
preds, pred_times = model.predict_class_and_earliness(X_train)

assert preds.shape == (8,)
assert pred_times.shape == (8,)
```

### LLM Instruction Prompt
- `fit(X, y)` internally clusters the data and calls `train_test_split` stratified by these clusters; therefore, the dataset must be large and distinct enough to guarantee that `TimeSeriesKMeans` assigns at least 2 samples to every cluster, otherwise a `ValueError` is raised.
- To avoid stratification errors in small tests, explicitly construct a dataset with highly distinct, perfectly separable groups (e.g., 4 identical samples per group) matching the `n_clusters` parameter.
- The correct method to predict classes and their decision delays is `predict_class_and_earliness(X)`, not `early_predict(X)`.
- Do not expect or handle `np.nan` outputs for short series; this is hallucinated behavior.
- Always format training and prediction data into a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`.

### Prompt Snippet
```text
Use `tslearn.early_classification.NonMyopicEarlyClassifier` to train an early classifier. Set `n_clusters=2`, `min_t=1`, `lamb=1.0`, and `cost_time_parameter=0.1`. Fit it on a 3D array `X_train` and labels `y_train`. CRITICAL: Construct `X_train` with highly distinct, perfectly separable groups (e.g., 4 identical samples per group) to guarantee the internal `TimeSeriesKMeans` assigns >= 2 samples per cluster, avoiding a stratified split ValueError. Then, use `.predict_class_and_earliness(X_test)` to get the predicted classes and time delays. Do not check for NaNs.
```

### Common Failure Modes
- **Stratified Split ValueError during `fit()`:** The internal `TimeSeriesKMeans` produced a cluster with only 1 sample, triggering a `ValueError` in scikit-learn's `train_test_split(stratify=c_k)`. The dataset must guarantee at least 2 samples per cluster.
- **Hallucinated Method Name:** Calling `.early_predict(X)` instead of the actual method `.predict_class_and_earliness(X)`, resulting in an `AttributeError`.
- **Hallucinated NaN Behavior:** Expecting the model to return `np.nan` for series shorter than `min_t`. This is hallucinated behavior and should not be tested or relied upon.
- **Strict Delay Assertions Failing (`AssertionError: Delays should be at least min_t`):** Asserting that all returned prediction times (delays) are `>= min_t` when `min_t > 1`. A known off-by-one bug in `tslearn` can cause the model to return prediction times less than `min_t` (e.g., 1 when `min_t=2`).

### Fix Code Hint
```python
# WRONG: Small/indistinct dataset causing ValueError, hallucinated method, and NaN handling
X_train = to_time_series_dataset([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]) # Fails: < 2 samples per cluster
model = NonMyopicEarlyClassifier(n_clusters=2)
model.fit(X_train, y_train)
preds, delays = model.early_predict(X_test)
valid_preds = preds[~np.isnan(preds)]

# FIX: Distinct dataset with >= 2 samples per cluster, correct method, no NaN handling
X_train = to_time_series_dataset([
    [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0], 
    [9.0, 9.0], [9.0, 9.0], [9.0, 9.0], [9.0, 9.0]
])
model = NonMyopicEarlyClassifier(n_clusters=2)
model.fit(X_train, y_train)
preds, delays = model.predict_class_and_earliness(X_test)
```