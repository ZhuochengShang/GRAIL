# AIDEAL independent-branch study report

Protocol: [main plan](README.md). Record the snapshot timestamp, revisions,
manifest/config/document/fixture fingerprints, completed and missing stages,
and whether each result is new, compatibly reused, historical or diagnostic.
This amendment was agreed after some outcomes were known; it is not a preregistration.

## 1. Documentation style and input comparison — required for every repository

Compare **four distinct artifacts**: root original README; configured original
documentation bundle available to A1; generated A2 README; final repaired README
used for fresh B2. Record exact paths and hashes. Configured availability is not
proof that every file or byte was delivered in every API request: retain the
selected fragments, retrieval/truncation policy and delivered hashes separately.

| Dimension | Original README alone | A1 original bundle | A2 generated README | Repaired README / fresh B2 |
|---|---|---|---|---|
| Role and structure | Gateway / tutorial / task examples / reference; evidence headings | Added local docs, reference, hosted snapshot | Per-API structure and observed fields | Retained structure and exact changed entries |
| Size and provenance | Bytes, lines, pinned revision, SHA256 | Config paths, expanded file count, text hash | Bytes, API-entry count, SHA256 | Bytes, API-entry count, SHA256 |
| Coverage | Frozen bare-name references / full manifest | Same detector and denominator | Parsed entries / manifest; missing and extra names | Same, plus changed / unchanged entries |
| Examples | Representative exact snippet and source location | Where examples are supplied | Correctness review state and snippet evidence | Which examples changed and why |
| Setup and dependencies | Installation, imports, versions, optional packages | Additional setup guidance | Environment assumptions or additions | Corrections and remaining limits |
| Data and fixtures | Shape, dtype, units, format, sample and placeholder paths | Additional contracts | Sample construction and fixture references | Changed constraints and validated fixture use |
| Call contracts | Receiver, call order, return type, side effects, errors | Reference-level additions | Supported facts versus inferred claims | Error/source evidence supporting each correction |
| Reader benefit and barrier | Observable useful features and omissions | What the wider bundle supplies | Added detail and any incorrect/invented advice | Corrected barriers and remaining gaps |

Never equate root README reference coverage with A1's full bundle coverage.
Bare-name matches do not certify qualified-symbol ownership or complete contracts.
Label subjective interpretations as such. A long or structured README is not
necessarily correct. Missing artifacts remain “not available”, not zero quality.
For RDPro, retain historical and v5 scope separately; for MDAnalysis, distinguish
an evolving generated file from a completed baseline; Sedona remains unassessed
until its pinned input, validated manifest and fixtures are registered.

Published local comparison: audit `data_validation/documentation_style_v1/index.html`.
Builder: `../study_dashboard/documentation_style.py`; curated observations:
`../study_dashboard/documentation_styles.json`. This is a reporting-only snapshot,
not a model call or measured-input change. Refresh after final documents stabilize.

## 2. Stage outcomes

| Stage | Inputs / scope | Budget | Required result fields |
|---|---|---|---|
| A1 | Original documentation; independent control | Zero snippet fixes | Pass, execution fail, provider unresolved, unrecorded; full and observed denominators |
| A2 | Generated README; full manifest | Zero snippet fixes | Same, plus frozen failure names and input identities |
| B2-1 | Frozen A2 failures; README + previous snippet + errors | Up to 5 **new** snippet fixes; A2 is round 0; stuck=2; no new source/tests diagnosis | Recovered, unresolved, blocked, unprocessed; per-round code/error/timing; README unchanged |
| B2-2 | Independently the same A2 failures; source/tests + errors | Up to 5 README repair rounds; zero-snippet-fix validation each round | Targets, processed, retained edits, rejected edits; full round/validation history |
| Fresh B2 | Full manifest; final B2-2 README | Fresh snippets; zero snippet fixes | Same baseline fields; fresh test is separate from repair-time validation |

B2-2 does not inherit B2-1 fixes or its remaining failures. Original-doc repair
is omitted. Old S_A2/S_B2 source recovery and old B1 are supplementary/historical;
do not relabel them as the current B2-1 arm. Disclose legacy restart budget limits.

## 3. Paired comparisons and why outcomes differ

For root-README-referenced, full-original-bundle-referenced, remaining and full
manifest cohorts, show A1/A2 pass numerator and denominator. Separate provider
unresolved and unrecorded APIs. For APIs with both usable outcomes, list both-pass,
A1-only-pass, A2-only-pass and both-fail. Use one fixed cohort for paired differences.

For A2 versus fresh B2, list every recovery and regression, unchanged versus
changed delivered documentation, receiver/data setup, target-call evidence,
assertion state and error category. Keep gross gains, regressions and net change
separate. Do not claim that README style caused an outcome without a matched
style-only experiment; content accuracy, retrieval, API coverage, environment,
harness defects and stochastic generation remain alternative explanations.

| API | Stage / round | Exact doc + code evidence | Failure mechanism | Confidence | Developer improvement | Review status |
|---|---|---|---|---|---|---|
| ... | ... | Paths, hashes, delivered excerpt, error, target reached? | Doc contradiction / model invention / input contract / receiver / surface / dependency / provider / harness | Observed / inferred / unknown | Reviewable code/doc/fixture change | Human accepted / agent reviewed / pending |

## 4. Data, execution validity and timing

Include package versions and actual import identities; fixture paths, hashes,
formats, sample construction and values, shapes/dtypes/units, generated outputs
and cleanup ownership. YAML declarations do not alone prove runtime usage.
Distinguish code generated, compiled, process started, target reached, native
accepted and independently verified. Keep native outcomes and isolated replay
outcomes in separate tables with their own denominators and evidence bindings.
Replay alone cannot certify the document-repair pipeline.

For every API, retain request timestamps, local execution time, total wall time,
provider attempts and measured retry intervals, snippet-fix rounds, document rounds,
stop reasons and missing telemetry. Provider retry is not a code/doc fix round.
Follow the detailed timing/data requirements in the historical master template
where compatible with this protocol. Finish with evidence-backed readiness
barriers and a reviewable improvement queue, not a single unqualified score.
