# Working on this project — daily cheat sheet

Everything you need each time you open the project. (README.md explains
*what* the project is; this file is *how to work on it*.)

## 1. Session startup (every time)

```bash
conda activate geo_llm_spark        # NOT Homebrew python (pip will refuse)
cd ~/Documents/phd_projects/code/geoAI/GRAIL
export OPENAI_API_KEY="sk-proj-..." # needed for any LLM step
git status                          # see where you left off (section 3)
```

First time on a new machine only:

```bash
cd grail-agent && pip install -e . && pip install -r ui/requirements.txt
```

After `pip install -e .` the commands `aideal` and `aideal-mcp` exist directly.
If not installed, substitute `python -m aideal.cli` for `aideal`.

## 2. Where to stand

`aideal` picks the project from the folder you're standing in
(it searches upward for `configs/aideal.yaml`):

| To work on | Stand in |
|---|---|
| testbed study (barelib) | `experiments/testbed/` |
| RDPro case study | `experiments/rdpro/` |
| Sedona case study | `experiments/sedona/` |
| demo pipeline / curated RDPro docs | `grail-agent/src/` |

## 3. Git — the commands you keep forgetting

There are THREE kinds of git repo here. Know which one you're in:

1. **GRAIL repo** (this folder) — your code, configs, docs, patches.
2. **Clone repos** (`experiments/rdpro/beast/`, `experiments/sedona/sedona/`)
   — upstream code; your changes live on `aideal/*` branches. Gitignored by
   GRAIL, so commits there never show up in GRAIL's status.
3. Nothing else is a repo.

### Daily GRAIL repo flow

```bash
git status                  # what changed / where was I
git diff                    # unstaged changes, line by line
git log --oneline -10       # recent history
git add -A && git commit -m "what I did"     # checkpoint
git push                    # after the GitHub remote exists
```

### Working in a clone (Beast / Sedona)

```bash
cd experiments/rdpro/beast
git branch -a                              # which conditions exist
git switch master                          # back to untouched upstream
git switch -c aideal/stage1-llm-readme     # start a NEW condition
# ...edit...
git add -A && git commit -m "stage1: generated docs for raptor"
git switch aideal/stage2-aliases           # jump to another condition
git diff master..aideal/stage2-aliases     # exactly what a condition changed
git log --oneline master..HEAD             # commits in current condition
```

When a condition is final, export it so GRAIL's repo records it:

```bash
cd experiments && ./export_changes.sh rdpro/beast
git add rdpro/changes && git commit -m "export rdpro condition patches"
```

### "Help, what state am I in?"

```bash
git branch --show-current   # which branch am I on
git stash                   # park uncommitted mess; git stash pop to resume
git restore <file>          # throw away changes to one file
git log --oneline --all --graph | head -20   # the whole picture
```

## 4. AIDEAL CLI reference (run from a project folder, section 2)

```bash
aideal init                  # scaffold config -> profile + AGENTS.md (run twice on bare dir)
aideal profile               # is the intake complete? (gate for LLM steps)
# -- the four checks --
aideal readme                # find/create LLM_readme.md  (--generate = author model fills)
aideal form                  # entries structurally complete? (no LLM)
aideal completeness          # all public functions documented? (no LLM)
aideal comprehension         # readme unit test (LLM; --doc original = baseline README)
aideal puzzle                # integration + fix loop (--dry-run = preview only)
aideal all --static-only     # quick non-LLM pass
# -- memory loop --
aideal log-add --function X --error "..." --step code-test   # record a failure
aideal log-prompt            # render failures for prompts
aideal notes-distill         # repeated errors -> notes_to_self.md
aideal notes-prompt          # render lessons
aideal alias-suggest         # hallucinated names -> alias candidates
aideal alias-add NAME CANONICAL   # record an alias you actually added
aideal alias-report          # histogram + added/proposed
# -- tasks --
aideal tasks                 # list benchmark tasks
aideal tasks --generate 5    # author model writes tasks from the profile
```

Other runners:

```bash
# testbed puzzle runner (executes generated Python; the measurement tool)
cd experiments/testbed && python runner/puzzle_runner.py --num-puzzles 5
# GRAIL demo UI
cd grail-agent && streamlit run ui/grail_ui.py
# RDPro Scala puzzle evaluator (needs Spark setup)
cd grail-agent/src && python -m rdpro_section_codegen.puzzle_eval --dry-run
```

## 5. Things to keep in mind

- **Profile gate**: LLM steps refuse to run until `aideal profile` says
  `ready: true`. Static checks always work.
- **Fixed seed = comparable runs.** Keep `--seed 42` (or the config value)
  so every condition faces identical puzzles. Record (branch, seed) for
  every measurement.
- **Don't edit barelib or the clones' master** — improvements go through the
  pipeline (testbed stages) or condition branches (clones).
- **Sample data**: big datasets stay OUT of git (paths in
  `grail-agent/configs/local_data_paths.md`); tiny fixtures live in
  `grail-agent/examples/fixtures/`.
- **Run artifacts** (`outputs/`, `logs/`, `ui_mock_runs/`, egg-info) are
  gitignored — never commit them, reports stay reproducible from configs.
- **Prompts**: package defaults are used automatically; create a local
  `prompts/` folder in a project only when running a prompt ablation.
- **API keys**: export per session, never write them into files. Gemini uses
  `GOOGLE_API_KEY` (langchain default), not `GEMINI_API_KEY`.
- **MCP for coding agents**: `claude mcp add aideal -- aideal-mcp`
  (set `AIDEAL_CONFIG=<path to aideal.yaml>` if the agent starts elsewhere).
