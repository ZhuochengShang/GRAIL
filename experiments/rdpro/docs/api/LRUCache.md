# LRUCache

_The `size` function retrieves the size of a raster dataset in bytes, which is essential for understanding memory usage and data management in geospatial…_

**Receiver:** instance — obtain a `LRUCache` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `size` **(primary)**

---

## API Test: `size`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def size: Long
override def size: Long
override def size: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:41  (+2 more definition site/overload)_

_Source doc:_ Size in bytes

### Goal
The `size` function retrieves the size of a raster dataset in bytes, which is essential for understanding memory usage and data management in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded into the RDPro framework. The dataset should be in a compatible format, such as GeoTIFF, and must be accessible in the Spark environment.

### Output
Returns `Long` — the size of the raster dataset in bytes, representing the total amount of memory used by the dataset.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val sizeInBytes: Long = raster.size
```

### LLM Instruction Prompt
- When calling `size`, ensure that the raster dataset is properly loaded and accessible in the Spark context. The call should be made on a valid raster RDD.

### Prompt Snippet
```text
To get the size of a raster dataset in bytes, use the `size` method on the loaded raster RDD.
```

### Common Failure Modes
- **[compile]** error: value size is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Int]] _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the raster dataset is loaded correctly before calling size
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_geotiff.tif")
val sizeInBytes: Long = raster.size
```
