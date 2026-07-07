# AIDEAL — design flow (init → comprehension test, with fix loop)

This is the **design flow**, not the runtime trace: what each stage is *for*, where its
code and its LLM prompt live, how the stages relate through shared stores, and where each
piece is going next. Read the diagram top-to-bottom; read this for the detail behind each box.

Two node types in the diagram:

- **LLM-prompt step** (purple) — calls a model with a prompt template in `default_prompts/aideal/`.
- **Code / static step** (teal) — deterministic Python, no model.

All paths are relative to `grail-agent/src/aideal/`.

---

## 1. The stages

### 0 · Init / Profile — *code*
`cli init` → `profile.py`. The human fills `project_profile.yaml`: target **author** model,
**audience** model, domain, use-cases, hard constraints. Nothing downstream runs without it —
it's the grounding injected as `{project_context}` into every prompt. This is the one place a
person supplies intent; everything after is derived.

### 1 · Static surface discovery — *code*
`api-surface`, `api-tests`, `scaffold` → `readme_agent.public_api_details` / `visibility_model` /
`api_test_examples`. Parses the codebase into the public API surface, mines **passing** usage out
of the existing test suite (the strongest static grounding), and generates the runnable test
scaffold. No model — this is the evidence base the doc is later grounded on.

### 2 · Intent — *LLM*
`cli intended` → prompt **`intent_common.md`**. Selects the commonly-used, user-facing subset of
the surface (not lifecycle/iterator/serializer plumbing), so you document the ~200 APIs a user
actually calls, not the ~2000 raw defs. Static scoring proposes; the model only adjudicates the
ambiguous band.

### 3 · README generation — *LLM*
`readme --generate` → `readme_agent.find_or_create`, prompts **`readme_distill.md`** (distill the
original project docs into grounding notes) then **`readme_entry.md`** (write one entry per API
from *authoritative API facts + passing tests + distilled context*). Each entry is stamped with a
**grounding tier**: `verified > grounded > sibling > guessed`. Output: the flat `LLM_readme.md`
(one `## API Test:` section per API). The prompts forbid inventing parameters/call-shapes — call
forms are reproduced from tests or the original README, never guessed.

### 4 · Grounding + Catalogue / index — *code*
`grounding`, `organize`, `catalogue` → `readme_agent._grounding_tiers`, `organize_report`,
`write_catalogue`. Groups entries by defining class and emits the two-level shape:
`LLM_readme_index.md` (the catalogue: per class → purpose, how to obtain the receiver, its APIs
with tier badges, primary marked) + `api/<Class>.md` (per-class shards). This is the **function
index** — it turns the flat 550 KB README into a *scan-then-open* structure. No model; it's a
render over Stage-3 data. (Collision-safe filenames as of 2026-07-01.)

### 5 · Comprehension test = README unit test — *LLM* + **fix loop**
`comprehension [--execute]` → `doc_checks.comprehension_check` / `_comprehension_execute`.
The **audience** model writes code from the doc *alone* (**`comprehension_write.md`**, or
**`comprehension_write_exec.md`** for the runnable path); the **author** model grades it
(**`comprehension_grade.md`**) — or, with `--execute`, it's compiled and run for real.

- **Fix loop** (`--execute`): write snippet → compile+run via scaffold → on failure,
  `fix_guide.classify` turns the compiler error into a *category + targeted hint*, which is
  injected alongside the accumulated `known_failures` into the next round. Retries up to
  `max_fix_rounds`. Build-gap (`NoClassDefFound`) failures are marked **infra** and excluded from
  the score, so the pass rate measures doc quality, not your classpath.
- **Catalogue read (index-first)**: when `class_context` is on, the tested API's write prompt is
  prefixed with its catalogue class header — *how to obtain the receiver* + *a verified sibling's
  proven call pattern* — so the model stops inventing the receiver (see §4 of the prompt appendix).

Every run appends `pass` / `fail` / `fixed` records (with the working or failing snippet) to the
error log.

