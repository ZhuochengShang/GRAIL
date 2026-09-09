# AIDEAL readiness assessment and improvement queue

Updated: 2026-09-09T02:13:55.796122+00:00

**Measured scope:** how documentation affects an LLM’s API use under a fixed harness. Overall agent readiness is not yet fully measured; no composite score is assigned.

| Repository | A1 | A2 | B1 | B2 | Matched comparison |
|---|---|---|---|---|---|
| mir_eval | 3/148 provisional | 135/148 final | pending (148 APIs) | 137/148 final | WITHHELD/PARTIAL |
| thumbnailator | 130/149 final | 127/149 final | pending (149 APIs) | 139/149 final | WITHHELD/PARTIAL |
| tslearn | 7/235 provisional | 175/235 final | pending (235 APIs) | 217/235 final | WITHHELD/PARTIAL |

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
| mir_eval | api-identity-or-version | 1 |
| mir_eval | assertion-or-behavior | 7 |
| mir_eval | doc-wrong | 2 |
| mir_eval | example-invalid | 1 |
| mir_eval | input-contract-or-api-call | 7 |
| mir_eval | input-or-output-path | 4 |
| mir_eval | provider | 17 |
| mir_eval | test/scaffold | 5 |
| mir_eval | unknown | 6 |
| thumbnailator | input-or-output-path | 4 |
| thumbnailator | unknown | 47 |
| tslearn | api-identity-or-version | 22 |
| tslearn | assertion-or-behavior | 22 |
| tslearn | input-contract-or-api-call | 12 |
| tslearn | provider | 21 |
| tslearn | unknown | 41 |

## Reviewable improvements (219)

Review states: `{'open': 218, 'proposed': 1}`. Observation errors: 0. Inactive reviewed IDs retained: 0.

Each card separates native failure, diagnosis confidence, proposed action, validation and review decisions. Provider barriers concern execution infrastructure; they are not automatically codebase or documentation defects.

