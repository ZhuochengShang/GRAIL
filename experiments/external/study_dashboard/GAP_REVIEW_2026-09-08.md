# A2 to fresh B2: what the improvement hides

Evidence inspected September 8, 2026. Native outcomes remain unchanged.

| Repository | A2 native passes | Fresh B2 native passes | Fail → pass | Pass → fail | Net | Gross recovery / A2 failures |
|---|---:|---:|---:|---:|---:|---:|
| mir_eval | 135/148 | 137/148 | 6 | 4 | +2 (+1.35 percentage points) | 6/13 = 46.2% |
| Thumbnailator | 127/149 | 139/149 | 16 | 4 | +12 (+8.05 points) | 16/22 = 72.7% |
| tslearn | 175/235 | 217/235 | 44 | 2 | +42 (+17.87 points) | 44/60 = 73.3% |

The final difference is gross recoveries minus new failures. A high A2 score
also leaves little room for an absolute percentage-point improvement. These are
descriptive results from one saved comparison, not repeated-trial causal effects.

All ten regressing APIs have unchanged generated README entries and no targeted
document-repair record. This does not establish identical full prompts or runtime
state. Their observed barriers are:

* mir_eval: `cemgil` trims short fixture events to empty; `hierarchy` checks a
  rendering implementation detail instead of the documented output;
  `precision_recall_f1_overlap` combines four intervals with five frame pitches;
  `tmeasure` asserts a made-up level-count formula.
* Thumbnailator: `FileImageSink`, `FileThumbnailTask`, and `allowOverwrite` treat
  the configured output file path as a directory. Existing isolated A2 replays
  also fail, despite native A2 passes. `formatType` uses nonexistent
  `getFormatType()` instead of `getOutputFormatType()`.
* tslearn: `TimeSeriesMixin` invents an `allow_nan=True` contract;
  `shapelets_as_time_series_` is blocked by missing Keras. Its original A2
  snippet is not bound in this snapshot, so an actual successful property access
  cannot be inferred from the resumed native pass.

The detailed pages expose every gained and lost API, A2/B2 errors, the exact
before/after README entries, saved repair diagnoses, retained rounds, and fresh
test evidence. `review_notes.py` contains inspected findings for all regressions
and four limited-scope gains. `review_bindings.json` binds those notes to the
reviewed native metrics and README text; changed evidence is marked stale.

## Gains also require a scope check

The saved tslearn B2 stdout proves that `shapelets_` and `get_config` passed the
native marker check through a missing-Keras skip branch. The target property or
method did not execute. `from_cesium_dataset` and `to_cesium_dataset` call the
target but test the missing-dependency exception, not a successful conversion.
These four native gains must not be described as restored normal API capability.
This targeted review does not certify the remaining forty gains.

Other retained examples show useful repair directions: `NumPyBackend` fixes its
import to the defining submodule; `cdist_sax` uses integer SAX symbols and checks
a distance matrix; `deprecated` corrects a warning-category expectation;
`ThumbnailMaker` needs concrete receiver construction rather than instantiating
an abstract type. Saved model diagnoses remain hypotheses until checked against
code, input values, and execution evidence.

The saved `hierarchy` source diagnosis illustrates this limit: it speculates
about empty input, although the retained snippet supplies nonempty arrays.
The source delegates plotting to `labeled_intervals`/`broken_barh`; S_B2 passes
after checking documented legend labels. A confident diagnosis is not proof.

## Implications for the next reviewed protocol

Use separate outcomes for target not reached, normal-output check, expected
exception check, and independent semantic validation. Give each API a fresh
output directory with explicit file/directory bindings. Pair fixture shapes and
domains to API contracts. Use a reviewed oracle and record target-call witnesses.
Separate document improvement from repeated-reader variability through matched
repeated seeds or unchanged-document control reruns. These are proposed changes;
the active measured jobs and historical scores have not been modified.

Thumbnailator's existing isolated A2/B2 assertions-on replay is 114/149 versus
126/149, compared with native 127/149 versus 139/149. Both differences happen to
equal twelve; the underlying API outcomes differ. Replay is a separate endpoint
and does not certify the repair-time decisions or whole documentation pipeline.
