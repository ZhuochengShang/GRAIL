# Final report: data, configuration, and API-test methods

Evidence reviewed September 7, 2026, America/Los_Angeles. This is the data and
methods appendix of the Wednesday report, not a declaration that the study
is complete. The deadline covers mir_eval, Thumbnailator, and tslearn.

In the delivered report package, this appendix resides under `data_validation/`:

- [Measured results and release decisions](../FINAL_REPORT_WITH_DATA_CHECKS.md)
- [Central readiness assessment and improvement queue](readiness/ASSESSMENT.md)
- [Detailed results, failures, attempts, and repair rounds](../DETAILED_PRIORITY_REPORT.md)
- [Live input validation](DATA_VALIDATION.md)
- [Automation health, forecasts, configuration bundles, and review queue](automation/AUTOMATION_STATUS.md)
- [Complete design logic: LLMs, prompts, skills, and human decisions](AIDEAL_DESIGN_LOGIC.md)

Those links are relative to the delivered package, not this source-template
directory. The existing data observer copies this whole directory into
`deadline_snapshot/data_validation` at its first iteration at or after
September 9, 10:45 AM. Existing experiment jobs are unchanged.

## 1. Data supplied to the priority experiments

Paths below are relative to the individual experiment root in each condition's
worktree. A1/A2/B1/B2 inherit the same data construction; work and output paths
are condition-specific. Availability is not proof that every test uses a file.

| Repository / pinned source | Binding and checked-in path | Format and full fixture size | Actual supplied sample / intended API family |
|---|---|---|---|
| mir_eval / `fe73b3533737814f83dbd9739f06e90f5f82f758` | `beat_reference_file`: `source/tests/data/beat/ref00.txt`; `beat_estimate_file`: `source/tests/data/beat/est00.txt` | Plain text; 528 and 522 single-column event-time rows | File paths for event readers; times are in seconds. This is annotation data, not raw audio. |
| mir_eval / same revision | `chord_reference_file`: `source/tests/data/chord/ref00.lab` | 136 three-column rows: interval start, end, chord label | Interval/label readers; interval times in seconds. |
| mir_eval / same revision | `melody_reference_file`: `source/tests/data/melody/ref00.txt` | 3,632 two-column rows: time and frequency | Time/frequency readers; seconds and Hz. |
| Thumbnailator 0.4.21 / `c9d99613878bbbf1f4d9369585b4cb5352c3b474` | `grid_png`: `source/src/test/resources/Thumbnailator/grid.png`; `grid_jpeg`: same directory, `grid.jpg` | PNG: 100×100 pixels, RGBA; JPEG: 100×100 pixels, RGB | Image reading, resizing, conversion, and output checks where the generated call selects these paths. |
| Thumbnailator / same revision | `exif_jpeg`: `source/src/test/resources/Exif/original.jpg` | JPEG: 160×160 pixels, RGB, EXIF fixture | Metadata/orientation-related tests where selected. File identity and image decoding do not prove a particular EXIF field was exercised. |
| tslearn / `f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7` | `trace_npz`: `tslearn/tslearn/.cached_datasets/Trace.npz` | NumPy NPZ: `X_train`, `X_test` each `(100,275,1)` float64; `y_train`, `y_test` each `(100,)` int64 | Training input actually uses 8 selected series and their first 40 steps: `(8,40,1)`. Second input uses first 4 test series and first 32 steps: `(4,32,1)`. Time steps are array indices; no physical time unit is established here. |

The tslearn NPZ SHA-256 is
`0de0b7fa727cfabaf8481552db2b95fcccd12e54b67058aea79ff05b483cf807`.
Every supplied file's absolute path, Git blob, SHA-256, size, and decoded
metadata are recorded separately for each active cell in `data_evidence.json`.

## 2. Constructed inputs and exact sampling

