# Fix-loop report — aideal_run_ra_ezy6l

_Generated 2026-09-08 21:35 by `aideal fix-report`._

- kind: **comprehension**  ·  run_id: `20260909-042925Z`  ·  models: audience=google:gemini-3.1-pro-preview, fixer=google:gemini-3.1-pro-preview
- pass **129/235** raw (54.9%)  ·  scored **129/175** (73.7%) after excluding 60 infra
- wall 0.1 h  ·  tokens in 1,323 / out 63,033 ·  llm calls 1  ·  max_fix_rounds 0
- pass-by-round: r0:129  ·  **0 rescued by the fix loop** (pass@0 = 129)

## Chronic failures across runs (28)

_Failed in ≥2 recorded runs with the same error signature at least twice — candidates for doc-repair with deep-dive, exclusion, or a harness/fixture fix rather than more snippet retries._

| API | runs failed | same-sig runs | distinct sigs | first seen |
|---|---|---|---|---|
| `from_numpy` | 6 | 4 | 3 | 2026-09-08 |
| `PatchingLayer` | 5 | 4 | 2 | 2026-09-07 |
| `TimeSeriesDBSCAN` | 5 | 4 | 2 | 2026-09-07 |
| `accumulated_matrix` | 5 | 4 | 2 | 2026-09-07 |
| `accumulated_matrix_from_dist_matrix` | 5 | 4 | 2 | 2026-09-07 |
| `cdist_sax` | 5 | 4 | 2 | 2026-09-07 |
| `check_keras_backend` | 5 | 4 | 2 | 2026-09-07 |
| `compute_mask` | 5 | 4 | 2 | 2026-09-08 |
| `compute_var` | 5 | 3 | 3 | 2026-09-08 |
| `cydist_1d_sax` | 5 | 4 | 2 | 2026-09-08 |
| `cydist_sax` | 5 | 4 | 2 | 2026-09-08 |
| `distance` | 5 | 4 | 2 | 2026-09-08 |
| `gamma_soft_dtw` | 5 | 4 | 2 | 2026-09-08 |
| `get_early_predict_generator` | 5 | 4 | 2 | 2026-09-08 |
| `get_early_predict_proba_generator` | 5 | 4 | 2 | 2026-09-08 |
| `is_float` | 5 | 4 | 2 | 2026-09-08 |
| `is_float32` | 5 | 4 | 2 | 2026-09-08 |
| `is_numpy` | 5 | 4 | 2 | 2026-09-08 |
| `iscomplex` | 5 | 4 | 2 | 2026-09-08 |
| `jacobian_product` | 5 | 4 | 2 | 2026-09-08 |
| `mase` | 5 | 4 | 2 | 2026-09-08 |
| `mse` | 5 | 4 | 2 | 2026-09-08 |
| `normal` | 5 | 3 | 3 | 2026-09-08 |
| `partial_fit` | 5 | 4 | 2 | 2026-09-08 |
| `save_dict` | 5 | 4 | 2 | 2026-09-08 |
| `njit_sakoe_chiba_mask` | 4 | 3 | 2 | 2026-09-08 |
| `baseline_accuracy` | 3 | 2 | 2 | 2026-09-07 |
| `call` | 3 | 2 | 2 | 2026-09-07 |

## Failure clusters (one issue, many APIs)

_Current failures grouped by normalized error signature (identifiers masked). Fixing the top cluster's root cause pays across all its APIs._

- **45x** [infra] resumed: fail
  - `Backend`, `GlobalArgminPooling1D`, `GlobalMinPooling1D`, `KNeighborsTimeSeriesMixin`, `LearningShapelets`, `LocalSquaredDistanceLayer`, `NumPyBackend`, `NumPyLinalg`, `NumPyTesting`, `PyTorchBackend`, `PyTorchRandom`, `PyTorchTesting`, `TsLearnTags`, `build` …
