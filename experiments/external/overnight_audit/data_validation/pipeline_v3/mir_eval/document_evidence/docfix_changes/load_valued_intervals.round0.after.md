## API Test: `load_valued_intervals`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def load_valued_intervals(filename, delimiter=r"\s+", comment="#")
```

### Goal
Load time intervals and their associated numerical values (e.g., start/end times and pitches) from a 3-column text file or in-memory file-like object into deterministic NumPy arrays. This is a user-facing I/O utility.

### Parameters
- `filename` (`str`, `os.PathLike`, or file-like object): Path to the annotation file or an open file handle. Accepts in-memory file-like objects such as `io.StringIO`.
- `delimiter` (`str`, default `r"\s+"`): Regular expression string used to separate columns. Defaults to any whitespace.
- `comment` (`str` or `None`, default `"#"`): Regular expression string indicating the start of a comment. Lines starting with this pattern are ignored. `None` disables comments.

### Input
A file or file-like object (e.g., `io.StringIO`) containing three columns of numeric data: start time, end time, and value (e.g., pitch).

### Output
Returns a tuple of two `numpy.ndarray` objects:
- `intervals`: A 2D array of shape `(n_events, 2)` containing start and end times as floats.
- `values`: A 1D array of shape `(n_events,)` containing the numeric values as floats.

### Valid Call Patterns
```python
import io
import numpy as np
from mir_eval.io import load_valued_intervals

# Create an in-memory file-like object simulating a 3-column text file
mock_file = io.StringIO(
    "# start end pitch\n"
    "0.0 1.0 100.0\n"
    "1.0 2.5 200.5\n"
    "3.0 4.0 300.0\n"
)

intervals, values = load_valued_intervals(mock_file)

assert isinstance(intervals, np.ndarray)
assert isinstance(values, np.ndarray)
assert intervals.shape == (3, 2)
assert values.shape == (3,)
```

### LLM Instruction Prompt
- When loading transcription or multipitch data containing both time intervals and associated values, use `mir_eval.io.load_valued_intervals`.
- For testing or dynamic data loading, use `io.StringIO` rather than attempting to write temporary files to the filesystem.
- Do not assume the existence of an `output_dir` or write access to the filesystem in test snippets.
- Always unpack the return value into exactly two variables: `intervals` and `values`.

### Prompt Snippet
```text
Use `mir_eval.io.load_valued_intervals(mock_file)` with an `io.StringIO` object to parse the 3-column transcription text data. Unpack the result into `intervals, values`. Do not write to the filesystem.
```

### Common Failure Modes
- **Environment Assumption / FileNotFoundError:** Attempting to write a test file to an undefined `output_dir` or non-existent directory. Always use `io.StringIO` for in-memory file-like objects instead of writing to the filesystem.
- **ValueError (unpacking):** Failing to unpack the result into exactly two variables (e.g., assigning the result to a single variable without indexing).
- **Validation Warnings:** If an end time is before a start time, `util.validate_intervals` will catch the `ValueError` and convert it into a `warnings.warn` instead of halting execution.

### Fix Code Hint
```python
# BAD: Assumes filesystem write access and an existing output_dir
import os
test_file = os.path.join(output_dir, "test.txt")
with open(test_file, "w") as f:
    f.write("0.0 1.0 100.0\n")
intervals, values = load_valued_intervals(test_file)

# GOOD: Uses in-memory io.StringIO, avoiding filesystem dependencies
import io
mock_file = io.StringIO("0.0 1.0 100.0\n")
intervals, values = load_valued_intervals(mock_file)
```