# SpatialJoin

_`spatialJoin` performs a spatial join operation between two `SpatialRDD` datasets, returning pairs of matching features based on a specified join predicate._

**Receiver:** static object — call `SpatialJoin.<method>(...)`

**Members** (most robust first): ⚠️ `spatialJoin` **(primary)**, ⚠️ `spatialJoinBNLJ`, ⚠️ `spatialJoinDJ`, ⚠️ `spatialJoinIntersectsPlaneSweepFeatures`, ⚠️ `spatialJoinPBSM`, ⚠️ `spatialJoinRepJ`

---

## API Test: `spatialJoin`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialJoin(rdd2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, method: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(partitionedRDD2: PartitionedSpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, mbrCount: LongAccumulator = null): RDD[(IFeature, IFeature)]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD, predicate: SpatialJoinAlgorithms.ESJPredicate, algorithm: SpatialJoinAlgorithms.ESJDistributedAlgorithm): JavaPairRDD[IFeature, IFeature]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD): JavaPairRDD[IFeature, IFeature]
def spatialJoin(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, joinMethod: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, joinMethod: ESJDistributedAlgorithm, mbrCount: LongAccumulator, opts: BeastOptions): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:146  (+5 more definition site/overload)_

_Source doc:_ The main entry point for spatial join operations. Performs a spatial join between the given two inputs and returns an RDD of pairs of matching features. This method is a transformation. However, if the [[ESJDistributedAlgorithm.PBSM]] is used, the MBR of the two inputs has to be calculated first which runs a reduce action on each dataset even if the output of the spatial join is not used. You can specify a specific spatial join method through the [[joinMethod]] parameter. If not specified, an algorithm will be picked automatically based on the following rules. - If both datasets are spatially partitioned, the distributed join [[ESJDistributedAlgorithm.DJ]] algorithm is used. - If the product of the number of partitions of both datasets is less than [[SparkContext.defaultParallelism]], then the block nested loop join is used [[ESJDistributedAlgorithm.BNLJ]] - If at least one dataset is partition, then the repartition join is used [[ESJDistributedAlgorithm.REPJ]] - If none of the above, then the partition based spatial merge join is used [[ESJDistributedAlgorithm.PBSM]] @param r1 the first (left) dataset @param r2 the second (right) dataset @param joinPredicate the join predicate. The default is [[ESJPredicate.Intersects]] which finds all non-disjoint features @param joinMethod the join algorithm. If not specified the algorithm automatically chooses an algorithm based on the heuristic described above. @param mbrCount an (optional) accumulator to count the number of MBR tests during the algorithm. @return an RDD that contains pairs of matching features.

### Goal
`spatialJoin` performs a spatial join operation between two `SpatialRDD` datasets, returning pairs of matching features based on a specified join predicate.

### Parameters
- `r1` (`SpatialRDD`): The first (left) dataset containing spatial features to be joined.
- `r2` (`SpatialRDD`): The second (right) dataset containing spatial features to be joined.
- `joinPredicate` (`ESJPredicate`), default `ESJPredicate.Intersects`: The condition used to determine how features from the two datasets are matched. The default is to find all non-disjoint features.
- `joinMethod` (`ESJDistributedAlgorithm`), default `null`: The algorithm used for the spatial join. If not specified, an appropriate algorithm is chosen based on the characteristics of the input datasets.
- `mbrCount` (`LongAccumulator`), default `null`: An optional accumulator to count the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for configuring the behavior of the spatial join operation.

### Input
The input consists of two `SpatialRDD` datasets that must be properly formatted and accessible. Both datasets should ideally be spatially partitioned for optimal performance, but the function can handle unpartitioned datasets as well.

### Output
Returns `RDD[(IFeature, IFeature)]` — an RDD containing pairs of matching features from the two input datasets based on the specified join predicate.

### Valid Call Patterns
```scala
val joinResults = dataset1.spatialJoin(dataset2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)
val sjResults: RDD[(IFeature, IFeature)] =
      matchedPolygons.spatialJoin(matchedPoints, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)
```

### LLM Instruction Prompt
- Ensure that both input datasets are of type `SpatialRDD` and are accessible before calling `spatialJoin`. Use appropriate join predicates and methods based on the characteristics of the datasets.

