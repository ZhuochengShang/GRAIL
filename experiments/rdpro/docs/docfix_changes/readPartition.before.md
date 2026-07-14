## API Test: `readPartition`

### Signature
```scala
def readPartition(partition: FilePartition, featureReaderClass: Class[_ <: FeatureReader], applyDuplicateAvoidance: Boolean, opts: BeastOptions): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441_

_Source doc:_ Reads the given partition @param partition the partition to read @param featureReaderClass the class of the feature reader @param opts the user options @return an iterator to the features

### Goal
Read one `FilePartition` of a spatial input file using the selected `FeatureReader` class and return its features as an iterator.

### Parameters
- `partition` (`FilePartition`): A partition object produced for an input path (e.g., from `SpatialFileRDD.createPartitions`) that identifies the specific split/chunk to read.
- `featureReaderClass` (`Class[_ <: FeatureReader],
                    applyDuplicateAvoidance: Boolean, opts: BeastOptions`): The `FeatureReader` implementation class used to parse records in this partition (typically obtained from `SpatialFileRDD.getFeatureReaderClass(...)`).

### Input
Caller must provide:
- A valid `FilePartition` for the target input.
- A compatible `FeatureReader` class for that input format.
- `BeastOptions` containing relevant read options (in tested usage, `SpatialFileRDD.InputFormat -> "geojson"`).

Supported vector input families in Beast context include formats such as GeoJSON, Shapefile, CSV/WKT-style, etc., but this function’s exact behavior depends on the passed `featureReaderClass` and `opts`.

Precondition from real usage:
- Build `featureReaderClass` and `partitions` from the same input path/options combination before calling `readPartition`, so reader/partition stay consistent.

### Output
Returns `Iterator[IFeature]` — an iterator over spatial features decoded from the given partition.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)

for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  // consume features
}
```

### LLM Instruction Prompt
- Use the receiver exactly as `SpatialFileRDD.readPartition(partition, featureReaderClass, trueOrFalse, opts)`.
- Derive `featureReaderClass` via `SpatialFileRDD.getFeatureReaderClass(inputPath, opts)`.
- Derive `partition` values via `SpatialFileRDD.createPartitions(inputPath, opts, hadoopConf)`.
- Keep options consistent across `getFeatureReaderClass`, `createPartitions`, and `readPartition`.
- Do not invent extra parameters or overloads.

### Prompt Snippet
```text
Given an input path and BeastOptions, first call SpatialFileRDD.getFeatureReaderClass(path, opts), then SpatialFileRDD.createPartitions(path, opts, sparkContext.hadoopConfiguration). For each partition, call SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts) and consume the returned Iterator[IFeature].
```

### Common Failure Modes
- Passing a `featureReaderClass` that does not match the actual input format/options.
- Building partitions from one path/options set and reading with a different reader/options set.
- Assuming `readPartition` is a standalone bare function call (use `SpatialFileRDD.readPartition(...)` as shown).
- Providing incomplete read options (e.g., missing/incorrect input format hint when auto-detection is not sufficient).

### Fix Code Hint
```scala
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputPath, opts, sparkContext.hadoopConfiguration)

val allFeatures =
  partitions.iterator.flatMap { p =>
    SpatialFileRDD.readPartition(p, featureReaderClass, true, opts)
  }
```