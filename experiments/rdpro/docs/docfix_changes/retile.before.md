## API Test: `retile`

### Signature
```scala
def retile(tileWidth: Int, tileHeight: Int)
def retile[T: ClassTag](raster: RasterRDD[T], tileWidth: Int, tileHeight: Int): RasterRDD[T]
def retile(newTileWidth: Int, newTileHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566  (+2 more definition site/overload)_

_Source doc:_ Regrids the given raster to the target tile width and height @param raster the raster to regrid @param tileWidth the new tile width in pixels @param tileHeight the new tile height in pixels @tparam T the type of the pixel values in the raster @return a new raster with the given tile width and height

### Goal
Regrid a `RasterRDD[T]` into a new tile layout by setting tile width/height in pixels, while keeping the same pixel value type `T`.

### Parameters
- `raster` (`RasterRDD[T]`): input distributed raster to retile.
- `tileWidth` (`Int`): target tile width in pixels.
- `tileHeight` (`Int`): target tile height in pixels.

### Input
A `RasterRDD[T]` (commonly loaded from GeoTIFF or HDF in RDPro workflows) and integer target tile dimensions.  
Preconditions and compatibility/type rules to keep calls correct:

- Use a correctly typed raster load before calling (`sc.geoTiff[T]` type must match the real pixel type).
- `tileWidth` and `tileHeight` are pixel counts for the new tile grid.
- If this is part of a multi-raster pipeline (for example before `overlay`), ensure downstream metadata compatibility requirements are met (same resolution/CRS/tile size across rasters), potentially by reshape/reproject operations before combining datasets.

### Output
Returns `RasterRDD[T]` — a new raster dataset containing the same pixel type `T`, but regridded to the requested tile width and tile height.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64).explode
retiled.saveAsGeoTiff("glc_retiled", GeoTiffWriter.WriteMode -> "distributed")

val retiled: RasterRDD[Int] = RasterOperationsFocal.retile(raster, 20, 20)
```

### LLM Instruction Prompt
- Call `retile` using a real supported receiver form: `raster.retile(tileWidth, tileHeight)` or `RasterOperationsFocal.retile(raster, tileWidth, tileHeight)`.
- Keep argument order exactly `(raster, tileWidth, tileHeight)` for the static form.
- Ensure raster type parameter `T` is already correct at load time (`sc.geoTiff[T]` matched to actual pixel type).
- Do not invent extra parameters (no CRS/resampling/compression args on `retile` itself).
- If the result is used with operations that require matching metadata (e.g., overlay), align datasets as needed in preceding steps.

### Prompt Snippet
```text
Retile this RasterRDD to a new tile grid using raster.retile(tileWidth, tileHeight), keeping the same pixel type T. 
Use only the provided RasterRDD and integer tile sizes; do not add extra retile arguments.
If this raster will be combined with other rasters later, ensure metadata compatibility in the pipeline.
```

### Common Failure Modes
- Loading raster with wrong `T` (e.g., `sc.geoTiff[Int]` for non-integer pixel data), causing type/runtime issues earlier in pipeline.
- Using unsupported/invented call shapes or extra arguments not in the API.
- Retiling one raster but not other rasters before metadata-sensitive combination steps (such as overlay), causing compatibility errors downstream.
- Confusing `retile` overloads: one overload returns `RasterRDD[T]` (raster retile), another listed overload returns `RasterMetadata`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled: RasterRDD[Int] = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")
```