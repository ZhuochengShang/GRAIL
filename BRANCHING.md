# GRAIL branching guide — one branch per improvement/fix

Advisor rule: every claim gets a number, every comparison is a re-runnable
condition. Git branches are how conditions stay diffable and reversible.
Two kinds of branches, two repos:

- **Tool branches** — changes to `grail-agent/` (the AIDEAL tool itself).
  Live in the GRAIL repo, short-lived, merged into `main` after tests pass.
- **Condition branches** — experiment states (which docs/config the audience
  saw). Live in the GRAIL repo for configs/docs; for treatments that edit the
  TARGET codebase (aliases, error-message rewrites in `experiments/rdpro/beast`),
  branch inside that repo per WORKING.md. Condition branches are NEVER merged —
  they exist to be diffed, re-run, and cited.

## Step 0 — do this first: baseline-commit the current tree

Repo reality (verified 2026-07-13): you are on **`exp/root-before-api-cards`**
@ `6cffc2c` (tracks origin); `main` is back at `424e6fc` (06-13); several
experiment WORKTREES hang off this line (GRAIL_api_cards, GRAIL_design_base,
GRAIL_feature_api_cards, GRAIL_exp_runner); `origin` already exists =
`https://github.com/ZhuochengShang/GRAIL.git`. So: capture the state on a NEW
branch from HERE — do not commit onto `root-before-api-cards` (other worktrees
treat it as a fixed fork point) and do not touch `main` yet.

About the ~930 pending deletions: **886 are `rdpro-backend/`** + testbed +
old grail-agent/configs — the intentional 2026-06-22 restructure, finally
recorded. Every deleted file is tracked in `6cffc2c` (and on origin), so all
are recoverable anytime via `git show 6cffc2c:rdpro-backend/<path>` — no
archive/ folder is needed (the one made on 06-22 was since removed from disk).

```bash
cd ~/Documents/phd_projects/code/geoAI/GRAIL
rm -f .git/index.lock                      # stale lock, if still present
git switch -c exp/aideal-state-2026-07-13  # new branch from 6cffc2c

# commit 1 — the 07-08 experiment state (everything except this session's files)
git add -A
git reset -- $(cat .aideal_tmp/today_files.txt)
git commit -m "Docfix v2 + robustness + deep-dive: state of 2026-07-08

gemini-3.1 doc-repair 36/99=36.4%; robustness: gemini-2.5 +7.5pp scored,
codex-5.3 +16.7pp on repaired catalog; deep-dive module; 4-condition table.
Also records the 2026-06-22 restructure deletions (rdpro-backend/, testbed/,
grail-agent/configs/) — recoverable via git show 6cffc2c:<path>."

# commit 2 — this session's tool work (2026-07-13)
git add -A
git commit -m "Surface visibility fix + fix-report + python adapter (tslearn) + demo stability

- api-surface: private/protected leak fixed (regex lookahead never worked;
  container-level modifiers now checked): 820 -> 652 public names; 34/205
  catalog entries flagged -> aideal surface-audit
- fix loop: per-round rows in error_log (round=), aideal fix-report readable
  markdown (verdict vs baseline, same-issue-not-solved, clusters, per-API
  why-failed), auto-written after --execute / fix-docs
- python adapter + experiments/tslearn study (condition ladder A/B/C runbook)
- run_demo_stability.sh 5-run protocol + DEMO_PLAN.md
- default roles -> google:gemini-3.2-pro-preview"

# push the NEW branch (origin already configured — no `git remote add`)
git push -u origin exp/aideal-state-2026-07-13
```

Fast-forwarding `main` (or PR-ing into it) is a separate, deliberate step once
you're happy with the state — nothing above touches `main` or the worktrees.

## Naming scheme

```
aideal/fix-<slug>       tool bugfix        (aideal/fix-surface-visibility)
aideal/feat-<slug>      tool feature       (aideal/feat-fix-report)
aideal/<study>-<cond>   condition          (aideal/rdpro-a-original, aideal/tsl-b-readme,
                                            aideal/tsl-c-catalog)
```