### 6 · Feedback / consolidation — *code (+ small LLM)*
`augment`, `notes-distill`, `alias-suggest/add`.
- **`augment_from_log`** folds a *passing* snippet back into the entry's `Valid Call Patterns`
  (promoting it to `verified`), and failures into `Common Failure Modes` + `Fix Code Hint`.
- **`notes_to_self.distill`** consolidates repeated failures into compact lessons.
- **`alias_functions`** promotes a recurring, verified fix into a wrapper in `GrailAliases` so the
  next generation calls one grounded, type-correct name.
This is the improvement loop: evidence in the log makes the doc better on the next pass.

### 7 · Puzzle / integration test — *LLM* + *code*
`tasks` / `puzzle` → `task_generator` (prompt **`tasks_generate.md`**) + `doc_checks.puzzle_check`.
Composes K sampled APIs into a natural-language task and runs it through the same notes+log fix
loop — integration-level rather than per-API.

---

## 2. Shared stores & design relationships

The stages don't call each other directly; they meet through five persistent artifacts. This is
the "relationship" layer (who writes / who reads), which is the real coupling in the design.

| Store | Written by | Read by | Role |
|---|---|---|---|
| `LLM_readme.md` | 3 README-gen; refreshed by 6 augment | 4, 5, 7 | the doc = source of truth |
| Catalogue: `LLM_readme_index.md` + `api/<Class>.md` | 4 catalogue | **5 (class_context)** | scan-then-open function index |
| `error_log.jsonl` | 5 comprehension, 7 puzzle | 6 augment/distill/alias | append-only pass/fail/fixed memory |
| `notes_to_self.md` | 6 distill | injected into 5 & 7 prompts | consolidated lessons |
| alias registry + `GrailAliases.scala` | 6 alias | 1 surface, 3 README | recurring fix → grounded name |

The two loops that matter: **error_log → augment → LLM_readme** (doc improves from execution
evidence) and **catalogue → comprehension write-prompt** (the doc is fed back in as receiver
grounding). Everything else is a one-way derive.

---

## 3. Where the LLM is — prompt inventory

| # | Prompt file | Role | Model role | Called from |
|---|---|---|---|---|
| 1 | `readme_distill.md` | original docs → grounding notes | author | `distilled_readme_context` |
| 2 | `intent_common.md` | pick user-facing APIs | author | `intent` |
| 3 | `readme_entry.md` | write one API doc entry | author | `find_or_create` |
| 4 | `comprehension_write.md` | audience writes code (graded) | audience | `comprehension_check` |
| 5 | `comprehension_write_exec.md` | audience writes runnable code | audience | `_comprehension_execute` |
| 6 | `comprehension_grade.md` | grade code vs doc (PASS/FAIL) | author | `comprehension_check` |
| 7 | `probe_write.md` | probe an undocumented function | audience | `probe.run_probe` (opt-in) |
| 8 | `tasks_generate.md` | generate benchmark tasks | author | `task_generator` |
| + | inline in `_resolve_preamble` / `_resolve_io_hints` | auto-derive I/O grounding from reader docs | author | `_comprehension_execute` |

`prompts.load()` fills `{project_context}` / `{language}` automatically; every other `{placeholder}`
must be passed by the caller (a missing one is a hard `KeyError` — that's the bug the receiver
slot caused earlier).

---

## 4. The prompt when it must "get the API from the catalogue README"

This is Stage 5's `--execute` write prompt **with `class_context` on**. `_class_context_body`
(`readme_agent.py`) reads the catalogue model and prepends a class header to the API's own body;
the whole thing is passed as `{api_body}` into `comprehension_write_exec.md`. So the model first
sees *how to obtain the receiver + a proven sibling call*, then the target API.

**(a) The injected class header** (built from the catalogue, no LLM call):

```markdown
## Class context — `RasterOperationsLocal`
_<one-line purpose, from the class's primary entry Goal>_

**Obtaining the receiver:** instance — obtain a `RasterOperationsLocal` value, then `<value>.<method>(...)`

**Proven setup from a verified sibling `overlay` — reuse its receiver/imports, then call `mapPixels` instead:**
```scala
val rasterRDD: RasterRDD[Float] = sc.geoTiff[Float](rasterPath)
val out = rasterRDD.overlay(otherRaster)
```

---
<the target API's own LLM_readme entry: Signature / Goal / Params / Valid Call Patterns / …>
```

