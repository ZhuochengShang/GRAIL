## API Test: `modelToGrid`

### Signature
```scala
def modelToGrid(x: Double, y: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:161_

_Source doc:_ Converts a point location from model (world) space to grid (pixel) space @param x the x-coordinate in the model space (e.g., longitude) @param y the y-coordinate in the model space (e.g., latitude) @param outPoint the output point that contains the grid coordinates

### Goal
Convert a world/model coordinate (for example longitude/latitude or projected coordinates) into raster grid (pixel) coordinates using a raster’s metadata transform.

### Parameters
- `x` (`Double`): X coordinate in model/world space (e.g., longitude or projected X), in the same CRS/units as the raster metadata.
- `y` (`Double`): Y coordinate in model/world space (e.g., latitude or projected Y), in the same CRS/units as the raster metadata.
- `outPoint` (`Point2D.Double`): Mutable output object that will be filled with the computed grid/pixel coordinates (`outPoint.x`, `outPoint.y`).

### Input
You call this on a `RasterMetadata` instance (as shown in tests: `reader.metadata.modelToGrid(...)`), so required input is:

- A valid raster metadata transform already initialized from a raster reader (e.g., GeoTIFF/HDF readers in RDPro/Raptor internals).
- Model-space coordinates `x`, `y` that are expressed in the raster’s model CRS/units.
- A non-null `Point2D.Double` instance to receive output.

Preconditions:
- Coordinate system compatibility is required: if `x`,`y` are in a different CRS than the raster metadata, results will be incorrect (no implicit reprojection is documented here).
- `outPoint` must be allocated by caller before invocation.

### Output
Returns `Unit` — the method writes the computed grid coordinates into `outPoint` in-place.

### Valid Call Patterns
```scala
val outPoint = new Point2D.Double
reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)
```

```scala
val pt = new Point2D.Double
reader.metadata.modelToGrid(Math.toRadians(-110.0) * HDF4Reader.Scale, Math.toRadians(30.0) * HDF4Reader.Scale, pt)
```

### LLM Instruction Prompt
- Call this as an instance method on raster metadata: `reader.metadata.modelToGrid(x, y, outPoint)`.
- Always create and pass a mutable `Point2D.Double` output object.
- Ensure `x` and `y` are in the same model CRS/units as `reader.metadata`.
- Do not expect a return value; read results from `outPoint.x` and `outPoint.y`.

### Prompt Snippet
```text
Given an initialized raster reader, allocate Point2D.Double and call:
reader.metadata.modelToGrid(xModel, yModel, outPoint)
Then use outPoint.x/outPoint.y as pixel coordinates. Keep CRS/units consistent with metadata.
```

### Common Failure Modes
- Passing coordinates in a different CRS/units than raster metadata, producing wrong pixel locations.
- Forgetting to initialize `outPoint` (`null`), causing runtime failure.
- Assuming the method returns coordinates directly (it returns `Unit`).
- Calling `modelToGrid` without a metadata receiver (bare call), which will not match documented usage.

### Fix Code Hint
```scala
val pt = new Point2D.Double
// x/y must be in the raster metadata model space
reader.metadata.modelToGrid(x, y, pt)
val pixelX = pt.x
val pixelY = pt.y
```