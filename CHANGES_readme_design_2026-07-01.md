# What changed this session vs. the previous README design (2026-07-01)

**Previous design (Version A, unchanged in spirit):** enumerate public functions → intent-score to the commonly-used set → for each, build the doc from static evidence (existing test → tested sibling → else signature-only) → then execute-verify *downstream* (`comprehension --execute`) and fold passing snippets back with `augment`.

This session did **not** replace that. It (a) fixed two measurement bugs that were making the pipeline's own numbers untrustworthy, (b) removed the I/O confound that was dominating the failure rate, and (c) added an opt-in execution-first branch for the one case Version A can't ground. Every change is additive or a bug fix; the default Version-A flow is unchanged except where noted.

---

## The changes

| # | Change | Previous behavior | Now | File(s) |
|---|--------|-------------------|-----|---------|
| 1 | **Sticky-pass fix** | `_exec_status_map` set pass once and never downgraded; a plain `pass` also never upgraded a prior fail | Last-outcome by append order (append-only log = chronological); `fixed`/`pass`→pass, `fail`→fail | `readme_agent.py` |
| 2 | **Staleness guard** | `ErrorLog` had no version/time tag; `_augment_block` promoted `passed[-1]`/`fixed[-1]` by file order — a 3-commits-old verified example could be promoted as current | Added `library_version`+`timestamp` fields (+`git_version`); `_fresh`/`_recency_key` drop version-mismatched rows and pick the truly-newest | `error_log.py`, `readme_agent.py` |
| 3 | **Preamble pinned** | `preamble:` empty → every snippet reinvented Beast I/O; the `auto` path had grounded on the Java readers (→ `JavaRasterRDD`/`JavaSpatialRDD`, forcing invented `.toRDD` adapters) | Pinned to the Scala-mixin loads verified by your own passing rows: `rasterRDD: RasterRDD[Float] = sc.geoTiff[Float](...)`, `featuresRDD: RDD[IFeature] = sc.shapefile(...)` | `experiments/rdpro/configs/aideal.yaml` |
| 4 | **`auto` hardening** | Reader doc-entries chosen by name-regex, capped at 8, with no return-type signal → Scala/Java name collisions | Rank readers by how many documented ops **consume** their return type; drop shadow readers (return consumed by nothing); tell the model the target consumed types; post-filter unconsumed bindings | `doc_checks.py` |
| 5 | **io_hints ranking** | First-12-by-doc-order truncation dropped `shapefile` (#27) → always suggested geojson | Rank reader/writer entries by consumed-return before the cap, so central readers survive | `doc_checks.py` |
| 6 | **Version B probe (opt-in)** | Guessed-tier functions (no test, no sibling) got Goal/Valid Call Patterns written from the signature alone — nothing ran first | `probe_on_missing: true` runs the function once (signature → type-matched input → compile/run) and grounds the entry on the real pass/fail before writing. **Default OFF (parked).** | `probe.py` (new), `probe_write.md` (new), `readme_agent.py` hook |

---

## What each change buys you

**#1 and #2 are about trusting your own numbers.** #1 was actively producing a wrong artifact: `readme_index.md` badged `zonalStatsLocal` as your only ★ *verified* API while it failed every recent run (verified on the real 895-row log: pass→fail; net counts moved 63→64 pass, 156→155 fail). #2 stops `augment` from promoting a verified example that predates a signature change.

**#3 is the headline lever.** Your 29.4% pass rate was mostly measuring "can the LLM reinvent Beast I/O for ~150 unrelated functions," not "is each doc good enough." Pinning removes that burden for the raster/vector-consuming majority. Note the finding that motivated the pixel type: the *same* raster passed as both `geoTiff[Float]` (45×) and `geoTiff[Int]` (34×) — so `require_correctness` is not type-strict, which is itself a paper-worthy datapoint (compiled+ran ≠ correct). I pinned `Float` (NLDAS is 32-bit float); it is the one token to revisit.

**#4 and #5 are the generality story.** Pinning is hand-work per codebase, which cuts against "make the workflow general." The hardened `auto` reaches the same result *without* hand-pinning by using a codebase-agnostic signal — a reader is useful iff its output type feeds documented operations — so the Scala mixin beats the Java wrapper with no "Java" rule. RDPro itself is pinned, so #4/#5 don't change its numbers; they matter for the next repo and for the paper's claim.

**#6 targets Version A's one blind spot** (guessed tier), but it's parked because 13 guessed functions are a rounding error next to 154 execution failures with a shared root cause (#3). Turn it on later with `probe_on_missing: true`.

_Verification: the pure logic of #1, #2, #4, #5 and the probe helpers was unit-tested against the real log / synthetic collisions and passes. The LLM- and Spark-dependent paths (#3 at runtime, #4's live generation) need your machine — there is no Spark/LLM key in the sandbox._

---

## What to re-run (in order)

Run from `experiments/rdpro/` (point `--config` at your `configs/aideal.yaml`).

1. **Fix the false badge now — no execution needed:**
   `aideal organize --index --config configs/aideal.yaml`
   Re-derives `readme_index.md` with the #1 fix, so `zonalStatsLocal` stops showing ★ verified.

2. **The real re-measurement (this exercises the pinned preamble, #3):**
   `aideal comprehension --execute --config configs/aideal.yaml`
   Run it **~5 times** and report a pass *rate*, not one boolean — the audience model writes a fresh snippet each run. First sanity-check one function: `... comprehension --execute --api mapPixels --show-code`.

3. **Fold the new passing snippets back (staleness filter #2 now active):**
   `aideal augment --config configs/aideal.yaml`  (add `--only-missing` to preserve curated examples)

4. **Regenerate the index/grounding from the fresh data:**
   `aideal organize --index` and, if you use per-entry grounding lines, `aideal grounding --annotate`.

**Before step 2**, either add the missing `packages` (the jetty/calcite `NoClassDefFoundError` cluster, ~5 functions) to `aideal.yaml`, or exclude those functions from the denominator — they're a build-config gap, not a doc failure.

You do **not** need `aideal readme --generate` (the entry text didn't change), and the probe stays off unless you set `probe_on_missing: true` and regenerate.

---

## Files touched
- `grail-agent/src/aideal/probe.py` — new (Version B core + CLI)
- `grail-agent/src/aideal/default_prompts/aideal/probe_write.md` — new (signature-only probe prompt)
- `grail-agent/src/aideal/error_log.py` — `library_version`+`timestamp` fields, `git_version()`
- `grail-agent/src/aideal/readme_agent.py` — sticky-pass fix, `_fresh`/`_recency_key` staleness filter, probe hook (opt-in)
- `grail-agent/src/aideal/doc_checks.py` — `auto` preamble/io_hints hardening (`_base_type`, `_consumed_type_counts`, `_useful_readers`, `_drop_unconsumed_lines`)
- `experiments/rdpro/configs/aideal.yaml` — pinned preamble
