# Deep-dive: `reduce_extended_quality`

model: google:gemini-3.1-pro-preview · tokens in=4,930 out=2,228 · wall 21s · 2026-09-08 01:52

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as INTERNAL/FRAMEWORK. While it lacks a private underscore prefix, it is a highly specific string-mapping utility designed to be consumed by the higher-level `mir_eval.chord.split` function (as seen at `source/mir_eval/chord.py:430`) during chord label parsing. It should likely be excluded from a main user-facing benchmark denominator. 

The API is TESTABLE FROM PUBLIC INPUTS. It is a pure, module-level function that takes a standard Python string and returns a tuple of standard Python types, requiring no complex setup or object instantiation.

L1 PURPOSE
`reduce_extended_quality` is a normalization utility within the chord evaluation data flow. Its purpose is to map complex, extended chord qualities (like "maj9" or "13") into a simpler base quality (like "maj7" or "7") alongside a set of explicit scale degree extensions (like `{"9"}` or `{"9", "11", "13"}`). This reduction allows downstream evaluation metrics to compare chords with differing levels of extension detail on a more standardized, structural basis.

L2 CONTRACT
*   **Receiver**: None (module-level function).
*   **Parameters**:
    *   `quality` (`str`): The string representation of an extended chord quality (e.g., `"maj9"`, `"min11"`). It should not include the chord root or bass.
*   **Returns**: A two-element `tuple` containing:
    *   `base_quality` (`str`): The simplified chord quality.
    *   `extensions` (`set` of `str`): The scale degree extensions extracted from the original quality.
*   **Visibility**: Public module-level function.
*   **Thread-safety/Laziness**: Thread-safe and eager. It is a pure function that performs a dictionary lookup on a static, module-level constant.

L3 MECHANICS
The function operates entirely by querying the `EXTENDED_QUALITY_REDUX` dictionary defined at `source/mir_eval/chord.py:302`. 
1. It calls `.get(quality, (quality, set()))` on this dictionary (line 336).
2. If the `quality` string exists in the dictionary (e.g., `"maj9"`), it returns the predefined tuple (e.g., `("maj7", {"9"})`).
3. If the `quality` string is not found in the dictionary (e.g., `"maj"`, `"dim"`, or an invalid string), it defaults to returning the original `quality` string unmodified, paired with an empty `set()`.
4. It does not perform any validation on the input string and will not raise any exceptions.

L4 CORRECT MINIMAL USAGE
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

L5 FAILURE FORENSICS
*   **Failed Attempt**: `AssertionError: Expected base quality 'maj', got maj7`
*   **Why it failed**: The test author assumed that `"maj9"` would be reduced all the way down to a triad base quality (`"maj"`) with both the 7th and 9th extracted as extensions (`{"7", "9"}`). However, looking at the `EXTENDED_QUALITY_REDUX` dictionary at `source/mir_eval/chord.py:304`, `"maj9"` is explicitly mapped to `("maj7", {"9"})`. The function preserves the 7th as part of the base quality rather than stripping it out into the extensions set.

L6 SELF-ASSESSMENT
*   **Inferences**: None. All claims are directly traceable to the provided source code, specifically the `EXTENDED_QUALITY_REDUX` dictionary and the function definition.
*   **Information needed for certainty**: None. The function is entirely self-contained within the provided context.
*   **Confidence Scores**:
    *   L2 (Contract): 10/10. The parameter and return types are explicitly documented in the docstring and verified by the `return` statement.
    *   L3 (Mechanics): 10/10. The function is a single line of code performing a dictionary lookup.
    *   L4 (Usage): 10/10. The usage snippet directly exercises the dictionary lookup and correctly asserts the exact values defined in the source code.