### Prompt Snippet
```text
To perform a spatial join, ensure both datasets are loaded as SpatialRDDs and specify the desired join predicate and method if necessary.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
Ensure both datasets are of type SpatialRDD and check the join predicate and method for compatibility with your data.
```

## API Test: `spatialJoinBNLJ`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialJoinBNLJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null) : RDD[(IFeature, IFeature)]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:418  (+2 more definition site/overload)_

_Source doc:_ Runs a spatial join between the two given RDDs using the block-nested-loop join algorithm. @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @return

### Goal
`spatialJoinBNLJ` performs a spatial join between two `SpatialRDD` datasets using a block-nested-loop join algorithm, allowing for the combination of features based on spatial relationships.

### Parameters
- `r1` (`SpatialRDD`): The first set of spatial features to be joined. This RDD should contain geometries that will be evaluated against the geometries in `r2`.
- `r2` (`SpatialRDD`): The second set of spatial features to be joined. This RDD should also contain geometries that will be evaluated against those in `r1`.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the spatial relationship used to join features from `r1` and `r2`. Common predicates include spatial relationships like intersection or containment.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of minimum bounding rectangle (MBR) tests performed during the join operation. This can be useful for performance monitoring.

### Input
The caller must provide two `SpatialRDD` instances (`r1` and `r2`) containing spatial features, along with a valid `joinPredicate`. The input RDDs must be properly formatted and accessible within the Spark context. Ensure that the geometries in both RDDs are compatible with the specified join predicate.

### Output
Returns `RDD[(IFeature, IFeature)]` — a distributed collection of pairs of features, where each pair consists of one feature from `r1` and one feature from `r2` that satisfy the specified `joinPredicate`. The output represents the results of the spatial join operation.

### Valid Call Patterns
```scala
val results = SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate = ESJPredicate.MBRIntersects)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are instances of `SpatialRDD` containing valid geometries.
- Specify a valid `joinPredicate` that defines the spatial relationship for the join.
- Optionally provide a `LongAccumulator` for tracking MBR tests.

### Prompt Snippet
```text
To perform a spatial join using the block-nested-loop join algorithm, call `spatialJoinBNLJ` with two `SpatialRDD` instances and a valid `joinPredicate`.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
Ensure that both `r1` and `r2` contain valid geometries and that the `joinPredicate` is appropriate for the types of geometries being joined.
```

## API Test: `spatialJoinDJ`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialJoinDJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:461_

_Source doc:_ Distributed join algorithm between spatially partitioned RDDs @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @param numMBRTests   a counter that will contain the number of MBR tests @return a pair RDD for joined features

### Goal
`spatialJoinDJ` performs a distributed join operation between two spatially partitioned RDDs based on a specified join predicate.

### Parameters
- `r1` (`SpatialRDD`): The first set of spatial features to be joined. This RDD should contain geometries that will be evaluated against the second RDD.
- `r2` (`SpatialRDD`): The second set of spatial features to be joined. This RDD should also contain geometries that will be evaluated against the first RDD.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the criteria for joining features from `r1` with features in `r2`. This predicate determines how the geometries in the two RDDs relate to each other.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional counter that tracks the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation. This can be useful for performance monitoring.

### Input
The caller must provide two `SpatialRDD` instances containing spatial features. The geometries in these RDDs should be compatible with the join predicate specified. There are no specific file formats required for the input, but the RDDs must be properly initialized and populated with spatial data.

### Output
Returns `RDD[(IFeature, IFeature)]` — a pair RDD containing tuples of joined features from `r1` and `r2`. Each tuple consists of an `IFeature` from the first RDD and an `IFeature` from the second RDD that satisfy the join predicate.

### Valid Call Patterns
```scala
val joinedFeatures: RDD[(IFeature, IFeature)] = value.spatialJoinDJ(r1, r2, joinPredicate)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are initialized as `SpatialRDD` instances containing spatial features. The `joinPredicate` must be defined to specify how the features should be joined.

