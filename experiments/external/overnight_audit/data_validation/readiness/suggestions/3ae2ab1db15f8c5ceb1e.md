# get_early_predict_proba_generator: Investigate provider failures and recorded retry behavior

ID: `3ae2ab1db15f8c5ceb1e` · tslearn/A1 · **open**

Evidence version: `a56969e9eb269dcfebcad08711b0fa47dcc07d1ef5f3bd078a536a32eb91a407`

Candidate category: **provider**. Confidence: **high**.

## Barrier and evidence

Recorded provider failure; preserve and retry under existing policy.

Source: `tslearn/tslearn/early_classification/early_classification.py:677`. Native category: `llm-error`.

```text
ServerError: 504 DEADLINE_EXCEEDED. {'error': {'code': 504, 'message': 'Deadline expired before operation could complete.', 'status': 'DEADLINE_EXCEEDED'}}
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/a56969e9eb269dcfebcad08711b0fa47dcc07d1ef5f3bd078a536a32eb91a407.json)

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
