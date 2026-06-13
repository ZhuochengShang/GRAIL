# GRAIL Pipeline Redesign: Generalizing Beyond RDPro

Goal: turn the current NL/Python → RDPro Scala pipeline into a general "LLM-ready codebase" framework, where RDPro is just the first plugged-in backend.

## Current State

The pipeline is one LangGraph with seven nodes:

```
prepare_prompt → generate_candidate → validate_scope → semantic_check
              → compile_submit → evaluate → final_review
```

It works, but RDPro is hard-wired in four places:

1. **Prompts and docs** — `docs/rdpro_api_doc_combined.md` is passed directly; prompt rules in `_build_section_prompt_rules` mention RDPro APIs by name.
2. **Section specs** — `section_specs.py` and `contracts.py` encode the load/process/save sections of a geospatial Spark job.
3. **Validation** — `validation_checks.py` and `api_fix_guides.py` contain RDPro-specific API signatures and fix recipes.
4. **Execution** — `compile_runner.py` assumes sbt/Spark compile-and-submit.

Also, `langgraph_section_agent.py` is 1,577 lines mixing graph wiring, prompt templating, Scala text manipulation, and metrics.

## Proposed Architecture

Split into a generic engine plus a per-target **Backend Profile**. The engine never names RDPro.

```
grail-agent/src/
  grail_core/                  # generic, target-agnostic
    graph.py                   # LangGraph wiring (the 7 nodes, routing)
    state.py                   # AgentState, Config, metrics/trace
    prompting.py               # prompt assembly from profile-provided pieces
    sectioning.py              # generic section plan model
    repair.py                  # retry/repair loop logic
  grail_backends/
    rdpro/                     # everything RDPro-specific, as data + small code
      profile.yaml             # name, language, build/run commands
      api_docs/                # the current docs/*.md
      aliases.json             # alias function table (LLM-friendly names → real APIs)
      fix_guides.md            # current api_fix_guides content
      sections.yaml            # section specs + contracts
      validators.py            # target-specific static checks
      runner.py                # compile/package/submit (wraps compile_runner)
```

### Backend Profile contract

A backend is registered by implementing one small interface:

```python
class BackendProfile(Protocol):
    name: str
    target_language: str
    def api_docs(self, section: str | None) -> str          # retrieval-scoped docs
    def section_plan(self, analysis) -> list[SectionSpec]   # how to slice a job
    def scaffold(self) -> str                                # empty-job template
    def validate(self, code: str, section: str) -> list[Issue]
    def fix_guide(self, issue: Issue) -> str                 # repair hint for LLM
    def compile_and_run(self, code: str, workdir: Path) -> RunResult
```

The seven graph nodes stay exactly as they are — they just call profile methods instead of importing RDPro modules. Adding a new target (e.g., Sedona, DuckDB-spatial, Flink) means writing one profile, not touching the agent.

### LLM-ready assets become first-class, generated artifacts

This is where the project's broader thesis lives. For any codebase, an `llm-readiness` toolkit generates the profile inputs automatically:

1. **README/doc generation** — agent walks the target codebase, emits per-API markdown (what `docs/*.md` is today, but produced by a script, not by hand).
2. **Alias library** — mine the API surface, generate intuitive alias functions (`clipRasterToPolygon` → `raptorjoin(...)` chain) with docstrings; emit `aliases.json` + a thin alias source file compiled into the target.
3. **Augmented error log** — wrap the target's compiler/runtime errors with a mapping table (error pattern → cause → fix guide), which is exactly what `api_fix_guides.py` does manually today. Make it a data file the repair node consumes.
4. **Puzzle-game validation** — readiness test: randomly sample 5 public functions from the target, ask the agent to compose them into a small working program ("puzzle"), and score compile/run success. This becomes the benchmark for *how LLM-ready a codebase is*, independent of the geospatial demo.

### Pipeline flow (redesigned)

```
                    ┌─ llm-readiness toolkit (offline, per codebase) ─┐
                    │  doc-gen · alias-gen · error-map · puzzle-eval  │
                    └────────────────┬────────────────────────────────┘
                                     ▼  produces BackendProfile assets
 NL / Python script → analyze → plan(sections) → [per section:
     prompt(profile docs + contract) → generate → static validate
     → semantic check → repair loop] → assemble → compile/run (profile)
     → evaluate → final review
```

## Migration Steps (incremental, nothing breaks mid-way)

1. **Extract state + graph** from `langgraph_section_agent.py` into `grail_core/` (mechanical move; keep a shim so the old CLI command still works).
2. **Define `BackendProfile`** and implement `rdpro` by wrapping existing modules (`section_specs`, `validation_checks`, `api_fix_guides`, `compile_runner`) — no rewrites yet.
3. **Move RDPro knowledge to data files** (sections.yaml, aliases.json, fix_guides.md) so the profile is mostly declarative.
4. **Build the puzzle-game evaluator** as `grail_core/puzzle_eval.py`: sample N functions from profile docs, generate a task, run the pipeline, score. Reuses the whole existing loop.
5. **Add a second toy backend** (even plain PySpark → prove the abstraction) before claiming generality in the paper.

## Other Suggestions

- **Retrieval-scoped docs**: the combined 1-file API doc inflates prompts; the `api_docs(section)` method should return only sections relevant to the planned APIs (the planner already knows them).
- **Structured issues**: `validate_scope`/`semantic_check` currently pass strings; a typed `Issue {code, span, message, severity}` makes routing and fix-guide lookup deterministic.
- **Single run directory**: every run writes to `outputs/runs/<timestamp>/` (scala, logs, metrics.json, trace.json) instead of scattered `generated_scala/one_shot_output_sectional_NN.scala` files.
- **Config over flags**: the agent has ~15 CLI flags; a `run.yaml` (profile, model, mode, paths) is easier for benchmarks and the UI to drive.
- **UI hookup**: `aideal_v4.html` is a static mock; once the profile interface exists, a tiny FastAPI server can expose `/run` and stream node-level trace events to it — the trace plumbing (`_trace_with_event`) already exists.
