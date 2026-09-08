# Deep-dive: `set_backend`

model: google:gemini-3.1-pro-preview · tokens in=2,794 out=2,429 · wall 20s · 2026-09-08 15:53

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** ADVANCED/LOW-LEVEL. This is an internal state-mutation method on the backend abstraction wrapper, primarily used by library developers or advanced users writing custom backend-agnostic time-series algorithms.
- **Testability:** TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. The method is an instance method on the `Backend` class. It requires explicitly importing and instantiating `Backend` before it can be called.

**L1 PURPOSE**
The `set_backend` method dynamically updates the active computational engine (e.g., NumPy or PyTorch) for an existing `Backend` wrapper instance. It sits at the foundation of `tslearn`'s backend-dispatch system, allowing a single `Backend` object to switch its delegation target on the fly based on a string identifier or the type of a provided data array.

**L2 CONTRACT**
- **Receiver:** An instance of `tslearn.backend.Backend`. Obtained via `from tslearn.backend import Backend; b = Backend()`.
- **Parameters:**
  - `data` (array-like, string, or `None`, default `None`): The indicator for which backend to select. Valid strings include `"numpy"`, `"pytorch"`, or `"torch"`. Alternatively, passing a NumPy array or PyTorch tensor will infer the backend from the object type. Unrecognized inputs or `None` default to the NumPy backend.
- **Return Value:** `None`. The method mutates the receiver in place.
- **Visibility:** Public (though intended for low-level backend management).
- **Thread-Safety:** Not explicitly thread-safe. Mutating the backend of a shared `Backend` instance concurrently with operations relying on `__getattr__` delegation could lead to race conditions.

**L3 MECHANICS**
- When called, `set_backend` delegates to the module-level helper `select_backend(data)` (defined elsewhere in `tslearn.backend.backend.py`).
- It takes the returned backend implementation object (e.g., an instance of `NumPyBackend` or `PyTorchBackend`) and assigns it to `self.backend` (line 88).
- Because the `Backend` class implements `__getattr__` (lines 72-74) to forward missing attribute calls to `self.backend`, updating this attribute instantly changes the computational engine used for all subsequent array operations called on the `Backend` instance.
- It also updates the behavior of the `is_numpy` and `is_pytorch` properties, which rely on `self.backend_string`.

**L4 CORRECT MINIMAL USAGE**
```python
from tslearn.backend import Backend

# 1. Explicit low-level construction of the Backend wrapper
backend_instance = Backend()

# 2. Mutate the backend state explicitly
backend_instance.set_backend("numpy")

# 3. Verify the internal state has been updated
assert backend_instance.is_numpy
assert not backend_instance.is_pytorch

print("__CHECK__ set_backend")
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `cannot import name 'NumPyBackend' from 'tslearn.backend'`
- **Reason for Failure:** The execution harness attempted to import `NumPyBackend` directly from the `tslearn.backend` namespace (`from tslearn.backend import Backend, NumPyBackend`). While `Backend` is exposed there, the specific implementation classes like `NumPyBackend` are either kept in private submodules or not hoisted to the `__init__.py` level. The test suite in the repository likely imports them from their specific internal files (e.g., `tslearn.backend.numpy_backend`), making the public import fail with an `ImportError`.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - I inferred that `select_backend` is a module-level function that returns an instantiated backend implementation object (like `NumPyBackend`), based on its usage in `__init__` and `set_backend`.
  - I inferred that `NumPyBackend` is not exposed in `tslearn.backend.__init__.py` based on the `ImportError` in the failure history.
- **Information needed for certainty:** The exact definition of `select_backend` and the `__init__.py` exports of `tslearn.backend` to confirm the import paths of the backend implementation classes.
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The parameter types, defaults, and return values are explicitly visible in the source and docstring.
  - **L3 (Mechanics):** 9/10. The delegation to `select_backend` and `__getattr__` is clear, though the exact internals of `select_backend` are off-screen.
  - **L4 (Minimal Usage):** 10/10. The provided snippet avoids the problematic imports and relies only on the public `Backend` class and its boolean properties, ensuring deterministic execution.