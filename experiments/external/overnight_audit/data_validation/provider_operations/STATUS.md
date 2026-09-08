# Execution status and API timing

2026-09-08T16:11:23.229245-07:00

**No single “partial” label:** each unresolved case has an explicit reason. A finished evaluation can contain real failures. A provider failure is not executed code. A running test does not prove the target API was reached.

| Repository | Cell | State | Pass | Compile fail | Execution fail | Setup/import | Provider pending | Other/timeout |
|---|---|---|---:|---:|---:|---:|---:|---:|
| mir_eval | A1 | 26 provider cases unresolved | 70 | 0 | 49 | 2 | 26 | 1 |
| mir_eval | A2 | Native evaluation finished (failures still count) | 135 | 0 | 13 | 0 | 0 | 0 |
| mir_eval | B2 | Native evaluation finished (failures still count) | 137 | 0 | 11 | 0 | 0 | 0 |
| Thumbnailator | A1 | Native evaluation finished (failures still count) | 130 | 8 | 9 | 0 | 0 | 2 |
| Thumbnailator | A2 | Native evaluation finished (failures still count) | 127 | 14 | 8 | 0 | 0 | 0 |
| Thumbnailator | B2 | Native evaluation finished (failures still count) | 139 | 7 | 3 | 0 | 0 | 0 |
| tslearn | A1 | 34 provider cases unresolved | 121 | 0 | 29 | 51 | 34 | 0 |
| tslearn | A2 | Native evaluation finished (failures still count) | 175 | 0 | 32 | 28 | 0 | 0 |
| tslearn | B2 | Not started / no native results | 0 | 0 | 0 | 0 | 0 | 0 |

Other failures/timeouts, if present, remain explicit in summary.json and the full API table. B1 is intentionally omitted. MDAnalysis, Sedona and RDPro reruns are deferred.

[Searchable dashboard](REPORT.html) · [Every API timing (CSV)](API_TIMINGS.csv) · [Machine-readable status](summary.json)

Timing: latest_native_attempt_s is one recorded generation-plus-test attempt, not lifetime duration. retained_attempt_total_s sums retained checkpoint events only. Provider transport duration is measured separately for instrumented retries. last_retry_interval_s is the interval from a previous provider end to the next provider start, including queue/cooldown. Blank historical timing means unavailable, not zero.

New workers may use the explicitly registered 600s × 1 transport and output-directory setup amendment. Existing workers finish under their previous settings. Each instrumented request records policy/adapter hashes; native fingerprints alone do not distinguish transport revisions. Source and README repairs remain separate from these operational corrections.

## Separate source-recovery progress

- mir_eval / A2 source fixes: {'recovered_native': 13}; cohort 13 APIs.
- mir_eval / Post-B2 source fixes: {'recovered_native': 11}; cohort 11 APIs.
- Thumbnailator / A2 source fixes: {'recovered_native': 20, 'stuck': 2}; cohort 22 APIs.
- Thumbnailator / Post-B2 source fixes: {'recovered_native': 8, 'stuck': 2}; cohort 10 APIs.
- tslearn / A2 source fixes: {'recovered_native': 32}; cohort 32 APIs.

## Transport rollout

- mir_eval A1: Installed; awaiting next natural worker start; observed workers [].
- Thumbnailator A1: New transport observed in worker logs; observed workers [16216].
- tslearn A1: Installed; awaiting next natural worker start; observed workers [].
- tslearn A2: New transport observed in worker logs; observed workers [12853].
