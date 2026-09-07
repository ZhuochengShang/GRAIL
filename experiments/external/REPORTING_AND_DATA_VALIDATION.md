# Reporting results and verifying experiment data

The Wednesday report is populated from measured artifacts, not estimates.
The deadline covers mir_eval, Thumbnailator and tslearn; MDAnalysis, Sedona
and RDPro reruns are deferred. All twelve priority cells retain their full
manifests and zero-code-fix final measurements.

## Which artifacts supply the numbers

| Report field | Source |
|---|---|
| Pass/fail and native infrastructure exclusions | Condition's atomically promoted `comprehension.json` |
| Pending/transient progress | Fingerprinted `comprehension_progress.jsonl`; explicitly provisional |
| Public API denominator | Frozen ordered `docs/eval/api_manifest.json`, checked against the current scanner |
| Original/generated/repaired treatment | `doc_source`, delivered-document hash and condition configuration |
| Attempts and provider errors | Per-API checkpoint history plus watchdog start/finish logs |
| Fix/deep-dive/stuck history | `docfix.json` API records and their `doc_rounds`, including reverted attempts |
| Source/config/environment | Result fingerprint, per-cell inventories, pinned source commit and file hashes |
| Data identity and script evidence | `data_validation/<repository>/<cell>/data_evidence.json` and `api_test_data.csv` |
| Native failure category | Original result metric; retained even when reviewed classification differs |
| Reviewed failure cause | Hash-bound review annotation, source/document evidence and isolated diagnostic logs |

`RESULT_COMPARISON_REPORT_TEMPLATE.md` defines the human-readable report. The
running `audit_overnight.py` observer refreshes result tables and ledgers every
minute and commits changed evidence in the separate audit worktree every
15 minutes. It withholds cross-cell effects until all four compatible final
measurements, repair completion, and required test evidence are present.

The report directory is:

```
/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_overnight_evidence_audit/experiments/external/overnight_audit
```

Start with `FINAL_REPORT_WITH_DATA_CHECKS.md`, `DETAILED_PRIORITY_REPORT.md`, the per-repository
`DETAILED_REPORT.md` files and `data_validation/DATA_VALIDATION.md`.
The result observer freezes a deadline package at or after 10:45 AM Wednesday,
September 9, before the 11:00 AM deadline. The data observer independently
copies its evidence into `deadline_snapshot/data_validation`. Both continue
updating live reports afterward. A missing or incompatible result remains
missing or invalid; the deadline cannot make it valid.

## How the correct data are verified

The data observer makes no provider calls and never executes a generated
snippet. It is read-only with respect to every experiment worktree.

1. Check the exact pinned upstream revision, tracked source changes, frozen
   manifest bytes, full discovered API names, effective condition config,
   project profile and scaffold.
2. Resolve the actual configured data bindings. For each input file, verify
   that its Git blob equals the blob at the pinned source commit, and record
   its absolute path, SHA-256 and size. Merely having the right filename is
   insufficient.
3. Decode image metadata and array shapes/dtypes, or record text-file layout.
   Preserve the construction-code hash for deterministic in-memory inputs.
4. Check a completed result's manifest, source and scaffold fingerprints
   against those inputs. Keep generated output directories separate from
   input data.
5. Record the generated script/hash for every manifest API. Inspect only its
   generated code region for fixture/preloaded-value references, target-call
   text, assertions and correctness-witness text. Do not count a binding
   declared elsewhere in the scaffold as evidence that the snippet uses it.
6. Review API-specific semantics: correct owner/overload, supported inputs,
   dimensions/dtypes/units, meaningful expected values and nontrivial checks.
   Static references alone cannot establish runtime dataflow or a correct
   assertion, so unverified semantics stay explicitly unverified.

An API that processes numbers, strings or in-memory images need not read a
dataset file. Conversely, a fixture with a valid hash may still be unsuitable
for a particular API. The report separates those two questions.

## Verified initial input inventory, September 7

All six existing A1/A2 condition worktrees passed manifest/config/source and
supplied-fixture identity checks. B1/B2 are checked when their worktrees appear.

- mir_eval: four pinned fixtures per cell: beat reference/estimate, chord
  annotations and melody annotations. The observed text layouts were 528 and
  522 single-column beat rows, 136 three-column chord rows, and 3,632
  two-column melody rows.
- Thumbnailator: three pinned images per cell: a 100×100 RGBA PNG, a 100×100
  RGB JPEG and a 160×160 RGB EXIF JPEG; image decoding/verification succeeded.
  Its preamble also constructs deterministic in-memory images.
- tslearn: the checked-in Trace NPZ has `X_train` and `X_test` of shape
  `(100, 275, 1)`, float64, and two int64 label arrays of length 100. The
  preamble used by each generated test is retained and hashed separately.

## Known limitations that must remain in the final report

- Some supplied output directories were absent, causing failures before the
  target API call. These are visible separately from input-fixture identity.
- Some generated assertions or inputs are wrong even when the fixture is
  correct. Isolated diagnostics must not replace native measured outcomes.
- The original Python classifier can confuse a wrong public import/member
  with a missing third-party dependency. Preserve native and reviewed labels.
- Nested watchdogs inherited an outer environment fingerprint. Per-cell
  inventories are separately retained and compared; do not claim the recorded
  fingerprint alone certifies each child environment.
- The old runner's aggregate fixture hash can include an existing output
  directory. The independent audit records input-only hashes and flags this
  difference rather than treating generated outputs as input data.
- Provider-internal retries are not available in the current client logs.
  Report them as unknown. A configured limit is not a measured count.
- Passing upstream tests supports the pinned environment and baseline code;
  it does not certify every generated API test's assertion or input suitability.

## Read-only audit command

```bash
env PYTHONPATH=grail-agent/src:. \
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python \
  experiments/external/audit_experiment_data.py \
  --workspace-parent /Users/clockorangezoe/Documents/phd_projects/code/geoAI \
  --out /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_overnight_evidence_audit/experiments/external/overnight_audit/data_validation \
  --watch
```

The observer owns only `data_validation` and its deadline copy, uses its own
process lock, and makes no changes to active checkpoints, source, fixtures,
documents, configurations, API tests or Gemini rate state.
