# A1/A2 interpretation, provider errors, and current progress

Observation: Tuesday September 8, 2026, approximately 13:35 PDT. This is an interim analysis; native and recovery records are separate. Exact observations, source hashes, regression names and retry counts are in [analysis.json](analysis.json).

## What the changes mean

| Repository | A1 native | A2 native | Net change | Decomposition of changed outcomes |
|---|---:|---:|---:|---|
| mir_eval | 70/148 (47.3%) | 135/148 (91.2%) | +65 | 46 non-provider failures become passes; 4 passes regress; 23 A1-provider cases pass in A2 |
| Thumbnailator | 129/149 (86.6%) | 127/149 (85.2%) | -2 | 12 non-provider failures become passes; 14 passes regress; no A1-provider case passes in A2 |
| tslearn | 121/235 (51.5%) | 175/235 (74.5%) | +54 | 44 non-provider failures become passes; 13 passes regress; 23 A1-provider cases pass in A2 |

Thus raw A2-A1 mixes documentation-conditioned code generation with provider completion differences. It is not solely a documentation quality effect. On the same APIs with no provider failure in either cell, mir_eval changes 70/122 -> 112/122, Thumbnailator 129/146 -> 127/146, and tslearn 121/201 -> 152/201. This selected comparison still includes infrastructure failures and is not unbiased randomized inference.

On the frozen original-documentation detection subgroup, mir_eval changes 18/25 -> 23/25, Thumbnailator 128/146 -> 127/146, and tslearn 89/103 -> 89/103. Consequently, most of the total mir_eval gain and all net tslearn gain occur outside this detected subgroup. Detection is a heuristic for code/backtick/call-form mentions; it does not establish absent documentation elsewhere. Frozen generated-coverage fields predate generation and must not be read as current zero coverage.

The strongest supported interpretation is that the generated documentation often improves practical access to the broader API surface, but can introduce or fail to prevent new usage errors. This remains a single adaptive run. It does not establish repeatable effect size, equal-cost superiority, or independently correct programs.

## Observed failure mechanisms

- mir_eval A2 regressions include nonexistent output paths, empty arrays after beat trimming, wrong boolean/numeric input types, and header parsing. Source inspection found a likely library defect in load_ragged_time_series: header=True changes enumerate numbering without consuming the header. Documentation cannot be assumed to be the cause of this defect.
- Thumbnailator regressions include incorrect constructors or method names, builder lifecycle/state, malformed EXIF input and access to package-private methods. The original bundle includes extensive Javadocs. Generated summaries may omit contracts, but attributing an individual error to a particular sentence requires delivered-document review and a controlled test. The frozen manifest itself includes non-public entries that deserve review in a future version.
- tslearn regressions include an invalid SVC kernel, wrong array dimensions/probability shape, wrong serialization assumptions, insufficient class samples, invalid import names and an unavailable network endpoint. Setup failures mix missing optional dependencies with generated wrong imports; they are not all evidence of packages missing from the environment.

README repair has a clearer completed before/after comparison: mir_eval fixes 6 of 13 A2 failures but loses 4 previous passes, net +2 (137/148). Thumbnailator fixes 16 of 22 A2 failures but loses 4 previous passes, net +12 (139/149). The fresh B2 run exposes regressions that a failure-only retest would miss. A2 source-only recovery is separate and is never used to inflate these native scores.

## Why 504s are numerous

Confirmed: the provider returns 504 DEADLINE_EXCEEDED before usable code/native execution. The latest baseline state has 65 unresolved provider API/cell rows. A1 accounts for 63; tslearn A2 accounts for 2. Repeated calls to the same small set inflate the event count: the inspected currently represented fingerprint groups contain 488 recorded 504 events, approximately 81.3 summed invocation-hours across parallel workers. This is not 81 elapsed clock hours, not an account billing estimate and not a complete HTTP request count.

At the inspected cutoff, tslearn A2 compute has 31 and jacobian_product has 30 retained 504 events; Thumbnailator A1 clear, createOutputStream and region each have 25. Some retries eventually succeed: Thumbnailator B2 retained two 504 events but has no unresolved provider rows. The recurring blockers show that unlimited retry is not reliably recovering every request.

