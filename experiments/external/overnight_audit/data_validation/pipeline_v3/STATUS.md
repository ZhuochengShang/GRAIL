# AIDEAL: three separate stages

2026-09-08T07:51:16.619344-07:00

A1/A2 are zero-fix controls. S_A2 repairs snippets from A2 failures. Independent README repair produces fresh zero-fix B2. S_B2 repairs only eligible B2 failures.

| Repository | Measurement | State | Native pass/recovered | Denominator |
|---|---|---|---:|---:|
| mir_eval | A1 | native partial | 70 | 148 |
| mir_eval | A2 | native complete | 135 | 148 |
| mir_eval | B2 | native complete | 137 | 148 |
| mir_eval | S_A2 | {'recovered_native': 13} | 13 | 13 |
| mir_eval | S_B2 | priority complete | — | — |
| thumbnailator | A1 | native partial | 129 | 149 |
| thumbnailator | A2 | native complete | 127 | 149 |
| thumbnailator | B2 | native complete | 139 | 149 |
| thumbnailator | S_A2 | {'recovered_native': 18, 'provider_blocked': 2, 'stuck': 2} | 18 | 22 |
| thumbnailator | S_B2 | ValueError: A2 source work/retries still pending; preserve its provider capacity | — | — |
| tslearn | A1 | native partial | 120 | 235 |
| tslearn | A2 | native partial | 175 | 235 |
| tslearn | B2 | pending native evidence | — | — |
| tslearn | S_A2 | FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/docs/eval/A2/comprehension.json' | — | — |
| tslearn | S_B2 | FileNotFoundError: [Errno 2] No such file or directory: '/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_A2/experiments/tslearn/docs/eval/A2/comprehension.json' | — | — |

Denominators: A1/A2/B2 use the full manifest; S_A2 and S_B2 use different frozen eligible-failure cohorts.
The composite B2 + S_B2 endpoint is never reported as the native B2 score.

[Exact protocol and diagram](PIPELINE_V3.md) · [Report template](REPORT_TEMPLATE_V3.md) · [Full evidence JSON](live.json) · [Data/API methods](../FINAL_REPORT_DATA_AND_API_METHODS.md) · [Independent assertion replay](../assertion_replay/REPLAY.html)

Method limitations: single adaptive run; no equal-cost randomized comparison. Legacy document retries can restart an unfinished API, and initial A2 error-context seeding is unverified. See document_protocol_audit in JSON for observed round counts. Native passes still require semantic review.
