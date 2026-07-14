## API Test: `numPartitions`

### Signature
```scala
def numPartitions(num: Int): JavaSpatialGeneratorBuilder
def numPartitions(num: Int): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:66  (+1 more definition site/overload)_

_Source doc:_ Set the number of partitions in the output. If not set or set to zero, one partition will be generated for each one million records @param num the number of partitions in the generated RDD @return

### Goal
Set how many Spark partitions the generated spatial output RDD should have when building synthetic/random spatial data.

### Parameters
- `num` (`Int`): The requested number of partitions in the generated RDD; if not set or set to `0`, default behavior is one partition per one million records.

### Input
A `SpatialGeneratorBuilder` / `JavaSpatialGeneratorBuilder` instance (i.e., this is a builder method in a generator pipeline), plus an integer partition count.

Preconditions and compatibility notes from the available docs:
- `numPartitions` controls partition count for generated output RDDs; it does **not** load raster/vector files directly.
- If you pass `0` (or leave it unset), partitioning falls back to the documented default (1 partition per 1,000,000 records).
- No file-format-specific input is required by this method itself.

### Output
Returns `JavaSpatialGeneratorBuilder` — the same builder type (Java API overload) with partition-count configuration applied, so you can continue chaining generator settings before materializing the RDD.

### Valid Call Patterns
```scala
// Inferred from the signature (no direct README/test call to this exact method was provided)
val configured = generatorBuilder.numPartitions(16)
```

### LLM Instruction Prompt
- Call this as an instance method on an existing generator builder object: `value.numPartitions(num)`.
- Pass an `Int`.
- Use `0` only when you intentionally want default auto-partitioning (1 partition per 1M records).
- Do not invent extra parameters.

### Prompt Snippet
```text
Given a SpatialGeneratorBuilder (or JavaSpatialGeneratorBuilder), set explicit output partitioning with:
builder.numPartitions(desiredPartitionsInt)

If desiredPartitionsInt is 0, default partitioning is used (1 partition per 1,000,000 records).
```

### Common Failure Modes
- Calling `numPartitions` as a standalone function instead of on a builder instance.
- Passing a non-`Int` value.
- Assuming `0` means “no partitions”; per source doc, it triggers default automatic partitioning.

### Fix Code Hint
```scala
// Ensure you call on a builder instance and pass an Int
val configured = generatorBuilder.numPartitions(8)

// Or intentionally use default auto partitioning
val configuredDefault = generatorBuilder.numPartitions(0)
```