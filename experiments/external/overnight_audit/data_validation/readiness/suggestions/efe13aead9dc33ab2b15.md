# jacobian_product: Investigate provider failures and recorded retry behavior

ID: `efe13aead9dc33ab2b15` · tslearn/A1 · **open**

Evidence version: `f78ee207d2fce6ba7092e483494eaee47e3941388aa76373b87a1bfe7c824677`

Candidate category: **provider**. Confidence: **high**.

## Barrier and evidence

Recorded provider failure; preserve and retry under existing policy.

Source: `tslearn/tslearn/metrics/softdtw_variants.py:1218`. Native category: `llm-error`.

```text
ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/f78ee207d2fce6ba7092e483494eaee47e3941388aa76373b87a1bfe7c824677.json)

Recorded attempts: 2; provider errors: 2; document rounds: None.

## Proposed action

Check quota/cooldown and error histories; preserve existing retry policy and completed checkpoints.

## Required validation

Reattempt only compatible unresolved requests under authorized policy; report recovery separately from documentation benefit.

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
