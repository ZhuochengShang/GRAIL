# tslearn detailed A1/A2/B1/B2 report

**Comparison status: PARTIAL.**

Frozen denominator: 235 public API names. Final evaluations allow zero code-fix rounds. B cells are fresh evaluations following at most five document-repair rounds, with two stuck rounds and no separate retry rounds.

## Reproducibility

Exact result paths, branches, commits, environment hashes and PASS_TO_PASS evidence are recorded in provenance.json. The native result JSON retains source/fixture/scaffold/engine/model/document fingerprints. Full checkpoint and document-round histories are in each cell ledger.json; ledger.csv contains every manifest API, including pending APIs.

## Cell results

| Cell | State | Pass | APIs | Infra/provider excluded | Raw % | Scored % |
|---|---|---:|---:|---:|---:|---:|
| A1 | pending/partial | — | 235 | — | — | — |
| A2 | pending/partial | — | 235 | — | — | — |
| B1 | pending/partial | — | 235 | — | — | — |
| B2 | pending/partial | — | 235 | — | — | — |

The scored column uses native infrastructure/provider labels. Secondary harness diagnoses are reported separately and do not rewrite outcomes.

## Effects

Effects withheld until all four matched final cells and their repair/test evidence exist.

## Failure categories and round accounting

### A1

Primary failure categories: {"api-identity": 5, "llm-error": 10, "test/scaffold": 9, "unknown": 7}.

Recorded provider-error attempts across all checkpoint fingerprints: 10. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.

- `Backend`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/backend.py:55`. Error: `missing module/import: No module named 'tslearn.backends'`. Review: Runner classified this as infrastructure.
- `BaseModelPackage`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/bases/bases.py:78`. Error: `AttributeError: 'DummyModel' object has no attribute 'to_dict'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `GlobalArgminPooling1D`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:97`. Error: `missing module/import: No module named 'tensorflow'`. Review: Runner classified this as infrastructure.
- `GlobalMinPooling1D`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:66`. Error: `missing module/import: No module named 'tensorflow'`. Review: Runner classified this as infrastructure.
- `KNeighborsTimeSeriesMixin`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/neighbors/neighbors.py:28`. Error: `missing module/import: cannot import name 'KNeighborsTimeSeriesMixin' from 'tslearn.neighbors' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/neighbors/`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `LearningShapelets`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:290`. Error: `missing module/import: No module named 'keras'`. Review: Runner classified this as infrastructure.
- `LocalSquaredDistanceLayer`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:167`. Error: `missing module/import: No module named 'tensorflow'`. Review: Runner classified this as infrastructure.
- `NumPyBackend`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:22`. Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `NumPyLinalg`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:126`. Error: `missing module/import: No module named 'tslearn.backends'`. Review: Runner classified this as infrastructure.
- `NumPyTesting`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:139`. Error: `missing module/import: No module named 'tslearn.backends'`. Review: Runner classified this as infrastructure.
- `PatchingLayer`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:128`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `PyTorchBackend`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:37`. Error: `missing module/import: No module named 'tslearn.backends'`. Review: Runner classified this as infrastructure.
- `PyTorchRandom`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:243`. Error: `missing module/import: cannot import name 'PyTorchRandom' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `PyTorchTesting`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:263`. Error: `missing module/import: cannot import name 'PyTorchTesting' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `SoftDTW`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1068`. Error: `AttributeError: type object 'SoftDTW' has no attribute 'apply'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `SquaredEuclidean`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1176`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `TimeSeriesCentroidBasedClusteringMixin`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/clustering/utils.py:225`. Error: `AssertionError: The documented contract is insufficient to verify the result.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `TimeSeriesDBSCAN`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/clustering/dbscan.py:19`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `TimeSeriesMixin`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/bases/bases.py:53`. Error: `AssertionError: The documented contract is insufficient to verify the result of TimeSeriesMixin.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `TimeSeriesSVMMixin`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/svm/svm.py:20`. Error: `AttributeError: 'TimeSeriesSVC' object has no attribute 'support_vectors_time_series_'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `TsLearnTags`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/bases/bases.py:29`. Error: `missing module/import: cannot import name 'TsLearnTags' from 'tslearn.bases' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A1/experiments/tslearn/tslearn/tslearn/bases/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `accumulated_matrix`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/_dtw.py:286`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `accumulated_matrix_from_dist_matrix`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/dtw_variants.py:456`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `baseline_accuracy`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/datasets/ucr_uea.py:121`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `belongs_to_backend`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:86`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `build`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:188`. Error: `missing module/import: No module named 'keras'`. Review: Runner classified this as infrastructure.
- `cache_all`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/datasets/ucr_uea.py:376`. Error: `AttributeError: <tslearn.datasets.ucr_uea.UCR_UEA_datasets object at 0x104204f70> does not have the attribute 'cache_dataset'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `call`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:89`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `cast`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/backend.py:91`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `cdist_normalized_cc`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/cycc.py:54`. Error: `TypeError: not enough arguments: expected 5, got 2`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `cdist_sax`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/sax.py:10`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.

