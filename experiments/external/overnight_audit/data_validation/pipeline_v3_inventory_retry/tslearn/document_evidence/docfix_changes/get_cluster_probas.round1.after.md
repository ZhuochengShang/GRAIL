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
The model must be fitted first using a 3D time-series dataset `(n_ts, max_sz, d)` and a target array `y`. Do not rely on the harness-provided `X` and `y` because `y` may not have at least 2 samples per class; explicitly construct a small training dataset and labels (e.g., `y = [0, 0, 1, 1]`) to satisfy the internal cross-validation requirement. The input `Xi` to `get_cluster_probas` must be a single 2D time series `(t, d)`, not a 3D dataset.

### Output
A 1D numpy array of shape `(n_clusters,)` containing the normalized probabilities that the partial time series `Xi` belongs to each of the model's clusters.

### Valid Call Patterns
```python
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.utils import to_time_series_dataset, to_time_series
import numpy as np

dataset = to_time_series_dataset([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [4, 3, 2, 1]
])
y_train = [0, 0, 1, 1]

model = NonMyopicEarlyClassifier(n_clusters=2, lamb=1.0, random_state=42)
model.fit(dataset, y_train)

partial_ts = to_time_series([1, 2])
probas = model.get_cluster_probas(partial_ts)

assert probas.shape == (2,)
assert np.isclose(np.sum(probas), 1.0)
```

### LLM Instruction Prompt
- Do not rely on the harness-provided `X` and `y` because `y` may not have at least 2 samples per class; explicitly construct a small training dataset and labels (e.g., `y = [0, 0, 1, 1]`) to satisfy the cross-validation requirement.
- `get_cluster_probas` must be called on a fitted `NonMyopicEarlyClassifier` instance.
- The input to `get_cluster_probas` must be a single 2D time series `(t, d)`, not a 3D dataset.

### Prompt Snippet
```python
# Explicitly construct dataset to ensure >= 2 samples per class
X_train = to_time_series_dataset([[1, 2], [1, 2], [3, 4], [3, 4]])
y_train = [0, 0, 1, 1]

model = NonMyopicEarlyClassifier(n_clusters=2, lamb=1.0, random_state=0)
model.fit(X_train, y_train)

partial_ts = to_time_series([1])
probas = model.get_cluster_probas(partial_ts)
```

### Common Failure Modes
- **`ValueError: The least populated class in y has only 1 member...`**: This occurs during the preceding `model.fit()` step if you rely on a default harness `y` where classes have only 1 member. The model uses internal cross-validation which strictly requires at least 2 members per class.
- **Passing a 3D dataset instead of a 2D time series**: `get_cluster_probas` expects a single time series `(t, d)`. Passing a full dataset `(n_ts, max_sz, d)` will cause shape mismatch errors during distance computation.
- **Calling before fitting**: Attempting to compute probabilities before calling `.fit()` will raise a `NotFittedError` because the cluster centers are not yet initialized.

### Fix Code Hint
```python
# BAD: Relying on harness variables that might have 1 sample per class, or passing 3D data
# model.fit(X, y)  # Fails if y has a class with 1 member
# probas = model.get_cluster_probas(X_test)  # Fails if X_test is 3D

# GOOD: Explicitly constructing valid training data and passing a 2D time series
X_train = to_time_series_dataset([[1, 2], [1, 2], [3, 4], [3, 4]])
y_train = [0, 0, 1, 1]  # >= 2 samples per class
model.fit(X_train, y_train)

ts_single = to_time_series([1, 2])
probas = model.get_cluster_probas(ts_single)
```