| Repository | Preamble inputs | Relevant constraints and limits |
|---|---|---|
| mir_eval | Five frame times; four reference and estimated events; four `(start,end)` intervals per set; labels `C:maj`, `G:maj`, `A:min`, `F:maj`; five reference/estimated frequencies; synthetic source matrices with shape `(2,5)` | Values cover several API families, but some functions require different dtypes, shapes, longer signals, or other file formats. These common inputs are not a universal valid input contract. |
| Thumbnailator | 32×24 RGB image: blue background and yellow rectangle at `(8,6)` of size 16×12; 16×12 RGB destination image; byte output stream; `output_dir/thumbnail.png` | Intended checks include dimensions, pixels, bytes, or files. The preamble creates the output directory. Individual APIs may need other object types or valid ranges. |
| tslearn | Training indices `[0,4,1,17,3,13,2,5]`; first 40 steps; labels verified as `[1,1,2,2,3,3,4,4]`; `s1` and `s2` are flattened 40-element series; `tiny_matrix = arange(12.0).reshape(3,4)` | Balanced four-class sample, two examples per class. Small deterministic data support bounded API tests; this is not full-dataset model evaluation. |

Actual tslearn construction from `configs/aideal_full235_base.yaml`:

```python
_trace = np.load(trace_npz)
_balanced = np.array([0, 4, 1, 17, 3, 13, 2, 5], dtype=int)
X = _trace["X_train"][_balanced, :40, :]
X2 = _trace["X_test"][:4, :32, :]
y = _trace["y_train"][_balanced]
s1, s2 = X[0].ravel(), X[1].ravel()
```

The full235 manifest counts unique public names, with 343 definition sites
retained as provenance. It does not mean every overload, parameter combination,
dependency, or dataset row has been exercised.

## 3. How data reach an API test

1. The framework resolves inherited YAML and converts `sample_data` paths to
   bindings in the selected scaffold.
2. The configured preamble constructs arrays/images/objects before the generated
   snippet runs. Output paths are kept separate from immutable input fixtures.
3. The audience-generated snippet chooses an API call and arguments, using
   supplied bindings, constructed inputs, or its own literals/objects. Review
   must distinguish those choices; a declared binding alone proves no use.
4. The configured interpreter or Java compiler/runtime executes the harness.
   The current pass gate checks exit status, success/error markers, and the
   `__CHECK__` witness when `require_correctness` is true. Assertions can fail
   execution, but the gate does not independently validate their meaning.
5. Per-API scripts, hashes, results, and attempt histories remain the evidence.
   File provenance and textual call detection alone cannot prove runtime
   dataflow, correct ownership, valid arguments, or a meaningful oracle.

### Observed positive example: mir_eval A2 `load_events`

The saved generated script calls `mir_eval.io.load_events(beat_reference_file)`.
It asserts an ndarray, one dimension, nonzero length, nondecreasing timestamps,
and nonnegative first timestamp, then prints the length and first value in a
`__CHECK__` witness. This connects an appropriate event annotation fixture to
the reader and checks structural properties. It does not independently compare
every parsed value with the file's contents.

### Observed failures: mir_eval A2

- `load_key` constructs `test_key.txt` containing `C:maj`. The pinned API expects
  two string columns, such as `C major`. The generated input is unsuitable even
  though the repository's configured fixtures have correct hashes.
- Five tests initially failed while writing beneath an absent supplied output
  directory. Separate diagnostics with a precreated output directory let
  `first_n_three_layer_P`, `load_tempo`, and `load_valued_intervals` pass;
  `load_key` then exposed the format error and `load_wav` a wrong expected sample
  value. Native outcomes remain unchanged.
- `load_patterns` references an absent `pattern/reference.txt`. A plausible
  repository-looking path is not a validated fixture.

Diagnostic successes are not substituted into measured A1/A2/B1/B2 scores or
counted as document-repair successes. See the result report's hash-bound failure
reviews and diagnostic evidence for exact attempts and results.

## 4. Configuration and dependency evidence

The experiment is not specified by one YAML alone. The reproducible unit
includes resolved YAML, frozen API manifest, source revision, scaffold,
documentation treatment, runtime environment, and per-condition launch settings.

