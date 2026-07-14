# Deep-dive: `zonalStats2`

model: google:gemini-3.1-pro-preview · tokens in=7,992 out=5,334 · wall 48s · 2026-07-08 09:43

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience:** USER-FACING. The documentation explicitly describes it as a tool to "Compute distributed zonal statistics," and it operates on high-level RDDs of features and tiles, which is the primary user-facing abstraction in RDPro.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The real call sites demonstrate that it can be invoked directly using standard public objects like `BeastOptions` and a class reference to a `Collector` implementation (e.g., `classOf[Statistics]`).

**L1 PURPOSE**
`zonalStats2` computes distributed zonal statistics by joining a set of polygon zones (vector features) with a raster dataset (tiles) and aggregating the pixel values that fall within each zone. It sits at the core of RDPro's raster-vector analysis pipeline, enabling users to extract aggregated metrics (like sum, min, max, or count) from raster imagery over administrative boundaries or other regions of interest.

**L2 CONTRACT**
- **Receiver:** `ZonalStatistics` object (inferred from the static-style invocation `ZonalStatistics.zonalStats2` in the provided tests).
- **Type Parameter `T`:** The pixel type of the raster. Must have an implicit `ClassTag[T]`. Crucially, the implementation assumes `T` is a scalar numeric type that boxes to `java.lang.Number` (e.g., `Int`, `Float`).
- **`zones` (`RDD[IFeature]`):** The polygon features representing the zones to aggregate over.
- **`raster` (`RDD[ITile[T]]`):** The raster tiles containing the pixel data.
- **`collectorClass` (`Class[_ <: Collector]`):** The class definition of the collector used to aggregate pixel values (e.g., `classOf[Statistics]`). It must have a public no-argument constructor.
- **`opts` (`BeastOptions`):** Additional user-defined options passed down to the join algorithm.
- **`numTiles` (`LongAccumulator`, default `null`):** An optional Spark accumulator to track the total number of processed tiles.
- **Return Value:** `RDD[(IFeature, Collector)]`, a lazy Spark transformation resulting in an RDD of pairs, where each pair contains the original zone feature and its populated `Collector` containing the statistics.
- **Visibility:** Public.
- **Thread-Safety/Laziness:** It is a lazy Spark transformation (building a DAG of `map`, `aggregateByKey`, and `join` operations). It is thread-safe to call, provided the underlying RDDs are not concurrently mutated.

**L3 MECHANICS**
1. **Initialization & Reprojection:** Retrieves the Spark configuration and extracts the spatial reference ID (`rasterSRID`) from the first tile's metadata (`ZonalStatistics.scala:130-131`). It then reprojects the `zones` to match the raster's CRS and assigns a unique ID to each feature using `zipWithUniqueId()` (`lines 133-135`).
2. **Distributed Join:** Performs a full distributed join between the raster tiles and the ID-assigned features using `RaptorJoin.raptorJoinIDFull` (`line 138`).
3. **Mapping:** Maps the join result to extract the feature ID, pixel coordinates, and pixel value (`line 139`).
4. **Aggregation Setup:** Instantiates a zero-value collector using reflection (`collectorClass.getConstructor().newInstance()`) and hardcodes its number of bands to 1 (`lines 142-143`).
5. **Reduction:** Aggregates the pixel values by feature ID using `aggregateByKey`. **Note:** It explicitly casts the pixel value to `Number` via `v._3.asInstanceOf[Number].floatValue()` (`line 145`).
6. **Final Join:** Joins the aggregated statistics back with the original features to restore the full feature data and drops the temporary ID, returning the final `RDD[(IFeature, Collector)]` (`line 150`).

**L4 CORRECT MINIMAL USAGE**
```scala
import org.apache.spark.rdd.RDD
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{IFeature, ITile}
import scala.reflect.ClassTag

// INFERENCE: Assuming `Statistics` is a valid Collector class available in scope,
// and `zonesRDD` / `rasterRDD` are provided by the environment.
def runZonalStats[T: ClassTag](
    zonesRDD: RDD[IFeature], 
    rasterRDD: RDD[ITile[T]], 
    collectorClass: Class[_ <: Collector]
): RDD[(IFeature, Collector)] = {
  
  val opts = new BeastOptions()
  
  // Note: T must be a scalar numeric type (e.g., Int, Float) for zonalStats2.
  // If T is an Array type, this will fail at runtime.
  ZonalStatistics.zonalStats2(zonesRDD, rasterRDD, collectorClass, opts)
}
```

**L5 FAILURE FORENSICS**
- **Attempt 1:** Failed at compile time in the test harness (`value isFinite is not a member of Array[Double]`). The test code attempted to call a non-existent method on an array returned by the collector. This is a flaw in the test assertion, not the API.
- **Attempts 2-5:** Failed at runtime with a `SparkException` caused by a task failure, with the root cause truncated as `java.la...`. Based on the source code at `ZonalStatistics.scala:145` (`v._3.asInstanceOf[Number].floatValue()`), this is almost certainly a `java.lang.ClassCastException`. Unlike `zonalStatsLocal` (which safely pattern-matches on array types like `Array[Float]`), `zonalStats2` hardcodes the assumption that the pixel type `T` is a scalar numeric type. If the test harness provided a `rasterRDD` with an array pixel type (e.g., `Array[Int]` for multi-band rasters), the `.asInstanceOf[Number]` cast fails immediately.

**L6 SELF-ASSESSMENT**
- **INFERENCE:** `ZonalStatistics` is a singleton object. This is inferred from the static-style invocation `ZonalStatistics.zonalStats2` in the real call sites and the presence of `def printUsage` at the end of the block.
- **INFERENCE:** The truncated exception `java.la...` in attempts 2-5 is `java.lang.ClassCastException`. This is deduced from the unsafe `.asInstanceOf[Number]` cast on line 145, which is a known danger zone in generic Scala code.
- **INFERENCE:** `Collector` has a no-argument constructor and methods like `setNumBands`, `collect`, and `accumulate`. This is inferred from their direct usage in the source code.
- **Information needed for certainty:** The full stack trace of the failed attempts to confirm the exact exception, and the definition of the `Collector` trait to verify its exact bounds.
- **Confidence in L2 (Contract):** 9/10. The signature and types are clear, though the exact bounds of `T` are implicitly restricted by the implementation's casting logic.
- **Confidence in L3 (Mechanics):** 10/10. The source code explicitly shows the step-by-step transformations, reprojections, and joins.
- **Confidence in L4 (Minimal Usage):** 9/10. The snippet is standard Spark/Scala and matches the real call sites perfectly, assuming the required types are in scope.