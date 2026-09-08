# AIDEAL readiness assessment and improvement queue

Updated: 2026-09-08T01:23:36.617314+00:00

**Measured scope:** how documentation affects an LLM’s API use under a fixed harness. Overall agent readiness is not yet fully measured; no composite score is assigned.

| Repository | A1 | A2 | B1 | B2 | Matched comparison |
|---|---|---|---|---|---|
| mir_eval | 67/148 provisional | 135/148 final | pending (148 APIs) | pending (148 APIs) | WITHHELD/PARTIAL |
| thumbnailator | 86/149 provisional | 127/149 final | pending (149 APIs) | pending (149 APIs) | WITHHELD/PARTIAL |
| tslearn | 52/235 provisional | 96/235 provisional | pending (235 APIs) | pending (235 APIs) | WITHHELD/PARTIAL |

Provisional counts retain pending and provider-error APIs in the denominator. Final counts are native pass/all-API results. Cross-cell effects require the separate matched-comparison release checks.

| Readiness dimension | Current evidence |
|---|---|
| Discovery | Not measured: the target API is supplied. |
| Setup and inputs | Partial: frozen configuration and fixture identity; autonomous setup and API-specific suitability remain unverified. |
| API execution | Measured in complete cells; provisional elsewhere. |
| Workflow completion | Not measured: held-out multi-API tasks are needed. |
| Verification and recovery | Partial: assertions and retry histories; independent oracle checks and agent recovery tasks are needed. |

## Observed barriers

| Repository | Candidate barrier | Affected API/cell records |
|---|---|---:|
| mir_eval | api-identity-or-version | 4 |
| mir_eval | assertion-or-behavior | 17 |
| mir_eval | doc-wrong | 2 |
| mir_eval | example-invalid | 1 |
| mir_eval | input-contract-or-api-call | 19 |
| mir_eval | input-or-output-path | 6 |
| mir_eval | provider | 31 |
| mir_eval | test/scaffold | 5 |
| mir_eval | unknown | 9 |
| thumbnailator | input-or-output-path | 2 |
| thumbnailator | provider | 6 |
| thumbnailator | unknown | 35 |
| tslearn | api-identity-or-version | 19 |
| tslearn | assertion-or-behavior | 11 |
| tslearn | input-contract-or-api-call | 7 |
| tslearn | provider | 21 |
| tslearn | unknown | 27 |

## Reviewable improvements (222)

Review states: `{'open': 221, 'proposed': 1}`. Observation errors: 0. Inactive reviewed IDs retained: 0.

Each card separates native failure, diagnosis confidence, proposed action, validation and review decisions. Provider barriers concern execution infrastructure; they are not automatically codebase or documentation defects.

