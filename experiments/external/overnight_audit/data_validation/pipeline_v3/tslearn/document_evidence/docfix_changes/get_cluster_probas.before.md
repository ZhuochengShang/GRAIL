## API Test: `get_cluster_probas`

### Signature
```python
def get_cluster_probas(self, Xi)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:215_

_Source doc:_ Compute cluster probability :math:`P(c_k | Xi)`. This quantity is computed using the following formula: .. math:: P(c_k | Xi) = \frac{s_k(Xi)}{\sum_j s_j(Xi)} where .. math:: s_k(Xi) = \frac{1}{1 + \exp{-\lambda \Delta_k(Xi)}} with .. math:: \Delta_k(Xi) = \frac{\bar{D} - d(Xi, c_k)}{\bar{D}} and :math:`\bar{D}` is the average of the distances between `Xi` and the cluster centers. Parameters ---------- Xi: numpy array, shape (t, d) A time series observed up to time t Returns ------- probas : numpy array, shape (n_clusters, ) Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> ts0 = to_time_series([1, 2]) >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=0., ...                                  random_state=0) >>> probas = model.fit(dataset, y).get_cluster_probas(ts0) >>> probas.shape (3,) >>> probas  # doctest: +ELLIPSIS array([0.33..., 0.33..., 0.33...]) >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=10000., ...                                  random_state=0) >>> probas = model.fit(dataset, y).get_cluster_probas(ts0) >>> probas.shape (3,) >>> probas array([0.5, 0.5, 0. ]) >>> ts1 = to_time_series([3, 2]) >>> model.get_cluster_probas(ts1)

### Goal
Compute the probability of a partially observed time series belonging to each cluster in a fitted early classification model.

### Parameters
- `self`: A fitted instance of `NonMyopicEarlyClassifier`.
- `Xi`: A single time series observed up to time `t`, formatted as a 2D numpy array of shape `(t, d)`.

### Input
The model must be fitted first using a 3D time-series dataset `(n_ts, max_sz, d)`. The input `Xi` must be a *single* time series formatted as a 2D numpy array `(t, d)`, typically prepared using `tslearn.utils.to_time_series`. It should not be a 3D dataset.

### Output
Returns `unspecified` — A 1D numpy array of shape `(n_clusters,)` containing the computed probabilities that the partial time series `Xi` belongs to each of the model's clusters.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset, to_time_series
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare the training dataset and fit the model
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1],
    [3, 2, 1, 1, 2, 3],
    [3, 2, 1, 1, 2, 3]
])
y = [0, 0, 0, 1, 1, 1, 0, 0]

model = NonMyopicEarlyClassifier(n_clusters=3, lamb=0., random_state=0)
model.fit(dataset, y)

# 2. Prepare a single partially observed time series
ts0 = to_time_series([1, 2])

# 3. Compute cluster probabilities
probas = model.get_cluster_probas(ts0)

assert probas.shape == (3,)
assert np.allclose(probas, [1/3, 1/3, 1/3])
print(f"Cluster probabilities: {probas}")
```

### LLM Instruction Prompt
- Call `get_cluster_probas` only on a fitted `NonMyopicEarlyClassifier` instance.
- Pass a single 2D time series `(t, d)` as `Xi`, not a 3D dataset `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series` to format the input correctly.
- Do not pass multiple time series at once; this method evaluates one partial series at a time.

### Prompt Snippet
```text
# Fit the early classifier
model = NonMyopicEarlyClassifier(n_clusters=3, lamb=10000., random_state=0)
model.fit(X_train, y_train)

# Evaluate a single partial time series
partial_ts = to_time_series([3, 2])
probas = model.get_cluster_probas(partial_ts)
```

### Common Failure Modes
- **Passing a 3D dataset instead of a 2D time series**: `get_cluster_probas` expects a single time series `(t, d)`. Passing a full dataset `(n_ts, max_sz, d)` will cause shape mismatch errors during distance computation.
- **Calling before fitting**: Attempting to compute probabilities before calling `.fit()` will raise a `NotFittedError` because the cluster centers are not yet initialized.
- **Passing raw lists**: Failing to convert the input list to a 2D numpy array using `to_time_series` can lead to unexpected behavior or attribute errors.

### Fix Code Hint
```python
# BAD: Passing a raw list or a 3D dataset
# probas = model.get_cluster_probas([1, 2, 3])
# probas = model.get_cluster_probas(X_test)

# GOOD: Formatting as a single 2D time series
from tslearn.utils import to_time_series
ts_single = to_time_series([1, 2, 3])
probas = model.get_cluster_probas(ts_single)
```