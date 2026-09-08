# Deep-dive: `first_n_three_layer_P`

model: google:gemini-3.1-pro-preview · tokens in=5,247 out=3,947 · wall 37s · 2026-09-08 01:24

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience**: USER-FACING. This is a standard evaluation metric function for pattern discovery, explicitly documented with examples and exported as part of the public API.
- **Testability**: TESTABLE FROM PUBLIC INPUTS. The function can be tested by creating standard pattern text files and loading them via `mir_eval.io.load_patterns()` to produce the required in-memory list structures, as demonstrated in the official documentation.

L1 PURPOSE
The `first_n_three_layer_P` function computes the three-layer precision metric restricted to the first *n* estimated musical patterns. It sits at the end of the pattern discovery evaluation data flow, comparing a subset of estimated patterns against a full set of reference (ground truth) patterns. This specific metric formulation is standard in the Music Information Retrieval Evaluation eXchange (MIREX) pattern discovery task.

L2 CONTRACT
- **Receiver**: None (standalone module-level function).
- **Parameters**:
  - `reference_patterns` (list): The reference (ground truth) patterns, strictly in the in-memory format returned by `mir_eval.io.load_patterns()`.
  - `estimated_patterns` (list): The estimated patterns, in the same format.
  - `n` (int, default=5): The maximum number of patterns to consider from the estimated results, evaluated in the order they appear in the list.
- **Returns**: 
  - `precision` (float): The first *n* three-layer precision score. *(Note: If either input contains zero patterns, the function currently returns a tuple of three floats `(0.0, 0.0, 0.0)` instead of a single float, which violates its documented return type).*
- **Visibility**: Public.
- **Thread-safety/laziness**: Synchronous and thread-safe (pure function with no shared mutable state).

L3 MECHANICS
1. The function first delegates to `validate(reference_patterns, estimated_patterns)` (line 540) to ensure the inputs are well-formed.
2. It checks if either input is empty using `_n_onset_midi(...) == 0`. If true, it short-circuits and returns `0.0, 0.0, 0.0` (lines 542-543).
3. It slices the `estimated_patterns` list to retain only the first `n` elements: `estimated_patterns[: min(len(estimated_patterns), n)]` (line 546).
4. It delegates the actual metric computation to `three_layer_FPR(reference_patterns, fn_est_patterns)`, which returns a tuple of F-measure, Precision, and Recall (line 549).
5. It discards the F-measure and Recall, returning only the Precision `P` (line 551).

L4 CORRECT MINIMAL USAGE
```python
import mir_eval
import tempfile
import os

# Create temporary files to generate the required in-memory list structures
with tempfile.TemporaryDirectory() as tmpdir:
    ref_path = os.path.join(tmpdir, "ref_pattern.txt")
    est_path = os.path.join(tmpdir, "est_pattern.txt")
    
    # Write minimal valid pattern data
    pattern_data = "pattern 1\n0.5, 1.5\n2.5, 3.5\n"
    with open(ref_path, "w") as f:
        f.write(pattern_data)
    with open(est_path, "w") as f:
        f.write(pattern_data)
        
    # Load patterns using the required I/O helper
    ref_patterns = mir_eval.io.load_patterns(ref_path)
    est_patterns = mir_eval.io.load_patterns(est_path)
    
    # Compute the first n three-layer precision
    precision = mir_eval.pattern.first_n_three_layer_P(
        ref_patterns, 
        est_patterns, 
        n=5
    )
    print(f"Precision: {precision}")
```

L5 FAILURE FORENSICS
- **Attempt 1**: `FileNotFoundError: [Errno 2] No such file or directory: '.../ref_pattern.txt'`
  - **Why it failed**: The execution harness attempted to write the reference file to a specific `output_dir` using `os.path.join(output_dir, "ref_pattern.txt")`. However, when subsequently calling `mir_eval.io.load_patterns()`, the code likely passed the bare string `"ref_pattern.txt"` (copied verbatim from the docstring example) instead of the `ref_file` variable that contained the absolute path. Consequently, the I/O function looked for the file in the current working directory, where it did not exist.

L6 SELF-ASSESSMENT
- **Inferences**: 
  - I inferred the exact string format required for the pattern text files (`"pattern 1\n0.5, 1.5\n..."`) based on the partial snippet in the failure history, as the internal structure of `mir_eval.io.load_patterns()` is not provided in the context.
  - I inferred that the cut-off code in the failure history (`est_file = os.`) was followed by a hardcoded call to `load_patterns("ref_pattern.txt")`, which explains the specific `FileNotFoundError` path mismatch.
- **Information needed for certainty**: The source code for `mir_eval.io.load_patterns()` to confirm the exact expected text file syntax and the resulting in-memory Python list structure.
- **Confidence Scores**:
  - **L2 (Contract)**: 9/10. The parameters and types are explicitly documented, though I deducted one point because the function's return type is inconsistent (returns a float normally, but a tuple of three floats on empty inputs).
  - **L3 (Mechanics)**: 10/10. The logic is entirely contained within the provided source snippet (lines 540-551) and is straightforward to trace.
  - **L4 (Minimal Usage)**: 9/10. The usage is correct according to the documentation, but relies on standard file I/O to bypass the unknown internal list structure.