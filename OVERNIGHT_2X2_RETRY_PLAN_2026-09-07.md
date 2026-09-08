# AIDEAL overnight A1/A2/B1/B2 retry and fix-round plan

Date: 2026-09-07 (America/Los_Angeles)

**Updated September 7, 14:15:** the user approved parallel execution of
mir_eval, Thumbnailator and tslearn for the Wednesday 11:00 AM deadline.
MDAnalysis, Sedona and RDPro reruns may wait. The serial graph below records
the original plan; the current admission and reporting handoff is
`STATUS_2026-09-07_PRIORITY_PARALLEL.md`. Measurement and repair limits remain
unchanged.

## Measurement rule

Every final A1/A2/B1/B2 comprehension run uses `--max-fix-rounds 0`.
Therefore no generated code repair is credited in the final measurement. A
provider/network failure is transient and cannot satisfy a completion
predicate; the watchdog resumes the fingerprinted per-API checkpoint or
retries the job.

## Repair rule

B1 and B2 documentation repair runs use at most five document rounds per
failed API (`--doc-rounds 5`), stop after two consecutive stuck rounds
(`--doc-stuck 2`), and use no separate retry rounds (`--retry-rounds 0`).
The subsequent B1/B2 comprehension is a fresh zero-round measurement.

## Repository matrix

| Repository | A1 | A2 | B1 | B2 | Provider retries |
|---|---|---|---|---|---|
| mir_eval | original, zero fix rounds | generated README, zero fix rounds | ≤5 doc rounds, then zero-round test | ≤5 doc rounds, then zero-round test | 2 |
| Thumbnailator | original, zero fix rounds | generated README, zero fix rounds | ≤5 doc rounds, then zero-round test | ≤5 doc rounds, then zero-round test | 2 |
| tslearn | original, zero fix rounds | full corrected 235-name README, then zero-round test | ≤5 doc rounds, then zero-round test | ≤5 doc rounds, then zero-round test | 2 |
| MDAnalysis | original, zero fix rounds | full corrected 1,032-name README, then zero-round test | ≤5 doc rounds with `create-missing`, then zero-round test | ≤5 doc rounds, then zero-round test | 2 |
| RDPro | existing finished evidence retained | existing finished evidence retained | duplicate rerun stopped | duplicate rerun stopped | historical runner: 8; 24 supervisor restarts |

For the active four-repository queue, `max_restarts: 0` means unlimited
watchdog restarts. The separate repair-round limit above is not a provider
retry limit.

## Queue and isolation

```text
mir_eval A1/A2 -> mir_eval B1/B2
                         |
                         v
Thumbnailator A1/A2 -> Thumbnailator B1/B2
                         |
                         v
tslearn full235 A1/A2 -> tslearn full235 B1/B2
                         |
                         v
MDAnalysis full1032 A1/A2 -> MDAnalysis full1032 B1/B2
```

Condition jobs are parallel inside each repository where dependencies allow;
repository-level admission is staggered behind durable success markers so the
shared Gemini rate gate remains safe. Each cell has a separate branch,
worktree, checkpoint, output directory, error log, and failure-analysis
directory. PASS_TO_PASS tests are required before and after treatment.

## Current state at memo time

- mir_eval A2 generation and zero-round result: complete. A1 was being
  retried after transient 504 responses; incomplete output is rejected.
- Thumbnailator full 149-entry README generation: complete; its 2×2 driver is
  waiting for mir_eval completion.
- tslearn corrected full surface: 235 names / 343 definition sites; plan
  committed and queued behind Thumbnailator.
- MDAnalysis corrected full surface: 1,032 names / 1,397 definition sites,
  492 checked-in fixtures; validator passes and plan is queued behind tslearn.
- RDPro: no duplicate paid run is active; prior finished work is preserved.

All generated and measured outputs must retain their source commit, manifest
hash, fixture hashes, YAML/profile fingerprint, interpreter inventory, and
per-function failure details. Historical 99-name tslearn and 661-name
MDAnalysis artifacts are reference-only and are not reused as full-surface
denominators.
# September 8 scope update

The user replaced the pending original-README repair branch with an A2-only
repair study. [Active protocol](experiments/external/recovery/PIPELINE_V2.md):
A1 original zero-fix control; A2 generated zero-fix baseline; source-only
snippet recovery from A2 failures; independent generated-README repair and
fresh B2. Historical B1 is omitted. A1 does not block the A2 repair chain.
MDAnalysis, Sedona and RDPro reruns remain outside the deadline priority package.
The dated 2×2 plan below is retained as history, not the active stage graph.
