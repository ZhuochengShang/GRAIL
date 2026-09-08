# Deep-dive: `load_tempo`

model: google:gemini-3.1-pro-preview · tokens in=4,593 out=3,154 · wall 27s · 2026-09-08 01:37

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. This is a public I/O utility function designed to load standard MIREX-format tempo annotations from disk into the in-memory formats required by `mir_eval`'s evaluation metrics.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function requires a valid file path containing specific delimited text. This can be easily tested by creating a temporary file with the required contents using Python's standard library before invoking the function.

**L1 PURPOSE**
The `load_tempo` API reads a single-line text file containing tempo annotations in MIREX format and parses it into a NumPy array of two tempo estimates (in beats-per-minute) and a float representing the relative confidence/weight of the first estimate. It sits at the ingestion boundary of the library, converting on-disk ground truth or system predictions into the exact data structures required by `mir_eval.tempo.evaluate`.

**L2 CONTRACT**
- **Receiver:** None (module-level function in `mir_eval.io`).
- **Parameters:**
  - `filename` (`str` or `os.PathLike`): The path to the annotation file to be loaded.
  - `delimiter` (`str`, default `r"\s+"`): A regular expression string used to split the values on the line. Defaults to any amount of whitespace.
  - `comment` (`str` or `None`, default `"#"`): A regular expression string indicating a comment. Any lines starting with this pattern are ignored. Setting to `None` disables comment filtering.
- **Returns:** A two-element tuple `(tempi, weight)`:
  - `tempi` (`np.ndarray`): A 1D NumPy array containing exactly two non-negative tempo estimates (e.g., `[t1, t2]`).
  - `weight` (`float`): A value in the range `[0.0, 1.0]` representing the relative importance of `tempi[0]` compared to `tempi[1]`.
- **Visibility:** Public.
- **Thread-safety/Laziness:** Eagerly reads the file into memory. Thread-safe assuming the underlying file is not being concurrently modified.

**L3 MECHANICS**
1. **Delegation:** Calls the internal/universal `load_delimited` function (line 572) with the provided `filename`, `delimiter`, and `comment`, specifying the expected column types as `[float, float, float]`.
2. **Extraction:** Extracts the scalar `weight` from the returned column array (`weight = weight[0]`) and combines the two tempo columns into a single 1D NumPy array using `np.concatenate([t1, t2])` (lines 576-577).
3. **Validation (Length):** Checks if `len(t1) != 1`. If the file contains more or fewer than one data line, it raises a `ValueError("Tempo file should contain only one line.")` (line 579).
4. **Validation (Tempi):** Delegates to `tempo.validate_tempi(tempi)` (line 584). If this validation fails (raises a `ValueError`), the error is caught and downgraded to a warning via `warnings.warn(error.args[0])` (lines 585-586).
5. **Validation (Weight):** Checks if `0 <= weight <= 1`. If not, it raises a `ValueError(f"Invalid weight: {weight}")` (line 588).
6. **Return:** Yields the validated `tempi` array and `weight` float.

**L4 CORRECT MINIMAL USAGE**
```python
import mir_eval
import numpy as np
import tempfile
import os

# Create a deterministic tempo annotation file
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.lab') as f:
    f.write("# This is a comment line\n")
    f.write("60.0 120.0 0.5\n")
    temp_filepath = f.name

try:
    # Load the tempo data
    tempi, weight = mir_eval.io.load_tempo(temp_filepath)
    
    # Verify the outputs
    assert np.allclose(tempi, [60.0, 120.0])
    assert weight == 0.5
finally:
    # Clean up the temporary file
    os.remove(temp_filepath)
```

**L5 FAILURE FORENSICS**
- **`[fail/runtime] FileNotFoundError`**: The attempted code tried to write a test file to `os.path.join(output_dir, "test_tempo.txt")`. This failed at the `open(tempo_file, "w")` step because `output_dir` was either undefined or pointed to a directory that did not exist in the execution environment. When opening a file in `"w"` mode, Python requires the parent directory to already exist; otherwise, it raises a `FileNotFoundError`.
- **`[fail/doc-repair] round 0: rewrite fabricated members: remove`**: The agent likely hallucinated a non-existent function or failed to provide a complete, executable snippet in the previous round, triggering a structural rejection by the harness.

**L6 SELF-ASSESSMENT**
- **INFERENCES:** 
  - I inferred that `load_delimited` returns a tuple of 1D NumPy arrays (or lists that behave like them) based on the usage `weight = weight[0]` and `np.concatenate([t1, t2])`.
  - I inferred that `tempo.validate_tempi` exists in the `mir_eval.tempo` module and raises a `ValueError` for invalid tempi (e.g., negative values), based on the `try/except` block at line 583.
- **INFORMATION NEEDED FOR CERTAINTY:** The exact implementation of `load_delimited` and `tempo.validate_tempi` to confirm their return types and specific validation rules.
- **CONFIDENCE SCORES:**
  - **L2 (Contract): 10/10** - The docstring and source code explicitly define the inputs, outputs, and their expected types/ranges.
  - **L3 (Mechanics): 10/10** - The provided source code for `load_tempo` is complete and the logic is linear and unambiguous.
  - **L4 (Minimal Usage): 10/10** - The usage snippet relies only on standard Python libraries for file I/O and correctly matches the real call site provided in the context.