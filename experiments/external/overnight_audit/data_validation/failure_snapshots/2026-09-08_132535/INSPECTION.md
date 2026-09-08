# Saved failure inspection — 8 September 2026, 13:25 PDT

328 native non-pass repository/cell/API records saved across mir_eval, Thumbnailator and tslearn. This is a timestamped observation, not 328 distinct functions or a final unresolved recovery count. A1 and tslearn A2 are still partial. A2 failures remain recorded even when a separate recovery succeeds.

[Full failure list (CSV)](FAILED_FUNCTIONS.csv) · [Machine-readable index](FAILED_FUNCTIONS.json) · [Capture metadata](summary.json)

| Repository | Cell | Native status | Non-pass | Categories |
|---|---|---|---:|---|
| mir_eval | A1 | Partial | 78 | {'llm-error': 26, 'runtime': 49, 'unknown': 1, 'infra': 2} |
| mir_eval | A2 | Complete | 13 | {'runtime': 13} |
| mir_eval | B2 | Complete | 11 | {'runtime': 11} |
| thumbnailator | A1 | Partial | 20 | {'runtime': 9, 'compile': 8, 'llm-error': 3} |
| thumbnailator | A2 | Complete | 22 | {'compile': 14, 'runtime': 8} |
| thumbnailator | B2 | Complete | 10 | {'runtime': 3, 'compile': 7} |
| tslearn | A1 | Partial | 114 | {'infra': 51, 'runtime': 29, 'llm-error': 34} |
| tslearn | A2 | Partial | 60 | {'runtime': 31, 'infra': 27, 'llm-error': 2} |

## Provider failures

All 65 current provider-failure rows record `504 DEADLINE_EXCEEDED`. They contain no generated execution code and no exit code. These are failed generation requests, not evidence that the named library functions failed at runtime. Provider usage fields at zero do not mean no request was sent. The underlying service cause and SDK retry count remain unverified.

Priority blockers: tslearn A2 `compute`, `jacobian_product`; Thumbnailator A1 `clear`, `createOutputStream`, `region`. Their recorded walls are approximately 600 seconds. See per-row evidence and the copied PROVIDER_504_DIAGNOSIS.md; the latter is an earlier contextual observation, not the current failure index.

Source inspection: `compute` represents multiple class methods (SoftDTW.compute and SquaredEuclidean.compute), with different object preparation and output contracts. `SquaredEuclidean.jacobian_product(E)` requires E shaped (m,n) for X (m,d), Y (n,d), and returns (m,d). These requirements may matter for future generated code, but cannot explain a provider 504 that occurred before execution.

## Inspection of all 21 native B2 failures

These are static diagnoses from recorded errors, snippets and source. No new code was executed, no prompts were changed, and no findings were supplied to measured audience workers. No claim is made that README changes caused these failures. Suggested corrections require a separately recorded validation.

