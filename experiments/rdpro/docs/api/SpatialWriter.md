# SpatialWriter

_`saveFeatures` saves a set of geospatial features to a specified output format, enabling users to persist processed spatial data for further analysis or…_

**Receiver:** static object — call `SpatialWriter.<method>(...)`

**Members** (most robust first): ⚠️ `saveFeatures` **(primary)**

---

## API Test: `saveFeatures`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def saveFeatures(features: SpatialRDD, oFormat: String, outPath: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:123_

_Source doc:_ Saves the given set of features to the output using the provided output format. @param features the set of features to store to the output @param oFormat the output format to use for writing @param outPath the path to write the output to @param opts user options to configure the writer

### Goal
`saveFeatures` saves a set of geospatial features to a specified output format, enabling users to persist processed spatial data for further analysis or sharing.

### Parameters
- `features` (`SpatialRDD`): The set of geospatial features to be saved. This should be an RDD containing spatial data, such as points, lines, or polygons.
- `oFormat` (`String`): The output format to use for writing the features. Supported formats include "geojson", "shapefile", and potentially others as defined in the library.
- `outPath` (`String`): The file path where the output will be written. This should include the desired file name and extension corresponding to the specified output format.
- `opts` (`BeastOptions`): User options to configure the writer, which may include settings for compression, file handling, or other output-specific parameters.

### Input
The caller must provide a valid `SpatialRDD` containing the features to be saved, a string indicating the output format, a valid file path for the output, and an instance of `BeastOptions` for configuration. The output path must be accessible and writable.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output is saved in the specified format (e.g., GeoJSON or Shapefile) at the provided path.

### Valid Call Patterns
```scala
val outputPath = new File(scratchDir, "test.geojson.bz2")
val features: RDD[IFeature] = sparkContext.parallelize(Seq(
  Feature.create(null, GeometryReader.DefaultGeometryFactory.createPoint(new CoordinateXY(1, 2)))
))
SpatialWriter.saveFeatures(features, "geojson", outputPath.getPath, new BeastOptions())
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing geospatial data.
- The `oFormat` must be a recognized output format string.
- The `outPath` must be a valid and writable file path.
- Provide a properly configured `BeastOptions` instance.

### Prompt Snippet
```text
Save the features to a specified output format using the saveFeatures method, ensuring the output path is valid and writable.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the output path is valid and accessible
val outputPath = new File(scratchDir, "output.geojson")
if (!outputPath.getParentFile.exists()) {
  outputPath.getParentFile.mkdirs() // Create directories if they do not exist
}
```
