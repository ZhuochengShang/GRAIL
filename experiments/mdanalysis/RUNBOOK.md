# MDAnalysis experiments

The current complete-public-surface A1/A2/B1/B2 protocol is frozen in
`docs/full_1032/FULL_SURFACE_2X2_PLAN.md`. It uses 1,032 unique public names at
1,397 definition sites. The older 171/286/600/661/1,000 artifacts are retained
only as historical or scale-study evidence and are not the denominator of the
full-surface experiment.

## Historical 171-API baseline

Pinned target: MDAnalysis 2.9.0 (`81b8ef51`) with the version-matched
MDAnalysisTests 2.9.0 fixture package. Run in `conda activate geo_llm_spark`.

```bash
aideal prepare-docs
aideal profile
aideal api-surface
aideal intent
aideal intended > docs/qualified_intent_summary.json
```

`aideal intended` is the only paid setup step. It rates the statically eligible
qualified identities with the general intent rubric, groups them into
capability families, and deterministically freezes a diverse top-171 study
sample. `docs/qualified_intent_rankings.json` retains every judgment, score,
rank, exclusion reason, and family; the full public inventory remains separate.

The fixed 171 is a cost-matched representative evaluation sample, not a claim
that MDAnalysis exposes only 171 APIs. A1 and A2 share this frozen denominator
and use the same PSF/DCD fixture, relevant-document retrieval budget, audience
model, zero-round protocol, and five-round recovery protocol.
