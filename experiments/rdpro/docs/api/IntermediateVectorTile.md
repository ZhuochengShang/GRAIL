# IntermediateVectorTile

_The `rasterizeGeometry` function plots a given geometry onto the raster's blocked pixels, allowing for the visualization of vector geometries in a raster…_

**Receiver:** instance — obtain a `IntermediateVectorTile` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `rasterizeGeometry` **(primary)**, ⚠️ `simplifyGeometry`, ⚠️ `trimLineSegment`

---

## API Test: `rasterizeGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[davinci] def rasterizeGeometry(geometry: Geometry): Boolean
private def rasterizeGeometry(geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:220  (+1 more definition site/overload)_

_Source doc:_ Plot the given geometry to the blocked pixels @param geometry the geometry to plot. The geometry should already be in the image space. @return `true` if the pixels changed as a result of this step. Not 100% accurate, though.

### Goal
The `rasterizeGeometry` function plots a given geometry onto the raster's blocked pixels, allowing for the visualization of vector geometries in a raster format.

### Parameters
- `geometry` (`Geometry`): The geometry to plot, which should already be transformed into the image space. This can include various geometric shapes such as points, lines, or polygons.

### Input
The input must be a valid `Geometry` object that is already in the image space. The geometry should be compatible with the raster's coordinate system and resolution.

### Output
Returns `Boolean` — `true` if the raster pixels were modified as a result of the rasterization process, indicating that the geometry has successfully altered the raster representation.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.rasterizeGeometry(factory.createGeometryCollection(Array(factory.createLineString(), factory.createPoint(new CoordinateXY(0, 0)))))
```

### LLM Instruction Prompt
- Ensure that the `geometry` parameter is a valid `Geometry` object in the correct image space before calling `rasterizeGeometry`. 

### Prompt Snippet
```text
Call `rasterizeGeometry` with a valid `Geometry` object that is already in the image space to plot the geometry onto the raster.
```

### Common Failure Modes
- **[compile]** error: method rasterizeGeometry in class VectorCanvas cannot be accessed in edu.ucr.cs.bdlab.davinci.VectorCanvas _(seen 2x)_
- **[compile]** error: Missing closing brace `}' assumed here
- **[compile]** error: object GeometryReader is not a member of package edu.ucr.cs.bdlab.beast.io

### Fix Code Hint
```scala
// Ensure the geometry is properly transformed to the image space before calling rasterizeGeometry
val transformedGeometry = transformToImageSpace(originalGeometry)
canvas.rasterizeGeometry(transformedGeometry)
```

## API Test: `simplifyGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[davinci] def simplifyGeometry(geometry: Geometry): LiteGeometry
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:207_

_Source doc:_ Takes a geometry that is already projected to the image space of this tile and returns a simplified lite geometry that satisfies the following: - If the geometry does not overlap with the tile boundaries, null is returned - Coordinates are snapped to the nearest integer - Parts of the geometry that are outside the tile boundaries can be simplified without affecting the portion that is within the tile boundaries. - If there are consecutive coordinates that snap to the same pixel, only one can be kept @param geometry the input geometry @return the simplified geometry or null if empty

### Goal
The `simplifyGeometry` function simplifies a given geometry by reducing its complexity while ensuring it remains within the boundaries of the associated raster tile.

### Parameters
- `geometry` (`Geometry`): The input geometry that is already projected to the image space of the tile. This can include points, lines, or polygons.

### Input
The caller must provide a `Geometry` object that is projected to the image space of the tile. The geometry must overlap with the tile boundaries; otherwise, the function will return null.

### Output
Returns `LiteGeometry` — a simplified version of the input geometry that has been adjusted to fit within the tile boundaries. If the input geometry does not overlap with the tile, null is returned.

### Valid Call Patterns
```scala
val interTile = new IntermediateVectorTile(10, 0)
val point = GeometryReader.DefaultGeometryFactory.createPoint(new Coordinate(5, 5))
val simplifiedPoint = interTile.simplifyGeometry(point)
```

### LLM Instruction Prompt
- Ensure that the input geometry is projected to the image space of the tile and overlaps with the tile boundaries before calling `simplifyGeometry`.

### Prompt Snippet
```text
Call `simplifyGeometry` with a projected geometry that overlaps the tile boundaries to obtain a simplified lite geometry.
```

### Common Failure Modes
- **[no-correctness-check]** ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ simplifyGeometry " + <witness>). _(seen 4x)_

### Fix Code Hint
```scala
if (geometry.overlaps(tileBoundary)) {
    val simplified = interTile.simplifyGeometry(geometry)
} else {
    // Handle the case where geometry does not overlap
}
```

## API Test: `trimLineSegment`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[davinci] def trimLineSegment(x1: Double, y1: Double, x2: Double, y2: Double): (Double, Double, Double, Double)
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:146_

_Source doc:_ Trim a line segment with the boundaries of this tile, i.e., the box (-buffer, -buffer, resolution + buffer, resolution + buffer) @param x1 the x-coordinate of the first point @param y1 the y-coordinate of the first point @param x2 the x-coordinate of the second point @param y2 the y-coordinate of the second point @return the given line segment trimmed to the tile boundaries or null if the line segment is completely outside

### Goal
The `trimLineSegment` function trims a line segment to fit within the boundaries of a specified tile in a geospatial raster context.

### Parameters
- `x1` (`Double`): The x-coordinate of the first endpoint of the line segment.
- `y1` (`Double`): The y-coordinate of the first endpoint of the line segment.
- `x2` (`Double`): The x-coordinate of the second endpoint of the line segment.
- `y2` (`Double`): The y-coordinate of the second endpoint of the line segment.

### Input
The caller must provide four `Double` values representing the coordinates of the two endpoints of the line segment. The line segment should be defined in relation to the tile boundaries.

### Output
Returns `(Double, Double, Double, Double)` — a tuple containing the trimmed coordinates of the line segment. If the line segment is completely outside the tile boundaries, it returns `null`.

### Valid Call Patterns
```scala
val tile = new IntermediateVectorTile(10, 2)
assertResult((1, 2, 3, 4))(tile.trimLineSegment(1, 2, 3, 4))
assertResult(null)(tile.trimLineSegment(-4, 2, -3, 5))
assertResult((-2, 3, 2, 5))(tile.trimLineSegment(-4, 2, 2, 5))
assertResult((6, 8, 4, 12))(tile.trimLineSegment(6, 8, 3, 14))
```

### LLM Instruction Prompt
When calling `trimLineSegment`, ensure that the coordinates provided are within the expected range of the tile boundaries. The function will return the trimmed coordinates or `null` if the segment is outside.

### Prompt Snippet
```text
Call `trimLineSegment` with the coordinates of the line segment endpoints to get the trimmed segment within the tile boundaries.
```

### Common Failure Modes
- **[compile]** error: method trimLineSegment in class IntermediateVectorTile cannot be accessed in edu.ucr.cs.bdlab.davinci.IntermediateVectorTile _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the coordinates are within the tile boundaries before calling trimLineSegment
val trimmedSegment = tile.trimLineSegment(x1, y1, x2, y2)
if (trimmedSegment == null) {
  println("The line segment is completely outside the tile boundaries.")
}
```
