# Current AIDEAL pipeline: A2-only repair v2

This is the active report entry point for the September 9, 11 AM Pacific deadline.
The user omitted original-README repair on September 8. Historical B1 is omitted,
not pending; older four-cell dashboards retain the previous protocol view.

A1 uses original documentation with zero fixes. A2 uses generated documentation
with zero fixes. A2 failures feed source-only snippet recovery (up to five new
proposals, stuck threshold two) and an independent generated-README repair loop
(up to five document rounds), followed by fresh zero-fix full-manifest B2 tests.
A1 continues in parallel and does not block A2 repair.

| Repository | Current HTML | Status and machine-readable evidence | Configured watchdog |
|---|---|---|---|
| mir_eval, 148 APIs | [Report](mir_eval/REPORT.html) | [Status](mir_eval/STATUS.md), [JSON](mir_eval/live.json) | [YAML](plans/mir_eval.yaml) |
| Thumbnailator, 149 APIs | [Report](thumbnailator/REPORT.html) | [Status](thumbnailator/STATUS.md), [JSON](thumbnailator/live.json) | [YAML](plans/thumbnailator.yaml) |
| tslearn, 235 APIs | [Report](tslearn/REPORT.html) | [Status](tslearn/STATUS.md), [JSON](tslearn/live.json) | [YAML](plans/tslearn.yaml) |

[Exact design and diagram](PIPELINE_V2.md) · [Report template](REPORT_TEMPLATE_V2.md)
· [Registered policy](protocol.yaml) · [Controller activation evidence](ACTIVATION.json)
· [Data, samples, formats and API-test methods](../FINAL_REPORT_DATA_AND_API_METHODS.md)
· [Native versus assertion replay](../assertion_replay/REPLAY.html)
· [Readiness assessment and human review queue](../readiness/ASSESSMENT.md)

Each repository refreshes its report every 30 seconds. Per-API source recovery
histories are exported to `source/cases/`; native B2 document rounds and fresh
results retain their own worktree provenance. The original four API workers were
preserved during controller replacement. The isolated Thumbnailator replay
remains a live watcher; its historical B1 placeholder is not part of v2 completion.

Preflight validated all 13 mir_eval and 22 Thumbnailator A2 eligible failures;
tslearn passed isolated runtime/import checks while its A2 measurement remained
incomplete. These are input/runtime checks, not additional API passes. The first
mir_eval controller invocation failed in the legacy Git path adapter before
model calls; its automatic retry used the corrected adapter.

Native passes, assertions-on replay acceptance and independently reviewed
correctness remain separate. Neither source recovery nor replay alone certifies
the entire documentation-repair pipeline. Legacy script binding and output-state
limits remain in the evidence. Provider availability still prevents a guaranteed
finish time; the 10:45 AM Wednesday snapshot includes partial results honestly.
MDAnalysis, Sedona and RDPro reruns remain deferred from this priority package.
