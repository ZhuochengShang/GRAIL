# AIDEAL readiness assessment and improvement queue

Updated: 2026-09-08T07:02:15.700301+00:00

**Measured scope:** how documentation affects an LLM’s API use under a fixed harness. Overall agent readiness is not yet fully measured; no composite score is assigned.

| Repository | A1 | A2 | B1 | B2 | Matched comparison |
|---|---|---|---|---|---|
| mir_eval | 0/148 provisional | 135/148 final | pending (148 APIs) | pending (148 APIs) | WITHHELD/PARTIAL |
| thumbnailator | 1/149 provisional | 127/149 final | pending (149 APIs) | pending (149 APIs) | WITHHELD/PARTIAL |
| tslearn | 118/235 provisional | 172/235 provisional | pending (235 APIs) | pending (235 APIs) | WITHHELD/PARTIAL |

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
| mir_eval | doc-wrong | 2 |
| mir_eval | example-invalid | 1 |
| mir_eval | provider | 2 |
| mir_eval | test/scaffold | 5 |
| mir_eval | unknown | 5 |
| thumbnailator | provider | 4 |
| thumbnailator | unknown | 23 |
| tslearn | api-identity-or-version | 48 |
| tslearn | assertion-or-behavior | 23 |
| tslearn | input-contract-or-api-call | 10 |
| tslearn | provider | 50 |
| tslearn | unknown | 49 |

## Reviewable improvements (222)

Review states: `{'open': 221, 'proposed': 1}`. Observation errors: 0. Inactive reviewed IDs retained: 0.

Each card separates native failure, diagnosis confidence, proposed action, validation and review decisions. Provider barriers concern execution infrastructure; they are not automatically codebase or documentation defects.

