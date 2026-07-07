# IndexHelper

_Constructs a spatial partitioner for a given set of features to optimize the distribution of spatial data across partitions in a Spark job._

**Receiver:** static object — call `IndexHelper.<method>(...)`

**Members** (most robust first): ⚠️ `createPartitioner` **(primary)**, ⚠️ `partitionFeatures`, ⚠️ `partitionFeatures2`, ⚠️ `runDuplicateAvoidance`, ⚠️ `saveIndex2`

---

## API Test: `createPartitioner`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def createPartitioner(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: NumPartitions, sizeFunction: IFeature=>Int, opts: BeastOptions ): SpatialPartitioner
def createPartitioner(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], pcriterion: String, pvalue: Long, sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int] = {_.getStorageSize}, opts: BeastOptions ): SpatialPartitioner
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:136  (+1 more definition site/overload)_

_Source doc:_ Constructs a spatial partitioner for the given features. Returns an instance of the spatial partitioner class that is given which is initialized based on the given features. @param features the features to create the partitioner on @param partitionerClass the class of the partitioner to construct @param numPartitions the desired number of partitions (this is just a loose hint not a strict number) @param sizeFunction a function that calculates the size of each feature for load balancing. Only needed if the partition criterion is specified through partition size [[Size]] @return a constructed spatial partitioner

### Goal
Constructs a spatial partitioner for a given set of features to optimize the distribution of spatial data across partitions in a Spark job.

### Parameters
- `features` (`SpatialRDD`): The spatial features on which the partitioner will be based. This should be a valid `SpatialRDD` containing the spatial data to be partitioned.
- `partitionerClass` (`Class[_ <: SpatialPartitioner], numPartitions: NumPartitions, sizeFunction: IFeature=>Int`): The class of the spatial partitioner to construct, along with the desired number of partitions and a function that calculates the size of each feature for load balancing.
- `opts` (`BeastOptions`): Options for configuring the behavior of the partitioner, such as spatial partitioning criteria.

### Input
The caller must provide a valid `SpatialRDD` containing spatial features, a class type for the partitioner, a `NumPartitions` instance indicating the desired number of partitions, a size function for load balancing, and any additional options encapsulated in `BeastOptions`.

### Output
Returns `SpatialPartitioner` — an instance of the specified spatial partitioner class, initialized based on the provided features, which will be used to manage the distribution of spatial data across partitions.

### Valid Call Patterns
```scala
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, new BeastOptions())
```

### LLM Instruction Prompt
When calling `createPartitioner`, ensure that the `features` parameter is a valid `SpatialRDD`, the `partitionerClass` is a subclass of `SpatialPartitioner`, and the `numPartitions` is specified correctly. The `sizeFunction` should be a function that takes an `IFeature` and returns an integer representing its size.

### Prompt Snippet
```text
Create a spatial partitioner using the provided features and partitioner class, ensuring the size function is defined for load balancing.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the features are properly initialized and that the partitioner class is valid.
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), feature => feature.getStorageSize, new BeastOptions())
```

