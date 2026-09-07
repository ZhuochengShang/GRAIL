# AIDEAL automation extensions

The current protocol and active supervisors are unchanged. These modules
separate passive study observation from opt-in future execution components.

| File | Responsibility |
|---|---|
| `observe.py` | Passive report collection, resolved YAML/profile/inventory bundles, AST evidence, health and exclusive output ownership |
| `analysis.py` | Pure scoped forecasts, candidate failure classification, path overlap checks |
| `contracts.py` | Offline input-metadata contracts and conservative Python AST review |
| `quota.py` | Local SQLite quota admission core, no SDK or provider calls |
| `next_protocol.yaml` | Disabled example; actual quotas and transport integration remain required |
| `PROMPTS_NEXT_PROTOCOL.md` | Future generation/review prompts; not used by active experiments |

From the repository root, use the Python environment that already runs AIDEAL:

```bash
env PYTHONPATH=grail-agent/src:. python -m experiments.external.automation.observe \
  --workspace-parent /path/to/worktree-parent \
  --report-root /path/to/audit-worktree/experiments/external/overnight_audit
```

Add `--watch` for 60-second refreshes only after checking the output lock and
heartbeat. One observer owns `data_validation/automation`; it writes no other
namespace and never calls providers, executes snippets, or changes jobs.
The existing data observer includes this directory in its deadline snapshot.
The existing report observer commits files under the report root periodically.

Results: `AUTOMATION_STATUS.md`, `deadline_forecast.json`,
`failure_review_queue.json`, `health.json`, and per-cell configuration/AST
evidence. Redacted resolved configs are accompanied by hashes of the effective
configuration; recorded environments are not fresh worker attestations.
The profile is resolved from `files.project_profile`, including tslearn's
full235 profile, rather than assuming `project_profile.yaml`.

Forecasts use the latest 30 compatible attempt durations and observed terminal
fraction. Five timing samples are required. No recent terminal outcomes means
stalled/unknown, never zero remaining time. Optimistic/likely/conservative are
sensitivity scenarios, not confidence intervals. They exclude generation,
repair, future B runs, final tests, and unobserved queue/cooldown changes.

The quota core must remain disabled until a transport adapter reserves every
actual attempt, including retries. Configure shared scope/limits from the
actual provider project, supply an input-token upper bound, reconcile usage,
handle provider cooldowns and applicable spend limits, and bound retries.
Active leases do not auto-expire: a hung request must not silently free a
concurrency slot. Dead-owner reconciliation needs process evidence. All local
workers in a scope must share one SQLite file and identical policy. This is
not a distributed scheduler and is not wired to active Gemini clients.

Input metadata matching and static assertions are preliminary checks. Do not
credit them as independent semantic validation. Complete per-API contracts,
runtime target/dataflow evidence and reference/metamorphic oracle validation
are future protocol work. The supplied prompt defines the required review
evidence without exposing source-informed review to audience generation.

```bash
env PYTHONPATH=grail-agent/src:. python -m pytest -q \
  experiments/external/automation/test_automation.py
```

Tests use temporary databases and processes, make no model calls, and do not
touch experiment artifacts. The observer requires Unix `fcntl`; the pure
helpers and quota core have no machine-specific paths. Existing study configs
still need explicit environment provisioning/rebasing for a new machine.
