# RasterPartitioner

_The `getPartition` function determines the partition ID associated with a specific tile ID within the raster metadata, facilitating efficient data processing…_

**Receiver:** instance — obtain a `RasterPartitioner` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `getPartition` **(primary)**

---

## API Test: `getPartition`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def getPartition(tile: Any): Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterPartitioner.scala:43_

_Source doc:_ Returns the partition of the given tileID @param tile the tile ID in the input RasterMetadata to return its partition @return the partition ID associated with the given tile

### Goal
The `getPartition` function determines the partition ID associated with a specific tile ID within the raster metadata, facilitating efficient data processing in distributed raster operations.

### Parameters
- `tile` (`Any`): The tile ID for which the partition is being requested. This ID should correspond to a valid tile within the input raster's metadata.

### Input
The caller must provide a valid tile ID that exists within the raster metadata. The input should be part of a raster dataset that has been properly loaded and partitioned using RDPro.

### Output
Returns `Int` — the partition ID associated with the given tile ID, indicating which partition the tile belongs to in the distributed processing framework.

### Valid Call Patterns
```scala
val rasterMetadata = new RasterMetadata(0, 0, 1000, 1000, 100, 100, 4326, new AffineTransform())
val partitioner = new RasterPartitioner(rasterMetadata, 25)
assertResult(0)(partitioner.getPartition(0))
assertResult(0)(partitioner.getPartition(11))
assertResult(24)(partitioner.getPartition(99))
```

### LLM Instruction Prompt
- When calling `getPartition`, ensure that the tile ID provided is valid and corresponds to a tile within the raster metadata. The function should be invoked on an instance of `RasterPartitioner`.

### Prompt Snippet
```text
val partitionId = partitioner.getPartition(tileId)
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the tile ID is valid and corresponds to a tile in the raster metadata before calling getPartition.
val validTileId = 0 // Example of a valid tile ID
val partitionId = partitioner.getPartition(validTileId)
```