## API Test: `partitionFeatures`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def partitionFeatures(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaPairRDD[Integer, IFeature]
def partitionFeatures(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaPartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:413  (+3 more definition site/overload)_

### Goal
The `partitionFeatures` function partitions a set of spatial features into a spatially indexed structure, optimizing for spatial queries and operations.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features that need to be partitioned. This can include points, lines, or polygons represented as `IFeature` objects.
- `partitionerClass` (`Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int`): The class of the spatial partitioner to be used for partitioning the features, along with a size function that determines the size of each feature. This helps in distributing the features evenly across partitions.
- `opts` (`BeastOptions`): Configuration options for the partitioning process, which may include parameters like the number of partitions or specific behaviors of the partitioning algorithm.

### Input
The input must consist of a valid `SpatialRDD` containing spatial features. The `partitionerClass` must be a valid subclass of `SpatialPartitioner`, and the `sizeFunction` must be a function that can compute an integer size for each `IFeature`. The `opts` parameter should be an instance of `BeastOptions` with any necessary configurations set.

### Output
Returns `PartitionedSpatialRDD` — a spatially partitioned representation of the input features, which allows for efficient spatial queries and operations on the dataset.

### Valid Call Patterns
```scala
val geometryFactor: GeometryFactory = FeatureReader.DefaultGeometryFactory
val features = sparkContext.parallelize(Seq[IFeature](
  Feature.create(null, new PointND(geometryFactor, 2, 0, 0)),
  Feature.create(null, new PointND(geometryFactor, 2, 1, 1)),
  Feature.create(null, new PointND(geometryFactor, 2, 3, 1)),
  Feature.create(null, new PointND(geometryFactor, 2, 1, 4))
))
val partitionedFeatures: JavaPartitionedSpatialRDD =
  IndexHelper.partitionFeatures(JavaRDD.fromRDD(features), classOf[RSGrovePartitioner],
  new org.apache.spark.api.java.function.Function[IFeature, Int]() {
    override def call(v1: IFeature): Int = 1
  }, new BeastOptions())
```

### LLM Instruction Prompt
When calling `partitionFeatures`, ensure that the `features` parameter is a valid `SpatialRDD` or `JavaSpatialRDD`, the `partitionerClass` is a valid subclass of `SpatialPartitioner`, and the `sizeFunction` is correctly defined to return an integer for each feature.

### Prompt Snippet
```text
To partition spatial features, use the `partitionFeatures` function with a valid `SpatialRDD`, a suitable `SpatialPartitioner` class, and a size function that computes the size of each feature.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the `features` parameter is a properly initialized `SpatialRDD` and that the `partitionerClass` and `sizeFunction` are correctly implemented to match the expected types.
```

## API Test: `partitionFeatures2`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def partitionFeatures2(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaSpatialRDD
def partitionFeatures2(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:429  (+3 more definition site/overload)_

_Source doc:_ Partitions the given features using a partitioner of the given type. This method first initializes the partitioner and then uses this initialized partitioner to partition the data. @param features the set of features to spatially partition @param partitionerClass the type of the spatial partition @param sizeFunction the function used to compute the size @param opts additional options @return the same set of input features after they are partitioned.

### Goal
`partitionFeatures2` partitions a set of spatial features into a specified number of partitions using a defined spatial partitioner, facilitating efficient spatial data processing in distributed environments.

### Parameters
- `features` (`SpatialRDD`): The set of spatial features that need to be partitioned. This should be a distributed dataset containing geometrical data points or shapes.
- `partitionerClass` (`Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int`): The class type of the spatial partitioner to be used for partitioning the features, along with a function that computes the size of each feature, which helps in determining how to distribute the features across partitions.
- `opts` (`BeastOptions`): Additional options that can be specified to customize the partitioning process, such as configuration settings or parameters that influence the behavior of the partitioner.

### Input
The caller must provide a `SpatialRDD` containing spatial features. The `partitionerClass` must be a valid subclass of `SpatialPartitioner`, and the `sizeFunction` must be a function that takes an `IFeature` and returns an integer representing its size. The `opts` parameter should be an instance of `BeastOptions` containing any necessary configuration.

### Output
Returns `SpatialRDD` — a partitioned set of input features, where the features are distributed across the specified number of partitions based on the spatial partitioner used.

### Valid Call Patterns
```scala
val dataset = new RandomSpatialRDD(sparkContext, UniformDistribution, 10000, opts = Seq("maxSize" -> "0.1,0.1", "geometry" -> "box"))
val partitionedFeatures: SpatialRDD = IndexHelper.partitionFeatures2(dataset, new GridPartitioner(unitsquare, Array(3, 3)), feature => 1, BeastOptions())
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` and that the `partitionerClass` is a valid subclass of `SpatialPartitioner`. The `sizeFunction` must be correctly defined to compute the size of each feature.

### Prompt Snippet
```text
To partition spatial features, call `partitionFeatures2` with a valid `SpatialRDD`, a spatial partitioner class, a size function, and any additional options as `BeastOptions`.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the `features` parameter is a properly initialized `SpatialRDD`, and verify that the `partitionerClass` and `sizeFunction` are correctly implemented and compatible with the input features.
```

## API Test: `runDuplicateAvoidance`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[beast] def runDuplicateAvoidance(features: SpatialRDD): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:354_

_Source doc:_ Run the duplicate avoidance technique on the given set of features if it is spatially partitioned using a disjoint partitioner. Otherwise, the input set is returned as-is. @param features the set of features to remove the duplicates from. @return a set of features with all duplicates removed.

### Goal
The `runDuplicateAvoidance` function removes duplicate features from a spatially partitioned `SpatialRDD`, ensuring that the output contains only unique features.

### Parameters
- `features` (`SpatialRDD`): A set of spatial features from which duplicates need to be removed. This input should be spatially partitioned using a disjoint partitioner for the duplicate avoidance technique to be applied effectively.

### Input
The input must be a `SpatialRDD` that is spatially partitioned. If the input is not partitioned correctly, the function will return the input set as-is. The `SpatialRDD` should contain spatial features that may have duplicates.

### Output
Returns `SpatialRDD` — a new set of spatial features with all duplicates removed, provided that the input was appropriately partitioned. If the input was not partitioned, the original `SpatialRDD` is returned unchanged.

### Valid Call Patterns
```scala
val uniqueFeatures = IndexHelper.runDuplicateAvoidance(partitioned1)
```

### LLM Instruction Prompt
- Ensure that the input `SpatialRDD` is spatially partitioned using a disjoint partitioner before calling `runDuplicateAvoidance`. If the input is not partitioned, the function will return the input as-is.

### Prompt Snippet
```text
To remove duplicates from a spatially partitioned set of features, use the following call:
val uniqueFeatures = IndexHelper.runDuplicateAvoidance(partitioned1)
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 3x)_
- **[compile]** error: overloaded method value readInput with alternatives:

### Fix Code Hint
```scala
Ensure that the `SpatialRDD` is partitioned using a disjoint partitioner before invoking `runDuplicateAvoidance` to effectively remove duplicates.
```

## API Test: `saveIndex2`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def saveIndex2(partitionFeatures: SpatialRDD, path: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:541_

_Source doc:_ Saves a partitioned RDD to disk. Each partition is stored to a separate file and an additional master file that stores the partition information. @param partitionFeatures a set of partitioned features @param path the path to store the files @param opts additional options for storing the data

### Goal
`saveIndex2` saves a partitioned RDD of spatial features to disk, creating separate files for each partition along with a master file for partition information.

### Parameters
- `partitionFeatures` (`SpatialRDD`): A set of partitioned spatial features that are to be saved. This RDD must be partitioned using a spatial partitioner.
- `path` (`String`): The file path where the partitioned files will be stored. This path must be accessible and writable.
- `opts` (`BeastOptions`): Additional options for storing the data, which may include format specifications or other storage parameters.

### Input
The caller must provide a `SpatialRDD` that has been partitioned, a valid file path as a `String`, and a `BeastOptions` instance with any necessary options for the save operation. The input RDD must be partitioned using a spatial partitioner to ensure proper file organization.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output consists of multiple files saved to the specified path, including individual files for each partition and a master file containing partition metadata.

### Valid Call Patterns
```scala
IndexHelper.saveIndex2(partitionedFeatures, outPath.getPath, "oformat" -> "wkt(0)")
```

### LLM Instruction Prompt
- Ensure that `partitionFeatures` is a properly partitioned `SpatialRDD` before calling `saveIndex2`.
- Verify that the `path` provided is valid and writable.
- Use appropriate `BeastOptions` to specify any additional storage parameters.

### Prompt Snippet
```text
To save a partitioned RDD of spatial features, use the `saveIndex2` method with the appropriate parameters.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the RDD is partitioned using a spatial partitioner and that the output path is valid and writable before calling `saveIndex2`.
```