There are three layers: SDK retries within one model invocation, the 630-second outer invocation guard, and watchdog restarts with a 300-second delay and max_restarts=0 (unlimited). Installed client configuration uses a 300-second request timeout and two SDK attempts. About 600 seconds per failed invocation is consistent with deadline/retry interaction, but per-SDK-attempt timing is absent; it does not prove exactly two 300-second server calls.

Google defines 504 as an operation exceeding its deadline, with large context as one possible cause; rate-limit exhaustion is a distinct 429. Our failures also occur with documentation fragments of only 87-100 characters, so documentation length alone is not established as the cause. Total prompt size, server processing/queue delay, model reasoning behavior and SDK/transport effects are unresolved. Google documents increased latency from reasoning and warns that non-default generation parameters can affect Gemini 3 behavior; these are diagnostic hypotheses, not proven causes in this experiment.

Sources: [GenerateContent error reference](https://ai.google.dev/gemini-api/docs/generate-content/api-errors), [troubleshooting and retries](https://ai.google.dev/gemini-api/docs/troubleshooting), [project-level rate limits](https://ai.google.dev/gemini-api/docs/rate-limits).

## Current execution and deadline

mir_eval/Thumbnailator A2 and B2 are complete. A1 remains resumable and partial. At process inspection, mir_eval and Thumbnailator A1 were between invocations in retry cooldown, with live controllers; tslearn A1 and A2 had live comprehension workers. tslearn A2 is watchdog invocation 35 and still gates its own repair/B2. The supplemental scheduler is alive and progressing, sharing one recovery admission slot; native capacity is reserved conservatively. No mutable path conflict was reported by the passive audit. Neither this lock nor request spacing proves compliance with account-wide RPM/TPM/RPD; unrelated clients and SDK internal attempts are not fully observed.

Current recovery counts are in analysis.json. At the immediately preceding read: mir_eval S_A2 13/13 recovered; S_B2 2/11 recovered, 9 pending. Thumbnailator S_A2 19/22 recovered, 1 provider-blocked (createOutputStream), 2 stuck (getRenderingHints/getSourceRegion); S_B2 2/10 recovered, 8 pending. README repair processed all 13 and 22 respective targets. B1 is intentionally omitted. MDAnalysis and RDPro have idle deferred waiters; Sedona is deferred.

Thumbnailator isolated replay is complete for A2/B2: native 127/149 -> 139/149, assertions-off replay 120/149 -> 134/149, assertions-on replay 114/149 -> 126/149. Six A2 and eight B2 tests pass with assertions off and fail with assertions on. The replay does not certify the full repair pipeline; A1 legacy binding remains incomplete.

About 21.4 hours remain until Wednesday 11 AM. A complete study is at risk, especially tslearn's unstarted repair/B2 chain and persistent A1 provider failures. There is no defensible unconditional finish ETA. The old automation ETA is unsuitable: it still includes omitted B1 and inflated remaining counts inconsistent with compatible native evidence. Use the version-3 status and this direct evidence inspection instead. Report framework, visual reports, methods appendix and saved failures exist; the final reconciled detailed report is not yet complete. A deadline report must disclose remaining provider and validation gaps rather than label them finished.

## Recommended next diagnostic improvements (not applied to active measurements)

1. Record per-SDK-attempt start/end, request identifier, full prompt hash/token estimate, timeout, generation/thinking settings and concurrency. This separates service delay from retry amplification.
2. Add per-API exponential backoff with jitter and a persisted cooldown after repeated identical 504s; prioritize useful work without discarding checkpoints. Google recommends bounded retries and backoff for transient errors. Measurement changes must be explicit.
3. Test one-variable changes on isolated failed-request diagnostics: concurrency, timeout, prompt ambiguity or reasoning budget. A model/prompt change belongs to a separate condition, not a silent baseline rescue.
4. Preserve immutable native scores, report provider-completion rate separately, and compare paired API outcomes plus original-documentation subgroups.

No existing worker was restarted or stopped, no measured configuration was changed, and no diagnostic Gemini request was made for this analysis.
