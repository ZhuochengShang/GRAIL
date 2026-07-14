# AIDEAL / GRAIL — full pipeline (rdpro)

> **CURRENT EXPERIMENT LADDER (2026-07-13) — supersedes the g1/g2 condition
> naming below.** One branch per condition, default models
> `google:gemini-3.2-pro-preview` (configs/aideal.yaml roles):
>
> - **A `aideal/rdpro-a-original`** — pure original repo/README, no AIDEAL
>   artifacts: `aideal comprehension --execute --doc original` (never run yet).
> - **B `aideal/rdpro-b-readme`** — generated ENTIRE readme + full fix
>   pipeline (comprehension code fix loop + error log + `fix-docs
>   --deep-dive-first`), class-context OFF.
> - **C `aideal/rdpro-c-catalog`** — exactly B + the catalogue index
>   (`aideal catalogue`, `class_context: true`); branch from B's
>   post-`readme --generate` commit so C−B isolates the index.
>
> Exact commands: `GRAIL/BRANCHING.md`. Hygiene: `aideal surface-audit`
> (34/205 current entries flagged non-callable/deselected after the
> 2026-07-13 visibility fix), `aideal fix-report --run <json> [--baseline
> <json>]` for the readable per-run analysis. The older g1/g2/g3/g4 suites
> below remain valid as scripted primitives inside these arms.

Run from `experiments/rdpro/`. Static steps need no key; LLM/execution steps need
a model key (`GOOGLE_API_KEY` for the gemini-3.2 defaults; `OPENAI_API_KEY` for
gpt/codex arms) + scalac / spark-submit for `--execute`.

## 0 · Setup (once)
```bash
cd ../../grail-agent && pip install -e . && cd ../experiments/rdpro
```

## 1 · Bootstrap config + profile
```bash
aideal init          # 1st: scaffolds configs/aideal.yaml
aideal init          # 2nd: scaffolds configs/project_profile.yaml (+ AGENTS.md)
# edit configs/aideal.yaml     -> source_globs, extends:[scala-spark], jars/packages
# edit configs/project_profile.yaml -> role, domain, target_users, use_cases, constraints
aideal profile       # gate: want "ready": true
```

## 2 · Static discovery (no key)
```bash
aideal api-surface        # discovered public API surface
aideal intent             # intended-API selection (static evidence + LLM signal)
aideal intent-compare     # optional: with-vs-without the LLM signal
aideal api-tests          # real usage mined from the test suite (grounding + oracle)
```

## 3 · Generate the doc (needs key)
```bash
export OPENAI_API_KEY=...
aideal readme --generate --limit 0 --force
#  -> LLM_readme.md (with SIBLING grounding) + io_hints.txt + preamble.scala (eager, in sync)
```

## 4 · Curate the doc (static — pick robust APIs)
```bash
aideal grounding             # 3 tiers: grounded / sibling-grounded / guessed
aideal grounding --annotate  # write a Grounding line into each entry
aideal organize --index      # group by class, rank robust-first, mark primary -> docs/readme_index.md
```

## 5 · Static doc checks
```bash
aideal form            # every entry has the required sections
aideal completeness    # all intended APIs are documented
```

## 6 · Execution-grounded comprehension (needs key + Scala/Spark)
```bash
aideal scaffold --generate                         # docs/api_test_scaffold.scala
aideal comprehension --api raptorJoinIDFull --execute --show-code   # one API
aideal comprehension --execute --sample 0          # all intended APIs
#  - preamble pre-loads typed inputs (rasterRDD/featuresRDD) -> tests only the API call
#  - 3-round fix loop; live per-round progress; io_hints injected each round
#  - failures + fixes -> logs/error_log.jsonl
```

## 7 · Learn from failures (fold back into the doc)
```bash
aideal augment                       # error_log -> Common Failure Modes / Fix Code Hint
aideal notes-distill                 # repeated errors -> docs/notes_to_self.md
aideal alias-suggest                 # hallucinated names -> alias candidates
aideal alias-add <alias> <canonical> # promote an alias into the codebase
```

## 8 · Integration puzzle (needs key + runner)
```bash
aideal puzzle        # pick k functions, make the pipeline pass; fix loop
```

## 9 · One command for the checks (after profile ready)
```bash
aideal all           # find readme -> form -> completeness -> comprehension -> puzzle
```

