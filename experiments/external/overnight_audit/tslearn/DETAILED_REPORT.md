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

Primary failure categories: {"api-identity": 2, "test/scaffold": 7, "unknown": 1}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.

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

### A2

Primary failure categories: {}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.


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
