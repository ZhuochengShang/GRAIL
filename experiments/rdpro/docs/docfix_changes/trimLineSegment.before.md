## API Test: `trimLineSegment`

### Signature
```scala
private[davinci] def trimLineSegment(x1: Double, y1: Double, x2: Double, y2: Double): (Double, Double, Double, Double)
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:146_

_Source doc:_ Trim a line segment with the boundaries of this tile, i.e., the box (-buffer, -buffer, resolution + buffer, resolution + buffer) @param x1 the x-coordinate of the first point @param y1 the y-coordinate of the first point @param x2 the x-coordinate of the second point @param y2 the y-coordinate of the second point @return the given line segment trimmed to the tile boundaries or null if the line segment is completely outside

### Goal
`trimLineSegment` trims a line segment to fit within the boundaries of a specified tile in a geospatial raster context.

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
- When calling `trimLineSegment`, ensure that the provided coordinates are within the expected range of the tile boundaries. If the line segment is completely outside, expect a return value of `null`.

### Prompt Snippet
```text
Call `trimLineSegment` with the coordinates of the line segment endpoints to get the trimmed segment within the tile boundaries.
```

### Common Failure Modes
- Providing coordinates that do not correspond to a valid line segment (e.g., both endpoints being the same).
- Expecting a non-null return value when the line segment is completely outside the tile boundaries.

### Fix Code Hint
```scala
// Ensure the coordinates provided are within the expected tile boundaries before calling trimLineSegment.
```