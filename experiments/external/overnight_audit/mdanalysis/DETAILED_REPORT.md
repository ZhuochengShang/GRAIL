# mdanalysis detailed A1/A2/B1/B2 report

**Comparison status: PARTIAL.**

Frozen denominator: 1032 public API names. Final evaluations allow zero code-fix rounds. B cells are fresh evaluations following at most five document-repair rounds, with two stuck rounds and no separate retry rounds.

## Reproducibility

Exact result paths, branches, commits, environment hashes and PASS_TO_PASS evidence are recorded in provenance.json. The native result JSON retains source/fixture/scaffold/engine/model/document fingerprints. Full checkpoint and document-round histories are in each cell ledger.json; ledger.csv contains every manifest API, including pending APIs.

## Cell results

| Cell | State | Pass | APIs | Infra/provider excluded | Raw % | Scored % |
|---|---|---:|---:|---:|---:|---:|
| A1 | pending/partial | — | 1032 | — | — | — |
| A2 | pending/partial | — | 1032 | — | — | — |
| B1 | pending/partial | — | 1032 | — | — | — |
| B2 | pending/partial | — | 1032 | — | — | — |

The scored column uses native infrastructure/provider labels. Secondary harness diagnoses are reported separately and do not rewrite outcomes.

## Effects

Effects withheld until all four matched final cells and their repair/test evidence exist.

## Failure categories and round accounting

### A1

Primary failure categories: {}.

Recorded provider-error attempts across all checkpoint fingerprints: 0. Provider-internal retries are not recorded by the existing client and cannot be inferred from the configured limit. Watchdog logs retain process attempts; checkpoint attempts and document-fix rounds are separate ledger fields.


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
