# Deep-dive: `get_cluster_probas`

model: google:gemini-3.1-pro-preview · tokens in=6,276 out=3,496 · wall 28s · 2026-09-08 15:25

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as USER-FACING. While it serves as an internal helper for `_expected_costs` during the early classification prediction phase, it is explicitly documented with public examples and mathematical formulations, allowing users to inspect the cluster assignment probabilities of incoming partial time series. 

Standalone testability is classified as TESTABLE FROM PUBLIC INPUTS. The receiver (`NonMyopicEarlyClassifier`) can be instantiated and fitted using standard public APIs (`fit` with a valid dataset), after which `get_cluster_probas` can be invoked directly on a partial time series.

L1 PURPOSE
The `get_cluster_probas` method computes the probability that a single, partially observed time series belongs to each of the clusters discovered by a `NonMyopicEarlyClassifier` during its training phase. In the library's data flow, it bridges the clustering step (which groups full-length training series) and the cost-evaluation step (which estimates the expected cost of predicting at the current time step versus waiting), by providing the conditional probability $P(c_k | Xi)$ used in the expected cost formula.

L2 CONTRACT
- **Receiver (`self`)**: An instance of `NonMyopicEarlyClassifier` that has already been fitted via `.fit(X, y)`. The fitting process initializes `self.cluster_.cluster_centers_`, which is strictly required by this method.
- **Parameters**:
  - `Xi`: A 2D numpy array of shape `(t, d)` representing a single time series observed up to time `t`. It is typically prepared using `tslearn.utils.to_time_series`.
- **Returns**: 
  - `probas`: A 1D numpy array of shape `(n_clusters,)` containing the normalized probabilities that `Xi` belongs to each cluster.
- **Visibility**: Public.
- **Thread-safety/Laziness**: The method is not lazy (computes eagerly). It is thread-safe for concurrent reads (predictions) provided the underlying `self.cluster_.cluster_centers_` is not being mutated by a concurrent `fit` call.

L3 MECHANICS
1. The method first validates the input `Xi` using `check_array(Xi)` (line 278).
2. It computes the element-wise differences between the partial series `Xi` and the model's cluster centers, truncating the cluster centers to the length of `Xi` (`self.cluster_.cluster_centers_[:, :len(Xi)]`) (line 279).
3. It calculates the Euclidean distance for each cluster using `np.linalg.norm(diffs, axis=(1, 2))` (line 280).
4. It computes the average of these distances across all clusters (line 281).
5. It calculates a relative proximity score $\Delta_k$ for each cluster: `1. - distances_clusters / average_distance` (line 282).
6. It applies a sigmoid-like transformation using the model's $\lambda$ parameter to get unnormalized probabilities $s_k$: `1. / (1. + np.exp(-self.lamb * delta_k))` (line 283).
7. Finally, it normalizes these values by dividing by their sum so they form a valid probability distribution, returning the result (line 284).

L4 CORRECT MINIMAL USAGE
```python
from tslearn.utils import to_time_series_dataset, to_time_series
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare a training dataset. 
# CRITICAL: y_train must have >= 2 samples per class for internal cross-validation.
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

# 2. Instantiate and fit the model
model = NonMyopicEarlyClassifier(n_clusters=3, lamb=0.0, random_state=0)
model.fit(dataset, y_train)

# 3. Prepare a single partially observed time series (2D array)
ts0 = to_time_series([1, 2])

# 4. Compute cluster probabilities
probas = model.get_cluster_probas(ts0)

assert probas.shape == (3,)
print(f"Cluster probabilities: {probas}")
```

L5 FAILURE FORENSICS
- **`ValueError: The least populated class in y has only 1 member...`**: 
  In the recorded failed attempts, the execution harness injected a dataset (`X`, `y`) into the `model.fit(X, y)` call where at least one class in `y` contained only a single sample. The `NonMyopicEarlyClassifier.fit` method relies on internal cross-validation (likely `StratifiedKFold` from scikit-learn) to calibrate probabilities. This cross-validation strictly requires a minimum of 2 samples per class to form valid train/test splits. The failure occurs before `get_cluster_probas` is even reached.

L6 SELF-ASSESSMENT
- **Inferences**: 
  - `check_array` is inferred to be imported from `sklearn.utils.validation`, which is standard in scikit-learn compatible estimators.
  - The exact mechanism causing the `ValueError` during `fit` is inferred to be `StratifiedKFold` or a similar scikit-learn cross-validation splitter, based on the standard scikit-learn error message present in the failure logs.
- **Information needed for certainty**: The full import block of `early_classification.py` and the implementation of `NonMyopicEarlyClassifier.fit` to confirm the exact cross-validation strategy used.
- **Confidence scores**:
  - L2 (Contract): 10/10. The docstring explicitly defines the shapes and types of the inputs and outputs.
  - L3 (Mechanics): 10/10. The mathematical operations are entirely contained within the provided 7 lines of the method body.
  - L4 (Usage): 10/10. The minimal usage is directly adapted from the provided doctest, which is known to pass when the dataset constraints are respected.