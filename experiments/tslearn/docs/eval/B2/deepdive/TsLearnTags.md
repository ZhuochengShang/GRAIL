# Deep-dive: `TsLearnTags`

model: google:gemini-3.1-pro-preview · tokens in=4,442 out=4,134 · wall 32s · 2026-09-08 14:58

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
INTERNAL/FRAMEWORK. TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION.
This API is an internal utility used to bridge `tslearn` estimators with scikit-learn's estimator tag system. It is not intended for direct use by end-users and should be excluded from main user-facing benchmark denominators. It is testable by explicitly providing the required dataclass fields expected by scikit-learn's `Tags` base class.

**L1 PURPOSE**
`TsLearnTags` is a dataclass (or a `dict` fallback for older scikit-learn versions) that extends scikit-learn's estimator `Tags` system to include time-series specific capabilities. It sits at the base of `tslearn`'s estimator hierarchy (via `TimeSeriesMixin`), signaling to scikit-learn's validation and tuning utilities that `tslearn` models accept 3D arrays and optionally support variable-length time series, while explicitly rejecting sparse inputs.

**L2 CONTRACT**
- **Receiver:** `TsLearnTags` class.
- **Parameters:** `**kwargs` representing the fields of scikit-learn's `Tags` dataclass (e.g., `estimator_type`, `target_tags`, `input_tags`, etc.). If scikit-learn < 1.6, it acts as a standard `dict` constructor and accepts arbitrary keyword arguments.
- **Return value:** An instance of `TsLearnTags` (which is a subclass of `sklearn.utils.Tags` or an alias for `dict`).
- **Visibility:** Public within the package, but intended for internal framework use.
- **Thread-safety:** Safe to instantiate across threads; instances are mutable but typically used as read-only metadata configurations.

**L3 MECHANICS**
When instantiated (in scikit-learn >= 1.6 environments), `TsLearnTags` calls `super().__init__(**kwargs)` to populate the standard scikit-learn tags. It then mutates its own `input_tags` attribute, setting `sparse = False` and `three_d_array = True`. It also defines a custom field `allow_variable_length` defaulting to `False`. In environments with scikit-learn < 1.6, the `sklearn.utils.Tags` import fails, and `TsLearnTags` gracefully degrades to a standard Python `dict` via an `ImportError` catch.

**L4 CORRECT MINIMAL USAGE**
```python
from tslearn.bases.bases import TsLearnTags

if TsLearnTags is dict:
    # Fallback for scikit-learn < 1.6
    tags = TsLearnTags()
    assert isinstance(tags, dict)
else:
    # scikit-learn >= 1.6
    from sklearn.base import BaseEstimator
    from dataclasses import fields
    
    # Obtain default tags from a base estimator to satisfy required fields
    tags_orig = BaseEstimator().__sklearn_tags__()
    as_dict = {field.name: getattr(tags_orig, field.name) for field in fields(tags_orig)}
    
    # Instantiate TsLearnTags with the required fields
    tags = TsLearnTags(**as_dict)
    
    assert tags.input_tags.sparse is False
    assert tags.input_tags.three_d_array is True
    assert tags.allow_variable_length is False

print(f"__CHECK__ TsLearnTags {type(tags).__name__}")
```

**L5 FAILURE FORENSICS**
- `TypeError: Tags.__init__() missing 2 required positional arguments: 'estimator_type' and 'target_tags'`: This occurred because the test attempted to instantiate `TsLearnTags()` without any arguments. In environments with scikit-learn >= 1.6, `TsLearnTags` inherits from `sklearn.utils.Tags`, which is a dataclass that requires specific fields (`estimator_type` and `target_tags`) to be provided upon initialization. The documentation incorrectly stated that it takes no arguments.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** The exact required fields of `sklearn.utils.Tags` (`estimator_type` and `target_tags`) are inferred from the failure message, though their existence as required dataclass fields is standard Python behavior.
- **INFERENCE:** The assumption that `BaseEstimator().__sklearn_tags__()` provides all necessary fields to instantiate `TsLearnTags` is based on the implementation of `TimeSeriesMixin.__sklearn_tags__` in the provided source.
- **Confidence in L2 (Contract):** 9/10. The contract is clear from the source code and the fallback mechanism.
- **Confidence in L3 (Mechanics):** 10/10. The mechanics are explicitly written in the `__init__` method and the `try/except` block.
- **Confidence in L4 (Usage):** 9/10. The usage snippet correctly handles both the dataclass and dict fallback scenarios based on the scikit-learn version, mirroring the library's own internal usage pattern.