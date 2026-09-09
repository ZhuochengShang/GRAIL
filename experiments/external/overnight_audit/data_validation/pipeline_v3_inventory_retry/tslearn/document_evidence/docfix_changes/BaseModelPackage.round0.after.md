## API Test: `BaseModelPackage`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class BaseModelPackage(object)
```

### Goal
INTERNAL/FRAMEWORK abstract base class (mixin) used internally by `tslearn` estimators to standardize model packaging and serialization. It bridges scikit-learn's estimator API with disk-persistence formats by automatically extracting hyperparameters and fitted model state. This is an advanced/internal API and should be excluded from standard user-facing workflows.

### Parameters
_None._ (Inherits from `object`).

### Input
TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. You must create a subclass of `BaseModelPackage`. The subclass must:
1. Implement the abstract method `_is_fitted()`.
2. Provide a `get_params()` method (typically by inheriting from `sklearn.base.BaseEstimator`), as `_to_dict()` relies on it to extract hyperparameters.
3. Store fitted model parameters in instance attributes ending with a single trailing underscore (`_`), which are automatically extracted by `_get_model_params()`.

### Output
An instance of the subclass capable of aggregating its hyperparameters and fitted state into a dictionary via the internal `_to_dict()` method.

### Valid Call Patterns
```python
from tslearn.bases import BaseModelPackage

# 1. Define a subclass that fulfills the framework contract
class DummyEstimator(BaseModelPackage):
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        
    def get_params(self, deep=True):
        # Required by BaseModelPackage._to_dict()
        return {"alpha": self.alpha}
        
    def _is_fitted(self):
        # Required abstract method
        return hasattr(self, "coef_")

# 2. Instantiate the subclass
model = DummyEstimator(alpha=2.0)

# 3. Simulate fitting by setting an attribute with a trailing underscore
model.coef_ = [1, 2, 3]

# 4. Exercise the packaging logic
pkg_dict = model._to_dict()

# 5. Verify the contract
assert pkg_dict["hyper_params"]["alpha"] == 2.0
assert pkg_dict["model_params"]["coef_"] == [1, 2, 3]
print("__CHECK__ BaseModelPackage successfully packaged dummy estimator.")
```

### LLM Instruction Prompt
`BaseModelPackage` is an internal framework mixin. Do not instantiate it directly. To test it, define a subclass that implements `_is_fitted()` and `get_params()`. Instantiate your subclass, assign a mock fitted attribute ending with an underscore (e.g., `self.coef_`), and call `_to_dict()` to verify that hyperparameters and fitted state are correctly extracted.

### Prompt Snippet
```text
`BaseModelPackage` is an internal abstract base class. Test it via explicit low-level construction: subclass it, implement `_is_fitted()` and `get_params()`, set a trailing-underscore attribute, and call `_to_dict()`.
```

### Common Failure Modes
- **Direct Instantiation (The Previous Failure):** Instantiating the base class directly (`model = BaseModelPackage()`). Because Python 3 ignores the legacy `__metaclass__ = ABCMeta` syntax, this technically executes without error. However, calling `model._to_dict()` immediately crashes with an `AttributeError` because the base class lacks the `get_params()` method expected from a scikit-learn estimator.
- **Missing `get_params()` in Subclass:** Failing to define `get_params()` in the subclass causes `_to_dict()` to crash when extracting `hyper_params`.
- **Missing Trailing Underscores:** Naming fitted attributes without a trailing underscore (e.g., `self.coef` instead of `self.coef_`), causing `_get_model_params()` to silently ignore them.

### Fix Code Hint
```python
# WRONG: Direct instantiation crashes on method call
# model = BaseModelPackage()
# pkg = model._to_dict() # AttributeError: 'BaseModelPackage' object has no attribute 'get_params'

# RIGHT: Subclass and implement required scikit-learn and tslearn interfaces
class MyEstimator(BaseModelPackage):
    def get_params(self, deep=True): return {}
    def _is_fitted(self): return True

model = MyEstimator()
model.learned_state_ = [1, 2]
pkg = model._to_dict()
```