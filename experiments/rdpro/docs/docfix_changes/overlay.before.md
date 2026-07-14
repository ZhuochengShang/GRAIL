## API Test: `overlay`

### Signature
```scala
def overlay[V](rasters: RasterRDD[T]*)
def overlay[T: ClassTag, V](@varargs inputs: RDD[ITile[T]]*)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96  (+1 more definition site/overload)_

_Source doc:_ Overlays this raster RDD on top other ones @param rasters the other rasters to stack this raster on @return a new RasterRDD which contains the stack of this raster on top of the given ones

### Goal
Stack this raster with one or more other rasters so each defined pixel carries values from all overlaid inputs (band-like array output per pixel).

### Parameters
- `rasters` (`RasterRDD[T]*`): One or more other raster RDDs to overlay with the receiver raster (`this`), in the given order.

### Input
Caller provides `RasterRDD[T]` inputs (or `RDD[ITile[T]]` for the overload), typically loaded from RDPro-supported raster sources such as GeoTIFF/HDF beforehand.

Preconditions (critical):
- All rasters must be metadata-compatible (same resolution, CRS, and tile size).
- If not compatible, first align them using reshape/reprojection operations (for example `reshapeNN` / other reshape ops per workflow).
- When loading GeoTIFF, use the correct typed loader `sc.geoTiff[T]` that matches the real pixel type.

### Output
Returns `unspecified` — a new overlaid raster RDD representing the stacked inputs; documented usage shows `RasterRDD[Array[Int]]` for `Int` inputs, and tests show `RasterRDD[Array[Short]]` for `Short` tile inputs.

### Valid Call Patterns
```scala
val raster1: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val raster2: RasterRDD[Int] = sc.geoTiff[Int]("vegetation")
val stacked: RasterRDD[Array[Int]] = raster1.overlay(raster2)
```

```scala
val raster3: RasterRDD[Array[Short]] = RasterOperationsLocal.overlay(raster1, raster2)
```

### LLM Instruction Prompt
- Use the instance call form when working from `RasterRDD` values: `rasterA.overlay(rasterB, ...)`.
- Only pass raster inputs of compatible metadata (resolution/CRS/tile size); otherwise reshape/reproject first.
- Ensure typed raster loading matches true pixel type (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, etc.) before calling overlay.
- Do not invent extra parameters; `overlay` takes only varargs raster inputs.

### Prompt Snippet
```text
Given compatible RasterRDDs with matching resolution, CRS, and tile size, call overlay in instance form:
val stacked = raster1.overlay(raster2)
If metadata differs, first reshape/reproject to align them, then overlay.
Use typed loaders that match actual pixel type.
```

### Common Failure Modes
- Metadata mismatch across inputs (different CRS/resolution/tile size) causing invalid overlay semantics or runtime issues.
- Wrong pixel type at load time (`sc.geoTiff[T]` not matching actual raster type), which can break downstream typing.
- Using a non-receiver/bare call shape not shown in project usage.

### Fix Code Hint
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```