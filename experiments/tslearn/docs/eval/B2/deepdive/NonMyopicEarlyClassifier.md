# Deep-dive: `NonMyopicEarlyClassifier`

model: google:gemini-3.1-pro-preview · tokens in=6,644 out=4,399 · wall 35s · 2026-09-08 14:44

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
USER-FACING. This is a public, scikit-learn compatible estimator intended for end-users to train early classification models on time-series data.
TESTABLE FROM PUBLIC INPUTS. It can be instantiated directly and trained using standard NumPy arrays formatted via `tslearn.utils.to_time_series_dataset`.

L1 PURPOSE
`NonMyopicEarlyClassifier` is a predictive model for time-series data that aims to classify an incoming time series as early as possible. It sits at the end of the machine learning pipeline. By balancing the accuracy of the classification against a user-defined cost for delaying the decision, it determines the optimal timestamp to halt observation and emit a prediction.

L2 CONTRACT
- **Receiver**: A `NonMyopicEarlyClassifier` instance, obtained by calling its constructor.
- **Parameters**:
  - `n_clusters` (int, default=2): Number of clusters to form during the internal clustering phase.
  - `base_classifier` (Estimator or None, default=None): The base scikit-learn compatible classifier to be cloned for each timestamp. If `None`, defaults to a 1-Nearest Neighbor classifier with Euclidean distance.
  - `min_t` (int, default=1): The earliest timestamp at which a classification decision is allowed.
  - `lamb` (float, default=1.0): Hyperparameter $\lambda$ used in the cost function to evaluate cluster probabilities.
  - `cost_time_parameter` (float, default=1.0): Coefficient for the linear time-delay cost function $f(time) = time \times cost\_time\_parameter$.
  - `random_state` (int or None, default=None): Seed for reproducible clustering and data splitting.
- **Return value**: The `.fit(X, y)` method returns `self` (the fitted estimator).
- **Visibility**: Public.
- **Thread-safety/Laziness**: Not thread-safe during `.fit()` as it mutates internal state (e.g., `classifiers_`, `pyhatyck_`, `pyck_`).

L3 MECHANICS
- **Algorithm & Delegation**: 
  1. In `.fit(X, y)`, the input is validated and converted to a 3D time-series dataset using `check_array`, `check_dims`, and `to_time_series_dataset` (lines 150-152).
  2. It instantiates a `TimeSeriesKMeans` model and fits it on `X` to assign each time series to a cluster `c_k` (lines 156-157, 171).
  3. It clones the `base_classifier` (or the default `KNeighborsTimeSeriesClassifier`) for every possible timestamp from `min_t` to the maximum series length `sz`, storing them in the `classifiers_` dictionary (lines 166-167).
  4. It splits the training data in half using `sklearn.model_selection.train_test_split` with `test_size=0.5` and `stratify=c_k` (lines 172-177).
  5. (Inferred from documentation) It trains the cloned classifiers on the first half and uses the second half to estimate the probabilities of true classes given predicted classes and clusters, populating `pyhatyck_` and `pyck_`.
- **State Mutated**: Sets `cluster_`, `__n_classes_`, `_X_fit_dims`, `classifiers_`, `pyhatyck_`, and `pyck_` on the instance.
- **Failure Conditions**: 
  - Raises `ValueError` during `.fit()` if `TimeSeriesKMeans` produces any cluster with only 1 member, because `train_test_split` is called with `stratify=c_k` (line 175) and scikit-learn requires at least 2 members per stratified group.

L4 CORRECT MINIMAL USAGE
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier

# Create a dataset with 2 highly distinct groups of 4 samples each.
# This guarantees TimeSeriesKMeans(n_clusters=2) will create clusters 
# with exactly 4 members each, avoiding the train_test_split stratify ValueError.
X = to_time_series_dataset([
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0],
    [9.0, 9.0, 9.0, 9.0]
])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

model = NonMyopicEarlyClassifier(
    n_clusters=2,
    min_t=1,
    lamb=1.0,
    cost_time_parameter=0.1,
    random_state=42
)

# Fit the model
model.fit(X, y)

# Predict classes and the time at which the decision was made
preds, pred_times = model.predict_class_and_earliness(X)

assert preds.shape == (8,)
assert pred_times.shape == (8,)
print("Predictions:", preds)
print("Prediction times:", pred_times)
```

L5 FAILURE FORENSICS
- **Failure 1 (`AssertionError: Delays should be at least min_t (2)`)**: The user instantiated the model with `min_t=2` and asserted that all returned prediction times were `>= 2`. As explicitly noted in the documentation, `tslearn` has a known off-by-one bug where it can return prediction times less than `min_t`. The assertion failed because the library returned a delay of 1.
- **Failure 2 (`ValueError: The least populated class in y has only 1 member...`)**: The user instantiated the model with `n_clusters=3` and fitted it on a small dataset (likely the 8-sample docstring example). `TimeSeriesKMeans` assigned only 1 sample to one of the 3 clusters. On line 172, `fit` calls `train_test_split(..., stratify=c_k)`. Scikit-learn's `train_test_split` raises a `ValueError` because it cannot stratify a group (in this case, the cluster `c_k`) that contains fewer than 2 samples.

L6 SELF-ASSESSMENT
- **Inferences**: 
  - The exact mechanism of how `pyhatyck_` and `pyck_` are populated after the `train_test_split` is inferred, as the source code snippet truncates immediately after the split.
  - The exact signature of `predict_class_and_earliness` is inferred from the documentation and call sites, as its definition is not in the provided source snippet.
- **Information needed for certainty**: The complete source code of the `fit` and `predict_class_and_earliness` methods.
- **Confidence Scores**:
  - L2 (Contract): 10/10. The constructor signature and documentation are fully provided.
  - L3 (Mechanics): 9/10. The first half of `fit` is explicitly visible and explains the exact cause of the stratification failure; the second half is standard scikit-learn estimator behavior.
  - L4 (Minimal Usage): 10/10. The provided snippet deterministically avoids the stratification bug by providing perfectly separable clusters with sufficient members.