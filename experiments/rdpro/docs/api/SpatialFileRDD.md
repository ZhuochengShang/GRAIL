# SpatialFileRDD

_The `createPartitions` function creates partitions for a given input file, enabling distributed processing of geospatial raster data in Spark._

**Receiver:** instance — obtain a `SpatialFileRDD` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `createPartitions` **(primary)**, ★ `getFeatureReaderClass`, ★ `readLocal`, ★ `readPartition`, ⚠️ `skipDuplicateAvoidance`

---

## API Test: `createPartitions`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def createPartitions(path: String, opts: BeastOptions, conf: Configuration): Array[FilePartition]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:318_

_Source doc:_ Create all partitions in this RDD for the given input file @return

### Goal
The `createPartitions` function creates partitions for a given input file, enabling distributed processing of geospatial raster data in Spark.

### Parameters
- `path` (`String`): The file path to the input data, which can be a single file or a comma-separated list of files.
- `opts` (`BeastOptions`): Options for reading the input file, such as the format of the file (e.g., "geojson", "shapefile").
- `conf` (`Configuration`): The Hadoop configuration object that contains settings for the Spark job.

### Input
The caller must provide a valid file path to a supported input format (e.g., GeoTIFF, HDF, Shapefile, GeoJSON) and ensure that the input files are accessible and correctly formatted. The `opts` parameter should specify the input format.

### Output
Returns `Array[FilePartition]` — an array of `FilePartition` objects representing the partitions created for the input file, which can be processed in parallel by Spark.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
- Ensure that the `path` parameter points to a valid input file and that the `opts` parameter specifies the correct input format. The `conf` parameter should be the Hadoop configuration for the Spark context.

### Prompt Snippet
```text
Create partitions for the input file using the specified options and configuration.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the file path is correct and accessible, and that the input format is supported.
```

## API Test: `getFeatureReaderClass`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getFeatureReaderClass(path: String, opts: BeastOptions): Class[_ <: FeatureReader]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:398_

_Source doc:_ The class of the feature reader to use with this RDD. All partitions use the same feature reader.

### Goal
The `getFeatureReaderClass` function determines the appropriate feature reader class to use for reading spatial features from a specified file path in a distributed raster processing context.

### Parameters
- `path` (`String`): The file path to the spatial data source (e.g., a GeoJSON file) from which features will be read.
- `opts` (`BeastOptions`): Options that specify the input format and other configurations for reading the features.

### Input
The caller must provide a valid file path to a supported spatial data format (e.g., GeoJSON) and a `BeastOptions` instance that indicates the input format. The input file must be accessible and correctly formatted for the feature reader to function properly.

