# Local Experiment Tracking

Baseline/root branch:

- `exp/root-before-api-cards`
- tag: `exp-root-before-api-cards`
- commit: `6cffc2c Establish AIDEAL RDPro experiment baseline`

Clean active experiment worktree:

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_api_cards
git branch --show-current
```

Current active branch:

- `exp/current-experiment`

This branch starts from `exp-root-before-api-cards` and is where unfinished experiments should continue. Commit each feature/evaluation step here or branch from here.

Important:

- Do not use `/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL` for new feature work right now; it still has old unstaged deletions and leftover run artifacts.
- Keep `exp/root-before-api-cards` as the fixed baseline, not a working branch.
- For each new measured feature, create a branch from the clean worktree:

```bash
git switch -c exp/api-cards-static-v1
# implement feature + run tests + save metrics
git add <files>
git commit -m "Add static API cards v1"
```

Useful checks:

```bash
git status --short
git log --oneline --decorate -n 5
git branch -vv
git worktree list
```