## The condition ladder (per study) — first baseline = LLM + original repo

Per Zoe 2026-07-13: condition **A is always "just the LLM on the original
codebase/original README"** — no AIDEAL artifacts — and the **catalog (per-
class index) is the ADVANCED step that comes only after the full generated
doc exists**. Ladder: A original → B generated readme + FULL fix pipeline
(code fix loop, deep-dive doc-repair, error log) → C = B + catalogue index.
B and C are complete treatments differing ONLY in the index (C − B isolates
what the index is worth).
Each improvement is its own branch so `git diff` shows exactly what the
treatment changed.

```bash
# A — original-readme floor (run BEFORE generating any catalog)
git checkout -b aideal/rdpro-a-original exp/aideal-state-2026-07-13
cd experiments/rdpro
aideal comprehension --execute --doc original > docs/comprehension_A_original.json
git add -A && git commit -m "A: original-readme baseline: <pass>/<n> (<pct>)"

# B — generated README + FULL fix pipeline, no index (class-context off).
#     "readme fix loop, deep dive, code error log" all inside this arm.
git checkout -b aideal/rdpro-b-readme exp/aideal-state-2026-07-13
aideal readme --generate --limit 0 --force
git add -A && git commit -m "B/C shared setup: generated readme"   # C branches from here
aideal comprehension --execute --class-context off > docs/comprehension_B0.json
aideal fix-docs --from-results docs/comprehension_B0.json --deep-dive-first --retry-rounds 3 --report docs/docfix_B.json
aideal comprehension --execute --class-context off > docs/comprehension_B_final.json
aideal fix-report --run docs/comprehension_B_final.json --baseline docs/comprehension_A_original.json
git add -A && git commit -m "B: readme+fixloop: <pass>/<n>; delta vs A: +<pp>"

# C — SAME pipeline as B + the catalogue index (the ADVANCED step; branch from
#     B's generated-readme commit so the arms differ ONLY in the index).
git checkout -b aideal/rdpro-c-catalog <B-setup-commit>
# configs/aideal.yaml: comprehension.class_context: true  (docfix retries too)
aideal catalogue
aideal comprehension --execute --class-context on > docs/comprehension_C0.json
aideal fix-docs --from-results docs/comprehension_C0.json --deep-dive-first --retry-rounds 3 --report docs/docfix_C.json
aideal comprehension --execute --class-context on > docs/comprehension_C_final.json
aideal fix-report --run docs/comprehension_C_final.json --baseline docs/comprehension_B_final.json
git add -A && git commit -m "C: +catalogue index: <pass>/<n>; delta vs B: +<pp>"

# Further treatments (aliases, error-message rewrites in beast/) — same pattern,
# one branch each.
```

(The same ladder for tslearn is written out in `experiments/tslearn/RUNBOOK.md`.)

## Per-fix workflow (tool branches)

```bash
git checkout -b aideal/fix-<slug> <integration-branch>   # today: exp/aideal-state-2026-07-13
# edit grail-agent/...
python3 -m pytest grail-agent/tests -q          # must pass (30 tests)
cd experiments/rdpro && aideal surface-audit    # or the check the fix targets
git add -A && git commit -m "fix: <what> — <evidence number before -> after>"
git switch <integration-branch> && git merge --no-ff aideal/fix-<slug>
```

Rules of thumb: commit messages carry the measured number (pass rate, count
delta) — that's what makes history citable in the paper; never run two
conditions in one working tree at the same time (shared `.aideal_exec` +
error log clobber — RUNBOOK rule); tag paper-cited states
(`git tag vldb-demo-freeze`) so slides point at immutable commits.

## Remote

`origin` = https://github.com/ZhuochengShang/GRAIL.git (already configured —
never `git remote add`). Check the repo is PRIVATE before pushing anything new
(github.com/ZhuochengShang/GRAIL → Settings): LLM_readme + deepdive reports
quote Beast/RDPro source, and the paper is unpublished. Push condition
branches individually (`git push -u origin <branch>`); `git push --all` only
once you've reviewed the branch list (`git branch -vv`).
