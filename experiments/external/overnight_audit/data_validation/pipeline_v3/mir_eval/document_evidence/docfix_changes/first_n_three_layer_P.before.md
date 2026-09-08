## API Test: `first_n_three_layer_P`

### Signature
```python
def first_n_three_layer_P(reference_patterns, estimated_patterns, n=5)
```
_Source: source/mir_eval/pattern.py:509_

_Source doc:_ First n three-layer precision. This metric is basically the same as the three-layer FPR but it is only applied to the first n estimated patterns, and it only returns the precision. In MIREX and typically, n = 5. Examples -------- >>> ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt") >>> est_patterns = mir_eval.io.load_patterns("est_pattern.txt") >>> P = mir_eval.pattern.first_n_three_layer_P(ref_patterns, ...                                            est_patterns, n=5) Parameters ---------- reference_patterns : list The reference patterns in the format returned by :func:`mir_eval.io.load_patterns()` estimated_patterns : list The estimated patterns in the same format n : int Number of patterns to consider from the estimated results, in the order they appear in the matrix (Default value = 5) Returns ------- precision : float The first n three-layer Precision

### Goal
Computes the three-layer precision metric restricted to the first *n* estimated musical patterns, commonly used in MIREX pattern discovery evaluation.

### Parameters
- `reference_patterns`: A list of reference (ground truth) patterns in the format returned by `mir_eval.io.load_patterns()`.
- `estimated_patterns`: A list of estimated patterns in the same format as the reference patterns.
- `n`, default `5`: An integer specifying the number of patterns to consider from the estimated results, evaluated in the order they appear.

### Input
The caller must provide reference and estimated patterns as parsed Python lists, not raw file paths. These lists must be loaded from repository-format text files using `mir_eval.io.load_patterns()`. 

### Output
Returns `unspecified` — A float representing the first *n* three-layer precision score.

### Valid Call Patterns
```python
import mir_eval

# Example derived from the authoritative source documentation
ref_patterns = mir_eval.io.load_patterns("ref_pattern.txt")
est_patterns = mir_eval.io.load_patterns("est_pattern.txt")

precision = mir_eval.pattern.first_n_three_layer_P(
    ref_patterns, 
    est_patterns, 
    n=5
)
```

### LLM Instruction Prompt
- When evaluating pattern discovery using `first_n_three_layer_P`, you MUST first parse the text files into lists using `mir_eval.io.load_patterns()`. Do not pass file paths directly to the metric function. Leave `n=5` unless a different threshold is explicitly requested, as 5 is the MIREX standard.

### Prompt Snippet
```text
mir_eval.pattern.first_n_three_layer_P requires lists of patterns, not file paths. Parse your text files with `mir_eval.io.load_patterns(filepath)` before passing them to the metric.
```

### Common Failure Modes
- **Passing file paths instead of lists**: Providing string file paths directly to `first_n_three_layer_P` will cause a failure, as the function expects the in-memory list structures returned by the I/O module.
- **Incorrect pattern format**: Manually constructing the pattern lists incorrectly instead of relying on `mir_eval.io.load_patterns()` to guarantee the expected internal format.

### Fix Code Hint
```python
# BAD: Passing file paths directly
# p = mir_eval.pattern.first_n_three_layer_P("ref.txt", "est.txt")

# GOOD: Loading patterns first
ref_patterns = mir_eval.io.load_patterns("ref.txt")
est_patterns = mir_eval.io.load_patterns("est.txt")
p = mir_eval.pattern.first_n_three_layer_P(ref_patterns, est_patterns, n=5)
```