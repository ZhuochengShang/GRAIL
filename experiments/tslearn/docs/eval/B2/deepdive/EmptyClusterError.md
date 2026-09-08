# Deep-dive: `EmptyClusterError`

model: google:gemini-3.1-pro-preview · tokens in=5,263 out=1,769 · wall 15s · 2026-09-08 14:34

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
USER-FACING. This is a public exception class that users of `tslearn`'s clustering algorithms (such as `TimeSeriesKMeans`) may need to catch when a clustering iteration fails due to an empty cluster.
TESTABLE FROM PUBLIC INPUTS. The exception can be directly imported, instantiated, and raised without any complex setup.

**L1 PURPOSE**
`EmptyClusterError` is a custom exception used within `tslearn`'s clustering module to signal that a cluster has lost all of its assigned time-series samples during an algorithm's execution. It sits in the error-handling flow, allowing algorithms to abort gracefully and users to catch the specific failure mode (often caused by setting `n_clusters` too high or poor initialization) to trigger fallback strategies.

**L2 CONTRACT**
*   **Constructor**: `EmptyClusterError(message="")`
*   **Parameters**: 
    *   `message` (str, optional): A custom string providing additional context about the error. Defaults to `""`.
*   **Return value**: An instance of `EmptyClusterError`, which inherits from Python's built-in `Exception`.
*   **Visibility**: Public.

**L3 MECHANICS**
The class inherits from `Exception`. 
*   In `__init__` (tslearn/tslearn/clustering/utils.py:18), it calls `super().__init__()` and stores the provided `message` in `self.message`.
*   In `__str__` (tslearn/tslearn/clustering/utils.py:22), it overrides the default string representation. If `self.message` is not empty, it formats a suffix as `" (<message>)"`. It then returns the hardcoded prefix `"Cluster assignments lead to at least one empty cluster"` concatenated with the suffix.
*   It is raised internally by helpers like `_check_no_empty_cluster` (tslearn/tslearn/clustering/utils.py:37) and directly in algorithms like `KernelKMeans` (tslearn/tslearn/clustering/kmeans.py:399).

**L4 CORRECT MINIMAL USAGE**
```python
from tslearn.clustering.utils import EmptyClusterError

def test_empty_cluster_error():
    # 1. Instantiate with no message
    err_empty = EmptyClusterError()
    assert str(err_empty) == "Cluster assignments lead to at least one empty cluster"
    
    # 2. Instantiate with a custom message
    custom_msg = "try smaller n_cluster"
    err_msg = EmptyClusterError(custom_msg)
    expected_str = f"Cluster assignments lead to at least one empty cluster ({custom_msg})"
    assert str(err_msg) == expected_str
    
    # 3. Verify it can be raised and caught as an Exception
    try:
        raise err_msg
    except EmptyClusterError as e:
        assert isinstance(e, Exception)
        print(f"Successfully caught: {e}")

test_empty_cluster_error()
```

**L5 FAILURE FORENSICS**
The recorded failed attempt:
```python
        try:
            raise EmptyClusterError("Test empty cluster")
        except EmptyClusterError as e:
            assert isinstance(e, Exception), "EmptyClusterError should inherit from Exception"
            assert str(e) == "Test empt...
```
This failed with an `AssertionError` because the author assumed `str(e)` would exactly equal the passed message (`"Test empty cluster"`). However, looking at `tslearn/tslearn/clustering/utils.py:22-28`, the `__str__` method explicitly prepends a hardcoded string. The actual value of `str(e)` in the failed test was `"Cluster assignments lead to at least one empty cluster (Test empty cluster)"`.

**L6 SELF-ASSESSMENT**
*   **Inferences**: None. The behavior, inheritance, and string formatting are entirely visible in the provided source code.
*   **Missing Information**: None. The provided context contains the complete definition of the class.
*   **Confidence Scores**:
    *   L2 (Contract): 10/10. The signature and types are explicitly defined in the source.
    *   L3 (Mechanics): 10/10. The logic for `__init__` and `__str__` is trivial and fully visible.
    *   L4 (Usage): 10/10. The snippet correctly exercises the class and accounts for the custom `__str__` implementation that caused previous failures.