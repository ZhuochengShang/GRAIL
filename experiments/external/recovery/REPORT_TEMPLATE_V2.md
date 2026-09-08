# AIDEAL A2-only repair report

Snapshot time, repository/source commit, AIDEAL commit, protocol version,
ordered manifest hash, data/scaffold/config/model/prompt hashes: `<evidence>`.

| Measurement | Denominator | Native outcome | Independently validated outcome |
|---|---|---|---|
| A1 original README, zero fixes | Full frozen manifest | `<pass/N>` | `<verified/inspected; unknown remainder>` |
| A2 generated README, zero fixes | Same manifest | `<pass/N>` | `<verified/inspected>` |
| Source recovery from A2 failures | Fixed eligible failure cohort F | `<recovered/F>` | `<verified/inspected>` |
| B2 rewritten generated README, fresh zero-fix test | Same full manifest | `<pass/N>` | `<verified/inspected>` |
| B2 on the source-eligible A2-failure cohort | Same F | `<pass/F>` | `<verified/inspected>` |

Original-README repair is omitted. The study does not estimate a 2×2 interaction.
Source recovery measures immediate task recovery; B2 measures transfer through
rewritten documentation to fresh generation. They have different evidence and
compute budgets; their difference is not a pure equal-cost source-access effect.

| New code-fix round | A2 baseline 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Cumulative source recoveries / F | 0/F | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |
| Additional recoveries in round | — | `<...>` | `<...>` | `<...>` | `<...>` | `<...>` |

Count provider events separately from code proposals. Retain stuck stops,
exhausted budgets, infrastructure exclusions and unavailable script evidence.
Do not remove blocked APIs from F after freezing it. Passing generated code is
native recovery until target execution, input contracts and assertions are reviewed.

| API | A2 failure and code evidence | Source diagnosis | Code rounds/outcomes | Document rounds, rejected/reverted proposals | Final B2 | Proposed developer improvement | Review status |
|---|---|---|---|---|---|---|---|
| `<API>` | `<category/error/hash>` | `<source/tests/report>` | `<round history>` | `<docfix.json and README diffs>` | `<status>` | `<evidence-backed suggestion>` | `<pending/accepted/rejected>` |

Report A2−A1 and B2−A2 in raw percentage points on the common manifest. List
A2-pass→B2-fail regressions and distinguish stochastic generation from proven
document defects. Keep costs for diagnosis, code fixes, document rewrites,
fresh evaluation and provider retries separate; unobserved SDK retries are unknown.

Include each repository's concrete data paths/formats, decoded samples,
in-memory construction/slicing, API input shapes/types/units, target/receiver,
assertion meaning, effective YAML layers, import/package evidence and fixture
hashes. Link the populated data/API appendix and independent replay, retaining
native scores and historical binding/output-state limitations.

Final state: `<complete native / partial / validation blocked>`. Explicitly list
remaining provider errors, unreviewed semantics and missing artifacts. Record the
Wednesday 10:45 AM snapshot and the 11 AM deadline; never substitute estimates
for measurements. MDAnalysis, Sedona and RDPro reruns are outside this package.