| Repository | Active configuration layers | Runtime / recorded dependency evidence |
|---|---|---|
| mir_eval | Framework defaults → Python adapter → `configs/aideal.yaml` → `configs/aideal_A1.yaml` (or corresponding cell) | Worktree `source/.venv/bin/python`; NumPy 1.26.4, SciPy 1.15.3, Matplotlib 3.10.9 verified by imports on September 7. Full inventory: `docs/eval/setup/environment_A1.txt`. |
| Thumbnailator | Framework defaults → Java adapter → `configs/aideal.yaml` → condition YAML | Explicit Java 8 compiler/runtime; `target/thumbnailator-0.4.21.jar`; Maven 3.9.4 in setup evidence. Inventory: `docs/eval/setup/environment_A1.txt`. |
| tslearn | Framework defaults → Python adapter → historical `configs/aideal.yaml` → `configs/aideal_full235_base.yaml` → `configs/aideal_A1_full235.yaml` (or corresponding cell) | Explicit conda Python and worktree `PYTHONPATH`; NumPy 1.26.4, SciPy 1.15.3, scikit-learn 1.7.2, Numba 0.66.0 verified by imports on September 7. Full inventory: `docs/eval/setup/environment_A1.txt`. |

For tslearn, the full235 layer overrides the historical base settings with
`surface_filter: all`, the Trace fixture, the full235 scaffold, and
`require_correctness: true`. The historical base YAML alone is not the effective
experiment. Both Python import probes resolved the target library from the
respective A1 source worktree. This probe is not a historical attestation of
every worker or every optional dependency.

Installed-package inventories describe availability, not package usage by each
API. Optional-dependency and wrong-import failures require separate attribution.
The existing nested-watchdog environment-fingerprint limitation remains in the
result report; do not claim that a parent fingerprint certifies every child.

## 5. Per-API evidence and review status

For each repository and cell, preserve:

- `<repository>/<cell>/data_evidence.json`: resolved input paths, pinned blobs,
  hashes, decoded formats/shapes, configuration and result consistency checks.
- `<repository>/<cell>/api_test_data.csv`: every manifest API, generated script
  path/hash, status, fixture/preloaded references, visible target-call/assertion/
  witness text, and explicit semantic-review limitations.
- Result ledgers and hash-bound reviews: actual failure, attempt/fix round,
  diagnosis, and any diagnostic-only change.

For an independently reviewed API, record its canonical owner/signature,
actual arguments, expected dtype/shape/units/range or file schema, observed
result, assertion rationale, and a decision: verified, mismatch, needs review,
or not applicable. Unreviewed passing tests remain semantically unverified.

At the September 7 review, the six available A1/A2 worktrees passed the existing
input-identity audit with limitations. B1/B2 checks are populated as their
worktrees appear. Current status belongs to `DATA_VALIDATION.md`; this dated
statement must not be read as certifying unfinished cells.

## 6. Deferred repositories

| Repository | Prepared or historical data | Status and boundary |
|---|---|---|
| MDAnalysis 2.9.0 | `adk.psf` topology with `adk_dims.dcd` binary trajectory; `adk_open.pdb`; `adk_oplsaa.gro` with `adk_oplsaa.xtc`; upstream `MDAnalysisTests/data` directory | Prepared full1032 configuration constructs a Universe, atom groups, trajectory, and first timestep. It is outside the priority data observer's three-repository audit. Do not describe all 1,032 API/data pairings as verified. |
| RDPro | Retained historical spatial-fixture experiments | Reuse only. This appendix does not newly certify the historical cells' fixture equivalence or a matched four-cell design. |
| Apache Sedona | Existing placeholder configuration lacks a validated full-public-API fixture setup | Preparation and data selection are deferred; no completed API experiment or validated dataset is claimed. |

## Recovery and stopping-policy addendum

See [the staged recovery extension](recovery/README.md) and its [consistency review](recovery/CONSISTENCY_REVIEW_2026-09-07.md). No live recovery run has started. The two-round stagnation default is a configurable cost-control heuristic, not a demonstrated optimum. Document, code, provider and deep-dive rounds remain separate in the [comparison template](RESULT_COMPARISON_REPORT_TEMPLATE.md).

## Accepted study limits and RDPro parity

The user confirmed the stagnation threshold remains **2** consistently. See the [current RDPro alignment note](recovery_study_locked/RDPRO_PROTOCOL_ALIGNMENT_2026-09-07.md) and [locked recovery protocol](recovery_study_locked/README.md). This supersedes the earlier addendum's suggestion of alternative thresholds for this study. The corrected RDPro/priority/queued MDAnalysis static parity check passed; retained older RDPro engine differences remain recorded. Twenty tests passed. No new recovery worker was launched.