| Suggestion | Cell | Priority | Confidence | Review |
|---|---|---|---|---|
| [mir_eval: IntervalFormatter](suggestions/43eb9410c759c001a0ca.md) | A1 | execution_blocker | high | open |
| [mir_eval: absolute_error](suggestions/082799557f3d00ef3959.md) | A1 | execution_blocker | high | open |
| [thumbnailator: clear](suggestions/3f911dbe0befc683e80e.md) | A1 | execution_blocker | high | open |
| [thumbnailator: createOutputStream](suggestions/8c69e4aae53d75a4ecbd.md) | A1 | execution_blocker | high | open |
| [thumbnailator: format](suggestions/a4ae9b56216ff3fc31e1.md) | A1 | execution_blocker | high | open |
| [thumbnailator: region](suggestions/760de2afb8c91ba44d2a.md) | A1 | execution_blocker | high | open |
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
| [tslearn: early_predict](suggestions/3c11412b7b124c2586be.md) | A1 | execution_blocker | high | open |
| [tslearn: fix_force_all_finite_warning](suggestions/31a797e1c04a6d32d433.md) | A1 | execution_blocker | high | open |
| [tslearn: frechet](suggestions/f34bfa3d928fc87d7712.md) | A1 | execution_blocker | high | open |
| [tslearn: from_numpy](suggestions/a9a5f5305a9c56f56d78.md) | A1 | execution_blocker | high | open |
| [tslearn: from_pickle](suggestions/64d5f423ce89ffd24885.md) | A1 | execution_blocker | high | open |
| [tslearn: gamma_soft_dtw](suggestions/438ddac357b01927a578.md) | A1 | execution_blocker | high | open |
| [tslearn: get_backend](suggestions/5b561e6f3abaf83879f5.md) | A1 | execution_blocker | high | open |
| [tslearn: get_early_predict_generator](suggestions/da327bb49da71d852107.md) | A1 | execution_blocker | high | open |
| [tslearn: get_early_predict_proba_generator](suggestions/3ae2ab1db15f8c5ceb1e.md) | A1 | execution_blocker | high | open |
| [tslearn: is_array](suggestions/e1024e725bbecccd33ed.md) | A1 | execution_blocker | high | open |
| [tslearn: is_float](suggestions/0b0c74d7bbfc877ac3f6.md) | A1 | execution_blocker | high | open |
| [tslearn: is_float32](suggestions/e4a6a53c15dc8f409272.md) | A1 | execution_blocker | high | open |
| [tslearn: is_numpy](suggestions/585c5d6b183ad80a9a85.md) | A1 | execution_blocker | high | open |
| [tslearn: iscomplex](suggestions/25813de0f12d953e9275.md) | A1 | execution_blocker | high | open |
| [tslearn: jacobian_product](suggestions/efe13aead9dc33ab2b15.md) | A1 | execution_blocker | high | open |
| [tslearn: mase](suggestions/d6318ccb7f4952366621.md) | A1 | execution_blocker | high | open |
| [tslearn: mse](suggestions/3af68a89e69ff9f8ddde.md) | A1 | execution_blocker | high | open |
| [tslearn: njit_lcss_accumulated_matrix](suggestions/82cd652dd43be2a632db.md) | A1 | execution_blocker | high | open |
| [tslearn: njit_sakoe_chiba_mask](suggestions/fd70f1ac5129406e5761.md) | A1 | execution_blocker | high | open |
| [tslearn: normal](suggestions/8d62931fe716c65b2b83.md) | A1 | execution_blocker | high | open |
| [tslearn: partial_fit](suggestions/f0c4cd50ddf3925e7c6a.md) | A1 | execution_blocker | high | open |
| [tslearn: predict_proba_and_earliness](suggestions/2caa8ac2f3722ae16c2d.md) | A1 | execution_blocker | high | open |
| [tslearn: save_dict](suggestions/64042927743239068f2f.md) | A1 | execution_blocker | high | open |
| [tslearn: set_weights](suggestions/c6e70a9295e0b43a89cb.md) | A1 | execution_blocker | high | open |
| [tslearn: shapelets_](suggestions/f3bf662dc22f29f79acf.md) | A1 | execution_blocker | high | open |
| [tslearn: time_series_to_str](suggestions/9652e1731d654fce29a6.md) | A1 | execution_blocker | high | open |
| [tslearn: to_numpy](suggestions/2e3b666651dfa822d085.md) | A1 | execution_blocker | high | open |
| [tslearn: compute](suggestions/4a28af1f1c30cd779151.md) | A2 | execution_blocker | high | open |
| [tslearn: jacobian_product](suggestions/5eb42a36285bbdb40258.md) | A2 | execution_blocker | high | open |
| [tslearn: predict_class_and_earliness](suggestions/d2ff189e60095b0de249.md) | A2 | execution_blocker | high | open |
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
| [tslearn: from_cesium_dataset](suggestions/74e41bf5593381100866.md) | A1 | needs_diagnosis | low | open |
| [tslearn: get_config](suggestions/fb7d4835a71492d56456.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: get_weights](suggestions/83c83dcec847f0d943ac.md) | A1 | needs_diagnosis | low | open |
| [tslearn: grabocka_params_to_shapelet_size_dict](suggestions/c3cb9b853138fa7c069d.md) | A1 | needs_diagnosis | low | open |
| [tslearn: in_file_string_replace](suggestions/3282c032f77f266a111b.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: intercept_](suggestions/78a1eb5f5696690a735e.md) | A1 | needs_diagnosis | low | open |
| [tslearn: inv_transform_1d_sax](suggestions/cf8546b8ee3ce06e5d54.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: inv_transform_paa](suggestions/a44b4ec0aad52bf06da7.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: inv_transform_sax](suggestions/8b3b78113a8ea76d8445.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: is_float64](suggestions/545702fa480e865ad66f.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: is_pytorch](suggestions/9abd9792d2738f2a7ece.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: itakura_mask](suggestions/616661edba3331238939.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: lcss_accumulated_matrix](suggestions/991948e2bb7e96320036.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: lcss_accumulated_matrix_from_dist_matrix](suggestions/f5bb96cdd1d0d8a7962c.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: list_cached_datasets](suggestions/cf40b090c19e4acb2bbd.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: load_dict](suggestions/d6a84054031158dccd7c.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: locate](suggestions/884c0788395a87c4ac28.md) | A1 | needs_diagnosis | low | open |
| [tslearn: n_iter_](suggestions/2b36250d86a6501de6fc.md) | A1 | needs_diagnosis | low | open |
| [tslearn: njit_accumulated_matrix](suggestions/0e550abc302b6355626e.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: njit_accumulated_matrix_from_dist_matrix](suggestions/f294249de8aada17af69.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: njit_lcss_accumulated_matrix_from_dist_matrix](suggestions/cf58d9000a1035ad27a0.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: normalized_cc](suggestions/7b9cdbc1d982d1e04280.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: pdist](suggestions/47b9e17eb225846e80f1.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: sakoe_chiba_mask](suggestions/794af5d1beaf4b0923a9.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: select_backend](suggestions/2961207c342b88fd36d0.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: set_backend](suggestions/ad3b8b8a985b219f35d1.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: shapelets_as_time_series_](suggestions/f06adb8819276f99434e.md) | A1 | needs_diagnosis | low | open |
| [tslearn: sigma_gak](suggestions/7d395854025311aa6d96.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: to_cesium_dataset](suggestions/3bffa156bd3848d8d745.md) | A1 | needs_diagnosis | low | open |
| [tslearn: to_hdf5](suggestions/bdb5c733f5946d18f9a7.md) | A1 | needs_diagnosis | low | open |
| [tslearn: to_json](suggestions/b46525822e9ee905585b.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: to_pickle](suggestions/b3bae748f28acda78bca.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: transform](suggestions/24cec3efaf9a7aad4548.md) | A1 | needs_diagnosis | low | open |
| [tslearn: tril](suggestions/e05bdc1a311e4986ce33.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: tril_indices](suggestions/74dcb9c00104264d76ff.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: triu](suggestions/eb410220623eddf2a39d.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: triu_indices](suggestions/2b0c145acb8fe92a71a8.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: uniform](suggestions/fe38236ea9ba8c3a2aad.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: y_shifted_sbd_vec](suggestions/a116a86c554f8be3af5f.md) | A1 | needs_diagnosis | medium | open |
| [tslearn: BaseModelPackage](suggestions/f995a70ba75a6f818ba5.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: EmptyClusterError](suggestions/3bb29d868c529bcad84e.md) | A2 | needs_diagnosis | medium | open |
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
| [tslearn: TimeSeriesMixin](suggestions/aa8648d7d75d5da46815.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesResampler](suggestions/dd12fb1c790d34bcc370.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TimeSeriesSVMMixin](suggestions/0f6325e1b4f2389d4abb.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: TsLearnTags](suggestions/00dd44f6e4ef414dbbf4.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: accumulated_matrix](suggestions/f2643d45b8ffc2210fa6.md) | A2 | needs_diagnosis | low | open |
| [tslearn: build](suggestions/f73b986047aa6c515b80.md) | A2 | needs_diagnosis | low | open |
| [tslearn: call](suggestions/5de88051085748a6a12c.md) | A2 | needs_diagnosis | low | open |
| [tslearn: compute_output_shape](suggestions/e11427e7509aeb1fabff.md) | A2 | needs_diagnosis | low | open |
| [tslearn: cydist_1d_sax](suggestions/2e76ea80776db663eb78.md) | A2 | needs_diagnosis | low | open |
| [tslearn: decision_function](suggestions/90f1882d52407388781f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: dtw_barycenter_averaging_one_init](suggestions/c58de824dd094aad07bc.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: early_predict_proba](suggestions/1d9195b5c2bf45a1c7da.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: extract_from_zip_url](suggestions/556446f978a96da3cd17.md) | A2 | needs_diagnosis | low | open |
| [tslearn: fix_force_all_finite_warning](suggestions/19d92b0287f41c177588.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: from_cesium_dataset](suggestions/983fb54c898d2b3bb990.md) | A2 | needs_diagnosis | low | open |
| [tslearn: from_hdf5](suggestions/db7a06f2638d29b9e384.md) | A2 | needs_diagnosis | low | open |
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
| [tslearn: lcss_accumulated_matrix](suggestions/a052216881cad4209ce1.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: load_dict](suggestions/8f3b17699f7dcf2be90f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: locate](suggestions/c501d3c2fb0362ac8b0f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: normal](suggestions/e910f1e8c01175070256.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: pairwise_distances](suggestions/832fea73997fc2266b64.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: select_backend](suggestions/db7d46ac6987e477fc50.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: set_backend](suggestions/75e45300371051b6a516.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: set_weights](suggestions/7eefa619cd3fce110254.md) | A2 | needs_diagnosis | low | open |
| [tslearn: shapelets_](suggestions/c05340e86035f734bb6f.md) | A2 | needs_diagnosis | low | open |
| [tslearn: shapelets_as_time_series_](suggestions/d6a9bb0ebcc53693508b.md) | A2 | needs_diagnosis | low | open |
| [tslearn: support_vectors_](suggestions/2ac402a74c2257cb4cfd.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: to_cesium_dataset](suggestions/7e892c56816236b0eeff.md) | A2 | needs_diagnosis | low | open |
| [tslearn: to_pickle](suggestions/fbf9d5a6bd05cc38a021.md) | A2 | needs_diagnosis | medium | open |
| [tslearn: uniform](suggestions/8e82751fb4e01235d481.md) | A2 | needs_diagnosis | medium | open |

## Human and agent workflow

`open → proposed → human-approved plan → human/agent implementation → submitted validation → human acceptance or revision`

Defer or reject any suggestion. A changed evidence version makes older decisions stale. Actor labels are operator-supplied audit records, not an authentication system. Approval records authorize no automatic subprocess or LLM execution in this tool.

- [Review command and decision formats](WORKFLOW.md)
- [Machine-readable assessment](assessment.json) · [Improvement queue](improvement_queue.json)
- [Architecture and human involvement](../AIDEAL_DESIGN_LOGIC.md)
- [Data, formats, samples, and API tests](../FINAL_REPORT_DATA_AND_API_METHODS.md)
- [Detailed 2×2 evidence](../../DETAILED_PRIORITY_REPORT.md)

Errors: none observed