| Suggestion | Cell | Priority | Confidence | Review |
|---|---|---|---|---|
| [mir_eval: IntervalFormatter](suggestions/43eb9410c759c001a0ca.md) | A1 | execution_blocker | high | open |
| [mir_eval: absolute_error](suggestions/082799557f3d00ef3959.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_accuracy](suggestions/3e452364bc3ce7629a00.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_err_score](suggestions/15ea9b007008778fffe3.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_num_true_positives](suggestions/a94de7dba8b2518329b0.md) | A1 | execution_blocker | high | open |
| [mir_eval: constant_hop_timebase](suggestions/a94d44ba733dc35068c1.md) | A1 | execution_blocker | high | open |
| [mir_eval: deprecated](suggestions/beb42a32875dfb8074a9.md) | A1 | execution_blocker | high | open |
| [mir_eval: deviation](suggestions/485cfbe27e59e994869a.md) | A1 | execution_blocker | high | open |
| [mir_eval: generate_labels](suggestions/206b1afbab047351560f.md) | A1 | execution_blocker | high | open |
| [mir_eval: goto](suggestions/31d759747e60a47ee7f0.md) | A1 | execution_blocker | high | open |
| [mir_eval: hz_to_midi](suggestions/0fc9f77b57e5ec9906c5.md) | A1 | execution_blocker | high | open |
| [mir_eval: join](suggestions/d1241d280613693e892c.md) | A1 | execution_blocker | high | open |
| [mir_eval: karaoke_perceptual_metric](suggestions/9118ca03cd85bcb44076.md) | A1 | execution_blocker | high | open |
| [mir_eval: lmeasure](suggestions/8bbd52b230f0a2c7fecd.md) | A1 | execution_blocker | high | open |
| [mir_eval: merge_chord_intervals](suggestions/81c93234379912055f49.md) | A1 | execution_blocker | high | open |
| [mir_eval: midi_to_hz](suggestions/211e4c04d67f8fca45b9.md) | A1 | execution_blocker | high | open |
| [mir_eval: overseg](suggestions/6e74d2f73232d8dff637.md) | A1 | execution_blocker | high | open |
| [mir_eval: pairwise](suggestions/12909b3482309d45070c.md) | A1 | execution_blocker | high | open |
| [mir_eval: percentage_correct](suggestions/e9ac493292c3af9f7a53.md) | A1 | execution_blocker | high | open |
| [mir_eval: percentage_correct_segments](suggestions/9c570f531c4d4f940760.md) | A1 | execution_blocker | high | open |
| [mir_eval: piano_roll](suggestions/0a2ca18c14109cd4b39e.md) | A1 | execution_blocker | high | open |
| [mir_eval: rand_index](suggestions/43e353481c75a9c347f4.md) | A1 | execution_blocker | high | open |
| [mir_eval: reduce_extended_quality](suggestions/f4e1161a1968ed0e9d38.md) | A1 | execution_blocker | high | open |
| [mir_eval: register_colormap](suggestions/d6485c290c7bda782770.md) | A1 | execution_blocker | high | open |
| [mir_eval: seg](suggestions/8203ae2ebabf0a487d90.md) | A1 | execution_blocker | high | open |
| [mir_eval: split](suggestions/5a88eb99e29f3d5b416e.md) | A1 | execution_blocker | high | open |
| [mir_eval: underseg](suggestions/d815da7665f94bd15133.md) | A1 | execution_blocker | high | open |
| [mir_eval: validate_boundary](suggestions/641d57339a66dbb3993a.md) | A1 | execution_blocker | high | open |
| [mir_eval: validate_structure](suggestions/970d60a4c88d8d112a3e.md) | A1 | execution_blocker | high | open |
| [mir_eval: validate_voicing](suggestions/e0708b0abc31ac82b20f.md) | A1 | execution_blocker | high | open |
| [mir_eval: vmeasure](suggestions/24f231e5d234a7e41345.md) | A1 | execution_blocker | high | open |
| [thumbnailator: antialiasing](suggestions/9ebf739748447f9c6fd6.md) | A1 | execution_blocker | high | open |
| [thumbnailator: build](suggestions/3f447775fd599b0e1381.md) | A1 | execution_blocker | high | open |
| [thumbnailator: clear](suggestions/3f911dbe0befc683e80e.md) | A1 | execution_blocker | high | open |
| [thumbnailator: createOutputStream](suggestions/8c69e4aae53d75a4ecbd.md) | A1 | execution_blocker | high | open |
| [thumbnailator: format](suggestions/a4ae9b56216ff3fc31e1.md) | A1 | execution_blocker | high | open |
| [thumbnailator: getSize](suggestions/8ee1c82133dfcdb52307.md) | A1 | execution_blocker | high | open |
| [tslearn: PatchingLayer](suggestions/492a7a8c40fbef8c50dd.md) | A1 | execution_blocker | high | open |
| [tslearn: SquaredEuclidean](suggestions/9cb2806d53f90d5dc13a.md) | A1 | execution_blocker | high | open |
| [tslearn: TimeSeriesDBSCAN](suggestions/1268880b6e8ce0e28497.md) | A1 | execution_blocker | high | open |
| [tslearn: accumulated_matrix](suggestions/31932007a7b91d0395d7.md) | A1 | execution_blocker | high | open |
| [tslearn: accumulated_matrix_from_dist_matrix](suggestions/c873c572383ded07dabd.md) | A1 | execution_blocker | high | open |
| [tslearn: baseline_accuracy](suggestions/efc0eaaf68454e1f6b3d.md) | A1 | execution_blocker | high | open |
| [tslearn: belongs_to_backend](suggestions/f46ab268890b4c653478.md) | A1 | execution_blocker | high | open |
| [tslearn: call](suggestions/d9bb728a68e8297ee02c.md) | A1 | execution_blocker | high | open |
| [tslearn: cast](suggestions/965682daafd9a388c930.md) | A1 | execution_blocker | high | open |
| [tslearn: cdist_sax](suggestions/c25207efc332a03acceb.md) | A1 | execution_blocker | high | open |
| [tslearn: check_dataset](suggestions/a8e4c6f1f84f7f2405c8.md) | A1 | execution_blocker | high | open |
| [tslearn: check_keras_backend](suggestions/66e5440c2bd6bad1b798.md) | A1 | execution_blocker | high | open |
| [tslearn: check_variable_length_input](suggestions/83ebfbea39deaaf62e23.md) | A1 | execution_blocker | high | open |
| [tslearn: compute](suggestions/f362c4d35ee2416d1275.md) | A1 | execution_blocker | high | open |
| [tslearn: compute_mask](suggestions/0512d9254c63496e4707.md) | A1 | execution_blocker | high | open |
| [tslearn: compute_var](suggestions/87cd83f687ee55e86575.md) | A1 | execution_blocker | high | open |
| [tslearn: cydist_1d_sax](suggestions/00d5cb3b04ed3df7886c.md) | A1 | execution_blocker | high | open |
| [tslearn: cydist_sax](suggestions/dc883b22a8c2a53c612c.md) | A1 | execution_blocker | high | open |
| [tslearn: distance](suggestions/bc355c8ca83308070d8a.md) | A1 | execution_blocker | high | open |
| [tslearn: distance_paa](suggestions/e04db690a2878d710e3c.md) | A1 | execution_blocker | high | open |
| [tslearn: compute](suggestions/4a28af1f1c30cd779151.md) | A2 | execution_blocker | high | open |
| [mir_eval: deprecated](suggestions/8c1892028fee0fa4c019.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: first_n_three_layer_P](suggestions/1350063ad65ccf061962.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_key](suggestions/436854cbe884009d1ba7.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_patterns](suggestions/3ec965f5d5ef03de9a59.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_ragged_time_series](suggestions/26d31ac39c6a5b88d156.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_tempo](suggestions/d3d7c120d2f0cf5ef1c7.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_valued_intervals](suggestions/094a8d589f0601565cf5.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: load_wav](suggestions/eda6ce99cf1dfa09b8dd.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: p_score](suggestions/1be317ac447e9d35b68b.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: piano_roll](suggestions/b721a09f840e891eee3a.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: reduce_extended_quality](suggestions/84d3132e80a965f61bc2.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: ticker_pitch](suggestions/f0e1ab94a6656e53a513.md) | A2 | reviewed_barrier | reviewed | proposed |
| [mir_eval: voicing_recall](suggestions/049822fa462033a54c69.md) | A2 | reviewed_barrier | reviewed | open |
| [mir_eval: adjust_events](suggestions/b5d8d720382ae6f3937c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: bss_eval_images_framewise](suggestions/ee546cfee6a917867a24.md) | A1 | needs_diagnosis | low | open |
| [mir_eval: cemgil](suggestions/c6506c88fc534d7355a4.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: directional_hamming_distance](suggestions/2f801be73cdc571eaa87.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: encode](suggestions/c0b0ea84a8bbdb141a5c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: establishment_FPR](suggestions/fb3df82af9d781a1029f.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: filter_kwargs](suggestions/d21e6895b4ba7d321840.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: freq_to_voicing](suggestions/9d92f0294a7e43670cce.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: hierarchy](suggestions/e80a3571919b0a3060aa.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: index_labels](suggestions/6748fbb926345164f1d3.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: intervals_to_samples](suggestions/22787fa4aeff29aba5bc.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: labeled_intervals](suggestions/f19880ca9e62ee01d0f2.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_intervals](suggestions/e28c89662ce0bddd2858.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_key](suggestions/07935a2cc87763bd5029.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_labeled_events](suggestions/435fb3ecec357acd1560.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_patterns](suggestions/b0f6efc6ada8ec91bae2.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_tempo](suggestions/ee0ffa4decac662d0a75.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_valued_intervals](suggestions/5294f3212213f9d21189.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: load_wav](suggestions/38ea0baa3c61534b7a7e.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: match_note_offsets](suggestions/cab7744907893c737877.md) | A1 | needs_diagnosis | low | open |
| [mir_eval: match_note_onsets](suggestions/8c47855a97838c3c58c4.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: match_notes](suggestions/4bf8494d3551483021cb.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: merge_labeled_intervals](suggestions/43aa2b1071c2e3da200d.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: metrics](suggestions/941c61218671eccf5b9c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: midi_to_chroma](suggestions/0c1ac2019580dec1cc7a.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: mirex](suggestions/d1e8c581e99ac74b898a.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: mutual_information](suggestions/c31dbc02e1005fbaf427.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: nce](suggestions/a92aa7c41c283dded174.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: occurrence_FPR](suggestions/491f0c1de7473c2033c6.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: offset_precision_recall_f1](suggestions/7349ba90280378efdc50.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: onset_precision_recall_f1](suggestions/7100e1f4c564b26a4619.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: precision_recall_f1_overlap](suggestions/5b99bf662ca3113b5cc7.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: raw_chroma_accuracy](suggestions/304393ce33554ee7d978.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: raw_pitch_accuracy](suggestions/1ae98db80158b959aac2.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: rotate_bitmap_to_root](suggestions/4b04290420ac757e9c40.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: rotate_bitmaps_to_roots](suggestions/d036fb8b6d4739ea3ef9.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: segments](suggestions/9793c2361b05ee449388.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: split_key_string](suggestions/2666c133dc301e4d1ba4.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: standard_FPR](suggestions/fe10055b088c95ed3948.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: tetrads_inv](suggestions/d22f4169f098fc3a9d7c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: thirds](suggestions/6c1ad712345a7259ceb0.md) | A1 | needs_diagnosis | low | open |
| [mir_eval: ticker_notes](suggestions/189cb354c4b873209fcd.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: ticker_pitch](suggestions/fa6ec02b12da0c18e301.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: tmeasure](suggestions/676c59a8af6e8969699c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: to_cent_voicing](suggestions/60bb7e394ebacc6994b1.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: validate_chord_label](suggestions/7d86acd1d5814a7b82ba.md) | A1 | needs_diagnosis | low | open |
| [mir_eval: validate_frequencies](suggestions/9891f992fd74be0eda19.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: validate_hier_intervals](suggestions/40e5a297c10597e0956c.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: validate_tempi](suggestions/7f53a0233f322c209ab8.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: weighted_accuracy](suggestions/565d2c3c8c28402a7c31.md) | A1 | needs_diagnosis | medium | open |
| [thumbnailator: ConsecutivelyNumberedFilenames](suggestions/5016037ef7fc294905d0.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: FileThumbnailTask](suggestions/58bf3dac62f80d4532db.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: FixedSizeThumbnailMaker](suggestions/bd5578d463c01aa0aa71.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: ScaledThumbnailMaker](suggestions/34297d32edf8629951fa.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: SourceSinkThumbnailTask](suggestions/53b927039e5d23e21cdd.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: StreamThumbnailTask](suggestions/5e573cca4bdb06ef54fc.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: ThumbnailParameter](suggestions/ecf7381933b438eedfea.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: alphaInterpolation](suggestions/dac238e929493b14167d.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: asFiles](suggestions/5a7c1bfd405f2798481a.md) | A1 | needs_diagnosis | medium | open |
| [thumbnailator: defaultResizerFactory](suggestions/a572d945958ab12bce0a.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: determineOutputFormat](suggestions/8048ba5d90202c25e5c5.md) | A1 | needs_diagnosis | medium | open |
| [thumbnailator: getDestination](suggestions/bd7fb5599c84e7077452.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getExifOrientation](suggestions/21091435f0dc321f37a9.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getOutputFormat](suggestions/59cd4a9ffd1a5d440328.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getResizerFactory](suggestions/665cdf4f18dee8254496.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: Pipeline](suggestions/bef11a67152a2a4d29da.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: ThumbnailMaker](suggestions/c03bfc3c50c6bd4fe7f4.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: UnsupportedFormatException](suggestions/015a729896c83e876640.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: clear](suggestions/594bd164c69bacf81341.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: createOutputStream](suggestions/359469b6855c1fddff31.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: defaultResizer](suggestions/e31f85a5b6abefa51720.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: defaultResizerFactory](suggestions/96a1dbd629caaeb53f5c.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: filters](suggestions/601fab65b7dc4f724b7f.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: fitWithinDimenions](suggestions/6f1a2b85a8c5a38ada54.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getDestination](suggestions/b30f1f6cfcc03646c58e.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getExifOrientation](suggestions/1c57a93aa6c204cff94e.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getFormatName](suggestions/19a3e96cb0603ee3337c.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getInstance](suggestions/e39583482c0b2865c5f1.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getOrientationFromExif](suggestions/ca24486c54b665be5dad.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getOutputFormat](suggestions/034793073434ecfce739.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getRenderingHints](suggestions/b8257fe9accc05a62dbb.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: getSourceRegion](suggestions/adc087f3d3411a0addaa.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: init](suggestions/12b0562e2a1326672978.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: quality](suggestions/749e61125bd757b8c5d2.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: region](suggestions/bab805102a468e66fe83.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: resizerFactory](suggestions/d9b38c984d25135a41c9.md) | A2 | needs_diagnosis | low | open |
| [thumbnailator: setThumbnailParameter](suggestions/f075e31e736dd79ddc46.md) | A2 | needs_diagnosis | low | open |
| [tslearn: Backend](suggestions/fde0dbe3dea078c863e1.md) | A1 | needs_diagnosis | low | open |
| [tslearn: BaseModelPackage](suggestions/3031292af0c7a888c372.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: GlobalArgminPooling1D](suggestions/4adc96ee48fc77032de0.md) | A1 | needs_diagnosis | low | open |
| [tslearn: GlobalMinPooling1D](suggestions/de3bc03b2f39342c7227.md) | A1 | needs_diagnosis | low | open |
| [tslearn: KNeighborsTimeSeriesMixin](suggestions/cc09f29ef1dee034dd63.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: LearningShapelets](suggestions/7b528f6b5e6a582cf4c8.md) | A1 | needs_diagnosis | low | open |
| [tslearn: LocalSquaredDistanceLayer](suggestions/7e8242c0f6e88aaff9bd.md) | A1 | needs_diagnosis | low | open |
| [tslearn: NumPyBackend](suggestions/2459befdfa5e1206534c.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: NumPyLinalg](suggestions/52fed50fba2e2a006f63.md) | A1 | needs_diagnosis | low | open |
| [tslearn: NumPyTesting](suggestions/fc5541214312b981da73.md) | A1 | needs_diagnosis | low | open |
| [tslearn: PyTorchBackend](suggestions/dc08f3328d1d23caabcd.md) | A1 | needs_diagnosis | low | open |
| [tslearn: PyTorchRandom](suggestions/82b72baec83cba836ab5.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: PyTorchTesting](suggestions/a9f63bcd9c3190301bc6.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: SoftDTW](suggestions/3a7621a36075d20f3bc0.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesCentroidBasedClusteringMixin](suggestions/cdcab909fcc7ec733b37.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesMixin](suggestions/e2c8af8b5978d8d3da03.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesSVMMixin](suggestions/11d995fc2dd7fbee16b2.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: TsLearnTags](suggestions/681e82e5b808dbfb1775.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: build](suggestions/7e11c469f83c17237a28.md) | A1 | needs_diagnosis | low | open |
| [tslearn: cache_all](suggestions/23caf3a06117c042a923.md) | A1 | needs_diagnosis | low | open |
| [tslearn: cdist_normalized_cc](suggestions/49bd3af4a48a4fcf459a.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: check_dims](suggestions/6c93adff9b1148b3b1c4.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: compute_output_shape](suggestions/970a6d69666b6677a91c.md) | A1 | needs_diagnosis | low | open |
| [tslearn: copy](suggestions/65781e4d62bb097ff4df.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: ctw](suggestions/8a1016becc1e0c3e1411.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: cyslopes](suggestions/6d5242e702503acc5ea7.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: distance_1d_sax](suggestions/1897ad90895237cf1464.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: distance_sax](suggestions/9f65eb32431f1c29b145.md) | A1 | needs_diagnosis | low | open |
| [tslearn: dtw_barycenter_averaging_one_init](suggestions/a0d51bb81e801919bb03.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: dual_coef_](suggestions/a41b60921e77b0ccd729.md) | A1 | needs_diagnosis | low | open |
| [tslearn: early_classification_cost](suggestions/18f431a907cd00761972.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: BaseModelPackage](suggestions/f995a70ba75a6f818ba5.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: GlobalArgminPooling1D](suggestions/7fec39a7ce54e7122bf8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: GlobalMinPooling1D](suggestions/4019272c56a19f2872ad.md) | A2 | needs_diagnosis | low | open |
| [tslearn: KNeighborsTimeSeriesMixin](suggestions/66288f871906a29f15a8.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: LearningShapelets](suggestions/a03010ee7627aa0f49c8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: LocalSquaredDistanceLayer](suggestions/06a7cd0158af8a0604f8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: NumPyBackend](suggestions/3bc2e78380cd347e066f.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: NumPyRandom](suggestions/d50d93cf638187995e0f.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PatchingLayer](suggestions/d0957863ecb711faa6c8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: PyTorchBackend](suggestions/d2a2e06b853eef716bb1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PyTorchRandom](suggestions/900f8f4a475dc62bb350.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PyTorchTesting](suggestions/e75daed6c7429f1a1048.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: SoftDTW](suggestions/3eb071d1a1ee8cb916a7.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: SquaredEuclidean](suggestions/3f27f4b6cc2ff519a694.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesFeatureSynchronizer](suggestions/b5fe88244bab77b3db09.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesSVMMixin](suggestions/0f6325e1b4f2389d4abb.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TsLearnTags](suggestions/00dd44f6e4ef414dbbf4.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: accumulated_matrix](suggestions/f2643d45b8ffc2210fa6.md) | A2 | needs_diagnosis | low | open |
| [tslearn: build](suggestions/f73b986047aa6c515b80.md) | A2 | needs_diagnosis | low | open |
| [tslearn: call](suggestions/5de88051085748a6a12c.md) | A2 | needs_diagnosis | low | open |
| [tslearn: check_keras_backend](suggestions/0476ec0dd20cfcfc0f3a.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: compute_output_shape](suggestions/e11427e7509aeb1fabff.md) | A2 | needs_diagnosis | low | open |
| [tslearn: cydist_1d_sax](suggestions/2e76ea80776db663eb78.md) | A2 | needs_diagnosis | low | open |
| [tslearn: decision_function](suggestions/90f1882d52407388781f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: dtw_barycenter_averaging_one_init](suggestions/c58de824dd094aad07bc.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: early_predict_proba](suggestions/1d9195b5c2bf45a1c7da.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: extract_from_zip_url](suggestions/556446f978a96da3cd17.md) | A2 | needs_diagnosis | low | open |
| [tslearn: fix_force_all_finite_warning](suggestions/19d92b0287f41c177588.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: from_cesium_dataset](suggestions/983fb54c898d2b3bb990.md) | A2 | needs_diagnosis | low | open |
| [tslearn: from_hdf5](suggestions/db7a06f2638d29b9e384.md) | A2 | needs_diagnosis | low | open |
| [tslearn: from_pickle](suggestions/0f71db7bc37749a20233.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_backend](suggestions/1f1c9231449a82dd76e1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_cluster_probas](suggestions/dbbbd6d4fe034fb71a4c.md) | A2 | needs_diagnosis | medium | open |

## Human and agent workflow

`open → proposed → human-approved plan → human/agent implementation → submitted validation → human acceptance or revision`

Defer or reject any suggestion. A changed evidence version makes older decisions stale. Actor labels are operator-supplied audit records, not an authentication system. Approval records authorize no automatic subprocess or LLM execution in this tool.

- [Review command and decision formats](WORKFLOW.md)
- [Machine-readable assessment](assessment.json) · [Improvement queue](improvement_queue.json)
- [Architecture and human involvement](../AIDEAL_DESIGN_LOGIC.md)
- [Data, formats, samples, and API tests](../FINAL_REPORT_DATA_AND_API_METHODS.md)
- [Detailed 2×2 evidence](../../DETAILED_PRIORITY_REPORT.md)

Errors: none observed