| Repository | API and saved evidence | Finding |
|---|---|---|
| mir_eval | [cemgil](mir_eval/B2/api_7a86f8010e0a6028/evidence.json) | Fixture/preprocessing mismatch: ref_events=[0,0.5,1,1.5]; default trim_beats drops events before 5 seconds. Both arrays become empty, so the perfect-score assertion is invalid. |
| mir_eval | [hierarchy](mir_eval/B2/api_c954b1a77ec09113/evidence.json) | Oracle mismatch: snippet counts ax.patches; source renders intervals using broken_barh. A zero patch count alone does not mean no intervals were rendered. |
| mir_eval | [load_key](mir_eval/B2/api_230d135ac5fc0d17/evidence.json) | Test setup fails opening output_dir/test_key.txt for writing; the target API is never reached. Missing output directory at that attempt. |
| mir_eval | [load_patterns](mir_eval/B2/api_1e3e621021b0f4af/evidence.json) | Snippet guesses a sibling pattern/reference.txt fixture that does not exist at the recorded location; fixture path assumption fails. |
| mir_eval | [load_ragged_time_series](mir_eval/B2/api_7d14f6a8cd3b33b1/evidence.json) | Likely library defect: header=True sets enumerate start to 1 but does not consume the first input line. The documented header is parsed as float and fails. Source inspected; no new reproduction run. |
| mir_eval | [load_tempo](mir_eval/B2/api_08838312b1b57088/evidence.json) | Test setup fails creating output_dir/test_tempo.txt before the API is reached; missing output directory at that attempt. |
| mir_eval | [load_wav](mir_eval/B2/api_1d864a7f1e69c627/evidence.json) | Test setup fails writing output_dir/test_load.wav before load_wav is reached; missing output directory at that attempt. |
| mir_eval | [piano_roll](mir_eval/B2/api_98a467ad87f941d8/evidence.json) | Oracle mismatch: snippet expects one ax.patches entry per interval; plotting code uses broken_barh. Inspect the returned collections instead in a separately reviewed test. |
| mir_eval | [precision_recall_f1_overlap](mir_eval/B2/api_5cdc828a3cb84967/evidence.json) | Input contract: generic interval and pitch fixtures have different lengths. Validator rejects them; pair aligned arrays for a reviewed diagnostic. |
| mir_eval | [ticker_pitch](mir_eval/B2/api_3547dfad8ca4e63b/evidence.json) | Oracle mismatch: source installs a MIDI-to-Hz formatter. MIDI 69 returns 440, whereas the snippet incorrectly expects a note-name label containing A. |
| mir_eval | [tmeasure](mir_eval/B2/api_e5a21dfb99c8c9d8/evidence.json) | Unjustified oracle: snippet equates matching hierarchy levels with precision=1, recall=0.5. Recorded precision is 0; mathematical oracle still requires deeper validation. |
| thumbnailator | [FileImageSink](thumbnailator/B2/api_c372af91113e5d6f/evidence.json) | Output binding misuse: snippet appends test_sink.png under a path already ending thumbnail.png; file path treated as directory. |
| thumbnailator | [FileThumbnailTask](thumbnailator/B2/api_4bca98d52358470a/evidence.json) | Output binding misuse: snippet appends task_out.png under the thumbnail.png output file path. |
| thumbnailator | [allowOverwrite](thumbnailator/B2/api_bad43a77d385ba23/evidence.json) | Output binding misuse: snippet appends test_overwrite.png under the thumbnail.png output file path; setup fails before overwrite behavior is established. |
| thumbnailator | [clear](thumbnailator/B2/api_0cd2ab3859aa33ee/evidence.json) | Surface/accessibility issue: Configurations.clear is package-private and intended only for tests. External harness cannot call it directly. Review manifest inclusion. |
| thumbnailator | [createOutputStream](thumbnailator/B2/api_c104478a17487842/evidence.json) | Surface/accessibility issue: FileImageSink.createOutputStream(File) is package-private. External harness cannot call it directly. Review manifest inclusion. |
| thumbnailator | [fitWithinDimenions](thumbnailator/B2/api_f28c3109155133da/evidence.json) | Constructor overload ambiguity: untyped null matches both Resizer and ResizerFactory overloads. Requires explicit intended type. |
| thumbnailator | [formatType](thumbnailator/B2/api_ac58fb0d7dfc3adc/evidence.json) | Wrong method name in generated oracle: getFormatType does not exist on ThumbnailParameter; source exposes getOutputFormatType. |
| thumbnailator | [getDestination](thumbnailator/B2/api_aba2dab196002ea1/evidence.json) | Harness scope collision: generated Object[] args redeclares main(String[] args). Compilation fails before API behavior can be tested. |
| thumbnailator | [getSourceRegion](thumbnailator/B2/api_b1488294b1423c93/evidence.json) | Incorrect Region constructor (Dimension instead of Position, Size) plus ambiguous ThumbnailParameter overloads from untyped null. |
| thumbnailator | [init](thumbnailator/B2/api_3ca8c15d0e2eabb9/evidence.json) | Surface/accessibility issue: Configurations.init is package-private and intended only for tests. Review manifest inclusion; do not silently remove it from this frozen denominator. |

## Evidence limitations and saved recovery rounds

All 328 rows retain native category, error, attempts field, elapsed time, source location and fingerprint when present. Complete checkpoint events for these API names are preserved separately; they include multiple fingerprint groups and must be filtered before counting comparable retries. `attempts=1` in a native row is not a lifetime retry count and not an SDK attempt count.

57 retained scripts contain the recorded snippet/prefix; this is partial code binding, not proof that the entire harness was unchanged historically. 206 scripts lack recorded code needed to establish binding and are explicitly marked unbound legacy. No stale script was attached to any of the 65 provider failures. Source windows include hashes of the source file as observed. A named API row can cover multiple source sites; only its primary source window is captured.

S_A2 and S_B2 summaries and available detailed case/round records were copied into recovery_observations. They are sequential file observations rather than one atomic transaction. At capture, Thumbnailator S_A2 retained provider-blocked createOutputStream and setThumbnailParameter, and stuck getRenderingHints/getSourceRegion. These states may advance independently after capture. Native scores remain separate.

The remaining A1/A2 execution and infrastructure failures are saved and category-indexed, not all individually source-diagnosed in this review. Infrastructure labels include both absent optional dependencies (for example keras/tensorflow) and invalid import names; do not treat every import failure as a missing installation.

## Review queue

1. Validate the mir_eval header-handling defect with an isolated minimal reproduction before proposing a library patch.
2. Review Thumbnailator non-public API inclusion for a future manifest version; preserve the current denominator.
3. Review per-API data shapes, output-file versus output-directory bindings, and library-specific assertion oracles.
4. Keep provider retries separate from snippet fixes and document repair rounds; preserve exact request failures for later diagnosis.

This capture introduced no model calls, reruns, scheduler changes or worker signals. MDAnalysis, Sedona and RDPro were outside this snapshot scope.
