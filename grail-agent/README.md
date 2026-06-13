# GRAIL Agent

This folder contains the main GRAIL agent implementation.

## Layout

- `src/rdpro_section_codegen`: Python package for analysis, planning, LangGraph section generation, validation, repair, and compile/run. Code only — no run artifacts.
- `src/aideal`: **AIDEAL — the backend.** Generic, codebase-agnostic LLM-readiness toolkit; GRAIL sits on top of it (AIDEAL never imports GRAIL code). Pipeline: `readme` (find/create `LLM_readme.md`) → `form` → `comprehension` (readme unit test: given only the doc, the audience model must write correct code) → `completeness` (all functions covered?) → `puzzle` (integration tasks + fix loop). Workspace files, all configured in `configs/aideal.yaml`: `LLM_readme.md`, `notes_to_self.md` (distilled memory, `issue {{}} fix {{}} pattern {{}}`), `configs/integration_tasks.yaml` (NL benchmark tasks), `aliases/aliases.json` (proposed + added aliases per model), `logs/error_log.jsonl` (structured records: run_id, step, language, task, status, function, error, root_cause, suggested_fix_code). Model registry covers Claude family, Kimi, Qwen, llama3, GPT, with author/audience role split; runtime section has local/HPCC/Jetstream/cloud settings.
- `configs`: scaffold files, `aideal.yaml` (single config), `project_profile.yaml` (user intake: description, target users, domain, use cases — required before LLM steps), `integration_tasks.yaml`, local machine notes.
- `prompts`: all LLM prompts as `.md` templates (SYSTEM/USER blocks with `{placeholders}`); swap `files.prompts_dir` in `aideal.yaml` for prompt ablations. The project profile is auto-injected into every prompt.
- `docs`: LLM-ready RDPro documentation used as generation context.
- `examples/python`: Python example scripts used as translation inputs.
- `examples/fixtures`: small sample data files (geojson, csv, tif) for demos.
- `benchmarks`: benchmark scripts and result summaries.
- `outputs`: generated Scala, HTML demo artifacts, and `cluster_submit_runs/` run logs.

## Entry Points

- Full pipeline (NL/Python → RDPro Scala): `src/rdpro_section_codegen/langgraph_section_agent.py` (argparse CLI, see Main Script below).
- Analyze + plan only: `python -m rdpro_section_codegen.cli <python_script>` — prints the section plan as JSON.
- Baseline (raw via-Python, no sectioning): `src/rdpro_section_codegen/langgraph_section_agent_via_python_raw_baseline.py`.
- LLM-readiness puzzle evaluator: `python -m rdpro_section_codegen.puzzle_eval` — samples N random APIs from the docs, composes them into a task, runs the pipeline, and scores compile/run success (`--dry-run` to preview puzzles; same `--seed` reproduces puzzles across ablation tags).
- AIDEAL CLI: `cd src && python -m aideal.cli {readme|form|comprehension|completeness|puzzle|all|tasks|alias-report|alias-overlap|alias-suggest|alias-add|log-add|log-prompt|notes-add|notes-distill|notes-prompt}` — every command prints JSON, so coding agents can invoke it repeatedly. `readme`, `form`, `completeness`, `tasks`, and all alias/log/notes commands need no LLM/API key.
- GRAIL demo UI (Streamlit, the interface in the paper figures): `streamlit run ui/grail_ui.py` — see `ui/README.md`.
- AIDEAL UI mock (static HTML): `outputs/aideal_v4.html`.

## Setup

Use the `geo_llm_spark` conda env — the UI's run buttons and the compile/submit
loop call this env's `python` and `spark-submit`, so installing into another
env gives you a UI that cannot execute anything. Do NOT use the Homebrew
system Python (pip will refuse with `externally-managed-environment`).

```bash
conda activate geo_llm_spark    # or: source ~/miniconda3/bin/activate geo_llm_spark
cd ~/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
pip install -e .                          # agent + AIDEAL deps (langgraph, pyyaml, ...)
pip install -r ui/requirements.txt        # only needed for the Streamlit UI
export OPENAI_API_KEY=...                 # needed by the agent and LLM-based checks
```

Extra model providers (Claude / Gemini / Ollama for Kimi, Qwen):
`pip install -e ".[providers]"`.

Machine-specific paths (conda envs, spark-submit, Beast lib dir, demo
datasets) are hard-coded near the top of `ui/grail_ui.py` and in
`configs/local_data_paths.md` — update both on a new machine.

## Main Script

```bash
conda activate geo_llm_spark
cd ~/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
python src/rdpro_section_codegen/langgraph_section_agent.py \
  --translation-mode direct \
  --free-text "Calculate land-cover percentages for each polygon from a raster and write CSV output." \
  --scaffold configs/job_scaffold.scala \
  --output-scala outputs/generated.scala \
  --api-doc docs/rdpro_api_doc_combined.md \
  --provider openai \
  --model gpt-4o
```

The local data paths used for the Boston/NLCD demo are listed in `configs/local_data_paths.md`.

## Demo UI

The GRAIL interface (the one in the paper figures and screen recordings) is a
**Streamlit app, not an HTML file**:

```bash
conda activate geo_llm_spark
cd ~/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
streamlit run ui/grail_ui.py
```

Static pages in `outputs/`:

- `outputs/boston_land_use_comparison_map.html`: Boston land-use comparison map exported from a UI mock run.
- `outputs/aideal_v4.html`: AIDEAL UI mock (the doc-test tool the `aideal` CLI backs).

## Common Commands

```bash
cd src

# 0. intake — REQUIRED first on any new codebase. On a bare directory the
#    first run scaffolds configs/aideal.yaml; the next run creates
#    project_profile.yaml + AGENTS.md (conventions for coding agents).
#    Fill description, target users, domain, use cases — LLM steps refuse
#    to run until the profile is complete.
#    With `pip install -e .` the `aideal` command works directly, and
#    `aideal-mcp` (pip install -e ".[mcp]") exposes the checks as MCP tools
#    for Claude Code / Cursor / Windsurf:  claude mcp add aideal -- aideal-mcp
python -m aideal.cli init
python -m aideal.cli profile             # show missing fields / readiness

# doc readiness pipeline (static steps need no API key)
python -m aideal.cli readme              # find or create LLM_readme.md
python -m aideal.cli form                # required sections present?
python -m aideal.cli completeness        # all public functions documented?
python -m aideal.cli all --static-only   # the above in one run
python -m aideal.cli comprehension       # readme unit test (needs API key)
python -m aideal.cli puzzle --dry-run    # integration puzzles + fix loop

# memory loop: errors -> notes -> aliases
python -m aideal.cli log-add --step code-test --task ndvi_pipeline \
  --function saveAsGeoTiff --error "unsupported raster datatype Float64" \
  --root-cause "ClassCastException: ..." --suggested-fix-code "sc.geoTiff[Float](path)"
python -m aideal.cli notes-distill       # repeated errors -> notes_to_self.md
python -m aideal.cli alias-suggest       # hallucinated names -> alias candidates
python -m aideal.cli alias-add zonalStats raptorJoin   # track what was ADDED

# benchmark tasks
python -m aideal.cli tasks               # list configs/integration_tasks.yaml
```
