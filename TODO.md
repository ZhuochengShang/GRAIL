# GRAIL — next todo (meeting 2026-07-06)

Six workstreams. Rule for all of them: **every claim gets a number** (counts,
fractions, token costs, pass rates) and every comparison is a git-branch /
config condition so it can be re-run.

## 1. Reduce redundancy in the API surface / intent catalog

**Problem.** The surface the agent sees still carries redundant entries:
overloads, alias duplicates, near-identical signatures, and catalog text
(`docs/LLM_readme.md`) that repeats the same operation under several names.

**Do.**
- Dedup pass over `aideal api-surface` output: group by (normalized name,
  param types), collapse overload families to one canonical entry + variants.
- Cross-check the alias registry (`experiments/rdpro/aliases/GrailAliases.scala`)
  vs catalog: an alias should point at its canonical API, not appear as a
  second first-class entry.
- Add `aideal intent --dedup-report`: for each collapsed group, which member
  was kept and why (intent_score, doc quality).

**Quantify.** raw surface → post-intent → post-dedup; tokens of
`LLM_readme.md` before/after; comprehension pass rate must not drop after
dedup (re-run `comprehension_check`).

**STATUS 2026-07-06 — implemented (see `CHANGES_2026-07-06.md`).**
Numbers (full beast tree; old "113→41" was a module-scoped glob):
raw 820 (was 826; `this` constructor artifact excluded) → intent-selected
**205** static (was 218; code-context doc mentions + many_impls fan-out
penalty dropped 13 interface-plumbing names, all 12 demo APIs kept) →
**203** catalog entries after full-forwarder aliasing (`aideal dedup`,
report in `docs/dedup_report.json`). Catalog today ≈138K tokens (552,866
chars). Telescoping overloads (same function, different parameter lists)
subsume into the **longest needed signature**: 19 sites / 17 names; facade
paths (`Java*.scala`) deprioritized in canonical election so geoTiff /
raptorJoin / shapefile document the Scala-mixin forms the preamble verifies.
New failure class identified 2026-07-07 (zonalStatsLocal, correct snippet,
3× "not found: type Collector"): **signature types defined in JAVA sources
are invisible to Scala-only import mining** — quick-fixed via
`extra_imports: edu.ucr.cs.bdlab.raptor._`; the general fix is type-import
derivation: parse each entry's signature types and import their owning
packages (scan .java too). This is the unbuilt "type-sig transfer" item.

Remaining (needs OPENAI_API_KEY, run on Mac):
- regenerate the catalog from the 205-surface → before/after token count;
- re-run comprehension on the new surface → pass rate must not drop;
- `aideal intent-compare` to refresh the LLM-arm selection (old cache was
  an empty `[]` — now treated as a miss, will re-judge).

**Files.** `grail-agent/src/aideal/{readme_agent.py,cli.py,adapters/scala-spark.yaml}`,
`grail-agent/tests/test_intent_dedup.py`, `experiments/rdpro/docs/{dedup_report.json,decision_log.json}`.

## 2. Justify every pipeline decision quantitatively

**Problem.** Decisions (intent threshold = 5, sample = 5, weight vector,
grounding tier order, doc-section budget) are currently asserted, not derived.

**Do.** For each decision point in `PIPELINE.md`, record the *basis*:
- token-based? (fits a context budget — state the budget and measured tokens)
- fraction-based? (e.g. threshold chosen so selected/total ≈ target fraction)
- evaluation-based? (sweep the knob, report pass-rate curve, pick the elbow)

Emit a machine-readable `docs/decision_log.json`: one entry per decision =
{knob, value, basis: token|fraction|eval, evidence, alternatives tried}.
Sweeps to actually run: intent threshold ∈ {3,4,5,6,7} → surface size +
comprehension pass rate; comprehension sample ∈ {3,5,10} → variance.

**STATUS 2026-07-06 — started.** `docs/decision_log.json` exists with 7
entries: threshold=5 (justified by count sweep 533/258/205/194/102),
many_impls, docs_mention_mode, `this` exclude (justified); sample=5,
class_context, catalog-regen marked pending-evidence (need API key).

