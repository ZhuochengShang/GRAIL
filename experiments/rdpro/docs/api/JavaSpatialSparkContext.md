# JavaSpatialSparkContext

_Loads a GeoTIFF file and returns its content as a distributed collection of raster tiles for further geospatial analysis._

**Receiver:** instance — obtain a `JavaSpatialSparkContext` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `geoTiff` **(primary)**, ★ `geojsonFile`, ★ `shapefile`, ★ `spatialFile`, ⚠️ `hdfFile`, ⚠️ `readCSVPoint`, ⚠️ `readWKTFile`

---

## API Test: `geoTiff`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def geoTiff[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]]
def geoTiff[T](filename: String, layer: Int, opts: BeastOptions): JavaRasterRDD[T]
def geoTiff[T](filename: String, layer: Int): JavaRasterRDD[T]
def geoTiff[T](filename: String): JavaRasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:40  (+3 more definition site/overload)_

_Source doc:_ Loads a GeoTIFF file as an RDD of tiles @param path the path of the file @param iLayer the index of the band to load (0 by default) @param opts additional options for loading the file @return a [[RasterRDD]] that represents all tiles in the file

### Goal
Loads a GeoTIFF file and returns its content as a distributed collection of raster tiles for further geospatial analysis.

### Parameters
- `path` (`String`): The file path to the GeoTIFF file to be loaded. This should be a valid path to an accessible GeoTIFF file.
- `iLayer` (`Int`), default `0`: The index of the band (layer) to load from the GeoTIFF file. The default value is `0`, which typically corresponds to the first band.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional options for loading the file, which can include configurations such as data type handling or performance tuning.

### Input
The caller must provide a valid path to a GeoTIFF file. The file must be accessible and correctly formatted as a GeoTIFF. The pixel type must be compatible with the expected type parameter `T` when loading the raster data.

### Output
Returns `RDD[ITile[T]]` — a distributed collection of raster tiles representing the data from the specified GeoTIFF file. Each tile contains pixel data of the specified type `T`.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("treecover")
val treecover: RDD[ITile[Float]] = sc.geoTiff("treecover")
```

### LLM Instruction Prompt
- Ensure the provided path is a valid GeoTIFF file and accessible. Use the appropriate type parameter `T` based on the expected pixel data type in the GeoTIFF.

### Prompt Snippet
```text
Load a GeoTIFF file using the geoTiff function, specifying the path and optional parameters for layer and loading options.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the path is correct and the file exists
val raster: RDD[ITile[Int]] = sc.geoTiff("valid_path_to_geotiff.tif")
// Check the number of layers in the GeoTIFF before specifying iLayer
val raster: RDD[ITile[Float]] = sc.geoTiff("valid_path_to_geotiff.tif", 1) // Ensure layer index is valid
```

## API Test: `geojsonFile`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def geojsonFile(filename: String) : SpatialRDD
def geojsonFile(filename: String) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:84  (+1 more definition site/overload)_

_Source doc:_ Reads data from a Shapefile @param filename the name of the GeoJSON file or a directory that contains GeoJSON file @return an RDD of features

### Goal
The `geojsonFile` function reads GeoJSON data and returns it as a distributed collection of spatial features for further geospatial analysis.

### Parameters
- `filename` (`String`): The name of the GeoJSON file or a directory that contains GeoJSON files.

### Input
The input must be a valid GeoJSON file or a directory containing GeoJSON files. Ensure that the file is accessible and correctly formatted as per GeoJSON specifications.

### Output
Returns `SpatialRDD` — a distributed collection of spatial features extracted from the GeoJSON file, which can be used for spatial operations and analysis.

### Valid Call Patterns
```scala
val records = sparkContext.geojsonFile("input.json")
```

### LLM Instruction Prompt
- When calling `geojsonFile`, ensure that the provided filename points to a valid GeoJSON file or directory containing GeoJSON files.

### Prompt Snippet
```text
Read a GeoJSON file using the geojsonFile function to obtain a SpatialRDD for spatial analysis.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure the filename is correct and that the file is formatted according to GeoJSON standards before calling geojsonFile.
```

## API Test: `shapefile`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def shapefile(filename: String) : SpatialRDD
def shapefile(filename: String) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:76  (+1 more definition site/overload)_

_Source doc:_ Reads features from an Esri Shapefile(c) @param filename the name of the .shp file, a compressed ZIP file that contains shapefiles, or a directory that contains shapefiles or ZIP files. @return an RDD of features

### Goal
The `shapefile` function reads geospatial features from an Esri Shapefile or a compressed ZIP file containing shapefiles, returning them as a distributed collection for further processing in Spark.

### Parameters
- `filename` (`String`): The path to the .shp file, a compressed ZIP file that contains shapefiles, or a directory that contains shapefiles or ZIP files.

### Input
The input must be a valid path to an Esri Shapefile or a ZIP file containing shapefiles. The specified file or directory must be accessible and correctly formatted as per the Esri Shapefile specifications.

### Output
Returns `SpatialRDD` — a distributed collection of geospatial features that can be processed in Spark. This RDD allows for spatial operations and analyses on the loaded features.

### Valid Call Patterns
```scala
val records = sparkContext.shapefile("input.zip")
// Or
val records = sparkContext.shapefile("input.shp")
```

### LLM Instruction Prompt
- Ensure that the provided filename points to a valid shapefile or a ZIP file containing shapefiles. The file must be accessible and correctly formatted.

### Prompt Snippet
```text
To load shapefiles, use the `shapefile` method with the path to your .shp file or a ZIP file containing shapefiles.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the file path is correct and points to a valid shapefile or ZIP file.
val records = sparkContext.shapefile("path/to/your/shapefile.shp")
```

## API Test: `spatialFile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def spatialFile(filename: String, format: String = null, opts: BeastOptions = new BeastOptions): SpatialRDD
def spatialFile(filename: String, opts: BeastOptions): SpatialRDD
def spatialFile(filename: String, iformat: String, opts: BeastOptions): JavaSpatialRDD
def spatialFile(filename: String, iformat: String): JavaSpatialRDD
def spatialFile(filename: String, opts: BeastOptions): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:46  (+4 more definition site/overload)_

