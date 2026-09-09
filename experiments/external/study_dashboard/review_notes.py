"""Manually inspected evidence notes; no model-generated diagnosis is treated as proof."""
NOTES = {
    'mir_eval': {
        'cemgil': ('Input preprocessing conflict',
            'B2 trims the supplied 0–1.5 second events using trim_beats (default minimum 5 seconds), leaving empty arrays. cemgil returns zero for empty input, so the perfect-score assertion fails. The unchanged README overstates trimming as mandatory. S_B2 shifts events past the cutoff and records a native pass.',
            'Document the empty-input result and distinguish benchmark preprocessing from the function’s actual preconditions.'),
        'hierarchy': ('Incorrect test oracle',
            'B2 assumes eight ax.patches. Source display.py delegates to labeled_intervals, which uses ax.broken_barh; counting patches does not establish whether the plot was drawn. S_B2 checks documented legend labels and passes. The saved LLM diagnosis speculates about empty inputs, but the retained snippet contains nonempty inputs, so that explanation is unsupported.',
            'Specify observable output contracts; inspect delegated drawing code before inferring that zero patches means no plot.'),
        'precision_recall_f1_overlap': ('Mismatched input contracts',
            'B2 supplies four note intervals and five frame frequencies, including zero frequency. The API rejects unequal lengths. S_B2 aligns lengths and uses positive pitches, then passes. These are generic harness fixtures from different tasks, not a valid matched note dataset.',
            'Provide a note fixture with one strictly positive pitch per interval; do not silently equate frame-level melody data with note-level transcription data.'),
        'tmeasure': ('Unsupported numerical expectation',
            'B2 invents precision 1 and recall 0.5 from the number of hierarchy levels. The recorded result is precision zero. S_B2 switches to identical nontrivial hierarchies and passes an identity check. This changes the test case; it does not validate the original level-count formula.',
            'Document a worked numerical example and distinguish hierarchical ranking metrics from counting matched levels.')},
    'Thumbnailator': {
        'FileImageSink': ('Output-path misuse / shared-state confound',
            'The A2 and B2 retained snippets are identical: outputPath.resolve("test_sink.png"). The configured outputPath already ends in thumbnail.png. A2 recorded a pass, but isolated A2 replay fails with assertions both off and on. B2 fails on the same path construction. Historical shared filesystem state is implicated; the exact directory-creating test is not established.',
            'Use separate outputFile and outputDirectory bindings and a fresh directory per API. Preserve the native pass alongside the isolated replay failure.'),
        'FileThumbnailTask': ('Output-path misuse / shared-state confound',
            'B2 appends task_out.png below outputPath, which is a file path. A2 used the same path pattern and passed natively, but its isolated replay fails. S_B2 uses outputPath directly and records a pass. This is not evidence that a README edit damaged the API.',
            'Enforce file-versus-directory contracts and report filesystem isolation as a measured condition.'),
        'allowOverwrite': ('Failure before the target call',
            'Files.write fails while creating test data below thumbnail.png, before allowOverwrite is invoked. The A2 isolated replay also exposes this path misuse. S_B2 writes directly to outputPath and records a pass.',
            'Record target-call reachability separately from test-process failure; give file paths explicit names.'),
        'formatType': ('Invented companion method',
            'A2 correctly calls param.getOutputFormatType(). B2 instead calls nonexistent getFormatType() and fails compilation. The setter’s README entry is unchanged. Pinned ThumbnailParameter.java exposes getOutputFormatType at line 891; S_B2 makes that correction and passes.',
            'Show a setter/build/getter example using verified names, and distinguish target misuse from a wrong assertion helper.')},
    'tslearn': {
        'TimeSeriesMixin': ('Unsupported test oracle',
            'B2 asserts allow_nan is True. The pinned _DEFAULT_TAGS does not declare allow_nan, and the README makes no such promise. S_B2 tests declared X_types and attribute restoration and passes. This is a newly invented expectation, not a changed document entry.',
            'Publish exact capability tags and inheritance examples; assertions should target specified behavior.'),
        'shapelets_as_time_series_': ('Dependency-blocked fresh test; weak A2 evidence',
            'B2 imports LearningShapelets and fails because keras is missing. The unchanged README contains an ImportError skip example. A2 retains a native pass but only a resumed status, without a bound original snippet/output here; it cannot prove that the property was reached. A skipped A2 branch is plausible but not established.',
            'Classify missing-dependency skips separately; require a fitted-model/property-access witness before claiming this API executed.'),
        'shapelets_': ('Native pass is a skip, not property execution',
            'B2 stdout explicitly says skipped due to missing optional dependency: No module named keras. The snippet catches the import failure and prints the acceptance marker; it never fits the estimator or accesses shapelets_.',
            'Preserve the native score and add a reviewed not-exercised label; require target reachability for capability claims.'),
        'get_config': ('Native pass is a skip, not method execution',
            'B2 stdout says get_config skipped due to missing keras. The import-exception branch prints the acceptance marker without constructing the layer or calling get_config.',
            'Separate skipped setup from a successful method call; never use an acceptance marker alone as the oracle.'),
        'from_cesium_dataset': ('Missing-dependency contract only',
            'B2 invokes the converter and confirms the ImportError message. Its stdout is missing_dependency. This checks dependency-error behavior, not successful data conversion.',
            'Keep separate negative-contract and successful-conversion outcomes, with a real Cesium object for the latter.'),
        'to_cesium_dataset': ('Missing-dependency contract only',
            'B2 invokes the converter and catches ImportError; stdout reports cesium not installed. The conversion branch was not exercised.',
            'Report the exception-contract pass separately from normal-output capability.')}
}


def evidence_key(row):
    import hashlib
    import json
    evidence = {c: row['native'][c]['metric'] for c in ('A2', 'B2')}
    evidence.update(before=row['readme_before'], after=row['readme_after'])
    return hashlib.sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()
