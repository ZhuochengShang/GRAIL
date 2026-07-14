## API Test: `flatten`
_Grounding: doc-repaired from source (docfix)._

### Goal
Convert a distributed raster (`RasterRDD[T]`) into a regular Spark RDD of per-pixel records `(x, y, metadata, value)` for downstream Spark transformations/aggregations.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal` (Scala object) and `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala class).

```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// Flatten the raster into an RDD of (x, y, metadata, pixelValue)
val pixels = RasterOperationsGlobal.flatten(rasterRDD)
val n = pixels.count()
require(n > 0, "empty result for flatten")

val sample = pixels.first()
val v = sample._4

// Safely handle the pixel value, which may be a multi-band array
val vStr = v match {
  case arr: Array[_] => arr.mkString("[", ",", "]")
  case other => other.toString
}

println("__CHECK__ flatten " + s"count=$n sample=(${sample._1},${sample._2},$vStr)")
```

### LLM Instruction Prompt
- Call form must preserve the tested receiver exactly: `RasterOperationsGlobal.flatten(rasterRDD)`.
- Pass a `RasterRDD[T]` argument.
- Keep the tuple field order exactly as returned: `(Int, Int, RasterMetadata, T)`.
- The provided `rasterRDD` in the test environment has a pixel type `T` of `Array[Float]` (representing multi-band pixels), not a scalar `Float`.
- Do not assume `T` is a scalar like `Float` or `Int` when extracting values from the flattened RDD; use pattern matching or generic array handling if you need to inspect or print the pixel value.

### Prompt Snippet
```text
Use RasterOperationsGlobal.flatten(rasterRDD) to extract per-pixel rows.
Input must be RasterRDD[T]. The output schema is exactly:
(Int x, Int y, RasterMetadata metadata, T value).
The provided rasterRDD has pixel type T = Array[Float] (multi-band). Do not assume T is a scalar Float/Int. Use pattern matching (e.g., case arr: Array[_]) to handle the pixel value safely.
```

### Common Failure Modes
- **ClassCastException on Pixel Value:** Assuming the generic pixel type `T` of the provided `rasterRDD` is a scalar `Float` and attempting to call scalar methods (like `java.lang.Float.isNaN(v)`). The test harness provides a `RasterRDD[Array[Float]]` (multi-band pixels), resulting in a crash when the JVM attempts to cast `[F` (Array of Float) to `java.lang.Float`.
- Assuming a different tuple layout/order than `(x, y, metadata, value)` and reading wrong fields.
- Calling a bare `flatten(...)` or changing receiver shape; tested portable form here is `RasterOperationsGlobal.flatten(...)`.

### Fix Code Hint
```scala
// WRONG: Assuming T is a scalar Float and casting/calling scalar methods
val pixels = RasterOperationsGlobal.flatten(rasterRDD)
val v = pixels.first()._4
if (java.lang.Float.isNaN(v.asInstanceOf[Float])) { ... } // ClassCastException: [F cannot be cast to java.lang.Float

// CORRECT: Handling T as a potential Array (multi-band) via pattern matching
val pixels = RasterOperationsGlobal.flatten(rasterRDD)
val v = pixels.first()._4
val vStr = v match {
  case arr: Array[_] => arr.mkString("[", ",", "]")
  case other => other.toString
}
```