# Reviewing and improving agent readiness

AIDEAL's central output is an evidence-backed readiness assessment and a
reviewable improvement queue. The existing executable 2×2 study measures
documentation-conditioned API use. Discovery, independent setup, multi-API
workflow completion and agent recovery remain separate evaluation needs.

## Open the report

In the report root, open `AIDEAL_REPORT.md`, then
`data_validation/readiness/ASSESSMENT.md`. Each suggestion links to the native
ledger and saved evidence, states diagnosis confidence, proposes an action,
and defines validation. No composite readiness score is invented from partial
dimensions. Partial-cell pass counts remain provisional with full denominators.

`assessment.json` and `improvement_queue.json` are machine-readable. Cards use
stable IDs and evidence versions; `decisions.jsonl` preserves review history
independently of report regeneration. Accepted or deferred decisions are
marked stale when the current evidence changes. A vanished failure card is
not automatically credited as a successful improvement.

## Commands

Run from the AIDEAL repository with its existing Python environment. Paths
below are supplied by the operator; no machine-specific location is built in.

```bash
env PYTHONPATH=grail-agent/src:. python -m experiments.external.readiness \
  --report-root /path/to/report publish

env PYTHONPATH=grail-agent/src:. python -m experiments.external.readiness \
  --report-root /path/to/report review --decision /path/to/decision.json
```

`publish --watch` refreshes every minute and owns a dedicated process lock.
The publisher writes only the new central index and `data_validation/readiness`.
It makes no provider calls, executes no generated tests, and modifies no
experiment or native result. The existing data observer's deadline copy
includes this directory. Its decision log and snapshots travel with the report.

## Review sequence

1. Inspect a suggestion and its evidence. A human or agent can propose a
   concrete plan. This is separate from the generic suggested action.
2. The human reviews the plan and chooses a human or agent executor.
3. The selected executor implements the authorized work in an isolated branch
   or diagnostic directory using existing tools. This CLI records decisions;
   it does not launch an implementation agent or treat a record as authenticated
   permission. An operator still follows actual user authorization.
4. The executor submits change, validation, and before/after comparison files.
   The CLI saves immutable content-hashed copies. Validation status is a
   submitted claim for review, not an independently recomputed test result.
5. The human accepts the submitted work or requests changes. Acceptance never
   changes baseline scores. A measured benefit needs an independently validated,
   appropriately matched re-evaluation; an investigation can be accepted even
   if it establishes that no codebase change is warranted.

Actor labels are supplied by the operator, not verified identities. The local
decision log is an audit record with consistency checks, not an access-control
or tamper-proof system. Policy-based automatic approval is not implemented.

### Propose a concrete plan

Use the current card's actual ID and full evidence version. Example structure:

```json
{
  "id": "<current suggestion ID>",
  "evidence_version": "<current evidence hash>",
  "action": "propose",
  "actor": "Codex",
  "actor_type": "agent",
  "note": "Source review identifies an input format omitted from the example.",
  "plan": {
    "summary": "Document the required two-column key format and add a valid example.",
    "files": ["<exact proposed documentation path>"],
    "validation": "Check the example against pinned source and run an isolated reader test; preserve native A2 results.",
    "risks": "A corrected document creates a new treatment and needs a separate comparison.",
    "isolation": "Use a new improvement branch; do not edit the active measured worktree."
  }
}
```

### Review the plan

Keep `id` and `evidence_version`, set `action` to `approve_plan`, record the
actual human actor with `actor_type: human`, a review note, and
`executor: human` or `executor: agent`. The current state must be `proposed`.
An agent proposal is not automatically a human approval.

### Submit and review the result

The assigned executor uses `action: submit_result` and includes:

```json
{
  "validation_status": "passed",
  "change": "/path/to/change.diff-or-investigation.md",
  "validation": "/path/to/validation-evidence.json",
  "comparison": "/path/to/before-after-comparison.md"
}
```

Place that object under `result`, alongside ID, evidence version, actor,
actor_type and note. The human can then record `accept_result`. Use `defer`,
`reject`, or `request_changes` to record alternatives. A revised plan uses
`propose` again, which clears previous implementation approval and submitted
result state for that evidence version. All earlier events remain in the log.

## Development and boundaries

The modules separate pure assessment (`model.py`), review state (`review.py`),
report rendering (`report.py`), and command/lock ownership (`__main__.py`).
The adapter consumes existing report artifacts; it does not require a checkout
at a particular home directory. This command uses Unix file locks. Existing
source/fixture paths in historical evidence can still refer to the old machine.

```bash
env PYTHONPATH=grail-agent/src:. python -m pytest -q \
  experiments/external/readiness/test_readiness.py
```

Future evaluations should add independently checked inputs/oracles and held-out
workflows. Packaging, API/code design, fixture, and documentation improvements
must be versioned and evaluated separately so their effects remain attributable.
