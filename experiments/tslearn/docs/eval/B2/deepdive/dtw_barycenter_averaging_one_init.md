# Deep-dive: `dtw_barycenter_averaging_one_init`

model: google:gemini-3.1-pro-preview · tokens in=5,808 out=4,385 · wall 33s · 2026-09-08 15:10

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** ADVANCED/LOW-LEVEL. This is a single-initialization helper function that acts as the core optimization engine for the higher-level, user-facing `dtw_barycenter_averaging` function (which loops over `n_init` and calls this API).
- **Testability:** TESTABLE FROM PUBLIC INPUTS. It can be executed directly by providing a standard 3D time-series array, provided it is imported from its specific submodule rather than the top-level package.

**L1 PURPOSE**
The `dtw_barycenter_averaging_one_init` API computes the Dynamic Time Warping (DTW) Barycenter Averaging (DBA) for a time-series dataset using a single initialization of the Expectation-Maximization (EM) algorithm. It sits at the core of the library's barycenter computation data flow, performing the actual Majorize-Minimize Mean Algorithm optimization steps to find a representative average sequence for a set of time series.

**L2 CONTRACT**
- **Parameters:**
  - `X`: array-like, shape `(n_ts, sz, d)`. The time-series dataset to average.
  - `barycenter_size`: `int` or `None` (default: `None`). The length of the generated barycenter. If `None`, defaults to the size of the data or the initial barycenter.
  - `init_barycenter`: array or `None` (default: `None`). The initial barycenter time series to start the optimization process.
  - `max_iter`: `int` (default: `30`). The maximum number of Expectation-Maximization iterations.
  - `tol`: `float` (default: `1e-5`). The tolerance for early stopping based on cost decrease.
  - `weights`: `None` or array (default: `None`). The weights for each time series in `X`. Must be the same length as `X`. If `None`, uniform weights are used.
  - `metric_params`: `dict` or `None` (default: `None`). DTW constraint parameters (e.g., `global_constraint`, `sakoe_chiba_radius`).
  - `verbose`: `boolean` (default: `False`). Whether to print cost information at each iteration.
  - `n_jobs`: `int` or `None` (default: `None`). The number of parallel jobs to run.
- **Returns:**
  - `barycenter`: `numpy.ndarray` of shape `(barycenter_size, d)` or `(sz, d)`. The optimized DBA barycenter.
  - `cost`: `float`. The associated inertia (DTW cost).

**L3 MECHANICS**
1. **Initialization:** The function instantiates a NumPy backend (line 700) and ensures `X` is a properly formatted time-series dataset using `to_time_series_dataset` (line 702). It sets up weights using `_set_weights` (line 705) and initializes the barycenter (either from `init_barycenter` or using `_init_avg` at line 707).
2. **Optimization Loop:** It enters an EM optimization loop up to `max_iter` times:
   - Computes assignments and the current cost using `_mm_assignment` (line 717).
   - Computes valence warping using `_mm_valence_warping` (line 724).
   - Updates the barycenter using `_mm_update_barycenter` (line 728).
3. **Convergence Check:** If the absolute difference between the previous and current cost is less than `tol`, it breaks (line 729). If the cost increases, it emits a `ConvergenceWarning` and breaks (line 732).
4. **Return:** Finally, it returns the optimized barycenter and its final cost.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
from tslearn.barycenters.dba import dtw_barycenter_averaging_one_init
from tslearn.utils import to_time_series_dataset

# 1. Format data into the required 3D shape (n_ts, sz, d)
X = to_time_series_dataset([
    [1.0, 2.0, 3.0], 
    [1.0, 2.0, 2.0], 
    [2.0, 2.0, 3.0]
])

# 2. Compute the DBA barycenter and inertia for a single initialization
barycenter, inertia = dtw_barycenter_averaging_one_init(
    X=X, 
    max_iter=10, 
    tol=1e-4
)

assert isinstance(barycenter, np.ndarray)
assert barycenter.shape == (3, 1)
assert isinstance(inertia, float)
print(f"Inertia: {inertia:.4f}")
```

**L5 FAILURE FORENSICS**
- **Failure:** `cannot import name 'dtw_barycenter_averaging_one_init' from 'tslearn.barycenters'`
- **Reason:** The documentation entry incorrectly suggested `from tslearn.barycenters import dtw_barycenter_averaging_one_init`. This function is an advanced helper and is not exposed in the `__init__.py` of the `tslearn.barycenters` package. It must be imported directly from the submodule where it is defined: `from tslearn.barycenters.dba import dtw_barycenter_averaging_one_init`.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** The exact reason the import failed from `tslearn.barycenters` is inferred to be its omission from the package's `__init__.py`, based on standard Python module resolution and the fact that it is defined in `tslearn/barycenters/dba.py`.
- **INFERENCE:** The `ConvergenceWarning` is inferred to be imported from `sklearn.exceptions` or a similar internal module, though its exact origin isn't shown in the provided snippet.
- **Confidence Score L2 (Contract):** 10/10. The parameters and return types are explicitly documented in the docstring and visible in the code.
- **Confidence Score L3 (Mechanics):** 10/10. The algorithm's steps and internal helper function calls are clearly visible in the provided source code.
- **Confidence Score L4 (Usage):** 10/10. The minimal usage snippet correctly bypasses the import failure by targeting the submodule directly and uses the correct input shapes.