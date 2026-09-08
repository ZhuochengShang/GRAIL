# Deep-dive: `cdist_sax`

model: google:gemini-3.1-pro-preview · tokens in=4,168 out=2,612 · wall 21s · 2026-09-08 15:01

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. The function is exposed in the public `tslearn.metrics` namespace, has a detailed docstring with references, and is intended for users computing MINDIST distances on SAX-transformed data.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function can be invoked directly with standard Python lists or NumPy arrays representing the SAX symbols, breakpoints, and original sizes, as demonstrated by the real call site in `test_metrics.py`.

**L1 PURPOSE**
`cdist_sax` calculates a cross-similarity matrix of MINDIST distances between two datasets of SAX-transformed (Symbolic Aggregate approXimation) time series. It sits in the metrics module, acting as a high-level Python wrapper that normalizes the input data types and delegates the core pairwise distance computations to a Cython backend (`cydist_sax`) via a generic parallelization helper.

**L2 CONTRACT**
- **Parameters:**
  - `dataset1`: Array-like of shape `(n_ts1, sz1, d)`, `(n_ts1, sz1)`, or `(sz1,)`. The first dataset of SAX-transformed time series (represented as integer symbols).
  - `breakpoints_avg`: Array-like, 1D. The breakpoints used to assign the SAX alphabet symbols.
  - `size_fitted`: `int`. The original number of timesteps in the time series before they were discretized through SAX.
  - `dataset2`: Array-like of shape `(n_ts2, sz2, d)`, `(n_ts2, sz2)`, or `(sz2,)`, default `None`. The second dataset of SAX-transformed time series. If `None`, the self-similarity matrix of `dataset1` is computed.
  - `n_jobs`: `int` or `None`, default `None`. The number of parallel jobs to run (`-1` means all processors).
  - `verbose`: `int`, default `0`. The verbosity level for progress messages.
- **Returns:**
  - `cdist`: Array-like (NumPy array) of shape `(n_ts1, n_ts2)`. The cross-similarity matrix containing the computed MINDIST distances.
- **Preconditions:** The original time series from which the SAX symbols were derived must have been normalized to zero mean and unit variance, as the MINDIST mathematical formulation relies on this assumption.

**L3 MECHANICS**
1. **Backend Initialization:** It instantiates a NumPy backend explicitly (`be = instantiate_backend("numpy")`) (line 70).
2. **Data Formatting:** It converts `dataset1` (and `dataset2` if provided) into 3D time-series datasets using `to_time_series_dataset`. Crucially, it forces the data type to `int` (`dtype=int`) because SAX representations are discrete integer symbols (lines 71-73).
3. **Delegation:** It calls the internal helper `_cdist_sax` (line 74), passing the formatted datasets, breakpoints, original size, and parallelization arguments.
4. **Execution:** `_cdist_sax` delegates to `_cdist_generic` (line 96), passing the Cython function `cydist_sax` as the `dist_fun`. `_cdist_generic` handles the pairwise iteration, parallelization (`n_jobs`), and verbosity, while `cydist_sax` computes the actual MINDIST distance between individual pairs of SAX representations.

**L4 CORRECT MINIMAL USAGE**
```python
import numpy as np
import tslearn.metrics

# SAX-transformed data (integer symbols)
dataset1 = [[-1, 0, 1], [1, 0, 1]]
# Breakpoints used for the SAX transformation
breakpoints = [-0.5, 0.0, 0.5]
# Original length of the time series before SAX
size_fitted = 3

# Compute self-similarity matrix
dists = tslearn.metrics.cdist_sax(
    dataset1=dataset1,
    breakpoints_avg=breakpoints,
    size_fitted=size_fitted
)

assert dists.shape == (2, 2)
print(f"Computed SAX MINDIST matrix:\n{dists}")
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `TypeError: SymbolicAggregateApproximation.__init__() got an unexpected keyword argument 'alphabet_size'`
- **Reason:** The user attempted to generate the SAX inputs dynamically using `tslearn.piecewise.SymbolicAggregateApproximation` but passed an invalid keyword argument (`alphabet_size`) to its constructor (likely confusing it with `n_bins` or a similar parameter). The failure occurred during the setup phase before `cdist_sax` was ever called. To test `cdist_sax` directly, one should bypass the transformer and provide the integer symbols directly, as shown in the minimal usage example.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - I inferred that `cydist_sax` is a Cython function based on the import name (`from .cysax import cydist_sax`).
  - I inferred that the user's failed attempt was trying to use `tslearn.piecewise.SymbolicAggregateApproximation` to generate inputs, based on the class name in the `TypeError`.
- **Information needed for certainty:** The exact implementation of `cydist_sax` and `_cdist_generic` to confirm how the parallelization and Cython GIL release are handled.
- **Confidence Scores:**
  - **L2 (Contract): 10/10** - The docstring and type conversions in the source code explicitly define the inputs, outputs, and expected types.
  - **L3 (Mechanics): 10/10** - The source code provided shows the exact step-by-step delegation from `cdist_sax` to `_cdist_sax` to `_cdist_generic`.
  - **L4 (Minimal Usage): 10/10** - The usage is directly adapted from the provided real call site in `test_metrics.py`, ensuring correctness.