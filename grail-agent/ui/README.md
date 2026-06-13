# GRAIL UI (Streamlit)

The demo interface from the screenshots/recordings — Setup bar (Preload Setup /
NLP Prompt / Python Editor), Generation Workspace (Python ↔ Generated Scala,
Translate workflow), side-by-side ground-truth vs. generated maps, and the
Pipeline/Spark-DAG preview.

This was previously `LangGraph/Notebook/agentic_ui_mockup.py`. It is a
Streamlit app, not a static HTML page — there is no .html file for it.

## Run

```bash
conda activate geo_llm_spark   # required: run buttons call this env's python/spark-submit
cd ~/Documents/phd_projects/code/geoAI/GRAIL/grail-agent
pip install -e . && pip install -r ui/requirements.txt
streamlit run ui/grail_ui.py
```

Do not use the Homebrew system Python (`externally-managed-environment` error).

## Notes

- Repo paths (agent script, docs, scaffold) now resolve relative to this repo.
- Machine-specific paths still hard-coded near the top of `grail_ui.py` and in
  the preloaded demo cases (lines ~115-140): conda envs, spark-submit, the
  Beast lib dir, and local dataset paths (Landsat8, NLCD, Boston shapefile).
  Update them per `configs/local_data_paths.md` when running on a new machine.
