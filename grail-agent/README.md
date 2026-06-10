# GRAIL Agent

This folder contains the main GRAIL agent implementation.

## Layout

- `src/rdpro_section_codegen`: Python package for analysis, planning, LangGraph section generation, validation, repair, and compile/run.
- `configs`: scaffold files and local machine configuration notes.
- `docs`: LLM-ready RDPro documentation used as generation context.
- `examples`: Python examples and lightweight demo fixtures.
- `benchmarks`: benchmark scripts and result summaries.
- `outputs`: generated Scala and HTML demo artifacts.

## Main Script

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
python -m pip install -e .
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

## Demo Pages

- `outputs/boston_land_use_comparison_map.html`: Boston land-use comparison map generated from the UI mock run.
- `outputs/aideal_v4.html`: another candidate start/landing page found under the Desktop GRAIL folder.
