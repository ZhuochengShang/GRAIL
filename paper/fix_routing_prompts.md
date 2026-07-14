# Fix-routing prompts — original vs doc-repair (2026-07-07)

Two fix routings now exist. Both are prompt-file driven
(`grail-agent/src/aideal/default_prompts/aideal/`; a project `prompts/` dir
overrides them for ablations).

## Routing A — ORIGINAL (snippet-retry). `aideal comprehension --execute`

One prompt serves both the first write (round 0) and every fix round: on a
retry, `{known_failures}` is filled with the last ≤4 failures for this API
(error text + fix hints + any fix-that-worked), and the model rewrites the
SNIPPET. The documentation never changes. Measured on RDPro: gpt-4o rescued
3/158 failures this way; gemini-2.5-pro 26/128; identical-error loops were
common (stuck detector now stops those after 3 repeats).

File: `default_prompts/aideal/comprehension_write_exec.md` (verbatim):

```
SYSTEM:
You write {language} code that will be spliced into a runnable test harness.
A SparkContext `sc` is in scope, plus the typed input-path variables listed in
the task. Common RDPro/Beast/Spark classes and operation-object members are
already imported by the scaffold. Pick the input variable(s) whose type matches
the API's parameters (e.g. a raster `.tif` path for raster ops; a vector
`.geojson`/`.shp` path or a geometry for vector / zonal-stats ops). Do NOT create
a SparkSession/SparkContext, do NOT redeclare those variables, do NOT write
imports, an object, or a main — output ONLY the body statements that exercise the
API. Use ONLY the documentation provided. Output only code, no markdown fences.

{project_context}

USER:
Documentation:
{api_body}

Available input path variables already in scope (choose the matching one(s) by type):
{available_inputs}

RECEIVER — call `{api_name}` on the RIGHT type (calling it on the wrong receiver is
the #1 failure; if it is an instance method, first obtain a value of the owner type,
do NOT call it on an unrelated preloaded input):
{receiver}

{known_failures}

Write minimal body statements that use `{api_name}` correctly per the docs,
reading from the appropriate input variable(s) above.
{io_hints}
The snippet MUST EXECUTE the operation AND VERIFY the result is correct — not just
that it ran (some frameworks defer/lazily evaluate, and a wrong pixel TYPE can read
garbage without throwing). End with a CORRECTNESS CHECK:
- force the result to materialize and compute a small witness of it — a count, a
  size, or a sampled element;
- assert the witness is NON-DEGENERATE with `require(...)`, so a wrong type or an
  empty output fails loudly instead of silently passing. E.g.
  `require(n > 0, "empty result for {api_name}")`, or for a sampled numeric value
  require it is finite (not NaN/Inf) and in a plausible range;
- then print it as a STRUCTURED line exactly like:
  `println("__CHECK__ {api_name} " + <witness>)`.
If `{api_name}` is itself the writer/output API, write to `output_dir`, then
`require` the output exists / is non-empty and print the same `__CHECK__` line.
Do not call other heavyweight operations unless `{api_name}` is the writer; keep the
body focused on `{api_name}` so the run isolates that one call.
{exec_hints}
```

The `{known_failures}` block a fix round sees (rendered by
`ErrorLog.failures_for`, last ≤4 rows):

```
Prior failures for `<api>` — avoid repeating these:
- [<category>] <error text ≤200 chars>  (at: <root cause ≤120 chars>)
  suggested fix: <FIX_GUIDE hint ≤300 chars>        # or "fix that worked: <code>"
```

## Routing B — NEW (doc-repair). `aideal fix-docs`

Per failed API: (1) failed function from the error log → (2) canonical
definition located (`file:line`, dedup election) and ±15/+80 source lines
read → (3) SENIOR-ENGINEER diagnosis against the real source → (4) the API's
readme entry is REWRITTEN folding the diagnosis in → (5) the comprehension
test re-runs with the repaired entry. Entry kept on pass, reverted on fail
(catalog is monotonically non-worse). The failure is treated as evidence
about the DOC — the artifact GRAIL actually ships.

### Step-3 prompt: `default_prompts/aideal/docfix_diagnose.md` (verbatim)

