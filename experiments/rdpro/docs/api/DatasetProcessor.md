# DatasetProcessor

_The `decompressDatasetFiles` function decompresses any ZIP files located in the dataset's path, cleans up by deleting the original ZIP files, and updates the…_

**Receiver:** instance — obtain a `DatasetProcessor` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `decompressDatasetFiles` **(primary)**, ⚠️ `geometryType`, ⚠️ `id`, ⚠️ `summarizeData`, ⚠️ `visualize`

---

## API Test: `decompressDatasetFiles`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[dataExplorer] def decompressDatasetFiles(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:195_

_Source doc:_ Decompresses dataset files that are stored locally. Specifically, it decompress any ZIP files found in the dataset's path. It deletes those ZIP files and finally updates the dataset's status in the database after decompression.

### Goal
The `decompressDatasetFiles` function decompresses any ZIP files located in the dataset's path, cleans up by deleting the original ZIP files, and updates the dataset's status in the database.

### Parameters
_None._

### Input
The function operates on dataset files that must be stored locally in a specified directory. The precondition is that the dataset must contain ZIP files that need to be decompressed.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs actions such as file decompression and database updates.

### Valid Call Patterns
```scala
datasetProcessor.decompressDatasetFiles()
```

### LLM Instruction Prompt
- Ensure that the dataset containing ZIP files is correctly set up and accessible before calling `decompressDatasetFiles`.

### Prompt Snippet
```text
Call `decompressDatasetFiles` on an instance of `DatasetProcessor` to decompress ZIP files in the dataset's path and update the database status.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor DatasetProcessor: (datasetName: String, dbConnection: java.sql.Connection, datasetsDir: String, datasetFS: org.apache.hadoop.fs.FileSystem, sparkSession: or _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the dataset path is correct and contains ZIP files before calling the function.
if (datasetDir.listFiles().exists(_.getName.endsWith(".zip"))) {
    datasetProcessor.decompressDatasetFiles()
} else {
    println("No ZIP files found in the dataset directory.")
}
```

## API Test: `geometryType`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def geometryType: GeometryType
def geometryType: DataType
def geometryType: String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:60  (+2 more definition site/overload)_

_Source doc:_ The most inclusive geometry type for this partition. This can be interpreted as below. - Empty: All geometries are empty - Point: Contains at least one point and zero or more empty geometries - LineString: Contains at least one linestring and zero or more empty geometries - Polygon: Contains at least one polygon and zero or more empty geometries - MultiPoint: Contains at least one multipoint, and zero or more point or empty geometry. - MultiLineString: Contains at least one MultiLineString, and zero or more linestrings and empty geometries. - MultiPolygon: Contains at least one MultiPolygon, and zero or more polygons and empty geometries. - GeometryCollection: Everything else, i.e., none of the above.

### Goal
The `geometryType` function determines the most inclusive geometry type present in a given spatial partition, which is essential for understanding the nature of geometries being processed in geospatial analysis.

### Parameters
_None._

### Input
The function operates on a spatial partition that has been previously defined and populated with geometries. There are no specific file formats required as input, but the geometries must be valid and conform to the expected types.

### Output
Returns `GeometryType` — a representation of the most inclusive geometry type for the partition, which can indicate whether the geometries are empty, points, lines, polygons, or collections of these types.

### Valid Call Patterns
```scala
val geometryType: GeometryType = spatialPartition.geometryType
```

### LLM Instruction Prompt
- When calling `geometryType`, ensure that the spatial partition is properly initialized and contains valid geometries to avoid unexpected results.

### Prompt Snippet
```text
Retrieve the geometry type of the spatial partition to understand the types of geometries it contains.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 2x)_
- **[runtime]** java.lang.ClassCastException: class edu.ucr.cs.bdlab.beast.io.SpatialFileRDD$FilePartition cannot be cast to class edu.ucr.cs.bdlab.beast.cg.SpatialPartition (edu.ucr.cs.bdlab.beast.io.SpatialFileRDD$
- **[compile]** error: overloaded method value readInput with alternatives:

### Fix Code Hint
```scala
// Ensure the spatial partition is initialized and populated with valid geometries before calling geometryType
val spatialPartition = ... // Initialize and populate the spatial partition
val geometryType = spatialPartition.geometryType
```

## API Test: `id`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def id: Int
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58_

### Goal
The `id` function retrieves an integer identifier associated with the current instance of the dataset processor.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Int` — the integer identifier that uniquely represents the current instance of the dataset processor.

### Valid Call Patterns
```scala
val identifier: Int = value.id
```

### LLM Instruction Prompt
- When calling `id`, ensure that it is invoked on an instance of the dataset processor.

### Prompt Snippet
```text
Retrieve the identifier of the dataset processor instance using the `id` method.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor DatasetProcessor: (datasetName: String, dbConnection: java.sql.Connection, datasetsDir: String, datasetFS: org.apache.hadoop.fs.FileSystem, sparkSession: or _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the dataset processor instance is properly initialized before calling id
val processor = new DatasetProcessor()
val identifier: Int = processor.id
```

## API Test: `summarizeData`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[dataExplorer] def summarizeData(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:219_

_Source doc:_ Summarize the dataset and set the corresponding attributes in the dataset.

### Goal
The `summarizeData` function summarizes the dataset and updates the corresponding attributes within the dataset, facilitating better understanding and management of the data.

### Parameters
_None._

### Input
The function does not require any parameters. However, it operates on a dataset that must be properly initialized and loaded prior to calling this function.

### Output
Returns `Unit` — this indicates that the function does not return any value but performs an operation that modifies the dataset's attributes.

### Valid Call Patterns
```scala
value.summarizeData()
```

### LLM Instruction Prompt
- Ensure that the dataset is initialized and loaded before calling `summarizeData`.

### Prompt Snippet
```text
Call `summarizeData` on an initialized dataset to summarize its attributes.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor DatasetProcessor: (datasetName: String, dbConnection: java.sql.Connection, datasetsDir: String, datasetFS: org.apache.hadoop.fs.FileSystem, sparkSession: or _(seen 4x)_

### Fix Code Hint
```scala
Ensure the dataset is properly initialized and loaded before calling `summarizeData()`.
```

## API Test: `visualize`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private[dataExplorer] def visualize(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:357_

_Source doc:_ Build the visualization index for this dataset

### Goal
The `visualize` function builds the visualization index for the dataset, enabling graphical representation of the raster data.

### Parameters
_None._

### Input
The function does not require any parameters. However, it assumes that the dataset has been properly initialized and is ready for visualization.

### Output
Returns `Unit` — this indicates that the function completes its operation without returning a value, signifying that the visualization index has been successfully built.

### Valid Call Patterns
```scala
value.visualize()
```

### LLM Instruction Prompt
- Ensure that the dataset is initialized and ready for visualization before calling `visualize`.

### Prompt Snippet
```text
Call the visualize method on the dataset processor instance to build the visualization index.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor DatasetProcessor: (datasetName: String, dbConnection: java.sql.Connection, datasetsDir: String, datasetFS: org.apache.hadoop.fs.FileSystem, sparkSession: or _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the dataset is initialized before calling visualize
if (dataset.isInitialized) {
  value.visualize()
} else {
  println("Dataset is not initialized.")
}
```
