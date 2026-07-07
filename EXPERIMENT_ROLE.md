# Worktree Role: Original Design Baseline

Branch: `exp/design-baseline`

Purpose: preserve the baseline design before new API-card/retrieval features.
This branch is for the original pipeline design and reference artifacts:

1. init/profile
2. API surface
3. intent selection
4. duplicate/redundancy removal (`aideal dedup`)
5. LLM README generation
6. full flat README and catalog/index README artifacts

Do not run mutating experiments here except to regenerate the original baseline artifacts intentionally.

Important README snapshots:

- Current tracked `experiments/rdpro/docs/LLM_readme.md`: clean generated README in the root baseline, no `doc-repaired from source` markers, but currently only 67 entries.
- `experiments/rdpro/docs/LLM_readme.baseline_docfix_20260708.md`: 205 entries, but includes one early `compress` docfix marker.
- Old dirty-tree snapshot, not in this clean worktree: `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/archive/20260707_001443/LLM_readme.md` has 218 entries and no docfix markers.

If you need a pure post-dedup full README, regenerate it here with the author model and record the output before running any comprehension/docfix:

```bash
cd experiments/rdpro
aideal api-surface > docs/api_surface.txt
aideal intent --all > docs/intent_all_nollm.json
aideal dedup --out docs/dedup_report.json
aideal readme --generate --limit 0 --force > docs/readme_generate_original_design.json
aideal catalogue
cp docs/LLM_readme.md docs/LLM_readme.original_design_full.md
```
