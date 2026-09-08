# tslearn full235 B2 failure analysis

- Result: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/docs/eval/B2/comprehension.json`
- Experiment fingerprint: `30cc839a6cf5014970320c8ba149a2470efab72ef9275c5c4eccb4eb6c6ff969`
- APIs: 235
- Failures: 18

## Failure categories

- `infra`: 13
- `runtime`: 5

## Per-function evidence

### `GlobalArgminPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:97`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `GlobalMinPooling1D`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:66`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 9.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

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
- Attempts / wall seconds: 1 / 25.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `PatchingLayer`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:128`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 26.5
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `TimeSeriesMixin`

- Category: `runtime`
- Source definition: `tslearn/tslearn/bases/bases.py:53`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 10.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: TimeSeriesMixin should set 'allow_nan' to True in tags`

### `build`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:188`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 27.4
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `call`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:89`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 18.9
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'tensorflow'`

### `compute_output_shape`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:86`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 18.7
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `extract_from_zip_url`

- Category: `runtime`
- Source definition: `tslearn/tslearn/datasets/datasets.py:16`
- Reached codebase frames: `tslearn/tslearn/datasets/datasets.py:39`
- Attempts / wall seconds: 1 / 8.0
- Diagnosis: Generated code compiled but failed at runtime; inspect inputs, preconditions, and return semantics.
- Error: `URLError: <urlopen error [Errno 61] Connection refused>`

### `get_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:828`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 11.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `grabocka_params_to_shapelet_size_dict`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:235`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 24.8
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `is_float`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:106`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 7.7
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected the backend to identify the float array X as a float type.`

### `is_float32`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:110`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 7.2
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Expected True for float32 array`

### `is_float64`

- Category: `runtime`
- Source definition: `tslearn/tslearn/backend/numpy_backend.py:114`
- Reached codebase frames: `none`
- Attempts / wall seconds: 1 / 9.6
- Diagnosis: The call ran, but the generated semantic expectation/correctness assertion was wrong.
- Error: `AssertionError: Failed to identify float64 array.`

### `locate`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:625`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 11.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `set_weights`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:866`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 10.6
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`

### `shapelets_as_time_series_`

- Category: `infra`
- Source definition: `tslearn/tslearn/shapelets/shapelets.py:455`
- Reached codebase frames: `tslearn/tslearn/__init__.py:14; tslearn/tslearn/shapelets/shapelets.py:7`
- Attempts / wall seconds: 1 / 17.2
- Diagnosis: Execution environment or optional dependency gap, not documentation quality.
- Error: `missing module/import: No module named 'keras'`
