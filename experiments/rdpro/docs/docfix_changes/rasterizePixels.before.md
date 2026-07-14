## API Test: `rasterizePixels`

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Create a raster from a set of pixel values @param pixels the list of pixel locations and values @param metadata the raster metadata that defines the geography of the pixels @return a raster that contains all the pixels

### Goal
Create a distributed raster (`RasterRDD[T]`) from explicit pixel coordinates and values, using provided raster metadata and feature attributes.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): An RDD of pixel records, each as `(x, y, value)` where the first two `Int`s are pixel coordinates and `T` is the pixel value.
- `metadata` (`RasterMetadata`): Raster grid/georeferencing definition used to interpret the pixel coordinates (extent, dimensions, tiling, CRS/SRID, transform).
- `rasterFeature` (`RasterFeature`): Raster-level feature metadata attached to the raster (tests use `RasterFeature.create(Array("fileName"), Array("testFile.tif"))`).

### Input
- In-memory Spark input (not file-based): you must provide an `RDD[(Int, Int, T)]`.
- `metadata` must be prepared before the call and must describe the target raster layout.
- `T` is generic and must be consistent with pixel values in `pixels` (e.g., test usage uses `Float` values and gets float tiles).
- Call form must follow real project usage. Verified test usage calls:
  `RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)`.
- README also shows an instance-style `sc.rasterizePixels(pixels, metadata)` call, but that form does not include `rasterFeature` and is a different overload/wrapper shape than the signature listed here.

### Output
Returns `RasterRDD[T]` — a distributed raster containing the provided pixels, organized as raster tiles according to `metadata`, with pixel type `T`.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 360, 180, 90, 90, 4326,
  new AffineTransform(1, 0, 0, -1, -180, 90))
val pixels = sparkContext.parallelize(Seq(
  (0, 0, 100f),
  (180, 0, 200f),
  (100, 50, 300f),
))
val rasterRDD: RDD[ITile[Float]] =
  RasterOperationsGlobal.rasterizePixels(
    pixels,
    metadata,
    RasterFeature.create(Array("fileName"), Array("testFile.tif"))
  )
```

### LLM Instruction Prompt
- Use the exact 3-argument form from the signature when targeting this API: `(pixels, metadata, rasterFeature)`.
- Keep receiver/qualifier exactly as in verified usage when possible: `RasterOperationsGlobal.rasterizePixels(...)`.
- Ensure `pixels` is an `RDD[(Int, Int, T)]` and `T` matches the actual value type in tuples.
- Do not invent missing arguments or alternative parameter types.
- If using an instance helper like `sc.rasterizePixels(...)`, treat it as a separate call shape and do not assume it has the same parameter list unless explicitly documented.

### Prompt Snippet
```text
Create RasterMetadata first, then build an RDD of (xPixel: Int, yPixel: Int, value: T), and call RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature). Keep T consistent with pixel values (e.g., Float values => T = Float).
```

### Common Failure Modes
- Passing tuples in the wrong shape/type (anything other than `(Int, Int, T)`).
- Type mismatch between tuple values and `T` (e.g., mixing `Int` and `Float` unexpectedly).
- Omitting `rasterFeature` when calling the 3-argument global method.
- Using a different receiver/call shape than the one available in scope (e.g., calling bare `rasterizePixels(...)` without qualifier/import support).

### Fix Code Hint
```scala
val pixels: RDD[(Int, Int, Float)] = sparkContext.parallelize(Seq(
  (0, 0, 100f),
  (99, 94, 300f)
))

val metadata = new RasterMetadata(0, 0, 100, 95, 30, 30, 4326, new AffineTransform())

val raster: RasterRDD[Float] =
  RasterOperationsGlobal.rasterizePixels(
    pixels,
    metadata,
    RasterFeature.create(Array("fileName"), Array("testFile.tif"))
  )
```