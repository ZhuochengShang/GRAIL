# GeometryQuadSplitter

_The `splitGeometryAcrossDateLine` function is designed to handle geometries that may cross the dateline, ensuring accurate representation in geospatial…_

**Receiver:** instance — obtain a `GeometryQuadSplitter` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `splitGeometryAcrossDateLine` **(primary)**

---

## API Test: `splitGeometryAcrossDateLine`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def splitGeometryAcrossDateLine(geometry: Geometry): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/GeometryQuadSplitter.scala:122_

_Source doc:_ Splits the given geometry across the dateline (-180 or +180 meridian) to avoid errors. 1. This function assumes that the input consists of a polygon with a single ring (outer shell). 1. We assume that the width cannot be greater than 180 degrees. 1. If the geometry width is greater than 180, we assume that it crosses the dateline. 1. To fix the geometry, we rotate all negative longitudes by adding 360. 1. After that, we split the geometry by intersecting it with the western hemisphere once and with the eastern hemisphere once. @param geometry the input geometry to detect and split @return Either the same geometry if it does not cross the dateline, or the same one split into two if it crosses the dateline.

### Goal
The `splitGeometryAcrossDateLine` function is designed to handle geometries that may cross the dateline, ensuring accurate representation in geospatial analyses.

### Parameters
- `geometry` (`Geometry`): The input geometry, which is expected to be a polygon with a single ring (outer shell).

### Input
The caller must provide a `Geometry` object that represents a polygon. The function assumes that the geometry's width does not exceed 180 degrees. If the geometry crosses the dateline, it will be split accordingly.

### Output
Returns `Geometry` — the output is either the original geometry if it does not cross the dateline, or a new geometry that consists of two separate geometries if it does cross the dateline.

### Valid Call Patterns
```scala
val geometry = GeometryReader.DefaultGeometryFactory.createPolygon(
  Array(new Coordinate(170, 50), new Coordinate(-170, 60), new Coordinate(-170, 50), new Coordinate(170, 50))
)
val split = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)
```

### LLM Instruction Prompt
- When calling `splitGeometryAcrossDateLine`, ensure that the input geometry is a polygon with a single ring and that it adheres to the width constraints regarding the dateline.

### Prompt Snippet
```text
Call `splitGeometryAcrossDateLine` with a valid `Geometry` object representing a polygon to handle cases where the geometry crosses the dateline.
```

### Common Failure Modes
- **[no-correctness-check]** ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ splitGeometryAcrossDateLine " + <witness>).
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: Can only work with geometries in the EPSG:4326 format
- **[compile]** error: object beast is not a member of package org.apache.spark.sql
- **[compile]** error: not found: value spark

### Fix Code Hint
```scala
// Ensure the input geometry is a single-ring polygon and check its width before calling the function.
```
