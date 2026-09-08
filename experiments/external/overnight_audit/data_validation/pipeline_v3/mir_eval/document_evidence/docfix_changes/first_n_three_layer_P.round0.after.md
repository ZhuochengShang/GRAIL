## API Test: `first_n_three_layer_P`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def first_n_three_layer_P(reference_patterns, estimated_patterns, n=5)
```

### Goal
Computes the three-layer precision metric restricted to the first *n* estimated musical patterns, commonly used in MIREX pattern discovery evaluation.

### Parameters
- `reference_patterns` (list): The reference (ground truth) patterns, strictly in the in-memory format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns` (list): The estimated patterns, in the same format.
- `n` (int, default=5): The maximum number of patterns to consider from the estimated results, evaluated in the order they appear in the list.

### Input
The caller must provide reference and estimated patterns as parsed Python lists, not raw file paths. These lists must be loaded from repository-format text files using `mir_eval.io.load_patterns()`. When creating mock text files for testing, you must use Python's standard `tempfile.TemporaryDirectory()` to guarantee a valid, writable path. Do not assume the existence of an `output_dir` or any pre-existing writable directory in the test environment.

### Output
Returns a `float` representing the first *n* three-layer precision score. 
*Note: If either input contains zero patterns, the function short-circuits and returns a tuple of three floats `(0.0, 0.0, 0.0)` instead of a single float.*

### Valid Call Patterns
```python
import tempfile
import os
import mir_eval

with tempfile.TemporaryDirectory() as tmpdir:
    ref_file = os.path.join(tmpdir, "ref_pattern.txt")
    est_file = os.path.join(tmpdir, "est_pattern.txt")
    
    # Write minimal valid pattern data
    with open(ref_file, "w") as f:
        f.write("pattern 1\n0.5, 1.5\n2.5, 3.5\npattern 2\n4.5, 5.5\n6.5, 7.5\n")
        
    with open(est_file, "w") as f:
        f.write("pattern 1\n0.5, 1.5\n2.5, 3.5\n")
        
    # Load patterns using the required I/O helper
    ref_patterns = mir_eval.io.load_patterns(ref_file)
    est_patterns = mir_eval.io.load_patterns(est_file)
    
    # Compute the first n three-layer precision
    precision = mir_eval.pattern.first_n_three_layer_P(
        ref_patterns, 
        est_patterns, 
        n=5
    )
```

### LLM Instruction Prompt
When evaluating pattern discovery using `first_n_three_layer_P`, you MUST first parse the text files into lists using `mir_eval.io.load_patterns()`. When creating mock text files to pass to the I/O loader, always use Python's standard `tempfile.TemporaryDirectory()` to guarantee a valid, writable path. Do not assume the existence of an `output_dir` or write to the current working directory.

### Prompt Snippet
```text
mir_eval.pattern.first_n_three_layer_P requires lists of patterns loaded via `mir_eval.io.load_patterns()`. To avoid FileNotFoundError in tests, write mock pattern text files exclusively within a `tempfile.TemporaryDirectory()`.
```

### Common Failure Modes
- **Environment Assumption (FileNotFoundError)**: Attempting to write mock text files to an undefined `output_dir` or a bare string filename (e.g., `"ref_pattern.txt"`) in the current working directory, which fails during `open(..., "w")` or subsequent loading.
- **Passing file paths instead of lists**: Providing string file paths directly to `first_n_three_layer_P` will cause a failure, as the function expects the in-memory list structures returned by the I/O module.
- **Unexpected Tuple Return**: Expecting a float when passing empty pattern lists; the function returns `(0.0, 0.0, 0.0)` if either input has zero patterns.

### Fix Code Hint
```python
# BAD: Assuming output_dir exists or writing to current directory
# ref_file = "ref_pattern.txt"
# with open(ref_file, "w") as f: ...

# GOOD: Using tempfile to guarantee a writable directory
import tempfile
import os
import mir_eval

with tempfile.TemporaryDirectory() as tmpdir:
    ref_file = os.path.join(tmpdir, "ref_pattern.txt")
    est_file = os.path.join(tmpdir, "est_pattern.txt")
    
    with open(ref_file, "w") as f:
        f.write("pattern 1\n0.5, 1.5\n")
    with open(est_file, "w") as f:
        f.write("pattern 1\n0.5, 1.5\n")
        
    ref_patterns = mir_eval.io.load_patterns(ref_file)
    est_patterns = mir_eval.io.load_patterns(est_file)
    p = mir_eval.pattern.first_n_three_layer_P(ref_patterns, est_patterns, n=5)
```