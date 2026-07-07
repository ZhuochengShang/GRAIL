# VectorCanvas

_The `addGeometry` function adds a specified geometry to the canvas, potentially modifying the existing geometries to ensure the canvas remains manageable._

**Receiver:** instance — obtain a `VectorCanvas` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `addGeometry` **(primary)**, ⚠️ `createRingsForOccupiedPixels`, ⚠️ `findIntersections`

---

## API Test: `addGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def addGeometry(geometry: Geometry, title: String): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:169_

_Source doc:_ Adds the given geometry to the canvas. This method might simplify, drop, or combine geometries to accommodate the given geometry without getting too big. @param geometry the geometry to add @param title an optional title to attach to the geometry in the SVG file @return `true` if the state of the canvas was modified.

### Goal
The `addGeometry` function adds a specified geometry to the canvas, potentially modifying the existing geometries to ensure the canvas remains manageable.

### Parameters
- `geometry` (`Geometry`): The geometry object to be added to the canvas. This can represent various geometric shapes such as points, lines, or polygons.
- `title` (`String`): An optional title that can be attached to the geometry for identification purposes in the SVG file. It can be `null` if no title is needed.

### Input
The caller must provide a valid `Geometry` object and an optional `String` for the title. The geometry should be compatible with the canvas's existing geometries, and the canvas must be initialized properly before calling this method.

### Output
Returns `Boolean` — `true` if the state of the canvas was modified by the addition of the geometry, indicating that the geometry was successfully added or combined with existing geometries.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
```

### LLM Instruction Prompt
- Ensure that the `geometry` provided is a valid instance of the `Geometry` class and that the canvas is properly initialized. The `title` can be `null` if no title is required.

### Prompt Snippet
```text
Add a geometry to the canvas using the `addGeometry` method, ensuring the geometry is valid and the canvas is initialized.
```

### Common Failure Modes
- **[compile]** error: object GeometryReader is not a member of package edu.ucr.cs.bdlab.beast.io

### Fix Code Hint
```scala
Ensure the canvas is initialized and that the geometry being added is appropriate for the current state of the canvas. If necessary, check the geometry's type and size before calling `addGeometry`.
```

## API Test: `createRingsForOccupiedPixels`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[davinci] def createRingsForOccupiedPixels: Array[LinearRing]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:671_

_Source doc:_ Creates one linear ring for each contiguous part of occupied pixels. A pixel is connected to the four pixels to its west, east, north, and south. The linear ring is returned in image space based on the pixel location. Think of the corners of pixels as points in space that are connected with orthogonal lines to form the linear rings. @return

### Goal
The `createRingsForOccupiedPixels` function generates linear rings that outline contiguous areas of occupied pixels in a raster dataset, facilitating further geospatial analysis.

### Parameters
_None._

### Input
The function operates on a raster dataset that has been previously defined and contains occupied pixels. The raster must be structured such that pixels are connected in a grid format, allowing for identification of contiguous occupied areas.

### Output
Returns `Array[LinearRing]` — an array of linear rings, where each ring represents the boundary of a contiguous area of occupied pixels in image space.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 3, 0, 3), 3, 3, 0, 5)
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 1)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(1, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(1, 1)), null)
val rings = canvas.createRingsForOccupiedPixels
```

### LLM Instruction Prompt
- When calling `createRingsForOccupiedPixels`, ensure that the raster data has been properly initialized and that occupied pixels are defined in the context of the `VectorCanvas` instance.

### Prompt Snippet
```text
To create linear rings for occupied pixels, first ensure that the raster data is set up correctly in a VectorCanvas instance, then call the createRingsForOccupiedPixels method.
```

### Common Failure Modes
- **[compile]** error: method createRingsForOccupiedPixels in class VectorCanvas cannot be accessed in edu.ucr.cs.bdlab.davinci.VectorCanvas _(seen 2x)_
- **[compile]** error: not found: value factory
- **[compile]** error: object RasterRDD is not a member of package org.apache.spark.rdd

### Fix Code Hint
```scala
Ensure that the raster data is correctly populated with occupied pixels before calling createRingsForOccupiedPixels. Check the connectivity of the occupied pixels to ensure they form contiguous areas.
```

## API Test: `findIntersections`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[davinci] def findIntersections(_x1: Double, _y1: Double, _x2: Double, _y2: Double, intersections: mutable.ArrayBuffer[(Int, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:313_

_Source doc:_ Find all intersections between the given line segment and the horizontal scan line centers @param x1 @param y1 @param x2 @param y2 @param intersections all computed intersections will be appended to this list

### Goal
`findIntersections` computes the intersection points between a specified line segment and horizontal scan lines, appending the results to a provided collection.

### Parameters
- `_x1` (`Double`): The x-coordinate of the starting point of the line segment.
- `_y1` (`Double`): The y-coordinate of the starting point of the line segment.
- `_x2` (`Double`): The x-coordinate of the ending point of the line segment.
- `_y2` (`Double`): The y-coordinate of the ending point of the line segment.
- `intersections` (`mutable.ArrayBuffer[(Int, Int)]`): A mutable collection that will store the computed intersection points as tuples of integer coordinates.

### Input
The caller must provide valid double values for the coordinates of the line segment and a mutable array buffer to store the intersection results. The line segment is defined by its two endpoints, and the intersections will be calculated against horizontal lines at integer y-coordinates.

### Output
Returns `Unit` — this indicates that the function does not return a value but modifies the `intersections` parameter in place by appending the computed intersection points.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 5, 0, 5), 5, 5, 0, 5)
val intersections = new mutable.ArrayBuffer[(Int, Int)]()
canvas.findIntersections(0, 0, 3, 4, intersections)
```

### LLM Instruction Prompt
- Ensure that the coordinates provided for the line segment are valid double values and that the `intersections` parameter is a mutable array buffer ready to store results.

### Prompt Snippet
```text
Call `findIntersections` with the coordinates of the line segment and a mutable array buffer to collect intersection points.
```

### Common Failure Modes
- **[compile]** error: method findIntersections in class VectorCanvas cannot be accessed in edu.ucr.cs.bdlab.davinci.VectorCanvas _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the intersections array buffer is initialized before calling the function
val intersections = new mutable.ArrayBuffer[(Int, Int)]()
```