**(b) The template it's spliced into** (`comprehension_write_exec.md`, abridged — full text in the
appendix). Note the header above arrives as `{api_body}`, and `{receiver}` is the separate
type-hint line:

```text
SYSTEM: You write {language} code spliced into a runnable harness. A SparkContext `sc`
is in scope, plus typed input-path variables. Use ONLY the documentation provided …

USER:
Documentation:
{api_body}            ← the class header + the target entry (from the catalogue)

Available input path variables already in scope:
{available_inputs}

RECEIVER — call `{api_name}` on the RIGHT type …:
{receiver}

{known_failures}      ← replayed from error_log for this API

Write minimal body statements that use `{api_name}` correctly … end with a
correctness check: require(<non-degenerate>) then println("__CHECK__ {api_name} " + witness).
{io_hints}
{exec_hints}
```

The design point: the receiver — the #1 failure class (`value X is not a member`) — is grounded
**three** ways that reinforce each other: the `{receiver}` type hint (from `_owner_map`), the
`class_context` proven sibling (from the catalogue), and `{io_hints}`/preamble (auto-derived).

---

## 5. Roadmap — designed but not yet built

- **Fix loop** — today it's per-API and the puzzle picker samples **random** K. Next: type-compat
  *smart* sampling (compose functions whose types actually connect), and a **verified chain** as
  the doc unit (a working multi-function pipeline), not just isolated calls.
- **Fix hint + error log** — hints are generic categories today; next is type-signature-aware
  hints, and a fuller **staleness** rule (invalidate an example when the library version moves —
  the `library_version`/`timestamp` fields exist; the invalidation policy is partial).
- **Summarize (`notes_to_self`)** — distills **failures only**. Next: distill *successes* too, and
  reuse a verified call as a **prior** for sibling functions (cross-function transfer).
- **Alias function** — promotion is manual. Next: an auto-promotion policy from error-log
  frequency + alias metrics (distinct aliases per canonical), and the wrapper getting its own
  `LLM_readme` entry so it enters the loop like any API.
- **Function index (catalogue)** — the index-first read path is wired into **comprehension only**.
  Next: switch `augment` / `grounding` / `organize` to read the shards too, so the whole pipeline
  stops loading the flat 550 KB file.

---

## Appendix — full prompt texts

### `intent_common.md`
```text
SYSTEM:
{project_context}

Using the role and domain above, identify which functions form the COMMONLY-USED,
user-facing API of this codebase — the operations a typical user actually calls in
real workflows — as opposed to internal helpers, lifecycle / iterator / serializer
plumbing, framework callbacks, builders, or rarely-used accessors. Judge each
function by what it does (its domain meaning and signature), not by its name
length or superficial wording.

USER:
Candidate functions (name: signature):
{api_list}

Return ONLY a JSON array of the names that are commonly-used, user-facing
operations — nothing else. Example: ["functionA", "functionB"].
```

### `readme_entry.md` (core)
```text
SYSTEM:
You write LLM-facing API documentation in an exact markdown template. You ground
every fact in the provided API facts and context. You NEVER invent parameters,
types, return values, or APIs. If something is unknown, say so.
{project_context}

USER:
Document the {language} function `{api_name}` of {project_name}.

Authoritative API facts (JSON — do not contradict; do not add parameters/types):
{api_facts}

Project context distilled from the original README (grounding):
{original_readme_context}

Real usage from the project's existing test suite (these compile and pass — base
Valid Call Patterns on them; may be empty):
{test_examples}

Verbatim example(s) from the ORIGINAL README that call `{api_name}` (may be empty):
{original_examples}

GROUND THE CALL FORM by combining the sources above, in priority order — NEVER
invent a call shape that appears in none of them:
1. test-suite example is authoritative (it compiles + passes);
2. else the original-README example;
3. if both, reproduce a real form verbatim; when they differ, prefer value.{api_name}(...);
4. if neither, derive from the Signature and SAY the example is inferred (not verified).
Preserve the receiver/qualifier EXACTLY — do not collapse Object.m(...) / value.m(...)
to a bare m(...). State PRECONDITIONS and TYPE-PARAMETER selection rules explicitly.
Output ONLY the filled template.
{template}
```

