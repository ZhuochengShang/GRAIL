## API Test: `load_valued_intervals`

### Signature
```python
def load_valued_intervals(filename, delimiter='\s+', comment='#')
```
_Source: source/mir_eval/io.py:448_

### Goal
Load time intervals and their associated numerical values (such as transcription note events with start/end times and pitches) from a repository-format text file into deterministic in-memory arrays.

### Parameters
- `filename`: The path to the text file containing the valued intervals. Can be a string file path, an open file descriptor, or a `pathlib.Path` (or `os.PathLike`) object.
- `delimiter`, default `'\s+'`: The string or regular expression used to separate columns in the text file. Defaults to any whitespace.
- `comment`, default `'#'`: The character indicating the start of a comment line. Lines starting with this character will be ignored during parsing.

### Input
A text file where each non-comment line represents an interval and its corresponding value, typically formatted with three columns: `start_time end_time value` (e.g., onset time, offset time, and pitch in Hz). The file must exist, be readable, and contain valid numeric data separated by the specified `delimiter`. 

### Output
Returns `unspecified` — A tuple of two elements, typically unpacked as `(intervals, values)`. `intervals` represents the parsed time boundaries (usually a 2D array of start and end times), and `values` represents the corresponding numerical values for each interval (such as frequencies in Hz).

### Valid Call Patterns
```python
from mir_eval.io import load_valued_intervals
import mir_eval.util

# Load reference and estimated transcription data
ref_t, ref_p = load_valued_intervals("data/transcription/ref04.txt")
est_t, est_p = load_valued_intervals("data/transcription/est04.txt")

# Values (ref_p, est_p) are often frequencies in Hz that can be converted to MIDI
ref_midi = mir_eval.util.hz_to_midi(ref_p)
```

### LLM Instruction Prompt
- When loading transcription or multipitch data containing both time intervals and associated values (like pitch), use `mir_eval.io.load_valued_intervals`.
- Always unpack the return value into exactly two variables: one for the intervals and one for the values (e.g., `intervals, values = load_valued_intervals(...)`).
- If the file uses a specific separator (like commas), explicitly pass the `delimiter` argument (e.g., `delimiter=','`).
- Pass the resulting `intervals` and `values` directly to evaluation metrics or display functions like `mir_eval.display.piano_roll`.

### Prompt Snippet
```text
Use `mir_eval.io.load_valued_intervals(filename)` to parse the transcription text file. Unpack the result into `ref_intervals, ref_pitches`. Convert the pitches to MIDI using `mir_eval.util.hz_to_midi` before passing them to the piano roll display.
```

### Common Failure Modes
- **ValueError (too many/too few values to unpack):** Failing to unpack the result into exactly two variables (e.g., assigning the result to a single variable without indexing, or trying to unpack into three variables).
- **Parsing Errors:** Providing a file that only contains timestamps (events) without a third value column, which will fail to parse as a valued interval. Use `mir_eval.io.load_events` or `mir_eval.io.load_intervals` instead for those formats.
- **Delimiter Mismatch:** Using the default whitespace delimiter (`'\s+'`) on a CSV file, causing the parser to read the entire line as a single string and fail numeric conversion.
- **FileNotFoundError:** Providing a string path to a file that does not exist in the checked-in test fixtures.

### Fix Code Hint
```python
# BAD: Fails to unpack the tuple, causing downstream type errors
data = load_valued_intervals("transcription.txt")
mir_eval.display.piano_roll(data, label="Reference")

# GOOD: Unpack into intervals and values
ref_intervals, ref_pitches = load_valued_intervals("transcription.txt")
mir_eval.display.piano_roll(ref_intervals, ref_pitches, label="Reference")
```