### Prompt Snippet
```text
Call `spatialJoinDJ` with two initialized `SpatialRDD` instances and a valid `ESJPredicate` to perform a spatial join.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Ensure both RDDs are initialized and the join predicate is correctly defined
val r1: SpatialRDD = ...
val r2: SpatialRDD = ...
val joinPredicate: ESJPredicate = ...
val numMBRTests: LongAccumulator = sparkContext.longAccumulator("MBR Tests")

val joinedFeatures: RDD[(IFeature, IFeature)] = value.spatialJoinDJ(r1, r2, joinPredicate, numMBRTests)
```

## API Test: `spatialJoinIntersectsPlaneSweepFeatures`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[beast] def spatialJoinIntersectsPlaneSweepFeatures[T1 <: IFeature, T2 <: IFeature] (r: Array[T1], s: Array[T2], dupAvoidanceMBR: EnvelopeNDLite, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): TraversableOnce[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:244_

_Source doc:_ Runs a plane-sweep algorithm between the given two arrays of input features and returns an iterator of pairs of features. @param r the first set of features @param s the second set of features @param dupAvoidanceMBR the duplicate avoidance MBR to run the reference point technique. @param joinPredicate the join predicate to match features @param numMBRTests an (optional) accumulator to count the number of MBR tests @tparam T1 the type of the first dataset @tparam T2 the type of the second dataset @return an iterator over pairs of features

### Goal
The `spatialJoinIntersectsPlaneSweepFeatures` function performs a spatial join between two sets of features using a plane-sweep algorithm, identifying pairs of features that intersect based on a specified join predicate.

### Parameters
- `r` (`Array[T1]`): An array of features representing the first dataset to be joined. Each feature must implement the `IFeature` interface.
- `s` (`Array[T2]`): An array of features representing the second dataset to be joined. Each feature must also implement the `IFeature` interface.
- `dupAvoidanceMBR` (`EnvelopeNDLite`): A minimum bounding rectangle (MBR) used to avoid duplicate feature matches during the join process. It defines the spatial extent within which to check for intersections.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the criteria for joining features. It specifies how the features from the two datasets should be compared (e.g., whether they intersect).
- `numMBRTests` (`LongAccumulator`): An optional accumulator that counts the number of MBR tests performed during the join operation. This can be used for performance monitoring.

### Input
The caller must provide two arrays of features (`r` and `s`) that are compatible with the `IFeature` interface. The `dupAvoidanceMBR` must be defined to cover the spatial extent of interest, and the `joinPredicate` must be specified to determine how features are matched. The `numMBRTests` can be provided as `null` if not needed.

### Output
Returns `TraversableOnce[(IFeature, IFeature)]` — an iterator over pairs of features that intersect according to the specified join predicate. Each pair consists of one feature from the first dataset and one from the second dataset.

### Valid Call Patterns
```scala
val r = List(
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 10.0, 10.0, 10.1, 10.1)),
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 3.0, 1.0, 5.0, 3.0))
)
val s = List(
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 2.0, 0.0, 4.0, 2.0))
)
val results = SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(r.toArray, s.toArray,
  new EnvelopeNDLite(2, 2.0, 0.0, 5.0, 3.0), ESJPredicate.Intersects, null)
```

### LLM Instruction Prompt
When calling `spatialJoinIntersectsPlaneSweepFeatures`, ensure that both input arrays contain features that implement the `IFeature` interface, and provide a valid `dupAvoidanceMBR` and `joinPredicate`.

### Prompt Snippet
```text
Call `spatialJoinIntersectsPlaneSweepFeatures` with two arrays of features, a duplicate avoidance MBR, and a join predicate to find intersecting feature pairs.
```

### Common Failure Modes
- **[compile]** error: method spatialJoinIntersectsPlaneSweepFeatures in object SpatialJoin cannot be accessed in object edu.ucr.cs.bdlab.beast.operations.SpatialJoin _(seen 3x)_
- **[compile]** error: object GeometryFactory is not a member of package edu.ucr.cs.bdlab.beast.geolite

### Fix Code Hint
```scala
Ensure that both input arrays contain valid `IFeature` instances and that the `dupAvoidanceMBR` is appropriately defined to encompass the area of interest.
```

## API Test: `spatialJoinPBSM`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialJoinPBSM(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate) : JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:297  (+2 more definition site/overload)_

