# tslearn — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `AutoVARIMA`

### Signature
```python
class AutoVARIMA(TimeSeriesMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/forecasting/_arima.py:466_

_Source doc:_ Automatically selects the best Vector Autoregressive Integrated Moving Average (VARIMA) model through Hyndman-Khandakar algorithm [1]_ [2]_. Parameters ---------- max_p : int (default: 5) Maximum order of the AutoRegressive (AR) component to consider. max_d : int (default: 2) Maximum order of differencing considered to achieve stationarity. max_q : int (default: 5) Maximum order of the Moving-Average (MA) component to consider. default_d_for_non_stationarity : int or None (default 0) Used as differentiation order if stationarity cannot be achieved within max_d. If None, an error is raised if stationarity cannot be achieved within max_d. seasonal_period: int or None (default: None) Naïve seasonal integration to apply to VARIMA models max_iter : int (default: 50) The maximum number of iterations to apply to VARIMA models fitting. verbose : int (default 0) When set to a positive integer, displays logs of the tested VARIMA models selection process. If set to 2 or more, also propagates verbosity to the VARIMA models. Attributes ---------- best_estimator_: VARIMA the fitted VARIMA model. Notes ----- This estimator supports variable length time-series See Also -------- VARIMA: Vector AutoRegressive Integrated Moving Average (VARIMA) estimator. References ---------- .. [1] R. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice. OTexts, 2014. https://otexts.com/fpp3/ .. [2] Hyndman, R. J., & Khandakar, Y. (2008). Automatic time series forecasting: The forecast package for R. Journal of Statistical Software, 27(1), 1–22.

### Goal
Automatically selects and fits the best Vector Autoregressive Integrated Moving Average (VARIMA) model for time-series forecasting using the Hyndman-Khandakar algorithm.

### Parameters
_None._

*   **max_p** (int, default: 5): Maximum order of the AutoRegressive (AR) component to consider.
*   **max_d** (int, default: 2): Maximum order of differencing considered to achieve stationarity.
*   **max_q** (int, default: 5): Maximum order of the Moving-Average (MA) component to consider.
*   **default_d_for_non_stationarity** (int or None, default: 0): Used as the differentiation order if stationarity cannot be achieved within `max_d`. If `None`, an error is raised if stationarity cannot be achieved.
*   **seasonal_period** (int or None, default: None): Naïve seasonal integration period to apply to VARIMA models.
*   **max_iter** (int, default: 50): The maximum number of iterations to apply during VARIMA model fitting.
*   **verbose** (int, default: 0): When set to a positive integer, displays logs of the tested VARIMA models selection process.

### Input
*   **Training Data (`X`)**: Passed to `.fit(X)`. Must be a 3D `numpy` array of shape `(n_ts, max_sz, d)` representing the time-series dataset. Variable-length time series are natively supported (shorter series should be padded with `nan`).

### Output
Returns `unspecified` — an instantiated `AutoVARIMA` estimator object (or `self` when `.fit()` is called). After fitting, it exposes a `best_estimator_` attribute containing the selected and fitted `VARIMA` model.

### Valid Call Patterns
```python
import numpy as np
from tslearn.forecasting import AutoVARIMA

# 1. Prepare deterministic 3D time-series data: (n_ts, max_sz, d)
rng = np.random.RandomState(0)
data = rng.normal(size=(10, 100, 2))

# 2. Instantiate and fit the AutoVARIMA model with small search bounds
model = AutoVARIMA(max_p=1, max_q=1, max_d=1, max_iter=2).fit(data)

# 3. Inspect the best selected estimator
best_model = model.best_estimator_
assert best_model.p == 0 and best_model.q == 0 and best_model.d == 0
print(f"Selected VARIMA orders: p={best_model.p}, d={best_model.d}, q={best_model.q}")
```

### LLM Instruction Prompt
- Use `AutoVARIMA` to automatically select the best hyperparameters (`p`, `d`, `q`) for a Vector Autoregressive Integrated Moving Average (VARIMA) model using the Hyndman-Khandakar algorithm.
- Always ensure the input data to `.fit()` or `.predict()` is formatted as a strict 3D `numpy` array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` if converting from raw lists.
- Access the underlying fitted `VARIMA` model via the `.best_estimator_` attribute after calling `.fit()`.
- To prevent long execution times in testing or constrained environments, explicitly set `max_p`, `max_q`, `max_d`, and `max_iter` to small integers (e.g., `0` or `1`).

### Prompt Snippet
```text
from tslearn.forecasting import AutoVARIMA
model = AutoVARIMA(max_p=2, max_q=2, max_d=1, max_iter=10).fit(X_3d)
best_varima = model.best_estimator_
```

### Common Failure Modes
- **ValueError on Non-Stationarity:** If `default_d_for_non_stationarity=None` and stationarity cannot be achieved within `max_d`, a `ValueError` is raised. Provide a default integer fallback to avoid this.
- **ValueError on Short Series:** Providing time series that are too short for the specified `seasonal_period` or differencing orders will raise a `ValueError` during `.fit()` or `.predict()`.
- **Dimensionality Errors:** Passing 1D or 2D arrays instead of the strict 3D `(n_ts, max_sz, d)` format required by `tslearn` estimators.

### Fix Code Hint
```python
# FIX: Ensure data is 3D (n_ts, max_sz, d) and handle potential non-stationarity errors
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
model = AutoVARIMA(max_d=2, default_d_for_non_stationarity=0).fit(X_3d)
```

## API Test: `Backend`

### Signature
```python
class Backend(object)
```
_Source: tslearn/tslearn/backend/backend.py:55_

_Source doc:_ Class for the  backend. Parameter --------- data : array-like or string or None Indicates the backend to choose. If data is a Numpy array or data equals 'numpy' or data is None, self.backend is set to NumpyBackend(). If data is a PyTorch array or data equals 'pytorch', self.backend is set to PytorchBackend(). Optional, default equals None.

### Goal
A stateful wrapper class that manages and queries the active computational backend (NumPy or PyTorch) for time-series operations, allowing dynamic backend switching.

### Parameters
_None._

### Input
Although the signature reflects no formal parameters, the constructor accepts an optional `data` argument to indicate the backend to choose:
- **`data`** (array-like, string, or `None`): 
  - If `data` is a NumPy array, the string `"numpy"`, or `None`, the backend is set to `NumPyBackend`.
  - If `data` is a PyTorch tensor, the string `"pytorch"`, or the string `"torch"`, the backend is set to `PyTorchBackend`.

### Output
Returns `unspecified` — An instance of the `Backend` class. This instance acts as a manager, exposing boolean properties (`.is_numpy`, `.is_pytorch`) to check the active state, and methods (`.get_backend()`, `.set_backend(data)`) to retrieve or change the underlying backend implementation object.

### Valid Call Patterns
```python
from tslearn.backend import Backend
import numpy as np

# Initialize the backend manager using a string
backend_ = Backend("numpy")

# Assert falsifiable properties about the active backend state
assert backend_.is_numpy
assert not backend_.is_pytorch

# Retrieve the underlying backend implementation instance
actual_be = backend_.get_backend()

# Switch the backend dynamically using a NumPy array
backend_.set_backend(np.array([1.0, 2.0, 3.0]))
assert backend_.is_numpy

print(f"Correctness witness: Backend managed successfully. Active class: {actual_be.__class__.__name__}")
```

### LLM Instruction Prompt
- Use `Backend` to instantiate a stateful manager for the computational backend (NumPy or PyTorch).
- Pass `"numpy"`, `"pytorch"`, `"torch"`, a NumPy array, a PyTorch tensor, or `None` to the constructor to select the backend.
- Do not call mathematical functions directly on the `Backend` instance; you must call `.get_backend()` to retrieve the actual backend implementation (e.g., `NumPyBackend`).
- Check the current backend state using the boolean properties `.is_numpy` and `.is_pytorch`.
- Change the active backend after initialization using `.set_backend(data)`.

### Prompt Snippet
```text
`Backend(data)` creates a backend manager. `data` can be "numpy", "pytorch", "torch", an array/tensor, or None. Use `.is_numpy` or `.is_pytorch` to check the active backend, `.get_backend()` to retrieve the backend instance, and `.set_backend(data)` to switch it dynamically.
```

### Common Failure Modes
- **Missing PyTorch Dependency:** Initializing with `"torch"` or `"pytorch"` when the `pytorch` package is not installed locally will raise a `ValueError` matching `"Could not use the PyTorch backend"`.
- **Using the Wrapper as the Backend:** Attempting to call backend-specific mathematical functions directly on the `Backend` instance instead of calling `.get_backend()` first to retrieve the actual backend implementation object.

### Fix Code Hint
```python
from tslearn.backend import Backend

# Safely initialize a backend, falling back to NumPy if PyTorch is unavailable
try:
    be_manager = Backend("torch")
except ValueError as e:
    if "Could not use the PyTorch backend" in str(e):
        be_manager = Backend("numpy")
    else:
        raise

# Always call get_backend() to access the actual backend functions
active_backend = be_manager.get_backend()
```

## API Test: `BaseModelPackage`

### Signature
```python
class BaseModelPackage(object)
```
_Source: tslearn/tslearn/bases/bases.py:78_

### Goal
Acts as a base class for model packaging and serialization within the `tslearn` library.

### Parameters
_None._

### Input
No inputs or preconditions are required to instantiate this base class.

### Output
Returns `unspecified` — an initialized instance of the `BaseModelPackage` object.

### Valid Call Patterns
```python
from tslearn.bases import BaseModelPackage

# Inferred from signature: instantiate the base class without arguments
model_package = BaseModelPackage()

# Verify instantiation
assert isinstance(model_package, BaseModelPackage)
print(f"Successfully instantiated: {type(model_package).__name__}")
```

### LLM Instruction Prompt
- When interacting with `BaseModelPackage`, do not pass any arguments to its constructor. 
- Recognize it as a base class for model packaging; do not invent serialization methods (like `.save()` or `.load()`) on this base class unless explicitly provided by a derived estimator's API facts.

### Prompt Snippet
```text
`BaseModelPackage` is a base class in `tslearn.bases`. It takes no arguments in its constructor (`BaseModelPackage()`). Do not invent or call undocumented serialization methods on it directly.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Because it inherits directly from `object` and defines no parameters, passing hyperparameters or data during instantiation will raise a `TypeError`.
- **Calling invented methods:** Assuming the presence of standard serialization methods (e.g., `to_json()`, `save()`) that are not explicitly listed in the API facts.

### Fix Code Hint
```python
# WRONG: model_package = BaseModelPackage(model=my_model)
# RIGHT:
model_package = BaseModelPackage()
```

## API Test: `CachedDatasets`

### Signature
```python
class CachedDatasets
```
_Source: tslearn/tslearn/datasets/cached.py:5_

_Source doc:_ A convenience class to access cached time series datasets. Note, that these *cached datasets* are statically included into *tslearn* and are distinct from the ones in :class:`UCR_UEA_datasets`. When using the Trace dataset, please cite [1]_. See Also -------- UCR_UEA_datasets : Provides more datasets and supports caching. References ---------- .. [1] A. Bagnall, J. Lines, W. Vickers and E. Keogh, The UEA & UCR Time Series Classification Repository, www.timeseriesclassification.com

### Goal
Instantiate a convenience class to access statically included time-series datasets (such as the Trace dataset) bundled with `tslearn`.

### Parameters
_None._

### Input
No arguments are required to instantiate the class.

### Output
Returns `unspecified` — an instance of `CachedDatasets` that provides methods (like `list_datasets()`) to interact with the statically bundled datasets.

### Valid Call Patterns
```python
from tslearn.datasets import CachedDatasets

data_loader = CachedDatasets()
cached = data_loader.list_datasets()

print(f"Available cached datasets: {cached}")
assert "Trace" in cached, "Trace dataset must be statically included."
```

### LLM Instruction Prompt
- Instantiate `CachedDatasets` without any arguments.
- Use this class specifically for statically included datasets (like "Trace"), not for downloading external UCR/UEA datasets (use `UCR_UEA_datasets` for that).

### Prompt Snippet
```text
Use `tslearn.datasets.CachedDatasets()` to access statically included time-series datasets like "Trace". It takes no arguments.
```

### Common Failure Modes
- Passing dataset names or paths to the constructor (it takes no arguments).
- Attempting to use this class to download external datasets from the UCR/UEA repository (which requires `UCR_UEA_datasets` instead).

### Fix Code Hint
```python
# WRONG: data_loader = CachedDatasets(dataset_name="Trace")
# RIGHT: data_loader = CachedDatasets()
```

## API Test: `EmptyClusterError`

### Signature
```python
class EmptyClusterError(Exception)
```
_Source: tslearn/tslearn/clustering/utils.py:17_

### Goal
An exception class raised when a cluster loses all its assigned time-series samples during the execution of a clustering algorithm.

### Parameters
_None._

### Input
As a standard Python exception subclass, it accepts standard `Exception` arguments (such as a string error message) when instantiated, though no custom parameters are defined by the API.

### Output
Returns `unspecified` — An exception object that inherits from Python's built-in `Exception`, which can be raised or caught during time-series clustering workflows.

### Valid Call Patterns
```python
from tslearn.clustering.utils import EmptyClusterError

# Example inferred from the signature (not verified by existing tests)
try:
    # Simulate the exception being raised internally by a tslearn clustering estimator
    raise EmptyClusterError("A cluster became empty during iteration.")
except EmptyClusterError as e:
    assert isinstance(e, Exception)
    print(f"Successfully caught: {type(e).__name__}")
```

### LLM Instruction Prompt
- When writing robust time-series clustering pipelines or custom `tslearn`-compatible clustering estimators, catch `EmptyClusterError` to gracefully handle edge cases where a cluster centroid loses all its assigned time series. If implementing a custom clusterer, raise this exception when an empty cluster is detected.

### Prompt Snippet
```text
Catch `tslearn.clustering.utils.EmptyClusterError` to handle unstable clustering iterations where a cluster becomes empty, often due to `n_clusters` being too high.
```

### Common Failure Modes
- **Unhandled Exception on Fit:** An unhandled `EmptyClusterError` crashing a training pipeline. This typically occurs when `n_clusters` is set too high relative to the dataset size, or when using a poor centroid initialization strategy that leaves some centroids stranded far from the data.

### Fix Code Hint
```python
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering.utils import EmptyClusterError

try:
    # Attempt to fit the model
    model = TimeSeriesKMeans(n_clusters=10, metric="dtw")
    model.fit(X_scaled)
except EmptyClusterError:
    # Fallback strategy: reduce the number of clusters or change initialization
    print("Empty cluster encountered. Falling back to fewer clusters.")
    model = TimeSeriesKMeans(n_clusters=3, metric="dtw")
    model.fit(X_scaled)
```

## API Test: `GlobalArgminPooling1D`

### Signature
```python
class GlobalArgminPooling1D(Layer)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:97_

_Source doc:_ Global argmin pooling operation for temporal data. # Input shape 3D tensor with shape: `(batch_size, steps, features)`. # Output shape 2D tensor with shape: `(batch_size, features)`. Examples -------- >>> x = numpy.array([5.0, 6.8, numpy.inf]) >>> x = x.reshape([1, 3, 1]) >>> ops.convert_to_numpy(GlobalArgminPooling1D()(x)) array([[0.]], dtype=float32)

### Goal
A neural network layer that performs global argmin pooling over the temporal dimension of a time-series tensor, returning the index of the minimum value for each feature.

### Parameters
_None._

### Input
A 3D tensor or NumPy array with shape `(batch_size, steps, features)` (corresponding to `(n_ts, max_sz, d)`). Raw lists or 1D/2D arrays must be converted to this strict 3D format before being passed to the layer, typically using `numpy.reshape` or `tslearn.utils.to_time_series_dataset`.

### Output
Returns `unspecified` — A 2D tensor with shape `(batch_size, features)` containing the temporal indices (typically as floats) of the minimum values for each feature along the `steps` dimension.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets.shapelets import GlobalArgminPooling1D

# 1. Prepare a 3D time-series tensor: (batch_size=1, steps=3, features=1)
x = np.array([5.0, 6.8, np.inf]).reshape(1, 3, 1)

# 2. Instantiate the pooling layer
pooling_layer = GlobalArgminPooling1D()

# 3. Apply the layer to the 3D input
output = pooling_layer(x)

# 4. Convert the output tensor to a NumPy array for inspection
output_np = np.array(output)

assert output_np.shape == (1, 1), f"Expected shape (1, 1), got {output_np.shape}"
assert output_np[0, 0] == 0.0, "Expected the minimum value (5.0) to be at index 0"
print(f"Argmin indices: {output_np.tolist()}")
```

### LLM Instruction Prompt
- Instantiate `GlobalArgminPooling1D` without arguments.
- Call the instantiated layer on a 3D tensor or array strictly formatted as `(batch_size, steps, features)`.
- Expect a 2D tensor output of shape `(batch_size, features)` representing the argmin indices.

### Prompt Snippet
```text
Instantiate `GlobalArgminPooling1D` and call it on a 3D tensor `(batch_size, steps, features)`. It returns a 2D tensor `(batch_size, features)` containing the index of the minimum value along the steps dimension.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the strictly required 3D tensor `(batch_size, steps, features)`, which will cause shape mismatch errors in the underlying backend operations.
- Failing to convert raw time-series lists into the required 3D format before passing them to the layer.

### Fix Code Hint
```python
# Ensure input is strictly 3D (batch_size, steps, features) before calling the layer
x_3d = np.array(x).reshape(batch_size, steps, features)
layer = GlobalArgminPooling1D()
output = layer(x_3d)
```

## API Test: `GlobalMinPooling1D`

### Signature
```python
class GlobalMinPooling1D(Layer)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:66_

_Source doc:_ Global min pooling operation for temporal data. # Input shape 3D tensor with shape: `(batch_size, steps, features)`. # Output shape 2D tensor with shape: `(batch_size, features)`. Examples -------- >>> x = numpy.array([5.0, 6.8, numpy.inf]) >>> x = x.reshape([1, 3, 1]) >>> ops.convert_to_numpy(GlobalMinPooling1D()(x)) array([[5.]], dtype=float32)

### Goal
Performs a global minimum pooling operation over the temporal dimension of a time-series tensor, extracting the minimum value for each feature across all time steps.

### Parameters
_None._

### Input
- A 3D tensor or NumPy array of shape `(batch_size, steps, features)` representing a batch of time series.
- The input must strictly have 3 dimensions. If working with univariate time series, the `features` dimension must be explicitly sized to `1`.

### Output
Returns `unspecified` — A 2D tensor of shape `(batch_size, features)` containing the minimum values across the `steps` dimension. The exact return type depends on the active backend (e.g., a Keras/TensorFlow tensor).

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets.shapelets import GlobalMinPooling1D

# 1. Prepare a 3D input tensor (batch_size=1, steps=3, features=1)
x = np.array([5.0, 6.8, np.inf]).reshape(1, 3, 1)

# 2. Instantiate the pooling layer
pool_layer = GlobalMinPooling1D()

# 3. Apply the layer to the temporal data
output = pool_layer(x)

# 4. Convert output to NumPy array for inspection (handles backend tensors)
if hasattr(output, "numpy"):
    output_np = output.numpy()
else:
    output_np = np.asarray(output)

assert output_np.shape == (1, 1)
assert output_np[0, 0] == 5.0
print("GlobalMinPooling1D output:", output_np)
```

### LLM Instruction Prompt
- Use `GlobalMinPooling1D` to extract the minimum value across the time steps of a 3D time-series tensor, typically within a neural network or shapelet-learning architecture.
- Ensure the input is strictly a 3D tensor/array of shape `(batch_size, steps, features)`.
- The output will be a 2D tensor of shape `(batch_size, features)`.
- Do not pass arguments to the constructor; it takes no parameters.

### Prompt Snippet
```text
tslearn.shapelets.shapelets.GlobalMinPooling1D: Keras-compatible layer for global min pooling over temporal data.
Input: 3D tensor (batch_size, steps, features).
Output: 2D tensor (batch_size, features).
Usage: layer = GlobalMinPooling1D(); out = layer(x)
```

### Common Failure Modes
- **Dimensionality Error:** Passing a 2D array `(batch_size, steps)` instead of the required 3D array `(batch_size, steps, features)`. This will cause backend tensor shape mismatches.
- **Constructor Arguments:** Attempting to pass pooling sizes or strides to the constructor (e.g., `GlobalMinPooling1D(pool_size=2)`). The class takes no parameters because it pools globally over the entire temporal dimension.

### Fix Code Hint
```python
# Ensure input is 3D: (batch_size, steps, features)
if x.ndim == 2:
    x = x.reshape(x.shape[0], x.shape[1], 1)

# Instantiate without arguments and call
layer = GlobalMinPooling1D()
output = layer(x)
```

## API Test: `KNeighborsTimeSeries`

### Signature
```python
class KNeighborsTimeSeries(KNeighborsTimeSeriesMixin, NearestNeighbors, BaseModelPackage)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:236_

_Source doc:_ Unsupervised learner for implementing neighbor searches for Time Series. Parameters ---------- n_neighbors : int (default: 5) Number of nearest neighbors to be considered for the decision. metric : {'dtw', 'softdtw', 'ctw', 'euclidean', 'sqeuclidean', \ 'cityblock',  'sax'} (default: 'dtw') Metric to be used at the core of the nearest neighbor procedure. DTW and SAX are described in more detail in :mod:`tslearn.metrics`. When SAX is provided as a metric, the data is expected to be normalized such that each time series has zero mean and unit variance. Other metrics are described in `scipy.spatial.distance doc <https://docs.scipy.org/doc/scipy/reference/spatial.distance.html>`_. metric_params : dict or None (default: None) Dictionary of metric parameters. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` and `verbose` keys passed in `metric_params` are overridden by the `n_jobs` and `verbose` arguments. For 'sax' metric, these are hyper-parameters to be passed at the creation of the `SymbolicAggregateApproximation` object. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. Notes ----- The training data are saved to disk if this model is serialized and may result in a large model file if the training dataset is large. Examples -------- >>> time_series = to_time_series_dataset([[1, 2, 3, 4], ...                                       [3, 3, 2, 0], ...                                       [1, 2, 2, 4]]) >>> knn = KNeighborsTimeSeries(n_neighbors=1).fit(time_series) >>> dataset = to_time_series_dataset([[1, 1, 2, 2, 2, 3, 4]]) >>> dist, ind = knn.kneighbors(dataset, return_distance=True) >>> dist array([[0.]]) >>> print(ind) [[0]] >>> knn2 = KNeighborsTimeSeries(n_neighbors=10, ...                             metric="euclidean").fit(time_series) >>> print(knn2.kneighbors(return_distance=False)) [[2 1] [2 0] [0 1]]

### Goal
Instantiate an unsupervised learner for implementing nearest neighbor searches on time-series data using specialized alignment metrics like DTW or Soft-DTW.

### Parameters
_None._

### Input
- **Constructor Arguments** (passed as kwargs): `n_neighbors` (int, default 5), `metric` (string, e.g., `'dtw'`, `'softdtw'`, `'euclidean'`, `'ctw'`, `'frechet'`, `'sax'`), `metric_params` (dict), and `n_jobs` (int).
- **Training Data**: The dataset `X` passed to `.fit(X)` and `.kneighbors(X)` must be a strict 3D numpy array of shape `(n_ts, max_sz, d)`.
- **Preconditions**: If `metric='sax'` is used, the input time series must be pre-normalized to have zero mean and unit variance.

### Output
Returns `unspecified` — an initialized `KNeighborsTimeSeries` estimator instance that can be fitted with `.fit(X)` and queried with `.kneighbors(X)`. Note that serializing this model saves the entire training dataset to disk, which may result in large files.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors import KNeighborsTimeSeries

# 1. Prepare 3D time-series data (n_ts, max_sz, d)
n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
X = rng.randn(n, sz, d)

# 2. Initialize and fit the unsupervised nearest neighbors model
model = KNeighborsTimeSeries(n_neighbors=5, metric='softdtw')
model.fit(X)

# 3. Query the nearest neighbors
indices = model.kneighbors(X, return_distance=False)

assert indices[0].tolist() == [0, 13, 12, 7, 3]
print("Nearest neighbors for the first time series:", indices[0])
```

### LLM Instruction Prompt
- Always ensure the input data `X` is formatted as a 3D array `(n_ts, max_sz, d)` before calling `.fit(X)` or `.kneighbors(X)`. Use `tslearn.utils.to_time_series_dataset` if converting from raw lists.
- Valid `metric` options include `'dtw'`, `'softdtw'`, `'ctw'`, `'euclidean'`, `'sqeuclidean'`, `'cityblock'`, `'sax'`, and `'frechet'`.
- Do not confuse this unsupervised model with `KNeighborsTimeSeriesClassifier` or `KNeighborsTimeSeriesRegressor`. It does not accept target labels `y` during `.fit()`.

### Prompt Snippet
```text
from tslearn.neighbors import KNeighborsTimeSeries
from tslearn.utils import to_time_series_dataset

X_3d = to_time_series_dataset(X_raw)
model = KNeighborsTimeSeries(n_neighbors=3, metric='dtw')
model.fit(X_3d)

distances, indices = model.kneighbors(X_query_3d, return_distance=True)
```

### Common Failure Modes
- **ValueError for invalid metric**: Passing an unsupported metric string (e.g., `metric='invalid'`) will raise a `ValueError` during `.fit()`.
- **Dimensionality Error**: Passing a 2D array `(n_ts, max_sz)` instead of the required 3D array `(n_ts, max_sz, d)` will cause shape mismatch errors.
- **Unexpected Labels**: Passing `y` labels to `.fit(X, y)` is invalid for this unsupervised estimator; use `KNeighborsTimeSeriesClassifier` instead if classification is the goal.
- **Large Serialized Models**: Because it is a nearest-neighbors model, the entire training dataset is stored in the model object. Serializing it (e.g., with `pickle`) will save the data to disk, potentially creating massive files.

### Fix Code Hint
```python
# Ensure data is 3D before fitting
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)

# Initialize and fit the unsupervised model (no 'y' labels)
knn = KNeighborsTimeSeries(n_neighbors=3, metric="softdtw")
knn.fit(X_3d)

# Query neighbors
distances, indices = knn.kneighbors(X_3d, return_distance=True)
```

## API Test: `KNeighborsTimeSeriesClassifier`

### Signature
```python
class KNeighborsTimeSeriesClassifier(KNeighborsTimeSeriesMixin, KNeighborsClassifier, BaseModelPackage)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:431_

_Source doc:_ Classifier implementing the k-nearest neighbors vote for Time Series. Parameters ---------- n_neighbors : int (default: 5) Number of nearest neighbors to be considered for the decision. weights : str or callable, optional (default: 'uniform') Weight function used in prediction. Possible values: - 'uniform' : uniform weights. All points in each neighborhood are weighted equally. - 'distance' : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away. - [callable] : a user-defined function which accepts an array of distances, and returns an array of the same shape containing the weights. metric : one of the metrics allowed for :class:`.KNeighborsTimeSeries`\ class (default: 'dtw') Metric to be used at the core of the nearest neighbor procedure metric_params : dict or None (default: None) Dictionnary of metric parameters. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` and `verbose` keys passed in `metric_params` are overridden by the `n_jobs` and `verbose` arguments. For 'sax' metric, these are hyper-parameters to be passed at the creation of the `SymbolicAggregateApproximation` object. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. verbose : int, optional (default=0) The verbosity level: if non zero, progress messages are printed. Above 50, the output is sent to stdout. The frequency of the messages increases with the verbosity level. If it more than 10, all iterations are reported. `Glossary <https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation>`__ for more details. Notes ----- The training data are saved to disk if this model is serialized and may result in a large model file if the training dataset is large. Examples -------- >>> clf = KNeighborsTimeSeriesClassifier(n_neighbors=2, metric="dtw") >>> clf.fit([[1, 2, 3], [1, 1.2, 3.2], [3, 2, 1]], ...         y=[0, 0, 1]).predict([[1, 2.2, 3.5]]) array([0]) >>> clf = KNeighborsTimeSeriesClassifier(n_neighbors=2, ...                                      metric="dtw",

### Goal
A scikit-learn compatible classifier that implements the k-nearest neighbors vote for time-series data using specialized distance metrics like Dynamic Time Warping (DTW) or Soft-DTW.

### Parameters
_None._

### Input
*   **Constructor Arguments**: Accepts standard k-NN hyperparameters such as `n_neighbors` (int, default 5), `weights` (str or callable, default 'uniform'), `metric` (str, default 'dtw'), `metric_params` (dict), `n_jobs` (int), and `verbose` (int).
*   **Training Data (`X`)**: For `.fit(X, y)` and `.predict(X)`, the time-series dataset `X` **must** be formatted as a 3D NumPy array of shape `(n_ts, max_sz, d)` (number of time series, maximum sequence length, number of dimensions). Variable-length series should be padded with `nan`.
*   **Labels (`y`)**: An array-like of shape `(n_ts,)` containing the target class labels for training.

### Output
Returns `unspecified` — An instantiated `KNeighborsTimeSeriesClassifier` estimator object. Once fitted, its `.predict(X)` method returns a 1D NumPy array of shape `(n_ts,)` containing the predicted class labels.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

# 1. Deterministic in-memory dataset (3D array: n_ts=3, max_sz=3, d=1)
X_train = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.0], [1.2], [3.2]], 
    [[3.0], [2.0], [1.0]]
])
y_train = np.array([0, 0, 1])
X_test = np.array([[[1.0], [2.2], [3.5]]])

# 2. Standard DTW metric
clf_dtw = KNeighborsTimeSeriesClassifier(n_neighbors=2, metric="dtw")
clf_dtw.fit(X_train, y_train)
preds_dtw = clf_dtw.predict(X_test)

assert preds_dtw.shape == (1,)
print("DTW Predictions:", preds_dtw)

# 3. Soft-DTW with metric_params dictionary
clf_softdtw = KNeighborsTimeSeriesClassifier(
    n_neighbors=2,
    metric="softdtw",
    metric_params={"gamma": 1e-6}
)
clf_softdtw.fit(X_train, y_train)
preds_softdtw = clf_softdtw.predict(X_test)

assert preds_softdtw[0] in [0, 1]
print("Soft-DTW Predictions:", preds_softdtw)
```

### LLM Instruction Prompt
- When using `KNeighborsTimeSeriesClassifier`, ensure the input data `X` is strictly a 3D array of shape `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to convert standard 2D arrays or lists of lists into this required format.
- Do not pass metric-specific arguments (like `gamma` for Soft-DTW or `sakoe_chiba_radius` for DTW) directly as keyword arguments to the constructor. They must be wrapped in a dictionary and passed to the `metric_params` argument.
- Be aware that serializing this model (e.g., via `pickle`) saves the entire training dataset to disk, which can result in massive file sizes for large datasets.

### Prompt Snippet
```text
tslearn's KNeighborsTimeSeriesClassifier requires 3D array inputs (n_ts, max_sz, d). Use `tslearn.utils.to_time_series_dataset` to format data. Pass metric hyperparameters (e.g., gamma) inside a dictionary to the `metric_params` argument, not as direct kwargs.
```

### Common Failure Modes
- **ValueError due to 2D input**: Passing a standard scikit-learn 2D array `(n_samples, n_features)` to `.fit()` or `.predict()` will fail. It must be reshaped to `(n_samples, n_features, 1)` if univariate.
- **TypeError for unexpected kwargs**: Attempting to pass `gamma=0.1` directly to `KNeighborsTimeSeriesClassifier(metric="softdtw", gamma=0.1)` will raise an error. It must be `metric_params={"gamma": 0.1}`.
- **Memory/Storage Exhaustion**: Pickling the fitted estimator for deployment without realizing it stores the entire `X_train` dataset inside the object.

### Fix Code Hint
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

# BAD: Passing 2D arrays and metric parameters as direct kwargs
# clf = KNeighborsTimeSeriesClassifier(n_neighbors=1, metric="softdtw", gamma=0.1)
# clf.fit([[1, 2], [3, 4]], [0, 1])

# GOOD: Convert to 3D array and use the metric_params dictionary
X_2d = [[1, 2], [3, 4]]
y = [0, 1]
X_3d = to_time_series_dataset(X_2d) # Automatically reshapes to (2, 2, 1)

clf = KNeighborsTimeSeriesClassifier(
    n_neighbors=1,
    metric="softdtw",
    metric_params={"gamma": 0.1}
)
clf.fit(X_3d, y)
print("Successfully fitted on 3D data.")
```

## API Test: `KNeighborsTimeSeriesMixin`

### Signature
```python
class KNeighborsTimeSeriesMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:28_

_Source doc:_ Mixin for k-neighbors searches on Time Series.

### Goal
Provides a mixin class for k-neighbors searches on time-series data, intended for developers building custom scikit-learn compatible time-series estimators.

### Parameters
_None._

### Input
As a mixin class, it does not take direct runtime data inputs upon instantiation. It expects to be inherited by an estimator class that processes time-series datasets strictly formatted as 3D `numpy` arrays with shape `(n_ts, max_sz, d)` (number of time series, maximum sequence length, and dimensions).

### Output
Returns `unspecified` — it is a class used for inheritance to provide k-neighbors search capabilities to derived estimator classes, rather than a function returning a data value.

### Valid Call Patterns
```python
from tslearn.neighbors import KNeighborsTimeSeriesMixin
from sklearn.base import BaseEstimator

# 1. Use as a base class for a custom time-series estimator (Inferred from signature)
class CustomTimeSeriesKNN(KNeighborsTimeSeriesMixin, BaseEstimator):
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors

# Verify the mixin is properly inherited
estimator = CustomTimeSeriesKNN()
assert isinstance(estimator, KNeighborsTimeSeriesMixin)
print("Successfully inherited from KNeighborsTimeSeriesMixin.")
```

### LLM Instruction Prompt
- Do not instantiate `KNeighborsTimeSeriesMixin` directly. It is a mixin class designed to be used via multiple inheritance when creating custom time-series k-nearest neighbors estimators.
- Ensure that any custom estimator inheriting from this mixin enforces the `tslearn` strict 3D array format `(n_ts, max_sz, d)` for its `X` inputs during `fit` and `predict`/`kneighbors` calls.

### Prompt Snippet
```text
When building custom k-nearest neighbors models for time-series data in tslearn, inherit from `tslearn.neighbors.KNeighborsTimeSeriesMixin` alongside `sklearn.base.BaseEstimator`. Do not instantiate the mixin directly.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate `KNeighborsTimeSeriesMixin()` directly instead of using it as a base class for an estimator.
- **Incorrect Data Dimensions in Derived Classes:** Failing to format the input data as a 3D array `(n_ts, max_sz, d)` before passing it to the methods provided by the mixin, which will cause underlying distance computations (like DTW) to fail.

### Fix Code Hint
```python
# WRONG: Direct instantiation
# knn = KNeighborsTimeSeriesMixin()

# RIGHT: Inherit to build a custom estimator
from tslearn.neighbors import KNeighborsTimeSeriesMixin
from sklearn.base import BaseEstimator

class MyKNN(KNeighborsTimeSeriesMixin, BaseEstimator):
    pass
```

## API Test: `KNeighborsTimeSeriesRegressor`

### Signature
```python
class KNeighborsTimeSeriesRegressor(KNeighborsTimeSeriesMixin, KNeighborsRegressor, BaseModelPackage)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:614_

_Source doc:_ Regressor implementing the k-nearest neighbors vote for Time Series. Parameters ---------- n_neighbors : int (default: 5) Number of nearest neighbors to be considered for the decision. weights : str or callable, optional (default: 'uniform') Weight function used in prediction. Possible values: - 'uniform' : uniform weights. All points in each neighborhood are weighted equally. - 'distance' : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away. - [callable] : a user-defined function which accepts an array of distances, and returns an array of the same shape containing the weights. metric : one of the metrics allowed for :class:`.KNeighborsTimeSeries`\ class (default: 'dtw') Metric to be used at the core of the nearest neighbor procedure metric_params : dict or None (default: None) Dictionnary of metric parameters. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` and `verbose` keys passed in `metric_params` are overridden by the `n_jobs` and `verbose` arguments. For 'sax' metric, these are hyper-parameters to be passed at the creation of the `SymbolicAggregateApproximation` object. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. verbose : int, optional (default=0) The verbosity level: if non zero, progress messages are printed. Above 50, the output is sent to stdout. The frequency of the messages increases with the verbosity level. If it more than 10, all iterations are reported. `Glossary <https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation>`__ for more details. Examples -------- >>> clf = KNeighborsTimeSeriesRegressor(n_neighbors=2, metric="dtw") >>> clf.fit([[1, 2, 3], [1, 1.2, 3.2], [3, 2, 1]], ...         y=[0.1, 0.1, 1.1]).predict([[1, 2.2, 3.5]]) array([0.1]) >>> clf = KNeighborsTimeSeriesRegressor(n_neighbors=2, ...                                     metric="dtw", ...                                     n_jobs=2) >>> clf.fit([[1, 2, 3], [1, 1.2, 3.2], [3, 2, 1]], ...         y=[0.1, 0.1, 1.1]).predict([[1, 2.2, 3.5]]) array([0.1]) >>> clf = KNeighborsTimeSeriesRegressor(n_neighbors=2, ...                                     metric="dtw",

### Goal
A scikit-learn compatible regressor that predicts continuous target values for time series based on the k-nearest neighbors vote, utilizing specialized time-series distance metrics like Dynamic Time Warping (DTW).

### Parameters
_None._

### Input
**Constructor Arguments:**
- `n_neighbors` (int, default: 5): Number of nearest neighbors to use for the regression vote.
- `weights` (str or callable, default: 'uniform'): Weight function used in prediction ('uniform', 'distance', or a callable).
- `metric` (str, default: 'dtw'): Time-series distance metric to use (e.g., 'dtw', 'softdtw', 'euclidean').
- `metric_params` (dict or None): Additional parameters for the chosen metric.
- `n_jobs` (int or None): Number of parallel jobs for cross-distance matrix computations.
- `verbose` (int): Verbosity level.

**Method Inputs (`fit`, `predict`):**
- `X`: Time-series dataset. Must be formatted as a strict 3D NumPy array of shape `(n_ts, max_sz, d)` (number of time series, maximum length, dimensions). Use `tslearn.utils.to_time_series_dataset` to prepare raw lists or 2D arrays.
- `y`: Target values for regression. A 1D array-like of floats of shape `(n_ts,)`.

### Output
Returns `unspecified` — A fitted `KNeighborsTimeSeriesRegressor` estimator instance (when calling the constructor or `.fit()`). Calling `.predict(X)` on the fitted estimator returns a 1D NumPy array of shape `(n_ts,)` containing the continuous target predictions.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors import KNeighborsTimeSeriesRegressor
from tslearn.utils import to_time_series_dataset

# 1. Prepare data in the strict 3D format (n_ts, max_sz, d)
X_train = to_time_series_dataset([[1.0, 2.0, 3.0], [1.0, 1.2, 3.2], [3.0, 2.0, 1.0]])
y_train = np.array([0.1, 0.1, 1.1])
X_test = to_time_series_dataset([[1.0, 2.2, 3.5]])

# 2. Initialize the regressor with a time-series metric
reg = KNeighborsTimeSeriesRegressor(n_neighbors=2, metric="dtw")

# 3. Fit the model and predict
reg.fit(X_train, y_train)
preds = reg.predict(X_test)

assert isinstance(preds, np.ndarray)
assert preds.shape == (1,)
print(f"Predicted value: {preds[0]}")
```

### LLM Instruction Prompt
- Always convert raw time-series data into a 3D NumPy array of shape `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before passing it to `.fit()` or `.predict()`.
- Use `KNeighborsTimeSeriesRegressor` for continuous target prediction based on time-series similarity.
- Specify a valid time-series distance metric (e.g., `metric="dtw"`) during initialization.
- Ensure `n_neighbors` is less than or equal to the number of training samples.

### Prompt Snippet
```text
Use tslearn's KNeighborsTimeSeriesRegressor to predict continuous values for time series. Convert the training and test data to 3D arrays using to_time_series_dataset first. Initialize the regressor with metric="dtw" and fit it on the training data and target values.
```

### Common Failure Modes
- **Shape Mismatch / ValueErrors**: Passing 1D or 2D arrays directly to `.fit()` or `.predict()` without converting them to the required `(n_ts, max_sz, d)` 3D format.
- **Invalid `n_neighbors`**: Setting `n_neighbors` to a value larger than the number of samples in the training dataset `X`, which will cause a failure during the nearest neighbor query.
- **Invalid Metric**: Providing an unsupported string to the `metric` parameter (must be a valid `tslearn` metric like `"dtw"`, `"softdtw"`, `"euclidean"`, etc.).

### Fix Code Hint
```python
# FIX: Convert raw lists/arrays to the required 3D format before fitting
from tslearn.utils import to_time_series_dataset
X_train_3d = to_time_series_dataset(X_train_raw)
X_test_3d = to_time_series_dataset(X_test_raw)

# FIX: Ensure n_neighbors <= n_samples
reg = KNeighborsTimeSeriesRegressor(n_neighbors=min(5, len(X_train_3d)), metric="dtw")
reg.fit(X_train_3d, y_train)
predictions = reg.predict(X_test_3d)
```

## API Test: `KShape`

### Signature
```python
class KShape(TimeSeriesCentroidBasedClusteringMixin, ClusterMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/clustering/kshape.py:19_

_Source doc:_ KShape clustering for time series. KShape was originally presented in [1]_. Parameters ---------- n_clusters : int (default: 3) Number of clusters to form. max_iter : int (default: 100) Maximum number of iterations of the k-Shape algorithm. tol : float (default: 1e-6) Inertia variation threshold. If at some point, inertia varies less than this threshold between two consecutive iterations, the model is considered to have converged and the algorithm stops. n_init : int (default: 1) Number of time the k-Shape algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia. Ignored if initialization is not random. verbose : bool (default: False) Whether or not to print information about the inertia while learning the model. random_state : integer or numpy.RandomState, optional Generator used to initialize the centers. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. init : {'random' or ndarray} (default: 'random') Method for initialization. 'random': choose k observations (rows) at random from data for the initial centroids. If an ndarray is passed, it should be of shape (n_clusters, ts_size, d) and gives the initial centers. Attributes ---------- cluster_centers_ : numpy.ndarray of shape (sz, d). Centroids labels_ : numpy.ndarray of integers with shape (n_ts, ). Labels of each point inertia_ : float Sum of distances of samples to their closest cluster center. n_iter_ : int The number of iterations performed during fit. Notes ----- This method requires a dataset of equal-sized time series. Examples --------

### Goal
Trains a k-Shape clustering model to group equal-sized time series based on shape similarity using cross-correlation measures.

### Parameters
_None._ (Constructor parameters:)
- `n_clusters` (int, default: 3): Number of clusters to form.
- `max_iter` (int, default: 100): Maximum number of iterations of the k-Shape algorithm.
- `tol` (float, default: 1e-6): Inertia variation threshold. The algorithm stops if inertia varies less than this between consecutive iterations.
- `n_init` (int, default: 1): Number of times the algorithm will be run with different centroid seeds.
- `verbose` (bool, default: False): Whether to print information about the inertia while learning.
- `random_state` (integer or numpy.RandomState, optional): Seed or generator used to initialize the centers.
- `init` ({'random' or ndarray}, default: 'random'): Method for initialization. If an ndarray, it must have shape `(n_clusters, ts_size, d)`.

### Input
- A 3D NumPy array of shape `(n_ts, sz, d)` representing the time-series dataset.
- **Preconditions**: 
  - The dataset **must** consist of equal-sized time series (no variable-length padding or `nan` values).
  - The data should typically be z-normalized (mean 0, variance 1) per time series before fitting, as the k-Shape algorithm relies on scale-invariant cross-correlation. Use `tslearn.preprocessing.TimeSeriesScalerMeanVariance`.

### Output
Returns `unspecified` — The fitted `KShape` estimator instance. After calling `.fit()`, it exposes the following attributes:
- `cluster_centers_`: A 3D NumPy array of shape `(n_clusters, sz, d)` containing the computed shape centroids.
- `labels_`: A 1D NumPy array of shape `(n_ts,)` containing the integer cluster labels for each point.
- `inertia_`: A float representing the sum of distances of samples to their closest cluster center.
- `n_iter_`: An integer representing the number of iterations performed.

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import KShape
from tslearn.preprocessing import TimeSeriesScalerMeanVariance

# 1. Create deterministic equal-sized time series data (n_ts=4, sz=5, d=1)
X = np.array([
    [[1.0], [2.0], [3.0], [4.0], [5.0]],
    [[1.1], [2.1], [3.1], [4.1], [5.1]],
    [[5.0], [4.0], [3.0], [2.0], [1.0]],
    [[5.1], [4.1], [3.1], [2.1], [1.1]]
])

# 2. K-Shape requires z-normalized data for optimal cross-correlation
X_scaled = TimeSeriesScalerMeanVariance().fit_transform(X)

# 3. Initialize and fit the KShape estimator
ks = KShape(n_clusters=2, n_init=1, max_iter=10, random_state=42)
ks.fit(X_scaled)

# 4. Inspect the results
assert ks.labels_.shape == (4,)
assert ks.cluster_centers_.shape == (2, 5, 1)
print(f"Cluster labels: {ks.labels_}")
```

### LLM Instruction Prompt
- Always ensure the input data is strictly a 3D array of shape `(n_ts, sz, d)`.
- Ensure all time series are of equal length. `KShape` does not support variable-length time series padded with `nan`.
- Always scale the input data using `TimeSeriesScalerMeanVariance` before fitting, as k-Shape is designed to operate on z-normalized sequences.
- Do not set `n_clusters` to a value greater than the number of time series in the dataset (`n_ts`).

### Prompt Snippet
```text
Use `tslearn.clustering.KShape` to cluster the time series. First, scale the 3D array `X` using `TimeSeriesScalerMeanVariance`. Then, instantiate `KShape(n_clusters=K, random_state=42)` and call `.fit_predict(X_scaled)`. Ensure `X` contains equal-sized time series without NaNs.
```

### Common Failure Modes
- **`ValueError` on fit**: Occurs if `n_clusters` is strictly greater than the number of samples in the dataset (e.g., `KShape(n_clusters=101).fit(X)` where `len(X) == 15`).
- **`ValueError` on initialization**: Occurs if an invalid string is passed to the `init` parameter (e.g., `init="invalid"` instead of `"random"`).
- **Poor Convergence / Meaningless Clusters**: Occurs if the input time series are not z-normalized prior to fitting.
- **`ValueError` / `NaN` errors**: Occurs if the dataset contains variable-length time series padded with `nan` values.

### Fix Code Hint
```python
from tslearn.clustering import KShape
from tslearn.preprocessing import TimeSeriesScalerMeanVariance

# Ensure X is a 3D array (n_ts, sz, d) without NaNs
X_scaled = TimeSeriesScalerMeanVariance().fit_transform(X)

# n_clusters must be <= n_ts
ks = KShape(n_clusters=3, n_init=1, random_state=42)
labels = ks.fit_predict(X_scaled)
```

## API Test: `KernelKMeans`

### Signature
```python
class KernelKMeans(TimeSeriesMixin, ClusterMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/clustering/kmeans.py:129_

_Source doc:_ Kernel K-means. Parameters ---------- n_clusters : int (default: 3) Number of clusters to form. kernel : string, or callable (default: "gak") The kernel should either be "gak", in which case the Global Alignment Kernel from [2]_ is used or a value that is accepted as a metric by `scikit-learn's pairwise_kernels <https://scikit-learn.org/stable/modules/generated/\ sklearn.metrics.pairwise.pairwise_kernels.html>`_ max_iter : int (default: 50) Maximum number of iterations of the k-means algorithm for a single run. tol : float (default: 1e-6) Inertia variation threshold. If at some point, inertia varies less than this threshold between two consecutive iterations, the model is considered to have converged and the algorithm stops. n_init : int (default: 1) Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia. kernel_params : dict or None (default: None) Kernel parameters to be passed to the kernel function. None means no kernel parameter is set. For Global Alignment Kernel, the only parameter of interest is `sigma`. If set to 'auto', it is computed based on a sampling of the training set (cf :ref:`tslearn.metrics.sigma_gak <fun-tslearn.metrics.sigma_gak>`). If no specific value is set for `sigma`, its defaults to 1. A `RuntimeError` is raised at fit time when computed or explicit value is close to 0 and therefore not compatible with 'gak' kernel. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for GAK cross-similarity matrix computations. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`_ for more details. verbose : int (default: 0) If nonzero, joblib progress messages are printed. random_state : integer or numpy.RandomState, optional Generator used to initialize the centers. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. Attributes ---------- labels_ : numpy.ndarray Labels of each point

### Goal
Clusters time-series data using the Kernel K-means algorithm, natively supporting the Global Alignment Kernel (GAK) or standard scikit-learn pairwise kernels.

### Parameters
_None._

### Input
The constructor accepts hyperparameters to configure the clustering process, including `n_clusters` (int), `kernel` (string, default `"gak"`), `kernel_params` (dict), `max_iter` (int), and `random_state`. 
For the `.fit()`, `.predict()`, and `.fit_predict()` methods, the input data `X` **must** be a 3D `numpy.ndarray` of shape `(n_ts, max_sz, d)` representing the number of time series, maximum sequence length, and dimensionality, respectively.

### Output
Returns `unspecified` — A fitted `KernelKMeans` estimator instance (following scikit-learn conventions). After calling `.fit()`, the instance exposes a `labels_` attribute (a 1D `numpy.ndarray` of cluster assignments) and can be used to `.predict()` cluster assignments for new time-series data.

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import KernelKMeans

# 1. Generate a small deterministic 3D time-series dataset (n_ts=15, max_sz=10, d=3)
rng = np.random.RandomState(0)
time_series = rng.randn(15, 10, 3)

# 2. Initialize and fit KernelKMeans using the Global Alignment Kernel (GAK)
gak_km = KernelKMeans(
    n_clusters=3,
    verbose=False,
    max_iter=5,
    kernel_params={"sigma": "auto"},
    random_state=0
).fit(time_series)

# 3. Verify predictions match the fitted labels
predictions = gak_km.predict(time_series)
np.testing.assert_allclose(gak_km.labels_, predictions)
print(f"GAK Cluster labels: {gak_km.labels_}")

# 4. Initialize and fit using a standard scikit-learn RBF kernel
rbf_km = KernelKMeans(
    n_clusters=2,
    verbose=False,
    kernel="rbf",
    kernel_params={"gamma": 1.0},
    random_state=rng
).fit(time_series)

assert rbf_km.labels_.shape == (15,)
print(f"RBF Cluster labels: {rbf_km.labels_}")
```

### LLM Instruction Prompt
- When using `tslearn.clustering.KernelKMeans`, always ensure the input data passed to `.fit()` or `.predict()` is strictly formatted as a 3D `numpy` array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` if converting from raw lists.
- The default kernel is `"gak"` (Global Alignment Kernel). When using `"gak"`, you can pass `kernel_params={"sigma": "auto"}` to automatically compute the bandwidth based on a sample of the training set.
- Never set `sigma` to `0` (or a value extremely close to `0`) when using the `"gak"` kernel, as this is mathematically incompatible and will raise a `RuntimeError` at fit time.
- The estimator follows the `scikit-learn` API; use `.fit(X)` to train, access `.labels_` for training cluster assignments, and use `.predict(X)` for inference.

### Prompt Snippet
```text
tslearn.clustering.KernelKMeans is a scikit-learn compatible estimator for time-series clustering. 
Inputs to `.fit()` and `.predict()` MUST be 3D numpy arrays of shape `(n_ts, max_sz, d)`. 
When using the default "gak" kernel, pass `kernel_params={"sigma": "auto"}` for automatic bandwidth selection. Do not set sigma to 0.
```

### Common Failure Modes
- **`ValueError` (Dimensionality):** Passing a 1D or 2D array to `.fit()` or `.predict()`. `tslearn` strictly requires a 3D array `(n_ts, max_sz, d)`.
- **`RuntimeError` (Invalid Sigma):** Explicitly setting `kernel_params={"sigma": 0}` when `kernel="gak"`. The GAK kernel requires a strictly positive bandwidth.
- **`ModuleNotFoundError`:** Attempting to import `KernelKMeans` from `sklearn.cluster` instead of `tslearn.clustering`.

### Fix Code Hint
```python
# BAD: 2D array input and invalid sigma for GAK
# km = KernelKMeans(kernel_params={"sigma": 0}).fit(X_2d)

# GOOD: Convert to 3D array and use "auto" sigma
from tslearn.utils import to_time_series_dataset
from tslearn.clustering import KernelKMeans

X_3d = to_time_series_dataset(X_raw)
km = KernelKMeans(
    n_clusters=3, 
    kernel="gak", 
    kernel_params={"sigma": "auto"}
)
km.fit(X_3d)
```

## API Test: `LearningShapelets`

### Signature
```python
class LearningShapelets(TimeSeriesMixin, ClassifierMixin, TransformerMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:290_

_Source doc:_ Learning Time-Series Shapelets model. Learning Time-Series Shapelets was originally presented in [1]_. From an input (possibly multidimensional) time series :math:`x` and a set of shapelets :math:`\{s_i\}_i`, the :math:`i`-th coordinate of the Shapelet transform is computed as: .. math:: ST(x, s_i) = \min_t \sum_{\delta_t} \left\|x(t+\delta_t) - s_i(\delta_t)\right\|_2^2 The Shapelet model consists in a logistic regression layer on top of this transform. Shapelet coefficients as well as logistic regression weights are optimized by gradient descent on a L2-penalized cross-entropy loss. Parameters ---------- n_shapelets_per_size: dict (default: None) Dictionary giving, for each shapelet size (key), the number of such shapelets to be trained (value). If None, :func:`grabocka_params_to_shapelet_size_dict` is used and the size used to compute is that of the shortest time series passed at fit time. max_iter: int (default: 10,000) Number of training epochs. .. versionchanged:: 0.3 default value for max_iter is set to 10,000 instead of 100 batch_size: int (default: 256) Batch size to be used. verbose: {0, 1, 2} (default: 0) `keras` verbose level. optimizer: str or keras.optimizers.Optimizer (default: "sgd") `keras` optimizer to use for training. weight_regularizer: float (default: 0.) Strength of the L2 regularizer to use for training the classification (softmax) layer. If 0, no regularization is performed. shapelet_length: float (default: 0.15) The length of the shapelets, expressed as a fraction of the time series length. Used only if `n_shapelets_per_size` is None. total_lengths: int (default: 3) The number of different shapelet lengths. Will extract shapelets of length i * shapelet_length for i in [1, total_lengths] Used only if `n_shapelets_per_size` is None. max_size: int or None (default: None) Maximum size for time series to be fed to the model. If None, it is set to the size (number of timestamps) of the training time series. scale: bool (default: False)

### Goal
Trains a time-series classification model that simultaneously learns discriminative sub-sequences (shapelets) and a logistic regression classifier on top of the shapelet transform distances.

### Parameters
_None._

### Input
- **Constructor Configuration**: Accepts hyperparameters defined in the docstring, including `n_shapelets_per_size` (dict mapping shapelet size to count), `max_iter` (int, default 10,000), `batch_size` (int), `verbose` (int), `optimizer` (string or keras optimizer), `weight_regularizer` (float), `shapelet_length` (float), `total_lengths` (int), `max_size` (int), and `scale` (bool).
- **Training Data (`X`)**: A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time series. Must be formatted using `tslearn.utils.to_time_series_dataset` if starting from raw lists.
- **Target Labels (`y`)**: A 1D array of shape `(n_ts,)` containing class labels.

### Output
Returns `unspecified` — an instantiated scikit-learn compatible estimator. Once `.fit(X, y)` is called, it learns the shapelets (accessible via `.shapelets_`) and can be used to `.predict(X)` class labels or `.transform(X)` time series into the shapelet-distance feature space.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets import LearningShapelets

# 1. Prepare deterministic 3D time-series data (n_ts, max_sz, d)
rng = np.random.RandomState(0)
X = rng.randn(15, 10, 2)
y = rng.randint(2, size=15)

# 2. Initialize the LearningShapelets classifier
# Using a small max_iter for fast execution in tests
clf = LearningShapelets(
    n_shapelets_per_size={3: 2, 4: 1},
    max_iter=1,
    verbose=0,
    optimizer="sgd"
)

# 3. Fit the model and predict
clf.fit(X, y)
predictions = clf.predict(X)

assert predictions.shape == (15,)
print(f"Predicted classes: {predictions}")
```

### LLM Instruction Prompt
- Always format the input time series `X` as a strict 3D NumPy array `(n_ts, max_sz, d)`.
- When generating tests or examples, set `max_iter` to a very small integer (e.g., `1` or `2`) to prevent long training times, as the default is `10,000`.
- Provide `n_shapelets_per_size` as a dictionary (e.g., `{3: 2, 4: 1}`) to explicitly define the lengths and quantities of shapelets to learn.
- Note that `LearningShapelets` relies on `keras` and `tensorflow` under the hood; ensure the environment supports it.

### Prompt Snippet
```text
Use `tslearn.shapelets.LearningShapelets` to train a shapelet-based classifier. Ensure the input data is a 3D array `(n_ts, max_sz, d)`. Set `max_iter=2` to keep the test fast, and explicitly define `n_shapelets_per_size={3: 2}`.
```

### Common Failure Modes
- **Dimensionality Error**: Passing a 2D array `(n_ts, max_sz)` instead of the required 3D array `(n_ts, max_sz, d)`.
- **Timeout/Slow Execution**: Leaving `max_iter` at its default (`10,000`), which will cause test suites or CI pipelines to hang.
- **Missing Dependencies**: Failing to import due to missing `tensorflow` or `keras` packages, which are required for the gradient descent optimization of shapelets.

### Fix Code Hint
```python
# Convert 2D data to 3D before fitting, and keep max_iter small for tests
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_2d)
clf = LearningShapelets(n_shapelets_per_size={3: 5}, max_iter=2)
clf.fit(X_3d, y)
```

## API Test: `LocalSquaredDistanceLayer`

### Signature
```python
class LocalSquaredDistanceLayer(Layer)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:167_

_Source doc:_ Pairwise (squared) distance computation between local patches and shapelets # Input shape 4D tensor with shape: `(batch_size, steps - shapelet_size, shapelet_length, features)`. # Output shape 3D tensor with shape: `(batch_size, steps, n_shapelets)`.

### Goal
Compute pairwise squared distances between local time-series patches and learned shapelets within a neural network architecture.

### Parameters
_None._

### Input
A 4D tensor representing local time-series patches. The tensor must strictly have the shape `(batch_size, steps - shapelet_size, shapelet_length, features)`.

### Output
Returns `unspecified` — a 3D tensor representing the computed squared distances, with the shape `(batch_size, steps, n_shapelets)`.

### Valid Call Patterns
```python
from tslearn.shapelets.shapelets import LocalSquaredDistanceLayer

# The example is inferred from the signature (not verified)
layer = LocalSquaredDistanceLayer()
assert layer is not None
```

### LLM Instruction Prompt
- Instantiate `LocalSquaredDistanceLayer` without any arguments.
- When calling the instantiated layer, ensure the input is a 4D tensor formatted as `(batch_size, steps - shapelet_size, shapelet_length, features)`.
- Expect the layer to return a 3D tensor of shape `(batch_size, steps, n_shapelets)`.

### Prompt Snippet
```text
Use `LocalSquaredDistanceLayer()` to compute pairwise squared distances between local patches and shapelets in a shapelet learning model. The input must be a 4D tensor `(batch_size, steps - shapelet_size, shapelet_length, features)` and it outputs a 3D tensor `(batch_size, steps, n_shapelets)`.
```

### Common Failure Modes
- Passing arguments during instantiation; the class constructor takes no parameters.
- Providing an input tensor with incorrect dimensions (e.g., passing a standard 3D `(n_ts, max_sz, d)` tslearn dataset directly instead of the required 4D patch tensor).

### Fix Code Hint
```python
# Ensure the layer is instantiated without arguments
layer = LocalSquaredDistanceLayer()

# The input to the layer must be reshaped/extracted into a 4D tensor first
# distances = layer(input_4d_patch_tensor)
```

## API Test: `MatrixProfile`

### Signature
```python
class MatrixProfile(TimeSeriesMixin, TransformerMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/matrix_profile/matrix_profile.py:69_

_Source doc:_ Matrix Profile transformation. Matrix Profile was originally presented in [1]_. Parameters ---------- subsequence_length : int (default: 1) Length of the subseries (also called window size) to be used for subseries distance computations. implementation : str (default: "numpy") Matrix profile implementation to use. Defaults to "numpy" to use the pure numpy version. All the available implementations are ["numpy", "stump", "gpu_stump"]. "stump" and "gpu_stump" are both implementations from the stumpy python library, the latter requiring a GPU. Stumpy is a library for efficiently computing the matrix profile which is optimized for speed, performance and memory. See [2]_ for the documentation. "numpy" is the default pure numpy implementation and does not require stumpy to be installed. scale: bool (default: True) Whether input data should be scaled for each feature of each time series to have zero mean and unit variance. Default for this parameter is set to `True` to match the standard matrix profile setup. Examples -------- >>> time_series = [0., 1., 3., 2., 9., 1., 14., 15., 1., 2., 2., 10., 7.] >>> ds = [time_series] >>> mp = MatrixProfile(subsequence_length=4, scale=False) >>> mp.fit_transform(ds)[0, :, 0]  # doctest: +ELLIPSIS array([ 6.85...,  1.41...,  6.16...,  7.93..., 11.40..., 13.56..., 18.  ..., 13.96...,  1.41...,  6.16...]) References ---------- .. [1] C. M. Yeh, Y. Zhu, L. Ulanova, N.Begum et al. Matrix Profile I: All Pairs Similarity Joins for Time Series: A Unifying View that Includes Motifs, Discords and Shapelets. ICDM 2016. .. [2] STUMPY documentation https://stumpy.readthedocs.io/en/latest/

### Goal
Compute the Matrix Profile transformation of a time-series dataset, which calculates the distances to the nearest neighbor for all subsequences of a given length to identify motifs, discords, and shapelets.

### Parameters
_None._

### Input
- **Constructor arguments:** 
  - `subsequence_length` (int, default: `1`): The window size used for subseries distance computations.
  - `implementation` (str, default: `"numpy"`): The backend to use. Options are `"numpy"`, `"stump"`, and `"gpu_stump"`. The latter two require the `stumpy` library to be installed.
  - `scale` (bool, default: `True`): Whether to zero-mean and unit-variance scale each subsequence before computing distances.
- **Data:** The `.fit_transform(X)` method expects `X` to be a strictly 3D numpy array of shape `(n_ts, max_sz, d)` representing the time-series dataset. Use `tslearn.utils.to_time_series_dataset` to prepare raw lists or 2D arrays.

### Output
Returns `unspecified` — A 3D numpy array representing the matrix profile distances. The shape is typically `(n_ts, max_sz - subsequence_length + 1, d)`, where each value corresponds to the distance of that specific subsequence to its nearest neighbor in the series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.matrix_profile import MatrixProfile

# Deterministic in-memory data: 1 time series, 20 time steps, 1 dimension
rng = np.random.RandomState(0)
X = rng.randn(1, 20, 1)

# Initialize the transformer
mp = MatrixProfile(subsequence_length=10, implementation="numpy", scale=True)

# Compute the matrix profile
X_tr = mp.fit_transform(X)

# Assert falsifiable property
assert X_tr.shape == (1, 11, 1), f"Expected shape (1, 11, 1), got {X_tr.shape}"
print("Matrix Profile computed successfully. Shape:", X_tr.shape)
```

### LLM Instruction Prompt
- Use `tslearn.matrix_profile.MatrixProfile` to compute matrix profiles for time-series motif and discord discovery.
- Initialize the class with `subsequence_length` (int). You may optionally specify `implementation="numpy"` (default) or `"stump"` (requires the `stumpy` package), and `scale=True` (default) or `False`.
- Always ensure the input data `X` passed to `.fit_transform(X)` is formatted as a 3D array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` if necessary.

### Prompt Snippet
```text
from tslearn.matrix_profile import MatrixProfile
from tslearn.utils import to_time_series_dataset

X_3d = to_time_series_dataset([[0., 1., 3., 2., 9., 1., 14., 15., 1., 2., 2., 10., 7.]])
mp = MatrixProfile(subsequence_length=4, scale=False)
X_profile = mp.fit_transform(X_3d)
```

### Common Failure Modes
- **Missing `stumpy` dependency:** Requesting `implementation="stump"` or `"gpu_stump"` when the `stumpy` library is not installed in the environment.
- **Incorrect Input Dimensions:** Passing a 1D list or 2D array directly to `fit_transform` instead of the required `(n_ts, max_sz, d)` 3D array format.
- **Subsequence Length Too Large:** Providing a `subsequence_length` that is greater than or equal to the length of the time series (`max_sz`), which makes it impossible to extract valid subsequences for comparison.

### Fix Code Hint
```python
# FIX: Convert data to 3D format and use the default numpy implementation if stumpy is unavailable
from tslearn.utils import to_time_series_dataset
from tslearn.matrix_profile import MatrixProfile

X_raw = [[1, 2, 3, 4, 5, 6, 7, 8]]
X_3d = to_time_series_dataset(X_raw)

# Ensure subsequence_length < length of time series
mp = MatrixProfile(subsequence_length=4, implementation="numpy")
X_tr = mp.fit_transform(X_3d)
```

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

## API Test: `NumPyBackend`

### Signature
```python
class NumPyBackend(object)
```
_Source: tslearn/tslearn/backend/numpy_backend.py:22_

_Source doc:_ Class for the Numpy  backend.

### Goal
Instantiate the NumPy computational backend, which provides standard CPU-based array operations and metric calculations for time-series data without automatic differentiation.

### Parameters
_None._

### Input
No arguments are required to instantiate this class.

### Output
Returns an instance of `NumPyBackend` — an object providing NumPy-backed implementations of mathematical and array operations used internally by `tslearn` metrics.

### Valid Call Patterns
```python
from tslearn.backend import NumPyBackend

# Example inferred from signature
backend = NumPyBackend()

assert type(backend).__name__ == "NumPyBackend"
print("NumPyBackend instantiated successfully.")
```

### LLM Instruction Prompt
- Instantiate `NumPyBackend` without any arguments.
- Use this backend when standard CPU-based NumPy operations are sufficient and automatic differentiation is not required.
- Note that `tslearn.backend.instantiate_backend("numpy")` is the typical, higher-level way to obtain this backend dynamically.

### Prompt Snippet
```text
`tslearn.backend.NumPyBackend()` creates the NumPy backend instance. It takes no arguments. It is the default backend for tslearn and does not support automatic differentiation.
```

### Common Failure Modes
- **Passing arguments to the constructor:** `NumPyBackend` takes no parameters. Passing strings or arrays directly to the class constructor will raise a `TypeError`.
- **Expecting gradients:** Attempting to compute gradients or use `.backward()` on outputs generated by this backend will fail, as only the PyTorch backend supports automatic differentiation.

### Fix Code Hint
```python
# Incorrect: backend = NumPyBackend("numpy")
# Correct:
from tslearn.backend import NumPyBackend
backend = NumPyBackend()

# Alternatively, use the dynamic instantiator:
from tslearn.backend import instantiate_backend
backend = instantiate_backend("numpy")
```

## API Test: `NumPyLinalg`

### Signature
```python
class NumPyLinalg
```
_Source: tslearn/tslearn/backend/numpy_backend.py:126_

### Goal
A low-level backend helper class that acts as a namespace for NumPy-based linear algebra operations within `tslearn`'s dual-backend system.

### Parameters
_None._

### Input
No inputs are required to instantiate this class. It is typically instantiated internally by the `NumPyBackend` to provide a unified linear algebra interface (mirroring `torch.linalg` for the PyTorch backend).

### Output
Returns `unspecified` — an instance of the `NumPyLinalg` class, which exposes standard linear algebra methods for NumPy arrays used in time-series metric computations.

### Valid Call Patterns
*(Inferred from the signature, as no verbatim examples exist in the documentation or tests)*
```python
from tslearn.backend.numpy_backend import NumPyLinalg

# Instantiate the linear algebra backend helper
np_linalg = NumPyLinalg()

assert isinstance(np_linalg, NumPyLinalg)
print("NumPyLinalg helper instantiated successfully.")
```

### LLM Instruction Prompt
- Do not instantiate `NumPyLinalg` directly in standard time-series workflows; it is a low-level backend component.
- When writing custom metrics or extending `tslearn`, access linear algebra operations dynamically via the instantiated backend's `.linalg` attribute (e.g., `be = instantiate_backend(...); be.linalg`) to maintain compatibility across both NumPy and PyTorch.
- Never pass PyTorch tensors to methods of a `NumPyLinalg` instance, as it strictly expects NumPy arrays.

### Prompt Snippet
```text
`NumPyLinalg` is a backend helper class in `tslearn.backend.numpy_backend`. It takes no parameters upon instantiation. It provides NumPy-specific linear algebra operations for time-series metric calculations. Users should generally rely on `tslearn.backend.instantiate_backend(...)` and use the resulting backend's `.linalg` property rather than hardcoding `NumPyLinalg`.
```

### Common Failure Modes
- **Type Mismatch (PyTorch Tensors):** Passing `torch.Tensor` objects (especially those with `requires_grad=True`) to the underlying methods of `NumPyLinalg` will fail, as this class is strictly bound to the NumPy backend.
- **Direct Instantiation in High-Level Code:** Hardcoding `NumPyLinalg` in custom metric functions breaks `tslearn`'s automatic differentiation capabilities, as it forces NumPy operations instead of allowing dynamic fallback to PyTorch when gradients are needed.

### Fix Code Hint
```python
# INCORECT: Hardcoding the NumPy linalg backend
from tslearn.backend.numpy_backend import NumPyLinalg
linalg = NumPyLinalg()
# linalg.norm(tensor_with_grad) -> Fails or breaks computation graph

# CORRECT: Dynamically resolving the backend to support both NumPy and PyTorch
from tslearn.backend import instantiate_backend
be = instantiate_backend(1, None, input_data)
linalg = be.linalg
# linalg.norm(input_data) -> Safely computes norm while preserving gradients if using PyTorch
```

## API Test: `NumPyRandom`

### Signature
```python
class NumPyRandom
```
_Source: tslearn/tslearn/backend/numpy_backend.py:132_

### Goal
A backend-specific helper class that encapsulates random number generation utilities for the NumPy computational backend in `tslearn`.

### Parameters
_None._

### Input
No arguments are required to instantiate this class. It is typically instantiated internally by the `NumPyBackend` to provide a unified random number generation interface.

### Output
Returns `unspecified` — an instance of the `NumPyRandom` class. (Note: Specific random generation methods attached to this class are not detailed in the provided API facts).

### Valid Call Patterns
```python
# Inferred from signature (no verbatim examples provided in context)
from tslearn.backend.numpy_backend import NumPyRandom

# Instantiate the NumPy random helper
np_random = NumPyRandom()

# Verify the instance type
assert isinstance(np_random, NumPyRandom), "Failed to instantiate NumPyRandom"
print(f"Successfully instantiated: {type(np_random).__name__}")
```

### LLM Instruction Prompt
- Do not pass any arguments when instantiating `NumPyRandom`.
- Recognize that this is a low-level backend helper class. In standard `tslearn` workflows, users typically do not instantiate this directly; instead, they access random utilities via the `.random` attribute of an instantiated backend object (e.g., from `instantiate_backend()`).
- Do not invent or assume specific method signatures on this class without verifying them against the active backend's capabilities.

### Prompt Snippet
```text
When working with tslearn's backend system, `NumPyRandom` is the class responsible for random operations under the NumPy backend. It takes no initialization parameters. Instantiate it directly via `NumPyRandom()` if explicitly required for low-level backend extensions.
```

### Common Failure Modes
- **Passing arguments to the constructor:** The `NumPyRandom` class signature accepts no parameters. Passing seeds or dimensions during instantiation will raise a `TypeError`.
- **Assuming PyTorch compatibility:** This class is strictly for the NumPy backend. If the active backend is PyTorch (e.g., for automatic differentiation with `soft_dtw`), the equivalent `PyTorchRandom` should be used instead.

### Fix Code Hint
```python
# BAD: Passing a seed or shape to the constructor
# rng = NumPyRandom(seed=42)

# GOOD: Instantiate without arguments (seeding is handled by backend methods, not the constructor)
from tslearn.backend.numpy_backend import NumPyRandom
rng = NumPyRandom()
```

## API Test: `NumPyTesting`

### Signature
```python
class NumPyTesting
```
_Source: tslearn/tslearn/backend/numpy_backend.py:139_

### Goal
Provides testing utilities and assertions for validating array operations and metric computations within the NumPy backend of `tslearn`.

### Parameters
_None._

### Input
Takes no arguments upon instantiation.

### Output
Returns `unspecified` — an instance of the `NumPyTesting` class containing backend-specific assertion methods (e.g., for checking array equality or closeness).

### Valid Call Patterns
```python
from tslearn.backend.numpy_backend import NumPyTesting

# Instantiate the testing utility (inferred from signature)
tester = NumPyTesting()

assert isinstance(tester, NumPyTesting), "Failed to instantiate NumPyTesting"
print("NumPyTesting instantiated successfully.")
```

### LLM Instruction Prompt
- Use `NumPyTesting` when you need to access NumPy-specific testing utilities within the `tslearn` backend framework.
- Instantiate the class without any arguments.
- Do not assume the presence of specific assertion methods unless verified, though it typically mirrors standard `numpy.testing` functionality for backend abstraction.

### Prompt Snippet
```text
from tslearn.backend.numpy_backend import NumPyTesting
tester = NumPyTesting()
```

### Common Failure Modes
- **Passing arguments during instantiation**: `NumPyTesting` takes no parameters. Passing configuration arguments or backend strings will raise a `TypeError`.

### Fix Code Hint
```python
# Incorrect: tester = NumPyTesting(backend="numpy")
# Correct:
tester = NumPyTesting()
```

## API Test: `OneD_SymbolicAggregateApproximation`

### Signature
```python
class OneD_SymbolicAggregateApproximation(SymbolicAggregateApproximation)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:530_

_Source doc:_ One-D Symbolic Aggregate approXimation (1d-SAX) transformation. 1d-SAX was originally presented in [1]_. Parameters ---------- n_segments : int (default: 1) Number of PAA segments to compute. alphabet_size_avg : int (default: 5) Number of SAX symbols to use to describe average values. alphabet_size_slope : int (default: 5) Number of SAX symbols to use to describe slopes. sigma_l : float or None (default: None) Scale parameter of the Gaussian distribution used to quantize slopes. If None, the formula given in [1]_ is used: :math:`\sigma_L = \sqrt{0.03 / L}` where :math:`L` is the length of each segment. scale: bool (default: False) Whether input data should be scaled for each feature of each time series to have zero mean and unit variance. Default for this parameter is set to `False` in version 0.4 to ensure backward compatibility, but is likely to change in a future version. Attributes ---------- breakpoints_avg_ : numpy.ndarray of shape (alphabet_size_avg - 1, ) List of breakpoints used to generate SAX symbols for average values. breakpoints_slope_ : numpy.ndarray of shape (alphabet_size_slope - 1, ) List of breakpoints used to generate SAX symbols for slopes. Notes ----- This method requires a dataset of equal-sized time series. Examples -------- >>> one_d_sax = OneD_SymbolicAggregateApproximation(n_segments=3, ...         alphabet_size_avg=2, alphabet_size_slope=2, sigma_l=1.) >>> data = [[-1., 2., 0.1, -1., 1., -1.], [1., 3.2, -1., -3., 1., -1.]] >>> one_d_sax_data = one_d_sax.fit_transform(data) >>> one_d_sax_data.shape (2, 3, 2) >>> one_d_sax_data array([[[1, 1], [0, 0], [1, 0]], <BLANKLINE> [[1, 1], [0, 0], [1, 0]]]) >>> one_d_sax.distance_sax(one_d_sax_data[0], one_d_sax_data[1]) 0.0 >>> one_d_sax.distance(data[0], data[1]) 0.0 >>> one_d_sax.inverse_transform(one_d_sax_data) array([[[ 0.33724488],

### Goal
Applies a One-D Symbolic Aggregate approXimation (1d-SAX) transformation to time-series data, quantizing both the average values and slopes of segments into discrete symbols.

### Parameters
_None._

### Input
Constructor arguments configure the transformation (e.g., `n_segments`, `alphabet_size_avg`, `alphabet_size_slope`, `sigma_l`, `scale`). When calling `.fit(X)` or `.transform(X)`, the input `X` must be a dataset of equal-sized time series, formatted as a strict 3D numpy array `(n_ts, max_sz, d)`. Variable-length time series (padded with `nan`) are not supported by this method.

### Output
Returns `unspecified` — an unfitted estimator instance of `OneD_SymbolicAggregateApproximation` that exposes scikit-learn compatible `fit`, `transform`, and `fit_transform` methods. The transformed output is a 3D array of shape `(n_ts, n_segments, 2)`, where the last dimension holds the average symbol and the slope symbol.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import OneD_SymbolicAggregateApproximation
from tslearn.utils import to_time_series_dataset

# 1. Instantiate the 1d-SAX transformer
one_d_sax = OneD_SymbolicAggregateApproximation(
    n_segments=3,
    alphabet_size_avg=2,
    alphabet_size_slope=2,
    sigma_l=1.0
)

# 2. Prepare equal-sized time series data
data = [[-1., 2., 0.1, -1., 1., -1.], [1., 3.2, -1., -3., 1., -1.]]
X = to_time_series_dataset(data)

# 3. Fit and transform the data
one_d_sax_data = one_d_sax.fit_transform(X)

# 4. Assert falsifiable properties
assert one_d_sax_data.shape == (2, 3, 2), "Output should have shape (n_ts, n_segments, 2)"
assert np.array_equal(one_d_sax_data[0], [[1, 1], [0, 0], [1, 0]])

# 5. Compute distance using the fitted estimator
dist = one_d_sax.distance(X[0], X[1])
assert isinstance(dist, float)
print(f"1d-SAX representation shape: {one_d_sax_data.shape}")
print(f"Distance between first two series: {dist}")
```

### LLM Instruction Prompt
- Instantiate the class with desired `n_segments`, `alphabet_size_avg`, and `alphabet_size_slope`.
- Ensure the input time-series dataset contains equal-sized series (no variable-length padding).
- Always call `.fit(X)` or `.fit_transform(X)` before attempting to compute distances with `.distance(ts1, ts2)`.
- The transformed output will have shape `(n_ts, n_segments, 2)`, where the last dimension contains the average symbol and the slope symbol.

### Prompt Snippet
```text
Use `tslearn.piecewise.OneD_SymbolicAggregateApproximation` to compute 1d-SAX representations. Ensure the input dataset consists of equal-sized time series formatted as a 3D array `(n_ts, max_sz, d)`. You must fit the estimator using `.fit(X)` before calling `.distance(ts1, ts2)`.
```

### Common Failure Modes
- **`NotFittedError`**: Attempting to call `.distance(ts1, ts2)` or `.transform(X)` before fitting the estimator with `.fit(X)`.
- **Incompatible Data**: Passing variable-length time series (containing `nan` padding), as 1d-SAX requires equal-sized time series.
- **Shape Errors**: Passing a 1D or 2D array instead of the required 3D array `(n_ts, max_sz, d)` to `.fit()` or `.transform()`.

### Fix Code Hint
```python
# WRONG: Calling distance on an unfitted estimator
one_d_sax = OneD_SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2, alphabet_size_slope=2)
dist = one_d_sax.distance(X[0], X[1])  # Raises NotFittedError

# CORRECT: Fit the estimator on the dataset first
one_d_sax.fit(X)
dist = one_d_sax.distance(X[0], X[1])
```

## API Test: `PatchingLayer`

### Signature
```python
class PatchingLayer(Layer)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:128_

_Source doc:_ Format data for processing with patches matching shapelets length and nans removal. # Input shape 3D tensor with shape: `(batch_size, steps, features)`. # Output shape 4D tensor with shape: `(batch_size, steps - shapelet_size, shapelet_length, features)`.

### Goal
Format 3D time-series data into 4D patches matching shapelet lengths and remove NaNs for shapelet-based learning.

### Parameters
_None._

### Input
A 3D tensor with shape `(batch_size, steps, features)`.

### Output
Returns `unspecified` — a 4D tensor with shape `(batch_size, steps - shapelet_size, shapelet_length, features)` representing the extracted patches.

### Valid Call Patterns
```python
from tslearn.shapelets import PatchingLayer

# Example inferred from signature (not verified)
layer = PatchingLayer()
assert layer.__class__.__name__ == "PatchingLayer"
print("PatchingLayer instantiated.")
```

### LLM Instruction Prompt
- Use `PatchingLayer` to format 3D time-series tensors into 4D patch tensors for shapelet processing.
- Do not pass any parameters to the constructor, as none are documented in the public signature.
- Ensure the input to the layer is a 3D tensor of shape `(batch_size, steps, features)`.

### Prompt Snippet
```text
`tslearn.shapelets.PatchingLayer` formats 3D time-series tensors `(batch_size, steps, features)` into 4D patch tensors `(batch_size, steps - shapelet_size, shapelet_length, features)` with NaN removal.
```

### Common Failure Modes
- Passing a 2D array instead of the required 3D tensor `(batch_size, steps, features)`.
- Providing parameters to the constructor when none are accepted in the signature.

### Fix Code Hint
```python
from tslearn.shapelets import PatchingLayer

# Instantiate without arguments as per the signature
layer = PatchingLayer()
```

## API Test: `PiecewiseAggregateApproximation`

### Signature
```python
class PiecewiseAggregateApproximation(TimeSeriesMixin, TransformerMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:61_

_Source doc:_ Piecewise Aggregate Approximation (PAA) transformation. PAA was originally presented in [1]_. Parameters ---------- n_segments : int (default: 1) Number of PAA segments to compute Notes ----- This method requires a dataset of equal-sized time series. Examples -------- >>> paa = PiecewiseAggregateApproximation(n_segments=3) >>> data = [[-1., 2., 0.1, -1., 1., -1.], [1., 3.2, -1., -3., 1., -1.]] >>> paa_data = paa.fit_transform(data) >>> paa_data.shape (2, 3, 1) >>> paa_data array([[[ 0.5 ], [-0.45], [ 0.  ]], <BLANKLINE> [[ 2.1 ], [-2.  ], [ 0.  ]]]) >>> float(paa.distance_paa(paa_data[0], paa_data[1]))  # doctest: +ELLIPSIS 3.15039... >>> float(paa.distance(data[0], data[1]))  # doctest: +ELLIPSIS 3.15039... >>> paa.inverse_transform(paa_data) array([[[ 0.5 ], [ 0.5 ], [-0.45], [-0.45], [ 0.  ], [ 0.  ]], <BLANKLINE> [[ 2.1 ], [ 2.1 ], [-2.  ], [-2.  ], [ 0.  ], [ 0.  ]]]) References ---------- .. [1] E. Keogh & M. Pazzani. Scaling up dynamic time warping for datamining applications. SIGKDD 2000, pp. 285--289.

### Goal
Reduces the dimensionality of time-series datasets by dividing them into equal-sized segments and computing the mean value for each segment (Piecewise Aggregate Approximation).

### Parameters
_None._

### Input
- **Constructor Arguments:** Accepts `n_segments` (int, default: 1) to specify the target number of PAA segments to compute.
- **Data (`X`):** A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time-series dataset. 
- **Preconditions:** The dataset *must* consist of equal-sized time series. Variable-length time series padded with `nan` values are not supported by this specific transformation.

### Output
Returns `unspecified` — represents the instantiated estimator object. When calling `.fit_transform(X)`, it returns a 3D NumPy array of shape `(n_ts, n_segments, d)` containing the PAA-transformed time series. When calling `.distance(x1, x2)` or `.distance_paa(paa1, paa2)`, it returns a scalar float representing the distance.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PiecewiseAggregateApproximation
from sklearn.exceptions import NotFittedError

# 1. Initialize the PAA transformer
paa = PiecewiseAggregateApproximation(n_segments=3)

# 2. Prepare equal-sized 3D time-series data: (n_ts, max_sz, d)
# 2 time series, 6 time steps, 1 dimension
X = np.array([[[-1.], [ 2. ], [ 0.1], [-1.], [ 1.], [-1.]],
              [[ 1.], [ 3.2], [-1. ], [-3.], [ 1.], [-1.]]])

# 3. Verify NotFittedError is raised if distance is called before fitting
try:
    paa.distance(X[0], X[1])
    raise AssertionError("Should have raised NotFittedError")
except NotFittedError:
    pass

# 4. Fit and transform the data
X_paa = paa.fit_transform(X)

# 5. Assertions on the transformed shape and values
assert X_paa.shape == (2, 3, 1), f"Expected shape (2, 3, 1), got {X_paa.shape}"
# The first segment of the first time series is the mean of [-1.0, 2.0] -> 0.5
assert np.isclose(X_paa[0, 0, 0], 0.5)

# 6. Compute distances using the fitted estimator
dist = paa.distance(X[0], X[1])
dist_paa = paa.distance_paa(X_paa[0], X_paa[1])
assert np.isclose(dist, dist_paa)

print(f"PAA transform successful. Output shape: {X_paa.shape}, Distance: {dist:.4f}")
```

### LLM Instruction Prompt
- Always format input data into the strict 3D `(n_ts, max_sz, d)` NumPy array structure before passing it to `fit` or `fit_transform`.
- Ensure the dataset contains only equal-sized time series; PAA does not support variable-length series padded with `nan`.
- Pass `n_segments` during initialization to define the target dimensionality.
- You must call `.fit()` or `.fit_transform()` on the dataset before attempting to use `.distance()` or `.inverse_transform()`, otherwise a `NotFittedError` will be raised.

### Prompt Snippet
```text
Use `tslearn.piecewise.PiecewiseAggregateApproximation` to reduce the dimensionality of the time-series dataset `X` to 10 segments. Ensure `X` is a 3D array of equal-sized series. Fit the model and transform the data, then compute the PAA distance between the first two original time series in `X`.
```

### Common Failure Modes
- **`NotFittedError` on Distance Calculation:** Calling `paa.distance(x1, x2)` before calling `paa.fit(X)` will fail because the estimator needs to learn the segment sizes from the training data's `max_sz`.
- **Incorrect Input Dimensions:** Passing a 1D list or 2D array instead of the required 3D `(n_ts, max_sz, d)` array will cause shape mismatch errors during transformation.
- **Variable-Length Time Series:** Passing a dataset containing `nan` padding (variable-length series) violates the equal-sized precondition and will result in `nan` values propagating through the segment means.

### Fix Code Hint
```python
# BAD: Calling distance before fitting, or using 2D arrays
paa = PiecewiseAggregateApproximation(n_segments=5)
# paa.distance(ts1, ts2)  # Raises NotFittedError

# GOOD: Format to 3D, fit first, then compute distance
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw) # Ensures (n_ts, max_sz, d)
X_paa = paa.fit_transform(X_3d)
dist = paa.distance(X_3d[0], X_3d[1]) # Now safe to call
```

## API Test: `PyTorchBackend`

### Signature
```python
class PyTorchBackend
class PyTorchBackend(object)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:29  (+1 more definition site/overload)_

### Goal
Instantiates the PyTorch backend utility class, which provides tensor operations and automatic differentiation capabilities for time-series metrics.

### Parameters
_None._

### Input
No arguments are required to instantiate the class. The local environment must have the `pytorch` package installed to successfully utilize this backend's methods.

### Output
Returns `unspecified` — an instance of the `PyTorchBackend` class, which acts as a namespace/utility object providing PyTorch-specific implementations of array and mathematical operations.

### Valid Call Patterns
```python
# Inferred from signature (not verified in existing tests)
from tslearn.backend import PyTorchBackend

# Instantiate the backend directly (takes no arguments)
pytorch_be = PyTorchBackend()

# Verify instantiation
assert pytorch_be.__class__.__name__ == "PyTorchBackend"
print(f"Successfully instantiated: {type(pytorch_be)}")
```

### LLM Instruction Prompt
- Call `PyTorchBackend()` with exactly zero arguments.
- Note that in typical `tslearn` workflows, users do not need to instantiate this class directly; instead, they should use `tslearn.backend.instantiate_backend(..., "pytorch")` or pass `be="pytorch"` directly to metric functions (like `soft_dtw`) to auto-resolve the backend.
- Ensure `torch` is installed in the environment before attempting to use PyTorch backend features, as it is a strict precondition for automatic differentiation.

### Prompt Snippet
```text
`tslearn.backend.PyTorchBackend()` initializes the PyTorch backend for automatic differentiation and gradient computation. It takes no arguments. Typically accessed dynamically via `instantiate_backend` or by passing `be="pytorch"` to metric functions.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Providing strings (like `"pytorch"`) or configuration dictionaries to `PyTorchBackend()` will raise a `TypeError` because the constructor takes no arguments.
- **Missing PyTorch dependency:** Attempting to use the backend's tensor operations when the `pytorch` package is not installed locally will result in `ImportError` or fallback behaviors.

### Fix Code Hint
```python
# Incorrect: Passing a string identifier to the constructor
# be = PyTorchBackend("pytorch")

# Correct: Instantiate with no arguments
from tslearn.backend import PyTorchBackend
be = PyTorchBackend()

# Alternative (Preferred for dynamic workflows):
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
```

## API Test: `PyTorchLinalg`

### Signature
```python
class PyTorchLinalg
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:238_

### Goal
Acts as a linear algebra helper class for the PyTorch backend in `tslearn`, providing a namespace for matrix operations that mirrors NumPy's `linalg` module for automatic differentiation workflows.

### Parameters
_None._

### Input
No arguments are required to instantiate this class. The environment must have `pytorch` installed locally to successfully import and utilize the PyTorch backend components.

### Output
Returns `unspecified` — an instance of the `PyTorchLinalg` class, which exposes PyTorch-backed linear algebra methods used internally by `tslearn` metrics and alignments.

### Valid Call Patterns
```python
# Inferred from the signature (no verbatim examples found in documentation)
try:
    import torch
    from tslearn.backend.pytorch_backend import PyTorchLinalg
    
    # Instantiate the PyTorch linear algebra backend helper
    linalg_helper = PyTorchLinalg()
    
    # Assert it is correctly instantiated
    assert isinstance(linalg_helper, PyTorchLinalg)
    
    print(f"Successfully instantiated: {type(linalg_helper).__name__}")
except ImportError:
    print("PyTorch is not installed; skipping PyTorchLinalg test.")
```

### LLM Instruction Prompt
- When interacting with low-level `tslearn` backend internals, instantiate `PyTorchLinalg()` without any arguments.
- Ensure that `torch` is installed in the environment before attempting to import or use this class, as it is strictly tied to the PyTorch backend.
- Do not invent parameters for the constructor; it takes none.

### Prompt Snippet
```text
Use `tslearn.backend.pytorch_backend.PyTorchLinalg` to access PyTorch-specific linear algebra operations when extending or debugging `tslearn`'s automatic differentiation metrics. Instantiate it with `PyTorchLinalg()` (no arguments).
```

### Common Failure Modes
- **`TypeError: PyTorchLinalg() takes no arguments`**: Occurs if you attempt to pass configuration arguments or tensors directly to the constructor.
- **`ModuleNotFoundError: No module named 'torch'`**: Occurs if the PyTorch backend is invoked or imported in an environment where the `pytorch` package is not installed.

### Fix Code Hint
```python
# WRONG: Passing arguments to the constructor
# linalg = PyTorchLinalg(backend="pytorch")

# CORRECT: Instantiate without arguments
from tslearn.backend.pytorch_backend import PyTorchLinalg
linalg = PyTorchLinalg()
```

## API Test: `PyTorchRandom`

### Signature
```python
class PyTorchRandom
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:243_

### Goal
Provides a PyTorch-specific random number generator interface for the `tslearn` backend system, mirroring NumPy's random utilities.

### Parameters
_None._

### Input
No arguments are required for instantiation. The environment must have `torch` installed to use PyTorch backend components.

### Output
Returns `unspecified` — an instance of `PyTorchRandom` that serves as a random number generation namespace or utility for the PyTorch backend.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchRandom

# Inferred from signature (not verified)
rng = PyTorchRandom()

assert isinstance(rng, PyTorchRandom)
print("PyTorchRandom instantiated successfully.")
```

### LLM Instruction Prompt
- Use `PyTorchRandom` to access random number generation capabilities specifically tied to the PyTorch backend in `tslearn`.
- Do not pass any arguments to the constructor, as it takes no parameters.
- Ensure `torch` is installed in the environment before interacting with PyTorch backend helpers.
- Do not invent or call undocumented methods on the resulting instance.

### Prompt Snippet
```text
When working with the PyTorch backend in `tslearn`, use `PyTorchRandom()` to instantiate the backend-specific random number generator. It requires no initialization arguments.
```

### Common Failure Modes
- **Passing arguments to the constructor**: `PyTorchRandom` takes no parameters. Providing arguments will raise a `TypeError`.
- **Missing PyTorch dependency**: Attempting to import or use this class without `torch` installed will result in an `ImportError`.

### Fix Code Hint
```python
# Correct instantiation with no arguments
from tslearn.backend.pytorch_backend import PyTorchRandom

try:
    rng = PyTorchRandom()
except TypeError as e:
    print(f"Failed to instantiate: {e}")
```

## API Test: `PyTorchTesting`

### Signature
```python
class PyTorchTesting
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:263_

### Goal
Provides a low-level testing utility class for verifying PyTorch backend behaviors (such as automatic differentiation and tensor operations) in `tslearn`.

### Parameters
_None._

### Input
No inputs are required for instantiation. (Note: Specific testing methods and their preconditions are unspecified in the provided facts).

### Output
Returns `unspecified` — an instance of the `PyTorchTesting` class.

### Valid Call Patterns
```python
from tslearn.backend.pytorch_backend import PyTorchTesting

# Instantiate the testing utility class (inferred from signature)
tester = PyTorchTesting()

assert isinstance(tester, PyTorchTesting)
print("PyTorchTesting instantiated successfully.")
```

### LLM Instruction Prompt
- Instantiate `PyTorchTesting` without arguments.
- Recognize that this is a low-level backend helper primarily used for internal test suites (e.g., verifying PyTorch tensor gradients and metric computations) rather than standard time-series modeling workflows.
- Do not assume the existence of specific testing methods on this class, as they are not specified in the public API facts.

### Prompt Snippet
```text
To access PyTorch backend testing utilities in tslearn, instantiate the class without arguments:
```python
from tslearn.backend.pytorch_backend import PyTorchTesting
tester = PyTorchTesting()
```
```

### Common Failure Modes
- **Passing arguments to the constructor**: The `PyTorchTesting` class signature takes no parameters. Providing arguments will raise a `TypeError`.
- **Missing PyTorch dependency**: Because this is part of the PyTorch backend, the local environment must have the `pytorch` package installed, otherwise importing from `pytorch_backend` may fail.

### Fix Code Hint
```python
# BAD: Passing arguments to the constructor
# tester = PyTorchTesting(strict=True)

# GOOD: Instantiate without arguments
tester = PyTorchTesting()
```

## API Test: `SoftDTW`

### Signature
```python
class SoftDTW
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1068_

_Source doc:_ Soft Dynamic Time Warping

### Goal
Represents the Soft Dynamic Time Warping (Soft-DTW) metric class, used for computing differentiable alignments between time series.

### Parameters
_None._

### Input
No initialization parameters are documented in the authoritative API facts. If used as a PyTorch `autograd.Function` or similar backend helper, inputs to its methods (if any) are unknown.

### Output
Returns `unspecified` — an instance of the `SoftDTW` class.

### Valid Call Patterns
```python
from tslearn.metrics import SoftDTW

# Inferred from signature (no verified examples available)
def test_soft_dtw_instantiation():
    soft_dtw_instance = SoftDTW()
    assert isinstance(soft_dtw_instance, SoftDTW)
    print(f"Successfully instantiated: {type(soft_dtw_instance).__name__}")

test_soft_dtw_instantiation()
```

### LLM Instruction Prompt
- Do not invent initialization parameters for the `SoftDTW` class; the API facts list an empty parameter signature (`params: []`).
- Do not confuse the `SoftDTW` class with the `soft_dtw` function (which computes the metric and accepts arguments like `gamma` and `compute_with_backend`).
- Import `SoftDTW` explicitly from `tslearn.metrics`.

### Prompt Snippet
```text
When referencing the Soft-DTW class directly, use `SoftDTW()` without arguments as no parameters are documented. For computing the metric, prefer the `soft_dtw` function instead.
```

### Common Failure Modes
- **Inventing parameters:** Passing arguments (like `gamma` or `dataset`) to the `SoftDTW` class constructor will likely cause a `TypeError` since no parameters are defined in the signature.
- **Confusing class and function:** Attempting to use `SoftDTW` as a drop-in replacement for the `soft_dtw` function to compute distances directly on 3D `(n_ts, max_sz, d)` arrays.

### Fix Code Hint
```python
from tslearn.metrics import SoftDTW

# Instantiate the class exactly as defined by the signature (no arguments)
soft_dtw_metric = SoftDTW()
```

## API Test: `SoftDTWLossPyTorch`

### Signature
```python
class SoftDTWLossPyTorch(torch.nn.Module)
```
_Source: tslearn/tslearn/metrics/soft_dtw_loss_pytorch.py:22  (+1 more definition site/overload)_

### Goal
A PyTorch `nn.Module` that computes the differentiable Soft-DTW loss or Soft-DTW divergence between batches of time series, enabling automatic differentiation and gradient computation for neural network integration.

### Parameters
_None._

### Input
**Initialization Arguments:**
- `gamma` (float): Regularization parameter. Must be strictly positive. Lower values are less smoothed (closer to true hard-DTW).
- `normalize` (bool, default `False`): If `True`, computes the Soft-DTW divergence, which counteracts the non-positivity of Soft-DTW and is exactly 0 when $X = Y$.
- `dist_func` (callable, default `None`): Custom distance function supporting PyTorch automatic differentiation. Takes two arguments of shape `(batch_size, ts_length, dim)`. If `None`, the squared Euclidean distance is used.

**Call/Forward Arguments:**
- `x`, `y`: Two PyTorch tensors of shape `(batch_size, ts_length, dim)`. The time-series lengths can differ between `x` and `y`. To compute gradients, at least one input tensor must have `requires_grad=True`.

### Output
Returns `unspecified` — A 1D PyTorch tensor of shape `(batch_size,)` containing the computed Soft-DTW loss or divergence for each pair of time series in the batch. The tensor is attached to the PyTorch computation graph, allowing `.backward()` to compute gradients.

### Valid Call Patterns
```python
import torch
import tslearn.metrics

# 1. Prepare 3D PyTorch tensors (batch_size, length, dim)
b, m, n, d = 2, 5, 7, 3
batch_ts_1 = torch.zeros((b, m, d), requires_grad=True)
batch_ts_2 = torch.ones((b, n, d), requires_grad=True)

# 2. Instantiate the PyTorch loss module
soft_dtw_loss_pytorch = tslearn.metrics.SoftDTWLossPyTorch(
    gamma=1.0, 
    normalize=True, 
    dist_func=None
)

# 3. Compute the forward pass
loss = soft_dtw_loss_pytorch.forward(batch_ts_1, batch_ts_2)

# 4. Verify the output is a differentiable tensor
assert loss.shape == (b,)
assert loss.requires_grad is True
print(f"Computed Soft-DTW divergence: {loss.detach().numpy()}")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.SoftDTWLossPyTorch` to compute differentiable Soft-DTW loss or divergence within PyTorch neural networks.
- Instantiate the class with a strictly positive `gamma` and optionally `normalize=True`.
- Pass 3D PyTorch tensors `(batch_size, length, dim)` to the `.forward()` method.
- Do not pass NumPy arrays; this module strictly requires PyTorch tensors.

### Prompt Snippet
```text
`tslearn.metrics.SoftDTWLossPyTorch(gamma=1.0, normalize=False)` is a PyTorch `nn.Module` for computing differentiable Soft-DTW loss. Inputs to `forward(x, y)` must be 3D PyTorch tensors `(batch_size, length, dim)`. Set `normalize=True` for Soft-DTW divergence.
```

### Common Failure Modes
- **Incorrect Input Type:** Passing NumPy arrays instead of PyTorch tensors raises a PyTorch `TypeError`.
- **Incorrect Dimensionality:** Passing 2D tensors `(batch_size, length)` instead of the required 3D tensors `(batch_size, length, dim)` causes shape mismatch errors during distance computation.
- **Missing Gradients:** Forgetting to set `requires_grad=True` on the input tensors prevents `.backward()` from populating `.grad` attributes.
- **Zero Gamma:** Setting `gamma=0` is not supported by this soft-min implementation and will cause division by zero or `NaN` outputs.

### Fix Code Hint
```python
import torch
import tslearn.metrics

# Ensure inputs are 3D PyTorch tensors (batch_size, length, dim)
x = torch.tensor([[[1.0], [2.0]]], requires_grad=True)
y = torch.tensor([[[1.5], [2.5]]])

# Instantiate the PyTorch nn.Module
criterion = tslearn.metrics.SoftDTWLossPyTorch(gamma=1.0, normalize=True)

# Call forward with tensors
loss = criterion.forward(x, y)
loss.sum().backward()
```

## API Test: `SquaredEuclidean`

### Signature
```python
class SquaredEuclidean
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1176_

_Source doc:_ Squared Euclidean distance.

### Goal
Instantiate a metric object representing the squared Euclidean distance, typically used as a base point-wise metric for time-series alignment algorithms.

### Parameters
_None._

### Input
No arguments are required for instantiation.

### Output
Returns `unspecified` — an instance of the `SquaredEuclidean` class representing the distance metric.

### Valid Call Patterns
```python
# Inferred from signature (not verified by test suite or README examples)
from tslearn.metrics.softdtw_variants import SquaredEuclidean

# Instantiate the metric object
metric = SquaredEuclidean()
```

### LLM Instruction Prompt
- Instantiate `SquaredEuclidean` without any arguments.
- Do not pass time-series arrays directly to the class constructor; it is a metric object factory, not a direct distance function.

### Prompt Snippet
```text
from tslearn.metrics.softdtw_variants import SquaredEuclidean
sq_euclidean_metric = SquaredEuclidean()
```

### Common Failure Modes
- **Passing arrays to the constructor:** Attempting to compute the distance by passing time-series arrays directly to `SquaredEuclidean(ts1, ts2)` will fail because the constructor takes no parameters.

### Fix Code Hint
```python
# WRONG: Passing arrays directly to the constructor
# dist = SquaredEuclidean(ts1, ts2)

# RIGHT: Instantiate the metric object without arguments
metric = SquaredEuclidean()
```

## API Test: `SymbolicAggregateApproximation`

### Signature
```python
class SymbolicAggregateApproximation(PiecewiseAggregateApproximation)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:276_

_Source doc:_ Symbolic Aggregate approXimation (SAX) transformation. SAX was originally presented in [1]_. Parameters ---------- n_segments : int (default: 1) Number of PAA segments to compute alphabet_size_avg : int (default: 5) Number of SAX symbols to use scale: bool (default: False) Whether input data should be scaled for each feature to have zero mean and unit variance across the dataset passed at fit time. Default for this parameter is set to `False` in version 0.4 to ensure backward compatibility, but is likely to change in a future version. Attributes ---------- breakpoints_avg_ : numpy.ndarray of shape (alphabet_size - 1, ) List of breakpoints used to generate SAX symbols Notes ----- This method requires a dataset of equal-sized time series. Examples -------- >>> sax = SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2) >>> data = [[-1., 2., 0.1, -1., 1., -1.], [1., 3.2, -1., -3., 1., -1.]] >>> sax_data = sax.fit_transform(data) >>> sax_data.shape (2, 3, 1) >>> sax_data array([[[1], [0], [1]], <BLANKLINE> [[1], [0], [1]]]) >>> sax.distance_sax(sax_data[0], sax_data[1])  # doctest: +ELLIPSIS 0.0 >>> sax.distance(data[0], data[1])  # doctest: +ELLIPSIS 0.0 >>> sax.inverse_transform(sax_data) array([[[ 0.67448975], [ 0.67448975], [-0.67448975], [-0.67448975], [ 0.67448975], [ 0.67448975]], <BLANKLINE> [[ 0.67448975], [ 0.67448975], [-0.67448975], [-0.67448975], [ 0.67448975], [ 0.67448975]]])

### Goal
Transforms time-series data into a discrete symbolic representation (SAX) by first applying Piecewise Aggregate Approximation (PAA) and then mapping the segments to a finite alphabet of symbols.

### Parameters
_None._

### Input
- **Constructor Arguments**: 
  - `n_segments` (int, default: 1): The number of PAA segments to reduce the time series into.
  - `alphabet_size_avg` (int, default: 5): The number of discrete SAX symbols (bins) to use.
  - `scale` (bool, default: False): Whether to scale the input data to zero mean and unit variance across the dataset at fit time.
- **Data Preconditions**: Data passed to `.fit()` or `.fit_transform()` must be a dataset of **equal-sized** time series, formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)` (or a list of lists that can be converted to this shape). Variable-length time series are not supported by this method.

### Output
Returns `unspecified` — An unfitted `SymbolicAggregateApproximation` estimator instance. Once `.fit_transform(X)` is called, it returns a 3D `numpy.ndarray` of shape `(n_ts, n_segments, d)` containing integer values representing the SAX symbols.

### Valid Call Patterns
```python
from tslearn.piecewise import SymbolicAggregateApproximation
from tslearn.utils import to_time_series_dataset

# 1. Prepare a dataset of equal-sized time series
data = [[-1., 2., 0.1, -1., 1., -1.], 
        [1., 3.2, -1., -3., 1., -1.]]
X = to_time_series_dataset(data)

# 2. Instantiate the SAX transformer
sax = SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2, scale=False)

# 3. Fit and transform the data into SAX symbols
sax_data = sax.fit_transform(X)

# 4. Compute distances (requires the estimator to be fitted first)
dist_raw = sax.distance(X[0], X[1])
dist_sax = sax.distance_sax(sax_data[0], sax_data[1])

assert sax_data.shape == (2, 3, 1)
print(f"SAX representation shape: {sax_data.shape}")
print(f"Distance between raw series using SAX: {dist_raw}")
```

### LLM Instruction Prompt
- Use `tslearn.piecewise.SymbolicAggregateApproximation` to discretize time series into symbolic representations.
- Ensure the input dataset consists strictly of equal-sized time series; variable-length series padded with `nan` will cause errors or invalid outputs.
- Always call `.fit(X)` or `.fit_transform(X)` before attempting to use `.distance()` or `.distance_sax()`, otherwise a `NotFittedError` will be raised.
- The output of `.fit_transform()` is a 3D array of integers of shape `(n_ts, n_segments, d)`.

### Prompt Snippet
```text
Use `tslearn.piecewise.SymbolicAggregateApproximation` to convert equal-sized time series into symbolic representations (SAX). Instantiate with `n_segments` and `alphabet_size_avg`. You must fit the model with `.fit()` or `.fit_transform()` before calling `.distance()` or `.distance_sax()` to avoid a `NotFittedError`.
```

### Common Failure Modes
- **`NotFittedError`**: Calling `.distance(ts1, ts2)` or `.distance_sax(sax1, sax2)` on an unfitted estimator instance.
- **Variable-Length Data**: Passing a dataset with variable-length time series (which `tslearn` pads with `nan` values). SAX requires all time series to be of equal length; `nan` values will propagate and ruin the PAA segment calculations.
- **Incorrect Output Expectations**: Assuming `.fit_transform()` returns a 2D array or strings. It returns a 3D `numpy` array of integers representing the symbol indices.

### Fix Code Hint
```python
# WRONG: Calling distance before fitting the estimator
sax = SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2)
dist = sax.distance(X[0], X[1])  # Raises NotFittedError

# CORRECT: Fit the estimator on the dataset first
sax = SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2)
sax.fit(X)
dist = sax.distance(X[0], X[1])  # Now succeeds
```

## API Test: `TimeSeriesCentroidBasedClusteringMixin`

### Signature
```python
class TimeSeriesCentroidBasedClusteringMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/clustering/utils.py:225_

_Source doc:_ Mixin class for centroid-based clustering of time series.

### Goal
Provides a mixin class for centroid-based clustering of time series, intended to be inherited by custom or internal clustering estimators to share common centroid-related functionality.

### Parameters
_None._

### Input
As a mixin class, it is not instantiated directly and takes no direct data inputs. It is designed to be inherited by clustering estimator classes. Child classes implementing the actual clustering logic will typically expect time-series datasets formatted as 3D `numpy` arrays of shape `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — acts as a base class providing inherited methods and properties for centroid-based clustering models.

### Valid Call Patterns
```python
from tslearn.clustering.utils import TimeSeriesCentroidBasedClusteringMixin

# Inferred from signature: Mixins are meant to be inherited by custom estimators
class CustomCentroidClustering(TimeSeriesCentroidBasedClusteringMixin):
    def __init__(self):
        self.cluster_centers_ = None
        
    def fit(self, X, y=None):
        # Custom clustering logic would go here
        return self

# Instantiate the custom child class
estimator = CustomCentroidClustering()

# Assert the inheritance property
assert isinstance(estimator, TimeSeriesCentroidBasedClusteringMixin)
print("Successfully instantiated a class inheriting from TimeSeriesCentroidBasedClusteringMixin.")
```

### LLM Instruction Prompt
- Do not instantiate `TimeSeriesCentroidBasedClusteringMixin` directly to perform clustering.
- Use this mixin strictly as a base class when developing custom centroid-based time-series clustering estimators to ensure architectural compatibility with `tslearn` and `scikit-learn`.
- Ensure that any child class inheriting from this mixin implements standard estimator methods like `fit()` and `predict()`, and handles the strict 3D array format `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
When building custom centroid-based time-series clustering estimators in tslearn, inherit from `tslearn.clustering.utils.TimeSeriesCentroidBasedClusteringMixin` to ensure compatibility with the toolkit's clustering utilities. Do not instantiate the mixin directly.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate the mixin directly and calling `.fit()` or `.predict()` on it. It lacks the concrete implementation of a clustering algorithm (like K-Means or K-Shape) and will fail.
- **Missing Estimator Methods:** Inheriting from the mixin but failing to implement the required `scikit-learn` compatible methods (`fit`, `predict`, `fit_predict`) in the child class.
- **Incorrect Data Dimensions in Child Classes:** Passing 1D or 2D arrays to the child estimator's `fit` method instead of the strictly required 3D `(n_ts, max_sz, d)` format.

### Fix Code Hint
```python
# WRONG: Do not instantiate the mixin directly
# model = TimeSeriesCentroidBasedClusteringMixin()
# model.fit(X)

# CORRECT: Inherit from the mixin to build a custom estimator
from tslearn.clustering.utils import TimeSeriesCentroidBasedClusteringMixin
from sklearn.base import BaseEstimator, ClusterMixin

class MyTimeSeriesKMeans(TimeSeriesCentroidBasedClusteringMixin, ClusterMixin, BaseEstimator):
    def fit(self, X, y=None):
        # Implement 3D array validation and centroid-based clustering logic here
        return self
```

## API Test: `TimeSeriesDBSCAN`

### Signature
```python
class TimeSeriesDBSCAN(TimeSeriesMixin, ClusterMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/clustering/dbscan.py:19_

_Source doc:_ DBSCAN clustering for time series. Parameters ---------- eps : float (default: 0.5) The maximum distance between two time series for one to be considered as in the neighborhood of the other. min_ts : int (default: 5) The number of time series (including itself) in a neighborhood for a time series to be considered as a core point. metric: {'dtw', 'ctw', 'frechet', 'euclidean', 'precomputed'} (default: 'dtw') Metric to be used for similarity measure between time series. metric_params : dict (default: None) Additional keyword arguments to pass to the metric function. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` key passed in `metric_params` is overridden by the `n_jobs` argument. Parameters that do not match the metric computation function signature are ignored. n_jobs : int or None (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`_ for more details. Attributes ---------- core_ts_indices_ : numpy.ndarray of shape (n_core_ts). Indices of core time series. components_: numpy.ndarray of shape (n_core_ts, sz, d) Copy of each core time series found by training. labels_ : numpy.ndarray of integers with shape (n_ts). Labels of each time series. Noisy time series are given the label -1. n_features_in_ : int Number of features seen during training. Notes ----- If `metric` is set to `"euclidean"`, the algorithm expects a dataset of equal-sized time series. Examples -------- >>> from tslearn.generators import random_walk_blobs >>> from tslearn.preprocessing import TimeSeriesScalerMeanVariance >>> X, y = random_walk_blobs(n_ts_per_blob=20, sz=32, d=2, n_blobs=4, random_state=0) >>> X = TimeSeriesScalerMeanVariance(mu=0., std=1.).fit_transform(X) >>> db = TimeSeriesDBSCAN(eps=4, min_ts=3).fit(X) >>> np.unique(db.labels_) # Clusters and noise array([-1,  0,  1,  2,  3]) >>> list(db.labels_).count(-1) # Nb noisy elements 37

### Goal
Perform Density-Based Spatial Clustering of Applications with Noise (DBSCAN) on time-series datasets using specialized alignment metrics like DTW.

### Parameters
_None._

### Input
- For `.fit(X)`: `X` must be a 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time-series dataset.
- If `metric="precomputed"`, `X` must instead be a 2D NumPy array of shape `(n_ts, n_ts)` containing precomputed cross-distances.
- If `metric="euclidean"`, the dataset must consist of equal-sized time series (no variable-length padding).
- Data should be formatted using `tslearn.utils.to_time_series_dataset` prior to fitting.

### Output
Returns `unspecified` — The fitted `TimeSeriesDBSCAN` estimator instance (`self`). After calling `.fit()`, it exposes attributes such as `labels_` (cluster assignments, with `-1` for noise), `components_` (copies of core time series), and `core_ts_indices_` (indices of core points).

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import TimeSeriesDBSCAN
from tslearn.utils import to_time_series_dataset

# 1. Create a small deterministic dataset of 6 time series
X_raw = np.vstack((
    np.eye(3).reshape(-1, 3),
    -1 * np.eye(3).reshape(-1, 3)
))
X_raw = np.insert(X_raw, 0, 0, axis=1)
X_raw = np.append(X_raw, np.zeros((X_raw.shape[0], 1)), axis=1)

# 2. Format to strict 3D shape (6, 5, 1)
X = to_time_series_dataset(X_raw)

# 3. Initialize and fit DBSCAN
db = TimeSeriesDBSCAN(eps=1e-6, min_ts=3, metric='dtw')
db.fit(X)

# 4. Verify clustering results
assert len(db.labels_) == 6
assert -1 not in db.labels_  # In this specific deterministic setup, there is no noise
print(f"Cluster labels: {db.labels_}")
print(f"Core TS indices: {db.core_ts_indices_}")
```

### LLM Instruction Prompt
- Always format the input dataset into a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before calling `.fit()`, unless using `metric="precomputed"`.
- Only use supported metrics: `'dtw'`, `'ctw'`, `'frechet'`, `'euclidean'`, or `'precomputed'`. Do not use `'gak'`.
- Remember that DBSCAN does not have a `.predict()` method for new data; cluster assignments for the training data are accessed via the `.labels_` attribute after fitting.
- Noise points are assigned a label of `-1`.

### Prompt Snippet
```text
Use `TimeSeriesDBSCAN` to cluster the time-series data. Ensure the data is converted to a 3D array first. Use DTW as the metric, set `eps` to 2.5, and `min_ts` to 3. Print the number of noise points found.
```

### Common Failure Modes
- **ValueError on invalid metric**: Passing an unsupported metric like `'gak'` directly to the `metric` parameter will raise a `ValueError: Metric must be one of...`.
- **Shape mismatch**: Passing a 2D array of time series directly to `.fit()` without converting it to the required 3D shape `(n_ts, max_sz, d)` (unless `metric='precomputed'`).
- **Variable-length data with Euclidean metric**: Using `metric='euclidean'` on a dataset containing variable-length time series (padded with NaNs) will lead to unexpected behavior or errors, as Euclidean distance requires equal-sized series.

### Fix Code Hint
```python
# WRONG: Passing 2D array or invalid metric
db = TimeSeriesDBSCAN(eps=0.5, min_ts=2, metric='gak')
db.fit(X_2d)

# RIGHT: Convert to 3D array and use a valid metric
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_2d)
db = TimeSeriesDBSCAN(eps=0.5, min_ts=2, metric='dtw')
db.fit(X_3d)
labels = db.labels_
```

## API Test: `TimeSeriesFeatureSynchronizer`

### Signature
```python
class TimeSeriesFeatureSynchronizer(TimeSeriesMixin, TransformerMixin, BaseEstimator)
```
_Source: tslearn/tslearn/preprocessing/_synchronizer.py:12_

_Source doc:_ Feature synchronizer for time series. Synchronizes features of each time series of a dataset to deal with: * acquisition at different sampling rates: linear interpolation is performed to match the sampling rate of the reference feature * desynchronized timestamps: linear interpolation is performed to match the temporal grid of the reference feature Parameters ---------- reference_feature_index : int (default: 0) The feature that is used as reference for synchronization among each time series. Examples -------- >>> data = [ ...    [[1, 2], [2, np.nan]], ...    [[1, 2], [np.nan, 3]], ... ] >>> TimeSeriesFeatureSynchronizer().fit_transform(data) array([[[ 1.,  2.], [ 2.,  2.]], <BLANKLINE> [[ 1.,  2.], [nan, nan]]]) >>> data = [[[1, 2], [2, 4] , [9, np.nan]]] >>> timestamps = np.array([ ...    [np.array(["2025-01-01", "2025-01-02"], dtype='datetime64'), ...     np.array(["2025-01-03", "2025-01-07"], dtype='datetime64'), ...     np.array(["2025-01-10", "nat"], dtype='datetime64')], ... ]) >>> TimeSeriesFeatureSynchronizer().fit_transform(data, timestamps=timestamps) array([[[1. , 2. ], [2. , 2.4], [9. , 4. ]]])

### Goal
Synchronizes features of each time series in a dataset by performing linear interpolation to match the sampling rate or temporal grid of a reference feature.

### Parameters
_None._

### Input
- **`X`**: A time-series dataset, provided as a list of lists or a 3D NumPy array of shape `(n_ts, max_sz, d)`.
- **`timestamps`** (optional, passed to `fit_transform`): A NumPy array of `datetime64` arrays representing the temporal grid for each feature.
- **Preconditions**: If `timestamps` are provided, they must be monotonically increasing for each feature. The reference feature index defaults to `0` but can be modified via the `reference_feature_index` attribute.

### Output
Returns `unspecified` — A transformed 3D NumPy array of shape `(n_ts, new_max_sz, d)` where all features have been linearly interpolated to align with the reference feature's temporal grid.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesFeatureSynchronizer

# 1. Basic synchronization without explicit timestamps
synchronizer = TimeSeriesFeatureSynchronizer()
data = [
    [[1, 2], [2, np.nan]],
    [[1, 2], [np.nan, 3]],
]
transformed = synchronizer.fit_transform(data)
assert transformed.shape == (2, 2, 2)
print("Synchronized without timestamps:\n", transformed)

# 2. Synchronization with explicit datetime64 timestamps
data_ts = [[[1, 2], [2, 4], [9, np.nan]]]
timestamps = np.array([
    [np.array(["2025-01-01", "2025-01-02"], dtype='datetime64'),
     np.array(["2025-01-03", "2025-01-07"], dtype='datetime64'),
     np.array(["2025-01-10", "nat"], dtype='datetime64')],
], dtype=object)

transformed_ts = synchronizer.fit_transform(data_ts, timestamps=timestamps)
assert transformed_ts.shape == (1, 3, 2)
print("Synchronized with timestamps:\n", transformed_ts)
```

### LLM Instruction Prompt
- Use `TimeSeriesFeatureSynchronizer` to align multi-dimensional time series features that were sampled at different rates or have desynchronized timestamps.
- Call `.fit_transform(X)` or `.fit_transform(X, timestamps=...)` to perform the synchronization.
- If the data has explicit temporal grids, pass them via the `timestamps` keyword argument to `fit_transform`.
- Ensure that any provided `timestamps` arrays are strictly monotonically increasing; otherwise, a `ValueError` will be raised.
- To change the reference feature from the default (index `0`), set the `reference_feature_index` attribute on the instantiated synchronizer before calling `fit_transform`.

### Prompt Snippet
```text
from tslearn.preprocessing import TimeSeriesFeatureSynchronizer
synchronizer = TimeSeriesFeatureSynchronizer()
synchronizer.reference_feature_index = 1  # Optional: change reference feature
X_sync = synchronizer.fit_transform(X, timestamps=my_timestamps)
```

### Common Failure Modes
- **Non-increasing timestamps**: Passing a `timestamps` array where the dates go backwards (e.g., `"2025-01-03"` followed by `"2024-01-04"`) will raise a `ValueError`.
- **Incorrect data shape**: Failing to provide data that can be parsed into the strict `(n_ts, max_sz, d)` 3D array format expected by `tslearn` estimators.

### Fix Code Hint
```python
# ERROR: ValueError raised due to non-increasing timestamps
# timestamps = np.array([[np.array(["2025-01-03", "2024-01-04"], dtype='datetime64')]])

# FIX: Ensure all timestamp arrays are monotonically increasing
timestamps = np.array([
    [np.array(["2025-01-01", "2025-01-02"], dtype='datetime64'),
     np.array(["2025-01-03", "2025-01-04"], dtype='datetime64'), # Fixed order
     np.array(["2025-01-05", "nat"], dtype='datetime64')],
], dtype=object)
transformed = synchronizer.fit_transform(data, timestamps=timestamps)
```

## API Test: `TimeSeriesImputer`

### Signature
```python
class TimeSeriesImputer(TimeSeriesMixin, TransformerMixin, BaseEstimator)
```
_Source: tslearn/tslearn/preprocessing/preprocessing.py:422_

_Source doc:_ Missing value imputer for time series. Missing values (nans) are replaced according to the chosen imputation method. There might be cases where the computation of missing values is impossible, in which case they are left unchanged (ex: mean of all nans, ffill for the first value... ). The imputer can be configured so that trailing 'empty' samples (nans for all features) are unprocessed by setting the `keep_trailing_nans` parameter to `True`. This might be handy when dealing with variable length time series datasets formatted with :ref:`to_time_series_dataset <fun-tslearn.utils.to_time_series_dataset>`, where time series are padded with 'empty' samples to match the length of the longest time serie. This option aims at preserving the variable length nature of the input dataset. Time series are processed sequentially by the :func:`~transform` and :func:`~fit_transform` methods, and gathered using :ref:`to_time_series_dataset <fun-tslearn.utils.to_time_series_dataset>`, effectively padding if needed. Parameters ---------- method : {'mean', 'median', 'ffill', 'bfill', 'linear', 'constant', Callable}(default: 'mean') The method used to compute missing values. When using linear imputation, starting nans will be replaced with first non-null value and ending nans will be replaced with last non-null value ( except for 'empty' samples when `keep_trailing_nans` set to `True`). When using a Callable, the function should take an array-like representing a timeseries with missing values as input parameter and should return the transformed timeseries. value: float (default: nan) The value to replace missing values with. Only used when method is `constant`. keep_trailing_nans: bool (default: True) Whether trailing samples with nans on all dimensions should be considered padding for variable length time series and kept unprocessed. When set to `False` , trailing 'empty' samples  will be imputed. Notes ----- This method allows datasets of variable lenght time series. While most missing values should be replaced, there might still be nan values in the resulting dataset representing padding when used with variable length time series, or uncomputable data. Examples -------- >>> TimeSeriesImputer().fit_transform([[0, numpy.nan, 6]]) array([[[0.], [3.], [6.]]]) >>> # Dealing with variable length dataset >>> TimeSeriesImputer().fit_transform([[numpy.nan, 3, 6], [numpy.nan, 3]]) array([[[4.5], [3. ], [6. ]], <BLANKLINE>

### Goal
Replaces missing values (`nan`) in time-series datasets using statistical or interpolation methods, while optionally preserving trailing `nan`s that represent variable-length padding.

### Parameters
_None._

### Input
*   **Constructor Arguments:** While the class signature takes no positional arguments, it accepts configuration kwargs: `method` (string like `'mean'`, `'median'`, `'ffill'`, `'bfill'`, `'linear'`, `'constant'`, or a Callable; defaults to `'mean'`), `value` (float, used if method is `'constant'`), and `keep_trailing_nans` (bool, defaults to `True`).
*   **Data (`X`):** Passed to `.fit()`, `.transform()`, or `.fit_transform()`. Must be a time-series dataset, typically a 3D NumPy array of shape `(n_ts, max_sz, d)` or a list of variable-length lists that `tslearn` can internally convert to the strict 3D format.
*   **Preconditions:** The input data must contain numeric values and `numpy.nan` for missing entries.

### Output
Returns `unspecified` — Calling `.fit_transform(X)` or `.transform(X)` returns a 3D NumPy array of shape `(n_ts, max_sz, d)` representing the imputed time-series dataset. Calling `.fit(X)` returns the fitted `TimeSeriesImputer` instance itself.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesImputer

# Dataset with missing values and variable lengths
univariate_dataset = [
    [1.0, np.nan, 3.0],
    [1.0, 2.0, np.nan, 9.0]
]

# Initialize imputer with a specific method and padding preservation
imputer = TimeSeriesImputer(method="mean", keep_trailing_nans=True)

# Fit and transform the dataset into a strict 3D array (n_ts, max_sz, d)
transformed = imputer.fit_transform(univariate_dataset)

# The first series is padded to length 4. The trailing NaN is kept.
# The internal NaN in the first series is replaced by the mean of [1.0, 3.0] = 2.0
expected_first_series = np.array([[1.0], [2.0], [3.0], [np.nan]])

assert transformed.shape == (2, 4, 1), f"Expected shape (2, 4, 1), got {transformed.shape}"
np.testing.assert_array_equal(transformed[0], expected_first_series)
print("Imputation successful, trailing padding preserved.")
```

### LLM Instruction Prompt
- Use `TimeSeriesImputer` to handle missing data (`numpy.nan`) in time-series datasets before passing them to distance metrics or estimators.
- Always instantiate the class first (e.g., `imputer = TimeSeriesImputer(method='mean')`), then call `.fit_transform(X)`.
- Remember that `tslearn` pads variable-length time series with `nan`s. By default, `TimeSeriesImputer(keep_trailing_nans=True)` preserves these trailing `nan`s so that the variable-length nature of the dataset is maintained. If you want to impute *all* `nan`s including padding, explicitly set `keep_trailing_nans=False`.
- Supported `method` strings include `'mean'`, `'median'`, `'ffill'`, `'bfill'`, `'linear'`, and `'constant'`.

### Prompt Snippet
```text
Use `tslearn.preprocessing.TimeSeriesImputer` to replace missing values in the time-series data. Configure it to use linear interpolation but ensure that trailing NaNs (which act as padding for variable-length series) are left untouched. Apply it to `X_raw` to produce `X_imputed`.
```

### Common Failure Modes
- **Unexpected Trailing NaNs:** Users might expect `.fit_transform()` to remove all `nan` values, but if the input has variable lengths, the output will still contain trailing `nan`s because `keep_trailing_nans=True` is the default.
- **Uncomputable Imputations:** If a time series consists entirely of `nan`s, or if `'ffill'` is used but the first value is `nan`, those specific `nan`s cannot be computed and will remain in the output array.
- **Incorrect Input Dimensions:** Passing a 1D array directly without wrapping it in a list or reshaping it to 3D may cause unexpected broadcasting or formatting errors during transformation.

### Fix Code Hint
```python
# BAD: Assuming all NaNs are removed, which breaks if variable-length padding is present
imputer = TimeSeriesImputer()
X_clean = imputer.fit_transform(X_variable_length)
assert not np.isnan(X_clean).any() # This will fail due to trailing padding NaNs

# GOOD: Acknowledge padding NaNs, or explicitly disable keeping them if strictly required
imputer = TimeSeriesImputer(keep_trailing_nans=False)
X_clean = imputer.fit_transform(X_variable_length)
# Now X_clean has no NaNs, but variable-length structure is lost (padded with imputed values)
```

## API Test: `TimeSeriesKMeans`

### Signature
```python
class TimeSeriesKMeans(TimeSeriesCentroidBasedClusteringMixin, TransformerMixin, ClusterMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/clustering/kmeans.py:476_

_Source doc:_ K-means clustering for time-series data. Parameters ---------- n_clusters : int (default: 3) Number of clusters to form. max_iter : int (default: 50) Maximum number of iterations of the k-means algorithm for a single run. tol : float (default: 1e-6) Inertia variation threshold. If at some point, inertia varies less than this threshold between two consecutive iterations, the model is considered to have converged and the algorithm stops. n_init : int (default: 1) Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia. metric : {"euclidean", "dtw", "softdtw"} (default: "euclidean") Metric to be used for both cluster assignment and barycenter computation. If "dtw", DBA is used for barycenter computation. max_iter_barycenter : int (default: 100) Number of iterations for the barycenter computation process. Only used if `metric="dtw"` or `metric="softdtw"`. metric_params : dict or None (default: None) Parameter values for the chosen metric. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` key passed in `metric_params` is overridden by the `n_jobs` argument. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`_ for more details. dtw_inertia: bool (default: False) Whether to compute DTW inertia even if DTW is not the chosen metric. verbose : int (default: 0) If nonzero, print information about the inertia while learning the model and joblib progress messages are printed. random_state : integer or numpy.RandomState, optional Generator used to initialize the centers. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. init : {'k-means++', 'random' or an ndarray} (default: 'k-means++') Method for initialization:

### Goal
Perform K-means clustering on time-series datasets using specialized time-series distance metrics (Euclidean, DTW, or Soft-DTW) and their corresponding barycenter computations.

### Parameters
_None._

### Input
The constructor accepts hyperparameters to configure the clustering algorithm, including `n_clusters` (int), `metric` (string: `"euclidean"`, `"dtw"`, or `"softdtw"`), `max_iter` (int), `dtw_inertia` (bool), and `random_state`. 

When calling `.fit()`, `.predict()`, or `.fit_predict()` on the instantiated model, the input data **must** be a 3D NumPy array of shape `(n_ts, max_sz, d)`, representing the number of time series, the maximum sequence length, and the number of dimensions, respectively.

### Output
Returns `unspecified` — A fitted `TimeSeriesKMeans` estimator instance (following scikit-learn conventions) that exposes attributes such as `.labels_` (cluster assignments for the training data), `.cluster_centers_` (the computed barycenters of shape `(n_clusters, max_sz, d)`), and `.inertia_` (the sum of squared distances to the closest cluster center).

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import TimeSeriesKMeans

# 1. Prepare deterministic 3D time-series data (n_ts=15, max_sz=10, d=3)
n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
time_series = rng.randn(n, sz, d)

# 2. Instantiate and fit the TimeSeriesKMeans model
km = TimeSeriesKMeans(
    n_clusters=3, 
    metric="euclidean", 
    max_iter=5,
    verbose=False, 
    random_state=rng
).fit(time_series)

# 3. Inspect the results
assert km.labels_.shape == (15,)
assert km.cluster_centers_.shape == (3, 10, 3)
print(f"Cluster labels: {km.labels_}")
print(f"Inertia: {km.inertia_}")

# 4. Predict on new data
predictions = km.predict(time_series)
np.testing.assert_allclose(km.labels_, predictions)
```

### LLM Instruction Prompt
- Always ensure the input data passed to `.fit()` or `.predict()` is strictly formatted as a 3D array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` if starting from lists of variable-length arrays.
- When `metric="dtw"` is selected, the algorithm automatically uses DTW Barycenter Averaging (DBA) to compute the cluster centers.
- Keep `max_iter` and `max_iter_barycenter` small in testing environments to prevent long execution times, especially when using computationally expensive metrics like `"dtw"` or `"softdtw"`.
- Pass a fixed `random_state` (integer or `np.random.RandomState`) to guarantee deterministic centroid initialization.

### Prompt Snippet
```text
Use `tslearn.clustering.TimeSeriesKMeans` to cluster the time-series data into 3 groups using the "dtw" metric. Ensure the input is a 3D array `(n_ts, max_sz, d)`. Set `max_iter=5` and `random_state=42` for deterministic, fast execution. Print the `.inertia_` and `.labels_` after fitting.
```

### Common Failure Modes
- **ValueError due to 2D input:** Passing a standard 2D scikit-learn array `(n_samples, n_features)` to `.fit()` will fail. `tslearn` strictly requires the 3D `(n_ts, max_sz, d)` format.
- **Slow convergence/execution:** Using `metric="dtw"` or `metric="softdtw"` on long time series or large datasets without limiting `max_iter` or `max_iter_barycenter` can cause the algorithm to hang or take excessively long.
- **Invalid metric string:** Passing an unsupported metric (e.g., `"manhattan"`) will raise an error. Only `"euclidean"`, `"dtw"`, and `"softdtw"` are supported.

### Fix Code Hint
```python
# BAD: Passing a 2D array directly to fit
# km.fit(X_2d)

# GOOD: Convert to 3D array first
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_2d)
km.fit(X_3d)
```

## API Test: `TimeSeriesMLPClassifier`

### Signature
```python
class TimeSeriesMLPClassifier(TimeSeriesMixin, MLPClassifier)
```
_Source: tslearn/tslearn/neural_network/neural_network.py:11_

_Source doc:_ A Multi-Layer Perceptron classifier for time series. This class mainly reshapes data so that it can be fed to `scikit-learn`'s ``MLPClassifier``. It accepts the exact same hyper-parameters as ``MLPClassifier``, check `scikit-learn docs <https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html>`__ for a list of parameters and attributes. Notes ----- This method requires a dataset of equal-sized time series. Examples -------- >>> from tslearn.generators import random_walk_blobs >>> X, y = random_walk_blobs(n_ts_per_blob=30, sz=16, d=2, n_blobs=3, ...                          random_state=0) >>> mlp = TimeSeriesMLPClassifier(hidden_layer_sizes=(64, 64), ...                               random_state=0) >>> mlp.fit(X, y)  # doctest: +ELLIPSIS TimeSeriesMLPClassifier(...) >>> [c.shape for c in mlp.coefs_] [(32, 64), (64, 64), (64, 3)] >>> [c.shape for c in mlp.intercepts_] [(64,), (64,), (3,)]

### Goal
A Multi-Layer Perceptron (MLP) classifier for time-series data that automatically reshapes 3D time-series arrays to be compatible with `scikit-learn`'s underlying `MLPClassifier`.

### Parameters
_None._

### Input
A 3D NumPy array of shape `(n_ts, sz, d)` representing the time-series dataset, and a 1D array or list of shape `(n_ts,)` for the target class labels. 
**Precondition:** The dataset *must* consist of equal-sized time series. Unlike some other `tslearn` estimators, this class does not support variable-length time series padded with `nan` values, because the underlying `scikit-learn` MLP cannot process `nan` inputs.

### Output
Returns `unspecified` — An instantiated `TimeSeriesMLPClassifier` object (inheriting from `sklearn.neural_network.MLPClassifier`). Once fitted via `.fit(X, y)`, it exposes standard scikit-learn attributes like `.coefs_` and `.intercepts_`, and can predict classes via `.predict(X)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neural_network import TimeSeriesMLPClassifier

# 1. Prepare a small deterministic 3D dataset (n_ts=4, sz=5, d=2)
X = np.array([
    [[0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5], [0.5, 0.6]],
    [[0.9, 0.8], [0.8, 0.7], [0.7, 0.6], [0.6, 0.5], [0.5, 0.4]],
    [[0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4], [0.5, 0.5]],
    [[0.9, 0.9], [0.8, 0.8], [0.7, 0.7], [0.6, 0.6], [0.5, 0.5]]
])
y = np.array([0, 1, 0, 1])

# 2. Instantiate the classifier with scikit-learn MLP kwargs
mlp = TimeSeriesMLPClassifier(
    hidden_layer_sizes=(8,), 
    max_iter=50, 
    random_state=42
)

# 3. Fit and predict
mlp.fit(X, y)
preds = mlp.predict(X)

# 4. Verify properties
assert preds.shape == (4,)
# The input is flattened from (5, 2) to 10 features before the first hidden layer of size 8
assert mlp.coefs_[0].shape == (10, 8)
print(f"Predictions: {preds}")
```

### LLM Instruction Prompt
- When using `TimeSeriesMLPClassifier`, ensure the input data is strictly formatted as a 3D array `(n_ts, sz, d)`.
- Do not pass variable-length time series padded with `nan` values; this estimator requires equal-sized time series because it flattens the temporal and feature dimensions to feed into `scikit-learn`'s `MLPClassifier`.
- You may pass any standard `sklearn.neural_network.MLPClassifier` hyper-parameters (e.g., `hidden_layer_sizes`, `max_iter`, `activation`) directly to the constructor.

### Prompt Snippet
```text
Use `tslearn.neural_network.TimeSeriesMLPClassifier` to train a neural network on the time-series data. Ensure the input `X` is a 3D array of shape `(n_ts, sz, d)` without any `nan` padding, as this estimator requires equal-length series. Pass `hidden_layer_sizes=(32, 32)` to the constructor.
```

### Common Failure Modes
- **Variable-length series (NaNs):** Passing a dataset generated by `to_time_series_dataset` that contains variable-length series padded with `nan`. The underlying `scikit-learn` MLP will raise a `ValueError` regarding invalid values (NaN).
- **2D Array Input:** Passing a 2D array `(n_ts, sz)` instead of the required 3D array `(n_ts, sz, d)`. `tslearn` estimators strictly expect 3D inputs.
- **Missing scikit-learn kwargs:** Assuming `tslearn` provides default neural network architectures that don't need tuning. It inherits `scikit-learn`'s defaults (e.g., `hidden_layer_sizes=(100,)`), which may be too large or slow for small time-series tasks.

### Fix Code Hint
```python
# BAD: Passing 2D data or data with NaNs
# mlp.fit(X_2d_or_nan, y)

# GOOD: Ensure 3D format and equal lengths (no NaNs)
from tslearn.utils import to_time_series_dataset
from tslearn.preprocessing import TimeSeriesResampler

# If you have variable length series, resample them to a fixed size first
X_resampled = TimeSeriesResampler(sz=10).fit_transform(X_variable)
mlp.fit(X_resampled, y)
```

## API Test: `TimeSeriesMLPRegressor`

### Signature
```python
class TimeSeriesMLPRegressor(TimeSeriesMixin, MLPRegressor)
```
_Source: tslearn/tslearn/neural_network/neural_network.py:133_

_Source doc:_ A Multi-Layer Perceptron regressor for time series. This class mainly reshapes data so that it can be fed to `scikit-learn`'s ``MLPRegressor``. It accepts the exact same hyper-parameters as ``MLPRegressor``, check `scikit-learn docs <https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html>`__ for a list of parameters and attributes. Notes ----- This method requires a dataset of equal-sized time series. Examples -------- >>> mlp = TimeSeriesMLPRegressor(hidden_layer_sizes=(64, 64), ...                               random_state=0) >>> mlp.fit(X=[[1, 2, 3], [1, 1.2, 3.2], [3, 2, 1]], ...         y=[0, 0, 1])  # doctest: +ELLIPSIS TimeSeriesMLPRegressor(...) >>> [c.shape for c in mlp.coefs_] [(3, 64), (64, 64), (64, 1)] >>> [c.shape for c in mlp.intercepts_] [(64,), (64,), (1,)]

### Goal
A Multi-Layer Perceptron (MLP) regressor tailored for time-series data that automatically reshapes 3D time-series arrays to be compatible with `scikit-learn`'s underlying `MLPRegressor`.

### Parameters
_None._ (Note: While the signature facts list no explicit parameters, the source documentation specifies that this class accepts the exact same hyper-parameters as `scikit-learn`'s `MLPRegressor`, such as `hidden_layer_sizes` and `random_state`, via `**kwargs`).

### Input
A dataset of equal-sized time series for `X` and a corresponding array of continuous target values for `y`. While `tslearn` strictly expects time-series datasets to be formatted as 3D `numpy` arrays of shape `(n_ts, max_sz, d)`, this estimator's `.fit()` method will also accept and internally reshape 2D lists or arrays of equal-length sequences. **Precondition:** The time series must be of equal size; variable-length time series are not supported by this method.

### Output
Returns `unspecified` — An instantiated `TimeSeriesMLPRegressor` object (inheriting from `sklearn.neural_network.MLPRegressor`). Once fitted, it exposes standard scikit-learn attributes like `.coefs_` and `.intercepts_`, and can execute `.predict()` to return a 1D array of continuous predictions.

### Valid Call Patterns
```python
from tslearn.neural_network import TimeSeriesMLPRegressor
import numpy as np

# 1. Prepare a small dataset of equal-sized time series (n_ts=3, max_sz=3, d=1)
X_train = np.array([
    [[1.0], [2.0], [3.0]],
    [[1.0], [1.2], [3.2]],
    [[3.0], [2.0], [1.0]]
])
# Continuous target values for regression
y_train = np.array([0.5, 0.6, 1.5])

# 2. Instantiate the regressor with scikit-learn MLP hyperparameters
mlp = TimeSeriesMLPRegressor(
    hidden_layer_sizes=(8,), 
    random_state=42, 
    max_iter=50
)

# 3. Fit the model
mlp.fit(X_train, y_train)

# 4. Predict and verify
preds = mlp.predict(X_train)

assert preds.shape == (3,), f"Expected predictions shape (3,), got {preds.shape}"
print(f"Predictions shape: {preds.shape}")
print(f"Network coefficient shapes: {[c.shape for c in mlp.coefs_]}")
```

### LLM Instruction Prompt
- Use `TimeSeriesMLPRegressor` when you need to train a neural network for time-series regression tasks using a `scikit-learn` compatible API.
- Pass standard `sklearn.neural_network.MLPRegressor` hyperparameters (e.g., `hidden_layer_sizes`, `max_iter`, `random_state`) directly to the constructor.
- Ensure the input dataset `X` consists of strictly equal-sized time series. Do not use this estimator for variable-length time series padded with `nan`, as the underlying scikit-learn MLP requires fixed-size feature vectors without missing values.

### Prompt Snippet
```text
from tslearn.neural_network import TimeSeriesMLPRegressor
# Instantiate with standard sklearn MLP kwargs
regressor = TimeSeriesMLPRegressor(hidden_layer_sizes=(32, 16), random_state=0)
# X must contain equal-sized time series (no NaNs)
regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)
```

### Common Failure Modes
- **Variable-length time series:** Passing a dataset containing variable-length time series (which `tslearn` pads with `nan` values) will cause the underlying `scikit-learn` MLP to fail, as it cannot process `nan` inputs or dynamically sized features.
- **Incorrect target type:** Passing categorical labels instead of continuous values to `.fit(X, y)` will train a regressor on categorical indices, which is mathematically invalid for regression tasks. Use `TimeSeriesMLPClassifier` for classification.

### Fix Code Hint
```python
# If you have variable-length time series, you must resample them to equal lengths first
from tslearn.preprocessing import TimeSeriesResampler
from tslearn.neural_network import TimeSeriesMLPRegressor

# Resample all series to a fixed size (e.g., 10 steps) before fitting
X_resampled = TimeSeriesResampler(sz=10).fit_transform(X_variable_length)

mlp = TimeSeriesMLPRegressor(hidden_layer_sizes=(16,), random_state=42)
mlp.fit(X_resampled, y_continuous)
```

## API Test: `TimeSeriesMixin`

### Signature
```python
class TimeSeriesMixin(object)
```
_Source: tslearn/tslearn/bases/bases.py:53_

### Goal
Provides a base mixin class for custom time-series estimators in `tslearn` to ensure compatibility with the library's internal conventions and scikit-learn pipelines.

### Parameters
_None._

### Input
This is a mixin class, so it does not take standard data inputs directly during initialization. It is intended to be used as a base class (via multiple inheritance) when defining custom time-series estimators. The resulting child class will typically expect time-series datasets formatted as 3D `numpy` arrays of shape `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — when inherited, it provides the child estimator instance with internal `tslearn` tagging and utility methods (such as standardizing time-series data validation).

### Valid Call Patterns
```python
# Inferred from signature and scikit-learn mixin conventions
from tslearn.bases import TimeSeriesMixin
from sklearn.base import BaseEstimator

# 1. Inherit from TimeSeriesMixin when creating a custom estimator
class CustomTimeSeriesModel(BaseEstimator, TimeSeriesMixin):
    def __init__(self):
        pass
        
    def fit(self, X, y=None):
        # Custom estimators should expect X to be (n_ts, max_sz, d)
        return self

# 2. Instantiate the custom model
model = CustomTimeSeriesModel()

# 3. Verify inheritance
assert isinstance(model, TimeSeriesMixin)
print(f"Successfully instantiated custom model inheriting from TimeSeriesMixin: {type(model)}")
```

### LLM Instruction Prompt
- Use `TimeSeriesMixin` strictly as a base class (mixin) when defining custom time-series estimators that need to integrate with `tslearn` and `scikit-learn` pipelines.
- Do not instantiate `TimeSeriesMixin` directly.
- Ensure that any custom estimator inheriting from this mixin expects input data `X` to be formatted as a 3D array `(n_ts, max_sz, d)`, which is the strict requirement for all `tslearn` estimators.

### Prompt Snippet
```text
When building a custom time-series clustering or classification algorithm for `tslearn`, inherit from `sklearn.base.BaseEstimator` and `tslearn.bases.TimeSeriesMixin`. Ensure your `fit` and `predict` methods handle the standard `(n_ts, max_sz, d)` 3D numpy array format.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate `TimeSeriesMixin()` directly or calling it as a function, rather than using it as a base class in a class definition.
- **Ignoring 3D Array Preconditions:** Inheriting from the mixin but failing to design the custom estimator's `fit` or `predict` methods to handle the strict `(n_ts, max_sz, d)` 3D array format required by `tslearn`.
- **Missing Scikit-Learn Base:** Forgetting to also inherit from `sklearn.base.BaseEstimator`, which is required for full pipeline compatibility (e.g., `get_params` and `set_params`).

### Fix Code Hint
```python
# WRONG: Direct instantiation or function call
# mixin = TimeSeriesMixin(X)

# RIGHT: Use as a base class alongside BaseEstimator
from tslearn.bases import TimeSeriesMixin
from sklearn.base import BaseEstimator

class MyTSEstimator(BaseEstimator, TimeSeriesMixin):
    def fit(self, X, y=None):
        # X must be (n_ts, max_sz, d)
        pass
```

## API Test: `TimeSeriesResampler`

### Signature
```python
class TimeSeriesResampler(TimeSeriesMixin, TransformerMixin, BaseEstimator)
```
_Source: tslearn/tslearn/preprocessing/preprocessing.py:23_

_Source doc:_ Resampler for time series. Resample time series so that they reach the target size. Parameters ---------- sz : int (default: -1) Size of the output time series. If not strictly positive, the size of the longuest timeseries in the dataset is used. Examples -------- >>> TimeSeriesResampler(sz=5).fit_transform([[0, 3, 6]]) array([[[0. ], [1.5], [3. ], [4.5], [6. ]]])

### Goal
Resample time-series datasets to a uniform target length (number of time steps) using linear interpolation, facilitating fixed-length requirements for downstream estimators.

### Parameters
_None._

### Input
*   **Constructor Arguments:** The constructor accepts `sz` (int, default: `-1`), which specifies the target size of the output time series. If `sz` is not strictly positive (e.g., `-1`), the resampler will automatically use the size of the longest time series in the dataset passed to `.fit()`.
*   **Data:** The `.fit()`, `.transform()`, and `.fit_transform()` methods expect a time-series dataset formatted as a 3D NumPy array of shape `(n_ts, max_sz, d)`. Raw lists or 2D arrays should be converted using `tslearn.utils.to_time_series_dataset` prior to transformation.

### Output
Returns `unspecified` — Calling `.fit_transform()` or `.transform()` returns a 3D NumPy array of shape `(n_ts, sz, d)` containing the resampled time series. Calling `.fit()` returns the fitted `TimeSeriesResampler` instance itself.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesResampler
from tslearn.utils import to_time_series_dataset

# Pattern 1: Resampling to a specific target size (sz)
X_raw = [[0, 3, 6]]
X_formatted = to_time_series_dataset(X_raw)

resampler = TimeSeriesResampler(sz=5)
X_resampled = resampler.fit_transform(X_formatted)

assert X_resampled.shape == (1, 5, 1)
assert np.allclose(X_resampled[0, :, 0], [0.0, 1.5, 3.0, 4.5, 6.0])

# Pattern 2: Auto-resampling to the longest time series in the dataset
X_train = to_time_series_dataset([
    [1, 2, 3, 4],
    [1, 2, 3],
    [2, 5, 6, 7, 8, 9],  # Longest series: length 6
    [3, 5, 6, 7, 8]
])
X_test = to_time_series_dataset([
    [1, 2, 3],
    [3, 5, 6, 7, 8]
])

# sz defaults to -1, meaning it will learn max_sz=6 from X_train
auto_resampler = TimeSeriesResampler()
auto_resampler.fit(X_train)
X_test_resampled = auto_resampler.transform(X_test)

assert X_test_resampled.shape == (2, 6, 1)
```

### LLM Instruction Prompt
- Always format raw time-series data into a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before passing it to `TimeSeriesResampler`.
- To resample to a specific length, pass `sz=<int>` to the constructor.
- To dynamically pad/resample to the length of the longest sequence in the training set, omit `sz` (it defaults to `-1`) and ensure you call `.fit(X_train)` before calling `.transform(X_test)`.
- Treat this class as a standard `scikit-learn` transformer; it implements `.fit()`, `.transform()`, and `.fit_transform()`.

### Prompt Snippet
```text
tslearn.preprocessing.TimeSeriesResampler resamples time series to a target size `sz` using linear interpolation. Initialize with `TimeSeriesResampler(sz=10)` for a fixed size, or `TimeSeriesResampler()` to auto-detect the maximum length from the fitted dataset. Inputs to `.fit()` and `.transform()` MUST be 3D arrays `(n_ts, max_sz, d)` prepared via `tslearn.utils.to_time_series_dataset`.
```

### Common Failure Modes
- **Not calling `fit` before `transform` with default `sz`:** If initialized with `sz=-1` (the default), the resampler must learn the target size from a training set via `.fit()`. Calling `.transform()` directly will raise a `NotFittedError`.
- **Incorrect Input Dimensionality:** Passing a flat 1D list or a 2D array of shape `(n_ts, max_sz)` directly to `.fit_transform()` without converting it to the required 3D `(n_ts, max_sz, d)` format can cause broadcasting or interpolation errors.

### Fix Code Hint
```python
# BAD: Passing 2D lists directly or forgetting to fit
# resampler = TimeSeriesResampler()
# X_resampled = resampler.transform([[1, 2], [3, 4, 5]])

# GOOD: Convert to 3D dataset and use fit_transform
from tslearn.utils import to_time_series_dataset
from tslearn.preprocessing import TimeSeriesResampler

X = to_time_series_dataset([[1, 2], [3, 4, 5]])
resampler = TimeSeriesResampler(sz=10)
X_resampled = resampler.fit_transform(X)
```

## API Test: `TimeSeriesSVC`

### Signature
```python
class TimeSeriesSVC(TimeSeriesSVMMixin, ClassifierMixin, BaseEstimator)
```
_Source: tslearn/tslearn/svm/svm.py:110_

_Source doc:_ Time-series specific Support Vector Classifier. Parameters ---------- C : float, optional (default=1.0) Penalty parameter C of the error term. kernel : string, optional (default='gak') Specifies the kernel type to be used in the algorithm. It must be one of 'gak' or a kernel accepted by ``sklearn.svm.SVC``. If none is given, 'gak' will be used. If a callable is given it is used to pre-compute the kernel matrix from data matrices; that matrix should be an array of shape ``(n_samples, n_samples)``. degree : int, optional (default=3) Degree of the polynomial kernel function ('poly'). Ignored by all other kernels. gamma : float, optional (default='auto') Kernel coefficient for 'gak', 'rbf', 'poly' and 'sigmoid'. For 'gak' kernel, a `RuntimeError` is raised at fit time when value is close to 0 and therefore not compatible with 'gak' kernel. If gamma is 'auto' then: - for 'gak' kernel, it is computed based on a sampling of the training set (cf :ref:`tslearn.metrics.gamma_soft_dtw <fun-tslearn.metrics.gamma_soft_dtw>`). A `RuntimeError` is raised at fit time when computed value is close to 0 and therefore not compatible with 'gak' kernel. - for other kernels (eg. 'rbf'), 1/n_features will be used. coef0 : float, optional (default=0.0) Independent term in kernel function. It is only significant in 'poly' and 'sigmoid'. shrinking : boolean, optional (default=True) Whether to use the shrinking heuristic. probability : boolean, optional (default=False) Whether to enable probability estimates. This must be enabled prior to calling `fit`, and will slow down that method. Also, probability estimates are not guaranteed to match predict output. See our :ref:`dedicated user guide section <kernels-ml>` for more details. tol : float, optional (default=1e-3) Tolerance for stopping criterion. cache_size : float, optional (default=200.0) Specify the size of the kernel cache (in MB). class_weight : {dict, 'balanced'}, optional Set the parameter C of class i to class_weight[i]*C for SVC. If not given, all classes are supposed to have weight one. The "balanced" mode uses the values of y to automatically adjust weights inversely proportional to class frequencies in the input data as ``n_samples / (n_classes * np.bincount(y))``

### Goal
Train a Support Vector Machine classifier specifically designed for time-series data, utilizing time-series specific kernels like the Global Alignment Kernel (`gak`).

### Parameters
_None._

### Input
- **Constructor Arguments**: 
  - `C` (float): Penalty parameter (default 1.0).
  - `kernel` (str): Kernel type, defaults to `"gak"` (Global Alignment Kernel). Can also be standard `sklearn` kernels.
  - `gamma` (float or `"auto"`): Kernel coefficient. For `"gak"`, `"auto"` computes it based on training set sampling.
  - `probability` (bool): Set to `True` to enable probability estimates (must be done prior to `fit`).
  - `class_weight` (dict or `"balanced"`): Class weights.
- **Training Data (`X`)**: A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time series. Variable-length time series must be padded with `nan` values (typically prepared via `tslearn.utils.to_time_series_dataset`).
- **Training Labels (`y`)**: A 1D array-like of shape `(n_ts,)` containing the target class labels.

### Output
Returns `unspecified` — an instantiated and (after calling `.fit()`) fitted `TimeSeriesSVC` estimator object, fully compatible with `scikit-learn` pipelines and cross-validation utilities.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare variable-length time-series data into the required 3D format
X = to_time_series_dataset([
    [1, 2, 3, 4],
    [1, 2, 3],
    [2, 5, 6, 7, 8, 9],
    [3, 5, 6, 7, 8]
])
y = [0, 0, 1, 1]

# 2. Instantiate the classifier with the Global Alignment Kernel
rng = np.random.RandomState(0)
clf = TimeSeriesSVC(kernel="gak", random_state=rng)

# 3. Fit the model and predict
clf.fit(X, y)
predictions = clf.predict(X)

assert np.array_equal(predictions, [0, 0, 1, 1])
```

### LLM Instruction Prompt
- Use `tslearn.svm.TimeSeriesSVC` for time-series classification tasks requiring Support Vector Machines.
- Always ensure the input data `X` is formatted as a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before calling `.fit()` or `.predict()`.
- The default kernel is `"gak"` (Global Alignment Kernel), which natively handles variable-length time series padded with `nan`s.
- If probability estimates are required (e.g., for `.predict_proba()`), you must explicitly pass `probability=True` during initialization.
- Be aware that for the `"gak"` kernel, if the computed `gamma` value is close to 0, a `RuntimeError` will be raised at fit time.

### Prompt Snippet
```text
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

X_train = to_time_series_dataset([[1, 2], [1, 2, 3], [8, 9], [7, 8, 9]])
y_train = [0, 0, 1, 1]

clf = TimeSeriesSVC(kernel="gak", C=1.0)
clf.fit(X_train, y_train)
preds = clf.predict(X_train)
```

### Common Failure Modes
- **ValueError (2D Array Input)**: Passing a standard 2D `scikit-learn` array `(n_samples, n_features)` instead of the required 3D `(n_ts, max_sz, d)` array. Always preprocess raw lists with `to_time_series_dataset`.
- **RuntimeError (Gamma close to 0)**: When using `kernel="gak"` and `gamma="auto"`, if the training data has zero variance or identical samples causing the sampled `gamma` to approach 0, the model will fail to fit.
- **AttributeError (predict_proba not available)**: Attempting to call `.predict_proba()` when the estimator was initialized with the default `probability=False`.

### Fix Code Hint
```python
# BAD: Passing 2D lists directly or forgetting probability=True for predict_proba
clf = TimeSeriesSVC()
clf.fit([[1, 2], [8, 9]], [0, 1])
probs = clf.predict_proba([[1, 2]])

# GOOD: Convert to 3D array and enable probability
from tslearn.utils import to_time_series_dataset
X = to_time_series_dataset([[1, 2], [8, 9]])
clf = TimeSeriesSVC(probability=True)
clf.fit(X, [0, 1])
probs = clf.predict_proba(X)
```

## API Test: `TimeSeriesSVMMixin`

### Signature
```python
class TimeSeriesSVMMixin(TimeSeriesMixin)
```
_Source: tslearn/tslearn/svm/svm.py:20_

_Source doc:_ Time series mixin for SVM based estimators.

### Goal
Provides a mixin class for Support Vector Machine (SVM) based time-series estimators to ensure compatibility with `tslearn`'s 3D array data formats and `scikit-learn`'s API.

### Parameters
_None._

### Input
As a mixin class, it takes no runtime data inputs during initialization. It is intended to be inherited by custom SVM estimator classes. Methods provided by this mixin will expect time-series datasets to be strictly formatted as 3D `numpy` arrays of shape `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — acts as a base class providing SVM-specific time-series utility methods and attributes for derived estimators.

### Valid Call Patterns
```python
from tslearn.svm.svm import TimeSeriesSVMMixin
from sklearn.base import BaseEstimator

# Inferred from signature: Mixins are meant to be inherited, not instantiated directly.
class CustomTimeSeriesSVM(BaseEstimator, TimeSeriesSVMMixin):
    def __init__(self):
        pass

estimator = CustomTimeSeriesSVM()

assert isinstance(estimator, TimeSeriesSVMMixin), "Estimator should inherit from TimeSeriesSVMMixin"
print("Custom SVM estimator successfully inherited from TimeSeriesSVMMixin.")
```

### LLM Instruction Prompt
- Use `TimeSeriesSVMMixin` strictly as a base class (mixin) when creating custom SVM-based time-series estimators.
- Do not instantiate `TimeSeriesSVMMixin` directly.
- Ensure that any data passed to the resulting estimator's methods is formatted as a 3D `numpy` array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`.

### Prompt Snippet
```text
Use `TimeSeriesSVMMixin` as a base class for custom SVM time-series estimators. Do not instantiate it directly. Ensure input data to the derived estimator is a 3D array `(n_ts, max_sz, d)`.
```

### Common Failure Modes
- **Direct Instantiation:** Attempting to instantiate `TimeSeriesSVMMixin` directly rather than using it as a base class for an estimator.
- **Incorrect Data Dimensions:** Passing 1D or 2D arrays to the methods inherited from this mixin, which strictly require the `(n_ts, max_sz, d)` 3D array format.

### Fix Code Hint
```python
# Inherit from the mixin rather than instantiating it
class MySVM(BaseEstimator, TimeSeriesSVMMixin):
    pass

# Ensure data is 3D before passing to inherited methods
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
```

## API Test: `TimeSeriesSVR`

### Signature
```python
class TimeSeriesSVR(TimeSeriesSVMMixin, RegressorMixin, BaseEstimator)
```
_Source: tslearn/tslearn/svm/svm.py:413_

_Source doc:_ Time-series specific Support Vector Regressor. Parameters ---------- C : float, optional (default=1.0) Penalty parameter C of the error term. kernel : string, optional (default='gak') Specifies the kernel type to be used in the algorithm. It must be one of 'gak' or a kernel accepted by ``sklearn.svm.SVC``. If none is given, 'gak' will be used. If a callable is given it is used to pre-compute the kernel matrix from data matrices; that matrix should be an array of shape ``(n_samples, n_samples)``. degree : int, optional (default=3) Degree of the polynomial kernel function ('poly'). Ignored by all other kernels. gamma : float, optional (default='auto') Kernel coefficient for 'gak', 'rbf', 'poly' and 'sigmoid'. For 'gak' kernel, a `RuntimeError` is raised at fit time when value is close to 0 and therefore not compatible with 'gak' kernel. If gamma is 'auto' then: - for 'gak' kernel, it is computed based on a sampling of the training set (cf :ref:`tslearn.metrics.gamma_soft_dtw <fun-tslearn.metrics.gamma_soft_dtw>`). A `RuntimeError` is raised at fit time when computed value is close to 0 and therefore not compatible with 'gak' kernel. - for other kernels (eg. 'rbf'), 1/n_features will be used. coef0 : float, optional (default=0.0) Independent term in kernel function. It is only significant in 'poly' and 'sigmoid'. tol : float, optional (default=1e-3) Tolerance for stopping criterion. epsilon : float, optional (default=0.1) Epsilon in the epsilon-SVR model. It specifies the epsilon-tube within which no penalty is associated in the training loss function with points predicted within a distance epsilon from the actual value. shrinking : boolean, optional (default=True) Whether to use the shrinking heuristic. cache_size :  float, optional (default=200.0) Specify the size of the kernel cache (in MB). n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for GAK cross-similarity matrix computations. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`_ for more details. verbose : int, default: 0

### Goal
Trains a time-series specific Support Vector Regressor, typically utilizing the Global Alignment Kernel (GAK) to handle variable-length sequences and temporal shifts.

### Parameters
_None._

### Input
- **`X` (Training Data)**: Must be a strictly formatted 3D `numpy` array of shape `(n_ts, max_sz, d)` representing the number of time series, maximum sequence length, and dimensionality. Variable-length time series must be padded with `nan` values (handled automatically by `tslearn.utils.to_time_series_dataset`).
- **`y` (Target Values)**: A 1D array-like of shape `(n_ts,)` containing continuous regression targets.

### Output
Returns `unspecified` — A fitted `TimeSeriesSVR` estimator object that is fully compatible with `scikit-learn` pipelines and exposes a `.predict(X)` method returning a 1D array of continuous predictions.

### Valid Call Patterns
```python
from tslearn.svm import TimeSeriesSVR
from tslearn.utils import to_time_series_dataset
import numpy as np

# 1. Prepare variable-length time series data
X = to_time_series_dataset([
    [1.0, 2.0, 3.0, 4.0],
    [1.0, 2.0, 3.0],
    [2.0, 5.0, 6.0, 7.0, 8.0, 9.0],
    [3.0, 5.0, 6.0, 7.0, 8.0]
])
y_reg = [-1.0, -1.3, 3.2, 4.1]

# 2. Initialize and fit the regressor
clf = TimeSeriesSVR(kernel="gak")
clf.fit(X, y_reg)

# 3. Predict on new or existing data
preds = clf.predict(X)

assert preds.shape == (4,)
print(f"Predictions: {preds}")
```

### LLM Instruction Prompt
- Use `TimeSeriesSVR` for time-series regression tasks where temporal alignment is important.
- ALWAYS ensure the input `X` is converted to a 3D `numpy` array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before calling `.fit()` or `.predict()`.
- The default kernel is `"gak"` (Global Alignment Kernel), which natively supports variable-length time series padded with `nan`.
- `TimeSeriesSVR` is fully compatible with `scikit-learn` utilities like `cross_val_score` and `KFold`.

### Prompt Snippet
```text
Use `tslearn.svm.TimeSeriesSVR` for time-series regression. Convert raw lists to a 3D array `(n_ts, max_sz, d)` using `to_time_series_dataset` before fitting. The default `"gak"` kernel handles variable-length series padded with `nan`.
```

### Common Failure Modes
- **Dimensionality Error**: Passing 2D arrays or raw lists directly to `.fit()` or `.predict()` instead of the required 3D array format.
- **Incompatible Kernel with Variable Lengths**: Using standard `scikit-learn` kernels (like `"rbf"`) on variable-length time series containing `nan` padding, which will cause standard kernels to fail. Stick to `"gak"` for variable-length data.
- **Gamma Value Error**: A `RuntimeError` is raised at fit time if the `gamma` parameter is computed or set to a value too close to 0, making it incompatible with the `"gak"` kernel.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.svm import TimeSeriesSVR

# FIX: Convert raw data to the required 3D format before fitting
X_formatted = to_time_series_dataset(X_raw)

# FIX: Use the "gak" kernel to safely handle nan-padded variable-length series
regressor = TimeSeriesSVR(kernel="gak")
regressor.fit(X_formatted, y_targets)
predictions = regressor.predict(X_formatted)
```

## API Test: `TimeSeriesScalerMeanVariance`

### Signature
```python
class TimeSeriesScalerMeanVariance(TimeSeriesMixin, TransformerMixin, BaseEstimator)
```
_Source: tslearn/tslearn/preprocessing/preprocessing.py:283_

_Source doc:_ Scaler for time series datasets. When `per_timeseries` is False, scales features based on computation led on the fitted data, so that their mean (resp. standard deviation) in given dimensions is mu (resp. std). The transformation is stateless otherwise, dealing with each timeseries individually. Parameters ---------- mu : float (default: 0.) Mean of the output time series. std : float (default: 1.) Standard deviation of the output time series. per_timeseries: bool (default: True) Whether the scaling should be performed per time series. per_feature: bool (default: True) Whether the scaling should be performed per feature. Meaningless for univariate timeseries. Notes ----- NaNs within a time series are ignored when calculating mu and std. Examples -------- >>> TimeSeriesScalerMeanVariance(mu=0., ...                              std=1.).fit_transform([[0, 3, 6]]) array([[[-1.22474487], [ 0.        ], [ 1.22474487]]]) >>> TimeSeriesScalerMeanVariance(mu=0., ...                              std=1.).fit_transform([[numpy.nan, 3, 6]]) array([[[nan], [-1.], [ 1.]]]) >>> TimeSeriesScalerMeanVariance(per_timeseries=False, ...                              per_feature=False ... ).fit_transform([[[1, 2], [2, 3]], [[3, 4], [4, 5]]]) array([[[-1.63299316, -0.81649658], [-0.81649658,  0.        ]], <BLANKLINE> [[ 0.        ,  0.81649658], [ 0.81649658,  1.63299316]]])

### Goal
Scales time-series datasets so that their mean and standard deviation match specified target values (defaulting to 0 and 1), operating either independently per time series or globally across the fitted dataset.

### Parameters
_None._

### Input
*   **Constructor Arguments** (inferred from docstring): 
    *   `mu` (float, default: `0.`): Target mean of the output time series.
    *   `std` (float, default: `1.`): Target standard deviation of the output time series.
    *   `per_timeseries` (bool, default: `True`): If `True`, scaling is stateless and performed independently for each time series. If `False`, scaling is stateful and based on the global statistics of the fitted training data.
    *   `per_feature` (bool, default: `True`): Whether scaling should be performed independently per feature dimension.
*   **Data**: A 3D NumPy array of shape `(n_ts, max_sz, d)` passed to `.fit()`, `.transform()`, or `.fit_transform()`.
*   **Preconditions**: Raw lists or 2D arrays must be converted to the strict 3D format using `tslearn.utils.to_time_series_dataset` prior to scaling. Variable-length time series should be padded with `np.nan` (which the scaler safely ignores during mean/std calculations).

### Output
Returns `unspecified` — A transformed 3D NumPy array of shape `(n_ts, max_sz, d)` containing the scaled time-series data. `NaN` padding values from the input are preserved in the output.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn.utils import to_time_series_dataset

# 1. Prepare variable-length time series data
raw_data = [[0, 3, 6], [np.nan, 3, 6]]
X = to_time_series_dataset(raw_data)

# 2. Instantiate the scaler (stateless per-timeseries scaling by default)
scaler = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0)

# 3. Fit and transform the dataset
X_scaled = scaler.fit_transform(X)

# 4. Verify the output shape and scaled values
assert X_scaled.shape == (2, 3, 1)

# First time series: [0, 3, 6] -> mean 3, std ~2.449 -> [-1.2247, 0, 1.2247]
np.testing.assert_allclose(X_scaled[0, 0, 0], -1.22474487, rtol=1e-5)

# Second time series: [nan, 3, 6] -> mean 4.5, std 1.5 -> [nan, -1, 1]
np.testing.assert_allclose(X_scaled[1, 1, 0], -1.0, rtol=1e-5)
assert np.isnan(X_scaled[1, 0, 0])

print(f"Successfully scaled {X_scaled.shape[0]} time series.")
```

### LLM Instruction Prompt
- Always ensure the input to `fit_transform` or `transform` is a 3D array of shape `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists or 2D arrays before scaling.
- By default, `TimeSeriesScalerMeanVariance` operates statelessly (`per_timeseries=True`), meaning it scales each time series individually based on its own mean and variance. If you need to scale a test set based on the global statistics of a training set, you must explicitly set `per_timeseries=False` during instantiation.
- Do not manually strip `NaN` values before scaling; the scaler natively ignores `NaN`s when computing statistics and preserves them in the output to maintain the 3D array structure for variable-length series.

### Prompt Snippet
```text
Use `tslearn.preprocessing.TimeSeriesScalerMeanVariance` to normalize the time-series data to zero mean and unit variance. Ensure the input is formatted as a 3D array `(n_ts, max_sz, d)` using `to_time_series_dataset` before calling `.fit_transform()`.
```

### Common Failure Modes
- **Dimensionality Error (ValueError)**: Passing a 1D or 2D array directly to `.fit_transform()` instead of the required 3D `(n_ts, max_sz, d)` format.
- **Data Leakage / Incorrect Scaling Semantics**: Assuming the scaler fits global dataset statistics by default (like `sklearn.preprocessing.StandardScaler`). Because `per_timeseries=True` is the default, calling `.transform()` on new data will scale it using its *own* statistics, not the training set's statistics, unless `per_timeseries=False` is specified.
- **Zero Variance Warning/NaNs**: If a time series (or feature) has zero variance (e.g., all constant values), scaling to unit variance may result in division by zero or `NaN`s if not handled properly by the underlying data.

### Fix Code Hint
```python
# BAD: Passing a 2D array directly
# scaler = TimeSeriesScalerMeanVariance()
# X_scaled = scaler.fit_transform([[1, 2, 3], [4, 5, 6]])

# GOOD: Convert to 3D first
from tslearn.utils import to_time_series_dataset
from tslearn.preprocessing import TimeSeriesScalerMeanVariance

X_3d = to_time_series_dataset([[1, 2, 3], [4, 5, 6]])
scaler = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0)
X_scaled = scaler.fit_transform(X_3d)
```

## API Test: `TimeSeriesScalerMinMax`

### Signature
```python
class TimeSeriesScalerMinMax(TimeSeriesMixin, TransformerMixin, BaseEstimator)
```
_Source: tslearn/tslearn/preprocessing/preprocessing.py:141_

_Source doc:_ Scaler for time series datasets. When `per_timeseries` is False, scales features based on computation led on the fitted data, so that their span in given dimensions is between ``min`` and ``max`` where ``value_range=(min, max)``. The transformation is stateless otherwise, dealing with each timeseries individually. Parameters ---------- value_range : tuple (default: (0., 1.)) The minimum and maximum value for the output time series. per_timeseries: bool (default: True) Wether the scaling should be performed per time series. per_feature: bool (default: True) Wether the scaling should be performed per feature. Meaningless for univariate timeseries. Notes ----- NaNs within a time series are ignored when calculating min and max. Examples -------- >>> TimeSeriesScalerMinMax(value_range=(1., 2.)).fit_transform([[0, 3, 6]]) array([[[1. ], [1.5], [2. ]]]) >>> TimeSeriesScalerMinMax(value_range=(1., 2.)).fit_transform( ...     [[numpy.nan, 3, 6]] ... ) array([[[nan], [ 1.], [ 2.]]]) >>> TimeSeriesScalerMinMax(value_range=(1., 2.), per_timeseries=False, per_feature=False).fit_transform( ...    [[[1, 2], [2, 3]], ...    [[3, 4], [4, 5]]] ... ) array([[[1.  , 1.25], [1.25, 1.5 ]], <BLANKLINE> [[1.5 , 1.75], [1.75, 2.  ]]])

### Goal
Scales time-series datasets so that their values fall within a specified range (default 0 to 1), either independently per time series and feature, or globally across the fitted data.

### Parameters
_None._

### Input
The `fit`, `transform`, and `fit_transform` methods expect a time-series dataset, strictly formatted as a 3D NumPy array of shape `(n_ts, max_sz, d)` (number of time series, maximum sequence length, number of dimensions). Variable-length time series should be padded with `numpy.nan`. 

The constructor accepts configuration arguments: `value_range` (tuple, default `(0., 1.)`), `per_timeseries` (bool, default `True`), and `per_feature` (bool, default `True`).

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)` containing the scaled time series. `NaN` values used for padding are ignored during min/max calculation and are preserved in the output array.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.utils import to_time_series_dataset

# Example 1: Default scaling (0 to 1, per time series)
X = to_time_series_dataset([[1, 3, 4, 2], [1, 2, 4, 2]])
scaler = TimeSeriesScalerMinMax()
X_scaled = scaler.fit_transform(X)

assert X_scaled.shape == (2, 4, 1)
assert np.nanmax(X_scaled) == 1.0
assert np.nanmin(X_scaled) == 0.0

# Example 2: Custom range and variable length with NaNs
X_var = [
    [1, np.nan],
    [3, 4]
]
scaler_custom = TimeSeriesScalerMinMax(value_range=(1., 2.), per_timeseries=True)
X_var_scaled = scaler_custom.fit_transform(X_var)

# Shorter series retain their NaN padding
assert np.isnan(X_var_scaled[0, 1, 0])
assert np.nanmax(X_var_scaled) == 2.0
```

### LLM Instruction Prompt
- Always ensure the input data is formatted as a 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` before calling `.fit()` or `.fit_transform()`.
- Use `per_timeseries=False` in the constructor if you want to scale based on a global min/max computed across the entire fitted dataset instead of scaling each time series individually (which is the default stateless behavior).
- Remember that `NaN` values (used for padding variable-length series) are safely ignored during min/max calculation and are preserved in the output. Do not attempt to impute them before scaling if they represent padding.

### Prompt Snippet
```text
# Scale the time series dataset to a range of [-1, 1] globally across all series
from tslearn.preprocessing import TimeSeriesScalerMinMax
scaler = TimeSeriesScalerMinMax(value_range=(-1.0, 1.0), per_timeseries=False)
X_scaled = scaler.fit_transform(X_3d)
```

### Common Failure Modes
- Passing 1D or 2D arrays directly without reshaping or using `to_time_series_dataset`, which may cause shape mismatch errors or incorrect feature-wise scaling.
- Assuming the scaler handles `NaN` imputation; it ignores `NaN`s for scaling but leaves them in the output, which might cause downstream estimators (like standard scikit-learn models) to fail if they do not support `NaN`s.
- Using `per_timeseries=True` (the default) on a dataset where some individual time series have zero variance (e.g., all values are identical), which can lead to division by zero or `NaN` outputs for those specific series.

### Fix Code Hint
```python
# Wrap raw lists in to_time_series_dataset to ensure the strict 3D format (n_ts, max_sz, d)
from tslearn.utils import to_time_series_dataset
from tslearn.preprocessing import TimeSeriesScalerMinMax

X_3d = to_time_series_dataset(raw_data)
scaler = TimeSeriesScalerMinMax(value_range=(0.0, 1.0))
X_scaled = scaler.fit_transform(X_3d)
```

## API Test: `TsLearnTags`

### Signature
```python
class TsLearnTags(Tags)
```
_Source: tslearn/tslearn/bases/bases.py:29_

### Goal
Defines scikit-learn compatible estimator tags specific to `tslearn` models, indicating their capabilities (such as accepting 3D variable-length time-series data).

### Parameters
_None._

### Input
No input parameters are required to instantiate this class. It is typically used internally or by custom estimators to declare compatibility with `tslearn`'s strict `(n_ts, max_sz, d)` 3D array format and variable-length time-series handling.

### Output
Returns an instance of `TsLearnTags` (inheriting from `Tags`) representing the estimator's tag configuration. The exact internal tag dictionary structure is not specified in the provided facts.

### Valid Call Patterns
```python
# Inferred from the signature (no verified examples in the provided context)
from tslearn.bases.bases import TsLearnTags

# Instantiate the tags object
tags = TsLearnTags()

# Assert falsifiable property
assert isinstance(tags, TsLearnTags), "Failed to instantiate TsLearnTags"
print("TsLearnTags instantiated successfully.")
```

### LLM Instruction Prompt
- When creating custom `tslearn` estimators or inspecting `tslearn` base classes, use `TsLearnTags()` to generate or represent the appropriate scikit-learn compatible tags. Do not pass any arguments to the constructor.

### Prompt Snippet
```text
`TsLearnTags` is a base class/utility in `tslearn.bases.bases` used to define scikit-learn compatible estimator tags for time-series models. It takes no arguments upon instantiation: `tags = TsLearnTags()`.
```

### Common Failure Modes
- **Passing arguments to the constructor:** Because `TsLearnTags` takes no parameters, providing arguments (e.g., trying to pass a dictionary of tags directly into the constructor) will raise a `TypeError`.

### Fix Code Hint
```python
# BAD: Attempting to pass arguments to the constructor
# tags = TsLearnTags({"allow_nan": True})

# GOOD: Instantiate without arguments
tags = TsLearnTags()
```

## API Test: `UCR_UEA_datasets`

### Signature
```python
class UCR_UEA_datasets
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:36_

_Source doc:_ A convenience class to access UCR/UEA time series datasets. When using one (or several) of these datasets in research projects, please cite [1]_. This class will attempt to recover from some known misnamed files, like the `StarLightCurves` dataset being provided in `StarlightCurves.zip` and alike. Parameters ---------- use_cache : bool (default: True) Whether a cached version of the dataset should be used in :meth:`~load_dataset`, if one is found. Datasets are always cached upon loading, and this parameter only determines whether the cached version shall be refreshed upon loading. root_dir : str or None (default: None) Directory to be used to cache downloaded datasets. If None, a default directory is used: - If the environment variable `XDG_DATA_HOME` is set, the default directory is `$XDG_DATA_HOME/tslearn/UCR_UEA`. - Otherwise, the default directory is `~/.tslearn/datasets/UCR_UEA`. Notes ----- Downloading dataset files can be time-consuming, it is recommended using `use_cache=True` (default) in order to only experience downloading time once per dataset and work on a cached version of the datasets afterward. See Also -------- CachedDatasets : Provides pre-selected datasets for offline use. References ---------- .. [1] A. Bagnall, J. Lines, W. Vickers and E. Keogh, The UEA & UCR Time Series Classification Repository, www.timeseriesclassification.com

### Goal
Instantiate a data loader to access, cache, and manage time-series datasets from the UCR/UEA classification repository.

### Parameters
_None._

### Input
Optional constructor arguments (parsed from the docstring):
- `use_cache` (bool, default `True`): Whether to use a cached version of the dataset if one is found.
- `root_dir` (str or None, default `None`): Directory to be used to cache downloaded datasets. If `None`, defaults to `$XDG_DATA_HOME/tslearn/UCR_UEA` or `~/.tslearn/datasets/UCR_UEA`.

### Output
Returns `unspecified` — an instance of the `UCR_UEA_datasets` class, which provides methods like `load_dataset(name)` and `list_cached_datasets()`.

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets
import tempfile

# Instantiate the loader with a custom temporary directory to avoid network calls during testing
with tempfile.TemporaryDirectory() as tmp_path:
    data_loader = UCR_UEA_datasets(root_dir=tmp_path)
    
    # List cached datasets in the empty directory
    cached_dir = data_loader.list_cached_datasets()
    
    assert isinstance(cached_dir, list)
    assert len(cached_dir) == 0
    print(f"Successfully initialized UCR_UEA_datasets. Cached items: {cached_dir}")
```

### LLM Instruction Prompt
- Use `UCR_UEA_datasets` to download and cache standard time-series datasets (e.g., "Trace").
- Always prefer `use_cache=True` (the default) to avoid redundant network requests.
- In offline or restricted environments, either provide a `root_dir` pointing to an existing cache, or use `tslearn.datasets.CachedDatasets` instead.
- Remember that calling `load_dataset("DatasetName")` on the resulting instance returns a 4-tuple: `(X_train, y_train, X_test, y_test)`.
- The loaded `X_train` and `X_test` arrays will strictly follow the `tslearn` 3D format `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
tslearn.datasets.UCR_UEA_datasets(use_cache=True, root_dir=None)
A class to download and cache UCR/UEA datasets. Use `.load_dataset("Name")` to get (X_train, y_train, X_test, y_test) in 3D format. Requires network access unless the dataset is already cached in `root_dir`.
```

### Common Failure Modes
- **Network Errors**: Calling `load_dataset()` for an uncached dataset in an environment without internet access will raise an exception.
- **Permission Errors**: Providing a `root_dir` that the current user does not have write permissions for will cause caching to fail.
- **Shape Mismatch Assumptions**: Assuming the loaded `X_train` is a 2D `scikit-learn` array; `tslearn` datasets are strictly loaded as 3D arrays `(n_ts, max_sz, d)`.

### Fix Code Hint
```python
# If network access is restricted, point root_dir to a pre-populated cache directory
data_loader = UCR_UEA_datasets(root_dir="/path/to/offline/cache")

# Alternatively, use CachedDatasets for built-in offline datasets like "Trace"
from tslearn.datasets import CachedDatasets
offline_loader = CachedDatasets()
X_train, y_train, X_test, y_test = offline_loader.load_dataset("Trace")
```

## API Test: `VARIMA`

### Signature
```python
class VARIMA(TimeSeriesMixin, BaseEstimator, BaseModelPackage)
```
_Source: tslearn/tslearn/forecasting/_arima.py:111_

_Source doc:_ Vector AutoRegressive Integrated Moving Average (VARIMA) estimator [1]_. Parameters ---------- p : int, (default: 1) AutoRegressive (AR) order of the model. d : int (default: 0) Differentiation order of the model. q : int (default: 0) Moving-Average (MA) order of the model. with_constant : bool (default: True) Whether the model should include an intercept term. seasonal_period: int or None (default: None) When set to a positive integer :math:`m`, the model includes a naïve seasonal integration step where :math:`x'_t = x_t - x_{t-m}`. max_iter : int (default: 50) The maximum number of iterations used while fitting the model. verbose : int (default 0) When set to a positive integer, displays logs of the iteration of the optimization. Not relevant if q=0. Attributes ---------- lle_ : float Loglikelihood of the fitted model intercept_ : array-like of shape=(n_features) Intercept term of the fitted model ar_coeffs_ : array-like of shape=(p, n_features, n_features) AR coefficients of the fitted model ma_coeffs_ : array-like of shape=(q, n_features, n_features) MA coefficients of the fitted model Notes ----- This estimator supports variable length time-series See Also -------- AutoVARIMA: Automatic order selection of a VARIMA model References ---------- .. [1] R. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice. OTexts, 2014. https://otexts.com/fpp3/

### Goal
Train a Vector AutoRegressive Integrated Moving Average (VARIMA) model for time-series forecasting, supporting variable-length multivariate sequences.

### Parameters
_None._

### Input
A 3D numpy array of shape `(n_ts, max_sz, d)` representing the time-series dataset to fit or predict. Variable-length time series are natively supported and must be right-padded with `np.nan`. The time series must have a sufficient minimum length (greater than 1 non-NaN observation) to avoid a `ValueError` during fitting or prediction.

### Output
Returns `unspecified` — A fitted `VARIMA` estimator instance (when calling `.fit()`), which exposes attributes like `ar_coeffs_` and `ma_coeffs_`, and provides `.predict()` and `.fit_predict()` methods to generate future time-series values.

### Valid Call Patterns
```python
import numpy as np
from tslearn.forecasting import VARIMA

# 3D array: (n_ts=2, max_sz=5, d=1)
# The second time series is shorter and padded with np.nan
data = np.array([
    [[1.0], [2.0], [3.0], [4.0], [5.0]],
    [[2.0], [4.0], [6.0], [8.0], [np.nan]]
])

# Instantiate with AR order (p=1), differencing (d=0), and MA order (q=0)
model = VARIMA(1, 0, 0, with_constant=False)

# Fit the model and forecast 2 steps ahead
horizon = 2
predicted = model.fit_predict(data, n=horizon)

assert predicted.shape == (2, horizon, 1)
print("Forecast shape:", predicted.shape)
```

### LLM Instruction Prompt
- Instantiate `VARIMA` with the AR order `p`, differencing order `d`, and MA order `q` as positional arguments (e.g., `VARIMA(1, 0, 0)`).
- Ensure input data is strictly a 3D numpy array of shape `(n_ts, max_sz, d)`.
- Handle variable-length time series by padding shorter series with `np.nan` at the end.
- Use `.fit_predict(data, n=horizon)` to train the model and immediately forecast `n` steps ahead.
- Ensure time series have sufficient length (more than 1 observation) to avoid `ValueError`.

### Prompt Snippet
```text
[VARIMA]
Estimator for Vector AutoRegressive Integrated Moving Average forecasting.
Init: VARIMA(p, d, q, with_constant=True, max_iter=50)
Input: 3D array (n_ts, max_sz, d). Variable lengths padded with np.nan at the end.
Output: Fitted model. Use .fit_predict(X, n=horizon) to get forecasts of shape (n_ts, horizon, d).
```

### Common Failure Modes
- Passing 1D or 2D arrays instead of the required 3D `(n_ts, max_sz, d)` format, which violates `tslearn` estimator conventions.
- Providing time series that are too short (e.g., only 1 non-NaN observation), which raises a `ValueError` regarding `min_size` during `.fit()` or `.predict()`.
- Failing to pad variable-length sequences with `np.nan`, leading to jagged array instantiation errors in NumPy.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.forecasting import VARIMA

# Convert raw lists of varying lengths into a properly padded 3D array
raw_data = [[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0]]
X = to_time_series_dataset(raw_data)

# Fit and forecast 3 steps ahead
model = VARIMA(1, 0, 0)
predictions = model.fit_predict(X, n=3)
```

## API Test: `accumulated_matrix`

### Signature
```python
def accumulated_matrix(s1, s2, mask, be=None)
```
_Source: tslearn/tslearn/metrics/_dtw.py:286  (+2 more definition site/overload)_

_Source doc:_ Compute the DTW accumulated cost matrix score between two time series. It is not required that both time series share the same size, but they must be the same dimension. Parameters ---------- s1 : array-like, shape=(sz1,) or (sz1, d) First time series. s2 : array-like, shape=(sz2,) or (sz2, d) Second time series. mask : array-like, shape=(sz1, sz2) Mask used to constrain the region of computation. Unconsidered cells must have False values. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- mat : array-like, shape=(sz1, sz2) Accumulated cost matrix. Non computed cells due to masking have infinite value.

### Goal
Compute the Dynamic Time Warping (DTW) accumulated cost matrix between two time series, constrained by a provided boolean mask.

### Parameters
- `s1`: First time series. Array-like of shape `(sz1,)` or `(sz1, d)`.
- `s2`: Second time series. Array-like of shape `(sz2,)` or `(sz2, d)`.
- `mask`: Array-like of shape `(sz1, sz2)` used to constrain the region of computation. Unconsidered cells must have `False` values.
- `be`, default `None`: Backend object or string (`"numpy"` or `"pytorch"`). If `None`, the backend is automatically determined by the input arrays.

### Input
- `s1` and `s2` must be array-like time series of the same feature dimension `d`. They do not need to share the same length (`sz1` and `sz2` can differ).
- `mask` must be a boolean array-like of shape `(sz1, sz2)` where `False` indicates cells to ignore.
- Inputs can be NumPy arrays or PyTorch tensors.

### Output
Returns `unspecified` — An array-like accumulated cost matrix of shape `(sz1, sz2)`. Non-computed cells due to masking have infinite values. The return type matches the chosen backend (NumPy array or PyTorch tensor).

### Valid Call Patterns
```python
import tslearn.metrics
from tslearn.utils import to_time_series
import warnings

s1 = [1, 2, 3]
s2 = [1.0, 2.0, 2.0, 3.0]
mask = tslearn.metrics.compute_mask(s1, s2, be="numpy")

# Note: This function is deprecated in favor of tslearn.metrics.dtw_accumulated_matrix
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    matrix = tslearn.metrics.dtw_variants.accumulated_matrix(
        to_time_series(s1),
        to_time_series(s2),
        mask,
        be="numpy"
    )

assert matrix.shape == (3, 4)
print("Accumulated matrix computed successfully.")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.dtw_variants.accumulated_matrix`, always provide a pre-computed boolean `mask` of shape `(sz1, sz2)`.
- Note that this function is deprecated; prefer `tslearn.metrics.dtw_accumulated_matrix` for new code.
- Ensure `s1` and `s2` have the same number of dimensions (features).

### Prompt Snippet
```text
When calling `tslearn.metrics.dtw_variants.accumulated_matrix`, you must provide a pre-computed boolean `mask` of shape `(sz1, sz2)`. Ensure `s1` and `s2` have the same feature dimension. Note that this function is deprecated in favor of `tslearn.metrics.dtw_accumulated_matrix`.
```

### Common Failure Modes
- Passing time series with different feature dimensions `d`.
- Failing to provide a `mask` argument, or providing a mask with an incorrect shape `(sz1, sz2)`.
- Mixing NumPy arrays and PyTorch tensors without explicitly specifying a compatible backend.

### Fix Code Hint
```python
import tslearn.metrics
from tslearn.utils import to_time_series
import warnings

s1 = to_time_series([1, 2, 3])
s2 = to_time_series([1.0, 2.0, 2.0, 3.0])

# Compute the required mask first
mask = tslearn.metrics.compute_mask(s1, s2)

# Call the function with the mask
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    matrix = tslearn.metrics.dtw_variants.accumulated_matrix(s1, s2, mask)
```

## API Test: `accumulated_matrix_from_dist_matrix`

### Signature
```python
def accumulated_matrix_from_dist_matrix(dist_matrix, mask, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:456_

_Source doc:_ Compute the accumulated cost matrix score between two time series using a precomputed distance matrix. Parameters ---------- dist_matrix : array-like, shape=(sz1, sz2) Array containing the pairwise distances. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- mat : array-like, shape=(sz1, sz2) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix (as used in Dynamic Time Warping) between two time series using a precomputed pairwise distance matrix and a boolean mask.

### Parameters
- `dist_matrix`: array-like, shape `(sz1, sz2)`. A 2D array containing the precomputed pairwise distances between the points of two time series.
- `mask`: array-like, shape `(sz1, sz2)`. A 2D boolean mask of the same shape as `dist_matrix`. Unconsidered cells (e.g., those outside a Sakoe-Chiba band or Itakura parallelogram) must have `False` values.
- `be`, default `None`: Backend object, string (`"numpy"` or `"pytorch"`), or `None`. Determines the computational backend. If `None`, the backend is automatically inferred from the input arrays.

### Input
The caller must provide a 2D distance matrix and a 2D boolean mask of the exact same shape `(sz1, sz2)`. The inputs can be NumPy arrays or PyTorch tensors. If using PyTorch tensors that require gradients, the PyTorch backend will be automatically selected if `be=None`.

### Output
Returns `unspecified` — an array-like (NumPy array or PyTorch tensor, depending on the backend) of shape `(sz1, sz2)` representing the accumulated cost matrix, where each cell contains the minimum cumulative cost to reach that alignment path coordinate.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import accumulated_matrix_from_dist_matrix

# 1. Define a precomputed 2D distance matrix and a matching 2D mask
dist_matrix = np.array([
    [1.0, 2.0, 5.0], 
    [3.0, 4.0, 1.0],
    [6.0, 2.0, 3.0]
])
mask = np.array([
    [True, True, False], 
    [True, True, True],
    [False, True, True]
])

# 2. Compute the accumulated cost matrix (inferred from signature)
acc_mat = accumulated_matrix_from_dist_matrix(dist_matrix, mask, be="numpy")

assert acc_mat.shape == (3, 3)
print("Accumulated Cost Matrix:\n", acc_mat)
```

### LLM Instruction Prompt
- Provide a 2D `dist_matrix` and a 2D `mask` of the exact same shape `(sz1, sz2)`.
- Ensure `mask` contains boolean values where `False` indicates cells that should be ignored during the accumulation step.
- Do not pass 3D `(n_ts, max_sz, d)` datasets directly to this low-level helper; it expects a 2D pairwise distance matrix between exactly two time series.

### Prompt Snippet
```text
When computing an accumulated cost matrix from a precomputed distance matrix in tslearn, use `accumulated_matrix_from_dist_matrix(dist_matrix, mask, be=None)`. Both `dist_matrix` and `mask` must be 2D arrays of shape `(sz1, sz2)`. The `mask` must contain `False` for unconsidered cells. The backend `be` can be `"numpy"`, `"pytorch"`, or `None` (auto-detected).
```

### Common Failure Modes
- Passing raw 1D or 3D time-series data instead of a 2D pairwise distance matrix.
- Providing a `mask` that has a different shape than `dist_matrix`, resulting in broadcasting errors or backend crashes.
- Providing a `mask` with non-boolean values that do not correctly evaluate to `False` for unconsidered cells, leading to incorrect accumulation paths.
- Attempting to compute gradients with PyTorch tensors without ensuring the inputs have `requires_grad=True` and the backend resolves to PyTorch.

### Fix Code Hint
```python
# Ensure both inputs are 2D and share the exact same shape
if dist_matrix.ndim != 2 or mask.ndim != 2:
    raise ValueError("dist_matrix and mask must be 2D arrays.")
if dist_matrix.shape != mask.shape:
    raise ValueError("dist_matrix and mask must have the same shape.")

acc_mat = accumulated_matrix_from_dist_matrix(dist_matrix, mask, be="numpy")
```

## API Test: `all`

### Signature
```python
def all(x, axis=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:90_

### Goal
Evaluates whether all elements in a backend-specific array or tensor evaluate to `True`, optionally reducing along a specified axis in a backend-agnostic manner.

### Parameters
- `x`: The input time-series array or tensor (NumPy array or PyTorch tensor) containing boolean values.
- `axis`, default `None`: The integer axis or dimension along which to perform the logical AND reduction. If `None`, the reduction is applied over all elements.

### Input
A boolean array or tensor created via backend operations. The input type must match the instantiated backend (e.g., a `numpy.ndarray` for the NumPy backend, or a `torch.Tensor` for the PyTorch backend).

### Output
Returns `unspecified` — A boolean scalar (if `axis=None`) or a reduced array/tensor of booleans, matching the type of the active backend.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend
import numpy as np

# Note: Example inferred from signature and backend conventions
be = instantiate_backend("numpy")
x = np.array([[True, True], [True, False]])

# Reduce along the columns (axis=1)
result = be.all(x, axis=1)

assert np.array_equal(result, [True, False])
print("Backend all() reduction successful.")
```

### LLM Instruction Prompt
- Call `be.all(x, axis=None)` via a backend instance created by `tslearn.backend.instantiate_backend` to compute logical AND reductions in a backend-agnostic way.
- Do not use Python's built-in `all()` on PyTorch tensors or multi-dimensional NumPy arrays if you need to compute along specific axes or maintain backend compatibility.

### Prompt Snippet
```text
When writing custom metrics or alignment functions in tslearn, use the backend's `all` method to perform logical AND reductions. This ensures your code works seamlessly with both NumPy arrays and PyTorch tensors (for automatic differentiation).
```

### Common Failure Modes
- **Axis Out of Bounds**: Passing an `axis` value that exceeds the dimensions of the input array/tensor (e.g., `axis=2` for a 2D array) will raise a backend-specific error (`ValueError` in NumPy or `IndexError` in PyTorch).
- **Using Built-in `all()`**: Attempting to pass an `axis` argument to Python's built-in `all()` function will raise a `TypeError`, as the built-in function only accepts an iterable.
- **Type Mismatch**: Passing a PyTorch tensor to a NumPy backend instance's `all` method (or vice versa) may result in unexpected behavior or crashes.

### Fix Code Hint
```python
# Instead of using Python's built-in all() which doesn't support 'axis':
# result = all(x, axis=1)  # Raises TypeError

# Use the tslearn backend instance:
from tslearn.backend import instantiate_backend
be = instantiate_backend("numpy")
result = be.all(x, axis=1)
```

## API Test: `array`

### Signature
```python
def array(self, val, dtype=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:106_

### Goal
Converts a given input value into a backend-specific array or tensor (e.g., a PyTorch tensor or NumPy array) using the instantiated backend.

### Parameters
- `self`: The instantiated backend object (e.g., `PyTorchBackend` or `NumPyBackend`) on which this method is called.
- `val`: The input data (such as a Python list, scalar, or NumPy array) to be converted into the backend's native array format.
- `dtype`, default `None`: The desired data type of the resulting array or tensor. If `None`, the data type is inferred from `val`.

### Input
The caller must provide an instantiated backend object (typically obtained via `tslearn.backend.instantiate_backend`) and an array-like input `val`. If providing a `dtype`, it must be compatible with the active backend (e.g., `torch.float64` for the PyTorch backend, or `numpy.float64` for the NumPy backend).

### Output
Returns `unspecified` — A backend-specific array object representing the input data. For the PyTorch backend, this is a `torch.Tensor`; for the NumPy backend, this is a `numpy.ndarray`.

### Valid Call Patterns
```python
import torch
from tslearn.backend import instantiate_backend

# Note: Call pattern inferred from signature and backend context
be = instantiate_backend("pytorch")
val = [[1.0, 2.0], [3.0, 4.0]]

# Convert a standard Python list to a backend-specific array (PyTorch tensor)
arr = be.array(val, dtype=torch.float64)

assert isinstance(arr, torch.Tensor)
assert arr.dtype == torch.float64
print(f"Created backend array:\n{arr}")
```

### LLM Instruction Prompt
- When generating code to create arrays for `tslearn` metrics or operations, do not call `array` as a standalone function. It must be called as a method on an instantiated backend object (e.g., `be.array(val)`). Ensure that any `dtype` provided matches the specific backend being used (e.g., `torch.dtype` for PyTorch, `numpy.dtype` for NumPy).

### Prompt Snippet
```text
# Correct usage of the backend array method
be = instantiate_backend("pytorch")
tensor_data = be.array([1, 2, 3], dtype=torch.float32)
```

### Common Failure Modes
- **Standalone Function Call:** Attempting to import and call `array(val)` directly instead of calling it as a method on a backend instance (`be.array(val)`), resulting in a `NameError` or `TypeError`.
- **Incompatible `dtype`:** Passing a PyTorch-specific `dtype` (like `torch.float32`) when the active backend is NumPy, or vice versa, causing a backend-level type error.
- **Invalid Input Shape:** Passing jagged or non-rectangular lists to `val` when the backend expects a strictly rectangular array structure.

### Fix Code Hint
```python
# BAD: Calling array directly or using the wrong dtype for the backend
# from tslearn.backend.pytorch_backend import array
# arr = array([1, 2, 3], dtype=np.float32)

# GOOD: Instantiate the backend and call its array method with a matching dtype
from tslearn.backend import instantiate_backend
import torch

be = instantiate_backend("pytorch")
arr = be.array([1, 2, 3], dtype=torch.float32)
```

## API Test: `backward`

### Signature
```python
def backward(ctx, grad_output)
```
_Source: tslearn/tslearn/metrics/soft_dtw_loss_pytorch.py:62_

### Goal
Computes the gradients of the Soft-DTW loss with respect to the input time series during the PyTorch backward pass.

### Parameters
- `ctx`: A PyTorch autograd context object (`torch.autograd.function._ContextMethodMixin`) containing saved tensors (e.g., distance matrices, alignment paths) from the forward pass.
- `grad_output`: A PyTorch tensor representing the gradient of the loss with respect to the output of the forward pass.

### Input
Requires the forward pass to have been computed using `requires_grad=True` on the input PyTorch tensors, which saves the necessary variables in the `ctx` object. The PyTorch backend must be active.

### Output
Returns `unspecified` — typically a tuple of PyTorch tensors representing the gradients with respect to the inputs of the `forward` method (e.g., `grad_x`, `grad_y`, and `None` for non-tensor arguments like `gamma`).

### Valid Call Patterns
```python
import torch
from tslearn.metrics import soft_dtw
from tslearn.metrics.soft_dtw_loss_pytorch import _SoftDTWLossPyTorch

# 1. Standard implicit invocation via PyTorch autograd engine (Recommended)
ts1 = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True)
ts2 = torch.tensor([[3.0], [4.0], [-3.0]])

# compute_with_backend=True is required to build the computation graph
sim = soft_dtw(ts1, ts2, gamma=1.0, be="pytorch", compute_with_backend=True)

# Implicitly calls _SoftDTWLossPyTorch.backward(ctx, grad_output) internally
sim.backward()

assert ts1.grad is not None, "Gradient should be populated by the backward pass"
print("Gradients successfully computed via backward pass:")
print(ts1.grad)

# 2. Direct invocation (inferred from signature, not verified)
# Note: Direct invocation is not recommended as it requires a manually 
# constructed autograd context (ctx) populated by the forward pass.
# grad_output = torch.tensor(1.0)
# grads = _SoftDTWLossPyTorch.backward(ctx, grad_output)
```

### LLM Instruction Prompt
- Do not call `backward(ctx, grad_output)` directly on the autograd function class. Instead, trigger it implicitly by calling `.backward()` on the resulting loss tensor from `soft_dtw` (with `compute_with_backend=True`) or `SoftDTWLossPyTorch`.
- Ensure input tensors have `requires_grad=True` and the PyTorch backend is active.

### Prompt Snippet
```text
DO NOT call `backward(ctx, grad_output)` directly. Trigger it implicitly by calling `.backward()` on the resulting loss tensor from `soft_dtw` (with `compute_with_backend=True`) or `SoftDTWLossPyTorch`.
```

### Common Failure Modes
- Calling `backward` directly without a valid PyTorch autograd context (`ctx`) populated by the forward pass will raise an `AttributeError` or `RuntimeError`.
- Attempting to compute gradients on tensors where `requires_grad=False` will result in `None` gradients.
- Forgetting to set `compute_with_backend=True` when using `soft_dtw` will prevent the computation graph from being built, making `.backward()` unavailable.

### Fix Code Hint
```python
# WRONG: Direct invocation without a valid context
# grads = _SoftDTWLossPyTorch.backward(ctx, grad_output)

# CORRECT: Implicit invocation via the autograd engine
sim = soft_dtw(ts1, ts2, gamma=1.0, be="pytorch", compute_with_backend=True)
sim.backward()
```

## API Test: `baseline_accuracy`

### Signature
```python
def baseline_accuracy(self, list_datasets=None, list_methods=None)
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:121_

_Source doc:_ Report baseline performances as provided by UEA/UCR website (for univariate datasets only). Parameters ---------- list_datasets: list or None (default: None) A list of strings indicating for which datasets performance should be reported. If None, performance is reported for all datasets. list_methods: list or None (default: None) A list of baselines methods for which performance should be reported. If None, performance for all baseline methods is reported. Returns ------- dict A dictionary in which keys are dataset names and associated values are themselves dictionaries that provide accuracy scores for the requested methods. Examples -------- >>> uea_ucr = UCR_UEA_datasets() >>> dict_acc = uea_ucr.baseline_accuracy( ...         list_datasets=["Adiac", "ChlorineConcentration"], ...         list_methods=["C45"]) >>> len(dict_acc) 2 >>> dict_acc["Adiac"]  # doctest: +ELLIPSIS {'C45': 0.542199...} >>> all_dict_acc = uea_ucr.baseline_accuracy() >>> len(all_dict_acc) 85

### Goal
Retrieve baseline classification accuracy scores for univariate UCR/UEA datasets across various standard machine-learning methods.

### Parameters
- `self`: An instantiated `tslearn.datasets.UCR_UEA_datasets` object.
- `list_datasets`, default `None`: A list of strings specifying the dataset names to query (e.g., `["Adiac"]`). If `None`, baseline performances for all available univariate datasets are reported.
- `list_methods`, default `None`: A list of strings specifying the baseline methods to query (e.g., `["C45", "1NN-DTW"]`). If `None`, performances for all available baseline methods are reported.

### Input
- Requires an instantiated `UCR_UEA_datasets` object to call the method.
- `list_datasets` and `list_methods` must be lists of strings (not single strings) or `None`.
- The requested datasets must be univariate; this method does not provide baselines for multivariate datasets.

### Output
Returns `dict` — A dictionary where the keys are dataset names (strings) and the values are nested dictionaries mapping baseline method names (strings) to their accuracy scores (floats).

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Instantiate the dataset loader
uea_ucr = UCR_UEA_datasets()

# Query specific datasets and methods
dict_acc = uea_ucr.baseline_accuracy(
    list_datasets=["Adiac", "ChlorineConcentration"],
    list_methods=["C45"]
)

assert len(dict_acc) == 2
assert "Adiac" in dict_acc
assert "C45" in dict_acc["Adiac"]
print(f"Adiac C45 Baseline Accuracy: {dict_acc['Adiac']['C45']:.4f}")
```

### LLM Instruction Prompt
- Call `baseline_accuracy` as an instance method on a `tslearn.datasets.UCR_UEA_datasets` object, never as a standalone function.
- Always pass lists of strings for `list_datasets` and `list_methods` if you want to filter the results; do not pass bare strings.
- Remember that this method only returns baseline accuracies for univariate datasets.

### Prompt Snippet
```text
To retrieve baseline accuracies for UCR datasets, instantiate `UCR_UEA_datasets` and call `.baseline_accuracy(list_datasets=[...], list_methods=[...])`. It returns a nested dictionary of `dataset_name -> method_name -> accuracy_float`.
```

### Common Failure Modes
- **Calling as a standalone function**: Attempting to import and call `baseline_accuracy` directly instead of calling it on a `UCR_UEA_datasets` instance.
- **Passing bare strings**: Providing a single string like `"Adiac"` instead of a list `["Adiac"]` to `list_datasets`, which can cause iteration errors or unexpected empty results.
- **Querying multivariate datasets**: Expecting baseline accuracies for multivariate datasets, which are not supported by this specific method.

### Fix Code Hint
```python
from tslearn.datasets import UCR_UEA_datasets

# CORRECT: Instantiate the class first
loader = UCR_UEA_datasets()

# CORRECT: Pass lists of strings
accuracies = loader.baseline_accuracy(
    list_datasets=["Adiac"], 
    list_methods=["C45"]
)
```

## API Test: `belongs_to_backend`

### Signature
```python
def belongs_to_backend(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:126  (+1 more definition site/overload)_

### Goal
Determine whether a given data object (such as an array or tensor) is a native type belonging to the instantiated computational backend (NumPy or PyTorch).

### Parameters
- `x`: The data object (e.g., time-series array, distance matrix, or scalar) to evaluate for backend compatibility.

### Input
Any Python object, typically a `numpy.ndarray` or `torch.Tensor` representing time-series data, distance matrices, or metric outputs.

### Output
Returns `unspecified` (implicitly a boolean) — `True` if the object `x` is a native data structure for the specific backend instance (e.g., a NumPy array for `NumPyBackend`, or a PyTorch tensor for `PyTorchBackend`), and `False` otherwise.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Instantiate the NumPy backend
backend = instantiate_backend("numpy")
matrix = np.array([[0.0, 1.0], [1.0, 0.0]])

# Verify the matrix belongs to the backend
is_native = backend.belongs_to_backend(matrix)
assert is_native is True
print(f"Matrix belongs to backend: {is_native}")
```

### LLM Instruction Prompt
- Call `belongs_to_backend(x)` as a method on an instantiated backend object (e.g., `backend.belongs_to_backend(x)`), not as a standalone module-level function.
- Use this method to verify that metric outputs or time-series arrays match the expected backend type (NumPy array or PyTorch tensor) before performing backend-specific operations like `.backward()`.

### Prompt Snippet
```text
Call `backend.belongs_to_backend(x)` on an instantiated backend object to check if `x` is a native array/tensor type for that backend (returns a boolean). Do not call it as a standalone function.
```

### Common Failure Modes
- **Calling as a standalone function**: Attempting to import and call `belongs_to_backend(x)` directly from `tslearn.backend` or `tslearn.metrics` instead of calling it on a backend instance returned by `instantiate_backend`.
- **Assuming implicit conversion**: Passing a NumPy array to a PyTorch backend's `belongs_to_backend` method will return `False`; it checks the type strictly and does not convert the array.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend
import torch

# Correct: Call on the backend instance
backend = instantiate_backend("pytorch")
tensor_data = torch.tensor([[1.0, 2.0]])

# Check if the object is a native PyTorch tensor
if backend.belongs_to_backend(tensor_data):
    print("Data is compatible with the PyTorch backend.")
```

## API Test: `build`

### Signature
```python
def build(self, input_shape)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:188_

### Goal
Initializes the internal weights or computational graph for a shapelet-based neural network layer or model, given the expected shape of the input time-series data.

### Parameters
- `self`: The instance of the shapelet model or internal neural network layer (e.g., a custom layer used within `tslearn.shapelets.LearningShapelets`).
- `input_shape`: A tuple of integers representing the expected dimensions of the input data.

### Input
A tuple representing the shape of the time-series data. Based on `tslearn` conventions, time-series datasets are strictly formatted as 3D arrays `(n_ts, max_sz, d)`. The `input_shape` typically corresponds to this format or the per-sample `(max_sz, d)` shape required by the underlying neural network backend (e.g., Keras/TensorFlow).

### Output
Returns `unspecified` — typically returns `None` and modifies the instance in-place by allocating internal weights or resources.

### Valid Call Patterns
```python
from tslearn.shapelets import LearningShapelets

# Inferred from signature (not verified)
# Note: `build` is typically an internal method (e.g., for custom neural network layers) 
# and is called automatically during the `fit` process of LearningShapelets.
estimator = LearningShapelets(n_shapelets_per_size={10: 5})

# Example of how it might be called if exposed on the estimator or an internal layer
if hasattr(estimator, "build"):
    estimator.build(input_shape=(10, 50, 1))
    print("Successfully called build on estimator.")
else:
    print("build is an internal method on a shapelet layer class, invoked during fit().")
```

### LLM Instruction Prompt
- Recognize that `build(self, input_shape)` is a method on a shapelet-related class (likely an internal neural network layer used by `LearningShapelets`).
- Do not call `build` manually in standard machine-learning pipelines; rely on `fit()` to automatically build and train the model.
- If interacting with internal layers, ensure `input_shape` correctly reflects the 3D time-series format `(n_ts, max_sz, d)` or the specific tensor shape expected by the layer.

### Prompt Snippet
```text
The `build(self, input_shape)` method in `tslearn.shapelets` initializes the internal weights or architecture for a shapelet model or layer. It is typically invoked automatically during `fit()`. If called manually on an internal layer, `input_shape` must be a tuple representing the expected data dimensions.
```

### Common Failure Modes
- **Standalone Call:** Attempting to call `build(input_shape)` as a standalone function instead of a method on a class instance (e.g., `layer.build(...)`).
- **Incorrect Shape Format:** Providing an `input_shape` that does not align with `tslearn`'s strict 3D array requirement `(n_ts, max_sz, d)` or the specific backend's expected tensor shape.
- **Manual Invocation:** Manually calling `build` on an already fitted model or layer, which may inadvertently reset learned shapelet weights or cause backend-specific errors.

### Fix Code Hint
```python
# Instead of calling build manually, use the standard scikit-learn fit() method,
# which handles data formatting and internal building automatically.
from tslearn.utils import to_time_series_dataset

# Ensure data is in the strict (n_ts, max_sz, d) 3D format
X_3d = to_time_series_dataset(X_raw)
estimator.fit(X_3d, y)
```

## API Test: `cache_all`

### Signature
```python
def cache_all(self)
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:376_

_Source doc:_ Cache all datasets from the UCR/UEA archive for later use.

### Goal
Cache all time-series datasets from the UCR/UEA archive to the local disk for later offline use.

### Parameters
- `self`: The `UCR_UEA_datasets` instance on which this method is called.

### Input
No arguments are required. The environment must have an active internet connection and sufficient disk space to download and store the entire archive.

### Output
Returns `unspecified` (typically `None`). The side effect is that the datasets are downloaded and saved to the local `tslearn` data directory.

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Inferred from signature (not verified by tests/README)
loader = UCR_UEA_datasets()

# We assert the method exists rather than calling it, 
# to avoid downloading the entire archive and violating network constraints.
assert callable(loader.cache_all), "cache_all must be a callable method on UCR_UEA_datasets"
print("UCR_UEA_datasets.cache_all is available.")
```

### LLM Instruction Prompt
- Call `cache_all` on an instance of `UCR_UEA_datasets`, not the class itself.
- Avoid generating calls to `cache_all` in automated tests, CI pipelines, or constrained environments, as it initiates a massive network download of the entire UCR/UEA archive.

### Prompt Snippet
```text
from tslearn.datasets import UCR_UEA_datasets
loader = UCR_UEA_datasets()
# loader.cache_all() # Downloads all datasets to local cache
```

### Common Failure Modes
- **Network/Timeout Errors:** The UCR/UEA server may be down, unreachable, or rate-limiting requests, causing the download to fail.
- **Disk Space Exhaustion:** The full archive is large; downloading it may fill up the local disk.
- **Missing Instance:** Calling `UCR_UEA_datasets.cache_all()` directly on the class instead of an instance raises a `TypeError` because `self` is not provided.

### Fix Code Hint
```python
from tslearn.datasets import UCR_UEA_datasets

# Correct: Instantiate the loader first
loader = UCR_UEA_datasets()
try:
    # loader.cache_all()
    pass
except Exception as e:
    print(f"Download failed: {e}")
```

## API Test: `call`

### Signature
```python
def call(self, inputs, mask=None)
def call(self, inputs)
def call(self, x, **kwargs)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:89  (+3 more definition site/overload)_

### Goal
Executes the forward pass of an internal neural network layer (such as those used in `tslearn.shapelets`), applying its specific transformation to the input time-series data.

### Parameters
- `self`: The instance of the neural network layer or model.
- `inputs`: The input time-series tensor or array to be processed by the layer.
- `mask`, default `None`: An optional boolean tensor indicating which timesteps should be masked out or ignored during the forward pass.

### Input
A 3D tensor of time-series data, typically formatted as `(batch_size, max_sz, d)`, compatible with the underlying neural network backend (e.g., Keras/TensorFlow).

### Output
Returns `unspecified` — The transformed tensor after applying the layer's operations (e.g., computed shapelet distances or pooled features).

### Valid Call Patterns
```python
# Inferred from signature (not verified)
# `call` is an internal method of neural network layers in `tslearn.shapelets`.
# It is typically invoked automatically by the backend framework (e.g., Keras) 
# during model training and prediction, rather than being called directly.

class DummyLayer:
    def call(self, inputs, mask=None):
        return inputs

layer = DummyLayer()
inputs = [[[1.0], [2.0]]]
outputs = layer.call(inputs)

assert outputs == inputs
print("call() executed successfully.")
```

### LLM Instruction Prompt
- Do not call `call` directly on `tslearn` estimators. It is an internal method of neural network layers (e.g., Keras layers used in `LearningShapelets`). Use standard `scikit-learn` methods like `fit()`, `predict()`, or `transform()` on the top-level estimators instead.

### Prompt Snippet
```text
`call` is an internal forward-pass method for neural network layers in `tslearn.shapelets`. End-users should not invoke it directly; use `fit()` and `predict()` on the `LearningShapelets` estimator.
```

### Common Failure Modes
- Calling `call` directly on a top-level estimator like `LearningShapelets` will fail with an `AttributeError`, as it is a method of the internal layer/model objects, not the `scikit-learn` compatible wrapper.
- Passing incorrectly formatted data (not a 3D tensor) to the internal layer's `call` method will result in backend-specific shape mismatch errors.

### Fix Code Hint
```python
# Instead of trying to use .call() on an estimator:
# model.call(X)  # Anti-pattern

# Use the standard scikit-learn API:
# predictions = model.predict(X)
```

## API Test: `cast`

### Signature
```python
def cast(data, array_type='numpy')
def cast(self, x, dtype)
def cast(x, dtype)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:129  (+2 more definition site/overload)_

### Goal
Cast time-series data to a standard Python list or a specific computational backend array type (NumPy or PyTorch).

### Parameters
- `data`: array-like — The input time-series data to cast. Can be a list, NumPy array, or PyTorch tensor.
- `array_type`: string — The target format to cast the data into. Must be `"numpy"`, `"pytorch"`, or `"list"`. Defaults to `"numpy"`.
- `self`: Backend instance — The backend object (used in internal backend-specific overloads).
- `x`: array-like — The input data to cast (used in internal backend-specific overloads).
- `dtype`: string or type — The target data type (used in internal backend-specific overloads).

### Input
Array-like time-series data, such as a standard Python list of numbers, a `numpy.ndarray`, or a `torch.Tensor`.

### Output
Returns `unspecified` — The input data cast to the requested `array_type` (a Python `list`, a `numpy.ndarray`, or a `torch.Tensor`).

### Valid Call Patterns
```python
from tslearn.backend import cast
import numpy as np

# Cast a standard Python list to a NumPy array
s1 = cast([1, 2, 3], array_type="numpy")
assert isinstance(s1, np.ndarray)
assert s1.shape == (3,)

# Cast a list of floats to a standard Python list
s2 = cast([1.0, 2.0, 3.0], array_type="list")
assert isinstance(s2, list)
```

### LLM Instruction Prompt
- Use `cast(data, array_type="numpy")` to convert raw time-series data into a specific backend format.
- The `array_type` parameter strictly accepts `"numpy"`, `"pytorch"`, or `"list"`.
- The `cast(self, x, dtype)` and `cast(x, dtype)` signatures are internal backend-specific overloads; always prefer the top-level `cast(data, array_type)` function for general use.

### Prompt Snippet
```text
`tslearn.backend.cast(data, array_type='numpy')` converts array-like time-series data to a list, numpy array, or torch tensor. `array_type` must be "numpy", "pytorch", or "list".
```

### Common Failure Modes
- Providing an invalid `array_type` string (e.g., `"ndarray"` or `"torch"` instead of `"numpy"` or `"pytorch"`).
- Calling the internal backend method `cast(self, x, dtype)` directly instead of the top-level `cast(data, array_type)`.
- Attempting to cast to `"pytorch"` in an environment where the PyTorch library is not installed.

### Fix Code Hint
```python
from tslearn.backend import cast

# WRONG: cast(data, "ndarray") or cast(data, "torch")
# RIGHT: Use exactly "numpy", "pytorch", or "list"
data_np = cast([1.0, 2.0, 3.0], array_type="numpy")
```

## API Test: `cdist`

### Signature
```python
def cdist(x, y, metric='euclidean', p=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:135_

### Goal
Computes the pairwise distance matrix between two collections of observations, implemented as a PyTorch backend helper to support automatic differentiation.

### Parameters
- `x`: A 2D PyTorch tensor of shape `(n_samples_x, n_features)` representing the first collection of observations.
- `y`: A 2D PyTorch tensor of shape `(n_samples_y, n_features)` representing the second collection of observations.
- `metric`, default `'euclidean'`: A string indicating the distance metric to compute (e.g., `'euclidean'`, `'sqeuclidean'`).
- `p`, default `None`: The power parameter for the Minkowski metric (if applicable).

### Input
Two 2D PyTorch tensors `x` and `y` with the same number of features (columns). Unlike high-level `tslearn` estimators, this low-level backend helper expects 2D inputs, not 3D time-series arrays.

### Output
Returns a 2D PyTorch tensor of shape `(n_samples_x, n_samples_y)` containing the pairwise distances between the observations in `x` and `y`. If `x` requires gradients, the output tensor will be attached to a computation graph.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import PyTorchBackend

# cdist is implemented as an instance method on the backend class
be = PyTorchBackend()
cdist = be.cdist

x = torch.tensor([[0.0, 0.0], [1.0, 1.0]], requires_grad=True)
y = torch.tensor([[0.0, 1.0]])

# Compute pairwise Euclidean distances
dist_matrix = cdist(x, y, metric="euclidean")

assert dist_matrix.shape == (2, 1)
assert dist_matrix.requires_grad
print(dist_matrix)
```

### LLM Instruction Prompt
- Access `cdist` via a backend instance (e.g., `PyTorchBackend().cdist(x, y)` or `instantiate_backend("pytorch").cdist(x, y)`) rather than importing it as a standalone module-level function.
- Ensure inputs `x` and `y` are 2D tensors `(n_samples, n_features)`, not the standard 3D `(n_ts, max_sz, d)` time-series format used by `tslearn` estimators.
- Use this backend helper when you need pairwise distances that preserve PyTorch computation graphs for automatic differentiation.

### Prompt Snippet
```text
import torch
from tslearn.backend import instantiate_backend

be = instantiate_backend("pytorch")
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
y = torch.tensor([[1.0, 2.0]])

# Compute pairwise distances using the PyTorch backend
dist_matrix = be.cdist(x, y, metric="euclidean")
dist_matrix.sum().backward()
```

### Common Failure Modes
- **Standalone Import**: Attempting to `from tslearn.backend.pytorch_backend import cdist` will fail because `cdist` is an instance method of the backend class, not a module-level function.
- **3D Array Input**: Passing a 3D time-series dataset `(n_ts, max_sz, d)` directly to `cdist` will cause a shape mismatch; it strictly expects 2D inputs `(n_samples, n_features)`.
- **Type Mismatch**: Passing NumPy arrays to the PyTorch backend's `cdist` method will raise a TypeError; inputs must be PyTorch tensors.

### Fix Code Hint
```python
# FIX: Reshape 3D time-series data to 2D before calling cdist, 
# and ensure you are using the correct backend instance method.
import torch
from tslearn.backend import instantiate_backend

be = instantiate_backend("pytorch")
x_3d = torch.randn(10, 5, 1)
y_3d = torch.randn(3, 5, 1)

# Reshape to (n_samples, n_features)
x_2d = x_3d.reshape(x_3d.shape[0], -1)
y_2d = y_3d.reshape(y_3d.shape[0], -1)

dist_matrix = be.cdist(x_2d, y_2d, metric="euclidean")
```

## API Test: `cdist_ctw`

### Signature
```python
def cdist_ctw(dataset1, dataset2=None, max_iter=100, n_components=None, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, n_jobs=None, verbose=0, be=None)
```
_Source: tslearn/tslearn/metrics/ctw.py:302_

_Source doc:_ Compute cross-similarity matrix using Canonical Time Warping (CTW) similarity measure. Canonical Time Warping is a method to align time series under rigid registration of the feature space. It should not be confused with Dynamic Time Warping (DTW), though CTW uses DTW. It is not required that both time series share the same size, nor the same dimension (CTW will find a subspace that best aligns feature spaces). CTW was originally presented in [1]_. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz1, d) or (n_ts1, sz1) or (sz1,) A dataset of time series. If shape is (n_ts1, sz1), the dataset is composed of univariate time series. If shape is (sz1,), the dataset is composed of a unique univariate time series. dataset2 : None or array-like, shape=(n_ts2, sz2, d) or (n_ts2, sz2) or (sz2,) (default: None) Another dataset of time series. If `None`, self-similarity of `dataset1` is returned. If shape is (n_ts2, sz2), the dataset is composed of univariate time series. If shape is (sz2,), the dataset is composed of a unique univariate time series. max_iter : int (default: 100) Number of iterations for the CTW algorithm. Each iteration n_components : int (default: None) Number of components to be used for Canonical Correlation Analysis. If None, the lower minimum number of features between seq1 and seq2 is used. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for DTW calls. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n-jobs>`__ for more details. verbose : int, optional (default=0) The verbosity level: if non zero, progress messages are printed. Above 50, the output is sent to stdout. The frequency of the messages increases with the verbosity level. If it more than 10, all iterations are reported.

### Goal
Compute the pairwise cross-similarity matrix between two collections of time series using Canonical Time Warping (CTW), which aligns time series even if they have different feature dimensions.

### Parameters
- `dataset1`: array-like, shape `(n_ts1, sz1, d1)` or `(n_ts1, sz1)` or `(sz1,)`. The first dataset of time series.
- `dataset2`, default `None`: array-like, shape `(n_ts2, sz2, d2)` or `(n_ts2, sz2)` or `(sz2,)`. The second dataset of time series. If `None`, computes the self-similarity matrix of `dataset1`.
- `max_iter`, default `100`: int. The maximum number of iterations for the CTW algorithm to converge.
- `n_components`, default `None`: int. The number of components to use for Canonical Correlation Analysis (CCA). If `None`, defaults to the minimum number of features between the two datasets.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. The global constraint to restrict admissible paths during the underlying DTW calls.
- `sakoe_chiba_radius`, default `None`: int or `None`. The radius for the Sakoe-Chiba band constraint. If `None` but `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: float or `None`. The maximum slope for the Itakura parallelogram constraint. If `None` but `global_constraint="itakura"`, defaults to 2.0.
- `n_jobs`, default `None`: int or `None`. The number of parallel jobs to run. `-1` uses all available processors.
- `verbose`, default `0`: int. The verbosity level for printing progress messages.
- `be`, default `None`: Backend identifier (e.g., `"numpy"`, `"pytorch"`) or a backend instance. If `None`, defaults to NumPy unless PyTorch tensors are passed.

### Input
Two datasets of time series. Unlike standard DTW, CTW does not require the time series to share the same feature dimension (`d1` can be different from `d2`), nor the same length. Data should ideally be formatted as 3D arrays `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`, though 1D and 2D arrays are accepted and internally expanded.

### Output
Returns `unspecified` — A 2D array (or tensor, depending on the backend) of shape `(n_ts1, n_ts2)` containing the pairwise CTW distances between the time series in `dataset1` and `dataset2`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import cdist_ctw

# 2 time series, length 5, dimension 2
dataset1 = np.array([
    [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0], [5.0, 6.0]],
    [[0.0, 1.0], [1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]]
])

# 3 time series, length 4, dimension 3 (different length and dimension)
dataset2 = np.array([
    [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0]],
    [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0]],
    [[2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0], [5.0, 5.0, 5.0]]
])

# Inferred from signature
dist_matrix = cdist_ctw(dataset1, dataset2, max_iter=5)

assert dist_matrix.shape == (2, 3)
print(f"CTW distance matrix shape: {dist_matrix.shape}")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.cdist_ctw` to compute pairwise Canonical Time Warping distances between two sets of time series.
- CTW is specifically designed to align time series that exist in different feature spaces (i.e., `dataset1` and `dataset2` can have different feature dimensions `d`).
- Pass `dataset2=None` to compute the self-similarity matrix of `dataset1`.
- Keep `max_iter` small (e.g., 5-10) in testing environments to avoid long execution times, as CTW involves iterative Canonical Correlation Analysis (CCA) and DTW.

### Prompt Snippet
```text
Compute the pairwise Canonical Time Warping (CTW) distance matrix between `X_train` (dimension 2) and `X_test` (dimension 3) using `tslearn.metrics.cdist_ctw`. Limit the iterations to 10.
```

### Common Failure Modes
- **Conflicting Constraints**: Setting `sakoe_chiba_radius` while `global_constraint` is set to `"itakura"` (or vice versa) will cause a `RuntimeWarning` and result in no global constraint being applied.
- **Invalid `n_components`**: Providing an `n_components` value that is strictly greater than the minimum feature dimension of `dataset1` and `dataset2` will cause the underlying CCA to fail.
- **Missing PyTorch**: Requesting `be="pytorch"` in an environment where `torch` is not installed will fall back to NumPy or raise an error depending on the exact backend instantiation flow.

### Fix Code Hint
```python
# Ensure n_components is valid if explicitly provided
min_features = min(dataset1.shape[-1], dataset2.shape[-1])
n_comp = min(requested_components, min_features)

# Compute the cross-distance matrix
dist_matrix = cdist_ctw(
    dataset1, 
    dataset2, 
    max_iter=10, 
    n_components=n_comp,
    global_constraint="sakoe_chiba", 
    sakoe_chiba_radius=3
)
```

## API Test: `cdist_dtw`

### Signature
```python
def cdist_dtw(dataset1, dataset2=None, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, n_jobs=None, verbose=0, be=None)
```
_Source: tslearn/tslearn/metrics/_dtw.py:639  (+1 more definition site/overload)_

### Goal
Compute the cross-similarity matrix between two time-series datasets (or the self-similarity matrix of a single dataset) using the Dynamic Time Warping (DTW) distance metric.

### Parameters
- `dataset1`: array-like, shape `(n_ts1, sz1, d)` or `(n_ts1, sz1)` or `(sz1,)`. The primary dataset of time series. If 2D or 1D, it is treated as univariate.
- `dataset2`, default `None`: array-like, shape `(n_ts2, sz2, d)` or `(n_ts2, sz2)` or `(sz2,)`. A secondary dataset of time series. If `None`, the self-similarity matrix of `dataset1` is computed.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. The global constraint to restrict admissible alignment paths for DTW.
- `sakoe_chiba_radius`, default `None`: `int` or `None`. The radius (window size) for the Sakoe-Chiba band constraint. If `global_constraint="sakoe_chiba"` and this is `None`, defaults to 1.
- `itakura_max_slope`, default `None`: `float` or `None`. The maximum slope for the Itakura parallelogram constraint. If `global_constraint="itakura"` and this is `None`, defaults to 2.0.
- `n_jobs`, default `None`: `int` or `None`. The number of parallel jobs to run. `None` means 1, `-1` means all processors.
- `verbose`, default `0`: `int`. The verbosity level during computation.
- `be`, default `None`: `str` or Backend object. The backend to use (e.g., `"numpy"`, `"pytorch"`). Auto-detected if inputs are PyTorch tensors.

### Input
Time-series datasets formatted as NumPy arrays or PyTorch tensors. Ideally, inputs should be strictly formatted as 3D arrays `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`. `dataset1` and `dataset2` do not need to share the same time-series length (`sz1` vs `sz2`), but they **must** share the same feature dimension `d`.

### Output
Returns `unspecified` — A 2D array (matrix) of shape `(n_ts1, n_ts2)` containing the pairwise DTW distances as floats. If `dataset2` is `None`, returns a symmetric matrix of shape `(n_ts1, n_ts1)`. If the PyTorch backend is used, this returns a PyTorch tensor attached to a computation graph.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import cdist_dtw

# 1. Cross-similarity between two datasets
X = np.array([[[1.0], [2.0]], [[3.0], [4.0]]]) # shape: (2, 2, 1)
Y = np.array([[[1.0], [2.0]], [[5.0], [6.0]], [[7.0], [8.0]]]) # shape: (3, 2, 1)

dist_matrix = cdist_dtw(X, Y)
assert dist_matrix.shape == (2, 3)
assert dist_matrix[0, 0] == 0.0  # X[0] and Y[0] are identical

# 2. Self-similarity of a single dataset with a global constraint
self_dist_matrix = cdist_dtw(X, global_constraint="sakoe_chiba", sakoe_chiba_radius=1)
assert self_dist_matrix.shape == (2, 2)
assert self_dist_matrix[0, 0] == 0.0
```

### LLM Instruction Prompt
- Use `cdist_dtw` to compute pairwise distance matrices between collections of time series. Do not use it to compute the distance between two individual time series (use `tslearn.metrics.dtw` for scalars).
- Ensure both datasets have the exact same feature dimensionality `d` (the third dimension of the `(n_ts, max_sz, d)` shape).
- To speed up computation or prevent pathological warpings, provide `global_constraint="sakoe_chiba"` along with an appropriate `sakoe_chiba_radius`.

### Prompt Snippet
```text
When computing pairwise DTW distances for clustering or k-NN, use `tslearn.metrics.cdist_dtw(dataset1, dataset2)`. Ensure inputs are 3D arrays `(n_ts, max_sz, d)`. If comparing a dataset against itself, omit `dataset2`.
```

### Common Failure Modes
- **Dimensionality Mismatch:** Passing `dataset1` with `d=1` (univariate) and `dataset2` with `d=3` (multivariate) will raise an error. Both datasets must have the same number of features.
- **Scalar Expectation:** Calling `cdist_dtw` on two single 1D time series expecting a scalar float. It will return a `(1, 1)` matrix instead.
- **Conflicting Constraints:** Setting both `sakoe_chiba_radius` and `itakura_max_slope` without explicitly setting `global_constraint` will raise a `RuntimeWarning` and default to no constraint.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import cdist_dtw

# Ensure inputs are strictly 3D (n_ts, max_sz, d) before computing the matrix
X_formatted = to_time_series_dataset(X_raw)
Y_formatted = to_time_series_dataset(Y_raw)

# Compute cross-similarity matrix
distance_matrix = cdist_dtw(X_formatted, Y_formatted, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
```

## API Test: `cdist_frechet`

### Signature
```python
def cdist_frechet(dataset1, dataset2=None, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, n_jobs=None, verbose=0, be=None)
```
_Source: tslearn/tslearn/metrics/_frechet.py:647_

### Goal
Compute the cross-similarity matrix between two collections of time series using the discrete Fréchet distance, which measures the maximum distance between aligned points on an optimal path.

### Parameters
- `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of time series.
- `dataset2`, default `None`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`. The second dataset of time series. If `None`, the self-similarity matrix of `dataset1` is computed.
- `global_constraint`, default `None`: String `{"itakura", "sakoe_chiba"}` or `None`. The global constraint to restrict admissible alignment paths.
- `sakoe_chiba_radius`, default `None`: Integer or `None`. The radius for the Sakoe-Chiba band constraint (controls how far in time the alignment can deviate). Defaults to 1 if `global_constraint="sakoe_chiba"` and this is `None`.
- `itakura_max_slope`, default `None`: Float or `None`. The maximum slope for the Itakura parallelogram constraint. Defaults to 2.0 if `global_constraint="itakura"` and this is `None`.
- `n_jobs`, default `None`: Integer or `None`. The number of parallel jobs to run. `None` means 1, and `-1` means using all available processors.
- `verbose`, default `0`: Integer controlling the verbosity level of the parallel execution.
- `be`, default `None`: String (`"numpy"`, `"pytorch"`) or backend instance. Dynamically selects the computational backend. If `None`, it auto-detects based on input types or defaults to NumPy.

### Input
The caller must provide time-series datasets, ideally formatted as strict 3D arrays of shape `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`. The two datasets can have different numbers of time series (`n_ts1` vs `n_ts2`) and different maximum lengths (`sz1` vs `sz2`), but they **must** share the exact same feature dimension `d`. Variable-length time series within a dataset should be padded with `nan` values.

### Output
Returns `unspecified` — A 2D cross-similarity matrix of shape `(n_ts1, n_ts2)` (or `(n_ts1, n_ts1)` if `dataset2` is `None`) containing the pairwise Fréchet distances as floats. The return type is a NumPy array or a PyTorch tensor, depending on the selected backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import cdist_frechet
from tslearn.utils import to_time_series_dataset

# Inferred from signature (no verbatim example in context)
X = to_time_series_dataset([[1.0, 2.0, 3.0], [1.0, 2.0, 2.0, 3.0]])
Y = to_time_series_dataset([[1.0, 0.0, 2.0, 4.0]])

# Compute cross-similarity matrix between X (2 series) and Y (1 series)
dist_matrix = cdist_frechet(X, Y)
assert dist_matrix.shape == (2, 1)

# Compute self-similarity matrix of X
self_dist_matrix = cdist_frechet(X)
assert self_dist_matrix.shape == (2, 2)
np.testing.assert_allclose(np.diag(self_dist_matrix), [0.0, 0.0], atol=1e-5)
```

### LLM Instruction Prompt
- When calling `cdist_frechet`, ensure both `dataset1` and `dataset2` are formatted as 3D arrays `(n_ts, max_sz, d)`.
- You must guarantee that the feature dimension `d` is identical between `dataset1` and `dataset2`.
- If you want to compute pairwise distances within a single dataset, omit `dataset2` (leave it as `None`) rather than passing the same dataset twice, as it is more efficient.

### Prompt Snippet
```text
Ensure time series datasets passed to `cdist_frechet` share the same feature dimension `d`. Use `tslearn.utils.to_time_series_dataset` to format raw lists into the required `(n_ts, max_sz, d)` shape before computing the distance matrix.
```

### Common Failure Modes
- **Dimension Mismatch (`ValueError`)**: Passing datasets with different feature dimensions (e.g., `dataset1` has shape `(3, 10, 1)` and `dataset2` has shape `(3, 10, 2)`). The Fréchet distance requires points to be in the same dimensional space.
- **Ambiguous Constraints (`RuntimeWarning`)**: Setting both `sakoe_chiba_radius` and `itakura_max_slope` while leaving `global_constraint=None`. The function will raise a warning and ignore both constraints.
- **Unformatted Inputs**: Passing raw lists of lists with varying lengths without first converting them via `to_time_series_dataset`, which can cause NumPy array creation failures or incorrect distance calculations.

### Fix Code Hint
```python
# FIX: Ensure both datasets are properly formatted and share the same dimension 'd'
from tslearn.utils import to_time_series_dataset

# Convert raw lists to (n_ts, max_sz, d) arrays
dataset1_3d = to_time_series_dataset(raw_dataset1)
dataset2_3d = to_time_series_dataset(raw_dataset2)

# Verify feature dimensions match before calling
if dataset1_3d.shape[2] != dataset2_3d.shape[2]:
    raise ValueError("Datasets must have the same feature dimension.")

matrix = cdist_frechet(dataset1_3d, dataset2_3d, global_constraint="sakoe_chiba", sakoe_chiba_radius=2)
```

## API Test: `cdist_gak`

### Signature
```python
def cdist_gak(dataset1, dataset2=None, sigma=1.0, n_jobs=None, verbose=0, be=None)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:270  (+1 more definition site/overload)_

### Goal
Compute the cross-similarity matrix between two collections of time series using the Global Alignment Kernel (GAK).

### Parameters
- `dataset1`: A dataset of time series (array-like).
- `dataset2`, default `None`: Another dataset of time series (array-like). If `None`, the self-similarity matrix of `dataset1` is computed.
- `sigma`, default `1.0`: Bandwidth of the internal Gaussian kernel used for GAK (float).
- `n_jobs`, default `None`: The number of jobs to run in parallel (int or `None`). `None` means 1, `-1` means using all processors.
- `verbose`, default `0`: The verbosity level for progress messages (int).
- `be`, default `None`: The backend to use for computation. Can be the string `"numpy"`, `"pytorch"`, a Backend instance, or `None` to auto-detect based on input types.

### Input
- Time-series datasets formatted as 3D arrays `(n_ts, max_sz, d)`, 2D arrays `(n_ts, max_sz)` for univariate series, or 1D arrays `(max_sz,)` for a single univariate series.
- Variable-length time series should be padded with `nan` values (e.g., via `tslearn.utils.to_time_series_dataset`).
- `sigma` must be strictly greater than `0` to avoid division by zero.

### Output
Returns `array-like` — A 2D cross-similarity matrix of shape `(n_ts1, n_ts2)` as a NumPy array or PyTorch tensor (depending on the backend). Note that GAK returns similarities (larger values mean more similar), not distances.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

dataset1 = [[1, 2, 2, 3], [1.0, 2.0, 3.0, 4.0]]
dataset2 = [[1, 2, 2], [1.0, 2.0, 3.0, 4.0], [1, 2, 2, 3]]

# Compute self-similarity matrix
self_sim_matrix = tslearn.metrics.cdist_gak(dataset1, sigma=2.0)
assert self_sim_matrix.shape == (2, 2)
np.testing.assert_allclose(self_sim_matrix[0, 1], 0.65629661, atol=1e-5)

# Compute cross-similarity matrix
cross_sim_matrix = tslearn.metrics.cdist_gak(dataset1, dataset2, sigma=2.0)
assert cross_sim_matrix.shape == (2, 3)
np.testing.assert_allclose(cross_sim_matrix[1, 1], 1.0, atol=1e-5)

print("GAK similarity matrices computed successfully.")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.cdist_gak` to compute the Global Alignment Kernel similarity matrix between time-series datasets.
- Remember that GAK computes *similarities*, not distances. Larger values indicate greater similarity.
- Ensure `sigma > 0`. Passing `sigma=0` will raise a `ZeroDivisionError`.
- To compute a self-similarity matrix, pass only `dataset1` and leave `dataset2=None`.

### Prompt Snippet
```text
Use `tslearn.metrics.cdist_gak(dataset1, dataset2=None, sigma=1.0)` to compute the Global Alignment Kernel cross-similarity matrix. Note that GAK returns similarities (larger is more similar), not distances. Ensure `sigma > 0` to avoid `ZeroDivisionError`.
```

### Common Failure Modes
- **`ZeroDivisionError`**: Occurs if `sigma=0` is passed. `sigma` must be strictly positive.
- **Inconsistent Dimensions**: Passing raw lists of lists with varying lengths without first converting them to a padded 3D array using `tslearn.utils.to_time_series_dataset`.
- **Misinterpreting Output**: Treating the output as a distance matrix (where 0 means identical) instead of a similarity matrix (where larger values mean identical/similar).

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
import tslearn.metrics

# Ensure data is properly formatted and sigma > 0
X1 = to_time_series_dataset([[1, 2, 3], [1, 2]])
X2 = to_time_series_dataset([[1, 2, 3, 4]])

# Compute similarity matrix (larger values = more similar)
sim_matrix = tslearn.metrics.cdist_gak(X1, X2, sigma=1.0)
```

## API Test: `cdist_normalized_cc`

### Signature
```python
def cdist_normalized_cc(dataset1, dataset2, norms1, norms2, self_similarity)
```
_Source: tslearn/tslearn/metrics/cycc.py:54_

_Source doc:_ Compute the distance matrix between two time series dataset. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz, d), dtype=float64 A dataset of time series. dataset2 : array-like, shape=(n_ts2, sz, d), dtype=float64 Another dataset of time series. norms1 : array-like, shape=(n_ts1,), dtype=float64 norms2 : array-like, shape=(n_ts2,), dtype=float64 self_similarity : bool Returns ------- dists : array-like, shape=(n_ts1, n_ts2), dtype=float64

### Goal
Compute the pairwise distance matrix between two time-series datasets using normalized cross-correlation, utilizing a low-level Cython backend helper.

### Parameters
- `dataset1`: A dataset of time series, formatted as a 3D array-like of shape `(n_ts1, sz, d)` and dtype `float64`.
- `dataset2`: Another dataset of time series, formatted as a 3D array-like of shape `(n_ts2, sz, d)` and dtype `float64`.
- `norms1`: Precomputed norms for the first dataset, formatted as a 1D array-like of shape `(n_ts1,)` and dtype `float64`.
- `norms2`: Precomputed norms for the second dataset, formatted as a 1D array-like of shape `(n_ts2,)` and dtype `float64`.
- `self_similarity`: A boolean flag indicating whether `dataset1` and `dataset2` are the same dataset (allows optimization by computing only the necessary triangle of the distance matrix).

### Input
- `dataset1` and `dataset2` must be strictly 3D NumPy arrays `(n_ts, max_sz, d)` of type `float64`. If you have raw lists or 2D arrays, they must be converted using `tslearn.utils.to_time_series_dataset` first.
- `norms1` and `norms2` must be 1D NumPy arrays of type `float64` containing the precomputed norms for each time series in the respective datasets.
- `self_similarity` must be a standard Python `bool`.

### Output
Returns `unspecified` — A 2D NumPy array of shape `(n_ts1, n_ts2)` and dtype `float64` representing the pairwise normalized cross-correlation distances between the time series in `dataset1` and `dataset2`.

### Valid Call Patterns
```python
# Inferred from signature and project context
import numpy as np
from tslearn.metrics.cycc import cdist_normalized_cc

# 1. Prepare 3D float64 datasets (n_ts, sz, d)
dataset1 = np.random.rand(2, 10, 1).astype(np.float64)
dataset2 = np.random.rand(3, 10, 1).astype(np.float64)

# 2. Precompute norms for each time series (shape: (n_ts,))
norms1 = np.linalg.norm(dataset1, axis=(1, 2)).astype(np.float64)
norms2 = np.linalg.norm(dataset2, axis=(1, 2)).astype(np.float64)

# 3. Compute the distance matrix
dists = cdist_normalized_cc(
    dataset1, 
    dataset2, 
    norms1, 
    norms2, 
    self_similarity=False
)

assert dists.shape == (2, 3)
print(f"Distance matrix shape: {dists.shape}")
```

### LLM Instruction Prompt
- Always ensure `dataset1` and `dataset2` are strictly 3D arrays of shape `(n_ts, sz, d)` and dtype `float64`. Use `tslearn.utils.to_time_series_dataset` if formatting is needed.
- You must precompute and provide `norms1` and `norms2` as 1D `float64` arrays of shape `(n_ts,)`.
- Set `self_similarity=True` if `dataset1` is the exact same object/data as `dataset2` to save computation time.
- Import this low-level Cython helper directly from `tslearn.metrics.cycc`.

### Prompt Snippet
```text
When using `cdist_normalized_cc` from `tslearn.metrics.cycc`, ensure inputs are 3D `float64` NumPy arrays `(n_ts, sz, d)`. You must manually precompute the 1D norms for both datasets and pass them as `norms1` and `norms2`. Set `self_similarity=True` if comparing a dataset to itself.
```

### Common Failure Modes
- **Incorrect Dimensions:** Passing 2D arrays or raw lists instead of the required 3D `(n_ts, sz, d)` arrays will cause Cython memoryview errors.
- **Incorrect Dtype:** Failing to cast the datasets and norms to `float64` can lead to type mismatch errors in the underlying Cython C-extensions.
- **Missing Norms:** Forgetting to compute the norms over the time and dimension axes, resulting in shape mismatches for `norms1` or `norms2`.

### Fix Code Hint
```python
# FIX: Ensure inputs are 3D float64 arrays and norms are precomputed as 1D float64 arrays
dataset1 = tslearn.utils.to_time_series_dataset(raw_data1).astype(np.float64)
dataset2 = tslearn.utils.to_time_series_dataset(raw_data2).astype(np.float64)

norms1 = np.linalg.norm(dataset1, axis=(1, 2)).astype(np.float64)
norms2 = np.linalg.norm(dataset2, axis=(1, 2)).astype(np.float64)

dists = cdist_normalized_cc(dataset1, dataset2, norms1, norms2, self_similarity=False)
```

## API Test: `cdist_sax`

### Signature
```python
def cdist_sax(dataset1, breakpoints_avg, size_fitted, dataset2=None, n_jobs=None, verbose=0)
```
_Source: tslearn/tslearn/metrics/sax.py:10_

_Source doc:_ Calculates a matrix of distances (MINDIST) on SAX-transformed data, as presented in [1]_. It is important to note that this function expects the timeseries in dataset1 and dataset2 to be normalized to each have zero mean and unit variance. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz1, d) or (n_ts1, sz1) or (sz1,) A dataset of time series. If shape is (n_ts1, sz1), the dataset is composed of univariate time series. If shape is (sz1,), the dataset is composed of a unique univariate time series. breakpoints_avg : array-like, ndim=1 The breakpoints used to assign the alphabet symbols. size_fitted: int The original timesteps in the timeseries, before discretizing through SAX. dataset2 : None or array-like, shape=(n_ts2, sz2, d) or (n_ts2, sz2) or (sz2,) (default: None) Another dataset of time series. If `None`, self-similarity of `dataset1` is returned. If shape is (n_ts2, sz2), the dataset is composed of univariate time series. If shape is (sz2,), the dataset is composed of a unique univariate time series. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. verbose : int, optional (default=0) The verbosity level: if non zero, progress messages are printed. Above 50, the output is sent to stdout. The frequency of the messages increases with the verbosity level. If it more than 10, all iterations are reported. `Glossary <https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation>`__ for more details. Returns ------- cdist : array-like, shape=(n_ts1, n_ts2) Cross-similarity matrix. References ---------- .. [1] Lin, Jessica, et al. "Experiencing SAX: a novel symbolic representation of time series." Data Mining and knowledge discovery 15.2 (2007): 107-144.

### Goal
Calculates a cross-similarity matrix of MINDIST distances between two datasets of SAX-transformed time series.

### Parameters
- `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of time series.
- `breakpoints_avg`: 1D array-like. The breakpoints used to assign the SAX alphabet symbols.
- `size_fitted`: Integer. The original number of timesteps in the time series before they were discretized through SAX.
- `dataset2`, default `None`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`. The second dataset of time series. If `None`, the self-similarity matrix of `dataset1` is returned.
- `n_jobs`, default `None`: Integer or `None`. The number of parallel jobs to run (`-1` uses all processors).
- `verbose`, default `0`: Integer. The verbosity level for progress messages.

### Input
Time-series datasets provided as array-like structures (lists or NumPy arrays). 
**Crucial Precondition:** The time series in `dataset1` and `dataset2` MUST be normalized to have zero mean and unit variance before being passed to this function (e.g., using `tslearn.preprocessing.TimeSeriesScalerMeanVariance`). The function mathematically assumes this normalization for the MINDIST calculation.

### Output
Returns `unspecified` — A 2D array-like cross-similarity matrix of shape `(n_ts1, n_ts2)` containing the computed MINDIST distances between the time series in `dataset1` and `dataset2`.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# Note: Inputs here are assumed to be already normalized (zero mean, unit variance)
expected = np.array([[0, 1], [1, 0]])
dists = tslearn.metrics.cdist_sax(
    [[-1, 0, 1], [1, 0, 1]],
    [-0.5, 0., 0.5],
    3,
    dataset2=[[-1, 0, 1], [1, 0, 1]],
)

np.testing.assert_equal(dists, expected)
print(f"Computed SAX MINDIST matrix:\n{dists}")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.cdist_sax`, you MUST ensure the input time series (`dataset1` and `dataset2`) are normalized to zero mean and unit variance.
- You must provide the 1D array of `breakpoints_avg` and the integer `size_fitted` (the original length of the time series before SAX discretization) as positional arguments.
- If computing pairwise distances between two different datasets, pass the second dataset to the `dataset2` keyword argument.

### Prompt Snippet
```text
Compute the SAX MINDIST distance matrix between `X_sax` and `Y_sax`. Assume both datasets were derived from time series of original length 50 that were normalized to zero mean and unit variance. Use the breakpoints array `sax_breakpoints`.
```

### Common Failure Modes
- **Unnormalized Data:** Passing raw time series that do not have zero mean and unit variance. The function will execute, but the resulting MINDIST distances will be mathematically invalid.
- **Missing Positional Arguments:** Failing to provide `breakpoints_avg` or `size_fitted`, which are required positional arguments without defaults.
- **Incorrect Breakpoints Shape:** Passing a 2D array for `breakpoints_avg` instead of the required 1D array.

### Fix Code Hint
```python
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import tslearn.metrics

# Ensure data is normalized before SAX transformation and distance computation
scaler = TimeSeriesScalerMeanVariance()
X_normalized = scaler.fit_transform(X_raw)
Y_normalized = scaler.fit_transform(Y_raw)

# Compute distances using the normalized data representations
dists = tslearn.metrics.cdist_sax(
    X_normalized, 
    breakpoints_avg=my_breakpoints, 
    size_fitted=X_raw.shape[1], 
    dataset2=Y_normalized
)
```

## API Test: `cdist_soft_dtw`

### Signature
```python
def cdist_soft_dtw(dataset1, dataset2=None, gamma=1.0, be=None, compute_with_backend=False)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:765_

_Source doc:_ Compute cross-similarity matrix using Soft-DTW metric. Soft-DTW was originally presented in [1]_ and is discussed in more details in our :ref:`user-guide page on DTW and its variants<dtw>`. Soft-DTW is computed as: .. math:: \text{soft-DTW}_{\gamma}(X, Y) = \min_{\pi}{}^\gamma \sum_{(i, j) \in \pi} \|X_i, Y_j\|^2 where :math:`\min^\gamma` is the soft-min operator of parameter :math:`\gamma`. In the limit case :math:`\gamma = 0`, :math:`\min^\gamma` reduces to a hard-min operator and soft-DTW is defined as the square of the DTW similarity measure. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz1, d) or (n_ts1, sz1) or (sz1,) A dataset of time series. If shape is (n_ts1, sz1), the dataset is composed of univariate time series. If shape is (sz1,), the dataset is composed of a unique univariate time series. dataset2 : None or array-like, shape=(n_ts2, sz2, d) or (n_ts2, sz2) or (sz2,) (default: None) Another dataset of time series. If `None`, self-similarity of `dataset1` is returned. If shape is (n_ts2, sz2), the dataset is composed of univariate time series. If shape is (sz2,), the dataset is composed of a unique univariate time series. gamma : float (default 1.) Gamma parameter for Soft-DTW. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. compute_with_backend : bool, default=False This parameter has no influence when the NumPy backend is used. When a backend different from NumPy is used (cf parameter `be`): If `True`, the computation is done with the corresponding backend. If `False`, a conversion to the NumPy backend can be used to accelerate the computation. Returns ------- array-like, shape=(n_ts1, n_ts2) Cross-similarity matrix. Examples -------- >>> cdist_soft_dtw([[1, 2, 2, 3], [1., 2., 3., 4.]], gamma=.01) array([[-0.01098612,  1.        ], [ 1.        ,  0.        ]]) >>> cdist_soft_dtw([[1, 2, 2, 3], [1., 2., 3., 4.]], ...                [[1, 2, 2, 3], [1., 2., 3., 4.]], gamma=.01) array([[-0.01098612,  1.        ], [ 1.        ,  0.        ]])

### Goal
Compute the pairwise cross-similarity matrix between two collections of time series using the differentiable Soft-DTW metric.

### Parameters
- `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of time series.
- `dataset2`, default `None`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`. The second dataset of time series. If `None`, the self-similarity matrix of `dataset1` is computed.
- `gamma`, default `1.0`: Float representing the smoothing parameter for the soft-min operator. As `gamma` approaches `0`, the metric converges to the squared DTW distance.
- `be`, default `None`: The backend to use (`"numpy"`, `"pytorch"`, or a Backend instance). If `None`, it is automatically inferred from the input array types.
- `compute_with_backend`, default `False`: Boolean flag. When using a non-NumPy backend (like PyTorch), setting this to `True` forces the computation to stay in that backend, which is strictly required to preserve the computation graph for automatic differentiation.

### Input
- Time-series datasets, ideally formatted as 3D arrays `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`. 2D or 1D inputs are accepted and interpreted as univariate time series.
- If computing gradients with PyTorch, inputs must be PyTorch tensors with `requires_grad=True`.

### Output
Returns `unspecified` — An array-like (NumPy array or PyTorch tensor, depending on the backend) of shape `(n_ts1, n_ts2)` containing the pairwise Soft-DTW similarities.

### Valid Call Patterns
```python
from tslearn.metrics import cdist_soft_dtw
import numpy as np
import torch

# 1. Standard NumPy usage (inferred from docstring)
dataset1 = [[1.0, 2.0, 2.0, 3.0], [1.0, 2.0, 3.0, 4.0]]
sim_matrix = cdist_soft_dtw(dataset1, gamma=0.01)

assert sim_matrix.shape == (2, 2)
print("NumPy Soft-DTW Matrix:\n", sim_matrix)

# 2. PyTorch usage with automatic differentiation
ts1 = torch.tensor([[[1.0], [2.0]]], requires_grad=True)
ts2 = torch.tensor([[[3.0], [4.0]]])

# compute_with_backend=True is REQUIRED to keep the computation graph intact
sim_pt = cdist_soft_dtw(ts1, ts2, gamma=1.0, be="pytorch", compute_with_backend=True)
sim_pt.sum().backward()

assert ts1.grad is not None
print("PyTorch Gradients:\n", ts1.grad)
```

### LLM Instruction Prompt
- Use `tslearn.metrics.cdist_soft_dtw(dataset1, dataset2=None, gamma=1.0)` to compute the pairwise Soft-DTW cross-similarity matrix.
- If `dataset2` is omitted or `None`, it computes the self-similarity matrix of `dataset1`.
- **Crucial for PyTorch:** If you need to compute gradients via `.backward()`, you MUST pass `be="pytorch"` and `compute_with_backend=True`. Otherwise, `tslearn` will silently convert the tensors to NumPy to accelerate the computation, breaking the computation graph.
- Note that Soft-DTW self-similarity (the diagonal of the matrix) is not strictly zero when `gamma > 0`, and can even be negative.

### Prompt Snippet
```text
Use `tslearn.metrics.cdist_soft_dtw(dataset1, dataset2=None, gamma=1.0)` for pairwise Soft-DTW matrices. For PyTorch automatic differentiation, you MUST pass `be="pytorch"` and `compute_with_backend=True` to prevent silent conversion to NumPy. Note that Soft-DTW self-similarity is not strictly zero when `gamma > 0`.
```

### Common Failure Modes
- **Broken PyTorch Computation Graphs:** Passing PyTorch tensors with `requires_grad=True` but leaving `compute_with_backend=False` (the default). This causes `tslearn` to convert the tensors to NumPy arrays for speed, which drops the `grad_fn` and raises an error when `.backward()` is called.
- **Assuming Zero Self-Distance:** Unlike standard DTW, Soft-DTW does not guarantee that the distance between a time series and itself is zero when `gamma > 0`. Asserting that the diagonal of a self-similarity matrix is exactly `0.0` will fail.
- **Shape Mismatches:** Passing raw lists of varying lengths without first padding them using `tslearn.utils.to_time_series_dataset`. While `cdist_soft_dtw` can handle simple lists, complex jagged arrays will cause NumPy/PyTorch conversion errors.

### Fix Code Hint
```python
# If PyTorch gradients are dropped (e.g., tensor lacks grad_fn):
# Change:
sim_matrix = cdist_soft_dtw(ts1, ts2, gamma=1.0, be="pytorch")

# To:
sim_matrix = cdist_soft_dtw(ts1, ts2, gamma=1.0, be="pytorch", compute_with_backend=True)
```

## API Test: `cdist_soft_dtw_normalized`

### Signature
```python
def cdist_soft_dtw_normalized(dataset1, dataset2=None, gamma=1.0, be=None, compute_with_backend=False)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:911_

_Source doc:_ Compute cross-similarity matrix using a normalized version of the Soft-DTW metric. Soft-DTW was originally presented in [1]_ and is discussed in more details in our :ref:`user-guide page on DTW and its variants<dtw>`. Soft-DTW is computed as: .. math:: \text{soft-DTW}_{\gamma}(X, Y) = \min_{\pi}{}^\gamma \sum_{(i, j) \in \pi} \|X_i, Y_j\|^2 where :math:`\min^\gamma` is the soft-min operator of parameter :math:`\gamma`. In the limit case :math:`\gamma = 0`, :math:`\min^\gamma` reduces to a hard-min operator and soft-DTW is defined as the square of the DTW similarity measure. This normalized version is defined as: .. math:: \text{norm-soft-DTW}_{\gamma}(X, Y) = \text{soft-DTW}_{\gamma}(X, Y) - \frac{1}{2} \left(\text{soft-DTW}_{\gamma}(X, X) + \text{soft-DTW}_{\gamma}(Y, Y)\right) and ensures that all returned values are positive and that :math:`\text{norm-soft-DTW}_{\gamma}(X, X) = 0`. Parameters ---------- dataset1 : array-like, shape=(n_ts1, sz1, d) or (n_ts1, sz1) or (sz1,) A dataset of time series. If shape is (n_ts1, sz1), the dataset is composed of univariate time series. If shape is (sz1,), the dataset is composed of a unique univariate time series. dataset2 : None or array-like, shape=(n_ts2, sz2, d) or (n_ts2, sz2) or (sz2,) (default: None) Another dataset of time series. If `None`, self-similarity of `dataset1` is returned. If shape is (n_ts2, sz2), the dataset is composed of univariate time series. If shape is (sz2,), the dataset is composed of a unique univariate time series. gamma : float (default 1.) Gamma parameter for Soft-DTW. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. compute_with_backend : bool, default=False This parameter has no influence when the NumPy backend is used. When a backend different from NumPy is used (cf parameter `be`): If `True`, the computation is done with the corresponding backend. If `False`, a conversion to the NumPy backend can be used to accelerate the computation. Returns

### Goal
Compute the pairwise cross-similarity matrix between two time-series datasets using a normalized version of the Soft-DTW metric, ensuring that the distance of any time series to itself is exactly zero.

### Parameters
- `dataset1`: An array-like dataset of time series, ideally formatted as a 3D array of shape `(n_ts1, max_sz1, d)`.
- `dataset2`, default `None`: A second array-like dataset of time series of shape `(n_ts2, max_sz2, d)`. If `None`, the function computes the self-similarity matrix of `dataset1`.
- `gamma`, default `1.0`: The smoothing parameter for the soft-min operator. As `gamma` approaches 0, the metric converges to the squared hard DTW distance.
- `be`, default `None`: The computational backend to use (`"numpy"`, `"pytorch"`, or a backend instance). If `None`, it is automatically inferred from the input data types.
- `compute_with_backend`, default `False`: If `True` and using a non-NumPy backend (like PyTorch), forces the computation to stay within that backend. This is strictly required to preserve the computation graph for automatic differentiation.

### Input
Time-series datasets provided as NumPy arrays or PyTorch tensors. To ensure correct behavior, raw lists of variable-length time series should first be converted into the strict `(n_ts, max_sz, d)` 3D array format using `tslearn.utils.to_time_series_dataset`. Both datasets must share the same feature dimensionality `d`.

### Output
Returns `unspecified` — A 2D cross-similarity matrix of shape `(n_ts1, n_ts2)` (or `(n_ts1, n_ts1)` if `dataset2` is `None`). The returned object is a NumPy array or a PyTorch tensor, depending on the backend used.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import cdist_soft_dtw_normalized

# Deterministic in-memory time series of variable lengths
ts1 = [[1.0], [2.0], [3.0]]
ts2 = [[1.0], [2.0], [3.0], [4.0]]
dataset = to_time_series_dataset([ts1, ts2])

# Compute pairwise normalized Soft-DTW distance matrix
dist_matrix = cdist_soft_dtw_normalized(dataset, gamma=1.0, be="numpy")

# The matrix should be 2x2, and the diagonal (self-distance) must be exactly 0
assert dist_matrix.shape == (2, 2)
np.testing.assert_allclose(np.diag(dist_matrix), [0.0, 0.0], atol=1e-7)
print(f"Distance matrix:\n{dist_matrix}")
```

### LLM Instruction Prompt
- When calling `cdist_soft_dtw_normalized`, always format inputs into 3D arrays `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` to prevent shape mismatch errors.
- If you need to compute gradients using PyTorch's `.backward()`, you **must** provide tensors with `requires_grad=True`, set `be="pytorch"`, and explicitly pass `compute_with_backend=True`.
- Omit `dataset2` (or pass `None`) to efficiently compute the symmetric self-similarity matrix of `dataset1`.

### Prompt Snippet
```text
Compute the normalized Soft-DTW distance matrix for the given PyTorch tensor `X`. Ensure the computation graph is preserved so we can backpropagate through the distance matrix later.
```

### Common Failure Modes
- **Missing `compute_with_backend=True`**: When using the PyTorch backend for automatic differentiation, failing to set this flag will cause the function to fall back to NumPy for acceleration, dropping the computation graph and returning a detached tensor or array.
- **Incorrect Input Shape**: Passing 1D or 2D lists without converting them to the strict `(n_ts, max_sz, d)` 3D array format, leading to broadcasting or shape mismatch errors.
- **Incompatible Feature Dimensions**: `dataset1` and `dataset2` having different sizes in the last dimension `d` (e.g., comparing univariate series to multivariate series).

### Fix Code Hint
```python
# FIX: Convert inputs to 3D arrays and enable backend computation for gradients
import torch
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import cdist_soft_dtw_normalized

dataset = to_time_series_dataset([[1.0, 2.0], [3.0, 4.0]])
tensor_ds = torch.tensor(dataset, requires_grad=True)

# compute_with_backend=True is strictly required to keep the PyTorch gradient graph
dist_matrix = cdist_soft_dtw_normalized(
    tensor_ds, 
    gamma=1.0, 
    be="pytorch", 
    compute_with_backend=True
)
```

## API Test: `check_dataset`

### Signature
```python
def check_dataset(X, force_univariate=False, force_equal_length=False, force_single_time_series=False)
```
_Source: tslearn/tslearn/utils/utils.py:548_

_Source doc:_ Check if X is a valid tslearn dataset, with possibly additional extra constraints. Parameters ---------- X: array-like, shape=(n_ts, sz, d) Time series dataset. force_univariate: bool (default: False) If True, only univariate datasets are considered valid. force_equal_length: bool (default: False) If True, only equal-length datasets are considered valid. force_single_time_series: bool (default: False) If True, only datasets made of a single time series are considered valid. Returns ------- array-like, shape=(n_ts, sz, d) Formatted dataset, if it is valid Raises ------ ValueError Raised if X is not a valid dataset, or one of the constraints is not satisfied. Examples -------- >>> X = [[1, 2, 3], [1, 2, 3, 4]] >>> X_new = check_dataset(X) >>> X_new.shape (2, 4, 1) >>> check_dataset( ...     X, ...     force_equal_length=True ... )  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: All the time series in the array should be of equal lengths. >>> other_X = numpy.random.randn(3, 10, 2) >>> check_dataset( ...     other_X, ...     force_univariate=True ... )  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: Array should be univariate and is of shape: (3, 10, 2) >>> other_X = numpy.random.randn(3, 10, 2) >>> check_dataset( ...     other_X, ...     force_single_time_series=True ... )  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: Array should be made of a single time series (3 here)

### Goal
Validates and formats an array-like object into a strict `tslearn` 3D time-series dataset `(n_ts, max_sz, d)`, optionally enforcing constraints like univariate data, equal lengths, or a single time series.

### Parameters
- `X`: array-like. The raw time-series dataset to be checked and formatted. Can be a list of lists, a 2D array, or a 3D array.
- `force_univariate`, default `False`: boolean. If `True`, raises an error if the dataset has more than one feature dimension (`d > 1`).
- `force_equal_length`, default `False`: boolean. If `True`, raises an error if the time series in the dataset have varying lengths.
- `force_single_time_series`, default `False`: boolean. If `True`, raises an error if the dataset contains more than one time series (`n_ts > 1`).

### Input
The caller must provide an array-like object `X`. If `X` contains variable-length time series (e.g., a list of lists of different sizes), it will be padded with `nan` values to match the length of the longest time series (`max_sz`).

### Output
Returns `unspecified` — A formatted 3D NumPy array of shape `(n_ts, max_sz, d)` representing the valid time-series dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import check_dataset

# 1. Format a variable-length dataset
X_raw = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0, 4.0]]
X_formatted = check_dataset(X_raw)

assert X_formatted.shape == (2, 4, 1)
assert np.isnan(X_formatted[0, 3, 0])  # Shorter series is padded with nan
print(f"Formatted shape: {X_formatted.shape}")

# 2. Enforce constraints (e.g., univariate)
X_3d = np.random.randn(3, 10, 1)
X_checked = check_dataset(X_3d, force_univariate=True)
assert X_checked.shape == (3, 10, 1)
```

### LLM Instruction Prompt
- Use `tslearn.utils.check_dataset` to validate and format raw time-series data into the strict 3D `(n_ts, max_sz, d)` NumPy array shape required by `tslearn` estimators.
- Use the `force_*` boolean flags to assert preconditions before passing data to algorithms that have strict requirements (e.g., algorithms that cannot handle multivariate data or variable lengths).
- Be aware that variable-length time series will be padded with `nan` values in the output array.

### Prompt Snippet
```text
When preparing data for tslearn estimators that require specific shapes, use `tslearn.utils.check_dataset(X, force_univariate=True)` to validate the input and automatically format it into a 3D array `(n_ts, max_sz, d)`. Catch `ValueError` if the constraints are violated.
```

### Common Failure Modes
- **Varying Lengths with `force_equal_length=True`**: Raises a `ValueError` if the input contains time series of different lengths and the equal-length constraint is enforced.
- **Multivariate Data with `force_univariate=True`**: Raises a `ValueError` if the input has multiple dimensions (`d > 1`) but the univariate constraint is enforced.
- **Multiple Series with `force_single_time_series=True`**: Raises a `ValueError` if the input contains multiple time series (`n_ts > 1`) but the single time series constraint is enforced.

### Fix Code Hint
```python
from tslearn.utils import check_dataset

try:
    # This will fail because the lengths are different
    X_invalid = check_dataset([[1, 2], [1, 2, 3]], force_equal_length=True)
except ValueError as e:
    print(f"Validation failed: {e}")
    # Fix: Remove the constraint or pad/truncate the data beforehand
    X_valid = check_dataset([[1, 2], [1, 2, 3]]) 
```

## API Test: `check_dims`

### Signature
```python
def check_dims(X, X_fit_dims=None, extend=True, check_n_features_only=False)
```
_Source: tslearn/tslearn/utils/utils.py:65_

_Source doc:_ Reshapes X to a 3-dimensional array of X.shape[0] univariate timeseries of length X.shape[1] if X is 2-dimensional and extend is True. Then checks whether the provided X_fit_dims and the dimensions of X (except for the first one), match. Parameters ---------- X : array-like The first array to be compared. X_fit_dims : tuple (default: None) The dimensions of the data generated by fit, to compare with the dimensions of the provided array X. If None, then only perform reshaping of X, if necessary. extend : boolean (default: True) Whether to reshape X, if it is 2-dimensional. check_n_features_only: boolean (default: False) Returns ------- array Reshaped X array Examples -------- >>> X = numpy.empty((10, 3)) >>> check_dims(X).shape (10, 3, 1) >>> X = numpy.empty((10, 3, 1)) >>> check_dims(X).shape (10, 3, 1) >>> X_fit_dims = (5, 3, 1) >>> check_dims(X, X_fit_dims).shape (10, 3, 1) >>> X_fit_dims = (5, 3, 2) >>> check_dims(X, X_fit_dims)  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ValueError: Dimensions (except first) must match! ((5, 3, 2) and (10, 3, 1) are passed shapes) >>> X_fit_dims = (5, 5, 1) >>> check_dims(X, X_fit_dims, check_n_features_only=True).shape (10, 3, 1) >>> X_fit_dims = (5, 5, 2) >>> check_dims( ...     X, ...     X_fit_dims, ...     check_n_features_only=True ... )  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ValueError: Number of features of the provided timeseries must match! (last dimension) must match the one of the fitted data! ((5, 5, 2) and (10, 3, 1) are passed shapes) Raises ------ ValueError Will raise exception if X is None or (if X_fit_dims is provided) one of the dimensions of the provided data, except the first, does not match X_fit_dims.

### Goal
Validates and reshapes an input time-series array to the strict 3D format `(n_ts, max_sz, d)` required by `tslearn`, optionally verifying its dimensions against a previously fitted dataset's shape.

### Parameters
- `X`: array-like. The input time-series dataset to be reshaped and validated.
- `X_fit_dims`, default `None`: tuple. The expected shape tuple (e.g., from a fitted estimator's training data) to compare against `X.shape`. The first dimension (number of samples) is ignored during comparison.
- `extend`, default `True`: boolean. If True, automatically reshapes a 2D array `(n_ts, max_sz)` into a 3D array `(n_ts, max_sz, 1)` by appending a univariate feature dimension.
- `check_n_features_only`, default `False`: boolean. If True, only the last dimension (number of features, `d`) is compared against `X_fit_dims`, allowing the sequence length (`max_sz`) to vary between fit and predict steps.

### Input
An array-like object `X` (typically a NumPy array). If `extend=True`, it can be 2D `(n_ts, max_sz)` or 3D `(n_ts, max_sz, d)`. If `X_fit_dims` is provided, it must be a tuple representing a 3D shape `(n_ts_fit, max_sz_fit, d_fit)`.

### Output
Returns `array` — A NumPy array representing the reshaped `X` in the strict 3D format `(n_ts, max_sz, d)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import check_dims

# 1. Reshape a 2D array to 3D (univariate)
X_2d = np.zeros((10, 5))
X_3d = check_dims(X_2d)
assert X_3d.shape == (10, 5, 1)
print(f"Reshaped 2D to 3D: {X_3d.shape}")

# 2. Validate against a fitted shape (ignoring n_ts)
X_fit_shape = (50, 5, 1) # e.g., 50 samples during fit
X_valid = check_dims(X_2d, X_fit_dims=X_fit_shape)
assert X_valid.shape == (10, 5, 1)
print(f"Validated against fit shape: {X_valid.shape}")

# 3. Validate only the number of features (allowing different sequence lengths)
X_diff_length = np.zeros((10, 8, 1))
X_feat_valid = check_dims(X_diff_length, X_fit_dims=X_fit_shape, check_n_features_only=True)
assert X_feat_valid.shape == (10, 8, 1)
print(f"Validated features only: {X_feat_valid.shape}")
```

### LLM Instruction Prompt
- Use `check_dims` from `tslearn.utils` when implementing custom estimators or preprocessing steps to ensure input arrays conform to the strict 3D `(n_ts, max_sz, d)` format required by `tslearn`.
- When validating data during a `.predict()` or `.transform()` step, pass the training data's shape to `X_fit_dims`.
- If the algorithm natively supports variable-length time series (like DTW-based methods), set `check_n_features_only=True` to prevent `ValueError`s when test sequences have different lengths than training sequences.

### Prompt Snippet
```text
When writing a custom scikit-learn compatible estimator for tslearn, use `tslearn.utils.check_dims(X, X_fit_dims=self.X_fit_dims_, check_n_features_only=True)` in your `predict` method to safely reshape 2D inputs to 3D and validate that the number of features matches the training data, while still allowing variable sequence lengths.
```

### Common Failure Modes
- **Mismatched Sequence Lengths:** Passing an array with a different sequence length than `X_fit_dims` without setting `check_n_features_only=True` raises a `ValueError`.
- **Mismatched Feature Dimensions:** Passing an array with a different number of features (the last dimension) than `X_fit_dims` will always raise a `ValueError`.
- **Passing None:** Passing `X=None` raises a `ValueError`.

### Fix Code Hint
```python
import numpy as np
from tslearn.utils import check_dims

X_test = np.zeros((10, 7, 1))
X_fit_shape = (50, 5, 1)

try:
    # This fails because sequence length (7 vs 5) doesn't match
    check_dims(X_test, X_fit_dims=X_fit_shape)
except ValueError as e:
    print(f"Expected failure: {e}")
    
    # Fix: Use check_n_features_only=True if the estimator supports variable lengths
    X_fixed = check_dims(X_test, X_fit_dims=X_fit_shape, check_n_features_only=True)
    assert X_fixed.shape == (10, 7, 1)
    print(f"Successfully validated with check_n_features_only=True: {X_fixed.shape}")
```

## API Test: `check_equal_size`

### Signature
```python
def check_equal_size(dataset, be=None)
```
_Source: tslearn/tslearn/utils/utils.py:425_

_Source doc:_ Check if all time series in the dataset have the same size. Parameters ---------- dataset: array-like The dataset to check. Returns ------- bool Whether all time series in the dataset have the same size. Examples -------- >>> check_equal_size([[1, 2, 3], [4, 5, 6], [5, 3, 2]]) True >>> check_equal_size([[1, 2, 3, 4], [4, 5, 6], [5, 3, 2]]) False >>> check_equal_size([]) True

### Goal
Check if all time series within a given dataset have the exact same length (number of time steps).

### Parameters
- `dataset`: array-like. The dataset to check, typically a list of lists, a NumPy array, or a PyTorch tensor representing a collection of time series.
- `be`, default `None`: The backend identifier (e.g., `"numpy"`, `"pytorch"`, or a backend instance) to use for the check. If `None`, the backend is automatically inferred from the input data types.

### Input
An iterable collection of time series. This is often a raw list of lists of varying lengths before it is converted into `tslearn`'s strict `(n_ts, max_sz, d)` 3D array format.

### Output
Returns `unspecified` — A boolean value: `True` if all time series in the dataset have the same size or if the dataset is empty, and `False` if there are variable-length time series.

### Valid Call Patterns
```python
import tslearn.utils

# Check a dataset with equal-length time series
is_equal = tslearn.utils.check_equal_size([[0], [0]])
assert is_equal is True

# Check a dataset with variable-length time series
is_equal_var = tslearn.utils.check_equal_size([[0], [0, 0]])
assert is_equal_var is False

# Empty datasets are considered to have equal sizes
assert tslearn.utils.check_equal_size([]) is True

print("check_equal_size passed")
```

### LLM Instruction Prompt
- Use `tslearn.utils.check_equal_size(dataset)` to determine if a raw dataset contains variable-length time series before attempting to convert it to a strict 3D array or applying algorithms that require equal-length series.

### Prompt Snippet
```text
Use `tslearn.utils.check_equal_size(dataset)` to verify if all time series in an array-like dataset have the same length. Returns a boolean.
```

### Common Failure Modes
- Passing a single 1D time series (e.g., `[1, 2, 3]`) instead of a dataset (a collection of time series). The function expects an iterable of iterables; passing a flat list of numbers will cause it to attempt to check the length of scalar integers, resulting in a `TypeError: object of type 'int' has no len()`.

### Fix Code Hint
```python
# WRONG: Passing a single time series directly
# tslearn.utils.check_equal_size([1, 2, 3])  # Raises TypeError

# RIGHT: Wrap the single time series in a list to form a dataset of size 1
is_equal = tslearn.utils.check_equal_size([[1, 2, 3]])
```

## API Test: `check_keras_backend`

### Signature
```python
def check_keras_backend()
```
_Source: tslearn/tslearn/backend/__init__.py:12_

_Source doc:_ Select a backend based on installed packages when none is explicitly selected.

### Goal
Select a backend based on installed packages when none is explicitly selected, typically checking the environment for Keras availability.

### Parameters
_None._

### Input
No input parameters are required. The function relies on the current Python environment and installed packages.

### Output
Returns `None` — the function performs an environment check and backend selection as a side effect rather than returning a backend instance.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
from tslearn.backend import check_keras_backend

def test_check_keras_backend():
    # Execute the backend check (takes no arguments)
    result = check_keras_backend()
    
    # Assert the function returns None as it operates via side effects
    assert result is None, f"Expected check_keras_backend to return None, got {type(result)}"
    print("check_keras_backend() executed successfully and returned None.")

test_check_keras_backend()
```

### LLM Instruction Prompt
- Call `check_keras_backend()` without any arguments to trigger backend selection based on installed packages.
- Do not expect a backend object to be returned; the function returns `None` and configures the environment internally.

### Prompt Snippet
```text
Use `tslearn.backend.check_keras_backend()` to check for installed packages and select a backend when none is explicitly selected. It takes no arguments and returns None.
```

### Common Failure Modes
- Passing arguments (like a backend string or tensor) to `check_keras_backend`, which takes no parameters.
- Attempting to assign the return value to a variable and use it as a backend instance (it returns `None`).

### Fix Code Hint
```python
# WRONG: backend = check_keras_backend("tensorflow")
# RIGHT: check_keras_backend()  # Returns None; configures backend via side effects
```

## API Test: `check_variable_length_input`

### Signature
```python
def check_variable_length_input(X)
```
_Source: tslearn/tslearn/utils/utils.py:39_

_Source doc:_ Input validation on a variable length dataset. Parameters ---------- X : object Input object to check / convert. Returns ------- array_converted : object The converted and validated array.

### Goal
Validates and converts an input object containing variable-length time series into a standardized array format suitable for `tslearn` estimators.

### Parameters
- `X`: The input object (e.g., a list of lists, list of arrays, or an existing NumPy array) representing a variable-length time-series dataset to check and convert.

### Input
The caller must provide a dataset `X` that can be interpreted as a collection of time series. Because `tslearn` natively supports variable-length time series, `X` can be an iterable of 1D or 2D sequences with differing lengths (e.g., `[[1, 2], [1, 2, 3]]`). 

### Output
Returns `unspecified` — The converted and validated array object. Based on `tslearn` conventions, this is typically a 3D NumPy array of shape `(n_ts, max_sz, d)`, where shorter time series are padded with `nan` values to match the maximum sequence length (`max_sz`).

### Valid Call Patterns
```python
from tslearn.utils import check_variable_length_input
import numpy as np

# Inferred from signature (not verified by existing tests)
raw_variable_length_data = [[1.0, 2.0], [1.0, 2.0, 3.0]]
checked_data = check_variable_length_input(raw_variable_length_data)

assert checked_data is not None, "Expected a converted array"
assert hasattr(checked_data, "shape"), "Expected an array-like object"
assert checked_data.ndim == 3, "tslearn standardizes to 3D arrays (n_ts, max_sz, d)"
assert np.isnan(checked_data[0, -1, 0]), "Shorter series should be nan-padded"

print(f"Validated array shape: {checked_data.shape}")
```

### LLM Instruction Prompt
- Call `check_variable_length_input(X)` to validate and standardize raw variable-length time-series data before passing it to internal estimators or custom metric functions. Expect the output to be a 3D array padded with `nan`s. Do not invent additional parameters like `dtype` or `padding_value`, as they are not supported by this signature.

### Prompt Snippet
```text
tslearn.utils.check_variable_length_input(X)
Validates and converts variable-length time-series iterables into standardized 3D arrays (n_ts, max_sz, d) padded with `nan`s.
```

### Common Failure Modes
- **Assuming a 2D output:** Callers might expect a 2D array `(n_ts, max_sz)` for univariate data, but `tslearn` strictly enforces a 3D structure `(n_ts, max_sz, d)`.
- **Incompatible nested structures:** Passing deeply nested irregular lists (beyond 3 dimensions) or objects that cannot be cast to numeric arrays will cause validation to fail.
- **Missing imports:** Failing to import the function explicitly from `tslearn.utils`.

### Fix Code Hint
```python
# If validation fails due to shape or type errors, ensure the input is a list of time series
# and handle the resulting 3D array properly.
from tslearn.utils import check_variable_length_input

X_raw = [[1, 2], [3, 4, 5]]
X_valid = check_variable_length_input(X_raw)
# X_valid is now a 3D array of shape (2, 3, 1)
```

## API Test: `classes_`

### Signature
```python
def classes_(self)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:124_

### Goal
Retrieves the unique class labels known to the classifier, typically populated after the model has been fitted.

### Parameters
- `self`: The classifier instance (e.g., `NonMyopicEarlyClassifier`).

### Input
A classifier instance. For meaningful results, the classifier must have been fitted on a dataset using `.fit(X, y)`.

### Output
Returns `unspecified` — typically a NumPy array of unique class labels seen during training, or `None` if the model has not yet been fitted.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare 3D time-series dataset and labels
dataset = to_time_series_dataset([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [4, 3, 2, 1],
    [4, 3, 2, 1]
])
y = [0, 0, 1, 1]

# 2. Instantiate the classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1),
    min_t=2,
    cost_time_parameter=0.1
)

# 3. Before fitting, classes_ is None
assert model.classes_ is None

# 4. Fit the model
model.fit(dataset, y)

# 5. Access classes_ as a property
classes = model.classes_
print(f"Discovered classes: {classes}")
assert np.array_equal(classes, [0, 1])
```

### LLM Instruction Prompt
- Access `classes_` as a property (without parentheses), not as a method.
- Ensure the classifier has been fitted with `.fit(X, y)` before accessing `classes_`, otherwise it may return `None`.

### Prompt Snippet
```text
Access `model.classes_` as a property to retrieve the unique class labels from a fitted `tslearn` classifier. Do not call it as a function.
```

### Common Failure Modes
- Calling `classes_` as a method (`model.classes_()`), which raises a `TypeError: 'numpy.ndarray' object is not callable` or `TypeError: 'NoneType' object is not callable`.
- Accessing `classes_` before the model is fitted, which evaluates to `None` and causes downstream operations expecting an array to fail.

### Fix Code Hint
```python
# WRONG: Calling as a method
# labels = model.classes_()

# CORRECT: Accessing as a property after fitting
model.fit(X, y)
labels = model.classes_
```

## API Test: `coef_`

### Signature
```python
def coef_(self)
```
_Source: tslearn/tslearn/svm/svm.py:34_

### Goal
Retrieves the weights (coefficients) assigned to the features for a fitted linear time-series Support Vector Machine (SVM) model.

### Parameters
- `self`: The fitted `tslearn.svm.TimeSeriesSVC` or `tslearn.svm.TimeSeriesSVR` estimator instance.

### Input
The estimator must already be fitted on a strictly formatted 3D time-series dataset `(n_ts, max_sz, d)` using `.fit(X, y)`. Crucially, the SVM must have been instantiated with a linear kernel (e.g., `kernel="linear"`), as non-linear kernels (like the default Global Alignment Kernel `gak`) do not compute explicit feature coefficients.

### Output
Returns `unspecified` — typically a NumPy `ndarray` representing the weights of the features in the decision function. The exact shape depends on the number of classes and the flattened size of the input time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Create a simple 3D time-series dataset (n_ts, max_sz, d)
X = np.array([[[1.0]], [[2.0]], [[3.0]], [[4.0]]])
y = np.array([0, 0, 1, 1])

# 2. Initialize and fit a TimeSeriesSVC with a linear kernel
# (coef_ is only available for linear kernels in SVMs)
clf = TimeSeriesSVC(kernel="linear")
clf.fit(X, y)

# 3. Access the coef_ property
# Note: Inferred as a property access based on scikit-learn conventions,
# despite the raw signature `def coef_(self)`.
coefficients = clf.coef_

print("Coefficients shape:", coefficients.shape)
assert coefficients is not None, "coef_ should return the model weights"
```

### LLM Instruction Prompt
- When accessing `coef_` on a `tslearn` SVM estimator, you MUST ensure the model was instantiated with `kernel="linear"`. Do not attempt to access `coef_` on models using `gak` or other non-linear kernels.
- You MUST ensure the model has been fitted with `.fit(X, y)` before accessing this property.
- Access it as a property (`model.coef_`), following standard `scikit-learn` conventions, rather than calling it as a method.

### Prompt Snippet
```text
# Fit a linear time-series SVM to inspect feature weights
classifier = TimeSeriesSVC(kernel="linear")
classifier.fit(X_train, y_train)

# Retrieve the coefficients
weights = classifier.coef_
```

### Common Failure Modes
- **AttributeError (Non-linear kernel):** Accessing `coef_` on a `TimeSeriesSVC` or `TimeSeriesSVR` that was initialized with a non-linear kernel (like `gak` or `rbf`). Only linear kernels expose feature coefficients.
- **NotFittedError:** Accessing `coef_` before calling `.fit(X, y)` on the estimator.
- **TypeError (Method call):** Attempting to call it as a method (`clf.coef_()`) instead of accessing it as a property (`clf.coef_`), which violates the underlying `scikit-learn` API design.

### Fix Code Hint
```python
# WRONG: Using default kernel (gak) and trying to get coefficients
clf = TimeSeriesSVC()
clf.fit(X, y)
# weights = clf.coef_  # Raises AttributeError

# CORRECT: Explicitly use a linear kernel if you need to inspect coef_
clf_linear = TimeSeriesSVC(kernel="linear")
clf_linear.fit(X, y)
weights = clf_linear.coef_
```

## API Test: `compute`

### Signature
```python
def compute(self)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1111  (+1 more definition site/overload)_

_Source doc:_ Compute soft-DTW by dynamic programming. Returns ------- sdtw: float soft-DTW discrepancy.

### Goal
Compute the soft-DTW (Dynamic Time Warping) discrepancy between time series using dynamic programming.

### Parameters
- `self`: The instantiated Soft-DTW calculator object containing the initialized time-series data and metric hyperparameters (such as `gamma`).

### Input
This method takes no arguments other than `self`. The caller must have already instantiated the parent object with the necessary time-series data. As per `tslearn` conventions, the underlying time-series data provided to the object's constructor must be properly formatted (typically as 3D `numpy` arrays or PyTorch tensors of shape `(n_ts, max_sz, d)`).

### Output
Returns `unspecified` — A `float` representing the computed soft-DTW discrepancy score.

### Valid Call Patterns
```python
# Inferred from signature (not verified in provided examples)
# Assuming `soft_dtw_obj` is an already-instantiated Soft-DTW calculator object

sdtw_discrepancy = soft_dtw_obj.compute()
```

### LLM Instruction Prompt
- When calling `compute`, invoke it without any arguments on an already-initialized Soft-DTW object. Do not pass the time-series arrays or hyperparameters (like `gamma`) to `compute()`; these must be provided during the object's instantiation.

### Prompt Snippet
```text
# Compute the soft-DTW discrepancy using the pre-configured object
sdtw_score = soft_dtw_obj.compute()
```

### Common Failure Modes
- **Passing arguments to `compute`:** Providing time-series arrays directly to `compute(ts1, ts2)` will raise a `TypeError`, as the method only accepts `self`.
- **Unformatted underlying data:** If the parent object was initialized with raw lists instead of the strict `(n_ts, max_sz, d)` 3D array format required by `tslearn`, the computation will fail internally.

### Fix Code Hint
```python
# WRONG: Passing data directly to the compute method
# score = soft_dtw_obj.compute(ts1, ts2)

# RIGHT: Call compute without arguments (data is handled by the object's constructor)
score = soft_dtw_obj.compute()
```

## API Test: `compute_mask`

### Signature
```python
def compute_mask(s1, s2, global_constraint=0, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
def compute_mask(self, inputs, mask=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1770  (+2 more definition site/overload)_

_Source doc:_ Compute the mask (region constraint). Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series or integer. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series or integer. If shape is (sz2,), the time series is assumed to be univariate. global_constraint : {0, 1, 2} (default: 0) Global constraint to restrict admissible paths for DTW: - "itakura" if 1 - "sakoe_chiba" if 2 - no constraint otherwise sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [1]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to 2 (sakoe-chiba), a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to 1 (itakura), a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- mask : array-like, shape=(sz1, sz2) Constraint region.

### Goal
Compute a boolean mask matrix representing the allowed region constraint (such as a Sakoe-Chiba band or Itakura parallelogram) for Dynamic Time Warping (DTW) alignment paths.

### Parameters
- `s1`: A time series array of shape `(sz1, d)` or `(sz1,)`, or an integer `sz1`. If an integer is provided, it is used directly as the dimension size for the mask.
- `s2`: Another time series array of shape `(sz2, d)` or `(sz2,)`, or an integer `sz2`. If an integer is provided, it is used directly as the dimension size for the mask.
- `global_constraint`, default `0`: Integer specifying the global constraint to restrict admissible paths: `0` for no constraint, `1` for Itakura parallelogram, or `2` for Sakoe-Chiba band.
- `sakoe_chiba_radius`, default `None`: Integer radius for the Sakoe-Chiba band constraint. Controls how far in time the alignment can deviate from the diagonal. If `None` and `global_constraint=2`, defaults to `1`.
- `itakura_max_slope`, default `None`: Float maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint=1`, defaults to `2.0`.
- `be`, default `None`: The backend to use for computation. Can be a backend instance, `"numpy"`, `"pytorch"`, or `None` (auto-detected from the input arrays).

### Input
`s1` and `s2` must be either integers representing the lengths of the two time series, or 1D/2D arrays/tensors representing the time series themselves. Unlike many `tslearn` estimators, this function expects individual time series (or their lengths), not 3D datasets.

### Output
Returns `unspecified` — A boolean array-like (NumPy array or PyTorch tensor, depending on the backend) of shape `(sz1, sz2)`. `True` values indicate valid regions where the DTW path is allowed to pass; `False` values indicate restricted regions.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# 1. Compute mask using integer lengths and Sakoe-Chiba constraint
mask_sc = tslearn.metrics.compute_mask(
    s1=4, 
    s2=4, 
    global_constraint=2, 
    sakoe_chiba_radius=1, 
    be="numpy"
)
assert mask_sc.shape == (4, 4)
assert not mask_sc[0, 2]  # Outside radius 1

# 2. Compute mask using time series arrays and no constraint
s1 = np.array([1.0, 2.0, 3.0])
s2 = np.array([1.0, 2.0, 2.0, 3.0])
mask_none = tslearn.metrics.compute_mask(s1, s2, global_constraint=0)

assert mask_none.shape == (3, 4)
assert np.all(mask_none)  # No constraint means all True
print("Masks computed successfully.")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.compute_mask` to generate boolean constraint matrices for custom DTW implementations or visualizations.
- Pass either the raw time series arrays (1D or 2D) or simply their integer lengths as `s1` and `s2`. Do not pass 3D datasets.
- Explicitly set `global_constraint` to `1` (Itakura) or `2` (Sakoe-Chiba) when providing `itakura_max_slope` or `sakoe_chiba_radius`.
- If both constraint parameters are provided but `global_constraint` is left as `0`, a `RuntimeWarning` will be raised and no constraint will be applied.

### Prompt Snippet
```text
Generate a boolean mask for a Sakoe-Chiba band with a radius of 2 for two time series of lengths 10 and 12 using `tslearn.metrics.compute_mask`. Ensure the correct `global_constraint` integer is passed.
```

### Common Failure Modes
- Passing 3D datasets `(n_ts, max_sz, d)` instead of individual time series `(sz, d)` or integer lengths, resulting in incorrect mask dimensions or errors.
- Providing both `sakoe_chiba_radius` and `itakura_max_slope` while leaving `global_constraint=0`, which causes the function to emit a `RuntimeWarning` and return an unconstrained mask (all `True`).
- Passing PyTorch tensors but explicitly setting `be="numpy"`, which may cause type conflicts if the backend does not match the input types.

### Fix Code Hint
```python
# Incorrect: Passing 3D datasets or ambiguous constraints
# mask = tslearn.metrics.compute_mask(X_train, X_test, sakoe_chiba_radius=2, itakura_max_slope=1.5)

# Correct: Pass individual lengths/series and explicitly set the global_constraint integer
mask = tslearn.metrics.compute_mask(
    s1=len(X_train[0]), 
    s2=len(X_test[0]), 
    global_constraint=2, 
    sakoe_chiba_radius=2
)
```

## API Test: `compute_output_shape`

### Signature
```python
def compute_output_shape(self, input_shape)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:86  (+3 more definition site/overload)_

### Goal
Computes the output shape of a custom neural network layer given its input shape, used internally by the `LearningShapelets` estimator during model compilation.

### Parameters
- `self`: A custom layer instance from `tslearn.shapelets` (e.g., `LocalSquaredDistanceLayer`, `GlobalMinPooling1DLayer`, or `ArgminLayer`).
- `input_shape`: A tuple of integers (or `None` for dynamic dimensions) representing the shape of the input tensor.

### Input
A tuple representing the input dimensions to the layer. In standard `tslearn` workflows, this corresponds to the 3D shape `(batch_size, max_sz, d)` derived from datasets formatted by `to_time_series_dataset`.

### Output
Returns `unspecified` — A tuple of integers representing the expected shape of the output tensor after passing through the custom layer.

### Valid Call Patterns
```python
# Inferred from signature (not verified)
import tslearn.shapelets.shapelets as shp
import inspect

# Dynamically locate internal layer classes that implement compute_output_shape
layer_classes = [
    cls for name, cls in inspect.getmembers(shp, inspect.isclass)
    if "compute_output_shape" in cls.__dict__
]

assert len(layer_classes) == 3, "Expected to find 3 custom layer classes with compute_output_shape"
print(f"Found classes with compute_output_shape: {[cls.__name__ for cls in layer_classes]}")

# Note: In practice, this method is called automatically by the neural network 
# backend (e.g., Keras/TensorFlow) when building the LearningShapelets model.
# output_shape = layer_instance.compute_output_shape((None, 10, 1))
```

### LLM Instruction Prompt
- Do not call `compute_output_shape` directly in standard time-series workflows. It is an internal Keras-style layer method used by `LearningShapelets` to infer tensor dimensions during model building.
- If you need to use `LearningShapelets`, interact with its `fit`, `predict`, and `transform` methods instead of its underlying layer components.

### Prompt Snippet
```text
`compute_output_shape(self, input_shape)` is an internal method on custom neural network layers in `tslearn.shapelets`. It calculates the output tensor shape from the `input_shape` tuple. Do not call this directly; it is invoked automatically by the backend during `LearningShapelets` model compilation.
```

### Common Failure Modes
- **Direct Invocation Errors:** Attempting to instantiate internal layer classes and call this method directly without providing the correct backend-specific initialization arguments.
- **Shape Mismatches:** Passing an `input_shape` tuple that does not account for the batch dimension (e.g., passing `(max_sz, d)` instead of `(None, max_sz, d)`).

### Fix Code Hint
```python
# compute_output_shape is called automatically by the underlying neural network framework.
# Ensure your input data to LearningShapelets is properly formatted as a 3D array (n_ts, max_sz, d)
# using tslearn.utils.to_time_series_dataset, and let the estimator handle layer shapes.
from tslearn.utils import to_time_series_dataset
from tslearn.shapelets import LearningShapelets

X = to_time_series_dataset([[1, 2, 3], [1, 2, 3, 4]])
clf = LearningShapelets(n_shapelets_per_size={3: 1})
# clf.fit(X, y) # The backend will call compute_output_shape internally here
```

## API Test: `compute_var`

### Signature
```python
def compute_var(p, X, with_constant=False)
```
_Source: tslearn/tslearn/forecasting/_arima.py:21_

_Source doc:_ Compute the VAR parameters associated with a given time series. Parameters ---------- p : int AR order X : array-like, shape (sz, d) time-series data, sz should be greater or equal than p with_constant : bool (default: False) whether to compute an intercept term. Returns ------- (intercept, ar_coeffs, residuals) tuple

### Goal
Compute the Vector AutoRegressive (VAR) model parameters (intercept, autoregressive coefficients, and residuals) for a given multivariate time series.

### Parameters
- `p`: `int` — The autoregressive (AR) order, representing the number of lagged past time steps to use as predictors.
- `X`: `array-like` — The time-series data of shape `(sz, d)`, where `sz` is the number of time steps and `d` is the number of dimensions.
- `with_constant`, default `False`: `bool` — Whether to compute and include an intercept (constant) term in the VAR model.

### Input
- `X` must be a 2D array-like object of shape `(sz, d)`. Note that this differs from the standard 3D `(n_ts, max_sz, d)` format used by most high-level `tslearn` estimators, as this is a low-level helper operating on a single time series.
- The number of time steps `sz` must be greater than or equal to the autoregressive order `p`.
- `X` should not contain `nan` values in the segment being processed.

### Output
Returns `tuple` — A 3-element tuple containing `(intercept, ar_coeffs, residuals)` representing the fitted VAR parameters and the model's training residuals.

### Valid Call Patterns
```python
import numpy as np
# Inferred from signature
from tslearn.forecasting._arima import compute_var

# 2D time series: 5 time steps, 2 dimensions
X = np.array([
    [1.0, 2.0], 
    [1.5, 2.5], 
    [1.2, 2.2], 
    [1.8, 2.8], 
    [1.1, 2.1]
])

# Compute VAR parameters with AR order p=2
intercept, ar_coeffs, residuals = compute_var(p=2, X=X, with_constant=True)

assert isinstance(ar_coeffs, np.ndarray)
print("VAR computation successful.")
```

### LLM Instruction Prompt
- Do not pass standard 3D `tslearn` datasets `(n_ts, max_sz, d)` to `compute_var`. It strictly expects a 2D array `(sz, d)` representing a single multivariate time series.
- Ensure the time series length `sz` is strictly greater than or equal to the AR order `p`.
- If working with univariate data, reshape it to `(sz, 1)` before passing it to `X`.
- Expect a tuple of exactly three elements: `(intercept, ar_coeffs, residuals)`.

### Prompt Snippet
```text
When using `tslearn.forecasting._arima.compute_var`, ensure the input `X` is a 2D array of shape `(sz, d)` and that `sz >= p`. Do not pass 3D arrays. It returns a tuple of `(intercept, ar_coeffs, residuals)`.
```

### Common Failure Modes
- **Dimensionality Error (`ValueError` or `IndexError`)**: Passing a 3D array `(n_ts, sz, d)` or a 1D array `(sz,)` instead of the required 2D array `(sz, d)`.
- **Insufficient Length (`ValueError`)**: Passing an AR order `p` that is strictly greater than the number of time steps `sz` in `X`.
- **Import Error**: Attempting to import `compute_var` from the top-level `tslearn` namespace instead of the internal `tslearn.forecasting._arima` module.

### Fix Code Hint
```python
import numpy as np
from tslearn.forecasting._arima import compute_var

def safe_compute_var(p, X_single, with_constant=False):
    # Ensure X is 2D (sz, d)
    X_arr = np.asarray(X_single)
    if X_arr.ndim == 1:
        X_arr = X_arr.reshape(-1, 1)
    elif X_arr.ndim == 3:
        raise ValueError("compute_var expects a single 2D time series, not a 3D dataset.")
        
    if X_arr.shape[0] < p:
        raise ValueError(f"Time series length ({X_arr.shape[0]}) must be >= p ({p})")
        
    return compute_var(p, X_arr, with_constant=with_constant)
```

## API Test: `copy`

### Signature
```python
def copy(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:145  (+1 more definition site/overload)_

### Goal
Creates an independent duplicate of a time-series array or tensor, preserving its specific backend type (NumPy or PyTorch).

### Parameters
- `x`: The input time-series data structure (NumPy array or PyTorch tensor) to be duplicated.

### Input
A valid NumPy `ndarray` or PyTorch `Tensor`. In the context of `tslearn`, this is typically a 3D array of shape `(n_ts, max_sz, d)`, but as a low-level backend helper, it accepts arbitrary shapes supported by the underlying backend.

### Output
Returns `unspecified` — A new object of the exact same type, shape, and data as `x`, but allocated in a separate memory space so that in-place mutations to the copy do not affect the original.

### Valid Call Patterns
```python
# Inferred from signature and backend architecture (no existing test found)
from tslearn.backend import instantiate_backend
import numpy as np

# 1. Instantiate the backend (e.g., NumPy)
be = instantiate_backend("numpy")
x = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])

# 2. Create a backend-agnostic copy
x_copy = be.copy(x)

# 3. Verify it is an independent object
assert x_copy is not x, "copy() must return a new object in memory"
assert np.array_equal(x_copy, x), "copy() must preserve the data"
print("Successfully created an independent copy of the time-series array.")
```

### LLM Instruction Prompt
- When writing backend-agnostic time-series algorithms in `tslearn`, use the backend instance's `copy(x)` method to duplicate arrays or tensors before performing in-place mutations. Do not use `numpy.copy()` or `torch.clone()` directly if the code needs to support both backends dynamically.

### Prompt Snippet
```text
Use the instantiated backend's `copy` method to safely duplicate time-series data without tying the implementation to a specific framework (NumPy or PyTorch).
```

### Common Failure Modes
- **Type Mismatch with Backend:** Passing a raw Python list or a NumPy array to a PyTorch backend's `copy` method (or vice versa) may raise an error if the specific backend implementation strictly expects its native tensor/array type.
- **Missing Backend Instantiation:** Attempting to call `copy(x)` as a standalone global function rather than as a method on a resolved backend instance (e.g., `be.copy(x)`).

### Fix Code Hint
```python
# WRONG: Calling copy globally or mixing backend types
# import torch
# x_list = [1, 2, 3]
# x_copy = copy(x_list) 

# CORRECT: Resolve the backend first, ensure the input matches, then call its copy method
from tslearn.backend import instantiate_backend
import torch

x_tensor = torch.tensor([[[1.0], [2.0]]])
be = instantiate_backend("pytorch") # or instantiate_backend(x_tensor)
x_copy = be.copy(x_tensor)
```

## API Test: `ctw`

### Signature
```python
def ctw(s1, s2, max_iter=100, n_components=None, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, verbose=False, be=None)
```
_Source: tslearn/tslearn/metrics/ctw.py:200_

_Source doc:_ Compute Canonical Time Warping (CTW) similarity measure between (possibly multidimensional) time series and return the similarity. Canonical Time Warping is a method to align time series under rigid registration of the feature space. It should not be confused with Dynamic Time Warping (DTW), though CTW uses DTW. It is not required that both time series share the same size, nor the same dimension (CTW will find a subspace that best aligns feature spaces). CTW was originally presented in [1]_. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. max_iter : int (default: 100) Number of iterations for the CTW algorithm. Each iteration n_components : int (default: None) Number of components to be used for Canonical Correlation Analysis. If None, the lower minimum number of features between seq1 and seq2 is used. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for DTW calls. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. verbose : bool (default: True) If True, scores are printed at each iteration of the algorithm. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- float Similarity score Examples

### Goal
Compute the Canonical Time Warping (CTW) similarity measure between two time series, aligning them under rigid registration of their feature spaces even if they have different dimensionalities.

### Parameters
- `s1`: array-like, shape `(sz1, d1)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d2)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `max_iter`, default `100`: int. The maximum number of iterations for the CTW algorithm to converge.
- `n_components`, default `None`: int or None. The number of components to use for Canonical Correlation Analysis. If `None`, it defaults to the minimum number of features between `s1` and `s2`.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. The global constraint to restrict admissible paths for the underlying DTW calls.
- `sakoe_chiba_radius`, default `None`: int or None. The radius for the Sakoe-Chiba band constraint. If `None` but `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: float or None. The maximum slope for the Itakura parallelogram constraint. If `None` but `global_constraint="itakura"`, defaults to 2.0.
- `verbose`, default `False`: bool. If `True`, prints the score at each iteration.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. The computational backend to use. If `None`, it is inferred from the input types.

### Input
Two individual time series arrays (not 3D datasets). They can be NumPy arrays or PyTorch tensors. Unlike standard DTW, `s1` and `s2` are not required to share the same number of dimensions (features) or the same length.

### Output
Returns `unspecified` — a `float` (or a PyTorch scalar tensor if the PyTorch backend is used) representing the computed CTW similarity score between the two time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import ctw

# Two time series with different lengths and different dimensionalities
s1 = np.array([[1.0, 0.5], [2.0, 1.0], [3.0, 1.5]]) # shape (3, 2)
s2 = np.array([[1.0], [2.0], [2.0], [3.0]])         # shape (4, 1)

# Compute CTW similarity
similarity = ctw(s1, s2, max_iter=10, be="numpy")

assert isinstance(similarity, float)
print(f"CTW similarity: {similarity:.4f}")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.ctw` to compute the Canonical Time Warping similarity between exactly two time series.
- Remember that `ctw` expects 1D or 2D arrays representing individual time series `(sz, d)`, not 3D dataset arrays `(n_ts, sz, d)`.
- Take advantage of CTW's ability to compare time series with different feature dimensions (e.g., `d1 != d2`).
- If you need to compute gradients, pass PyTorch tensors with `requires_grad=True` and specify `be="pytorch"`.

### Prompt Snippet
```text
Use `tslearn.metrics.ctw(s1, s2)` to compute the Canonical Time Warping similarity between two time series. Unlike standard DTW, CTW aligns time series under rigid registration of the feature space, meaning `s1` and `s2` can have different lengths AND different dimensionalities (e.g., `(sz1, d1)` and `(sz2, d2)`). Pass individual 2D arrays, not 3D datasets.
```

### Common Failure Modes
- **Passing 3D datasets**: Providing arrays of shape `(n_ts, sz, d)` instead of individual time series `(sz, d)`. `ctw` compares exactly two time series, not two datasets.
- **Ambiguous constraints**: Providing both `sakoe_chiba_radius` and `itakura_max_slope` without explicitly setting `global_constraint` to choose between them. This raises a `RuntimeWarning` and ignores both constraints.
- **Invalid constraint string**: Setting `global_constraint` to a typo or unsupported string (must be exactly `"itakura"`, `"sakoe_chiba"`, or `None`).

### Fix Code Hint
```python
# BAD: Passing entire 3D datasets to ctw
# dist = ctw(X_train, X_test)

# GOOD: Passing individual 1D or 2D time series
dist = ctw(X_train[0], X_test[0])

# BAD: Ambiguous global constraints
# dist = ctw(s1, s2, sakoe_chiba_radius=3, itakura_max_slope=1.5)

# GOOD: Explicitly selecting the constraint
dist = ctw(s1, s2, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
```

## API Test: `ctw_path`

### Signature
```python
def ctw_path(s1, s2, max_iter=100, n_components=None, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, verbose=False, be=None)
```
_Source: tslearn/tslearn/metrics/ctw.py:46_

_Source doc:_ Compute Canonical Time Warping (CTW) similarity measure between (possibly multidimensional) time series and return the alignment path, the canonical correlation analysis (sklearn) object and the similarity. Canonical Time Warping is a method to align time series under rigid registration of the feature space. It should not be confused with Dynamic Time Warping (DTW), though CTW uses DTW. It is not required that both time series share the same size, nor the same dimension (CTW will find a subspace that best aligns feature spaces). CTW was originally presented in [1]_. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. max_iter : int (default: 100) Number of iterations for the CTW algorithm. Each iteration n_components : int (default: None) Number of components to be used for Canonical Correlation Analysis. If None, the lower minimum number of features between s1 and s2 is used. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for DTW calls. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. verbose : bool (default: True) If True, scores are printed at each iteration of the algorithm. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- list of integer pairs Matching path represented as a list of index pairs. In each pair, the first index corresponds to s1 and the second one corresponds to s2

### Goal
Compute the Canonical Time Warping (CTW) similarity measure between two time series, returning the alignment path, the fitted Canonical Correlation Analysis (CCA) object, and the final distance.

### Parameters
- `s1`: array-like, shape `(sz1, d1)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d2)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `max_iter`, default `100`: int. The maximum number of iterations for the CTW algorithm to alternate between CCA and DTW.
- `n_components`, default `None`: int. The number of components to be used for Canonical Correlation Analysis. If `None`, the minimum number of features between `s1` and `s2` is used.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. The global constraint to restrict admissible paths for the underlying DTW calls.
- `sakoe_chiba_radius`, default `None`: int or `None`. The radius to be used for the Sakoe-Chiba band global constraint.
- `itakura_max_slope`, default `None`: float or `None`. The maximum slope for the Itakura parallelogram constraint.
- `verbose`, default `False`: bool. If `True`, scores are printed at each iteration of the algorithm.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. The computational backend. If `None`, it is automatically inferred from the input arrays.

### Input
Two individual time series arrays (`s1` and `s2`). Unlike many `tslearn` estimators that require 3D datasets, these must be 1D or 2D arrays representing single time series. They do not need to share the same length (`sz1` vs `sz2`) nor the same feature dimension (`d1` vs `d2`), as CTW will find a subspace that best aligns their feature spaces.

### Output
Returns a tuple of three elements: `(path, cca, dist)`.
1. `path`: A list of integer index pairs `(i, j)` representing the matching alignment path, where `i` is an index from `s1` and `j` is an index from `s2`.
2. `cca`: The fitted `sklearn.cross_decomposition.CCA` object used to align the feature spaces.
3. `dist`: A float (or PyTorch scalar tensor) representing the final CTW similarity/distance score.

### Valid Call Patterns
```python
import tslearn.metrics

# s1 and s2 can have different lengths and different dimensions
s1 = [1, 2, 3]
s2 = [1.0, 2.0, 2.0, 3.0]

path, cca, dist = tslearn.metrics.ctw_path(s1, s2, be="numpy")

assert isinstance(path, list)
assert isinstance(path[0], tuple)
print(f"Path: {path}")
print(f"Distance: {dist}")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.ctw_path` to compute the Canonical Time Warping alignment path, CCA object, and distance between two individual time series.
- Pass 1D or 2D arrays for `s1` and `s2`, not 3D dataset arrays.
- Remember that `ctw_path` returns a tuple of three elements `(path, cca, dist)`, unlike `dtw_path` which only returns `(path, dist)`. Always unpack three variables.
- `s1` and `s2` are allowed to have different feature dimensions; CTW handles the subspace projection automatically.

### Prompt Snippet
```text
Calculate the Canonical Time Warping path and distance between the two multivariate time series `ts_a` (shape 10x3) and `ts_b` (shape 15x2). Extract the alignment path and the final distance score.
```

### Common Failure Modes
- **Unpacking Error**: Attempting to unpack the result into two variables (e.g., `path, dist = ctw_path(...)`). `ctw_path` returns three values: `path`, `cca`, and `dist`.
- **Passing 3D Datasets**: Passing a 3D array `(n_ts, sz, d)` instead of a single 2D time series `(sz, d)`. This function compares exactly two individual time series.
- **Conflicting Constraints**: Setting both `sakoe_chiba_radius` and `itakura_max_slope` without explicitly defining `global_constraint` to resolve which one to use, resulting in a `RuntimeWarning` and no constraint being applied.

### Fix Code Hint
```python
# WRONG: Unpacking into two variables
# path, dist = tslearn.metrics.ctw_path(s1, s2)

# CORRECT: Unpack into three variables
path, cca, dist = tslearn.metrics.ctw_path(s1, s2)

# WRONG: Passing 3D datasets
# path, cca, dist = tslearn.metrics.ctw_path(X_train, X_test)

# CORRECT: Pass individual time series (1D or 2D)
path, cca, dist = tslearn.metrics.ctw_path(X_train[0], X_test[0])
```

## API Test: `cydist_1d_sax`

### Signature
```python
def cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:135_

_Source doc:_ Compute distance between 1d-SAX representations as defined in [1]_. Parameters ---------- sax1 : array-like, shape=(sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) 1d-SAX representation of a time series. sax2 : array-like, shape=(sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) 1d-SAX representation of another time series. breakpoints_avg_middle_ : array-like, ndim=1, dtype=float64 breakpoints_slope_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dist_1d_sax : float64 1d-SAX distance. Notes ----- Unlike SAX distance, 1d-SAX distance does not lower bound Euclidean distance between original time series. References ---------- .. [1] S. Malinowski, T. Guyet, R. Quiniou, R. Tavenard. 1d-SAX: a Novel Symbolic Representation for Time Series. IDA 2013.

### Goal
Compute the distance between two 1d-SAX (1-dimensional Symbolic Aggregate approXimation) representations of time series using a low-level Cython backend helper.

### Parameters
- `sax1`: array-like, shape=(sz, 2 * d). The 1d-SAX representation of the first time series.
- `sax2`: array-like, shape=(sz, 2 * d). The 1d-SAX representation of the second time series.
- `breakpoints_avg_middle_`: array-like, ndim=1. The middle values of the breakpoints for the average component.
- `breakpoints_slope_middle_`: array-like, ndim=1. The middle values of the breakpoints for the slope component.
- `original_size`: int. The length of the original time series before it was transformed into the 1d-SAX representation.

### Input
The caller must provide pre-computed 1d-SAX representations (`sax1` and `sax2`) as 2D NumPy arrays of shape `(sz, 2 * d)`, where `sz` is the number of segments and `d` is the dimensionality. The breakpoint arrays must be 1D NumPy arrays of type `float64`. The `original_size` must be an integer. Note that data types are platform-dependent (e.g., `float64` and `int64` on Linux/macOS, `float32` and `int32` on Windows), but standard NumPy arrays will typically be cast appropriately by Cython.

### Output
Returns `float64` — A scalar float representing the 1d-SAX distance between the two representations. Note that unlike standard SAX distance, this metric does not lower-bound the Euclidean distance between the original time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import cydist_1d_sax

# Example inferred from signature (not verified)
sz = 3
d = 1
# Create dummy 1d-SAX representations of shape (sz, 2 * d)
sax1 = np.zeros((sz, 2 * d), dtype=np.float64)
sax2 = np.ones((sz, 2 * d), dtype=np.float64)

# Create dummy breakpoint middle values
breakpoints_avg_middle = np.array([-0.5, 0.5], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

original_size = 15

dist = cydist_1d_sax(
    sax1, 
    sax2, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)

print(f"1d-SAX distance: {dist}")
assert isinstance(dist, float)
```

### LLM Instruction Prompt
- Use `cydist_1d_sax` only when you need to compute the distance between pre-computed 1d-SAX representations.
- Do not pass raw time-series data to this function; it expects the symbolic representations of shape `(sz, 2 * d)`.
- Ensure that `breakpoints_avg_middle_` and `breakpoints_slope_middle_` are strictly 1-dimensional arrays.
- Remember to pass the `original_size` of the time series as an integer, as it is required for the distance scaling.

### Prompt Snippet
```text
When calculating the distance between 1d-SAX representations, use `tslearn.metrics.cysax.cydist_1d_sax(sax1, sax2, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)`. Ensure `sax1` and `sax2` are 2D arrays of shape `(sz, 2 * d)`, the breakpoints are 1D arrays, and `original_size` is an integer.
```

### Common Failure Modes
- Passing raw 3D time-series datasets `(n_ts, max_sz, d)` instead of the 2D 1d-SAX representations `(sz, 2 * d)`.
- Providing multi-dimensional arrays for the breakpoint parameters, which will cause Cython buffer shape errors.
- Forgetting to pass the `original_size` argument, resulting in a `TypeError` for missing required positional arguments.
- Shape mismatches between `sax1` and `sax2` (they must have the same number of segments and dimensions).

### Fix Code Hint
```python
# FIX: Ensure inputs are 2D SAX representations and breakpoints are 1D arrays
sax1 = np.asarray(sax1, dtype=np.float64)
sax2 = np.asarray(sax2, dtype=np.float64)
bp_avg = np.asarray(breakpoints_avg_middle_, dtype=np.float64).flatten()
bp_slope = np.asarray(breakpoints_slope_middle_, dtype=np.float64).flatten()

dist = cydist_1d_sax(sax1, sax2, bp_avg, bp_slope, int(original_size))
```

## API Test: `cydist_sax`

### Signature
```python
def cydist_sax(sax1, sax2, breakpoints, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:38_

_Source doc:_ Compute distance between SAX representations as defined in [1]_. Parameters ---------- sax1 : array-like, shape=(sz, d) SAX representation of a time series. sax2 : array-like, shape=(sz, d) SAX representation of another time series. breakpoints : array-like, ndim=1, dtype=float64 The breakpoints used to assign the alphabet symbols. original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dist_sax : float64 SAX distance. References ---------- .. [1] J. Lin, E. Keogh, L. Wei, et al. Experiencing SAX: a novel symbolic representation of time series. Data Mining and Knowledge Discovery, 2007. vol. 15(107)

### Goal
Compute the distance between two Symbolic Aggregate approXimation (SAX) representations of time series using a low-level Cython backend helper.

### Parameters
- `sax1`: array-like, shape=(sz, d). The SAX representation of the first time series (typically integer symbols).
- `sax2`: array-like, shape=(sz, d). The SAX representation of the second time series.
- `breakpoints`: array-like, ndim=1, dtype=float64. The breakpoints used to assign the alphabet symbols during the SAX transformation.
- `original_size`: int. The length of the original time series before it was reduced to the SAX representation.

### Input
- `sax1` and `sax2` must be 2D arrays of the exact same shape `(sz, d)`.
- `breakpoints` must be a 1D NumPy array strictly of type `float64`.
- `original_size` must be an integer. Due to Cython bindings, it expects a 64-bit integer on Linux/macOS and a 32-bit integer on Windows; passing a standard Python `int` allows Cython to handle the platform-specific C-integer casting automatically.

### Output
Returns `float64` — The computed SAX distance between the two representations as a scalar float.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import cydist_sax

# Example inferred from signature
sax1 = np.array([[0], [1], [2]], dtype=np.int32)
sax2 = np.array([[1], [1], [1]], dtype=np.int32)
breakpoints = np.array([-0.43, 0.43], dtype=np.float64)
original_size = 10

dist = cydist_sax(sax1, sax2, breakpoints, original_size)
print(f"SAX Distance: {dist}")
assert isinstance(dist, float)
```

### LLM Instruction Prompt
- Use `cydist_sax` only when you need to compute distances between already-transformed SAX representations.
- Ensure `sax1` and `sax2` are 2D arrays of shape `(sz, d)`. Do not pass 1D arrays.
- Ensure `breakpoints` is a 1D array explicitly cast to `dtype=np.float64`.
- Pass `original_size` as a standard Python `int` to avoid platform-specific Cython `TypeError`s (int32 on Windows vs int64 on POSIX) that can occur if passing explicitly typed NumPy scalar integers.

### Prompt Snippet
```text
Ensure `sax1` and `sax2` are 2D arrays `(sz, d)`. `breakpoints` must be a 1D `float64` array. Pass `original_size` as a standard Python `int`.
```

### Common Failure Modes
- Passing 1D arrays for `sax1` or `sax2`, which violates the expected `(sz, d)` shape and causes Cython memoryview errors.
- Passing `breakpoints` as a list or an array with an integer dtype, which fails the strict `float64` Cython type requirement.
- Passing a NumPy scalar like `np.int64(10)` for `original_size` on a Windows machine, which expects a 32-bit integer, resulting in a `TypeError`.

### Fix Code Hint
```python
# FIX: Ensure 2D shapes, float64 breakpoints, and standard Python int for original_size
sax1 = np.atleast_2d(sax1_1d).T
sax2 = np.atleast_2d(sax2_1d).T
breakpoints = np.asarray(breakpoints, dtype=np.float64)
original_size = int(original_size)
dist = cydist_sax(sax1, sax2, breakpoints, original_size)
```

## API Test: `cyslopes`

### Signature
```python
def cyslopes(dataset, t0)
```
_Source: tslearn/tslearn/metrics/cysax.py:107_

_Source doc:_ Compute slopes. Parameters ---------- dataset : array-like, shape=(n_ts, sz, d), dtype=float64 t0 : int32 Returns ------- dataset_out : array-like, shape=(n_ts, d), dtype=float64

### Goal
Compute the slopes of time series within a dataset, acting as a low-level Cython backend helper for Symbolic Aggregate approXimation (SAX) or related representations.

### Parameters
- `dataset`: A 3D array-like object of shape `(n_ts, sz, d)` and dtype `float64` representing a collection of time series.
- `t0`: An `int32` representing the time step or interval parameter for the slope computation.

### Input
The caller must provide a strictly formatted 3D numpy array `(n_ts, sz, d)` of type `float64`. The `t0` parameter must be an integer. If the data is not 3D, it must be converted first (e.g., using `tslearn.utils.to_time_series_dataset`).

### Output
Returns `unspecified` — An array-like object (typically a numpy array) of shape `(n_ts, d)` and dtype `float64` containing the computed slopes for each time series across each dimension.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cysax import cyslopes

# Inferred from signature (not verified)
# n_ts=2, sz=3, d=1
dataset = np.array([
    [[1.0], [2.0], [3.0]], 
    [[4.0], [5.0], [6.0]]
], dtype=np.float64)
t0 = 1

slopes = cyslopes(dataset, t0)

assert slopes.shape == (2, 1), "Output shape must be (n_ts, d)"
print("cyslopes executed successfully.")
```

### LLM Instruction Prompt
- Ensure `dataset` is strictly a 3D array of shape `(n_ts, sz, d)` and dtype `float64`.
- Ensure `t0` is an integer (`int32`).
- Import `cyslopes` directly from `tslearn.metrics.cysax`.
- Note that this is a low-level backend helper function; standard users should typically use higher-level estimators unless explicitly building custom metrics.

### Prompt Snippet
```text
Use `tslearn.metrics.cysax.cyslopes(dataset, t0)` to compute slopes for a time-series dataset. The `dataset` must be a 3D array of shape `(n_ts, sz, d)` with dtype `float64`, and `t0` must be an integer.
```

### Common Failure Modes
- **Incorrect Array Dimensions:** Passing a 1D or 2D array instead of the required 3D `(n_ts, sz, d)` format.
- **Incorrect Data Type:** Passing a dataset with a dtype other than `float64`, which may cause Cython type errors or unexpected behavior.
- **Invalid `t0` Type:** Passing a float or non-integer for `t0` when an `int32` is expected.

### Fix Code Hint
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.metrics.cysax import cyslopes

# Ensure dataset is strictly 3D and float64
dataset_3d = to_time_series_dataset(raw_data).astype(np.float64)
t0_int = int(t0)

slopes = cyslopes(dataset_3d, t0_int)
```

## API Test: `decision_function`

### Signature
```python
def decision_function(self, X)
```
_Source: tslearn/tslearn/svm/svm.py:352_

_Source doc:_ Evaluates the decision function for the samples in X. Parameters ---------- X : array-like of shape=(n_ts, sz, d) Time series dataset. Returns ------- ndarray of shape (n_samples, n_classes * (n_classes-1) / 2) Returns the decision function of the sample for each class in the model. If decision_function_shape='ovr', the shape is (n_samples, n_classes).

### Goal
Evaluates the decision function (e.g., the distance to the separating hyperplane) for each class in a fitted time-series support vector machine model.

### Parameters
- `self`: A fitted instance of a `tslearn` classifier that supports decision functions (e.g., `TimeSeriesSVC`).
- `X`: The time-series dataset to evaluate, formatted as a 3D array-like of shape `(n_ts, sz, d)`.

### Input
- `X` must be strictly formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. If starting from raw lists or variable-length sequences, it must be converted using `tslearn.utils.to_time_series_dataset` first.
- The estimator instance (`self`) must be fitted with training data before calling this method.

### Output
Returns `unspecified` — A `numpy.ndarray` representing the decision function scores for the samples in `X`. The shape is `(n_samples, n_classes * (n_classes-1) / 2)` by default, or `(n_samples, n_classes)` if the estimator was configured with `decision_function_shape='ovr'`. For binary classification, it typically returns a 1D array of shape `(n_samples,)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Prepare deterministic 3D time-series data (n_ts, max_sz, d)
X_train = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.5], [2.5], [3.5]], 
    [[8.0], [9.0], [10.0]], 
    [[8.5], [9.5], [10.5]]
])
y_train = np.array([0, 0, 1, 1])

# 2. Initialize and fit the classifier
clf = TimeSeriesSVC(kernel="euclidean")
clf.fit(X_train, y_train)

# 3. Evaluate the decision function on new 3D data
X_test = np.array([
    [[1.2], [2.2], [3.2]], 
    [[8.2], [9.2], [10.2]]
])
scores = clf.decision_function(X_test)

assert isinstance(scores, np.ndarray)
assert scores.shape[0] == X_test.shape[0]
print("Decision function scores:\n", scores)
```
_Note: This example is inferred from the signature and standard `tslearn` / `scikit-learn` conventions, as no verbatim example was found in the context._

### LLM Instruction Prompt
- Call `decision_function` as an instance method on a fitted classifier (like `TimeSeriesSVC`), never as a standalone function.
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists or variable-length sequences before passing them to this method.
- Do not call this method before calling `.fit()` on the estimator.

### Prompt Snippet
```text
# Evaluate the decision function on the test set
# Ensure X_test is a 3D array (n_ts, max_sz, d)
decision_scores = clf.decision_function(X_test)
```

### Common Failure Modes
- **`ValueError: Expected 3D array`**: Occurs if `X` is passed as a 1D or 2D array. `tslearn` strictly requires the `(n_ts, max_sz, d)` format.
- **`NotFittedError`**: Occurs if `decision_function` is called before the model has been fitted with `.fit()`.
- **`AttributeError`**: Occurs if attempting to call `decision_function` as a standalone function from the module rather than as a method on an instantiated estimator.

### Fix Code Hint
```python
# WRONG: Passing a 2D array or calling before fitting
# scores = clf.decision_function([[1, 2], [3, 4]])

# RIGHT: Convert to 3D array and ensure the model is fitted
from tslearn.utils import to_time_series_dataset

X_test_3d = to_time_series_dataset([[1, 2], [3, 4]])
# clf.fit(X_train_3d, y_train) # Must be called first
scores = clf.decision_function(X_test_3d)
```

## API Test: `distance`

### Signature
```python
def distance(self, ts1, ts2)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:219  (+2 more definition site/overload)_

_Source doc:_ Compute distance between PAA representations as defined in [1]_. Parameters ---------- ts1 : array-like A time series ts2 : array-like Another time series Returns ------- float PAA distance References ---------- .. [1] E. Keogh & M. Pazzani. Scaling up dynamic time warping for datamining applications. SIGKDD 2000, pp. 285--289.

### Goal
Compute the distance between the Piecewise Aggregate Approximation (PAA) or Symbolic Aggregate Approximation (SAX) representations of two time series.

### Parameters
- `self`: A fitted instance of a piecewise transformation estimator (e.g., `PiecewiseAggregateApproximation` or `SymbolicAggregateApproximation`).
- `ts1`: array-like. The first time series to compare.
- `ts2`: array-like. The second time series to compare.

### Input
Two individual time series (e.g., 1D lists or 2D arrays of shape `(max_sz, d)`). The estimator instance (`self`) must already be fitted on a dataset to establish the transformation parameters (like segment bounds or SAX bins).

### Output
Returns `unspecified` — A `float` representing the PAA or SAX distance between the two time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PiecewiseAggregateApproximation

paa_est = PiecewiseAggregateApproximation(n_segments=3)
X = np.array([[[-1.0], [2.0], [0.1], [-1.0], [1.0], [-1.0]], 
              [[1.0], [3.2], [-1.0], [-3.0], [1.0], [-1.0]]])

# The estimator must be fitted before computing distances
paa_est.fit(X)

# Compute distance between two individual time series
dist = paa_est.distance(X[0], X[1])

assert isinstance(dist, float)
print(f"PAA distance: {dist}")
```

### LLM Instruction Prompt
- Always call `.fit()` or `.fit_transform()` on the piecewise estimator before calling `.distance()`.
- Pass individual time series (e.g., 1D or 2D arrays) as `ts1` and `ts2`, not the entire 3D dataset `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
# Fit the estimator first to avoid NotFittedError
paa = PiecewiseAggregateApproximation(n_segments=3).fit(X)

# Calculate distance between two specific time series
dist = paa.distance(X[0], X[1])
```

### Common Failure Modes
- **`NotFittedError`**: Raised if `.distance()` is called before the estimator has been fitted with `.fit()`.
- **Dimension mismatch**: Passing a full 3D dataset `(n_ts, max_sz, d)` instead of a single time series `(max_sz, d)` for `ts1` or `ts2`.

### Fix Code Hint
```python
# WRONG: Calling distance on an unfitted estimator
paa = PiecewiseAggregateApproximation(n_segments=3)
dist = paa.distance(ts1, ts2)  # Raises NotFittedError

# CORRECT: Fit the estimator first
paa = PiecewiseAggregateApproximation(n_segments=3)
paa.fit(X_train)
dist = paa.distance(ts1, ts2)
```

## API Test: `distance_1d_sax`

### Signature
```python
def distance_1d_sax(self, sax1, sax2)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:726_

_Source doc:_ Compute distance between 1d-SAX representations as defined in [1]_. Parameters ---------- sax1 : array-like 1d-SAX representation of a time series sax2 : array-like 1d-SAX representation of another time series Returns ------- float 1d-SAX distance Notes ----- Unlike SAX distance, 1d-SAX distance does not lower bound Euclidean distance between original time series. References ---------- .. [1] S. Malinowski, T. Guyet, R. Quiniou, R. Tavenard. 1d-SAX: a Novel Symbolic Representation for Time Series. IDA 2013.

### Goal
Compute the distance between two 1d-SAX (1-dimensional Symbolic Aggregate approXimation) representations of time series.

### Parameters
- `self`: A fitted instance of `OneD_SymbolicAggregateApproximation` that provides the alphabet and segment parameters used to define the 1d-SAX space.
- `sax1`: Array-like 1d-SAX representation of the first time series (typically the output of the estimator's `transform` or `fit_transform` method).
- `sax2`: Array-like 1d-SAX representation of the second time series.

### Input
The caller must provide two 1d-SAX transformed arrays, not raw time series. The estimator (`self`) must be instantiated and fitted on a 3D `(n_ts, max_sz, d)` time-series dataset to establish the alphabet bounds and scaling parameters before transforming the inputs and computing their distance.

### Output
Returns `float` — The computed 1d-SAX distance between the two symbolic representations. Note that unlike standard SAX distance, 1d-SAX distance does not lower-bound the Euclidean distance between the original time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import OneD_SymbolicAggregateApproximation

# 1. Prepare deterministic in-memory 3D time-series data (n_ts, max_sz, d)
X = np.array([
    [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]],
    [[1.5], [2.5], [3.5], [4.5], [5.5], [6.5]]
])

# 2. Instantiate and fit the 1d-SAX estimator
sax1d_est = OneD_SymbolicAggregateApproximation(
    n_segments=2, 
    alphabet_size_avg=2, 
    alphabet_size_slope=2
)
sax1d_repr = sax1d_est.fit_transform(X)

# 3. Compute the distance between the 1d-SAX representations
dist = sax1d_est.distance_1d_sax(sax1d_repr[0], sax1d_repr[1])

# 4. Assert falsifiable property and print witness
assert isinstance(dist, float), "Distance must be a float"
print(f"1d-SAX distance: {dist}")
```

### LLM Instruction Prompt
When calling `distance_1d_sax`, ensure it is called as an instance method on a fitted `OneD_SymbolicAggregateApproximation` object. You MUST pass two 1d-SAX representations (the outputs of `transform` or `fit_transform`), NOT the raw time-series arrays.

### Prompt Snippet
```text
sax1d_repr = sax1d_est.fit_transform(X)
dist = sax1d_est.distance_1d_sax(sax1d_repr[0], sax1d_repr[1])
```

### Common Failure Modes
- **Passing raw time series:** Providing the original `(max_sz, d)` time-series arrays instead of the transformed 1d-SAX representations will result in incorrect distance calculations or shape mismatch errors.
- **Calling on an unfitted estimator:** Attempting to compute distances before calling `fit()` or `fit_transform()` on the `OneD_SymbolicAggregateApproximation` instance will raise a `NotFittedError` because the alphabet breakpoints are not yet defined.
- **Calling as a static function:** Attempting to call `tslearn.piecewise.distance_1d_sax(sax1, sax2)` directly will fail; it must be called on the estimator instance.

### Fix Code Hint
```python
# BAD: Passing raw time series to the distance function
# dist = sax1d_est.distance_1d_sax(X[0], X[1])

# GOOD: Transform the data first, then compute distance on the representations
sax1d_repr = sax1d_est.transform(X)
dist = sax1d_est.distance_1d_sax(sax1d_repr[0], sax1d_repr[1])
```

## API Test: `distance_paa`

### Signature
```python
def distance_paa(self, paa1, paa2)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:195_

_Source doc:_ Compute distance between PAA representations as defined in [1]_. Parameters ---------- paa1 : array-like PAA representation of a time series paa2 : array-like PAA representation of another time series Returns ------- float PAA distance References ---------- .. [1] E. Keogh & M. Pazzani. Scaling up dynamic time warping for datamining applications. SIGKDD 2000, pp. 285--289.

### Goal
Compute the distance between two Piecewise Aggregate Approximation (PAA) representations of time series.

### Parameters
- `self`: A fitted `PiecewiseAggregateApproximation` estimator instance.
- `paa1`: An array-like PAA representation of the first time series.
- `paa2`: An array-like PAA representation of the second time series.

### Input
`paa1` and `paa2` must be transformed PAA representations, not raw time series. They are typically obtained by calling `.fit_transform()` or `.transform()` on a `PiecewiseAggregateApproximation` instance. The inputs should represent individual time series (e.g., sliced from the 3D transformed dataset array).

### Output
Returns `unspecified` — A `float` representing the computed PAA distance between the two representations.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PiecewiseAggregateApproximation

# 1. Prepare a 3D time-series dataset (n_ts, max_sz, d)
X = np.array([
    [[1.0], [2.0], [3.0], [4.0]], 
    [[4.0], [3.0], [2.0], [1.0]]
])

# 2. Instantiate and fit the PAA estimator
paa_est = PiecewiseAggregateApproximation(n_segments=2)
paa_repr = paa_est.fit_transform(X)

# 3. Compute distance between the PAA representations of the first two series
dist = paa_est.distance_paa(paa_repr[0], paa_repr[1])

assert isinstance(dist, float)
print(f"PAA distance: {dist}")
```

### LLM Instruction Prompt
- Call `distance_paa` as an instance method on a `PiecewiseAggregateApproximation` object, never as a standalone function.
- Pass individual PAA representations (e.g., `paa_repr[0]`), not the entire 3D dataset.
- Do not pass raw time series to `distance_paa`; if you have raw time series, either transform them first using `.transform()` or use the `.distance()` method instead.

### Prompt Snippet
```text
To compute the distance between PAA representations, instantiate `PiecewiseAggregateApproximation`, transform your 3D dataset, and call `paa_est.distance_paa(paa_repr[0], paa_repr[1])`. Ensure inputs are the transformed representations, not raw time series.
```

### Common Failure Modes
- **Passing raw time series:** Providing raw time series arrays instead of their PAA representations will result in incorrect distance calculations or shape mismatches.
- **Passing full 3D datasets:** Passing the entire `(n_ts, n_segments, d)` array instead of slicing individual time series (e.g., `paa_repr[0]`) will cause broadcasting errors.
- **Calling as a static function:** Attempting to import and call `distance_paa(paa1, paa2)` directly will fail with a `NameError` or missing `self` argument.

### Fix Code Hint
```python
# WRONG: Passing raw time series or calling as a standalone function
# dist = distance_paa(X[0], X[1])

# CORRECT: Instantiate estimator, transform data, and call on the instance
from tslearn.piecewise import PiecewiseAggregateApproximation

paa_est = PiecewiseAggregateApproximation(n_segments=3)
paa_repr = paa_est.fit_transform(X)
dist = paa_est.distance_paa(paa_repr[0], paa_repr[1])
```

## API Test: `distance_sax`

### Signature
```python
def distance_sax(self, sax1, sax2)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:444_

_Source doc:_ Compute distance between SAX representations as defined in [1]_. Parameters ---------- sax1 : array-like SAX representation of a time series sax2 : array-like SAX representation of another time series Returns ------- float SAX distance References ---------- .. [1] J. Lin, E. Keogh, L. Wei, et al. Experiencing SAX: a novel symbolic representation of time series. Data Mining and Knowledge Discovery, 2007. vol. 15(107)

### Goal
Compute the distance between two Symbolic Aggregate approXimation (SAX) representations of time series.

### Parameters
- `self`: A fitted instance of `tslearn.piecewise.SymbolicAggregateApproximation`.
- `sax1`: Array-like SAX representation of the first time series (typically an array of integers representing symbols).
- `sax2`: Array-like SAX representation of the second time series.

### Input
`sax1` and `sax2` must be valid SAX representations generated by the `transform` or `fit_transform` methods of the same `SymbolicAggregateApproximation` instance. The estimator (`self`) must be fitted before calling this method, as the distance calculation relies on the breakpoints learned during `fit`.

### Output
Returns `unspecified` — A `float` representing the computed SAX distance between the two representations.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import SymbolicAggregateApproximation

# 1. Initialize and fit the SAX estimator
sax_est = SymbolicAggregateApproximation(n_segments=3, alphabet_size_avg=2)
X = np.random.RandomState(0).randn(2, 10, 3)
sax_repr = sax_est.fit_transform(X)

# 2. Compute the distance between the SAX representations of the two time series
dist = sax_est.distance_sax(sax_repr[0], sax_repr[1])
assert isinstance(dist, float)
```

### LLM Instruction Prompt
- Call `distance_sax` only on a fitted `SymbolicAggregateApproximation` instance.
- Pass the transformed SAX representations (the output of `transform`), not the raw time-series data. To compute the distance directly from raw time series, use the `distance(ts1, ts2)` method instead.
- Ensure both SAX representations were generated using the same alphabet size and breakpoints.

### Prompt Snippet
```text
To compute the distance between two SAX representations, use `sax_est.distance_sax(sax1, sax2)`. The estimator must be fitted first, and the inputs must be the transformed integer arrays, not the raw 3D time-series arrays.
```

### Common Failure Modes
- **`NotFittedError`**: Calling `distance_sax` on an unfitted `SymbolicAggregateApproximation` instance. The estimator needs to learn breakpoints before it can compute distances.
- **Passing raw time series**: Providing raw float arrays instead of the integer SAX representations. This will result in incorrect distance calculations or type errors.
- **Mismatched dimensions**: Passing full 3D datasets `(n_ts, max_sz, d)` instead of individual representations `(n_segments, d)`.

### Fix Code Hint
```python
# WRONG: Passing raw time series or using an unfitted estimator
# dist = sax_est.distance_sax(X[0], X[1])

# CORRECT: Fit the estimator, transform the data, and pass the representations
sax_est.fit(X)
sax_repr = sax_est.transform(X)
dist = sax_est.distance_sax(sax_repr[0], sax_repr[1])
```

## API Test: `dtw`

### Signature
```python
def dtw(s1, s2, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/_dtw.py:30  (+1 more definition site/overload)_

_Source doc:_ Compute Dynamic Time Warping (DTW) similarity measure between (possibly multidimensional) time series and return it. DTW is computed as the Euclidean distance between aligned time series, i.e., if :math:`\pi` is the optimal alignment path: .. math:: DTW(X, Y) = \sqrt{\sum_{(i, j) \in \pi} \|X_{i} - Y_{j}\|^2} Note that this formula is still valid for the multivariate case. It is not required that both time series share the same size, but they must be the same dimension. DTW was originally presented in [1]_ and is discussed in more details in our :ref:`dedicated user-guide page <dtw>`. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for DTW. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [1]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns -------

### Goal
Compute the Dynamic Time Warping (DTW) similarity measure (the Euclidean distance between optimally aligned points) between two possibly multidimensional time series.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. Must have the same number of dimensions `d` as `s1`.
- `global_constraint`, default `None`: String `{"itakura", "sakoe_chiba"}` or `None`. Restricts admissible paths for DTW to speed up computation and prevent pathological warpings.
- `sakoe_chiba_radius`, default `None`: Integer or `None`. Radius for the Sakoe-Chiba band constraint. If `None` and `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: Float or `None`. Maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint="itakura"`, defaults to 2.0.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. If `None`, the backend is automatically inferred from the input arrays.

### Input
Two time series arrays (NumPy arrays, lists, or PyTorch tensors). They can have different lengths (number of time steps `sz1` vs `sz2`) but must have the exact same feature dimensionality `d`.

### Output
Returns `unspecified` — A scalar float (if using the NumPy backend) or a 0-dimensional PyTorch tensor (if using the PyTorch backend) representing the computed DTW distance.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# Two time series of different lengths but the same dimension (d=1)
x = np.array([[1.0], [2.0], [3.0]])
y = np.array([[1.0], [2.0], [2.0], [3.0]])

# Compute standard DTW distance
distance = tslearn.metrics.dtw(x, y)

assert np.isclose(distance, 0.0), "Identical sequences with stuttering should have 0.0 DTW distance"
print(f"DTW distance: {distance}")

# Compute DTW distance with a Sakoe-Chiba band constraint
constrained_distance = tslearn.metrics.dtw(x, y, global_constraint="sakoe_chiba", sakoe_chiba_radius=1)
print(f"Constrained DTW distance: {constrained_distance}")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.dtw`, ensure both time series have the same feature dimension `d`.
- Pass `be="pytorch"` or provide PyTorch tensors if you need the output to be a PyTorch tensor. Note that standard `dtw` is not differentiable; use `soft_dtw` with `compute_with_backend=True` if you need to compute gradients via `.backward()`.
- Use `global_constraint="sakoe_chiba"` with `sakoe_chiba_radius` or `global_constraint="itakura"` with `itakura_max_slope` to speed up computation and restrict warping paths.

### Prompt Snippet
```text
Use `tslearn.metrics.dtw(s1, s2)` to compute the Dynamic Time Warping distance between two time series. Both inputs must have the same feature dimension `d`, though their lengths can differ. To restrict the warping path, use `global_constraint="sakoe_chiba"` and set `sakoe_chiba_radius`.
```

### Common Failure Modes
- Passing time series with different feature dimensions (e.g., `s1` has shape `(10, 2)` and `s2` has shape `(15, 3)`). This will raise a `ValueError`.
- Setting both `sakoe_chiba_radius` and `itakura_max_slope` without specifying `global_constraint`. This raises a `RuntimeWarning` and ignores the constraints because the function does not know which one to apply.
- Attempting to call `.backward()` on the output of `dtw` when using PyTorch tensors. Standard DTW is not differentiable; `soft_dtw` must be used for automatic differentiation.

### Fix Code Hint
```python
# Ensure both time series have the same dimension `d`
if s1.shape[-1] != s2.shape[-1]:
    raise ValueError("Time series must have the same feature dimension.")

# Correctly apply a global constraint by explicitly setting `global_constraint`
dist = tslearn.metrics.dtw(s1, s2, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
```

## API Test: `dtw_barycenter_averaging`

### Signature
```python
def dtw_barycenter_averaging(X, barycenter_size=None, init_barycenter=None, max_iter=30, tol=1e-05, weights=None, metric_params=None, verbose=False, n_init=1, n_jobs=None)
```
_Source: tslearn/tslearn/barycenters/dba.py:485_

_Source doc:_ DTW Barycenter Averaging (DBA) method estimated through Expectation-Maximization algorithm. DBA was originally presented in [1]_. This implementation is based on an idea from [2]_ (Majorize-Minimize Mean Algorithm). Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. barycenter_size : int or None (default: None) Size of the barycenter to generate. If None, the size of the barycenter is that of the data provided at fit time or that of the initial barycenter if specified. init_barycenter : array or None (default: None) Initial barycenter to start from for the optimization process. max_iter : int (default: 30) Number of iterations of the Expectation-Maximization optimization procedure. tol : float (default: 1e-5) Tolerance to use for early stopping: if the decrease in cost is lower than this value, the Expectation-Maximization procedure stops. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. metric_params: dict or None (default: None) DTW constraint parameters to be used. See :ref:`tslearn.metrics.dtw_path <fun-tslearn.metrics.dtw_path>` for a list of accepted parameters If None, no constraint is used for DTW computations. verbose : boolean (default: False) Whether to print information about the cost at each iteration or not. n_init : int (default: 1) Number of different initializations to be tried (useful only is init_barycenter is set to None, otherwise, all trials will reach the same performance) n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. Returns ------- numpy.array of shape (barycenter_size, d) or (sz, d) if barycenter_size \ is None DBA barycenter of the provided time series dataset.

### Goal
Computes the DTW Barycenter Averaging (DBA) of a time-series dataset using an Expectation-Maximization algorithm to find a representative average sequence.

### Parameters
- `X`: array-like, shape `(n_ts, sz, d)`. The time-series dataset to average.
- `barycenter_size`, default `None`: int or None. The desired length of the generated barycenter. If `None`, defaults to the length of the input data (`sz`) or the `init_barycenter`.
- `init_barycenter`, default `None`: array or None. An initial barycenter sequence to start the optimization process.
- `max_iter`, default `30`: int. The maximum number of iterations for the Expectation-Maximization optimization procedure.
- `tol`, default `1e-05`: float. Tolerance for early stopping; the procedure stops if the cost decrease is below this threshold.
- `weights`, default `None`: array or None. Weights for each time series in `X`. Must be of length `len(X)`. If `None`, uniform weights are applied.
- `metric_params`, default `None`: dict or None. DTW constraint parameters (e.g., `{"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3}`).
- `verbose`, default `False`: boolean. Whether to print cost information at each iteration.
- `n_init`, default `1`: int. Number of different initializations to try (only useful if `init_barycenter` is `None`).
- `n_jobs`, default `None`: int or None. The number of parallel jobs to run. `-1` uses all available processors.

### Input
`X` must be a 3D array of shape `(n_ts, sz, d)` representing the number of time series, the maximum sequence length, and the number of dimensions. Raw lists of variable-length time series must be converted and padded using `tslearn.utils.to_time_series_dataset` before being passed to this function.

### Output
Returns `numpy.array` — A 2D NumPy array of shape `(barycenter_size, d)` (or `(sz, d)` if `barycenter_size` is `None`) representing the computed DBA barycenter of the dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging
from tslearn.utils import to_time_series_dataset

# 1. Basic usage with a formatted 3D dataset
X_raw = [[1.0, 2.0, 3.0], [1.0, 2.0, 2.0], [2.0, 2.0, 3.0]]
X = to_time_series_dataset(X_raw)

barycenter = dtw_barycenter_averaging(X, max_iter=5)
assert barycenter.shape == (3, 1)
print(f"Barycenter shape: {barycenter.shape}")

# 2. Specifying a custom barycenter size and DTW constraints
barycenter_custom = dtw_barycenter_averaging(
    X, 
    barycenter_size=5, 
    max_iter=10,
    metric_params={"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 1}
)
assert barycenter_custom.shape == (5, 1)
```

### LLM Instruction Prompt
- Always ensure the input `X` is a strictly 3D array `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists or 2D arrays before calling `dtw_barycenter_averaging`.
- If providing `weights`, ensure the length of the weights array exactly matches `len(X)`.
- Keep `max_iter` small (e.g., 5-10) in testing or constrained environments to avoid long execution times, as DBA can be computationally expensive.

### Prompt Snippet
```text
Compute the DTW barycenter of a list of time series `[ts1, ts2, ts3]` using `dtw_barycenter_averaging`. Ensure the data is formatted as a 3D array first. Set `max_iter=5` and `barycenter_size=4`.
```

### Common Failure Modes
- **ValueError (Dimensionality):** Passing a 1D or 2D array directly instead of a 3D array `(n_ts, sz, d)`. Always preprocess with `to_time_series_dataset`.
- **ValueError (Weights mismatch):** Providing a `weights` array that does not have exactly `n_ts` elements.
- **Performance Hangs:** Leaving `max_iter` at its default (30) on large datasets without setting `n_jobs=-1`, causing the EM algorithm to run slowly on a single thread.

### Fix Code Hint
```python
# FIX: Convert 2D array or list of lists to the required 3D shape (n_ts, sz, d)
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
barycenter = dtw_barycenter_averaging(X_3d, max_iter=5)
```

## API Test: `dtw_barycenter_averaging_one_init`

### Signature
```python
def dtw_barycenter_averaging_one_init(X, barycenter_size=None, init_barycenter=None, max_iter=30, tol=1e-05, weights=None, metric_params=None, verbose=False, n_jobs=None)
```
_Source: tslearn/tslearn/barycenters/dba.py:621_

_Source doc:_ DTW Barycenter Averaging (DBA) method estimated through Expectation-Maximization algorithm. DBA was originally presented in [1]_. This implementation is based on a idea from [2]_ (Majorize-Minimize Mean Algorithm). Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. barycenter_size : int or None (default: None) Size of the barycenter to generate. If None, the size of the barycenter is that of the data provided at fit time or that of the initial barycenter if specified. init_barycenter : array or None (default: None) Initial barycenter to start from for the optimization process. max_iter : int (default: 30) Number of iterations of the Expectation-Maximization optimization procedure. tol : float (default: 1e-5) Tolerance to use for early stopping: if the decrease in cost is lower than this value, the Expectation-Maximization procedure stops. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. metric_params: dict or None (default: None) DTW constraint parameters to be used. See :ref:`tslearn.metrics.dtw_path <fun-tslearn.metrics.dtw_path>` for a list of accepted parameters If None, no constraint is used for DTW computations. verbose : boolean (default: False) Whether to print information about the cost at each iteration or not. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. Returns ------- numpy.array of shape (barycenter_size, d) or (sz, d) if barycenter_size \ is None DBA barycenter of the provided time series dataset. float Associated inertia References ----------

### Goal
Computes the Dynamic Time Warping (DTW) Barycenter Averaging (DBA) for a time-series dataset using a single initialization of the Expectation-Maximization algorithm.

### Parameters
- `X`: array-like, shape `(n_ts, sz, d)`. The time-series dataset to average.
- `barycenter_size`, default `None`: int or None. The length of the generated barycenter. If `None`, defaults to the size of the data or the initial barycenter.
- `init_barycenter`, default `None`: array or None. The initial barycenter time series to start the optimization process.
- `max_iter`, default `30`: int. The maximum number of Expectation-Maximization iterations.
- `tol`, default `1e-05`: float. The tolerance for early stopping based on cost decrease.
- `weights`, default `None`: array or None. The weights for each time series in `X`. Must be the same length as `X`. If `None`, uniform weights are used.
- `metric_params`, default `None`: dict or None. DTW constraint parameters (e.g., `global_constraint`, `sakoe_chiba_radius`).
- `verbose`, default `False`: boolean. Whether to print cost information at each iteration.
- `n_jobs`, default `None`: int or None. The number of parallel jobs to run.

### Input
- `X` must be formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. Raw lists or 2D arrays must be converted using `tslearn.utils.to_time_series_dataset` before calling this function.
- `weights`, if provided, must be a 1D array of length `n_ts`.

### Output
Returns a tuple `(barycenter, inertia)` where `barycenter` is a 2D `numpy.ndarray` of shape `(barycenter_size, d)` representing the averaged time series, and `inertia` is a `float` representing the associated DTW cost.

### Valid Call Patterns
```python
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging_one_init
from tslearn.utils import to_time_series_dataset

# 1. Format data into the required 3D shape (n_ts, sz, d)
X = to_time_series_dataset([
    [1.0, 2.0, 3.0], 
    [1.0, 2.0, 2.0], 
    [2.0, 2.0, 3.0]
])

# 2. Compute the DBA barycenter and inertia (inferred from signature)
barycenter, inertia = dtw_barycenter_averaging_one_init(X, max_iter=10, tol=1e-4)

assert isinstance(barycenter, np.ndarray)
assert barycenter.shape == (3, 1)
assert isinstance(inertia, float)
print(f"Inertia: {inertia:.4f}")
```

### LLM Instruction Prompt
- When calling `dtw_barycenter_averaging_one_init`, ensure the input `X` is a 3D array of shape `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to enforce this.
- Always unpack the return value into two variables: `barycenter, inertia`.
- Keep `max_iter` small (e.g., 10-30) for fast execution in tests.

### Prompt Snippet
```text
Use `tslearn.barycenters.dtw_barycenter_averaging_one_init` to compute the DTW barycenter of a time-series dataset. Ensure the input is a 3D array `(n_ts, sz, d)` and unpack the returned tuple `(barycenter, inertia)`.
```

### Common Failure Modes
- Passing a 1D or 2D array for `X` instead of the required 3D array `(n_ts, sz, d)`, which causes shape mismatch errors during DTW computation.
- Failing to unpack the return value into two variables, leading to type errors when attempting to use the tuple as a numpy array.
- Providing `weights` that do not match the length of `X` (`n_ts`).

### Fix Code Hint
```python
# Ensure X is 3D
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X)

# Unpack the tuple
barycenter, inertia = dtw_barycenter_averaging_one_init(X_3d, max_iter=10)
```

## API Test: `dtw_barycenter_averaging_petitjean`

### Signature
```python
def dtw_barycenter_averaging_petitjean(X, barycenter_size=None, init_barycenter=None, max_iter=30, tol=1e-05, weights=None, metric_params=None, verbose=False, n_jobs=None)
```
_Source: tslearn/tslearn/barycenters/dba.py:92_

_Source doc:_ DTW Barycenter Averaging (DBA) method. DBA was originally presented in [1]_. This implementation is not the one documented in the API, but is kept in the codebase to check the documented one for non-regression. Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. barycenter_size : int or None (default: None) Size of the barycenter to generate. If None, the size of the barycenter is that of the data provided at fit time or that of the initial barycenter if specified. init_barycenter : array or None (default: None) Initial barycenter to start from for the optimization process. max_iter : int (default: 30) Number of iterations of the Expectation-Maximization optimization procedure. tol : float (default: 1e-5) Tolerance to use for early stopping: if the decrease in cost is lower than this value, the Expectation-Maximization procedure stops. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. metric_params: dict or None (default: None) DTW constraint parameters to be used. See :ref:`tslearn.metrics.dtw_path <fun-tslearn.metrics.dtw_path>` for a list of accepted parameters If None, no constraint is used for DTW computations. verbose : boolean (default: False) Whether to print information about the cost at each iteration or not. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`__ for more details. Returns ------- numpy.array of shape (barycenter_size, d) or (sz, d) if barycenter_size \ is None DBA barycenter of the provided time series dataset. Examples -------- >>> time_series = [[1, 2, 3, 4], [1, 2, 4, 5]] >>> dtw_barycenter_averaging_petitjean(time_series, max_iter=5) array([[1. ], [2. ],

### Goal
Computes the DTW Barycenter Averaging (DBA) of a time-series dataset using the original Petitjean Expectation-Maximization implementation (maintained primarily for non-regression testing).

### Parameters
- `X`: array-like, shape `(n_ts, sz, d)`. The time-series dataset to average.
- `barycenter_size`, default `None`: int or None. The length of the generated barycenter. If `None`, defaults to the length of the input data or the initial barycenter.
- `init_barycenter`, default `None`: array or None. The initial barycenter to start the optimization process from.
- `max_iter`, default `30`: int. The maximum number of iterations for the Expectation-Maximization optimization procedure.
- `tol`, default `1e-05`: float. Tolerance for early stopping; the procedure stops if the cost decrease is lower than this value.
- `weights`, default `None`: array or None. Weights for each time series in `X`. Must be the same size as `len(X)`. If `None`, uniform weights are used.
- `metric_params`, default `None`: dict or None. DTW constraint parameters (e.g., `global_constraint`, `sakoe_chiba_radius`).
- `verbose`, default `False`: boolean. Whether to print cost information at each iteration.
- `n_jobs`, default `None`: int or None. The number of parallel jobs to run. `-1` means using all processors.

### Input
- `X` must be formatted as a 3D array `(n_ts, max_sz, d)` representing the number of time series, the maximum sequence length, and the number of dimensions. Raw lists should be converted using `tslearn.utils.to_time_series_dataset`.
- If `weights` are provided, they must be a 1D array of length `n_ts`.

### Output
Returns `unspecified` — A `numpy.ndarray` of shape `(barycenter_size, d)` (or `(sz, d)` if `barycenter_size` is `None`) representing the computed DBA barycenter.

### Valid Call Patterns
```python
import numpy as np
import tslearn.barycenters

# Generate a small synthetic 3D time-series dataset
rng = np.random.RandomState(0)
time_series = rng.randn(15, 10, 3)

# Compute the DTW barycenter using the Petitjean implementation
dba_bar = tslearn.barycenters.dtw_barycenter_averaging_petitjean(
    time_series,
    max_iter=5
)

print(dba_bar.shape)
```

### LLM Instruction Prompt
- Call `tslearn.barycenters.dtw_barycenter_averaging_petitjean` to compute a DTW barycenter using the legacy Petitjean implementation.
- Ensure the input `X` is strictly a 3D array `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` if starting from lists of variable lengths.
- Keep `max_iter` small (e.g., 5 or 10) in testing environments to prevent long execution times.

### Prompt Snippet
```text
import numpy as np
import tslearn.barycenters
from tslearn.utils import to_time_series_dataset

X = to_time_series_dataset([[1, 2, 3, 4], [1, 2, 4, 5]])
barycenter = tslearn.barycenters.dtw_barycenter_averaging_petitjean(X, max_iter=5)
assert barycenter.shape == (4, 1)
```

### Common Failure Modes
- **ValueError due to 1D/2D input**: Passing a flat list or a 2D array instead of the required 3D `(n_ts, sz, d)` format. Always format data with `to_time_series_dataset` first.
- **ValueError due to mismatched weights**: Providing a `weights` array whose length does not exactly match `len(X)`.
- **Slow execution**: Leaving `max_iter` at its default (30) or higher on large datasets without setting `n_jobs=-1` can cause the EM algorithm to run slowly.

### Fix Code Hint
```python
# FIX: Ensure input is a 3D array before passing to the barycenter function
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
barycenter = tslearn.barycenters.dtw_barycenter_averaging_petitjean(X_3d, max_iter=5)
```

## API Test: `dtw_barycenter_averaging_subgradient`

### Signature
```python
def dtw_barycenter_averaging_subgradient(X, barycenter_size=None, init_barycenter=None, max_iter=30, initial_step_size=0.05, final_step_size=0.005, tol=1e-05, random_state=None, weights=None, metric_params=None, verbose=False)
```
_Source: tslearn/tslearn/barycenters/dba.py:740_

_Source doc:_ DTW Barycenter Averaging (DBA) method estimated through subgradient descent algorithm. DBA was originally presented in [1]_. This implementation is based on a idea from [2]_ (Stochastic Subgradient Mean Algorithm). Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. barycenter_size : int or None (default: None) Size of the barycenter to generate. If None, the size of the barycenter is that of the data provided at fit time or that of the initial barycenter if specified. init_barycenter : array or None (default: None) Initial barycenter to start from for the optimization process. max_iter : int (default: 30) Number of iterations of the Expectation-Maximization optimization procedure. initial_step_size : float (default: 0.05) Initial step size for the subgradient descent algorithm. Default value is the one suggested in [2]_. final_step_size : float (default: 0.005) Final step size for the subgradient descent algorithm. Default value is the one suggested in [2]_. tol : float (default: 1e-5) Tolerance to use for early stopping: if the decrease in cost is lower than this value, the Expectation-Maximization procedure stops. random_state : int, RandomState instance or None, optional (default=None) If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator; If None, the random number generator is the RandomState instance used by `np.random`. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. metric_params: dict or None (default: None) DTW constraint parameters to be used. See :ref:`tslearn.metrics.dtw_path <fun-tslearn.metrics.dtw_path>` for a list of accepted parameters If None, no constraint is used for DTW computations. verbose : boolean (default: False) Whether to print information about the cost at each iteration or not. Returns ------- numpy.array of shape (barycenter_size, d) or (sz, d) if barycenter_size \ is None

### Goal
Computes the Dynamic Time Warping (DTW) Barycenter Averaging (DBA) of a time-series dataset using a stochastic subgradient descent algorithm.

### Parameters
- `X`: array-like, shape=(n_ts, sz, d). The time-series dataset to average.
- `barycenter_size`, default `None`: int or None. The length of the generated barycenter time series. If `None`, defaults to the length of the input data (`sz`) or the `init_barycenter`.
- `init_barycenter`, default `None`: array or None. The initial barycenter time series to start the optimization process from.
- `max_iter`, default `30`: int. The maximum number of iterations for the optimization procedure.
- `initial_step_size`, default `0.05`: float. The initial step size for the subgradient descent algorithm.
- `final_step_size`, default `0.005`: float. The final step size for the subgradient descent algorithm.
- `tol`, default `1e-05`: float. The tolerance for early stopping; optimization stops if the cost decrease is below this value.
- `random_state`, default `None`: int, RandomState instance, or None. Seed or random number generator for reproducible results.
- `weights`, default `None`: array or None. Weights for each time series in `X`. Must be of length `n_ts`. If `None`, uniform weights are used.
- `metric_params`, default `None`: dict or None. DTW constraint parameters (e.g., `{"global_constraint": "sakoe_chiba", "sakoe_chiba_radius": 3}`).
- `verbose`, default `False`: boolean. Whether to print cost information at each iteration.

### Input
`X` must be a 3D array of shape `(n_ts, sz, d)` representing `n_ts` time series, each of maximum length `sz` with `d` dimensions. Raw lists of lists must be converted using `tslearn.utils.to_time_series_dataset` prior to calling this function.

### Output
Returns `numpy.array` — A 2D numpy array of shape `(barycenter_size, d)` (or `(sz, d)` if `barycenter_size` is `None`) representing the computed average time series (barycenter).

### Valid Call Patterns
```python
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging_subgradient

# Note: Example inferred from signature and project context (not verified in test suite)
rng = np.random.RandomState(42)
X = rng.randn(5, 10, 2)  # 5 time series, length 10, 2 dimensions

barycenter = dtw_barycenter_averaging_subgradient(
    X, 
    max_iter=5, 
    random_state=42
)

assert barycenter.shape == (10, 2)
print(barycenter)
```

### LLM Instruction Prompt
- Always ensure the input `X` is strictly a 3D array of shape `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` if the input is a list of variable-length sequences.
- Keep `max_iter` small (e.g., 5 or 10) in generated tests to ensure fast execution.
- If providing `weights`, ensure the length of the weights array exactly matches `len(X)`.

### Prompt Snippet
```text
When computing a DTW barycenter using subgradient descent, use `tslearn.barycenters.dtw_barycenter_averaging_subgradient`. Ensure the input is a 3D array `(n_ts, sz, d)`. You can control the output length with `barycenter_size` and pass DTW constraints via `metric_params`.
```

### Common Failure Modes
- Passing a 1D or 2D array (or a raw list of lists) for `X` instead of the required 3D array format `(n_ts, sz, d)`.
- Providing a `weights` array whose length does not match the number of time series in `X` (`n_ts`).
- Setting `max_iter` too high in testing environments, leading to slow execution times.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.barycenters import dtw_barycenter_averaging_subgradient

# Convert raw lists to the required 3D array format (n_ts, sz, d)
raw_data = [[1, 2, 3], [1, 2, 3, 4]]
X_formatted = to_time_series_dataset(raw_data)

# Compute the barycenter
barycenter = dtw_barycenter_averaging_subgradient(X_formatted, max_iter=5)
```

## API Test: `dtw_limited_warping_length`

### Signature
```python
def dtw_limited_warping_length(s1, s2, max_length, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:922_

_Source doc:_ Compute Dynamic Time Warping (DTW) similarity measure between (possibly multidimensional) time series under an upper bound constraint on the resulting path length and return the similarity cost. DTW is computed as the Euclidean distance between aligned time series, i.e., if :math:`\pi` is the optimal alignment path: .. math:: DTW(X, Y) = \sqrt{\sum_{(i, j) \in \pi} \|X_{i} - Y_{j}\|^2} Note that this formula is still valid for the multivariate case. It is not required that both time series share the same size, but they must be the same dimension. DTW was originally presented in [1]_. This constrained-length variant was introduced in [2]_. Both bariants are discussed in more details in our :ref:`dedicated user-guide page <dtw>` Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. max_length : int Maximum allowed warping path length. If greater than len(s1) + len(s2), then it is equivalent to unconstrained DTW. If lower than max(len(s1), len(s2)), no path can be found and a ValueError is raised. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- float Similarity score Examples -------- >>> float(dtw_limited_warping_length([1, 2, 3], [1., 2., 2., 3.], 5)) 0.0 >>> float(dtw_limited_warping_length([1, 2, 3], [1., 2., 2., 3., 4.], 5)) 1.0 See Also -------- dtw : Get the similarity score for DTW dtw_path_limited_warping_length : Get both the warping path and the similarity score for DTW with limited warping path length References ---------- .. [1] H. Sakoe, S. Chiba, "Dynamic programming algorithm optimization for

### Goal
Compute the Dynamic Time Warping (DTW) similarity score between two time series, constrained by a strict upper bound on the maximum allowed warping path length.

### Parameters
- `s1`: array-like of shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like of shape `(sz2, d)` or `(sz2,)`. The second time series. Must have the same feature dimension `d` as `s1`.
- `max_length`: int. The maximum allowed length for the DTW warping path.
- `be`, default `None`: Backend object, string (`"numpy"` or `"pytorch"`), or `None`. If `None`, the backend is automatically inferred from the input array types.

### Input
The caller must provide two time series (`s1` and `s2`) as lists, NumPy arrays, or PyTorch tensors. They can have different lengths (`sz1` and `sz2`) but must share the same feature dimensionality `d`. The `max_length` parameter must be an integer strictly greater than or equal to `max(len(s1), len(s2))`.

### Output
Returns `unspecified` — A scalar value (a Python `float` if using the NumPy backend, or a 0-dimensional PyTorch tensor if using the PyTorch backend) representing the constrained DTW similarity cost.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

# Two time series of different lengths but same dimension (d=1)
x = np.array([[1.0], [2.0], [3.0]])
y = np.array([[1.0], [2.0], [2.0], [3.0]])

# max_length must be >= max(len(x), len(y)), which is 4
cost = tslearn.metrics.dtw_limited_warping_length(x, y, max_length=5, be="numpy")

assert isinstance(cost, float)
assert cost == 0.0
```

### LLM Instruction Prompt
- When calling `dtw_limited_warping_length`, you MUST ensure that `max_length >= max(len(s1), len(s2))`. If it is smaller, no valid path can be found and the function will raise a `ValueError`.
- Ensure both time series have the same feature dimension `d`.
- If you need to compute gradients, pass PyTorch tensors with `requires_grad=True` and specify `be="pytorch"`.

### Prompt Snippet
```text
Ensure `max_length` is at least `max(len(s1), len(s2))` when calling `tslearn.metrics.dtw_limited_warping_length` to avoid a ValueError. Both time series must have the same feature dimension.
```

### Common Failure Modes
- **ValueError for short max_length**: Raising a `ValueError` because `max_length` is less than `max(len(s1), len(s2))`. A valid DTW path must traverse at least the length of the longest sequence.
- **Dimension Mismatch**: Providing time series with different feature dimensions (e.g., `s1` has shape `(10, 2)` and `s2` has shape `(15, 3)`).
- **Invalid Backend**: Passing an unrecognized string to `be` instead of `"numpy"`, `"pytorch"`, or `None`.

### Fix Code Hint
```python
# Calculate the minimum required path length dynamically to prevent ValueErrors
min_required_length = max(len(s1), len(s2))
safe_max_length = min_required_length + 2  # Add a margin for warping

cost = tslearn.metrics.dtw_limited_warping_length(
    s1, s2, 
    max_length=safe_max_length, 
    be="numpy"
)
```

## API Test: `dtw_path`

### Signature
```python
def dtw_path(s1, s2, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/_dtw.py:166  (+1 more definition site/overload)_

### Goal
Compute the Dynamic Time Warping (DTW) similarity measure between two time series and return both the optimal alignment path and the similarity score.

### Parameters
- `s1`: array-like, shape=(sz1, d) or (sz1,). The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape=(sz2, d) or (sz2,). The second time series. If 1D, it is assumed to be univariate.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. Global constraint to restrict admissible paths for DTW.
- `sakoe_chiba_radius`, default `None`: `int` or `None`. Radius to be used for the Sakoe-Chiba band global constraint. If `None` and `global_constraint` is `"sakoe_chiba"`, a radius of 1 is used.
- `itakura_max_slope`, default `None`: `float` or `None`. Maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint` is `"itakura"`, a maximum slope of 2.0 is used.
- `be`, default `None`: Backend object, string (`"numpy"` or `"pytorch"`), or `None`. If `None`, the backend is automatically inferred from the input arrays.

### Input
Two time-series arrays (NumPy arrays, PyTorch tensors, or standard Python lists). The two time series do not need to share the same length (`sz1` and `sz2` can differ), but they **must** have the exact same number of dimensions `d`.

### Output
Returns `unspecified` — A tuple `(path, similarity_score)` where:
1. `path` is a list of integer pairs `(i, j)` representing the matching alignment path (the first index corresponds to `s1` and the second to `s2`).
2. `similarity_score` is a `float` (or a PyTorch tensor if the PyTorch backend is used) representing the Euclidean distance between the aligned time series.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# Compute DTW path and distance between two univariate time series of different lengths
path, dist = tslearn.metrics.dtw_path(
    [1, 2, 3],
    [1.0, 2.0, 2.0, 3.0],
    be="numpy"
)

assert path == [(0, 0), (1, 1), (1, 2), (2, 3)]
assert np.isclose(dist, 0.0)
```

### LLM Instruction Prompt
- Call `tslearn.metrics.dtw_path(s1, s2)` to get both the alignment path and the distance score. If you only need the distance, use `tslearn.metrics.dtw` instead.
- Ensure both time series have the same feature dimensionality `d`.
- To speed up computation or enforce locality, provide `global_constraint="sakoe_chiba"` and an integer `sakoe_chiba_radius`.
- The function returns a tuple `(path, distance)`. Do not forget to unpack it.
- If passing PyTorch tensors, the PyTorch backend is automatically detected, and the returned distance will be a tensor.

### Prompt Snippet
```text
Use `tslearn.metrics.dtw_path(s1, s2)` to compute the DTW alignment path and distance between two time series. Unpack the result as `path, dist`. The inputs can have different lengths but must have the same number of dimensions. You can restrict the warping path by passing `global_constraint="sakoe_chiba"` and `sakoe_chiba_radius=...`.
```

### Common Failure Modes
- **Empty Arrays**: Passing empty lists or arrays (e.g., `dtw_path([], [])`) raises a `ValueError`.
- **Mismatched Dimensions**: Passing time series with different feature dimensions (e.g., `d=1` for `s1` and `d=2` for `s2`) will cause a failure.
- **Ambiguous Constraints**: If both `sakoe_chiba_radius` and `itakura_max_slope` are provided but `global_constraint` is `None`, a `RuntimeWarning` is raised and no global constraint is applied.
- **Forgetting to Unpack**: Assigning the result to a single variable and treating it as a float distance will cause `TypeError`s in downstream mathematical operations, as the result is a tuple.

### Fix Code Hint
```python
# WRONG: Forgetting to unpack the tuple
dist = tslearn.metrics.dtw_path(s1, s2)
# WRONG: Ambiguous constraints
path, dist = tslearn.metrics.dtw_path(s1, s2, sakoe_chiba_radius=3, itakura_max_slope=2.0)

# CORRECT: Unpack the tuple and explicitly specify the global constraint
path, dist = tslearn.metrics.dtw_path(s1, s2, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
```

## API Test: `dtw_path_from_metric`

### Signature
```python
def dtw_path_from_metric(s1, s2=None, metric='euclidean', global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None, **kwds)
```
_Source: tslearn/tslearn/metrics/_dtw.py:450  (+1 more definition site/overload)_

_Source doc:_ Compute Dynamic Time Warping (DTW) similarity measure between (possibly multidimensional) time series using a distance metric defined by the user and return both the path and the similarity. Similarity is computed as the cumulative cost along the aligned time series. It is not required that both time series share the same size, but they must be the same dimension. DTW was originally presented in [1]_. Valid values for metric are the same as for scikit-learn `pairwise_distances`_ function i.e. a string (e.g. "euclidean", "sqeuclidean", "hamming") or a function that is used to compute the pairwise distances. See `scikit`_ and `scipy`_ documentations for more information about the available metrics. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) if metric!="precomputed", (sz1, sz2) otherwise A time series or an array of pairwise distances between samples. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,), optional (default: None) A second time series, only allowed if metric != "precomputed". If shape is (sz2,), the time series is assumed to be univariate. metric : string or callable (default: "euclidean") Function used to compute the pairwise distances between each points of `s1` and `s2`. If metric is "precomputed", `s1` is assumed to be a distance matrix. If metric is an other string, it must be one of the options compatible with sklearn.metrics.pairwise_distances. Alternatively, if metric is a callable function, it is called on pairs of rows of `s1` and `s2`. The callable should take two 1 dimensional arrays as input and return a value indicating the distance between them. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for DTW. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [1]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used.

### Goal
Compute the Dynamic Time Warping (DTW) similarity measure and the optimal alignment path between two time series using a user-defined distance metric.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)` if `metric != "precomputed"`, or `(sz1, sz2)` otherwise. The first time series, or a precomputed pairwise distance matrix.
- `s2`, default `None`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. Only allowed if `metric != "precomputed"`.
- `metric`, default `'euclidean'`: string or callable. The distance metric to use. Can be `"precomputed"`, a string compatible with `sklearn.metrics.pairwise_distances` (e.g., `"sqeuclidean"`), or a callable taking two 1D arrays and returning a scalar distance.
- `global_constraint`, default `None`: string `{"itakura", "sakoe_chiba"}` or `None`. Global constraint to restrict admissible paths.
- `sakoe_chiba_radius`, default `None`: int or `None`. Radius for the Sakoe-Chiba band constraint.
- `itakura_max_slope`, default `None`: float or `None`. Maximum slope for the Itakura parallelogram constraint.
- `be`, default `None`: Backend identifier (e.g., `"numpy"`, `"pytorch"`) or `None`. If `None`, auto-detected from inputs.
- `**kwds`: Additional keyword arguments passed to the metric function (e.g., for `scipy` or `scikit-learn` distance functions).

### Input
- `s1` and `s2` must be array-like (NumPy arrays or PyTorch tensors).
- If `metric != "precomputed"`, `s1` and `s2` must have the same number of feature dimensions `d` (e.g., both shape `(length, d)`). They can have different lengths (`sz1` and `sz2`).
- If `metric == "precomputed"`, `s1` must be a 2D distance matrix of shape `(sz1, sz2)` and `s2` must be `None`.

### Output
Returns `tuple` — A tuple `(path, similarity)` where `path` is a list of integer index pairs `[(i, j), ...]` representing the optimal alignment between `s1` and `s2`, and `similarity` is the cumulative cost (scalar float or PyTorch tensor) along that path.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])

# Using a built-in string metric
path, dist = tslearn.metrics.dtw_path_from_metric(
    s1, s2, metric="sqeuclidean"
)
assert isinstance(path, list)
assert path[0] == (0, 0)
print(f"Path: {path}, Distance: {dist}")

# Using a custom callable metric
def custom_sqeuclidean(x, y):
    return np.sum((x - y) ** 2)

path_custom, dist_custom = tslearn.metrics.dtw_path_from_metric(
    s1, s2, metric=custom_sqeuclidean
)
assert path == path_custom
```

### LLM Instruction Prompt
- When calling `dtw_path_from_metric`, ensure `s1` and `s2` have the same number of dimensions (e.g., both 2D arrays of shape `(length, dim)`).
- If `metric="precomputed"`, pass the distance matrix as `s1` and leave `s2=None`.
- The function returns a tuple `(path, similarity)`. Do not treat the return value as a single scalar distance.
- If providing a custom callable for `metric`, ensure it accepts two 1D arrays (representing single timesteps) and returns a scalar distance.

### Prompt Snippet
```text
# Compute DTW path and distance using a custom metric
path, dist = tslearn.metrics.dtw_path_from_metric(s1, s2, metric="cityblock")
```

### Common Failure Modes
- Providing `s2` when `metric="precomputed"` (raises an error).
- Providing time series `s1` and `s2` with different feature dimensions `d` (e.g., `s1` is `(10, 2)` and `s2` is `(15, 3)`).
- Providing a custom callable `metric` that expects 2D arrays instead of 1D arrays (the callable is applied to pairs of rows/timesteps, not the entire series at once).
- Forgetting to unpack the tuple return value, leading to type errors when trying to use the result as a scalar distance.

### Fix Code Hint
```python
# If using a custom metric, ensure it operates on 1D arrays (single timesteps)
def custom_dist(x, y):
    return np.sum(np.abs(x - y))

# Unpack the tuple to get both the path and the distance
path, dist = tslearn.metrics.dtw_path_from_metric(s1, s2, metric=custom_dist)
```

## API Test: `dtw_path_limited_warping_length`

### Signature
```python
def dtw_path_limited_warping_length(s1, s2, max_length, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1063_

_Source doc:_ Compute Dynamic Time Warping (DTW) similarity measure between (possibly multidimensional) time series under an upper bound constraint on the resulting path length and return the path as well as the similarity cost. DTW is computed as the Euclidean distance between aligned time series, i.e., if :math:`\pi` is the optimal alignment path: .. math:: DTW(X, Y) = \sqrt{\sum_{(i, j) \in \pi} \|X_{i} - Y_{j}\|^2} Note that this formula is still valid for the multivariate case. It is not required that both time series share the same size, but they must be the same dimension. DTW was originally presented in [1]_. This constrained-length variant was introduced in [2]_. Both variants are discussed in more details in our :ref:`dedicated user-guide page <dtw>` Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. max_length : int Maximum allowed warping path length. If greater than len(s1) + len(s2), then it is equivalent to unconstrained DTW. If lower than max(len(s1), len(s2)), no path can be found and a ValueError is raised. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- list of integer pairs Optimal path float Similarity score Examples -------- >>> path, cost = dtw_path_limited_warping_length([1, 2, 3], ...                                              [1., 2., 2., 3.], 5) >>> float(cost) 0.0 >>> path [(0, 0), (1, 1), (1, 2), (2, 3)] >>> path, cost = dtw_path_limited_warping_length([1, 2, 3], ...                                              [1., 2., 2., 3., 4.], 5) >>> float(cost) 1.0 >>> path

### Goal
Compute the Dynamic Time Warping (DTW) similarity cost and the optimal alignment path between two time series, strictly constrained by a maximum allowed warping path length.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is treated as univariate (`d=1`).
- `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. Must have the same feature dimension `d` as `s1`.
- `max_length`: int. The maximum allowed length for the warping path. Must be at least `max(len(s1), len(s2))`.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`). If `None`, the backend is automatically inferred from the input array types.

### Input
- `s1` and `s2` can be standard Python lists, NumPy arrays, or PyTorch tensors.
- The two time series can have different lengths (`sz1` and `sz2`), but they must share the exact same number of feature dimensions `d`.
- `max_length` must be an integer $\ge \max(\text{len}(s1), \text{len}(s2))$.

### Output
Returns `unspecified` — A tuple `(path, cost)` where `path` is a list of integer pairs `(i, j)` representing the optimal alignment indices, and `cost` is a float representing the Euclidean distance between the aligned time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import dtw_path_limited_warping_length

s1 = np.array([1.0, 2.0, 3.0])
s2 = np.array([1.0, 2.0, 2.0, 3.0])
max_length = 5

path, cost = dtw_path_limited_warping_length(s1, s2, max_length)

assert len(path) <= max_length, "Path length exceeds max_length constraint"
assert cost == 0.0, "Cost should be 0.0 for this exact alignment"
print(f"Path: {path}, Cost: {cost}")
```

### LLM Instruction Prompt
- Always ensure `max_length` is greater than or equal to the maximum length of the two input time series. If it is smaller, the function will raise a `ValueError`.
- Remember that this function returns a tuple of `(path, cost)`. Do not confuse it with `dtw_limited_warping_length`, which only returns the scalar cost.
- Ensure both time series have the same feature dimensionality `d`.

### Prompt Snippet
```text
When using `dtw_path_limited_warping_length` to find constrained alignments, ensure `max_length >= max(len(s1), len(s2))`. The function returns a tuple `(path, cost)`.
```

### Common Failure Modes
- **`ValueError`**: Raised if `max_length < max(len(s1), len(s2))`, because no valid path can physically be constructed that traverses both sequences entirely within that length limit.
- **Dimensionality Mismatch**: Raised if `s1` and `s2` have different feature dimensions (e.g., `s1` has shape `(10, 2)` and `s2` has shape `(15, 3)`).

### Fix Code Hint
```python
# Ensure max_length is physically possible for the given sequences
min_required_length = max(len(s1), len(s2))
max_len = max(min_required_length + 2, desired_max_length)

path, cost = dtw_path_limited_warping_length(s1, s2, max_length=max_len)
```

## API Test: `dtw_subsequence_path`

### Signature
```python
def dtw_subsequence_path(subseq, longseq, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1417_

_Source doc:_ Compute sub-sequence Dynamic Time Warping (DTW) similarity measure between a (possibly multidimensional) query and a long time series and return both the path and the similarity. DTW is computed as the Euclidean distance between aligned time series, i.e., if :math:`\pi` is the alignment path: .. math:: DTW(X, Y) = \sqrt{\sum_{(i, j) \in \pi} \|X_{i} - Y_{j}\|^2} Compared to traditional DTW, here, border constraints on admissible paths :math:`\pi` are relaxed such that :math:`\pi_0 = (0, ?)` and :math:`\pi_L = (N-1, ?)` where :math:`L` is the length of the considered path and :math:`N` is the length of the subsequence time series. It is not required that both time series share the same size, but they must be the same dimension. This implementation finds the best matching starting and ending positions for `subseq` inside `longseq`. Parameters ---------- subseq : array-like, shape=(sz1, d) or (sz1,) A query time series. If shape is (sz1,), the time series is assumed to be univariate. longseq : array-like, shape=(sz2, d) or (sz2,) A reference (supposed to be longer than `subseq`) time series. If shape is (sz2,), the time series is assumed to be univariate. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- list of integer pairs Matching path represented as a list of index pairs. In each pair, the first index corresponds to `subseq` and the second one corresponds to `longseq`. float Similarity score Examples -------- >>> path, dist = dtw_subsequence_path([2., 3.], [1., 2., 2., 3., 4.]) >>> path [(0, 2), (1, 3)] >>> float(dist) 0.0 See Also -------- dtw : Get the similarity score for DTW subsequence_cost_matrix: Calculate the required cost matrix subsequence_path: Calculate a matching path manually

### Goal
Compute the sub-sequence Dynamic Time Warping (DTW) similarity measure and alignment path to locate the best matching position of a short query time series within a longer reference time series.

### Parameters
- `subseq`: array-like of shape `(sz1, d)` or `(sz1,)`. The query time series to search for. If 1D, it is assumed to be univariate.
- `longseq`: array-like of shape `(sz2, d)` or `(sz2,)`. The reference time series, which is expected to be longer than `subseq`.
- `be`, default `None`: Backend identifier (string `"numpy"` or `"pytorch"`) or a backend instance. If `None`, the backend is automatically determined from the input array types.

### Input
Two time series provided as lists, NumPy arrays, or PyTorch tensors. They do not need to share the same length (`sz1` vs `sz2`), but they *must* have the exact same feature dimension `d`.

### Output
Returns a tuple `(path, dist)` where `path` is a list of integer pairs `(i, j)` representing the alignment path (index `i` in `subseq` matches index `j` in `longseq`), and `dist` is a float representing the DTW similarity score (Euclidean distance of the aligned sub-sequence).

### Valid Call Patterns
```python
import tslearn.metrics

# Basic usage with lists
path, dist = tslearn.metrics.dtw_subsequence_path([2.0, 3.0], [1.0, 2.0, 2.0, 3.0, 4.0])

# Usage with explicit backend
path, dist = tslearn.metrics.dtw_subsequence_path(
    [1.0, 4.0], 
    [1.0, 2.0, 2.0, 3.0, 4.0], 
    be="numpy"
)
```

### LLM Instruction Prompt
- Use `tslearn.metrics.dtw_subsequence_path` when you need to find a short pattern within a longer time series (relaxed border constraints), rather than globally aligning two sequences.
- Always unpack the return value into two variables: `path, dist`. Do not treat the return value as a single scalar distance.
- Ensure both `subseq` and `longseq` have the same number of feature dimensions `d`.

### Prompt Snippet
```python
import tslearn.metrics
import numpy as np

# Query sequence (length 2) and long reference sequence (length 5)
subseq = np.array([2.0, 3.0])
longseq = np.array([1.0, 2.0, 2.0, 3.0, 4.0])

# Compute subsequence path and distance
path, dist = tslearn.metrics.dtw_subsequence_path(subseq, longseq)

# The query [2.0, 3.0] perfectly matches the slice at indices 2 and 3 in longseq
assert path == [(0, 2), (1, 3)], f"Unexpected path: {path}"
assert np.isclose(dist, 0.0), f"Unexpected distance: {dist}"

print(f"Matched path: {path}")
print(f"Distance: {dist}")
```

### Common Failure Modes
- **Unpacking Error**: Expecting a single float return value (like standard `dtw` returns) and failing to unpack the `(path, dist)` tuple.
- **Dimension Mismatch**: Providing a `subseq` and `longseq` with different feature dimensions (e.g., `subseq` is univariate `d=1` but `longseq` is multivariate `d=3`).
- **Argument Order**: Passing the long sequence as the first argument and the short query as the second argument, which violates the expected `(subseq, longseq)` signature and semantics.

### Fix Code Hint
```python
# FIX: Ensure correct argument order (short, long) and unpack the tuple
path, dist = tslearn.metrics.dtw_subsequence_path(short_query, long_reference)
```

## API Test: `dual_coef_`

### Signature
```python
def dual_coef_(self)
```
_Source: tslearn/tslearn/svm/svm.py:29_

### Goal
Retrieve the dual coefficients of the support vectors in a fitted time-series Support Vector Machine (SVM) model.

### Parameters
- `self`: A fitted `tslearn.svm.TimeSeriesSVC` or `tslearn.svm.TimeSeriesSVR` estimator instance.

### Input
The estimator must first be fitted using `.fit(X, y)`, where `X` is a strictly formatted 3D `numpy` array of shape `(n_ts, max_sz, d)` representing the time-series dataset, and `y` contains the target labels or values.

### Output
Returns `unspecified` — typically a NumPy array containing the dual coefficients of the support vectors in the decision function, delegated from the underlying `scikit-learn` SVM implementation.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC

# 1. Prepare a 3D time-series dataset (n_ts, max_sz, d)
X = np.array([
    [[1.0], [2.0], [3.0]], 
    [[1.0], [2.0], [4.0]], 
    [[3.0], [4.0], [5.0]]
])
y = np.array([0, 0, 1])

# 2. Initialize and fit the time-series SVM
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)

# 3. Access the dual coefficients (inferred from signature and scikit-learn conventions)
coefs = clf.dual_coef_
assert coefs is not None
assert isinstance(coefs, np.ndarray)
print(f"Dual coefficients shape: {coefs.shape}")
```

### LLM Instruction Prompt
- When accessing `dual_coef_`, ensure the `TimeSeriesSVC` or `TimeSeriesSVR` model has already been fitted using `.fit(X, y)` where `X` is a 3D array of shape `(n_ts, max_sz, d)`.
- Treat `dual_coef_` as a property (do not call it as a function with parentheses), adhering to `scikit-learn` conventions for attributes learned during fitting.

### Prompt Snippet
```text
Ensure the time-series SVM model is fitted on a 3D array `(n_ts, max_sz, d)` before accessing the `dual_coef_` property. Do not call it as a function.
```

### Common Failure Modes
- **NotFittedError / AttributeError:** Accessing `dual_coef_` before calling `.fit()` results in an error because the underlying support vectors and coefficients have not yet been computed.
- **Dimensionality Error during Fit:** Passing unformatted 1D or 2D data to `.fit()` will cause the training step to fail before `dual_coef_` can ever be accessed. Data must be converted using `to_time_series_dataset`.
- **Calling as a Method:** Attempting to execute `clf.dual_coef_()` will raise a `TypeError` because it evaluates to a NumPy array, not a callable function.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset

# Ensure data is 3D and model is fitted before accessing dual_coef_
X_3d = to_time_series_dataset(X_raw)
clf.fit(X_3d, y)

# Access as a property, not a method
coefs = clf.dual_coef_
```

## API Test: `early_classification_cost`

### Signature
```python
def early_classification_cost(self, X, y)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:517_

_Source doc:_ Compute early classification score. The score is computed as: .. math:: 1 - acc + \alpha \frac{1}{n} \sum_i t_i where :math:`\alpha` is the trade-off parameter (`self.cost_time_parameter`) and :math:`t_i` are prediction timestamps. Parameters ---------- X : array-like of shape (n_series, n_timestamps, n_features) Vector to be scored, where `n_series` is the number of time series, `n_timestamps` is the number of timestamps in the series and `n_features` is the number of features recorded at each timestamp. y : array-like, shape = (n_samples) or (n_samples, n_outputs) True labels for X. Returns ------- float Early classification cost (a positive number, the lower the better) Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=1000., ...                                  cost_time_parameter=.1, ...                                  random_state=0) >>> model.fit(dataset, y)  # doctest: +ELLIPSIS NonMyopicEarlyClassifier(...) >>> preds, pred_times = model.predict_class_and_earliness(dataset) >>> preds array([0, 0, 0, 1, 1, 1, 0, 0]) >>> pred_times array([4, 4, 4, 4, 4, 4, 1, 1]) >>> float(model.early_classification_cost(dataset, y)) 0.325

### Goal
Compute the early classification cost for a fitted early classifier, which balances prediction accuracy against the time (number of timestamps) taken to make the prediction.

### Parameters
- `self`: A fitted early classifier instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: The time-series dataset to be scored, formatted as a 3D array of shape `(n_series, n_timestamps, n_features)`.
- `y`: The true ground-truth labels for `X`, formatted as a 1D array of shape `(n_samples,)` or a 2D array of shape `(n_samples, n_outputs)`.

### Input
`X` must be a strictly formatted 3D `numpy` array `(n_ts, max_sz, d)`. Raw lists of time series must be converted using `tslearn.utils.to_time_series_dataset` prior to calling this method. The estimator `self` must already be fitted on training data. The number of samples in `X` must exactly match the number of labels in `y`.

### Output
Returns `unspecified` — A `float` representing the early classification cost. It is a positive number where a lower value indicates a better trade-off between accuracy and earliness.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

# 1. Prepare the 3D time-series dataset and labels
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1]
])
y = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1),
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(dataset, y)

# 3. Compute the early classification cost
cost = model.early_classification_cost(dataset, y)

assert isinstance(cost, float)
assert cost >= 0.0
print(f"Early classification cost: {cost}")
```

### LLM Instruction Prompt
- Always ensure `X` is converted to the strict 3D array format `(n_series, n_timestamps, n_features)` using `tslearn.utils.to_time_series_dataset` before passing it to `early_classification_cost`.
- Ensure the early classifier model has been fitted using `.fit(X_train, y_train)` before attempting to compute the cost.
- Call this method as an instance method on a fitted early classifier object (e.g., `model.early_classification_cost(X, y)`).

### Prompt Snippet
```text
Use `tslearn.utils.to_time_series_dataset` to format the test data into a 3D array. Then, call `model.early_classification_cost(X_test, y_test)` on the fitted `NonMyopicEarlyClassifier` to evaluate the trade-off between accuracy and prediction delay.
```

### Common Failure Modes
- **`ValueError: Expected 3D array`**: Occurs if `X` is passed as a 2D array or a raw list of lists. It must be converted to a 3D array first.
- **`NotFittedError`**: Occurs if `early_classification_cost` is called before the model has been fitted with `.fit()`.
- **Dimension Mismatch**: Occurs if the length of `y` does not match the number of time series (`n_series`) in `X`.

### Fix Code Hint
```python
# FIX: Convert raw lists to the required 3D array format and ensure the model is fitted
from tslearn.utils import to_time_series_dataset

X_3d = to_time_series_dataset(X_raw)
model.fit(X_train_3d, y_train)
cost = model.early_classification_cost(X_3d, y)
```

## API Test: `early_predict`

### Signature
```python
def early_predict(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:574_

_Source doc:_ Provides predicted classes as well as estimated delays before prediction timestamps for a dataset of incomplete time series. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- X : array-like of shape (n_series, t, n_features) A dataset of incomplete time series observed up to time t Returns ------- array-like, shape (n_series,) Predicted classes. array-like, shape (n_series,) Estimated delays before prediction timestamps.

### Goal
Predicts class labels and estimates the delay before a reliable prediction can be made for a dataset of incomplete time series.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: A 3D array-like of shape `(n_series, t, n_features)` representing a dataset of incomplete time series observed up to time `t`.

### Input
- `X` must be formatted as a strict 3D array `(n_series, t, n_features)` using `tslearn.utils.to_time_series_dataset`.
- The estimator must be fitted prior to calling this method.
- `t` represents the number of observed timestamps. If `t` is less than the estimator's configured `min_t` (minimum timestamps required), the method will return `np.nan` for all predictions and delays.

### Output
Returns `unspecified` — A tuple of two 1D numpy arrays `(predictions, delays)`, both of shape `(n_series,)`. `predictions` contains the predicted class labels, and `delays` contains the estimated number of additional timestamps needed before a reliable prediction can be made.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

# 1. Prepare full training data
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [3, 2, 1, 1, 2, 3],
    [3, 2, 1, 1, 2, 3]
])
y = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1),
    min_t=2,
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(dataset, y)

# 3. Predict using an incomplete time series (only the first 3 timestamps)
X_incomplete = dataset[:, :3]
pred, delays = model.early_predict(X_incomplete)

assert pred.shape == (4,)
assert delays.shape == (4,)
print("Predictions:", pred)
print("Delays:", delays)
```

### LLM Instruction Prompt
- Call `early_predict(X)` on a fitted early classification model to obtain both class predictions and estimated delays.
- Always unpack the return value into two variables: `predictions, delays = model.early_predict(X)`.
- Ensure `X` is a 3D array of shape `(n_series, t, n_features)`.
- Handle cases where `t < min_t` by checking for `np.nan` in the returned arrays.

### Prompt Snippet
```text
predictions, delays = model.early_predict(X_incomplete)
```

### Common Failure Modes
- **ValueError**: Passing a 1D or 2D array instead of the required 3D `(n_series, t, n_features)` format.
- **NotFittedError**: Calling `early_predict` before calling `fit()` on the model.
- **Tuple Unpacking Error**: Forgetting that `early_predict` returns a tuple of two arrays and trying to assign it to a single variable that is later used as a numeric array.
- **Unexpected `np.nan` values**: Passing an incomplete time series where the observed length `t` is strictly less than the model's `min_t` parameter, resulting in `np.nan` predictions and delays.

### Fix Code Hint
```python
# Ensure X is a 3D array and unpack the returned tuple
X_incomplete = to_time_series_dataset(raw_data)
predictions, delays = model.early_predict(X_incomplete)

# Handle potential nan values if t < min_t
valid_mask = ~np.isnan(predictions)
valid_predictions = predictions[valid_mask]
```

## API Test: `early_predict_proba`

### Signature
```python
def early_predict_proba(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:600_

_Source doc:_ Provides probability estimates as well as estimated delays before prediction timestamps for a dataset of incomplete time series. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- X : array-like of shape (n_series, t, n_features) A dataset of incomplete time series observed up to time t Returns ------- array-like, shape (n_series, n_classes) Probabilities for each class in the model, where classes are ordered as they are in ``self.classes_``. array-like of shape (n_series,) Estimated delays before prediction timestamps.

### Goal
Computes class probability estimates and estimated delays before prediction timestamps for a dataset of incomplete time series using a fitted early classification estimator.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: An array-like dataset of incomplete time series observed up to time `t`, with shape `(n_series, t, n_features)`.

### Input
`X` must be a 3D array formatted via `tslearn.utils.to_time_series_dataset` representing incomplete time series (where the time dimension `t` is typically smaller than the full series length seen during training). The estimator (`self`) must be fitted first. If `t` is smaller than the estimator's configured `min_t`, the method will return `NaN` values.

### Output
Returns `unspecified` — A tuple of two array-likes: `(probabilities, delays)`. `probabilities` has shape `(n_series, n_classes)` containing the class probabilities ordered by `self.classes_`. `delays` has shape `(n_series,)` containing the estimated delays before prediction timestamps.

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
import numpy as np

# 1. Prepare full-length training data
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1]
])
y = [0, 0, 1, 1]

# 2. Initialize and fit the early classifier
model = NonMyopicEarlyClassifier(
    n_clusters=2,
    base_classifier=KNeighborsTimeSeriesClassifier(n_neighbors=1, metric="euclidean"),
    min_t=2,
    lamb=1000.0,
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(dataset, y)

# 3. Predict probabilities on incomplete time series (e.g., first 3 timestamps)
incomplete_X = dataset[:, :3]
probas, delays = model.early_predict_proba(incomplete_X)

# 4. Verify outputs
assert probas.shape == (4, 2), "Expected probabilities shape (n_series, n_classes)"
assert delays.shape == (4,), "Expected delays shape (n_series,)"
print(f"Probabilities:\n{probas}\nDelays:\n{delays}")
```

### LLM Instruction Prompt
- When calling `early_predict_proba`, ensure the input `X` is strictly a 3D array `(n_series, t, n_features)` representing incomplete time series.
- Always unpack the return value into two variables (e.g., `probas, delays = model.early_predict_proba(X)`), as it returns both the probability estimates and the estimated delays.
- Ensure the time dimension `t` of the input `X` is at least the `min_t` parameter of the fitted model; otherwise, the returned arrays will contain `NaN` values.

### Prompt Snippet
```text
Use the fitted `NonMyopicEarlyClassifier` to predict probabilities and delays for the incomplete time series `X_incomplete`. Unpack the results into `probas` and `delays`.
```

### Common Failure Modes
- **Not unpacking the return value:** Assigning the result to a single variable and attempting to use it as a probability matrix, which fails because the method returns a tuple `(probabilities, delays)`.
- **Passing 2D arrays:** Providing a 2D array `(n_series, t)` instead of the required 3D array `(n_series, t, n_features)`, leading to shape mismatch errors.
- **Calling before `fit`:** Attempting to call `early_predict_proba` on an unfitted estimator, raising a `NotFittedError`.
- **Providing too few timestamps:** Passing an `X` where the time dimension `t` is less than the model's `min_t`, resulting in arrays filled with `np.nan` instead of valid probabilities and delays.

### Fix Code Hint
```python
# FIX: Ensure X is 3D and unpack the tuple return value
X_incomplete_3d = to_time_series_dataset(X_incomplete)
probas, delays = model.early_predict_proba(X_incomplete_3d)

# Check for NaNs if the series is too short
if np.isnan(probas).any():
    print("Warning: Input time series length is shorter than the model's min_t.")
```

## API Test: `euclidean_barycenter`

### Signature
```python
def euclidean_barycenter(X, weights=None)
```
_Source: tslearn/tslearn/barycenters/euclidean.py:9_

_Source doc:_ Standard Euclidean barycenter computed from a set of time series. Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. Returns ------- numpy.array of shape (sz, d) Barycenter of the provided time series dataset. Notes ----- This method requires a dataset of equal-sized time series Examples -------- >>> time_series = [[1, 2, 3, 4], [1, 2, 4, 5]] >>> bar = euclidean_barycenter(time_series) >>> bar.shape (4, 1) >>> bar array([[1. ], [2. ], [3.5], [4.5]])

### Goal
Computes the standard Euclidean barycenter (the weighted or unweighted mean) from a set of equal-sized time series.

### Parameters
- `X`: Time series dataset, provided as an array-like object of shape `(n_ts, sz, d)`.
- `weights`, default `None`: Weights for each time series `X[i]`. Must be an array of the same size as `len(X)`. If `None`, uniform weights are used.

### Input
A dataset of strictly equal-sized time series formatted as a 3D array `(n_ts, sz, d)`, where `n_ts` is the number of time series, `sz` is the number of time steps, and `d` is the number of dimensions. Variable-length time series (padded with `nan`) are not supported by this specific method.

### Output
Returns `unspecified` — A 2D `numpy.array` of shape `(sz, d)` representing the Euclidean barycenter of the provided time series dataset.

### Valid Call Patterns
```python
import numpy as np
import tslearn.barycenters

n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
time_series = rng.randn(n, sz, d)

# Unweighted Euclidean barycenter
bar = tslearn.barycenters.euclidean_barycenter(time_series)
np.testing.assert_allclose(bar, time_series.mean(axis=0))

# Weighted Euclidean barycenter
weights = rng.rand(n, )
weights /= np.sum(weights)
bar_weighted = tslearn.barycenters.euclidean_barycenter(time_series, weights=weights)
np.testing.assert_allclose(bar_weighted, np.average(time_series, axis=0, weights=weights))
```

### LLM Instruction Prompt
- Call `tslearn.barycenters.euclidean_barycenter(X, weights=None)` to compute the Euclidean mean of a time series dataset.
- Ensure `X` is formatted as a 3D array of shape `(n_ts, sz, d)`.
- Do not use this function for variable-length time series; it strictly requires a dataset of equal-sized time series.
- If `weights` is provided, it must be a 1D array of length `n_ts`.

### Prompt Snippet
```text
Use `tslearn.barycenters.euclidean_barycenter(X, weights=None)` to compute the Euclidean barycenter. `X` must be a 3D array `(n_ts, sz, d)` of equal-sized time series. `weights` must be length `n_ts` if provided.
```

### Common Failure Modes
- Passing variable-length time series (e.g., padded with `nan`), which violates the equal-sized requirement of this method.
- Passing a 1D or 2D array instead of the strictly required 3D `(n_ts, sz, d)` array format.
- Providing a `weights` array whose length does not match the number of time series `n_ts`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
import tslearn.barycenters

# Ensure data is in the required 3D format (n_ts, sz, d)
X_3d = to_time_series_dataset(X_raw)

# X_3d must contain equal-sized time series (no nan padding)
bar = tslearn.barycenters.euclidean_barycenter(X_3d)
```

## API Test: `extract_from_zip_url`

### Signature
```python
def extract_from_zip_url(url, target_dir=None, verbose=False)
```
_Source: tslearn/tslearn/datasets/datasets.py:16_

_Source doc:_ Download a zip file from its URL and unzip it. A `RuntimeWarning` is printed on failure. Parameters ---------- url : string URL from which to download. target_dir : str or None (default: None) Directory to be used to extract unzipped downloaded files. verbose : bool (default: False) Whether to print information about the process (cached files used, ...) Returns ------- str or None Directory in which the zip file has been extracted if the process was successful, None otherwise

### Goal
Download a zip file from a specified URL and extract its contents into a target directory.

### Parameters
- `url`: A string representing the URL from which to download the zip archive.
- `target_dir`, default `None`: A string representing the directory path where the unzipped files should be extracted, or `None` to use a default location.
- `verbose`, default `False`: A boolean indicating whether to print information about the download and extraction process (e.g., cached files used).

### Input
A valid URL string pointing to a downloadable zip file. If `target_dir` is provided, the executing environment must have write permissions to that path.

### Output
Returns `unspecified` — A string representing the directory path where the zip file was extracted if the process was successful, or `None` if the download or extraction failed.

### Valid Call Patterns
```python
import warnings
from tslearn.datasets import extract_from_zip_url

# Inferred from signature (not verified by existing tests)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    # Using an invalid URL to avoid network access and demonstrate the failure mode
    out_dir = extract_from_zip_url(
        url="http://0.0.0.0/nonexistent_dataset.zip", 
        target_dir=None, 
        verbose=False
    )

assert out_dir is None, f"Expected None on failure, got {out_dir}"
assert any(issubclass(warn.category, RuntimeWarning) for warn in w), "Expected a RuntimeWarning"
print("extract_from_zip_url correctly returned None on failure.")
```

### LLM Instruction Prompt
- When calling `extract_from_zip_url`, always check if the return value is `None` before attempting to access the extracted files, as the function catches exceptions and returns `None` on failure.
- Do not use this function in environments without network access unless you are intentionally testing the failure mode.

### Prompt Snippet
```text
`tslearn.datasets.extract_from_zip_url(url, target_dir=None, verbose=False)` downloads and extracts a zip file. It returns the extraction directory path as a string on success, or `None` on failure (emitting a `RuntimeWarning`).
```

### Common Failure Modes
- Providing an unreachable or invalid URL, which causes the function to emit a `RuntimeWarning` and return `None` instead of raising an exception.
- Providing a `target_dir` where the user lacks write permissions, which will also result in a failure and a return value of `None`.

### Fix Code Hint
```python
out_dir = extract_from_zip_url("http://example.com/data.zip")
if out_dir is None:
    raise RuntimeError("Failed to download or extract the dataset.")
# Proceed to load data from out_dir
```

## API Test: `fit`

### Signature
```python
def fit(self, X, y=None)
def fit(self, X, y=None, sample_weight=None)
def fit(self, X, y)
def fit(self, X, y, sample_weight=None)
def fit(self, X, y=None, **kwargs)
```
_Source: tslearn/tslearn/clustering/kmeans.py:321  (+23 more definition site/overload)_

_Source doc:_ Compute kernel k-means clustering. Parameters ---------- X : array-like of shape=(n_ts, sz, d) Time series dataset. y Ignored sample_weight : array-like of shape=(n_ts, ) or None (default: None) Weights to be given to time series in the learning process. By default, all time series weights are equal.

### Goal
Train a time-series machine learning estimator (such as clustering, classification, or regression) on a formatted 3D time-series dataset.

### Parameters
- `self`: The instantiated `tslearn` estimator object (e.g., `KernelKMeans`, `TimeSeriesKMeans`, `KNeighborsTimeSeriesClassifier`).
- `X`: array-like of shape `(n_ts, sz, d)`. The training time-series dataset.
- `y`, default `None`: array-like of shape `(n_ts, )` or `None`. Target values (class labels or regression targets) for supervised learning. Ignored for unsupervised estimators like kernel k-means.
- `sample_weight`, default `None`: array-like of shape `(n_ts, )` or `None`. Weights to be given to individual time series in the learning process. By default, all time series weights are equal.

### Input
- `X` must be strictly formatted as a 3D array of shape `(n_ts, max_sz, d)`.
- If the original data consists of raw lists or variable-length sequences, it must first be converted and padded with `nan` values using `tslearn.utils.to_time_series_dataset`.
- `y` must match the number of time series `n_ts` if provided for supervised tasks.

### Output
Returns `unspecified` — The fitted estimator instance (e.g., `self`), which is populated with learned attributes (such as `labels_` or `cluster_centers_`) and is ready to execute `.predict()` or `.fit_predict()`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import KernelKMeans
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
from tslearn.utils import to_time_series_dataset

# 1. Unsupervised learning (Clustering)
rng = np.random.RandomState(0)
time_series = rng.randn(15, 10, 3) # (n_ts, max_sz, d)
gak_km = KernelKMeans(n_clusters=3, max_iter=5, random_state=0)
gak_km.fit(time_series)

assert hasattr(gak_km, "labels_"), "Estimator should have labels_ after fitting"
print("Cluster labels:", gak_km.labels_)

# 2. Supervised learning (Classification)
X_raw = [[1, 3, 4, 2], [1, 2, 4, 2], [1, 2, 4, 2, 2]]
X = to_time_series_dataset(X_raw)
y = [0, 1, 1]
knn = KNeighborsTimeSeriesClassifier(n_neighbors=1)
knn.fit(X, y)

predictions = knn.predict(X)
assert len(predictions) == 3, "Should predict one label per time series"
print("Predictions:", predictions)
```

### LLM Instruction Prompt
- Always ensure the input `X` is a 3D array of shape `(n_ts, max_sz, d)` before calling `fit`.
- If the input data consists of raw lists or variable-length sequences, preprocess it using `tslearn.utils.to_time_series_dataset` first.
- For supervised estimators, provide the target array `y`. For unsupervised estimators (like `KernelKMeans`), `y` can be omitted or set to `None`.

### Prompt Snippet
```text
When calling `fit` on a tslearn estimator, the input `X` MUST be a 3D array of shape `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to convert raw lists or variable-length sequences into this padded 3D format before fitting.
```

### Common Failure Modes
- **ValueError due to 2D input:** Passing a standard 2D scikit-learn array `(n_samples, n_features)` instead of the required 3D `tslearn` array `(n_ts, max_sz, d)`.
- **Inconsistent lengths:** Passing a raw list of variable-length lists directly to `fit` without converting and padding them via `to_time_series_dataset`.
- **RuntimeError in metric computation:** Providing invalid hyper-parameters during estimator initialization (e.g., `sigma=0` for `KernelKMeans`) which causes the underlying distance/kernel metric to fail during `fit`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset

# WRONG: estimator.fit(X_raw_lists, y)
# RIGHT: Convert to 3D array (n_ts, max_sz, d) first
X_formatted = to_time_series_dataset(X_raw_lists)
estimator.fit(X_formatted, y)
```

## API Test: `fit_predict`

### Signature
```python
def fit_predict(self, X, y=None)
def fit_predict(self, X, y=None, n=1)
```
_Source: tslearn/tslearn/forecasting/_arima.py:431  (+5 more definition site/overload)_

_Source doc:_ Computes VARIMA model and forecasts n timestamps for the given data. Parameters ---------- X: array-like, shape (n_ts, sz, d) Time-series dataset. y : Ignored n : int (default: 1) The number of timestamps to forecast, a.k.a. the horizon. Returns ------- array, shape = (n_ts, n, d) Array of forecasted timestamps

### Goal
Fits a time-series estimator to the provided dataset and returns the predictions or forecasts (e.g., computing a VARIMA model and forecasting `n` future timestamps).

### Parameters
- `self`: The instantiated estimator object (e.g., `VARIMA(...)` or a clustering model like `TimeSeriesKMeans(...)`).
- `X`: The input time-series dataset, formatted as a 3D array of shape `(n_ts, sz, d)`.
- `y`, default `None`: Target values (ignored, present for scikit-learn API compatibility).
- `n`, default `1`: The number of timestamps to forecast (the horizon). Only applicable to forecasting models like `VARIMA`.

### Input
- `X` must be a 3D numpy array of shape `(n_ts, max_sz, d)`. Variable-length time series must be padded with `nan` values.
- `n` must be an integer representing the forecast horizon.

### Output
Returns `unspecified` — An array of predictions. For forecasting models, this is a 3D array of shape `(n_ts, n, d)` containing the forecasted timestamps. For clustering models, this is typically a 1D array of cluster labels.

### Valid Call Patterns
```python
import numpy as np
from tslearn.forecasting import VARIMA
from tslearn.generators import random_walks

# Generate synthetic 3D time-series data: (n_ts, sz, d)
horizon = 2
data = random_walks(n_ts=5, sz=15, d=3, std=0)

# Introduce variable length by padding with nan
data[2, 12:, :] = np.nan

# Fit the VARIMA model and predict the next 2 timestamps
predicted = VARIMA(2, 1, 2, with_constant=False).fit_predict(data, n=horizon)

assert predicted.shape == (data.shape[0], horizon, data.shape[-1])
print("Forecast shape:", predicted.shape)
```

### LLM Instruction Prompt
- Always ensure the input dataset `X` is strictly formatted as a 3D array `(n_ts, max_sz, d)`.
- When calling `fit_predict` on a forecasting model like `VARIMA`, provide the forecast horizon using the `n` parameter.
- Do not pass a target variable to `y` as it is ignored.

### Prompt Snippet
```text
Ensure time-series data is formatted as a 3D array `(n_ts, max_sz, d)` before calling `fit_predict`. For forecasting models like `VARIMA`, specify the forecast horizon using the `n` parameter.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D array `(n_ts, max_sz, d)`.
- Failing to pad variable-length time series with `nan` values before passing them to `fit_predict`.
- Providing a dataset where the time series length is smaller than the minimum size required by the model (e.g., raising a `ValueError` for `min_size` in VARIMA).

### Fix Code Hint
```python
# Convert 2D data to 3D format before calling fit_predict
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_2d)
predicted = model.fit_predict(X_3d, n=horizon)
```

## API Test: `fit_transform`

### Signature
```python
def fit_transform(self, X, y=None, **fit_params)
def fit_transform(self, X, y=None, **transform_params)
def fit_transform(self, X, y=None, **kwargs)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:178  (+8 more definition site/overload)_

_Source doc:_ Fit a PAA representation and transform the data accordingly. Parameters ---------- X : array-like of shape (n_ts, sz, d) Time series dataset Returns ------- numpy.ndarray of shape (n_ts, n_segments, d) PAA-Transformed dataset

### Goal
Fit a time-series transformer to the data and return the transformed representation (e.g., scaled, piecewise-aggregated, or matrix profile) in a single step.

### Parameters
- `self`: The instantiated transformer object (e.g., `TimeSeriesScalerMinMax`, `MatrixProfile`, `PAA`).
- `X`: The time-series dataset to fit and transform, expected as a 3D array-like of shape `(n_ts, sz, d)`.
- `y`, default `None`: Target values (optional, usually ignored for unsupervised transformers).
- `**fit_params`: Additional keyword arguments passed to the underlying `fit` method.

### Input
`X` must be a 3D array of shape `(n_ts, sz, d)` (number of time series, maximum sequence length, number of dimensions). Raw lists of variable-length time series must be converted and padded using `tslearn.utils.to_time_series_dataset` before calling this method.

### Output
Returns `unspecified` — A 3D `numpy.ndarray` representing the transformed dataset. The exact shape depends on the transformer used (e.g., `(n_ts, sz, d)` for scalers, `(n_ts, n_segments, d)` for PAA, `(n_ts, output_size, 1)` for Matrix Profile).

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax
from tslearn.matrix_profile import MatrixProfile

# Example 1: Scaling
X = np.arange(30, dtype=float).reshape(2, 5, 3)
X_scaled = TimeSeriesScalerMinMax().fit_transform(X)
assert X_scaled.shape == (2, 5, 3)
print(f"Scaled shape: {X_scaled.shape}")

# Example 2: Matrix Profile
X_mp = np.arange(20, dtype=float).reshape(1, 20, 1)
mp = MatrixProfile(subsequence_length=10)
X_tr = mp.fit_transform(X_mp)
assert X_tr.shape == (1, 11, 1)
print(f"Matrix Profile shape: {X_tr.shape}")
```

### LLM Instruction Prompt
- Always ensure the input `X` is formatted as a 3D array `(n_ts, sz, d)` before calling `fit_transform`.
- Call `fit_transform` on an instantiated transformer object (e.g., `TimeSeriesScalerMinMax().fit_transform(X)`).
- Do not pass raw lists of lists; use `to_time_series_dataset` first to handle variable-length padding.

### Prompt Snippet
```text
Use `transformer.fit_transform(X)` to fit a tslearn preprocessing or transformation model and apply it to the 3D time-series array `X` in a single step. Ensure `X` is strictly a 3D array `(n_ts, sz, d)`.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D `(n_ts, sz, d)` array, causing shape mismatch errors.
- Passing variable-length time series as a raw list of lists without first padding them into a 3D array using `to_time_series_dataset`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset

# Convert raw lists to 3D array before fit_transform
X_3d = to_time_series_dataset(X_raw)
X_transformed = transformer.fit_transform(X_3d)
```

## API Test: `fix_force_all_finite_warning`

### Signature
```python
def fix_force_all_finite_warning(func)
```
_Source: tslearn/tslearn/utils/utils.py:24_

_Source doc:_ Make sure to use sklearn >=1.6 ensure_finite_attribute if available rather than deprecated force_all_attribute

### Goal
Wraps a function to ensure compatibility with `scikit-learn` >= 1.6 by automatically translating the deprecated `force_all_finite` attribute to the newer `ensure_all_finite` equivalent during validation calls.

### Parameters
- `func`: The target function or method to be wrapped, typically one that wraps or calls `scikit-learn` data validation routines.

### Input
A callable function. When the wrapped function is executed, it expects keyword arguments related to finite value checks (e.g., `force_all_finite`).

### Output
Returns `unspecified` — A wrapped callable that intercepts and corrects finite-check keyword arguments before passing them to the original function.

### Valid Call Patterns
```python
from tslearn.utils import fix_force_all_finite_warning

# Inferred from signature
@fix_force_all_finite_warning
def mock_validation(**kwargs):
    return kwargs

# The decorator intercepts and translates deprecated kwargs for scikit-learn >= 1.6
result = mock_validation(force_all_finite=False)
assert isinstance(result, dict), "Wrapped function should return the kwargs dictionary"
print("fix_force_all_finite_warning check passed")
```

### LLM Instruction Prompt
- Use `fix_force_all_finite_warning` as a decorator when writing custom time-series estimators or validation helpers that interface with `scikit-learn`'s `check_array` to prevent deprecation warnings in `scikit-learn` >= 1.6.

### Prompt Snippet
```text
Use `tslearn.utils.fix_force_all_finite_warning` to decorate functions calling `scikit-learn` validation utilities, ensuring the deprecated `force_all_finite` argument is safely translated for `scikit-learn` >= 1.6.
```

### Common Failure Modes
- Passing a non-callable object to `fix_force_all_finite_warning`, which will raise a `TypeError` when the decorator attempts to wrap it or when the result is called.
- Assuming the decorator modifies positional arguments; it strictly intercepts specific keyword arguments related to finite checks.

### Fix Code Hint
```python
# Ensure the decorator is applied to a function definition or a callable
from tslearn.utils import fix_force_all_finite_warning

@fix_force_all_finite_warning
def my_check_array(X, **kwargs):
    # ... internal validation logic ...
    return X
```

## API Test: `forward`

### Signature
```python
def forward(ctx, D, gamma)
def forward(self, x, y)
```
_Source: tslearn/tslearn/metrics/soft_dtw_loss_pytorch.py:34  (+1 more definition site/overload)_

_Source doc:_ Parameters ---------- ctx : context D : Tensor, shape=[b, m, n] Matrix of pairwise distances. gamma : float Regularization parameter. Lower is less smoothed (closer to true DTW). Returns ------- loss : Tensor, shape=[batch_size,] The loss values.

### Goal
Computes the forward pass of the Soft-DTW loss, either by calculating the loss from pairwise distance matrices or directly from batches of time series.

### Parameters
- `ctx`: PyTorch autograd context object used to stash variables for the backward pass (applicable when calling the `torch.autograd.Function` directly).
- `D`: PyTorch `Tensor` of shape `[batch_size, m, n]` representing the matrix of pairwise distances between time series points.
- `gamma`: `float` representing the regularization parameter; lower values are less smoothed and closer to true DTW.

### Input
When calling the `torch.autograd.Function` directly, `D` must be a 3D PyTorch tensor of pairwise distances. When calling the `SoftDTWLossPyTorch` module instance (the `forward(self, x, y)` overload), inputs `x` and `y` must be 3D PyTorch tensors of shape `(batch_size, length, dimensions)`. If gradients are needed for automatic differentiation, the input tensors must be created with `requires_grad=True`.

### Output
Returns `unspecified` — A PyTorch `Tensor` of shape `(batch_size,)` containing the computed Soft-DTW loss values for each pair in the batch.

### Valid Call Patterns
```python
import torch
import tslearn.metrics

b, m, n, d = 5, 10, 12, 8
batch_ts_1 = torch.zeros((b, m, d), requires_grad=True)
batch_ts_2 = torch.ones((b, n, d), requires_grad=True)

# Calling the module overload (most common usage)
soft_dtw_loss_pytorch = tslearn.metrics.SoftDTWLossPyTorch(
    gamma=1.0, normalize=False, dist_func=None
)
loss = soft_dtw_loss_pytorch.forward(batch_ts_1, batch_ts_2)

# The loss is a tensor of shape (batch_size,)
assert loss.shape == (b,)
print(loss.detach().numpy())
```

### LLM Instruction Prompt
- Use `forward` on a `SoftDTWLossPyTorch` instance by passing two 3D PyTorch tensors `x` and `y` of shape `(batch_size, length, dimensions)`.
- Do not pass NumPy arrays; this API strictly requires PyTorch tensors.
- Ensure inputs are 3D tensors, even for a single pair of time series (use `batch_size=1`).
- If gradients are required, ensure the input tensors have `requires_grad=True`.

### Prompt Snippet
```text
When calling `forward` on `SoftDTWLossPyTorch`, provide 3D PyTorch tensors `(batch_size, length, dim)`. Do not pass NumPy arrays. The output is a 1D tensor of shape `(batch_size,)` containing the loss values.
```

### Common Failure Modes
- Passing NumPy arrays instead of PyTorch tensors, which causes PyTorch type errors.
- Passing 2D tensors `(length, dim)` instead of the required 3D batched tensors `(batch_size, length, dim)`.
- Attempting to call `.backward()` on the result when the input tensors were not created with `requires_grad=True`.

### Fix Code Hint
```python
# Wrap inputs in 3D PyTorch tensors with requires_grad=True
batch_ts_1 = torch.tensor(ts1_data, dtype=torch.float64, requires_grad=True).view(1, -1, 1)
batch_ts_2 = torch.tensor(ts2_data, dtype=torch.float64).view(1, -1, 1)

loss_module = tslearn.metrics.SoftDTWLossPyTorch(gamma=1.0)
loss = loss_module.forward(batch_ts_1, batch_ts_2)
```

## API Test: `frechet`

### Signature
```python
def frechet(s1, s2, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/_frechet.py:30_

_Source doc:_ Compute Frechet similarity [1]_ measure between (possibly multidimensional) time series and return it. Frechet similarity score is computed as the maximum distance between aligned time series, i.e., if :math:`\pi` is an optimal alignment path: .. math:: Frechet(X, Y) = \max_{(i, j) \in \pi} \|X_{i} - Y_{j}\| Note that this formula is still valid for the multivariate case. It is not required that both time series share the same size, but they must be the same dimension. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for Frechet distance. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [2]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- float

### Goal
Compute the discrete Fréchet distance between two time series, defined as the maximum distance between aligned points along the optimal alignment path.

### Parameters
- `s1`: array-like of shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like of shape `(sz2, d)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `global_constraint`, default `None`: String (`"itakura"` or `"sakoe_chiba"`) or `None`. Restricts the admissible alignment paths.
- `sakoe_chiba_radius`, default `None`: Integer or `None`. The radius for the Sakoe-Chiba band constraint. If `None` and `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: Float or `None`. The maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint="itakura"`, defaults to 2.0.
- `be`, default `None`: Backend identifier (`"numpy"`, `"pytorch"`, a Backend instance, or `None`). If `None`, the backend is automatically inferred from the input array types.

### Input
Two time series arrays or tensors. They are permitted to have different lengths (`sz1` and `sz2`), but they **must** have the exact same feature dimension `d`. The inputs cannot be empty arrays or lists.

### Output
Returns `float` (or a PyTorch scalar tensor if the PyTorch backend is used). Represents the computed Fréchet distance score.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics

# 1. Basic usage with NumPy arrays
s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.0], [3.0]])
dist = tslearn.metrics.frechet(s1, s2)

assert isinstance(dist, float)
assert np.isclose(dist, 0.0)

# 2. Usage with global constraints
dist_constrained = tslearn.metrics.frechet(
    s1, s2, 
    global_constraint="sakoe_chiba", 
    sakoe_chiba_radius=1
)
assert isinstance(dist_constrained, float)
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.frechet`, ensure both time series have the exact same feature dimension `d` (e.g., both must be `(sz, 2)` or both `(sz, 1)`).
- Do not pass empty lists or arrays; this will raise a `ValueError`.
- If providing both `sakoe_chiba_radius` and `itakura_max_slope`, you must explicitly set `global_constraint` to indicate which one to use, otherwise a `RuntimeWarning` is raised and no constraint is applied.

### Prompt Snippet
```text
Use `tslearn.metrics.frechet(s1, s2)` to compute the Fréchet distance between two time series. The series can have different lengths but must share the same feature dimension. You can restrict the alignment path using `global_constraint="sakoe_chiba"` and `sakoe_chiba_radius=r`.
```

### Common Failure Modes
- **Dimension Mismatch**: Passing time series with different feature dimensions (e.g., `s1` has shape `(10, 1)` and `s2` has shape `(10, 2)`) raises a `ValueError`.
- **Empty Inputs**: Passing empty lists `[]` or empty arrays raises a `ValueError`.
- **Ambiguous Constraints**: Setting both `sakoe_chiba_radius` and `itakura_max_slope` without setting `global_constraint` raises a `RuntimeWarning` and ignores the constraints.

### Fix Code Hint
```python
# FIX: Ensure both time series have the same feature dimension before calling frechet
if s1.shape[-1] != s2.shape[-1]:
    raise ValueError("Time series must have the same feature dimension to compute Fréchet distance.")

# FIX: Explicitly set global_constraint if passing constraint parameters
dist = tslearn.metrics.frechet(
    s1, s2, 
    global_constraint="sakoe_chiba", 
    sakoe_chiba_radius=2
)
```

## API Test: `frechet_path`

### Signature
```python
def frechet_path(s1, s2, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/_frechet.py:171_

### Goal
Compute the Fréchet distance and the optimal alignment path between two (possibly multidimensional) time series.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. Global constraint to restrict admissible paths for the Fréchet distance.
- `sakoe_chiba_radius`, default `None`: `int` or `None`. Radius to be used for the Sakoe-Chiba band global constraint. If `None` and `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: `float` or `None`. Maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint="itakura"`, defaults to 2.0.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`). If `None`, the backend is inferred from the input arrays.

### Input
- Two time series arrays. They can have different lengths (`sz1` and `sz2`) but MUST have the exact same number of feature dimensions (`d`).
- Empty arrays are not allowed.
- Inputs can be standard Python lists, NumPy arrays, or PyTorch tensors.

### Output
Returns `tuple` — A tuple `(path, dist)` where `path` is a list of integer pairs `(i, j)` representing the optimal alignment path, and `dist` is a float (or PyTorch scalar tensor if using the PyTorch backend) representing the Fréchet distance (the maximum distance between aligned points).

### Valid Call Patterns
```python
import tslearn.metrics

# Basic usage with lists
path, dist = tslearn.metrics.frechet_path(
    [1.0, 2.0, 3.0],
    [1.0, 2.0, 2.0, 3.0]
)

assert isinstance(path, list)
assert path == [(0, 0), (1, 1), (1, 2), (2, 3)]
assert dist == 0.0
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.frechet_path`, ensure both time series have the same number of feature dimensions (e.g., both univariate or both having `d` features).
- Expect a tuple of `(path, distance)` to be returned, where `path` is a list of index tuples.
- Do not pass empty arrays.

### Prompt Snippet
```text
Use `tslearn.metrics.frechet_path(s1, s2)` to compute the Fréchet distance and alignment path between two time series. Both inputs must have the same feature dimension `d`. It returns a tuple `(path, dist)` where `path` is a list of `(i, j)` index pairs and `dist` is a float.
```

### Common Failure Modes
- `ValueError`: Raised if either input array is empty (e.g., `tslearn.metrics.frechet_path([], [1, 2])`).
- `ValueError`: Raised if the two time series have a different number of feature dimensions (e.g., `s1` has shape `(10, 1)` and `s2` has shape `(10, 2)`).
- `RuntimeWarning`: Raised if both `sakoe_chiba_radius` and `itakura_max_slope` are provided but `global_constraint` is `None`. The constraints will be ignored.

### Fix Code Hint
```python
import numpy as np
import tslearn.metrics

# Ensure both time series have the same feature dimension before calling
s1 = np.asarray(s1)
s2 = np.asarray(s2)

if s1.ndim == 1:
    s1 = s1.reshape(-1, 1)
if s2.ndim == 1:
    s2 = s2.reshape(-1, 1)
    
if s1.shape[1] != s2.shape[1]:
    raise ValueError(f"Dimension mismatch: {s1.shape[1]} != {s2.shape[1]}")

path, dist = tslearn.metrics.frechet_path(s1, s2)
```

## API Test: `frechet_path_from_metric`

### Signature
```python
def frechet_path_from_metric(s1, s2=None, metric='precomputed', global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None, **kwds)
```
_Source: tslearn/tslearn/metrics/_frechet.py:457_

_Source doc:_ Compute Frechet similarity measure and an optimal alignment path [1]_ between (possibly multidimensional) time series using a distance metric defined by the user. It is not required that both time series share the same size, but they must be the same dimension. When using Pytorch backend only "precomputed", "euclidean", "sqeuclidean" and callable metrics are available. Otherwise, valid values for metric are the same as for scikit-learn `pairwise_distances`_ function i.e. a string (e.g. "euclidean", "sqeuclidean", "hamming") or a function that is used to compute the pairwise distances. See `scikit`_ and `scipy`_ documentations for more information about the available metrics. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) if metric!="precomputed", (sz1, sz2) otherwise A time series or an array of pairwise distances between samples. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,), optional (default: None) A second time series, only used if metric != "precomputed". If shape is (sz2,), the time series is assumed to be univariate. metric : string or callable (default: "precomputed") If metric is "precomputed", `s1` is assumed to be a distance matrix. Otherwise, function used to compute the pairwise distances between each points of `s1` and `s2`. If metric is a string, it must be one of the options compatible with sklearn.metrics.pairwise_distances. Alternatively, if metric is a callable function, it is called on pairs of rows of `s1` and `s2`. The callable should take two 1 dimensional arrays as input and return a value indicating the distance between them. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for Frechet. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [2]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global

### Goal
Compute the discrete Fréchet distance and its optimal alignment path between two time series using a specified distance metric, or directly from a precomputed distance matrix.

### Parameters
- `s1`: Array-like. If `metric="precomputed"`, a 2D distance matrix of shape `(sz1, sz2)`. Otherwise, the first time series of shape `(sz1, d)` or `(sz1,)`.
- `s2`, default `None`: Array-like. The second time series of shape `(sz2, d)` or `(sz2,)`. Only used and required if `metric != "precomputed"`.
- `metric`, default `'precomputed'`: String or callable. If `"precomputed"`, `s1` is treated as a distance matrix. Otherwise, it specifies the pairwise distance metric (e.g., `"euclidean"`, `"sqeuclidean"`) to compute between points of `s1` and `s2`.
- `global_constraint`, default `None`: String (`"itakura"` or `"sakoe_chiba"`) or `None`. Restricts the admissible alignment paths.
- `sakoe_chiba_radius`, default `None`: Integer. The radius for the Sakoe-Chiba band constraint. Defaults to 1 if `global_constraint="sakoe_chiba"`.
- `itakura_max_slope`, default `None`: Float. The maximum slope for the Itakura parallelogram constraint. Defaults to 2.0 if `global_constraint="itakura"`.
- `be`, default `None`: Backend identifier (e.g., `"numpy"`, `"pytorch"`) or a Backend instance. Auto-detected from inputs if `None`.
- `**kwds`: Additional keyword arguments passed to the underlying metric function (e.g., `sklearn.metrics.pairwise_distances`).

### Input
- If `metric="precomputed"`, `s1` must be a 2D array of shape `(sz1, sz2)` representing pairwise distances, and `s2` should be omitted or `None`.
- If `metric!="precomputed"`, both `s1` and `s2` must be provided. They can have different lengths (`sz1` and `sz2`) but must share the exact same feature dimension `d`.
- When using the PyTorch backend, `metric` is strictly limited to `"precomputed"`, `"euclidean"`, `"sqeuclidean"`, or a callable.

### Output
Returns `unspecified` — A tuple `(path, distance)` where `path` is a list of integer index pairs `[(i, j), ...]` representing the optimal alignment, and `distance` is the scalar Fréchet distance (as a float or a PyTorch tensor, depending on the backend).

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import frechet_path_from_metric

# 1. Using a precomputed distance matrix (default metric)
dist_matrix = np.array([
    [0.0, 1.0, 2.0],
    [1.0, 0.0, 1.0],
    [2.0, 1.0, 0.0]
])
path, dist = frechet_path_from_metric(dist_matrix)
assert isinstance(path, list)
assert dist >= 0.0

# 2. Computing from raw time series using a specific metric
s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.0], [3.0]])
path, dist = frechet_path_from_metric(s1, s2, metric="euclidean")
assert path[0] == (0, 0)
```

### LLM Instruction Prompt
- When `metric="precomputed"` (the default), pass ONLY `s1` as a 2D distance matrix of shape `(sz1, sz2)`. Do not pass `s2`.
- When `metric` is a string like `"euclidean"`, you MUST pass both `s1` and `s2`. Ensure they have the same feature dimension `d`.
- If using the PyTorch backend for automatic differentiation, ensure `metric` is one of the supported subset (`"precomputed"`, `"euclidean"`, `"sqeuclidean"`, or callable).

### Prompt Snippet
```text
tslearn.metrics.frechet_path_from_metric(s1, s2=None, metric='precomputed', global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None, **kwds)
Computes the Fréchet distance and alignment path. If metric="precomputed", s1 must be a 2D distance matrix and s2 is None. Otherwise, s1 and s2 are time series arrays of shape (sz, d). Returns (path_list, distance_scalar).
```

### Common Failure Modes
- **Missing `s2` with non-precomputed metric**: Calling `frechet_path_from_metric(s1, metric="euclidean")` without `s2` will raise an error because the function needs a second time series to compute pairwise distances.
- **Dimension mismatch**: Passing `s1` of shape `(10, 2)` and `s2` of shape `(15, 3)` when `metric="euclidean"` will fail because the feature dimensions (`d=2` vs `d=3`) do not match.
- **Unsupported PyTorch metric**: Passing `metric="cityblock"` while providing PyTorch tensors will raise an error, as the PyTorch backend only supports a restricted set of metrics.

### Fix Code Hint
```python
# If you have raw time series, you must specify the metric and provide both s1 and s2:
path, dist = frechet_path_from_metric(ts1, ts2, metric="euclidean")

# If you have a precomputed distance matrix, pass it as s1 and leave s2 as None:
dist_matrix = compute_my_custom_distances(ts1, ts2)
path, dist = frechet_path_from_metric(dist_matrix, metric="precomputed")
```

## API Test: `from_cesium_dataset`

### Signature
```python
def from_cesium_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:713_

_Source doc:_ Transform a cesium-compatible dataset into a tslearn dataset. Parameters ---------- X: list of cesium TimeSeries cesium-formatted dataset (cf. `link <http://cesium-ml.org/docs/api/cesium.time_series.html#cesium.time_series.TimeSeries>`_) Returns ------- array, shape=(n_ts, sz, d) tslearn-formatted dataset. Examples -------- >>> from cesium.time_series import TimeSeries >>> cesium_ds = [TimeSeries(m=numpy.array([1, 2, 3, 4]))] >>> tslearn_arr = from_cesium_dataset(cesium_ds) >>> tslearn_arr.shape (1, 4, 1) >>> cesium_ds = [ ...     TimeSeries(m=numpy.array([[1, 2, 3, 4], ...                               [5, 6, 7, 8]])) ... ] >>> tslearn_arr = from_cesium_dataset(cesium_ds) >>> tslearn_arr.shape (1, 4, 2) Notes ----- Conversion from/to cesium format requires cesium to be installed.

### Goal
Transform a `cesium`-compatible dataset (a list of `cesium.time_series.TimeSeries` objects) into a strict 3D `tslearn` time-series dataset.

### Parameters
- `X`: A list of `cesium.time_series.TimeSeries` objects representing the dataset to be converted.

### Input
A list of `cesium` `TimeSeries` objects. 
**Precondition:** The external `cesium` package must be installed in the Python environment, as `tslearn` relies on it to parse the objects.

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the `tslearn`-formatted dataset, where `n_ts` is the number of time series, `max_sz` is the maximum number of measurements per time series, and `d` is the number of dimensions.

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

try:
    import cesium
    
    # Create a deterministic tslearn dataset
    n, sz, d = 2, 4, 1
    rng = np.random.RandomState(0)
    tslearn_dataset = rng.randn(n, sz, d)
    
    # Roundtrip: tslearn -> cesium -> tslearn
    cesium_ds = tslearn.utils.to_cesium_dataset(tslearn_dataset)
    recovered_dataset = tslearn.utils.from_cesium_dataset(cesium_ds)
    
    assert recovered_dataset.shape == (2, 4, 1)
    np.testing.assert_allclose(tslearn_dataset, recovered_dataset)
    print("Successfully converted from cesium dataset.")

except ImportError:
    print("cesium is not installed; skipping execution.")
```

### LLM Instruction Prompt
- When converting data from the `cesium` library to `tslearn`, use `tslearn.utils.from_cesium_dataset(X)`. Ensure `X` is a list of `cesium.time_series.TimeSeries` objects. Note that this function strictly requires the `cesium` package to be installed in the environment. The output will be a standard `tslearn` 3D NumPy array of shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
tslearn.utils.from_cesium_dataset(X) converts a list of cesium TimeSeries objects into a 3D tslearn NumPy array (n_ts, max_sz, d). Requires the `cesium` package to be installed.
```

### Common Failure Modes
- **`ImportError` or `ModuleNotFoundError`**: Occurs if the `cesium` package is not installed in the environment.
- **`AttributeError`**: Occurs if `X` is a standard Python list of lists or a raw NumPy array instead of a list of `cesium.time_series.TimeSeries` objects, as the function expects to access `cesium`-specific attributes (like `.m` or `.time`).

### Fix Code Hint
```python
# Ensure cesium is installed and imported, or handle the missing dependency gracefully
try:
    from cesium.time_series import TimeSeries
    import tslearn.utils
    
    # X must be a list of TimeSeries objects, not raw arrays
    cesium_ds = [TimeSeries(m=np.array([1, 2, 3, 4]))]
    tslearn_arr = tslearn.utils.from_cesium_dataset(cesium_ds)
except ImportError:
    print("Please install cesium to use from_cesium_dataset.")
```

## API Test: `from_hdf5`

### Signature
```python
def from_hdf5(cls, path)
```
_Source: tslearn/tslearn/bases/bases.py:232_

_Source doc:_ Load model from a HDF5 file. Requires ``h5py`` http://docs.h5py.org/ Parameters ---------- path : str Full path to file. Returns ------- Model instance

### Goal
Loads a serialized `tslearn` machine-learning model instance (such as a clustering or classification estimator) from an HDF5 file.

### Parameters
- `cls`: The class of the model being loaded (e.g., `TimeSeriesKMeans`). Because this is a class method, this parameter is passed implicitly by Python when the method is called on a class (e.g., `ModelClass.from_hdf5(path)`).
- `path`: A string representing the full file path to the `.hdf5` file containing the saved model data.

### Input
The caller must provide a valid string path pointing to an HDF5 file that was previously generated by a `tslearn` model's serialization routine. The Python environment must have the `h5py` package installed to parse the file format.

### Output
Returns `unspecified` — A deserialized instance of the model class (e.g., a fitted `scikit-learn` compatible estimator capable of `.predict()`), populated with the hyperparameters and learned weights stored in the HDF5 file.

### Valid Call Patterns
```python
from tslearn.clustering import TimeSeriesKMeans

# The example is inferred from the signature (not verified).
try:
    # Called as a class method on the specific estimator class
    loaded_model = TimeSeriesKMeans.from_hdf5("non_existent_model.hdf5")
    assert False, "Execution should not reach here without a valid HDF5 file."
except Exception as e:
    # We expect an OSError/FileNotFoundError (missing file) or ImportError (missing h5py)
    assert type(e).__name__ in ("OSError", "FileNotFoundError", "ImportError")
    print(f"Call shape verified. Expected failure without valid file/h5py: {type(e).__name__}")
```

### LLM Instruction Prompt
- When loading a `tslearn` model from disk, you MUST call `from_hdf5` as a class method on the specific estimator class you intend to load (e.g., `TimeSeriesKMeans.from_hdf5(path)`). Do not call it as a standalone function or on an already instantiated object. Ensure `h5py` is installed in the environment.

### Prompt Snippet
```text
# Load a previously saved TimeSeriesKMeans model from an HDF5 file
# Note: Requires `h5py` to be installed in the environment.
from tslearn.clustering import TimeSeriesKMeans

loaded_model = TimeSeriesKMeans.from_hdf5("/path/to/saved_model.hdf5")
predictions = loaded_model.predict(X_scaled)
```

### Common Failure Modes
- **`ImportError`**: Raised if the `h5py` library is not installed in the current Python environment.
- **`FileNotFoundError` / `OSError`**: Raised if the specified `path` does not exist, is misspelled, or lacks read permissions.
- **`TypeError`**: Raised if `from_hdf5` is incorrectly called as a standalone function without a class context, causing the `cls` argument to be missing.

### Fix Code Hint
```python
# BAD: Calling as a standalone function (missing 'cls' argument)
# model = from_hdf5("my_model.hdf5")

# GOOD: Call as a class method on the target estimator class
from tslearn.clustering import TimeSeriesKMeans
model = TimeSeriesKMeans.from_hdf5("my_model.hdf5")
```

## API Test: `from_json`

### Signature
```python
def from_json(cls, path)
```
_Source: tslearn/tslearn/bases/bases.py:273_

_Source doc:_ Load model from a JSON file. Parameters ---------- path : str Full path to file. Returns ------- Model instance

### Goal
Load a serialized time-series machine learning model instance from a JSON file.

### Parameters
- `cls`: The class object of the model to be instantiated. This is passed implicitly when `from_json` is called as a class method (e.g., `EstimatorClass.from_json(...)`).
- `path`: A string representing the full path to the JSON file containing the saved model.

### Input
A string path pointing to a valid JSON file that was previously generated by the corresponding `to_json` serialization method of a `tslearn` estimator.

### Output
Returns `unspecified` — A deserialized instance of the model class (e.g., a fitted estimator) populated with the parameters and learned attributes from the JSON file.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.clustering import TimeSeriesKMeans

# Inferred from signature (not verified by test suite or README)
# We use TimeSeriesKMeans as a representative estimator class
model = TimeSeriesKMeans(n_clusters=2, max_iter=2, random_state=42)

with tempfile.TemporaryDirectory() as tmpdir:
    model_path = os.path.join(tmpdir, "model.json")
    
    # Setup: serialize a model to create a valid JSON file
    model.to_json(model_path)
    
    # Target API: load the model using the class method
    loaded_model = TimeSeriesKMeans.from_json(model_path)
    
    assert isinstance(loaded_model, TimeSeriesKMeans)
    assert loaded_model.n_clusters == 2
    print("Model successfully loaded from JSON.")
```

### LLM Instruction Prompt
- Call `from_json` as a class method on the specific `tslearn` estimator class you intend to load (e.g., `TimeSeriesKMeans.from_json(path)`).
- Do not call it as a standalone function or as an instance method.
- Ensure the provided path points to a valid JSON file previously serialized by a compatible `tslearn` model.

### Prompt Snippet
```text
To load a saved tslearn model, use the `from_json` class method on the target estimator class: `loaded_model = EstimatorClass.from_json("path/to/model.json")`.
```

### Common Failure Modes
- **Incorrect Class:** Calling `from_json` on a different class than the one used to save the model (e.g., attempting to load a classification model using a clustering class) will result in deserialization errors or an invalid object state.
- **Instance Method Call:** Attempting to call `from_json` on an already instantiated object (`my_model.from_json(...)`) instead of the class itself.
- **Missing or Invalid File:** Providing a path to a file that does not exist, or a file that is not formatted as a valid `tslearn` JSON serialization.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function or on an instance
# model = from_json("model.json")
# model = my_model.from_json("model.json")

# RIGHT: Calling as a class method on the specific estimator class
# loaded_model = TimeSeriesKMeans.from_json("model.json")
```

## API Test: `from_numpy`

### Signature
```python
def from_numpy(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:149  (+1 more definition site/overload)_

### Goal
Converts a NumPy array into the active backend's native tensor format (e.g., a PyTorch tensor) for time-series metric computations and automatic differentiation.

### Parameters
- `x`: The input NumPy array to be converted into the backend's native format.

### Input
A standard `numpy.ndarray`, typically representing time-series data formatted as a 3D array `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — A backend-specific data structure (e.g., a `torch.Tensor` for the PyTorch backend or a `numpy.ndarray` for the NumPy backend) containing the same numerical data as the input.

### Valid Call Patterns
```python
import numpy as np
import torch
from tslearn.backend import instantiate_backend

# Inferred from signature and backend context (not verified)
# Instantiate the PyTorch backend
be = instantiate_backend("pytorch")

# Create a standard 3D time-series NumPy array (n_ts=1, max_sz=3, d=1)
x_np = np.array([[[1.0], [2.0], [3.0]]])

# Convert the NumPy array to the backend's native format
x_tensor = be.from_numpy(x_np)

assert isinstance(x_tensor, torch.Tensor), "Expected a PyTorch tensor from the PyTorch backend"
print(f"Converted type: {type(x_tensor)}")
```

### LLM Instruction Prompt
- When preparing data for backend-specific operations (like PyTorch automatic differentiation), instantiate the backend first using `instantiate_backend`, then call `from_numpy(x)` on the backend instance to convert standard NumPy arrays into the target backend's native format.

### Prompt Snippet
```text
be = instantiate_backend("pytorch")
x_tensor = be.from_numpy(x_array)
```

### Common Failure Modes
- Calling `from_numpy` directly as a top-level module function instead of invoking it on a dynamically instantiated backend object.
- Passing non-NumPy objects (like raw Python lists) that the specific backend's `from_numpy` implementation cannot safely cast or ingest.
- Forgetting that the output type changes dynamically based on the active backend (e.g., expecting a NumPy array when the PyTorch backend is active).

### Fix Code Hint
```python
# Incorrect: from tslearn.backend import from_numpy; from_numpy(x)
# Correct:
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
x_tensor = be.from_numpy(x_numpy_array)
```

## API Test: `from_pickle`

### Signature
```python
def from_pickle(cls, path)
```
_Source: tslearn/tslearn/bases/bases.py:321_

_Source doc:_ Load model from a pickle file. Parameters ---------- path : str Full path to file. Returns ------- Model instance

### Goal
Load a serialized `tslearn` model instance from a pickle file on disk.

### Parameters
- `cls`: The class of the model being loaded (implicitly passed when called as a class method on a `tslearn` estimator).
- `path`: A string representing the full path to the pickle file to load.

### Input
A valid file path string pointing to a pickle file that contains a serialized `tslearn` model.

### Output
Returns `unspecified` — A deserialized instance of the model class.

### Valid Call Patterns
```python
import os
import pickle
from tslearn.clustering import TimeSeriesKMeans

# Setup: create a dummy pickle file containing a model
model = TimeSeriesKMeans(n_clusters=2)
with open("dummy_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Inferred from signature: call as a class method on the estimator
loaded_model = TimeSeriesKMeans.from_pickle("dummy_model.pkl")

assert isinstance(loaded_model, TimeSeriesKMeans)
print("Successfully loaded:", type(loaded_model).__name__)

# Teardown
os.remove("dummy_model.pkl")
```

### LLM Instruction Prompt
- Call `from_pickle` as a class method on the specific `tslearn` estimator class you wish to load (e.g., `TimeSeriesKMeans.from_pickle(path)`).
- Do not call it as a standalone module-level function.
- Provide a valid string path to an existing pickle file.

### Prompt Snippet
```text
Call `from_pickle` as a class method on the specific `tslearn` estimator class (e.g., `TimeSeriesKMeans.from_pickle("model.pkl")`). Do not call it as a standalone function. Ensure the file path exists and contains a valid pickled model.
```

### Common Failure Modes
- Calling `from_pickle` as a standalone module-level function instead of a class method on an estimator class, resulting in a `NameError` or missing `cls` argument.
- `FileNotFoundError` if the provided `path` does not exist.
- `AttributeError` or `TypeError` if the pickle file contains an object incompatible with the calling class or if the environment lacks the dependencies required to unpickle the object.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function
# model = from_pickle("model.pkl")

# RIGHT: Calling as a class method on the target estimator class
from tslearn.clustering import TimeSeriesKMeans
model = TimeSeriesKMeans.from_pickle("model.pkl")
```

## API Test: `from_pyflux_dataset`

### Signature
```python
def from_pyflux_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:460_

_Source doc:_ Transform a pyflux-compatible dataset into a tslearn dataset. Parameters ---------- X: pandas data-frame pyflux-formatted dataset Returns ------- array, shape=(n_ts, sz, d), where n_ts=1 tslearn-formatted dataset. Column order is kept the same as in the original data frame. Examples -------- >>> import pandas as pd >>> pyflux_df = pd.DataFrame() >>> pyflux_df["dim_0"] = numpy.random.rand(10) >>> tslearn_arr = from_pyflux_dataset(pyflux_df) >>> tslearn_arr.shape (1, 10, 1) >>> pyflux_df = pd.DataFrame() >>> pyflux_df["dim_0"] = numpy.random.rand(10) >>> pyflux_df["dim_1"] = numpy.random.rand(10) >>> pyflux_df["dim_2"] = numpy.random.rand(10) >>> tslearn_arr = from_pyflux_dataset(pyflux_df) >>> tslearn_arr.shape (1, 10, 3) >>> pyflux_arr = numpy.random.randn(10, 1, 16) >>> from_pyflux_dataset( ...     pyflux_arr ... )  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: X is not a valid input pyflux array. Notes ----- Conversion from/to pyflux format requires pandas to be installed.

### Goal
Transform a pyflux-compatible dataset (a pandas DataFrame) into a strict 3D `tslearn`-formatted numpy array.

### Parameters
- `X`: A pandas DataFrame representing a pyflux-formatted dataset, where columns correspond to dimensions and rows correspond to time steps.

### Input
- A `pandas.DataFrame` containing the time-series data.
- The `pandas` library must be installed in the Python environment.
- The input represents a *single* time series, meaning the resulting `tslearn` dataset will always have exactly one time series (`n_ts=1`).

### Output
Returns `unspecified` — A 3D `numpy.ndarray` of shape `(1, sz, d)`, where `sz` is the number of time steps (rows in the DataFrame) and `d` is the number of dimensions (columns). The column order is preserved from the original DataFrame.

### Valid Call Patterns
```python
import pandas as pd
import numpy as np
from tslearn.utils import from_pyflux_dataset

# Create a deterministic pyflux-compatible pandas DataFrame
pyflux_df = pd.DataFrame({
    "dim_0": np.array([0.1, 0.2, 0.3, 0.4]),
    "dim_1": np.array([0.5, 0.6, 0.7, 0.8])
})

# Convert to tslearn format
tslearn_arr = from_pyflux_dataset(pyflux_df)

# Assert the expected 3D shape (n_ts=1, sz=4, d=2)
assert tslearn_arr.shape == (1, 4, 2)
print("Converted array shape:", tslearn_arr.shape)
```

### LLM Instruction Prompt
- Use `tslearn.utils.from_pyflux_dataset(X)` to convert a pyflux-formatted pandas DataFrame into a `tslearn` 3D numpy array.
- Ensure the input `X` is a pandas DataFrame, not a numpy array.
- Be aware that the resulting array will always represent a single time series (`n_ts=1`), with shape `(1, sz, d)`.

### Prompt Snippet
```text
Use `tslearn.utils.from_pyflux_dataset(X)` to convert a pyflux pandas DataFrame into a tslearn 3D array of shape `(1, sz, d)`. The input must be a pandas DataFrame.
```

### Common Failure Modes
- Passing a numpy array instead of a pandas DataFrame results in `ValueError: X is not a valid input pyflux array.`
- Missing the `pandas` dependency will raise an `ImportError`.
- Assuming the output can contain multiple time series (`n_ts > 1`); pyflux DataFrames are mapped to a single time series in `tslearn`.

### Fix Code Hint
```python
import pandas as pd
from tslearn.utils import from_pyflux_dataset

# If you have a numpy array, convert it to a DataFrame first, 
# or use to_time_series_dataset instead if it's not pyflux data.
if not isinstance(X, pd.DataFrame):
    X = pd.DataFrame(X)

tslearn_arr = from_pyflux_dataset(X)
```

## API Test: `from_pyts_dataset`

### Signature
```python
def from_pyts_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:100_

_Source doc:_ Transform a pyts-compatible dataset into a tslearn dataset. Parameters ---------- X: array, shape = (n_ts, sz) or (n_ts, d, sz) pyts-formatted dataset Returns ------- array, shape=(n_ts, sz, d) tslearn-formatted dataset Examples -------- >>> pyts_arr = numpy.random.randn(10, 16) >>> tslearn_arr = from_pyts_dataset(pyts_arr) >>> tslearn_arr.shape (10, 16, 1) >>> pyts_arr = numpy.random.randn(10, 2, 16) >>> tslearn_arr = from_pyts_dataset(pyts_arr) >>> tslearn_arr.shape (10, 16, 2) >>> pyts_arr = numpy.random.randn(10) >>> from_pyts_dataset(pyts_arr)  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: X is not a valid input pyts array.

### Goal
Transform a `pyts`-formatted time-series dataset into the strict 3D `(n_ts, sz, d)` array format required by `tslearn` estimators and metrics.

### Parameters
- `X`: A `pyts`-formatted dataset array. It must have a shape of `(n_ts, sz)` for univariate time series or `(n_ts, d, sz)` for multivariate time series, where `n_ts` is the number of time series, `sz` is the length, and `d` is the number of dimensions.

### Input
The caller must provide a 2D or 3D NumPy array representing time-series data formatted for the `pyts` library. 1D arrays (e.g., a single un-batched time series) are invalid and will be rejected.

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, sz, d)` representing the `tslearn`-formatted dataset, ready to be consumed by `tslearn` preprocessing, clustering, or classification APIs.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import from_pyts_dataset

# 1. Univariate pyts dataset: shape (n_ts, sz)
pyts_univariate = np.zeros((10, 16))
tslearn_univariate = from_pyts_dataset(pyts_univariate)

assert tslearn_univariate.shape == (10, 16, 1)

# 2. Multivariate pyts dataset: shape (n_ts, d, sz)
pyts_multivariate = np.zeros((10, 2, 16))
tslearn_multivariate = from_pyts_dataset(pyts_multivariate)

assert tslearn_multivariate.shape == (10, 16, 2)
print(f"Successfully converted pyts arrays to tslearn shapes: {tslearn_univariate.shape} and {tslearn_multivariate.shape}")
```

### LLM Instruction Prompt
- When integrating data from `pyts` pipelines into `tslearn`, use `tslearn.utils.from_pyts_dataset(X)` to automatically transpose and reshape the data into `tslearn`'s required `(n_ts, sz, d)` 3D format. Ensure the input `X` is strictly 2D or 3D; 1D arrays will raise a `ValueError`.

### Prompt Snippet
```text
Use `tslearn.utils.from_pyts_dataset(X)` to convert `pyts` arrays `(n_ts, sz)` or `(n_ts, d, sz)` into `tslearn`'s strict 3D format `(n_ts, sz, d)`. Do not pass 1D arrays.
```

### Common Failure Modes
- Passing a 1D array (e.g., `np.random.randn(10)`) representing a single time series without the batch dimension. This raises `ValueError: X is not a valid input pyts array.`
- Passing a dataset that is already in `tslearn` format `(n_ts, sz, d)` when `d > 1`. The function will misinterpret the dimensions, assuming the second dimension is `d` and the third is `sz`, resulting in an incorrectly transposed output.

### Fix Code Hint
```python
# If you have a 1D array, reshape it to 2D (1, sz) before converting, 
# or use to_time_series_dataset instead.
import numpy as np
from tslearn.utils import from_pyts_dataset

pyts_1d = np.zeros(16)
# Fix: Reshape to add the n_ts dimension
tslearn_arr = from_pyts_dataset(pyts_1d.reshape(1, -1))
```

## API Test: `from_seglearn_dataset`

### Signature
```python
def from_seglearn_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:182_

_Source doc:_ Transform a seglearn-compatible dataset into a tslearn dataset. Parameters ---------- X: list of arrays, or array of arrays, shape = (n_ts, ) seglearn-formatted dataset. i-th sub-array in the list has shape (sz_i, d) Returns ------- array, shape=(n_ts, sz, d), where sz is the maximum of all array lengths tslearn-formatted dataset Examples -------- >>> seglearn_arr = [numpy.random.randn(10, 1), numpy.random.randn(10, 1)] >>> tslearn_arr = from_seglearn_dataset(seglearn_arr) >>> tslearn_arr.shape (2, 10, 1) >>> seglearn_arr = [numpy.random.randn(10, 1), numpy.random.randn(5, 1)] >>> tslearn_arr = from_seglearn_dataset(seglearn_arr) >>> tslearn_arr.shape (2, 10, 1) >>> seglearn_arr = numpy.random.randn(2, 10, 1) >>> tslearn_arr = from_seglearn_dataset(seglearn_arr) >>> tslearn_arr.shape (2, 10, 1)

### Goal
Transform a `seglearn`-compatible dataset (a list or array of 2D arrays) into a strict 3D `tslearn`-formatted NumPy array `(n_ts, max_sz, d)`.

### Parameters
- `X`: A list of arrays or an array of arrays representing a `seglearn`-formatted dataset. The `i`-th sub-array in the list must have shape `(sz_i, d)`, where `sz_i` is the length of the `i`-th time series and `d` is the number of dimensions/features.

### Input
The caller must provide a list of 2D NumPy arrays (or a single 3D array) where each element represents a time series. Variable-length time series are natively supported (i.e., `sz_i` can vary across the sub-arrays). The feature dimension `d` must be consistent across all time series.

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)`, where `n_ts` is the number of time series, `max_sz` is the maximum length among all input time series, and `d` is the feature dimension. Shorter time series are padded with `nan` values at the end to match `max_sz`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import from_seglearn_dataset

# Create a seglearn-formatted dataset with variable-length univariate time series
seglearn_arr = [
    np.ones((10, 1)),  # Length 10, 1 dimension
    np.ones((5, 1))    # Length 5, 1 dimension
]

# Convert to tslearn format
tslearn_arr = from_seglearn_dataset(seglearn_arr)

# Verify the shape is (n_ts, max_sz, d)
assert tslearn_arr.shape == (2, 10, 1)

# Verify that the shorter time series is padded with NaNs
assert np.isnan(tslearn_arr[1, 5:, 0]).all()
print(f"Converted shape: {tslearn_arr.shape}")
```

### LLM Instruction Prompt
- When converting data from `seglearn` to `tslearn`, pass the list of 2D arrays to `from_seglearn_dataset`. Expect a 3D NumPy array `(n_ts, max_sz, d)` back, where shorter series are padded with `nan`. Ensure the input sub-arrays are strictly 2D `(sz_i, d)`, not 1D.

### Prompt Snippet
```text
tslearn.utils.from_seglearn_dataset(X) converts a seglearn dataset (list of 2D arrays of shape (sz_i, d)) into a tslearn 3D array (n_ts, max_sz, d), padding shorter series with NaNs.
```

### Common Failure Modes
- Passing a list of 1D arrays (e.g., `[np.array([1, 2, 3])]`) instead of 2D arrays. `seglearn` format strictly requires the feature dimension `d` to be explicit, even for univariate data (e.g., `(sz_i, 1)`).
- Passing sub-arrays with inconsistent feature dimensions `d`. All time series must have the same number of features.

### Fix Code Hint
```python
# Incorrect: List of 1D arrays
# bad_seglearn_arr = [np.array([1, 2, 3]), np.array([4, 5])]

# Correct: Reshape to 2D arrays (sz_i, 1) before passing to from_seglearn_dataset
good_seglearn_arr = [np.array([[1], [2], [3]]), np.array([[4], [5]])]
tslearn_arr = from_seglearn_dataset(good_seglearn_arr)
```

## API Test: `from_sktime_dataset`

### Signature
```python
def from_sktime_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:335_

### Goal
Convert a `sktime`-formatted time-series dataset (a pandas DataFrame containing pandas Series in its cells) into `tslearn`'s strict 3D NumPy array format `(n_ts, max_sz, d)`.

### Parameters
- `X`: A pandas DataFrame representing a `sktime`-formatted dataset, where rows correspond to individual time series, columns correspond to dimensions, and individual cells contain `pandas.Series` objects.

### Input
The caller must provide a valid `sktime` pandas DataFrame. The `pandas` library must be installed in the environment. The input natively supports variable-length time series (where the `pandas.Series` in different rows have different lengths). Passing a raw NumPy array or standard 2D DataFrame will fail.

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the `tslearn`-formatted dataset. For variable-length time series, shorter series are automatically right-padded with `nan` values to match `max_sz`.

### Valid Call Patterns
```python
import pandas as pd
import numpy as np
from tslearn.utils import from_sktime_dataset

# 1. Construct a sktime-formatted DataFrame with variable-length series
# Rows are instances (n_ts=2), columns are dimensions (d=2)
sktime_df = pd.DataFrame()
sktime_df["dim_0"] = [pd.Series([1.0, 2.0, 3.0]), pd.Series([4.0, 5.0])]
sktime_df["dim_1"] = [pd.Series([8.0, 9.0, 10.0]), pd.Series([11.0, 12.0])]

# 2. Convert to tslearn 3D array format
tslearn_arr = from_sktime_dataset(sktime_df)

# 3. Verify the shape (n_ts=2, max_sz=3, d=2) and padding
assert tslearn_arr.shape == (2, 3, 2)
assert np.isnan(tslearn_arr[1, 2, 0])  # The shorter series is padded with nan
print(f"Successfully converted sktime DataFrame to tslearn array of shape: {tslearn_arr.shape}")
```

### LLM Instruction Prompt
- When integrating `sktime` data pipelines with `tslearn` estimators, use `tslearn.utils.from_sktime_dataset(X)` to convert the data.
- Ensure the input `X` is a pandas DataFrame where cells contain `pandas.Series` objects.
- Do not pass raw NumPy arrays to this function; it will raise a `ValueError`. If you already have raw lists or arrays, use `tslearn.utils.to_time_series_dataset` instead.
- Be aware that variable-length series will be padded with `nan` values in the resulting `(n_ts, max_sz, d)` array.

### Prompt Snippet
```text
tslearn.utils.from_sktime_dataset(X)
Converts a sktime pandas DataFrame (cells are pd.Series) to a tslearn 3D numpy array (n_ts, max_sz, d). Pads variable-length series with nan. Raises ValueError if X is a raw numpy array. Requires pandas.
```

### Common Failure Modes
- **Passing a raw NumPy array:** Calling `from_sktime_dataset(numpy.random.randn(10, 1, 16))` raises `ValueError: X is not a valid input sktime array.`
- **Missing pandas dependency:** The conversion strictly requires `pandas` to be installed, as `sktime` format relies on pandas DataFrames and Series.
- **Standard 2D DataFrame:** Passing a standard pandas DataFrame containing scalar floats instead of `pandas.Series` objects will fail validation.

### Fix Code Hint
```python
import pandas as pd
import numpy as np
from tslearn.utils import from_sktime_dataset, to_time_series_dataset

# BAD: Passing a raw numpy array to the sktime converter
# X_bad = np.random.randn(10, 1, 16)
# tslearn_arr = from_sktime_dataset(X_bad)  # Raises ValueError

# GOOD: If you have a sktime DataFrame (cells are Series)
sktime_df = pd.DataFrame({
    "dim_0": [pd.Series([1, 2, 3]), pd.Series([4, 5, 6])]
})
tslearn_arr = from_sktime_dataset(sktime_df)

# ALTERNATIVE: If you just have raw lists/arrays, bypass sktime entirely
raw_data = [[1, 2, 3], [4, 5, 6]]
tslearn_arr_direct = to_time_series_dataset(raw_data)
```

## API Test: `from_stumpy_dataset`

### Signature
```python
def from_stumpy_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:256_

_Source doc:_ Transform a stumpy-compatible dataset into a tslearn dataset. Parameters ---------- X: list of arrays of shapes (d, sz_i) if d > 1 or (sz_i, ) otherwise stumpy-formatted dataset. Returns ------- array, shape=(n_ts, sz, d), where sz is the maximum of all array lengths tslearn-formatted dataset Examples -------- >>> stumpy_arr = [numpy.random.randn(10), numpy.random.randn(10)] >>> tslearn_arr = from_stumpy_dataset(stumpy_arr) >>> tslearn_arr.shape (2, 10, 1) >>> stumpy_arr = [numpy.random.randn(3, 10), numpy.random.randn(3, 5)] >>> tslearn_arr = from_stumpy_dataset(stumpy_arr) >>> tslearn_arr.shape (2, 10, 3)

### Goal
Convert a `stumpy`-compatible time-series dataset (a list of arrays where the spatial dimension precedes the time dimension) into a strict 3D `tslearn`-formatted NumPy array.

### Parameters
- `X`: A list of NumPy arrays representing the `stumpy`-formatted dataset. Each array must have the shape `(d, sz_i)` for multivariate data (where `d > 1`) or `(sz_i, )` for univariate data.

### Input
The caller must provide a list of NumPy arrays. The arrays can represent variable-length time series (different `sz_i` values). For multivariate data, the number of dimensions `d` must be consistent across all arrays in the list, and `d` must be the *first* axis (unlike `tslearn` where it is the last axis).

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, max_sz, d)`, where `n_ts` is the number of time series (length of the input list), `max_sz` is the maximum length among all provided time series, and `d` is the number of dimensions. Shorter time series are padded with `nan` values at the end.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import from_stumpy_dataset

# Deterministic stumpy-formatted dataset: list of (d, sz_i) arrays
stumpy_data = [
    np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]), # d=2, sz=3
    np.array([[7.0, 8.0], [9.0, 10.0]])           # d=2, sz=2
]

# Convert to tslearn format (n_ts, max_sz, d)
tslearn_data = from_stumpy_dataset(stumpy_data)

print(f"Converted shape: {tslearn_data.shape}")
assert tslearn_data.shape == (2, 3, 2)
assert np.isnan(tslearn_data[1, 2, 0]), "Shorter series should be nan-padded"
```

### LLM Instruction Prompt
- Use `from_stumpy_dataset` when bridging data from the `stumpy` library (e.g., matrix profile computations) into `tslearn` estimators.
- Remember that `stumpy` formats multivariate data as `(d, sz_i)` while `tslearn` expects `(sz_i, d)`. This function automatically handles the transposition and `nan`-padding for variable-length series.
- Do not pass a 3D array directly to this function; it expects a list of 1D or 2D arrays.

### Prompt Snippet
```text
When integrating `stumpy` matrix profile workflows with `tslearn` clustering, use `tslearn.utils.from_stumpy_dataset(stumpy_list)` to convert the list of `(d, sz_i)` arrays into the required `(n_ts, max_sz, d)` 3D array format.
```

### Common Failure Modes
- Passing a single 3D NumPy array instead of a list of 1D/2D arrays, which violates the expected `stumpy` format.
- Providing a list of arrays with inconsistent dimensionalities `d` (e.g., mixing univariate `(sz_i,)` and multivariate `(2, sz_i)` arrays).
- Passing arrays where the time dimension is the first axis for multivariate data (e.g., `(sz_i, d)`). `stumpy` strictly expects `(d, sz_i)`.

### Fix Code Hint
```python
# BAD: Passing a 3D array directly or using (sz_i, d) format
# tslearn_data = from_stumpy_dataset(np.random.randn(2, 10, 3))

# GOOD: Pass a list of arrays with shape (d, sz_i)
stumpy_list = [np.random.randn(3, 10), np.random.randn(3, 5)]
tslearn_data = from_stumpy_dataset(stumpy_list)
```

## API Test: `from_tsfresh_dataset`

### Signature
```python
def from_tsfresh_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:578_

### Goal
Convert a `tsfresh`-compatible flat pandas DataFrame into the strict 3D NumPy array `(n_ts, max_sz, d)` format required by `tslearn` estimators.

### Parameters
- `X`: A pandas DataFrame representing a `tsfresh`-formatted dataset (a "flat" data frame typically containing an identifier column, a time column, and one or more feature columns).

### Input
The environment must have `pandas` installed. The input `X` must be a pandas DataFrame structured in the `tsfresh` flat format. It cannot be a raw NumPy array or a standard Python list.

### Output
Returns a 3D NumPy array of shape `(n_ts, max_sz, d)` representing the `tslearn`-formatted dataset, where `n_ts` is the number of unique time series (IDs), `max_sz` is the maximum number of time steps, and `d` is the number of feature dimensions. Column order is kept the same as in the original data frame.

### Valid Call Patterns
```python
import pandas as pd
from tslearn.utils import from_tsfresh_dataset

# 1. Construct a tsfresh-compatible flat pandas DataFrame
tsfresh_df = pd.DataFrame({
    "id": [0, 0, 0, 1, 1],
    "time": [0, 1, 2, 0, 1],
    "feature_a": [-1, 4, 7, 9, 1]
})

# 2. Convert to a tslearn 3D array
tslearn_arr = from_tsfresh_dataset(tsfresh_df)

# 3. Verify the resulting shape (n_ts=2, max_sz=3, d=1)
assert tslearn_arr.shape == (2, 3, 1)
print(f"Successfully converted tsfresh DataFrame to tslearn array of shape: {tslearn_arr.shape}")
```

### LLM Instruction Prompt
- When converting data from `tsfresh` to `tslearn`, you MUST pass a pandas DataFrame to `from_tsfresh_dataset`. Do not pass a NumPy array or a list of lists.
- Ensure `pandas` is installed in the environment, as it is a strict requirement for this conversion utility.
- The resulting object is a 3D NumPy array `(n_ts, max_sz, d)` that can be directly fed into `tslearn` preprocessing and estimator APIs.

### Prompt Snippet
```text
Use `tslearn.utils.from_tsfresh_dataset(X)` to convert a flat `tsfresh` pandas DataFrame into a 3D `tslearn` NumPy array. The input `X` must be a pandas DataFrame; passing a NumPy array will raise a ValueError.
```

### Common Failure Modes
- **Passing a NumPy array instead of a DataFrame**: Yields `ValueError: X is not a valid input tsfresh array.` `tsfresh` format inherently relies on pandas DataFrames to distinguish IDs, time steps, and features.
- **Missing pandas dependency**: Yields an `ImportError` or `ModuleNotFoundError` if `pandas` is not installed in the environment, as the conversion explicitly requires it.

### Fix Code Hint
```python
# BAD: Passing a NumPy array directly
# tslearn_arr = from_tsfresh_dataset(np.random.randn(10, 1, 16))

# GOOD: Ensure the input is a properly formatted pandas DataFrame
import pandas as pd
from tslearn.utils import from_tsfresh_dataset

# Create a flat dataframe with 'id' and 'time' indicators
df = pd.DataFrame({
    "id": [0, 0, 1, 1],
    "time": [0, 1, 0, 1],
    "value": [1.5, 2.0, 3.1, 1.1]
})
tslearn_arr = from_tsfresh_dataset(df)
```

## API Test: `gak`

### Signature
```python
def gak(s1, s2, sigma=1.0, be=None)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:206  (+1 more definition site/overload)_

_Source doc:_ Compute Global Alignment Kernel (GAK) between (possibly multidimensional) time series and return it. It is not required that both time series share the same size, but they must be the same dimension. GAK was originally presented in [1]_. This is a normalized version that ensures that :math:`k(x,x)=1` for all :math:`x` and :math:`k(x,y) \in [0, 1]` for all :math:`x, y`. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. sigma : float (default 1.) Bandwidth of the internal gaussian kernel used for GAK. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- float Kernel value Examples -------- >>> float(gak([1, 2, 3], [1., 2., 2., 3.], sigma=2.))  # doctest: +ELLIPSIS 0.839... >>> float(gak([1, 2, 3], [1., 2., 2., 3., 4.]))  # doctest: +ELLIPSIS 0.273... See Also -------- cdist_gak : Compute cross-similarity matrix using Global Alignment kernel References ---------- .. [1] M. Cuturi, "Fast global alignment kernels," ICML 2011.

### Goal
Compute the normalized Global Alignment Kernel (GAK) similarity between two time series, yielding a value between 0 and 1.

### Parameters
- `s1`: The first time series. Array-like of shape `(sz1, d)` or `(sz1,)` (assumed univariate).
- `s2`: The second time series. Array-like of shape `(sz2, d)` or `(sz2,)` (assumed univariate).
- `sigma`, default `1.0`: Bandwidth of the internal Gaussian kernel used for GAK. Must be a non-zero float.
- `be`, default `None`: The computational backend to use. Can be the string `"numpy"`, `"pytorch"`, a Backend instance, or `None` to auto-detect based on the input array types.

### Input
Two time series provided as lists, NumPy arrays, or PyTorch tensors. The time series do not need to have the same length (`sz1` can differ from `sz2`), but they *must* have the exact same feature dimension `d`.

### Output
Returns `unspecified` — A `float` (or a backend-specific scalar tensor, like a PyTorch tensor if `be="pytorch"`) representing the normalized kernel similarity value. A value of `1.0` indicates identical time series, while values approaching `0.0` indicate high dissimilarity.

### Valid Call Patterns
```python
import pytest
from tslearn.metrics import gak

# 1. Standard usage with lists and explicit sigma
sim = gak([1, 2, 3], [1.0, 2.0, 2.0, 3.0], sigma=2.0)
assert 0.0 <= float(sim) <= 1.0
print(f"GAK similarity: {sim:.3f}")

# 2. Usage with default sigma
sim_default = gak([1, 2, 3], [1.0, 2.0, 2.0, 3.0, 4.0])
assert 0.0 <= float(sim_default) <= 1.0

# 3. Explicit backend selection
sim_np = gak([1, 2, 3], [1, 2, 3], sigma=1.5, be="numpy")
assert float(sim_np) == 1.0
```

### LLM Instruction Prompt
- Import `gak` from `tslearn.metrics`.
- Ensure `sigma` is strictly greater than `0` to avoid a `ZeroDivisionError`.
- Ensure `s1` and `s2` share the same feature dimension `d` (e.g., both univariate, or both having 3 features per timestep).
- Remember that `gak` computes a *similarity* kernel (higher is more similar, max 1.0), unlike distance metrics like DTW (where lower is more similar, min 0.0).

### Prompt Snippet
```text
Compute the Global Alignment Kernel similarity between `ts1` and `ts2` using `tslearn.metrics.gak`. Set the Gaussian kernel bandwidth `sigma` to 2.5.
```

### Common Failure Modes
- **`ZeroDivisionError`**: Occurs if `sigma=0` is passed, as the internal Gaussian kernel divides by `2 * sigma^2`.
- **Dimension Mismatch**: Occurs if `s1` and `s2` have different feature dimensions `d` (e.g., comparing a univariate time series to a multivariate one).

### Fix Code Hint
```python
from tslearn.metrics import gak

s1 = [[1.0, 0.5], [2.0, 0.5]] # shape (2, 2)
s2 = [[1.0, 0.5], [1.5, 0.5], [2.0, 0.5]] # shape (3, 2)

# FIX: Ensure sigma > 0 and both series have the same feature dimension (d=2)
similarity = gak(s1, s2, sigma=1.5)
```

## API Test: `gamma_soft_dtw`

### Signature
```python
def gamma_soft_dtw(dataset, n_samples=100, random_state=None, be=None)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:474_

_Source doc:_ Compute gamma value to be used for GAK/Soft-DTW. This method was originally presented in [1]_. Parameters ---------- dataset : array-like, shape=(n_ts, sz, d) or (n_ts, sz1) or (sz,) A dataset of time series. If shape is (n_ts, sz), the dataset is composed of univariate time series. If shape is (sz,), the dataset is composed of a unique univariate time series. n_samples : int (default: 100) Number of samples on which median distance should be estimated. random_state : integer or numpy.RandomState or None (default: None) The generator used to draw the samples. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- float Suggested :math:`\gamma` parameter for the Soft-DTW. Examples -------- >>> dataset = [[1, 2, 2, 3], [1., 2., 3., 4.]] >>> float(gamma_soft_dtw(dataset=dataset, ...                      n_samples=200, ...                      random_state=0))  # doctest: +ELLIPSIS 8.0... See Also -------- sigma_gak : Compute sigma parameter for Global Alignment kernel References ---------- .. [1] M. Cuturi, "Fast global alignment kernels," ICML 2011.

### Goal
Compute a heuristically suggested `gamma` hyperparameter based on median distances to be used for Soft-DTW or Global Alignment Kernel (GAK) computations.

### Parameters
- `dataset`: Array-like of time series. Expected shapes are `(n_ts, sz, d)` for multivariate, `(n_ts, sz)` for univariate, or `(sz,)` for a single univariate time series.
- `n_samples`, default `100`: Integer representing the number of samples drawn from the dataset on which the median distance should be estimated.
- `random_state`, default `None`: Integer, `numpy.RandomState` instance, or `None`. Fixes the seed for the random generator used to draw the samples.
- `be`, default `None`: Backend object, string (`"numpy"` or `"pytorch"`), or `None`. If `None`, the backend is automatically inferred from the input array types.

### Input
A dataset of time series, ideally formatted as a strict 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`. The input can be standard Python lists, NumPy arrays, or PyTorch tensors. If variable-length time series are provided as a 3D array, shorter series must be padded with `nan` values.

### Output
Returns `unspecified` — A scalar float (or a 0-dimensional PyTorch tensor if the PyTorch backend is used) representing the suggested $\gamma$ parameter for Soft-DTW.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

# Using standard lists (auto-converted to NumPy backend)
dataset = [[1, 2, 2, 3], [1.0, 2.0, 3.0, 4.0]]
gamma = tslearn.metrics.gamma_soft_dtw(
    dataset=dataset, 
    n_samples=200, 
    random_state=0
)

# Verify the heuristic output
np.testing.assert_allclose(float(gamma), 8.0)
```

### LLM Instruction Prompt
- When configuring a Soft-DTW metric or loss function, use `gamma_soft_dtw` to automatically estimate a sensible `gamma` value based on the dataset's median pairwise distances.
- Always pass a fixed `random_state` integer if deterministic execution is required, as this function relies on random sampling.
- If integrating with PyTorch neural networks, pass `be="pytorch"` or provide PyTorch tensors as the `dataset` so the returned gamma is compatible with the PyTorch backend.

### Prompt Snippet
```text
Use `tslearn.metrics.gamma_soft_dtw(dataset, random_state=42)` to heuristically determine the `gamma` parameter before computing `soft_dtw`. Ensure the dataset is formatted as a 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset` if it contains variable-length sequences.
```

### Common Failure Modes
- Passing a raw list of variable-length lists without first converting them using `to_time_series_dataset`, which can cause jagged array errors in NumPy.
- Expecting a standard Python `float` when passing PyTorch tensors; the function will return a 0D PyTorch tensor if the PyTorch backend is triggered.
- Setting `n_samples` larger than the number of possible pairs in a very small dataset, though the function handles sampling with replacement.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import gamma_soft_dtw

# FIX: Format variable-length data into a padded 3D array first
raw_data = [[1, 2, 3], [1, 2, 3, 4, 5]]
formatted_dataset = to_time_series_dataset(raw_data)

# Compute gamma deterministically
gamma_val = gamma_soft_dtw(formatted_dataset, random_state=42)
```

## API Test: `get_backend`

### Signature
```python
def get_backend(self)
```
_Source: tslearn/tslearn/backend/backend.py:84_

### Goal
Retrieves the underlying specific backend implementation instance (such as `NumPyBackend` or `PyTorchBackend`) from a `Backend` wrapper object.

### Parameters
- `self`: The instantiated `Backend` wrapper object from which to extract the active backend implementation.

### Input
A valid, instantiated `Backend` object (e.g., created via `Backend("torch")` or `Backend("numpy")`). The environment must have the corresponding dependencies installed (e.g., `pytorch` locally installed if the backend was initialized for PyTorch).

### Output
Returns `unspecified` — Represents the specific backend instance currently active within the wrapper. Depending on the configuration, this will typically be an instance of `NumPyBackend` or `PyTorchBackend`.

### Valid Call Patterns
```python
from tslearn.backend import Backend, PyTorchBackend, NumPyBackend

# Initialize a Backend wrapper requesting PyTorch
backend_ = Backend("torch")

# Retrieve the specific underlying backend instance
actual_backend = backend_.get_backend()

# Verify the correct backend was retrieved
assert isinstance(actual_backend, PyTorchBackend)

# Switch the backend and retrieve the new instance
backend_.set_backend("numpy")
new_actual_backend = backend_.get_backend()
assert isinstance(new_actual_backend, NumPyBackend)
```

### LLM Instruction Prompt
- When you need to access the specific underlying backend implementation (e.g., `NumPyBackend` or `PyTorchBackend`) from a generic `Backend` wrapper instance, call the `.get_backend()` instance method. Do not attempt to call `get_backend()` as a standalone module-level function.

### Prompt Snippet
```text
To retrieve the specific backend implementation (NumPy or PyTorch) from a `Backend` wrapper in tslearn, call `backend_instance.get_backend()`. This returns the underlying `NumPyBackend` or `PyTorchBackend` object.
```

### Common Failure Modes
- **Calling as a standalone function:** Attempting to call `tslearn.backend.get_backend()` directly will fail with an `AttributeError` or `TypeError` because it is an instance method of the `Backend` class, not a module-level function.
- **Missing PyTorch dependency:** If the `Backend` was initialized with `"torch"` but the `pytorch` package is not installed locally, the underlying backend may silently fall back to NumPy or fail during instantiation, causing `get_backend()` to return a `NumPyBackend` instead of the expected `PyTorchBackend`.

### Fix Code Hint
```python
# WRONG: Calling as a module-level function
# backend_impl = get_backend() 

# RIGHT: Calling as an instance method on a Backend object
from tslearn.backend import Backend
my_backend_wrapper = Backend("numpy")
backend_impl = my_backend_wrapper.get_backend()
```

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

## API Test: `get_config`

### Signature
```python
def get_config(self)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:160  (+1 more definition site/overload)_

### Goal
Returns the configuration dictionary of a custom neural network layer (e.g., `LocalSquaredDistanceLayer` or `GlobalMinPooling1D` used internally by `LearningShapelets`), enabling Keras model serialization and cloning.

### Parameters
- `self`: The instantiated custom Keras layer object within the `tslearn.shapelets` module whose configuration is being retrieved.

### Input
No additional arguments are required. The method relies entirely on the internal state and initialization parameters of the layer instance.

### Output
Returns a `dict` (unspecified in type hints) representing the configuration of the layer, containing key-value pairs of its hyperparameters and settings required by Keras to reconstruct the layer.

### Valid Call Patterns
```python
import tslearn.shapelets

# Inferred from signature: get_config is an instance method of custom Keras layers in tslearn.shapelets.
# We dynamically find a class with this method to demonstrate the call deterministically.
found = False
for name in dir(tslearn.shapelets):
    cls = getattr(tslearn.shapelets, name)
    if isinstance(cls, type) and hasattr(cls, "get_config"):
        try:
            # Attempt to instantiate the layer and get its config
            layer_instance = cls()
            config = layer_instance.get_config()
            assert isinstance(config, dict), "Configuration must be a dictionary."
            print(f"Successfully retrieved config for {name}: {config}")
            found = True
            break
        except TypeError:
            # Skip classes that require mandatory initialization arguments
            continue

if not found:
    print("No zero-argument custom layer found, but get_config exists for Keras serialization.")
```

### LLM Instruction Prompt
- Use `get_config()` strictly when interacting with the internal Keras layers of `tslearn.shapelets` for TensorFlow/Keras serialization workflows. 
- Do NOT call `get_config()` on `tslearn` estimators (like `LearningShapelets` or `TimeSeriesKMeans`); use the scikit-learn standard `get_params()` instead.

### Prompt Snippet
```text
When saving or cloning the underlying Keras model of a `LearningShapelets` estimator, the custom layers (`LocalSquaredDistanceLayer`, `GlobalMinPooling1D`) provide a `get_config()` method to serialize their hyperparameters into a dictionary.
```

### Common Failure Modes
- **Calling on Estimators:** Attempting to call `get_config()` on a scikit-learn compatible estimator (e.g., `LearningShapelets().get_config()`) will raise an `AttributeError`. Estimators use `get_params()`.
- **Unbound Method Call:** Calling `get_config()` directly on the class without instantiating it first will result in a `TypeError` due to the missing `self` argument.

### Fix Code Hint
```python
# WRONG: Attempting to get estimator configuration using Keras conventions
from tslearn.shapelets import LearningShapelets
clf = LearningShapelets(n_shapelets_per_size={3: 1}, max_iter=1)
# config = clf.get_config()  # Raises AttributeError

# CORRECT: Use scikit-learn's get_params() for estimators
config = clf.get_params()

# CORRECT: get_config() is reserved for the internal Keras layers
# layer_config = custom_layer_instance.get_config()
```

## API Test: `get_early_predict_generator`

### Signature
```python
def get_early_predict_generator(self, n_ts=1)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:627_

_Source doc:_ Allows streaming incoming timestamps of a time series and retrieving current predicted class as well as estimated delay before prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- n_ts: int (default 1) The number of time series that will be predicted by the generator Returns ------- generator Use the `send` method of the generator to stream timestamps as they become available and retrieve associated predictions and delays. This method takes an array-like, shape (n_ts, n_timestamps, n_features), representing freshly aquired data for all timeseries as input. This new data is concatenated with previously sent data, if any, to output the predicted classes and estimated delays before optimal prediction timestamps for all timeseries based all on available data (same output as :func:`~early_predict`). Use n_timestamps = 1 for step by step feeding. Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=1000., ...                                  cost_time_parameter=.1, ...                                  random_state=0).fit(dataset, y) >>> incoming_timestamps = np.array([1, 2, 3, 3, 1, 2]).reshape(6, 1, 1, 1) >>> gen = model.get_early_predict_generator() >>> for x in incoming_timestamps: ...     print(gen.send(x)) (array([0]), array([3])) (array([0]), array([2])) (array([0]), array([1])) (array([1]), array([0])) (array([1]), array([0])) (array([1]), array([0]))

### Goal
Creates a Python generator for streaming time-series data step-by-step to a fitted early classifier, yielding the current predicted class and the estimated delay before an optimal prediction can be made.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `n_ts`, default `1`: An integer representing the number of time series that will be concurrently predicted by the generator.

### Input
The caller must first fit an early classifier on a standard 3D `tslearn` dataset `(n_ts, max_sz, d)`. 
Once the generator is created, the caller must feed it using the generator's `.send(x)` method. The input `x` must be an array-like object of shape `(n_ts, n_timestamps, n_features)` representing freshly acquired data. For step-by-step streaming, `n_timestamps` should be `1`.

### Output
Returns `unspecified` — A Python generator object. When `.send(x)` is called, it yields a tuple `(predicted_classes, estimated_delays)`, where both elements are NumPy arrays of shape `(n_ts,)` containing the predictions and the remaining time steps needed before an optimal prediction is reached.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier

# 1. Prepare training data and fit the early classifier
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [3, 2, 1, 1, 2, 3]
])
y = [0, 0, 1, 0]

model = NonMyopicEarlyClassifier(
    n_clusters=2,
    lamb=1000.0,
    cost_time_parameter=0.1,
    random_state=0
)
model.fit(dataset, y)

# 2. Instantiate the generator for 1 time series
gen = model.get_early_predict_generator(n_ts=1)

# 3. Stream incoming timestamps step-by-step
# Shape must be (n_ts=1, n_timestamps=1, n_features=1) for each step
incoming_timestamps = np.array([1, 2, 3]).reshape(3, 1, 1, 1)

results = []
for x in incoming_timestamps:
    preds, delays = gen.send(x)
    results.append((preds[0], delays[0]))

assert len(results) == 3
print("Streaming predictions and delays:", results)
```

### LLM Instruction Prompt
- When using `get_early_predict_generator`, you must interact with the returned object using its `.send(x)` method, not by calling it as a function.
- The input `x` passed to `.send(x)` MUST strictly be a 3D array of shape `(n_ts, n_timestamps, n_features)`. If streaming a single univariate observation, reshape it to `(1, 1, 1)`.
- Ensure the `n_ts` parameter passed to `get_early_predict_generator` exactly matches the first dimension of the arrays you subsequently `.send()`.

### Prompt Snippet
```text
# Create the generator for streaming 2 concurrent time series
gen = early_classifier.get_early_predict_generator(n_ts=2)

# Stream a single new timestamp for both series
# x_new shape: (2, 1, 1) -> (n_ts, n_timestamps, n_features)
preds, delays = gen.send(x_new)
```

### Common Failure Modes
- Passing a 1D or 2D array to `.send(x)`. `tslearn` strictly requires the 3D `(n_ts, n_timestamps, n_features)` format even for single-step updates.
- Mismatching the `n_ts` argument in `get_early_predict_generator(n_ts=...)` with the first dimension of the array passed to `.send()`.
- Attempting to call `get_early_predict_generator` on an estimator that has not yet been fitted with `.fit()`.

### Fix Code Hint
```python
# BAD: Sending a 1D array or scalar to the generator
# gen = model.get_early_predict_generator(n_ts=1)
# preds, delays = gen.send(5.0)

# GOOD: Reshaping the incoming data to the required 3D format
gen = model.get_early_predict_generator(n_ts=1)
x_step = np.array([5.0]).reshape(1, 1, 1) # (n_ts, n_timestamps, n_features)
preds, delays = gen.send(x_step)
```

## API Test: `get_early_predict_proba_generator`

### Signature
```python
def get_early_predict_proba_generator(self, n_ts=1)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:677_

_Source doc:_ Allows streaming incoming timestamps of a time series and retrieving current probability estimates as well as estimated delay before prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- n_ts: int (default 1) The number of time series that will be predicted by the generator Returns ------- generator Use the `send` method of the generator to stream timestamps as they become available and retrieve associated prediction probalities and delays. This method takes an array-like, shape (n_ts, n_timestamps, n_features), representing freshly aquired data for all timeseries as input. This new data is concatenated with previously sent data, if any, to output the predicted probability estimates and estimated delays before optimal prediction timestamps for all timeseries based all on available data (same output as :func:`~early_predict_proba`). Use n_timestamps = 1 for step by step feeding. Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 4, 5, 6], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [1, 2, 3, 3, 2, 1], ...                                   [3, 2, 1, 1, 2, 3], ...                                   [3, 2, 1, 1, 2, 3]]) >>> y = [0, 0, 0, 1, 1, 1, 0, 0] >>> model = NonMyopicEarlyClassifier(n_clusters=3, lamb=1000., ...                                  cost_time_parameter=.1, ...                                  random_state=0).fit(dataset, y) >>> incoming_timestamps = np.array([1, 2, 3, 3, 1, 2]).reshape(6, 1, 1, 1) >>> gen = model.get_early_predict_proba_generator() >>> for x in incoming_timestamps: ...     print(gen.send(x)) (array([[1., 0.]]), array([3])) (array([[1., 0.]]), array([2])) (array([[1., 0.]]), array([1])) (array([[0., 1.]]), array([0])) (array([[0., 1.]]), array([0])) (array([[0., 1.]]), array([0]))

### Goal
Creates a generator that accepts streaming time-series data points and yields current class probability estimates along with the estimated delay before an optimal prediction can be made.

### Parameters
- `self`: A fitted early classification model instance (e.g., `NonMyopicEarlyClassifier`).
- `n_ts`, default `1`: `int`. The number of time series that will be predicted simultaneously by the generator.

### Input
The method itself takes an integer `n_ts`. The returned generator's `.send()` method requires an array-like input of shape `(n_ts, n_timestamps, n_features)` representing freshly acquired data. For step-by-step feeding, `n_timestamps` should be `1`. The model must be fitted before calling this method.

### Output
Returns `generator` — A Python generator object. When fed data via `.send(x)`, it yields a tuple `(probabilities, delays)` where `probabilities` is an array of shape `(n_ts, n_classes)` and `delays` is an array of shape `(n_ts,)` representing the estimated number of time steps to wait before making a prediction.

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
from tslearn.early_classification import NonMyopicEarlyClassifier
import numpy as np

# 1. Prepare training data and fit the early classifier
dataset = to_time_series_dataset([
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 3, 2, 1],
    [1, 2, 3, 3, 2, 1]
])
y = [0, 0, 1, 1]

model = NonMyopicEarlyClassifier(
    n_clusters=2, 
    lamb=1000.0, 
    cost_time_parameter=0.1, 
    random_state=0
)
model.fit(dataset, y)

# 2. Create the generator for 1 time series
gen = model.get_early_predict_proba_generator(n_ts=1)

# 3. Stream 3 timestamps one by one for a single time series
incoming_timestamps = np.array([1, 2, 3]).reshape(3, 1, 1, 1)
for x in incoming_timestamps:
    probas, delays = gen.send(x)
    
    # Assert the output shapes match the expected (n_ts, n_classes) and (n_ts,)
    assert probas.shape == (1, 2)
    assert delays.shape == (1,)

print(f"Final step probabilities: {probas}, delay: {delays}")
```

### LLM Instruction Prompt
- Use `get_early_predict_proba_generator` on a fitted early classifier to stream incoming time-series data.
- Do not pass the time-series data to the method itself; pass the number of time series (`n_ts`).
- Feed new data to the returned generator using its `.send(x)` method.
- Ensure the data `x` sent to the generator is strictly formatted as a 3D array `(n_ts, n_timestamps, n_features)`.

### Prompt Snippet
```text
To stream data for early classification, call `gen = model.get_early_predict_proba_generator(n_ts=1)` on a fitted model. Then, iteratively feed new time steps using `probas, delays = gen.send(x)`, ensuring `x` is a 3D array of shape `(n_ts, n_timestamps, n_features)`.
```

### Common Failure Modes
- Sending data to the generator with a different `n_ts` than what it was initialized with.
- Sending 1D or 2D arrays to the generator instead of the required 3D array `(n_ts, n_timestamps, n_features)`.
- Calling the method on an unfitted early classification model.

### Fix Code Hint
```python
# Ensure the input to .send() is a 3D array matching the initialized n_ts
gen = model.get_early_predict_proba_generator(n_ts=1)

# Reshape a single new measurement to (n_ts=1, n_timestamps=1, n_features=1)
new_data_point = np.array([value]).reshape(1, 1, 1)
probas, delays = gen.send(new_data_point)
```

## API Test: `get_weights`

### Signature
```python
def get_weights(self, layer_name=None)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:828_

_Source doc:_ Return model weights (or weights for a given layer if `layer_name` is provided). Parameters ---------- layer_name: str or None (default: None) Name of the layer for which  weights should be returned. If None, all model weights are returned. Available layer names with weights are: - "shapelets_i_j" with i an integer for the shapelet id and j an integer for the dimension - "classification" for the final classification layer Returns ------- list list of model (or layer) weights Examples -------- >>> from tslearn.generators import random_walk_blobs >>> X, y = random_walk_blobs(n_ts_per_blob=100, sz=256, d=1, n_blobs=3) >>> clf = LearningShapelets(n_shapelets_per_size={10: 5}, max_iter=1, ...                     verbose=0) >>> clf.fit(X, y).get_weights("classification")[0].shape (5, 3) >>> clf.get_weights("shapelets_0")[0].shape (5, 10, 1) >>> len(clf.get_weights("shapelets_0")) 1

### Goal
Retrieve the underlying neural network model weights, or weights for a specific layer, from a fitted `LearningShapelets` estimator.

### Parameters
- `self`: A fitted `tslearn.shapelets.LearningShapelets` estimator instance.
- `layer_name`, default `None`: A `str` specifying the name of the layer to retrieve weights for, or `None` to return all model weights. Valid layer names include `"classification"` for the final classification layer, and `"shapelets_i_j"` (or `"shapelets_i"`) where `i` is the shapelet ID and `j` is the dimension.

### Input
- The `LearningShapelets` estimator must be fitted on a strictly formatted 3D time-series dataset `(n_ts, max_sz, d)` before calling this method.
- `layer_name` must be a valid string corresponding to a layer in the underlying Keras model, or `None`.
- The environment must have `tensorflow` / `keras` installed, as `LearningShapelets` relies on it internally.

### Output
Returns `unspecified` — A `list` of `numpy.ndarray` objects representing the requested model or layer weights.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets import LearningShapelets

# 1. Prepare deterministic 3D time-series data (n_ts, max_sz, d)
X = np.array([[[1.0], [2.0], [3.0], [4.0]], 
              [[1.5], [2.5], [3.5], [4.5]], 
              [[9.0], [8.0], [7.0], [6.0]]])
y = np.array([0, 0, 1])

# 2. Initialize and fit the estimator
clf = LearningShapelets(n_shapelets_per_size={2: 2}, max_iter=1, random_state=42)
clf.fit(X, y)

# 3. Retrieve weights
all_weights = clf.get_weights()
cls_weights = clf.get_weights("classification")
shp_weights = clf.get_weights("shapelets_0")

# 4. Assert properties
assert isinstance(all_weights, list), "Weights should be returned as a list."
assert isinstance(cls_weights, list), "Classification weights should be a list."
assert len(cls_weights) > 0, "Classification weights list should not be empty."

print(f"Retrieved {len(all_weights)} total weight arrays.")
print(f"Classification weights shape: {cls_weights[0].shape}")
```

### LLM Instruction Prompt
- Call `get_weights` only on a `LearningShapelets` instance that has already been fitted with `.fit(X, y)`.
- Pass `layer_name="classification"` to inspect the final classification layer, or `None` to get all weights.
- Ensure the environment has TensorFlow/Keras installed, as `LearningShapelets` relies on it to build the model and store weights.

### Prompt Snippet
```text
tslearn.shapelets.LearningShapelets.get_weights(self, layer_name=None)
Returns a list of numpy arrays representing the underlying Keras model weights.
Requires the estimator to be fitted first. `layer_name` can be "classification", "shapelets_i_j", or None (all weights).
```

### Common Failure Modes
- Calling `get_weights()` before `.fit()` raises an `AttributeError` because the underlying Keras `model_` has not been constructed yet.
- Passing an invalid `layer_name` that does not exist in the Keras model architecture will raise a `ValueError`.
- Failing to install TensorFlow/Keras will cause `LearningShapelets` initialization or fitting to fail before `get_weights` can be called.

### Fix Code Hint
```python
# Ensure the model is fitted before extracting weights
clf = LearningShapelets(n_shapelets_per_size={3: 2}, max_iter=10)
clf.fit(X_train, y_train)  # Required before get_weights
classification_weights = clf.get_weights("classification")
```

## API Test: `grabocka_params_to_shapelet_size_dict`

### Signature
```python
def grabocka_params_to_shapelet_size_dict(n_ts, ts_sz, n_classes, l, r)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:235_

### Goal
Computes the optimal number and lengths of shapelets to extract for a time-series dataset using the heuristic proposed by Grabocka et al. (2014).

### Parameters
- `n_ts`: `unspecified` — Number of time series in the dataset (expected to be an `int`).
- `ts_sz`: `unspecified` — Length of the time series in the dataset (expected to be an `int`).
- `n_classes`: `unspecified` — Number of distinct classes in the dataset (expected to be an `int`).
- `l`: `unspecified` — Fraction of the time series length to be used for the base (minimum) shapelet length (expected to be a `float` between 0.0 and 1.0).
- `r`: `unspecified` — Number of different shapelet lengths to use, scaling up from the base length (expected to be an `int`).

### Input
Scalar integers and floats describing the dimensions and class count of a time-series dataset, along with hyperparameters `l` and `r` for the Grabocka heuristic. The dataset dimensions (`n_ts`, `ts_sz`) typically correspond to the shape of the 3D `(n_ts, max_sz, d)` array required by `tslearn` estimators.

### Output
Returns `unspecified` — A dictionary where each key is an integer representing a shapelet length, and the corresponding value is an integer representing the number of shapelets to generate of that length.

### Valid Call Patterns
```python
from tslearn.shapelets import grabocka_params_to_shapelet_size_dict

# Compute shapelet sizes for a dataset with 100 series, length 100, and 3 classes
# using a base length of 10% (0.1) and 2 different length scales.
shapelet_dict = grabocka_params_to_shapelet_size_dict(
    n_ts=100, 
    ts_sz=100, 
    n_classes=3, 
    l=0.1, 
    r=2
)

# The heuristic generates lengths 10 and 20, with 4 shapelets each
keys = sorted(shapelet_dict.keys())
assert keys == [10, 20], f"Expected lengths [10, 20], got {keys}"
assert shapelet_dict[10] == 4, f"Expected 4 shapelets of length 10, got {shapelet_dict[10]}"
assert shapelet_dict[20] == 4, f"Expected 4 shapelets of length 20, got {shapelet_dict[20]}"

print(f"Generated shapelet size dictionary: {shapelet_dict}")
```

### LLM Instruction Prompt
- When configuring the `shapelet_sizes` parameter for `tslearn.shapelets.LearningShapelets`, do not guess arbitrary dictionary values. Instead, use `grabocka_params_to_shapelet_size_dict(n_ts, ts_sz, n_classes, l, r)` to heuristically compute the optimal shapelet lengths and counts based on the dataset's shape and number of classes.

### Prompt Snippet
```text
Use `grabocka_params_to_shapelet_size_dict` to dynamically configure `LearningShapelets`. Pass the dataset's number of samples (`n_ts`), sequence length (`ts_sz`), and unique class count (`n_classes`), along with heuristic parameters `l` (e.g., 0.1) and `r` (e.g., 2). Pass the resulting dictionary directly to the `shapelet_sizes` argument of the estimator.
```

### Common Failure Modes
- Passing floating-point numbers for `n_ts`, `ts_sz`, `n_classes`, or `r`, which may cause type errors when the heuristic attempts to use them as counts or sequence lengths.
- Providing a fraction `l` that is too small or too large, resulting in a base shapelet length of `0` or a length that exceeds the total time-series length `ts_sz`.
- Failing to extract the dataset dimensions correctly from the strict `(n_ts, max_sz, d)` 3D array format before passing them to this function.

### Fix Code Hint
```python
# Ensure inputs are properly cast to integers where required
n_ts, ts_sz, _ = X_train.shape
n_classes = len(set(y_train))

shapelet_sizes = grabocka_params_to_shapelet_size_dict(
    n_ts=int(n_ts),
    ts_sz=int(ts_sz),
    n_classes=int(n_classes),
    l=0.1,
    r=2
)
```

## API Test: `grad`

### Signature
```python
def grad(self)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1137_

_Source doc:_ Compute gradient of soft-DTW w.r.t. D by dynamic programming. Returns ------- grad: array-like, shape=(m, n) Gradient w.r.t. D.

### Goal
Compute the gradient of the Soft-DTW alignment cost with respect to the pairwise distance matrix `D` using a dynamic programming backward pass.

### Parameters
- `self`: An instance of the `SoftDTW` class (e.g., `tslearn.metrics.softdtw_variants.SoftDTW`) that has been initialized with a distance matrix `D` and has already completed its forward pass.

### Input
The method takes no arguments. It strictly requires that the parent object was initialized with an `(m, n)` distance matrix `D` and that the `compute()` method has been called beforehand to populate the internal dynamic programming cost matrices.

### Output
Returns `unspecified` (documented as an `array-like` of shape `(m, n)`) — A NumPy array representing the gradient of the Soft-DTW loss with respect to the input distance matrix `D`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.softdtw_variants import SoftDTW

# 1. Define a pairwise distance matrix D of shape (m, n)
D = np.array([
    [0.0, 1.0, 4.0],
    [1.0, 0.0, 1.0],
    [4.0, 1.0, 0.0]
])

# 2. Instantiate the SoftDTW object (inferred from signature and source file)
sdtw = SoftDTW(D, gamma=1.0)

# 3. Perform the forward pass (required before backward pass)
cost = sdtw.compute()

# 4. Compute the gradient w.r.t. D
gradient = sdtw.grad()

assert gradient.shape == D.shape
assert isinstance(gradient, np.ndarray)
print(f"Gradient w.r.t D:\n{gradient}")
```

### LLM Instruction Prompt
- Call `grad()` only on an instantiated `SoftDTW` object after `compute()` has been executed.
- Do not pass any arguments to `grad()`.
- Recognize that this method computes the gradient with respect to the distance matrix `D`, not the original time series. For end-to-end gradients w.r.t time series, use the PyTorch backend via `tslearn.metrics.soft_dtw(..., compute_with_backend=True)` and `.backward()`.

### Prompt Snippet
```text
# Compute the gradient of Soft-DTW w.r.t the distance matrix D
sdtw = SoftDTW(D, gamma=1.0)
sdtw.compute()
grad_D = sdtw.grad()
```

### Common Failure Modes
- **Calling before `compute()`**: Invoking `grad()` before `compute()` will fail because the internal dynamic programming matrices (forward pass) have not been initialized.
- **Passing arguments**: Providing arguments to `grad()` will raise a `TypeError` since it only accepts `self`.
- **Misinterpreting the gradient target**: Assuming `grad()` returns the gradient w.r.t the raw time series instead of the pairwise distance matrix `D`.

### Fix Code Hint
```python
# WRONG: Calling grad() without compute() or passing arguments
sdtw = SoftDTW(D, gamma=1.0)
grad_D = sdtw.grad(D)

# CORRECT: Call compute() first, then grad() with no arguments
sdtw = SoftDTW(D, gamma=1.0)
sdtw.compute()
grad_D = sdtw.grad()
```

## API Test: `in_file_string_replace`

### Signature
```python
def in_file_string_replace(filename, old_string, new_string)
```
_Source: tslearn/tslearn/datasets/datasets.py:57_

_Source doc:_ String replacement within a text file. It is used to fix typos in downloaded csv file. The code was modified from "https://stackoverflow.com/questions/4128144/" Parameters ---------- filename : str Path to the file where strings should be replaced old_string : str The string to be replaced in the file. new_string : str The new string that will replace old_string

### Goal
Perform an in-place string replacement within a text file, typically used as an internal utility to fix typos in downloaded time-series CSV datasets.

### Parameters
- `filename`: `str` — Path to the file where strings should be replaced.
- `old_string`: `str` — The exact string to be found and replaced in the file.
- `new_string`: `str` — The new string that will replace all occurrences of `old_string`.

### Input
A valid path to an existing, writable text file on disk. The file must be readable and writable by the current process.

### Output
Returns `None` — the file is modified in-place on disk.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.datasets.datasets import in_file_string_replace

# Create a temporary text file with a typo
fd, temp_path = tempfile.mkstemp(text=True)
with os.fdopen(fd, 'w') as f:
    f.write("1.0, 2.0, typo, 4.0\n")

# Inferred call from signature (no verbatim example provided)
in_file_string_replace(temp_path, "typo", "3.0")

# Verify the replacement
with open(temp_path, 'r') as f:
    content = f.read()
    assert "3.0" in content, "New string not found in file"
    assert "typo" not in content, "Old string was not replaced"
    print("Replacement successful.")

os.remove(temp_path)
```

### LLM Instruction Prompt
- Use `in_file_string_replace` to perform in-place string replacements in text files, such as fixing formatting issues or typos in downloaded CSV datasets before parsing them into 3D arrays.
- Ensure the file exists and is writable before calling.
- Note that this function modifies the file on disk and returns `None`.

### Prompt Snippet
```text
Use `tslearn.datasets.datasets.in_file_string_replace(filename, old_string, new_string)` to perform in-place string replacements in text files. Note that this modifies the file on disk and returns `None`.
```

### Common Failure Modes
- `FileNotFoundError`: The provided `filename` does not exist.
- `PermissionError`: The file is read-only or the process lacks write permissions.
- Encoding errors: If the file contains non-text data or uses an encoding incompatible with the default text reader.

### Fix Code Hint
```python
import os
from tslearn.datasets.datasets import in_file_string_replace

if os.path.exists(filepath) and os.access(filepath, os.W_OK):
    in_file_string_replace(filepath, "old_val", "new_val")
```

## API Test: `instantiate_backend`

### Signature
```python
def instantiate_backend(*args)
```
_Source: tslearn/tslearn/backend/backend.py:7_

_Source doc:_ Select backend. Parameter --------- *args : Input arguments can be Backend instance or string or array or None Arguments used to define the backend instance. Returns ------- backend : Backend instance The backend instance.

### Goal
Dynamically select and initialize the appropriate computational backend (NumPy or PyTorch) by evaluating the provided hints in order.

### Parameters
- `*args`: Variable length argument list containing hints to define the backend. Valid hints include an existing `Backend` instance, a string (e.g., `"numpy"`, `"pytorch"`), a data array/tensor, or `None`.

### Input
One or more positional arguments representing backend hints. The function iterates through the arguments from left to right and stops at the first recognized hint. If no valid backend is specified or detected, the environment defaults to using NumPy.

### Output
Returns `unspecified` — A `Backend` instance (e.g., `NumPyBackend` or `PyTorchBackend`) that provides unified array operations and properties (like `.backend_string` and `.is_numpy`) for the selected framework.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Instantiate using an explicit string hint
np_backend = instantiate_backend("numpy")
assert np_backend.backend_string == "numpy"
assert np_backend.is_numpy is True

# Instantiate using a data array hint
data = np.array([1.0, 2.0, 3.0])
data_backend = instantiate_backend(data)
assert data_backend.backend_string == "numpy"

# Fallback behavior (evaluates left-to-right; unrecognized inputs fall through)
fallback_backend = instantiate_backend(None, "unrecognized_string", data)
assert fallback_backend.backend_string == "numpy"
```

### LLM Instruction Prompt
- Use `instantiate_backend(*args)` to dynamically resolve the backend for metric computations or custom time-series operations.
- Pass the data arrays/tensors or explicit strings (`"numpy"`, `"pytorch"`) as arguments.
- Remember that the function evaluates arguments from left to right and returns the first successfully resolved backend. Always place your highest-priority hints (like the input data itself) first, and fallback defaults last.
- If PyTorch is requested via a tensor or `"pytorch"` string, the local environment must have `pytorch` installed.

### Prompt Snippet
```text
# Resolve backend based on input data type, falling back to a default string
backend = instantiate_backend(input_time_series, "numpy")
is_pytorch = (backend.backend_string == "pytorch")
```

### Common Failure Modes
- **Expecting a string return:** Callers might expect `instantiate_backend` to return a string identifier, but it returns a full `Backend` object instance. You must use `backend.backend_string` to get the name, or use the object's methods (e.g., `backend.array()`).
- **Incorrect argument order:** Placing a default string like `"numpy"` before a tensor in the arguments (e.g., `instantiate_backend("numpy", my_tensor)`) will short-circuit the evaluation, causing it to ignore the tensor and incorrectly return the NumPy backend.
- **Missing PyTorch dependency:** Passing `"pytorch"` or a `torch.Tensor` in an environment where the `pytorch` package is not installed will cause backend instantiation to fail or fallback unexpectedly.

### Fix Code Hint
```python
# WRONG: Returns a Backend object, not a string, and order prevents tensor detection
be_name = instantiate_backend("numpy", my_tensor)
if be_name == "pytorch": ...

# RIGHT: Pass the tensor first to auto-detect, and access the backend_string property
backend = instantiate_backend(my_tensor, "numpy")
if backend.backend_string == "pytorch": ...
```

## API Test: `intercept_`

### Signature
```python
def intercept_(self)
```
_Source: tslearn/tslearn/svm/svm.py:39_

### Goal
Returns the constants (intercepts) in the decision function of a fitted time-series Support Vector Machine (SVM) estimator.

### Parameters
- `self`: A fitted instance of a `tslearn` SVM estimator (such as `TimeSeriesSVC` or `TimeSeriesSVR`).

### Input
The estimator must first be fitted using `.fit(X, y)`, where `X` is a strictly formatted 3D `numpy` array of shape `(n_ts, max_sz, d)` representing the time-series dataset, and `y` contains the target labels or values.

### Output
Returns `unspecified` — typically a `numpy` array of shape `(n_classes * (n_classes - 1) / 2,)` for classification or `(1,)` for regression, representing the constants in the decision function delegated from the underlying `scikit-learn` model.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data
X = to_time_series_dataset([[1.0, 2.0], [1.0, 2.0], [8.0, 9.0], [8.0, 9.0]])
y = [0, 0, 1, 1]

# 2. Initialize and fit the SVM estimator
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)

# 3. Access the intercept_ property (inferred from scikit-learn conventions)
intercept = clf.intercept_

assert isinstance(intercept, np.ndarray)
print(f"Intercept: {intercept}")
```

### LLM Instruction Prompt
- Access `intercept_` as a property on a `tslearn.svm` estimator (like `TimeSeriesSVC` or `TimeSeriesSVR`) to retrieve the decision function constants.
- You MUST ensure the estimator has been successfully fitted with `.fit(X, y)` before accessing this property.
- The input `X` to the `.fit()` method must be a 3D array of shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
To retrieve the decision function constants from a trained time-series SVM, access the `intercept_` property on the fitted `TimeSeriesSVC` or `TimeSeriesSVR` object. Ensure the model is fitted on a 3D array `(n_ts, max_sz, d)` first.
```

### Common Failure Modes
- **`NotFittedError` or `AttributeError`**: Attempting to access `intercept_` before calling `.fit()` on the estimator.
- **Dimensionality Error during Fit**: Passing a 2D array to `.fit()` instead of the required 3D `(n_ts, max_sz, d)` format, causing the fit to fail before the intercept can be accessed.
- **Calling as a Method**: Using `clf.intercept_()` instead of accessing it as a property `clf.intercept_`, resulting in a `TypeError: 'numpy.ndarray' object is not callable`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset

# Convert raw data to the required 3D format
X_3d = to_time_series_dataset(X_raw)

# Fit the model before accessing the property
clf.fit(X_3d, y)

# Access as a property, not a method
model_intercept = clf.intercept_
```

## API Test: `inv_transform_1d_sax`

### Signature
```python
def inv_transform_1d_sax(dataset_sax, breakpoints_avg_middle_, breakpoints_slope_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:189_

_Source doc:_ Compute time series corresponding to given 1d-SAX representations. Parameters ---------- dataset_sax : array-like, shape=(n_ts, sz, 2 * d), dtype=float64 (Linux and MacOS) or float32 (Windows) A dataset of SAX series. breakpoints_avg_middle_ : array-like, ndim=1, dtype=float64 breakpoints_slope_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dataset_out : array-like, shape=(n_ts, original_size, d), dtype=float64 A dataset of time series corresponding to the provided representation.

### Goal
Computes the inverse transformation of a 1d-SAX (1D Symbolic Aggregate approXimation) representation to reconstruct an approximation of the original time series using segment averages and slopes.

### Parameters
- `dataset_sax`: Array-like of shape `(n_ts, sz, 2 * d)`. The 1d-SAX representation of the dataset, where each segment contains both an average symbol and a slope symbol (hence `2 * d` features per segment).
- `breakpoints_avg_middle_`: 1D array-like of `float64`. The middle values of the bins used for the average breakpoints, used to map average symbols back to continuous values.
- `breakpoints_slope_middle_`: 1D array-like of `float64`. The middle values of the bins used for the slope breakpoints, used to map slope symbols back to continuous slopes.
- `original_size`: Integer (`int64` or `int32` depending on OS). The length of the original time series before it was reduced to `sz` segments.

### Input
The caller must provide a strictly 3D NumPy array for `dataset_sax` containing the SAX symbols (represented as floats), two 1D NumPy arrays containing the precomputed middle values of the SAX bins, and the target integer length of the reconstructed time series. 

### Output
Returns `array-like` — A 3D NumPy array of shape `(n_ts, original_size, d)` and dtype `float64` representing the reconstructed time series approximations.

### Valid Call Patterns
```python
import numpy as np
# Inferred from signature and source path (tslearn/tslearn/metrics/cysax.py)
from tslearn.metrics.cysax import inv_transform_1d_sax

# 1 time series, 2 segments, d=1 (so 2*d = 2 features per segment: avg and slope)
# Symbols are represented as float indices
dataset_sax = np.array([[[0.0, 0.0], [1.0, 1.0]]], dtype=np.float64)

# Middle values for the bins (e.g., from a fitted OneD_SymbolicAggregateApproximation)
breakpoints_avg_middle = np.array([0.25, 0.75], dtype=np.float64)
breakpoints_slope_middle = np.array([-0.1, 0.1], dtype=np.float64)

# Target original length
original_size = 4

reconstructed = inv_transform_1d_sax(
    dataset_sax,
    breakpoints_avg_middle,
    breakpoints_slope_middle,
    original_size
)

assert reconstructed.shape == (1, 4, 1)
print(reconstructed)
```

### LLM Instruction Prompt
- Use `inv_transform_1d_sax` to reconstruct time series from 1d-SAX representations.
- Ensure `dataset_sax` strictly follows the 3D shape `(n_ts, sz, 2 * d)`. The last dimension must be exactly twice the original dimensionality `d` because 1d-SAX stores both an average and a slope symbol for each segment.
- Provide the middle values of the breakpoints for both averages and slopes as 1D `float64` arrays.
- Pass the desired `original_size` as an integer.

### Prompt Snippet
```text
When reconstructing 1d-SAX representations in tslearn, use `tslearn.metrics.cysax.inv_transform_1d_sax`. Ensure the input SAX dataset is a 3D array of shape `(n_ts, sz, 2 * d)` and provide the 1D arrays for `breakpoints_avg_middle_` and `breakpoints_slope_middle_`.
```

### Common Failure Modes
- **Incorrect Last Dimension:** Passing a `dataset_sax` array where the last dimension is `d` instead of `2 * d`. 1d-SAX requires two values (average and slope) per original dimension.
- **Dimensionality Mismatch:** Passing a 2D array for `dataset_sax`. `tslearn` strictly requires the `(n_ts, sz, 2 * d)` 3D format.
- **Type Errors:** Passing integer arrays for `dataset_sax` on platforms where the Cython backend strictly expects `float64` (Linux/macOS) or `float32` (Windows). Always cast the SAX dataset to the appropriate float type before calling this low-level helper.

### Fix Code Hint
```python
# FIX: Ensure dataset_sax is 3D and cast to float64
dataset_sax = np.asarray(dataset_sax, dtype=np.float64)
if dataset_sax.ndim == 2:
    # Reshape (n_ts, sz * 2 * d) to (n_ts, sz, 2 * d) if flattened
    dataset_sax = dataset_sax.reshape(dataset_sax.shape[0], -1, 2 * d)

reconstructed = inv_transform_1d_sax(
    dataset_sax, 
    breakpoints_avg_middle, 
    breakpoints_slope_middle, 
    original_size
)
```

## API Test: `inv_transform_paa`

### Signature
```python
def inv_transform_paa(dataset_paa, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:11_

_Source doc:_ Compute time series corresponding to given PAA representations. Parameters ---------- dataset_paa : array-like, shape=(n_ts, sz, d), dtype=float64 A dataset of PAA series. original_size : int32 Length of the original time series. Returns ------- dataset_out : array-like, shape=(n_ts, original_size, d), dtype=float64 A dataset of time series corresponding to the provided representation.

### Goal
Compute the inverse Piecewise Aggregate Approximation (PAA) transform, reconstructing a time-series dataset of the original length from its compressed PAA representation.

### Parameters
- `dataset_paa`: A 3D array-like of shape `(n_ts, sz, d)` containing the PAA representations of the time series.
- `original_size`: An integer representing the target length of the reconstructed time series (the length before the PAA transform was applied).

### Input
- `dataset_paa` must be formatted as a strict 3D array `(n_ts, sz, d)`. If you have 1D or 2D data, it must be reshaped or converted using `tslearn.utils.to_time_series_dataset` prior to calling this function.
- `original_size` must be an integer greater than or equal to `sz`.

### Output
Returns `unspecified` — A 3D `numpy` array of shape `(n_ts, original_size, d)` and dtype `float64` containing the reconstructed time series, where each PAA segment's value is repeated to fill its corresponding original time steps.

### Valid Call Patterns
```python
from tslearn.metrics.cysax import inv_transform_paa
import numpy as np

# Inferred from signature (no existing test or verbatim example found)
# 1 time series, PAA size 2, 1 dimension
dataset_paa = np.array([[[0.5], [1.5]]])
original_size = 4

# Reconstruct to original size 4
dataset_out = inv_transform_paa(dataset_paa, original_size)

assert dataset_out.shape == (1, 4, 1)
print("Reconstructed PAA:\n", dataset_out)
```

### LLM Instruction Prompt
- Use `inv_transform_paa` to reconstruct a time-series dataset to its original length from a PAA representation.
- Ensure `dataset_paa` is a 3D array of shape `(n_ts, sz, d)`.
- Provide `original_size` as an integer representing the target length of the reconstructed time series.

### Prompt Snippet
```text
When reconstructing a time series from its Piecewise Aggregate Approximation (PAA), use `tslearn.metrics.cysax.inv_transform_paa(dataset_paa, original_size)`. The input `dataset_paa` must be a 3D array `(n_ts, sz, d)`, and `original_size` must be an integer. The output will be a 3D array of shape `(n_ts, original_size, d)`.
```

### Common Failure Modes
- Passing a 1D or 2D array for `dataset_paa` instead of the required 3D `(n_ts, sz, d)` format, which will cause shape mismatch errors.
- Providing an `original_size` that is not an integer, leading to type errors during array allocation.
- Providing an `original_size` smaller than the PAA size (`sz`), which is mathematically invalid for an inverse transform.

### Fix Code Hint
```python
import numpy as np
from tslearn.utils import to_time_series_dataset

# Ensure dataset_paa is strictly 3D (n_ts, sz, d)
dataset_paa_3d = to_time_series_dataset(dataset_paa)

# Ensure original_size is an integer
dataset_out = inv_transform_paa(dataset_paa_3d, int(original_size))
```

## API Test: `inv_transform_sax`

### Signature
```python
def inv_transform_sax(dataset_sax, breakpoints_middle_, original_size)
```
_Source: tslearn/tslearn/metrics/cysax.py:78_

_Source doc:_ Compute time series corresponding to given SAX representations. Parameters ---------- dataset_sax : array-like, shape=(n_ts, sz, d), dtype=float64 (Linux and MacOS) or float32 (Windows) A dataset of SAX series. breakpoints_middle_ : array-like, ndim=1, dtype=float64 original_size : int64 (Linux and MacOS) or int32 (Windows) Length of the original time series. Returns ------- dataset_out : array-like, shape=(n_ts, original_size, d), dtype=float64

### Goal
Computes the inverse transformation of a Symbolic Aggregate approXimation (SAX) representation, reconstructing a continuous time-series dataset of the original length from the discrete SAX symbols.

### Parameters
- `dataset_sax`: A 3D array-like of shape `(n_ts, sz, d)` containing the SAX representations of the time series (typically bin indices represented as floats).
- `breakpoints_middle_`: A 1D array-like of `float64` representing the middle values of the SAX bins, used to map the discrete symbols back to continuous values.
- `original_size`: An integer specifying the length of the original time series before it was reduced to length `sz`.

### Input
- `dataset_sax` must be a 3D numpy array of shape `(n_ts, sz, d)`. Due to Cython bindings, it expects `float64` on Linux/macOS and `float32` on Windows.
- `breakpoints_middle_` must be a 1D numpy array of `float64`.
- `original_size` must be an integer (`int64` on Linux/macOS, `int32` on Windows).

### Output
Returns `dataset_out` — A 3D numpy array of shape `(n_ts, original_size, d)` and dtype `float64` containing the reconstructed time series, where the SAX values are mapped to their bin centers and repeated to match the `original_size`.

### Valid Call Patterns
```python
import sys
import numpy as np
from tslearn.metrics.cysax import inv_transform_sax

# Platform-specific types for Cython memoryviews
float_type = np.float32 if sys.platform == "win32" else np.float64
int_type = np.int32 if sys.platform == "win32" else np.int64

# 1 time series, SAX size 3, 1 dimension
dataset_sax = np.array([[[0.0], [1.0], [2.0]]], dtype=float_type)
# 3 bins, so 3 middle breakpoints
breakpoints_middle = np.array([-0.5, 0.0, 0.5], dtype=np.float64)
original_size = int_type(6)

# Inferred from signature
dataset_out = inv_transform_sax(dataset_sax, breakpoints_middle, original_size)

assert dataset_out.shape == (1, 6, 1)
print("Reconstructed shape:", dataset_out.shape)
```

### LLM Instruction Prompt
- Always import `inv_transform_sax` from `tslearn.metrics.cysax`.
- Ensure `dataset_sax` is strictly a 3D array `(n_ts, sz, d)`. If you have 2D data, use `np.expand_dims` to add the feature dimension.
- Be mindful of the Cython dtype constraints: `dataset_sax` expects `float64` on Linux/macOS and `float32` on Windows. `original_size` expects `int64` on Linux/macOS and `int32` on Windows.
- `breakpoints_middle_` must be a 1D array of `float64`.

### Prompt Snippet
```text
When calling `inv_transform_sax`, ensure the input `dataset_sax` is a 3D array of shape `(n_ts, sz, d)`. The function requires `breakpoints_middle_` as a 1D array to map SAX indices back to continuous values, and `original_size` to determine the length of the output time series. Account for platform-specific Cython types (float32/int32 on Windows, float64/int64 elsewhere).
```

### Common Failure Modes
- **Dimensionality Error**: Passing a 2D array `(n_ts, sz)` for `dataset_sax` instead of the required 3D array `(n_ts, sz, d)`.
- **Cython Type Error**: Passing integers or the wrong float precision for `dataset_sax` or `original_size`, which can cause a Cython memoryview `ValueError` on different operating systems.
- **Shape Mismatch**: Providing a `breakpoints_middle_` array that is not 1D.

### Fix Code Hint
```python
import sys
import numpy as np

# Adjust dtype based on platform to satisfy Cython memoryviews
float_type = np.float32 if sys.platform == "win32" else np.float64
int_type = np.int32 if sys.platform == "win32" else np.int64

dataset_sax = np.asarray(dataset_sax, dtype=float_type)
if dataset_sax.ndim == 2:
    dataset_sax = np.expand_dims(dataset_sax, axis=-1)

breakpoints_middle = np.asarray(breakpoints_middle, dtype=np.float64)
original_size = int_type(original_size)
```

## API Test: `inverse_transform`

### Signature
```python
def inverse_transform(self, X)
```
_Source: tslearn/tslearn/piecewise/piecewise.py:242  (+2 more definition site/overload)_

_Source doc:_ Compute time series corresponding to given PAA representations. Parameters ---------- X : array-like of shape (n_ts, sz_paa, d) A dataset of PAA series. Returns ------- numpy.ndarray of shape (n_ts, sz_original_ts, d) A dataset of time series corresponding to the provided representation.

### Goal
Reconstruct a time-series dataset in its original dimensionality from its Piecewise Aggregate Approximation (PAA) or similar piecewise representation.

### Parameters
- `self`: A fitted instance of a piecewise transformer (e.g., `tslearn.piecewise.PAA`).
- `X`: An array-like dataset of piecewise representations of shape `(n_ts, sz_paa, d)`.

### Input
A 3D array-like of shape `(n_ts, sz_paa, d)` representing the compressed time series. The transformer instance must have been previously fitted on the original time series so it knows `sz_original_ts` (the original number of time steps).

### Output
Returns `numpy.ndarray` — A 3D array of shape `(n_ts, sz_original_ts, d)` representing the reconstructed time series, where each segment's compressed value is repeated to match the original time-series length.

### Valid Call Patterns
```python
import numpy as np
from tslearn.piecewise import PAA

# 1 time series, 4 time steps, 1 dimension
X_original = np.array([[[1.0], [2.0], [3.0], [4.0]]])
paa = PAA(n_segments=2)
X_paa = paa.fit_transform(X_original)

# Inferred from signature and docstring
X_reconstructed = paa.inverse_transform(X_paa)

assert X_reconstructed.shape == (1, 4, 1)
assert np.allclose(X_reconstructed[0, 0, 0], 1.5)  # Average of 1.0 and 2.0
print("Inverse transform successful, shape:", X_reconstructed.shape)
```

### LLM Instruction Prompt
- Call `inverse_transform` on a fitted piecewise transformer instance (like `PAA`).
- Ensure the input `X` is strictly a 3D array of shape `(n_ts, sz_paa, d)`.
- Do not call this method on an unfitted transformer, as it requires the original time series length (`sz_original_ts`) to reconstruct the array properly.

### Prompt Snippet
```text
When reconstructing time series from PAA representations using `inverse_transform`, ensure the input is a 3D array of shape `(n_ts, sz_paa, d)` and the transformer instance has already been fitted to learn the original time series length.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D array `(n_ts, sz_paa, d)`.
- Calling `inverse_transform` on an unfitted transformer, resulting in an error because `sz_original_ts` is unknown.
- Passing an array with a different number of segments (`sz_paa`) than what the transformer was configured for (`n_segments`).

### Fix Code Hint
```python
# Ensure input is 3D and the transformer is fitted
from tslearn.utils import to_time_series_dataset

X_paa_3d = to_time_series_dataset(X_paa)
X_reconstructed = paa.inverse_transform(X_paa_3d)
```

## API Test: `is_array`

### Signature
```python
def is_array(x)
```
_Source: tslearn/tslearn/backend/numpy_backend.py:102_

### Goal
Evaluates whether a given input object is recognized as a valid array type by the NumPy backend.

### Parameters
- `x`: The input object (e.g., a time-series dataset, list, or tensor) to be evaluated.

### Input
Any Python object. In the context of `tslearn`, this is typically a time-series dataset, a standard Python list, a NumPy array, or a PyTorch tensor being checked for compatibility with the active backend before metric computation.

### Output
Returns `unspecified` — A boolean value indicating whether the input `x` is recognized as an array (specifically a `numpy.ndarray`) by the NumPy backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# The example is inferred from the signature (not verified).
# Backends are dynamically instantiated; is_array is typically accessed via the backend instance.
be = instantiate_backend("numpy")
x = np.array([1.0, 2.0, 3.0])

result = be.is_array(x)
assert result is True, "NumPy array should be recognized as an array by the NumPy backend"
print(f"Correctness witness: {result}")
```

### LLM Instruction Prompt
- Use `is_array` via an instantiated backend object (e.g., `be = instantiate_backend("numpy")`) to verify if a variable matches the backend's expected array type before passing it to low-level metric functions.
- Do not assume standard Python lists will pass this check; `tslearn` strictly expects time-series datasets to be formatted as 3D `numpy` arrays or compatible backend tensors.

### Prompt Snippet
```text
Verify array compatibility using the backend's `is_array` method to ensure the input is a valid NumPy array before performing manual metric alignments.
```

### Common Failure Modes
- **Type Mismatch:** Passing a standard Python list (e.g., `[1, 2, 3]`) or a PyTorch tensor to the NumPy backend's `is_array` method will likely return `False`. Data must be converted using `tslearn.utils.to_time_series_dataset` or `numpy.array` first.
- **Missing Backend Instantiation:** Attempting to call `is_array` as a bare module-level function without routing it through the dynamically selected backend instance (via `instantiate_backend`).

### Fix Code Hint
```python
import numpy as np
from tslearn.backend import instantiate_backend
from tslearn.utils import to_time_series_dataset

be = instantiate_backend("numpy")
raw_data = [[1, 2, 3], [4, 5, 6]]

# FIX: Convert raw lists to the strict 3D numpy array format expected by tslearn
formatted_X = to_time_series_dataset(raw_data)

if not be.is_array(formatted_X):
    formatted_X = np.array(formatted_X)
```

## API Test: `is_float`

### Signature
```python
def is_float(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:159  (+1 more definition site/overload)_

### Goal
Checks whether a given scalar, array, or tensor represents a floating-point data type within the currently instantiated computational backend (NumPy or PyTorch).

### Parameters
- `x`: The value, array, or tensor to be evaluated.

### Input
A scalar, NumPy array, or PyTorch tensor. The caller must first instantiate a backend object using `tslearn.backend.instantiate_backend` before calling this method on that instance.

### Output
Returns `unspecified` — Evaluates to a boolean (`True` or `False`) indicating whether the input `x` is recognized as a floating-point type by the specific backend implementation.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend
import numpy as np

# Instantiate the NumPy backend
backend = instantiate_backend("numpy")

# Create a float value (e.g., simulating a distance metric output)
distance_val = np.float64(3.14)

# Check if it is a float using the backend helper
result = backend.is_float(distance_val)

print(f"Correctness witness: {result}")
assert result is True, "Expected the backend to identify np.float64 as a float."
```

### LLM Instruction Prompt
- Do NOT call `is_float` as a top-level function from `tslearn`. It is a method on a backend instance. You must first obtain a backend using `tslearn.backend.instantiate_backend(...)` and then call `backend.is_float(x)`.
- Use this method when writing backend-agnostic code (e.g., custom metrics) to verify that distance or alignment outputs are floating-point numbers before proceeding with operations that require continuous values.

### Prompt Snippet
```text
When verifying data types in a backend-agnostic time-series metric, instantiate the backend and use its `is_float` method. Do not use `isinstance(x, float)` as it will fail on PyTorch tensors and NumPy arrays.

```python
backend = instantiate_backend(be, array_type)
assert backend.is_float(dtw_sakoe)
```
```

### Common Failure Modes
- **AttributeError (Missing Receiver):** Attempting to call `tslearn.is_float(x)` or `tslearn.backend.is_float(x)` directly will fail. It must be called on an instantiated backend object.
- **Cross-Backend Type Mismatch:** Passing a PyTorch tensor to a NumPy backend's `is_float` method (or vice versa) may yield unexpected results or errors. Ensure the backend matches the data type of `x`.

### Fix Code Hint
```python
# BAD: Calling as a standalone function
# import tslearn
# result = tslearn.is_float(my_val)

# GOOD: Calling on an instantiated backend
from tslearn.backend import instantiate_backend
backend = instantiate_backend("numpy") # or "pytorch", or pass the array itself
result = backend.is_float(my_val)
```

## API Test: `is_float32`

### Signature
```python
def is_float32(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:165  (+1 more definition site/overload)_

### Goal
Determines whether the provided time-series array or tensor has a 32-bit floating-point data type, abstracting over NumPy and PyTorch backend differences.

### Parameters
- `x`: The input time-series data (NumPy array or PyTorch tensor) whose data type is to be checked.

### Input
A NumPy array or PyTorch tensor. The input must expose a `dtype` attribute compatible with the active backend. Native Python lists are not supported and must be converted first.

### Output
Returns `unspecified` — A boolean (`True` or `False`) indicating if the data type of `x` is exactly `float32` (e.g., `numpy.float32` or `torch.float32`).

### Valid Call Patterns
```python
import numpy as np
import torch
from tslearn.backend import instantiate_backend

# Note: The example is inferred from the signature and backend conventions.
# Instantiate the NumPy backend
be_np = instantiate_backend("numpy")

# Check a float32 NumPy array
x_np_32 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
is_np_32 = be_np.is_float32(x_np_32)
assert is_np_32 is True
print(f"NumPy float32 check: {is_np_32}")

# Instantiate the PyTorch backend
be_pt = instantiate_backend("pytorch")

# Check a float64 PyTorch tensor
x_pt_64 = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)
is_pt_32 = be_pt.is_float32(x_pt_64)
assert is_pt_32 is False
print(f"PyTorch float64 check: {is_pt_32}")
```

### LLM Instruction Prompt
- When checking the precision of time-series arrays or tensors in `tslearn`, use the `is_float32(x)` method on the instantiated backend object (e.g., `be.is_float32(x)`). 
- Do not call `is_float32` as a top-level standalone function; it must be accessed via a backend instance returned by `tslearn.backend.instantiate_backend`.
- Ensure the input is a NumPy array or PyTorch tensor, not a native Python list.

### Prompt Snippet
```text
Use `be.is_float32(x)` on an instantiated `tslearn` backend object to safely check if an array or tensor is 32-bit float across NumPy and PyTorch.
```

### Common Failure Modes
- **Missing Backend Instance:** Attempting to import and call `is_float32` directly as a standalone function, which will fail. It must be called on a backend instance.
- **AttributeError on Lists:** Passing a native Python list (e.g., `[1.0, 2.0]`) instead of an array or tensor. Lists lack the `dtype` attribute required by the backend check.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend
import numpy as np

# 1. Instantiate the backend
be = instantiate_backend("numpy")

# 2. Ensure input is an array/tensor
x = np.array([1.0, 2.0], dtype=np.float32)

# 3. Call the method on the backend instance
is_32 = be.is_float32(x)
```

## API Test: `is_float64`

### Signature
```python
def is_float64(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:169  (+1 more definition site/overload)_

### Goal
Checks whether the provided array or tensor has a 64-bit floating-point data type (`float64`), abstracting the type-check across the NumPy and PyTorch backends.

### Parameters
- `x`: The input time-series data structure (NumPy array or PyTorch tensor) whose data type is to be inspected.

### Input
A valid array-like object native to the instantiated backend. For the `NumPyBackend`, this must be a `numpy.ndarray`. For the `PyTorchBackend`, this must be a `torch.Tensor`. 

### Output
Returns `unspecified` — A boolean value (`True` or `False`) indicating whether the underlying data type of `x` is exactly 64-bit float (`numpy.float64` or `torch.float64`).

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Inferred from signature (not verified)
be = instantiate_backend("numpy")

x_float64 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
x_float32 = np.array([1.0, 2.0, 3.0], dtype=np.float32)

# Check dtypes using the backend helper
is_64 = be.is_float64(x_float64)
is_32 = be.is_float64(x_float32)

assert is_64 is True, "Failed to identify float64 array."
assert is_32 is False, "Incorrectly identified float32 as float64."
print(f"Float64 check passed. x_float64: {is_64}, x_float32: {is_32}")
```

### LLM Instruction Prompt
- When writing backend-agnostic metric code in `tslearn`, NEVER hardcode `x.dtype == np.float64`. Instead, instantiate the backend using `instantiate_backend(...)` and call `be.is_float64(x)` to safely check the precision of the inputs regardless of whether they are NumPy arrays or PyTorch tensors.
- Ensure `x` is already converted to the backend's native tensor/array type before calling this method; passing raw Python lists may cause attribute errors.

### Prompt Snippet
```text
Use the backend's `is_float64(x)` method to verify if the time-series data is double-precision before performing gradient-sensitive metric computations like Soft-DTW.
```

### Common Failure Modes
- **Passing Raw Python Lists:** Calling `be.is_float64([1.0, 2.0])` will likely fail with an `AttributeError` because standard Python lists do not have a `.dtype` attribute, which the backend helper expects to inspect.
- **Backend Mismatch:** Passing a PyTorch tensor to the `NumPyBackend`'s `is_float64` method (or vice versa) may yield unexpected results or crash, as the helper expects the input to match the backend's native type.

### Fix Code Hint
```python
# BAD: Hardcoding numpy dtype check breaks PyTorch compatibility
# if x.dtype == np.float64: ...

# GOOD: Use the backend helper
be = instantiate_backend(x)
if not be.is_float64(x):
    x = be.cast(x, dtype="float64") # Ensure double precision for stable metric gradients
```

## API Test: `is_numpy`

### Signature
```python
def is_numpy(self)
```
_Source: tslearn/tslearn/backend/backend.py:77_

### Goal
Determine if the current `tslearn` backend instance is configured to use the NumPy computational backend.

### Parameters
- `self`: The `tslearn.backend.Backend` instance whose active backend type is being checked.

### Input
An instantiated `Backend` object, typically created via `Backend("numpy")`, `Backend("torch")`, or returned by backend selection utilities like `instantiate_backend`.

### Output
Returns `unspecified` — A boolean value (`True` or `False`) representing whether the underlying backend is currently set to `NumPyBackend`.

### Valid Call Patterns
```python
from tslearn.backend import Backend

# Instantiate a PyTorch backend wrapper
backend_ = Backend("torch")
assert not backend_.is_numpy

# Switch to NumPy backend
backend_.set_backend("numpy")
assert backend_.is_numpy
```

### LLM Instruction Prompt
- When checking the backend type of a `tslearn.backend.Backend` instance, access `is_numpy` as a property (without parentheses), not as a method. This is required because, despite the raw signature extraction showing `def is_numpy(self)`, the project's test suite strictly accesses it as a property (e.g., `assert backend_.is_numpy`).

### Prompt Snippet
```text
`is_numpy` is a property on `tslearn.backend.Backend` instances that returns True if the active backend is NumPy. Access it without parentheses: `if backend_.is_numpy: ...`.
```

### Common Failure Modes
- **Calling as a method:** Attempting to invoke `is_numpy` with parentheses (e.g., `backend_.is_numpy()`) will result in a `TypeError: 'bool' object is not callable`, as it is implemented and accessed as a property.

### Fix Code Hint
```python
# WRONG: Calling the property as a method
# is_np = backend_.is_numpy()

# CORRECT: Accessing it as a property
is_np = backend_.is_numpy
if is_np:
    print("NumPy backend is active.")
```

## API Test: `is_pytorch`

### Signature
```python
def is_pytorch(self)
```
_Source: tslearn/tslearn/backend/backend.py:81_

### Goal
Evaluates whether the currently active computational backend managed by the `Backend` instance is PyTorch.

### Parameters
- `self`: The `tslearn.backend.Backend` instance whose active backend is being queried.

### Input
An instantiated `Backend` object, which manages the dual-backend system (NumPy and PyTorch) used for time-series metric computations and automatic differentiation.

### Output
Returns `unspecified` — A boolean value (`True` if the active backend is PyTorch, `False` otherwise).

### Valid Call Patterns
```python
from tslearn.backend import Backend

# Instantiate a backend manager requesting PyTorch
backend_ = Backend("torch")

# Check if the active backend is PyTorch (accessed as a property)
is_pt = backend_.is_pytorch
assert is_pt is True
print(f"Is PyTorch backend active? {is_pt}")

# Switch to NumPy and verify
backend_.set_backend("numpy")
assert not backend_.is_pytorch
```

### LLM Instruction Prompt
- When checking if a `tslearn.backend.Backend` instance is currently using the PyTorch backend, access `.is_pytorch` as a property without parentheses. Do not call it as a method.

### Prompt Snippet
```text
# Correct usage: property access
if backend_.is_pytorch:
    # Execute PyTorch-specific logic (e.g., requires_grad=True)
    pass
```

### Common Failure Modes
- **Calling as a method:** Attempting to invoke `backend_.is_pytorch()` with parentheses will raise a `TypeError` (e.g., `'bool' object is not callable`), as it is exposed as a property on the `Backend` instance.
- **Checking on the wrong object:** Attempting to call `.is_pytorch` directly on a PyTorch tensor or a NumPy array instead of the `tslearn.backend.Backend` manager instance.

### Fix Code Hint
```python
# BAD: Calling as a method
# is_pt = backend_.is_pytorch()

# GOOD: Accessing as a property
is_pt = backend_.is_pytorch
```

## API Test: `iscomplex`

### Signature
```python
def iscomplex(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:153_

### Goal
Determines whether a given PyTorch tensor has a complex data type, acting as a low-level backend helper for `tslearn` metric computations.

### Parameters
- `x`: The input PyTorch tensor to be evaluated for a complex data type.

### Input
A PyTorch tensor (`torch.Tensor`). The environment must have PyTorch installed locally to use this backend-specific helper.

### Output
Returns `unspecified` (typically a boolean) — indicates whether the input tensor's data type is complex (e.g., `torch.complex64` or `torch.complex128`).

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import iscomplex

# Note: Call form inferred from signature as no verbatim examples exist
real_tensor = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float32)
complex_tensor = torch.tensor([1.0+1j, 2.0+2j], dtype=torch.complex64)

is_real_cplx = iscomplex(real_tensor)
is_cplx_cplx = iscomplex(complex_tensor)

assert not is_real_cplx, "Real tensor should not be complex"
assert is_cplx_cplx, "Complex tensor should be complex"
print(f"Complex check passed. Real: {is_real_cplx}, Complex: {is_cplx_cplx}")
```

### LLM Instruction Prompt
- Use `iscomplex` from `tslearn.backend.pytorch_backend` to check if a PyTorch tensor is complex-valued when writing custom PyTorch-backend extensions for `tslearn`.
- Do not pass NumPy arrays or standard Python lists to this specific PyTorch backend helper; it strictly expects PyTorch tensors.
- Remember that this is a low-level backend function; general users should typically rely on the dynamic backend dispatcher (`instantiate_backend`) rather than calling this directly.

### Prompt Snippet
```text
When operating within the PyTorch backend of `tslearn`, use `tslearn.backend.pytorch_backend.iscomplex(x)` to verify if a tensor `x` has a complex data type. Ensure `x` is a `torch.Tensor`.
```

### Common Failure Modes
- **Type Errors:** Passing a NumPy array, standard Python list, or scalar instead of a PyTorch tensor, which will cause PyTorch-specific type checks or attribute accesses to fail.
- **Missing Dependencies:** Attempting to import or use this function in an environment where the `pytorch` package is not installed.

### Fix Code Hint
```python
# BAD: Passing a NumPy array to the PyTorch backend helper
# import numpy as np
# iscomplex(np.array([1.0+1j]))

# GOOD: Ensure the input is a PyTorch tensor
import torch
from tslearn.backend.pytorch_backend import iscomplex

tensor_input = torch.tensor([1.0+1j], dtype=torch.complex64)
result = iscomplex(tensor_input)
```

## API Test: `itakura_mask`

### Signature
```python
def itakura_mask(sz1, sz2, max_slope=2.0, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1702  (+1 more definition site/overload)_

_Source doc:_ Compute the Itakura mask. Parameters ---------- sz1 : int The size of the first time series sz2 : int The size of the second time series. max_slope : float (default = 2) The maximum slope of the parallelogram. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- mask : array-like, shape=(sz1, sz2) Itakura mask. Examples -------- >>> itakura_mask(6, 6) array([[ True, False, False, False, False, False], [False,  True,  True, False, False, False], [False,  True,  True,  True, False, False], [False, False,  True,  True,  True, False], [False, False, False,  True,  True, False], [False, False, False, False, False,  True]])

### Goal
Compute a boolean Itakura parallelogram mask of shape `(sz1, sz2)` to constrain the alignment path in Dynamic Time Warping (DTW).

### Parameters
- `sz1`: Integer representing the length (number of time steps) of the first time series.
- `sz2`: Integer representing the length (number of time steps) of the second time series.
- `max_slope`, default `2.0`: Float representing the maximum slope of the parallelogram constraint.
- `be`, default `None`: Backend object or string (`"numpy"` or `"pytorch"`) to determine the output array type. If `None`, defaults to the NumPy backend.

### Input
- `sz1` and `sz2` must be positive integers corresponding to the lengths of the time series being aligned.
- `max_slope` must be a float (typically `>= 1.0`).
- `be` must be a valid backend identifier if provided.

### Output
Returns `unspecified` — A boolean array or tensor of shape `(sz1, sz2)` where `True` indicates that a cell is within the Itakura parallelogram and allowed in the DTW path. The return type is a NumPy array or PyTorch tensor depending on the `be` parameter.

### Valid Call Patterns
```python
from tslearn.metrics import itakura_mask

# Default NumPy backend
mask_np = itakura_mask(6, 6, max_slope=3.0)

# PyTorch backend for automatic differentiation workflows
mask_pt = itakura_mask(10, 10, max_slope=2.0, be="pytorch")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.itakura_mask(sz1, sz2, max_slope=2.0, be=None)` to generate a boolean mask for constraining DTW paths.
- Provide the exact lengths of the two time series as `sz1` and `sz2`, NOT the time series arrays themselves.
- Set `be="pytorch"` if the mask will be used with PyTorch tensors for automatic differentiation.

### Prompt Snippet
```text
Generate an Itakura mask for two time series of lengths 8 and 8 with a maximum slope of 2.0 using the PyTorch backend.
```

### Common Failure Modes
- Providing time series arrays instead of their integer lengths (`sz1`, `sz2`), causing a `TypeError`.
- Specifying an unsupported backend string (e.g., `"tf"` or `"jax"`), which will fall back to NumPy or raise an error depending on the backend instantiation logic.
- Using the mask with time series of different lengths than `sz1` and `sz2`, causing shape mismatches during DTW computation.

### Fix Code Hint
```python
# WRONG: Passing arrays instead of lengths
# mask = itakura_mask(ts1, ts2)

# CORRECT: Pass the lengths of the time series
mask = itakura_mask(ts1.shape[0], ts2.shape[0], max_slope=2.0, be="numpy")
```

## API Test: `jacobian_product`

### Signature
```python
def jacobian_product(self, E)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:1218_

_Source doc:_ Compute the product between the Jacobian (a linear map from m x d to m x n) and a matrix E. Parameters ---------- E: array-like, shape=(m, n) Second time series. Returns ------- G: array-like, shape=(m, d) Product with Jacobian. ([m x d, m x n] * [m x n] = [m x d]).

### Goal
Computes the product between a Jacobian matrix (representing a linear map from `m x d` to `m x n`) and a matrix `E` of shape `(m, n)`.

### Parameters
- `self`: The instance of the undocumented class in `tslearn.metrics.softdtw_variants` that provides this method.
- `E`: array-like of shape `(m, n)`. Represents the second time series or a matrix to be multiplied with the Jacobian.

### Input
The caller must provide an instantiated object that implements this method, and an array-like `E` (e.g., a NumPy array) with exactly two dimensions `(m, n)`.

### Output
Returns `unspecified` — an array-like object `G` of shape `(m, d)` representing the product of the Jacobian and `E`.

### Valid Call Patterns
```python
from unittest.mock import Mock
import numpy as np

# Example inferred from signature (not verified).
# The exact tslearn class is unknown from the provided facts.
instance = Mock()
instance.jacobian_product.return_value = np.zeros((5, 3)) # shape (m, d)

# E must be a 2D array of shape (m, n)
E = np.zeros((5, 4)) 
G = instance.jacobian_product(E)

assert G.shape == (5, 3)
print("Call pattern demonstrated via mock.")
```

### LLM Instruction Prompt
- Call `jacobian_product(E)` as an instance method on the appropriate object from `tslearn.metrics.softdtw_variants`, never as a standalone function.
- Ensure the input `E` is a 2D array-like of shape `(m, n)`.
- Expect the output to be a 2D array-like of shape `(m, d)`.
- Note that the exact class implementing this method is not specified in the standard documentation context; if something is unknown, say so rather than guessing.

### Prompt Snippet
```text
# Call as an instance method on the appropriate object
G = instance.jacobian_product(E)
```

### Common Failure Modes
- Attempting to import and call `jacobian_product` as a standalone module-level function, which will raise an `ImportError` or `NameError`.
- Passing an `E` matrix with incorrect dimensions (e.g., a standard `tslearn` 3D time-series dataset `(n_ts, max_sz, d)` instead of the expected 2D `(m, n)` shape).

### Fix Code Hint
```python
# WRONG: Calling as a standalone function or passing a 3D array
# from tslearn.metrics.softdtw_variants import jacobian_product
# G = jacobian_product(E_3d)

# CORRECT: Calling on the appropriate instance with a 2D array
G = instance.jacobian_product(E_2d)
```

## API Test: `kneighbors`

### Signature
```python
def kneighbors(self, X=None, n_neighbors=None, return_distance=True)
```
_Source: tslearn/tslearn/neighbors/neighbors.py:101  (+1 more definition site/overload)_

_Source doc:_ Finds the K-neighbors of a point. Returns indices of and distances to the neighbors of each point. Parameters ---------- X : array-like, shape (n_ts, sz, d) The query time series. If not provided, neighbors of each indexed point are returned. In this case, the query point is not considered its own neighbor. n_neighbors : int Number of neighbors to get (default is the value passed to the constructor). return_distance : boolean, optional. Defaults to True. If False, distances will not be returned Returns ------- dist : array Array representing the distance to points, only present if return_distance=True ind : array Indices of the nearest points in the population matrix.

### Goal
Find the K-nearest neighbors of query time series within a fitted `tslearn` nearest neighbors estimator.

### Parameters
- `self`: The fitted nearest neighbors estimator instance (e.g., `KNeighborsTimeSeries`, `KNeighborsTimeSeriesClassifier`, or `KNeighborsTimeSeriesRegressor`).
- `X`, default `None`: The query time series dataset. If `None`, the neighbors of each point in the training data are returned (excluding the point itself).
- `n_neighbors`, default `None`: The number of neighbors to retrieve. If `None`, defaults to the `n_neighbors` value passed to the estimator's constructor.
- `return_distance`, default `True`: If `True`, returns both the distances and the indices of the neighbors. If `False`, returns only the indices.

### Input
`X` must be a 3D array-like object of shape `(n_ts, max_sz, d)` representing the query time series. If the time series are of variable lengths, they must be padded with `nan` values and formatted using `tslearn.utils.to_time_series_dataset`. The estimator (`self`) must be fitted with training data prior to calling this method.

### Output
Returns `unspecified` — If `return_distance=True`, returns a tuple `(dist, ind)` where `dist` is a 2D array of distances to the nearest points and `ind` is a 2D array of their indices in the training matrix. If `return_distance=False`, returns only the 2D array `ind`. Both arrays have shape `(n_queries, n_neighbors)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors import KNeighborsTimeSeries

# 1. Setup and fit the model
n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
X_train = rng.randn(n, sz, d)
X_query = rng.randn(2, sz, d)

model = KNeighborsTimeSeries(n_neighbors=5)
model.fit(X_train)

# 2. Return both distances and indices (default)
distances, indices = model.kneighbors(X_query, return_distance=True)
assert distances.shape == (2, 5)
assert indices.shape == (2, 5)

# 3. Return only indices
indices_only = model.kneighbors(X_query, return_distance=False)
assert indices_only.shape == (2, 5)
```

### LLM Instruction Prompt
- When calling `kneighbors`, ensure the estimator has already been fitted using `.fit()`.
- Ensure the query data `X` is strictly formatted as a 3D array `(n_ts, max_sz, d)`.
- Pay attention to the `return_distance` parameter: it dictates whether the method returns a tuple of two arrays `(distances, indices)` or a single array `indices`. Do not unpack a single array if `return_distance=False`.

### Prompt Snippet
```text
Ensure the query data is a 3D array `(n_ts, max_sz, d)`. If `return_distance=True`, unpack the result into `distances, indices`. If `return_distance=False`, assign the result to a single variable `indices`.
```

### Common Failure Modes
- **Not fitting the model first:** Calling `kneighbors` before `fit()` will raise a `NotFittedError`.
- **Incorrect Input Shape:** Passing a 1D or 2D array instead of the required 3D `(n_ts, max_sz, d)` array will cause shape mismatch errors or incorrect distance calculations.
- **Unpacking Errors:** Attempting to unpack the result into two variables when `return_distance=False` will raise a `ValueError: not enough values to unpack`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset

# Ensure query data is 3D
X_query_3d = to_time_series_dataset(X_query_raw)

# Ensure model is fitted
model.fit(X_train_3d)

# Correctly handle the return signature
distances, indices = model.kneighbors(X_query_3d, return_distance=True)
```

## API Test: `lb_envelope`

### Signature
```python
def lb_envelope(ts, radius=1, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2170_

_Source doc:_ Compute time series envelope as required by LB_Keogh. LB_Keogh was originally presented in [1]_. Parameters ---------- ts : array-like, shape=(sz, d) or (sz,) Time series for which the envelope should be computed. If shape is (sz,), the time series is assumed to be univariate. radius : int (default: 1) Radius to be used for the envelope generation (the envelope at time index i will be generated based on all observations from the time series at indices comprised between i-radius and i+radius). be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- envelope_down : array-like, shape=(sz, d) Lower-side of the envelope. envelope_up : array-like, shape=(sz, d) Upper-side of the envelope. Examples -------- >>> ts1 = [1, 2, 3, 2, 1] >>> env_low, env_up = lb_envelope(ts1, radius=1) >>> env_low array([[1.], [1.], [2.], [1.], [1.]]) >>> env_up array([[2.], [3.], [3.], [3.], [2.]]) See also -------- lb_keogh : Compute LB_Keogh similarity References ---------- .. [1] Keogh, E. Exact indexing of dynamic time warping. In International Conference on Very Large Data Bases, 2002. pp 406-417.

### Goal
Compute the lower and upper bounding envelopes of a single time series, which are required for calculating the LB_Keogh lower bound similarity metric.

### Parameters
- `ts`: An array-like time series of shape `(sz, d)` or `(sz,)` for which the envelope should be computed.
- `radius`, default `1`: The integer radius used for envelope generation. The envelope at time index `i` is generated based on all observations between indices `i-radius` and `i+radius`.
- `be`, default `None`: The computational backend to use. Can be `"numpy"`, `"pytorch"`, a Backend instance, or `None` (which auto-detects the backend based on the input array type).

### Input
A single time series provided as a list, NumPy array, or PyTorch tensor. It must be 1D `(sz,)` for univariate data or 2D `(sz, d)` for multivariate data. Note that unlike `tslearn` estimators which expect 3D datasets `(n_ts, sz, d)`, this metric helper expects a single time series.

### Output
Returns `unspecified` — A tuple of two array-like objects `(envelope_down, envelope_up)`. Both are of shape `(sz, d)` and represent the lower and upper sides of the envelope, respectively. The output type (NumPy array or PyTorch tensor) matches the selected or auto-detected backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import lb_envelope

# 1. Basic usage with a 1D list (auto-converted to 2D NumPy arrays)
ts1 = [1, 2, 3, 2, 1]
env_low, env_up = lb_envelope(ts1, radius=1)

assert np.allclose(env_low, [[1.], [1.], [2.], [1.], [1.]])
assert np.allclose(env_up, [[2.], [3.], [3.], [3.], [2.]])

# 2. Usage with PyTorch backend
import torch
ts_torch = torch.tensor([[1.0], [2.0], [3.0], [2.0], [1.0]])
env_low_pt, env_up_pt = lb_envelope(ts_torch, radius=1, be="pytorch")

assert isinstance(env_low_pt, torch.Tensor)
assert env_low_pt.shape == (5, 1)
```

### LLM Instruction Prompt
When calling `tslearn.metrics.lb_envelope`, ensure the input is a single time series (shape `(sz,)` or `(sz, d)`), not a full 3D dataset. The function returns a tuple of two arrays `(envelope_down, envelope_up)`. If you need PyTorch tensors for automatic differentiation, pass a PyTorch tensor as input or explicitly set `be="pytorch"`.

### Prompt Snippet
```text
Use `tslearn.metrics.lb_envelope(ts, radius=1)` to compute the lower and upper bounding envelopes for LB_Keogh. It returns a tuple `(envelope_down, envelope_up)`, both of shape `(sz, d)`.
```

### Common Failure Modes
- Passing a 3D dataset `(n_ts, sz, d)` instead of a single time series `(sz, d)`. `lb_envelope` operates on one time series at a time.
- Failing to unpack the return value into two variables, resulting in a tuple being mistakenly used as a single array in downstream calculations.
- Passing `radius=0`, which trivially returns the original time series as both the upper and lower envelope, defeating the purpose of the bounding envelope.

### Fix Code Hint
```python
# WRONG: Passing a 3D dataset or expecting a single return value
# env = lb_envelope(X_3d_dataset, radius=2)

# CORRECT: Pass a single time series (2D or 1D) and unpack the tuple
env_low, env_up = lb_envelope(X_3d_dataset[0], radius=2)
```

## API Test: `lb_keogh`

### Signature
```python
def lb_keogh(ts_query, ts_candidate=None, radius=1, envelope_candidate=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2008_

### Goal
Compute the LB_Keogh lower bound distance between a univariate query time series and a candidate time series (or its pre-computed envelope).

### Parameters
- `ts_query`: Univariate query time series to compare to the envelope of the candidate. Array-like, shape `(sz, 1)` or `(sz,)`.
- `ts_candidate`, default `None`: Univariate candidate time series. Array-like, shape `(sz, 1)` or `(sz,)`. If `None`, the envelope must be provided via the `envelope_candidate` parameter.
- `radius`, default `1`: Integer radius used for envelope generation (the envelope at index `i` uses candidate observations between `i-radius` and `i+radius`). Ignored if `ts_candidate` is `None`.
- `envelope_candidate`, default `None`: A pair of array-like structures `(envelope_down, envelope_up)` representing the pre-computed envelope of the candidate time series. If `None`, it is computed on the fly from `ts_candidate`.

### Input
- Univariate time series arrays or lists.
- `ts_query` and `ts_candidate` (or the arrays in `envelope_candidate`) **must be of exactly equal size**.
- The function expects either `ts_candidate` or `envelope_candidate` to be provided.

### Output
Returns `float` — The LB_Keogh distance between the query time series and the envelope of the candidate time series.

### Valid Call Patterns
```python
from tslearn.metrics import lb_keogh, lb_envelope

ts_query = [0.0, 0.0, 0.0, 0.0, 0.0]
ts_candidate = [1.0, 2.0, 3.0, 2.0, 1.0]

# Pattern 1: Compute envelope on the fly
dist = lb_keogh(ts_query=ts_query, ts_candidate=ts_candidate, radius=1)
print(f"LB_Keogh distance: {dist:.4f}")

# Pattern 2: Use pre-computed envelope (useful for querying many series against one candidate)
env_low, env_up = lb_envelope(ts_candidate, radius=1)
dist_env = lb_keogh(ts_query=ts_query, envelope_candidate=(env_low, env_up))
assert dist == dist_env
```

### LLM Instruction Prompt
- Use `lb_keogh` to compute a fast lower bound to the Dynamic Time Warping (DTW) distance.
- You must provide `ts_query` and either `ts_candidate` or `envelope_candidate`.
- Ensure the query and candidate time series are univariate and of equal length.
- If comparing multiple queries to the same candidate, pre-compute the envelope using `lb_envelope` and pass it via `envelope_candidate` to save computation time.

### Prompt Snippet
```text
When computing LB_Keogh lower bounds with `tslearn.metrics.lb_keogh`, ensure the query and candidate time series are univariate and of equal length. Pass either `ts_candidate` (with an optional `radius`) or a pre-computed `envelope_candidate` tuple.
```

### Common Failure Modes
- **Unequal lengths**: Passing a `ts_query` and `ts_candidate` (or envelope) of different sizes. LB_Keogh strictly requires equal-length series.
- **Missing candidate**: Passing neither `ts_candidate` nor `envelope_candidate`, which leaves the function with nothing to compare against.
- **Multivariate data**: Passing 3D arrays or multivariate time series. LB_Keogh is designed for univariate series `(sz, 1)` or `(sz,)`.

### Fix Code Hint
```python
# Ensure equal lengths and univariate shape before calling
if len(ts_query) == len(ts_candidate):
    dist = lb_keogh(ts_query=ts_query, ts_candidate=ts_candidate, radius=1)
else:
    raise ValueError("ts_query and ts_candidate must be of equal size for LB_Keogh.")
```

## API Test: `lcss`

### Signature
```python
def lcss(s1, s2, eps=1.0, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2383_

### Goal
Compute the Longest Common Subsequence (LCSS) similarity measure between two time series, returning a value between 0.0 and 1.0 that represents the percentage of matching points within a specified distance threshold.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. Must have the same dimension `d` as `s1`.
- `eps`, default `1.0`: float. The maximum matching distance threshold. Points are considered a match if their distance is less than or equal to this value.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. Global constraint to restrict admissible paths for LCSS, forcing paths to lie close to the diagonal.
- `sakoe_chiba_radius`, default `None`: int or `None`. Radius for the Sakoe-Chiba band constraint. If `None` and `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: float or `None`. Maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint="itakura"`, defaults to 2.0.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. Determines the computational backend. If `None`, it auto-detects based on input types (e.g., uses PyTorch if inputs are `torch` tensors).

### Input
The caller must provide two individual time series arrays (not full 3D datasets). They can be of different lengths (`sz1` and `sz2`) but must share the same feature dimensionality (`d`). If passing 1D arrays, they are treated as univariate time series.

### Output
Returns `unspecified` — A `float` (or a PyTorch tensor if the PyTorch backend is used) representing the LCSS similarity. The value ranges from 0.0 to 1.0, where 1.0 indicates a full match relative to the length of the shortest time series.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

# 1. Univariate time series with default eps
s1 = [1, 2, 3]
s2 = [1.0, 2.0, 2.0, 3.0]
sim = tslearn.metrics.lcss(s1, s2)

assert isinstance(sim, float)
np.testing.assert_equal(sim, 1.0)
print(f"Univariate LCSS similarity: {sim}")

# 2. Multivariate time series with strict eps threshold
s3 = [[1, 1], [2, 2], [3, 3]]
s4 = [[1.0, 1.0], [2.0, 2.0], [2.0, 2.0], [2.0, 2.0], [3.0, 3.0]]
sim_multi = tslearn.metrics.lcss(s3, s4, eps=0)

np.testing.assert_equal(sim_multi, 1.0)
print(f"Multivariate LCSS similarity: {sim_multi}")
```

### LLM Instruction Prompt
- Unlike DTW which returns a distance (lower is better), `lcss` returns a **similarity score** (higher is better, bounded between 0.0 and 1.0).
- Do not pass full 3D datasets `(n_ts, max_sz, d)` to `lcss`. It expects individual 1D or 2D time series arrays.
- If both `sakoe_chiba_radius` and `itakura_max_slope` are set, you must explicitly provide `global_constraint` to resolve the ambiguity, otherwise a `RuntimeWarning` is raised and no constraint is applied.
- LCSS paths do not need to be contiguous; it leaves some points unmatched to focus on similar parts.

### Prompt Snippet
```text
When comparing two time series with `tslearn.metrics.lcss`, remember that it returns a similarity percentage (0 to 1), not a distance. Ensure both inputs have the same feature dimension `d`. If you want to restrict the alignment path, specify `global_constraint="sakoe_chiba"` along with `sakoe_chiba_radius`.
```

### Common Failure Modes
- **Dimensionality Mismatch**: Passing two time series with different feature dimensions (e.g., `s1` has shape `(10, 2)` and `s2` has shape `(15, 3)`).
- **Passing 3D Datasets**: Passing a full dataset of shape `(n_ts, sz, d)` instead of a single time series `(sz, d)`.
- **Ambiguous Constraints**: Setting both `sakoe_chiba_radius` and `itakura_max_slope` without specifying `global_constraint`.
- **Misinterpreting Output**: Treating the output as a distance metric (where 0 is identical) rather than a similarity metric (where 1 is identical).

### Fix Code Hint
```python
# BAD: Passing 3D datasets and treating output as distance
# dist = tslearn.metrics.lcss(X_train, X_test)
# if dist == 0: ...

# GOOD: Passing individual 1D/2D time series and treating output as similarity
sim = tslearn.metrics.lcss(X_train[0], X_test[0], eps=0.5, global_constraint="sakoe_chiba", sakoe_chiba_radius=3)
if sim == 1.0:
    print("Time series are fully similar within the eps threshold.")
```

## API Test: `lcss_accumulated_matrix`

### Signature
```python
def lcss_accumulated_matrix(s1, s2, eps, mask, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2270_

_Source doc:_ Compute the longest common subsequence similarity score between two time series. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) First time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Second time series. If shape is (sz2,), the time series is assumed to be univariate. eps : float Matching threshold. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- acc_cost_mat : array-like, shape=(sz1 + 1, sz2 + 1) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) similarity between two time series.

### Parameters
- `s1`: First time series, array-like of shape `(sz1, d)` or `(sz1,)`. If 1D, it is assumed to be univariate.
- `s2`: Second time series, array-like of shape `(sz2, d)` or `(sz2,)`. If 1D, it is assumed to be univariate.
- `eps`: Matching threshold (float). Points are considered matching if their distance is less than or equal to `eps`.
- `mask`: Boolean mask array of shape `(sz1, sz2)`. Unconsidered cells must have `False` values.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`). If `None`, the backend is automatically determined from the input arrays.

### Input
- `s1` and `s2` must be 1D or 2D arrays (time steps, dimensions). Unlike high-level estimators, these low-level metric helpers expect single time series, not 3D datasets.
- `eps` must be a numeric float value.
- `mask` must be a boolean array matching the lengths of `s1` and `s2` exactly (`shape=(len(s1), len(s2))`).
- If using PyTorch for automatic differentiation, `s1` and `s2` must be `torch.Tensor` objects with `requires_grad=True`.

### Output
Returns `unspecified` — An accumulated cost matrix of shape `(sz1 + 1, sz2 + 1)` representing the dynamic programming table for the LCSS alignment. The type (NumPy array or PyTorch tensor) matches the selected backend.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import lcss_accumulated_matrix

s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])
eps = 0.5
mask = np.ones((len(s1), len(s2)), dtype=bool)

# Inferred from signature
acc_mat = lcss_accumulated_matrix(s1, s2, eps=eps, mask=mask)

assert acc_mat.shape == (len(s1) + 1, len(s2) + 1)
print(acc_mat)
```

### LLM Instruction Prompt
- When calling `lcss_accumulated_matrix`, you MUST provide the `mask` argument, as it has no default value.
- Ensure `mask` is a boolean array of shape `(len(s1), len(s2))`.
- Pass single time series (1D or 2D arrays) to `s1` and `s2`, not 3D dataset arrays.
- The returned matrix will have dimensions `(len(s1) + 1, len(s2) + 1)`.

### Prompt Snippet
```text
Use `tslearn.metrics.lcss_accumulated_matrix(s1, s2, eps, mask)` to compute the LCSS dynamic programming table. `s1` and `s2` must be 1D or 2D arrays. `mask` is required and must be a boolean array of shape `(len(s1), len(s2))`. Returns a matrix of shape `(len(s1) + 1, len(s2) + 1)`.
```

### Common Failure Modes
- **Missing `mask` argument**: Failing to provide `mask` will raise a `TypeError` because it is a required positional argument.
- **Incorrect `mask` shape**: Providing a mask that does not exactly match `(len(s1), len(s2))` will cause a shape mismatch error during the dynamic programming computation.
- **Passing 3D arrays**: Passing a full dataset `(n_ts, max_sz, d)` instead of a single time series `(sz, d)` will result in incorrect distance calculations or broadcast errors.

### Fix Code Hint
```python
# FIX: Ensure inputs are single time series and create a properly shaped boolean mask
s1_single = X[0]  # shape (sz1, d)
s2_single = X[1]  # shape (sz2, d)
mask = np.ones((len(s1_single), len(s2_single)), dtype=bool)

acc_mat = lcss_accumulated_matrix(s1_single, s2_single, eps=0.5, mask=mask)
```

## API Test: `lcss_accumulated_matrix_from_dist_matrix`

### Signature
```python
def lcss_accumulated_matrix_from_dist_matrix(dist_matrix, eps, mask, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2865_

_Source doc:_ Compute the accumulated cost matrix score between two time series using a precomputed distance matrix. Parameters ---------- dist_matrix : array-like, shape=(sz1, sz2) Array containing the pairwise distances. eps : float (default: 1.) Maximum matching distance threshold. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- acc_cost_mat : array-like, shape=(sz1 + 1, sz2 + 1) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) alignment between two time series using a precomputed pairwise distance matrix, a matching threshold, and a boolean mask.

### Parameters
- `dist_matrix`: Array-like of shape `(sz1, sz2)` containing the precomputed pairwise distances between the points of the two time series.
- `eps`: Float representing the maximum matching distance threshold. Distances less than or equal to this value are considered matches.
- `mask`: Boolean array-like of shape `(sz1, sz2)` indicating which cells in the distance matrix are valid to consider. Unconsidered cells must be `False`.
- `be`, default `None`: Backend object or string (`"numpy"` or `"pytorch"`). If `None`, the backend is automatically inferred from the input arrays.

### Input
- `dist_matrix` must be a 2D numeric array or tensor of shape `(sz1, sz2)`.
- `mask` must be a 2D boolean array or tensor of the exact same shape `(sz1, sz2)`.
- `eps` must be a scalar float.
- If using PyTorch for automatic differentiation, inputs must be PyTorch tensors and `be="pytorch"` should be specified or inferred.

### Output
Returns `unspecified` — An array-like (NumPy array or PyTorch tensor, depending on the backend) of shape `(sz1 + 1, sz2 + 1)` representing the accumulated LCSS cost matrix.

### Valid Call Patterns
```python
# Example inferred from signature
import numpy as np
from tslearn.metrics.dtw_variants import lcss_accumulated_matrix_from_dist_matrix

# 2 time series of lengths 2 and 3
dist_matrix = np.array([
    [0.5, 1.5, 2.0],
    [2.0, 0.1, 0.8]
])
mask = np.ones((2, 3), dtype=bool)
eps = 1.0

acc_cost_mat = lcss_accumulated_matrix_from_dist_matrix(
    dist_matrix=dist_matrix,
    eps=eps,
    mask=mask,
    be="numpy"
)

assert acc_cost_mat.shape == (3, 4)
print(acc_cost_mat)
```

### LLM Instruction Prompt
- When calling `lcss_accumulated_matrix_from_dist_matrix`, ensure that `dist_matrix` and `mask` are exactly 2D arrays of the same shape `(sz1, sz2)`.
- Do not pass raw 3D time-series datasets directly to this function; it expects a 2D pairwise distance matrix.
- The returned matrix will have dimensions `(sz1 + 1, sz2 + 1)`, padded with zeros along the first row and first column to facilitate dynamic programming.

### Prompt Snippet
```text
tslearn.metrics.dtw_variants.lcss_accumulated_matrix_from_dist_matrix(dist_matrix, eps, mask, be=None)
Computes the LCSS accumulated cost matrix from a 2D pairwise distance matrix and a boolean mask.
Returns a 2D array of shape (sz1 + 1, sz2 + 1).
```

### Common Failure Modes
- Passing 1D time series or 3D datasets instead of a 2D pairwise distance matrix.
- Providing a `mask` that has a different shape than `dist_matrix`, causing broadcasting errors or backend crashes.
- Forgetting that the output matrix is larger than the input matrix by 1 in both dimensions.
- Mixing NumPy arrays and PyTorch tensors without explicitly defining the `be` parameter, leading to backend resolution failures.

### Fix Code Hint
```python
# If you have raw time series, you must compute the distance matrix first
from tslearn.metrics import cdist_dtw
# Assuming ts1 is shape (sz1, d) and ts2 is shape (sz2, d)
from scipy.spatial.distance import cdist
dist_matrix = cdist(ts1, ts2, metric="euclidean")
mask = np.ones_like(dist_matrix, dtype=bool)

acc_cost_mat = lcss_accumulated_matrix_from_dist_matrix(
    dist_matrix=dist_matrix,
    eps=1.0,
    mask=mask
)
```

## API Test: `lcss_path`

### Signature
```python
def lcss_path(s1, s2, eps=1, global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2697_

_Source doc:_ Compute the Longest Common Subsequence (LCSS) similarity measure between (possibly multidimensional) time series and return both the path and the similarity. LCSS is computed by matching indexes that are met up until the eps threshold, so it leaves some points unmatched and focuses on the similar parts of two sequences. The matching can occur even if the time indexes are different. One can set additional constraints to the set of acceptable paths: the Sakoe-Chiba band which is parametrized by a radius or the Itakura parallelogram which is parametrized by a maximum slope. Both these constraints consists in forcing paths to lie close to the diagonal. To retrieve a meaningful similarity value from the length of the longest common subsequence, the percentage of that value regarding the length of the shortest time series is returned. According to this definition, the values returned by LCSS range from 0 to 1, the highest value taken when two time series fully match, and vice-versa. It is not required that both time series share the same size, but they must be the same dimension. LCSS was originally presented in [1]_ and is discussed in more details in our :ref:`dedicated user-guide page <lcss>`. Notes ----- Contrary to Dynamic Time Warping and variants, an LCSS path does not need to be contiguous. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. eps : float (default: 1.) Maximum matching distance threshold. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for LCSS. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [1]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. be : Backend object or string or None

### Goal
Compute the Longest Common Subsequence (LCSS) similarity measure and the optimal matching path between two time series, allowing for unmatched points.

### Parameters
- `s1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `s2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. Must have the same dimensionality `d` as `s1`.
- `eps`, default `1`: float. The maximum matching distance threshold. Points are considered a match if their distance is less than or equal to this value.
- `global_constraint`, default `None`: `{"itakura", "sakoe_chiba"}` or `None`. Global constraint to restrict admissible paths to lie close to the diagonal.
- `sakoe_chiba_radius`, default `None`: int or `None`. The radius to be used for the Sakoe-Chiba band global constraint.
- `itakura_max_slope`, default `None`: float or `None`. The maximum slope for the Itakura parallelogram constraint.
- `be`, default `None`: Backend object or string (`"numpy"`, `"pytorch"`) or `None`. Specifies the computational backend.

### Input
- `s1` and `s2` must be array-like structures (e.g., lists, NumPy arrays, or PyTorch tensors) representing individual time series.
- They can have different lengths (`sz1` and `sz2`) but must share the exact same feature dimensionality `d`.
- If using the PyTorch backend for automatic differentiation, inputs must be PyTorch tensors.

### Output
Returns `unspecified` — A tuple `(path, similarity)` where:
- `path` is a list of integer tuples `(i, j)` representing the matched indices between `s1` and `s2`. Unlike DTW, this path does not need to be contiguous.
- `similarity` is a float between `0.0` and `1.0`, representing the length of the longest common subsequence divided by the length of the shortest time series.

### Valid Call Patterns
```python
import tslearn.metrics

s1 = [1.0, 2.0, 3.0]
s2 = [1.0, 2.0, 2.0, 3.0]

# Compute LCSS path and similarity
path, sim = tslearn.metrics.lcss_path(s1, s2, eps=1.0, be="numpy")

assert isinstance(path, list)
assert isinstance(sim, float)
assert sim == 1.0
assert path == [(0, 1), (1, 2), (2, 3)]
print(f"LCSS Similarity: {sim}, Path: {path}")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.lcss_path`, ensure that `s1` and `s2` have the same number of feature dimensions.
- Remember that LCSS paths are not necessarily contiguous; they skip unmatched points that exceed the `eps` threshold.
- The returned similarity is a normalized percentage (0 to 1), not a raw distance.
- If providing `sakoe_chiba_radius` or `itakura_max_slope`, ensure `global_constraint` is explicitly set to `"sakoe_chiba"` or `"itakura"`, respectively, to avoid a `RuntimeWarning` and the constraint being ignored.

### Prompt Snippet
```text
Use `tslearn.metrics.lcss_path(s1, s2, eps=1.0)` to find the Longest Common Subsequence similarity and matching path between two time series. It returns a tuple `(path, similarity)` where `similarity` is a float between 0 and 1, and `path` is a list of matched index pairs `(i, j)`.
```

### Common Failure Modes
- **Mismatched Dimensions**: Passing two time series with different feature dimensions `d` (e.g., one univariate and one multivariate) will cause a failure.
- **Constraint Ignored**: Setting `sakoe_chiba_radius=3` but leaving `global_constraint=None` will raise a `RuntimeWarning` and compute the unconstrained LCSS.
- **Expecting a Distance**: Assuming the second return value is a distance metric (where lower is better). LCSS returns a *similarity* measure where `1.0` means a full match.
- **Expecting a Contiguous Path**: Assuming the returned path covers every index like DTW. LCSS intentionally leaves unmatched points out of the path.

### Fix Code Hint
```python
# FIX: Ensure global_constraint is set when using a radius
path, sim = tslearn.metrics.lcss_path(
    s1, s2, 
    eps=0.5, 
    global_constraint="sakoe_chiba", 
    sakoe_chiba_radius=2
)

# FIX: Ensure both time series have the same feature dimension
s1_2d = [[1.0], [2.0], [3.0]]
s2_2d = [[1.0], [2.0], [2.0], [3.0]]
path, sim = tslearn.metrics.lcss_path(s1_2d, s2_2d)
```

## API Test: `lcss_path_from_metric`

### Signature
```python
def lcss_path_from_metric(s1, s2=None, eps=1, metric='euclidean', global_constraint=None, sakoe_chiba_radius=None, itakura_max_slope=None, be=None, **kwds)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2908_

_Source doc:_ Compute the Longest Common Subsequence (LCSS) similarity measure between (possibly multidimensional) time series using a distance metric defined by the user and return both the path and the similarity. Having the length of the longest commom subsequence between two time series, the similarity is computed as the percentage of that value regarding the length of the shortest time series. It is not required that both time series share the same size, but they must be the same dimension. LCSS was originally presented in [1]_. Valid values for metric are the same as for scikit-learn `pairwise_distances`_ function i.e. a string (e.g. "euclidean", "sqeuclidean", "hamming") or a function that is used to compute the pairwise distances. See `scikit`_ and `scipy`_ documentations for more information about the available metrics. Parameters ---------- s1 : array-like, shape=(sz1, d) or (sz1,) if metric!="precomputed", (sz1, sz2) otherwise A time series or an array of pairwise distances between samples. If shape is (sz1,), the time series is assumed to be univariate. s2 : array-like, shape=(sz2, d) or (sz2,), optional (default: None) A second time series, only allowed if metric != "precomputed". If shape is (sz2,), the time series is assumed to be univariate. eps : float (default: 1.) Maximum matching distance threshold. metric : string or callable (default: "euclidean") Function used to compute the pairwise distances between each points of `s1` and `s2`. If metric is "precomputed", `s1` is assumed to be a distance matrix. If metric is an other string, it must be one of the options compatible with sklearn.metrics.pairwise_distances. Alternatively, if metric is a callable function, it is called on pairs of rows of `s1` and `s2`. The callable should take two 1 dimensional arrays as input and return a value indicating the distance between them. global_constraint : {"itakura", "sakoe_chiba"} or None (default: None) Global constraint to restrict admissible paths for LCSS. sakoe_chiba_radius : int or None (default: None) Radius to be used for Sakoe-Chiba band global constraint. The Sakoe-Chiba radius corresponds to the parameter :math:`\delta` mentioned in [1]_, it controls how far in time we can go in order to match a given point from one time series to a point in another time series. If None and `global_constraint` is set to "sakoe_chiba", a radius of 1 is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used. itakura_max_slope : float or None (default: None) Maximum slope for the Itakura parallelogram constraint. If None and `global_constraint` is set to "itakura", a maximum slope of 2. is used. If both `sakoe_chiba_radius` and `itakura_max_slope` are set, `global_constraint` is used to infer which constraint to use among the two. In this case, if `global_constraint` corresponds to no global constraint, a `RuntimeWarning` is raised and no global constraint is used.

### Goal
Compute the Longest Common Subsequence (LCSS) similarity and alignment path between two time series using a specified distance metric or a precomputed distance matrix.

### Parameters
- `s1`: array-like. A time series of shape `(sz1, d)` or `(sz1,)`. If `metric="precomputed"`, this must instead be a 2D distance matrix of shape `(sz1, sz2)`.
- `s2`, default `None`: array-like, optional. A second time series of shape `(sz2, d)` or `(sz2,)`. This is only allowed if `metric != "precomputed"`.
- `eps`, default `1`: float. The maximum matching distance threshold. Points are considered a match if their pairwise distance is less than or equal to this value.
- `metric`, default `'euclidean'`: string or callable. The function or string identifier (e.g., `"sqeuclidean"`, `"hamming"`) used to compute pairwise distances. If `"precomputed"`, `s1` is treated as the distance matrix. If a callable, it must take two 1D arrays and return a scalar distance.
- `global_constraint`, default `None`: string (`"itakura"` or `"sakoe_chiba"`) or `None`. Restricts the admissible alignment paths.
- `sakoe_chiba_radius`, default `None`: int or `None`. The radius for the Sakoe-Chiba band constraint. If `None` and `global_constraint="sakoe_chiba"`, defaults to 1.
- `itakura_max_slope`, default `None`: float or `None`. The maximum slope for the Itakura parallelogram constraint. If `None` and `global_constraint="itakura"`, defaults to 2.0.
- `be`, default `None`: Backend identifier (e.g., `"numpy"`, `"pytorch"`) or backend instance to execute the computations.
- `**kwds`: Additional keyword arguments passed to the underlying metric function.

### Input
- When `metric != "precomputed"`, `s1` and `s2` must be 1D or 2D arrays representing individual time series. They can have different lengths (`sz1` and `sz2`) but must share the same feature dimensionality `d`.
- When `metric == "precomputed"`, `s1` must be a 2D array of shape `(sz1, sz2)` representing pairwise distances, and `s2` must be omitted or `None`.

### Output
Returns `unspecified` — A tuple `(path, similarity)`. `path` is a list of integer index pairs `[(i_0, j_0), (i_1, j_1), ...]` representing the matched subsequence. `similarity` is a float representing the percentage of the LCSS length relative to the length of the shortest time series.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics
from scipy.spatial.distance import cdist

# 1. Using a string metric
s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [4.0], [3.0]])

path, sim = tslearn.metrics.lcss_path_from_metric(
    s1, s2, metric="sqeuclidean", eps=1.0
)
assert isinstance(path, list)
assert isinstance(sim, float)
print(f"Path: {path}, Similarity: {sim}")

# 2. Using a precomputed distance matrix
dist_matrix = cdist(s1, s2, metric="sqeuclidean")
path_pre, sim_pre = tslearn.metrics.lcss_path_from_metric(
    dist_matrix, metric="precomputed", eps=1.0
)
assert path == path_pre
assert sim == sim_pre

# 3. Using a custom callable metric
def custom_sqeuclidean(x, y):
    return sum((x - y) ** 2)

path_custom, sim_custom = tslearn.metrics.lcss_path_from_metric(
    s1, s2, metric=custom_sqeuclidean, eps=1.0
)
assert path == path_custom
```

### LLM Instruction Prompt
- When calling `lcss_path_from_metric`, remember that it returns a tuple of `(path, similarity)`.
- If `metric="precomputed"`, you MUST pass the distance matrix as `s1` and leave `s2` as `None`.
- If `metric != "precomputed"`, `s1` and `s2` must have the same feature dimension `d` (the second axis).
- Do not pass 3D dataset arrays `(n_ts, max_sz, d)` to this function; it expects individual time series `(sz, d)` or `(sz,)`.

### Prompt Snippet
```text
Calculate the LCSS path and similarity between two time series `ts_a` and `ts_b` using the squared euclidean distance and an epsilon threshold of 0.5.
```

### Common Failure Modes
- Passing `s2` when `metric="precomputed"`, which violates the precondition that `s1` alone represents the pairwise distances.
- Passing 3D arrays (e.g., `shape=(1, 10, 1)`) instead of 2D or 1D arrays, causing distance computation failures.
- Providing time series `s1` and `s2` with mismatched feature dimensions (e.g., `s1` has `d=2` and `s2` has `d=3`).
- Setting both `sakoe_chiba_radius` and `itakura_max_slope` without explicitly setting `global_constraint`, which raises a `RuntimeWarning` and disables global constraints.

### Fix Code Hint
```python
# BAD: Passing 3D arrays or passing s2 with precomputed metric
# path, sim = tslearn.metrics.lcss_path_from_metric(dist_matrix, s2, metric="precomputed")

# GOOD: Pass only the distance matrix as s1 when using "precomputed"
path, sim = tslearn.metrics.lcss_path_from_metric(dist_matrix, metric="precomputed", eps=0.5)

# GOOD: Pass 2D arrays for standard metrics
path, sim = tslearn.metrics.lcss_path_from_metric(ts_a, ts_b, metric="sqeuclidean", eps=0.5)
```

## API Test: `list_cached_datasets`

### Signature
```python
def list_cached_datasets(self)
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:236_

_Source doc:_ List datasets from the UCR/UEA archive that are available in cache. Examples -------- >>> beetlefly = UCR_UEA_datasets().load_dataset("BeetleFly") >>> l = UCR_UEA_datasets().list_cached_datasets() >>> "BeetleFly" in l True

### Goal
List the names of UCR/UEA time-series datasets that have been downloaded and are currently available in the local cache directory.

### Parameters
- `self`: An instantiated `UCR_UEA_datasets` object that manages the local dataset cache and directory paths.

### Input
No additional arguments are required. The method relies on the `root_dir` configured when the `UCR_UEA_datasets` instance was created (which defaults to a standard `tslearn` data home directory).

### Output
Returns `unspecified` — A list of strings, where each string is the name of a dataset currently present in the local cache directory.

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Initialize the dataset loader
data_loader = UCR_UEA_datasets()

# Load the checked-in Trace fixture to ensure it is cached
data_loader.load_dataset("Trace")

# Retrieve the list of cached datasets
cached_datasets = data_loader.list_cached_datasets()

assert isinstance(cached_datasets, list)
assert "Trace" in cached_datasets
print(f"Found {len(cached_datasets)} cached datasets, including 'Trace'.")
```

### LLM Instruction Prompt
- Call `list_cached_datasets()` on an instance of `UCR_UEA_datasets` to retrieve a list of locally cached dataset names.
- Do not pass any arguments to this method.
- Do not call this as a module-level function; it is an instance method.

### Prompt Snippet
```text
Use `UCR_UEA_datasets().list_cached_datasets()` to check which UCR/UEA datasets are already downloaded to the local cache. It returns a list of dataset name strings.
```

### Common Failure Modes
- Calling `list_cached_datasets()` as a standalone function or a static method on the class, which raises a `TypeError` or `NameError`.
- Passing arguments to the method, which takes only `self`.
- Expecting the method to return the actual dataset arrays rather than just their string names.

### Fix Code Hint
```python
# WRONG: Calling as a static method or standalone function
# cached = UCR_UEA_datasets.list_cached_datasets()
# cached = list_cached_datasets()

# RIGHT: Calling on an instance
from tslearn.datasets import UCR_UEA_datasets
loader = UCR_UEA_datasets()
cached_names = loader.list_cached_datasets()
```

## API Test: `list_datasets`

### Signature
```python
def list_datasets(self)
```
_Source: tslearn/tslearn/datasets/cached.py:26  (+1 more definition site/overload)_

_Source doc:_ List cached datasets. Examples -------- >>> from tslearn.datasets import CachedDatasets >>> cached = CachedDatasets().list_datasets() >>> "Trace" in cached True Returns ------- list of str: A list of names of all cached (univariate and multivariate) dataset names.

### Goal
Retrieves a list of all locally cached (univariate and multivariate) time-series dataset names bundled with the library.

### Parameters
- `self`: The `CachedDatasets` instance on which this method is called.

### Input
This method takes no arguments. The caller must first instantiate the `CachedDatasets` class from `tslearn.datasets`. No network access or external file downloads are required, as it queries the locally bundled cache.

### Output
Returns `unspecified` — A list of strings representing the names of all cached datasets available in the local environment (e.g., `["Trace", ...]`).

### Valid Call Patterns
```python
from tslearn.datasets import CachedDatasets

# Instantiate the data loader
data_loader = CachedDatasets()

# List all available cached datasets
cached = data_loader.list_datasets()

# Verify that the expected 'Trace' dataset is present
assert "Trace" in cached, "The 'Trace' dataset should be in the cached datasets list."
print(f"Successfully found {len(cached)} cached datasets, including 'Trace'.")
```

### LLM Instruction Prompt
- To list available built-in datasets in `tslearn`, you must first instantiate `tslearn.datasets.CachedDatasets` and then call `.list_datasets()` on the instance.
- Do not pass any arguments to `list_datasets()`.
- Do not attempt to call `list_datasets` as a module-level function directly from `tslearn.datasets`.

### Prompt Snippet
```text
To discover locally cached datasets in tslearn, instantiate `CachedDatasets` and call its instance method: `cached_names = CachedDatasets().list_datasets()`. It returns a list of strings, such as "Trace".
```

### Common Failure Modes
- **Calling as a module-level function:** Attempting to call `tslearn.datasets.list_datasets()` directly will result in an `AttributeError` or `ImportError`, as it is an instance method of the `CachedDatasets` class.
- **Providing arguments:** Passing arguments (like a dataset name or filter) to `list_datasets()` will raise a `TypeError` since the method only accepts `self`.

### Fix Code Hint
```python
# BAD: Calling as a module-level function
# from tslearn.datasets import list_datasets
# datasets = list_datasets()

# GOOD: Instantiating CachedDatasets first
from tslearn.datasets import CachedDatasets
datasets = CachedDatasets().list_datasets()
```

## API Test: `list_multivariate_datasets`

### Signature
```python
def list_multivariate_datasets(self)
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:194_

_Source doc:_ List multivariate datasets in the UCR/UEA archive. Examples -------- >>> l = UCR_UEA_datasets().list_multivariate_datasets() >>> "PenDigits" in l True Returns ------- list of str: A list of the names of all multivariate dataset namas.

### Goal
Returns a list of all available multivariate time-series dataset names from the UCR/UEA archive.

### Parameters
- `self`: The `UCR_UEA_datasets` instance on which this method is called.

### Input
No arguments are required. The method must be called on an instantiated `UCR_UEA_datasets` object.

### Output
Returns `unspecified` — A list of strings, where each string is the name of a multivariate dataset available in the UCR/UEA archive (e.g., `"PenDigits"`).

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Inferred from the source documentation example
archive = UCR_UEA_datasets()
multivariate_datasets = archive.list_multivariate_datasets()

assert isinstance(multivariate_datasets, list)
assert "PenDigits" in multivariate_datasets
print(f"Found multivariate datasets, including: {multivariate_datasets[0]}")
```

### LLM Instruction Prompt
- To list available multivariate datasets, you must first instantiate `tslearn.datasets.UCR_UEA_datasets` and then call `.list_multivariate_datasets()` on the instance. Do not call it as a module-level function and do not pass any arguments to it.

### Prompt Snippet
```text
To retrieve the names of multivariate datasets in tslearn:
```python
from tslearn.datasets import UCR_UEA_datasets
dataset_names = UCR_UEA_datasets().list_multivariate_datasets()
```
```

### Common Failure Modes
- **Calling as a module-level function:** Attempting to call `tslearn.datasets.list_multivariate_datasets()` directly will fail with an `AttributeError` or `ImportError`. It is an instance method of the `UCR_UEA_datasets` class.
- **Providing arguments:** The method takes no arguments other than `self`. Passing dataset names or filters will raise a `TypeError`.

### Fix Code Hint
```python
# WRONG: Calling directly from the module
# from tslearn.datasets import list_multivariate_datasets
# names = list_multivariate_datasets()

# RIGHT: Calling on the UCR_UEA_datasets instance
from tslearn.datasets import UCR_UEA_datasets
archive = UCR_UEA_datasets()
names = archive.list_multivariate_datasets()
```

## API Test: `list_univariate_datasets`

### Signature
```python
def list_univariate_datasets(self)
```
_Source: tslearn/tslearn/datasets/ucr_uea.py:174_

_Source doc:_ List univariate datasets in the UCR/UEA archive. Examples -------- >>> l = UCR_UEA_datasets().list_univariate_datasets() >>> len(l) 128 Returns ------- list of str: A list of the names of all univariate datasets.

### Goal
Returns a list of all univariate time-series dataset names available in the UCR/UEA archive.

### Parameters
- `self`: The `UCR_UEA_datasets` instance on which this method is called.

### Input
No arguments are required. The method must be called on an instantiated `UCR_UEA_datasets` object.

### Output
Returns `unspecified` (specifically, a `list` of `str`) — A list containing the string names of all univariate datasets in the UCR/UEA archive.

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Instantiate the dataset loader
loader = UCR_UEA_datasets()

# Retrieve the list of univariate dataset names
univariate_names = loader.list_univariate_datasets()

# Assert falsifiable properties
assert isinstance(univariate_names, list), "Expected a list of dataset names"
assert len(univariate_names) > 0, "Expected at least one dataset name"
assert isinstance(univariate_names[0], str), "Dataset names must be strings"

print(f"Successfully listed {len(univariate_names)} univariate datasets.")
```

### LLM Instruction Prompt
- Always instantiate `UCR_UEA_datasets` before calling `list_univariate_datasets()`. Do not call it as a static method or a module-level function.
- Do not pass any arguments to this method.

### Prompt Snippet
```text
Use `UCR_UEA_datasets().list_univariate_datasets()` to retrieve a list of strings containing the names of all univariate datasets in the UCR/UEA archive.
```

### Common Failure Modes
- **Calling as a module-level function:** Attempting to call `tslearn.datasets.list_univariate_datasets()` directly will fail with an `AttributeError` or `ImportError`. It is an instance method of `UCR_UEA_datasets`.
- **Passing arguments:** Providing arguments to `list_univariate_datasets()` will raise a `TypeError` since it only takes `self`.

### Fix Code Hint
```python
from tslearn.datasets import UCR_UEA_datasets

# WRONG: tslearn.datasets.list_univariate_datasets()
# RIGHT:
loader = UCR_UEA_datasets()
datasets = loader.list_univariate_datasets()
```

## API Test: `load_dataset`

### Signature
```python
def load_dataset(self, dataset_name)
```
_Source: tslearn/tslearn/datasets/cached.py:45  (+1 more definition site/overload)_

_Source doc:_ Load a cached dataset from its name. Parameters ---------- dataset_name : str Name of the dataset. Should be in the list returned by :meth:`~list_datasets`. Returns ------- numpy.ndarray of shape (n_ts_train, sz, d) or None Training time series. None if unsuccessful. numpy.ndarray of integers with shape (n_ts_train, ) or None Training labels. None if unsuccessful. numpy.ndarray of shape (n_ts_test, sz, d) or None Test time series. None if unsuccessful. numpy.ndarray of integers with shape (n_ts_test, ) or None Test labels. None if unsuccessful. Examples -------- >>> data_loader = CachedDatasets() >>> X_train, y_train, X_test, y_test = data_loader.load_dataset( ...                                        "Trace") >>> print(X_train.shape) (100, 275, 1) >>> print(y_train.shape) (100,) Raises ------ IOError If the dataset does not exist or cannot be read.

### Goal
Load a cached time-series dataset by its name, returning the training and testing splits formatted as 3D NumPy arrays and 1D label arrays.

### Parameters
- `self`: An instantiated dataset loader object, such as `UCR_UEA_datasets` or `CachedDatasets`.
- `dataset_name`: A string representing the exact name of the dataset to load (e.g., `"Trace"`).

### Input
The caller must provide a valid dataset name string that exists in the local cache or the loader's registry. To comply with offline constraints and avoid network calls, only use the checked-in `"Trace"` fixture.

### Output
Returns `unspecified` — A 4-tuple containing `(X_train, y_train, X_test, y_test)`. `X_train` and `X_test` are 3D `numpy.ndarray` objects of shape `(n_ts, max_sz, d)`. `y_train` and `y_test` are 1D `numpy.ndarray` objects of integers. If the load is unsuccessful, it returns `None` for each element.

### Valid Call Patterns
```python
from tslearn.datasets import UCR_UEA_datasets

# Instantiate the loader
data_loader = UCR_UEA_datasets()

# Load the offline Trace fixture
X_train, y_train, X_test, y_test = data_loader.load_dataset("Trace")

# Verify the strict 3D array structure (n_ts, max_sz, d)
assert X_train.ndim == 3
assert X_train.shape == (100, 275, 1)
assert y_train.shape == (100,)

print(f"Successfully loaded Trace dataset. X_train shape: {X_train.shape}")
```

### LLM Instruction Prompt
- Call `load_dataset` as an instance method on a dataset loader object (e.g., `UCR_UEA_datasets()`), never as a standalone function.
- Always unpack the return value into exactly four variables: `X_train, y_train, X_test, y_test`.
- Use the `"Trace"` dataset for all executable tests to guarantee offline, deterministic execution without network access.
- Expect the returned `X` arrays to already be in `tslearn`'s strict 3D format `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
Use `tslearn.datasets.UCR_UEA_datasets().load_dataset("Trace")` to load the offline Trace fixture. Unpack the result into `X_train, y_train, X_test, y_test`. The `X` arrays will be 3D NumPy arrays of shape `(n_ts, max_sz, d)`.
```

### Common Failure Modes
- **Calling as a static function:** Attempting to call `tslearn.datasets.load_dataset("Trace")` directly will fail; it must be called on an instance like `UCR_UEA_datasets()`.
- **Incorrect unpacking:** Unpacking into two variables (e.g., `X, y = ...`) will raise a `ValueError` because the method always returns a 4-tuple.
- **Network errors:** Requesting a dataset other than `"Trace"` may trigger a download attempt, violating offline constraints and potentially raising an `IOError` if the network is unreachable.

### Fix Code Hint
```python
# WRONG: Calling as a static function or unpacking incorrectly
# X, y = load_dataset("Trace")

# RIGHT: Instantiate a loader and unpack into 4 variables
from tslearn.datasets import UCR_UEA_datasets
loader = UCR_UEA_datasets()
X_train, y_train, X_test, y_test = loader.load_dataset("Trace")
```

## API Test: `load_dict`

### Signature
```python
def load_dict(filename, group)
```
_Source: tslearn/tslearn/hdftools/hdftools.py:118_

_Source doc:_ Recursively load a dict from an hdf5 group in a file. Parameters ---------- filename : str full path to the hdf5 file group : str Name of the group that contains the dict to load Returns ------- d : dict dict loaded from the specified hdf5 group.

### Goal
Recursively load a dictionary of data (such as NumPy arrays or nested dictionaries) from a specified group within an HDF5 file.

### Parameters
- `filename`: The full string path to the HDF5 file to read from.
- `group`: The string name of the HDF5 group that contains the dictionary to load.

### Input
- An existing HDF5 file at `filename` containing a valid group named `group`. The file is typically created by `tslearn.hdftools.save_dict` or standard `h5py` operations.
- The environment must have the `h5py` package installed to handle HDF5 operations.

### Output
Returns `unspecified` — a Python `dict` loaded from the specified HDF5 group, where keys correspond to HDF5 dataset/group names and values are the stored data (e.g., NumPy arrays).

### Valid Call Patterns
```python
import os
import numpy as np
import tempfile
from tslearn import hdftools

with tempfile.TemporaryDirectory() as tmp_dir:
    fname = os.path.join(tmp_dir, 'hdf_test.hdf5')
    original_dict = {'my_array': np.array([[1.0, 2.0], [3.0, 4.0]])}
    
    # Precondition: file and group must exist
    hdftools.save_dict(original_dict, filename=fname, group='data')
    
    # Load the dictionary
    loaded_dict = hdftools.load_dict(fname, 'data')
    
    assert np.array_equal(original_dict['my_array'], loaded_dict['my_array'])
    print(f"Loaded keys: {list(loaded_dict.keys())}")
```

### LLM Instruction Prompt
- Call `tslearn.hdftools.load_dict(filename, group)` to deserialize a dictionary of arrays from an HDF5 file.
- Ensure the target HDF5 file exists and contains the specified group before calling.
- Expect a Python `dict` as the return value.

### Prompt Snippet
```text
To load a dictionary of NumPy arrays from an HDF5 file in tslearn, use `tslearn.hdftools.load_dict(filename, group)`. The file must exist and contain the specified group.
```

### Common Failure Modes
- **File Not Found**: Calling `load_dict` on a `filename` that does not exist raises an error from the underlying HDF5 library.
- **Missing Group**: Providing a `group` name that does not exist within the HDF5 file will cause a `KeyError` or HDF5 error.
- **Missing Dependency**: Fails if `h5py` is not installed in the environment.

### Fix Code Hint
```python
import os
from tslearn import hdftools

# Ensure the file exists before attempting to load
if os.path.exists(fname):
    try:
        # The group name must exactly match the one used during saving
        d2 = hdftools.load_dict(fname, group='data')
    except KeyError:
        print("Group 'data' not found in the HDF5 file.")
```

## API Test: `load_time_series_txt`

### Signature
```python
def load_time_series_txt(fname)
```
_Source: tslearn/tslearn/utils/utils.py:393_

_Source doc:_ Loads a time series dataset from disk. Parameters ---------- fname : string Path to the file from which time series should be read. Returns ------- numpy.ndarray or array of numpy.ndarray The dataset of time series. Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4], [1, 2, 3]]) >>> save_time_series_txt("tmp-tslearn-test.txt", dataset) >>> reloaded_dataset = load_time_series_txt("tmp-tslearn-test.txt") See Also -------- save_time_series_txt : Save time series to disk

### Goal
Loads a time-series dataset from a text file on disk into a NumPy array structure.

### Parameters
- `fname`: string. The file path from which the time-series data should be read.

### Input
A valid string path pointing to an existing text file containing time-series data. The file should be formatted correctly, typically space-separated and previously exported via `tslearn.utils.save_time_series_txt`.

### Output
Returns `numpy.ndarray` or array of `numpy.ndarray` — The dataset of time series. For equal-length series, this is typically a 3D array of shape `(n_ts, max_sz, d)`. For variable-length series, it may be a 1D object array containing individual 2D arrays.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.utils import to_time_series_dataset, save_time_series_txt, load_time_series_txt

# 1. Create a deterministic in-memory derivative
raw_data = [[1.0, 2.0, 3.0], [1.0, 2.0]]
dataset = to_time_series_dataset(raw_data)

# 2. Save to a temporary file
fd, fname = tempfile.mkstemp(suffix=".txt")
os.close(fd)

try:
    save_time_series_txt(fname, dataset)
    
    # 3. Load the time series from disk
    reloaded_dataset = load_time_series_txt(fname)
    
    # 4. Assert falsifiable property
    assert len(reloaded_dataset) == 2, "Dataset should contain 2 time series"
    print(f"Successfully loaded dataset with {len(reloaded_dataset)} series.")
finally:
    os.remove(fname)
```

### LLM Instruction Prompt
- Use `tslearn.utils.load_time_series_txt` to read time-series datasets from text files on disk.
- Pass the file path as a string to the `fname` parameter.
- Expect the output to be a `numpy.ndarray` (typically 3D `(n_ts, max_sz, d)`) or an array of `numpy.ndarray`s for variable-length series.
- If the loaded data is not guaranteed to be in the strict 3D format required by `tslearn` estimators, pass the result through `to_time_series_dataset` to ensure proper padding and dimensionality.

### Prompt Snippet
```text
tslearn.utils.load_time_series_txt(fname)
Loads a time series dataset from a text file. Returns a numpy.ndarray or an array of numpy.ndarray. Ensure the file exists and is formatted correctly (e.g., created by save_time_series_txt).
```

### Common Failure Modes
- **`FileNotFoundError`**: The specified `fname` does not exist on disk.
- **Parsing Errors / `ValueError`**: The text file is not in the expected space-separated format, or it contains non-numeric values (like CSV headers) that cannot be parsed into floats.
- **Dimensionality Mismatch**: Attempting to pass the loaded raw array directly to estimators without ensuring it is in the strict `(n_ts, max_sz, d)` 3D format. While `load_time_series_txt` usually handles this if saved properly, variable-length series might load as an array of arrays.

### Fix Code Hint
```python
import os
from tslearn.utils import load_time_series_txt, to_time_series_dataset

fname = "my_timeseries_data.txt"
if os.path.exists(fname):
    # Load the data from disk
    raw_loaded = load_time_series_txt(fname)
    
    # Ensure it is in the strict 3D format (n_ts, max_sz, d) required by tslearn estimators
    X = to_time_series_dataset(raw_loaded)
```

## API Test: `locate`

### Signature
```python
def locate(self, X)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:625_

_Source doc:_ Compute shapelet match location for a set of time series. Parameters ---------- X : array-like of shape=(n_ts, sz, d) Time series dataset. Returns ------- array of shape=(n_ts, n_shapelets) Location of the shapelet matches for the provided time series. Examples -------- >>> from tslearn.generators import random_walk_blobs >>> X = numpy.zeros((3, 10, 1)) >>> X[0, 4:7, 0] = numpy.array([1, 2, 3]) >>> y = [1, 0, 0] >>> # Data is all zeros except a motif 1-2-3 in the first time series >>> clf = LearningShapelets(n_shapelets_per_size={3: 1}, max_iter=1, ...                     verbose=0) >>> _ = clf.fit(X, y) >>> weights_shapelet = [ ...     numpy.array([[[1], [2], [3]]]) ... ] >>> clf.set_weights(weights_shapelet, layer_name="shapelets_0") >>> clf.locate(X) array([[4], [0], [0]])

### Goal
Compute the starting index (location) of the best match for each learned shapelet within a set of time series.

### Parameters
- `self`: A fitted `LearningShapelets` estimator instance.
- `X`: A 3D array-like of shape `(n_ts, sz, d)` representing the time-series dataset to search for shapelet matches.

### Input
The input `X` must be a strictly formatted 3D array `(n_ts, max_sz, d)`. If starting from raw lists or 1D/2D arrays, it must be converted using `tslearn.utils.to_time_series_dataset`. The `LearningShapelets` estimator (`self`) must have already been fitted on training data using `.fit()`.

### Output
Returns `unspecified` — A NumPy array of shape `(n_ts, n_shapelets)` containing the integer indices representing the starting location of the best match for each shapelet in each provided time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets import LearningShapelets
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data
time_series = to_time_series_dataset([[1, 2, 3, 4, 5], [3, 2, 1]])
y = [0, 1]

# 2. Initialize and fit the LearningShapelets estimator
clf = LearningShapelets(
    n_shapelets_per_size={2: 1},
    max_iter=10,
    verbose=0,
    random_state=0
)
clf.fit(time_series, y)

# 3. Locate the shapelets in the time series
predicted_locations = clf.locate(time_series)

assert predicted_locations.shape == (2, 1)
print(f"Shapelet locations:\n{predicted_locations}")
```

### LLM Instruction Prompt
- When calling `locate` on a `LearningShapelets` instance, ensure the estimator has already been fitted using `.fit()`.
- Ensure the input `X` is strictly formatted as a 3D array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to guarantee this shape before passing data to `locate`.

### Prompt Snippet
```text
To find where shapelets occur in your data, first fit the `LearningShapelets` model, ensure your data is a 3D array `(n_ts, sz, d)`, and then call `clf.locate(X)`. It returns an array of shape `(n_ts, n_shapelets)` with the starting indices of the matches.
```

### Common Failure Modes
- **Not fitting the model first:** Calling `locate` before `fit` will raise a `NotFittedError` because the shapelets have not been learned or initialized yet.
- **Incorrect input dimensions:** Passing a 1D or 2D array (e.g., `(n_ts, sz)`) instead of the required 3D array `(n_ts, sz, d)` will cause shape mismatch errors during distance computation.
- **Variable-length series without padding:** Passing a raw list of lists of different lengths directly to `locate` will fail; they must be padded with `nan` into a uniform 3D array using `to_time_series_dataset`.

### Fix Code Hint
```python
# WRONG: Passing 2D data or calling locate before fit
# clf = LearningShapelets(...)
# locations = clf.locate(X_2d)

# RIGHT: Format to 3D, fit, then locate
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
clf.fit(X_3d, y)
locations = clf.locate(X_3d)
```

## API Test: `mae`

### Signature
```python
def mae(y_true, y_pred, ts_weights=None, timestamps_weights=None, multioutput='uniform_average')
```
_Source: tslearn/tslearn/metrics/performance.py:12_

_Source doc:_ Mean absolute error (MAE) MAE is a measure of the prediction accuracy for forecasting and regression tasks that computes the average of the deviations between ground truth and predicted values. Parameters ---------- y_true: array like, shape (n_ts, sz, d) Target dataset of ground_truth values y_pred: array like, shape (n_ts, sz, d) Estimated dataset of predicted values ts_weights: array like, shape (n_ts,) or None (default: None) Weights to apply to the time-series in the datasets if non-uniform. Use none for uniform weights. timestamps_weights: array like, shape (sz,) or None (default: None) Weights to apply to the timestamps of each-time series if non-uniform. Use none for uniform weights. multioutput: {'uniform_average', 'raw_values'} or array-like, shape (d,) (default: 'uniform_average') for multivariate timeseries, defines the aggregation of per feature results, if any. 'raw_values': no aggregation, result is per feature 'uniform_average': errors of all features are averaged with uniform weights array-like: errors of all features are averaged using the given weights Returns ------- float or array-like, shape (d,) If multioutput is ‘raw_values’, then mean absolute error is returned for each feature. Otherwise, the average of each feature is returned.

### Goal
Compute the Mean Absolute Error (MAE) between ground truth and predicted time-series datasets to measure prediction accuracy for forecasting and regression tasks.

### Parameters
- `y_true`: Target dataset of ground-truth values. Expected to be an array-like of shape `(n_ts, sz, d)`.
- `y_pred`: Estimated dataset of predicted values. Expected to be an array-like of shape `(n_ts, sz, d)`.
- `ts_weights`, default `None`: Weights to apply to each time-series in the dataset if non-uniform. Expected to be an array-like of shape `(n_ts,)` or `None` for uniform weights.
- `timestamps_weights`, default `None`: Weights to apply to the timestamps of each time-series if non-uniform. Expected to be an array-like of shape `(sz,)` or `None` for uniform weights.
- `multioutput`, default `'uniform_average'`: Defines the aggregation of per-feature results for multivariate time series. Can be `'uniform_average'` (average all features), `'raw_values'` (return per-feature errors without aggregation), or an array-like of shape `(d,)` specifying custom weights for each feature.

### Input
Both `y_true` and `y_pred` must be array-like structures representing time-series datasets. While raw nested lists are accepted, it is highly recommended to format them as strict 3D `numpy` arrays of shape `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`. The shapes of `y_true` and `y_pred` must be compatible.

### Output
Returns `unspecified` — A `float` representing the aggregated mean absolute error across all features and samples, or an array-like of shape `(d,)` containing the MAE for each individual feature if `multioutput='raw_values'` is specified.

### Valid Call Patterns
```python
from tslearn.metrics import performance
import numpy as np

# 2 time series, 3 timestamps, 2 dimensions
y_true = [
    [[1, 2], [2, 3], [3, 4]],
    [[1, 2], [2, 3], [3, 4]]
]
y_pred = [
    [[1, 2], [2, 3], [3, 4]],
    [[0, 1], [1, 2], [2, 3]]
]

# 1. Standard uniform average MAE
mae_val = performance.mae(y_true, y_pred)
assert mae_val == 0.5, f"Expected MAE of 0.5, got {mae_val}"

# 2. MAE with per-feature raw values
mae_raw = performance.mae(y_true, y_pred, multioutput="raw_values")
np.testing.assert_almost_equal(mae_raw, [0.5, 0.5])

# 3. MAE with custom timestamp weights
mae_ts_weighted = performance.mae(y_true, y_pred, timestamps_weights=[0, 1, 0])
assert mae_ts_weighted == 0.5

print("MAE calculations succeeded.")
```

### LLM Instruction Prompt
- When computing the Mean Absolute Error for time-series forecasting or regression in `tslearn`, use `tslearn.metrics.performance.mae(y_true, y_pred)`.
- Ensure `y_true` and `y_pred` have matching shapes, ideally formatted as 3D arrays `(n_ts, sz, d)`.
- To retrieve per-feature errors instead of a single aggregated float, pass `multioutput='raw_values'`.
- You can apply custom weighting to samples, timestamps, or features using `ts_weights`, `timestamps_weights`, and `multioutput` respectively.

### Prompt Snippet
```text
from tslearn.metrics import performance
from tslearn.utils import to_time_series_dataset

y_true_3d = to_time_series_dataset(y_true)
y_pred_3d = to_time_series_dataset(y_pred)

# Compute aggregated MAE
mae_score = performance.mae(y_true_3d, y_pred_3d)

# Compute per-feature MAE
mae_per_feature = performance.mae(y_true_3d, y_pred_3d, multioutput="raw_values")
```

### Common Failure Modes
- Passing inputs with mismatched shapes for `y_true` and `y_pred`.
- Providing `ts_weights` with a length that does not match the number of time series `n_ts`.
- Providing `timestamps_weights` with a length that does not match the number of timestamps `sz`.
- Providing a `multioutput` array with a length that does not match the feature dimension `d`.

### Fix Code Hint
```python
# Ensure inputs are properly formatted 3D arrays and weights match the respective dimensions
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import performance

y_true_3d = to_time_series_dataset(y_true)
y_pred_3d = to_time_series_dataset(y_pred)

# Verify shapes match before calling mae
assert y_true_3d.shape == y_pred_3d.shape
mae_score = performance.mae(y_true_3d, y_pred_3d)
```

## API Test: `mase`

### Signature
```python
def mase(y_true, y_pred, train_data, seasonal_period=1, ts_weights=None, timestamps_weights=None, multioutput='uniform_average')
```
_Source: tslearn/tslearn/metrics/performance.py:153_

_Source doc:_ Mean absolute scaled error (MASE) MASE is a measure of the prediction accuracy for forecasting and regression tasks that computes the scaled average of the deviations between ground truth and predicted values. The scaling factor is computed as the MAE of the naive m-seasonal forecast on the in-sample dataset. Parameters ---------- y_true: array like, shape (n_ts, sz, d) Target dataset of ground_truth values y_pred: array like, shape (n_ts, sz, d) Estimated dataset of predicted values train_data: array like the in-sample dataset, used to compute the scaling factor seasonal_period: int (default: 1) seasonal period used to compute the scaling factor ts_weights: array like, shape (n_ts,) or None (default: None) Weights to apply to the time-series in the datasets if non-uniform. Use none for uniform weights. timestamps_weights: array like, shape (sz,) or None (default: None) Weights to apply to the timestamps of each-time series if non-uniform. Use none for uniform weights. multioutput: {'uniform_average', 'raw_values'} or array-like, shape (d,) (default: 'uniform_average') for multivariate timeseries, defines the aggregation of per feature results, if any. 'raw_values': no aggregation, result is per feature 'uniform_average': errors of all features are averaged with uniform weights array-like: errors of all features are averaged using the given weights Returns ------- float or array-like, shape (d,) If multioutput is ‘raw_values’, then mean squared error is returned for each feature. Otherwise, the average of each feature is returned.

### Goal
Compute the Mean Absolute Scaled Error (MASE) for forecasting tasks, which scales the mean absolute error of predictions by the mean absolute error of a naive m-seasonal forecast on the training data.

### Parameters
- `y_true`: Array-like of shape `(n_ts, sz, d)`. The ground-truth target values.
- `y_pred`: Array-like of shape `(n_ts, sz, d)`. The estimated predicted values.
- `train_data`: Array-like. The in-sample training dataset used to compute the naive forecast scaling factor.
- `seasonal_period`, default `1`: `int`. The seasonal period `m` used to compute the naive m-seasonal forecast scaling factor.
- `ts_weights`, default `None`: Array-like of shape `(n_ts,)` or `None`. Weights to apply to each time series. `None` implies uniform weights.
- `timestamps_weights`, default `None`: Array-like of shape `(sz,)` or `None`. Weights to apply to each timestamp. `None` implies uniform weights.
- `multioutput`, default `'uniform_average'`: `{'uniform_average', 'raw_values'}` or array-like of shape `(d,)`. Defines how to aggregate errors across the feature dimension `d`.

### Input
- `y_true`, `y_pred`, and `train_data` should be array-like, ideally formatted as 3D NumPy arrays `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`.
- `y_true` and `y_pred` must have identical shapes.
- `train_data` must have enough timestamps to compute the naive forecast for the given `seasonal_period` (i.e., length > `seasonal_period`).

### Output
Returns `unspecified` — A `float` representing the aggregated scaled prediction error, or an array of shape `(d,)` containing the MASE for each feature dimension if `multioutput='raw_values'`.

### Valid Call Patterns
```python
from tslearn.metrics.performance import mase
import numpy as np

# 3D arrays: (n_ts, sz, d)
y_train = np.array([[[3, 4], [5, 5], [5, 6], [6, 7], [7, 8]]])
y_true = np.array([[[1, 2], [2, 3], [3, 4]]])
y_pred = np.array([[[0, 1], [1, 2], [2, 3]]])

# Compute MASE with a seasonal period of 1
error = mase(y_true, y_pred, y_train, seasonal_period=1)
assert error == 1.0

# Compute MASE returning raw values per feature dimension
raw_errors = mase(y_true, y_pred, y_train, seasonal_period=1, multioutput="raw_values")
np.testing.assert_allclose(raw_errors, [1.0, 1.0])
```

### LLM Instruction Prompt
- Always provide `train_data` to compute the scaling factor; it is a required positional argument.
- Ensure `train_data` has sufficient length for the specified `seasonal_period`.
- Handle potential `np.inf` returns and `RuntimeWarning`s if the naive forecast on `train_data` perfectly predicts the training set (zero MAE), which causes division by zero.
- Pass 3D arrays `(n_ts, sz, d)` for `y_true`, `y_pred`, and `train_data` to adhere to `tslearn` conventions.

### Prompt Snippet
```text
from tslearn.metrics.performance import mase

# Calculate MASE using the training data to scale the error
mase_score = mase(
    y_true=y_test, 
    y_pred=predictions, 
    train_data=y_train, 
    seasonal_period=12
)
```

### Common Failure Modes
- Passing `train_data` where all values are identical or the naive forecast has zero error. This raises a `RuntimeWarning` for division by zero and returns `np.inf`.
- Passing `train_data` with fewer timestamps than the `seasonal_period`, making it impossible to compute the naive forecast scaling factor.
- Providing `y_true` and `y_pred` with mismatched shapes, which will fail during the unscaled MAE computation.

### Fix Code Hint
```python
# Ensure train_data has variance and is long enough for the seasonal_period
if len(train_data[0]) <= seasonal_period:
    raise ValueError("train_data must be longer than seasonal_period")

# Catch division by zero if the naive forecast on train_data has 0 error
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", message="divide by zero")
    error = mase(y_true, y_pred, train_data, seasonal_period=seasonal_period)
    if np.isinf(error):
        error = 0.0 # or handle the perfect-training-forecast edge case
```

## API Test: `mse`

### Signature
```python
def mse(y_true, y_pred, ts_weights=None, timestamps_weights=None, multioutput='uniform_average')
```
_Source: tslearn/tslearn/metrics/performance.py:83_

_Source doc:_ Mean squared error (MSE) MSE is a measure of the prediction accuracy for forecasting and regression tasks that computes the average of the squared deviations between ground truth and predicted values. Parameters ---------- y_true: array like, shape (n_ts, sz, d) Target dataset of ground_truth values y_pred: array like, shape (n_ts, sz, d) Estimated dataset of predicted values ts_weights: array like, shape (n_ts,) or None (default: None) Weights to apply to the time-series in the datasets if non-uniform. Use none for uniform weights. timestamps_weights: array like, shape (sz,) or None (default: None) Weights to apply to the timestamps of each-time series if non-uniform. Use none for uniform weights. multioutput: {'uniform_average', 'raw_values'} or array-like, shape (d,) (default: 'uniform_average') for multivariate timeseries, defines the aggregation of per feature results, if any. 'raw_values': no aggregation, result is per feature 'uniform_average': errors of all features are averaged with uniform weights array-like: errors of all features are averaged using the given weights Returns ------- float or array-like, shape (d,) If multioutput is ‘raw_values’, then mean squared error is returned for each feature. Otherwise, the average of each feature is returned.

### Goal
Computes the mean squared error (MSE) between ground truth and predicted time-series datasets for forecasting and regression tasks.

### Parameters
- `y_true`: Target dataset of ground-truth values, array-like of shape `(n_ts, sz, d)`.
- `y_pred`: Estimated dataset of predicted values, array-like of shape `(n_ts, sz, d)`.
- `ts_weights`, default `None`: Weights to apply to the time-series in the datasets if non-uniform, array-like of shape `(n_ts,)`. Use `None` for uniform weights.
- `timestamps_weights`, default `None`: Weights to apply to the timestamps of each time-series if non-uniform, array-like of shape `(sz,)`. Use `None` for uniform weights.
- `multioutput`, default `'uniform_average'`: Defines the aggregation of per-feature results for multivariate time series. Can be `'uniform_average'` (errors of all features are averaged with uniform weights), `'raw_values'` (no aggregation, result is per feature), or array-like of shape `(d,)` (errors of all features are averaged using the given weights).

### Input
- `y_true` and `y_pred` must be array-like, ideally formatted as strict 3D arrays `(n_ts, sz, d)` using `tslearn.utils.to_time_series_dataset`.
- If provided, `ts_weights` must match the number of time series `n_ts`.
- If provided, `timestamps_weights` must match the number of timestamps `sz`.
- If provided as an array, `multioutput` weights must match the number of dimensions `d`.

### Output
Returns `unspecified` — A float representing the averaged mean squared error, or an array-like of shape `(d,)` containing the mean squared error for each feature if `multioutput='raw_values'`.

### Valid Call Patterns
```python
from tslearn.metrics import performance
from tslearn.utils import to_time_series_dataset
import numpy as np

# Format inputs to strict 3D shape (n_ts, sz, d)
y_true = to_time_series_dataset([[1, 2, 3]])
y_pred = to_time_series_dataset([[0, 1, 2]])

# Compute standard MSE
mse_val = performance.mse(y_true, y_pred)
assert mse_val == 1.0

# Compute MSE with timestamp weights
mse_weighted = performance.mse(y_true, y_pred, timestamps_weights=[1, 0, 0])
assert mse_weighted == 1.0

# Compute MSE returning raw values per feature
mse_raw = performance.mse(y_true, y_pred, multioutput="raw_values")
np.testing.assert_almost_equal(mse_raw, [1.0])
```

### LLM Instruction Prompt
- When calling `performance.mse`, ensure `y_true` and `y_pred` are 3D arrays of shape `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to guarantee this format.
- If providing `ts_weights`, ensure its length matches `n_ts`.
- If providing `timestamps_weights`, ensure its length matches `sz`.
- If providing `multioutput` as an array, ensure its length matches `d`.

### Prompt Snippet
```text
Use `tslearn.metrics.performance.mse` to compute the mean squared error between time-series datasets. Ensure inputs are formatted as 3D arrays `(n_ts, sz, d)` using `to_time_series_dataset`. You can apply weights across time series (`ts_weights`), across time steps (`timestamps_weights`), or across features (`multioutput`).
```

### Common Failure Modes
- Passing 1D or 2D arrays without converting them to the strict 3D `(n_ts, sz, d)` format expected by `tslearn`.
- Mismatch in dimensions between `y_true` and `y_pred`.
- Providing `ts_weights` or `timestamps_weights` with lengths that do not match `n_ts` or `sz`, respectively, causing broadcasting errors.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import performance

# Ensure inputs are in the strict 3D format (n_ts, sz, d)
y_true_3d = to_time_series_dataset(y_true)
y_pred_3d = to_time_series_dataset(y_pred)

mse_val = performance.mse(y_true_3d, y_pred_3d)
```

## API Test: `n_iter_`

### Signature
```python
def n_iter_(self)
```
_Source: tslearn/tslearn/svm/svm.py:279  (+1 more definition site/overload)_

### Goal
Retrieves the number of iterations run by the optimization routine to fit the underlying Support Vector Machine (SVM) estimator.

### Parameters
- `self`: A fitted time-series SVM estimator instance (e.g., `TimeSeriesSVC` or `TimeSeriesSVR`).

### Input
The estimator must be fitted first using `.fit(X, y)`, where `X` is a strictly formatted 3D `numpy` array of shape `(n_ts, max_sz, d)` and `y` contains the target labels or values.

### Output
Returns `unspecified` — typically an integer or an array of integers (depending on the underlying `scikit-learn` SVM implementation and multiclass strategy) representing the number of iterations the solver took to converge.

### Valid Call Patterns
```python
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series dataset
X = to_time_series_dataset([[1.0, 2.0], [1.0, 4.0], [9.0, 8.0], [8.0, 9.0]])
y = [0, 0, 1, 1]

# 2. Instantiate and fit the estimator
clf = TimeSeriesSVC(kernel="gak", random_state=42)
clf.fit(X, y)

# 3. Access the fitted property (inferred from scikit-learn conventions)
iterations = clf.n_iter_

assert iterations is not None, "n_iter_ should be populated after fitting"
print(f"SVM optimization iterations: {iterations}")
```

### LLM Instruction Prompt
- Access `n_iter_` as a property (attribute access without parentheses), not as a method, despite its definition as a `def` in the source code (it is decorated with `@property`).
- Ensure the estimator has been successfully fitted with `.fit(X, y)` before attempting to access `n_iter_`, or it will raise an error.
- Ensure the input `X` provided to `.fit()` is strictly a 3D array of shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
Access the `n_iter_` property on a fitted `TimeSeriesSVC` or `TimeSeriesSVR` to inspect the number of solver iterations. Do not call it as a function. Ensure the model is fitted on a 3D array `(n_ts, max_sz, d)` first.
```

### Common Failure Modes
- **`AttributeError` / `NotFittedError`**: Accessing `n_iter_` before calling `.fit()` will fail because the underlying `scikit-learn` SVM estimator has not yet been initialized or fitted.
- **`TypeError: '...' object is not callable`**: Attempting to call `clf.n_iter_()` with parentheses will fail because it is exposed as a property returning an integer or array, not a callable method.
- **`ValueError` during fit**: Failing to format the training data `X` into the required 3D shape `(n_ts, max_sz, d)` before fitting will prevent the model from training, making `n_iter_` inaccessible.

### Fix Code Hint
```python
# BAD: Calling as a method or accessing before fit
clf = TimeSeriesSVC()
# iters = clf.n_iter_()  # TypeError
# iters = clf.n_iter_    # AttributeError (not fitted)

# GOOD: Fit on 3D data first, then access as a property
X_3d = to_time_series_dataset(X_raw)
clf.fit(X_3d, y)
iters = clf.n_iter_
```

## API Test: `ndim`

### Signature
```python
def ndim(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:173  (+1 more definition site/overload)_

### Goal
Returns the number of dimensions of a given array or tensor, abstracting over the active computational backend (NumPy or PyTorch).

### Parameters
- `x`: The input time-series data structure, typically a NumPy array or a PyTorch tensor, whose dimensionality needs to be determined.

### Input
A NumPy array or PyTorch tensor. In `tslearn`, time-series datasets are strictly expected to be formatted as 3D arrays with the shape `(n_ts, max_sz, d)`.

### Output
Returns `unspecified` — An integer representing the number of dimensions of the input `x` (e.g., `3` for a standard `tslearn` time-series dataset).

### Valid Call Patterns
```python
import numpy as np
import torch
from tslearn.backend import instantiate_backend

# Inferred from the signature (not verified)
# Testing with the NumPy backend
be_np = instantiate_backend("numpy")
x_np = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])
dims_np = be_np.ndim(x_np)

assert dims_np == 3, f"Expected 3 dimensions, got {dims_np}"
print(f"NumPy backend ndim: {dims_np}")

# Testing with the PyTorch backend
be_pt = instantiate_backend("pytorch")
x_pt = torch.tensor([[[1.0], [2.0]], [[3.0], [4.0]]])
dims_pt = be_pt.ndim(x_pt)

assert dims_pt == 3, f"Expected 3 dimensions, got {dims_pt}"
print(f"PyTorch backend ndim: {dims_pt}")
```

### LLM Instruction Prompt
- When writing backend-agnostic code in `tslearn`, use the backend's `ndim(x)` method rather than accessing the `.ndim` property directly. This ensures compatibility because PyTorch tensors natively use `.dim()` instead of `.ndim`.
- Always ensure the input `x` is already converted to the appropriate backend type (NumPy array or PyTorch tensor) before calling this helper.

### Prompt Snippet
```text
# Inferred from signature
from tslearn.backend import instantiate_backend
be = instantiate_backend("pytorch")
dims = be.ndim(tensor_x)
```

### Common Failure Modes
- **AttributeError on PyTorch Tensors:** Attempting to use `x.ndim` directly on a PyTorch tensor will fail in older PyTorch versions or specific contexts where `.dim()` is required. Using `be.ndim(x)` prevents this.
- **Passing Raw Python Lists:** Passing a standard Python list (e.g., `[[[1, 2]]]\`) to `ndim` may fail or return unexpected results if the backend strictly expects its native array/tensor types.
- **Incorrect Data Formatting:** While `ndim` will return the dimensions of whatever is passed, `tslearn` estimators strictly require 3D arrays `(n_ts, max_sz, d)`. Passing a 1D or 2D array to downstream functions after checking `ndim` will cause failures.

### Fix Code Hint
```python
# Incorrect: Assuming .ndim property exists on all backend types
# dims = x.ndim 

# Correct: Use the backend helper to safely get dimensions
from tslearn.backend import instantiate_backend
be = instantiate_backend(x)
dims = be.ndim(x)

# If dims != 3, reshape or use to_time_series_dataset
if dims != 3:
    from tslearn.utils import to_time_series_dataset
    x = to_time_series_dataset(x)
```

## API Test: `njit_accumulated_matrix`

### Signature
```python
def njit_accumulated_matrix(s1, s2, mask)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:74_

_Source doc:_ Compute the accumulated cost matrix score between two time series. Parameters ---------- s1 : array-like, shape=(sz1, d) First time series. s2 : array-like, shape=(sz2, d) Second time series. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. Returns ------- mat : array-like, shape=(sz1, sz2) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix (e.g., for Dynamic Time Warping) between two individual time series, constrained by a boolean mask.

### Parameters
- `s1`: First time series, expected to be an array-like of shape `(sz1, d)`.
- `s2`: Second time series, expected to be an array-like of shape `(sz2, d)`.
- `mask`: A boolean mask array of shape `(sz1, sz2)` where unconsidered (invalid) cells are `False` and considered cells are `True`.

### Input
The caller must provide two individual time series as 2D NumPy arrays (not 3D dataset arrays) with matching feature dimensions `d`. The `mask` must be a 2D boolean NumPy array whose dimensions exactly match the lengths of `s1` and `s2` (`sz1` and `sz2`, respectively).

### Output
Returns `unspecified` — A 2D NumPy array of shape `(sz1, sz2)` representing the accumulated cost matrix, where each cell contains the cumulative alignment cost up to that point.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import njit_accumulated_matrix

# Inferred from signature
s1 = np.array([[1.0], [2.0], [3.0]]) # shape (3, 1)
s2 = np.array([[2.0], [3.0]])        # shape (2, 1)
mask = np.array([
    [True, True],
    [True, True],
    [True, True]
]) # shape (3, 2)

mat = njit_accumulated_matrix(s1, s2, mask)
assert mat.shape == (3, 2)
print(mat)
```

### LLM Instruction Prompt
- Call `njit_accumulated_matrix` to compute the low-level accumulated cost matrix between two individual time series.
- Do not pass 3D `(n_ts, max_sz, d)` dataset arrays; extract individual 2D `(sz, d)` time series first.
- Always provide a 2D boolean `mask` of shape `(sz1, sz2)` where valid alignment paths are marked `True`.

### Prompt Snippet
```text
Use `tslearn.metrics.dtw_variants.njit_accumulated_matrix` to compute the accumulated cost matrix. Ensure `s1` and `s2` are 2D arrays `(sz, d)` and provide a boolean `mask` of shape `(sz1, sz2)`.
```

### Common Failure Modes
- Passing standard `tslearn` 3D dataset arrays instead of 2D individual time series arrays, causing shape mismatches.
- Providing a `mask` with dimensions that do not match `(len(s1), len(s2))`.
- Using `True` for unconsidered cells and `False` for considered cells (the logic is inverted; `False` means unconsidered).
- Passing PyTorch tensors to this specific Numba-compiled (`njit_`) backend helper, which strictly expects NumPy arrays.

### Fix Code Hint
```python
# FIX: Extract 2D time series from 3D datasets and create a matching boolean mask
s1_2d = X_dataset[0]  # shape (sz1, d)
s2_2d = X_dataset[1]  # shape (sz2, d)

# Create a mask allowing all paths
mask = np.ones((s1_2d.shape[0], s2_2d.shape[0]), dtype=bool)

cost_matrix = njit_accumulated_matrix(s1_2d, s2_2d, mask)
```

## API Test: `njit_accumulated_matrix_from_dist_matrix`

### Signature
```python
def njit_accumulated_matrix_from_dist_matrix(dist_matrix, mask)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:426_

_Source doc:_ Compute the accumulated cost matrix score between two time series using a precomputed distance matrix. Parameters ---------- dist_matrix : array-like, shape=(sz1, sz2) Array containing the pairwise distances. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. Returns ------- mat : array-like, shape=(sz1, sz2) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix score between two time series using a precomputed pairwise distance matrix and a boolean mask, acting as a low-level backend helper for alignment metrics.

### Parameters
- `dist_matrix`: A 2D array-like of shape `(sz1, sz2)` containing the precomputed pairwise distances between the points of two time series.
- `mask`: A 2D array-like of shape `(sz1, sz2)` acting as a boolean mask, where unconsidered cells must have `False` values.

### Input
The caller must provide two 2D NumPy arrays of the exact same shape `(sz1, sz2)`. The `dist_matrix` contains numeric distance values (e.g., floats), and the `mask` contains boolean values restricting the alignment path (such as a Sakoe-Chiba band or Itakura parallelogram).

### Output
Returns `unspecified` — A 2D array-like of shape `(sz1, sz2)` representing the accumulated cost matrix for the allowed alignment paths.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import njit_accumulated_matrix_from_dist_matrix

# Inferred from signature
dist_matrix = np.array([
    [0.0, 1.0, 4.0],
    [1.0, 0.0, 1.0],
    [4.0, 1.0, 0.0]
])
mask = np.array([
    [True, True, False],
    [True, True, True],
    [False, True, True]
])

acc_matrix = njit_accumulated_matrix_from_dist_matrix(dist_matrix, mask)
assert acc_matrix.shape == (3, 3)
print("Accumulated cost matrix computed successfully.")
```

### LLM Instruction Prompt
- When calling `njit_accumulated_matrix_from_dist_matrix`, you MUST provide both a `dist_matrix` and a `mask` of the exact same 2D shape `(sz1, sz2)`.
- The `mask` must be a boolean array where `False` indicates cells that are excluded from the accumulated cost computation.
- Do not pass raw 3D time-series datasets `(n_ts, max_sz, d)` directly to this function; it expects a 2D pairwise distance matrix between exactly two time series.

### Prompt Snippet
```text
Use `tslearn.metrics.dtw_variants.njit_accumulated_matrix_from_dist_matrix(dist_matrix, mask)` to compute the accumulated cost matrix from a precomputed 2D distance matrix and a matching 2D boolean mask. Ensure both inputs are 2D NumPy arrays of identical shape `(sz1, sz2)`.
```

### Common Failure Modes
- Passing 3D time-series arrays `(n_ts, max_sz, d)` instead of a 2D pairwise distance matrix `(sz1, sz2)`.
- Providing a `dist_matrix` and a `mask` with mismatched shapes, which will cause indexing errors in the underlying compiled loop.
- Providing a `mask` containing non-boolean numeric values instead of explicit `True`/`False` values.
- Failing to import the function from its specific internal module (`tslearn.metrics.dtw_variants`), as it is a low-level helper and not exposed at the top level.

### Fix Code Hint
```python
# Ensure inputs are 2D arrays of the same shape and mask is boolean
dist_matrix = np.asarray(dist_matrix, dtype=float)
mask = np.asarray(mask, dtype=bool)
if dist_matrix.ndim != 2 or dist_matrix.shape != mask.shape:
    raise ValueError("dist_matrix and mask must be 2D arrays of the same shape.")
acc_matrix = njit_accumulated_matrix_from_dist_matrix(dist_matrix, mask)
```

## API Test: `njit_lcss_accumulated_matrix`

### Signature
```python
def njit_lcss_accumulated_matrix(s1, s2, eps, mask)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2233_

_Source doc:_ Compute the longest common subsequence similarity score between two time series. Parameters ---------- s1 : array-like, shape=(sz1, d) First time series. s2 : array-like, shape=(sz2, d) Second time series. eps : float Matching threshold. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. Returns ------- acc_cost_mat : array-like, shape=(sz1 + 1, sz2 + 1) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) similarity between two time series using a low-level, Numba-accelerated backend helper.

### Parameters
- `s1`: First time series, expected as a 2D array-like of shape `(sz1, d)`.
- `s2`: Second time series, expected as a 2D array-like of shape `(sz2, d)`.
- `eps`: Float representing the matching threshold; points are considered a match if their distance is within this threshold.
- `mask`: Boolean array-like of shape `(sz1, sz2)` where unconsidered cells must have `False` values.

### Input
- `s1` and `s2` must be 2D NumPy arrays representing individual time series (time steps, dimensions). They must not be 1D arrays or 3D dataset arrays `(n_ts, sz, d)`.
- `eps` must be a standard Python `float`.
- `mask` must be a 2D boolean NumPy array matching the lengths of `s1` and `s2`.

### Output
Returns `unspecified` — A 2D NumPy array of shape `(sz1 + 1, sz2 + 1)` representing the accumulated cost matrix for the LCSS computation.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import njit_lcss_accumulated_matrix

# Inferred from signature (not verified)
s1 = np.array([[1.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [2.5], [3.0]])
eps = 0.5
mask = np.ones((3, 4), dtype=bool)

acc_cost_mat = njit_lcss_accumulated_matrix(s1, s2, eps, mask)

assert acc_cost_mat.shape == (4, 5), f"Expected shape (4, 5), got {acc_cost_mat.shape}"
print("Accumulated cost matrix shape:", acc_cost_mat.shape)
```

### LLM Instruction Prompt
- Use `njit_lcss_accumulated_matrix` only when a low-level LCSS accumulated cost matrix is explicitly required.
- Ensure `s1` and `s2` are 2D arrays of shape `(sz1, d)` and `(sz2, d)`. Do not pass 3D dataset arrays.
- Always provide a boolean `mask` of shape `(sz1, sz2)`.

### Prompt Snippet
```text
When calling `njit_lcss_accumulated_matrix`, ensure `s1` and `s2` are 2D arrays of shape `(sz1, d)` and `(sz2, d)`. Provide a float `eps` for the matching threshold and a boolean `mask` of shape `(sz1, sz2)`. The function returns a 2D accumulated cost matrix of shape `(sz1 + 1, sz2 + 1)`.
```

### Common Failure Modes
- Passing 1D arrays or 3D dataset arrays `(n_ts, sz, d)` for `s1` and `s2` instead of 2D arrays `(sz, d)`.
- Providing a `mask` with dimensions that do not match `(sz1, sz2)`.
- Passing a non-boolean mask (e.g., integers or floats), which may cause Numba type-inference errors or unexpected behavior.

### Fix Code Hint
```python
# Ensure inputs are 2D arrays and mask is boolean
s1_2d = np.atleast_2d(s1_raw).reshape(-1, 1) if s1_raw.ndim == 1 else s1_raw
s2_2d = np.atleast_2d(s2_raw).reshape(-1, 1) if s2_raw.ndim == 1 else s2_raw
mask = np.ones((len(s1_2d), len(s2_2d)), dtype=bool)

acc_cost_mat = njit_lcss_accumulated_matrix(s1_2d, s2_2d, eps=0.5, mask=mask)
```

## API Test: `njit_lcss_accumulated_matrix_from_dist_matrix`

### Signature
```python
def njit_lcss_accumulated_matrix_from_dist_matrix(dist_matrix, eps, mask)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:2831_

_Source doc:_ Compute the accumulated cost matrix score between two time series using a precomputed distance matrix. Parameters ---------- dist_matrix : array-like, shape=(sz1, sz2) Array containing the pairwise distances. eps : float (default: 1.) Maximum matching distance threshold. mask : array-like, shape=(sz1, sz2) Mask. Unconsidered cells must have False values. Returns ------- acc_cost_mat : array-like, shape=(sz1 + 1, sz2 + 1) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix for the Longest Common Subsequence (LCSS) metric between two time series using a precomputed pairwise distance matrix and a matching threshold.

### Parameters
- `dist_matrix`: Array-like of shape `(sz1, sz2)` containing the precomputed pairwise distances between the points of two time series.
- `eps`: A float representing the maximum matching distance threshold. Points are considered to match if their distance is less than or equal to this value.
- `mask`: A boolean array-like of shape `(sz1, sz2)` acting as a mask. Cells that should not be considered during the accumulation must have `False` values.

### Input
The caller must provide a 2D numeric array for `dist_matrix` and a 2D boolean array for `mask`. Both arrays must have the exact same shape `(sz1, sz2)`, corresponding to the lengths of the two time series being compared. `eps` must be a numeric scalar (float).

### Output
Returns `unspecified` — An array-like of shape `(sz1 + 1, sz2 + 1)` representing the accumulated cost matrix for the LCSS alignment.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.dtw_variants import njit_lcss_accumulated_matrix_from_dist_matrix

# 1. Prepare a precomputed distance matrix (sz1=2, sz2=3)
dist_matrix = np.array([
    [0.5, 1.2, 0.1], 
    [2.0, 0.3, 1.5]
])

# 2. Define the matching threshold and a full boolean mask
eps = 1.0
mask = np.ones((2, 3), dtype=bool)

# 3. Compute the accumulated cost matrix (inferred from signature)
acc_cost_mat = njit_lcss_accumulated_matrix_from_dist_matrix(dist_matrix, eps, mask)

# The output shape is (sz1 + 1, sz2 + 1)
assert acc_cost_mat.shape == (3, 4)
print(acc_cost_mat)
```

### LLM Instruction Prompt
- Call `njit_lcss_accumulated_matrix_from_dist_matrix` to compute the LCSS accumulated cost matrix from an already computed pairwise distance matrix.
- Ensure that `dist_matrix` and `mask` are 2D arrays with identical shapes `(sz1, sz2)`.
- Provide `eps` as a float to define the maximum distance for two points to be considered a match.
- Note that the returned matrix will have dimensions `(sz1 + 1, sz2 + 1)`.

### Prompt Snippet
```text
When calculating the LCSS accumulated cost matrix using `njit_lcss_accumulated_matrix_from_dist_matrix(dist_matrix, eps, mask)`, ensure `dist_matrix` and `mask` are 2D arrays of the exact same shape `(sz1, sz2)`. The function returns a matrix of shape `(sz1 + 1, sz2 + 1)`.
```

### Common Failure Modes
- **Shape Mismatch:** Passing a `dist_matrix` and `mask` with different shapes will cause indexing errors during the matrix accumulation.
- **Incorrect Dimensionality:** Passing 1D or 3D arrays instead of 2D arrays for the distance matrix or mask.
- **Missing Mask:** Failing to provide the `mask` argument, as it is a required parameter without a default value.
- **Invalid Mask Type:** Providing a numeric array instead of a boolean array for the `mask`, which may lead to unexpected behavior in the unconsidered cells logic.

### Fix Code Hint
```python
# Ensure dist_matrix is 2D and mask is a boolean array of the same shape
dist_matrix = np.atleast_2d(dist_matrix)
mask = np.ones_like(dist_matrix, dtype=bool) # Or apply specific region constraints

acc_cost_mat = njit_lcss_accumulated_matrix_from_dist_matrix(
    dist_matrix=dist_matrix, 
    eps=float(eps), 
    mask=mask
)
```

## API Test: `njit_sakoe_chiba_mask`

### Signature
```python
def njit_sakoe_chiba_mask(sz1, sz2, radius=1)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1487_

_Source doc:_ Compute the Sakoe-Chiba mask. Parameters ---------- sz1 : int The size of the first time series sz2 : int The size of the second time series. radius : int The radius of the band. Returns ------- mask : array-like, shape=(sz1, sz2) Sakoe-Chiba mask. Examples -------- >>> njit_sakoe_chiba_mask(4, 4, 1) array([[ True,  True, False, False], [ True,  True,  True, False], [False,  True,  True,  True], [False, False,  True,  True]]) >>> njit_sakoe_chiba_mask(7, 3, 1) array([[ True,  True, False], [ True,  True,  True], [ True,  True,  True], [ True,  True,  True], [ True,  True,  True], [ True,  True,  True], [False,  True,  True]])

### Goal
Compute a 2D boolean array representing the Sakoe-Chiba band constraint used to restrict the alignment path in Dynamic Time Warping (DTW).

### Parameters
- `sz1`: Integer representing the length (number of time steps) of the first time series.
- `sz2`: Integer representing the length (number of time steps) of the second time series.
- `radius`, default `1`: Integer representing the radius (half-width) of the allowed warping band.

### Input
Scalar integers defining the dimensions of the alignment cost matrix (`sz1`, `sz2`) and the constraint radius. Do not pass the time-series arrays themselves.

### Output
Returns `unspecified` — A 2D boolean NumPy array of shape `(sz1, sz2)` where `True` indicates the cell is within the allowed Sakoe-Chiba band and `False` indicates it is restricted.

### Valid Call Patterns
```python
from tslearn.metrics.dtw_variants import njit_sakoe_chiba_mask

# Inferred from signature and source doc examples
sz1, sz2 = 4, 4
radius = 1
mask = njit_sakoe_chiba_mask(sz1, sz2, radius=radius)

assert mask.shape == (sz1, sz2), "Mask shape must match (sz1, sz2)"
assert mask[0, 0] == True, "Diagonal should be within the band"
assert mask[0, 3] == False, "Cells outside the radius should be False"

print("Sakoe-Chiba Mask:")
print(mask)
```

### LLM Instruction Prompt
- Use `njit_sakoe_chiba_mask` to generate boolean masks for custom DTW implementations or when debugging Sakoe-Chiba global constraints.
- Always pass the integer lengths of the time series, not the time-series arrays themselves.
- The function is a low-level backend helper located in `tslearn.metrics.dtw_variants`.

### Prompt Snippet
```text
When implementing custom constrained DTW logic or visualizing global constraints in `tslearn`, use `tslearn.metrics.dtw_variants.njit_sakoe_chiba_mask(sz1, sz2, radius)`. Pass the integer lengths of the two time series as `sz1` and `sz2`. It returns a boolean NumPy array of shape `(sz1, sz2)` where `True` denotes valid alignment cells.
```

### Common Failure Modes
- Passing the actual 3D or 2D time-series arrays instead of their integer lengths, which will cause a `TypeError` when the function attempts to use them as array dimensions.
- Passing negative integers for `sz1`, `sz2`, or `radius`.

### Fix Code Hint
```python
# BAD: Passing arrays directly
# mask = njit_sakoe_chiba_mask(ts1, ts2, radius=2)

# GOOD: Extracting lengths first
sz1 = ts1.shape[0]
sz2 = ts2.shape[0]
mask = njit_sakoe_chiba_mask(sz1, sz2, radius=2)
```

## API Test: `normal`

### Signature
```python
def normal(loc=0.0, scale=1.0, size=(1,))
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:250_

### Goal
Generates an array or tensor of random numbers drawn from a normal (Gaussian) distribution, utilizing the active computational backend (e.g., PyTorch or NumPy).

### Parameters
- `loc`, default `0.0`: The mean (center) of the normal distribution (numeric scalar).
- `scale`, default `1.0`: The standard deviation (spread) of the normal distribution (numeric scalar).
- `size`, default `(1,)`: The shape of the output array or tensor, provided as a tuple of integers.

### Input
Numeric scalars for `loc` and `scale`, and a tuple of integers for `size`. No specific preconditions other than valid dimensions.

### Output
Returns `unspecified` — A backend-specific data structure (e.g., a PyTorch `Tensor` or NumPy `ndarray`) of the specified `size`, populated with normally distributed random values.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")

# Call form inferred from signature and backend conventions
noise_array = be.normal(loc=0.0, scale=0.1, size=(2, 5, 1))

assert noise_array.shape == (2, 5, 1)
print("Generated normal array shape:", noise_array.shape)
```

### LLM Instruction Prompt
- Call `normal` via an instantiated backend object (e.g., `be.normal(...)`) to generate backend-native random arrays/tensors.
- Always provide `size` as a tuple of integers. To generate time-series data, use the standard `tslearn` 3D shape `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
To generate normally distributed random data in a backend-agnostic manner, instantiate a backend using `tslearn.backend.instantiate_backend` and call its `normal` method: `be.normal(loc=0.0, scale=1.0, size=(n_ts, max_sz, d))`.
```

### Common Failure Modes
- Calling `normal` as a top-level module function (e.g., `tslearn.normal()`) instead of accessing it through a backend instance.
- Passing a scalar instead of a tuple for `size`, which may cause PyTorch backend errors.
- Generating 1D or 2D data and passing it directly to `tslearn` estimators, which strictly require 3D `(n_ts, max_sz, d)` arrays.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend

# 1. Instantiate the backend
be = instantiate_backend("pytorch")

# 2. Call normal on the backend instance with a 3D size tuple
# (n_ts=5, max_sz=50, d=1)
random_ts = be.normal(loc=0.0, scale=1.0, size=(5, 50, 1))
```

## API Test: `normalized_cc`

### Signature
```python
def normalized_cc(s1, s2, norm1=-1.0, norm2=-1.0)
```
_Source: tslearn/tslearn/metrics/cycc.py:10_

_Source doc:_ Normalize cc. Parameters ---------- s1 : array-like, shape=(sz, d), dtype=float64 A time series. s2 : array-like, shape=(sz, d), dtype=float64 Another time series. norm1 : float64, default=-1.0 norm2 : float64, default=-1.0 Returns ------- norm_cc : array-like, shape=(2 * sz - 1), dtype=float64

### Goal
Compute the normalized cross-correlation sequence between two individual time series.

### Parameters
- `s1`: array-like of shape `(sz, d)` and dtype `float64`. A single time series.
- `s2`: array-like of shape `(sz, d)` and dtype `float64`. Another single time series to correlate with `s1`.
- `norm1`, default `-1.0`: float64. The precomputed normalization factor for `s1`. If left as `-1.0`, it is typically computed internally.
- `norm2`, default `-1.0`: float64. The precomputed normalization factor for `s2`. If left as `-1.0`, it is typically computed internally.

### Input
Two individual time series formatted as 2D arrays of shape `(sz, d)` with `float64` data types. Note that both time series are expected to have the exact same length `sz` and dimensionality `d`. Do not pass full 3D datasets `(n_ts, max_sz, d)`.

### Output
Returns `array-like` — an array of shape `(2 * sz - 1)` and dtype `float64` representing the normalized cross-correlation sequence between the two time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cycc import normalized_cc

# Inferred from signature
s1 = np.array([[1.0], [2.0], [3.0]], dtype=np.float64)
s2 = np.array([[2.0], [3.0], [4.0]], dtype=np.float64)

# Compute normalized cross-correlation
norm_cc_result = normalized_cc(s1, s2)

assert norm_cc_result.shape == (5,), "Output shape must be (2 * sz - 1)"
print(norm_cc_result)
```

### LLM Instruction Prompt
- Use `normalized_cc` to compute the normalized cross-correlation sequence between two single time series.
- Ensure `s1` and `s2` are 2D arrays of shape `(sz, d)` and dtype `float64`. Do not pass 3D dataset arrays `(n_ts, max_sz, d)`.
- Both input time series must have the same length `sz` and dimensionality `d`.

### Prompt Snippet
```text
When using `tslearn.metrics.cycc.normalized_cc`, pass two 2D `float64` arrays of shape `(sz, d)` representing individual time series. The function returns a 1D array of shape `(2 * sz - 1)` containing the normalized cross-correlation. Do not pass full 3D datasets.
```

### Common Failure Modes
- Passing a full 3D dataset `(n_ts, max_sz, d)` instead of a single 2D time series `(sz, d)`.
- Passing time series of different lengths, as the signature expects both to have length `sz`.
- Passing integer arrays or other non-`float64` types, which may cause type mismatch errors in the underlying Cython implementation.

### Fix Code Hint
```python
# Extract single time series from a 3D dataset and ensure float64
s1 = X_dataset[0].astype(np.float64)
s2 = X_dataset[1].astype(np.float64)

# Ensure both have the same length before calling
if s1.shape == s2.shape:
    result = normalized_cc(s1, s2)
```

## API Test: `pairwise_distances`

### Signature
```python
def pairwise_distances(X, Y=None, metric='euclidean')
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:177_

### Goal
Computes the pairwise distance matrix between two sets of data using a specified metric, implemented specifically as a PyTorch backend helper to enable automatic differentiation.

### Parameters
- `X`: The first set of data (typically a PyTorch tensor).
- `Y`, default `None`: The second set of data (typically a PyTorch tensor). If `None`, the pairwise distances are computed between the elements of `X` itself.
- `metric`, default `'euclidean'`: A string representing the distance metric to use for the computation.

### Input
Callers must provide PyTorch tensors for `X` (and optionally `Y`). To compute gradients, the input tensors must have `requires_grad=True`. While `tslearn` generally expects 3D arrays `(n_ts, max_sz, d)` for time-series estimators, this low-level backend helper typically operates on 2D tensors `(n_samples, n_features)` mirroring `scikit-learn`'s `pairwise_distances` utility.

### Output
Returns `unspecified` — A PyTorch tensor representing the pairwise distance matrix between the elements of `X` and `Y`. If `X` has shape `(N, ...)` and `Y` has shape `(M, ...)`, the output is an `(N, M)` tensor. If inputs require gradients, the output tensor will be attached to a computation graph.

### Valid Call Patterns
```python
import torch
from tslearn.backend.pytorch_backend import pairwise_distances

# Inferred from signature (no verbatim example provided in context)
X = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
Y = torch.tensor([[1.0, 2.0]])

# Compute pairwise euclidean distances
dist_matrix = pairwise_distances(X, Y, metric='euclidean')

assert dist_matrix.shape == (2, 1), "Distance matrix should be of shape (N, M)"
print(dist_matrix)
```

### LLM Instruction Prompt
- When calling `pairwise_distances` from the PyTorch backend, ensure inputs are PyTorch tensors, not NumPy arrays.
- If gradient computation is required, ensure the input tensors are instantiated with `requires_grad=True`.
- Do not invent unsupported metric strings; stick to standard metrics like `'euclidean'` unless otherwise specified.

### Prompt Snippet
```text
Use `tslearn.backend.pytorch_backend.pairwise_distances` to compute a differentiable distance matrix between two PyTorch tensors. Ensure inputs are tensors and specify `metric='euclidean'`.
```

### Common Failure Modes
- **Missing PyTorch Dependency:** Fails with an `ImportError` if the `pytorch` package is not installed locally, as this function resides in the PyTorch backend module.
- **Type Mismatch:** Passing NumPy arrays or standard Python lists instead of PyTorch tensors may cause backend tensor operations to fail.
- **Shape Mismatch:** Providing `X` and `Y` with incompatible feature dimensions (e.g., different sizes in the last dimension) will result in a PyTorch broadcasting or matrix operation error.
- **Unsupported Metric:** Passing an unrecognized string to `metric` will cause a `ValueError` or `NotImplementedError` during the distance calculation.

### Fix Code Hint
```python
# FIX: Ensure inputs are PyTorch tensors before passing to the PyTorch backend helper
import torch
from tslearn.backend.pytorch_backend import pairwise_distances

X_tensor = torch.as_tensor(X, dtype=torch.float32)
Y_tensor = torch.as_tensor(Y, dtype=torch.float32) if Y is not None else None

distances = pairwise_distances(X_tensor, Y_tensor, metric='euclidean')
```

## API Test: `partial_fit`

### Signature
```python
def partial_fit(self, X, y, *args, **kwargs)
```
_Source: tslearn/tslearn/neural_network/neural_network.py:62  (+1 more definition site/overload)_

_Source doc:_ Update the model with a single iteration over the given data. Parameters ---------- X : array-like, shape (n_ts, sz, d) The input data. y : array-like, shape (n_ts, ) or (n_ts, dim_y) Target values. *args, **kwargs : arguments for the underlying MLPClassifier's method from scikit-learn Returns ------- TimeSeriesMLPClassifier The fitted estimator

### Goal
Update the neural network model with a single iteration over a batch of time-series data, enabling out-of-core or online learning.

### Parameters
- `self`: The estimator instance (e.g., `TimeSeriesMLPClassifier` or `TimeSeriesMLPRegressor`).
- `X`: The input time-series data batch, formatted as a 3D array of shape `(n_ts, sz, d)`.
- `y`: The target values for the batch, formatted as a 1D array of shape `(n_ts, )` or a 2D array `(n_ts, dim_y)`.
- `*args`: Additional positional arguments passed directly to the underlying `scikit-learn` `MLPClassifier.partial_fit` method.
- `**kwargs`: Additional keyword arguments passed directly to the underlying `scikit-learn` `MLPClassifier.partial_fit` method (e.g., `classes`).

### Input
- `X` must be a strictly formatted 3D `numpy` array `(n_ts, sz, d)`. Use `tslearn.utils.to_time_series_dataset` to prepare raw lists or 2D arrays.
- `y` must be an array of target labels or continuous values corresponding to the samples in `X`.
- **Precondition:** For classifiers, the very first call to `partial_fit` MUST include the `classes` keyword argument specifying all possible class labels in the entire dataset, as required by `scikit-learn`.
- **Precondition:** Because `tslearn` flattens the 3D array into `(n_ts, sz * d)` for the underlying `scikit-learn` MLP, the time-series length `sz` must be identical across all batches passed to `partial_fit`.

### Output
Returns `unspecified` — The fitted estimator instance (`self`), allowing for method chaining.

### Valid Call Patterns
```python
# Inferred from signature and scikit-learn conventions
from tslearn.neural_network import TimeSeriesMLPClassifier
from tslearn.utils import to_time_series_dataset
import numpy as np

# 1. Prepare a 3D time-series data batch and targets
X_batch = to_time_series_dataset([[1.0, 2.0], [5.0, 6.0], [1.5, 2.5], [5.5, 6.5]])
y_batch = np.array([0, 1, 0, 1])

# 2. Initialize the classifier
clf = TimeSeriesMLPClassifier(hidden_layer_sizes=(4,), random_state=42)

# 3. Perform a partial fit (requires 'classes' on the first call)
clf.partial_fit(X_batch, y_batch, classes=np.array([0, 1]))

# 4. Verify the model was updated
assert hasattr(clf, "coefs_"), "Model was not fitted"
print(f"Model fitted with {len(clf.coefs_)} weight matrices.")
```

### LLM Instruction Prompt
- When calling `partial_fit` on `tslearn` neural network estimators, ensure `X` is strictly a 3D array `(n_ts, sz, d)`.
- For classifiers, you MUST provide the `classes` keyword argument (an array of all possible class labels) during the very first call to `partial_fit`.
- Ensure that every batch passed to `partial_fit` has the exact same time-series length (`sz`). If batches have different maximum lengths, the flattened feature count will mismatch and crash the underlying `scikit-learn` estimator.

### Prompt Snippet
```text
When using `TimeSeriesMLPClassifier.partial_fit` in tslearn, format `X` as a 3D array `(n_ts, sz, d)`. You must pass `classes=np.unique(all_y)` on the first call. Ensure `sz` is constant across all batches, as the model flattens the time series to `sz * d` features.
```

### Common Failure Modes
- **Missing `classes` argument:** Failing to provide `classes=...` on the first call to `partial_fit` for a classifier raises a `ValueError` from `scikit-learn`.
- **Incorrect Input Shape:** Passing a 2D array for `X` instead of the required 3D array `(n_ts, sz, d)` raises a `ValueError`.
- **Inconsistent Time-Series Lengths Across Batches:** If different batches have different maximum lengths (`sz`), the number of flattened features (`sz * d`) will change between calls, raising a `ValueError` about mismatched feature dimensions.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
import numpy as np

# Ensure X is 3D and padded/truncated to a consistent maximum length across ALL batches
X_batch = to_time_series_dataset(raw_batch) 
# (Optional: pad X_batch to a global max_sz if batches naturally vary in length)

# The first call requires the classes argument
clf.partial_fit(X_batch, y_batch, classes=np.array([0, 1, 2]))
```

## API Test: `pdist`

### Signature
```python
def pdist(x, metric='euclidean', p=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:193_

### Goal
Computes the pairwise distances between observations in an input tensor using the specified metric, serving as a PyTorch backend helper for distance calculations.

### Parameters
- `x`: The input data tensor containing observations (typically a 2D tensor of shape `(n_samples, n_features)`).
- `metric`, default `'euclidean'`: The distance metric to compute (e.g., `'euclidean'`).
- `p`, default `None`: The p-norm for the Minkowski distance metric, if applicable.

### Input
A PyTorch tensor `x` representing a collection of vectors. The tensor should typically be 2D.

### Output
Returns `unspecified` — A PyTorch tensor representing the condensed distance matrix (a 1D tensor of pairwise distances between the observations).

### Valid Call Patterns
```python
import torch

try:
    # Try importing as a standalone module-level function
    from tslearn.backend.pytorch_backend import pdist
    x = torch.tensor([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
    # Inferred from signature
    distances = pdist(x, metric='euclidean')
except ImportError:
    # Fallback to accessing it as a method on the PyTorchBackend instance
    from tslearn.backend.pytorch_backend import PyTorchBackend
    be = PyTorchBackend()
    x = torch.tensor([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
    # Inferred from signature
    distances = be.pdist(x, metric='euclidean')

assert distances.shape == (3,)
assert torch.allclose(distances[0], torch.tensor(5.0))
print("Pairwise distances:", distances)
```

### LLM Instruction Prompt
- Use `pdist` to compute pairwise distances for a PyTorch tensor within the `tslearn` backend system.
- Access it via the PyTorch backend instance (`instantiate_backend("pytorch").pdist`) or import it directly from `tslearn.backend.pytorch_backend`, depending on the specific `tslearn` version's internal structure.
- Ensure the input `x` is a 2D PyTorch tensor; do not pass NumPy arrays directly to the PyTorch backend's `pdist`.

### Prompt Snippet
```text
tslearn.backend.pytorch_backend.pdist computes pairwise distances for PyTorch tensors. It expects a 2D tensor `x` and returns a 1D tensor of condensed distances. It is typically accessed via a PyTorchBackend instance.
```

### Common Failure Modes
- Passing a NumPy array instead of a PyTorch tensor when using the PyTorch backend's `pdist` directly, which will cause PyTorch-specific operations to fail.
- Passing a 1D or 3D tensor instead of a 2D tensor, which may violate the expected input shape for pairwise distance computation.
- Specifying an unsupported metric string that the PyTorch backend cannot resolve.

### Fix Code Hint
```python
import torch
from tslearn.backend import instantiate_backend

# Ensure the backend is instantiated and the input is a PyTorch tensor
be = instantiate_backend("pytorch")
x = torch.tensor([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]], dtype=torch.float32)

# Call pdist through the backend instance
distances = be.pdist(x, metric='euclidean')
```

## API Test: `predict`

### Signature
```python
def predict(self, X)
def predict(self, X=None, n=1)
```
_Source: tslearn/tslearn/forecasting/_arima.py:351  (+12 more definition site/overload)_

_Source doc:_ Forecasts n timestamps of the given data if any, otherwise forecasts n timestamps for the fitted data. Parameters ---------- X : array-like, shape (n_ts, sz, d), optional Time-series dataset to forecast. If None, the fitted data is forecasted otherwise the fitted model is applied to the given data. n : int (default: 1) The number of timestamps to forecast, a.k.a. the horizon. Returns ------- array, shape = (n_ts, n, d) Array of forecasted timestamps

### Goal
Predicts class labels, cluster indices, or future time-series values (forecasts) for the provided dataset using a fitted `tslearn` estimator.

### Parameters
- `self`: A fitted `tslearn` estimator instance (e.g., `TimeSeriesKMeans`, `KNeighborsTimeSeriesClassifier`, or a forecasting model).
- `X`, default `None`: The time-series dataset to predict on, formatted as a 3D array-like of shape `(n_ts, sz, d)`. For forecasting models, if `None`, the model forecasts based on the originally fitted data.
- `n`, default `1`: The number of future timestamps to forecast (the horizon). This parameter is specific to forecasting estimators; classification and clustering estimators typically only accept `X`.

### Input
A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time series. Data must be formatted (e.g., via `tslearn.utils.to_time_series_dataset`) and should match the preprocessing (e.g., scaling) applied to the training data.

### Output
Returns `unspecified` — Returns an array of predictions. For classification and clustering, this is typically a 1D array of shape `(n_ts,)` containing integer labels. For forecasting, it is a 3D array of shape `(n_ts, n, d)` containing the forecasted timestamps.

### Valid Call Patterns
```python
import numpy as np
from tslearn.clustering import TimeSeriesKMeans

# 1. Create deterministic in-memory time-series data (n_ts, max_sz, d)
rng = np.random.RandomState(42)
X_train = rng.randn(5, 10, 1)
X_test = rng.randn(3, 10, 1)

# 2. Initialize and fit the estimator
km = TimeSeriesKMeans(n_clusters=2, metric="euclidean", random_state=rng)
km.fit(X_train)

# 3. Predict cluster labels for new data
predictions = km.predict(X_test)

# 4. Verify the output shape and type
assert predictions.shape == (3,)
assert np.issubdtype(predictions.dtype, np.integer)
print(f"Predicted cluster labels: {predictions}")
```

### LLM Instruction Prompt
- Always ensure `X` is strictly formatted as a 3D array `(n_ts, max_sz, d)` before calling `predict`, even if predicting for a single time series (which should be `(1, max_sz, d)`).
- Do not pass the `n` parameter to classification, clustering, or regression estimators; it is only valid for forecasting models.
- Ensure the estimator has been fitted (e.g., by calling `.fit(X)`) before calling `.predict(X)`.

### Prompt Snippet
```text
Ensure the time-series data is in the 3D format (n_ts, max_sz, d) before calling predict. If you have a list of 1D arrays, use `tslearn.utils.to_time_series_dataset` first. Call `predict(X)` on the fitted estimator.
```

### Common Failure Modes
- **ValueError (Incompatible Dimensions):** Passing a 1D or 2D array instead of the required 3D `(n_ts, max_sz, d)` format.
- **NotFittedError:** Calling `predict` on an estimator instance that has not yet been fitted with training data.
- **TypeError (Unexpected Keyword Argument):** Passing the `n` argument to a non-forecasting estimator (like `TimeSeriesKMeans` or `KNeighborsTimeSeriesClassifier`), which only accepts `X`.

### Fix Code Hint
```python
# FIX: Ensure data is 3D before predicting
from tslearn.utils import to_time_series_dataset

# If X_test is a list of flat lists or 1D arrays:
X_test_formatted = to_time_series_dataset(X_test)

# Call predict on the fitted model
predictions = model.predict(X_test_formatted)
```

## API Test: `predict_class_and_earliness`

### Signature
```python
def predict_class_and_earliness(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:399_

_Source doc:_ Provide predicted class as well as prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. Parameters ---------- X : array-like of shape (n_series, n_timestamps, n_features) Vector to be scored, where `n_series` is the number of time series, `n_timestamps` is the number of timestamps in the series and `n_features` is the number of features recorded at each timestamp. Returns ------- array, shape (n_series,) Predicted classes. array-like of shape (n_series, ) Prediction timestamps.

### Goal
Predict the class labels and the timestamps at which the early classification decision was made for a given time-series dataset.

### Parameters
- `self`: A fitted early classification estimator instance.
- `X`: The time-series dataset to be scored, formatted as a 3D array-like of shape `(n_series, n_timestamps, n_features)`.

### Input
- `X` must be a 3D array-like of shape `(n_series, n_timestamps, n_features)`. If your data is 1D or 2D, it must be reshaped or converted using `tslearn.utils.to_time_series_dataset` prior to calling this method.
- The estimator (`self`) must be fitted before calling this method.

### Output
Returns `unspecified` — A tuple containing two arrays:
1. `predicted_classes` (array of shape `(n_series,)`): The predicted class labels.
2. `prediction_timestamps` (array-like of shape `(n_series,)`): The timestamps at which the prediction was made.

### Valid Call Patterns
```python
# Example inferred from signature (exact estimator class not specified in context)
import numpy as np
from unittest.mock import Mock

# X must be a 3D array: (n_series, n_timestamps, n_features)
X_test = np.zeros((3, 10, 1))

# Mocking a fitted early classification estimator since the exact class is unknown
estimator = Mock()
estimator.predict_class_and_earliness.return_value = (
    np.array([0, 1, 0]), 
    np.array([2, 4, 3])
)

# Call the method
predicted_classes, prediction_timestamps = estimator.predict_class_and_earliness(X_test)

assert predicted_classes.shape == (3,)
assert prediction_timestamps.shape == (3,)
print(f"Predicted classes: {predicted_classes}")
print(f"Prediction timestamps: {prediction_timestamps}")
```

### LLM Instruction Prompt
- When calling `predict_class_and_earliness`, ensure the input `X` is strictly formatted as a 3D array `(n_series, n_timestamps, n_features)`.
- Expect a tuple of two arrays in return: the predicted classes and the timestamps of the early predictions.
- Call this method only on a fitted early classification estimator instance.

### Prompt Snippet
```text
Ensure `X` is a 3D array `(n_series, n_timestamps, n_features)`. `predict_class_and_earliness` returns a tuple `(predicted_classes, prediction_timestamps)`.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D array `(n_series, n_timestamps, n_features)`, which will cause shape mismatch errors.
- Calling the method on an unfitted estimator, resulting in a `NotFittedError`.
- Misinterpreting the return value as a single array rather than a tuple of two arrays, leading to unpacking errors.

### Fix Code Hint
```python
# Ensure X is 3D
if X.ndim == 2:
    X = X[:, :, np.newaxis]
elif X.ndim == 1:
    X = X[np.newaxis, :, np.newaxis]

# Unpack the tuple correctly
predicted_classes, prediction_timestamps = estimator.predict_class_and_earliness(X)
```

## API Test: `predict_log_proba`

### Signature
```python
def predict_log_proba(self, X)
```
_Source: tslearn/tslearn/svm/svm.py:370_

_Source doc:_ Predict class log-probabilities for a given set of time series. Note that probability estimates are not guaranteed to match predict output. See our :ref:`dedicated user guide section <kernels-ml>` for more details. Parameters ---------- X : array-like of shape=(n_ts, sz, d) Time series dataset. Returns ------- array of shape=(n_ts, n_classes), Class probability matrix.

### Goal
Predict class log-probabilities for a given set of time series using a fitted estimator (such as `TimeSeriesSVC`).

### Parameters
- `self`: The fitted classifier instance (e.g., a `TimeSeriesSVC` initialized with `probability=True`).
- `X`: The time series dataset to evaluate, formatted as a 3D array-like of shape `(n_ts, sz, d)`.

### Input
- `X` must be strictly formatted as a 3D `numpy` array of shape `(n_ts, max_sz, d)`. If you have raw lists or variable-length time series, you must convert them first using `tslearn.utils.to_time_series_dataset`.
- The estimator must have been fitted on training data prior to calling this method.
- For SVM-based estimators, the model must have been explicitly initialized with `probability=True` before fitting.

### Output
Returns `unspecified` — A `numpy` array of shape `(n_ts, n_classes)` representing the class log-probability matrix. Values are log-transformed probabilities (typically $\le 0.0$).

### Valid Call Patterns
```python
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset
import numpy as np

# Inferred from signature and scikit-learn conventions
X_train = to_time_series_dataset([[1.0, 2.0], [1.0, 2.0, 3.0], [8.0, 9.0]])
y_train = [0, 0, 1]

# The estimator MUST be initialized with probability=True
clf = TimeSeriesSVC(probability=True, kernel="gak")
clf.fit(X_train, y_train)

X_test = to_time_series_dataset([[1.0, 2.0]])
log_probs = clf.predict_log_proba(X_test)

assert log_probs.shape == (1, 2)
assert np.all(log_probs <= 0.0)
```

### LLM Instruction Prompt
- When calling `predict_log_proba`, ensure the input `X` is a 3D array of shape `(n_ts, max_sz, d)`. Use `to_time_series_dataset` to pad variable-length sequences.
- Ensure the estimator (e.g., `TimeSeriesSVC`) was initialized with `probability=True` before calling `.fit()`, otherwise this method will raise an error.
- Note that probability estimates are not guaranteed to perfectly match the deterministic `.predict()` output.

### Prompt Snippet
```text
Ensure the time-series classifier is initialized with `probability=True` before fitting. Format the test data into a 3D array `(n_ts, max_sz, d)` using `to_time_series_dataset` before passing it to `predict_log_proba`.
```

### Common Failure Modes
- **Not enabling probabilities:** Calling `predict_log_proba` on a `TimeSeriesSVC` that was initialized with the default `probability=False` raises an `AttributeError` or `NotFittedError`.
- **Incorrect Input Shape:** Passing a 2D array `(n_ts, max_sz)` or a raw list of lists instead of the required 3D array `(n_ts, max_sz, d)`.
- **Unfitted Estimator:** Calling `predict_log_proba` before calling `.fit()` raises a `NotFittedError`.

### Fix Code Hint
```python
# 1. Initialize with probability=True
clf = TimeSeriesSVC(probability=True, kernel="gak")
clf.fit(X_train, y_train)

# 2. Ensure X_test is a 3D array
X_test_3d = to_time_series_dataset(X_test_raw)

# 3. Predict log probabilities
log_probs = clf.predict_log_proba(X_test_3d)
```

## API Test: `predict_proba`

### Signature
```python
def predict_proba(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:491  (+4 more definition site/overload)_

_Source doc:_ Probability estimates. The returned estimates for all classes are ordered by the label of classes. Parameters ---------- X : array-like of shape (n_series, n_timestamps, n_features) Vector to be scored, where `n_series` is the number of time series, `n_timestamps` is the number of timestamps in the series and `n_features` is the number of features recorded at each timestamp. Returns ------- array-like of shape (n_series, n_classes) Probability of the sample for each class in the model, where classes are ordered as they are in ``self.classes_``.

### Goal
Compute probability estimates for each class for the provided time-series dataset using a fitted classifier.

### Parameters
- `self`: A fitted time-series classifier instance (e.g., `KNeighborsTimeSeriesClassifier`, `TimeSeriesSVC`, or `LearningShapelets`).
- `X`: The time-series dataset to be scored, formatted as a 3D array-like of shape `(n_series, n_timestamps, n_features)`.

### Input
The classifier (`self`) must be fitted prior to calling this method. The input `X` must strictly adhere to `tslearn`'s 3D array format `(n_ts, max_sz, d)`. If your data is a list of lists or a 2D array, it must be converted using `tslearn.utils.to_time_series_dataset` before being passed to `predict_proba`. The number of features (`d`) must match the data the model was trained on.

### Output
Returns `unspecified` — An array-like of shape `(n_series, n_classes)` containing the probability of the sample for each class in the model. The classes are ordered as they appear in the `self.classes_` attribute of the fitted estimator.

### Valid Call Patterns
```python
import numpy as np
from tslearn.neighbors import KNeighborsTimeSeriesClassifier
from tslearn.utils import to_time_series_dataset

# Inferred from signature and scikit-learn conventions
X_train = to_time_series_dataset([[1.0, 2.0], [1.0, 2.5], [9.0, 8.0]])
y_train = [0, 0, 1]

clf = KNeighborsTimeSeriesClassifier(n_neighbors=2)
clf.fit(X_train, y_train)

X_test = to_time_series_dataset([[1.0, 2.2]])
probabilities = clf.predict_proba(X_test)

assert probabilities.shape == (1, 2)
print(f"Class probabilities: {probabilities}")
```

### LLM Instruction Prompt
- Ensure the classifier is fitted before calling `predict_proba`.
- Ensure `X` is strictly a 3D array of shape `(n_series, n_timestamps, n_features)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists or 2D arrays.
- Do not pass target labels (`y`) to `predict_proba`.

### Prompt Snippet
```text
When calling `predict_proba(X)` on a tslearn classifier, ensure the model is already fitted and `X` is a 3D array of shape `(n_series, n_timestamps, n_features)`. The method returns an array of shape `(n_series, n_classes)` with class probabilities ordered by `clf.classes_`.
```

### Common Failure Modes
- **NotFittedError**: Calling `predict_proba` before calling `fit` on the classifier.
- **ValueError (Dimensionality)**: Passing a 1D or 2D array instead of the required 3D array `(n_series, n_timestamps, n_features)`.
- **ValueError (Feature Mismatch)**: Passing data with a different number of features (`n_features`) than the data used to fit the model.

### Fix Code Hint
```python
# Ensure X is 3D before predicting
from tslearn.utils import to_time_series_dataset

X_test_3d = to_time_series_dataset(X_test_raw)
probabilities = clf.predict_proba(X_test_3d)
```

## API Test: `predict_proba_and_earliness`

### Signature
```python
def predict_proba_and_earliness(self, X)
```
_Source: tslearn/tslearn/early_classification/early_classification.py:453_

_Source doc:_ Provide probability estimates as well as prediction timestamps. Prediction timestamps are timestamps at which a prediction is made in early classification setting. The returned estimates for all classes are ordered by the label of classes. Parameters ---------- X : array-like of shape (n_series, n_timestamps, n_features) Vector to be scored, where `n_series` is the number of time series, `n_timestamps` is the number of timestamps in the series and `n_features` is the number of features recorded at each timestamp. Returns ------- array-like of shape (n_series, n_classes) Probability of the sample for each class in the model, where classes are ordered as they are in ``self.classes_``. array-like of shape (n_series, ) Prediction timestamps.

### Goal
Compute class probability estimates and the exact timestamps at which the model made its early predictions for a given time-series dataset.

### Parameters
- `self`: A fitted early classification estimator instance (e.g., `NonMyopicEarlyClassifier`).
- `X`: The time-series dataset to be scored, formatted as a 3D array-like of shape `(n_series, n_timestamps, n_features)`.

### Input
- `X` must be a 3D array-like of shape `(n_series, n_timestamps, n_features)`. Raw lists or 2D arrays must be converted using `tslearn.utils.to_time_series_dataset` prior to calling this method.
- The estimator (`self`) must be fitted on training data before this method is called.

### Output
Returns `tuple[numpy.ndarray, numpy.ndarray]` — A tuple containing two arrays:
1. An array of shape `(n_series, n_classes)` representing the probability of each sample for each class, ordered by `self.classes_`.
2. An array of shape `(n_series,)` representing the prediction timestamps (earliness) at which the early classification decision was made for each series.

### Valid Call Patterns
```python
# Inferred from signature and tslearn conventions
from tslearn.early_classification import NonMyopicEarlyClassifier
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data
X_train = to_time_series_dataset([[1.0, 2.0, 3.0], [1.0, 2.0, 1.0], [3.0, 4.0, 5.0], [3.0, 4.0, 3.0]])
y_train = [0, 1, 0, 1]
X_test = to_time_series_dataset([[1.0, 2.0, 3.0], [3.0, 4.0, 3.0]])

# 2. Instantiate and fit the early classifier
clf = NonMyopicEarlyClassifier(random_state=42)
clf.fit(X_train, y_train)

# 3. Predict probabilities and earliness
probas, earliness = clf.predict_proba_and_earliness(X_test)

assert probas.shape == (2, 2), f"Expected shape (2, 2), got {probas.shape}"
assert earliness.shape == (2,), f"Expected shape (2,), got {earliness.shape}"
print("predict_proba_and_earliness returned probabilities and timestamps successfully.")
```

### LLM Instruction Prompt
- Ensure `X` is strictly formatted as a 3D array `(n_series, n_timestamps, n_features)` using `tslearn.utils.to_time_series_dataset` before passing it to `predict_proba_and_earliness`.
- The estimator must be fitted before calling this method.
- Expect a tuple of two arrays `(probabilities, earliness_timestamps)` to be returned; do not treat the return value as a single array.

### Prompt Snippet
```text
When using `predict_proba_and_earliness` on a `tslearn` early classifier, ensure the input `X` is a 3D array `(n_series, n_timestamps, n_features)`. The method returns a tuple of two arrays: `(probas, earliness)`. Unpack them accordingly.
```

### Common Failure Modes
- **ValueError (Dimensionality):** Passing a 1D or 2D array instead of the required 3D array `(n_series, n_timestamps, n_features)`.
- **NotFittedError:** Calling `predict_proba_and_earliness` before calling `.fit()` on the estimator.
- **ValueError (Unpacking):** Failing to unpack the return value into two variables, leading to shape mismatches if the tuple is mistakenly treated as a single probability array.

### Fix Code Hint
```python
# FIX: Convert input to 3D array and unpack the two return values
from tslearn.utils import to_time_series_dataset

X_test_3d = to_time_series_dataset(X_test_raw)
probas, earliness = clf.predict_proba_and_earliness(X_test_3d)
```

## API Test: `random_walk_blobs`

### Signature
```python
def random_walk_blobs(n_ts_per_blob=100, sz=256, d=1, n_blobs=2, noise_level=1.0, random_state=None)
```
_Source: tslearn/tslearn/generators/generators.py:57_

_Source doc:_ Blob-based random walk time series generator. Generate n_ts_per_blobs * n_blobs time series of size sz and dimensionality d. Generated time series follow the model: .. math:: ts[t] = ts[t - 1] + a where :math:`a` is drawn from a normal distribution of mean mu and standard deviation std. Each blob contains time series derived from a same seed time series with added white noise. Parameters ---------- n_ts_per_blob : int (default: 100) Number of time series in each blob sz : int (default: 256) Length of time series (number of time instants) d : int (default: 1) Dimensionality of time series n_blobs : int (default: 2) Number of blobs noise_level : float (default: 1.) Standard deviation of white noise added to time series in each blob random_state : integer or numpy.RandomState or None (default: None) Generator used to draw the time series. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. Returns ------- numpy.ndarray A dataset of random walk time series numpy.ndarray Labels associated to random walk time series (blob id) Examples -------- >>> X, y = random_walk_blobs(n_ts_per_blob=100, sz=256, d=5, n_blobs=3) >>> X.shape (300, 256, 5) >>> y.shape (300,)

### Goal
Generates a synthetic dataset of random walk time series grouped into distinct blobs (clusters) for testing classification and clustering algorithms.

### Parameters
- `n_ts_per_blob`, default `100`: The number of time series to generate for each blob (cluster).
- `sz`, default `256`: The length (number of time steps) of each generated time series.
- `d`, default `1`: The dimensionality of each time step in the time series.
- `n_blobs`, default `2`: The number of distinct blobs (clusters) to generate.
- `noise_level`, default `1.0`: The standard deviation of the Gaussian white noise added to the seed time series of each blob.
- `random_state`, default `None`: An integer seed or `numpy.RandomState` instance for deterministic data generation.

### Input
Scalar configuration values (integers and floats) defining the dimensions, cluster count, and noise characteristics of the desired synthetic dataset.

### Output
Returns `unspecified` — A tuple `(X, y)` containing two `numpy.ndarray` objects: `X` is the generated time-series dataset in `tslearn`'s strict 3D format `(n_ts_per_blob * n_blobs, sz, d)`, and `y` is a 1D array of shape `(n_ts_per_blob * n_blobs,)` containing the integer blob labels (cluster IDs).

### Valid Call Patterns
```python
from tslearn.generators import random_walk_blobs

# Generate a small deterministic dataset for testing
X, y = random_walk_blobs(
    n_ts_per_blob=15, 
    sz=50, 
    d=2, 
    n_blobs=3, 
    noise_level=0.5, 
    random_state=42
)

assert X.shape == (45, 50, 2)
assert y.shape == (45,)
print(f"Generated {X.shape[0]} time series across {len(set(y))} blobs.")
```

### LLM Instruction Prompt
- Use `tslearn.generators.random_walk_blobs` to create synthetic time-series data for testing clustering or classification pipelines.
- Always unpack the return value into two variables `(X, y)`.
- The returned `X` array is already in `tslearn`'s required 3D format `(n_ts, max_sz, d)`, so `to_time_series_dataset` is not needed.
- Keep `n_ts_per_blob`, `sz`, and `d` small in test environments to minimize memory usage and execution time.

### Prompt Snippet
```text
Use `tslearn.generators.random_walk_blobs(n_ts_per_blob=..., sz=..., d=..., n_blobs=..., random_state=...)` to generate synthetic time-series datasets. It returns a tuple `(X, y)` where `X` is a 3D numpy array of shape `(n_ts_per_blob * n_blobs, sz, d)` and `y` contains the integer blob labels.
```

### Common Failure Modes
- Failing to unpack the returned tuple into `X` and `y`, resulting in an `AttributeError` when trying to access `.shape` or pass the tuple to an estimator.
- Passing excessively large values for `n_ts_per_blob` or `sz`, causing out-of-memory errors during generation.

### Fix Code Hint
```python
# WRONG: Forgetting to unpack the tuple
dataset = random_walk_blobs(n_ts_per_blob=10, sz=50, n_blobs=2)
# model.fit(dataset) # Fails because dataset is a tuple

# CORRECT: Unpack into X and y
X, y = random_walk_blobs(n_ts_per_blob=10, sz=50, n_blobs=2, random_state=42)
# model.fit(X, y)
```

## API Test: `random_walks`

### Signature
```python
def random_walks(n_ts=100, sz=256, d=1, mu=0.0, std=1.0, random_state=None)
```
_Source: tslearn/tslearn/generators/generators.py:7_

_Source doc:_ Random walk time series generator. Generate n_ts time series of size sz and dimensionality d. Generated time series follow the model: .. math:: ts[t] = ts[t - 1] + a where :math:`a` is drawn from a normal distribution of mean mu and standard deviation std. Parameters ---------- n_ts : int (default: 100) Number of time series. sz : int (default: 256) Length of time series (number of time instants). d : int (default: 1) Dimensionality of time series. mu : float (default: 0.) Mean of the normal distribution from which random walk steps are drawn. std : float (default: 1.) Standard deviation of the normal distribution from which random walk steps are drawn. random_state : integer or numpy.RandomState or None (default: None) Generator used to draw the time series. If an integer is given, it fixes the seed. Defaults to the global numpy random number generator. Returns ------- numpy.ndarray A dataset of random walk time series Examples -------- >>> random_walks(n_ts=100, sz=256, d=5, mu=0., std=1.).shape (100, 256, 5)

### Goal
Generates a synthetic dataset of random walk time series, where each time step is computed by adding a normally distributed random value to the previous step.

### Parameters
- `n_ts`, default `100`: The number of independent time series to generate (integer).
- `sz`, default `256`: The length (number of time instants) of each generated time series (integer).
- `d`, default `1`: The dimensionality of each time series (integer).
- `mu`, default `0.0`: The mean of the normal distribution from which the random walk steps are drawn (float).
- `std`, default `1.0`: The standard deviation of the normal distribution from which the random walk steps are drawn (float).
- `random_state`, default `None`: The seed or random number generator used to draw the time series for reproducibility (integer, `numpy.RandomState`, or `None`).

### Input
No input data arrays are required as this is a generator function. The caller provides scalar configuration parameters (integers and floats) to define the shape and distribution of the generated synthetic dataset.

### Output
Returns `numpy.ndarray` — A 3D NumPy array of shape `(n_ts, sz, d)` containing the generated random walk time series. This output strictly adheres to `tslearn`'s standard 3D format and is immediately compatible with `tslearn` estimators and metrics.

### Valid Call Patterns
```python
from tslearn.generators import random_walks
import numpy as np

# 1. Generate a small univariate dataset of random walks
X_univariate = random_walks(n_ts=20, sz=16, d=1, random_state=42)
assert X_univariate.shape == (20, 16, 1)
assert isinstance(X_univariate, np.ndarray)

# 2. Generate multivariate random walks with zero standard deviation (constant series)
X_constant = random_walks(n_ts=5, sz=10, d=3, std=0.0, random_state=0)
assert X_constant.shape == (5, 10, 3)
# Since std=0, all steps are 0, meaning the series remains constant at its initial value
np.testing.assert_array_equal(X_constant[:, 0, :], X_constant[:, -1, :])
```

### LLM Instruction Prompt
- Use `tslearn.generators.random_walks` to create synthetic baseline datasets for testing time-series models or metrics.
- Remember that the output is already in the strict `(n_ts, max_sz, d)` 3D NumPy array format required by `tslearn` estimators; do not pass it through `to_time_series_dataset`.
- Always set `random_state` to an integer to ensure deterministic and reproducible test execution.
- If you need constant time series for edge-case testing, set `std=0.0`.

### Prompt Snippet
```text
When generating synthetic time-series data for tslearn tests, use `from tslearn.generators import random_walks`. It returns a 3D numpy array of shape `(n_ts, sz, d)`. Always provide a `random_state` integer for deterministic outputs.
```

### Common Failure Modes
- **Assuming 2D Output:** Forgetting that the output is a 3D array `(n_ts, sz, d)` and attempting to pass it directly into standard 2D `scikit-learn` estimators (like `sklearn.ensemble.RandomForestClassifier`) without reshaping or using `tslearn`'s compatible estimators.
- **Flaky Tests:** Omitting the `random_state` parameter, which causes the generated dataset to change across runs, leading to non-deterministic assertions in test suites.

### Fix Code Hint
```python
# BAD: Non-deterministic and assumes 2D output
X = random_walks(n_ts=10, sz=50)
# sklearn_model.fit(X, y) # Will fail due to 3D shape

# GOOD: Deterministic and explicitly handles the 3D shape
from tslearn.generators import random_walks
X = random_walks(n_ts=10, sz=50, d=1, random_state=42)
assert X.ndim == 3
# tslearn_model.fit(X, y) # Succeeds
```

## API Test: `sakoe_chiba_mask`

### Signature
```python
def sakoe_chiba_mask(sz1, sz2, radius=1, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1536  (+1 more definition site/overload)_

### Goal
Compute a boolean Sakoe-Chiba band mask of shape `(sz1, sz2)` to constrain the allowed alignment path in Dynamic Time Warping (DTW) calculations.

### Parameters
- `sz1`: `int` — The length (number of time steps) of the first time series.
- `sz2`: `int` — The length (number of time steps) of the second time series.
- `radius`, default `1`: `int` — The radius of the Sakoe-Chiba band. A radius of 0 restricts the path to the diagonal (if `sz1 == sz2`), while larger values allow more warping.
- `be`, default `None`: `Backend object or string or None` — The computational backend to use for generating the mask. Accepts `"numpy"`, `"pytorch"`, a backend instance, or `None`. If `None`, it defaults to NumPy since there are no input arrays to infer the backend from.

### Input
Integer dimensions representing the lengths of two time series to be aligned, and an integer radius defining the maximum allowed warping window. 

### Output
Returns `unspecified` — A boolean array-like object (NumPy array or PyTorch tensor, depending on the `be` parameter) of shape `(sz1, sz2)`. Cells with `True` are within the Sakoe-Chiba band (valid for alignment), and `False` indicates cells outside the band.

### Valid Call Patterns
```python
from tslearn.metrics import sakoe_chiba_mask
import numpy as np

# 1. Generate a 4x4 mask with radius 1 using the default NumPy backend
sk_mask = sakoe_chiba_mask(4, 4, radius=1, be="numpy")

reference_mask = np.array([
    [ True,  True, False, False],
    [ True,  True,  True, False],
    [False,  True,  True,  True],
    [False, False,  True,  True]
])
np.testing.assert_array_equal(sk_mask, reference_mask)

# 2. Generate an asymmetric mask (e.g., for time series of lengths 7 and 3)
sk_mask_asym = sakoe_chiba_mask(7, 3, 1)
assert sk_mask_asym.shape == (7, 3)
assert sk_mask_asym[6, 0] == False # Outside the band
assert sk_mask_asym[6, 2] == True  # Inside the band
```

### LLM Instruction Prompt
- When generating a Sakoe-Chiba mask for PyTorch tensors, you MUST explicitly pass `be="pytorch"`. Unlike metric functions (e.g., `dtw`) which auto-detect the backend from input arrays, `sakoe_chiba_mask` only takes integer sizes and cannot auto-detect PyTorch unless explicitly told.
- Use this function when you need to manually implement constrained DTW variants or visualize the alignment constraints.

### Prompt Snippet
```text
tslearn.metrics.sakoe_chiba_mask(sz1, sz2, radius=1, be=None)
Computes a boolean Sakoe-Chiba mask of shape (sz1, sz2) for DTW constraints. Returns an array/tensor where True means the cell is within the allowed warping band. Pass be="pytorch" if the mask will be applied to PyTorch tensors.
```

### Common Failure Modes
- **Backend Mismatch**: Generating the mask with the default NumPy backend and attempting to apply it directly to PyTorch tensors on a GPU or tensors requiring gradients, causing a `TypeError` or device mismatch.
- **Negative Dimensions**: Passing negative values for `sz1`, `sz2`, or `radius`, which will result in invalid array shapes or empty bands.

### Fix Code Hint
```python
# BAD: Mask defaults to NumPy, causing a type error when applied to PyTorch tensors
# mask = sakoe_chiba_mask(len(ts1), len(ts2), radius=2)
# cost_matrix[~mask] = float('inf') 

# GOOD: Explicitly request the PyTorch backend
mask = sakoe_chiba_mask(len(ts1), len(ts2), radius=2, be="pytorch")
cost_matrix[~mask] = float('inf')
```

## API Test: `save_dict`

### Signature
```python
def save_dict(d, filename, group, raise_type_fail=True)
```
_Source: tslearn/tslearn/hdftools/hdftools.py:8_

### Goal
Recursively serialize a Python dictionary (typically containing NumPy arrays or model parameters) into an HDF5 file under a specified group name.

### Parameters
- `d`: The Python dictionary to save to the HDF5 file.
- `filename`: A string representing the full path where the HDF5 file will be saved. The file at this path must not already exist.
- `group`: A string representing the HDF5 group name under which the dictionary contents will be stored.
- `raise_type_fail`, default `True`: A boolean flag. If `True`, raises a `TypeError` if a part of the dictionary cannot be saved to HDF5. If `False`, prints a warning and saves the unsupported object's `__str__()` return value instead.

### Input
A Python dictionary containing HDF5-compatible data (such as NumPy arrays, scalars, or nested dictionaries), a valid file path pointing to a non-existent file, and a string group name. 

### Output
Returns `unspecified` — `None`. The function operates via side effects, creating a new HDF5 file at the specified `filename` containing the dictionary's data.

### Valid Call Patterns
```python
import os
import tempfile
import numpy as np
from tslearn.hdftools import save_dict, load_dict

# Create a dictionary with deterministic NumPy arrays
d = {
    "weights": np.array([1.0, 2.0, 3.0], dtype=np.float64),
    "bias": np.array([0.5], dtype=np.float64)
}

# Use a temporary directory to ensure the file does not already exist
with tempfile.TemporaryDirectory() as tmp_dir:
    fname = os.path.join(tmp_dir, 'model_params.hdf5')
    
    # Save the dictionary to the HDF5 file under the group 'data'
    save_dict(d, filename=fname, group='data')
    
    # Verify the file was created and data can be loaded
    d2 = load_dict(fname, 'data')
    
    assert np.array_equal(d["weights"], d2["weights"]), "Weights mismatch"
    assert np.array_equal(d["bias"], d2["bias"]), "Bias mismatch"
    print("Dictionary successfully saved and verified.")
```

### LLM Instruction Prompt
- Ensure the target file path provided to `filename` does not already exist before calling `save_dict`, as it will strictly raise a `FileExistsError`.
- Ensure the dictionary values are HDF5-serializable (e.g., NumPy arrays, standard numeric scalars). If the dictionary contains complex Python objects, you must either convert them to NumPy arrays first or explicitly pass `raise_type_fail=False` to fallback to string representations.

### Prompt Snippet
```text
When serializing time-series model parameters or data dictionaries using `tslearn.hdftools.save_dict`, always verify that the destination file does not exist. If it might exist, remove it using `os.remove()` prior to calling `save_dict`. Ensure all dictionary values are NumPy arrays or native scalars to prevent `TypeError` during HDF5 conversion.
```

### Common Failure Modes
- **`FileExistsError`**: Raised if the file specified by `filename` already exists on the disk. `save_dict` will not overwrite existing files.
- **`TypeError`**: Raised if `raise_type_fail=True` (the default) and the dictionary contains an object type that the underlying HDF5 library (`h5py`) cannot natively serialize (e.g., custom class instances, unsupported collections).

### Fix Code Hint
```python
import os
from tslearn.hdftools import save_dict

# FIX: Remove the file if it already exists to prevent FileExistsError
if os.path.exists(fname):
    os.remove(fname)

# FIX: Ensure dictionary values are NumPy arrays, or set raise_type_fail=False
save_dict(d, filename=fname, group='data', raise_type_fail=False)
```

## API Test: `save_time_series_txt`

### Signature
```python
def save_time_series_txt(fname, dataset, fmt='%.18e')
```
_Source: tslearn/tslearn/utils/utils.py:364_

_Source doc:_ Writes a time series dataset to disk. Parameters ---------- fname : string Path to the file in which time series should be written. dataset : array-like The dataset of time series to be saved. fmt : string (default: "%.18e") Format to be used to write each value. Examples -------- >>> dataset = to_time_series_dataset([[1, 2, 3, 4], [1, 2, 3]]) >>> save_time_series_txt("tmp-tslearn-test.txt", dataset) See Also -------- load_time_series_txt : Load time series from disk

### Goal
Writes a time-series dataset to disk as a text file, serializing the values according to a specified format.

### Parameters
- `fname`: A string representing the file path where the time-series dataset should be written.
- `dataset`: An array-like object representing the time-series dataset to be saved. It must conform to the strict `(n_ts, max_sz, d)` 3D array structure.
- `fmt`, default `'%.18e'`: A string specifying the C-style format to be used when writing each numerical value to the text file.

### Input
The `dataset` must be a 3D `numpy` array of shape `(n_ts, max_sz, d)`. If you have raw lists of variable-length time series, you must first convert and pad them using `tslearn.utils.to_time_series_dataset` before passing them to this function. `fname` must be a valid, writable file path.

### Output
Returns `unspecified` — `None`; the function performs a side effect by writing the formatted dataset to the specified file on disk.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.utils import to_time_series_dataset, save_time_series_txt

# 1. Prepare variable-length time series into the required 3D format
raw_data = [[1.0, 2.5, 3.0], [4.2]]
dataset = to_time_series_dataset(raw_data)

# 2. Save to a text file
with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
    fname = tmp.name

save_time_series_txt(fname, dataset, fmt='%.6f')

# Verify the file was written
assert os.path.exists(fname)
assert os.path.getsize(fname) > 0
print(f"Successfully wrote dataset to {fname}")

# Clean up
os.remove(fname)
```

### LLM Instruction Prompt
- When saving a time-series dataset to a text file using `tslearn`, use `tslearn.utils.save_time_series_txt`. Ensure the dataset is properly formatted as a 3D array `(n_ts, max_sz, d)` using `to_time_series_dataset` before saving, as `tslearn` strictly expects this format.

### Prompt Snippet
```text
Use `tslearn.utils.save_time_series_txt(fname, dataset)` to serialize a time-series dataset to a text file. The `dataset` must be a 3D array `(n_ts, max_sz, d)`, typically prepared with `to_time_series_dataset`.
```

### Common Failure Modes
- Passing a raw list of variable-length lists directly to `dataset` without first converting it to a padded 3D array using `to_time_series_dataset`.
- Providing an invalid file path, a directory path instead of a file, or lacking write permissions for `fname`.
- Providing an invalid C-style format string to `fmt`, causing a formatting error during serialization.

### Fix Code Hint
```python
# WRONG: Passing raw variable-length lists directly
# save_time_series_txt("out.txt", [[1, 2], [3]])

# RIGHT: Convert to a 3D dataset first
from tslearn.utils import to_time_series_dataset, save_time_series_txt
dataset = to_time_series_dataset([[1, 2], [3]])
save_time_series_txt("out.txt", dataset)
```

## API Test: `select_backend`

### Signature
```python
def select_backend(data)
```
_Source: tslearn/tslearn/backend/backend.py:31_

_Source doc:_ Select backend. Parameter --------- data : array-like or string or None Indicates the backend to choose. Optional, default equals None. Returns ------- backend : class The backend class. If data is a Numpy array or data equals 'numpy' or data is None, backend equals NumpyBackend(). If data is a PyTorch array or data equals 'pytorch', backend equals PytorchBackend().

### Goal
Selects and returns the appropriate computational backend instance (`NumpyBackend` or `PytorchBackend`) based on the provided data type or string identifier.

### Parameters
- `data`: An array-like object (e.g., NumPy array, PyTorch tensor), a string (`'numpy'`, `'pytorch'`), or `None` indicating which backend to choose. Defaults to `None`.

### Input
A valid time-series data object (NumPy array or PyTorch tensor), a string literal specifying the backend, or `None`. If a PyTorch tensor or `'pytorch'` is provided, the `pytorch` package must be installed locally in the environment.

### Output
Returns `unspecified` — represents the instantiated backend object (e.g., `NumpyBackend()` or `PytorchBackend()`) used for backend-agnostic metric computations and automatic differentiation.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import select_backend

# Example inferred from signature (not verified by existing tests)

# 1. Select backend using a string identifier
be_from_str = select_backend("numpy")

# 2. Select backend dynamically from a NumPy array
data_array = np.array([[[1.0], [2.0]], [[3.0], [4.0]]])
be_from_data = select_backend(data_array)

# 3. Default fallback behavior
be_default = select_backend(None)

# Assert falsifiable property: all three should resolve to the same NumPy backend class
assert type(be_from_str) == type(be_from_data) == type(be_default), "Backend types diverged unexpectedly."

# Print correctness witness
print(f"Selected backend type: {type(be_from_str).__name__}")
```

### LLM Instruction Prompt
- When dynamically resolving the computational backend for time-series metrics, use `select_backend(data)`. 
- Pass the input array/tensor, a string (`"numpy"` or `"pytorch"`), or `None`. 
- Note that if PyTorch is requested, the environment must have `pytorch` installed. Unrecognized inputs or `None` will safely default to the NumPy backend.
- Do not expect a string return value; this function returns the actual backend class instance.

### Prompt Snippet
```text
from tslearn.backend import select_backend

# Auto-detect backend from data type or string
backend = select_backend(X_train)
# backend is now an instance of NumpyBackend() or PytorchBackend()
```

### Common Failure Modes
- **Missing Dependencies:** Requesting the PyTorch backend (`data='pytorch'` or passing a PyTorch tensor) in an environment where the `pytorch` package is not installed locally.
- **Type Misconceptions:** Assuming `select_backend` returns a string identifier; it returns a backend class instance (e.g., `NumpyBackend()`).
- **Unrecognized Strings:** Passing an unsupported string (e.g., `"tensorflow"`) will silently default to `NumpyBackend()` rather than raising a validation error.

### Fix Code Hint
```python
# Ensure safe fallback to numpy if pytorch is unavailable
try:
    import torch
    data = torch.tensor([[[1.0], [2.0]]], requires_grad=True)
    be = select_backend(data)
except ImportError:
    import numpy as np
    data = np.array([[[1.0], [2.0]]])
    be = select_backend("numpy")
```

## API Test: `set_backend`

### Signature
```python
def set_backend(self, data=None)
```
_Source: tslearn/tslearn/backend/backend.py:87_

### Goal
Updates the active computational backend (e.g., NumPy or PyTorch) for an existing `Backend` wrapper instance based on the provided string identifier or data type.

### Parameters
- `self`: The instantiated `Backend` wrapper object whose internal backend state is being mutated.
- `data`, default `None`: A string identifier (e.g., `"numpy"`, `"pytorch"`, `"torch"`), a data array/tensor, or `None` used to infer and set the new backend. Unrecognized inputs or `None` default to the NumPy backend.

### Input
The caller must provide an instantiated `Backend` object and optionally a valid backend identifier string or a representative data object (like a `numpy.ndarray` or `torch.Tensor`). If passing a string, `"numpy"`, `"pytorch"`, or `"torch"` are standard.

### Output
Returns `None` — mutates the `Backend` instance in place, updating its internal state so that subsequent operations (and calls to `get_backend()`) use the newly resolved backend (e.g., `NumPyBackend` or `PyTorchBackend`).

### Valid Call Patterns
```python
from tslearn.backend import Backend
from tslearn.backend import NumPyBackend

# Initialize a Backend wrapper requesting PyTorch
backend_ = Backend("torch")
assert backend_.is_pytorch
assert not backend_.is_numpy

# Mutate the instance to use NumPy instead
backend_.set_backend("numpy")

# Verify the internal state has been updated
assert not backend_.is_pytorch
assert backend_.is_numpy
assert isinstance(backend_.get_backend(), NumPyBackend)
print("Backend successfully switched to:", type(backend_.get_backend()).__name__)
```

### LLM Instruction Prompt
- When you need to dynamically switch the computational engine of an existing `tslearn.backend.Backend` instance, call its `.set_backend(data)` method. Pass a string like `"numpy"` or `"pytorch"`, or a representative data array/tensor. Do not call this as a standalone function; it is an instance method.

### Prompt Snippet
```text
To switch the backend of an existing `Backend` instance in tslearn, use the instance method: `backend_instance.set_backend("numpy")` or `backend_instance.set_backend("pytorch")`. Unrecognized inputs will safely default to NumPy.
```

### Common Failure Modes
- **Calling as a static function:** Attempting to call `set_backend("numpy")` directly without a `Backend` instance will raise a `NameError` or `TypeError`. It must be called on an instantiated `Backend` object.
- **Silent fallback to NumPy:** Passing an unsupported string (e.g., `"tensorflow"`) or an unrecognized object type will not raise an error; instead, the backend selection rules will silently default the instance to `NumPyBackend`.
- **Missing PyTorch dependency:** If `"pytorch"` or `"torch"` is requested but the `pytorch` package is not installed in the environment, the backend may fail to initialize or fallback to NumPy depending on the environment configuration.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function
# set_backend("numpy")

# CORRECT: Calling on a Backend instance
from tslearn.backend import Backend
my_backend = Backend("pytorch")
# ... perform PyTorch operations ...
my_backend.set_backend("numpy") # Switch to NumPy
```

## API Test: `set_weights`

### Signature
```python
def set_weights(self, weights, layer_name=None)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:866_

### Goal
Manually set the internal neural network weights of a `LearningShapelets` estimator, either for the entire model or for a specific layer.

### Parameters
- `self`: A `LearningShapelets` estimator instance.
- `weights`: A list of NumPy `ndarray` objects representing the weights to assign to the target layer or the entire model.
- `layer_name`, default `None`: A string specifying the name of the layer to update. If `None`, all model weights are set. Available layer names include `"shapelets_i_j"` (where `i` is the shapelet ID integer and `j` is the dimension integer) or `"classification"` for the final classification layer.

### Input
The estimator must typically be fitted first (e.g., via `.fit(X, y)`) so that the underlying neural network architecture is built and the layers exist. The `weights` argument must be a list of NumPy arrays, and the shapes of these arrays must exactly match the expected dimensions of the target layer.

### Output
Returns `unspecified` — Returns `None`; the operation modifies the estimator's internal neural network weights in place.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets import LearningShapelets
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data (n_ts, max_sz, d)
X = to_time_series_dataset([[1.0, 2.0, 3.0, 4.0, 5.0], [3.0, 2.0, 1.0]])
y = [0, 1]

# 2. Initialize and fit the model to build the underlying architecture
clf = LearningShapelets(n_shapelets_per_size={3: 1}, max_iter=1, random_state=0)
clf.fit(X, y)

# 3. Define new weights as a list of ndarrays
weights_shapelet = [np.array([[[1.0], [2.0], [3.0]]])]

# 4. Set the weights for the specific shapelet layer
clf.set_weights(weights_shapelet, layer_name="shapelets_0")

# 5. Verify the weights were updated
np.testing.assert_allclose(
    clf.shapelets_as_time_series_[0], 
    np.array([[1.], [2.], [3.]])
)
print("Weights successfully set and verified.")
```

### LLM Instruction Prompt
- When calling `set_weights` on a `LearningShapelets` model, you MUST pass the `weights` argument as a `list` of NumPy `ndarray` objects, not a single array.
- Ensure the model has been fitted (`.fit()`) before calling `set_weights` so that the internal layers are initialized.
- Use valid `layer_name` strings as defined by the API (e.g., `"shapelets_0"`, `"classification"`).

### Prompt Snippet
```text
tslearn.shapelets.LearningShapelets.set_weights(weights, layer_name=None)
Sets model weights. `weights` MUST be a list of ndarrays. `layer_name` can be "shapelets_i_j" (e.g., "shapelets_0") or "classification". Call `.fit()` first to build the model architecture.
```

### Common Failure Modes
- **Passing a bare array instead of a list**: Providing `np.array(...)` instead of `[np.array(...)]` for the `weights` parameter will cause iteration or shape mismatch errors in the underlying backend.
- **Calling before `fit`**: Attempting to set weights on a freshly instantiated `LearningShapelets` object before calling `.fit()` will fail because the internal neural network layers have not been constructed yet.
- **Shape mismatch**: Providing arrays in the `weights` list that do not match the expected dimensions of the target layer (e.g., wrong shapelet length or wrong number of classes).
- **Invalid layer name**: Providing a `layer_name` string that does not match the `"shapelets_i_j"` or `"classification"` pattern.

### Fix Code Hint
```python
# WRONG: Passing a bare array and/or calling before fit
clf = LearningShapelets(n_shapelets_per_size={3: 1})
clf.set_weights(np.array([[[1], [2], [3]]]), layer_name="shapelets_0")

# RIGHT: Fit first, and pass a list of arrays
clf = LearningShapelets(n_shapelets_per_size={3: 1}, max_iter=1)
clf.fit(X, y)  # Builds the architecture
clf.set_weights([np.array([[[1], [2], [3]]])], layer_name="shapelets_0")
```

## API Test: `shape`

### Signature
```python
def shape(self, data)
```

### Goal
Retrieves the dimensions (shape) of a time-series data array or tensor using the active computational backend, enabling backend-agnostic dimension inspection.

### Parameters
- `self`: The instantiated backend object (e.g., `NumPyBackend` or `PyTorchBackend`) on which this method is called.
- `data`: The time-series data array or tensor whose shape is to be determined.

### Input
A time-series dataset or array/tensor compatible with the active backend. For the NumPy backend, this is typically a 3D NumPy array of shape `(n_ts, max_sz, d)`. For the PyTorch backend, this must be a PyTorch tensor.

### Output
Returns `unspecified` — A tuple representing the dimensions of the input data array or tensor (e.g., `(n_ts, max_sz, d)`).

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Inferred from signature (not verified)
be = instantiate_backend("numpy")
data = np.zeros((3, 4, 2))

# Call shape as a method on the backend instance
result = be.shape(data)

assert result == (3, 4, 2), f"Expected (3, 4, 2), got {result}"
print("Correctness witness:", result)
```

### LLM Instruction Prompt
- Call `shape` as a method on an instantiated backend object (e.g., `be.shape(data)`), never as a standalone function.
- Use this method in backend-agnostic code to retrieve the dimensions of a time-series array or tensor, ensuring compatibility whether the underlying data is a NumPy array or a PyTorch tensor.

### Prompt Snippet
```text
from tslearn.backend import instantiate_backend
import numpy as np

be = instantiate_backend("numpy")
data = np.zeros((10, 5, 1))
dims = be.shape(data)
```

### Common Failure Modes
- **Standalone Call:** Attempting to import and call `shape(data)` directly instead of calling it as a method on a backend instance, resulting in a `NameError` or `ImportError`.
- **Backend Mismatch:** Passing a PyTorch tensor to a NumPy backend (or vice versa), which may result in an `AttributeError` if the backend expects a specific array type's properties.

### Fix Code Hint
```python
# WRONG: shape(data)
# RIGHT: be.shape(data)
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")
dims = be.shape(data)
```

## API Test: `shapelets_`

### Signature
```python
def shapelets_(self)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:441_

### Goal
Retrieves the collection of learned shapelet arrays from a fitted `LearningShapelets` model.

### Parameters
- `self`: A fitted `tslearn.shapelets.LearningShapelets` estimator instance.

### Input
- The estimator must have been successfully fitted using `.fit(X, y)` on a 3D time-series dataset of shape `(n_ts, max_sz, d)`.
- **Precondition**: `tslearn.shapelets` requires a deep learning backend (such as TensorFlow/Keras or PyTorch) to be installed in the environment.

### Output
Returns `unspecified` — A list of NumPy arrays. Each array represents a learned shapelet with shape `(shapelet_size, d)`, where `shapelet_size` corresponds to the sizes specified in `n_shapelets_per_size` during model initialization, and `d` is the dimensionality of the input time series.

### Valid Call Patterns
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    from tslearn.utils import to_time_series_dataset

    # 1. Prepare a 3D time-series dataset (n_ts, max_sz, d)
    X = to_time_series_dataset([[1.0, 2.0, 3.0, 4.0], [3.0, 2.0, 1.0, 0.0]])
    y = [0, 1]

    # 2. Initialize and fit the model
    clf = LearningShapelets(
        n_shapelets_per_size={2: 1}, 
        max_iter=1, 
        optimizer="sgd", 
        random_state=0
    )
    clf.fit(X, y)

    # 3. Access the learned shapelets property
    shapelets = clf.shapelets_

    # 4. Verify the output
    assert isinstance(shapelets, list)
    assert len(shapelets) == 1
    assert shapelets[0].shape == (2, 1)
    print(f"Successfully retrieved {len(shapelets)} shapelet(s) of shape {shapelets[0].shape}.")

except ImportError:
    print("Skipping execution: tslearn.shapelets requires a deep learning backend (e.g., TensorFlow/Keras).")
```

### LLM Instruction Prompt
- Access `shapelets_` as a property (without parentheses), following `scikit-learn` conventions for fitted attributes.
- Ensure the `LearningShapelets` model has been fitted with `.fit(X, y)` before accessing this property.
- Be aware that importing `tslearn.shapelets` will fail with an `ImportError` if a compatible deep learning backend is not installed.

### Prompt Snippet
```text
Access `shapelets_` as a property on a fitted `LearningShapelets` instance to retrieve the learned shapelets as a list of NumPy arrays. Do not call it as a function. Ensure `.fit(X, y)` has been called first.
```

### Common Failure Modes
- **Calling as a function**: Attempting to call `clf.shapelets_()` raises a `TypeError` because it evaluates to a list of arrays, which is not callable.
- **Accessing before fitting**: Accessing `clf.shapelets_` before calling `.fit(X, y)` raises an `AttributeError` or `NotFittedError`.
- **Missing Dependencies**: Attempting to use `LearningShapelets` without TensorFlow/Keras or PyTorch installed raises an `ImportError`.

### Fix Code Hint
```python
# WRONG: Calling as a function or accessing before fit
clf = LearningShapelets(n_shapelets_per_size={2: 1})
# shapelets = clf.shapelets_()  # TypeError: 'list' object is not callable

# RIGHT: Access as a property after fitting
clf.fit(X, y)
shapelets = clf.shapelets_  # Returns a list of NumPy arrays
```

## API Test: `shapelets_as_time_series_`

### Signature
```python
def shapelets_as_time_series_(self)
```
_Source: tslearn/tslearn/shapelets/shapelets.py:455_

_Source doc:_ Set of time-series shapelets formatted as a ``tslearn`` time series dataset. Examples -------- >>> from tslearn.generators import random_walk_blobs >>> X, y = random_walk_blobs(n_ts_per_blob=10, sz=256, d=1, n_blobs=3) >>> model = LearningShapelets(n_shapelets_per_size={3: 2, 4: 1}, ...                       max_iter=1) >>> _ = model.fit(X, y) >>> model.shapelets_as_time_series_.shape (3, 4, 1)

### Goal
Retrieves the learned shapelets from a fitted `LearningShapelets` model, formatted as a standard 3D `tslearn` time-series dataset.

### Parameters
- `self`: A fitted instance of `tslearn.shapelets.LearningShapelets`.

### Input
The `LearningShapelets` estimator must be instantiated and successfully fitted (using `.fit(X, y)`) on a 3D time-series dataset of shape `(n_ts, max_sz, d)` before this property can be accessed.

### Output
Returns `unspecified` — A 3D `numpy` array of shape `(n_shapelets, max_shapelet_length, d)` containing the learned shapelets. Because shapelets can have different lengths (as defined by `n_shapelets_per_size`), shorter shapelets are padded with `nan` values at the end to match the length of the longest shapelet (`max_shapelet_length`).

### Valid Call Patterns
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
except ImportError:
    print("Skipping: tslearn.shapelets requires keras/tensorflow.")
else:
    # 1. Create a small, deterministic 3D time-series dataset (n_ts=6, max_sz=10, d=1)
    rng = np.random.RandomState(0)
    X = rng.randn(6, 10, 1)
    y = rng.randint(2, size=6)

    # 2. Initialize the model requesting 2 shapelets of length 3, and 1 of length 4
    model = LearningShapelets(
        n_shapelets_per_size={3: 2, 4: 1}, 
        max_iter=1, 
        random_state=0
    )
    
    # 3. Fit the model
    model.fit(X, y)

    # 4. Access the shapelets as a formatted 3D time-series dataset (accessed as a property)
    ts_shapelets = model.shapelets_as_time_series_

    # 5. Verify the output shape: (total_shapelets=3, max_length=4, dimensions=1)
    assert ts_shapelets.shape == (3, 4, 1)
    
    # The shorter shapelets (length 3) will have a NaN at the last index
    print(f"Shapelets array shape: {ts_shapelets.shape}")
```

### LLM Instruction Prompt
- Access `shapelets_as_time_series_` as a property (without parentheses), not as a method, on a fitted `LearningShapelets` instance.
- Expect the returned object to be a 3D `numpy` array `(n_shapelets, max_sz, d)`.
- Account for `nan` values in the returned array; `tslearn` pads shorter shapelets with `nan`s to ensure the output is a strictly rectangular 3D array.
- Ensure the model has been fitted with `.fit(X, y)` before attempting to access this property.

### Prompt Snippet
```text
Extract the learned shapelets from the fitted `LearningShapelets` model `clf` as a 3D array. Remember to handle potential `nan` padding for variable-length shapelets.
```

### Common Failure Modes
- **TypeError (Not Callable):** Calling `model.shapelets_as_time_series_()` with parentheses will raise a `TypeError: 'numpy.ndarray' object is not callable` because it evaluates as a property returning an array.
- **AttributeError / NotFittedError:** Accessing the property before calling `.fit(X, y)` will fail because the underlying shapelet arrays have not been initialized or learned yet.
- **NaN Propagation Errors:** Passing the raw output of `shapelets_as_time_series_` directly into strict distance metrics or downstream models without accounting for the `nan` padding (used for shorter shapelets) can result in `nan` outputs or value errors.

### Fix Code Hint
```python
# WRONG: Calling as a method
# shapelets = model.shapelets_as_time_series_()

# CORRECT: Accessing as a property
shapelets = model.shapelets_as_time_series_

# Handle NaNs if iterating over variable-length shapelets
for shp in shapelets:
    valid_shp = shp[~np.isnan(shp).any(axis=1)]
    # Process valid_shp...
```

## API Test: `sigma_gak`

### Signature
```python
def sigma_gak(dataset, n_samples=100, random_state=None, be=None)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:397  (+1 more definition site/overload)_

### Goal
Compute the suggested bandwidth ($\sigma$) for the Global Alignment Kernel (GAK) by estimating the median distance over a random sample of time series from the dataset.

### Parameters
- `dataset`: array-like, shape `(n_ts, sz, d)` or `(n_ts, sz)` or `(sz,)`. A dataset of time series. If the shape is `(n_ts, sz)`, it is treated as a dataset of univariate time series. If `(sz,)`, it is treated as a single univariate time series.
- `n_samples`, default `100`: int. The number of samples on which the median distance should be estimated.
- `random_state`, default `None`: integer, `numpy.RandomState`, or `None`. The random number generator used to draw the samples. If an integer is given, it fixes the seed for reproducible results.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. The computational backend to use. If `None`, the backend is automatically determined from the input array types.

### Input
- A dataset of time series, typically formatted as a 3D array `(n_ts, max_sz, d)` using `tslearn.utils.to_time_series_dataset`, though 1D and 2D array-likes are also accepted and internally reshaped.
- Can be a standard Python list of lists, a NumPy array, or a PyTorch tensor.

### Output
Returns `float` — The suggested bandwidth ($\sigma$) to be used as the `sigma` parameter in `tslearn.metrics.gak` or `tslearn.metrics.cdist_gak`.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

# 1. Define a small dataset of time series
dataset = np.array([[1.0, 2.0, 2.0, 3.0], 
                    [1.0, 2.0, 3.0, 4.0]])

# 2. Compute the suggested sigma for GAK
sigma = tslearn.metrics.sigma_gak(
    dataset,
    n_samples=200,
    random_state=0
)

# 3. Assert falsifiable properties
assert isinstance(sigma, float), "Sigma must be a float."
assert sigma > 0.0, "Bandwidth sigma must be strictly positive."

# 4. Print the correctness witness
print(f"Computed GAK bandwidth (sigma): {sigma:.4f}")
```

### LLM Instruction Prompt
- Use `tslearn.metrics.sigma_gak` to heuristically determine a good `sigma` (bandwidth) parameter before computing the Global Alignment Kernel (`gak` or `cdist_gak`).
- Always provide a `random_state` integer for deterministic execution.
- The returned value is a float; pass it directly to the `sigma` argument of `gak` or `cdist_gak`. Do not use this value for Soft-DTW's `gamma` parameter, as they represent different mathematical concepts.

### Prompt Snippet
```text
When computing the Global Alignment Kernel (GAK) using `tslearn.metrics.gak` or `tslearn.metrics.cdist_gak`, first compute the optimal bandwidth `sigma` by calling `tslearn.metrics.sigma_gak(dataset, n_samples=100, random_state=42)`. Pass the resulting float to the `sigma` parameter of the kernel function.
```

### Common Failure Modes
- **Variable-length lists without padding**: Passing variable-length time series as a raw list of lists without first converting them to a padded 3D array using `tslearn.utils.to_time_series_dataset`.
- **Zero Division in GAK**: Failing to compute `sigma_gak` and manually passing `sigma=0` to `gak` or `cdist_gak`, which raises a `ZeroDivisionError`.
- **Misapplying the bandwidth**: Using the returned `sigma` for metrics other than GAK (e.g., passing it as `gamma` to `soft_dtw`).

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset
from tslearn.metrics import sigma_gak, cdist_gak

# Convert variable-length lists to a padded 3D array first
X = to_time_series_dataset([[1, 2, 3], [1, 2, 3, 4]])

# Compute the suggested sigma deterministically
sigma = sigma_gak(X, random_state=42)

# Use the computed sigma in GAK
kernel_matrix = cdist_gak(X, sigma=sigma)
```

## API Test: `silhouette_score`

### Signature
```python
def silhouette_score(X, labels, metric=None, sample_size=None, metric_params=None, n_jobs=None, verbose=0, random_state=None, **kwds)
```
_Source: tslearn/tslearn/clustering/utils.py:70_

_Source doc:_ Compute the mean Silhouette Coefficient of all samples (cf.  [1]_ and [2]_). Read more in the `scikit-learn documentation <http://scikit-learn.org/stable/modules/clustering.html\ #silhouette-coefficient>`_. Parameters ---------- X : array [n_ts, n_ts] if metric == "precomputed", or, \ [n_ts, sz, d] otherwise Array of pairwise distances between time series, or a time series dataset. labels : array, shape = [n_ts] Predicted labels for each time series. metric : string, callable or None (default: None) The metric to use when calculating distance between time series. Should be one of {'dtw', 'softdtw', 'euclidean'} or a callable distance function or None. If 'softdtw' is passed, a normalized version of Soft-DTW is used that is defined as `sdtw_(x,y) := sdtw(x,y) - 1/2(sdtw(x,x)+sdtw(y,y))`. If X is the distance array itself, use ``metric="precomputed"``. If None, dtw is used. sample_size : int or None (default: None) The size of the sample to use when computing the Silhouette Coefficient on a random subset of the data. If ``sample_size is None``, no sampling is used. metric_params : dict or None (default: None) Parameter values for the chosen metric. For metrics that accept parallelization of the cross-distance matrix computations, `n_jobs` key passed in `metric_params` is overridden by the `n_jobs` argument. n_jobs : int or None, optional (default=None) The number of jobs to run in parallel for cross-distance matrix computations. Ignored if the cross-distance matrix cannot be computed using parallelization. ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context. ``-1`` means using all processors. See scikit-learns' `Glossary <https://scikit-learn.org/stable/glossary.html#term-n_jobs>`_ for more details. verbose : int (default: 0) If nonzero, print information about the inertia while learning the model and joblib progress messages are printed. random_state : int, RandomState instance or None, optional (default: None) The generator used to randomly select a subset of samples.  If int, random_state is the seed used by the random number generator; If RandomState instance, random_state is the random number generator; If None, the random number generator is the RandomState instance used by `np.random`. Used when ``sample_size is not None``. **kwds : optional keyword parameters Any further parameters are passed directly to the distance function, just as for the `metric_params` parameter. Returns ------- silhouette : float

### Goal
Compute the mean Silhouette Coefficient to evaluate the quality and separation of time-series clusters.

### Parameters
- `X`: Array of pairwise distances `[n_ts, n_ts]` if `metric == "precomputed"`, or a time-series dataset `[n_ts, sz, d]` otherwise.
- `labels`: Predicted cluster labels for each time series, shape `[n_ts]`.
- `metric`, default `None`: The metric to use when calculating distance between time series. Should be one of `{'dtw', 'softdtw', 'euclidean'}`, a callable distance function, or `"precomputed"`. If `None`, `"dtw"` is used.
- `sample_size`, default `None`: The size of the sample to use when computing the Silhouette Coefficient on a random subset of the data. If `None`, no sampling is used.
- `metric_params`, default `None`: Dictionary of parameter values for the chosen metric.
- `n_jobs`, default `None`: The number of jobs to run in parallel for cross-distance matrix computations.
- `verbose`, default `0`: If nonzero, prints joblib progress messages.
- `random_state`, default `None`: The generator used to randomly select a subset of samples when `sample_size` is not `None`.
- `**kwds`: Any further parameters are passed directly to the distance function.

### Input
- If `metric` is a time-series metric (e.g., `"dtw"`, `"softdtw"`), `X` must be a strictly formatted 3D NumPy array of shape `(n_ts, max_sz, d)`.
- If `metric="precomputed"`, `X` must be a 2D NumPy array of shape `(n_ts, n_ts)` representing a precomputed pairwise distance matrix.
- `labels` must be a 1D array-like of length `n_ts` containing the cluster assignments.

### Output
Returns `float` — The mean Silhouette Coefficient for all samples, where a higher score indicates better-defined clusters (ranging from -1 to 1).

### Valid Call Patterns
```python
import numpy as np
import math
from tslearn.clustering import silhouette_score
from tslearn.generators import random_walks
from tslearn.metrics import cdist_dtw

# Generate synthetic time-series data and random cluster labels
np.random.seed(0)
X = random_walks(n_ts=20, sz=16, d=1)
labels = np.random.randint(2, size=20)

# 1. Compute silhouette score using a built-in time-series metric
score_dtw = silhouette_score(X, labels, metric="dtw")
assert math.isclose(score_dtw, 0.13383800, rel_tol=1e-07)
print(f"DTW Silhouette Score: {score_dtw}")

# 2. Compute silhouette score using a precomputed distance matrix
dist_matrix = cdist_dtw(X)
score_precomputed = silhouette_score(dist_matrix, labels, metric="precomputed")
assert math.isclose(score_precomputed, 0.13383800, rel_tol=1e-07)
print(f"Precomputed Silhouette Score: {score_precomputed}")
```

### LLM Instruction Prompt
- When calling `tslearn.clustering.silhouette_score`, ensure `X` matches the expected dimensionality for the chosen `metric`.
- If `metric` is `"dtw"`, `"softdtw"`, or `"euclidean"`, `X` MUST be a 3D array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` if the data is not already in this format.
- If `metric="precomputed"`, `X` MUST be a 2D array `(n_ts, n_ts)` containing pairwise distances.
- `labels` must be a 1D array of length `n_ts`.

### Prompt Snippet
```text
tslearn.clustering.silhouette_score(X, labels, metric=None, sample_size=None, metric_params=None, n_jobs=None, verbose=0, random_state=None, **kwds)
Computes the mean Silhouette Coefficient. If metric is a time-series metric (e.g., 'dtw', 'softdtw'), X must be a 3D array (n_ts, max_sz, d). If metric='precomputed', X must be a 2D pairwise distance matrix (n_ts, n_ts). labels must be a 1D array of length n_ts.
```

### Common Failure Modes
- **Dimensionality Error (3D vs 2D):** Passing a 2D array of raw time series when `metric="dtw"`. `tslearn` strictly requires a 3D array `(n_ts, max_sz, d)` for raw time-series data.
- **Dimensionality Error (Precomputed):** Passing a 3D array when `metric="precomputed"`. The function expects a 2D square distance matrix `(n_ts, n_ts)`.
- **Length Mismatch:** Providing a `labels` array whose length does not match `n_ts` (the first dimension of `X`).

### Fix Code Hint
```python
# If you have raw 2D time-series data (n_ts, max_sz) and want to use DTW:
from tslearn.utils import to_time_series_dataset
X_3d = to_time_series_dataset(X_raw)
score = silhouette_score(X_3d, labels, metric="dtw")

# If you have a precomputed distance matrix:
score = silhouette_score(dist_matrix, labels, metric="precomputed")
```

## API Test: `soft_dtw`

### Signature
```python
def soft_dtw(ts1, ts2, gamma=1.0, be=None, compute_with_backend=False)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:530_

### Goal
Compute the Soft Dynamic Time Warping (Soft-DTW) similarity metric between two time series, with optional support for automatic differentiation via the PyTorch backend.

### Parameters
- `ts1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `ts2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `gamma`, default `1.0`: float. The smoothing parameter for the soft-min operator. In the limit case `gamma=0`, it reduces to a hard-min operator (yielding the square of the standard DTW distance).
- `be`, default `None`: Backend object, string (`"numpy"` or `"pytorch"`), or `None`. If `None`, the backend is automatically inferred from the input array types.
- `compute_with_backend`, default `False`: bool. If `True` and a non-NumPy backend is used, the computation is strictly performed in that backend (required for PyTorch gradient tracking). If `False`, it may convert inputs to NumPy to accelerate the computation.

### Input
Two individual time series provided as 1D or 2D NumPy arrays, lists, or PyTorch tensors. They can have different lengths (`sz1` vs `sz2`) but must have the same number of dimensions `d`. If automatic differentiation is required, inputs must be PyTorch tensors with `requires_grad=True`.

### Output
Returns `unspecified` — A scalar float representing the Soft-DTW similarity. If the PyTorch backend is used and `compute_with_backend=True`, it returns a 0-dimensional PyTorch tensor attached to a computation graph (e.g., `grad_fn=<SelectBackward0>`).

### Valid Call Patterns
```python
import numpy as np
import torch
from tslearn.metrics import soft_dtw

# 1. Standard NumPy evaluation
ts1_np = np.array([[1.0], [2.0], [2.0], [3.0]])
ts2_np = np.array([[1.0], [2.0], [3.0], [4.0]])
sim_np = soft_dtw(ts1_np, ts2_np, gamma=1.0)
assert isinstance(sim_np, float)

# 2. PyTorch evaluation with automatic differentiation
ts1_pt = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True)
ts2_pt = torch.tensor([[3.0], [4.0], [-3.0]])
sim_pt = soft_dtw(
    ts1=ts1_pt, 
    ts2=ts2_pt, 
    gamma=1.0, 
    be="pytorch", 
    compute_with_backend=True
)
sim_pt.backward()
assert ts1_pt.grad is not None
```

### LLM Instruction Prompt
- When computing gradients for neural network integration, you MUST pass `compute_with_backend=True` and ensure inputs are PyTorch tensors with `requires_grad=True`.
- Do not pass full 3D datasets `(n_ts, max_sz, d)` to `soft_dtw`. It is a pairwise metric designed for individual 1D or 2D time series `(sz, d)`.
- Remember that `soft_dtw` with `gamma=0.0` computes the *square* of the DTW distance, not the standard DTW distance.

### Prompt Snippet
```text
When using `tslearn.metrics.soft_dtw` to compute differentiable alignment losses in PyTorch, ensure you explicitly set `compute_with_backend=True`. Otherwise, the function defaults to accelerating the computation via NumPy, which detaches the result from the PyTorch computation graph and causes `.backward()` to fail.
```

### Common Failure Modes
- **Missing Gradient Graph**: Calling `soft_dtw(ts1, ts2, be="pytorch")` without `compute_with_backend=True` returns a value detached from the PyTorch graph, raising an error when `.backward()` is called.
- **Dimensionality Error**: Passing a 3D dataset array `(n_ts, sz, d)` instead of a single time series `(sz, d)`.
- **Feature Dimension Mismatch**: Passing two time series with different feature dimensions `d` (e.g., `(10, 2)` and `(15, 3)`).

### Fix Code Hint
```python
# BAD: Will not track gradients because compute_with_backend defaults to False
loss = soft_dtw(tensor_a, tensor_b, gamma=0.1, be="pytorch")
loss.backward() # Fails

# GOOD: Explicitly forces the backend to retain the computation graph
loss = soft_dtw(tensor_a, tensor_b, gamma=0.1, be="pytorch", compute_with_backend=True)
loss.backward() # Succeeds
```

## API Test: `soft_dtw_alignment`

### Signature
```python
def soft_dtw_alignment(ts1, ts2, gamma=1.0, be=None, compute_with_backend=False)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:641_

_Source doc:_ Compute Soft-DTW metric between two time series and return both the similarity measure and the alignment matrix. Soft-DTW was originally presented in [1]_ and is discussed in more details in our :ref:`user-guide page on DTW and its variants<dtw>`. Soft-DTW is computed as: .. math:: \text{soft-DTW}_{\gamma}(X, Y) = \min_{\pi}{}^\gamma \sum_{(i, j) \in \pi} \|X_i, Y_j\|^2 where :math:`\min^\gamma` is the soft-min operator of parameter :math:`\gamma`. In the limit case :math:`\gamma = 0`, :math:`\min^\gamma` reduces to a hard-min operator and soft-DTW is defined as the square of the DTW similarity measure. Parameters ---------- ts1 : array-like, shape=(sz1, d) or (sz1,) A time series. If shape is (sz1,), the time series is assumed to be univariate. ts2 : array-like, shape=(sz2, d) or (sz2,) Another time series. If shape is (sz2,), the time series is assumed to be univariate. gamma : float (default 1.) Gamma parameter for Soft-DTW. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. compute_with_backend : bool, default=False This parameter has no influence when the NumPy backend is used. When a backend different from NumPy is used (cf parameter `be`): If `True`, the computation is done with the corresponding backend. If `False`, a conversion to the NumPy backend can be used to accelerate the computation. Returns ------- array-like, shape=(sz1, sz2) Soft-alignment matrix float Similarity Examples -------- >>> a, dist = soft_dtw_alignment([1, 2, 2, 3], ...                              [1., 2., 3., 4.], ...                              gamma=1.)  # doctest: +ELLIPSIS >>> float(dist) -0.89... >>> a  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE array([[1.00...e+00, 1.88...e-01, 2.83...e-04, 4.19...e-11],

### Goal
Compute the Soft-DTW metric between two individual time series, returning both the soft-alignment matrix and the similarity measure.

### Parameters
- `ts1`: array-like, shape `(sz1, d)` or `(sz1,)`. The first time series. If 1D, it is assumed to be univariate.
- `ts2`: array-like, shape `(sz2, d)` or `(sz2,)`. The second time series. If 1D, it is assumed to be univariate.
- `gamma`, default `1.0`: float. The gamma parameter controlling the soft-min operator. A value of `0.0` reduces the operation to a hard-min operator (equivalent to the square of the standard DTW similarity).
- `be`, default `None`: Backend object or string (`"numpy"` or `"pytorch"`). If `None`, the backend is automatically determined by the input array types.
- `compute_with_backend`, default `False`: bool. If `True` and a non-NumPy backend (like PyTorch) is used, the computation is strictly performed in that backend (required for automatic differentiation). If `False`, it may convert to NumPy to accelerate computation.

### Input
Two individual time series arrays or tensors. Unlike `tslearn` estimators which require 3D datasets `(n_ts, max_sz, d)`, this metric function expects 1D `(sz,)` or 2D `(sz, d)` inputs representing single time series. The lengths `sz1` and `sz2` can differ, but the feature dimension `d` must match. Inputs can be NumPy arrays or PyTorch tensors.

### Output
Returns a tuple `(alignment_matrix, similarity)` where:
- `alignment_matrix` is an array-like (NumPy array or PyTorch tensor) of shape `(sz1, sz2)` representing the soft-alignment path.
- `similarity` is a float (or a 0-dimensional PyTorch tensor) representing the Soft-DTW similarity measure.

### Valid Call Patterns
```python
import tslearn.metrics
import numpy as np

# 1. Standard NumPy usage
s1 = np.array([[1.0], [2.0], [2.0], [3.0]])
s2 = np.array([[1.0], [2.0], [3.0], [4.0]])

matrix_path, dist = tslearn.metrics.soft_dtw_alignment(s1, s2, gamma=1.0)

assert matrix_path.shape == (4, 4)
assert isinstance(dist, float)

# 2. PyTorch usage with gradients
import torch
ts1 = torch.tensor([[1.0], [2.0]], requires_grad=True)
ts2 = torch.tensor([[1.0], [3.0]])

# compute_with_backend=True is required to keep the computation graph intact
matrix_path_pt, dist_pt = tslearn.metrics.soft_dtw_alignment(
    ts1, ts2, gamma=0.5, be="pytorch", compute_with_backend=True
)

assert matrix_path_pt.shape == (2, 2)
assert dist_pt.requires_grad
```

### LLM Instruction Prompt
- When computing Soft-DTW alignments, pass individual time series `(sz, d)`, not full 3D datasets `(n_ts, max_sz, d)`.
- If you need to compute gradients using PyTorch (`.backward()`), you MUST pass `compute_with_backend=True` and ensure inputs are PyTorch tensors with `requires_grad=True`. Otherwise, the function defaults to accelerating via NumPy, which breaks the computation graph.
- To compute the exact square of the standard DTW distance and its hard-alignment path, set `gamma=0.0`.

### Prompt Snippet
```text
Use `tslearn.metrics.soft_dtw_alignment(ts1, ts2, gamma=1.0)` to get both the alignment matrix and the distance. Remember to set `compute_with_backend=True` if you are passing PyTorch tensors and need to backpropagate through the similarity measure.
```

### Common Failure Modes
- **Passing 3D arrays**: Providing a dataset of shape `(n_ts, max_sz, d)` instead of a single time series `(sz, d)` will result in shape mismatch errors or incorrect distance calculations.
- **Losing PyTorch Gradients**: Calling the function with PyTorch tensors but leaving `compute_with_backend=False` (the default). The function will silently convert to NumPy for speed, returning a float or a detached tensor without a `grad_fn`.
- **Dimension Mismatch**: Passing two time series with different feature dimensions `d` (e.g., `(10, 2)` and `(15, 3)`).

### Fix Code Hint
```python
# BAD: Passing 3D datasets to a pairwise metric
# matrix, dist = tslearn.metrics.soft_dtw_alignment(X_train, X_test)

# GOOD: Passing individual time series
matrix, dist = tslearn.metrics.soft_dtw_alignment(X_train[0], X_test[0], gamma=1.0)

# BAD: Expecting gradients without compute_with_backend=True
# matrix, dist = tslearn.metrics.soft_dtw_alignment(tensor1, tensor2, be="pytorch")
# dist.backward() # Fails: no grad_fn

# GOOD: Enabling backend computation for autograd
matrix, dist = tslearn.metrics.soft_dtw_alignment(
    tensor1, tensor2, be="pytorch", compute_with_backend=True
)
dist.backward()
```

## API Test: `softdtw_barycenter`

### Signature
```python
def softdtw_barycenter(X, gamma=1.0, weights=None, method='L-BFGS-B', tol=0.001, max_iter=50, init=None)
```
_Source: tslearn/tslearn/barycenters/softdtw.py:38_

_Source doc:_ Compute barycenter (time series averaging) under the soft-DTW geometry. Soft-DTW was originally presented in [1]_. Parameters ---------- X : array-like, shape=(n_ts, sz, d) Time series dataset. gamma: float Regularization parameter. Lower is less smoothed (closer to true DTW). weights: None or array Weights of each X[i]. Must be the same size as len(X). If None, uniform weights are used. method: string Optimization method, passed to `scipy.optimize.minimize`. Default: L-BFGS. tol: float Tolerance of the method used. max_iter: int Maximum number of iterations. init: array or None (default: None) Initial barycenter to start from for the optimization process. If `None`, euclidean barycenter is used as a starting point. Returns ------- numpy.array of shape (bsz, d) where `bsz` is the size of the `init` array \ if provided or `sz` otherwise Soft-DTW barycenter of the provided time series dataset. Examples -------- >>> time_series = [[1, 2, 3, 4], [1, 2, 4, 5]] >>> softdtw_barycenter(time_series, max_iter=5) array([[1.25161574], [2.03821705], [3.5101956 ], [4.36140605]]) >>> time_series = [[1, 2, 3, 4], [1, 2, 3, 4, 5]] >>> softdtw_barycenter(time_series, max_iter=5) array([[1.21349933], [1.8932251 ], [2.67573269], [3.51057026], [4.33645802]]) References ---------- .. [1] M. Cuturi, M. Blondel "Soft-DTW: a Differentiable Loss Function for Time-Series," ICML 2017.

### Goal
Compute the barycenter (time series average) of a dataset under the differentiable Soft-DTW (Dynamic Time Warping) geometry.

### Parameters
- `X`: Time series dataset, array-like of shape `(n_ts, sz, d)` where `n_ts` is the number of time series, `sz` is the maximum length, and `d` is the dimensionality.
- `gamma`, default `1.0`: Regularization parameter (float). Lower values result in less smoothing, making the metric closer to true DTW.
- `weights`, default `None`: Weights for each time series in `X`. Must be an array of the same size as `len(X)`. If `None`, uniform weights are used.
- `method`, default `'L-BFGS-B'`: Optimization method passed to `scipy.optimize.minimize` (string).
- `tol`, default `0.001`: Tolerance for the optimization method (float).
- `max_iter`, default `50`: Maximum number of iterations for the optimization process (int).
- `init`, default `None`: Initial barycenter array to start the optimization from. If `None`, the Euclidean barycenter is used as the starting point.

### Input
A collection of time series formatted as a strict 3D array-like structure of shape `(n_ts, max_sz, d)`. If starting from raw lists or variable-length sequences, the data must first be converted using `tslearn.utils.to_time_series_dataset`, which will pad shorter series with `nan` values to match `max_sz`.

### Output
Returns `unspecified` — A `numpy.ndarray` of shape `(bsz, d)` representing the Soft-DTW barycenter of the provided dataset. The length `bsz` is the size of the `init` array if one was provided, or `sz` (the maximum length of the input time series) otherwise.

### Valid Call Patterns
```python
import numpy as np
import tslearn.barycenters

# 1. Generate a small synthetic 3D time-series dataset: (n_ts=15, sz=10, d=3)
rng = np.random.RandomState(0)
time_series = rng.randn(15, 10, 3)

# 2. Compute the Soft-DTW barycenter with a small max_iter for fast execution
sdtw_bar = tslearn.barycenters.softdtw_barycenter(time_series, max_iter=5)

# 3. Verify the output shape matches (sz, d) since no `init` was provided
assert sdtw_bar.shape == (10, 3)
print(f"Computed Soft-DTW barycenter of shape: {sdtw_bar.shape}")
```

### LLM Instruction Prompt
- When calling `tslearn.barycenters.softdtw_barycenter`, ensure the input `X` is strictly a 3D array of shape `(n_ts, max_sz, d)`. If the input is a list of lists or variable-length arrays, preprocess it with `tslearn.utils.to_time_series_dataset` first.
- Keep `max_iter` small (e.g., 5 to 10) in testing or CI environments to prevent the `L-BFGS-B` optimization from causing long execution times.
- If providing `weights`, ensure the length of the weights array exactly matches `len(X)`.

### Prompt Snippet
```text
To compute the Soft-DTW average of a set of time series, use `tslearn.barycenters.softdtw_barycenter`. The input must be a 3D array `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset` to format raw lists. Set `max_iter` to a small integer for quick tests.
```

### Common Failure Modes
- **ValueError due to 1D/2D input**: Passing a flat list or a 2D array `(n_ts, max_sz)` without the required third dimension `d` will cause shape mismatch errors.
- **ValueError due to mismatched weights**: Providing a `weights` array that does not equal `len(X)` will raise an error.
- **Slow execution**: Leaving `max_iter` at its default (50) or higher on large datasets can cause the optimization to run for a very long time.

### Fix Code Hint
```python
# FIX: Convert 2D lists/arrays to the required 3D format before computing the barycenter
from tslearn.utils import to_time_series_dataset
from tslearn.barycenters import softdtw_barycenter

raw_data = [[1, 2, 3, 4], [1, 2, 4, 5]]
# Converts to shape (2, 4, 1)
X_formatted = to_time_series_dataset(raw_data) 

barycenter = softdtw_barycenter(X_formatted, max_iter=5)
```

## API Test: `sqrt`

### Signature
```python
def sqrt(self, x, out=None)
```

### Goal
Compute the element-wise square root of an array or tensor using the dynamically selected computational backend (NumPy or PyTorch).

### Parameters
- `self`: The instantiated backend object (e.g., `NumPyBackend` or `PyTorchBackend`) on which this method is called.
- `x`: The input numerical array or tensor for which to compute the square root.
- `out`, default `None`: An optional pre-allocated array or tensor of the same shape and type as `x` to store the result.

### Input
- `x` must be a backend-compatible data structure (a `numpy.ndarray` for the NumPy backend, or a `torch.Tensor` for the PyTorch backend) containing non-negative numerical values.
- If `out` is provided, it must be compatible with the active backend and match the shape of `x`.

### Output
Returns `unspecified` — An array or tensor of the same type and shape as `x` containing the element-wise square root values. If the PyTorch backend is used and the input tensor requires gradients, the output tensor will be attached to the computation graph.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# 1. Instantiate the backend (defaults to NumPy if "numpy" is passed)
backend = instantiate_backend("numpy")
x = np.array([0.0, 4.0, 16.0])

# 2. Call the backend's sqrt method
result = backend.sqrt(x)

# 3. Assert falsifiable properties
assert backend.belongs_to_backend(result), "Result must belong to the active backend"
np.testing.assert_allclose(result, [0.0, 2.0, 4.0])
print("sqrt computed successfully.")
```

### LLM Instruction Prompt
- Always call `sqrt` as an instance method on a backend object (e.g., `backend.sqrt(x)`), never as a standalone function.
- Use this backend method instead of `numpy.sqrt` or `math.sqrt` when writing backend-agnostic code or processing metric outputs that might be PyTorch tensors requiring gradients.
- Ensure the input data type matches the instantiated backend (NumPy arrays for `NumPyBackend`, PyTorch tensors for `PyTorchBackend`).

### Prompt Snippet
```text
# Correct backend-agnostic square root computation
from tslearn.backend import instantiate_backend

backend = instantiate_backend(input_data)
result = backend.sqrt(input_data)
```

### Common Failure Modes
- **Standalone Function Call:** Attempting to import and call `sqrt(x)` directly instead of calling it on a backend instance (`backend.sqrt(x)`), which will raise a `NameError` or `TypeError`.
- **Type Mismatch:** Passing a PyTorch tensor to a NumPy backend instance, or vice versa, which will raise backend-specific type errors.
- **Negative Inputs:** Passing arrays with negative values, which will result in `NaN` values in the output without raising an explicit exception.

### Fix Code Hint
```python
# BAD: Calling as a standalone function or using np.sqrt on a PyTorch tensor
# dist = sqrt(x)
# dist = np.sqrt(tensor_x)

# GOOD: Instantiate the backend and call its sqrt method
from tslearn.backend import instantiate_backend
backend = instantiate_backend(x)
dist = backend.sqrt(x)
```

## API Test: `str_to_time_series`

### Signature
```python
def str_to_time_series(ts_str)
```
_Source: tslearn/tslearn/utils/utils.py:326_

_Source doc:_ Reads a time series from its string representation (used when loading time series from disk). Parameters ---------- ts_str : string String representation of the time-series. Returns ------- numpy.ndarray Represented time-series. Examples -------- >>> str_to_time_series("1 2 3 4") array([[1.], [2.], [3.], [4.]]) >>> str_to_time_series("1 2|3 4") array([[1., 3.], [2., 4.]]) See Also -------- load_time_series_txt : Load time series from disk time_series_to_str : Transform a time series into a string

### Goal
Parses a string representation of a single time series into a 2D NumPy array, handling multi-dimensional data separated by pipe (`|`) characters.

### Parameters
- `ts_str`: A string containing the time-series data. Spaces separate individual timestamps within a dimension, and the pipe character (`|`) separates distinct dimensions.

### Input
A properly formatted string representing a single time series. If the time series is multi-dimensional, each dimension's sequence of values must be separated by a `|` and should ideally contain the same number of timestamps.

### Output
Returns `unspecified` — A 2D `numpy.ndarray` of shape `(n_timestamps, n_dimensions)` representing the parsed time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import str_to_time_series

# 1. Parse a 1D time series (4 timestamps, 1 dimension)
ts_1d = str_to_time_series("1.0 2.0 3.0 4.0")
assert ts_1d.shape == (4, 1), f"Expected shape (4, 1), got {ts_1d.shape}"
assert np.allclose(ts_1d, [[1.], [2.], [3.], [4.]])

# 2. Parse a 2D time series (2 timestamps, 2 dimensions)
# "1 2" is dimension 0, "3 4" is dimension 1
ts_2d = str_to_time_series("1 2|3 4")
assert ts_2d.shape == (2, 2), f"Expected shape (2, 2), got {ts_2d.shape}"
assert np.allclose(ts_2d, [[1., 3.], [2., 4.]])

print("str_to_time_series correctly parsed string representations.")
```

### LLM Instruction Prompt
- Use `str_to_time_series` to deserialize a single time series from a string format.
- Remember that spaces separate timestamps for a single dimension, and the pipe character (`|`) separates distinct dimensions.
- The function returns a 2D array `(n_timestamps, n_dimensions)`. Because `tslearn` estimators strictly require 3D arrays `(n_ts, max_sz, d)`, you must wrap the output in a list and pass it to `to_time_series_dataset` (or manually reshape it) before using it in a model.

### Prompt Snippet
```text
When parsing time series from strings using `tslearn.utils.str_to_time_series`, note that the returned array is 2D `(n_timestamps, n_dimensions)`. To use it with `tslearn` estimators, you must reshape it or pass it through `to_time_series_dataset` to achieve the required 3D `(n_ts, max_sz, d)` shape.
```

### Common Failure Modes
- **Assuming a 3D Output:** Passing the direct output of `str_to_time_series` to an estimator like `TimeSeriesKMeans` will fail because the output is 2D, not the required 3D `(n_ts, max_sz, d)` format.
- **Malformed Strings:** Providing strings with mismatched numbers of timestamps across dimensions (e.g., `"1 2 3|4 5"`) can lead to ragged arrays or parsing errors.
- **Incorrect Delimiters:** Using commas instead of spaces to separate timestamps, which will fail to parse into floats.

### Fix Code Hint
```python
# BAD: Passing 2D output directly to an estimator
ts = str_to_time_series("1 2 3 4")
# model.fit(ts)  # Raises ValueError due to 2D shape

# GOOD: Convert to the required 3D dataset format
from tslearn.utils import to_time_series_dataset
ts = str_to_time_series("1 2 3 4")
X = to_time_series_dataset([ts]) # Shape becomes (1, 4, 1)
# model.fit(X)
```

## API Test: `subsequence_cost_matrix`

### Signature
```python
def subsequence_cost_matrix(subseq, longseq, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1236_

_Source doc:_ Compute the accumulated cost matrix score between a subsequence and a reference time series. Parameters ---------- subseq : array-like, shape=(sz1, d) or (sz1,) Subsequence time series. If shape is (sz1,), the time series is assumed to be univariate. longseq : array-like, shape=(sz2, d) or (sz2,) Reference time series. If shape is (sz2,), the time series is assumed to be univariate. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- mat : array-like, shape=(sz1, sz2) Accumulated cost matrix.

### Goal
Compute the accumulated cost matrix between a shorter subsequence time series and a longer reference time series to facilitate subsequence alignment and matching.

### Parameters
- `subseq`: Array-like of shape `(sz1, d)` or `(sz1,)`. The shorter subsequence time series to align. If 1D, it is assumed to be univariate.
- `longseq`: Array-like of shape `(sz2, d)` or `(sz2,)`. The longer reference time series to search within. If 1D, it is assumed to be univariate.
- `be`, default `None`: The computational backend to use. Can be a string (`"numpy"` or `"pytorch"`), a Backend instance, or `None`. If `None`, the backend is automatically determined by the input array types.

### Input
Individual time series arrays (not full 3D datasets). Inputs can be standard Python lists, NumPy arrays, or PyTorch tensors. They should represent a single time series of shape `(sz, d)` or `(sz,)`. It is recommended to format raw lists using `tslearn.utils.to_time_series` before passing them to this function.

### Output
Returns `unspecified` — An array-like (NumPy array or PyTorch tensor, depending on the active backend) of shape `(sz1, sz2)` representing the accumulated cost matrix between the two sequences.

### Valid Call Patterns
```python
import numpy as np
import tslearn.metrics
from tslearn.utils import to_time_series

# Define a short subsequence and a longer reference sequence
subseq = to_time_series([1, 4])
longseq = to_time_series([1.0, 2.0, 2.0, 3.0, 4.0])

# Compute the accumulated cost matrix
cost_matrix = tslearn.metrics.subsequence_cost_matrix(subseq, longseq, be="numpy")

# Verify the shape of the resulting matrix (sz1, sz2)
assert cost_matrix.shape == (2, 5)
print("Cost matrix shape verified:", cost_matrix.shape)
```

### LLM Instruction Prompt
- When computing a subsequence cost matrix, ensure the inputs are individual time series of shape `(sz, d)` or `(sz,)`, not full 3D datasets `(n_ts, sz, d)`.
- Use `tslearn.utils.to_time_series` to format raw lists into the correct 2D shape before passing them to `subsequence_cost_matrix`.
- The returned matrix will have the shape `(len(subseq), len(longseq))`.

### Prompt Snippet
```text
tslearn.metrics.subsequence_cost_matrix(subseq, longseq, be=None) computes the accumulated cost matrix between a subsequence (sz1, d) and a reference series (sz2, d). Returns a matrix of shape (sz1, sz2). Do not pass full 3D datasets (n_ts, sz, d) to this metric.
```

### Common Failure Modes
- **Passing 3D datasets**: Providing a full dataset of shape `(n_ts, sz, d)` instead of a single time series `(sz, d)` will result in shape mismatch errors or incorrect distance calculations.
- **Mismatched dimensions**: Passing a `subseq` with `d1` dimensions and a `longseq` with `d2` dimensions where `d1 != d2`. Both time series must have the same number of features.

### Fix Code Hint
```python
# BAD: Passing a full 3D dataset to a metric expecting a single time series
# cost_matrix = tslearn.metrics.subsequence_cost_matrix(X_train, X_test)

# GOOD: Extracting individual time series or using to_time_series
from tslearn.utils import to_time_series
subseq = to_time_series([1, 4])
longseq = to_time_series([1.0, 2.0, 2.0, 3.0, 4.0])
cost_matrix = tslearn.metrics.subsequence_cost_matrix(subseq, longseq)
```

## API Test: `subsequence_path`

### Signature
```python
def subsequence_path(acc_cost_mat, idx_path_end, be=None)
```
_Source: tslearn/tslearn/metrics/dtw_variants.py:1367_

_Source doc:_ Compute the optimal path through an accumulated cost matrix given the endpoint of the sequence. Parameters ---------- acc_cost_mat: array-like, shape=(sz1, sz2) Accumulated cost matrix comparing subsequence from a longer sequence. idx_path_end: int The end position of the matched subsequence in the longer sequence. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- path: list of tuples of integer pairs Matching path represented as a list of index pairs. In each pair, the first index corresponds to `subseq` and the second one corresponds to `longseq`. The startpoint of the Path is :math:`P_0 = (0, ?)` and it ends at :math:`P_L = (len(subseq)-1, idx\_path\_end)` Examples -------- >>> acc_cost_mat = numpy.array([[1., 0., 0., 1., 4.], ...                             [5., 1., 1., 0., 1.]]) >>> # calculate the globally optimal path >>> optimal_end_point = numpy.argmin(acc_cost_mat[-1, :]) >>> path = subsequence_path(acc_cost_mat, optimal_end_point) >>> path [(0, 2), (1, 3)] See Also -------- dtw_subsequence_path : Get the similarity score for DTW subsequence_cost_matrix: Calculate the required cost matrix

### Goal
Compute the optimal alignment path through an accumulated cost matrix for a subsequence matched within a longer time series, backtracking from a specified endpoint.

### Parameters
- `acc_cost_mat`: array-like, shape=(sz1, sz2). The 2D accumulated cost matrix comparing a subsequence (length `sz1`) to a longer sequence (length `sz2`).
- `idx_path_end`: int. The index in the longer sequence where the matched subsequence ends (typically found by taking the `argmin` of the last row of the cost matrix).
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. Determines the computational backend. If `None`, the backend is automatically inferred from the input arrays.

### Input
`acc_cost_mat` must be a 2D array-like structure (NumPy array or PyTorch tensor) representing accumulated alignment costs, typically generated by `tslearn.metrics.subsequence_cost_matrix`. `idx_path_end` must be a valid integer index within the bounds of the second dimension of `acc_cost_mat` (i.e., `0 <= idx_path_end < sz2`).

### Output
Returns `unspecified` — A list of tuples of integer pairs representing the matching path. In each pair `(i, j)`, the first index `i` corresponds to the subsequence and the second index `j` corresponds to the longer sequence. The path starts at `(0, ?)` and ends at `(len(subseq)-1, idx_path_end)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics import subsequence_path

# Example accumulated cost matrix (subsequence length 2, long sequence length 5)
acc_cost_mat = np.array([
    [1., 0., 0., 1., 4.],
    [5., 1., 1., 0., 1.]
])

# Calculate the globally optimal path by finding the minimum cost in the last row
optimal_end_point = int(np.argmin(acc_cost_mat[-1, :]))

# Compute the path backtracking from the optimal endpoint
path = subsequence_path(acc_cost_mat, optimal_end_point)

# Verify the path matches the expected alignment
assert path == [(0, 2), (1, 3)]
assert isinstance(path, list)
```

### LLM Instruction Prompt
When calling `tslearn.metrics.subsequence_path`, ensure `acc_cost_mat` is a 2D array-like object (NumPy array or PyTorch tensor) representing the accumulated cost matrix, NOT the raw time series. The `idx_path_end` must be a valid integer index representing the end of the match in the longer sequence, typically found via `numpy.argmin(acc_cost_mat[-1, :])`.

### Prompt Snippet
```text
tslearn.metrics.subsequence_path(acc_cost_mat, idx_path_end, be=None)
Computes the optimal alignment path through a 2D accumulated cost matrix. `acc_cost_mat` must be a 2D array (e.g., from `subsequence_cost_matrix`). `idx_path_end` is the integer end position in the longer sequence. Returns a list of `(subseq_idx, longseq_idx)` tuples.
```

### Common Failure Modes
- Passing raw time-series arrays directly to `subsequence_path` instead of the accumulated cost matrix (which should be computed first via `tslearn.metrics.subsequence_cost_matrix`).
- Providing an `idx_path_end` that is out of bounds for the second dimension of `acc_cost_mat` (e.g., `>= acc_cost_mat.shape[1]`).
- Passing a 1D or 3D array for `acc_cost_mat` instead of a strictly 2D matrix.

### Fix Code Hint
```python
# INCORRECT: Passing raw time series
# path = subsequence_path(subseq, longseq, end_idx)

# CORRECT: Compute the cost matrix first, then find the path
from tslearn.metrics import subsequence_cost_matrix, subsequence_path
import numpy as np

cost_matrix = subsequence_cost_matrix(subseq, longseq)
optimal_end_point = int(np.argmin(cost_matrix[-1, :]))
path = subsequence_path(cost_matrix, optimal_end_point)
```

## API Test: `support_`

### Signature
```python
def support_(self)
```
_Source: tslearn/tslearn/svm/svm.py:24_

### Goal
Retrieves the indices of the support vectors from a fitted time-series Support Vector Machine (SVM) model, mirroring the `scikit-learn` API convention.

### Parameters
- `self`: A fitted `tslearn.svm.TimeSeriesSVC` or `tslearn.svm.TimeSeriesSVR` estimator instance.

### Input
The estimator must already be fitted using `.fit(X, y)`, where `X` is a strictly formatted 3D `numpy` array of shape `(n_ts, max_sz, d)` representing the time-series dataset, and `y` contains the corresponding target labels or values.

### Output
Returns `unspecified` — typically a 1D `numpy` array containing the integer indices of the training samples that were selected as support vectors by the underlying SVM backend.

### Valid Call Patterns
```python
# Inferred from signature and scikit-learn conventions (not verified)
import numpy as np
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare a small time-series dataset in the required 3D format
X = to_time_series_dataset([[1.0, 2.0], [1.0, 4.0], [9.0, 8.0], [8.0, 9.0]])
y = [0, 0, 1, 1]

# 2. Initialize and fit the TimeSeriesSVC
clf = TimeSeriesSVC(kernel="gak", random_state=42)
clf.fit(X, y)

# 3. Access the support_ property to get support vector indices
# Note: In the scikit-learn ecosystem, a trailing underscore denotes a fitted attribute/property.
support_indices = clf.support_

assert isinstance(support_indices, np.ndarray), "support_ should return a NumPy array of indices"
assert len(support_indices) > 0, "There should be at least one support vector"
print(f"Support vector indices: {support_indices}")
```

### LLM Instruction Prompt
- Access `support_` as a property (without parentheses) on a fitted `TimeSeriesSVC` or `TimeSeriesSVR` instance to get the indices of the support vectors.
- Ensure the model has been successfully fitted with `.fit(X, y)` before accessing `support_`.
- Remember that `X` must be preprocessed into the strict `(n_ts, max_sz, d)` 3D array format using `tslearn.utils.to_time_series_dataset` before fitting.

### Prompt Snippet
```text
Access the `support_` property on a fitted `tslearn.svm.TimeSeriesSVC` or `TimeSeriesSVR` to retrieve the indices of the support vectors. Do not call it as a method. The model must be fitted on a 3D time-series array `(n_ts, max_sz, d)` first.
```

### Common Failure Modes
- **`NotFittedError` or `AttributeError`**: Accessing `support_` before calling `.fit()` on the estimator. The underlying SVM model does not exist or has no support vectors until training is complete.
- **`TypeError`**: Attempting to call `support_()` as a method with parentheses. It is exposed as a property to match `scikit-learn`'s fitted attribute conventions.
- **`ValueError` during `.fit()`**: Passing a 1D or 2D array to `.fit()` instead of the required 3D array `(n_ts, max_sz, d)`, preventing the model from fitting and thus preventing access to `support_`.

### Fix Code Hint
```python
# 1. Ensure data is 3D
X_train_3d = to_time_series_dataset(X_train)

# 2. Fit the model first
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X_train_3d, y_train)

# 3. Access as a property, not a method
support_idx = clf.support_
```

## API Test: `support_vectors_`

### Signature
```python
def support_vectors_(self)
```
_Source: tslearn/tslearn/svm/svm.py:285  (+1 more definition site/overload)_

### Goal
Retrieves the support vectors of a fitted time-series Support Vector Machine (SVM) model, formatted as a 3D time-series array.

### Parameters
- `self`: A fitted instance of a `tslearn` SVM estimator (e.g., `tslearn.svm.TimeSeriesSVC` or `tslearn.svm.TimeSeriesSVR`).

### Input
The estimator must have been successfully fitted on a 3D time-series dataset of shape `(n_ts, max_sz, d)` using `.fit(X, y)`. 

### Output
Returns `unspecified` — A 3D `numpy` array of shape `(n_SV, max_sz, d)` containing the support vectors retained by the model, where `n_SV` is the number of support vectors.

### Valid Call Patterns
```python
import numpy as np
from tslearn.svm import TimeSeriesSVC
from tslearn.utils import to_time_series_dataset

# 1. Prepare 3D time-series data
X = to_time_series_dataset([[1.0, 2.0], [1.0, 4.0], [9.0, 8.0], [8.0, 9.0]])
y = [0, 0, 1, 1]

# 2. Fit the SVM classifier
clf = TimeSeriesSVC(kernel="gak")
clf.fit(X, y)

# 3. Access the support_vectors_ property (inferred from signature and scikit-learn conventions)
sv = clf.support_vectors_

assert isinstance(sv, np.ndarray)
assert sv.ndim == 3
print(f"Support vectors shape: {sv.shape}")
```

### LLM Instruction Prompt
- Access `support_vectors_` as a property on a fitted `TimeSeriesSVC` or `TimeSeriesSVR` instance. Do not call it as a method (no parentheses).
- Ensure the model is fitted before accessing this property.
- Expect the returned support vectors to be in the strict 3D `tslearn` format `(n_ts, max_sz, d)`.

### Prompt Snippet
```text
Access `support_vectors_` as a property (without parentheses) on a fitted `tslearn.svm.TimeSeriesSVC` or `TimeSeriesSVR` instance to retrieve the support vectors as a 3D numpy array.
```

### Common Failure Modes
- Accessing `support_vectors_` before calling `.fit()`, which raises an `AttributeError` or `NotFittedError`.
- Calling it as a method `clf.support_vectors_()` instead of accessing it as a property `clf.support_vectors_`, which raises a `TypeError` (e.g., `'numpy.ndarray' object is not callable`).
- Fitting the model with 2D data instead of the required 3D `(n_ts, max_sz, d)` format, causing `.fit()` to fail before the property can be accessed.

### Fix Code Hint
```python
# Ensure data is 3D before fitting
X_3d = to_time_series_dataset(X)
clf.fit(X_3d, y)

# Access as a property, not a method
sv = clf.support_vectors_
```

## API Test: `time_series_to_str`

### Signature
```python
def time_series_to_str(ts, fmt='%.18e')
```
_Source: tslearn/tslearn/utils/utils.py:289_

_Source doc:_ Transforms a time series to its representation as a string (used when saving time series to disk). Parameters ---------- ts : array-like Time series to be represented. fmt : string (default: "%.18e") Format to be used to write each value (only ASCII characters). Returns ------- string String representation of the time-series. Examples -------- >>> time_series_to_str([1, 2, 3, 4], fmt="%.1f") '1.0 2.0 3.0 4.0' >>> time_series_to_str([[1, 3], [2, 4]], fmt="%.1f") '1.0 2.0|3.0 4.0' See Also -------- load_time_series_txt : Load time series from disk str_to_time_series : Transform a string into a time series

### Goal
Transforms a single time series into a string representation, typically used for saving time-series data to disk in a text format.

### Parameters
- `ts`: Array-like representing a single time series (1D for univariate, 2D for multivariate with shape `(n_timestamps, n_dimensions)`).
- `fmt`, default `'%.18e'`: A C-style string format specifier (e.g., `'%.1f'`, `'%.18e'`) used to format each numeric value. Must contain only ASCII characters.

### Input
A single time series as a 1D or 2D array-like object. It must not be a full 3D dataset `(n_ts, max_sz, d)`. The `fmt` string must be compatible with the numeric types in `ts`.

### Output
Returns `unspecified` — A string representation of the time series. Values across time steps for a single dimension are separated by spaces, and multiple dimensions are separated by a pipe character (`|`).

### Valid Call Patterns
```python
from tslearn.utils import time_series_to_str

# 1D time series (1 dimension, 4 time steps)
ts_1d = [1, 2, 3, 4]
ts_str_1d = time_series_to_str(ts_1d, fmt="%.1f")
assert ts_str_1d == '1.0 2.0 3.0 4.0'
print("1D serialization correct")

# 2D time series (2 time steps, 2 dimensions)
ts_2d = [[1, 3], [2, 4]]
ts_str_2d = time_series_to_str(ts_2d, fmt="%.1f")
assert ts_str_2d == '1.0 2.0|3.0 4.0'
print("2D serialization correct")
```

### LLM Instruction Prompt
- Use `time_series_to_str` to serialize a single time series (not a full 3D dataset) into a string.
- Understand that the output string groups values by dimension, separated by `|`, with time steps separated by spaces.
- Ensure `fmt` is a valid C-style format string.

### Prompt Snippet
```text
`time_series_to_str(ts, fmt='%.18e')` serializes a single time series to a string. Dimensions are separated by `|` and time steps by spaces.
```

### Common Failure Modes
- Passing a full 3D dataset `(n_ts, max_sz, d)` instead of a single time series `(max_sz, d)`. This function serializes one time series at a time.
- Providing an invalid or incompatible C-style format string in `fmt`.

### Fix Code Hint
```python
# ERROR: Passing a 3D dataset to time_series_to_str
# ts_str = time_series_to_str(X_train, fmt="%.1f")

# FIX: Iterate over the dataset to serialize each time series individually
ts_strings = [time_series_to_str(ts, fmt="%.1f") for ts in X_train]
```

## API Test: `to_cesium_dataset`

### Signature
```python
def to_cesium_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:655_

_Source doc:_ Transform a tslearn-compatible dataset into a cesium dataset. Parameters ---------- X: array, shape = (n_ts, sz, d), where n_ts=1 tslearn-formatted dataset to be cast to cesium format Returns ------- list of cesium TimeSeries cesium-formatted dataset (cf. `link <http://cesium-ml.org/docs/api/cesium.time_series.html#cesium.time_series.TimeSeries>`_) Examples -------- >>> tslearn_arr = numpy.random.randn(3, 16, 1) >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 3 >>> cesium_ds[0].measurement.shape (16,) >>> tslearn_arr = numpy.random.randn(3, 16, 2) >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 3 >>> cesium_ds[0].measurement.shape (2, 16) >>> tslearn_arr = [[1, 2, 3], [1, 2, 3, 4]] >>> cesium_ds = to_cesium_dataset(tslearn_arr) >>> len(cesium_ds) 2 >>> cesium_ds[0].measurement.shape (3,) Notes ----- Conversion from/to cesium format requires cesium to be installed.

### Goal
Transform a standard 3D `tslearn`-compatible time-series dataset into a list of `cesium` `TimeSeries` objects.

### Parameters
- `X`: A `tslearn`-formatted dataset (array-like of shape `(n_ts, sz, d)`) to be cast to `cesium` format.

### Input
- A 3D `numpy` array of shape `(n_ts, max_sz, d)` representing `n_ts` time series, each with up to `max_sz` time steps and `d` dimensions. It also accepts a list of lists for variable-length time series.
- **Precondition**: The external `cesium` package must be installed in the Python environment.

### Output
Returns `unspecified` — A list of `cesium.time_series.TimeSeries` objects representing the converted dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_cesium_dataset

try:
    import cesium
    
    # 2 time series, 3 time steps, 2 dimensions
    tslearn_arr = np.array([
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]]
    ])
    
    cesium_ds = to_cesium_dataset(tslearn_arr)
    
    assert len(cesium_ds) == 2
    # cesium transposes the measurements to (d, sz)
    assert cesium_ds[0].measurement.shape == (2, 3)
    print(f"Successfully converted {len(cesium_ds)} series to cesium format.")
    
except ImportError:
    print("cesium is not installed; skipping execution.")
```

### LLM Instruction Prompt
- Use `tslearn.utils.to_cesium_dataset(X)` to convert a 3D `(n_ts, max_sz, d)` `tslearn` time-series dataset into a list of `cesium.time_series.TimeSeries` objects.
- Ensure the `cesium` package is installed in the environment before calling this function, as it is a strict dependency for the conversion.
- Be aware that `cesium` transposes the dimensions: a `tslearn` series of shape `(sz, d)` becomes a `cesium` measurement of shape `(d, sz)` (or `(sz,)` if `d=1`).

### Prompt Snippet
```text
When integrating with cesium, convert your 3D tslearn array using `tslearn.utils.to_cesium_dataset(X)`. This requires the `cesium` package to be installed and will return a list of `cesium.time_series.TimeSeries` objects where the measurement arrays are transposed to `(d, sz)`.
```

### Common Failure Modes
- **Missing Dependency**: Raising an `ImportError` or `ModuleNotFoundError` if the `cesium` package is not installed in the Python environment.
- **Invalid Input Shape**: Passing a dataset that has not been properly formatted into a 3D array or a valid list of lists, causing parsing errors during the conversion.

### Fix Code Hint
```python
try:
    import cesium
    from tslearn.utils import to_cesium_dataset
    
    # Ensure X is a properly formatted tslearn dataset before conversion
    cesium_dataset = to_cesium_dataset(X)
except ImportError:
    print("The 'cesium' package is required for this conversion. Please install it.")
```

## API Test: `to_hdf5`

### Signature
```python
def to_hdf5(self, path)
```
_Source: tslearn/tslearn/bases/bases.py:210  (+1 more definition site/overload)_

_Source doc:_ Save model to a HDF5 file. Requires ``h5py`` http://docs.h5py.org/ Parameters ---------- path : str Full file path. File must not already exist. Raises ------ FileExistsError If a file with the same path already exists.

### Goal
Save a `tslearn` estimator's architecture and learned parameters to an HDF5 file on disk for later deserialization.

### Parameters
- `self`: The instantiated `tslearn` model (e.g., a clustering, classification, or regression estimator) to be serialized.
- `path`: A string specifying the full file path where the HDF5 file should be written.

### Input
- The caller must provide a valid string path to a location where the file **does not currently exist**.
- The environment must have the `h5py` package installed.
- The model should typically be fitted before saving, though unfitted models can also be serialized.

### Output
Returns `None` (unspecified). The artifact generated is an HDF5 file at the specified `path` containing the model's state.

### Valid Call Patterns
```python
import os
import tempfile
import numpy as np
from tslearn.clustering import TimeSeriesKMeans

# 1. Prepare a small deterministic dataset and fit a model
X = np.array([[[1.0], [2.0]], [[1.5], [2.5]]])
model = TimeSeriesKMeans(n_clusters=1, max_iter=2, random_state=42)
model.fit(X)

with tempfile.TemporaryDirectory() as tmpdir:
    path = os.path.join(tmpdir, "model.hdf5")
    
    # 2. Call inferred from signature (no verbatim example available)
    model.to_hdf5(path)
    
    # 3. Verify the artifact was created
    assert os.path.exists(path), "HDF5 file was not created."
    assert os.path.getsize(path) > 0, "HDF5 file is empty."
    print("Model saved successfully.")
```

### LLM Instruction Prompt
- Call `to_hdf5(path)` as an instance method on a `tslearn` model object.
- Never pass a path that already exists; `to_hdf5` does not overwrite and will strictly raise a `FileExistsError`.
- Ensure `h5py` is available in the environment when generating code that uses this method.

### Prompt Snippet
```text
When serializing a tslearn model using `to_hdf5`, always verify that the destination file path does not already exist. If overwriting is intended, explicitly remove the existing file prior to calling the method, as `to_hdf5` will raise a FileExistsError instead of overwriting.
```

### Common Failure Modes
- **`FileExistsError`**: Raised immediately if the file at `path` already exists. The method will not overwrite existing files.
- **`ImportError` / `ModuleNotFoundError`**: Raised if the `h5py` library is not installed in the current Python environment.
- **`AttributeError`**: Raised if attempting to call this on a preprocessing object or utility class that does not inherit from the base model serialization classes.

### Fix Code Hint
```python
import os

# Check and remove the file if it already exists to prevent FileExistsError
if os.path.exists(path):
    os.remove(path)

# Save the model
model.to_hdf5(path)
```

## API Test: `to_json`

### Signature
```python
def to_json(self, path)
```
_Source: tslearn/tslearn/bases/bases.py:259_

_Source doc:_ Save model to a JSON file. Parameters ---------- path : str Full file path.

### Goal
Save a `tslearn` machine-learning model or estimator to a JSON file on disk.

### Parameters
- `self`: The instantiated `tslearn` model or estimator object to be serialized.
- `path`: A string representing the full file path where the JSON file will be saved.

### Input
A valid file path string with write permissions in an existing directory. The model (`self`) should typically be fitted before saving to ensure learned attributes (like cluster centers or weights) are serialized, though unfitted models can also be saved to preserve hyperparameters.

### Output
Returns `unspecified` — typically `None`. The operation produces a JSON file on disk containing the model's configuration, hyperparameters, and fitted attributes.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset

# Example inferred from signature (not verified)
X = to_time_series_dataset([[1.0, 2.0], [1.0, 4.0], [1.0, 2.0], [1.0, 4.0]])
model = TimeSeriesKMeans(n_clusters=2, max_iter=2, random_state=42)
model.fit(X)

with tempfile.TemporaryDirectory() as tmpdir:
    filepath = os.path.join(tmpdir, "ts_model.json")
    
    # Call as an instance method on the model
    model.to_json(filepath)
    
    assert os.path.exists(filepath), "JSON file was not created."
    assert os.path.getsize(filepath) > 0, "JSON file is empty."
    print(f"Model successfully serialized to {filepath}")
```

### LLM Instruction Prompt
- When serializing a `tslearn` model, use the `.to_json(path)` instance method directly on the model object.
- Do not attempt to call `to_json` as a standalone function or module-level API.
- Ensure the `path` argument is a string pointing to a valid, writable location where the parent directory already exists.

### Prompt Snippet
```text
To save a trained tslearn estimator, call the `to_json(path)` instance method on the model object. The `path` must be a string representing the full destination file path.
```

### Common Failure Modes
- Calling `to_json(model, path)` as a standalone function instead of an instance method (`model.to_json(path)`).
- Providing a `path` to a directory that does not exist, which will raise a `FileNotFoundError`.
- Passing a non-string object (like a file handle or `Path` object) if the underlying implementation strictly expects a string.

### Fix Code Hint
```python
import os

# Ensure the parent directory exists before saving
save_path = "/path/to/save/model.json"
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Correctly call as an instance method
model.to_json(save_path)
```

## API Test: `to_numpy`

### Signature
```python
def to_numpy(x)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:213  (+1 more definition site/overload)_

### Goal
Converts a backend-specific data structure (such as a PyTorch tensor or a NumPy array) into a standard NumPy array, enabling seamless integration with `scikit-learn` and standard Python evaluation pipelines.

### Parameters
- `x`: The input data structure (e.g., a PyTorch tensor or NumPy array) to be converted back to a standard NumPy array.

### Input
A time-series dataset, array, or scalar tensor, typically originating from a backend operation (such as a PyTorch metric computation like `soft_dtw` with `compute_with_backend=True`). 

### Output
Returns `unspecified` (conceptually a `numpy.ndarray` or Python scalar). Represents the same numerical data as the input `x`, safely detached from any computational graphs and formatted as a standard NumPy array.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Note: Call form inferred from signature and backend context.
# Instantiate the backend (defaults to NumPy if PyTorch is unavailable)
be = instantiate_backend("numpy")

# Create a dummy array representing a backend-specific tensor
x_backend = np.array([[1.0, 2.0], [3.0, 4.0]])

# Convert back to a standard NumPy array
x_np = be.to_numpy(x_backend)

assert isinstance(x_np, np.ndarray), "Output must be a NumPy array"
print(f"Converted array:\n{x_np}")
```

### LLM Instruction Prompt
- Use `to_numpy` via the instantiated backend object (e.g., `be.to_numpy(x)`) to safely convert backend-specific tensors (like PyTorch tensors) back to NumPy arrays.
- This is critical when extracting the results of automatic differentiation metrics (like `soft_dtw` gradients) to pass them into standard `scikit-learn` estimators or NumPy-based preprocessing steps.

### Prompt Snippet
```text
When extracting results from a PyTorch-backend metric in `tslearn`, use the backend's `to_numpy(x)` method to safely convert the tensor back to a NumPy array. This ensures compatibility with `scikit-learn` pipelines that strictly expect 3D `numpy.ndarray` inputs.
```

### Common Failure Modes
- **Gradient Graph Detachment Errors:** If using the PyTorch backend manually without the helper, attempting to convert a tensor with `requires_grad=True` directly to NumPy raises an error. The `to_numpy` backend helper typically handles detaching, but users should be aware of tensor states.
- **Unrecognized Backend Types:** Passing a custom object or a tensor from an uninstantiated/unsupported backend (e.g., passing a TensorFlow tensor to the PyTorch backend's `to_numpy`) will fail.
- **Missing Backend Instantiation:** Attempting to call `to_numpy` as a standalone function without first dynamically selecting the backend via `instantiate_backend`.

### Fix Code Hint
```python
# BAD: Calling numpy() directly on a PyTorch tensor that might require gradients
# x_np = my_tensor.numpy() 

# GOOD: Use the tslearn backend helper to safely convert
from tslearn.backend import instantiate_backend

be = instantiate_backend("pytorch")
# ... metric computation ...
x_np = be.to_numpy(my_tensor)
```

## API Test: `to_pickle`

### Signature
```python
def to_pickle(self, path)
```
_Source: tslearn/tslearn/bases/bases.py:307_

_Source doc:_ Save model to a pickle file. Parameters ---------- path : str Full file path.

### Goal
Serialize and save a `tslearn` time-series estimator or model to a file on disk using Python's pickle format.

### Parameters
- `self`: The `tslearn` model or estimator instance (e.g., a clustering, classification, or regression model) to be saved.
- `path`: A string representing the full file path where the pickled model will be written.

### Input
- **Preconditions:** The caller must have an instantiated `tslearn` model (fitted or unfitted) that inherits from the base classes providing this method. The provided `path` must be a valid, writable file path in the local filesystem.

### Output
Returns `unspecified` — typically `None`. The primary result is a side effect: a serialized `.pkl` file containing the model's state is written to the specified `path`.

### Valid Call Patterns
```python
import os
import tempfile
from tslearn.clustering import TimeSeriesKMeans

# Example inferred from the signature (not verified by existing tests)
model = TimeSeriesKMeans(n_clusters=2, random_state=42)

with tempfile.TemporaryDirectory() as tmpdir:
    filepath = os.path.join(tmpdir, "ts_model.pkl")
    
    # Call as an instance method
    model.to_pickle(filepath)
    
    assert os.path.exists(filepath)
    print(f"Model successfully saved to {filepath}")
```

### LLM Instruction Prompt
- Call `to_pickle` strictly as an instance method on a `tslearn` model object (e.g., `model.to_pickle("path/to/file.pkl")`), never as a standalone function.
- Ensure the `path` argument is a string representing a valid, writable file path.

### Prompt Snippet
```text
Save the trained `tslearn` model to disk using its built-in `to_pickle` method. Provide the full file path as a string.
```

### Common Failure Modes
- **Calling as a standalone function:** Attempting to call `tslearn.bases.to_pickle(model, path)` instead of `model.to_pickle(path)` will fail or cause import errors.
- **Invalid or read-only paths:** Providing a directory path instead of a file path, or a path where the user lacks write permissions, will raise an `OSError` or `PermissionError`.
- **Missing parent directories:** If the parent directories in the `path` do not exist, the underlying file open operation will fail with a `FileNotFoundError`.

### Fix Code Hint
```python
# WRONG: Calling as a standalone function or missing parent directories
# to_pickle(model, "missing_dir/model.pkl")

# RIGHT: Call as an instance method and ensure the directory exists
import os
os.makedirs("saved_models", exist_ok=True)
model.to_pickle("saved_models/my_model.pkl")
```

## API Test: `to_pyflux_dataset`

### Signature
```python
def to_pyflux_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:409_

_Source doc:_ Transform a tslearn-compatible dataset into a pyflux dataset. Parameters ---------- X: array, shape = (n_ts, sz, d), where n_ts=1 tslearn-formatted dataset to be cast to pyflux format Returns ------- Pandas data-frame pyflux-formatted dataset (cf. `link <https://pyflux.readthedocs.io/en/latest/getting_started.html>`_) Examples -------- >>> tslearn_arr = numpy.random.randn(1, 16, 1) >>> pyflux_df = to_pyflux_dataset(tslearn_arr) >>> pyflux_df.shape (16, 1) >>> pyflux_df.columns[0] 'dim_0' >>> tslearn_arr = numpy.random.randn(1, 16, 2) >>> pyflux_df = to_pyflux_dataset(tslearn_arr) >>> pyflux_df.shape (16, 2) >>> pyflux_df.columns[1] 'dim_1' >>> tslearn_arr = numpy.random.randn(10, 16, 1) >>> to_pyflux_dataset(tslearn_arr)  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: Array should be made of a single time series (10 here) Notes ----- Conversion from/to pyflux format requires pandas to be installed.

### Goal
Converts a single tslearn-formatted time series into a pandas DataFrame formatted for compatibility with the `pyflux` library.

### Parameters
- `X`: A 3D numpy array of shape `(n_ts, sz, d)` representing the tslearn-formatted dataset to be cast. Crucially, `n_ts` must be exactly 1.

### Input
The caller must provide a strict 3D numpy array formatted as `(n_ts, max_sz, d)`. The dataset must contain exactly one time series (`n_ts=1`). The environment must have `pandas` installed, as the conversion relies on it to construct the output DataFrame.

### Output
Returns `unspecified` — A pandas DataFrame of shape `(sz, d)` representing the pyflux-formatted dataset. The columns of the DataFrame are automatically named `'dim_0'`, `'dim_1'`, ..., up to `'dim_{d-1}'`.

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

# Create a single time series of length 10 with 2 dimensions
rng = np.random.RandomState(0)
tslearn_dataset = rng.randn(1, 10, 2)

# Convert to pyflux format
pyflux_df = tslearn.utils.to_pyflux_dataset(tslearn_dataset)

# Verify the output properties
assert pyflux_df.shape == (10, 2)
assert pyflux_df.columns[0] == 'dim_0'
assert pyflux_df.columns[1] == 'dim_1'
print(f"Successfully converted to pyflux DataFrame with shape {pyflux_df.shape}")
```

### LLM Instruction Prompt
- When calling `tslearn.utils.to_pyflux_dataset`, ensure the input `X` is a 3D array containing exactly one time series (shape `(1, sz, d)`). Do not pass datasets with multiple time series (`n_ts > 1`). If you have a larger dataset, slice it to extract a single time series while preserving the 3D shape (e.g., `X[0:1]`). Ensure `pandas` is available in the environment.

### Prompt Snippet
```text
import tslearn.utils
# X must have shape (1, sz, d)
pyflux_df = tslearn.utils.to_pyflux_dataset(X)
```

### Common Failure Modes
- **Multiple Time Series:** Passing an array where `n_ts > 1` (e.g., shape `(10, 16, 1)`) will raise a `ValueError: Array should be made of a single time series (10 here)`.
- **Incorrect Dimensionality:** Passing a 1D or 2D array instead of the strict 3D `(n_ts, sz, d)` tslearn format will cause unexpected behavior or errors.
- **Missing Dependency:** Calling this function in an environment without `pandas` installed will fail, as it explicitly returns a pandas DataFrame.

### Fix Code Hint
```python
# If X has multiple time series (e.g., shape (10, 16, 1)), 
# slice it to select just one before converting, keeping the 3D shape:
single_ts = X[0:1, :, :]  # Shape becomes (1, 16, 1)
pyflux_df = tslearn.utils.to_pyflux_dataset(single_ts)
```

## API Test: `to_pyts_dataset`

### Signature
```python
def to_pyts_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:64_

_Source doc:_ Transform a tslearn-compatible dataset into a pyts dataset. Parameters ---------- X: array, shape = (n_ts, sz, d) tslearn-formatted dataset to be cast to pyts format Returns ------- array, shape=(n_ts, sz) if d=1, (n_ts, d, sz) otherwise pyts-formatted dataset Examples -------- >>> tslearn_arr = numpy.random.randn(10, 16, 1) >>> pyts_arr = to_pyts_dataset(tslearn_arr) >>> pyts_arr.shape (10, 16) >>> tslearn_arr = numpy.random.randn(10, 16, 2) >>> pyts_arr = to_pyts_dataset(tslearn_arr) >>> pyts_arr.shape (10, 2, 16) >>> tslearn_arr = [numpy.random.randn(16, 1), numpy.random.randn(10, 1)] >>> to_pyts_dataset(tslearn_arr)  # doctest: +IGNORE_EXCEPTION_DETAIL Traceback (most recent call last): ... ValueError: All the time series in the array should be of equal lengths

### Goal
Convert a standard 3D `tslearn` time-series dataset into a format compatible with the `pyts` library.

### Parameters
- `X`: A `tslearn`-formatted time-series dataset to be cast to the `pyts` format.

### Input
A 3D NumPy array of shape `(n_ts, sz, d)` representing `n_ts` time series, each of length `sz` with `d` dimensions. Crucially, all time series in the array must be of equal length; variable-length time series are not supported by this conversion and will raise an error.

### Output
Returns `unspecified` — A NumPy array representing the `pyts`-formatted dataset. The output shape is `(n_ts, sz)` if the input is univariate (`d=1`), or `(n_ts, d, sz)` if the input is multivariate (`d > 1`).

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

# 1. Multivariate conversion (d > 1)
n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
tslearn_dataset_multi = rng.randn(n, sz, d)

pyts_dataset_multi = tslearn.utils.to_pyts_dataset(tslearn_dataset_multi)
assert pyts_dataset_multi.shape == (15, 3, 10)
print("Multivariate pyts shape:", pyts_dataset_multi.shape)

# 2. Univariate conversion (d = 1)
tslearn_dataset_uni = rng.randn(10, 16, 1)
pyts_dataset_uni = tslearn.utils.to_pyts_dataset(tslearn_dataset_uni)
assert pyts_dataset_uni.shape == (10, 16)
print("Univariate pyts shape:", pyts_dataset_uni.shape)
```

### LLM Instruction Prompt
When converting `tslearn` datasets to `pyts` format using `to_pyts_dataset`, ensure the input is a strict 3D array `(n_ts, sz, d)` and that all time series have the exact same length. Do not pass variable-length time series (e.g., lists of arrays of different lengths), as this will trigger a `ValueError`. Be aware that the output shape changes based on dimensionality: `(n_ts, sz)` for univariate and `(n_ts, d, sz)` for multivariate.

### Prompt Snippet
```text
Use `tslearn.utils.to_pyts_dataset(X)` to convert a 3D tslearn array `(n_ts, sz, d)` to pyts format. The output will be `(n_ts, sz)` if `d=1`, or `(n_ts, d, sz)` otherwise. Ensure all series in `X` are of equal length.
```

### Common Failure Modes
- **Variable-length time series:** Passing a list of arrays with different lengths (e.g., `[np.random.randn(16, 1), np.random.randn(10, 1)]`) raises `ValueError: All the time series in the array should be of equal lengths`.
- **Incorrect input dimensions:** Passing a 2D array instead of the strict 3D `(n_ts, sz, d)` format expected by `tslearn` utilities.

### Fix Code Hint
```python
import numpy as np
from tslearn.utils import to_time_series_dataset, to_pyts_dataset

# Ensure input is a 3D array with equal-length series
raw_data = [np.random.randn(10, 1), np.random.randn(10, 1)] # Must be equal lengths
tslearn_arr = to_time_series_dataset(raw_data) # Shape: (2, 10, 1)

# Convert to pyts format
pyts_arr = to_pyts_dataset(tslearn_arr) # Shape: (2, 10)
```

## API Test: `to_seglearn_dataset`

### Signature
```python
def to_seglearn_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:141_

_Source doc:_ Transform a tslearn-compatible dataset into a seglearn dataset. Parameters ---------- X: array, shape = (n_ts, sz, d) tslearn-formatted dataset to be cast to seglearn format Returns ------- array of arrays, shape=(n_ts, ) seglearn-formatted dataset. i-th sub-array in the list has shape (sz_i, d) Examples -------- >>> tslearn_arr = numpy.random.randn(10, 16, 1) >>> seglearn_arr = to_seglearn_dataset(tslearn_arr) >>> seglearn_arr.shape (10, 16, 1) >>> tslearn_arr = numpy.random.randn(10, 16, 2) >>> seglearn_arr = to_seglearn_dataset(tslearn_arr) >>> seglearn_arr.shape (10, 16, 2) >>> tslearn_arr = [numpy.random.randn(16, 2), numpy.random.randn(10, 2)] >>> seglearn_arr = to_seglearn_dataset(tslearn_arr) >>> seglearn_arr.shape (2,) >>> seglearn_arr[0].shape (16, 2) >>> seglearn_arr[1].shape (10, 2)

### Goal
Transform a standard 3D `tslearn`-formatted time-series dataset (or a list of variable-length 2D time series) into a `seglearn`-compatible format.

### Parameters
- `X`: A `tslearn`-formatted dataset. Typically a 3D NumPy array of shape `(n_ts, sz, d)` for uniform-length time series, or a list of 2D arrays of shape `(sz_i, d)` for variable-length time series.

### Input
The caller must provide a valid `tslearn` dataset. If the data is raw or not yet properly shaped, it should first be converted using `tslearn.utils.to_time_series_dataset` to ensure the strict `(n_ts, max_sz, d)` 3D structure or the equivalent variable-length list of 2D arrays.

### Output
Returns `unspecified` — A `seglearn`-formatted dataset. For variable-length inputs, this is a 1D NumPy object array of length `n_ts`, where the `i`-th element is a 2D array of shape `(sz_i, d)`. For uniform-length 3D array inputs, it returns a 3D NumPy array of shape `(n_ts, sz, d)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_seglearn_dataset

# 1. Uniform-length time series
n_ts, sz, d = 15, 10, 3
tslearn_dataset = np.zeros((n_ts, sz, d))
seglearn_dataset = to_seglearn_dataset(tslearn_dataset)

assert seglearn_dataset.shape == (15, 10, 3)
print(f"Uniform seglearn shape: {seglearn_dataset.shape}")

# 2. Variable-length time series
tslearn_var_dataset = [np.ones((16, 2)), np.ones((10, 2))]
seglearn_var_dataset = to_seglearn_dataset(tslearn_var_dataset)

assert seglearn_var_dataset.shape == (2,)
assert seglearn_var_dataset[0].shape == (16, 2)
print(f"Variable seglearn shape: {seglearn_var_dataset.shape}")
```

### LLM Instruction Prompt
- When interoperating between `tslearn` and `seglearn`, use `tslearn.utils.to_seglearn_dataset` to cast the dataset. Ensure the input `X` is already in the strict `tslearn` format (a 3D array `(n_ts, sz, d)` or a list of 2D arrays `(sz_i, d)`). Do not pass raw 1D or 2D arrays directly without reshaping them first.

### Prompt Snippet
```text
Convert the `tslearn` formatted 3D array `X_tslearn` into a `seglearn` compatible dataset using `tslearn.utils.to_seglearn_dataset`.
```

### Common Failure Modes
- Passing a 1D array `(sz,)` or a 2D array `(n_ts, sz)` instead of the required 3D `tslearn` format `(n_ts, sz, d)`.
- Passing a list of 1D arrays for variable-length data instead of a list of 2D arrays `(sz_i, d)`.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset, to_seglearn_dataset

# If X is raw 2D data (n_ts, sz), first convert it to the strict 3D tslearn format
X_tslearn = to_time_series_dataset(X_raw)
X_seglearn = to_seglearn_dataset(X_tslearn)
```

## API Test: `to_sklearn_dataset`

### Signature
```python
def to_sklearn_dataset(dataset, dtype=float, return_dim=False)
```
_Source: tslearn/tslearn/utils/cast.py:21_

_Source doc:_ Transforms a time series dataset so that it fits the format used in ``sklearn`` estimators. Parameters ---------- dataset : array-like The dataset of time series to be transformed. dtype : data type (default: float64) Data type for the returned dataset. return_dim : boolean  (optional, default: False) Whether the dimensionality (third dimension should be returned together with the transformed dataset). Returns ------- numpy.ndarray of shape (n_ts, sz * d) The transformed dataset of time series. int (optional, if return_dim=True) The dimensionality of the original tslearn dataset (third dimension) Examples -------- >>> to_sklearn_dataset([[1, 2]], return_dim=True) (array([[1., 2.]]), 1) >>> to_sklearn_dataset([[1, 2], [1, 4, 3]]) array([[ 1.,  2., nan], [ 1.,  4.,  3.]]) See Also -------- to_time_series_dataset : Transforms a time series dataset to ``tslearn`` format.

### Goal
Transforms a time-series dataset into a flattened 2D array format compatible with standard `scikit-learn` estimators.

### Parameters
- `dataset`: The array-like dataset of time series to be transformed (typically a 3D `tslearn` array or a list of variable-length sequences).
- `dtype`, default `float`: The desired data type for the returned `numpy.ndarray`.
- `return_dim`, default `False`: A boolean indicating whether the original dimensionality (the third dimension `d` of the `tslearn` format) should be returned alongside the transformed dataset.

### Input
An array-like collection of time series. This can be a strict 3D `numpy` array of shape `(n_ts, max_sz, d)` or a raw list of variable-length time series. 

### Output
Returns `unspecified` — A 2D `numpy.ndarray` of shape `(n_ts, max_sz * d)` representing the flattened dataset. If `return_dim=True`, it returns a tuple `(transformed_dataset, original_dim)` where `original_dim` is an `int` representing the third dimension of the original dataset.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_sklearn_dataset

# 1. Convert a list of variable-length time series to a 2D sklearn-compatible array
dataset = [[1.0, 2.0], [1.0, 4.0, 3.0]]
X_2d = to_sklearn_dataset(dataset)

assert X_2d.shape == (2, 3), f"Expected shape (2, 3), got {X_2d.shape}"
assert np.isnan(X_2d[0, 2]), "Expected NaN padding for the shorter time series"

# 2. Convert and retrieve the original dimensionality
X_2d_dim, dim = to_sklearn_dataset([[1, 2]], return_dim=True)

assert X_2d_dim.shape == (1, 2)
assert dim == 1
print("to_sklearn_dataset correctly flattened and padded the dataset.")
```

### LLM Instruction Prompt
- Use `to_sklearn_dataset` to flatten `tslearn`'s 3D time-series arrays `(n_ts, max_sz, d)` into 2D arrays `(n_ts, max_sz * d)` for compatibility with standard `scikit-learn` estimators (e.g., `RandomForestClassifier`, `PCA`).
- If `return_dim=True`, you MUST unpack the returned tuple `(transformed_dataset, original_dim)`.
- Be aware that variable-length time series will be padded with `nan` values in the resulting 2D array. Standard `scikit-learn` estimators may fail if they do not support missing values.

### Prompt Snippet
```text
Use `tslearn.utils.to_sklearn_dataset` to convert 3D time-series arrays into 2D arrays for standard scikit-learn estimators. Set `return_dim=True` if you need to keep track of the original feature dimensionality. Handle `nan` values if your dataset has variable-length series.
```

### Common Failure Modes
- **Tuple Unpacking Error:** Forgetting to unpack the tuple when `return_dim=True`, leading to a tuple being passed to a `scikit-learn` estimator's `.fit()` method instead of a `numpy` array.
- **NaN Value Rejection:** Passing the resulting 2D array directly to a `scikit-learn` estimator that does not support missing values, causing a `ValueError` because shorter time series were padded with `nan`.

### Fix Code Hint
```python
from tslearn.utils import to_sklearn_dataset
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# If return_dim=True, unpack the tuple
X_2d, dim = to_sklearn_dataset(X_3d, return_dim=True)

# If the original data had variable lengths, X_2d will contain NaNs.
# Ensure the downstream estimator can handle NaNs, or impute them first:
imputer = SimpleImputer(strategy='constant', fill_value=0)
X_2d_imputed = imputer.fit_transform(X_2d)

clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_2d_imputed, y)
```

## API Test: `to_sktime_dataset`

### Signature
```python
def to_sktime_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:288_

_Source doc:_ Transform a tslearn-compatible dataset into a sktime dataset. Parameters ---------- X: array, shape = (n_ts, sz, d) tslearn-formatted dataset to be cast to sktime format Returns ------- Pandas data-frame sktime-formatted dataset Examples -------- >>> tslearn_arr = numpy.random.randn(10, 16, 1) >>> sktime_arr = to_sktime_dataset(tslearn_arr) >>> sktime_arr.shape (10, 1) >>> sktime_arr["dim_0"][0].shape (16,) >>> tslearn_arr = numpy.random.randn(10, 16, 2) >>> sktime_arr = to_sktime_dataset(tslearn_arr) >>> sktime_arr.shape (10, 2) >>> sktime_arr["dim_1"][0].shape (16,) Notes ----- Conversion from/to sktime format requires pandas to be installed.

### Goal
Transform a 3D `tslearn`-formatted time-series dataset into a `sktime`-compatible pandas DataFrame.

### Parameters
- `X`: A 3D numpy array of shape `(n_ts, sz, d)` representing the `tslearn`-formatted dataset to be cast.

### Input
The caller must provide a strictly 3D numpy array representing time-series data, where the dimensions correspond to `(number of time series, maximum sequence length, number of dimensions)`. The environment must have `pandas` installed, as it is required for the conversion to the `sktime` format.

### Output
Returns `unspecified` — A `sktime`-formatted pandas DataFrame of shape `(n_ts, d)`. Each cell in the DataFrame contains a 1D structure (like a pandas Series or numpy array) of length `sz` representing the time-series measurements for that specific dimension. The columns are typically named `"dim_0"`, `"dim_1"`, etc.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_sktime_dataset

# 1. Create a deterministic tslearn-formatted dataset (n_ts=2, sz=3, d=2)
tslearn_dataset = np.array([
    [[1.0, 0.1], [2.0, 0.2], [3.0, 0.3]],
    [[4.0, 0.4], [5.0, 0.5], [6.0, 0.6]]
])

# 2. Convert to sktime format
sktime_df = to_sktime_dataset(tslearn_dataset)

# 3. Verify the output properties
assert sktime_df.shape == (2, 2), f"Expected shape (2, 2), got {sktime_df.shape}"
assert sktime_df["dim_0"][0].shape == (3,), "Expected inner series length of 3"
assert sktime_df["dim_1"][1].iloc[2] == 0.6, "Expected specific value in dim_1"
print(f"Successfully converted to sktime DataFrame with shape {sktime_df.shape}")
```

### LLM Instruction Prompt
- When calling `to_sktime_dataset`, ensure the input `X` is strictly a 3D numpy array of shape `(n_ts, sz, d)`. Do not pass 1D lists, 2D arrays, or raw data directly; if the data is not already in the 3D format, preprocess it using `tslearn.utils.to_time_series_dataset` first. Note that this function requires `pandas` to be installed in the execution environment.

### Prompt Snippet
```text
`tslearn.utils.to_sktime_dataset(X)` converts a 3D `(n_ts, sz, d)` numpy array into a `sktime` pandas DataFrame of shape `(n_ts, d)`. Requires `pandas`.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D `(n_ts, sz, d)` array, which will cause shape mismatch errors during DataFrame construction.
- Calling the function in an environment where `pandas` is not installed, resulting in an `ImportError`.
- Passing a dataset with variable-length time series that has not been properly padded with `nan` values into a uniform 3D array.

### Fix Code Hint
```python
# If X_raw is a list of lists or a 2D array, convert it to 3D first
from tslearn.utils import to_time_series_dataset, to_sktime_dataset

# Convert raw data to the required (n_ts, sz, d) format
X_3d = to_time_series_dataset(X_raw)

# Now safely cast to sktime format
sktime_df = to_sktime_dataset(X_3d)
```

## API Test: `to_stumpy_dataset`

### Signature
```python
def to_stumpy_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:214_

_Source doc:_ Transform a tslearn-compatible dataset into a stumpy dataset. Parameters ---------- X: array, shape = (n_ts, sz, d) tslearn-formatted dataset to be cast to stumpy format Returns ------- list of arrays of shape=(d, sz_i) if d > 1 or (sz_i, ) otherwise stumpy-formatted dataset. Examples -------- >>> tslearn_arr = numpy.random.randn(10, 16, 1) >>> stumpy_arr = to_stumpy_dataset(tslearn_arr) >>> len(stumpy_arr) 10 >>> stumpy_arr[0].shape (16,) >>> tslearn_arr = numpy.random.randn(10, 16, 2) >>> stumpy_arr = to_stumpy_dataset(tslearn_arr) >>> len(stumpy_arr) 10 >>> stumpy_arr[0].shape (2, 16)

### Goal
Transform a strict 3D `tslearn`-formatted time-series dataset into a `stumpy`-compatible format (a list of 1D or 2D arrays).

### Parameters
- `X`: A 3D `numpy` array of shape `(n_ts, sz, d)` representing the `tslearn`-formatted time-series dataset to be cast.

### Input
The input `X` must be a strictly formatted 3D `numpy` array with dimensions `(n_ts, max_sz, d)` (number of time series, maximum sequence length, and number of dimensions). If the raw data is not in this format, it must first be converted using `tslearn.utils.to_time_series_dataset`.

### Output
Returns `unspecified` — A list of `numpy` arrays representing the `stumpy`-formatted dataset. The shape of each array in the list depends on the dimensionality `d`: if `d > 1` (multivariate), the arrays have shape `(d, sz_i)`; if `d == 1` (univariate), the arrays are flattened to shape `(sz_i,)`.

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

# 1. Multivariate example (d > 1)
n, sz, d = 15, 10, 3
rng = np.random.RandomState(0)
tslearn_dataset_multi = rng.randn(n, sz, d)

stumpy_dataset_multi = tslearn.utils.to_stumpy_dataset(tslearn_dataset_multi)

assert len(stumpy_dataset_multi) == 15
# Note the transposition: (sz, d) becomes (d, sz) for stumpy
assert stumpy_dataset_multi[0].shape == (3, 10) 

# 2. Univariate example (d == 1)
tslearn_dataset_uni = rng.randn(10, 16, 1)
stumpy_dataset_uni = tslearn.utils.to_stumpy_dataset(tslearn_dataset_uni)

assert len(stumpy_dataset_uni) == 10
# Note the flattening: (sz, 1) becomes (sz,) for stumpy
assert stumpy_dataset_uni[0].shape == (16,)
```

### LLM Instruction Prompt
- When calling `to_stumpy_dataset`, ensure the input `X` is a strict 3D `numpy` array of shape `(n_ts, sz, d)`. Be aware that the output format depends on the dimensionality `d`: it returns a list of 1D arrays `(sz_i,)` if `d=1`, and a list of 2D arrays transposed to `(d, sz_i)` if `d>1`.

### Prompt Snippet
```text
Use `tslearn.utils.to_stumpy_dataset(X)` to convert a 3D tslearn array `(n_ts, sz, d)` into a stumpy-compatible list of arrays. The output arrays will be transposed to `(d, sz_i)` for multivariate data, or flattened to `(sz_i,)` for univariate data.
```

### Common Failure Modes
- Passing a 1D or 2D array instead of the required 3D `(n_ts, sz, d)` array.
- Assuming the output arrays retain the `(sz, d)` shape (they are transposed to `(d, sz)` or flattened to `(sz,)`).
- Failing to preprocess raw lists of varying lengths into a padded 3D array using `to_time_series_dataset` before calling this function.

### Fix Code Hint
```python
# Ensure input is a 3D array before converting
X_3d = tslearn.utils.to_time_series_dataset(X_raw)
stumpy_data = tslearn.utils.to_stumpy_dataset(X_3d)
```

## API Test: `to_time_series`

### Signature
```python
def to_time_series(ts, remove_nans=False, be=None, dtype=float)
```
_Source: tslearn/tslearn/utils/utils.py:154_

_Source doc:_ Transforms a time series so that it fits the format used in ``tslearn`` models. Parameters ---------- ts : array-like, shape=(sz, d) or (sz,) The time series to be transformed. If shape is (sz,), the time series is assumed to be univariate. remove_nans : bool (default: False) Whether trailing NaNs at the end of the time series should be removed or not be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. dtype : data type (default: float) Data type for the returned time series, depending on the backend. Returns ------- ts_out : array-like, shape=(sz, d) The transformed time series. This is always guaranteed to be a new time series and never just a view into the old one. Examples -------- >>> to_time_series([1, 2]) array([[1.], [2.]]) >>> to_time_series([1, 2, numpy.nan]) array([[ 1.], [ 2.], [nan]]) >>> to_time_series([1, 2, numpy.nan], remove_nans=True) array([[1.], [2.]]) See Also -------- to_time_series_dataset : Transforms a dataset of time series

### Goal
Transforms a single raw array-like time series into the strict 2D `(sz, d)` format required by `tslearn` models, ensuring it is a new copy rather than a view.

### Parameters
- `ts`: array-like, shape `(sz, d)` or `(sz,)`. The raw time series to be transformed. If the shape is 1D `(sz,)`, it is automatically assumed to be univariate and expanded to `(sz, 1)`.
- `remove_nans`, default `False`: bool. Whether trailing `NaN` values at the end of the time series should be stripped out.
- `be`, default `None`: Backend object, string (`"numpy"`, `"pytorch"`), or `None`. Determines the backend used for the output array. If `None`, the backend is automatically determined by the input array's type.
- `dtype`, default `float`: data type. The desired data type for the returned time series array or tensor.

### Input
A single time series represented as a Python list, NumPy array, or PyTorch tensor. It can be 1D (univariate) or 2D (multivariate). Do not pass a full dataset (multiple time series) to this function.

### Output
Returns `unspecified` — A 2D array or tensor of shape `(sz, d)` representing the formatted time series. It is guaranteed to be a newly allocated object, never a view of the original input.

### Valid Call Patterns
```python
import numpy as np
from tslearn.utils import to_time_series

# 1. Basic univariate conversion with trailing NaN removal
raw_ts = [1.5, 2.5, np.nan]
ts_formatted = to_time_series(raw_ts, remove_nans=True)

assert ts_formatted.shape == (2, 1)
assert np.allclose(ts_formatted, [[1.5], [2.5]])
print(f"Formatted TS shape: {ts_formatted.shape}")

# 2. Specifying a backend explicitly
ts_pytorch = to_time_series([1, 2, 3], be="pytorch", dtype=float)
assert ts_pytorch.shape == (3, 1)
print(f"PyTorch TS type: {type(ts_pytorch)}")
```

### LLM Instruction Prompt
- Use `to_time_series` to format a *single* time series into a 2D `(sz, d)` array.
- Do NOT use this function for a dataset of multiple time series; use `to_time_series_dataset` instead to get the required 3D `(n_ts, sz, d)` array for estimators.
- Set `remove_nans=True` if you need to strip trailing NaNs (often left over from variable-length series padding).
- The output is guaranteed to be a new copy, so mutating the result will not affect the input.

### Prompt Snippet
```text
When formatting a single time series for tslearn metrics or utilities, use `tslearn.utils.to_time_series(ts)`. It converts 1D lists/arrays into the required 2D `(sz, d)` shape. If you have a dataset of multiple time series, use `to_time_series_dataset` instead to get a 3D array.
```

### Common Failure Modes
- **Passing a dataset instead of a single series:** Passing a list of lists of varying lengths (a dataset) to `to_time_series` will result in a jagged array error or incorrect shape. Use `to_time_series_dataset` for datasets.
- **Expecting a 3D array:** `to_time_series` returns a 2D array `(sz, d)`. Most `tslearn` estimators (like `TimeSeriesKMeans`) require 3D arrays `(n_ts, sz, d)`.
- **Assuming the output is a view:** The function always allocates a new array. Modifying the output will not update the original input array.

### Fix Code Hint
```python
# BAD: Using to_time_series for a dataset
# X = to_time_series([[1, 2], [1, 2, 3]]) 

# GOOD: Use to_time_series_dataset for multiple series
from tslearn.utils import to_time_series_dataset
X = to_time_series_dataset([[1, 2], [1, 2, 3]])

# GOOD: Use to_time_series for a single series
from tslearn.utils import to_time_series
single_ts = to_time_series([1, 2, 3]) # Shape becomes (3, 1)
```

## API Test: `to_time_series_dataset`

### Signature
```python
def to_time_series_dataset(dataset, dtype=float, be=None)
```
_Source: tslearn/tslearn/utils/utils.py:215_

_Source doc:_ Transforms a time series dataset so that it fits the format used in ``tslearn`` models. Parameters ---------- dataset : array-like, shape=(n_ts, sz, d) or (n_ts, sz) or (sz,) The dataset of time series to be transformed. A single time series will be automatically wrapped into a dataset with a single entry. dtype : data type (default: float) Data type for the returned dataset, depending on the backend. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- dataset_out : array-like, shape=(n_ts, sz, d) The transformed dataset of time series. Examples -------- >>> to_time_series_dataset([[1, 2]]) array([[[1.], [2.]]]) >>> to_time_series_dataset([1, 2]) array([[[1.], [2.]]]) >>> to_time_series_dataset([[1, 2], [1, 4, 3]]) array([[[ 1.], [ 2.], [nan]], <BLANKLINE> [[ 1.], [ 4.], [ 3.]]]) >>> to_time_series_dataset([]).shape (0, 0, 0) See Also -------- to_time_series : Transforms a single time series

### Goal
Transforms raw lists or arrays of time-series data into the strict 3D array structure `(n_ts, max_sz, d)` required by all `tslearn` estimators, automatically padding variable-length series with `nan`.

### Parameters
- `dataset`: The raw dataset of time series to be transformed. Can be array-like with shape `(n_ts, sz, d)`, `(n_ts, sz)`, or `(sz,)`. A single time series is automatically wrapped into a dataset with a single entry.
- `dtype`, default `float`: The target data type for the returned dataset, depending on the backend.
- `be`, default `None`: The backend to use. Accepts a Backend object, `"numpy"`, `"pytorch"`, or `None`. If `None`, the backend is automatically determined by the input arrays.

### Input
Raw lists, lists of lists, 1D/2D NumPy arrays, or PyTorch tensors representing time-series data. The input can contain variable-length time series (e.g., a list of lists of different lengths).

### Output
Returns `unspecified` — A 3D array-like object (NumPy array or PyTorch tensor, depending on the backend) with shape `(n_ts, max_sz, d)`. Shorter time series are padded with `nan` values at the end to match the maximum length (`max_sz`).

### Valid Call Patterns
```python
from tslearn.utils import to_time_series_dataset
import numpy as np

# Format a list of variable-length time series
my_first_time_series = [1, 3, 4, 2]
my_second_time_series = [1, 2, 4, 2]
my_third_time_series = [1, 2, 4, 2, 2]

X = to_time_series_dataset([
    my_first_time_series,
    my_second_time_series,
    my_third_time_series
])

# Verify the strict (n_ts, max_sz, d) 3D shape
assert X.shape == (3, 5, 1), f"Expected shape (3, 5, 1), got {X.shape}"

# Verify that shorter series are padded with nan
assert np.isnan(X[0, 4, 0]), "Expected nan padding for shorter series"

print(f"Successfully formatted dataset to shape {X.shape} with nan padding.")
```

### LLM Instruction Prompt
- Always use `tslearn.utils.to_time_series_dataset` to format raw lists or 1D/2D arrays into the strict `(n_ts, max_sz, d)` 3D format required by `tslearn` estimators before preprocessing or training.
- Do not manually pad variable-length time series; pass them as a list of lists and let `to_time_series_dataset` handle the `nan` padding automatically.
- Remember that even univariate time series will be given a third dimension `d=1`.

### Prompt Snippet
```text
`tslearn` strictly expects time-series datasets to be formatted as 3D arrays: `(n_ts, max_sz, d)`. Use `tslearn.utils.to_time_series_dataset(raw_data)` to automatically convert lists or 2D arrays into this format and pad variable-length series with `nan`.
```

### Common Failure Modes
- **Shape Mismatch in Downstream Tasks:** Forgetting that `to_time_series_dataset` adds a third dimension `d` (features) even for univariate data, resulting in shape `(n_ts, max_sz, 1)`. Standard `scikit-learn` estimators expecting 2D arrays will fail unless the data is reshaped, but `tslearn` estimators require this 3D shape.
- **Manual Padding Errors:** Attempting to manually pad variable-length sequences with zeros before passing them to `tslearn` estimators. `tslearn` expects `nan` for padding, which `to_time_series_dataset` handles natively.

### Fix Code Hint
```python
# BAD: Passing a 2D array directly to a tslearn estimator
# model.fit([[1, 2, 3], [4, 5, 6]])

# GOOD: Always wrap raw data with to_time_series_dataset first
from tslearn.utils import to_time_series_dataset
X_train = to_time_series_dataset([[1, 2, 3], [4, 5, 6]])
# X_train.shape is now (2, 3, 1)
model.fit(X_train)
```

## API Test: `to_tsfresh_dataset`

### Signature
```python
def to_tsfresh_dataset(X)
```
_Source: tslearn/tslearn/utils/cast.py:527_

_Source doc:_ Transform a tslearn-compatible dataset into a tsfresh dataset. Parameters ---------- X: array, shape = (n_ts, sz, d) tslearn-formatted dataset to be cast to tsfresh format Returns ------- Pandas data-frame tsfresh-formatted dataset ("flat" data frame, as described `there <https://tsfresh.readthedocs.io/en/latest/text/data_formats.html#input-option-1-flat-dataframe-or-wide-dataframe>`_) Examples -------- >>> tslearn_arr = numpy.random.randn(1, 16, 1) >>> tsfresh_df = to_tsfresh_dataset(tslearn_arr) >>> tsfresh_df.shape (16, 3) >>> tslearn_arr = numpy.random.randn(1, 16, 2) >>> tsfresh_df = to_tsfresh_dataset(tslearn_arr) >>> tsfresh_df.shape (16, 4) Notes ----- Conversion from/to tsfresh format requires pandas to be installed.

### Goal
Convert a strict 3D `tslearn`-formatted time-series dataset into a "flat" pandas DataFrame compatible with the `tsfresh` feature extraction library.

### Parameters
- `X`: A 3D NumPy array of shape `(n_ts, max_sz, d)` representing the time-series dataset in standard `tslearn` format (number of time series, maximum sequence length, number of dimensions).

### Input
The caller must provide a strictly 3D NumPy array. If the original data is a list of variable-length arrays or a 2D array, it must first be converted using `tslearn.utils.to_time_series_dataset`. 
**Precondition:** The `pandas` library must be installed in the Python environment, as the output is a pandas DataFrame.

### Output
Returns `unspecified` — A pandas DataFrame representing the dataset in `tsfresh` "flat" format. The resulting DataFrame will have `n_ts * max_sz` rows and `d + 2` columns (an identifier column, a time step column, and `d` feature columns).

### Valid Call Patterns
```python
import numpy as np
import pandas as pd
from tslearn.utils import to_tsfresh_dataset

# 1. Create a small deterministic 3D tslearn dataset: (n_ts=2, sz=3, d=1)
X_tslearn = np.array([
    [[1.0], [2.0], [3.0]],
    [[4.0], [5.0], [6.0]]
])

# 2. Convert to tsfresh flat dataframe
tsfresh_df = to_tsfresh_dataset(X_tslearn)

# 3. Assert correctness
assert isinstance(tsfresh_df, pd.DataFrame), "Output must be a pandas DataFrame"
# Shape should be (n_ts * sz, d + 2) -> (2 * 3, 1 + 2) -> (6, 3)
assert tsfresh_df.shape == (6, 3), f"Expected shape (6, 3), got {tsfresh_df.shape}"

print(f"Successfully converted to tsfresh format. Columns: {list(tsfresh_df.columns)}")
```

### LLM Instruction Prompt
- When integrating `tslearn` with `tsfresh`, use `tslearn.utils.to_tsfresh_dataset(X)` to cast the 3D array into a flat pandas DataFrame.
- Ensure the input `X` is strictly a 3D array `(n_ts, max_sz, d)`. If the data is raw lists or 2D arrays, wrap it with `to_time_series_dataset` first.
- Do not call this function if `pandas` is not available in the environment.

### Prompt Snippet
```text
Convert the 3D tslearn array `X_train` into a tsfresh-compatible flat DataFrame using `tslearn.utils.to_tsfresh_dataset`. Ensure `pandas` is imported, as the function returns a DataFrame with `d + 2` columns containing the series IDs, time steps, and feature values.
```

### Common Failure Modes
- **ImportError for Pandas:** Calling this function in an environment without `pandas` installed will fail.
- **ValueError on 2D Inputs:** Passing a 2D array `(n_ts, max_sz)` instead of the required 3D array `(n_ts, max_sz, d)` will cause shape mismatch errors during the DataFrame construction.
- **Unpadded Variable-Length Data:** Passing a raw list of lists of different lengths directly to `to_tsfresh_dataset` will fail. It must be padded into a 3D array first.

### Fix Code Hint
```python
from tslearn.utils import to_time_series_dataset, to_tsfresh_dataset

# FIX: Ensure the input is a strict 3D array before converting to tsfresh format
X_3d = to_time_series_dataset(raw_variable_length_data)
tsfresh_df = to_tsfresh_dataset(X_3d)
```

## API Test: `transform`

### Signature
```python
def transform(self, X, y=None)
def transform(self, X)
def transform(self, X, y=None, timestamps=None)
def transform(self, X, y=None, **kwargs)
```
_Source: tslearn/tslearn/preprocessing/_synchronizer.py:78  (+10 more definition site/overload)_

_Source doc:_ Synchronizes features of each time series with the feature of reference through linear interpolation. When timestamps are not provided, constant sampling periods are assumed for all features and identical start and stop timestamps are assumed for all features of a given times series. When timestamps are provided, features are synchronized on the temporal grid of the reference feature. Parameters ---------- X : array-like of shape (n_ts, sz, d) Time series dataset to be synchronized feature wise. y : Ignored Not used, for API consistency by convention. timestamps : np.datetime64 array-like of shape (n_ts, sz, d) or None (default: None) Acquisition timestamps, same shape as X if not None. When provided, timestamps should be increasing for each feature and should use np.datetime64('nat') for missing values. Returns ------- numpy.ndarray Time series dataset synchronized feature wise.

### Goal
Applies a fitted transformation (such as scaling, resampling, or feature synchronization) to a time-series dataset, returning the transformed 3D array.

### Parameters
- `self`: The instantiated (and typically fitted) preprocessing estimator object (e.g., `TimeSeriesScalerMinMax`, `TimeSeriesScalerMeanVariance`, or a synchronizer).
- `X`: array-like of shape `(n_ts, sz, d)`. The time-series dataset to be transformed.
- `y`, default `None`: Ignored. Not used, present for `scikit-learn` API consistency by convention.
- `timestamps`, default `None`: `np.datetime64` array-like of shape `(n_ts, sz, d)` or `None`. Acquisition timestamps, used specifically by feature synchronizers to align features on a temporal grid.

### Input
- `X` must be a time-series dataset, ideally pre-formatted as a strict 3D `numpy` array of shape `(n_ts, max_sz, d)`. Raw lists of lists will be converted automatically.
- For variable-length time series, shorter series should be padded with `nan` values.
- The estimator (`self`) must have been previously fitted (e.g., via `.fit()` or `.fit_transform()`) if it learns parameters from data (like scalers).

### Output
Returns `numpy.ndarray` — A 3D `numpy` array of shape `(n_ts, new_sz, d)` containing the transformed time-series dataset. For variable-length inputs, shorter series remain padded with `nan` values in the scaled output.

### Valid Call Patterns
```python
import numpy as np
from tslearn.preprocessing import TimeSeriesScalerMinMax

# 1. Prepare variable-length training data
X_train = [
    [1, np.nan],
    [3, 4]
]

# 2. Instantiate and fit the estimator
estimator = TimeSeriesScalerMinMax(per_timeseries=True)
estimator.fit_transform(X_train)

# 3. Transform new data
transformed = estimator.transform([[1, 2, 3]])

np.testing.assert_array_equal(
    transformed,
    np.array([[[0.], [0.5], [1.]]])
)
```

### LLM Instruction Prompt
- Always ensure `X` is formatted as a 3D array `(n_ts, max_sz, d)` or a nested list that can be unambiguously converted to it.
- Call `transform` only on an already instantiated and fitted preprocessing estimator object.
- Do not pass `y` unless required by a specific pipeline, as it is ignored.
- Do not pass `timestamps` to standard scalers or resamplers; it is only supported by specific synchronizer estimators.

### Prompt Snippet
```text
When applying a transformation to new time-series data in tslearn, use `estimator.transform(X)`. Ensure the estimator is already fitted using `.fit(X_train)`. `X` should be a 3D array `(n_ts, max_sz, d)` or a list of lists. The output is always a 3D numpy array.
```

### Common Failure Modes
- **NotFittedError:** Calling `transform` on an estimator that requires fitting (like `TimeSeriesScalerMinMax`) before calling `fit` or `fit_transform`.
- **Incorrect Input Shape:** Passing a flat 1D array or a 2D array that cannot be safely broadcast to the `(n_ts, max_sz, d)` shape, leading to dimension mismatch errors.
- **Unsupported Arguments:** Passing the `timestamps` argument to standard scalers or resamplers that do not accept it (only synchronizers use it).

### Fix Code Hint
```python
# Ensure the estimator is fitted first, and input is properly nested
estimator = TimeSeriesScalerMinMax()
estimator.fit(X_train)

# X_test must be convertible to 3D (n_ts, max_sz, d)
X_test_transformed = estimator.transform(X_test)
```

## API Test: `tril`

### Signature
```python
def tril(mat, k=0)
```

### Goal
Returns the lower triangular portion of a 2D matrix, zeroing out elements above the specified diagonal, using the active computational backend (NumPy or PyTorch).

### Parameters
- `mat`: The input 2D matrix (NumPy array or PyTorch tensor) from which to extract the lower triangle.
- `k`, default `0`: The diagonal index above which elements are zeroed. `0` is the main diagonal, positive values are above it, and negative values are below it.

### Input
A 2D array-like object or tensor. The data type must be compatible with the specific backend being used (e.g., a `numpy.ndarray` for the NumPy backend or a `torch.Tensor` for the PyTorch backend).

### Output
Returns `unspecified` — A 2D matrix (array or tensor, matching the input type and backend) representing the lower triangular part of `mat`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.backend import instantiate_backend

# Instantiate the default NumPy backend
be = instantiate_backend("numpy")

# Create a 3x3 matrix
mat = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Extract the lower triangle (inferred from signature)
lower_tri = be.tril(mat, k=0)

# Verify elements above the main diagonal are zeroed
assert lower_tri[0, 1] == 0
assert lower_tri[0, 2] == 0
assert lower_tri[1, 2] == 0
assert lower_tri[2, 0] == 7  # Lower elements remain intact

print(lower_tri)
```

### LLM Instruction Prompt
- When extracting the lower triangle of a matrix in backend-agnostic `tslearn` code, use the `tril` method of the instantiated backend object. 
- Ensure the input matrix type matches the instantiated backend (e.g., pass a PyTorch tensor if the backend was instantiated with `"pytorch"`).
- Do not pass 1D arrays; `tril` expects a 2D matrix.

### Prompt Snippet
```text
# Use the backend's tril method to safely compute the lower triangle
# regardless of whether the input is a NumPy array or PyTorch tensor.
be = instantiate_backend(dataset)
lower_matrix = be.tril(dataset_matrix, k=0)
```

### Common Failure Modes
- **Type Mismatch:** Passing a PyTorch tensor to the NumPy backend's `tril` (or a NumPy array to the PyTorch backend) will raise a type error or `AttributeError` because the backend expects its native array type.
- **Dimensionality Error:** Passing a 1D array or a 3D time-series dataset `(n_ts, max_sz, d)` directly to `tril` without reshaping or selecting a 2D slice may result in unexpected broadcasting or backend-specific dimension errors.

### Fix Code Hint
```python
# FIX: Ensure the backend matches the input type and the input is 2D
be = instantiate_backend(mat) # Auto-detects backend from 'mat'
if be.ndim(mat) == 3:
    # Extract a single 2D time series if passing a 3D dataset
    mat = mat[0]
lower_tri = be.tril(mat, k=0)
```

## API Test: `tril_indices`

### Signature
```python
def tril_indices(n, k=0, m=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:221_

### Goal
Generates the row and column indices for the lower triangle of an `(n, m)` matrix, serving as a backend-agnostic helper (NumPy or PyTorch) for time-series alignment and distance metric computations.

### Parameters
- `n`: Integer representing the row dimension of the 2D array for which to return the indices.
- `k`, default `0`: Integer representing the diagonal offset. `0` is the main diagonal, positive values are above the main diagonal, and negative values are below it.
- `m`, default `None`: Integer representing the column dimension of the 2D array. If `None`, it defaults to `n` (creating indices for a square matrix).

### Input
Integer dimensions (`n`, `m`) and an integer offset (`k`). This is typically used internally when constructing distance matrices or alignment paths for time-series metrics.

### Output
Returns `unspecified` — A tuple of two 1D arrays (if using the NumPy backend) or two 1D tensors (if using the PyTorch backend) containing the row and column indices of the lower triangle.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

# Inferred from signature and backend usage patterns
be = instantiate_backend("numpy")
row_idx, col_idx = be.tril_indices(n=3, k=0)

assert len(row_idx) == 6
assert len(col_idx) == 6
print("Row indices:", row_idx)
print("Col indices:", col_idx)
```

### LLM Instruction Prompt
- When computing custom alignment paths or distance matrices, use `tril_indices` via the instantiated backend object (e.g., `be = instantiate_backend(...)`) to ensure the returned index arrays match the active backend type (NumPy arrays or PyTorch tensors). Do not attempt to import it as a standalone top-level function.

### Prompt Snippet
```text
tslearn.backend.Backend.tril_indices: Generates lower-triangle indices for an (n, m) matrix.
Call via an instantiated backend: `be = instantiate_backend('numpy'); be.tril_indices(n=3)`.
Returns a tuple of (row_indices, col_indices) as arrays or tensors depending on the backend.
```

### Common Failure Modes
- **Calling as a standalone function:** Attempting to import and call `tril_indices` directly from `tslearn` instead of accessing it through an instantiated backend object (e.g., `be.tril_indices(n)`).
- **Non-integer dimensions:** Passing float values for `n`, `k`, or `m`, which will trigger a `TypeError` in the underlying NumPy or PyTorch implementations.
- **Missing PyTorch dependency:** Attempting to use this method via the PyTorch backend (`instantiate_backend("pytorch")`) in an environment where `torch` is not installed.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend

# 1. Instantiate the desired backend (e.g., "numpy" or "pytorch")
be = instantiate_backend("numpy")

# 2. Call tril_indices on the backend instance with integer dimensions
n_rows = 4
row_indices, col_indices = be.tril_indices(n=n_rows, k=0)
```

## API Test: `triu`

### Signature
```python
def triu(mat, k=0)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:228_

### Goal
Returns the upper triangular part of a 2D matrix or tensor, zeroing out elements below the specified diagonal.

### Parameters
- `mat`: The input 2D matrix (PyTorch tensor) from which to extract the upper triangular portion.
- `k`, default `0`: The diagonal offset. `k=0` represents the main diagonal, `k>0` is above the main diagonal, and `k<0` is below it.

### Input
A 2D PyTorch tensor. When using the PyTorch backend, the input must be a valid `torch.Tensor`.

### Output
Returns `unspecified` — A PyTorch tensor of the same shape and data type as `mat`, with all elements below the `k`-th diagonal set to zero.

### Valid Call Patterns
```python
import torch
from tslearn.backend import instantiate_backend

# Instantiate the PyTorch backend
be = instantiate_backend("pytorch")
mat = torch.tensor([[1.0, 2.0, 3.0], 
                    [4.0, 5.0, 6.0], 
                    [7.0, 8.0, 9.0]])

# Inferred from signature (not verified)
upper_tri = be.triu(mat, k=0)

assert upper_tri[1, 0].item() == 0.0
assert upper_tri[2, 0].item() == 0.0
assert upper_tri[2, 1].item() == 0.0
assert upper_tri[0, 2].item() == 3.0
```

### LLM Instruction Prompt
- Call `triu` via a dynamically instantiated backend object (e.g., `be = instantiate_backend("pytorch")`) to ensure cross-compatibility, rather than importing the backend module directly.
- Ensure the input `mat` matches the expected type of the active backend (e.g., a `torch.Tensor` for the PyTorch backend).
- Use the `k` parameter to control which diagonal serves as the boundary for zeroing out elements.

### Prompt Snippet
```text
tslearn.backend.instantiate_backend("pytorch").triu(mat, k=0)
```

### Common Failure Modes
- Passing a NumPy array to the PyTorch backend's `triu` function without converting it to a `torch.Tensor` first, resulting in a type error.
- Passing a 1D array or a tensor with more than 2 dimensions, which may cause unexpected broadcasting or shape errors depending on the underlying PyTorch `triu` implementation.
- Attempting to call `triu` as a standalone function without routing it through the backend instance.

### Fix Code Hint
```python
import torch
from tslearn.backend import instantiate_backend

be = instantiate_backend("pytorch")
# Ensure input is a 2D PyTorch tensor before calling the PyTorch backend
mat = torch.tensor([[1, 2], [3, 4]])
upper = be.triu(mat, k=0)
```

## API Test: `triu_indices`

### Signature
```python
def triu_indices(n, k=0, m=None)
```
_Source: tslearn/tslearn/backend/pytorch_backend.py:232_

### Goal
Returns the indices for the upper-triangle of an (n, m) matrix, abstracting over the NumPy and PyTorch backends.

### Parameters
- `n`: Integer representing the size of the first dimension (rows) of the matrix.
- `k`, default `0`: Integer representing the diagonal offset. `k=0` includes the main diagonal, `k>0` is above it, and `k<0` is below it.
- `m`, default `None`: Integer representing the size of the second dimension (columns). If `None`, it defaults to `n` (creating a square matrix).

### Input
Integer dimensions `n` (rows) and optionally `m` (columns), along with an integer diagonal offset `k`. No time-series data is passed directly to this helper.

### Output
Returns `unspecified` — A tuple of two 1D arrays (if using the NumPy backend) or tensors (if using the PyTorch backend) containing the row and column indices for the upper triangle of the specified matrix dimensions.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

# Instantiate the desired backend
be = instantiate_backend("numpy")

# Call form inferred from signature
row_idx, col_idx = be.triu_indices(3, k=0)

assert len(row_idx) == 6
assert len(col_idx) == 6
print("triu_indices returned valid indices")
```

### LLM Instruction Prompt
- Call `triu_indices` via an instantiated backend object (e.g., `be = instantiate_backend("numpy"); be.triu_indices(n)`) to ensure compatibility across NumPy and PyTorch.
- Provide integer dimensions `n` (and optionally `m`) to generate the upper-triangular indices.

### Prompt Snippet
```text
When computing upper-triangular indices in tslearn, use the backend instance's `triu_indices(n, k=0, m=None)` method. This returns a tuple of row and column indices (as arrays or tensors) for an (n, m) matrix, abstracting over NumPy and PyTorch.
```

### Common Failure Modes
- Calling `triu_indices` directly from `tslearn.backend` instead of an instantiated backend object (e.g., `NumPyBackend` or `PyTorchBackend`).
- Passing non-integer values for `n`, `k`, or `m`, which will cause a `TypeError` in the underlying NumPy or PyTorch function.

### Fix Code Hint
```python
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")
# Correct: access via the backend instance
row_idx, col_idx = be.triu_indices(n=3, k=1)
```

## API Test: `ts_size`

### Signature
```python
def ts_size(ts, be=None)
```
_Source: tslearn/tslearn/utils/utils.py:465_

_Source doc:_ Returns actual time series size. Final timesteps that have `NaN` values for all dimensions will be removed from the count. Infinity and negative infinity ar considered valid time series values. Parameters ---------- ts : array-like A time series. be : Backend object or string or None Backend. If `be` is an instance of the class `NumPyBackend` or the string `"numpy"`, the NumPy backend is used. If `be` is an instance of the class `PyTorchBackend` or the string `"pytorch"`, the PyTorch backend is used. If `be` is `None`, the backend is determined by the input arrays. See our :ref:`dedicated user-guide page <backend>` for more information. Returns ------- int Actual size of the time series. Examples -------- >>> ts_size([1, 2, 3, numpy.nan]) 3 >>> ts_size([1, numpy.nan]) 1 >>> ts_size([numpy.nan]) 0 >>> ts_size([[1, 2], ...          [2, 3], ...          [3, 4], ...          [numpy.nan, 2], ...          [numpy.nan, numpy.nan]]) 4 >>> ts_size([numpy.nan, 3, numpy.inf, numpy.nan]) 3

### Goal
Calculate the actual unpadded length of a single time series by ignoring trailing timesteps that consist entirely of `NaN` values.

### Parameters
- `ts`: An array-like (e.g., list, NumPy array, or PyTorch tensor) representing a single time series.
- `be`, default `None`: The backend to use for computation. Can be a Backend instance, the string `"numpy"`, or the string `"pytorch"`. If `None`, the backend is automatically inferred from the type of the `ts` input.

### Input
The caller must provide a single time series (1D or 2D array-like of shape `(sz,)` or `(sz, d)`). If the time series was extracted from a padded 3D `tslearn` dataset, it may contain trailing `NaN` values. 
*Preconditions:* The input should represent a *single* time series, not a full 3D dataset of multiple time series. For multidimensional time series, a trailing timestep is only considered padding (and thus excluded from the size) if *all* of its dimensions are `NaN`. Infinity (`inf` or `-inf`) is considered a valid measurement.

### Output
Returns `unspecified` — An integer (`int`) representing the actual number of valid timesteps in the time series before the trailing all-`NaN` padding begins.

### Valid Call Patterns
```python
import numpy as np
import tslearn.utils

# 1D time series with trailing NaN
ts_1d = np.array([1.0, 2.0, 3.0, np.nan, np.nan])
size_1d = tslearn.utils.ts_size(ts_1d)
assert size_1d == 3

# 2D time series where a partially-NaN timestep is still counted
ts_2d = np.array([
    [1.0, 2.0],
    [np.nan, 2.0], # Counted: not ALL dimensions are NaN
    [np.nan, np.nan] # Ignored: trailing and ALL dimensions are NaN
])
size_2d = tslearn.utils.ts_size(ts_2d)
assert size_2d == 2
```

### LLM Instruction Prompt
- Use `tslearn.utils.ts_size(ts)` to determine the true length of a single time series that may have been padded with `NaN`s to fit into a uniform 3D dataset array.
- Remember that `ts_size` only strips *trailing* `NaN`s. Internal `NaN`s or trailing `inf` values are counted as valid timesteps.
- For multidimensional time series, a timestep is only stripped if *every* dimension in that timestep is `NaN`.

### Prompt Snippet
```text
`tslearn.utils.ts_size(ts, be=None)` returns the integer length of a single time series `ts`, ignoring any trailing timesteps that are entirely `NaN`. Useful for finding the original length of variable-length time series extracted from a padded `(n_ts, max_sz, d)` dataset.
```

### Common Failure Modes
- **Passing a full 3D dataset:** `ts_size` is designed to evaluate a *single* time series (1D or 2D). Passing a 3D array `(n_ts, max_sz, d)` will yield incorrect or unexpected results. You must iterate over the dataset to get individual sizes.
- **Assuming internal NaNs are removed:** `ts_size([np.nan, 3.0, np.nan])` returns `2`, not `1`. Only the contiguous block of `NaN`s at the very end of the array is subtracted from the total length.
- **Assuming partial NaNs are removed:** In a multidimensional time series, a timestep like `[np.nan, 5.0]` at the end of the series will *not* be removed because it is not entirely `NaN`.

### Fix Code Hint
```python
# BAD: Trying to get the size of an entire 3D dataset at once
# dataset_size = tslearn.utils.ts_size(X_padded)

# GOOD: Iterating through the dataset to find the true length of each time series
actual_lengths = [tslearn.utils.ts_size(ts) for ts in X_padded]

# GOOD: Slicing a padded time series to its true length
ts_true = ts[:tslearn.utils.ts_size(ts)]
```

## API Test: `ts_zeros`

### Signature
```python
def ts_zeros(sz, d=1)
```
_Source: tslearn/tslearn/utils/utils.py:521_

_Source doc:_ Returns a time series made of zero values. Parameters ---------- sz : int Time series size. d : int (optional, default: 1) Time series dimensionality. Returns ------- numpy.ndarray A time series made of zeros. Examples -------- >>> ts_zeros(3, 2)  # doctest: +NORMALIZE_WHITESPACE array([[0., 0.], [0., 0.], [0., 0.]]) >>> ts_zeros(5).shape (5, 1)

### Goal
Generates a single synthetic time series of a specified length and dimensionality filled entirely with zero values.

### Parameters
- `sz`: `int` — The size (number of time steps) of the generated time series.
- `d`, default `1`: `int` — The dimensionality (number of features per time step) of the generated time series.

### Input
The caller must provide integer values for the size (`sz`) and optionally the dimensionality (`d`). No external data or file formats are required.

### Output
Returns `unspecified` — A 2D `numpy.ndarray` of floats with shape `(sz, d)` representing a single time series filled with `0.0`.

### Valid Call Patterns
```python
from tslearn.utils import ts_zeros
import numpy as np

# Inferred from signature and source doc examples
# Generate a single time series of length 3 with 2 dimensions
ts = ts_zeros(sz=3, d=2)

assert isinstance(ts, np.ndarray), "Output must be a NumPy array"
assert ts.shape == (3, 2), "Output shape must match (sz, d)"
assert np.all(ts == 0.0), "All values must be zero"

print("Generated zero time series:\n", ts)
```

### LLM Instruction Prompt
- Use `ts_zeros(sz, d)` to generate a single baseline or synthetic time series filled with zeros.
- **Crucial:** `ts_zeros` returns a 2D array `(sz, d)` representing a *single* time series. `tslearn` estimators strictly require 3D arrays `(n_ts, max_sz, d)`. If you intend to pass the output of `ts_zeros` to an estimator's `.fit()` or `.predict()` method, you must reshape it to 3D (e.g., using `numpy.expand_dims(ts, axis=0)` or `to_time_series_dataset([ts])`).

### Prompt Snippet
```text
Generate a single 2D zero-filled time series of length 10 and 1 dimension using `tslearn.utils.ts_zeros`, then reshape it to the strict 3D format `(n_ts, max_sz, d)` required by tslearn estimators.
```

### Common Failure Modes
- **Dimensionality Error with Estimators:** Passing the raw 2D output of `ts_zeros` directly into a `tslearn` estimator (like `TimeSeriesKMeans` or `TimeSeriesScalerMinMax`). This will fail because estimators strictly expect a 3D array `(n_ts, max_sz, d)`.
- **Type Errors:** Passing non-integer values (like floats) for `sz` or `d`, which will cause NumPy shape initialization to fail.

### Fix Code Hint
```python
from tslearn.utils import ts_zeros
import numpy as np

# 1. Generate the single time series (returns a 2D array: sz=5, d=1)
single_ts_2d = ts_zeros(sz=5, d=1)

# 2. Convert to the strict 3D format (n_ts=1, max_sz=5, d=1) required by estimators
dataset_3d = np.expand_dims(single_ts_2d, axis=0)

# Now dataset_3d can be safely passed to tslearn estimators or preprocessing APIs
```

## API Test: `uniform`

### Signature
```python
def uniform(low=0.0, high=1.0, size=(1,), dtype=None)
```

### Goal
Generates an array or tensor of uniformly distributed random numbers within a specified range, using the active computational backend (NumPy or PyTorch).

### Parameters
- `low`, default `0.0`: The lower bound (inclusive) of the uniform distribution.
- `high`, default `1.0`: The upper bound (exclusive) of the uniform distribution.
- `size`, default `(1,)`: A tuple specifying the shape of the output array or tensor.
- `dtype`, default `None`: The desired data type of the output (e.g., `numpy.float64` or `torch.float64`). If `None`, defaults to the backend's standard float type.

### Input
Scalar bounds and a tuple for the desired shape. The backend must be instantiated first via `tslearn.backend.instantiate_backend`.

### Output
Returns `unspecified` — A backend-specific array or tensor (NumPy `ndarray` or PyTorch `Tensor`) containing random values sampled from the uniform distribution `[low, high)`.

### Valid Call Patterns
```python
from tslearn.backend import instantiate_backend

be = instantiate_backend("numpy")

# Call inferred from signature (not verified)
random_tensor = be.uniform(low=-0.5, high=0.5, size=(10, 5, 1))
assert random_tensor.shape == (10, 5, 1)
print(random_tensor.shape)
```

### LLM Instruction Prompt
- When generating random time-series data or initializing weights within a backend-agnostic function, use `be.uniform()` on the instantiated backend object rather than hardcoding `numpy.random.uniform` or `torch.rand`.

### Prompt Snippet
```text
from tslearn.backend import instantiate_backend

# Generate a random 3D time-series dataset using the PyTorch backend
be = instantiate_backend("pytorch")
X_random = be.uniform(low=-1.0, high=1.0, size=(10, 50, 1))
```

### Common Failure Modes
- Calling `uniform` directly as a module-level function instead of as a method on an instantiated backend object.
- Passing a scalar instead of a tuple for the `size` parameter, which may cause shape resolution errors in some backends.
- Requesting a `dtype` that is incompatible with the active backend (e.g., passing a PyTorch dtype to the NumPy backend).

### Fix Code Hint
```python
# BAD: Calling uniform directly or using incompatible dtypes
# import tslearn.backend as backend
# arr = backend.uniform(size=10)

# GOOD: Instantiate the backend and pass a tuple for size
from tslearn.backend import instantiate_backend
be = instantiate_backend("numpy")
arr = be.uniform(low=0.0, high=1.0, size=(10,))
```

## API Test: `unnormalized_gak`

### Signature
```python
def unnormalized_gak(s1, s2, sigma=1.0, be=None)
```
_Source: tslearn/tslearn/metrics/softdtw_variants.py:138  (+1 more definition site/overload)_

### Goal
Compute the unnormalized Global Alignment Kernel (GAK) similarity between two (possibly multidimensional and variable-length) time series.

### Parameters
- `s1`: First time series. Array-like of shape `(sz1, d)` for multivariate or `(sz1,)` for univariate time series.
- `s2`: Second time series. Array-like of shape `(sz2, d)` for multivariate or `(sz2,)` for univariate time series.
- `sigma`, default `1.0`: Bandwidth of the internal Gaussian kernel used for GAK (float). Must be strictly greater than 0.
- `be`, default `None`: Backend identifier. Can be a string (`"numpy"` or `"pytorch"`), a Backend instance, or `None`. If `None`, the backend is automatically determined by the input array types.

### Input
The caller must provide two time series as lists, NumPy arrays, or PyTorch tensors. The two time series are not required to share the same length (`sz1` and `sz2` can differ), but they **must** have the exact same feature dimensionality (`d`). If using the PyTorch backend for automatic differentiation, inputs must be PyTorch tensors.

### Output
Returns `unspecified` — A scalar float (if using the NumPy backend) or a 0-dimensional PyTorch tensor (if using the PyTorch backend) representing the unnormalized kernel similarity value between the two time series.

### Valid Call Patterns
```python
import tslearn.metrics
import torch

# 1. Standard NumPy/List usage
s1 = [1.0, 2.0, 3.0]
s2 = [1.0, 2.0, 2.0, 3.0, 4.0]
kernel_val = tslearn.metrics.unnormalized_gak(s1, s2, sigma=2.0)
assert isinstance(kernel_val, float)

# 2. PyTorch backend usage
ts1 = torch.tensor([[1.0], [2.0], [3.0]])
ts2 = torch.tensor([[1.0], [2.0], [2.0], [3.0]])
kernel_tensor = tslearn.metrics.unnormalized_gak(ts1, ts2, sigma=2.0, be="pytorch")
```

### LLM Instruction Prompt
- When calling `tslearn.metrics.unnormalized_gak`, ensure that `sigma` is strictly greater than `0` to prevent a `ZeroDivisionError`.
- Ensure both time series `s1` and `s2` have the same feature dimension `d`.
- If you need a normalized similarity metric where `k(x,x) = 1`, use `tslearn.metrics.gak` instead.
- If passing PyTorch tensors that require gradients, explicitly pass `be="pytorch"` or rely on auto-detection, but ensure inputs are properly shaped 2D tensors `(length, dim)`.

### Prompt Snippet
```text
Use `tslearn.metrics.unnormalized_gak(s1, s2, sigma=1.0)` to compute the unnormalized Global Alignment Kernel between two time series. Both inputs must have the same feature dimension `d`. `sigma` must be > 0. For normalized GAK, use `tslearn.metrics.gak`.
```

### Common Failure Modes
- **`ZeroDivisionError`**: Occurs if `sigma=0` is passed, as the internal Gaussian kernel divides by `2 * sigma^2`.
- **Dimension Mismatch**: Occurs if `s1` has shape `(sz1, d1)` and `s2` has shape `(sz2, d2)` where `d1 != d2`.
- **Missing Import**: Calling `unnormalized_gak` directly without importing `tslearn.metrics` first.

### Fix Code Hint
```python
import tslearn.metrics

# FIX: Ensure sigma > 0 to avoid ZeroDivisionError
# FIX: Ensure both time series have the same feature dimension (e.g., both univariate)
s1 = [[1.0], [2.0], [3.0]]
s2 = [[1.0], [2.0], [2.0], [3.0]]

# Compute unnormalized GAK with a valid sigma
similarity = tslearn.metrics.unnormalized_gak(s1, s2, sigma=1.5)
```

## API Test: `y_shifted_sbd_vec`

### Signature
```python
def y_shifted_sbd_vec(ref_ts, dataset, norm_ref, norms_dataset)
```
_Source: tslearn/tslearn/metrics/cycc.py:99_

_Source doc:_ Shift a time series dataset w.r.t. a time series of reference. Parameters ---------- ref_ts : array-like, shape=(sz, d), dtype=float64 Time series of reference. dataset : array-like, shape=(n_ts, sz, d), dtype=float64 Time series dataset. norm_ref : float64 norms_dataset : array-like, shape=(n_ts,), dtype=float64 Norms of the time series dataset. Returns ------- dataset_shifted : array-like, shape=(n_ts, sz, d), dtype=float64 Shifted dataset.

### Goal
Shift a time-series dataset to optimally align with a reference time series based on Shape-Based Distance (SBD) cross-correlation.

### Parameters
- `ref_ts`: The reference time series to align against, expected as a 2D array of shape `(sz, d)` and dtype `float64`.
- `dataset`: The time-series dataset to be shifted, expected as a 3D array of shape `(n_ts, sz, d)` and dtype `float64`.
- `norm_ref`: The precomputed scalar norm of the reference time series, as a `float64`.
- `norms_dataset`: The precomputed norms of each time series in the dataset, expected as a 1D array of shape `(n_ts,)` and dtype `float64`.

### Input
The caller must provide NumPy arrays strictly cast to `float64`. The `dataset` must follow `tslearn`'s standard 3D format `(n_ts, sz, d)`, while the `ref_ts` must be a single 2D time series `(sz, d)`. The lengths (`sz`) and dimensions (`d`) of the reference and the dataset must match exactly. The norms must be precomputed by the caller (typically using the L2 norm).

### Output
Returns `unspecified` — A 3D NumPy array of shape `(n_ts, sz, d)` and dtype `float64` representing the shifted dataset, where each time series has been circularly shifted to maximize its cross-correlation with the reference time series.

### Valid Call Patterns
```python
import numpy as np
from tslearn.metrics.cycc import y_shifted_sbd_vec

# 1. Prepare deterministic float64 inputs
ref_ts = np.array([[1.0], [2.0], [3.0]], dtype=np.float64)
dataset = np.array([
    [[2.0], [3.0], [1.0]], 
    [[3.0], [1.0], [2.0]]
], dtype=np.float64)

# 2. Precompute norms
norm_ref = float(np.linalg.norm(ref_ts))
norms_dataset = np.linalg.norm(dataset, axis=(1, 2)).astype(np.float64)

# 3. Compute the shifted dataset (inferred from signature)
shifted_dataset = y_shifted_sbd_vec(ref_ts, dataset, norm_ref, norms_dataset)

assert shifted_dataset.shape == (2, 3, 1)
print(f"Shifted dataset shape: {shifted_dataset.shape}")
```

### LLM Instruction Prompt
- When calling `y_shifted_sbd_vec`, you MUST ensure `ref_ts` is a 2D array `(sz, d)` and `dataset` is a 3D array `(n_ts, sz, d)`. Do not pass 1D arrays or lists.
- You MUST precompute the norms of the reference and dataset before passing them as `norm_ref` and `norms_dataset`.
- You MUST cast all array inputs to `numpy.float64` to prevent Cython type errors.

### Prompt Snippet
```text
Use `tslearn.metrics.cycc.y_shifted_sbd_vec` to align a dataset to a reference time series. Ensure `ref_ts` is `(sz, d)` and `dataset` is `(n_ts, sz, d)`. Precompute `norm_ref` (scalar) and `norms_dataset` (1D array). Cast all arrays to `float64`.
```

### Common Failure Modes
- **Cython Type Errors**: Passing integers, `float32`, or standard Python lists instead of `float64` NumPy arrays will cause Cython buffer type mismatches.
- **Dimensionality Mismatch**: Passing a 1D array for `ref_ts` or a 2D array for `dataset` violates the strict `(sz, d)` and `(n_ts, sz, d)` shape requirements.
- **Length Mismatch**: Providing a `ref_ts` with a different number of time steps (`sz`) than the `dataset` will result in alignment failures or out-of-bounds memory access.

### Fix Code Hint
```python
# Ensure correct shapes and float64 types
ref_ts = np.asarray(ref_ts, dtype=np.float64)
if ref_ts.ndim == 1:
    ref_ts = ref_ts.reshape(-1, 1)

dataset = np.asarray(dataset, dtype=np.float64)
if dataset.ndim == 2:
    dataset = dataset.reshape(dataset.shape[0], dataset.shape[1], 1)

# Precompute norms
norm_ref = float(np.linalg.norm(ref_ts))
norms_dataset = np.linalg.norm(dataset, axis=(1, 2)).astype(np.float64)

# Call the Cython helper
shifted = y_shifted_sbd_vec(ref_ts, dataset, norm_ref, norms_dataset)
```

