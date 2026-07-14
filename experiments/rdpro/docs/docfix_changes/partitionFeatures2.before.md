## API Test: `partitionFeatures2`

### Signature
```scala
def partitionFeatures2(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaSpatialRDD
def partitionFeatures2(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:429  (+3 more definition site/overload)_

_Source doc:_ Partitions the given features using a partitioner of the given type. This method first initializes the partitioner and then uses this initialized partitioner to partition the data. @param features the set of features to spatially partition @param partitionerClass the type of the spatial partition @param sizeFunction the function used to computed the size @param opts additional options @return the same set of input features after they are partitioned.

### Goal
Spatially repartition a vector `SpatialRDD` using a Beast `SpatialPartitioner` so downstream distributed spatial operations (indexing, joins, queries) run on partitioned data.

### Parameters
- `features` (`SpatialRDD`): The input spatial features (`RDD[IFeature]`) to partition.
- `partitionerClass` (`Class[_ <: SpatialPartitioner],
                        sizeFunction: IFeature=>Int`): In this overload, provide the `SpatialPartitioner` class to initialize, plus a feature-size function used during partitioner initialization.
- `opts` (`BeastOptions`): Additional options used while initializing/configuring partitioning behavior.

### Input
A valid Beast `SpatialRDD` as input (vector features).  
No file path is passed directly to this function; load/create the `SpatialRDD` first (e.g., shapefile/GeoJSON readers or generated features), then call `IndexHelper.partitionFeatures2(...)`.

Preconditions and compatibility notes from project context/tests:
- Use a valid `SpatialPartitioner` (e.g., `GridPartitioner` in tests; `RSGrovePartitioner` is recommended generally in Beast docs).
- If working with replicated/disjoint partitioned data, duplicate handling may be needed in later steps (tests use `IndexHelper.runDuplicateAvoidance(...)`).
- For `-disjoint`-style behavior (context rule), only partitioners that support disjoint partitions can be used.

### Output
Returns `SpatialRDD` — the same logical input features after spatial partitioning is applied, with Spark partitioner metadata set to a `SpatialPartitioner`.

### Valid Call Patterns
```scala
val partitioned1 = IndexHelper.partitionFeatures2(dataset, new GridPartitioner(unitsquare, Array(3, 3)))
val partitioned2 = IndexHelper.partitionFeatures2(partitioned1, new GridPartitioner(unitsquare, Array(5, 5)))
```

```scala
val partitionedFeatures: RDD[IFeature] = IndexHelper.partitionFeatures2(features,
  new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))
```

### LLM Instruction Prompt
- Use the receiver exactly as `IndexHelper.partitionFeatures2(...)` (verified by tests).
- Prefer the tested overload with an initialized `SpatialPartitioner` instance when possible.
- Pass a `SpatialRDD`/`RDD[IFeature]` as the first argument.
- Do not invent options/arguments not present in the signature.
- If disjoint replication is involved, include a duplicate-avoidance step in downstream logic.

### Prompt Snippet
```text
Given an existing SpatialRDD named `features`, repartition it with Beast using:
`IndexHelper.partitionFeatures2(features, new GridPartitioner(...))`.
Return the partitioned SpatialRDD and preserve this exact call shape.
```

### Common Failure Modes
- Passing a non-spatial RDD instead of `SpatialRDD`/`RDD[IFeature]`.
- Using the wrong overload argument shape (e.g., mixing `partitionerClass` form with instantiated partitioner form).
- Using a partitioner/configuration incompatible with requested disjoint behavior (context rule: unsupported disjoint partitioning errors).
- Assuming repartitioning removes duplicates automatically in replicated scenarios; tests explicitly run duplicate avoidance when needed.

### Fix Code Hint
```scala
val partitioned: RDD[IFeature] =
  IndexHelper.partitionFeatures2(features,
    new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))

// Optional downstream safety for replicated/disjoint cases:
val deduped = IndexHelper.runDuplicateAvoidance(partitioned)
```