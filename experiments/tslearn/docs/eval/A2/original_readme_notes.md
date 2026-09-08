Here are the distilled factual notes for the `tslearn` documentation, structured for README and API generation.

### 1. Project purpose
`tslearn` is a scientific machine-learning toolkit dedicated to time-series data analysis in Python. It provides a comprehensive suite of tools for time-series classification, clustering, regression, forecasting, and distance metric calculations. The library is architected to be fully compatible with `scikit-learn`, allowing users to seamlessly integrate time-series estimators into standard machine-learning pipelines. Additionally, it features a dual-backend system (NumPy and PyTorch) to enable automatic differentiation and gradient computation for complex time-series alignment metrics.

### 2. Main workflows
The primary workflows in `tslearn` consist of:
*   **Data Formatting:** Converting raw lists or arrays of time-series data into a strict 3D array structure required by all estimators.
*   **Preprocessing and Transformation:** Scaling, resampling, or applying piece-wise transformations to time-series datasets to speed up training times and facilitate algorithm convergence.
*   **Model Training:** Fitting classification, clustering, or regression models to the formatted data using a `scikit-learn` compatible API.
*   **Metric Computation:** Calculating distances, similarities, alignments, and barycenters between time series using specialized metrics like Dynamic Time Warping (DTW) and Soft-DTW.
*   **Automatic Differentiation:** Utilizing the PyTorch backend to compute gradients of metric functions for advanced neural network integration.

### 3. Important APIs and usage patterns
*   **Data Preparation:** `tslearn.utils.to_time_series_dataset` converts raw data into the required 3D format. `tslearn.datasets` loads UCR datasets. `tslearn.generators` creates synthetic data.
*   **Preprocessing:** `tslearn.preprocessing.TimeSeriesScalerMinMax` scales data. `tslearn.preprocessing.TimeSeriesResampler` resamples data. `tslearn.piecewise` handles piece-wise transformations.
*   **Classification:** `tslearn.neighbors.KNeighborsTimeSeriesClassifier`, `tslearn.svm.TimeSeriesSVC`, `tslearn.shapelets.LearningShapelets`, and `tslearn.early_classification`.
*   **Clustering:** `tslearn.clustering.TimeSeriesKMeans`, `tslearn.clustering.KShape`, and `tslearn.clustering.KernelKMeans`.
*   **Regression:** `tslearn.neighbors.KNeighborsTimeSeriesRegressor` and `tslearn.svm.TimeSeriesSVR`.
*   **Neural Networks:** `tslearn.neural_network` provides MLP implementations.
*   **Metrics:** `tslearn.metrics.dtw`, `tslearn.metrics.soft_dtw`, and `tslearn.metrics.gak` (Global Alignment Kernel).
*   **Advanced Analysis:** `tslearn.barycenters` computes barycenters; `tslearn.matrix_profile` computes matrix profiles.
*   **Backends:** `tslearn.backend.instantiate_backend` dynamically selects and initializes the computational backend.

### 4. Inputs and file formats
`tslearn` strictly expects time-series datasets to be formatted as 3D `numpy` arrays. The three dimensions must correspond to `(n_ts, max_sz, d)`, representing the number of time series, the maximum number of measurements per time series, and the number of dimensions, respectively. The toolkit natively supports variable-length time series. The library also includes built-in parsers for standard UCR datasets (e.g., the "Beef" dataset spectrograms). Inputs to backend metric functions can be `numpy` arrays or `torch` tensors.

### 5. Outputs and generated artifacts
*   **Transformed Data:** Preprocessing APIs output 3D `numpy` arrays. For variable-length time series, shorter series are padded with `nan` values in the scaled output.
*   **Estimators:** Training yields fitted model objects capable of executing `.predict()` or `.fit_predict()` methods.
*   **Metrics:** Distance functions return scalar similarity/distance floats or PyTorch tensors.
*   **Gradients:** When using the PyTorch backend, metric outputs are tensors attached to a computation graph (e.g., `grad_fn=<SqrtBackward0>`), allowing `.backward()` to populate `.grad` attributes on the input tensors.

### 6. Configuration and environment assumptions
*   The library requires Python 3.10 or higher.
*   Core dependencies include `numpy`, `scikit-learn`, `scipy`, and `matplotlib`.
*   The PyTorch backend requires the `pytorch` package to be installed locally.
*   Backends are dynamically instantiated. If no valid backend is specified or detected, the environment defaults to using NumPy.