### A2

Primary failure categories: {"api-identity": 3, "test/scaffold": 5, "unknown": 9}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.

- `BaseModelPackage`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/bases/bases.py:78`. Error: `AssertionError: The documented contract is insufficient to verify the result non-tautologically.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `EmptyClusterError`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/clustering/utils.py:17`. Error: `AssertionError:`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `GlobalArgminPooling1D`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:97`. Error: `missing module/import: No module named 'keras'`. Review: Runner classified this as infrastructure.
- `GlobalMinPooling1D`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:66`. Error: `missing module/import: No module named 'keras'`. Review: Runner classified this as infrastructure.
- `KNeighborsTimeSeriesMixin`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/neighbors/neighbors.py:28`. Error: `missing module/import: cannot import name 'KNeighborsTimeSeriesMixin' from 'tslearn.neighbors' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/neighbors/`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `LearningShapelets`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:290`. Error: `missing module/import: No module named 'keras'`. Review: Runner classified this as infrastructure.
- `LocalSquaredDistanceLayer`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:167`. Error: `missing module/import: No module named 'tensorflow'`. Review: Runner classified this as infrastructure.
- `NonMyopicEarlyClassifier`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/early_classification/early_classification.py:18`. Error: `AssertionError: Delays should be at least min_t (2)`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `NumPyBackend`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:22`. Error: `missing module/import: cannot import name 'NumPyBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `NumPyRandom`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/numpy_backend.py:132`. Error: `AssertionError: The documented contract is insufficient to verify the result`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `PatchingLayer`: test/scaffold; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:128`. Error: `missing module/import: No module named 'tensorflow'`. Review: Runner classified this as infrastructure.
- `PyTorchBackend`: api-identity; native=infra; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:37`. Error: `missing module/import: cannot import name 'PyTorchBackend' from 'tslearn.backend' (/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/tslearn/tslearn/backend/__init__.py)`. Review: Import/member selection failed; the runner's infrastructure label needs review.
- `PyTorchRandom`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:243`. Error: `AssertionError: The documented contract is insufficient to verify the result of PyTorchRandom.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `PyTorchTesting`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/backend/pytorch_backend.py:263`. Error: `AssertionError: The documented contract is insufficient to verify the result.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `SoftDTW`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1068`. Error: `TypeError: SoftDTW.__init__() missing 1 required positional argument: 'D'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `SquaredEuclidean`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1176`. Error: `TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `TimeSeriesSVMMixin`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/svm/svm.py:20`. Error: `AssertionError: The documented contract is insufficient to verify the result non-tautologically as it does not specify any methods or attributes provided by the mixin.`. Review: Observed runtime; doc attribution requires source, document, and snippet review.

### B1

Primary failure categories: {}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.


### B2

Primary failure categories: {}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.


## Validity and remaining review

- Recorded PASS_TO_PASS result/exit-status markers and per-cell fixture fingerprints are checked before effects are released.
- Unknown primary categories require source/document review; do not relabel provider errors as documentation failures.
- Report runtime from the first start through completion, including watchdog waits, rather than the last resumed invocation alone.