## 10 · Downstream task — the demo agent (needs key + Spark)
```bash
python demo_agent.py --text "Compute land-use % per Boston neighborhood ..." --execute --rounds 3
python demo_agent.py --python ../../grail-agent/examples/python/zonal_stats_minmax.py --execute
```

## The self-improving loop (repeat)
```
comprehension --execute   ->   augment   ->   readme --generate   ->   comprehension --execute
      (log errors/fixes)      (fold in)      (regen, learnings)          (fewer failures)
```
Each pass makes the doc — and the next generation — better, with no hand-written Scala.

---
### Which steps need a key
- **No key (static):** init, profile, api-surface, intent*, api-tests, grounding,
  organize, form, completeness, scaffold --generate.
- **Needs OPENAI_API_KEY:** readme --generate, comprehension (LLM-graded or --execute),
  puzzle, demo_agent, and the auto io_hints/preamble generation.
- **Also needs scalac + spark-submit:** comprehension --execute, puzzle, demo_agent --execute.


cd experiments/rdpro
export PYTHONPATH=../../grail-agent/src        # so `import aideal` resolves
python demo_agent.py --text "Compute land-use % per Boston neighborhood ..." --execute
# or translate a Python script:
python demo_agent.py --python ../../grail-agent/examples/python/zonal_stats_minmax.py --execute
## R · Full rerun from init — post-dedup (2026-07-06) + backend micro-benchmarks

The surface changed (dedup: 820 raw → 205 selected → 203 catalog entries), so
rerun the whole chain and quantify each comparison. Run from `experiments/rdpro/`.

```bash
# 0. snapshot BEFORE numbers (the comparison baseline)
wc -c docs/LLM_readme.md                       # old catalog size (552,866 chars)
cp docs/comprehension_run.json docs/comprehension_run.pre_dedup.json 2>/dev/null || true

# 1. bootstrap (idempotent) + profile gate
aideal init && aideal profile

# 2. static chain — no key; artifacts refresh
aideal api-surface > docs/api_surface.txt
aideal intent --all > docs/intent_all_nollm.json
aideal dedup --out docs/dedup_report.json

# 3. LLM arm of intent (key; empty [] cache now re-judges instead of sticking)
aideal intent-compare --names > docs/intent_compare.json

# 4. regenerate the catalog from the deduped surface (key; the token payoff)
aideal readme --generate --force
wc -c docs/LLM_readme.md                       # AFTER size -> report the delta

# 5. comprehension on the new catalog (key + spark) — pass rate must NOT drop.
#    Crash-safe since 2026-07-06: per-API checkpoint + --resume (the 07-01
#    all-API run died at ~120/218 on a timeout-handler bug and lost everything).
rm -rf exec_out/*        # stale writer temp dirs fail saveAsGeoTiff-style APIs
aideal comprehension --execute --timeout 300 > docs/comprehension_run.json
#    interrupted/crashed? SAME command + --resume — finished APIs are skipped:
# aideal comprehension --execute --timeout 300 --resume > docs/comprehension_run.json

# 6. fold verified fixes back in, then puzzle
aideal augment && aideal puzzle
```

### Backend micro-benchmarks (TODO items 3 + 5)

`bench_conditions.py` runs each condition as one clean `aideal comprehension
--execute` process over ALL documented APIs and saves per-API metrics
(status, attempts, pass_round, wall_s, provider-reported tokens, per-model
split) to `results/bench/`:

| condition | what it isolates |
|---|---|
| `openai_chat` | plain OpenAI chat-completions (config default) |
| `codex_api` | same task via the Codex/Responses endpoint (`--role audience=codex:$BENCH_CODEX_MODEL`) |
| `gemini_maxfix` | Gemini as the FIXER with `--max-fix-rounds 99` — fix as much as possible, count rounds+tokens |
| `no_fix` | `--max-fix-rounds 0` single-shot — the value of the fix loop itself |

```bash
export BENCH_CODEX_MODEL=...   # the codex model your account offers
export BENCH_GEMINI_MODEL=...  # e.g. gemini-2.5-pro   (+ GOOGLE_API_KEY)
python bench_conditions.py --dry-run          # see the exact commands
python bench_conditions.py --sample 10        # pilot on 10 APIs
python bench_conditions.py                    # full: every documented API
python bench_conditions.py --table            # pass rate / pass@0 / attempts / tokens / wall
```

Metrics definitions: `pass@0` = solved single-shot (no fix round);
`att/pass` = mean attempts among eventual passes (fix-loop depth actually
needed); token counts are provider-reported (usage_metadata), split per model
so the Gemini-fixer condition shows who spent what.

