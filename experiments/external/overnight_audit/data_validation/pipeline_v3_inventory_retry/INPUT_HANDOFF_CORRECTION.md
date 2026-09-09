# Verified A2 input handoff before README repair

September 8 operational correction, applied before the first successful document-worker invocation.

The live check found that `fix-docs --from-results docs/eval/A2/comprehension.json`
and `--report docs/eval/B2/docfix.json` are resolved from the worktree root,
whereas the driver stores them under the experiment directory. mir_eval's first
invocations failed before any model call.

`experiments/external/docfix_input_handoff.py` now waits for each controller to
create its B2 worktree and inherit the exact complete A2 result. It creates an
A2-only failure log for the B2 document worker, records the source/result/script
hashes and path mapping, and then releases a worktree-local `docs/eval` symlink
to the owned experiment directory. Inputs and outputs resolve to the intended
paths. No pipeline or model worker is restarted, and no S_A2 diagnoses or fixes
are supplied to the independent document arm.

The deterministic helper owns `pipeline_v3/input_preparation`, uses no Gemini
calls, runs the same checks for all three repositories, and commits only the
alias/proof on each B2 branch. Its controller remains resumable until all three
handoffs are prepared. Native B2 completion will push those B2 branch commits.

[Live per-repository handoff proof](input_preparation/status.json) is authoritative
for whether seeding is prepared. Earlier static HTML caveats say initial error
seeding is unverified; this new proof supersedes that caveat only for repositories
marked `prepared`. The append-prefix hash verifies the seed survives subsequent
error-log appends. Retained scripts with no historical full-byte association are
still labeled `retained_unbound_legacy`; missing/colliding snippet evidence is
explicit. This correction does not certify native assertions or remove the
legacy document-round restart limitation.
