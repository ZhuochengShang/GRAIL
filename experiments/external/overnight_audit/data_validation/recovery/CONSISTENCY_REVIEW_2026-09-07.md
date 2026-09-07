# September 7 consistency review and recovery addition

Read-only inspection preserved active workers, supervisors, checkpoints and
watchdog plans. This review changes reporting and adds a staged extension;
it does not claim that unfinished final cells are valid completed comparisons.

| Repository | Frozen names | Four final snippet budgets | B doc budget / stagnation limit | Execution timeout per final cell | Audit result |
|---|---:|---|---|---|---|
| mir_eval | 148 | 0 / 0 / 0 / 0 | 5 / 2 | 600 s | Frozen non-document settings match; final comparison partial |
| Thumbnailator | 149 | 0 / 0 / 0 / 0 | 5 / 2 | 600 s | Frozen non-document settings match; final comparison partial |
| tslearn | 235 | 0 / 0 / 0 / 0 | 5 / 2 | 300 s | Frozen non-document settings match; final comparison partial |

Both priority drivers explicitly launch deep-dive-first document repair with
zero snippet retries, followed by fresh final evaluations. B1 uses original
documentation plus repaired supplemental entries; B2 uses the repaired generated
document. Timeouts are matched within each repository. Repository-specific
environments/data differ, so do not pool percentages or timing as interchangeable
measurements. The original serial admission note is superseded by the September 7
parallel-priority instruction; the active watchdog plans reflect that instruction.

The [machine-readable snapshot](audits/2026-09-07/protocol_audit_and_queue.json)
checks all four frozen effective YAML configurations per repository, including
models, execution settings, context budget, profile and audience prompt hashes.
Existing worker effective configurations match their freezes. The input observer
reports no pinned-input failures for the six existing A-cell worktrees, with
limitations; some supplied output directories do not exist. The ownership
observer reports zero cross-condition mutable-path conflicts. These are timed
observations, not guarantees about future outputs or every generated assertion.

All three priority watchdog plans share the same Google request-start gate and
three-second interval. This spaces application calls; it does not prove absence
of token-quota contention or account for every provider-internal retry.
mir_eval A1 still has unresolved provider outcomes. B results and post-treatment
validation are pending, preventing certification of the final 2x2 comparisons.

Report corrections:

- Separate document-round budgets from zero code-round headline evaluations.
- Keep unresolved provider failures partial; do not manufacture a completed
  cell by excluding them from its scored denominator.
- Preserve native errors separately from evidence-backed causal review.
- Report common-denominator raw and paired effects alongside scored percentages.
- Record stagnation detection as a heuristic, including rejected rewrites.
- Report the new feedback/source recovery experiment separately, with matched
  failure sets, thresholds and budgets, plus diagnosis cost and semantic review.

The new recovery implementation is staged and tested with fake provider/harness
calls. No live recovery job or new provider request was launched. Thirteen
mir_eval A2 failures have paired candidate entries at snapshot time. Missing
cells do not contribute candidates, and the candidate list must be refreshed
after all priority results and their validation reports finish.

Two is not a measured optimum. The historical RDPro B2 report has five APIs
stopped after two rejected document rewrites and lacks their third attempts.
The full five-round pilot and threshold-2/3 sensitivity design are described in
[the recovery note](README.md). Existing live thresholds remain unchanged.
