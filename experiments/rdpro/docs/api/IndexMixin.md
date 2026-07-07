# IndexMixin

_The `partitionBy` function is used to reorganize a spatial RDD into partitions based on a specified spatial partitioning strategy, optimizing spatial queries…_

**Receiver:** instance — obtain a `IndexMixin` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `partitionBy` **(primary)**

---

## API Test: `partitionBy`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def partitionBy(spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionBy(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): PartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:35  (+1 more definition site/overload)_

### Goal
The `partitionBy` function is used to reorganize a spatial RDD into partitions based on a specified spatial partitioning strategy, optimizing spatial queries and operations.

### Parameters
- `spatialPartitioner` (`SpatialPartitioner`): An instance of a spatial partitioner that defines how the data should be divided into partitions. This can include various partitioning strategies such as grid or quad-tree partitioning.

### Input
The caller must provide a `SpatialRDD` that has been previously loaded from a supported format (e.g., CSV points, shapefiles). The input data must be spatially indexed to ensure effective partitioning.

### Output
Returns `PartitionedSpatialRDD` — a spatially partitioned RDD that allows for efficient spatial queries and operations, maintaining the spatial relationships of the data.

### Valid Call Patterns
```scala
val testFile = makeFileCopy("/test111.points")
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val gridPartitioner = new GridPartitioner(data.summary, Array(2, 2))
val partitionedData = data.partitionBy(gridPartitioner)
```

### LLM Instruction Prompt
- When calling `partitionBy`, ensure that the input RDD is a `SpatialRDD` and that a valid `SpatialPartitioner` is provided to optimize the partitioning of the spatial data.

### Prompt Snippet
```text
val partitionedData = data.partitionBy(new GridPartitioner(mbr, Array(2, 2)))
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the input RDD is a `SpatialRDD` and that the `SpatialPartitioner` is correctly instantiated and compatible with the data being processed.
```
