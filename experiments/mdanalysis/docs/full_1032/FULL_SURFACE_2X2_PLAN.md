# MDAnalysis 2.9.0 full-surface A1/A2/B1/B2 plan

## Frozen denominator

This experiment uses every visibility-correct public API **name** discovered at
the pinned MDAnalysis commit, not the historical 661-entry generated artifact:

- 1,032 unique public names;
- 1,397 public definition sites;
- source commit `81b8ef51e5bc1aa2824294ac6c52818c74975658`;
- ordered manifest `api_manifest.json`;
- comprehension manifest SHA-256
  `86524a56a316f95593a8db4acc94c7d7889e329076bb0982d9e769b70995cb54`.

The older 661 manifest remains historical evidence. It must not be supplied to
any full-surface command.

## Experimental cells

| Cell | Starting documentation | Treatment | Fresh final measurement |
|---|---|---|---|
| A1 | Original upstream documentation | None | `--doc original`, 1,032 APIs, zero code-fix rounds |
| A2 | Initial generated README | Generate one entry for every frozen API | `--doc aideal`, 1,032 APIs, zero code-fix rounds |
| B1 | A1 result plus original docs | Repair A1 failures with `--create-missing --doc original+aideal` | Original docs plus only execution-gated created entries, zero code-fix rounds |
| B2 | A2 result plus frozen A2 README | Repair A2 failures in a copy of the A2 README | Repaired generated README, zero code-fix rounds |

B1 is not a fabricated complete generated README. Its README starts absent.
`fix-docs --create-missing` targets the failed functions in the immutable A1
result, reads the real source and original documentation, and retains a new
entry only when its zero-code-repair retry passes. If all repair rounds fail,
the entry is removed again. Its final audience context is explicitly
`original+aideal`.

## Isolation and dependency graph

```text
aideal/mdanalysis-full1032-freeze
  │  upstream PASS_TO_PASS BEFORE
  │  1,032-entry A2 generation (crash-resumed and then frozen)
  ├── aideal/mdanalysis-full1032-A1 ── A1 ── aideal/mdanalysis-full1032-B1
  │                                          B1 repair → B1 zero → P2P AFTER
  ├── aideal/mdanalysis-full1032-A2 ── A2 ── aideal/mdanalysis-full1032-B2
  │                                          B2 repair → B2 zero → P2P AFTER
  └── aideal/mdanalysis-full1032-analysis   immutable result copies/comparison
```

Each cell has its own Git branch, physical worktree, nested source clone,
error log, generated document, checkpoint, execution output directory, final
JSON, and environment inventory. A1/A2 run concurrently; B1/B2 run
concurrently. The shared provider gate enforces at least three seconds between
Google requests across processes.

## Crash and restart behavior

- README generation writes a fingerprinted state file after each completed API.
- Comprehension writes one fingerprinted JSONL row after each API; provider
  failures are transient and are retried rather than accepted as final rows.
- Doc repair writes its report after every round and re-enters interrupted or
  provider-error APIs.
- Watchdog results are first written to `.tmp` and atomically promoted only
  when the completion predicate verifies the full denominator and no transient
  provider failures.
- `max_restarts: 0` intentionally means unlimited watchdog restarts. A job that
  exceeds its wall-time bound is terminated and resumed after five minutes.
- Re-running the same pipeline command resumes completed work. Changing source,
  model, YAML, profile, fixture, scaffold, engine, interpreter, document, or
  manifest changes the fingerprint and prevents checkpoint mixing.

## Upstream PASS_TO_PASS

Before A2 generation, the complete pinned upstream test suite runs with the
pinned source on `PYTHONPATH`; generation cannot start unless it exits cleanly.
After B1 and B2, the identical suite runs again. JUnit case identities and
statuses are compared with the committed baseline, and every previously
passing test must still pass. The nested MDAnalysis source must remain at the
same commit throughout; documentation treatment never edits it.

## Failure evidence and commits

After every final cell measurement, `analyze_failures.py` emits Markdown, CSV,
and JSON with every failed function, category, source definition, reached
codebase frames, captured error, generated code, tokens, attempts, and a
failure diagnosis. Provider and missing-optional-dependency outcomes remain
visible but are excluded from the semantic denominator.

The orchestrator commits and pushes only after a cell passes its completeness
predicate:

1. freeze branch: manifest, profile/config/fixture provenance, upstream-before,
   complete generated README and generation state;
2. A1 and A2 branches: final zero-round result plus failure analysis;
3. B1 and B2 branches: repair trail, final zero-round result, failure analysis,
   and PASS_TO_PASS-after evidence;
4. analysis branch: immutable copies of all four results and paired transitions.

## Queue command

Static preparation does not call Gemini:

```bash
cd /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mdanalysis_full1032_freeze
env PYTHONPATH=grail-agent/src:. \
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/mdanalysis/run_full_2x2_pipeline.py \
  --freeze-worktree "$PWD" \
  --source-seed /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_mdanalysis_setup/experiments/mdanalysis/mdanalysis \
  --prepare-only
```

Only after explicit approval, remove `--prepare-only` and run the same command
under `caffeinate -i`. It first supervises upstream-before and generation, then
executes every dependent branch. If the controlling shell dies, rerun the
identical command.

## Time and deadline risk

The historical 661-API A2 zero-round run took about 3.5 hours, suggesting
roughly 5.5 hours per 1,032-API zero-round arm under similar service latency.
A1/A2 and B1/B2 are paired in parallel, so the four final measurements have an
optimistic wall-clock floor near 11–14 hours, excluding generation, repairs,
upstream tests, throttling, and retries.

Generation adds 1,032 author calls. B1/B2 repair cost depends on the unknown
full-surface failure count and may require deep-dive, diagnosis, rewrite, and
retry calls for as many as five rounds per failed API. The historical repaired
MDAnalysis work required about 13.5 hours for roughly 200 targets; the raw full
surface contains more utility, abstract, format-specific, and optional-
dependency APIs and can be substantially slower. A realistic total is about
30–72 hours if the provider is stable; the configured worst case is longer.

Therefore unattended completion is engineered, but completion by Wednesday is
**not guaranteed** for the non-sampled 1,032-API requirement. A1/A2 are likely
to finish earlier; B1/B2 repair is the critical path. The protocol must not
silently shrink the denominator to meet the deadline.

## Blocking conditions

- Gemini quota/provider availability is external and can extend the schedule.
- The full upstream suite must pass in the pinned environment before any paid
  generation begins.
- Any edit to a fingerprinted input after starting requires a fresh state path
  or a deliberate new experiment; the watchdog refuses silent mixing.
- Optional MDAnalysis format dependencies may create infrastructure exclusions.
  They must be reported, not relabeled as documentation failures.
