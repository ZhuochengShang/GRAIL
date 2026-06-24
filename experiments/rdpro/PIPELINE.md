# AIDEAL Pipeline — RDPro Case Study (full logic, init → comprehension)

Framework code: `grail-agent/src/aideal` — a **codebase-agnostic harness with
per-codebase execution config** (not turnkey-generic: RDPro still supplies
curated imports, Spark packages, local fixtures, and classpath in
`configs/aideal.yaml`). Experiment config + outputs: `experiments/rdpro/`. Every
command reads `configs/aideal.yaml` and prints JSON.

NOTE: `surface_filter` (the intended-API definition) is **part of the
experimental design**, not an implementation detail — it sets the denominator
for coverage and the target set for comprehension/execution, so state it
explicitly in the writeup. Two model roles: **author** (writes docs,
grades) and **audience** (consumes docs to write code) — the split is the method:
docs are "good" only if a model with *nothing but the doc* can use the API.

## Setup (once)
```bash
conda activate geo_llm_spark
cd grail-agent && pip install -e .          # aideal CLI (editable)
export OPENAI_API_KEY=...                    # author=gpt-4o-mini, audience=gpt-4o
cd ../experiments/rdpro                       # aideal auto-finds configs/aideal.yaml
```

## The logic, stage by stage

### 1. `aideal init`
Reads `configs/aideal.yaml`; creates `configs/project_profile.yaml` (template,
incl. a `role` field) + `AGENTS.md`. Idempotent (never clobbers). Everything
else (docs, scaffold, logs) is produced by later stages.

### 2. `aideal profile`
Validates the profile is filled → `ready: true` (gates all LLM stages). The
profile is injected into every prompt as `project_context`, now led by **`role`**
("an expert in geospatial raster pipelines…") so the agent adopts the persona,
then domain / target users / use cases / constraints.

### 3. `aideal api-surface [--json]`  (static, no key)
Discovers the public API surface from `codebase.source_globs` via
`public_def_regex`, filtered by a **language visibility model** (Scala = `deny`:
drop `private`/`protected`). Produces, per API: signature, structured params
`{name,type,default}`, return type, Scaladoc, `file:line`. RDPro raw surface:
**113 public names** / 242 definition sites.

**Intended-API filter (`codebase.surface_filter`, GENERAL/codebase-agnostic).**
The raw 113 is a regex artifact (sweeps in `hasNext`/`compareTo`/`close`/…). A
reproducible filter narrows it to the *intended* API and governs documentation +
completeness + execution. Tightness needs human-intent signals; no single one is
ideal, so the paper-quality default is **`intent_score`** — an evidence score per
API, codebase-agnostic:

  +documented (2)  +tested (3)  +mentioned_in_docs (4)  +non_override (1)
  −override (3)  −internal_path (5)  −boilerplate_name (4)        select if ≥ threshold

Weights/threshold are config (`codebase.intent`), with optional reportable
`manual_include`/`manual_exclude`/`exclude_name_patterns`. Every decision is
auditable via `aideal intent` (per-API score + reasons). RDPro: threshold 5 →
**41** (the real operation surface; raw 113). Simpler modes still exist:
`all` | `documented` (68) | `tested` (48) | `documented_or_tested` (86) |
`non_override` (94) | `documented_non_override`; `documented` degrades
docs→tested→non_override→all. **Framing:** AIDEAL does not assume every public
symbol is intended for docs — it estimates the intended API from reproducible
evidence (docs, tests, doc-mentions, visibility) with structural penalties, emits
per-symbol reasons, and allows small transparent overrides.

### 4. `aideal api-tests`  (static, no key)
Mines `codebase.test_globs` (`beast/raptor/src/test/**`): for each API, the
`test("…"){…}` blocks that call it — real, compiling usage. RDPro: **48/113**
have examples. These are *grounding* for generation (stage 6), not executed here.

### 5. `aideal completeness`  (static, no key)
Intended-API surface (the `surface_filter` set, e.g. 41 with `intent_score`) vs documented entries →
coverage %. Denominator is the intended API, not the raw 113 (keep 113 as a
context number for "raw surface").

### 6. `aideal readme --generate [--limit N] [--force]`  (author model)
Builds `docs/LLM_readme.md`, one `## API Test:` entry per API in the intended-API
surface (`surface_filter`). Each entry is generated from FOUR grounded inputs:
- **API facts (JSON)** from the surface — signature, params, returns, doc;
- **distilled original docs** — `distilled_readme_context` summarizes README +
  `beast/doc/` (17 files) ONCE into `docs/original_readme_notes.md` (~700 words,
  cached, mtime-invalidated; `--force` re-distils);
- **real test examples** (stage 4) for that API;
- **profile + role**.
Prompt forbids contradicting the signature / inventing APIs. Streams to disk
with `[i/total]` progress; reports `generated_ok` / `fallback_to_skeleton`.
Sections: Signature / Goal / Parameters / Input / Output / Valid Call Patterns /
LLM Instruction Prompt / Prompt Snippet / Common Failure Modes / Fix Code Hint.
`--limit 0` = all; `--force` overwrites + re-distils.

### 7. `aideal scaffold --generate`  (static, no key)
Writes `docs/api_test_scaffold.scala` — the compiled execution frame
(`object GeoJob { def run(sc) } + GeoJobMain`, with `// AIDEAL_DATA_BINDINGS`
and `// TODO API_TEST_START/END` markers, prints `__DONE__`/`__RUN_ERR__`).
Imports: either auto-derived from source packages **verified against the actual
jars** (drops unresolvable ones like internal `jhdf`), or a curated
`comprehension.execute.imports` block (RDPro uses this — avoids wildcard
collisions like an ambiguous `RasterRDD`).

