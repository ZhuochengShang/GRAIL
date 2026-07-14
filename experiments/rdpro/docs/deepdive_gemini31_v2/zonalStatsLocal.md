# Deep-dive: `zonalStatsLocal`

model: google:gemini-3.1-pro-preview · tokens in=6,043 out=4,188 · wall 41s · 2026-07-08 10:05

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as ADVANCED/LOW-LEVEL. It bypasses Spark's distributed RDD partitioning to perform single-threaded, local zonal statistics, which is only appropriate for small, in-memory arrays of geometries against a single raster file. It should be excluded from a main user-facing benchmark denominator, as typical users should rely on distributed RDD-based joins (e.g., `RaptorJoin.raptorJoinIDFull` seen in the source).

Testability: TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. The API requires an initialized `IRasterReader[T]`. While the context does not show the exact instantiation of the reader (e.g., `new GeoTiffReader()`), the provided test snippet demonstrates that it must be explicitly initialized using `rasterReader.initialize(fileSystem, path, layer, opts)` before being passed to the API.

L1 PURPOSE
`zonalStatsLocal` computes zonal statistics for a small, in-memory array of vector zones against a raster file using a single-threaded local execution path. It sits at the low-level execution layer of the RDPro/Beast pipeline, designed as an optimization to avoid the overhead of Spark partitioning and shuffling when the number of query geometries is small enough to be processed efficiently on a single driver or executor node.

L2 CONTRACT
- **Receiver**: `ZonalStatistics` (object).
- **Parameters**:
  - `geometries` (`Array[Geometry]`) or `zones` (`Array[IFeature]`): The array of vector zones to aggregate raster pixels over.
  - `raster` (`IRasterReader[T]`): An initialized raster reader pointing to the raster file being aggregated. Must be initialized via `.initialize(...)` prior to the call.
  - `collectorClass` (`Class[_ <: Collector]`): The class that defines and computes the statistics (e.g., `classOf[Statistics]`). Must have a no-argument constructor.
- **Return Value**: `Array[Collector]`. An array of collectors equal in length to the input array, preserving the input order. Features that do not overlap any pixels will have `null` at their corresponding index.
- **Visibility**: Public.
- **Thread-safety/Laziness**: Eagerly evaluated. It is single-threaded and mutates the instantiated `Collector` objects internally.

L3 MECHANICS
- The `IFeature` overload maps the features to their underlying geometries (`zones.map(_.getGeometry)`) and delegates to the `Geometry` overload.
- The `Geometry` overload delegates the spatial intersection to `RaptorJoin.raptorJoinLocal(Array(raster), geometries)`, which returns an iterator of overlapping pixels (`joinResults`).
- It allocates an `Array[Collector]` of the same length as the input geometries.
- It iterates over the `joinResults`. For each pixel intersection:
  - It normalizes the pixel value `m` into an `Array[Float]`, handling various numeric types (`Float`, `Integer`, `Array[Float]`, etc.).
  - It checks the `results` array at the index corresponding to `result.featureID`. If `null`, it uses reflection (`collectorClass.getConstructor().newInstance()`) to instantiate a new collector, sets its band count (`setNumBands(m.length)`), and stores it in the array.
  - It accumulates the pixel value into the collector via `collector.collect(result.x, result.y, m)`.
- It returns the populated `results` array.

L4 CORRECT MINIMAL USAGE
```scala
import edu.ucr.cs.bdlab.raptor.{ZonalStatistics, Collector, Statistics, IRasterReader}
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import org.apache.hadoop.fs.Path

// ASSUMED BINDINGS from harness/history:
// featuresRDD: RDD[IFeature]
// rasterReader: IRasterReader[Float] (instantiated but uninitialized)
// rasterFile: Path
// sparkContext: SparkContext

// 1. Collect a small array of features to the driver
val features: Array[IFeature] = featuresRDD.take(10)

// 2. Initialize the raster reader explicitly (as shown in the test suite)
rasterReader.initialize(
  rasterFile.getFileSystem(sparkContext.hadoopConfiguration),
  rasterFile.toString,
  "0",
  new BeastOptions()
)

// 3. Execute local zonal statistics
val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(
  features,
  rasterReader,
  classOf[Statistics]
)

// 4. Filter out nulls (zones with no overlapping pixels)
val validResults: Array[Collector] = zsResults.filter(_ != null)
```

L5 FAILURE FORENSICS
- **Attempt 1**: Failed with `IFeature is not a member of package org.apache.spark.b`. The user attempted to import `IFeature` from `org.apache.spark.beast`, but `IFeature` belongs to a different package (likely `edu.ucr.cs.bdlab.beast.geolite.IFeature`).
- **Attempt 2**: Failed with `value create is not a member of object edu.ucr.cs.bdlab.rapto[GeoTiffReader]`. The user tried to instantiate a reader using a non-existent factory method `GeoTiffReader.create(...)` instead of instantiating it and calling `.initialize(...)`.
- **Attempts 3, 4, & 5**: Failed with `value rasterFeature is not a member of edu.ucr.cs.bdlab.beast...`. The user attempted to extract a local `IRasterReader` directly from a distributed `rasterRDD` using non-existent properties (`rasterRDD.rasterFeature`, `rasterRDD.rasterFeature.raster`). A distributed RDD of tiles cannot be trivially unwrapped into a local file reader; the reader must be initialized directly from the file path.

L6 SELF-ASSESSMENT
- **Inferences**: 
  - I inferred that `Statistics` is a valid subclass of `Collector` based on its usage in the provided test snippet.
  - I inferred that `BeastOptions` is the correct configuration class to pass to `initialize` based on the test snippet.
  - I inferred that `IFeature` is not in `org.apache.spark.beast` based on the compiler error, though its exact package is not provided in the context.
- **Information needed for certainty**: The exact concrete class of `IRasterReader` (e.g., `GeoTiffReader`) and its constructor signature to show a truly standalone, from-scratch instantiation.
- **Confidence Scores**:
  - **L2 (Contract)**: 10/10. The signature, parameters, and return types are explicitly defined in the provided source and documentation.
  - **L3 (Mechanics)**: 10/10. The entire method body is provided, making the internal algorithm and delegation completely transparent.
  - **L4 (Minimal Usage)**: 9/10. The usage is correct based on the test snippet, but relies on the harness providing an uninitialized `IRasterReader` instance since the concrete reader class constructor is missing from the context.