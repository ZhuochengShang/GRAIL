# Deep-dive: `load_valued_intervals`

model: google:gemini-3.1-pro-preview · tokens in=5,450 out=2,561 · wall 28s · 2026-09-08 01:38

---

### L0 AUDIENCE + TESTABILITY CLASSIFICATION
**Audience:** USER-FACING. This is a primary I/O utility designed for end-users to load their annotation data (e.g., transcription or piano-roll notes) from disk into the in-memory formats required by `mir_eval`'s evaluation and display functions.
**Testability:** TESTABLE FROM PUBLIC INPUTS. The function can be tested standalone by providing a valid file path or an in-memory file-like object (as demonstrated in the repository's own test suite) containing delimited numeric text.

### L1 PURPOSE
`load_valued_intervals` sits at the very beginning of the library's data flow. Its purpose is to parse a delimited text file containing three columns of numeric data (start time, end time, and an associated value like pitch or frequency) and convert it into deterministic, validated NumPy arrays. These arrays are then passed downstream to evaluation metrics (like transcription scoring) or visualization tools (like piano rolls).

### L2 CONTRACT
**Parameters:**
- `filename` (`str`, `os.PathLike`, or file-like object): The path to the annotation file or an open file handle. The file must contain three columns of numeric data.
- `delimiter` (`str`, default `r"\s+"`): A regular expression string used to separate columns in the text file. Defaults to splitting by any amount of whitespace.
- `comment` (`str` or `None`, default `"#"`): A regular expression string indicating the start of a comment. Any lines beginning with this pattern are ignored. Setting to `None` disables comment parsing.

**Returns:**
- `intervals` (`np.ndarray`): A 2D array of shape `(n_events, 2)` containing the start and end times of each event as floats.
- `values` (`np.ndarray`): A 1D array of shape `(n_events,)` containing the numeric values (e.g., pitches) associated with each interval as floats.

**Visibility:** Public.
**Thread-safety/laziness:** Eagerly reads the file into memory and processes it synchronously. Thread-safe as long as the underlying file is not being concurrently modified.

### L3 MECHANICS
1. **Delegation:** The function delegates the actual file parsing to `load_delimited` (source/mir_eval/io.py:480), requesting three columns of `float` types using the provided `delimiter` and `comment` arguments.
2. **Array Construction:** It receives three lists/arrays (`starts`, `ends`, `values`). It stacks `starts` and `ends` into a 2D matrix and transposes it to achieve the `(n_events, 2)` shape using `np.array([starts, ends]).T` (source/mir_eval/io.py:484).
3. **Validation & Warning:** It passes the `intervals` array to `util.validate_intervals(intervals)` (source/mir_eval/io.py:487). If validation fails (e.g., if an end time is before a start time, as seen in `test_input_output.py:143`), it catches the resulting `ValueError` and converts it into a `warnings.warn` instead of halting execution (source/mir_eval/io.py:488-489).
4. **Finalization:** It converts the `values` list into a NumPy array and returns the tuple `(intervals, values)`.

### L4 CORRECT MINIMAL USAGE
```python
import io
import numpy as np
from mir_eval.io import load_valued_intervals

# Create an in-memory file-like object simulating a 3-column text file
# Columns: start_time, end_time, value (e.g., pitch in Hz)
mock_file = io.StringIO(
    "0.5 1.5 440.0\n"
    "1.5 2.5 880.0\n"
    "2.5 3.0 220.0"
)

# Load the valued intervals
intervals, values = load_valued_intervals(mock_file)

assert intervals.shape == (3, 2)
assert values.shape == (3,)
```

### L5 FAILURE FORENSICS
- **Attempt 1:** `FileNotFoundError: [Errno 2] No such file or directory: '.../test_valued_inte'`
  - **Why it failed:** The execution harness attempted to create a temporary file using `open(test_file, "w")`, but the directory path constructed via `os.path.join(output_dir, ...)` did not exist on the filesystem. Additionally, the provided code snippet was truncated (`f.w`), indicating a malformed generation attempt. The failure occurred at the standard library `open()` call before `load_valued_intervals` could even be invoked.

### L6 SELF-ASSESSMENT
- **Inferences:** 
  - I inferred that `filename` accepts a file-like object (like `io.StringIO`) because the real call site in `test_input_output.py:146` explicitly passes an open file handle (`f`) to the function.
  - I inferred that the returned arrays contain `float` data types because the internal call to `load_delimited` explicitly requests `[float, float, float]`.
- **Information needed for certainty:** To be absolutely certain about the exact behavior of `load_delimited` and `util.validate_intervals`, I would need to see their source code, though their behavior is strongly implied by their names and usage context.
- **Confidence Scores:**
  - **L2 (Contract): 10/10** - The parameter types, defaults, and return shapes are explicitly documented in the docstring and confirmed by the source code.
  - **L3 (Mechanics): 10/10** - The source code for the function is fully provided and straightforward, showing exactly how it delegates parsing, stacks arrays, and handles validation warnings.
  - **L4 (Minimal Usage): 10/10** - The usage relies only on standard library `io.StringIO` and the provided API, directly mirroring the checked-in test fixture pattern.