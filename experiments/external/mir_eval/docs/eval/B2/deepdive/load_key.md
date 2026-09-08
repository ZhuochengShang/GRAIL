# Deep-dive: `load_key`

model: google:gemini-3.1-pro-preview · tokens in=4,887 out=2,925 · wall 28s · 2026-09-08 01:28

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. This is a public I/O utility designed for end-users to load key annotations from disk into memory for evaluation.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The function can be tested standalone by providing a path to a properly formatted text file (which can be created dynamically in a temporary directory).

**L1 PURPOSE**
The `load_key` function reads a musical key annotation from a text file and formats it into a standardized string representation. It sits at the very beginning of the `mir_eval` key evaluation data flow, converting repository-format text files into the in-memory string format (e.g., `"C major"`) required by evaluation metrics like `mir_eval.key.weighted_score`.

**L2 CONTRACT**
- **Receiver:** None (module-level function).
- **Parameters:**
  - `filename` (`str` or `os.PathLike`): The path to the annotation file to be loaded.
  - `delimiter` (`str`, default `r"\s+"`): A regular expression string used to separate columns in the text file. By default, it splits on any amount of whitespace.
  - `comment` (`str` or `None`, default `"#"`): A regular expression string indicating the start of a comment. Lines beginning with this pattern are ignored. Setting this to `None` disables comment filtering.
- **Returns:**
  - `key_string` (`str`): The parsed key label, formatted as `"{scale} {mode}"` (e.g., `"C major"`).
- **Visibility:** Public.
- **Thread-safety/Laziness:** Eagerly reads the file into memory. Thread-safe as long as the underlying file is not being concurrently modified.

**L3 MECHANICS**
1. **Delegation:** Calls the internal/universal helper `load_delimited(filename, [str, str], delimiter=delimiter, comment=comment)` (source: `mir_eval/io.py:525`) to parse the file into two lists of strings: `scale` and `mode`.
2. **Validation (Length):** Checks if exactly one line/event was parsed (`len(scale) != 1`). If not, it raises a `ValueError("Key file should contain only one line.")`.
3. **Formatting:** Extracts the first element from both `scale` and `mode` and concatenates them with a single space: `key_string = f"{scale} {mode}"`.
4. **Validation (Domain):** Passes the resulting string to `key.validate_key(key_string)` (source: `mir_eval/io.py:535`).
5. **Warning on Invalid Key:** If `validate_key` raises a `ValueError` (e.g., if the key is not a recognized musical key), the error is caught and emitted as a `UserWarning` via `warnings.warn(error.args[0])`, rather than halting execution.
6. **Return:** Returns the formatted `key_string`.

**L4 CORRECT MINIMAL USAGE**
```python
import tempfile
import os
import mir_eval

# Create a temporary file with a valid key annotation
# The file must contain exactly two columns: scale degree and mode
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("# This is a comment\n")
    f.write("C major\n")
    temp_path = f.name

try:
    # Load the key using the default whitespace delimiter
    key_string = mir_eval.io.load_key(temp_path)
    print(f"Loaded key: '{key_string}'")
finally:
    # Clean up the temporary file
    os.remove(temp_path)
```

**L5 FAILURE FORENSICS**
- **Attempt 1 (`FileNotFoundError: [Errno 2] No such file or directory`)**:
  The test attempted to write to `os.path.join(output_dir, "test_key.txt")`. The failure occurred on the line `with open(key_file, "w") as f:` because the parent directory (`output_dir`) did not exist in the execution environment. 
  *Secondary logical error:* Even if the file had been written, the test wrote `"C:maj\n"`. Because the default `delimiter` is `r"\s+"`, `load_delimited` expects two distinct whitespace-separated columns (one for scale, one for mode). `"C:maj"` is a single string without whitespace, which would have caused `load_delimited` to fail or return malformed data. The correct file content should have been `"C maj"` or `"C major"`.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - I inferred that `load_delimited` with `[str, str]` strictly expects two columns per line, based on the docstring stating "The file should consist of two string columns".
  - I inferred that `"C major"` is a valid key string that will pass `key.validate_key` without a warning, based on standard music theory and typical MIR conventions.
- **Information needed for certainty:** The exact implementation of `load_delimited` and `key.validate_key` to know exactly how malformed lines (like `"C:maj"`) are handled (whether they raise an error inside `load_delimited` or just return empty arrays).
- **Confidence Scores:**
  - **L2 (Contract):** 10/10. The signature, docstring, and return types are explicitly defined in the provided source.
  - **L3 (Mechanics):** 10/10. The source code for `load_key` is fully provided and linearly readable.
  - **L4 (Minimal Usage):** 9/10. The usage is correct and handles file I/O safely, though the exact string that avoids a warning depends on the unseen `validate_key` function.