**Current scheduling amendment:** [Independent repository admission](INDEPENDENT_SCHEDULING.md) removes the global wait and resumes source-provider retries independently of A1. The older scheduling section below is historical. Measurement rules remain unchanged.

**Input handoff correction:** [Verified A2 errors and CLI paths](INPUT_HANDOFF_CORRECTION.md) supersedes the initial-error-seeding caveat below for repositories whose handoff status is `prepared`. The document-round restart limitation remains.

# AIDEAL separated-stage experiment report

Snapshot `<timestamp/timezone>`; protocol `aideal-separated-recovery-v3`;
repository/source/AIDEAL commits `<...>`; run state `<finished / running / awaiting provider / awaiting prerequisites>`.
Record the amendment time and observations already available at registration.

| Measurement | Denominator | Native result | Independent validation |
|---|---|---|---|
| A1 original README, zero fixes | N | `<pass/N; provider/infra/other>` | `<reviewed/unknown>` |
| A2 generated README, zero fixes | N | `<pass/N; provider/infra/other>` | `<reviewed/unknown>` |
| S_A2 source-only recovery | Frozen F_A2 | `<recovered/F_A2; blocked retained>` | `<reviewed/unknown>` |
| B2 rewritten README, fresh zero fixes | N | `<pass/N; regressions>` | `<reviewed/unknown>` |
| S_B2 post-B2 source recovery | Frozen F_B2 | `<recovered/F_B2; blocked retained>` | `<reviewed/unknown>` |
| B2 + S_B2 composite | N | `<native B2 passes + recovered B2 failures>` | `<reviewed/unknown>` |

The composite is not the B2 score. No original-README repair or 2×2 interaction
is estimated. Native acceptance, replay acceptance and correctness are separate.

## Matched per-API outcomes

| API | A2 status/category | In F_A2? | S_A2 outcome/round | README repair outcome/rounds | Fresh B2 | In F_B2? | S_B2 outcome/round | B2 regression? | Evidence and review |
|---|---|---|---|---|---|---|---|---|---|
| `<API>` | `<...>` | `<yes/no/reason>` | `<...>` | `<...>` | `<...>` | `<yes/no/reason>` | `<...>` | `<...>` | `<hash/path>` |

On F_A2 report S_A2 recovered, B2 passed and B2+S_B2 passed, paired by API.
Report raw percentage-point changes on N and absolute counts. Different failure
cohorts/budgets are not equal-cost causal comparisons. No unsupported significance
or held-out generalization claims. State macro/micro aggregation if pooling repos.

## Attempts, rounds, cost and failure causes

| Stage | Cohort | Round 0 | New rounds 1/2/3/4/5 | Diagnosis calls | Provider events | Watchdog attempts | Time/tokens | Unknown evidence |
|---|---|---|---|---|---|---|---|---|
| S_A2 | F_A2 | Frozen A2 failure | `<incremental and cumulative recoveries>` | `<...>` | `<...>` | `<...>` | `<scope>` | `<...>` |
| README repair | Actual selected targets, including infrastructure if present | Frozen document | `<actual starts, validations, rejected/reverted drafts>` | `<...>` | `<...>` | `<...>` | `<scope>` | `<missing restart drafts>` |
| S_B2 | F_B2 | Frozen B2 failure | `<incremental and cumulative recoveries>` | `<...>` | `<...>` | `<...>` | `<scope>` | `<...>` |

Audit repeated doc round numbers after restart from append-only logs; distinguish
round starts from completed rewrites/validations. Record configured versus actual
budgets. Check A2 error/snippet seeding into the document worker independently of
target selection; retain the current limitation if unverified. Stuck-two source
and document loops have different stopping definitions. SDK retries may be unknown.

### Per-API execution and timing evidence

Use [the execution/timing reporter](../provider_retry/README.md) alongside this
template. For every API and condition record the latest generation-plus-test
attempt duration, retained attempt count and summed duration, code-fix rounds,
document rounds, provider invocations, each measured SDK attempt duration,
provider start/end timestamps, end-to-next-start retry interval and scheduled
cooldown. The retry interval includes scheduler/admission delay. Retained duration
is not a complete lifetime total. Missing historical timestamps mean unavailable,
never zero. An unfinished invocation has no inferred end or success.

Report native passes, compilation failures, execution failures/timeouts,
setup/import blocks, unresolved providers and not-started cases separately.
Provide counts summing to the manifest denominator and explain missing rows.
An API selected for generation is not necessarily executed; process execution
does not independently prove the target API was reached or used correctly.
Cooldown deferrals send no request and must not inflate 504 or code-fix counts.

For the September 8 operational amendment, group results by transport policy
and adapter hashes: historical 300 seconds × 2 SDK attempts versus enrolled
600 seconds × 1, both with a 630-second outer guard. Record actual worker
activation, not just installed configuration. Frozen native fingerprints do
not encode this extension. Record output-directory setup changes separately.
Keep native outcomes, unchanged-snippet harness replay, assertion replay and
source recovery in distinct columns; none silently replaces another score.

For each unresolved API retain error category, actual snippet/error, round-by-round
change, source/document evidence, proposed developer fix, confidence, alternative
causes, and human review status. Separate provider, dependency/import, data/setup,
input contract, target API use, compilation, assertion and documentation candidates.
A failure after a generated README is not proof that the README caused it.

## Data and reproducibility appendix

For each repository include source/API manifest identity, receiver/overload ambiguity,
fixture path/hash/origin, concrete decoded sample, format, shape/dtype/units, sample
construction, how the target consumes it, expected postcondition, and assertion status.
Record effective YAML layers, profiles, command, runtime imports/packages, model roles,
prompts, engine and document hashes, timeouts, scope/caps and checkpoint compatibility.
Distinguish API attempted, code generated, compiled, process started, target reached,
native passed and independently verified. Unknown stages remain unknown.

Link the data/API methods appendix, isolated Thumbnailator replay, readiness assessment,
review queue, source/B2 raw artifacts and per-case histories. Log all protocol deviations,
missing historical bindings and semantic-review gaps. Final timestamped partial reports
must retain unresolved providers and pending stages; never insert forecast counts.
