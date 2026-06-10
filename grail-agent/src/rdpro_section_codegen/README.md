This folder contains a small Python-first planning pipeline for RDPro code generation.

Flow:
- analyze a Python script
- optionally classify task type with an LLM
- infer task type, inputs, outputs, and operations
- infer RDPro APIs
- derive section-level plan
- render section contracts

Quick usage:

```bash
python -m rdpro_section_codegen.cli /path/to/script.py
```

Main modules:
- `analyzer.py`: parse Python script into an `AnalysisResult`
- `planner.py`: infer APIs and sections
- `contracts.py`: base and task-specific section contracts
- `models.py`: dataclasses for analysis and plan results


<!-- /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
langgraph_section_agent.py \
--translation-mode direct \
--free-text "Calculate land-cover percentages for each polygon in this shapefile from this raster ..." \
--scaffold /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
job_scaffold.scala \
--output-scala /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
one_shot_output_sectional.scala \
--api-doc /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Doc/rdpro_api_doc_combined.md \
--guide /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/
RDProAgentLoop_perAPI_fix_migration_guide.md \
--provider openai --model gpt-4o

/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
langgraph_section_agent.py \
--translation-mode via-python \
--free-text "Calculate land-cover percentages for each polygon in this shapefile from this raster ..." \
--scaffold /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
job_scaffold.scala \
--output-scala /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/
one_shot_output_sectional.scala \
--api-doc /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Doc/rdpro_api_doc_combined.md \
--guide /Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/
RDProAgentLoop_perAPI_fix_migration_guide.md \
--provider openai --model gpt-4o -->
