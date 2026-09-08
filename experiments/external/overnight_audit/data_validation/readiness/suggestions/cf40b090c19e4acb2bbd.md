# list_cached_datasets: Investigate the observed API-use barrier

ID: `cf40b090c19e4acb2bbd` · tslearn/A1 · **open**

Evidence version: `a0943fb8be2804bb9f4e57ae1818541865a4e610b6677452326f57b90d5f6293`

Candidate category: **assertion-or-behavior**. Confidence: **medium**.

## Barrier and evidence

Compare expected value with pinned implementation; do not weaken the assertion.

Source: `tslearn/tslearn/datasets/ucr_uea.py:236`. Native category: `runtime`.

```text
AssertionError: The documented contract is insufficient to verify the result without network access or a configurable cache directory.
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/a0943fb8be2804bb9f4e57ae1818541865a4e610b6677452326f57b90d5f6293.json)

Recorded attempts: 1; provider errors: 0; document rounds: None.

## Proposed action

Compare expected value with pinned implementation; do not weaken the assertion.

## Required validation

Reproduce in an isolated diagnostic; establish input, call and assertion validity before attributing a documentation or code defect.

Hypothesis only; measure against the pinned baseline before claiming improvement.

## Review and implementation

Choose a concrete plan, then assign approved work to a human or agent. This card never executes changes.

Reviewer acceptance does not alter measured scores or certify readiness. New improvements need matched evaluation evidence.

```json
{
  "status": "open",
  "events": []
}
```