**Files.** `experiments/rdpro/PIPELINE.md`, `configs/aideal.yaml`
(`codebase.intent` weights), new `docs/decision_log.json`.

## 3. Agent-in-the-loop error fixing + ablations (all quantified)

Three controlled comparisons, each on the same task set
(`demo_test_cases.md` groups) with fixed seeds/models:

| # | Condition A | Condition B | Metric |
|---|---|---|---|
| 3a | deep-dive fix agent (e.g. Gemini) reads error_log + source, iterates | single-shot, no fix loop | pass rate, #iterations, tokens, wall time |
| 3b | intent-clean surface (41, deduped) | raw surface (113) | pass rate, wrong-API-choice count, tokens |
| 3c | with catalog API (`LLM_readme.md` / MCP `read_doc`/`search_doc`) | no catalog (source-only) | pass rate, grounding-tier hits, tokens |

- 3a builds on `logs/error_log.jsonl` + `fix_guide.py`; the fix agent gets
  the augmented error log as input — this is the error-log payoff experiment.

**STATUS 2026-07-06 — harness ready, runs pending keys.** New `fixer` role
(fallback audience) + `--role role=provider:model` + `--max-fix-rounds` CLI;
per-API metrics (attempts, pass_round, wall, provider-reported tokens,
per-model split) in comprehension `--execute` output;
`bench_conditions.py` runs 3a as `gemini_maxfix` (fixer=Gemini, rounds 99)
vs `no_fix` (rounds 0) vs default. See RUNBOOK section R.
- 3b reuses `docs/intent_all_llm.json` vs `intent_all_nollm.json` as a third
  arm (LLM-intent vs score-intent vs raw).
- Run as `aideal/*` branches in `experiments/rdpro/beast` per WORKING.md so
  each condition is a diffable branch; export via `export_changes.sh`.

**STATUS 2026-07-07 — Gemini doc-fix measured; Codex fresh-README condition set up.**
Gemini flat g1 result exists:
`results/bench/20260706_173509_g1_gemini_flat.json` → 90/207 scored pass
(43.5%; 11 infra excluded; pass@0 29.4%; mean attempts 2.83). Post-dedup full
comprehension: 77/196 scored pass (39.3%; 9 infra excluded). Gemini failed-subset
fix-all recovered 7/119 scored failures (5.9% marginal recovery; not a full
pass-rate denominator). Source-aware `aideal fix-docs` with Gemini attempted
117 failures, accepted 10 doc repairs (8.5%), rejected 35 rewrites for
fabricated members, skipped 11 not-testable APIs, and reverted 61 still-failing
entries. Current README has 15 repaired markers total; comparison report:
`docs/gemini_fix_comparison.md`.

Codex account/model smoke: available model IDs include `gpt-5-codex`,
`gpt-5.1-codex`, `gpt-5.1-codex-max`, `gpt-5.1-codex-mini`,
`gpt-5.2-codex`, `gpt-5.3-codex`; one-API `codex_api` smoke passed on
`setLong` with `gpt-5.3-codex`. Added `codex_suite.py` for g1/g4 and enabled
`aideal readme --role author=codex:...` so Codex can generate a fresh README.
Archived the Gemini-fixed README before overwrite at
`docs/codex_fresh_archives/20260707_115728/LLM_readme.gemini_docfix.md`, cleared
active `logs/error_log.jsonl` and `.aideal_exec/comprehension_progress.jsonl`,
and wrote the exact command/file checklist:
`docs/codex_fresh_comparison_files.md`.

## 4. Measure the automation ceiling

**Question.** How much of the pipeline runs with zero human input?

**Do.** Classify every stage (init → profile → api-surface → intent → docs →
comprehension → puzzle → demo) as auto / human-gated / human-optional, and
count the human tokens actually supplied (project_profile fields, fixture
pinning, surface_filter overrides, manual_include/exclude).

**Quantify.** automation fraction = auto stages / total; human-input tokens
vs pipeline tokens; then one experiment: run the pipeline with an empty vs
filled `project_profile.yaml` and report the pass-rate delta (what the human
context is worth).

