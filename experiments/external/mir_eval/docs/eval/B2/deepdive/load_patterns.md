# Deep-dive: `load_patterns`

model: google:gemini-3.1-pro-preview · tokens in=5,964 out=3,404 · wall 31s · 2026-09-08 01:30

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is USER-FACING. It is a public I/O utility designed to be called directly by users to load pattern data from disk into the specific nested list structure required by `mir_eval.pattern` evaluation metrics. 

Standalone testability: TESTABLE FROM PUBLIC INPUTS. The function requires a file path as input. While the exact path to a checked-in fixture is not reliably known in the harness (as evidenced by the failure history), the function can be tested by creating a temporary file with deterministic MIREX 2013 formatted text and passing its path.

L1 PURPOSE
`load_patterns` is an I/O function that reads a text file formatted according to the MIREX 2013 "Discovery of Repeated Themes & Sections" specification and parses it into a deeply nested Python list. It sits at the very beginning of the pattern evaluation data flow, converting on-disk annotations into the in-memory data structure required by `mir_eval.pattern.evaluate()`.

L2 CONTRACT
- **Receiver**: None (module-level function).
- **Parameters**:
  - `filename` (`str` or `os.PathLike`): The path to the input text file containing the patterns. The file must strictly follow the MIREX 2013 format (lines containing "pattern", "occurrence", or comma-separated float pairs).
- **Returns**:
  - `pattern_list` (`list`): A three-level nested list of patterns. The structure is `list[list[list[tuple[float, float]]]]`. The outer list contains patterns, the middle list contains occurrences of that pattern, and the inner list contains `(onset_time, midi_number)` tuples representing the notes in that occurrence.
- **Visibility**: Public.
- **Thread-safety/laziness**: The function is eager; it reads the entire file into memory at once (`input_file.readlines()`). It is thread-safe provided the underlying file is not being concurrently modified by another thread or process.

L3 MECHANICS
- The function initializes three empty lists: `pattern_list`, `pattern`, and `occurrence`.
- It opens the file using an internal `_open(filename, mode="r")` helper (source/mir_eval/io.py:380) and reads all lines.
- It iterates through each line:
  - If the line contains the substring `"pattern"` (source/mir_eval/io.py:382), it flushes the current `occurrence` into `pattern` (if not empty), flushes the current `pattern` into `pattern_list` (if not empty), and resets both `occurrence` and `pattern` to empty lists.
  - If the line contains the substring `"occurrence"` (source/mir_eval/io.py:390), it flushes the current `occurrence` into `pattern` (if not empty) and resets `occurrence` to an empty list.
  - Otherwise, it assumes the line is a data row, splits it by `","` (source/mir_eval/io.py:395), parses the first two elements as `float`, and appends the resulting `(onset, midi)` tuple to the current `occurrence`.
- After the loop finishes, it flushes any remaining `occurrence` and `pattern` into the final `pattern_list` (source/mir_eval/io.py:400-403).
- **Failure conditions**: Raises `FileNotFoundError` (or similar I/O error from `_open`) if the file does not exist. Raises `ValueError` or `IndexError` if a data line cannot be split by a comma into at least two elements that parse as floats.

L4 CORRECT MINIMAL USAGE
```python
import tempfile
import os
import mir_eval

# Create a deterministic temporary file adhering to the MIREX 2013 format
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    f.write("pattern 1\n")
    f.write("occurrence 1\n")
    f.write("0.5,67.0\n")
    f.write("1.0,67.0\n")
    f.write("occurrence 2\n")
    f.write("4.5,65.0\n")
    f.write("5.0,65.0\n")
    temp_path = f.name

try:
    # Load the patterns using the API
    patterns = mir_eval.io.load_patterns(temp_path)
    
    # Verify the nested structure: 1 pattern, 2 occurrences, 2 notes per occurrence
    assert len(patterns) == 1
    assert len(patterns[0]) == 2
    assert patterns[0][0][0] == (0.5, 67.0)
finally:
    # Clean up the temporary file
    os.remove(temp_path)
```

L5 FAILURE FORENSICS
- **`FileNotFoundError`**: The user attempted to dynamically construct a path to a checked-in test fixture (`reference.txt`) by navigating relative directories from a `beat_reference_file` variable. This resulted in an absolute path (`/Users/clockorangezoe/.../reference.txt`) that did not exist in the execution harness environment. The failure occurred at `source/mir_eval/io.py:380` when `_open(filename, mode="r")` attempted to access the non-existent file.
- **`round 0: rewrite fabricated members: remove`**: The user likely submitted an incomplete code snippet or attempted to use fabricated variables (like `beat_reference_file` without defining it), causing the harness's static analysis or execution to reject the attempt before it even reached the API call.

L6 SELF-ASSESSMENT
- **Inferences**: I inferred that `_open` is a thin wrapper around Python's built-in `open` (or `io.open`) that accepts standard file paths and modes, and raises standard I/O exceptions like `FileNotFoundError`.
- **Needed for certainty**: The exact implementation of `_open` from `mir_eval.io` to confirm it doesn't have unexpected side effects or require specific path types.
- **Confidence scores**:
  - L2 (Contract): 10/10. The docstring explicitly details the exact nested list structure and the types of the tuples.
  - L3 (Mechanics): 10/10. The entire source code of the function is provided, making the parsing logic completely transparent.
  - L4 (Usage): 9/10. The usage is correct and standard for testing I/O functions, though it relies on `tempfile` to satisfy the requirement of deterministic inputs without knowing the exact path to a checked-in fixture.