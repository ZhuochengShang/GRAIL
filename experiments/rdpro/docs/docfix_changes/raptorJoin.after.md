## API Test: `raptorJoin`
_Grounding: doc-repaired from source (docfix)._

### Goal
Run a distributed raster–vector overlap join (Raptor) to return all feature/pixel intersections, enabling zonal-style analysis such as per-polygon raster aggregation.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS:
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.raptor.RaptorJoinFeature
import edu.ucr.cs.bdlab.beast._ // Provides RaptorMixinOperations3 implicit

// Call via Scala implicit method directly on the RasterRDD
val joined = rasterRDD.raptorJoin(featuresRDD, new BeastOptions())
val n = joined.count()
require(n > 0, "empty result for raptorJoin")

val sample = joined.first()
// Safely handle the pixel value `m` which may be an array (multi-band) or scalar (single-band)
val mFirstBand = sample.m match {
  case arr: Array[Float] => arr.headOption.getOrElse(Float.NaN)
  case f: Float => f
  case _ => Float.NaN
}

require(!java.lang.Float.isNaN(mFirstBand) && !java.lang.Float.isInfinite(mFirstBand), s"invalid pixel value in raptorJoin result: $mFirstBand")
println("__CHECK__ raptorJoin " + s"count=$n,m=$mFirstBand")
```

### LLM Instruction Prompt
- `raptorJoin` must be called via the Scala implicit class `RaptorMixinOperations3` as `raster.raptorJoin(features, new BeastOptions())`, rather than using `JavaSpatialRDDHelper` directly.
- The pixel type `T` of the resulting `RaptorJoinFeature[T]` matches the raster's pixel type. For multi-band rasters, this is an array (e.g., `Array[Float]`), not a scalar `Float`.
- Accessing the pixel value `.m` on the join result will return an array for multi-band rasters. Attempting to use it directly as a scalar `Float` (e.g., passing it to `java.lang.Float.isNaN`) will cause Scala to infer `T = Float`, insert a cast, and throw a `ClassCastException` at runtime.
- Always use pattern matching on `.m` to safely extract the value, handling both `Array[Float]` and `Float` cases.

### Prompt Snippet
```text
Given a raster RDD and a vector SpatialRDD, call `raster.raptorJoin(features, new BeastOptions())` using the Scala implicit. Handle the resulting `RaptorJoinFeature[T]` pixel value `.m` safely using pattern matching, as it may be an `Array[Float]` (multi-band) or `Float` (single-band). Do not assume `.m` is always a scalar.
```

### Common Failure Modes
- **ClassCastException on pixel value access:** Assuming the pixel value `.m` in `RaptorJoinFeature[T]` is always a scalar `Float` and passing it to functions like `java.lang.Float.isNaN`. For multi-band rasters, `.m` is an `Array[Float]`, and type inference will insert an invalid cast if treated as a scalar.
- **Incorrect API invocation:** Calling `JavaSpatialRDDHelper` directly instead of using the Scala implicit `raster.raptorJoin(features)`.

### Fix Code Hint
```scala
// WRONG: Assumes `m` is always a scalar, causing ClassCastException on multi-band rasters
val joined = rasterRDD.raptorJoin(featuresRDD, new BeastOptions())
val badFilter = joined.filter(v => !java.lang.Float.isNaN(v.m)) // Fails if v.m is Array[Float]

// CORRECT: Use pattern matching to handle both Array[Float] and Float
val joined = rasterRDD.raptorJoin(featuresRDD, new BeastOptions())
val mFirstBand = joined.first().m match {
  case arr: Array[Float] => arr.headOption.getOrElse(Float.NaN)
  case f: Float => f
  case _ => Float.NaN
}
```