### `comprehension_write.md` (graded path)
```text
SYSTEM:
You write {language} code. You may use ONLY the documentation provided — no other
knowledge of the library. If input variables are listed, use those names rather
than inventing paths. Output only code.
{project_context}

USER:
Documentation:
{api_body}

Available input path variables, if useful:
{available_inputs}

Write a minimal snippet that uses `{api_name}` correctly per the documentation.
Verify with a LIGHTWEIGHT action only (.count(), .first(), print one value). Keep
the snippet focused on `{api_name}`.
```

### `comprehension_write_exec.md` (execute path — the catalogue-read prompt)
```text
SYSTEM:
You write {language} code that will be spliced into a runnable test harness. A
SparkContext `sc` is in scope, plus the typed input-path variables listed. Common
RDPro/Beast/Spark classes are already imported by the scaffold. Pick the input
variable(s) whose type matches the API's parameters. Do NOT create a
SparkSession/SparkContext, redeclare variables, or write imports/object/main —
output ONLY the body statements. Use ONLY the documentation provided.
{project_context}

USER:
Documentation:
{api_body}

Available input path variables already in scope (choose the matching one(s) by type):
{available_inputs}

RECEIVER — call `{api_name}` on the RIGHT type (calling it on the wrong receiver is
the #1 failure; if it is an instance method, first obtain a value of the owner type):
{receiver}

{known_failures}

Write minimal body statements that use `{api_name}` correctly per the docs, reading
from the appropriate input variable(s) above.
{io_hints}
The snippet MUST EXECUTE and VERIFY correctness — force materialization, compute a
small witness (count/size/sampled value), assert it is non-degenerate with
require(...), then print exactly: println("__CHECK__ {api_name} " + <witness>).
{exec_hints}
```

### `comprehension_grade.md`
```text
SYSTEM:
You grade whether code calls an API CORRECTLY per its documentation. Reply `PASS`
or `FAIL: <reason>`. Judge ONLY API-call correctness (name, args, receiver/return,
hard constraints). Do NOT fail for omitted defensive checks, not saving output, or
style. If the call is correct and no constraint is violated, reply PASS.

USER:
Documentation:
{api_body}

Candidate code:
{code}

Hard project constraints that must hold:
{constraints}
```

### `probe_write.md` (opt-in Version B)
```text
SYSTEM:
You write {language} code spliced into a runnable harness to PROBE one function
whose documentation does not exist yet. `sc` and typed input-path variables are in
scope. You are given ONLY the SIGNATURE — invent nothing. Find a call that compiles
and runs so its real behavior can be documented afterward. A loader that returns an
RDD/Dataset is usually sc.name(...); an operation on a value is usually value.name(...).
Output ONLY the body statements.
{project_context}

USER:
Probe the {language} function `{api_name}`. You have only its signature:
- signature: {signature}
- parameters: {params}
- returns: {returns}

Available input path variables already in scope:
{available_inputs}
{known_failures}

Invoke `{api_name}` with type-matched input(s), then VERIFY it did something (Spark
is lazy): materialize, require(n > 0, "empty result for {api_name}"), and print
println("__CHECK__ {api_name} " + n).
{io_hints}
{exec_hints}
```

### `tasks_generate.md`
```text
SYSTEM:
You design verifiable benchmark tasks for coding agents.
{project_context}

USER:
Available documented APIs:
{api_list}

Write {n} benchmark tasks grounded in the project's use cases.
Rules: solvable using ONLY the listed APIs (3-5 per task); goal = one NL sentence a
user would ask; result verifiable from output (count/CSV/file); no API combo twice.
Output YAML only:
tasks:
  - id: short_snake_case_id
    language: {language}
    goal: "..."
    apis: [api1, api2, api3]
```