- **25x** [runtime] resumed: fail
  - `BaseModelPackage`, `SoftDTW`, `TimeSeriesCentroidBasedClusteringMixin`, `TimeSeriesMixin`, `TimeSeriesSVMMixin`, `cache_all`, `cdist_normalized_cc`, `check_dims`, `copy`, `ctw`, `distance_1d_sax`, `distance_sax`, `dual_coef_`, `intercept_` …
- **9x** [infra] missing module/import: cannot import name <name> from <name> (<path>)
  - `compute_var`, `cydist_1d_sax`, `cydist_sax`, `from_numpy`, `get_backend`, `is_float32`, `iscomplex`, `mase`, `save_dict`
- **4x** [infra] missing module/import: No module named <name>
  - `call`, `njit_lcss_accumulated_matrix`, `set_weights`, `shapelets_`
- **2x** [infra] missing module/import: cannot import name <name> from <name> (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_
  - `accumulated_matrix_from_dist_matrix`, `fix_force_all_finite_warning`
- **2x** [runtime] AttributeError: <name> object has no attribute <name>
  - `distance`, `normal`
- **1x** [unknown] __CHECK__ PatchingLayer not found or optional dependency missing
  - `PatchingLayer`
- **1x** [runtime] TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: <name> and <name>
  - `SquaredEuclidean`
- **1x** [runtime] TypeError: TimeSeriesDBSCAN.__init__() got an unexpected keyword argument <name>
  - `TimeSeriesDBSCAN`
- **1x** [runtime] AssertionError: The documented contract for accumulated_matrix is insufficient to verify the result.
  - `accumulated_matrix`
- **1x** [runtime] AssertionError: Unexpected baseline accuracy: {<name>: {<name>: 0.8, <name>: 0.79, <name>: 0.73, <name>: 0.82, <name>: 0.82, <name>: 0.78, <
  - `baseline_accuracy`
- **1x** [runtime] TypeError: instantiate_backend() got an unexpected keyword argument <name>
  - `cast`

## Why each API fails (106 failing)

### `Backend` — infra

- canonical source: `tslearn/tslearn/backend/backend.py:55`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `BaseModelPackage` — runtime

- canonical source: `tslearn/tslearn/bases/bases.py:78`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `GlobalArgminPooling1D` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:97`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `GlobalMinPooling1D` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:66`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `KNeighborsTimeSeriesMixin` — infra

- canonical source: `tslearn/tslearn/neighbors/neighbors.py:28`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `LearningShapelets` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:290` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `LocalSquaredDistanceLayer` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:167`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `NumPyBackend` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:22`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `NumPyLinalg` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:126`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `NumPyTesting` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:139`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `PatchingLayer` — unknown

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:128`
- last error: __CHECK__ PatchingLayer not found or optional dependency missing
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [unknown] __CHECK__ PatchingLayer not found or optional dependency missing

### `PyTorchBackend` — infra

- canonical source: `tslearn/tslearn/backend/pytorch_backend.py:37`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `PyTorchRandom` — infra

- canonical source: `tslearn/tslearn/backend/pytorch_backend.py:243`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `PyTorchTesting` — infra

- canonical source: `tslearn/tslearn/backend/pytorch_backend.py:263`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `SoftDTW` — runtime

- canonical source: `tslearn/tslearn/metrics/softdtw_variants.py:1068`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `SquaredEuclidean` — runtime

- canonical source: `tslearn/tslearn/metrics/softdtw_variants.py:1176`
- last error: TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'

### `TimeSeriesCentroidBasedClusteringMixin` — runtime

- canonical source: `tslearn/tslearn/clustering/utils.py:225`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `TimeSeriesDBSCAN` — runtime

- canonical source: `tslearn/tslearn/clustering/dbscan.py:19`
- last error: TypeError: TimeSeriesDBSCAN.__init__() got an unexpected keyword argument 'min_samples'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] TypeError: TimeSeriesDBSCAN.__init__() got an unexpected keyword argument 'min_samples'

### `TimeSeriesMixin` — runtime

- canonical source: `tslearn/tslearn/bases/bases.py:53`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `TimeSeriesSVMMixin` — runtime

- canonical source: `tslearn/tslearn/svm/svm.py:20`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `TsLearnTags` — infra

- canonical source: `tslearn/tslearn/bases/bases.py:29`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `accumulated_matrix` — runtime

- canonical source: `tslearn/tslearn/metrics/_dtw.py:286`
- last error: AssertionError: The documented contract for accumulated_matrix is insufficient to verify the result.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: The documented contract for accumulated_matrix is insufficient to verify the result.

### `accumulated_matrix_from_dist_matrix` — infra

- canonical source: `tslearn/tslearn/metrics/dtw_variants.py:456`
- last error: missing module/import: cannot import name 'accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/me
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'accumulated_matrix_from_dist_matrix' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/c

### `baseline_accuracy` — runtime

- canonical source: `tslearn/tslearn/datasets/ucr_uea.py:121`
- last error: AssertionError: Unexpected baseline accuracy: {'Trace': {'NB': 0.8, 'C45': 0.79, 'SVML': 0.73, 'SVMQ': 0.82, 'BN': 0.82, 'RandF': 0.78, 'RotF': 0.93, 'MLP': 0.84, 'Euclidean_1NN': 0.76, 'DTW_R1_1NN': 1.0, 'DTW_Rn_1NN': 0.99, 'DDTW_R1_1NN': 1.0, 'DDTW_Rn_1NN': 0.99, 'ERP_1NN': 0.95, 'LCSS_1NN': 0.97,
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Unexpected baseline accuracy: {'Trace': {'NB': 0.8, 'C45': 0.79, 'SVML': 0.73, 'SVMQ': 0.82, 'BN': 0.82, 'RandF': 0.78, 'RotF': 0.93, 

### `build` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:188` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `cache_all` — runtime

- canonical source: `tslearn/tslearn/datasets/ucr_uea.py:376`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `call` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:89`
- last error: missing module/import: No module named 'tensorflow'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: No module named 'tensorflow'

### `cast` — runtime

- canonical source: `tslearn/tslearn/backend/backend.py:91`
- last error: TypeError: instantiate_backend() got an unexpected keyword argument 'backend'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] TypeError: instantiate_backend() got an unexpected keyword argument 'backend'

### `cdist_normalized_cc` — runtime

- canonical source: `tslearn/tslearn/metrics/cycc.py:54`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `cdist_sax` — runtime

- canonical source: `tslearn/tslearn/metrics/sax.py:10`
- last error: AssertionError: cdist_sax contract is insufficient to verify the result or signature mismatch: cdist_sax() got an unexpected keyword argument 'n_segments'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: cdist_sax contract is insufficient to verify the result or signature mismatch: cdist_sax() got an unexpected keyword argument 'n_segme

### `check_dims` — runtime

- canonical source: `tslearn/tslearn/utils/utils.py:65`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `check_keras_backend` — runtime

- canonical source: `tslearn/tslearn/backend/__init__.py:12`
- last error: AssertionError: check_keras_backend failed: module 'tslearn.utils' has no attribute 'check_keras_backend'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: check_keras_backend failed: module 'tslearn.utils' has no attribute 'check_keras_backend'

### `compute_mask` — runtime

- canonical source: `tslearn/tslearn/metrics/_masks.py:199` · reached: `tslearn/tslearn/metrics/_masks.py:288`
- last error: TypeError: object of type 'NoneType' has no len()
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] TypeError: object of type 'NoneType' has no len()

### `compute_output_shape` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:86` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `compute_var` — infra

- canonical source: `tslearn/tslearn/forecasting/_arima.py:21`
- last error: missing module/import: cannot import name 'compute_var' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'compute_var' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_

### `copy` — runtime

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:94`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `ctw` — runtime

- canonical source: `tslearn/tslearn/metrics/ctw.py:200`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `cydist_1d_sax` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:135`
- last error: missing module/import: cannot import name 'cydist_1d_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'cydist_1d_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslear

### `cydist_sax` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:38`
- last error: missing module/import: cannot import name 'cydist_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'cydist_sax' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_f

### `cyslopes` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:107`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `distance` — runtime

- canonical source: `tslearn/tslearn/piecewise/piecewise.py:219`
- last error: AttributeError: 'MatrixProfile' object has no attribute 'distance'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AttributeError: 'MatrixProfile' object has no attribute 'distance'

### `distance_1d_sax` — runtime

- canonical source: `tslearn/tslearn/piecewise/piecewise.py:726`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `distance_sax` — runtime

- canonical source: `tslearn/tslearn/piecewise/piecewise.py:444` · reached: `tslearn/tslearn/metrics/cysax.py:65`, `tslearn/tslearn/piecewise/piecewise.py:466`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `dtw_barycenter_averaging_one_init` — infra

- canonical source: `tslearn/tslearn/barycenters/dba.py:621`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `dual_coef_` — runtime

- canonical source: `tslearn/tslearn/svm/svm.py:29` · reached: `tslearn/tslearn/svm/svm.py:328`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `early_classification_cost` — infra

- canonical source: `tslearn/tslearn/early_classification/early_classification.py:517`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `fix_force_all_finite_warning` — infra

- canonical source: `tslearn/tslearn/utils/utils.py:24`
- last error: missing module/import: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__ini
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'fix_force_all_finite_warning' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI

### `from_cesium_dataset` — infra

- canonical source: `tslearn/tslearn/utils/cast.py:713`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `from_numpy` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:98`
- last error: missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_

### `gamma_soft_dtw` — runtime

- canonical source: `tslearn/tslearn/metrics/softdtw_variants.py:474`
- last error: AssertionError: Documented contract is insufficient to verify gamma_soft_dtw: gamma_soft_dtw() got an unexpected keyword argument 'gamma'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Documented contract is insufficient to verify gamma_soft_dtw: gamma_soft_dtw() got an unexpected keyword argument 'gamma'

### `get_backend` — infra

- canonical source: `tslearn/tslearn/backend/backend.py:84`
- last error: missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'get_backend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_

### `get_config` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:160`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `get_early_predict_generator` — runtime

- canonical source: `tslearn/tslearn/early_classification/early_classification.py:627`
- last error: AssertionError: Contract is insufficient to verify the result.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Contract is insufficient to verify the result.

### `get_early_predict_proba_generator` — runtime

- canonical source: `tslearn/tslearn/early_classification/early_classification.py:677`
- last error: AssertionError: The documented contract is insufficient to verify the result of get_early_predict_proba_generator.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: The documented contract is insufficient to verify the result of get_early_predict_proba_generator.

### `get_weights` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:828` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `grabocka_params_to_shapelet_size_dict` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:235` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `in_file_string_replace` — infra

- canonical source: `tslearn/tslearn/datasets/datasets.py:57`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `intercept_` — runtime

- canonical source: `tslearn/tslearn/svm/svm.py:39` · reached: `tslearn/tslearn/svm/svm.py:328`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `inv_transform_1d_sax` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:189`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `inv_transform_paa` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:11`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `inv_transform_sax` — infra

- canonical source: `tslearn/tslearn/metrics/cysax.py:78`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `is_array` — runtime

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:102`
- last error: AttributeError: module 'tslearn.backend.numpy_backend' has no attribute 'is_array'
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AttributeError: module 'tslearn.backend.numpy_backend' has no attribute 'is_array'

### `is_float` — runtime

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:106`
- last error: AssertionError: Expected float array to be identified as float
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: Expected float array to be identified as float

### `is_float32` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:110`
- last error: missing module/import: cannot import name 'is_float32' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/utils/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'is_float32' from 'tslearn.utils' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_ful

### `is_float64` — infra

- canonical source: `tslearn/tslearn/backend/numpy_backend.py:114`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `is_numpy` — runtime

- canonical source: `tslearn/tslearn/backend/backend.py:77`
- last error: TypeError: 'bool' object is not callable
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] TypeError: 'bool' object is not callable

### `is_pytorch` — infra

- canonical source: `tslearn/tslearn/backend/backend.py:81`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `iscomplex` — infra

- canonical source: `tslearn/tslearn/backend/pytorch_backend.py:153`
- last error: missing module/import: cannot import name 'iscomplex' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'iscomplex' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_fu

### `itakura_mask` — runtime

- canonical source: `tslearn/tslearn/metrics/_masks.py:154`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `jacobian_product` — runtime

- canonical source: `tslearn/tslearn/metrics/softdtw_variants.py:1218` · reached: `tslearn/tslearn/backend/backend.py:74`
- last error: AssertionError: The documented contract for jacobian_product is insufficient to verify the result.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: The documented contract for jacobian_product is insufficient to verify the result.

### `lcss_accumulated_matrix` — infra

- canonical source: `tslearn/tslearn/metrics/dtw_variants.py:2270`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `lcss_accumulated_matrix_from_dist_matrix` — infra

- canonical source: `tslearn/tslearn/metrics/dtw_variants.py:2865`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `list_cached_datasets` — runtime

- canonical source: `tslearn/tslearn/datasets/ucr_uea.py:236`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `load_dict` — infra

- canonical source: `tslearn/tslearn/hdftools/hdftools.py:118`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `locate` — infra

- canonical source: `tslearn/tslearn/shapelets/shapelets.py:625` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `mase` — infra

- canonical source: `tslearn/tslearn/metrics/performance.py:153`
- last error: missing module/import: cannot import name 'mase' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/metrics/__init__.py)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing module/import: cannot import name 'mase' from 'tslearn.metrics' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235

### `mse` — runtime

- canonical source: `tslearn/tslearn/metrics/performance.py:83`
- last error: AssertionError: The documented contract for `mse` is insufficient to verify the result or the function does not exist in the expected location.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] AssertionError: The documented contract for `mse` is insufficient to verify the result or the function does not exist in the expected location.

### `n_iter_` — infra

- canonical source: `tslearn/tslearn/svm/svm.py:279` · reached: `tslearn/tslearn/__init__.py:14`, `tslearn/tslearn/shapelets/shapelets.py:7`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `njit_accumulated_matrix` — runtime

- canonical source: `tslearn/tslearn/metrics/dtw_variants.py:74`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

### `njit_accumulated_matrix_from_dist_matrix` — infra

- canonical source: `tslearn/tslearn/metrics/dtw_variants.py:426`
- last error: resumed: fail
- attempts: 1 (no per-round trace recorded — older run; new runs log `round` in error_log.jsonl)

_… 26 more failing APIs omitted (--max-api-detail to raise)._

**Infra failures excluded from doc-quality scoring (60):** `Backend`, `GlobalArgminPooling1D`, `GlobalMinPooling1D`, `KNeighborsTimeSeriesMixin`, `LearningShapelets`, `LocalSquaredDistanceLayer`, `NumPyBackend`, `NumPyLinalg`, `NumPyTesting`, `PyTorchBackend`, `PyTorchRandom`, `PyTorchTesting`, `TsLearnTags`, `accumulated_matrix_from_dist_matrix`, `build`, `call`, `compute_output_shape`, `compute_var`, `cydist_1d_sax`, `cydist_sax`, `cyslopes`, `dtw_barycenter_averaging_one_init`, `early_classification_cost`, `fix_force_all_finite_warning`, `from_cesium_dataset`, `from_numpy`, `get_backend`, `get_config`, `get_weights`, `grabocka_params_to_shapelet_size_dict`, `in_file_string_replace`, `inv_transform_1d_sax`, `inv_transform_paa`, `inv_transform_sax`, `is_float32`, `is_float64`, `is_pytorch`, `iscomplex`, `lcss_accumulated_matrix`, `lcss_accumulated_matrix_from_dist_matrix`, `load_dict`, `locate`, `mase`, `n_iter_`, `njit_accumulated_matrix_from_dist_matrix`, `njit_lcss_accumulated_matrix`, `njit_lcss_accumulated_matrix_from_dist_matrix`, `normalized_cc`, `pdist`, `save_dict`, `set_backend`, `set_weights`, `shapelets_`, `shapelets_as_time_series_`, `to_cesium_dataset`, `transform`, `tril`, `tril_indices`, `triu`, `triu_indices`
