# September 7 late-evening runtime check: alive, with a resumability defect

**Remediation update (approximately 22:40 PDT):** the repair is now committed
and deployed for subsequent worker invocations, with verified compatibility
records and preserved checkpoint backups. Existing processes were not restarted.
See [repair evidence and rollout state](checkpoint_repair/README.md). The original
diagnosis below is preserved as the pre-repair observation.

Inspected approximately 22:23–22:27 PDT. This is a diagnosis, not a remediation
or completed-result claim. No active process, checkpoint, fixture, output,
configuration, or result was changed during this inspection.

## Process and report health

Priority supervisors and workers exist. mir_eval A1 and Thumbnailator A1 are
retrying provider failures; tslearn A1 remains in its first full evaluation,
and tslearn A2 is executing another pass. All four report observers exist and
have refreshed heartbeats. A briefly stale data-observer warning cleared on
the next observation. No cross-condition mutable-path conflicts were reported.

Completed cells: mir_eval A2 135/148 pass; Thumbnailator A2 127/149 pass.
At the checkpoint observation, mir_eval A1 had 30 unresolved provider outcomes;
Thumbnailator A1 had 7; tslearn A1 had 39 plus 57 not-yet-attempted APIs.
These are provider-blocked/pending outcomes, not documentation-failure counts.
B1/B2 are still pending. MDAnalysis is an admission waiter. RDPro remains
reuse-only, and Sedona remains deferred.

## Confirmed fingerprint defect

`grail-agent/src/aideal/doc_checks.py:_execute_sample_data` adds `output_dir`
to the available bindings. `_comprehension_fingerprint_components` passes
**all** binding paths to `_sha256_files`, which recursively hashes files in a
directory. Thus generated outputs become part of the purported input identity.
Writing another output can change the fingerprint and prevent checkpoint reuse.

The diagnosis was reproduced without a provider call: construct the fingerprint
from current source/config/document/scaffold and the inherited supervisor
environment inventory, then compare inclusion/exclusion of `output_dir`.

| Cell | Initial fingerprint prefix, reproduced with input-only bindings | Current fingerprint prefix, reproduced with output directory included | File count: input-only / with outputs |
|---|---|---|---|
| tslearn A2 | `b5b9bb6530` | `b3a7e6316e` | 1 / 18 |
| Thumbnailator A1 | `15c376d07a` | `6361a90a8d` | 3 / 7 |

Both reconstructed hashes exactly match preserved checkpoint fingerprints.
tslearn A2 has four completed 235-event passes under different fingerprints
and a fifth in progress. Thumbnailator A1 has three fingerprints; A2 has two.
The differing output-directory hashes explain rejection of earlier checkpoints
in the reproduced cases. This is not a duplicate-supervisor/path-ownership bug.

The environment hash used by the current workers is inherited from the outer
supervisor's setup/freeze inventory, not the per-cell inventory: reconstructing
with the setup/freeze hash matched the checkpoints; using the cell inventory
hash did not. Preserve that provenance distinction when reviewing validity.

## Remediation boundary and reporting

Unresolved. Correct the fingerprint contract to hash declared immutable input
fixtures separately from mutable output paths. Keep output location in the
execution configuration. Validate consistent behavior across all study cells,
including the corrected RDPro runner. Preserve old fingerprint groups and
attempts; do not relabel historical successes as newly executed measurements.
Any compatible-artifact migration requires an explicit provenance mapping and
evidence that actual source/document/input/harness/model semantics match.

Applying an engine change in place would itself change recorded engine hashes
and cannot be treated as a transparent hot fix to already loaded workers. The
current no-restart/no-delete instruction remains in effect. No silent engine
patch or checkpoint migration was applied during this status check.

The automatic observers continue publishing. Whole-pipeline completion by
Wednesday 11:00 AM remains unverified; repeated full passes and provider 504s
are material deadline risks. Being alive does not mean every stage is healthy.
