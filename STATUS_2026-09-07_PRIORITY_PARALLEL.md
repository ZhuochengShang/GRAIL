# AIDEAL priority parallel handoff — September 7, 2026

Deadline: Wednesday September 9 at **11:00 AM America/Los_Angeles**.
This memo supersedes the serial admission order in the earlier overnight plan.

## Deadline scope

- mir_eval: 148 APIs, A1/A2/B1/B2.
- Thumbnailator: 149 APIs, A1/A2/B1/B2.
- tslearn: full 235 APIs, A1/A2/B1/B2.
- Detailed result, failure, provider-attempt and document-repair report for those three.
- MDAnalysis full1032, Apache Sedona preparation, and RDPro reruns can wait.

The user approved parallel priority execution after the initial instruction to
preserve running jobs. Only the two idle waiting supervisors were gracefully
replaced: Thumbnailator 84375/84379 and tslearn 96398/96405. The active mir_eval
supervisor 84228, driver 84232 and A1 worker 962 were left untouched. No paid
checkpoint or result was deleted. Exact old plans, states, logs and waiting
stdout are under `.aideal_exec/priority_admission_20260907/*_before`.

The two admission-only migrations retain the same state paths/job identities,
preserve attempt counters, record the old plan hashes, and bind the saved state
to the new plan hash. The old queued-wait attempt is not a comprehension retry.
The replacement supervisors started at 14:15 on September 7.

## Concurrency and resumption

All 12 priority cells have distinct physical worktrees, documents, checkpoints,
execution directories, output directories and error logs. The checked layout
contains 60 unique mutable paths; its complete inventory is at
`.aideal_exec/priority_admission_20260907/layout.json`.

Every priority watchdog uses `/tmp/aideal_google_rate_gate.txt` and a three-second
request-start interval. The gate uses an exclusive process-shared file lock.
A four-process regression test confirms serialized starts. Each repository's
own scheduler also avoids simultaneous jobs in the same worktree.

The gate coordinates application request starts. Gemini-internal retries and
token quotas are not measured by this gate. Provider 429/504 failures remain
transient, retain their evidence, and cannot satisfy completion predicates.
No model, prompt, source, fixture, evaluation engine or scoring fingerprint was
changed during admission. Final evaluations remain zero code-fix rounds;
document repair retains five rounds maximum, two stuck rounds, no separate
retry rounds, followed by a fresh zero-round measurement.

MDAnalysis's already-waiting process is retained. Its future pipeline entry
now additionally waits for **all three** priority repository success states,
so tslearn finishing early cannot admit MDAnalysis ahead of mir_eval or
Thumbnailator. Sedona remains deferred. The RDPro entry point checks the
committed reuse-only policy before launching paid work, including the old
already-queued command. That policy hashes retained historical results and
does not claim they form a matched four-cell experiment.

## Current evidence and errors

- mir_eval A2 is complete: 135/148 pass, 13 native runtime failures, zero
  unresolved provider failures. It is committed on its own condition branch.
- mir_eval A1 has 148 checkpoint identities, but 32 provider-error APIs remain
  unresolved on its third invocation. The second invocation recovered only
  two of 34 provider-error APIs. All 32 remaining provider errors had a short
  missing-documentation message as relevant context; this is correlation,
  not evidence that documentation caused the provider errors.
- Thumbnailator A1/A2 and tslearn A1/A2 generation have started concurrently.
- tslearn validation passes: 235 unique names / 343 definition sites.
- MDAnalysis validation passes: 1,032 names / 1,397 sites / 492 fixtures.
- Existing nested supervisors inherit the outer environment fingerprint,
  rather than hashing each child's inventory into the recorded fingerprint.
  The observer separately preserves and compares per-cell inventory contents;
  this provenance limitation must be reported rather than silently repaired
  in already-running measurements.
- The native Python classifier can call a wrong package member/import an
  infrastructure failure. The audit distinguishes API identity errors from
  genuine absent third-party dependencies; native scores remain unchanged.
- Five mir_eval A2 failures first encountered an absent supplied output
  directory. The identical snippets for first_n_three_layer_P, load_tempo and
  load_valued_intervals pass when only that directory binding is corrected in
  isolated diagnostic copies. load_key then exposes a format error, and
  load_wav then exposes a wrong sample-value assertion. These diagnostics are
  not new headline evaluations or credited document repairs.
- Source review verifies a generated-document semantic error for ticker_pitch
  and an upstream implementation/doc mismatch for the ragged-series header
  flag. Hash-bound annotations for all 13 A2 failures are committed under
  `experiments/external/failure_reviews/mir_eval_A2.json`.

## Report delivery

`experiments/external/audit_overnight.py` is a passive observer. It never
launches, terminates or restarts experiment jobs and writes only to a separate
`aideal/overnight-evidence-audit` worktree. It records every manifest API,
checkpoint attempts across fingerprints, provider-error attempts, document
rounds, failure evidence, source paths, branches, commits and environment
inventories. Provider-internal retry counts that were never logged remain
unknown, not zero. Native resumed JSON runtime/usage covers its last invocation;
the full attempt history is retained separately.

The observer refreshes reports every minute and commits changed reports every
15 minutes. `DETAILED_PRIORITY_REPORT.md` links the three detailed reports and
per-cell JSON/CSV ledgers. At or after **10:45 AM Wednesday**, it freezes a
self-contained deadline snapshot while retaining the continuously updated
live report. A partial run remains explicitly partial at that cutoff.

## Deadline assessment

Parallel admission removes the previous serial bottleneck and gives the three
priority studies approximately 44 hours from the migration. This materially
improves the schedule, but completion cannot honestly be guaranteed: mir_eval's
repeated 504s have not recovered reliably, and B1/B2 document repair duration
is not known until the baselines finish. Preserve full denominators and
completion predicates; do not hide provider errors or substitute repair
success unions to manufacture a Wednesday result.
