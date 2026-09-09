# tslearn full235 A1 failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/docs/eval/A1/comprehension.json`
- Experiment fingerprint: `d56d5a544a2ba19ef8b88ef7fd390e3c24bea013165e493964ac20e1e16c3cea`
- APIs: 235
- Failures: 106

## Failure categories

- `infra`: 60
- `no-correctness-check`: 1
- `runtime`: 44
- `unknown`: 1

## Per-function evidence

### `Backend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:55`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tslearn.backends'`

### `BaseModelPackage`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:78`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 35.1
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'DummyModel' object has no attribute 'to_dict'`

### `GlobalArgminPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:97`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `GlobalMinPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:66`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 14.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `KNeighborsTimeSeriesMixin`

- Category: `infra`
- Source definition: `tslearn/tslearn/neighbors/neighbors.py:28`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 43.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'KNeighborsTimeSeriesMixin' from 'tslearn.neighbors' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/neighbors/`

### `LearningShapelets`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:290`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 14.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `LocalSquaredDistanceLayer`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:167`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 27.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `NumPyBackend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:22`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 9.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `NumPyLinalg`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:126`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tslearn.backends'`

### `NumPyTesting`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:139`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tslearn.backends'`

### `PatchingLayer`

- Category: `unknown`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:128`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 365.9
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `__CHECK__ PatchingLayer not found or optional dependency missing`

### `PyTorchBackend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:37`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 10.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tslearn.backends'`

### `PyTorchRandom`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:243`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'PyTorchRandom' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `PyTorchTesting`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:263`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'PyTorchTesting' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `SoftDTW`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1068`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 331.4
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: type object 'SoftDTW' has no attribute 'apply'`

### `SquaredEuclidean`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1176`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 330.6
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`

### `TimeSeriesCentroidBasedClusteringMixin`

- Category: `runtime`
- Source definition: `tslearn/tslearn/clustering/utils.py:225`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 26.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result.`

### `TimeSeriesDBSCAN`

- Category: `runtime`
- Source definition: `tslearn/tslearn/clustering/dbscan.py:19`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 384.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: TimeSeriesDBSCAN.__init__() got an unexpected keyword argument 'min_samples'`

### `TimeSeriesMixin`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:53`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 318.3
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result of TimeSeriesMixin.`

### `TimeSeriesSVMMixin`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:20`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.7
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'TimeSeriesSVC' object has no attribute 'support_vectors_time_series_'`

### `TsLearnTags`

- Category: `infra`
- Source definition: `tslearn/tslearn/bases/bases.py:29`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'TsLearnTags' from 'tslearn.bases' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/bases/__init__.py)`

### `accumulated_matrix`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/_dtw.py:286`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 314.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract for accumulated_matrix is insufficient to verify the result.`

### `accumulated_matrix_from_dist_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:456`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 382.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/me`

### `baseline_accuracy`

- Category: `runtime`
- Source definition: `tslearn/tslearn/datasets/ucr_uea.py:121`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 38.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Unexpected baseline accuracy: {'Trace': {'NB': 0.8, 'C45': 0.79, 'SVML': 0.73, 'SVMQ': 0.82, 'BN': 0.82, 'RandF': 0.78, 'RotF': 0.93, 'MLP': 0.84, 'Euclidean_1NN': 0.76, 'DTW_R1_1NN': 1.0, 'DTW_Rn_1NN': 0.99, 'DDTW_R1_1NN': 1.0, 'DDTW_Rn_1NN': 0.99, 'ERP_1NN': 0.95, 'LCSS_1NN': 0.97, 'MSM_1NN': 0.93, 'TWE_1NN': 0.99, 'WDDTW_1NN': 1.0, 'WDTW_1NN': 1.0, 'DD_DTW': 1.0, 'DTD_C': 0.99, 'DTW_F': 1.0, 'ST': 1.0, 'LS': 1.0, 'FS': 1.0, 'BoP': 0.97, 'SAXVSM': 1.0, 'BOSS': 1.0, 'TSF': 0.99, 'TSBF': 0.98, 'LPS': 0.98, 'ACF': 1.0, 'PS': 0.95, 'EE': 0.99, 'COTE': 1.0, 'CID_DTW': 0.99}}`

### `build`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:188`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 24.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `cache_all`

- Category: `runtime`
- Source definition: `tslearn/tslearn/datasets/ucr_uea.py:376`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 27.1
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: <tslearn.datasets.ucr_uea.UCR_UEA_datasets object at 0x104204f70> does not have the attribute 'cache_dataset'`

### `call`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:89`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 35.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `cast`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/backend.py:91`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 42.9
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: instantiate_backend() got an unexpected keyword argument 'backend'`

### `cdist_normalized_cc`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/cycc.py:54`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 23.8
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: not enough arguments: expected 5, got 2`

### `cdist_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/sax.py:10`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 380.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: cdist_sax contract is insufficient to verify the result or signature mismatch: cdist_sax() got an unexpected keyword argument 'n_segments'`

### `check_dims`

