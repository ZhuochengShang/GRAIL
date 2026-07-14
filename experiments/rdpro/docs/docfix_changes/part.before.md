## API Test: `part`

### Signature
```scala
def part(i: Int): LiteList
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146_

### Goal
Return a geometry part (as a `LiteList`) at a given index from a `LiteGeometry` value.

### Parameters
- `i` (`Int`): Zero-based part index to retrieve from the geometry.

### Input
Call this on a `LiteGeometry` instance (instance-style call inferred from sibling methods like `simplifiedLine.numPoints`).

Preconditions:
- `i` should refer to an existing part index for that geometry.
- This method is geometry-internal; no raster file format input (GeoTIFF/HDF) is involved directly in this call.

### Output
Returns `LiteList` — the selected geometry part at index `i`, represented in Beast’s lightweight internal list structure.

### Valid Call Patterns
```scala
// Inferred from signature and sibling instance-call style (no direct test/readme example for `part`)
val p: LiteList = liteGeometry.part(0)
```

### LLM Instruction Prompt
- Use instance form: `value.part(i)` (not bare `part(i)`).
- Pass an `Int` index only.
- Do not invent overloads or extra parameters.
- If part count/bounds are unknown, validate index before calling.

### Prompt Snippet
```text
Given a LiteGeometry value `g`, get the first part with `g.part(0)`.
Use an Int index, and ensure the index is within available parts.
```

### Common Failure Modes
- Using a non-instance call (e.g., `part(0)`) that will not compile.
- Passing a non-`Int` argument.
- Using an out-of-range index for the geometry’s parts (behavior not documented here; may fail at runtime).

### Fix Code Hint
```scala
// Correct: call on a LiteGeometry instance with Int index
val idx: Int = 0
val part0: LiteList = liteGeometry.part(idx)
```