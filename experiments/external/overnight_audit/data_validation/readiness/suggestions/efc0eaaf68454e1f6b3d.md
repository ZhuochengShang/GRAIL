# baseline_accuracy: Investigate the observed API-use barrier

ID: `efc0eaaf68454e1f6b3d` · tslearn/A1 · **open**

Evidence version: `43ca069c19ca0531a85c9d54a1150e34891257c1596b2065390de6bb6754cd71`

Candidate category: **assertion-or-behavior**. Confidence: **medium**.

## Barrier and evidence

Compare expected value with pinned implementation; do not weaken the assertion.

Source: `tslearn/tslearn/datasets/ucr_uea.py:121`. Native category: `runtime`.

```text
AssertionError: Unexpected baseline accuracy: {'Trace': {'NB': 0.8, 'C45': 0.79, 'SVML': 0.73, 'SVMQ': 0.82, 'BN': 0.82, 'RandF': 0.78, 'RotF': 0.93, 'MLP': 0.84, 'Euclidean_1NN': 0.76, 'DTW_R1_1NN': 1.0, 'DTW_Rn_1NN': 0.99, 'DDTW_R1_1NN': 1.0, 'DDTW_Rn_1NN': 0.99, 'ERP_1NN': 0.95, 'LCSS_1NN': 0.97, 'MSM_1NN': 0.93, 'TWE_1NN': 0.99, 'WDDTW_1NN': 1.0, 'WDTW_1NN': 1.0, 'DD_DTW': 1.0, 'DTD_C': 0.99, 'DTW_F': 1.0, 'ST': 1.0, 'LS': 1.0, 'FS': 1.0, 'BoP': 0.97, 'SAXVSM': 1.0, 'BOSS': 1.0, 'TSF': 0.99, 'TSBF': 0.98, 'LPS': 0.98, 'ACF': 1.0, 'PS': 0.95, 'EE': 0.99, 'COTE': 1.0, 'CID_DTW': 0.99}}
```

[Evidence ledger](../../../tslearn/A1/ledger.json) · [Saved evidence](../evidence/43ca069c19ca0531a85c9d54a1150e34891257c1596b2065390de6bb6754cd71.json)

Recorded attempts: 2; provider errors: 1; document rounds: None.

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