- Category: `runtime`
- Source definition: `tslearn/tslearn/utils/utils.py:65`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 1D series to be expanded to 3D, got 1D`

### `check_keras_backend`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/__init__.py:12`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 375.8
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AssertionError: check_keras_backend failed: module 'tslearn.utils' has no attribute 'check_keras_backend'`

### `compute_mask`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/_masks.py:199`
- Reached codebase frames: `tslearn/tslearn/metrics/_masks.py:288`
- Attempts / wall seconds: 1 / 390.0
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: object of type 'NoneType' has no len()`

### `compute_output_shape`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:86`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `compute_var`

- Category: `infra`
- Source definition: `tslearn/tslearn/forecasting/_arima.py:21`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 349.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'compute_var' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)`

### `copy`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:94`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.6
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: module 'tslearn.backend.numpy_backend' has no attribute 'copy'`

### `ctw`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/ctw.py:200`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 328.0
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: 'float' object is not subscriptable`

### `cydist_1d_sax`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:135`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 384.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'cydist_1d_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)`

### `cydist_sax`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:38`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 364.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'cydist_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)`

### `cyslopes`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:107`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 35.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'cyslopes' from 'tslearn.piecewise' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/piecewise/__init__.py)`

### `distance`

- Category: `runtime`
- Source definition: `tslearn/tslearn/piecewise/piecewise.py:219`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 396.6
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'MatrixProfile' object has no attribute 'distance'`

### `distance_1d_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/piecewise/piecewise.py:726`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 600.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Documentation for distance_1d_sax is missing; cannot verify contract.`

### `distance_sax`

- Category: `runtime`
- Source definition: `tslearn/tslearn/piecewise/piecewise.py:444`
- Reached codebase frames: `tslearn/tslearn/metrics/cysax.py:65; tslearn/tslearn/piecewise/piecewise.py:466`
- Attempts / wall seconds: 1 / 31.6
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `TypingError: Failed in nopython mode pipeline (step: nopython frontend)`

### `dtw_barycenter_averaging_one_init`

- Category: `infra`
- Source definition: `tslearn/tslearn/barycenters/dba.py:621`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 24.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'dtw_barycenter_averaging_one_init' from 'tslearn.barycenters' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/`

### `dual_coef_`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:29`
- Reached codebase frames: `tslearn/tslearn/svm/svm.py:328`
- Attempts / wall seconds: 1 / 9.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `InvalidParameterError: The 'kernel' parameter of SVC must be a str among {'precomputed', 'linear', 'sigmoid', 'rbf', 'poly'} or a callable. Got 'euclidean' instead.`

### `early_classification_cost`

- Category: `infra`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:517`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 41.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'early_classification_cost' from 'tslearn.early_classification' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn`

### `fix_force_all_finite_warning`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/utils.py:24`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 345.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__ini`

### `from_cesium_dataset`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/cast.py:713`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 11.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'cesium'`

### `from_numpy`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:98`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 354.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `gamma_soft_dtw`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:474`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 369.4
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Documented contract is insufficient to verify gamma_soft_dtw: gamma_soft_dtw() got an unexpected keyword argument 'gamma'`

### `get_backend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:84`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 327.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `get_config`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:160`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 23.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'get_config' from 'tslearn' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/__init__.py)`

### `get_early_predict_generator`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:627`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 395.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Contract is insufficient to verify the result.`

### `get_early_predict_proba_generator`

- Category: `runtime`
- Source definition: `tslearn/tslearn/early_classification/early_classification.py:677`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 377.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract is insufficient to verify the result of get_early_predict_proba_generator.`

### `get_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:828`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `grabocka_params_to_shapelet_size_dict`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:235`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 18.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `in_file_string_replace`

- Category: `infra`
- Source definition: `tslearn/tslearn/datasets/datasets.py:57`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'in_file_string_replace' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__init__.py`

### `intercept_`

- Category: `runtime`
- Source definition: `tslearn/tslearn/svm/svm.py:39`
- Reached codebase frames: `tslearn/tslearn/svm/svm.py:328`
- Attempts / wall seconds: 1 / 17.8
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `InvalidParameterError: The 'kernel' parameter of SVC must be a str among {'precomputed', 'linear', 'sigmoid', 'rbf', 'poly'} or a callable. Got 'euclidean' instead.`

### `inv_transform_1d_sax`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:189`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 24.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'inv_transform_1d_sax' from 'tslearn.piecewise' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/piecewise/__ini`

### `inv_transform_paa`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:11`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 15.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'inv_transform_paa' from 'tslearn.piecewise' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/piecewise/__init__`

### `inv_transform_sax`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cysax.py:78`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 36.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'inv_transform_sax' from 'tslearn.piecewise' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/piecewise/__init__`

### `is_array`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:102`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 29.0
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: module 'tslearn.backend.numpy_backend' has no attribute 'is_array'`

### `is_float`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:106`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 350.5
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected float array to be identified as float`

### `is_float32`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:110`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 372.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'is_float32' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__init__.py)`

### `is_float64`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:114`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `is_numpy`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/backend.py:77`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 407.2
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: 'bool' object is not callable`

