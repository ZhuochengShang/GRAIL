# Deep-dive: `zonalStatsLocal`

model: google:gemini-3.1-pro-preview · tokens in=5,843 out=4,989 · wall 48s · 2026-07-08 09:33

---

**L1 PURPOSE**
The `zonalStatsLocal` API is a driver-side utility in the RDPro/Beast Raptor module designed to compute zonal statistics for a small, in-memory array of spatial zones against a raster file. It sits outside the distributed Spark execution path, bypassing the overhead of RDD partitioning and shuffling. It is intended for scenarios where the number of query geometries is small enough to be processed efficiently in a single thread on the driver node, reading directly from a raster file via a local reader.

**L2 CONTRACT**
*   **Receiver**: `ZonalStatistics` (INFERENCE: inferred to be a singleton `object` based on the static-style call `ZonalStatistics.zonalStatsLocal` in the test snippet).
*   **Parameters**:
    *   `geometries: Array[Geometry]` or `zones: Array[IFeature]`: The spatial boundaries to aggregate pixels over.
    *   `raster: IRasterReader[T]`: A local reader pointing to the raster file. It must be initialized (e.g., via `initialize()`) before calling this method.
    *   `collectorClass: Class[_ <: Collector]`: The `Class` object of the specific statistic collector to use (e.g., `classOf[Statistics]`). It must have a public no-argument constructor.
*   **Return Value**: `Array[Collector]`. The returned array is exactly the same length as the input `geometries`/`zones` array. The index of the collector corresponds to the index of the input zone. If a zone does not overlap any raster pixels, its corresponding entry in the array will be `null`.
*   **Visibility**: Public (no modifiers).
*   **Thread-Safety/Laziness**: Executes eagerly and synchronously in a single thread ("locally in one thread" per source doc). It mutates the instantiated `Collector` objects internally but does not share them across threads during execution.

**L3 MECHANICS**
*   **Algorithm**:
    1.  If called with `Array[IFeature]`, it maps the array to `Array[Geometry]` via `_.getGeometry` and delegates to the `Geometry` overload (line 188).
    2.  It delegates the spatial intersection to `RaptorJoin.raptorJoinLocal(Array(raster), geometries)` (line 164), which returns an iterable of pixel-level join results.
    3.  It initializes an empty `Array[Collector]` of the same length as the input geometries (line 166).
    4.  It iterates over the join results. For each pixel intersection, it extracts the pixel value `m` and normalizes it into an `Array[Float]` (handling `Float`, `Int`, `java.lang.Number`, and arrays of those) (lines 168-175).
    5.  It uses `result.featureID.toInt` to look up the corresponding `Collector` in the results array. If it is `null`, it instantiates a new collector via reflection (`constructor.newInstance()`), sets its band count (`collector.setNumBands(m.length)`), and stores it in the array (lines 176-181).
    6.  It accumulates the pixel value into the collector via `collector.collect(result.x, result.y, m)` (line 182).
*   **Delegates to**: `RaptorJoin.raptorJoinLocal` (not provided in context), `Collector.newInstance/setNumBands/collect`.
*   **Mutates**: The locally allocated `results: Array[Collector]` and the internal state of each instantiated `Collector`.
*   **Failure Conditions**: 
    *   Throws `NoSuchMethodException` / `InstantiationException` if `collectorClass` lacks a no-argument constructor.
    *   Throws `MatchError` if a pixel value `result.m` is of a type not covered in the pattern match (lines 168-175).
    *   Throws `IndexOutOfBoundsException` if `result.featureID.toInt` is out of bounds of the `geometries` array length.

**L4 CORRECT MINIMAL USAGE**
Because `zonalStatsLocal` requires an `IRasterReader[T]` (which reads directly from a file system path) rather than a distributed `rasterRDD`, and because the concrete implementation of `IRasterReader` (e.g., `GeoTiffReader`) is not provided in the context, this API cannot be exercised completely standalone from scratch using only the harness bindings. 

The smallest legitimate enclosing use assumes you have an initialized `IRasterReader[T]` and extracts a small local array from `featuresRDD`:

```scala
import org.apache.hadoop.fs.FileSystem
import org.apache.spark.SparkContext
// INFERENCE: Assuming BeastOptions, Collector, Statistics, IFeature are imported from their respective packages

def runLocalZonalStats[T](
    sc: SparkContext, 
    featuresRDD: org.apache.spark.rdd.RDD[IFeature], 
    rasterReader: IRasterReader[T] // Must be instantiated by caller (e.g., new GeoTiffReader[T]())
): Array[Collector] = {
  
  // 1. Collect a small array of zones to the driver
  val localZones: Array[IFeature] = featuresRDD.take(100)
  
  // 2. Ensure the reader is initialized (assuming rasterPath is known)
  // rasterReader.initialize(FileSystem.get(sc.hadoopConfiguration), "path/to/raster.tif", "0", new BeastOptions())
  
  // 3. Execute local zonal statistics
  val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(
    localZones, 
    rasterReader, 
    classOf[Statistics] // INFERENCE: Assuming Statistics extends Collector and has a no-arg constructor
  )
  
  // 4. Filter out nulls (zones with no overlapping pixels)
  zsResults.filter(_ != null)
}
```

**L5 FAILURE FORENSICS**
*   **Attempt 1**: `import org.apache.spark.beast.IFeature` failed because `IFeature` is not located in the `org.apache.spark.beast` package. (INFERENCE: It is likely in `edu.ucr.cs.bdlab.beast.geolite.IFeature`).
*   **Attempt 2**: `val rasterReader = ... create ...` failed because the user tried to call a non-existent `create` method on an `edu.ucr.cs.bdlab.raptor` object to instantiate the reader.
*   **Attempts 3, 4, & 5**: `val rasterReader = rasterRDD.rasterFeature...` failed because the user attempted to extract a local `IRasterReader` from a distributed `rasterRDD`. This is a fundamental misunderstanding of the API. `IRasterReader` is a file-based reader trait (`getFilePath`, `initialize(FileSystem...)`), whereas `rasterRDD` is a distributed Spark collection. There is no `rasterFeature` method on the RDD to magically convert a distributed dataset back into a local file reader.

**L6 SELF-ASSESSMENT**
*   **Inferences**:
    *   `ZonalStatistics` is a singleton object.
    *   `Geometry` refers to JTS `org.locationtech.jts.geom.Geometry`.
    *   `IFeature` is a Beast feature interface (likely `edu.ucr.cs.bdlab.beast.geolite.IFeature`).
    *   `Statistics` is a concrete class implementing `Collector` with a no-arg constructor.
    *   The concrete implementation of `IRasterReader[T]` (like `GeoTiffReader`) must be instantiated via `new` before calling `initialize`.
*   **Information needed for certainty**: The exact package paths for `Geometry`, `IFeature`, `Collector`, and `Statistics`; the concrete class name for `IRasterReader` to provide a 100% runnable end-to-end snippet.
*   **Confidence Scores**:
    *   **L2 (Contract)**: 9/10. The signature and behavior are explicitly clear in the source, though exact package imports for the types are missing from the context.
    *   **L3 (Mechanics)**: 9/10. The source code for the method is fully provided and straightforward, though the internal mechanics of `RaptorJoin.raptorJoinLocal` are a black box.
    *   **L4 (Usage)**: 7/10. I cannot provide a fully compilable snippet that instantiates the `IRasterReader` because the concrete class is missing from the context, forcing me to pass it as a parameter.