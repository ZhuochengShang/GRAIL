# GRAIL

GRAIL is organized as a clean research artifact with three active parts:

1. `grail-agent`: LangGraph-based translation from natural language or Python geospatial workflows to RDPro Scala.
2. `rdpro-backend`: the RDPro/Beast backend modified for LLM-ready usage, including documentation, aliases, and repair-oriented errors.
3. `paper`: VLDB demo paper source and figures.

Old experiments should go under `archive/old_experiments` if they are needed for provenance, but they are not part of the main artifact.

## Main Entry Points

- Agent implementation: `grail-agent/src/rdpro_section_codegen/langgraph_section_agent.py`
- Section planner: `grail-agent/src/rdpro_section_codegen/planner.py`
- Validation and repair: `grail-agent/src/rdpro_section_codegen/validation_checks.py`
- Compile/package/run loop: `grail-agent/src/rdpro_section_codegen/compile_runner.py`
- Demo HTML outputs: `grail-agent/outputs/`

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