**STATUS 2026-07-06 — baseline audit done (code + live Sedona run).**
*Automated once configured:* all static stages (surface/intent/dedup/
completeness/scaffold, no key) + all LLM stages (readme, comprehension+fix
loop, puzzle, error log, alias suggestions) given a key. LLM backends
openai/anthropic/google/ollama already exist in `llm.py` → item 5 needs only
config + keys, no code.
*Irreducible human inputs today:* project_profile (by design — persona gates
LLM stages), ~30-line project yaml, build wiring (jars/packages), fixtures
that semantically overlap, pinned preamble, API key.
*Generality, measured:* same-stack (Scala+Spark) new repo = config-only.
Any-language static = runs (12-language visibility defaults) **but two of
four evidence signals are Scala-hardcoded and die silently**: on Sedona
(Python) raw 670 names → **7 selected**, `documented` fired 0× (`_doc_above`
looks ABOVE the def; Python docstrings sit BELOW) and `tested` fired 0×
(`_TEST_BLOCK_RE` matches ScalaTest `test("…"){}` only, not pytest).
Fix path (small, adapter-level): per-language doc extraction direction +
per-adapter test-call patterns. Execution on a new stack = one new adapter
(~60 lines; `scaffold_frame`/`command` hooks already exist — only
scala-spark.yaml is written).

## 5. Backend comparison: OpenAI vs Gemini vs Ollama (local)

Same pipeline, same prompts, swap the coding model:
plain OpenAI (GPT/Codex-style) vs plain Gemini vs Ollama-served local code
model (e.g. qwen2.5-coder / codellama).

- Needs a backend abstraction in `grail-agent/src/aideal/llm.py` (author +
  audience roles both swappable; audience is the one that matters).
- Report per backend: comprehension pass rate, demo-suite pass rate, tokens,
  $ cost (0 for Ollama), latency.
- This doubles as the generality claim: the harness is model-agnostic.

**STATUS 2026-07-06 — mostly config now.** `llm.py` already had
openai/anthropic/google/ollama; added `codex` (OpenAI Responses API) for the
chat-vs-codex micro-benchmark. Any backend is one flag:
`--role audience=ollama:qwen2.5-coder`. `bench_conditions.py --table` gives
the per-backend comparison (pass rate, pass@0, attempts, tokens, wall, $ via
optional `results/bench/prices.json`).
**First comparison: gemini-2.5-flash vs gemini-2.5-pro on g1** (same flat
catalog; results keyed per model so both rows coexist). Decision rule: flash
within ~2pp (measured repeat variance) of pro → run the g2/g3/g4 ladder on
flash, keep pro for the headline arm. Runs strictly sequential — shared
checkpoint/error_log forbid parallel conditions in one project dir.
Codex fresh-README is a separate full-pipeline condition, not the same as the
same-README backend comparison: same README isolates the coding model; Codex
fresh README measures Codex as author + audience/fixer.

## 6. VLDB demo — stabilize user cases

**Goal.** Every case in `experiments/rdpro/demo_test_cases.md` passes
deterministically before the demo.

**Do.**
- Run `run_demo_suite.sh` N=5 times per case; mark each case
  stable / flaky / broken; keep the stable set as the demo script.
- Fix the Group 1 fixture gap: pin a real land-cover raster (NLCD) so the
  land-use % story works, per the note at the top of `demo_test_cases.md`.
- Freeze demo conditions: pinned model + temperature, pinned fixtures,
  cached fallback outputs (`results/*.json`) for offline/live-demo failure.
- Write the demo storyline: which cases shown live, which pre-baked, and the
  before/after (raw repo vs GRAIL-treated repo) moment.

**Quantify.** per-case pass rate over 5 runs; target: demo set = 100%.

## Order

1 → 2 are cheap and unblock 3 (clean surface + logged decisions are the
conditions being ablated). 3 is the paper's core evidence. 4–5 are additive
experiments on top of 3's harness. 6 runs in parallel with a hard deadline.
