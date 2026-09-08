# AIDEAL: three separate stages

2026-09-08T14:40:17.282739-07:00

A1/A2 are zero-fix controls. S_A2 repairs snippets from A2 failures. Independent README repair produces fresh zero-fix B2. S_B2 repairs only eligible B2 failures.

| Repository | Measurement | State | Native pass/recovered | Denominator |
|---|---|---|---:|---:|
| mir_eval | A1 | native partial | 70 | 148 |
| mir_eval | A2 | native complete | 135 | 148 |
| mir_eval | B2 | native complete | 137 | 148 |
| mir_eval | S_A2 | {'recovered_native': 13} | 13 | 13 |
| mir_eval | S_B2 | {'recovered_native': 11} | 11 | 11 |
| thumbnailator | A1 | native complete | 130 | 149 |
| thumbnailator | A2 | native complete | 127 | 149 |
| thumbnailator | B2 | native complete | 139 | 149 |
| thumbnailator | S_A2 | {'recovered_native': 20, 'stuck': 2} | 20 | 22 |
| thumbnailator | S_B2 | {'recovered_native': 8, 'stuck': 2} | 8 | 10 |
| tslearn | A1 | native partial | 121 | 235 |
| tslearn | A2 | native complete | 175 | 235 |
| tslearn | B2 | pending native evidence | — | — |
| tslearn | S_A2 | {'recovered_native': 32} | 32 | 32 |
| tslearn | S_B2 | FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/docs/eval/B2/comprehension.json' | — | — |

Denominators: A1/A2/B2 use the full manifest; S_A2 and S_B2 use different frozen eligible-failure cohorts.
The composite B2 + S_B2 endpoint is never reported as the native B2 score.

[Exact protocol and diagram](PIPELINE_V3.md) · [Report template](REPORT_TEMPLATE_V3.md) · [Full evidence JSON](live.json) · [Data/API methods](../FINAL_REPORT_DATA_AND_API_METHODS.md) · [Independent assertion replay](../assertion_replay/REPLAY.html)

Method limitations: single adaptive run; no equal-cost randomized comparison. Legacy document retries can restart an unfinished API; A2 error-log seed binding is audited per repository. See document_protocol_audit in JSON for observed round counts. Native passes still require semantic review.
