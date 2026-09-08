# tslearn PASS_TO_PASS after B2

- Exit code: 0
- Source commit: `f8f13ddf4186e2cc99c8ef495aeb46b1254a01f7`
- Python: `/Users/clockorangezoe/miniconda3/envs/geo_llm_spark/bin/python`
- Duration seconds: 83.0
- Output SHA-256: `e579b44c185b335604d584741c50c8c393ac54c042994ba4c8229b6d863b4e84`

```text
s.........................................XX..............s............. [  6%]
.............................XX......................................... [ 12%]
..........Xx.........................................x.......xx......... [ 19%]
..................................XX.................................... [ 25%]
.....XX..............................................XX...x............. [ 31%]
...........................XX........................................... [ 38%]
.XX...x........................................xx....................... [ 44%]
....................XX............................................XX.... [ 50%]
.........................................XX............................. [ 57%]
...................XX.................................................XX [ 63%]
.............s...........................................XX............. [ 69%]
....................................XX.................................. [ 76%]
........x........Xx...................................................x. [ 82%]
.......XX.................................................XX............ [ 88%]
................................XX...................................... [ 95%]
.................................sssss.......s........                   [100%]
=============================== warnings summary ===============================
tests/test_estimators.py:38
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tests/test_estimators.py:38: UserWarning: Skipped common tests for shapelets as it could not be imported. keras is probably not installed!
    warnings.warn('Skipped common tests for shapelets '

tests/test_early_classification.py: 38 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/early_classification/early_classification.py:283: RuntimeWarning: overflow encountered in exp
    s_k = 1. / (1. + np.exp(-self.lamb * delta_k))

tests/test_estimators.py: 120 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 20 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 300 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 1 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 18 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 21 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_positive_only_tag_during_fit]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_non_transformer_estimators_n_iter]
tests/test_estimators.py::test_all_estimators[MatrixProfile()-check_positive_only_tag_during_fit]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_positive_only_tag_during_fit]
tests/test_estimators.py::test_all_estimators[OneD_SymbolicAggregateApproximation()-check_positive_only_tag_during_fit]
tests/test_estimators.py::test_all_estimators[PiecewiseAggregateApproximation()-check_positive_only_tag_during_fit]
tests/test_estimators.py::test_all_estimators[SymbolicAggregateApproximation()-check_positive_only_tag_during_fit]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 150 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 14 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 12 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 121 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 30 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weights_shape]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weights_shape]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weights_shape]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weights_not_overwritten]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 16 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weight_equivalence_on_dense_data]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 27 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weight_equivalence_on_dense_data]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weight_equivalence_on_dense_data]
tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_sample_weight_equivalence_on_dense_data]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 15 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 12 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 80 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[KernelKMeans()-check_fit_check_is_fitted]
tests/test_estimators.py::test_all_estimators[MatrixProfile()-check_fit_check_is_fitted]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_fit_check_is_fitted]
tests/test_estimators.py::test_all_estimators[OneD_SymbolicAggregateApproximation()-check_fit_check_is_fitted]
tests/test_estimators.py::test_all_estimators[PiecewiseAggregateApproximation()-check_fit_check_is_fitted]
tests/test_estimators.py::test_all_estimators[SymbolicAggregateApproximation()-check_fit_check_is_fitted]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 100 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPClassifier()-check_classifiers_one_label]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 10 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
tests/test_estimators.py::test_all_estimators[NonMyopicEarlyClassifier()-check_classifiers_one_label]
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/sklearn/metrics/_classification.py:534: UserWarning: A single label was found in 'y_true' and 'y_pred'. For the confusion matrix to have the correct shape, use the 'labels' parameter to pass all known labels.
    warnings.warn(

tests/test_estimators.py: 59 warnings
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/sklearn/neural_network/_multilayer_perceptron.py:781: ConvergenceWarning: Stochastic Optimizer: Maximum iterations (10) reached and the optimization hasn't converged yet.
    warnings.warn(

tests/test_estimators.py::test_all_estimators[TimeSeriesMLPClassifier()-check_estimators_partial_fit_n_features]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_estimators_partial_fit_n_features]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressors_int]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressors_int]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 50 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[TimeSeriesMLPClassifier()-check_classifiers_multilabel_output_format_predict]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPClassifier()-check_classifiers_multilabel_output_format_predict_proba]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 25 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressor_data_not_an_array]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressor_data_not_an_array]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressor_data_not_an_array]
tests/test_estimators.py::test_all_estimators[TimeSeriesMLPRegressor()-check_regressor_data_not_an_array]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/utils/utils.py:129: UserWarning: 2-Dimensional data passed. Assuming these are 200 1-dimensional timeseries
    warnings.warn(

tests/test_estimators.py: 86 warnings
tests/test_metrics.py: 9 warnings
tests/test_svm.py: 4 warnings
tests/test_variablelength.py: 6 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/softdtw_variants.py:444: DeprecationWarning: This method is deprecated, use tslearn.metrics.sigma_gak instead.
    warnings.warn(

tests/test_estimators.py: 59 warnings
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/sklearn/svm/_base.py:305: ConvergenceWarning: Solver terminated early (max_iter=10).  Consider pre-processing your data with StandardScaler or MinMaxScaler.
    warnings.warn(

tests/test_estimators.py::test_all_estimators[TimeSeriesSVC()-check_non_transformer_estimators_n_iter]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/svm/svm.py:280: UserWarning: n_iter_ is always set to 1 for TimeSeriesSVC, since it is non-trivial to access the underlying libsvm
    warnings.warn('n_iter_ is always set to 1 for TimeSeriesSVC, since '

tests/test_estimators.py::test_all_estimators[TimeSeriesSVR()-check_non_transformer_estimators_n_iter]
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/svm/svm.py:553: UserWarning: n_iter_ is always set to 1 for TimeSeriesSVR, since it is non-trivial to access the underlying libsvm
    warnings.warn('n_iter_ is always set to 1 for TimeSeriesSVR, since '

tests/test_forecasting.py::test_VARIMA
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/forecasting/_arima.py:75: NumbaPerformanceWarning: np.dot() is faster on contiguous arrays, called on (Array(float64, 2, 'A', False, aligned=True), Array(float64, 2, 'C', False, aligned=True))
    current_err = X[:, i] - _varma_next(

tests/test_forecasting.py::test_verbosity
tests/test_forecasting.py::test_verbosity
tests/test_forecasting.py::test_verbosity
tests/test_forecasting.py::test_verbosity
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/forecasting/_arima.py:221: RuntimeWarning: Maximum number of iterations has been exceeded.
    res = scipy.optimize.minimize(

tests/test_metrics.py: 18 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/dtw_variants.py:391: DeprecationWarning: This method is deprecated, use tslearn.metrics.dtw_path instead.
    warnings.warn(

tests/test_metrics.py: 18 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/dtw_variants.py:803: DeprecationWarning: This method is deprecated, use tslearn.metrics.dtw instead.
    warnings.warn(

tests/test_metrics.py: 26 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/dtw_variants.py:1576: DeprecationWarning: This method is deprecated, use tslearn.metrics.sakoe_chiba_mask instead.
    warnings.warn(

tests/test_metrics.py: 27 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/dtw_variants.py:1736: DeprecationWarning: This method is deprecated, use tslearn.metrics.itakura_mask instead.
    warnings.warn(

tests/test_metrics.py: 63 warnings
  /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL_tslearn_full235_B2/experiments/tslearn/tslearn/tslearn/metrics/dtw_variants.py:1827: DeprecationWarning: This method is deprecated, use tslearn.metrics.compute_mask instead.
    warnings.warn(

tests/test_metrics.py::test_sax
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/numpy/core/numeric.py:330: RuntimeWarning: invalid value encountered in cast
    multiarray.copyto(a, fill_value, casting='unsafe')

tests/test_metrics.py::test_sax
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/numba/core/ir_utils.py:2087: NumbaPendingDeprecationWarning: 
  Encountered the use of a type that is scheduled for deprecation: type 'reflected list' found for argument 'breakpoints' of function 'cydist_sax'.
  
  For more information visit https://numba.readthedocs.io/en/stable/reference/deprecation.html#deprecation-of-reflection-for-list-and-set-types
  
  File "tslearn/metrics/cysax.py", line 38:
  @njit(parallel=True, fastmath=True)
  def cydist_sax(sax1, sax2, breakpoints, original_size):
  ^
  
    warnings.warn(NumbaPendingDeprecationWarning(msg, loc=loc))

tests/test_metrics.py::test_sax
  /Users/clockorangezoe/miniconda3/envs/geo_llm_spark/lib/python3.10/site-packages/numba/core/ir_utils.py:2087: NumbaPendingDeprecationWarning: 
  Encountered the use of a type that is scheduled for deprecation: type 'reflected list' found for argument 'breakpoints' of function '__numba_parfor_gufunc_0x17d3c6170'.
  
  For more information visit https://numba.readthedocs.io/en/stable/reference/deprecation.html#deprecation-of-reflection-for-list-and-set-types
  
  File "<string>", line 1:
  <source missing, REPL/exec in use?>
  
    warnings.warn(NumbaPendingDeprecationWarning(msg, loc=loc))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
1078 passed, 9 skipped, 11 xfailed, 36 xpassed, 1049 warnings in 78.60s (0:01:18)

```
