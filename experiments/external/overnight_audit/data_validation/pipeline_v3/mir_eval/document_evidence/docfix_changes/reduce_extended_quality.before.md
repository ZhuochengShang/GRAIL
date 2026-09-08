## API Test: `reduce_extended_quality`

### Signature
```python
def reduce_extended_quality(quality)
```
_Source: source/mir_eval/chord.py:319_

_Source doc:_ Map an extended chord quality to a simpler one, moving upper voices to a set of scale degree extensions. Parameters ---------- quality : str Extended chord quality to reduce. Returns ------- base_quality : str New chord quality. extensions : set Scale degrees extensions for the quality.

### Goal
Map an extended chord quality string to a simpler base quality, extracting the upper voices into a set of scale degree extensions for standardized chord evaluation.

### Parameters
- `quality`: A string representing the extended chord quality to reduce (e.g., "maj9", "min11").

### Input
A string representing a valid extended chord quality. The input must be the quality portion of the chord only (not including the root note). The quality string must conform to `mir_eval`'s chord regular expressions and be valid within the restricted `chord.QUALITIES` definitions.

### Output
Returns `unspecified` — A two-element tuple `(base_quality, extensions)` where `base_quality` is a `str` representing the simplified chord quality, and `extensions` is a `set` of strings representing the scale degree extensions extracted from the original quality.

### Valid Call Patterns
```python
# Note: Call form inferred from signature and project context (not verified by test suite)
import mir_eval

quality_str = "maj9"
base_quality, extensions = mir_eval.chord.reduce_extended_quality(quality_str)
```

### LLM Instruction Prompt
- When calling `mir_eval.chord.reduce_extended_quality`, pass a single string representing the chord quality (without the root note).
- Expect a tuple of `(str, set)` in return, representing the base quality and the set of scale degree extensions.
- Ensure the input string is a valid chord quality recognized by `mir_eval`'s chord validation regex.

### Prompt Snippet
```text
# Reduce an extended chord quality to its base and extensions
base_quality, extensions = mir_eval.chord.reduce_extended_quality("min11")
```

### Common Failure Modes
- **Passing a full chord string:** Providing "C:maj9" instead of "maj9" will fail or produce incorrect results, as the function expects only the quality portion of the chord.
- **Passing invalid qualities:** Providing a quality string that violates `mir_eval`'s restricted `chord.QUALITIES` or regex validation rules.
- **Type errors:** Passing a non-string type (e.g., `None` or a list) to the `quality` parameter.

### Fix Code Hint
```python
# Incorrect: Passing the full chord string including the root
# base, ext = mir_eval.chord.reduce_extended_quality("G:maj7")

# Correct: Pass only the quality string
chord_label = "G:maj7"
root, quality = chord_label.split(":") # Simplified split for example
base, ext = mir_eval.chord.reduce_extended_quality(quality)
```