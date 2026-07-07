# RaptorJoin

_`raptorJoinFeature` performs a spatial join between a raster dataset and a set of vector features, returning information about the pixels that intersect with…_

**Receiver:** static object — call `RaptorJoin.<method>(...)`

**Members** (most robust first): ★ `raptorJoinFeature` **(primary)**, ★ `raptorJoinIDFull`

---

## API Test: `raptorJoinFeature`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def raptorJoinFeature[T](raster: RasterRDD[T], features: RDD[IFeature], opts: BeastOptions = new BeastOptions(), numTiles: LongAccumulator = null): RDD[RaptorJoinFeature[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:73_

_Source doc:_ Performs a raptor join between a raster RDD and a set of features. The output contains information about all pixels that match with the set of features. @param raster the raster RDD that contains all the tiles to test @param features the set of features to join with the raster data @param opts additional options for the query processor @param numTiles an optional accumulator to count the number of tiles accesses during the query processing. @tparam T the type of the pixel values @return the set of overlaps between pixels and features

### Goal
`raptorJoinFeature` performs a spatial join between a raster dataset and a set of vector features, returning information about the pixels that intersect with the features.

### Parameters
- `raster` (`RasterRDD[T]`): The raster RDD containing the pixel data to be tested against the features. The pixel type `T` must be specified based on the raster data being processed (e.g., `Int`, `Float`).
- `features` (`RDD[IFeature]`): The RDD of vector features (e.g., polygons, points) that will be joined with the raster data. Each feature should implement the `IFeature` interface.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options for the query processor, allowing customization of the join operation (e.g., spatial predicates, output configurations).
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator that counts the number of tiles accessed during the query processing, useful for performance monitoring.

### Input
The caller must provide:
- A raster dataset loaded as `RasterRDD[T]`, which can be obtained from a GeoTIFF or other supported raster formats.
- A set of vector features loaded as `RDD[IFeature]`, which can be sourced from shapefiles, GeoJSON, or other vector formats.
- Ensure that the raster and features are in compatible coordinate reference systems (CRS) for accurate spatial joins.

### Output
Returns `RDD[RaptorJoinFeature[T]]` — an RDD containing the results of the join, where each element represents a pixel from the raster that overlaps with a feature, including relevant information about the feature and pixel.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val features: RDD[IFeature] = sc.shapefile("ne_10m_admin_0_countries.zip")
val result: RDD[RaptorJoinFeature[Int]] = RaptorJoin.raptorJoinFeature(raster, features)
```

### LLM Instruction Prompt
- When calling `raptorJoinFeature`, ensure that the raster and features are properly loaded and compatible in terms of CRS. Specify the pixel type `T` based on the raster data.

### Prompt Snippet
```text
To perform a raptor join between a raster and vector features, use the following pattern:
val result = RaptorJoin.raptorJoinFeature(raster, features)
```

### Common Failure Modes
- **[compile]** error: value shapefile is not a member of org.apache.spark.SparkContext _(seen 8x)_
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 4x)_
- **[compile]** error: not found: value sparkContext _(seen 4x)_
- **[compile]** error: value readCSVPoint is not a member of org.apache.spark.SparkContext _(seen 4x)_
- **[compile]** error: object dynoviz is not a member of package edu.ucr.cs.bdlab _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the raster and features are loaded correctly and that their coordinate reference systems match. Check the pixel type `T` to ensure it corresponds to the raster data being processed.
```

## API Test: `raptorJoinIDFull`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def raptorJoinIDFull[T](raster: RDD[ITile[T]], vector: RDD[(Long, IFeature)], opts: BeastOptions, numTiles: LongAccumulator = null, numRanges: LongAccumulator = null) : RDD[RaptorJoinResult[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180_

_Source doc:_ A Raptor join implementation that returns all the matches between features and pixels along with the raster metadata that puts the pixel in context. @param raster the RDD that contains the raster tiles @param vector the RDD that contains the vector features and their unique IDs @param opts additional options for the query processor @tparam T the type of the pixel values @return RDD that contains all overlaps between pixels and geometries

### Goal
`raptorJoinIDFull` performs a Raptor join between raster tiles and vector features, returning all matches along with the relevant raster metadata.

### Parameters
- `raster` (`RDD[ITile[T]]`): An RDD containing raster tiles, where each tile represents a portion of the raster data with pixel values of type `T`.
- `vector` (`RDD[(Long, IFeature)]`): An RDD containing vector features, where each feature is associated with a unique ID (of type `Long`) and represented as an `IFeature`.
- `opts` (`BeastOptions`): An instance of `BeastOptions` that provides additional configuration options for the join operation, such as spatial indexing or query parameters.
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator to track the number of tiles processed during the join operation.
- `numRanges` (`LongAccumulator`), default `null`: An optional accumulator to track the number of ranges processed during the join operation.

### Input
The caller must provide:
- An RDD of raster tiles loaded from a GeoTIFF or HDF file, ensuring the pixel type matches the expected type `T`.
- An RDD of vector features, which can be loaded from formats such as Shapefile or GeoJSON.
- A valid `BeastOptions` instance to configure the join operation.

### Output
Returns `RDD[RaptorJoinResult[T]]` — an RDD containing `RaptorJoinResult` objects that represent the overlaps between raster pixels and vector geometries, including the pixel's metadata for context.

### Valid Call Patterns
```scala
val rasterFile = makeFileCopy("/raptor/glc2000_small.tif").getPath
val testPoly = factory.toGeometry(new Envelope(-82.76, -80.25, 31.91, 35.17))
val vector: RDD[(Long, IFeature)] = sparkContext.parallelize(Seq((1L, Feature.create(null, testPoly))))
val raster: RasterFileRDD[Int] = new RasterFileRDD[Int](sparkContext, rasterFile, new BeastOptions())

val values: RDD[RaptorJoinResult[Int]] = RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
```

### LLM Instruction Prompt
- When calling `raptorJoinIDFull`, ensure that the raster and vector RDDs are properly initialized and that the pixel type `T` is correctly specified based on the raster data.

### Prompt Snippet
```text
To perform a Raptor join between raster tiles and vector features, use the `raptorJoinIDFull` function with the appropriate RDDs and options.
```

### Common Failure Modes
- **[compile]** error: not found: value sparkContext _(seen 8x)_
- **[compile]** error: overloaded method value readInput with alternatives:

### Fix Code Hint
```scala
Ensure that the raster and vector RDDs are correctly populated and that the `BeastOptions` are set according to the requirements of the join operation.
```