### `is_pytorch`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:81`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 314.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'is_pytorch' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `iscomplex`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:153`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 363.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'iscomplex' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `itakura_mask`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/_masks.py:154`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.1
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected (0,0) to be valid (0.0)`

### `jacobian_product`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/softdtw_variants.py:1218`
- Reached codebase frames: `tslearn/tslearn/backend/backend.py:74`
- Attempts / wall seconds: 1 / 368.8
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: The documented contract for jacobian_product is insufficient to verify the result.`

### `lcss_accumulated_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:2270`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'lcss_accumulated_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init`

### `lcss_accumulated_matrix_from_dist_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:2865`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 23.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'lcss_accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslea`

### `list_cached_datasets`

- Category: `runtime`
- Source definition: `tslearn/tslearn/datasets/ucr_uea.py:236`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 25.0
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `AssertionError: The documented contract is insufficient to verify the result without network access or a configurable cache directory.`

### `load_dict`

- Category: `infra`
- Source definition: `tslearn/tslearn/hdftools/hdftools.py:118`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'save_dict' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__init__.py)`

### `locate`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:625`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 10.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `mase`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/performance.py:153`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 401.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'mase' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)`

### `mse`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/performance.py:83`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 392.4
- Diagnosis: Missing or incorrectly bound repository fixture/output directory.
- Error: `AssertionError: The documented contract for 'mse' is insufficient to verify the result or the function does not exist in the expected location.`

### `n_iter_`

- Category: `infra`
- Source definition: `tslearn/tslearn/svm/svm.py:279`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 15.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `njit_accumulated_matrix`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:74`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 25.4
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: not enough arguments: expected 3, got 1`

### `njit_accumulated_matrix_from_dist_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:426`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 19.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'njit_accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslea`

### `njit_lcss_accumulated_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:2233`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 34.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tslearn.metrics.lcss'`

### `njit_lcss_accumulated_matrix_from_dist_matrix`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:2831`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 30.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'njit_lcss_accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/`

### `njit_sakoe_chiba_mask`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/dtw_variants.py:1487`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 329.0
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 12 invalid cells, got 0`

### `normal`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:250`
- Reached codebase frames: `tslearn/tslearn/backend/backend.py:74`
- Attempts / wall seconds: 1 / 377.5
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'NumPyBackend' object has no attribute 'normal'`

### `normalized_cc`

- Category: `infra`
- Source definition: `tslearn/tslearn/metrics/cycc.py:10`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 26.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'normalized_cc' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)`

### `partial_fit`

- Category: `no-correctness-check`
- Source definition: `tslearn/tslearn/neural_network/neural_network.py:62`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 393.7
- Diagnosis: Snippet ran but did not emit the required deterministic correctness witness.
- Error: `ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ partial_fit " + <witness>).`

### `pdist`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:193`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 26.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `sakoe_chiba_mask`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/_masks.py:42`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 17.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected 13 valid cells, got 25`

### `save_dict`

- Category: `infra`
- Source definition: `tslearn/tslearn/hdftools/hdftools.py:8`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 393.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'save_dict' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__init__.py)`

### `select_backend`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/backend.py:31`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 12.7
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: select_backend() takes 1 positional argument but 2 were given`

### `set_backend`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/backend.py:87`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 27.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'set_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `set_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:866`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `shapelets_`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:441`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 15.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `shapelets_as_time_series_`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:455`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 16.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `sigma_gak`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/_gak.py:20`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 16.3
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Scaling invariant failed: 22.33320650161996 != 2 * 11.12043399697152`

### `to_cesium_dataset`

- Category: `infra`
- Source definition: `tslearn/tslearn/utils/cast.py:655`
- Reached codebase frames: `tslearn/tslearn/utils/cast.py:695; tslearn/tslearn/utils/cast.py:697`
- Attempts / wall seconds: 1 / 13.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: Conversion from/to cesium cannot be performed if cesium is not installed.`

### `to_hdf5`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:210`
- Reached codebase frames: `tslearn/tslearn/bases/bases.py:229; tslearn/tslearn/hdftools/hdftools.py:42`
- Attempts / wall seconds: 1 / 20.9
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `FileExistsError:`

### `to_json`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:259`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 13.0
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AssertionError: n_clusters not found in serialized JSON`

### `to_pickle`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:307`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.6
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'dict' object has no attribute 'n_clusters'`

### `transform`

- Category: `infra`
- Source definition: `tslearn/tslearn/preprocessing/_synchronizer.py:78`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 16.3
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `tril`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:217`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 29.0
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `tril_indices`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:221`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 21.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `triu`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:228`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 31.1
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `triu_indices`

- Category: `infra`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:232`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 33.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`

### `uniform`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/pytorch_backend.py:256`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 22.6
- Diagnosis: Wrong API owner/import/member name, or a symbol absent from the pinned version.
- Error: `AttributeError: 'NumPyBackend' object has no attribute 'uniform'`

### `y_shifted_sbd_vec`

- Category: `runtime`
- Source definition: `tslearn/tslearn/metrics/cycc.py:99`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 14.5
- Diagnosis: Signature, receiver, argument-type, or return-type mismatch.
- Error: `TypeError: not enough arguments: expected 4, got 2`
