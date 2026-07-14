## API Test: `zonalStatsLocal`
_Grounding: doc-repaired from source (docfix)._

### Goal
**ADVANCED/LOW-LEVEL API.** Computes single-threaded local zonal statistics for a small in-memory array of geometries against a single raster file. 
*Note: Exclude this API from the main user-facing benchmark denominator. Typical users should rely on distributed RDD-based joins. This is an internal/optimization bypass that requires explicit low-level construction.*

### Input
- `zones`: `Array[IFeature]` or `Array[Geometry]` (caller-owned, typically collected to the driver via `featuresRDD.take(N)`).
- `raster`: An `IRasterReader[T]` that MUST be explicitly initialized from a local file system path. **Do not attempt to extract this from a distributed `RasterRDD`.**
- `collectorClass`: `Class[_ <: Collector]`, typically `classOf[edu.ucr.cs.bdlab.raptor.Statistics]`.

### Output
Returns an `Array[Collector]` equal in length to the input zones. Zones with no overlapping pixels will have `null` at their corresponding index.

### Valid Call Patterns
**Required Types & Imports:**
```scala
import edu.ucr.cs.bdlab.raptor.{ZonalStatistics, IRasterReader, Collector, Statistics}
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import org.apache.hadoop.fs.{Path, FileSystem}
```

**Corrected Call Sketch:**
```scala
// The harness provides:
// featuresRDD: RDD[IFeature]
// rasterReader: IRasterReader[Float] (uninitialized)
// rasterFile: String (path to the raster)
// sparkContext: SparkContext

val zones: Array[IFeature] = featuresRDD.take(32)
require(zones.nonEmpty, "No zones available for zonalStatsLocal test")

// 1. Initialize the local raster reader provided by the harness
val path = new Path(rasterFile)
val fs: FileSystem = path.getFileSystem(sparkContext.hadoopConfiguration)
rasterReader.initialize(fs, rasterFile, "0", new BeastOptions())

// 2. Execute local single-threaded zonal statistics
val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(
  zones, 
  rasterReader, 
  classOf[Statistics]
)

// 3. Filter out nulls (zones with no overlapping pixels)
val validResults: Array[Collector] = zsResults.filter(_ != null)
```

### LLM Instruction Prompt
- This is a low-level API. You must initialize the provided `rasterReader` explicitly using `rasterReader.initialize(fs, path, layer, options)` before calling `zonalStatsLocal`.
- Pass arguments exactly as: `(zonesArray, initializedRasterReader, classOf[Statistics])`.
- Handle `null` entries in the returned `Array[Collector]`, as non-overlapping zones return `null`.

### Prompt Snippet
```text
Collect a small array of zones to the driver. Initialize the provided `rasterReader` using `rasterReader.initialize(new Path(rasterFile).getFileSystem(sc.hadoopConfiguration), rasterFile, "0", new BeastOptions())`. Call `ZonalStatistics.zonalStatsLocal(zones, rasterReader, classOf[Statistics])`. Filter nulls from the result. Do not use RasterRDD.
```

### Common Failure Modes
- **Extracting reader from distributed RDD (The failure that just happened):** Attempting to extract a local `IRasterReader` from a distributed `RasterRDD` using non-existent properties (e.g., `rasterRDD.rasterFeature`). A distributed RDD of tiles cannot be trivially unwrapped; the reader must be initialized directly from the file path.
- **Uninitialized Reader:** Passing the harness-provided `rasterReader` without calling `.initialize(...)` first.
- **Null Pointer Exceptions:** Assuming all returned entries in the `Array[Collector]` are non-null.
- **Framework Misuse:** Using this local API for massive zone arrays where distributed partitioned workflows (`RaptorJoin`) are required.

### Fix Code Hint
```scala
// WRONG: Attempting to extract a local reader from a distributed RDD
val reader = rasterRDD.rasterFeature.raster // Fails to compile
val zsResults = ZonalStatistics.zonalStatsLocal(zones, reader, classOf[Statistics])

// RIGHT: Initializing the local reader directly from the file system path
val path = new org.apache.hadoop.fs.Path(rasterFile)
val fs = path.getFileSystem(sparkContext.hadoopConfiguration)
rasterReader.initialize(fs, rasterFile, "0", new edu.ucr.cs.bdlab.beast.common.BeastOptions())

val zsResults = edu.ucr.cs.bdlab.raptor.ZonalStatistics.zonalStatsLocal(
  zones, rasterReader, classOf[edu.ucr.cs.bdlab.raptor.Statistics]
)
val validResults = zsResults.filter(_ != null)
```