# Worktree Role: Experiment Runner

Branch: `exp/experiment-runner`

Purpose: run quantified experiments only. Keep feature/code changes out of this branch unless they are imported from a feature branch/commit for measurement.

Experiment groups:

- g1: flat full README comprehension.
- g2: catalog/index/class-context README comprehension.
- g3: dedup/fresh generated README condition.
- g4: rerun failures with fix loop.
- fix-docs: source-aware doc repair.
- puzzle: integration puzzle tests.

Use this tree to compare:

1. entire flat README vs catalog/index README,
2. no fix vs bounded fix vs fix-all,
3. original design vs API-card branch by merging/cherry-picking the feature branch into a new measurement branch.

Typical commands from `experiments/rdpro/`:

```bash
python gemini_suite.py --dry-run --stages g1,g2,g3,g4
python gemini_suite.py --stages g1,g4
python gemini_suite.py --stages g2,g4
python bench_conditions.py --table > docs/backend_comparison_table.txt
```

For a feature comparison:

```bash
git switch -c exp/run-api-cards-v1 exp/experiment-runner
git merge --no-ff exp/feature-api-cards
# run g1/g2/g4/puzzle and save result files
```

Rules:

- Do not run two conditions in parallel in this same worktree; `.aideal_exec` and `logs/error_log.jsonl` are shared.
- Archive result JSONs before clearing logs.
- Keep command lines in `RUNBOOK.md` or a new `docs/*comparison*.md` report.
