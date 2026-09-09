# list_cached_datasets: Investigate the observed API-use barrier

ID: `cf40b090c19e4acb2bbd` · tslearn/A1 · **open**

Evidence version: `1262cc953879f30985ff0b573d4b63368ead2125a62a7a24a930eed392fe74de`

Candidate category: **assertion-or-behavior**. Confidence: **medium**.

## Barrier and evidence

Compare expected value with pinned implementation; do not weaken the assertion.

Source: `tslearn/tslearn/datasets/ucr_uea.py:236`. Native category: `runtime`.

```text
AssertionError: The documented contract is insufficient to verify the result without network access or a configurable cache directory.
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/1262cc953879f30985ff0b573d4b63368ead2125a62a7a24a930eed392fe74de.json)

Recorded attempts: 0; provider errors: 0; document rounds: None.

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