### 7. Commands and examples

**Getting the data in the right format:**
```python3
>>> from tslearn.utils import to_time_series_dataset
>>> my_first_time_series = [1, 3, 4, 2]
>>> my_second_time_series = [1, 2, 4, 2]
>>> my_third_time_series = [1, 2, 4, 2, 2]
>>> X = to_time_series_dataset([my_first_time_series,
                                my_second_time_series,
                                my_third_time_series])
>>> y = [0, 1, 1]
```

**Data preprocessing and transformations:**
```python3
>>> from tslearn.preprocessing import TimeSeriesScalerMinMax
>>> X_scaled = TimeSeriesScalerMinMax().fit_transform(X)
>>> print(X_scaled)
[[[0.] [0.667] [1.] [0.333] [nan]]
 [[0.] [0.333] [1.] [0.333] [nan]]
 [[0.] [0.333] [1.] [0.333] [0.333]]]
```

**Training a model:**
```python3
>>> from tslearn.neighbors import KNeighborsTimeSeriesClassifier
>>> knn = KNeighborsTimeSeriesClassifier(n_neighbors=1)
>>> knn.fit(X_scaled, y)
>>> print(knn.predict(X_scaled))
[0 1 1]
```

**Backend selection loop:**
```python3
>>> be = instantiate_backend(1, None, "Hello, World!", torch.tensor([0]), "numpy")
>>> print(be.backend_string)
"pytorch"
```

**Automatic differentiation with Soft-DTW:**
```python3
>>> from tslearn.metrics import soft_dtw
>>> ts1 = torch.tensor([[1.0], [2.0], [3.0]], requires_grad=True)
>>> ts2 = torch.tensor([[3.0], [4.0], [-3.0]])
>>> sim = soft_dtw(ts1, ts2, gamma=1.0, be="pytorch", compute_with_backend=True)
>>> print(sim)
tensor(41.1876, dtype=torch.float64, grad_fn=<SelectBackward0>)
>>> sim.backward()
>>> d_ts1 = ts1.grad
>>> print(d_ts1)
tensor([[-4.0001],
        [-2.2852],
        [10.1643]])
```

### 8. Constraints, preconditions, compatibility rules, and type-selection rules
*   **Preconditions:** Data *must* be converted to the `(n_ts, max_sz, d)` 3D array format before applying preprocessing or training models.
*   **Compatibility:** Estimators are fully compatible with `scikit-learn` utilities, including hyper-parameter tuning and pipelines.
*   **Backend Selection Rules:** `instantiate_backend` accepts multiple arguments and evaluates them in a `for` loop until a backend is selected. Selection rules:
    *   String `"numpy"` or a `NumPy` array -> `NumPyBackend`.
    *   String `"pytorch"` or a `Torch` tensor -> `PyTorchBackend`.
    *   Existing Backend instance -> returns the input backend.
    *   `None` or unrecognized input -> defaults to `NumPyBackend`.
*   **Metric Backend Auto-detection:** Metric functions (like `dtw` and `soft_dtw`) have an optional `be` parameter (default `None`). They auto-detect the backend from the input data types. If inputs are `torch` tensors, the PyTorch backend is automatically instantiated and used, even if `be=None`.
*   **Gradient Computation Constraints:** To compute gradients using `.backward()`, inputs must be `torch` tensors with `requires_grad=True`, and the metric must be computed using the PyTorch backend. For `soft_dtw`, the flag `compute_with_backend=True` must be explicitly provided.

### 9. Facts to preserve in the final README
*   `tslearn` natively supports variable-length time series.
*   The library provides a PyTorch backend specifically to enable automatic differentiation for time-series metrics like DTW and Soft-DTW.
*   The API is intentionally designed to mirror `scikit-learn` conventions.
*   The toolkit includes built-in access to UCR datasets and synthetic data generators.

### 10. Missing or weak documentation
*   The exact internal representation and padding mechanism for variable-length time series is not clearly documented (the example shows `nan` values, but the padding process during `to_time_series_dataset` is implicit).
*   Specific usage examples for `LearningShapelets`, `Matrix Profile`, `Early Classification`, and `Barycenters` are missing from the core README and backend guides.
*   The documentation does not clearly explain the `compute_with_backend=True` parameter required in `soft_dtw` for gradient computation, nor why it differs from standard `dtw` calls.