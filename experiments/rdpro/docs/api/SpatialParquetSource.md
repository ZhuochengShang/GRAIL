# SpatialParquetSource

_Decodes a `DataFrame` that has been encoded in the SpatialParquet format, allowing for the retrieval of spatial data._

**Receiver:** static object — call `SpatialParquetSource.<method>(...)`

**Members** (most robust first): ⚠️ `decodeSpatialParquet` **(primary)**, ⚠️ `encodeGeoParquet`, ⚠️ `encodeSpatialParquet`

---

## API Test: `decodeSpatialParquet`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def decodeSpatialParquet(dataframe: DataFrame, geomColumnName: String): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:69_

_Source doc:_ Decodes a [[DataFrame]] that was encoded using the SpatialParquet format @param dataframe @param geomColumnName @return

### Goal
Decodes a `DataFrame` that has been encoded in the SpatialParquet format, allowing for the retrieval of spatial data.

### Parameters
- `dataframe` (`DataFrame`): A Spark DataFrame that contains spatial data encoded in the SpatialParquet format. This DataFrame should have been previously encoded using the `encodeSpatialParquet` method.
- `geomColumnName` (`String`): The name of the column in the DataFrame that contains the geometry information. This column is essential for decoding the spatial data correctly.

### Input
The caller must provide a `DataFrame` that has been encoded in the SpatialParquet format and includes a specified geometry column. The DataFrame must be accessible in the Spark session.

### Output
Returns `DataFrame` — A decoded DataFrame that contains the original spatial data, including the geometry specified by `geomColumnName`. The output retains the structure of the original DataFrame prior to encoding.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
```

### LLM Instruction Prompt
- Ensure that the input DataFrame is encoded in the SpatialParquet format and contains the specified geometry column before calling `decodeSpatialParquet`.

### Prompt Snippet
```text
To decode a DataFrame encoded in SpatialParquet format, use the decodeSpatialParquet method with the encoded DataFrame and the name of the geometry column.
```

### Common Failure Modes
- **[compile]** error: not found: value spark _(seen 2x)_
- **[runtime]** org.apache.spark.sql.AnalysisException: Unable to infer schema for geojson. It must be specified manually.
- **[compile]** error: not found: value sparkSession

### Fix Code Hint
```scala
Ensure that the DataFrame passed to decodeSpatialParquet was previously encoded using encodeSpatialParquet and that the specified geometry column exists in the DataFrame.
```

## API Test: `encodeGeoParquet`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def encodeGeoParquet(dataframe: DataFrame): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:99_

_Source doc:_ Encode the given DataFrame into GeoParquet format by replacing the geometry column with two new columns, MBR and the WKB representation of the geometry. @param dataframe @return

### Goal
The `encodeGeoParquet` function encodes a given DataFrame into the GeoParquet format, transforming the geometry column into two new columns representing the Minimum Bounding Rectangle (MBR) and the Well-Known Binary (WKB) representation of the geometry.

### Parameters
- `dataframe` (`DataFrame`): A Spark DataFrame containing geospatial data, which must include a geometry column that will be transformed into MBR and WKB columns.

### Input
The input must be a Spark DataFrame that is properly formatted and includes a geometry column. The DataFrame can be loaded from formats such as GeoJSON, and it should be accessible within the Spark session.

### Output
Returns `DataFrame` — a new DataFrame in GeoParquet format, which includes the original data with the geometry column replaced by two new columns: one for the Minimum Bounding Rectangle (MBR) and another for the Well-Known Binary (WKB) representation of the geometry.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
```

### LLM Instruction Prompt
- When calling `encodeGeoParquet`, ensure that the input DataFrame contains a geometry column and is formatted correctly as a Spark DataFrame. The function will return a new DataFrame with the geometry column transformed.

### Prompt Snippet
```text
To encode a DataFrame into GeoParquet format, use the `encodeGeoParquet` function, ensuring the DataFrame has a geometry column.
```

### Common Failure Modes
- **[compile]** error: not found: value spark _(seen 3x)_
- **[compile]** error: not found: value sparkSession

### Fix Code Hint
```scala
// Ensure the DataFrame is loaded correctly and contains a geometry column before calling encodeGeoParquet
val dataframe = sparkSession.read.format("geojson").load("path/to/your/file.geojson")
if (dataframe.columns.contains("geometry")) {
  val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
} else {
  throw new IllegalArgumentException("DataFrame must contain a geometry column.")
}
```

## API Test: `encodeSpatialParquet`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def encodeSpatialParquet(dataframe: DataFrame): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:81_

_Source doc:_ Parses an existing DataFrame according to the given options that determine the format of the spatial attributes. @param dataframe an existing dataframe @return a dataframe that parses and replaces the spatial attributes with a geometry column

### Goal
The `encodeSpatialParquet` function transforms an existing DataFrame by parsing its spatial attributes and replacing them with a geometry column, facilitating the storage of spatial data in a Parquet format.

### Parameters
- `dataframe` (`DataFrame`): An existing DataFrame containing spatial attributes that need to be encoded into a geometry column.

### Input
The input must be a valid DataFrame that includes spatial attributes, typically loaded from formats such as GeoJSON. The DataFrame should be structured correctly to ensure that spatial attributes can be parsed and transformed.

### Output
Returns `DataFrame` — a new DataFrame that has been modified to include a geometry column, suitable for further spatial analysis or storage in a Parquet format.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
```

### LLM Instruction Prompt
- When calling `encodeSpatialParquet`, ensure that the input DataFrame contains valid spatial attributes and is properly formatted. The function will return a DataFrame with a geometry column.

### Prompt Snippet
```text
To use the `encodeSpatialParquet` function, provide a DataFrame with spatial attributes that need to be encoded. The output will be a DataFrame with a geometry column.
```

### Common Failure Modes
- **[compile]** error: not found: value spark _(seen 3x)_
- **[compile]** error: not found: value sparkSession

### Fix Code Hint
```scala
Ensure that the input DataFrame is loaded correctly from a supported format (e.g., GeoJSON) and contains the necessary spatial attributes before calling `encodeSpatialParquet`.
```
