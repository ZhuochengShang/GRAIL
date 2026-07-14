# `mapPixels`: g1 README vs fixed README

## G1 README entry

## API Test: `mapPixels`

### Signature
```scala
def mapPixels[U: ClassTag](f: T => U)
def mapPixels[T: ClassTag, U: ClassTag](inputRaster: RasterRDD[T], f: T => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38  (+1 more definition site/overload)_

_Source doc:_ Apply a user-defined function for each pixel in the input raster to produce the output raster @param inputRaster the input raster RDD @param f the function to apply on each input pixel value to produce the output pixel value @tparam T the type of pixels in the input @tparam U the type of pixels in the output @return the resulting RDD

### Goal
Apply per-pixel band math/value transformation on a raster (e.g., unit conversion or thresholding) and return a new raster with transformed pixel type/value.

### Parameters
- `inputRaster` (`RasterRDD[T]`): the input raster RDD whose pixel values are read as type `T`.
- `f` (`T => U`): user function applied to each input pixel value to produce one output pixel value of type `U`.

### Input
A `RasterRDD[T]` already loaded in RDPro (commonly from GeoTIFF via `sc.geoTiff[T]` or HDF via `sc.hdfFile(...)` in project examples), plus a pure pixel-mapping function `T => U`.

Preconditions/type rules to keep calls valid:
- `T` must match the raster’s real runtime pixel type when loading typed rasters (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- Choose `U` to match your intended output pixel values (e.g., `Float => Float` for temperature conversion, `Short => Int` for thresholding with widening).
- Call shape should use the real receiver form shown in project usage (`value.mapPixels(...)`), which is documented and portable.

### Output
Returns `RasterRDD[U]` — a raster RDD with the same raster structure/coverage as input, but with each defined pixel value transformed by `f` into type `U`.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")
```

```scala
val outputRaster: RDD[ITile[Int]] = RasterOperationsLocal.mapPixels(inputRaster, (x: Short) => Math.max(x, 50))
```

### LLM Instruction Prompt
- Use the receiver form `raster.mapPixels(f)` when you already have a `RasterRDD[T]`.
- Ensure typed raster loading uses the correct `T` for source pixels before mapping.
- Make `f` a single-pixel transform `T => U`; do not pass multi-argument or neighborhood functions.
- If changing numeric range/type, set `U` explicitly via assignment type context (e.g., `RasterRDD[Int]`).
- Save raster outputs with GeoTIFF APIs when persistence is required.

### Prompt Snippet
```text
Given a RasterRDD[T], call mapPixels as raster.mapPixels(pixel => ...). 
Keep the lambda type-compatible with T => U, and ensure T matches the source raster load type (e.g., geoTiff[Int], geoTiff[Float], hdfFile layer type). 
Return/use RasterRDD[U], and save with saveAsGeoTiff(...) if output is needed on disk.
```

### Common Failure Modes
- Loading raster with wrong type parameter (`sc.geoTiff[T]`) so `mapPixels` lambda type does not match actual pixels.
- Using a lambda that is not `T => U` (wrong input type or returns unexpected type).
- Assuming `mapPixels` performs reprojection/resampling/alignment; it only transforms pixel values.
- Trying to write non-GeoTIFF output from raster pipeline when task expects GeoTIFF.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val input: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

val output: RasterRDD[Float] =
  input.mapPixels(k => (k - 273.15f) * 9 / 5 + 32)

output.saveAsGeoTiff("temperature_f")
```


---

## Fixed README entry

## API Test: `mapPixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Apply a user-defined function for each pixel in the input raster to produce an output raster with transformed pixel values.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS & TYPES:
// requires `edu.ucr.cs.bdlab.raptor.RasterOperationsLocal` — a Scala object; reference as `RasterOperationsLocal.mapPixels(...)`
// requires `edu.ucr.cs.bdlab.beast.geolite.ITile` — a Scala trait/class; reference as `ITile[T]`
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Apply per-pixel transformation
val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)

// Verify output
val n = mapped.count()
require(n > 0, "empty result for mapPixels")

// Extract a sample tile (RasterRDD[T] contains ITile[T], not raw pixels)
val sampleTile: ITile[Float] = mapped.take(1).head
println("__CHECK__ mapPixels " + s"count=$n sampleTile=$sampleTile")
```

### LLM Instruction Prompt
- `RasterRDD[T]` is an RDD of tiles (`ITile[T]`), not an RDD of individual pixels.
- Calling `.take(1).head` on a `RasterRDD[T]` returns an `ITile[T]`, not a raw pixel value like `Float` or `Int`.
- Do not attempt to call scalar methods (like `.isFinite` or arithmetic operations) directly on the elements of a `RasterRDD`.
- Use `RasterOperationsLocal.mapPixels(inputRaster, f)` to apply a function `T => U` to each pixel.

### Prompt Snippet
```text
RasterRDD[T] is an RDD of ITile[T], not individual pixels. Calling .take(1).head returns an ITile[T]. Do not call scalar methods (like .isFinite) on the elements of a RasterRDD. Use RasterOperationsLocal.mapPixels(raster, (x: T) => U) to transform pixel values.
```

### Common Failure Modes
- **Misunderstanding `RasterRDD[T]` semantics:** Assuming `RasterRDD[Float]` is an RDD of individual `Float` pixels, meaning `mapped.take(1).head` would return a `Float` on which `.isFinite` could be called. However, `RasterRDD[T]` is an RDD of tiles (`ITile[T]`), so `take(1).head` returns an `ITile[Float]`, which does not have an `isFinite` method.
- **Type mismatch on load:** Loading a raster with the wrong type parameter (e.g., `sc.geoTiff[Int]` when the data is `Float`), causing the `mapPixels` lambda type to fail against the actual pixels.

### Fix Code Hint
```scala
// WRONG: Treating RasterRDD elements as scalar pixels
val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)
val firstPixel = mapped.take(1).head
val isGood = firstPixel.isFinite // FAILS: firstPixel is an ITile[Float], not a Float

// CORRECT: Recognizing RasterRDD elements are ITile[T]
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal
import edu.ucr.cs.bdlab.beast.geolite.ITile

val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)
val n = mapped.count()
require(n > 0, "empty result for mapPixels")
val sampleTile: ITile[Float] = mapped.take(1).head
println("__CHECK__ mapPixels " + s"count=$n sampleTile=$sampleTile")
```

