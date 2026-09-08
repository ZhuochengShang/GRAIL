## API Test: `get_cluster_probas`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def get_cluster_probas(self, Xi)
```

### Goal
Compute the probability of a partially observed time series belonging to each cluster in a fitted `NonMyopicEarlyClassifier`.

### Parameters
- `self`: A fitted instance of `NonMyopicEarlyClassifier`.
- `Xi`: A single time series observed up to time `t`, formatted as a 2D numpy array of shape `(t, d)`.

### Input
The model must be fitted first using a 3D time-series dataset `(n_ts, max_sz, d)` and a target array `y`. The training labels `y` passed to `fit()` must contain at least 2 samples per class, as the model performs internal cross-validation that will otherwise raise a `ValueError`. The input `Xi` to `get_cluster_probas` must be a *single* time series formatted as a 2D numpy array `(t, d)`, typically prepared using `tslearn.utils.to_time_series`. It should not be a 3D dataset.

### Output
A 1D numpy array of shape `(n_clusters,)` containing the normalized probabilities that the partial time series `Xi` belongs to each of the model's clusters.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset, to_time_series
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare the training dataset and fit the model
# y_train MUST have at least 2 samples per class for internal cross-validation
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
y_train = [0, 0, 0, 1, 1, 1, 0, 0]

model = NonMyopicEarlyClassifier(n_clusters=3, lamb=0.0, random_state=0)
model.fit(dataset, y_train)

# 2. Prepare a single partially observed time series
ts0 = to_time_series([1, 2])

# 3. Compute cluster probabilities
probas = model.get_cluster_probas(ts0)

assert probas.shape == (3,)
print(f"Cluster probabilities: {probas}")
```

### LLM Instruction Prompt
- Call `get_cluster_probas` only on a fitted `NonMyopicEarlyClassifier` instance.
- Ensure the training labels `y` passed to `fit()` contain at least 2 samples per class to avoid a `ValueError` from internal cross-validation.
- Pass a single 2D time series `(t, d)` as `Xi`, not a 3D dataset `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series` to format the input correctly.

### Prompt Snippet
```python
# Fit the early classifier with >= 2 samples per class
model = NonMyopicEarlyClassifier(n_clusters=3, lamb=10000., random_state=0)
model.fit(X_train, y_train)

# Evaluate a single partial time series
partial_ts = to_time_series([3, 2])
probas = model.get_cluster_probas(partial_ts)
```

### Common Failure Modes
- **`ValueError: The least populated class in y has only 1 member...`**: This occurs during the preceding `model.fit()` step if any class in `y` has fewer than 2 samples. The model uses internal cross-validation (e.g., `StratifiedKFold`) which strictly requires at least 2 members per class.
- **Passing a 3D dataset instead of a 2D time series**: `get_cluster_probas` expects a single time series `(t, d)`. Passing a full dataset `(n_ts, max_sz, d)` will cause shape mismatch errors during distance computation.
- **Calling before fitting**: Attempting to compute probabilities before calling `.fit()` will raise a `NotFittedError` because the cluster centers are not yet initialized.

### Fix Code Hint
```python
# BAD: Fitting with a single sample for a class, or passing a 3D dataset to get_cluster_probas
# model.fit(X_train, [0, 1, 1])  # Fails if class 0 has only 1 sample
# probas = model.get_cluster_probas(X_test)  # Fails if X_test is 3D

# GOOD: Fitting with >= 2 samples per class, and passing a single 2D time series
# y_train must have >= 2 samples per class: e.g., [0, 0, 1, 1]
model.fit(X_train, y_train)
from tslearn.utils import to_time_series
ts_single = to_time_series([1, 2, 3])
probas = model.get_cluster_probas(ts_single)
```