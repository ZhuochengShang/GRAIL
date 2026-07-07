# GRAIL — Evaluation & Benchmarking Brief

*How to quantify the code an LLM generates from an AIDEAL-produced `LLM_readme.md`, what to
compare it against, which metrics to report, and how this positions against prior work.*

Date: 2026-06-30 · Case study: NL/Python → Spark-Scala on RDPro (Beast)

---

## 1. The question we are measuring

> Given **only a documentation condition** as grounding, how good is the code an LLM writes
> against a target API?

The **documentation condition is the independent variable**; **generated-code quality is the
dependent variable**. Everything else (audience model, sampled API set, seed, temperature,
number of samples) is held fixed across conditions. This isolates the doc — not the model — as
the thing under test, which is exactly AIDEAL's thesis: *"a doc is good only if a model with
nothing but the doc can use the API."*

---

## 2. Metrics (dependent variables), in three tiers

Report all three; lead with Tier A.

### Tier A — Execution truth (primary, the headline)
- **Compile rate** — fraction of generated snippets that compile (`scalac`).
- **Execution pass rate / pass@k** — fraction that compile *and* run to completion via
  `spark-submit` and produce the expected typed output. pass@k = problem solved if ≥1 of k
  samples passes (standard; report pass@1 and pass@5).
- **Functional correctness** — when a reference assertion or expected output exists (mined from
  the test suite), check output equality, not just "ran."

This is the "real evidence" path already implemented as `comprehension --execute`
(`scalac → jar → spark-submit`).

### Tier B — Doc-grounded comprehension (LLM-graded, no compiler)
- **Comprehension pass rate** — audience model writes code from the doc alone; author model
  grades strictly against the doc. Fast, no build toolchain, but it measures *internal doc
  usability*, not ground-truth correctness. Use as a cheap proxy and to scale to many APIs.

### Tier C — Static doc quality / coverage (no LLM)
- **Intended-API coverage / completeness** — of the intended-API denominator, how many are
  documented to standard.
- **Form compliance** — every entry has the required sections.
- **Alias overlap / mistake reduction** — Jaccard of proposed aliases across models; reduction
  in repeated error-log categories after augmentation.

### Secondary surface metrics (report, do not rely on)
- **CodeBLEU / exact-match** — cheap, but known to correlate weakly with functional
  correctness; include only for completeness/comparability.

