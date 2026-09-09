# jacobian_product: Investigate the observed API-use barrier

ID: `efe13aead9dc33ab2b15` · tslearn/A1 · **open**

Evidence version: `5e89c5bcccb4ecad1797151014e26af2a79eab24ec37dfc655de4faf7221ac24`

Candidate category: **assertion-or-behavior**. Confidence: **medium**.

## Barrier and evidence

Compare expected value with pinned implementation; do not weaken the assertion.

Source: `tslearn/tslearn/metrics/softdtw_variants.py:1218`. Native category: `runtime`.

```text
AssertionError: The documented contract for jacobian_product is insufficient to verify the result.
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/5e89c5bcccb4ecad1797151014e26af2a79eab24ec37dfc655de4faf7221ac24.json)

Recorded attempts: 4; provider errors: 3; document rounds: None.

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
