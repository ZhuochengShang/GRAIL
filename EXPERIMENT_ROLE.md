# Worktree Role: Feature Development - API Cards

Branch: `exp/feature-api-cards`

Purpose: implement feature changes such as static API cards / structured codebase facts.

Target feature idea:

```json
{
  "api": "mapPixels",
  "owner": "RasterOperationsGlobal",
  "receiver_type": "RasterRDD[Float]",
  "call_style": "extension_method",
  "required_imports": ["edu.ucr.cs.bdlab.raptor._"],
  "input_bindings": ["rasterRDD"],
  "known_passing_sibling": "filterPixels",
  "forbidden_patterns": ["GeoJob.mapPixels", "rasterRDD.first()._1"]
}
```

Implementation should be mostly static/mined, not LLM-heavy:

1. owner/class extraction,
2. signature type and import extraction,
3. receiver/call-style inference,
4. fixture binding mapping,
5. known passing sibling from tests/logs,
6. forbidden patterns from repeated failures.

After implementation, test locally here, then use the experiment runner worktree to quantify it:

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_exp_runner
git switch -c exp/run-api-cards-v1 exp/experiment-runner
git merge --no-ff exp/feature-api-cards
# run g1/g2/g4/puzzle and compare against baseline
```

Keep this branch focused on code/features. Do not store large run outputs here unless they are small curated reports needed for review.