| Suggestion | Cell | Priority | Confidence | Review |
|---|---|---|---|---|
| [mir_eval: absolute_error](suggestions/082799557f3d00ef3959.md) | A1 | execution_blocker | high | open |
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
| [tslearn: normal](suggestions/8d62931fe716c65b2b83.md) | A1 | execution_blocker | high | open |
| [tslearn: partial_fit](suggestions/f0c4cd50ddf3925e7c6a.md) | A1 | execution_blocker | high | open |
| [tslearn: predict_proba_and_earliness](suggestions/2caa8ac2f3722ae16c2d.md) | A1 | execution_blocker | high | open |
| [tslearn: save_dict](suggestions/64042927743239068f2f.md) | A1 | execution_blocker | high | open |
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
| [mir_eval: IntervalFormatter](suggestions/43eb9410c759c001a0ca.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: compute_accuracy](suggestions/3e452364bc3ce7629a00.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: compute_err_score](suggestions/15ea9b007008778fffe3.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: compute_num_true_positives](suggestions/a94de7dba8b2518329b0.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: constant_hop_timebase](suggestions/a94d44ba733dc35068c1.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: deprecated](suggestions/beb42a32875dfb8074a9.md) | A1 | needs_diagnosis | medium | open |
| [mir_eval: deviation](suggestions/485cfbe27e59e994869a.md) | A1 | needs_diagnosis | low | open |
| [mir_eval: hz_to_midi](suggestions/0fc9f77b57e5ec9906c5.md) | A1 | needs_diagnosis | medium | open |
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
| [thumbnailator: ConsecutivelyNumberedFilenames](suggestions/5016037ef7fc294905d0.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: FileThumbnailTask](suggestions/58bf3dac62f80d4532db.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: FixedSizeThumbnailMaker](suggestions/bd5578d463c01aa0aa71.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: ThumbnailMaker](suggestions/96208bacc216a9d49c24.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: ThumbnailParameter](suggestions/ecf7381933b438eedfea.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: alphaInterpolation](suggestions/dac238e929493b14167d.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: asFiles](suggestions/5a7c1bfd405f2798481a.md) | A1 | needs_diagnosis | medium | open |
| [thumbnailator: build](suggestions/3f447775fd599b0e1381.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: clear](suggestions/3f911dbe0befc683e80e.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: defaultResizer](suggestions/01249be854056fa380ea.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: determineOutputFormat](suggestions/8048ba5d90202c25e5c5.md) | A1 | needs_diagnosis | medium | open |
| [thumbnailator: getDestination](suggestions/bd7fb5599c84e7077452.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getExifOrientation](suggestions/21091435f0dc321f37a9.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getParam](suggestions/7a961ff4cb09e9b60bbe.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: getSourceRegion](suggestions/02d5d206d8aafbc672ff.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: keepAspectRatio](suggestions/cf4fae30d2fbbc61ab70.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: make](suggestions/afd3fa4d36040d0f8661.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: region](suggestions/760de2afb8c91ba44d2a.md) | A1 | needs_diagnosis | low | open |
| [thumbnailator: write](suggestions/889cbec3814af3365502.md) | A1 | needs_diagnosis | low | open |
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
| [tslearn: PatchingLayer](suggestions/492a7a8c40fbef8c50dd.md) | A1 | needs_diagnosis | low | open |
| [tslearn: SquaredEuclidean](suggestions/9cb2806d53f90d5dc13a.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesDBSCAN](suggestions/1268880b6e8ce0e28497.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: accumulated_matrix](suggestions/31932007a7b91d0395d7.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: accumulated_matrix_from_dist_matrix](suggestions/c873c572383ded07dabd.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: baseline_accuracy](suggestions/efc0eaaf68454e1f6b3d.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: call](suggestions/d9bb728a68e8297ee02c.md) | A1 | needs_diagnosis | low | open |
| [tslearn: cast](suggestions/965682daafd9a388c930.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: cdist_sax](suggestions/c25207efc332a03acceb.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: check_keras_backend](suggestions/66e5440c2bd6bad1b798.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: compute_mask](suggestions/0512d9254c63496e4707.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: compute_var](suggestions/87cd83f687ee55e86575.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: fix_force_all_finite_warning](suggestions/31a797e1c04a6d32d433.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: get_backend](suggestions/5b561e6f3abaf83879f5.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: is_array](suggestions/e1024e725bbecccd33ed.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: njit_lcss_accumulated_matrix](suggestions/82cd652dd43be2a632db.md) | A1 | needs_diagnosis | low | open |
| [tslearn: njit_sakoe_chiba_mask](suggestions/fd70f1ac5129406e5761.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: set_weights](suggestions/c6e70a9295e0b43a89cb.md) | A1 | needs_diagnosis | low | open |
| [tslearn: shapelets_](suggestions/f3bf662dc22f29f79acf.md) | A1 | needs_diagnosis | low | open |
| [tslearn: BaseModelPackage](suggestions/f995a70ba75a6f818ba5.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: EmptyClusterError](suggestions/3bb29d868c529bcad84e.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: GlobalArgminPooling1D](suggestions/7fec39a7ce54e7122bf8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: GlobalMinPooling1D](suggestions/4019272c56a19f2872ad.md) | A2 | needs_diagnosis | low | open |
| [tslearn: KNeighborsTimeSeriesMixin](suggestions/66288f871906a29f15a8.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: LearningShapelets](suggestions/a03010ee7627aa0f49c8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: LocalSquaredDistanceLayer](suggestions/06a7cd0158af8a0604f8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: NonMyopicEarlyClassifier](suggestions/4f037ac09d68fff30b4d.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: NumPyBackend](suggestions/3bc2e78380cd347e066f.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: NumPyRandom](suggestions/d50d93cf638187995e0f.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PatchingLayer](suggestions/d0957863ecb711faa6c8.md) | A2 | needs_diagnosis | low | open |
| [tslearn: PyTorchBackend](suggestions/d2a2e06b853eef716bb1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PyTorchRandom](suggestions/900f8f4a475dc62bb350.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: PyTorchTesting](suggestions/e75daed6c7429f1a1048.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: SoftDTW](suggestions/3eb071d1a1ee8cb916a7.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: SquaredEuclidean](suggestions/3f27f4b6cc2ff519a694.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesSVMMixin](suggestions/0f6325e1b4f2389d4abb.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TsLearnTags](suggestions/00dd44f6e4ef414dbbf4.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: build](suggestions/f73b986047aa6c515b80.md) | A2 | needs_diagnosis | low | open |
| [tslearn: call](suggestions/5de88051085748a6a12c.md) | A2 | needs_diagnosis | low | open |
| [tslearn: cdist_sax](suggestions/0f28003de98d5ae5656c.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: check_keras_backend](suggestions/0476ec0dd20cfcfc0f3a.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: compute](suggestions/4a28af1f1c30cd779151.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: compute_output_shape](suggestions/e11427e7509aeb1fabff.md) | A2 | needs_diagnosis | low | open |
| [tslearn: cydist_1d_sax](suggestions/2e76ea80776db663eb78.md) | A2 | needs_diagnosis | low | open |
| [tslearn: decision_function](suggestions/90f1882d52407388781f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: dtw_barycenter_averaging_one_init](suggestions/c58de824dd094aad07bc.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: early_predict_proba](suggestions/1d9195b5c2bf45a1c7da.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: extract_from_zip_url](suggestions/556446f978a96da3cd17.md) | A2 | needs_diagnosis | low | open |
| [tslearn: fix_force_all_finite_warning](suggestions/19d92b0287f41c177588.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: from_cesium_dataset](suggestions/983fb54c898d2b3bb990.md) | A2 | needs_diagnosis | low | open |
| [tslearn: from_json](suggestions/c00cb00d746fa1ffa697.md) | A2 | needs_diagnosis | low | open |
| [tslearn: from_pickle](suggestions/0f71db7bc37749a20233.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_backend](suggestions/1f1c9231449a82dd76e1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_cluster_probas](suggestions/dbbbd6d4fe034fb71a4c.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_config](suggestions/e7e4aeb1e4da6544276e.md) | A2 | needs_diagnosis | low | open |
| [tslearn: get_early_predict_proba_generator](suggestions/c7c8a7deba0271c30c59.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: get_weights](suggestions/d062f90a19b6676ec7cf.md) | A2 | needs_diagnosis | low | open |
| [tslearn: grabocka_params_to_shapelet_size_dict](suggestions/d09163a6488511cf5a43.md) | A2 | needs_diagnosis | low | open |
| [tslearn: inv_transform_1d_sax](suggestions/dfdfaa2f4d3624d46ed2.md) | A2 | needs_diagnosis | low | open |
| [tslearn: inv_transform_sax](suggestions/0141328727366391a9f5.md) | A2 | needs_diagnosis | low | open |
| [tslearn: inverse_transform](suggestions/27b2acd83b60d8ed2f90.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: is_float](suggestions/d24aaded888f4b4bfc87.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: is_float32](suggestions/b64a87449b75059926df.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: is_float64](suggestions/24b26619da067b29ed62.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: iscomplex](suggestions/ec9c6d62bb40991b43d6.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: jacobian_product](suggestions/5eb42a36285bbdb40258.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: lcss_accumulated_matrix](suggestions/a052216881cad4209ce1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: locate](suggestions/c501d3c2fb0362ac8b0f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: normal](suggestions/e910f1e8c01175070256.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: pairwise_distances](suggestions/832fea73997fc2266b64.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: predict_class_and_earliness](suggestions/d2ff189e60095b0de249.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: select_backend](suggestions/db7d46ac6987e477fc50.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: set_backend](suggestions/75e45300371051b6a516.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: set_weights](suggestions/7eefa619cd3fce110254.md) | A2 | needs_diagnosis | low | open |
| [tslearn: shapelets_](suggestions/c05340e86035f734bb6f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: support_vectors_](suggestions/2ac402a74c2257cb4cfd.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: to_cesium_dataset](suggestions/7e892c56816236b0eeff.md) | A2 | needs_diagnosis | low | open |
| [tslearn: to_pickle](suggestions/fbf9d5a6bd05cc38a021.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: uniform](suggestions/8e82751fb4e01235d481.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: GlobalArgminPooling1D](suggestions/5ea7e3a3114bca295a5c.md) | B2 | needs_diagnosis | low | open |
| [tslearn: GlobalMinPooling1D](suggestions/e1e8d10e181fb64feb86.md) | B2 | needs_diagnosis | low | open |
| [tslearn: LearningShapelets](suggestions/58c42fc13b0f89081067.md) | B2 | needs_diagnosis | low | open |
| [tslearn: LocalSquaredDistanceLayer](suggestions/eb45ba57f07931571043.md) | B2 | needs_diagnosis | low | open |
| [tslearn: PatchingLayer](suggestions/487cb9d4ac16bce9bc97.md) | B2 | needs_diagnosis | low | open |
| [tslearn: TimeSeriesMixin](suggestions/11539dd38bd61037c4cb.md) | B2 | needs_diagnosis | medium | open |
| [tslearn: build](suggestions/43d24967de8de0a3d000.md) | B2 | needs_diagnosis | low | open |
| [tslearn: call](suggestions/b9635ecc5e10771a1f83.md) | B2 | needs_diagnosis | low | open |
| [tslearn: compute_output_shape](suggestions/a741b87fdae129fa9481.md) | B2 | needs_diagnosis | low | open |
| [tslearn: extract_from_zip_url](suggestions/896b6032e9cffff495ef.md) | B2 | needs_diagnosis | low | open |
| [tslearn: get_weights](suggestions/863512fca8a77879a3e2.md) | B2 | needs_diagnosis | low | open |
| [tslearn: grabocka_params_to_shapelet_size_dict](suggestions/a6a899142bd729b141ad.md) | B2 | needs_diagnosis | low | open |
| [tslearn: is_float](suggestions/71dcc930c95d37f1574a.md) | B2 | needs_diagnosis | medium | open |
| [tslearn: is_float32](suggestions/4312ea140c5d67b30b30.md) | B2 | needs_diagnosis | medium | open |
| [tslearn: is_float64](suggestions/e91b825ffe942e8a181b.md) | B2 | needs_diagnosis | medium | open |
| [tslearn: locate](suggestions/f8756110411ba9f8061d.md) | B2 | needs_diagnosis | low | open |
| [tslearn: set_weights](suggestions/34b923bd31e87c818a5e.md) | B2 | needs_diagnosis | low | open |
| [tslearn: shapelets_as_time_series_](suggestions/e697b716fe60437245c2.md) | B2 | needs_diagnosis | low | open |

## Human and agent workflow

`open → proposed → human-approved plan → human/agent implementation → submitted validation → human acceptance or revision`

Defer or reject any suggestion. A changed evidence version makes older decisions stale. Actor labels are operator-supplied audit records, not an authentication system. Approval records authorize no automatic subprocess or LLM execution in this tool.

- [Review command and decision formats](WORKFLOW.md)
- [Machine-readable assessment](assessment.json) · [Improvement queue](improvement_queue.json)
- [Architecture and human involvement](../AIDEAL_DESIGN_LOGIC.md)
- [Data, formats, samples, and API tests](../FINAL_REPORT_DATA_AND_API_METHODS.md)
- [Detailed 2×2 evidence](../../DETAILED_PRIORITY_REPORT.md)

Errors: none observed
