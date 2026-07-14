## API Test: `numPartitions`
_Grounding: doc-repaired from source (docfix)._

### Goal
Set the number of Spark partitions for a synthetic spatial data generator before materializing the RDD.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.beast.generator.SpatialGeneratorBuilder` — a Scala class; must be instantiated with `new`.

```scala
import edu.ucr.cs.bdlab.beast.generator.SpatialGeneratorBuilder

// 1. Instantiate the builder using 'new' and the SparkContext
val builder = new SpatialGeneratorBuilder(sc)

// 2. Configure partitions (0 defaults to 1 partition per 1M records)
val configured = builder.numPartitions(8)

// 3. Specify distribution and cardinality (Long) to materialize the RDD
val generated = configured.uniform(1000L) 
```

### LLM Instruction Prompt
- `SpatialGeneratorBuilder` is a class, not a companion object. You MUST instantiate it with `new SpatialGeneratorBuilder(sc)`.
- Call `.numPartitions(num: Int)` on the builder instance.
- You MUST specify a distribution and a `cardinality: Long` to actually create the RDD. Do this by calling a distribution method like `.uniform(1000L)`, or by setting `.distribution(...)` followed by `.generate(1000L)`.
- The `.generate` method strictly requires a `cardinality: Long` parameter.

### Prompt Snippet
```text
To generate partitioned synthetic spatial data:
val rdd = new SpatialGeneratorBuilder(sc)
  .numPartitions(8)
  .uniform(1000L) // Sets distribution and cardinality
```

### Common Failure Modes
- **Missing `new` keyword:** Attempting to call `SpatialGeneratorBuilder(sc)` as if it were a companion object with an `apply` method causes compilation failure.
- **Missing cardinality:** Calling `.generate()` without the required `cardinality: Long` parameter causes compilation failure.
- **Missing distribution:** Calling `.generate(1000L)` without first setting a distribution (e.g., via `.distribution(...)` or using a shorthand like `.uniform(1000L)`) throws a runtime requirement error.

### Fix Code Hint
```scala
// WRONG: Missing 'new', missing cardinality, missing distribution
val rdd = SpatialGeneratorBuilder(sc).numPartitions(8).generate()

// CORRECT: Use 'new', and provide distribution + cardinality (Long)
val rdd = new SpatialGeneratorBuilder(sc).numPartitions(8).uniform(1000L)
```