_Source doc:_ Performs a partition-based spatial-merge (PBSM) join as explained in the following paper. Jignesh M. Patel, David J. DeWitt: Partition Based Spatial-Merge Join. SIGMOD Conference 1996: 259-270 https://doi.org/10.1145/233269.233338 @param r1            the first dataset @param r2            the second dataset @param joinPredicate the join predicate @param numMBRTests   (output) the number of MBR tests done during the algorithm @param opts          Additional options for the PBSM algorithm @return a pair RDD for joined features

### Goal
`spatialJoinPBSM` performs a partition-based spatial-merge join between two spatial datasets, allowing for efficient spatial queries and analysis.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset to be joined, which contains features with spatial attributes.
- `r2` (`SpatialRDD`): The second spatial dataset to be joined, which also contains features with spatial attributes.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the spatial relationship required for the join (e.g., intersection, containment).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of minimum bounding rectangle (MBR) tests performed during the join operation.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options for configuring the PBSM algorithm, allowing for customization of the join process.

### Input
The input consists of two `SpatialRDD` datasets, each containing spatial features. The datasets must be properly formatted and accessible in the Spark context. The `joinPredicate` must be a valid spatial relationship defined by the `ESJPredicate` enumeration.

### Output
Returns `RDD[(IFeature, IFeature)]` — a pair RDD containing the joined features from both datasets that satisfy the specified join predicate.

### Valid Call Patterns
```scala
val geometryFactory = GeometryReader.DefaultGeometryFactory
val dataset1: SpatialRDD = sparkContext.parallelize(Seq(
  Feature.create(null, new PointND(geometryFactory, 2, 1.0, 1.0))
))
val dataset2: SpatialRDD = sparkContext.parallelize(Seq(
  Feature.create(null, new EnvelopeND(geometryFactory, 2, 0.0, 0.0, 2.0, 2.0))
))
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

### LLM Instruction Prompt
- Ensure that both input datasets are of type `SpatialRDD` and contain valid spatial features. The `joinPredicate` must be a valid spatial relationship from the `ESJPredicate` enumeration.

### Prompt Snippet
```text
To perform a spatial join using the PBSM method, ensure you have two SpatialRDD datasets and a valid join predicate. Call the spatialJoinPBSM function with these parameters.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that both datasets are populated and the join predicate is correctly defined.
val dataset1: SpatialRDD = // Load or create your first dataset
val dataset2: SpatialRDD = // Load or create your second dataset
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

## API Test: `spatialJoinRepJ`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialJoinRepJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:488_

_Source doc:_ Repartition join algorithm between two datasets: r1 is spatially disjoint partitioned and r2 is not @param r1 the first dataset @param r2 the second dataset @param joinPredicate the join predicate @param numMBRTests an optional accumulator that counts the number of MBR tests @return an RDD of pairs of matching features

### Goal
`spatialJoinRepJ` performs a repartition join between two spatial datasets, where the first dataset is spatially disjoint partitioned, allowing for efficient matching of features based on a specified join predicate.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset that is partitioned in a way that ensures its features do not overlap spatially.
- `r2` (`SpatialRDD`): The second spatial dataset that may contain overlapping features with `r1`.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the conditions under which features from `r1` and `r2` should be joined.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation.

### Input
The caller must provide two `SpatialRDD` datasets (`r1` and `r2`) that are properly formatted and accessible. The `joinPredicate` must be defined to specify the criteria for joining features. The `numMBRTests` is optional and can be used for performance monitoring.

### Output
Returns `RDD[(IFeature, IFeature)]` — an RDD containing pairs of matching features from `r1` and `r2` based on the specified join predicate.

### Valid Call Patterns
```scala
val result: RDD[(IFeature, IFeature)] = value.spatialJoinRepJ(r1, r2, joinPredicate)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are `SpatialRDD` types and that `joinPredicate` is properly defined before calling `spatialJoinRepJ`. Optionally, provide a `LongAccumulator` for `numMBRTests` to track performance metrics.

### Prompt Snippet
```text
To perform a spatial join between two datasets, use the spatialJoinRepJ function with the appropriate SpatialRDDs and a join predicate.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the first dataset `r1` is partitioned correctly and that the `joinPredicate` is valid before invoking spatialJoinRepJ.
```
