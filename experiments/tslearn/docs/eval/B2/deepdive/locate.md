# Deep-dive: `locate`

model: google:gemini-3.1-pro-preview · tokens in=5,674 out=4,201 · wall 34s · 2026-09-08 15:48

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
USER-FACING. NOT TESTABLE IN THIS HARNESS. 
The `locate` method is a public, user-facing API on the `LearningShapelets` estimator. However, it is not testable in this harness because `LearningShapelets` relies on the `keras` library to build and execute its underlying neural network models (as evidenced by the `Model`, `Input`, and `GlobalArgminPooling1D` usage in `_build_auxiliary_models`). The failure history explicitly shows an infrastructure failure (`No module named 'keras'`), indicating this optional dependency is absent from the test environment.

L1 PURPOSE
The `locate` method computes the starting index (location) of the best match for each learned shapelet within a set of time series. It sits at the end of the shapelet learning data flow, allowing users to interpret a trained `LearningShapelets` model by extracting the specific subsequences in their data that correspond to the discriminative patterns the model has learned.

L2 CONTRACT
- **Receiver**: A fitted `LearningShapelets` instance. Obtained by instantiating `tslearn.shapelets.LearningShapelets` and calling `.fit(X, y)`.
- **Parameters**:
  - `X`: `array-like` of shape `(n_ts, sz, d)`. The time series dataset to search for shapelet matches.
- **Returns**: A `numpy.ndarray` of shape `(n_ts, n_shapelets)` and dtype `int`. It contains the integer indices representing the starting location of the best match for each shapelet in each provided time series.
- **Visibility**: Public.
- **Thread-safety/Laziness**: Eager execution. Thread-safety depends entirely on the thread-safety of the underlying Keras model's `predict` method.

L3 MECHANICS
1. **Validation**: Calls `check_is_fitted(self, '_X_fit_dims')` to ensure the estimator has been trained (line 657).
2. **Array Conversion**: Passes `X` through `check_array(..., allow_nd=True, force_all_finite=False)` to ensure it is a valid NumPy array (line 658).
3. **Preprocessing**: Delegates to `self._preprocess_series(X)` (line 659), which scales the data if `self.scale` is true and pads it with `numpy.nan` to match the maximum allowed size.
4. **Dimension Checks**: Calls `check_dims` to verify feature dimensions match the training data (line 660), and `self._check_series_length(X)` to ensure the series are longer than the longest shapelet but not longer than the maximum allowed size (line 662).
5. **Prediction**: Delegates the actual location computation to the underlying Keras model via `self.locator_model_.predict(X, batch_size=self.batch_size, verbose=self.verbose)` (line 664).
6. **Formatting**: Casts the resulting floating-point locations to `int` and returns them (line 668).

L4 CORRECT MINIMAL USAGE
```python
import numpy as np

try:
    from tslearn.shapelets import LearningShapelets
    from tslearn.utils import to_time_series_dataset
    HAS_KERAS = True
except ImportError as e:
    HAS_KERAS = False
    print(f"Skipping execution: {e}")

if HAS_KERAS:
    # 1. Prepare 3D time-series data
    X_raw = [[1, 2, 3, 4, 5], [3, 2, 1, 0, 0]]
    X = to_time_series_dataset(X_raw)
    y = [0, 1]

    # 2. Initialize and fit the LearningShapelets estimator
    clf = LearningShapelets(
        n_shapelets_per_size={2: 1},
        max_iter=1,
        verbose=0,
        random_state=0
    )
    clf.fit(X, y)

    # 3. Locate the shapelets in the time series
    locations = clf.locate(X)

    assert locations.shape == (2, 1), f"Expected shape (2, 1), got {locations.shape}"
    assert locations.dtype == int, f"Expected dtype int, got {locations.dtype}"
    print(f"Shapelet locations computed successfully:\n{locations}")
```

L5 FAILURE FORENSICS
- **`[fail/infra] missing module/import: No module named 'keras'`**: This failure occurred because the `LearningShapelets` class heavily relies on the Keras deep learning library to construct its auxiliary models (e.g., `self.locator_model_ = Model(...)` at line 762). The test harness environment does not have `keras` installed, causing an immediate `ImportError` when the module is imported or when the class attempts to initialize Keras components.

L6 SELF-ASSESSMENT
- **Inferences**: 
  - I inferred that `self.locator_model_` is specifically a Keras `Model` object based on the `predict(..., batch_size=..., verbose=...)` signature and the `_build_auxiliary_models` method using `Model(inputs=..., outputs=...)`.
  - I inferred that the `ImportError` for `keras` is unavoidable without skipping the test, as `tslearn.shapelets` requires it to function.
- **Information needed for certainty**: Verification of the exact Keras version compatibility expected by this specific version of `tslearn` (e.g., standalone `keras` vs `tensorflow.keras`).
- **Confidence Scores**:
  - L2 (Contract): 10/10. The types and shapes are explicitly documented in the docstring and enforced in the source code.
  - L3 (Mechanics): 10/10. The source code for `locate` is provided in full and clearly shows the sequence of validation, preprocessing, and prediction steps.
  - L4 (Usage): 9/10. The usage follows standard scikit-learn/tslearn patterns, though its actual execution depends entirely on the presence of the optional `keras` dependency which is missing in the harness.