### Codex fresh-README condition (author + audience/fixer)

The same-README backend runs above isolate the **coding model**: OpenAI chat,
Codex/Responses, Gemini, and Ollama consume identical `LLM_readme.md`. That is
the fair model-backend comparison. A separate condition tests Codex as the full
pipeline model: Codex regenerates the README, then Codex consumes/fixes from
that fresh README. Track it separately because the documentation input changes.

Preserved baseline for this branch of the experiment:

```text
docs/codex_fresh_archives/20260707_115728/
  LLM_readme.gemini_docfix.md       # Gemini doc-fixed README before overwrite
  docfix_run.gemini.json            # Gemini source-aware doc-repair report
  error_log.before_codex.jsonl      # pre-Codex mixed/Gemini error history
```

Clean-run setup already performed once: `logs/error_log.jsonl` was truncated
and `.aideal_exec/comprehension_progress.jsonl` removed, so `g4` will use only
Codex g1 failures. If you need to repeat, archive first, then clear both again.

```bash
export BENCH_CODEX_MODEL=gpt-5.3-codex

# 1. Regenerate the README with Codex as AUTHOR.
caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/aideal \
  readme --generate --limit 0 --force \
  --role author=codex:$BENCH_CODEX_MODEL \
  > docs/readme_generate_codex_fresh.json

cp docs/LLM_readme.md docs/LLM_readme.codex_fresh.md

# 2. Codex g1: fresh README, flat catalog, 3-round fix loop.
caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g1

# 3. Codex g4: rerun only the failures created by Codex g1.
export BENCH_G4_ROUNDS=15
caffeinate -i /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  codex_suite.py --stages g4

# 4. Aggregate with the existing backend table.
/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  bench_conditions.py --table \
  > docs/backend_comparison_table_after_codex.txt
```

Comparison checklist: `docs/codex_fresh_comparison_files.md`. Core outputs to
inspect are `docs/LLM_readme.codex_fresh.md`,
`results/bench/*g1_codex_flat*.json`,
`results/bench/*g4_codex_fixall*.json`, and
`docs/backend_comparison_table_after_codex.txt`.

### Gemini suite (items 3a/3c — all-Gemini conditions)

`gemini_suite.py` — 4 staged conditions, Gemini as the coding model throughout
(needs GOOGLE_API_KEY; set BENCH_GEMINI_MODEL from `python bench_check.py --list`):

```bash
python gemini_suite.py --dry-run --stages g1,g2,g3,g4   # see commands
python gemini_suite.py --stages g1,g4    # 1) flat big readme, then 4) Gemini fix-all on ITS failures
python gemini_suite.py --stages g2,g4    # 2) with catalogue index (class-context on), then fix-all
# 3) optional dedup arm: regen first (author model -> OPENAI_API_KEY), then:
aideal readme --generate --force && python gemini_suite.py --stages g3,g4
python bench_conditions.py --table       # aggregate everything
```

Notes: g4 fixes the failures of WHICHEVER stage ran last (`--rerun-failed` =
most-recent fail per function); rounds cap 99 means truly-unfixable APIs
(fixture/environment issues) burn many rounds — Ctrl-C is safe, rerunning g4
continues from the still-failing set. exec_out/ is auto-cleaned per stage.

### Model-tier comparison FIRST: gemini-2.5-flash vs gemini-2.5-pro

Before the deeper layers, quantify the tier choice on the SAME flat catalog
(g1). Results are keyed per model, so both rows coexist in the table:

```bash
# pro g1 is (or was) running; AFTER it finishes:
export BENCH_GEMINI_MODEL=gemini-2.5-flash
python gemini_suite.py --stages g1          # flash arm of the same condition
python bench_conditions.py --table          # pro vs flash vs gpt-4o, side by side
```

Decision rule: if flash is within ~2pp (the measured repeat-run variance) of
pro at a fraction of the cost, run the remaining ladder (g2/g3/g4) on flash
and keep pro for the headline model comparison only. For $ numbers, create
`results/bench/prices.json` (format in bench_conditions.py `_prices()`),
filling rates from the providers' current pricing pages.

**Never run two conditions in parallel in the same project dir** — they share
`.aideal_exec/` (checkpoint + per-API work dirs) and `logs/error_log.jsonl`;
a second run truncates the first one's checkpoint. Strictly sequential.
