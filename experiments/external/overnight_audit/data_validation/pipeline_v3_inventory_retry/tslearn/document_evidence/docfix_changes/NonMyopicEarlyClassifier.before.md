## API Test: `NonMyopicEarlyClassifier`

### Signature
```python
class NonMyopicEarlyClassifier(TimeSeriesMixin, ClassifierMixin, BaseEstimator)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:18_

_Source doc:_ Early Classification modelling for time series using the model presented in [1]_. Parameters ---------- n_clusters : int Number of clusters to form. base_classifier : Estimator or None Estimator (instance) to be cloned and used for classifications. If None, the chosen classifier is a 1NN with Euclidean metric. min_t : int Earliest time at which a classification can be performed on a time series lamb : float Value of the hyper parameter lambda used during the computation of the cost function to evaluate the probability that a time series belongs to a cluster given the time series. cost_time_parameter : float Parameter of the cost function of time. This function is of the form : f(time) = time * cost_time_parameter random_state: int Random state of the base estimator Attributes ---------- classifiers_ : list A list containing all the classifiers trained for the model, that is, (maximum_time_stamp - min_t) elements. pyhatyck_ : array like of shape (maximum_time_stamp - min_t, n_cluster, __n_classes, __n_classes) Contains the probabilities of being classified as class y_hat given class y and cluster ck for a trained classifier. The penultimate dimension of the array is associated to the true class of the series and the last dimension to the predicted class. pyck_ : array like of shape (__n_classes, n_cluster) Contains the probabilities of being of true class y given a cluster ck X_fit_dims : tuple of the same shape as the training dataset Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=1000.,

### Goal
A scikit-learn compatible estimator for non-myopic early classification of time series, which predicts the class of an incoming time series as early as possible by balancing classification accuracy against a time-delay cost.

### Parameters
_None._

### Input
**Constructor Arguments:**
*   `n_clusters` (int): Number of clusters to form.
*   `base_classifier` (Estimator or None): Estimator instance to be cloned and used for classifications (defaults to 1NN with Euclidean metric if `None`).
*   `min_t` (int): Earliest time at which a classification can be performed.
*   `lamb` (float): Hyperparameter lambda used in the cost function to evaluate cluster probabilities.
*   `cost_time_parameter` (float): Parameter of the time cost function `f(time) = time * cost_time_parameter`.
*   `random_state` (int): Random state for the base estimator.

**Training Data (`.fit(X, y)`):**
*   `X`: A 3D numpy array of shape `(n_ts, max_sz, d)` representing the training time series. Must be formatted using `tslearn.utils.to_time_series_dataset`.
*   `y`: A 1D array-like of shape `(n_ts,)` containing the target class labels.

### Output
Returns `unspecified` — An instantiated `NonMyopicEarlyClassifier` object (a scikit-learn compatible estimator). After calling `.fit()`, it populates attributes like `classifiers_`, `pyhatyck_`, and `pyck_`, and can be used to call `.early_predict(X)` which returns a tuple of `(predictions, delays)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

# 1. Prepare 3D time-series data
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [3, 2, 1, 1, 2, 3],
    [3, 2, 1, 1, 2, 3],
])
y = [0, 0, 0, 1, 1, 1, 0, 0]

# 2. Instantiate the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=3,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1, metric="euclidean"),
    min_t=2,
    lamb=1000.0,
    cost_time_parameter=0.1,
    random_state=0,
)

# 3. Fit the model
model.fit(dataset, y)

# 4. Predict on truncated series (length >= min_t)
preds, delays = model.early_predict(dataset[:, :3])
assert preds.shape == (8,)
assert delays.shape == (8,)

# 5. Predict on series shorter than min_t (returns NaNs)
preds_short, delays_short = model.early_predict(dataset[:, :1])
assert np.isnan(preds_short).all()
```

### LLM Instruction Prompt
- Always format training and prediction data into a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before passing it to `.fit()` or `.early_predict()`.
- When calling `.early_predict(X)`, expect a tuple of two arrays: `(predictions, delays)`.
- If the input time series provided to `.early_predict(X)` has fewer timestamps than the configured `min_t`, the model will return arrays filled with `np.nan` for both predictions and delays.
- Ensure `n_clusters` is less than or equal to the number of samples provided during `.fit()`.

### Prompt Snippet
```text
Use `tslearn.early_classification.NonMyopicEarlyClassifier` to train an early classifier. Set `min_t=2`, `lamb=1000.0`, and `cost_time_parameter=0.1`. Fit it on the 3D array `X_train` and labels `y_train`. Then, use `.early_predict(X_test)` to get the predicted classes and the time delays at which the decisions were made. Handle potential `np.nan` outputs if `X_test` is shorter than `min_t`.
```

### Common Failure Modes
- **2D Array Input:** Passing a 2D array `(n_ts, max_sz)` instead of the required 3D array `(n_ts, max_sz, d)` to `.fit()` or `.early_predict()`, resulting in shape mismatch errors.
- **Insufficient Timestamps:** Passing a time series to `.early_predict()` that is shorter than `min_t` and failing to handle the resulting `np.nan` values in downstream logic.
- **Too Many Clusters:** Setting `n_clusters` higher than the number of training samples, which will cause the internal clustering step to fail.

### Fix Code Hint
```python
# FIX: Ensure data is 3D and handle NaN predictions for short series
X_3d = to_time_series_dataset(X_raw)
model.fit(X_3d, y)

# early_predict returns a tuple of (predictions, delays)
preds, delays = model.early_predict(X_test_3d)

# Handle cases where the series was shorter than min_t
valid_mask = ~np.isnan(preds)
valid_preds = preds[valid_mask]
```