# AIDEAL + GRAIL

Two-part research artifact:

**AIDEAL is the base — the general method** (`grail-agent/src/aideal`). A codebase-agnostic system that tests and improves how LLM-ready any codebase is. Start point on any codebase: `python -m aideal.cli --config <target>/configs/aideal.yaml init` (user enters project description, target users, domain, use cases), then the pipeline: find/create `LLM_readme.md` → form check → comprehension check (readme unit test: write correct code from the doc alone) → completeness check → puzzle integration tests with a fix loop. LLM mistakes feed back into the codebase: structured `error_log.jsonl` → `notes_to_self.md` distilled memory → alias proposals → added aliases. One YAML config controls models (Claude / Kimi / Qwen / llama3 registry, author vs. audience roles), paths, languages, tasks, prompts, and runtime (local / HPCC / Jetstream / cloud). AIDEAL knows nothing about geospatial.

**GRAIL is the experimental program** that studies each AIDEAL step's effectiveness and demonstrates the method on real case studies:

- `experiments/testbed/`: controlled study — `barelib` starts with NOTHING (cryptic names, no docs, terse errors); add one LLM-ready asset per stage and measure the readiness delta of each step. Same seed at every stage; the "score vs. stage" curve is the core quantified result.
- `experiments/rdpro/`: case study 1 — real library, conditions: original README → AIDEAL-generated docs → hand-curated docs, measured on identical sampled functions.
- `experiments/sedona/`: case study 2 — Apache Sedona, external codebase with good original docs; tests generalizability (clone + `init`, then same pipeline).
- `grail-agent/src/rdpro_section_codegen` + `ui/`: the GRAIL demo apparatus — LangGraph NL/Python→RDPro-Scala translation with compile/run repair loop (every failure auto-logs to AIDEAL) and the Streamlit interface showing the applied changes working end to end.

Folders:

1. `grail-agent`: AIDEAL base (`src/aideal`, `prompts/`, `configs/aideal.yaml`) + GRAIL demo apparatus (`src/rdpro_section_codegen`, `ui/`).
2. `experiments`: ALL studies — `testbed/` (controlled step-by-step effectiveness, pure Python, fast), `rdpro/` (case study 1), `sedona/` (case study 2).
3. `rdpro-backend`: the RDPro/Beast backend under study (receives the applied changes: docs, aliases, repair-oriented errors).
4. `paper`: VLDB demo paper source and figures.

Old experiments should go under `archive/old_experiments` if they are needed for provenance, but they are not part of the main artifact.

## Quick Start

```bash
conda activate geo_llm_spark    # required env; system/Homebrew Python will not work
cd ~/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
pip install -e . && pip install -r ui/requirements.txt
export OPENAI_API_KEY=...

# AIDEAL (the method) on any target:
cd src && python -m aideal.cli all --static-only      # RDPro default config
python -m aideal.cli --config ../../experiments/testbed/configs/aideal.yaml completeness

# GRAIL (the study/demo):
streamlit run ../ui/grail_ui.py                       # demo interface
python ../../experiments/testbed/runner/puzzle_runner.py --dry-run  # stage-0 baseline puzzles
```

**Daily commands, git help, and CLI reference: [`WORKING.md`](WORKING.md)** — open that file every time you come back to the project.

Full setup, commands, and machine-specific path notes: `grail-agent/README.md`.

## Main Entry Points

- Agent implementation: `grail-agent/src/rdpro_section_codegen/langgraph_section_agent.py`
- Section planner: `grail-agent/src/rdpro_section_codegen/planner.py`
- Validation and repair: `grail-agent/src/rdpro_section_codegen/validation_checks.py`
- Compile/package/run loop: `grail-agent/src/rdpro_section_codegen/compile_runner.py`
- CLI (analyze + plan only): `python -m rdpro_section_codegen.cli <script.py>`
- HTML demo entry point: `grail-agent/outputs/aideal_v4.html`
- Sample data fixtures: `grail-agent/examples/fixtures/`

## GitHub Setup

This folder is ready to become the GitHub repository root.

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL
git init
git add .
git commit -m "Initial clean GRAIL artifact"
```

Then create a GitHub repo named `GRAIL`. The intended URL is:

```text
https://github.com/ZhuochengShang/GRAIL
```

The local `origin` remote is configured as:

```text
https://github.com/ZhuochengShang/GRAIL.git
```

After the remote repo exists, push it:

```bash
git branch -M main
git push -u origin main
```

Do not commit large local datasets. Keep them in `Downloads` or another data directory and document the paths in `grail-agent/configs/local_data_paths.md`.