```
SYSTEM:
You are a SENIOR ENGINEER on the {project_name} ({language}) codebase — you
wrote parts of this library and know its idioms. A documentation-driven test
failed: a code snippet written ONLY from the API's documentation entry did not
compile or run. Your job is to find the ROOT CAUSE by reading the REAL SOURCE
CODE below — not to guess. The documentation may be wrong, incomplete, or
missing a critical detail (receiver type, required import, Java-defined type,
parameter semantics, lazy evaluation, required option). The snippet may also
have misread correct documentation — say so if that is the case.

Be precise and grounded: every claim you make must be checkable against the
source shown. If the source window is insufficient to be certain, say what is
missing instead of inventing.

{project_context}

USER:
API under test: `{api_name}`

== REAL SOURCE (canonical definition and surrounding context) ==
{source_window}

Other definition sites for this name: {other_sites}
Receiver/owner type hint: {receiver}

== CURRENT DOCUMENTATION ENTRY (what the snippet-writer saw) ==
{entry_body}

== FAILING SNIPPET (written from that entry alone) ==
{snippet}

== ERROR ({error_category}) ==
{error}

Codebase stack frames reached (empty = failed before entering library code):
{frames}

Respond in EXACTLY this structure:

ROOT CAUSE:
(1-3 sentences: why this failed — doc gap / doc error / snippet misread /
environment. Name the exact missing fact, e.g. "Collector is a Java class in
edu.ucr.cs.bdlab.raptor and is not imported by default".)

CORRECT USAGE:
```{language_lower}
(a minimal, compilable call sketch using the REAL types and receiver from the
source — the statements only, no imports/object wrapper)
```

REQUIRED TYPES & IMPORTS:
(each fully-qualified type the caller must know about, one per line, with the
package it lives in and whether it is Scala- or Java-defined)

DOC MUST SAY:
(bullet list: the specific sentences/facts the documentation entry MUST
contain so a model writing code from the entry alone cannot repeat this
failure)
```

### Step-4 prompt: `default_prompts/aideal/docfix_rewrite.md` (verbatim)

```
SYSTEM:
You are the documentation engineer for the {project_name} ({language})
library. Rewrite ONE API documentation entry so that a code-writing model,
seeing ONLY this entry (never the source), produces code that compiles and
runs on the first try. A senior engineer has diagnosed why the previous entry
failed — fold every fact from that diagnosis into the entry. Ground every
statement in the diagnosis and source excerpt; do not invent behavior.

Hard rules:
- Output the COMPLETE entry and NOTHING else, starting exactly with:
  `## API Test: `{api_name}``
- Keep these section headings (same order, same names): {required_sections}
- `Valid Call Patterns` must contain the corrected, compilable call sketch —
  including any REQUIRED imports/types the caller must reference, stated
  explicitly (e.g. "requires `edu.ucr.cs.bdlab.raptor.Statistics` — a JAVA
  class; reference as `classOf[Statistics]`").
- `Common Failure Modes` must list the failure that just happened, phrased so
  a model recognizes it BEFORE writing code.
- `Fix Code Hint` must show the wrong form and the corrected form.
- Add the line `_Grounding: doc-repaired from source (docfix)._` right after
  the title.
- Be compact: no marketing prose, no repetition; every line must inform code.

{project_context}

USER:
API: `{api_name}`

== SENIOR-ENGINEER DIAGNOSIS (authoritative — fold ALL of it in) ==
{diagnosis}

== REAL SOURCE (for signatures/types; do not paraphrase beyond it) ==
{source_window}

== PREVIOUS ENTRY (being replaced — keep what was right, fix what was wrong) ==
{entry_body}

Write the replacement entry now.
```

### Step-5 prompt

The retry reuses Routing A's `comprehension_write_exec.md` unchanged — by
design: the ONLY thing that changed between the failing run and the retry is
the documentation entry, so a pass is attributable to the doc repair.

## Model choice — use the SWE-optimized text model, NOT the tool-calling variant

The doc-repair runs use `google:gemini-3.1-pro-preview` (verified in every
`docfix_*.json` `model` field). This is the correct coding model for GRAIL:

- GRAIL's harness is TEXT-IN / TEXT-OUT. `invoke_text` does
  `llm.invoke([system, user]) -> text`; there is NO `bind_tools`, no
  function-calling, anywhere in the pipeline. The diagnose step returns
  prose+code as text; the retry step returns a code snippet as text.
- Therefore `gemini-3.1-pro-preview` (described as "optimized for software
  engineering") is the right pick. The `-customtools` endpoint is tuned for
  models that CALL bash/custom tools — a capability GRAIL never invokes;
  using it wastes the specialization and can bias output toward tool-call
  JSON instead of clean code.
- Verify the model your account actually served: every report carries
  `"model": "google:gemini-3.1-pro-preview"`; the per-API `by_model` token
  split in the run header confirms which model wrote each snippet/diagnosis.
  Pin it explicitly with `--role fixer=google:gemini-3.1-pro-preview`
  (and `--role audience=...` if the RETRY should also use it).

## Usage & the experiment it enables

```bash
aideal fix-docs --dry-run                          # list target failures
aideal fix-docs --api zonalStatsLocal              # one API (~2-4 min)
aideal fix-docs --max-apis 20 --timeout 300 \
  --role fixer=google:gemini-2.5-pro               # batch
```

Comparison for the paper: same failure set → Routing A rescue rate
(snippet-retry: 3/158 gpt-4o, 26/128 gemini) vs Routing B doc-fix rate — and
Routing B's fixes PERSIST in the catalog (every later run benefits), while
Routing A's fixes evaporate after the run. Cost per API ≈ 2 LLM calls +
1 retry execute.