### Cross-cutting: error taxonomy
Categorize every failure from `error_log.jsonl`: *wrong API / hallucinated parameter or type /
import or resolution error / runtime error / logic error.* The **shift in this distribution
across conditions** is often more informative than the scalar pass rate (e.g. "AIDEAL removes
most hallucinated-API errors but not runtime-config errors").

---

## 3. Baseline conditions (the comparison design)

Same sampled API set, same seed, same audience model, same k. Doc condition varies:

| Cond | Documentation given to the audience model | Role |
|------|-------------------------------------------|------|
| **C₋** | nothing — name only | absolute lower bound |
| **C_sig** | signature + types only (no prose) | "free" structural baseline |
| **C0** | original README + project docs | real-world baseline |
| **C1** | **AIDEAL `LLM_readme.md`** | **method under test** |
| **C2** | hand-curated combined docs | quality ceiling |

### Ablations of C1 (attribute *where* the gain comes from)
- C1 − LLM-intent (static intent only)
- C1 − test-grounding (no mined `test()` examples in entries)
- C1 − distilled-README context
- C1 − augmented-error / alias assets

### A second baseline family worth including: inference-time retrieval
Prior private-library work injects retrieved doc snippets at inference (APICoder/APIFinder,
EVOR, ExploraCoder). Add a **retrieval baseline** (RAG over the original docs) so the
comparison is "improve the codebase artifact (AIDEAL)" vs "retrieve at inference (RAG)" — this
is the core scientific contrast for the paper.

---

## 4. Controls & protocol

1. Fix the **intended-API set** (the `intent_score` surface) = the denominator and target set.
2. For each condition C, for each API, sample **k** audience completions at fixed temperature.
3. Run each through `comprehension --execute` → record compile + run + (where available) output
   correctness → pass@1, pass@5.
4. Log every failure with its category; build the per-condition error taxonomy.
5. Report Tier A primary, Tier B/C as support, ablations to attribute gains.
6. **Ground truth oracle** = the existing test-suite usage already mined by `api-tests`.
7. **Generalization**: rerun the identical pipeline on a second library (Apache Sedona) to show
   the method transfers across codebases, not just RDPro.

---

## 5. Related work / benchmarks to position against

| Work | Setting | Metric(s) | Why it matters to GRAIL |
|------|---------|-----------|-------------------------|
| **HumanEval/MBPP + EvalPlus** | standalone functions | pass@k (EvalPlus hardens tests 35–80×) | source of the pass@k metric; shows weak tests inflate scores |
| **DS-1000** | 7 Python data-science libraries | functional correctness + surface-form constraints | closest "library-oriented" eval; precedent for execution + constraint checks |
| **CoderEval** (ICSE'24) | non-standalone real-project functions, 6 context-dependency levels | functional correctness on a self-contained runner | justifies the whole premise: >70% of real functions are non-standalone and models do far worse on them — AIDEAL's APIs are non-standalone (need imports/context) |
| **CrossCodeEval / RepoBench** | repo-level, cross-file completion | exact-match / edit-sim, retrieval | repository context as a variable; AIDEAL supplies that context as a doc asset |
| **AutoAPIEval** (arXiv 2409.15228) | API-oriented, needs **only API documentation** | % correctly recommended APIs; % uncompilable; % unexecutable | **methodologically the closest** — adopt its compilable/executable rates directly; AIDEAL produces the very doc input it assumes |
| **Private-Library-Oriented CodeGen** (2307.15370, APICoder/APIFinder); **PriCoder / "To See is Not to Master"** (NdonnxEval, NumbaEval); **ExploraCoder**, **EVOR** | unseen/private libraries | pass@k on new benchmarks | the key contrast: they intervene at **inference** (retrieve docs / train the model). Their finding that *"even given accurate knowledge, LLMs still struggle"* is the motivation for intervening on the **codebase artifact** instead |

---

## 6. Positioning / novelty (one paragraph for the paper)

Almost all prior work on getting LLMs to use unfamiliar APIs intervenes at **inference time** —
retrieve documentation and inject it into context (APICoder/APIFinder, EVOR, ExploraCoder), or
fine-tune the model on synthesized usage (PriCoder). A repeated empirical finding is that *even
with accurate injected knowledge, models still fail to invoke the API correctly.* GRAIL takes
the orthogonal position that **the codebase itself is the unit of intervention**: instead of
patching the prompt at every call, we produce persistent, measurable LLM-ready assets
(structured per-API docs, aliases, augmented error logs, mined usage examples) and **quantify
the marginal effect of each asset** via a step-effectiveness curve. AIDEAL is the
codebase-agnostic harness that both builds and tests these assets; the comprehension/execute
loop turns "is this doc good?" into a falsifiable, execution-grounded measurement.

---

## 7. Suggested headline figures

1. **Pass@1 (execute) vs documentation condition** — grouped bars over C₋ / C_sig / C0 / C1 /
   C2 on the N intended APIs. The money figure.
2. **C1 ablation bars** — pass@1 as each AIDEAL asset is removed (attributes the gain).
3. **Error-taxonomy stacked bars** per condition — shows *which* failure classes AIDEAL removes.
4. **Step-effectiveness curve** — readiness delta as each LLM-ready asset is added, one at a time.
5. **Generalization** — the same C0→C1 lift reproduced on Sedona.

---

## 8. Immediate next actions

- Lock the intended-API denominator (decide raptor-only ~41 vs curated multi-module surface).
- Run the C0 / C1 / C2 execute sweep at fixed seed → figure 1.
- Add the RAG-retrieval baseline for the inference-vs-codebase contrast.
- Adopt AutoAPIEval's compilable/executable rates as named, citable metrics.
- Wire the error taxonomy export from `error_log.jsonl` for figure 3.
