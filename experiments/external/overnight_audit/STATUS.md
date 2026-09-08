# AIDEAL overnight evidence audit

Deadline: 2026-09-09T11:00:00-07:00. This observer never starts, stops, or restarts experiment jobs.

| Repository | Cell | State | Pass | Fail | Pending | Recorded provider-error attempts |
|---|---|---|---:|---:|---:|---:|
| mir_eval | A1 | partial | 68 | 80 | 0 | 118 |
| mir_eval | A2 | complete | 135 | 13 | 0 | 1 |
| mir_eval | B1 | pending | 0 | 0 | 148 | 0 |
| mir_eval | B2 | pending | 0 | 0 | 148 | 0 |
| thumbnailator | A1 | partial | 126 | 23 | 0 | 28 |
| thumbnailator | A2 | complete | 127 | 22 | 0 | 1 |
| thumbnailator | B1 | pending | 0 | 0 | 149 | 0 |
| thumbnailator | B2 | pending | 0 | 0 | 149 | 0 |
| tslearn | A1 | partial | 87 | 91 | 57 | 39 |
| tslearn | A2 | partial | 151 | 59 | 25 | 12 |
| tslearn | B1 | pending | 0 | 0 | 235 | 0 |
| tslearn | B2 | pending | 0 | 0 | 235 | 0 |
| mdanalysis | A1 | pending | 0 | 0 | 1032 | 0 |
| mdanalysis | A2 | pending | 0 | 0 | 1032 | 0 |
| mdanalysis | B1 | pending | 0 | 0 | 1032 | 0 |
| mdanalysis | B2 | pending | 0 | 0 | 1032 | 0 |

## Interpretation

Partial counts are checkpoints, not final results. Provider failures remain visible and prevent completion. Per-API ledger.json/ledger.csv files include pending APIs, checkpoint attempts, errors, document rounds, and repair evidence. Provider-internal retries are unobserved in existing logs and are null, not zero. The configured retry ceiling is not an observed retry count. Unknown failure attribution requires review; execution errors alone do not prove a documentation defect.

Raw final results are preserved unchanged. Secondary harness diagnoses do not rewrite headline scores. Runtime and usage in a resumed final JSON describe its last invocation; use checkpoint histories and watchdog start/end logs for total accounting.

RDPro is reuse-only. Its queued entry point verifies retained evidence and exits without paid execution. Sedona preparation remains deferred until MDAnalysis has completed.

## Attention

- No structural errors found by this observer.
