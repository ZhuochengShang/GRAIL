# Deep-dive: `load_ragged_time_series`

model: google:gemini-3.1-pro-preview · tokens in=4,994 out=2,729 · wall 33s · 2026-09-08 01:34

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. This is a public I/O utility designed for end-users to load their custom annotation files (e.g., multipitch or variable-length event data) into the format expected by `mir_eval` evaluation functions.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function only requires a valid file path (or file-like object, depending on `_open`'s implementation) containing delimited text data, which can be easily generated using Python's standard `tempfile` module.

**L1 PURPOSE**
The `load_ragged_time_series` API is used to parse delimited text files where the first column represents a timestamp and the subsequent columns represent an arbitrary, variable number of values associated with that timestamp. It sits at the very beginning of the library's data flow, converting raw on-disk annotations (like multipitch ground truth or system outputs) into the in-memory data structures (a 1D numpy array of times and a list of 1D numpy arrays of values) required by evaluation metrics.

**L2 CONTRACT**
- **`filename`**: `str` or `os.PathLike`. The path to the annotation file to be loaded.
- **`dtype`**: `function` or type (default: `float`). The data type used to cast the parsed values in columns 1 through $n$.
- **`delimiter`**: `str` (default: `r"\s+"`). A regular expression string used to split each line into columns.
- **`header`**: `bool` (default: `False`). If `True`, the function skips the first row of the file.
- **`comment`**: `str` or `None` (default: `"#"`). A regular expression pattern. Any line starting with this pattern is ignored. If `None`, comment parsing is disabled.
- **Returns**: A tuple `(times, values)` where:
  - `times`: A 1D `np.ndarray` of `float` timestamps.
  - `values`: A Python `list` of 1D `np.ndarray`s, where each array contains the values for the corresponding timestamp, cast to `dtype`. If a timestamp has no values, the corresponding array is empty.

**L3 MECHANICS**
1. Initializes empty lists `times` and `values`.
2. Compiles the `delimiter` into a regex object (`splitter`).
3. If `comment` is not `None`, compiles a regex object (`commenter`) that matches the start of a line (`^{comment}`).
4. Determines the starting row index (`start_row`) for enumeration: `1` if `header` is `True`, else `0`.
5. Opens the file using an internal `_open` helper (line 660).
6. Iterates over the file line by line. If a line matches the `commenter`, it is skipped.
7. Strips whitespace from the line and splits it using the `splitter` regex.
8. Attempts to cast the first element (`data[0]`) to a `float`. If this fails (raising `TypeError` or `ValueError`), it catches the exception and raises a detailed `ValueError` indicating the exact file, row, line, and failed value (lines 671-676).
9. Attempts to cast the remaining elements (`data[1:]`) to a numpy array of type `dtype`. If this fails, it similarly raises a detailed `ValueError` (lines 684-689).
10. Appends the parsed time and values to their respective lists, and finally returns `np.array(times)` and the `values` list.

**L4 CORRECT MINIMAL USAGE**
```python
import tempfile
import os
import numpy as np
from mir_eval.io import load_ragged_time_series

# Create a temporary file with ragged time-series data
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    # Format: timestamp val1 val2 ...
    f.write("0.5 440.0\n")
    f.write("1.0 440.0 554.37\n") # Ragged: two values here
    f.write("1.5\n")              # Ragged: zero values here
    filename = f.name

try:
    # Load the data using default whitespace delimiter
    times, values = load_ragged_time_series(filename, dtype=float)
    
    assert isinstance(times, np.ndarray)
    assert isinstance(values, list)
    assert len(values[1]) == 2
finally:
    os.remove(filename)
```

**L5 FAILURE FORENSICS**
- **Failed Attempt:** `ValueError: Couldn't convert value timestamp using float found at ...`
  - **Why it failed:** The user created a CSV file with a header row (`"timestamp,f0_1,f0_2,f0_3\n"`) but called `load_ragged_time_series` without specifying `header=True` (and likely without specifying `delimiter=','`, though the snippet cuts off). Because `header` defaults to `False`, the function attempted to parse the first row. It split the line (or failed to split it if using the default `\s+` delimiter) and tried to cast the string `"timestamp"` (or `"timestamp,f0_1,f0_2,f0_3"`) to a `float` at line 669 (`converted_time = float(data[0])`). This raised a `ValueError`, which was caught and re-raised with the detailed error message at line 671.

**L6 SELF-ASSESSMENT**
- **Inferences:** I inferred that the internal `_open` function (used at line 660) acts as a standard context manager that yields lines from the file, which is standard practice for such wrappers in Python.
- **Information needed for certainty:** The exact implementation of `_open` to confirm if it handles file-like objects in addition to string paths, though the documentation explicitly states `str` or `os.Pathlike`.
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The types, defaults, and return structures are explicitly defined in the source code and docstring.
  - **L3 (Mechanics):** 10/10. The entire function body is provided, making the step-by-step execution completely transparent.
  - **L4 (Minimal Usage):** 10/10. The usage relies only on standard library file I/O and the provided function signature, which is straightforward to mock.