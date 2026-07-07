# GeoJSONTable

_Infers the schema of a dataset based on the provided files and options, facilitating the understanding of the data structure for geospatial analysis._

**Receiver:** instance — obtain a `GeoJSONTable` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `inferSchema` **(primary)**

---

## API Test: `inferSchema`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private def inferSchema(values: Array[Any]): StructType
def inferSchema(names: Array[String], values: Array[Any]): StructType
override def inferSchema(options: CaseInsensitiveStringMap): StructType
override def inferSchema(files: Seq[FileStatus]): Option[StructType]
override def inferSchema(sparkSession: SparkSession, options: Map[String, String], files: Seq[FileStatus]): Option[StructType]
def inferSchema(in: InputStream): Seq[StructField]
def inferSchema(in: InputStream, size: Long): StructType
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileFormat.scala:26  (+11 more definition site/overload)_

### Goal
Infers the schema of a dataset based on the provided files and options, facilitating the understanding of the data structure for geospatial analysis.

### Parameters
- `sparkSession` (`SparkSession`): The active Spark session used for executing the operation, which provides the context for the Spark application.
- `options` (`Map[String, String]`): A map of configuration options that may influence the schema inference process, such as file format specifications or parsing options.
- `files` (`Seq[FileStatus]`): A sequence of file statuses representing the files to be analyzed for schema inference, typically containing metadata about the files.

### Input
The caller must provide a valid Spark session, a map of options relevant to the schema inference, and a sequence of file statuses that point to the files being analyzed. The files should be accessible and correctly formatted for the schema inference to succeed.

### Output
Returns `Option[StructType]` — an optional structure representing the inferred schema of the dataset. If the schema cannot be inferred, it returns `None`. The `StructType` contains fields that describe the data types and names of the columns in the dataset.

### Valid Call Patterns
```scala
val schemaOption: Option[StructType] = value.inferSchema(sparkSession, options, files)
```

### LLM Instruction Prompt
- Ensure that the Spark session is active and properly configured before calling `inferSchema`.
- Provide a valid sequence of file statuses that point to accessible files.
- Include any relevant options in the map to guide the schema inference process.

### Prompt Snippet
```text
Infer the schema of the provided files using the active Spark session and specified options.
```

### Common Failure Modes
- **[compile]** error: not found: value inferSchema _(seen 3x)_
- **[compile]** error: object CaseInsensitiveStringMap is not a member of package org.apache.spark.sql.catalyst.util

### Fix Code Hint
```scala
// Ensure the Spark session is initialized and the files are accessible
val sparkSession: SparkSession = SparkSession.builder().appName("RDPro").getOrCreate()
val options: Map[String, String] = Map("format" -> "geojson")
val files: Seq[FileStatus] = Seq(/* valid FileStatus instances */)

val schemaOption: Option[StructType] = value.inferSchema(sparkSession, options, files)
```
