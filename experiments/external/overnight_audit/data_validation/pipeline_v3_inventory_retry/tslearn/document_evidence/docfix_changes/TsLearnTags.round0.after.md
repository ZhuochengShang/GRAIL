## API Test: `TsLearnTags`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class TsLearnTags(Tags) # Aliased to dict in scikit-learn < 1.6
```

### Goal
Internal framework compatibility shim bridging `tslearn` estimators with scikit-learn's estimator tag system. *Note: This is an INTERNAL/FRAMEWORK API requiring explicit low-level construction and should be excluded from the main user-facing benchmark denominator.*

### Parameters
- `**kwargs`: Keyword arguments representing the fields of scikit-learn's `Tags` dataclass (e.g., `estimator_type`, `target_tags`). Required in scikit-learn >= 1.6.

### Input
Requires explicit low-level construction. In scikit-learn >= 1.6, callers must provide all required dataclass fields expected by `sklearn.utils.Tags`. These are typically extracted from `sklearn.base.BaseEstimator().__sklearn_tags__()`. In scikit-learn < 1.6, it acts as a standard `dict` constructor.

### Output
An instance of `TsLearnTags` (a subclass of `sklearn.utils.Tags` or an alias for `dict`). When instantiated as a dataclass, it guarantees `input_tags.sparse = False`, `input_tags.three_d_array = True`, and `allow_variable_length = False`.

### Valid Call Patterns
```python
from tslearn.bases.bases import TsLearnTags

if TsLearnTags is dict:
    # Fallback for scikit-learn < 1.6
    tags = TsLearnTags()
    assert isinstance(tags, dict)
else:
    # scikit-learn >= 1.6 requires explicit low-level construction
    from sklearn.base import BaseEstimator
    from dataclasses import fields
    
    # Extract default tags from a base estimator to satisfy required dataclass fields
    tags_orig = BaseEstimator().__sklearn_tags__()
    as_dict = {
        field.name: getattr(tags_orig, field.name)
        for field in fields(tags_orig)
    }
    
    tags = TsLearnTags(**as_dict)
    
    assert tags.input_tags.sparse is False
    assert tags.input_tags.three_d_array is True
    assert tags.allow_variable_length is False

print(f"__CHECK__ TsLearnTags {type(tags).__name__}")
```

### LLM Instruction Prompt
`TsLearnTags` is an internal framework utility. Do not instantiate it without arguments in scikit-learn >= 1.6. Check if it is an alias for `dict` (scikit-learn < 1.6). If not, extract the required dataclass fields from `sklearn.base.BaseEstimator().__sklearn_tags__()` using `dataclasses.fields` and pass them as `**kwargs`.

### Prompt Snippet
`TsLearnTags` is an internal shim. In scikit-learn >= 1.6, it inherits from `sklearn.utils.Tags` (a dataclass) and requires keyword arguments like `estimator_type` and `target_tags`. Extract these from `BaseEstimator().__sklearn_tags__()` via `dataclasses.fields`.

### Common Failure Modes
- **Missing required positional arguments:** `TypeError: Tags.__init__() missing 2 required positional arguments: 'estimator_type' and 'target_tags'`. This occurs when calling `TsLearnTags()` without arguments in scikit-learn >= 1.6.
- **Misunderstanding API Audience:** Attempting to use this internal framework utility as a standard user-facing API. It requires explicit low-level construction and should be excluded from standard user workflows.

### Fix Code Hint
```python
# BAD: Attempting to instantiate without arguments in scikit-learn >= 1.6
# tags = TsLearnTags()

# GOOD: Extracting required fields from a base estimator
from sklearn.base import BaseEstimator
from dataclasses import fields

tags_orig = BaseEstimator().__sklearn_tags__()
as_dict = {field.name: getattr(tags_orig, field.name) for field in fields(tags_orig)}
tags = TsLearnTags(**as_dict)
```