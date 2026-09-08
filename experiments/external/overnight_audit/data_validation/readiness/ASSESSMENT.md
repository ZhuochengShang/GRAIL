# AIDEAL readiness assessment and improvement queue

Updated: 2026-09-08T17:38:03.251156+00:00

**Measured scope:** how documentation affects an LLM’s API use under a fixed harness. Overall agent readiness is not yet fully measured; no composite score is assigned.

| Repository | A1 | A2 | B1 | B2 | Matched comparison |
|---|---|---|---|---|---|
| mir_eval | 1/148 provisional | 135/148 final | pending (148 APIs) | 137/148 final | WITHHELD/PARTIAL |
| thumbnailator | 2/149 provisional | 127/149 final | pending (149 APIs) | 139/149 final | WITHHELD/PARTIAL |
| tslearn | 2/235 provisional | 0/235 provisional | pending (235 APIs) | pending (235 APIs) | WITHHELD/PARTIAL |

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
| mir_eval | assertion-or-behavior | 6 |
| mir_eval | doc-wrong | 2 |
| mir_eval | example-invalid | 1 |
| mir_eval | input-contract-or-api-call | 3 |
| mir_eval | input-or-output-path | 4 |
| mir_eval | provider | 26 |
| mir_eval | test/scaffold | 5 |
| mir_eval | unknown | 5 |
| thumbnailator | input-or-output-path | 2 |
| thumbnailator | provider | 3 |
| thumbnailator | unknown | 31 |
| tslearn | api-identity-or-version | 3 |
| tslearn | assertion-or-behavior | 1 |
| tslearn | input-contract-or-api-call | 3 |
| tslearn | provider | 37 |
| tslearn | unknown | 4 |

## Reviewable improvements (136)

Review states: `{'open': 135, 'proposed': 1}`. Observation errors: 0. Inactive reviewed IDs retained: 0.

Each card separates native failure, diagnosis confidence, proposed action, validation and review decisions. Provider barriers concern execution infrastructure; they are not automatically codebase or documentation defects.

