## API Test: `partitionFeatures2`
_Grounding: doc-repaired from source (docfix)._

### Goal
Spatially repartition a vector `SpatialRDD` using a Beast `SpatialPartitioner` (such as `RSGrovePartitioner`) so downstream distributed spatial operations run on partitioned data. The recommended overload automatically computes the correct data bounds to prevent data loss.

### Valid Call Patterns
**REQUIRED IMPORTS & TYPES:**
- requires `edu.ucr.cs.bdlab.beast.indexing.IndexHelper` — a Scala object.
- requires `edu.ucr.cs.bdlab.beast.indexing.RSGrovePartitioner` — a Scala class; reference as `classOf[RSGrovePartitioner]`.
- requires `edu.ucr.cs.bdlab.beast.geolite.IFeature` — a Scala trait.
- requires `edu.ucr.cs.bdlab.beast.common.BeastOptions` — a Scala class.

```scala
import edu.ucr.cs.bdlab.beast.indexing.{IndexHelper, RSGrovePartitioner}
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// Automatically computes data bounds via createPartitioner
val partitioned = IndexHelper.partitionFeatures2(
  featuresRDD,
  classOf[RSGrovePartitioner],
  (f: IFeature) => 1,
  new BeastOptions()
)
```

### LLM Instruction Prompt
- Do not use hardcoded bounding boxes (like `EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0)`) when manually initializing a partitioner. It will drop features outside those bounds and result in an empty RDD.
- Prefer the `partitionFeatures2` overload that takes a `partitionerClass` (e.g., `classOf[RSGrovePartitioner]`), a size function (e.g., `(f: IFeature) => 1`), and `BeastOptions`. This overload automatically computes the correct data bounds and initializes the partitioner.
- `RSGrovePartitioner` is located in the `edu.ucr.cs.bdlab.beast.indexing` package.

### Prompt Snippet
```text
Given an existing SpatialRDD named `featuresRDD`, repartition it using `IndexHelper.partitionFeatures2`. Pass `classOf[RSGrovePartitioner]`, a size function `(f: IFeature) => 1`, and `new BeastOptions()` so Beast automatically computes the correct data bounds. Include all required imports.
```

### Common Failure Modes
- **Empty RDD due to hardcoded bounds:** Instantiating a `GridPartitioner` (or similar) with a hardcoded bounding box that does not intersect the actual geometries in the `featuresRDD`. Any features outside the partitioner's envelope are dropped, resulting in an empty RDD.
- **Missing Imports:** Failing to import `RSGrovePartitioner`, `IFeature`, or `BeastOptions` when using the class-based overload.

### Fix Code Hint
```scala
// WRONG: Hardcoded bounds drop features outside the envelope, resulting in an empty RDD
val partitioned = IndexHelper.partitionFeatures2(
  featuresRDD,
  new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2))
)

// CORRECT: Pass the partitioner class and let Beast compute the bounds automatically
val partitioned = IndexHelper.partitionFeatures2(
  featuresRDD,
  classOf[edu.ucr.cs.bdlab.beast.indexing.RSGrovePartitioner],
  (f: edu.ucr.cs.bdlab.beast.geolite.IFeature) => 1,
  new edu.ucr.cs.bdlab.beast.common.BeastOptions()
)
```