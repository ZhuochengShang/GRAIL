## API Test: `flatten`

### Signature
```scala
def flatten[T](raster: RasterRDD[T]): RDD[(Int, Int, RasterMetadata, T)]
def flatten: RDD[(Int, Int, RasterMetadata, T)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69  (+1 more definition site/overload)_

_Source doc:_ Extract all pixel values into an RDD @param raster the raster to extract its pixels @tparam T the type of pixel values @return an RDD that contains all pixel locations and values

### Goal
Convert a distributed raster (`RasterRDD[T]`) into a regular Spark RDD of per-pixel records `(x, y, metadata, value)` for downstream Spark transformations/aggregations.

### Parameters
- `raster` (`RasterRDD[T]`): the raster dataset whose pixels should be extracted as individual rows.

### Input
`flatten` expects a `RasterRDD[T]` that is already loaded or produced by earlier RDPro steps (for example from `sc.geoTiff[T](...)`, `sc.hdfFile(...)`, `mapPixels`, `slidingWindow`, etc.).

Preconditions and compatibility notes from project context:
- Use the correct pixel type when creating the raster (critical rule): for GeoTIFF loading, `sc.geoTiff[T]` type parameter must match the real pixel type.
- `flatten` itself does not perform CRS/resolution/tile-size harmonization; if your raster came from multi-raster operations (like `overlay`), those inputs must have been made compatible beforehand (e.g., reshape/reproject/rescale as needed).
- Input raster formats in RDPro workflows are GeoTIFF/HDF, but `flatten` operates on the in-memory `RasterRDD[T]`, not directly on file paths.

### Output
Returns `RDD[(Int, Int, RasterMetadata, T)]` — each output row contains:
1. pixel x index (`Int`)
2. pixel y index (`Int`)
3. raster metadata (`RasterMetadata`) associated with that pixel context
4. pixel value (`T`)

This is a plain Spark `RDD`, so you can use standard RDD operations (`map`, `filter`, `collectAsMap`, aggregations, joins, etc.).

### Valid Call Patterns
```scala
val finalPixels: Map[(Int, Int), Double] = RasterOperationsGlobal.flatten(smoothedRaster)
  .map(x => ((x._1, x._2), x._4))
  .collectAsMap()
  .toMap
```

### LLM Instruction Prompt
- Call form must preserve the tested receiver exactly: `RasterOperationsGlobal.flatten(smoothedRaster)`.
- Pass a `RasterRDD[T]` argument.
- Keep the tuple field order exactly as returned: `(Int, Int, RasterMetadata, T)`.
- Do not invent extra arguments/options.
- Ensure upstream raster typing is correct (`sc.geoTiff[T]` must match actual raster pixel type).

### Prompt Snippet
```text
Use RasterOperationsGlobal.flatten(rasterRDD) to extract per-pixel rows.
Input must be RasterRDD[T]. The output schema is exactly:
(Int x, Int y, RasterMetadata metadata, T value).
If raster was loaded from GeoTIFF, ensure T matches the real pixel type.
Do not add any extra parameters.
```

### Common Failure Modes
- Using the wrong generic pixel type upstream (e.g., incorrect `sc.geoTiff[T]`) leading to type/runtime issues before flatten.
- Assuming a different tuple layout/order than `(x, y, metadata, value)` and reading wrong fields.
- Calling a bare `flatten(...)` or changing receiver shape; tested portable form here is `RasterOperationsGlobal.flatten(...)`.
- Expecting `flatten` to align/reproject rasters; compatibility must be handled before producing the input `RasterRDD`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

// Ensure raster is correctly typed at load time
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

// Correct tested call shape
val pixels: RDD[(Int, Int, RasterMetadata, Int)] =
  RasterOperationsGlobal.flatten(raster)

// Use tuple fields in the documented order
val xyToValue: RDD[((Int, Int), Int)] = pixels.map(p => ((p._1, p._2), p._4))
```