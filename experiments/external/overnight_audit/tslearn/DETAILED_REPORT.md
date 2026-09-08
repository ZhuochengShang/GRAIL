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

Primary failure categories: {"llm-error": 4, "unknown": 1}.

Recorded provider-error attempts across all checkpoint fingerprints: 51. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.

- `PatchingLayer`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/shapelets/shapelets.py:128`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `SquaredEuclidean`: unknown; native=runtime; checkpoint attempts=1; provider-error attempts=0; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1176`. Error: `TypeError: SquaredEuclidean.__init__() missing 2 required positional arguments: 'X' and 'Y'`. Review: Observed runtime; doc attribution requires source, document, and snippet review.
- `TimeSeriesDBSCAN`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/clustering/dbscan.py:19`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `accumulated_matrix`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/_dtw.py:286`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `accumulated_matrix_from_dist_matrix`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/dtw_variants.py:456`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.

### A2

Primary failure categories: {"llm-error": 3}.

Recorded provider-error attempts across all checkpoint fingerprints: 19. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.

- `compute`: llm-error; native=llm-error; checkpoint attempts=2; provider-error attempts=2; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1111`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `jacobian_product`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/metrics/softdtw_variants.py:1218`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.
- `predict_class_and_earliness`: llm-error; native=llm-error; checkpoint attempts=1; provider-error attempts=1; document rounds=None; repair=None. Source: `tslearn/tslearn/early_classification/early_classification.py:399`. Error: `ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}`. Review: Provider outcome; retry, never count as a documentation failure.

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