| Suggestion | Cell | Priority | Confidence | Review |
|---|---|---|---|---|
| [mir_eval: IntervalFormatter](suggestions/43eb9410c759c001a0ca.md) | A1 | execution_blocker | high | open |
| [mir_eval: absolute_error](suggestions/082799557f3d00ef3959.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_accuracy](suggestions/3e452364bc3ce7629a00.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_err_score](suggestions/15ea9b007008778fffe3.md) | A1 | execution_blocker | high | open |
| [mir_eval: compute_num_true_positives](suggestions/a94de7dba8b2518329b0.md) | A1 | execution_blocker | high | open |
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
| [mir_eval: percentage_correct](suggestions/e9ac493292c3af9f7a53.md) | A1 | execution_blocker | high | open |
| [mir_eval: percentage_correct_segments](suggestions/9c570f531c4d4f940760.md) | A1 | execution_blocker | high | open |
| [mir_eval: piano_roll](suggestions/0a2ca18c14109cd4b39e.md) | A1 | execution_blocker | high | open |
| [mir_eval: rand_index](suggestions/43e353481c75a9c347f4.md) | A1 | execution_blocker | high | open |
| [mir_eval: reduce_extended_quality](suggestions/f4e1161a1968ed0e9d38.md) | A1 | execution_blocker | high | open |
| [mir_eval: seg](suggestions/8203ae2ebabf0a487d90.md) | A1 | execution_blocker | high | open |
| [mir_eval: underseg](suggestions/d815da7665f94bd15133.md) | A1 | execution_blocker | high | open |
| [mir_eval: validate_boundary](suggestions/641d57339a66dbb3993a.md) | A1 | execution_blocker | high | open |
| [mir_eval: validate_structure](suggestions/970d60a4c88d8d112a3e.md) | A1 | execution_blocker | high | open |
| [mir_eval: vmeasure](suggestions/24f231e5d234a7e41345.md) | A1 | execution_blocker | high | open |
| [thumbnailator: clear](suggestions/3f911dbe0befc683e80e.md) | A1 | execution_blocker | high | open |
| [thumbnailator: createOutputStream](suggestions/8c69e4aae53d75a4ecbd.md) | A1 | execution_blocker | high | open |
| [thumbnailator: region](suggestions/760de2afb8c91ba44d2a.md) | A1 | execution_blocker | high | open |
| [tslearn: PatchingLayer](suggestions/492a7a8c40fbef8c50dd.md) | A1 | execution_blocker | high | open |
| [tslearn: TimeSeriesDBSCAN](suggestions/1268880b6e8ce0e28497.md) | A1 | execution_blocker | high | open |
| [tslearn: accumulated_matrix](suggestions/31932007a7b91d0395d7.md) | A1 | execution_blocker | high | open |
| [tslearn: accumulated_matrix_from_dist_matrix](suggestions/c873c572383ded07dabd.md) | A1 | execution_blocker | high | open |
| [tslearn: belongs_to_backend](suggestions/f46ab268890b4c653478.md) | A1 | execution_blocker | high | open |
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
| [tslearn: early_predict](suggestions/3c11412b7b124c2586be.md) | A1 | execution_blocker | high | open |
| [tslearn: frechet](suggestions/f34bfa3d928fc87d7712.md) | A1 | execution_blocker | high | open |
| [tslearn: from_numpy](suggestions/a9a5f5305a9c56f56d78.md) | A1 | execution_blocker | high | open |
| [tslearn: gamma_soft_dtw](suggestions/438ddac357b01927a578.md) | A1 | execution_blocker | high | open |
| [tslearn: get_early_predict_generator](suggestions/da327bb49da71d852107.md) | A1 | execution_blocker | high | open |
| [tslearn: get_early_predict_proba_generator](suggestions/3ae2ab1db15f8c5ceb1e.md) | A1 | execution_blocker | high | open |
| [tslearn: is_float](suggestions/0b0c74d7bbfc877ac3f6.md) | A1 | execution_blocker | high | open |
| [tslearn: is_float32](suggestions/e4a6a53c15dc8f409272.md) | A1 | execution_blocker | high | open |
| [tslearn: is_numpy](suggestions/585c5d6b183ad80a9a85.md) | A1 | execution_blocker | high | open |
| [tslearn: iscomplex](suggestions/25813de0f12d953e9275.md) | A1 | execution_blocker | high | open |
| [tslearn: jacobian_product](suggestions/efe13aead9dc33ab2b15.md) | A1 | execution_blocker | high | open |
| [tslearn: mase](suggestions/d6318ccb7f4952366621.md) | A1 | execution_blocker | high | open |
| [tslearn: mse](suggestions/3af68a89e69ff9f8ddde.md) | A1 | execution_blocker | high | open |
| [tslearn: njit_sakoe_chiba_mask](suggestions/fd70f1ac5129406e5761.md) | A1 | execution_blocker | high | open |
| [tslearn: normal](suggestions/8d62931fe716c65b2b83.md) | A1 | execution_blocker | high | open |
| [tslearn: partial_fit](suggestions/f0c4cd50ddf3925e7c6a.md) | A1 | execution_blocker | high | open |
| [tslearn: predict_proba_and_earliness](suggestions/2caa8ac2f3722ae16c2d.md) | A1 | execution_blocker | high | open |
| [tslearn: save_dict](suggestions/64042927743239068f2f.md) | A1 | execution_blocker | high | open |
| [tslearn: to_numpy](suggestions/2e3b666651dfa822d085.md) | A1 | execution_blocker | high | open |
| [tslearn: compute](suggestions/4a28af1f1c30cd779151.md) | A2 | execution_blocker | high | open |
| [tslearn: jacobian_product](suggestions/5eb42a36285bbdb40258.md) | A2 | execution_blocker | high | open |
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
| [mir_eval: constant_hop_timebase](suggestions/a94d44ba733dc35068c1.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: register_colormap](suggestions/d6485c290c7bda782770.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: cemgil](suggestions/b787266701666609d246.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: hierarchy](suggestions/2e97254929aecf73fb7a.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: load_key](suggestions/7d214c8b6b776db5054d.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: load_patterns](suggestions/0bef35621236805f4653.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: load_ragged_time_series](suggestions/dd141d53bf9018f5362f.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: load_tempo](suggestions/f6e3c129c6ec1eeead44.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: load_wav](suggestions/e7bc2b0c26e0d12f7f86.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: piano_roll](suggestions/856dfee1985f79dc4578.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: precision_recall_f1_overlap](suggestions/efa556125d5bfd4e4716.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: ticker_pitch](suggestions/42f7138e489af3f99f74.md) | B2 | needs_diagnosis | medium | open |
| [mir_eval: tmeasure](suggestions/50128731544757af10c4.md) | B2 | needs_diagnosis | medium | open |
| [thumbnailator: build](suggestions/3f447775fd599b0e1381.md) | A1 | needs_diagnosis | low | open |
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
| [thumbnailator: FileImageSink](suggestions/0bd87e137c0cf9a6e7e4.md) | B2 | needs_diagnosis | medium | open |
| [thumbnailator: FileThumbnailTask](suggestions/83018f021ff2f746463b.md) | B2 | needs_diagnosis | medium | open |
| [thumbnailator: allowOverwrite](suggestions/c4f3f3e67f12aea64cba.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: clear](suggestions/42794e8e3fe41f3c3f10.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: createOutputStream](suggestions/4bcb266ace31f0dfa9c9.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: fitWithinDimenions](suggestions/c4f1ca499c257611a829.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: formatType](suggestions/f8b6085edb4ee04c53d6.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: getDestination](suggestions/dde3d181030b49b81092.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: getSourceRegion](suggestions/ec70ff6061fe3ebc1206.md) | B2 | needs_diagnosis | low | open |
| [thumbnailator: init](suggestions/1d5565af4db2fe2faaf2.md) | B2 | needs_diagnosis | low | open |
| [tslearn: SquaredEuclidean](suggestions/9cb2806d53f90d5dc13a.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: baseline_accuracy](suggestions/efc0eaaf68454e1f6b3d.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: call](suggestions/d9bb728a68e8297ee02c.md) | A1 | needs_diagnosis | low | open |
| [tslearn: cast](suggestions/965682daafd9a388c930.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: fix_force_all_finite_warning](suggestions/31a797e1c04a6d32d433.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: get_backend](suggestions/5b561e6f3abaf83879f5.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: is_array](suggestions/e1024e725bbecccd33ed.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: njit_lcss_accumulated_matrix](suggestions/82cd652dd43be2a632db.md) | A1 | needs_diagnosis | low | open |
| [tslearn: set_weights](suggestions/c6e70a9295e0b43a89cb.md) | A1 | needs_diagnosis | low | open |
| [tslearn: shapelets_](suggestions/f3bf662dc22f29f79acf.md) | A1 | needs_diagnosis | low | open |
| [tslearn: predict_class_and_earliness](suggestions/d2ff189e60095b0de249.md) | A2 | needs_diagnosis | medium | open |

## Human and agent workflow

`open → proposed → human-approved plan → human/agent implementation → submitted validation → human acceptance or revision`

Defer or reject any suggestion. A changed evidence version makes older decisions stale. Actor labels are operator-supplied audit records, not an authentication system. Approval records authorize no automatic subprocess or LLM execution in this tool.

- [Review command and decision formats](WORKFLOW.md)
- [Machine-readable assessment](assessment.json) · [Improvement queue](improvement_queue.json)
- [Architecture and human involvement](../AIDEAL_DESIGN_LOGIC.md)
- [Data, formats, samples, and API tests](../FINAL_REPORT_DATA_AND_API_METHODS.md)
- [Detailed 2×2 evidence](../../DETAILED_PRIORITY_REPORT.md)

Errors: none observed
