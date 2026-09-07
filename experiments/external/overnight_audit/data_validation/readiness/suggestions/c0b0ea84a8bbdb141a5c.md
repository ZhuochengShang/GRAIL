# encode: Investigate the observed API-use barrier

ID: `c0b0ea84a8bbdb141a5c` · mir_eval/A1 · **open**

Evidence version: `fd894ffc5f5129310e5ea0975291379725e32d0f2f22fc8744618c3f6434bb8f`

Candidate category: **assertion-or-behavior**. Confidence: **medium**.

## Barrier and evidence

Compare expected value with pinned implementation; do not weaken the assertion.

Source: `source/mir_eval/chord.py:471`. Native category: `runtime`.

```text
AssertionError: Expected bass 2 for D:min, got 0
```

[Evidence ledger](../../../mir_eval/A1/ledger.json) · [Saved evidence](../evidence/fd894ffc5f5129310e5ea0975291379725e32d0f2f22fc8744618c3f6434bb8f.json)

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
