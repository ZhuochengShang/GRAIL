## API Test: `geometryType`

### Signature
```scala
def geometryType: GeometryType
def geometryType: DataType
def geometryType: String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:60  (+2 more definition site/overload)_

_Source doc:_ The most inclusive geometry type for this partition. This can be interpreted as below. - Empty: All geometries are empty - Point: Contains at least one point and zero or more empty geometries - LineString: Contains at least one linestring and zero or more empty geometries - Polygon: Contains at least one polygon and zero or more empty geometries - MultiPoint: Contains at least one multipoint, and zero or more point or empty geometry. - MultiLineString: Contains at least one MultiLineString, and zero or more linestrings and empty geometries. - MultiPolygon: Contains at least one MultiPolygon, and zero or more poylgons and empty geometries. - GeometryCollection: Everything else, i.e., none of the above.

### Goal
Return the most inclusive geometry category present in a `SpatialPartition`, which is useful for understanding mixed vector contents before downstream spatial processing.

### Parameters
_None._

### Input
Call this on an existing `SpatialPartition` value (instance method, no arguments).  
No direct file format is passed to `geometryType`; the partition is typically produced by Beast vector loading/processing workflows.

Preconditions:
- Receiver must be a valid `SpatialPartition` object.
- This API itself has no raster type-parameter selection requirements and no extra compatibility arguments.

### Output
Returns `GeometryType` — the partition-level inclusive geometry classification described by the source doc (`Empty`, `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, `MultiPolygon`, or `GeometryCollection` as catch-all).

### Valid Call Patterns
```scala
// Inferred from signature and sibling SpatialPartition call style in tests
val gt = summary.geometryType
```

### LLM Instruction Prompt
- Use it as a zero-argument instance member on a `SpatialPartition`-like value: `value.geometryType`.
- Do not add parameters.
- Do not assume which overload (`GeometryType` / `DataType` / `String`) is selected unless the expected type context is explicit.
- If receiver type is unknown, ask for/establish a `SpatialPartition` value first.

### Prompt Snippet
```text
Given a SpatialPartition value named `summary`, call `summary.geometryType` (no args) to get the partition’s most inclusive geometry type.
```

### Common Failure Modes
- Calling as a free function (`geometryType`) instead of on an instance.
- Adding nonexistent arguments (e.g., `geometryType(...)`).
- Assuming a specific return type overload without type context.
- Calling it on non-`SpatialPartition` objects.

### Fix Code Hint
```scala
// Correct shape: instance call, no arguments
val gt = summary.geometryType
```