# Independent repository scheduling

September 8 user-authorized scheduling amendment, before any S_B2 execution.
This replaces the earlier all-repository priority barrier. Measurement rules,
model roles, prompts, manifests, data, harness, five new source proposals and
stuck-two rules are unchanged.

- Each repository retains A2 → initial source pass → independent README repair
  → fresh B2 → S_B2 dependencies. There is no A1 dependency for repair.
- Completed B2 admits that repository to S_B2 even if another repository has
  incomplete A2/B2 or the same repository has residual source-provider failures.
- Residual S_A2 provider failures resume the original batch and per-case
  checkpoints after that repository's B2, independently of its A1 control.
  Existing source locks prevent duplicate case execution if the original
  controller later reaches its old retry loop.
- Repositories take turns through one shared supplemental admission slot.
  A caller holds `/tmp/aideal_google_recovery_admission.lock` throughout its
  operation; a second caller cannot acquire it. The slot is released on exit,
  not by an expiring lease while a request might still be running.
- The admission check reserves two native callers for each repository before
  B2 completion and one afterward (A1 or its sequential old source-retry loop).
  With the supplemental slot, the configured ceiling is six model-calling
  processes in this three-repository study. It is a conservative local policy,
  not an asserted Gemini account quota and does not govern unrelated clients.
- Every application request still uses the existing three-second Google
  request-start gate. This is not full TPM/RPD accounting. SDK-internal retries
  are not individually admitted or fully visible; no stronger claim is made.
- Source retries persist a 300-second cooldown. Native results and S_A2
  checkpoints are reused, never reset. S_B2 retains a separate cohort/output.

`admission.py:slot` implements the shared supplemental slot and native capacity
reservation. `source_retry.py:run` resumes the original S_A2 batch. The updated
`__main__.py:main` admits ready repositories independently and preserves pending
repositories in the report. The active plan is
`experiments/external/post_b2_independent_watchdog.yaml`.

Only the idle old post-B2 scheduling service is handed off. Existing v2
controllers, model workers, deadline reporters and assertion replay remain
running. The saved handoff record binds the old/new scheduler identities and
verifies no S_B2 cases existed before replacement. New S_B2 preflight validated
all 11 mir_eval and 10 Thumbnailator eligible failures without provider calls.

The 10:15 AM Wednesday cutoff applies to admission of new work; it does not kill
an active request. Results remain separate and the 10:45 AM snapshot can be partial.
