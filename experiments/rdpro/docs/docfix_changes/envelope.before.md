## API Test: `envelope`

### Signature
```scala
def envelope: java.awt.Rectangle
override def envelope: java.awt.Rectangle
def envelope: Envelope
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:24  (+4 more definition site/overload)_

### Goal
Return the bounding envelope (spatial extent) of the current geometry/raster-related object in model space.

### Parameters
_None._

### Input
Call `envelope` on an existing object instance that defines this method (no direct file-format argument is passed to `envelope` itself).

From the provided sources, a verified call form is:
- `Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)` where `envelope` is an array of four coordinates (`Array(-180.0, 0, 0, 90)`), showing envelope values are used as spatial bounds and may be transformed/restricted to valid CRS extents.

Related project preconditions that matter when envelope values are used in raster workflows:
- If combining rasters (e.g., overlay/join-like operations), metadata compatibility is required (resolution, CRS, tile size). If not compatible, reshape/reproject first.
- CRS consistency is critical before interpreting/combining envelope extents.

### Output
Returns `java.awt.Rectangle` — a rectangular bounding box of the object extent.  
Also documented with `def envelope: Envelope`, i.e., an envelope/bounds object representing raster-data boundaries in model space.

### Valid Call Patterns
```scala
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

### LLM Instruction Prompt
- Use `envelope` as a zero-argument member (`obj.envelope`), not a free function with arguments.
- Do not invent parameters for `envelope`; API facts list none.
- Treat output as a bounds object (`java.awt.Rectangle` or `Envelope` depending on implementing type).
- Before using envelope values across datasets, ensure CRS/metadata compatibility (reshape/reproject when needed).

### Prompt Snippet
```text
Get bounds by calling the instance member with no arguments: `value.envelope`.
Do not pass parameters. Use the returned rectangle/envelope as model-space extent.
If mixing datasets, align CRS/resolution/tile metadata first (reproject/reshape).
```

### Common Failure Modes
- Calling `envelope(...)` with arguments (invalid; method takes no parameters).
- Assuming a single concrete return class everywhere; documented overloads include both `java.awt.Rectangle` and `Envelope`.
- Using envelope extents across mismatched CRS/metadata without prior alignment, causing incorrect spatial results.

### Fix Code Hint
```scala
// Correct: zero-argument instance-style usage pattern
// (replace `value` with the concrete object that provides `envelope`)
val bounds = value.envelope

// If you need CRS-aligned numeric bounds, reproject envelope coordinates explicitly
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```