# tslearn full235 A2 failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/docs/eval/A2/comprehension.json`
- Experiment fingerprint: `366e0c64f58ebac296ba554d7ae3f9d9ca2a6b85bf15faf250291bc1c2198bb9`
- APIs: 235
- Failures: 60

## Failure categories

- `infra`: 28
- `runtime`: 32

## Per-function evidence

### `BaseModelPackage`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:78`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 10.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result non-tautologically.`

### `EmptyClusterError`

- Category: `runtime`
- Source definition: `tslearn/tslearn/clustering/utils.py:17`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 6.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError:`

### `GlobalArgminPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:97`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 9.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `GlobalMinPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:66`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 10.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `KNeighborsTimeSeriesMixin`

- Category: `infra`
- Source definition: `tslearn/tslearn/neighbors/neighbors.py:28`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 34.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'KNeighborsTimeSeriesMixin' from 'tslearn.neighbors' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/neighbors/`

### `LearningShapelets`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:290`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 10.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `LocalSquaredDistanceLayer`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:167`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 24.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `NonMyopicEarlyClassifier`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:18`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Delays should be at least min_t (2)`

### `NumPyBackend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:22`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `NumPyRandom`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:132`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 16.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result`

### `PatchingLayer`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:128`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 29.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `PyTorchBackend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:37`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 14.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'PyTorchBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `PyTorchRandom`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:243`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result of PyTorchRandom.`

### `PyTorchTesting`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:263`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 9.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result.`

### `SoftDTW`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1068`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.8
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: SoftDTW.__init__() missing 1 required positional argument: 'D'`

### `SquaredEuclidean`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1176`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.5
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`

### `TimeSeriesSVMMixin`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:20`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 23.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result non-tautologically as it does not specify any methods or attributes provided by the mixin.`

### `TsLearnTags`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:29`
- Reached codebase frames: `tslearn/tslearn/bases/bases.py:33`
- Attempts / wall seconds: 1 / 20.3
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: Tags.__init__() missing 2 required positional arguments: 'estimator_type' and 'target_tags'`

### `build`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:188`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 28.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `call`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:89`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `cdist_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/sax.py:10`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 119.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: SymbolicAggregateApproximation.__init__() got an unexpected keyword argument 'alphabet_size'`

### `check_keras_backend`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/__init__.py:12`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the side effect of check_keras_backend`

### `compute`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1111`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 395.8
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: SoftDTW.__init__() got an unexpected keyword argument 'ts1'`

### `compute_output_shape`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:86`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 21.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `cydist_1d_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/cysax.py:135`
- Reached codebase frames: `tslearn/tslearn/metrics/cysax.py:176`
- Attempts / wall seconds: 1 / 58.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`

### `decision_function`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:352`
- Reached codebase frames: `tslearn/tslearn/svm/svm.py:328`
- Attempts / wall seconds: 1 / 13.2
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `InvalidParameterError: The 'kernel' parameter of SVC must be a str among {'precomputed', 'linear', 'sigmoid', 'rbf', 'poly'} or a callable. Got 'euclidean' instead.`

### `dtw_barycenter_averaging_one_init`

- Category: `infra`
- Source definition: `tslearn/tslearn/barycenters/dba.py:621`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'dtw_barycenter_averaging_one_init' from 'tslearn.barycenters' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/`

### `early_predict_proba`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:600`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected probabilities shape (8, 4), got (8, 3)`

### `extract_from_zip_url`

- Category: `runtime`
- Source definition: `tslearn/tslearn/datasets/datasets.py:16`
- Reached codebase frames: `tslearn/tslearn/datasets/datasets.py:39`
- Attempts / wall seconds: 1 / 10.4
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `URLError: <urlopen error [Errno 61] Connection refused>`

### `fix_force_all_finite_warning`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/utils.py:24`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/utils/__ini`

### `from_cesium_dataset`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/cast.py:713`
- Reached codebase frames: `tslearn/tslearn/utils/cast.py:695; tslearn/tslearn/utils/cast.py:697`
- Attempts / wall seconds: 1 / 15.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`

### `from_json`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:273`
- Reached codebase frames: `tslearn/tslearn/bases/bases.py:269; tslearn/tslearn/bases/bases.py:121; tslearn/tslearn/clustering/kmeans.py:630`
- Attempts / wall seconds: 1 / 9.8
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `NotFittedError: This TimeSeriesKMeans instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.`

