# Checkpoint and provider repair, September 7, 2026

## Cause and implemented repair

The previous schema-2 fingerprint recursively hashed the generated `output_dir`
alongside real fixtures. New output files invalidated completed API rows. The
schema-3 fingerprint hashes input bindings only, handles local file URIs, and
retains output-location configuration. Real fixture, source, scaffold, model,
document, environment, and execution-setting changes still invalidate reuse.

Gemini's SDK request timeout and retry settings were correctly configured, but
did not provide an observed total wall-clock bound. New worker invocations use
a 630-second total deadline (300 seconds × 2 configured attempts + 30 seconds)
on the current POSIX main-thread runtime. Deadline expiry unwinds SDK retry
handlers and is recorded as a transient provider error. Other platforms and
non-main threads retain SDK timeouts; an existing application alarm takes
precedence. Request start/completion/failure timing is written to stderr without
prompt or credential content. SDK-internal retry counts and failed-call token
usage remain unknown. This change does not guarantee provider availability or
account quota headroom.

Model, prompts, temperature, execution timeout, scoring, and logical fix budgets
are unchanged. Final A1/A2/B1/B2 still use zero snippet fixes; B document repair
retains deep-dive-first, five document rounds, and two stagnant rounds.

## Evidence-preserving migration

`capture.py` replaces execution with an offline inspection hook: no snippets,
builds, or provider calls. It reconstructs old fingerprints using the effective
configuration and the **inherited setup/freeze environment inventory**, which
is what the existing supervisors supplied. Per-cell inventories remain separate
evidence and are not substituted for that inherited value.

The selection rule is fixed: choose the latest fully attempted legacy group
whose entire fingerprint can be reproduced; if none is fully attempted, choose
the latest reproducible group. Never choose by pass rate or combine outcomes
from several legacy groups. The initial `*_before.json` inspection also records
the first, less useful latest-group-only proposal; the deployed records refer
exclusively to the later `*_validated.json` captures and the rule above.

`install.py` verifies unchanged experimental inputs, saves an immutable copy of
the captured checkpoint prefix, and adds `checkpoint_compatibility.json` beside
the native append-only journal. The record binds exactly one old fingerprint to
the complete new component dictionary and reviewed engine commits. Its copy is
committed under each cell's `docs/eval` directory and in `20260907/` here. New
source/document/configuration/engine changes cannot reuse that authorization.
Provider-error rows are excluded from reuse. Current native terminal evidence
takes precedence. Existing checkpoint events and final results are untouched.

Reused metrics retain their original `evidence_fingerprint`; the final run
records the compatibility record and its SHA-256. Future checkpoint rows also
retain code/round/output details from the execution result. Older rows may lack
those details: a snippet subsequently overwritten by another pass must not be
attributed to an older metric. This is a reporting limitation, not permission to
invent missing execution evidence.

## Deployment and verification

Engine changes: `2b69710` and `985c8f3`, cherry-picked to the six priority A1/A2
worktrees, their three setup/freeze worktrees, the MDAnalysis full1032 freeze,
and the corrected RDPro runner. Historical retained RDPro result trees remain
unchanged. Compatibility records exist for all six current baseline cells.
No running process was stopped, restarted, or duplicated.

All six post-deployment offline captures exactly match their installed expected
components. Twelve focused tests pass, covering output mutation versus real
input mutation, explicit migration scope and engine binding, provider-error
exclusion, request timeout configuration, the shared rate gate, and a hard
deadline escaping an SDK-style retry loop. The corrected RDPro protocol parity
audit passes (`20260907/rdpro_parity_after_repair.json`).

Loaded Python workers do not hot-reload these changes. Existing supervisors
will launch repaired workers on their normal retries; later B workers inherit
the committed implementation. Completed A2 cells are not rerun. Until a new
worker is observed, the repaired resume and deadline behavior is verified
offline and deployed on disk, not claimed active in the old process.

## Recheck at approximately 22:40 PDT

All priority supervisors and existing workers are alive. All four report
observer heartbeats are fresh. The automation observer reports no structural
errors or mutable-path conflicts. The common Gemini request-start gate remains
`/tmp/aideal_google_rate_gate.txt` with three-second spacing; SDK retries are
not independently paced by that gate.

| Cell | Native status at recheck | Provider outcomes still unresolved |
|---|---|---:|
| mir_eval A1 | 148 attempted, 68 pass; partial | 30 |
| mir_eval A2 | Complete, 135/148 pass | 0 |
| Thumbnailator A1 | 149 attempted, 127 pass; partial | 6 |
| Thumbnailator A2 | Complete, 127/149 pass | 0 |
| tslearn A1 | 187/235 attempted, 92 pass; partial | 41 |
| tslearn A2 | Current extra pass progressing; 232/235 terminal rows reusable from the selected verified full group | 3 in selected group |

Counts are a timestamped observation, not final results. mir_eval A1 and tslearn
had recent new checkpoint events. B1/B2 remain pending behind baselines.
MDAnalysis remains an admission waiter; RDPro remains reuse-only and Sedona
deferred. Roughly 36.3 hours remain until Wednesday 11 AM. No defensible full
pipeline ETA exists yet: provider retries and B document rounds are unresolved.
The automatic final package must disclose incomplete cells if necessary.

## Final-report interpretation

Retain this repair record, all fingerprint groups and retries, the original
diagnosis, and the before/after verification. Distinguish provider retries,
document rounds, snippet fix rounds, and diagnostic recovery. Record the
schema/engine transition explicitly. Existing completed schema-2 results keep
their native fingerprints; do not silently label a mixed-schema comparison as
byte-identical. Strict comparison warnings require review against these proofs,
especially the completed Thumbnailator A2 output-inclusive fixture digest,
which is not the same as the selected legacy migration group. This repair does
not itself certify a final matched comparison or causal failure attribution.
