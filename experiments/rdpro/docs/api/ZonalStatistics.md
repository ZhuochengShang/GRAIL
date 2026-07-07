# ZonalStatistics

_`zonalStats2` computes zonal statistics for specified polygonal regions over a raster dataset, providing insights into the pixel values within those zones._

**Receiver:** static object — call `ZonalStatistics.<method>(...)`

**Members** (most robust first): ⚠️ `zonalStats2` **(primary)**, ⚠️ `zonalStatsLocal`

---

## API Test: `zonalStats2`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def zonalStats2[T](zones: RDD[IFeature], raster: RDD[ITile[T]], collectorClass: Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator = null)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:128_

_Source doc:_ Computes zonal statistics between a set of zones (polygons) and a raster file given by its path and a layer in that file. The result is an RDD of pairs of a feature and a collector value @param zones a set of polygons that represent the regions or zones @param raster the RDD of tiles @param collectorClass the class that collects the pixel values to compute the statistics @param opts additional user-defined options @param numTiles an optional accumulator to collect the total number of processed tiles @return a set of (Feature, Statistics)

### Goal
`zonalStats2` computes zonal statistics for specified polygonal regions over a raster dataset, providing insights into the pixel values within those zones.

### Parameters
- `zones` (`RDD[IFeature]`): An RDD containing polygon features that define the zones for which statistics will be computed. Each feature represents a distinct area of interest.
- `raster` (`RDD[ITile[T]]`): An RDD of raster tiles, where each tile contains pixel data of a specific type `T`. This represents the raster dataset from which statistics will be derived.
- `collectorClass` (`Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator`), default `null`: The class type of the collector that will aggregate pixel values to compute the desired statistics. `opts` are additional user-defined options for processing, and `numTiles` is an optional accumulator to track the total number of tiles processed.

### Input
The caller must provide:
- An RDD of polygon features (`zones`) that represent the areas for which statistics are to be calculated.
- An RDD of raster tiles (`raster`) that must be compatible with the expected pixel type `T`.
- A valid `collectorClass` that extends `Collector` to specify how the statistics should be aggregated.
- A `BeastOptions` instance for any additional processing options.

### Output
Returns an RDD of pairs, where each pair consists of a feature from `zones` and the corresponding statistics collected for that feature from the `raster`. The statistics are represented by the specified collector class.

### Valid Call Patterns
```scala
val vectorFile = locateResource("/vectors/ne_110m_admin_1_states_provinces.zip")
val rasterFile = locateResource("/rasters/glc2000_small.tif")

val polygons: RDD[IFeature] = SpatialReader.readInput(sparkContext, new BeastOptions(), vectorFile.getPath, "shapefile")
  .zipWithIndex()
  .map(featureIndex => new Feature((Row.unapplySeq(featureIndex._1).get :+ featureIndex._2.toInt).toArray,
    StructType(featureIndex._1.schema :+ StructField("index", IntegerType))))

val raster: RDD[ITile[Int]] = new RasterFileRDD[Int](sparkContext, rasterFile.getPath, new BeastOptions())

val zsResults: Array[Collector] =
  ZonalStatistics.zonalStats2(polygons, raster, classOf[Statistics], new BeastOptions())
    .map(fc => (fc._1.getAs[Int]("index"), fc._2))
    .collect
    .sortBy(_._1)
    .map(_._2)
```

### LLM Instruction Prompt
When calling `zonalStats2`, ensure that the input RDDs are properly defined and that the collector class is appropriate for the statistics you wish to compute.

### Prompt Snippet
```text
To compute zonal statistics using `zonalStats2`, provide an RDD of polygon features, an RDD of raster tiles, and specify the collector class for the desired statistics.
```

### Common Failure Modes
- **[compile]** error: not found: type Collector _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the RDDs for `zones` and `raster` are correctly loaded and that the `collectorClass` is a valid subclass of `Collector` before calling `zonalStats2`.
```

## API Test: `zonalStatsLocal`
_Grounding: VERIFIED — doc-derived code compiled and ran via comprehension --execute._

### Signature
```scala
def zonalStatsLocal[T](geometries: Array[Geometry], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
def zonalStatsLocal[T](zones: Array[IFeature], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:162  (+1 more definition site/overload)_

_Source doc:_ Run zonal statistics locally in one thread. This is useful when the array of geometries is small and the overhead of partitioning could be high. @param zones the array of features that describe the zones. @param raster the raster reader that points to the raster file being aggregated @param collectorClass the class that computes the statistics @return an array of collectors that is equal in length to the input array of features with the result for each. Features that do not overlap any pixels will have null.

### Goal
`zonalStatsLocal` computes zonal statistics for specified geometries against a raster dataset, returning the results in a collector format.

### Parameters
- `geometries` (`Array[Geometry]`): An array of geometries that define the zones for which statistics will be calculated. These geometries should represent areas of interest within the raster data.
- `raster` (`IRasterReader[T]`): An instance of `IRasterReader` that provides access to the raster data being analyzed. The raster must be loaded in a compatible format, such as GeoTIFF.
- `collectorClass` (`Class[_ <: Collector]`): A class type that specifies the type of collector to be used for computing the statistics. This class must extend the `Collector` interface.

### Input
The caller must provide:
- An array of geometries or features that define the zones (e.g., administrative boundaries).
- A raster reader initialized with a raster file (e.g., GeoTIFF) that contains the data to be analyzed.
- The collector class that will be used to compute the statistics.

### Output
Returns `Array[Collector]` — an array of collectors, each corresponding to an input geometry. Each collector contains the computed statistics for its respective zone. If a geometry does not overlap with any raster pixels, the corresponding collector will be `null`.

### Valid Call Patterns
```scala
val vectorFile = new Path(locateResource("/vectors/ne_110m_admin_1_states_provinces.zip").getPath)
val rasterFile = new Path(locateResource("/rasters/glc2000_small.tif").getPath)

val vectorReader = new ShapefileFeatureReader
vectorReader.initialize(vectorFile, new BeastOptions())
import scala.collection.JavaConverters._
val features: Array[IFeature] = vectorReader.iterator().asScala.toArray
val rasterReader: IRasterReader[Int] = new GeoTiffReader[Int]
rasterReader.initialize(rasterFile.getFileSystem(sparkContext.hadoopConfiguration), rasterFile.toString, "0", new BeastOptions())

val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
```

### LLM Instruction Prompt
- Ensure that the geometries provided overlap with the raster data to avoid null collectors in the output. The raster must be loaded using a compatible reader, and the collector class must be a valid implementation of the `Collector` interface.

### Prompt Snippet
```text
Compute zonal statistics using the provided geometries and raster data. Ensure that the geometries overlap with the raster to obtain valid results.
```

### Common Failure Modes
- **[compile]** error: not found: type Collector _(seen 4x)_
- **[compile]** error: value readInput is not a member of object edu.ucr.cs.bdlab.beast.io.SpatialFileRDD

### Fix Code Hint
```scala
Check that the geometries provided in the input actually intersect with the raster data. Ensure that the raster is correctly loaded and that the collector class is a valid implementation.
```