_Source doc:_ Reads the given file according to the given spatial format. If spatial format is not given, it auto-detects the input based on the extension and then file contents (for CSV files only) @param filename the name of the file or directory of files @return the [[SpatialRDD]] that contains the records

### Goal
The `spatialFile` function loads spatial data from a specified file or directory into a `SpatialRDD`, enabling further geospatial analysis and processing.

### Parameters
- `filename` (`String`): The name of the file or directory containing spatial data. This can include various formats such as CSV, GeoJSON, or other supported spatial formats.
- `format` (`String`), default `null`: The specific format of the spatial data. If not provided, the function will attempt to auto-detect the format based on the file extension and contents (for CSV files).
- `opts` (`BeastOptions`), default `new BeastOptions`: Options for reading the spatial data, which may include parameters like separators for CSV files or other format-specific options.

### Input
The caller must provide a valid file path as `filename`, which should point to a file or directory containing spatial data in a supported format (e.g., CSV, GeoJSON). The file must be accessible and correctly formatted for the function to process it successfully.

### Output
Returns `SpatialRDD` — a distributed collection of spatial records that can be used for further geospatial operations, such as joins or transformations.

### Valid Call Patterns
```scala
val parks = sparkContext.spatialFile("parks_index", "wkt")
val records = sparkContext.spatialFile("input.gpx", "gpx")
```

### LLM Instruction Prompt
- When calling `spatialFile`, ensure that the `filename` points to a valid file or directory containing spatial data, and specify the format if it cannot be auto-detected.

### Prompt Snippet
```text
To load spatial data, use the spatialFile method with the appropriate filename and format.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the filename is correct and accessible
val spatialData = sparkContext.spatialFile("valid_file_path.csv", "csv", new BeastOptions("separator:,"))
```

## API Test: `hdfFile`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]]
def hdfFile(filename: String, layer: String): JavaRasterRDD[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46  (+1 more definition site/overload)_

### Goal
Loads raster data from an HDF file for distributed processing in Spark, specifically extracting a specified layer as an RDD of float tiles.

### Parameters
- `path` (`String`): The file path to the HDF file from which to load the raster data. This should be a valid path to an existing HDF file.
- `layer` (`String`): The name of the specific layer within the HDF file to be extracted. This should correspond to a valid layer name present in the HDF file.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for configuring the loading process, such as specifying additional parameters for reading the HDF file. This can be left as default for standard loading behavior.

### Input
The caller must provide:
- A valid path to an HDF file.
- The name of a layer that exists within the specified HDF file.
- Ensure that the Spark environment is properly configured and running to execute the operation.

### Output
Returns `RDD[ITile[Float]]` — an RDD containing tiles of float values representing the raster data extracted from the specified layer of the HDF file.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] = sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
```

### LLM Instruction Prompt
- Ensure that the `path` points to a valid HDF file and that the `layer` name is correct and exists within that file. Use default `BeastOptions` unless specific configurations are needed.

### Prompt Snippet
```text
Load raster data from an HDF file using the hdfFile method, specifying the correct path and layer name.
```

### Common Failure Modes
- **[runtime]** java.io.FileNotFoundException: File file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/grail-agent/examples/fixtures/sample_data.hdf does not exist _(seen 3x)_
- **[runtime]** java.io.FileNotFoundException: File file:/path/to/your/valid/file.hdf does not exist

### Fix Code Hint
```scala
// Ensure the HDF file path and layer name are correct
val temperatureK: RasterRDD[Float] = sc.hdfFile("path/to/your/file.hdf", "your_layer_name")
```

## API Test: `readCSVPoint`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readCSVPoint(filename: String, xColumn: Any = 0, yColumn: Any = 1, delimiter: Char = ',', skipHeader: Boolean = false): SpatialRDD
def readCSVPoint(filename: String, xColumn: String, yColumn: String, delimiter: Char, skipHeader: Boolean): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:97  (+1 more definition site/overload)_

_Source doc:_ Reads points from a CSV file given the names of the columns that contain the x and y coordinates @param filename the name of the file or directory that contains the data @param xColumn the name of the column that contains the x coordinate @param yColumn the name of the column that contains the y coordinate @param delimiter the field delimiter, comma by default @param skipHeader whether to skip the header line or not. If either xColumn or yColumn is String, this option will be ignored a header line will be assumed. Otherwise, it is false by default @return the set of records in the file

### Goal
The `readCSVPoint` function reads point data from a CSV file, extracting x and y coordinates for geospatial analysis.

### Parameters
- `filename` (`String`): The path to the CSV file containing the point data. This file should be accessible and properly formatted.
- `xColumn` (`Any`), default `0`: The index or name of the column that contains the x coordinate. If specified as an index, it should be an integer; if as a name, it should be a string.
- `yColumn` (`Any`), default `1`: The index or name of the column that contains the y coordinate. Similar to `xColumn`, it can be specified as either an index or a name.
- `delimiter` (`Char`), default `','`: The character that separates values in the CSV file. The default is a comma, but it can be set to any character that matches the file's format.
- `'`: This parameter appears to be incorrectly documented and should be ignored.
- `skipHeader` (`Boolean`), default `false`: Indicates whether to skip the first line of the CSV file, which is typically a header. If either `xColumn` or `yColumn` is specified as a string, this option will be ignored, and a header line will be assumed.

