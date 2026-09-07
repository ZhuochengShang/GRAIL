# Accepted study policy: consistent with corrected RDPro logic

User decision September 7: keep two stagnant rounds and prioritize consistent
experiments using the same logic as RDPro. No threshold-sensitivity run is
scheduled. Existing processes, plans and checkpoints remain unchanged.

| Stage | Shared rule |
|---|---|
| A1 | Original documentation; fresh audience test; zero snippet fixes |
| A2 | Generated documentation; fresh audience test; zero snippet fixes |
| B1 treatment | Start from A1 failures; source deep dive, diagnosis, rewrite, execute; at most 5 document rounds, 2 stagnant rounds, 0 snippet retries; create missing entries when needed |
| B2 treatment | Start from A2 failures; the same repair loop and budgets |
| B1/B2 final tests | Fresh audience evaluations on repaired documents; zero snippet fixes; never a union of intermediate repair successes |
| Comparison | Same per-repository manifest, source, inputs, harness, models, context scope and timeout; per-API provenance and failure/round accounting |
| Separate staged recovery | Both feedback and source-assisted modes use 5 code proposals and the accepted threshold 2; documents/harness/fixtures/source stay fixed; no headline score changes |

The [static parity evidence](audits/2026-09-07/rdpro_protocol_parity.json) passes:

- The corrected RDPro runner, mir_eval/Thumbnailator driver, tslearn driver,
  and queued MDAnalysis baseline/repair YAML all contain the same literal
  relevant-scope, zero-final-fix, deep-dive-first, 5/2/0 repair limits.
- The six existing priority A-cell workers and their three setup/freeze
  worktrees, plus MDAnalysis's freeze, match the corrected RDPro implementation
  of `doc_fix_run`, `deep_dive_run`, `_diag_sig`, `_err_sig` and
  `_comprehension_execute`, compared as Python syntax trees.
- Repository datasets/languages/API counts differ by design. Timeouts remain
  matched within a repository (600 seconds for RDPro/mir_eval/Thumbnailator,
  300 for tslearn). Shared logical protocol does not mean identical data.

This verifies selected source implementations and declared launch settings.
It does not certify uncompleted B results, source/data suitability for every
API, or all runtime behavior. Existing final-report gates still apply.

## Historical RDPro boundary

The retained `GRAIL_rdpro_final_B1` and `GRAIL_rdpro_final_B2` worktrees use an
earlier engine. Their deep-dive and diagnosis/error-signature functions match,
but the corrected engine adds B1 missing-entry identity preservation on resume,
stronger comprehension fingerprints, retry handling for provider failures,
more retained error evidence, and Java/Spark harness support. These are recorded
version differences, not an excuse to rewrite old evidence.

Historical A1/A2 fix5 and the July-8 31-attempt stress tests remain separate.
They cannot replace a zero-round cell or establish a newly matched cross-repo
comparison. RDPro reruns remain deferred/reuse-only.

The staged recovery code is a separately named extension, not a claim that
historical RDPro already ran this exact paired feedback/source protocol.
The study adapter rejects a threshold override of 3 before input processing
or model calls. The generic state-machine tests may still exercise other
thresholds to verify correctness for future protocols.

Recheck without importing or executing any pipeline:

```bash
env PYTHONPATH=grail-agent/src:. python -m experiments.external.check_rdpro_protocol \
  --main-worktree /path/to/GRAIL_rdpro_puzzle_aideal \
  --out /new/path/rdpro_protocol_parity.json
```

The output file must be new so prior evidence is preserved. Changed or missing
implementations/declared limits fail the check. New B worktrees must also pass
the existing four-cell result, source, environment and data-validation gates.