### `from_pickle`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:321`
- Reached codebase frames: `tslearn/tslearn/bases/bases.py:335; tslearn/tslearn/bases/bases.py:205`
- Attempts / wall seconds: 1 / 12.4
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: 'TimeSeriesKMeans' object is not subscriptable`

### `get_backend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:84`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 5.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `get_cluster_probas`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:215`
- Reached codebase frames: `tslearn/tslearn/early_classification/early_classification.py:172`
- Attempts / wall seconds: 1 / 14.2
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: The least populated class in y has only 1 member, which is too few. The minimum number of groups for any class cannot be less than 2.`

### `get_config`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:160`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 28.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `get_early_predict_proba_generator`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:677`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 25.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected probas shape (1, 4), got (1, 3)`

### `get_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:828`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `grabocka_params_to_shapelet_size_dict`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:235`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 13.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `inv_transform_1d_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/cysax.py:189`
- Reached codebase frames: `tslearn/tslearn/metrics/cysax.py:219`
- Attempts / wall seconds: 1 / 24.8
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`

### `inv_transform_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/cysax.py:78`
- Reached codebase frames: `tslearn/tslearn/metrics/cysax.py:100`
- Attempts / wall seconds: 1 / 18.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`

### `inverse_transform`

- Category: `infra`
- Source definition: `tslearn/tslearn/piecewise/piecewise.py:242`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'PAA' from 'tslearn.piecewise' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/piecewise/__init__.py)`

### `is_float`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:106`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.9
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected float array to be recognized as float.`

### `is_float32`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:110`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 8.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected True for float32 array`

### `is_float64`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:114`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 9.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected True for float64 array`

### `iscomplex`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:153`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 7.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'iscomplex' from 'tslearn.backend.pytorch_backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/pyto`

### `jacobian_product`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1218`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 384.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'squared_distance_profile' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/metrics/__ini`

### `lcss_accumulated_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:2270`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 10.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'lcss_accumulated_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/metrics/__init`

### `locate`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:625`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 9.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `normal`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:250`
- Reached codebase frames: `tslearn/tslearn/backend/backend.py:74`
- Attempts / wall seconds: 1 / 13.0
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'NumPyBackend' object has no attribute 'normal'`

### `pairwise_distances`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:177`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'pairwise_distances' from 'tslearn.backend.pytorch_backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/bac`

### `predict_class_and_earliness`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:399`
- Reached codebase frames: `tslearn/tslearn/early_classification/early_classification.py:190`
- Attempts / wall seconds: 1 / 19.0
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `ValueError: Found array with dim 3, while dim <= 2 is required by DecisionTreeClassifier.`

### `select_backend`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/backend.py:31`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 7.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected NumpyBackend, got NumPyBackend`

### `set_backend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:87`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `set_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:866`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 14.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `shapelets_`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:441`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 14.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `support_vectors_`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:285`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.5
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'list' object has no attribute 'ndim'`

### `to_cesium_dataset`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/cast.py:655`
- Reached codebase frames: `tslearn/tslearn/utils/cast.py:695; tslearn/tslearn/utils/cast.py:697`
- Attempts / wall seconds: 1 / 10.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`

### `to_pickle`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:307`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.8
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'dict' object has no attribute 'n_clusters'`

### `uniform`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:256`
- Reached codebase frames: `tslearn/tslearn/backend/backend.py:74`
- Attempts / wall seconds: 1 / 8.9
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'NumPyBackend' object has no attribute 'uniform'`
