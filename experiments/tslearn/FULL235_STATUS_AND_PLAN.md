# tslearn corrected full-surface 2x2

## Frozen scope

This experiment is independent of the July 99-name semantic-subset evidence.
It evaluates every unique bare public API name discovered by the corrected
AST-backed scanner at upstream commit
`f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7`.

- 343 public definition sites collapse to 235 unique bare API identities.
- No sampling or intended-API filter is used (`surface_filter: all`).
- The manifest is `docs/eval/api_manifest.json`.
- A1/A2/B1/B2 share the same manifest, scaffold, fixture, interpreter,
  source commit, relevant-document cap, and zero snippet-fix evaluation rule.

### Why the count changed from 245 to 235

The historical regex scanner leaked ten nested/local implementation functions:
`cb_`, `f`, `format_to_tslearn`, `metric_fun`, `of`, `sklearn_metric`,
`transpose_or_expand`, `transpose_or_flatten`, `wrapper`, and `y`.
The corrected scanner removes exactly those ten and adds no names. Reintroducing
them would reproduce a known parser bug rather than test public APIs.

## Cells and isolation

| Cell | Branch | Worktree | Documentation |
|---|---|---|---|
| Freeze | `aideal/tslearn-full235-freeze` | `GRAIL_tslearn_full235_freeze` | immutable setup |
| A1 | `aideal/tslearn-full235-A1` | `GRAIL_tslearn_full235_A1` | pinned original docs |
| A2 | `aideal/tslearn-full235-A2` | `GRAIL_tslearn_full235_A2` | generated README before repair |
| B1 | `aideal/tslearn-full235-B1` | `GRAIL_tslearn_full235_B1` | original docs plus created repair entries |
| B2 | `aideal/tslearn-full235-B2` | `GRAIL_tslearn_full235_B2` | repaired copy of A2 README |

Each cell has unique `docs/eval/<cell>`, `logs/eval/<cell>`, and
`.aideal_exec/<cell>` paths. Branches are committed and pushed only after their
completion predicate, per-function analysis, and required test gate succeed.

## Dependency graph

```text
freeze + manifest + common harness
          |
          +-- A1 tests-before -> A1 zero -> tests-after ----------+
          |                                                       |
          |                                               B1 deep repair
          |                                                       |
          |                                      B1 fresh zero -> tests-after
          |
          +-- A2 tests-before -> README -> A2 zero -> tests-after-+
                                                                  |
                              B1/B2 tests-before -> B2 deep repair
                                                                  |
                                                 B2 fresh zero -> tests-after
```

The watchdog may run A1 alongside A2 generation, then A2 evaluation. B1 and
B2 repair/evaluation lanes run concurrently after their respective baselines.
All Gemini request starts share a process-safe three-second rate gate. Provider
requests are bounded at 300 seconds with two provider retries. Comprehension
uses fingerprinted per-API `--resume`; README generation and doc repair also
persist after every API.

## Evidence produced per cell

- Environment inventory and its hash
- PASS_TO_PASS-before and PASS_TO_PASS-after output and exact exit status
- Generated README state/result where applicable
- Zero-round comprehension JSON with 235 metrics and no transient LLM errors
- Per-function CSV, JSON, and Markdown failure analysis
- Doc-repair JSON plus per-round diagnoses for B1/B2
- Git commit and remote branch

Historical files in `GRAIL_tslearn_A1` and `GRAIL_tslearn_A2` are never read,
rewritten, cleaned, or used as resume checkpoints.

## Wednesday risk

This is materially larger than the 99-name run. The required paid workload is
at least 235 A2 author calls plus 940 zero-round audience calls, before any B1
or B2 repair/deep-dive calls. Historical tslearn calls commonly took 10–50
seconds, with occasional five-minute provider timeouts. A realistic unattended
wall-clock range is roughly 18–36 hours if Gemini is stable, and 36–60 hours
if many APIs enter multi-round repair or provider retries. Starting by early
Monday leaves a plausible Wednesday finish, but it is not guaranteed. The
watchdog prioritizes preservation and exact resumption over silently skipping
slow or failing APIs.
