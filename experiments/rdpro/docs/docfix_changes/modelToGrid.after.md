## API Test: `modelToGrid`
_Grounding: doc-repaired from source (docfix)._

### Goal
Convert a world/model coordinate (e.g., longitude/latitude or projected coordinates) into raster grid (pixel) coordinates using a raster’s metadata transform.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS & TYPES:
// import java.awt.geom.Point2D // Java class
// import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata // Scala class

val metadata: RasterMetadata = rasterRDD.first().rasterMetadata
val pt = new java.awt.geom.Point2D.Double()

// Note: metadata.x1, y1, x2, y2 are GRID (pixel) coordinates, not model coordinates.
// Obtain a valid model coordinate by converting a grid coordinate first:
metadata.gridToModel(metadata.x1.toDouble, metadata.y1.toDouble, pt)
val modelX = pt.x
val modelY = pt.y

// Convert the model coordinate back to grid space:
metadata.modelToGrid(modelX, modelY, pt)
val gridX = pt.x
val gridY = pt.y
```

### LLM Instruction Prompt
- `Point2D.Double` is a Java class from `java.awt.geom.Point2D.Double` and must be instantiated with its fully qualified name or imported.
- Scala 2.11/2.12 does not have `.isFinite` on `Double`; use `!d.isInfinity && !d.isNaN` or `java.lang.Double.isFinite(d)` if checking for finiteness.
- `RasterMetadata` properties `x1`, `y1`, `x2`, `y2` represent grid (pixel) coordinates, not model coordinates. Do not pass them directly as `x` and `y` to `modelToGrid`.
- `RasterMetadata` does not have `rasterWidth` or `rasterHeight` properties; use `x2 - x1` and `y2 - y1` to determine the grid dimensions.
- `modelToGrid` returns `Unit`; read results from the mutated `Point2D.Double` instance.

### Prompt Snippet
```text
To convert model coordinates to grid coordinates, use `metadata.modelToGrid(x, y, pt)` where `pt` is a `java.awt.geom.Point2D.Double`. Remember that `metadata.x1` and `x2` are grid coordinates, not model coordinates. Do not use `.isFinite` on Scala Doubles (use `java.lang.Double.isFinite`). Calculate grid dimensions via `x2 - x1` and `y2 - y1`.
```

### Common Failure Modes
- Calling `.isFinite` on a Scala `Double`, which fails to compile in Scala 2.11/2.12.
- Passing `metadata.x1` or `metadata.x2` directly into `modelToGrid` assuming they are model coordinates (they are grid/pixel bounds).
- Attempting to access `metadata.rasterWidth` or `metadata.rasterHeight` (these properties do not exist; use `x2 - x1` and `y2 - y1`).
- Forgetting to initialize the `Point2D.Double` output parameter, causing a NullPointerException.

### Fix Code Hint
```scala
// WRONG
val width = metadata.rasterWidth
val pt = new java.awt.geom.Point2D.Double()
metadata.modelToGrid(metadata.x1, metadata.y1, pt) // x1/y1 are already grid coords!
if (pt.x.isFinite) { println(pt.x) } // .isFinite fails in Scala 2.11/2.12

// CORRECT
val width = metadata.x2 - metadata.x1
val pt = new java.awt.geom.Point2D.Double()
// Convert grid to model first if you need a valid model coordinate from bounds
metadata.gridToModel(metadata.x1.toDouble, metadata.y1.toDouble, pt)
// Now convert back to grid
metadata.modelToGrid(pt.x, pt.y, pt)
if (!pt.x.isInfinity && !pt.x.isNaN) { println(pt.x) }
```