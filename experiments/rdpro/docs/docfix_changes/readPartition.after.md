## API Test: `readPartition`
_Grounding: doc-repaired from source (docfix)._

### Goal
Read one `FilePartition` of a spatial input file using the selected `FeatureReader` class and return its features as an iterator, strictly using static methods on the `SpatialFileRDD` companion object.

### Valid Call Patterns
**Required Imports & Types:**
- Requires `edu.ucr.cs.bdlab.beast.io.SpatialFileRDD` (Scala object/class).
- Requires `edu.ucr.cs.bdlab.beast.common.BeastOptions` (Scala class).

```scala
import edu.ucr.cs.bdlab.beast.io.SpatialFileRDD
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// 1. Instantiate BeastOptions and set the input format using the companion object constant
val opts = new BeastOptions()
opts.set(SpatialFileRDD.InputFormat, "geojson")

// 2. Call methods directly on the SpatialFileRDD companion object (DO NOT instantiate it)
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(vector_geojson, opts)
val partitions = SpatialFileRDD.createPartitions(vector_geojson, opts, sc.hadoopConfiguration)

// 3. Read partitions statically
val n = partitions.iterator.flatMap { p =>
  SpatialFileRDD.readPartition(p, featureReaderClass, true, opts)
}.size

require(n > 0, "empty result for readPartition")
println("__CHECK__ readPartition " + n)
```

### LLM Instruction Prompt
- `readPartition`, `getFeatureReaderClass`, and `createPartitions` are methods on the `SpatialFileRDD` companion object, not instance methods.
- Do not instantiate `SpatialFileRDD` to call these methods; call them directly on the `SpatialFileRDD` object (e.g., `SpatialFileRDD.readPartition(...)`).
- `SpatialFileRDD.InputFormat` is a constant on the companion object used to set the input format in `BeastOptions`.
- Instantiate `BeastOptions` with its no-argument constructor (`new BeastOptions()`) and use `.set(...)` to configure it.

### Prompt Snippet
```text
Instantiate `new BeastOptions()` and set the format using `opts.set(SpatialFileRDD.InputFormat, "geojson")`. Do not instantiate SpatialFileRDD. Call SpatialFileRDD.getFeatureReaderClass(path, opts), then SpatialFileRDD.createPartitions(path, opts, sc.hadoopConfiguration). For each partition, call SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts) and consume the returned Iterator[IFeature].
```

### Common Failure Modes
- **Attempting to instantiate `SpatialFileRDD`:** The snippet will fail if you write `new SpatialFileRDD(...)`. `readPartition`, `getFeatureReaderClass`, and `createPartitions` are methods on the companion object and must be called statically.
- Passing a `featureReaderClass` that does not match the actual input format/options.
- Building partitions from one path/options set and reading with a different reader/options set.

### Fix Code Hint
```scala
// WRONG: Instantiating SpatialFileRDD to call methods (will fail compilation/runtime)
val rdd = new SpatialFileRDD() 
val readerClass = rdd.getFeatureReaderClass(path, opts)
val features = rdd.readPartition(partition, readerClass, true, opts)

// CORRECT: Call methods directly on the SpatialFileRDD companion object
val opts = new BeastOptions()
opts.set(SpatialFileRDD.InputFormat, "geojson")

val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(path, opts)
val partitions = SpatialFileRDD.createPartitions(path, opts, sc.hadoopConfiguration)
val features = SpatialFileRDD.readPartition(partitions.head, featureReaderClass, true, opts)
```