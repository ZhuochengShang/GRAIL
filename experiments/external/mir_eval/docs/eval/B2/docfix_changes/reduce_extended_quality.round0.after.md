## API Test: `reduce_extended_quality`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
def reduce_extended_quality(quality)
```

### Goal
Map an extended chord quality string to a simpler base quality and a set of upper scale degree extensions. 
*Note: This is an INTERNAL/FRAMEWORK utility designed to be consumed by `mir_eval.chord.split`. It should be excluded from main user-facing benchmark denominators.*

### Parameters
- `quality` (`str`): The string representation of an extended chord quality (e.g., `"maj9"`, `"min11"`). It must not include the chord root or bass.

### Input
A standard Python string representing a chord quality. 
*Note: As an INTERNAL/FRAMEWORK API, it expects pre-parsed quality strings (e.g., `"maj9"`), not full chord labels (e.g., `"C:maj9"`).*

### Output
A two-element `tuple` containing:
- `base_quality` (`str`): The simplified chord quality.
- `extensions` (`set` of `str`): The scale degree extensions extracted from the original quality.
If the quality is not in the predefined reduction dictionary, it returns the original `quality` string unmodified and an empty `set()`.

### Valid Call Patterns
```python
import mir_eval.chord

# Reduce an extended chord quality
base_quality, extensions = mir_eval.chord.reduce_extended_quality("maj9")

assert base_quality == "maj7"
assert extensions == {"9"}

# Unrecognized or non-extended qualities are returned as-is with an empty set
base_quality_unmodified, extensions_empty = mir_eval.chord.reduce_extended_quality("maj")

assert base_quality_unmodified == "maj"
assert extensions_empty == set()
```

### LLM Instruction Prompt
- Use `mir_eval.chord.reduce_extended_quality` to map extended qualities to their 7th chord equivalents (e.g., `"maj9"` maps to `"maj7"` and `{"9"}`), not to triads.
- Pass only the quality string (e.g., `"maj9"`), not the full chord label.
- Expect a tuple of `(str, set)` in return. Unrecognized qualities return the original string and an empty set.

### Prompt Snippet
```python
import mir_eval.chord
base_quality, extensions = mir_eval.chord.reduce_extended_quality("maj9")
```

### Common Failure Modes
- **Misunderstanding reduction depth (The failure that just happened):** Assuming extended chords reduce all the way to triads (e.g., expecting `"maj9"` to yield `"maj"` and `{"7", "9"}`). The function preserves the 7th as part of the base quality, yielding `"maj7"` and `{"9"}`.
- **Passing a full chord string:** Providing `"C:maj9"` instead of `"maj9"`. The function performs a strict dictionary lookup and will return `"C:maj9"` unmodified with an empty set.
- **Misusing an INTERNAL/FRAMEWORK API:** Attempting to use this for general chord parsing instead of the higher-level `mir_eval.chord.split`.

### Fix Code Hint
```python
# Incorrect: Assuming reduction to triad
# base, ext = mir_eval.chord.reduce_extended_quality("maj9")
# assert base == "maj" and ext == {"7", "9"}

# Correct: Reduction maps to 7th chord equivalents
import mir_eval.chord
base, ext = mir_eval.chord.reduce_extended_quality("maj9")
assert base == "maj7" and ext == {"9"}
```