### Input
The input must be a properly formatted CSV file containing at least two columns for x and y coordinates. The file must be accessible to the Spark context. If using column names for `xColumn` and `yColumn`, the header must be present in the CSV.

### Output
Returns `SpatialRDD` — a distributed collection of spatial data points, where each point corresponds to a record in the CSV file, represented as x and y coordinates.

### Valid Call Patterns
```scala
val data: SpatialRDD = sparkContext.readCSVPoint("path/to/your/file.csv")
```

### LLM Instruction Prompt
- When calling `readCSVPoint`, ensure that the `filename` points to a valid CSV file and that the specified columns for x and y coordinates exist in the file.

### Prompt Snippet
```text
To read point data from a CSV file, use the `readCSVPoint` function with the appropriate filename and column specifications.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.50 executor driver): java.lan _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the CSV file exists and is correctly formatted before calling readCSVPoint
val data: SpatialRDD = sparkContext.readCSVPoint("path/to/your/file.csv", "longitude", "latitude")
```

## API Test: `readWKTFile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readWKTFile(filename: String, wktColumn: Any, delimiter: Char = '\t', skipHeader: Boolean = false): SpatialRDD
def readWKTFile(filename: String, wktColumn: String, delimiter: Char, skipHeader: Boolean): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:118  (+1 more definition site/overload)_

_Source doc:_ Read a CSV file with WKT-encoded geometry @param filename the name of the file or directory fo the input @param wktColumn the column that includes the WKT-encoded geometry, either an Integer for the index of the attribute or String for its name @param delimiter the field delimiter, tab by default @param skipHeader whether to skip the header line or not, if wktColumn is a string, this has to be true, if wktColumn is an Integer, this is false by default but can be overloaded @return the set of features in the input file

### Goal
The `readWKTFile` function reads a CSV file containing WKT-encoded geometries and returns a `SpatialRDD` of features for geospatial analysis.

### Parameters
- `filename` (`String`): The name of the input file or directory containing the CSV file with WKT geometries.
- `wktColumn` (`Any`): Specifies the column that contains the WKT-encoded geometry. This can be an `Integer` representing the index of the column or a `String` representing the column name.
- `delimiter` (`Char`), default `'\t'`: The character used to separate fields in the CSV file. The default is a tab character.
- `skipHeader` (`Boolean`), default `false`: Indicates whether to skip the header line in the CSV file. If `wktColumn` is a `String`, this must be `true`. If `wktColumn` is an `Integer`, it defaults to `false` but can be overridden.

### Input
The caller must provide a valid CSV file containing WKT-encoded geometries. The file must be accessible, and the specified `wktColumn` must exist in the file. If using a `String` for `wktColumn`, the `skipHeader` parameter must be set to `true`.

### Output
Returns `SpatialRDD` — a distributed collection of spatial features extracted from the input CSV file, which can be used for further geospatial processing and analysis.

### Valid Call Patterns
```scala
val testFile = makeDirCopy("/sjoinr.grid")
val data: RDD[IFeature] = sparkContext.readWKTFile(testFile.getPath, 0)
```

### LLM Instruction Prompt
- Ensure that the `filename` points to a valid CSV file with WKT geometries, and that the `wktColumn` is correctly specified as either an index or a column name.

### Prompt Snippet
```text
To read a CSV file with WKT-encoded geometries, use the `readWKTFile` function, ensuring the correct parameters are provided.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.50 executor driver): java.lan _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the filename is correct and accessible, and check the wktColumn index or name for validity.
```
