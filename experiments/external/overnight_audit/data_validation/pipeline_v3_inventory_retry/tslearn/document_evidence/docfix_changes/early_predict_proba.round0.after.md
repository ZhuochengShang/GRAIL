## API Test: `early_predict_proba`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def early_predict_proba(self, X)
```

### Goal
Computes class probability estimates and estimated delays before prediction timestamps for a dataset of incomplete time series using a fitted early classification estimator.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: Array-like of shape `(n_series, t, n_features)`. A dataset of incomplete time series observed up to time `t`.

### Input
`X` must be a 3D array formatted via `tslearn.utils.to_time_series_dataset` representing incomplete time series (where the time dimension `t` is typically smaller than the full series length seen during training). The estimator (`self`) must be fitted first. If `t` is smaller than the estimator's configured `min_t`, the method will return `NaN` values.

### Output
A tuple of two array-likes: `(probabilities, delays)`. 
- `probabilities` has shape `(n_series, len(self.classes_))` containing the class probabilities ordered by `self.classes_`. The number of columns is exactly `len(self.classes_)`, which may be smaller than the number of unique classes in the original training data if classes with too few samples are dropped during internal fitting.
- `delays` has shape `(n_series,)` containing the estimated delays before prediction timestamps.

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare full-length training data
X_train = to_time_series_dataset([
    [1.0, 2.0, 3.0, 4.0, 5.0],
    [1.1, 2.1, 3.1, 4.1, 5.1],
    [4.0, 3.0, 2.0, 1.0, 0.0],
    [4.1, 3.1, 2.1, 1.1, 0.1]
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

# 3. Predict probabilities on incomplete time series (first 3 timestamps)
X_incomplete = X_train[:, :3, :]
probas, delays = model.early_predict_proba(X_incomplete)

# 4. Verify outputs against the classes actually retained by the model
assert probas.shape == (4, len(model.classes_))
assert delays.shape == (4,)
```

### LLM Instruction Prompt
- When calling `early_predict_proba`, ensure the input `X` is strictly a 3D array `(n_series, t, n_features)` representing incomplete time series.
- Always unpack the return value into two variables (e.g., `probas, delays = model.early_predict_proba(X)`).
- Code asserting the shape of the returned probabilities should check against `len(self.classes_)` rather than `len(np.unique(y))`, as the model may drop classes with insufficient samples during internal fitting.

### Prompt Snippet
```text
Use the fitted `NonMyopicEarlyClassifier` to predict probabilities and delays for the incomplete time series `X_incomplete`. Unpack the results into `probas` and `delays`, and assert the probability shape against `len(model.classes_)`.
```

### Common Failure Modes
- **AssertionError on probability shape:** Asserting that the number of columns in the returned probabilities array matches `len(np.unique(y))` of the input labels. The model may drop classes during internal fitting (e.g., due to insufficient samples for cross-validation splits), so the returned array will have `len(model.classes_)` columns.
- **Not unpacking the return value:** Assigning the result to a single variable and attempting to use it as a probability matrix, which fails because the method returns a tuple `(probabilities, delays)`.
- **Passing 2D arrays:** Providing a 2D array `(n_series, t)` instead of the required 3D array `(n_series, t, n_features)`, leading to shape mismatch errors.

### Fix Code Hint
```python
# WRONG: Assuming output columns match original unique labels
probas, delays = model.early_predict_proba(X_incomplete)
assert probas.shape[1] == len(np.unique(y_train))

# CORRECT: Checking against the classes actually retained by the model
probas, delays = model.early_predict_proba(X_incomplete)
assert probas.shape[1] == len(model.classes_)
```