### Output
Returns `Class[_ <: FeatureReader]` — this value represents the class type of the feature reader that will be used to read features from the specified data source.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
```

### LLM Instruction Prompt
- Ensure that the `path` provided points to a valid spatial data file and that the `opts` specify the correct input format. The feature reader class returned should be used consistently across all partitions of the RDD.

### Prompt Snippet
```text
Use `getFeatureReaderClass` to obtain the feature reader class for a given spatial data file path and options.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure the file path is correct and the file exists. Verify that the `opts` parameter includes a valid input format for the data being read.
```

## API Test: `readLocal`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readLocal(path: String, iformat: String, opts: BeastOptions, conf: Configuration): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:492_

_Source doc:_ Reads the given path locally without creating any RDDs. Useful for reading a small file when SparkContext is not accessible, e.g., inside a mapPartition function. @param path path to a single file or a directory @param iformat the format of the data @param opts additional options for reading the file @return an iterator to features in the given path

### Goal
`readLocal` reads features from a specified file or directory locally, allowing for access to small datasets without requiring a SparkContext.

### Parameters
- `path` (`String`): The file path to a single file or a directory containing the data to be read. This should be a valid path accessible from the local filesystem.
- `iformat` (`String`): The format of the data being read, such as "wkt(1)" for Well-Known Text format. This informs the reader how to interpret the data.
- `opts` (`BeastOptions`): Additional options for reading the file, such as skipping headers or specifying field separators. These options can modify the behavior of the reading process.
- `conf` (`Configuration`): A Hadoop `Configuration` object that provides the necessary settings for file reading operations, including any required credentials or configurations for accessing the data.

### Input
The caller must provide a valid file path (either to a single file or a directory) containing data in a supported format (e.g., WKT, CSV). The input files should be accessible and correctly formatted according to the specified `iformat`.

### Output
Returns `Iterator[IFeature]` — an iterator over the features read from the specified path. Each feature represents a data record that can be processed further in the application.

### Valid Call Patterns
```scala
val features = SpatialFileRDD.readLocal(input.getPath, "wkt(1)",
  Seq(CSVFeatureReader.SkipHeader -> true, CSVFeatureReader.FieldSeparator -> '\t'), sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
When calling `readLocal`, ensure that the `path` points to a valid file or directory, the `iformat` is correctly specified, and the `opts` are appropriate for the data being read.

### Prompt Snippet
```text
Read features from a local file or directory using the readLocal function, ensuring the path and format are correctly specified.
```

### Common Failure Modes
- **[compile]** error: object BeastOptions is not a member of package edu.ucr.cs.bdlab.beast.util
- **[compile]** error: not found: value CSVFeatureReader

### Fix Code Hint
```scala
Ensure the file path is correct and accessible, the format is supported, and the options provided are valid for the data being read.
```

## API Test: `readPartition`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readPartition(partition: FilePartition, featureReaderClass: Class[_ <: FeatureReader], applyDuplicateAvoidance: Boolean, opts: BeastOptions): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441_

_Source doc:_ Reads the given partition @param partition the partition to read @param featureReaderClass the class of the feature reader @param opts the user options @return an iterator to the features

### Goal
`readPartition` reads features from a specified partition using a designated feature reader class, facilitating the processing of geospatial data in a distributed manner.

### Parameters
- `partition` (`FilePartition`): Represents a segment of a file that contains geospatial features to be read. It is expected to be a valid partition created from a geospatial data source.
- `featureReaderClass` (`Class[_ <: FeatureReader]`): The class type of the feature reader that will be used to interpret the features in the partition. This should correspond to the format of the data being read (e.g., GeoJSON, Shapefile).
- `applyDuplicateAvoidance` (`Boolean`): A flag indicating whether to apply duplicate avoidance logic when reading features. If set to true, the function will attempt to filter out duplicate features.
- `opts` (`BeastOptions`): User-defined options that may affect how the features are read, such as input format specifications.

### Input
The caller must provide a valid `FilePartition` that has been created from a geospatial data source, along with a corresponding `featureReaderClass` that matches the data format. The `opts` parameter should be configured to specify any additional reading options.

### Output
Returns `Iterator[IFeature]` — an iterator that provides access to the features read from the specified partition. Each feature is represented as an instance of `IFeature`, which encapsulates the geospatial data.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
var featureCount: Int = 0
for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  featureCount += features.length
}
assert(featureCount == 7)
```

### LLM Instruction Prompt
- When calling `readPartition`, ensure that the `partition` is a valid `FilePartition` and that the `featureReaderClass` corresponds to the data format of the partition. Set `applyDuplicateAvoidance` to true or false based on whether duplicate features should be filtered. Provide appropriate `BeastOptions` for reading.

### Prompt Snippet
```text
To read features from a partition, use the `readPartition` method with a valid `FilePartition`, a corresponding `featureReaderClass`, and specify whether to apply duplicate avoidance.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the `partition` is created from a compatible data source and that the `featureReaderClass` is correctly specified for the data format being read. Check the configuration of `BeastOptions` for any necessary parameters.
```

## API Test: `skipDuplicateAvoidance`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[beast] def skipDuplicateAvoidance(rdd: RDD[_]): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:535_

_Source doc:_ If the given RDD is based on a SpatialFileRDD, it causes it to skip duplicate avoidance. @param rdd the rdd to skip duplicate avoidance for

### Goal
The `skipDuplicateAvoidance` function allows a SpatialFileRDD to process records without filtering out duplicates, which can be useful in scenarios where duplicate records are expected and should be retained.

### Parameters
- `rdd` (`RDD[_]`): The RDD to apply duplicate avoidance skipping on. This RDD should be based on a SpatialFileRDD to ensure the function operates correctly.

### Input
The input must be an RDD derived from a SpatialFileRDD, which typically contains spatial data records. The RDD should be properly initialized and populated with data before calling this function.

### Output
Returns `Unit` — this indicates that the function does not return a value but modifies the behavior of the RDD to allow duplicate records to be processed.

### Valid Call Patterns
```scala
SpatialFileRDD.skipDuplicateAvoidance(features)
```

### LLM Instruction Prompt
- Ensure that the RDD passed to `skipDuplicateAvoidance` is based on a SpatialFileRDD and is properly initialized with spatial data.

### Prompt Snippet
```text
Call `skipDuplicateAvoidance` on a SpatialFileRDD to allow processing of duplicate records.
```

### Common Failure Modes
- **[compile]** error: edu.ucr.cs.bdlab.beast.io.SpatialFileRDD.type does not take parameters _(seen 3x)_
- **[compile]** error: value read is not a member of object edu.ucr.cs.bdlab.beast.io.SpatialFileRDD

### Fix Code Hint
```scala
Ensure the RDD is created from a valid SpatialFileRDD before calling skipDuplicateAvoidance.
```
