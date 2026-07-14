## API Test: `splitGeometryAcrossDateLine`

### Signature
```scala
def splitGeometryAcrossDateLine(geometry: Geometry): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/GeometryQuadSplitter.scala:122_

_Source doc:_ Splits the given geometry across the dateline (-180 or +180 meridian) to avoid errors. 1. This function assumes that the input consists of a polygon with a single ring (outer shell). 1. We assume that the width cannot be greater than 180 degrees. 1. If the geometry width is greater than 180, we assume that it crosses the dateline. 1. To fix the geometry, we rotate all negative longitudes by adding 360. 1. After that, we split the geometry by intersecting it with the western hemisphere once and with the easter hemisphere once. @param geometry the input geometry to detect and split @return Either the same geometry if it does not cross the dateline, or the same one split into two if it crosses the dateline.

### Goal
Split a polygon geometry that crosses the ±180° dateline into valid hemisphere-local pieces to avoid downstream geometric/topological errors.

### Parameters
- `geometry` (`Geometry`): Input geometry to inspect for dateline crossing and split if needed.

### Input
- In-memory JTS `Geometry` (not a file path argument).
- Documented preconditions from source doc:
  - Assumes a **polygon with a single ring (outer shell)**.
  - Assumes polygon width should not exceed **180 degrees** unless interpreted as dateline crossing.
  - If width > 180°, the method treats it as crossing the dateline and applies longitude rotation (+360 for negative longitudes) before splitting against hemispheres.
- No additional CRS conversion behavior is documented for this method; use geometries already in a longitude/latitude frame consistent with dateline logic.

### Output
Returns `Geometry` — either:
- the same geometry (if it does not cross the dateline), or
- a split geometry composed of two parts (west/east side) when dateline crossing is detected.

### Valid Call Patterns
```scala
val geometry = GeometryReader.DefaultGeometryFactory.createPolygon(
  Array(new Coordinate(170, 50), new Coordinate(-170, 60), new Coordinate(-170, 50), new Coordinate(170, 50))
)
val split = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)
assertResult(2)(split.getNumGeometries)
assertResult(9)(split.getNumPoints)
```

### LLM Instruction Prompt
- Call with the static/object receiver exactly as validated in tests: `GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)`.
- Provide a `Geometry` argument only; do not add extra parameters.
- Use this API for dateline handling of polygon-like input before operations that are sensitive to wraparound.
- Respect documented assumptions (single-ring polygon, width-based crossing logic); if data violates assumptions, state that behavior is not guaranteed by docs.

### Prompt Snippet
```text
Given a JTS Geometry polygon that may cross ±180°, call GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry) and use the returned Geometry (unchanged or split) for subsequent processing. Do not pass file paths or additional arguments.
```

### Common Failure Modes
- Passing geometries that do not meet the documented assumption (not a single-ring polygon outer shell); result is not specified by provided docs.
- Using coordinates not compatible with dateline longitude semantics (the function logic is explicitly based on -180/+180 and longitude rotation).
- Assuming it always returns two geometries; it may return the original geometry unchanged when no crossing is detected.

### Fix Code Hint
```scala
// Ensure you pass a Geometry and call the tested receiver form
val split: Geometry = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)

// Optional sanity check in your pipeline:
if (split.getNumGeometries > 1) {
  // geometry was split across dateline
}
```