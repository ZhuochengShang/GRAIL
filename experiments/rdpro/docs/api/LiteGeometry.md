# LiteGeometry

_Calculates the area of a geometric shape represented in the raster data._

**Receiver:** instance — obtain a `LiteGeometry` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `area` **(primary)**, ⚠️ `isCW`, ⚠️ `part`

---

## API Test: `area`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def area: Double
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115_

### Goal
Calculates the area of a geometric shape represented in the raster data.

### Parameters
_None._

### Input
The caller must provide a geometric shape that has been defined within the context of the raster data. This shape should be part of a valid raster dataset that has been loaded and processed using RDPro.

### Output
Returns `Double` — the area of the geometric shape in the same units as the coordinate system of the raster data.

### Valid Call Patterns
```scala
val areaValue: Double = value.area
```

### LLM Instruction Prompt
- Ensure that the geometric shape is defined and part of the raster data context before calling `area`.

### Prompt Snippet
```text
Calculate the area of the geometric shape using the area method.
```

### Common Failure Modes
- **[compile]** error: value area is not a member of edu.ucr.cs.bdlab.beast.geolite.IFeature _(seen 2x)_
- **[compile]** error: value area is not a member of org.locationtech.jts.geom.Geometry _(seen 2x)_

### Fix Code Hint
```scala
// Ensure the geometric shape is part of a valid raster dataset before calling area
val areaValue: Double = value.area
```

## API Test: `isCW`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def isCW: Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:97_

_Source doc:_ Checks whether this list of points form a closed ring stored in CW order @return `true` if the points form a ring and the ring is stored in clock-wise order

### Goal
Determines if a given set of points forms a closed ring in a clockwise order, which is essential for correctly interpreting geometric shapes in geospatial analysis.

### Parameters
_None._

### Input
The method operates on an internal representation of a geometric shape, specifically a list of points that define a polygon. The precondition is that the points must form a closed ring.

### Output
Returns `Boolean` — `true` if the points form a closed ring and are ordered in a clockwise direction; otherwise, it returns `false`.

### Valid Call Patterns
```scala
val isClockwise: Boolean = polygon.isCW
```

### LLM Instruction Prompt
- Ensure that the polygon object has been properly initialized and contains a valid closed ring of points before calling `isCW`.

### Prompt Snippet
```text
Check if the polygon's outer shell is in clockwise order using the isCW method.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the polygon is properly defined and closed before calling isCW
if (polygon.isClosed) {
    val isClockwise: Boolean = polygon.isCW
} else {
    throw new IllegalArgumentException("The polygon must be closed to check its orientation.")
}
```

## API Test: `part`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def part(i: Int): LiteList
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146_

### Goal
The `part` function retrieves a specific part of a geometric object, returning it as a `LiteList`.

### Parameters
- `i` (`Int`): The index of the part to retrieve. Expected values are non-negative integers corresponding to the part's position within the geometric structure.

### Input
The caller must provide a valid index `i` that corresponds to an existing part of the geometric object. The geometric object must be instantiated and accessible in the context where `part` is called.

### Output
Returns `LiteList` — a lightweight representation of the specified part of the geometric object, which can be used for further processing or analysis.

### Valid Call Patterns
```scala
val partList = geometry.part(0) // Assuming 'geometry' is an instance of a class that has the 'part' method
```

### LLM Instruction Prompt
- Ensure that the index `i` is within the bounds of the available parts in the geometric object. Handle cases where the index may be out of range.

### Prompt Snippet
```text
Call the `part` method on a geometric object with a valid index to retrieve a specific part as a LiteList.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 3x)_
- **[compile]** error: value part is not a member of edu.ucr.cs.bdlab.beast.geolite.IFeature

### Fix Code Hint
```scala
if (i < 0 || i >= geometry.numParts) {
  throw new IllegalArgumentException("Index out of bounds for the number of parts.")
}
```