### 8. `aideal form`  (static, no key)
Per-entry check that every `required_sections` header is present and no `TODO`
remains → format-compliance %.

### 9a. `aideal comprehension [--doc original] [--show-code]`  (LLM-judged, no Spark)
A **cheap proxy / README unit test**, NOT the final proof: audience model writes
a snippet from the doc only; author model grades PASS/FAIL against the doc. No
compilation — it's LLM-judged, so don't oversell it; the execution path (9b) is
the real evidence. `--doc original` = **C0 baseline**; default = **C1**
(generated readme). Use the same seed/sample across C0/C1/C2 so the sampled APIs
match; C0 gets the original docs as the only context, C1 the per-API entries. If
`comprehension.execute.sample_data` is configured, those variable names/paths are
also shown to the audience model so cheap comprehension uses the same fixture
vocabulary as execute mode (but it still does not run anything). `--sample N`
(default 5); `--sample 0` = all entries. `--show-code` includes the generated
snippet in JSON details.

### 9b. `aideal comprehension --execute`  (LLM + Spark, the execution truth)
The real ground truth — does doc-derived code actually compile and run?
1. **Targets = the intended-API surface** (`codebase.surface_filter`), i.e. the
   set documented in `LLM_readme.md` — general/codebase-agnostic, not a
   class list. Narrow further with `comprehension.execute.include`/`exclude`;
   `--sample N` to subsample.
2. **Per API**, up to `1 + max_fix_rounds` attempts:
   - audience model writes a snippet (prompt given the typed `sample_data`
     catalog + that API's **prior failures** pulled from the error log);
   - strip code fences; optionally strip generated imports
     (`comprehension.execute.strip_snippet_imports`) when the scaffold owns
     imports; splice into the scaffold; inject sample-data `val`s as `file://`
     URIs (local FS);
   - `scalac` (classpath = beast lib + Spark jars + uber, colon-joined) → `jar`
     → `spark-submit --class GeoJobMain` (`--jars` beast lib, `--packages`
     GeoTools/JTS/units from the osgeo `--repositories`), run via shell;
   - **PASS** iff exit 0 + `__DONE__` + no `__RUN_ERR__`.
3. **Log** every failure to `logs/error_log.jsonl` (categorized:
   `error_category` compile/runtime/timeout, `error`, `root_cause` = failing
   line/call, `code` = the snippet). On a retry that passes, log a `fixed`
   record (error → working `suggested_fix_code`). Accumulates across runs;
   `failures_for(api)` feeds the next attempt.
Result: pass-rate + `coverage` with **three explicit denominators** —
`raw_surface` (113, every visible public def), `intended_surface` (41 with
`intent_score`, the set documented/tested by design), `executed` (N, the sampled
or full subset actually compiled/run). Report all three; don't conflate them.
With `--show-code`, execute details also include the generated snippet, the
written `ApiTest.scala` path, exit code, and stdout/stderr tails; tail length is
configurable via `comprehension.execute.output_tail_chars`.

### (deferred) `--augment-from-log`
Fold observed `fixed` solutions back into each entry's Common Failure Modes /
Fix Code Hint (predicted → observed). Build after a real execute sweep.

## Three signals for the report
| Signal | Command | Judge | Spark | Measures |
|---|---|---|---|---|
| Coverage | `completeness` / `form` | static | no | intended-API documented to standard |
| Doc consistency | `comprehension` (C0/C1) | author LLM | no | doc internally usable |
| Execution truth | `comprehension --execute` | compiler+Spark | yes | doc → code that runs (intended API) |

Conditions (same seed = same sampled APIs): C0 original docs · C1 generated
`LLM_readme.md` · C2 curated `rdpro_api_doc_combined.md`.

## Run order
```bash
# no key
aideal profile && aideal api-surface && aideal api-tests
aideal completeness && aideal scaffold --generate
# key
aideal readme --generate --limit 0 --force
aideal form
aideal comprehension --doc original --sample 0     # C0 all intended APIs
aideal comprehension --sample 0 --show-code        # C1 all + generated snippets
# key + Spark/Maven (geo_llm_spark)
aideal comprehension --execute --sample 1 --show-code   # smoke 1 op + stdout/stderr tail
aideal comprehension --execute                       # full intended surface (41 with intent_score)
```

## Environment
| Need | Stages |
|---|---|
| nothing | profile, api-surface, api-tests, completeness, scaffold, form |
| OpenAI key | readme --generate, comprehension (±execute), puzzle |
| scalac + spark-submit + GeoTools `--packages` (geo_llm_spark) | comprehension --execute, puzzle |

## Where to configure what (`configs/aideal.yaml`)
- intended-API set (documentation + completeness + execution) → `codebase.surface_filter`
  (`intent_score` recommended; else `all`/`documented`/`tested`/`non_override`/…)
- intent scoring → `codebase.intent` (`threshold`, `weights`, `manual_include`/`exclude`, `exclude_name_patterns`); audit with `aideal intent`
- narrow execution further → `comprehension.execute.include`/`exclude`
- sample data by type → `comprehension.execute.sample_data` (`file://` auto)
- plain comprehension also receives `sample_data` as available input variables,
  but does not inject bindings or run code
- classpath/build → `jars`, `uberjar`, `build`; run line → `command`
- scaffold imports → `comprehension.execute.imports` (curated) or auto
- snippet/output controls → `comprehension.execute.strip_snippet_imports`,
  `output_tail_chars`
- repair rounds → `comprehension.execute.max_fix_rounds`
- the agent's persona/domain → `configs/project_profile.yaml` (`role`, domain, …)
