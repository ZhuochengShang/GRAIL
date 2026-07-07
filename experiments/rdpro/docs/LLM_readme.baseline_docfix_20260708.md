# RDPro — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `add`

### Signature
```scala
override def add(f: IFeature): Unit
override def add(v: PointND): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:54  (+1 more definition site/overload)_

### Goal
The `add` function accumulates features or points into a summary accumulator for further analysis in geospatial raster processing.

### Parameters
- `f` (`IFeature`): An instance of a feature that represents a geometric shape or spatial entity, typically loaded from vector data formats such as shapefiles or GeoJSON.

### Input
The caller must provide a valid `IFeature` or `PointND` object. The input data should be compatible with the expected types, and the features should be derived from a loaded vector dataset, such as those obtained from a shapefile.

### Output
Returns `Unit` — this indicates that the operation is performed without returning a value, and the state of the accumulator is updated internally.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = features.map(f => { accumulator.add(f); f })
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- When calling `add`, ensure that the input is either an `IFeature` or a `PointND` and that it is derived from a valid vector dataset.

### Prompt Snippet
```text
To accumulate features into the summary, use the `add` method with a valid `IFeature` or `PointND` object.
```

### Common Failure Modes
- Attempting to call `add` with an incompatible type that is neither `IFeature` nor `PointND`.
- Not initializing the accumulator before calling `add`, which may lead to a null reference or runtime error.

### Fix Code Hint
```scala
// Ensure the accumulator is created and the input feature is valid before calling add
val accumulator = Summary.createSummaryAccumulator(sparkContext)
val feature = ... // Load or define a valid IFeature
accumulator.add(feature)
```

## API Test: `addFeature`

### Signature
```scala
def addFeature(feature: IFeature): IntermediateVectorTile
def addFeature(feature: IFeature): Unit
def addFeature(feature: Row, geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:92  (+2 more definition site/overload)_

### Goal
The `addFeature` function adds a specified feature to a vector tile, either as-is or by rasterizing and aggregating it, depending on the tile's state.

### Parameters
- `feature` (`IFeature`): The feature to be added to the tile. This can be a geometric shape or a data structure representing spatial information.
- `geometry` (`LiteGeometry`): The geometric representation of the feature, used when adding features that require a specific geometry type.

### Input
The caller must provide a valid `IFeature` object, which represents the spatial feature to be added. If using the overload that includes `Row` and `LiteGeometry`, the `Row` should contain the attributes of the feature, and the `LiteGeometry` should represent its spatial geometry. Ensure that the feature's attributes and geometry are compatible with the vector tile's expected structure.

### Output
Returns `Unit` — this indicates that the operation has been completed successfully, allowing for method chaining for further operations on the tile.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"), null, Array(10, "pt")))
```

### LLM Instruction Prompt
- When calling `addFeature`, ensure that the `feature` parameter is a valid `IFeature` object. If using the overload with `Row` and `LiteGeometry`, ensure that the `Row` contains the correct attributes and that the `LiteGeometry` is properly defined.

### Prompt Snippet
```text
To add a feature to a vector tile, use the `addFeature` method with a valid `IFeature` object. If using the overload, provide a `Row` with attributes and a `LiteGeometry` for the feature's geometry.
```

### Common Failure Modes
- Attempting to add a feature with incompatible geometry or attributes may result in runtime errors.
- If the `feature` is null or improperly constructed, the method may throw an exception.

### Fix Code Hint
```scala
// Ensure the feature is properly created and not null before calling addFeature
val pointFeature = Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"), null, Array(10, "pt"))
if (pointFeature != null) {
    builder.addFeature(pointFeature)
}
```

## API Test: `addGeometry`

### Signature
```scala
def addGeometry(geometry: Geometry, title: String): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:169_

_Source doc:_ Adds the given geometry to the canvas. This method might simplify, drop, or combine geometries to accommodate the given geometry without getting too big. @param geometry the geometry to add @param title an optional title to attach to the geometry in the SVG file @return `true` if the state of the canvas was modified.

### Goal
The `addGeometry` function adds a specified geometry to the canvas, potentially modifying the existing geometries to ensure the canvas remains manageable.

### Parameters
- `geometry` (`Geometry`): The geometry object to be added to the canvas. This can represent various geometric shapes such as points, lines, or polygons.
- `title` (`String`): An optional title that can be attached to the geometry for identification purposes in the SVG file. If not provided, it can be set to `null`.

### Input
The caller must provide a valid `Geometry` object and an optional `String` for the title. The geometry should be compatible with the canvas's existing geometries, and the canvas must be initialized before calling this method.

### Output
Returns `Boolean` — `true` if the state of the canvas was modified by the addition of the geometry, indicating that the geometry was successfully added or combined with existing geometries.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(5, 5)), null)
```

### LLM Instruction Prompt
- Ensure that the `geometry` provided is a valid instance of the `Geometry` class and that the canvas is properly initialized before calling `addGeometry`. The `title` can be `null` if no title is needed.

### Prompt Snippet
```text
Add a geometry to the canvas using the `addGeometry` method, ensuring the geometry is valid and the canvas is initialized.
```

### Common Failure Modes
- Attempting to add a geometry when the canvas is not initialized will result in an error.
- Adding geometries that exceed the canvas's capacity may lead to no geometries being added, as the method may simplify or drop geometries to maintain size.

### Fix Code Hint
```scala
// Ensure the canvas is initialized and the geometry is valid before calling addGeometry
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val point = factory.createPoint(new CoordinateXY(10, 10))
if (!canvas.addGeometry(point, "Point Title")) {
  println("The canvas was not modified; check geometry size.")
}
```

## API Test: `addTile`

### Signature
```scala
private[raptor] def addTile[U](tile: ITile[U]): Unit
def addTile(tile: ITile[T]): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:52  (+2 more definition site/overload)_

_Source doc:_ Adds the given input tile into this partial convolution tile @param tile the tile to compute into this tile

### Goal
The `addTile` function integrates a specified input tile into the current convolution tile, facilitating the accumulation of pixel values for further processing in geospatial raster analysis.

### Parameters
- `tile` (`ITile[U]`): The input tile to be added, which contains pixel data that will be combined with the existing data in the convolution tile.

### Input
The caller must provide an `ITile[U]` instance, which represents a raster tile containing pixel values. The input tile should be compatible in terms of pixel type with the convolution tile it is being added to.

### Output
Returns `Unit` — this indicates that the operation is performed without returning a value, signifying successful integration of the input tile into the convolution tile.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326, new AffineTransform())
val tile1 = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile1.setPixelValue(0, 0, 0.5f)
val convWindow1 = new ConvolutionTileSingleBand(0, metadata, tile1.rasterFeature, 1, Array.fill(9)(0.11f), tile1.tileID)
convWindow1.addTile(tile1)
```

### LLM Instruction Prompt
- When calling `addTile`, ensure that the input tile is of the correct type and is compatible with the existing convolution tile. The operation should be performed within the context of a convolution tile instance.

### Prompt Snippet
```text
To add a tile to a convolution tile, use the `addTile` method on the convolution tile instance, passing in the tile you wish to integrate.
```

### Common Failure Modes
- Attempting to add a tile of an incompatible pixel type may result in a runtime error.
- If the convolution tile is not properly initialized, calling `addTile` may lead to unexpected behavior or exceptions.

### Fix Code Hint
```scala
Ensure that the tile being added is of the same pixel type as the convolution tile. Initialize the convolution tile correctly before calling `addTile`.
```

## API Test: `affineTransform`

### Signature
```scala
def affineTransform(matrix: AffineTransform): SpatialGeneratorBuilder
def affineTransform(geometry: Geometry): Geometry
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:85  (+1 more definition site/overload)_

_Source doc:_ Transform the given geometry using the affine transformation of this generator and returns the transformed geometry @param geometry the geometry to transform @return the transformed geometry

### Goal
The `affineTransform` function applies an affine transformation to a given geometry, enabling users to manipulate spatial data for geospatial analysis.

### Parameters
- `geometry` (`Geometry`): The geometry object that will be transformed using the affine transformation. This can represent various geometric shapes such as points, lines, or polygons.

### Input
The input must be a valid `Geometry` object. Ensure that the geometry is properly defined and compatible with the affine transformation being applied.

### Output
Returns `Geometry` — the transformed geometry after applying the affine transformation. The output retains the same geometric type as the input but with modified coordinates based on the transformation.

### Valid Call Patterns
```scala
val transform = new AffineTransform()
transform.scale(2.0, 1.0)
transform.translate(0.0, 3.0)
println(sparkContext.generateSpatialData
  .affineTransform(transform)
  .uniform(1000)
  .summary)
```

### LLM Instruction Prompt
- When calling `affineTransform`, ensure that the input is a valid `Geometry` object and that the affine transformation is correctly defined.

### Prompt Snippet
```text
Transform the geometry using the affine transformation defined by the AffineTransform object.
```

### Common Failure Modes
- Attempting to transform a `Geometry` object that is not properly defined or is null will result in an error.
- Using an incompatible affine transformation matrix may lead to unexpected results or runtime exceptions.

### Fix Code Hint
```scala
// Ensure the geometry is valid and properly defined before calling affineTransform
val validGeometry: Geometry = // obtain or create a valid Geometry object
val transformedGeometry = sparkContext.generateSpatialData.affineTransform(validGeometry)
```

## API Test: `append`

### Signature
```scala
def append(feature: IFeature, value: Any, name: String = null, dataType: DataType = null): IFeature
def append(rasterFeature: RasterFeature, name: String, value: Any): RasterFeature
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/Feature.scala:405  (+1 more definition site/overload)_

_Source doc:_ Appends an additional attribute to the given feature and returns a new feature @param feature the feature to append to. This feature is not modified. @param value the value to append. @param name (Optional) the name of the new attribute @param dataType (Optional) the type of the additional attribute. @return a new feature that contains the geometry and all attributes of the input feature + the new attribute.

### Goal
The `append` function adds an additional attribute to a geospatial feature, returning a new feature that includes the original geometry and attributes along with the new attribute.

### Parameters
- `feature` (`IFeature`): The geospatial feature to which the new attribute will be appended. This feature remains unchanged.
- `value` (`Any`): The value of the new attribute to be added to the feature. This can be of any type.
- `name` (`String`), default `null`: The name of the new attribute being added. If not provided, the attribute will not have a specific name.
- `dataType` (`DataType`), default `null`: The type of the new attribute. If not specified, the type will be inferred from the value.

### Input
The caller must provide a valid `IFeature` object, which represents a geospatial feature, and a value of any type to append as an attribute. The `name` and `dataType` parameters are optional.

### Output
Returns `IFeature` — a new feature that contains the original geometry and attributes of the input feature, plus the newly appended attribute.

### Valid Call Patterns
```scala
val finalResults: RDD[IFeature] = sjResults.map(pip => {
  val polygon: IFeature = pip._1
  val point: IFeature = pip._2
  Feature.append(point, polygon.getAs[String]("NAME"), "state")
})
```

### LLM Instruction Prompt
- When calling `append`, ensure that the `feature` is a valid `IFeature` and that the `value` is of a compatible type. The `name` and `dataType` parameters are optional but should be provided if specific naming or typing is required.

### Prompt Snippet
```text
To append an attribute to a feature, use the `append` method with the feature, value, and optionally, the name and data type of the new attribute.
```

### Common Failure Modes
- Providing a `feature` that is not an instance of `IFeature` will result in a type error.
- If the `value` is of an unexpected type that cannot be handled by the feature's attribute system, it may lead to runtime errors.

### Fix Code Hint
```scala
// Ensure that the feature is of type IFeature and the value is of a compatible type.
val newFeature = Feature.append(existingFeature, newValue, "attributeName", DataType.String)
```

## API Test: `area`

### Signature
```scala
def area: Double
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115_

### Goal
Calculates the area of a geometric shape represented in the raster data.

### Parameters
_None._

### Input
The caller must provide a geometric shape that has been defined within the context of the raster data. This shape should be compatible with the raster's coordinate reference system (CRS) and resolution.

### Output
Returns `Double` — the area of the geometric shape in the same units as the raster's coordinate system.

### Valid Call Patterns
```scala
val shapeArea: Double = value.area
```

### LLM Instruction Prompt
- Ensure that the geometric shape is properly defined and compatible with the raster data before calling `area`.

### Prompt Snippet
```text
Calculate the area of the defined geometric shape using the area method.
```

### Common Failure Modes
- Calling `area` on a shape that is not defined or is incompatible with the raster data may result in a runtime error.
- If the shape is empty or invalid, the method may return an unexpected value (e.g., zero or NaN).

### Fix Code Hint
```scala
// Ensure the shape is valid and defined before calling area
if (shape.isDefined) {
  val shapeArea: Double = shape.area
} else {
  // Handle the case where the shape is not defined
}
```

## API Test: `available`

### Signature
```scala
override def available(): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:99  (+1 more definition site/overload)_

### Goal
The `available` function returns the number of bytes that can be read from the input stream without blocking, which is useful for understanding how much data is ready to be processed in a geospatial raster processing context.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Int` — the number of bytes available to read from the input stream, indicating how much data can be processed immediately.

### Valid Call Patterns
```scala
val bytesAvailable: Int = value.available()
```

### LLM Instruction Prompt
- When calling `available`, ensure that the input stream is properly initialized and opened before invoking this method to avoid unexpected results.

### Prompt Snippet
```text
To check how many bytes are available for reading from the input stream, use the `available` method like this: `val bytesAvailable: Int = value.available()`.
```

### Common Failure Modes
- Calling `available` on a closed or uninitialized input stream may lead to unexpected behavior or exceptions.
- If the underlying stream is not properly set up, the returned value may not accurately reflect the available data.

### Fix Code Hint
```scala
// Ensure the input stream is open before calling available
if (inputStream.isOpen) {
  val bytesAvailable: Int = inputStream.available()
} else {
  // Handle the case where the stream is not open
}
```

## API Test: `bit`

### Signature
```scala
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): JavaSpatialRDD
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:139  (+1 more definition site/overload)_

_Source doc:_ Generate data from the bit distribution @param cardinality the number of records to generate @param digits the number of digits to set per coordinate @param probability the probability of setting each bit @return the RDD that contains the generated data

### Goal
The `bit` function generates spatial data based on a bit distribution, allowing users to create random points with specified characteristics.

### Parameters
- `cardinality` (`Long`): The total number of records (points) to generate. This value should be a positive integer representing how many spatial data points you want.
- `digits` (`Int`), default `10`: The number of digits to set per coordinate. This determines the precision of the generated coordinates, with higher values allowing for more detailed spatial representation.
- `probability` (`Double`), default `0.2`: The probability of setting each bit in the generated data. This value should be between `0.0` and `1.0`, where lower values result in sparser data and higher values lead to denser data.

### Input
The caller must provide a valid Spark context to execute the function. No specific file formats are required as this function generates data programmatically.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial data points based on the specified bit distribution parameters.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .bit(1000, digits = 10, probability = 0.2)
```

### LLM Instruction Prompt
- When calling `bit`, ensure that the `cardinality` is a positive `Long`, `digits` is a non-negative `Int`, and `probability` is a `Double` between `0.0` and `1.0`.

### Prompt Snippet
```text
Generate spatial data using the bit distribution with specified cardinality, digits, and probability.
```

### Common Failure Modes
- Providing a negative value for `cardinality` will result in an error, as it must be a positive integer.
- Setting `digits` to a negative value will also cause an error, as it must be a non-negative integer.
- If `probability` is outside the range of `0.0` to `1.0`, the function may not behave as expected.

### Fix Code Hint
```scala
// Ensure cardinality is positive, digits is non-negative, and probability is between 0.0 and 1.0
val randomPoints: SpatialRDD = sc.generateSpatialData.bit(1000, digits = 10, probability = 0.2)
```

## API Test: `build`

### Signature
```scala
def build(): VectorTile.Tile.Layer
override def build(): Scan
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:133  (+4 more definition site/overload)_

_Source doc:_ Finalize the layer and return it @return

### Goal
Finalize the vector layer by compiling all added features and return the constructed layer.

### Parameters
_None._

### Input
The caller must have previously added features to the `VectorLayerBuilder` instance using the `addFeature` method. There are no specific file formats required as input, but the features must be valid geometries and attributes.

### Output
Returns `VectorTile.Tile.Layer` — this represents the finalized vector layer containing all the features that were added, structured in a way that can be used for further processing or visualization.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"), null, Array(10, "pt")))
val layer = builder.build()
```

### LLM Instruction Prompt
- Ensure that the `build` method is called on an instance of `VectorLayerBuilder` after features have been added. Do not call `build` without adding features first.

### Prompt Snippet
```text
To finalize the vector layer, ensure you have added features using the `addFeature` method before calling `build()`.
```

### Common Failure Modes
- Calling `build` without adding any features will result in an empty layer, which may not be useful for further processing.
- Attempting to add features with invalid geometries or attributes may lead to runtime errors.

### Fix Code Hint
```scala
Ensure that you have added at least one valid feature to the builder before calling `build()`.
```

## API Test: `buildIndex`

### Signature
```scala
def buildIndex(sparkContext: SparkContext, dir: String, indexFile: String): Unit
private def buildIndex(sparkContext: SparkContext, fs: FileSystem, basePath: String): Map[String, (Int, String)]
private def buildIndex(fs: FileSystem, basePath: String): Map[String, (Int, String)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:186  (+2 more definition site/overload)_

_Source doc:_ Build a raster index on all GeoTIFF files in a directory. @param sparkContext spark context to parallelize index creation @param dir the directory that contains raster files @param indexFile the path of the index file to write

### Goal
The `buildIndex` function creates an index for GeoTIFF files located in a specified directory, facilitating efficient access and processing of raster data in large-scale geospatial analyses.

### Parameters
- `sparkContext` (`SparkContext`): The Spark context used to parallelize the index creation process, allowing for distributed computation across a Spark cluster.
- `dir` (`String`): The directory path containing the GeoTIFF files that need to be indexed.
- `indexFile` (`String`): The file path where the generated index will be saved, typically in CSV format.

### Input
The caller must provide a directory containing valid GeoTIFF files. The directory must be accessible by the Spark context, and the files should be in a format compatible with the RDPro library.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of creating and saving an index file at the specified path.

### Valid Call Patterns
```scala
RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)
```

### LLM Instruction Prompt
- When calling `buildIndex`, ensure that the `sparkContext` is properly initialized and that the `dir` contains valid GeoTIFF files. The `indexFile` path should be writable.

### Prompt Snippet
```text
To create an index for GeoTIFF files, use the buildIndex function with a valid SparkContext, directory containing the files, and a path for the index file.
```

### Common Failure Modes
- The specified directory does not exist or is not accessible, leading to a failure in reading the GeoTIFF files.
- The `sparkContext` is not properly initialized, which can cause the function to fail during execution.
- The `indexFile` path is invalid or not writable, resulting in an error when attempting to save the index.

### Fix Code Hint
```scala
// Ensure the directory exists and contains GeoTIFF files before calling buildIndex
val dir = new File("path/to/your/geotiff/directory")
if (dir.exists() && dir.isDirectory) {
    RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)
} else {
    throw new IllegalArgumentException("Directory does not exist or is not a valid directory.")
}
```

## API Test: `call`

### Signature
```scala
override def call(f: IFeature): Int
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/FeatureWriterSize.scala:31_

_Source doc:_ For Java callers

### Goal
The `call` function processes a given feature and returns an integer value, which may represent a specific property or characteristic of the feature in the context of geospatial analysis.

### Parameters
- `f` (`IFeature`): An instance of `IFeature` representing a geospatial feature that is to be processed. This feature can include various geometries and associated attributes.

### Input
The caller must provide an `IFeature` instance, which is expected to be properly initialized and contain valid geometrical data. The feature should conform to the specifications of the geospatial data being processed.

### Output
Returns `Int` — the integer value returned by the `call` function may represent a size, identifier, or other relevant metric associated with the processed feature.

### Valid Call Patterns
```scala
val feature: IFeature = // initialize your IFeature instance
val result: Int = someObject.call(feature)
```

### LLM Instruction Prompt
- When calling `call`, ensure that the provided `IFeature` instance is correctly initialized and contains valid geometrical data.

### Prompt Snippet
```text
Call the `call` method with a valid `IFeature` instance to obtain an integer result representing a property of the feature.
```

### Common Failure Modes
- Providing a null or uninitialized `IFeature` instance will result in a runtime error.
- The `IFeature` must contain valid geometrical data; otherwise, the processing may yield incorrect results or exceptions.

### Fix Code Hint
```scala
// Ensure the IFeature is properly initialized before calling
val feature: IFeature = Feature.create(null, new PointND(geometryFactory, 2, 0, 0))
val result: Int = someObject.call(feature)
```

## API Test: `checkOptions`

### Signature
```scala
def checkOptions(options: ParsedCommandLineOptions, out: PrintStream): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:293_

_Source doc:_ Check if the user options are valid. This means that the user did not add any unexpected options or leave out any required option @param options parsed command line options. @return

### Goal
`checkOptions` validates the user-provided command line options to ensure that all required options are present and no unexpected options are included.

### Parameters
- `options` (`ParsedCommandLineOptions`): Represents the parsed command line options provided by the user. This includes both required and optional parameters that the user intends to use in the RDPro operations.
- `out` (`PrintStream`): A stream to which output messages (such as error messages) can be printed. This is typically used for logging or displaying feedback to the user.

### Input
The caller must provide a valid instance of `ParsedCommandLineOptions` that contains the command line arguments parsed from user input. The input must conform to the expected structure defined by the RDPro application, including all required parameters.

### Output
Returns `Boolean` — `true` if the provided options are valid (i.e., all required options are present and no unexpected options are included), and `false` otherwise.

### Valid Call Patterns
```scala
// Example of checking user options
val commandLineOptions = OperationHelper.parseCommandLineArguments("test", "path1", "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")
assert(!OperationHelper.checkOptions(commandLineOptions, new PrintStream(new NullOutputStream)))

// Example of valid options
val parsedOptions2 = OperationHelper.parseCommandLineArguments("subtest1", "path1", "sparam2:1", "-sparam", "-no-param1[0]", "path2")
assert(OperationHelper.checkOptions(parsedOptions2, new PrintStream(new NullOutputStream)))
```

### LLM Instruction Prompt
- When calling `checkOptions`, ensure that the `options` parameter is a valid instance of `ParsedCommandLineOptions` containing the necessary command line arguments, and that the `out` parameter is a valid `PrintStream` for output.

### Prompt Snippet
```text
Check if the user options are valid using the checkOptions function.
```

### Common Failure Modes
- Providing a `ParsedCommandLineOptions` instance that is missing required parameters will result in a return value of `false`.
- Including unexpected options in the `ParsedCommandLineOptions` will also lead to a return value of `false`.

### Fix Code Hint
```scala
Ensure that all required options are included in the command line arguments and that no unexpected options are present before calling checkOptions.
```

## API Test: `compress`
_Grounding: doc-repaired from source (docfix)._

### Goal
Compresses a `MemoryTile`'s pixel data in-place using GZIP. This is a `protected[raptor]` method intended for internal library use and is not part of the public API. Users must not call this method directly. The `MemoryTile` class manages compression and decompression automatically; for example, `getPixelValue` will decompress data on-the-fly if needed.

### Valid Call Patterns|Valid Access Patterns
This method is `protected[raptor]` and cannot be called directly from user code outside that package. The following pattern uses Java reflection for demonstration and is not a standard use case.

```scala
// This pattern is for testing/demonstration only. Do not use in production code.
// Requires the following imports:
import edu.ucr.cs.bdlab.raptor.MemoryTile
import edu.ucr.cs.bdlab.beast.geolite.{RasterMetadata, RasterFeature}
import java.awt.geom.AffineTransform

// 1. A MemoryTile must be initialized with valid RasterMetadata (8 arguments).
val g2w = new AffineTransform()
val metadata = new RasterMetadata(0, 0, 100, 100, 100, 100, 4326, g2w)
val feature = RasterFeature.create(Array("fileName"), Array("testFile.tif"))
val tile = new MemoryTile[Array[Byte]](0, metadata, feature)
tile.setPixelValue(50, 50, Array[Byte](120, 34, 56))

// 2. Invoke the protected 'compress' method via reflection.
val compressMethod = tile.getClass.getDeclaredMethod("compress")
compressMethod.setAccessible(true)
compressMethod.invoke(tile)

// 3. Verification: getPixelValue implicitly decompresses the data.
val valueAfterCompress = tile.getPixelValue(50, 50)
require(valueAfterCompress.sameElements(Array[Byte](120, 34, 56)))
```

### LLM Instruction Prompt
- Do not call the `compress` method directly. It is a protected, internal-only method.
- To interact with pixel data on a `MemoryTile`, use public methods like `getPixelValue`. The library handles compression and decompression automatically.

### Prompt Snippet
```text
Do not call the `compress` method. Use `getPixelValue` to read pixel data; the tile will decompress automatically if needed.
```

### Common Failure Modes
- A direct call like `tile.compress` from user code will cause a compile-time error: `method compress in class MemoryTile cannot be accessed in ...`. This is because the method is `protected[raptor]` and not part of the public API.
- Instantiating `RasterMetadata` with the wrong number of arguments (e.g., nine instead of the required eight) will cause a compile-time error.

### Fix Code Hint
- **Wrong:** `tile.compress`
- **Corrected:** Do not call `compress` manually. The library manages this internally. Simply use accessor methods, which will trigger decompression as needed.
  ```scala
  // Correct usage: Let the library manage compression/decompression.
  val pixelValue = tile.getPixelValue(x, y) // Decompresses automatically if tile was compressed.
  ```

## API Test: `compute`

### Signature
```scala
override def compute(split: Partition, context: TaskContext): Iterator[ITile[T]]
protected def compute(geometries: Array[_<:Geometry], metadata: RasterMetadata): Unit
def compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int): Unit
override def compute(split: Partition, context: TaskContext): Iterator[IFeature]
override def compute(split: Partition, context: TaskContext): Iterator[(EnvelopeNDLite, (Iterator[IFeature], Iterator[IFeature]))]
override def compute(split: Partition, context: TaskContext): Iterator[(Iterator[T], Iterator[U])]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119  (+8 more definition site/overload)_

_Source doc:_ Compute the intersections for the given linear ring @param pID the ID of the polygon @param ring the list of coordinates that make the ring already projected to the raster space @param w the width of the raster in pixels @param h the height of the raster in pixels

### Goal
The `compute` function calculates the intersections of a specified linear ring with a raster grid, enabling geospatial analysis of polygonal areas within raster datasets.

### Parameters
- `pID` (`Int`): The ID of the polygon for which intersections are being computed. This should be a unique identifier for the polygon.
- `ring` (`CoordinateSequence`): A sequence of coordinates that define the linear ring, which must be projected to the raster space. This represents the boundary of the polygon.
- `w` (`Int`): The width of the raster in pixels. This defines the horizontal resolution of the raster grid.
- `h` (`Int`): The height of the raster in pixels. This defines the vertical resolution of the raster grid.

### Input
The caller must provide a valid `CoordinateSequence` that represents the polygon's boundary, along with the raster dimensions (width and height) as integers. The `pID` should be a valid integer identifier for the polygon.

### Output
Returns `Unit` — this indicates that the function performs its computation without returning a value. The results of the intersections are likely stored or processed internally.

### Valid Call Patterns
```scala
val ring: CoordinateSequence = // initialize with appropriate coordinates
val pID: Int = 1 // example polygon ID
val width: Int = 100 // example width in pixels
val height: Int = 100 // example height in pixels
intersections.compute(pID, ring, width, height)
```

### LLM Instruction Prompt
- Ensure that the `ring` parameter is a valid `CoordinateSequence` and that `pID`, `w`, and `h` are appropriate integers representing the polygon ID and raster dimensions.

### Prompt Snippet
```text
Compute the intersections for the polygon with ID 1 using the provided coordinate ring and raster dimensions.
```

### Common Failure Modes
- Providing an invalid `CoordinateSequence` that does not represent a closed linear ring.
- Using negative or zero values for `w` or `h`, which would not be valid raster dimensions.
- Using a `pID` that does not correspond to a valid polygon in the context of the application.

### Fix Code Hint
```scala
// Ensure the CoordinateSequence is properly defined and closed
val ring: CoordinateSequence = // create a valid closed CoordinateSequence
val pID: Int = 1 // ensure this ID is valid
val width: Int = 100 // must be positive
val height: Int = 100 // must be positive
intersections.compute(pID, ring, width, height)
```

## API Test: `computeForFeatures`

### Signature
```scala
def computeForFeatures(features: SpatialRDD, synopsisSize: Long = 1024 * 1024): Synopsis
def computeForFeatures(features: SpatialRDD, sizeFunction: IFeature => Int = f => f.getStorageSize) : Summary
def computeForFeatures(features : JavaSpatialRDD) : Summary
def computeForFeatures(features: SpatialRDD, numPartitions: Int*): (Summary, RDD[(Array[Int], Summary)])
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Synopsis.scala:34  (+3 more definition site/overload)_

### Goal
Computes a set of summaries for each grid cell in the bounding box of the input features, facilitating geospatial analysis.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features that will be summarized. This should contain geometries and associated attributes relevant to the analysis.
- `numPartitions` (`Int*`): An optional variable-length argument specifying either the total number of cells or an array of the number of partitions along each dimension for the grid.

### Input
The caller must provide a `SpatialRDD` containing spatial features. The input data should be properly formatted and loaded into the `SpatialRDD` before calling this function. Ensure that the features are within a defined bounding box for accurate summarization.

### Output
Returns a tuple containing a `Summary` for the entire dataset and an `RDD` of local summaries for each grid cell in the bounding box. The `Summary` provides aggregated statistics, while the `RDD` contains summaries indexed by grid cell coordinates.

### Valid Call Patterns
```scala
val features = new RandomSpatialRDD(sparkContext, UniformDistribution, 100, opts = "seed" -> 0)
val (globalSummary, localSummaries) = computeForFeatures(features)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing spatial data. The `numPartitions` parameter is optional and can be omitted if default partitioning is acceptable.

### Prompt Snippet
```text
Compute summaries for the provided spatial features using computeForFeatures.
```

### Common Failure Modes
- Providing an empty or improperly formatted `SpatialRDD` will result in errors during computation.
- Specifying an incorrect number of partitions may lead to inefficient processing or runtime exceptions.

### Fix Code Hint
```scala
// Ensure the SpatialRDD is properly initialized and contains valid spatial features.
val features = new RandomSpatialRDD(sparkContext, UniformDistribution, 100, opts = "seed" -> 0)
val (globalSummary, localSummaries) = computeForFeatures(features)
```

## API Test: `computeForFeaturesWithOutputSize`

### Signature
```scala
def computeForFeaturesWithOutputSize(features: JavaSpatialRDD, opts: BeastOptions) : Summary
def computeForFeaturesWithOutputSize(features : SpatialRDD, opts : BeastOptions) : Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GeometricSummary.scala:49  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
Computes the estimated output size for the given spatial features based on specified options.

### Parameters
- `features` (`JavaSpatialRDD`): A collection of spatial features that will be analyzed to estimate the output size. This should contain geometries and associated attributes.
- `opts` (`BeastOptions`): Configuration options for the computation, which may include parameters like output format and other processing options.

### Input
The input must consist of a valid `JavaSpatialRDD` containing spatial features. The `BeastOptions` must be properly configured to specify how the output size should be estimated, including any relevant parameters.

### Output
Returns `Summary` — an object that encapsulates the estimated output size and other relevant statistics about the computation.

### Valid Call Patterns
```scala
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `JavaSpatialRDD` and that `opts` is a properly configured `BeastOptions` instance before calling `computeForFeaturesWithOutputSize`.

### Prompt Snippet
```text
To estimate the output size for the given spatial features, use the `computeForFeaturesWithOutputSize` method with a valid `JavaSpatialRDD` and appropriate `BeastOptions`.
```

### Common Failure Modes
- The `features` parameter is not a valid `JavaSpatialRDD`, which will result in a type mismatch error.
- The `opts` parameter is not properly configured, leading to unexpected behavior or errors during computation.

### Fix Code Hint
```scala
// Ensure that features is a valid JavaSpatialRDD and opts is correctly set up
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
```

## API Test: `computePointHistogramSparse`

### Signature
```scala
@varargs def computePointHistogramSparse(features: SpatialRDD, sizeFunction: IFeature => Int, mbb: EnvelopeNDLite, numBuckets: Int*): UniformHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/HistogramOP.scala:72_

_Source doc:_ Compute a point histogram for sparse histograms. It maps each record to a bucket and then aggregate by bucket. This method can be helpful for very large histograms to avoid moving the entire histogram during the reduce step. @param features the features to compute their histogram @param sizeFunction the function that evaluates the size of each feature @param mbb the minimum bounding box of the histogram, typically, this is the same as the input MBB @param numBuckets the number of buckets in the histogram @return the computed histogram

### Goal
`computePointHistogramSparse` computes a histogram of point features in a spatial dataset, efficiently aggregating data into specified buckets.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features from which the histogram will be computed. Each feature represents a point in a multi-dimensional space.
- `sizeFunction` (`IFeature => Int`): A function that takes an `IFeature` and returns an integer representing the size of that feature. This is used to determine how to aggregate the features into histogram buckets.
- `mbb` (`EnvelopeNDLite`): The minimum bounding box that defines the spatial extent of the histogram. This typically matches the spatial extent of the input features.
- `numBuckets` (`Int*`): A variable-length argument representing the number of buckets to divide the histogram into. This allows for flexible bucket sizing based on the user's needs.

### Input
The input must consist of a `SpatialRDD` containing point features, a valid `sizeFunction` that can evaluate the size of each feature, a defined `EnvelopeNDLite` for the bounding box, and an integer specifying the number of buckets. The `SpatialRDD` should be properly initialized and contain valid spatial data.

### Output
Returns `UniformHistogram` — an object representing the computed histogram, which contains the distribution of point features across the specified buckets. The histogram can be queried for the number of partitions and the values in each bucket.

### Valid Call Patterns
```scala
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0))
))
val mbr = points.summary
val histogram: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _ => 1, mbr, 4)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing point features.
- The `sizeFunction` must be a function that correctly evaluates the size of each feature.
- The `mbb` must be a valid `EnvelopeNDLite` that encompasses the spatial extent of the features.
- The `numBuckets` should be specified as an integer or a sequence of integers.

### Prompt Snippet
```text
Compute a point histogram using `computePointHistogramSparse` with a valid `SpatialRDD`, a size function, a bounding box, and the desired number of buckets.
```

### Common Failure Modes
- Providing an empty or improperly initialized `SpatialRDD` will result in an error.
- If the `sizeFunction` does not return an integer, the computation will fail.
- An `EnvelopeNDLite` that does not encompass the features may lead to incorrect histogram results.
- Specifying a negative or zero value for `numBuckets` will cause an error.

### Fix Code Hint
```scala
// Ensure the SpatialRDD is properly initialized and contains valid point features
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0))
))

// Define a valid size function
val sizeFunction: IFeature => Int = _ => 1

// Create a valid minimum bounding box
val mbr = points.summary

// Call the computePointHistogramSparse function with valid parameters
val histogram: UniformHistogram = HistogramOP.computePointHistogramSparse(points, sizeFunction, mbr, 4)
```

## API Test: `config`

### Signature
```scala
def config(key: String, value: Any): JavaSpatialGeneratorBuilder
def config(opts: BeastOptions): JavaSpatialGeneratorBuilder
def config(key: String, value: Any): SpatialGeneratorBuilder
def config(opts: BeastOptions): SpatialGeneratorBuilder
def config: Map[String, String]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:32  (+4 more definition site/overload)_

_Source doc:_ Set configuration of the generated data

### Goal
The `config` function sets configuration options for the spatial data generation process in RDPro, allowing users to customize parameters for generating raster or vector data.

### Parameters
- `key` (`String`): The name of the configuration option to set. Expected values include specific parameters related to spatial generation, such as `UniformDistribution.MaxSize`, `UniformDistribution.NumSegments`, and `SpatialGenerator.Seed`.
- `value` (`Any`): The value to assign to the specified configuration key. This can be a numeric value, a string, or other types depending on the key being set.

### Input
The caller must provide a valid `SpatialGeneratorBuilder` instance to invoke `config`. The input parameters must match the expected types for the specified configuration keys.

### Output
Returns `JavaSpatialGeneratorBuilder` — an instance of the builder that has been configured with the specified options, which can be used to generate spatial data.

### Valid Call Patterns
```scala
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```

### LLM Instruction Prompt
- When calling `config`, ensure that the `key` corresponds to a valid configuration option and that the `value` is of the appropriate type for that option.

### Prompt Snippet
```text
To configure the spatial generator, use the `config` method with the appropriate key and value. For example, to set the maximum size of the uniform distribution, call `config(UniformDistribution.MaxSize, "0.2,0.1")`.
```

### Common Failure Modes
- Providing an invalid `key` that does not correspond to a recognized configuration option will result in an error.
- Setting a `value` of the wrong type for the specified `key` may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure that the key is valid and the value matches the expected type
val builder = new SpatialGeneratorBuilder(sparkContext)
builder.config(UniformDistribution.MaxSize, "0.2,0.1") // Correct usage
```

## API Test: `construct`

### Signature
```scala
def construct(out: DataOutput, entries: Array[(Long, Long, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:38_

_Source doc:_ Construct a compact hashtable for the given list of entries and write to the given output @param out the data output to write the hashtable to @param entries the list of entries in the form (key=tileID, val1=Offset, val2=Length)

### Goal
The `construct` function creates a compact hashtable from a specified list of entries and writes it to a designated output stream.

### Parameters
- `out` (`DataOutput`): The output stream where the constructed hashtable will be written. This should be an instance of `DataOutput` that is ready to receive binary data.
- `entries` (`Array[(Long, Long, Int)]`): An array of tuples representing the entries to be included in the hashtable, where each tuple consists of a `tileID` (key), an `Offset` (val1), and a `Length` (val2).

### Input
The caller must provide:
- A valid `DataOutput` instance that is open for writing.
- An array of entries formatted as `Array[(Long, Long, Int)]`, where each entry must contain valid long integers for `tileID` and `Offset`, and a valid integer for `Length`.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of writing the hashtable to the specified output.

### Valid Call Patterns
```scala
val rand = new Random(0)
val entries = new Array[(Long, Long, Int)](100).map( _ => (rand.nextLong().abs, rand.nextLong().abs, rand.nextInt().abs))
val file = new Path(scratchPath, "test")
val fileSystem = file.getFileSystem(sparkContext.hadoopConfiguration)
val out = fileSystem.create(file)
DiskTileHashtable.construct(out, entries)
out.close()
```

### LLM Instruction Prompt
- When calling `construct`, ensure that the `out` parameter is a valid `DataOutput` instance and that `entries` is an array of tuples formatted correctly as `(Long, Long, Int)`.

### Prompt Snippet
```text
To use the `construct` function, provide a valid DataOutput stream and an array of entries formatted as (tileID, Offset, Length).
```

### Common Failure Modes
- Providing a `DataOutput` that is not open for writing will result in an `IOException`.
- Passing an incorrectly formatted `entries` array (e.g., containing non-Long or non-Int values) will lead to a runtime error.

### Fix Code Hint
```scala
// Ensure the DataOutput is properly initialized and open before calling construct
val out: DataOutput = ... // Initialize your DataOutput here
val entries: Array[(Long, Long, Int)] = ... // Ensure this is correctly formatted
DiskTileHashtable.construct(out, entries)
```

## API Test: `copyResource`

### Signature
```scala
def copyResource(resourcePath: String, filePath: File, overwrite: Boolean): Unit
def copyResource(resourcePath: String, filePath: File): Unit
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:251  (+1 more definition site/overload)_

_Source doc:_ Copy a resource to a temporary file to allow reading it as a file. @param resourcePath the path of the resource to read @param filePath     the path of the file to write @param overwrite    set this flag to automatically overwrite the output file.

### Goal
`copyResource` copies a specified resource file to a designated file path, allowing it to be accessed as a regular file in the context of geospatial raster processing.

### Parameters
- `resourcePath` (`String`): The path of the resource to read, typically a relative path to a resource within the project or a classpath resource.
- `filePath` (`File`): The path of the file to write, which should be a valid file location on the filesystem where the resource will be copied.
- `overwrite` (`Boolean`): A flag indicating whether to overwrite the output file if it already exists. If set to `true`, the existing file will be replaced.

### Input
The caller must provide:
- A valid `resourcePath` that points to an existing resource.
- A `filePath` that specifies a writable location on the filesystem.
- The `overwrite` flag to control file replacement behavior.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value, but the side effect is the creation or replacement of the specified file at `filePath`.

### Valid Call Patterns
```scala
copyResource("/test.points", new File(path, "input.txt"), true)
copyResource("/test.points", new File(path, "_input.txt"), false)
```

### LLM Instruction Prompt
- When calling `copyResource`, ensure that the `resourcePath` is a valid string pointing to an existing resource, `filePath` is a valid writable file location, and the `overwrite` flag is set according to the desired file handling behavior.

### Prompt Snippet
```text
Copy the resource from the specified resourcePath to the filePath, ensuring that the overwrite flag is set correctly based on whether you want to replace an existing file.
```

### Common Failure Modes
- Providing an invalid `resourcePath` that does not exist will result in a failure to copy the resource.
- Specifying a `filePath` that points to a location where the user does not have write permissions will cause an error.
- If `overwrite` is set to `false` and the file already exists at `filePath`, the operation will fail without replacing the existing file.

### Fix Code Hint
```scala
// Ensure the resourcePath is correct and the filePath is writable
val resourcePath = "/test.points"
val filePath = new File(path, "input.txt")
copyResource(resourcePath, filePath, true) // Set overwrite to true if you want to replace existing files
```

## API Test: `count`

### Signature
```scala
def count: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860_

### Goal
Returns the number of elements in the raster dataset, providing a count of the total pixels or tiles processed.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded into an appropriate RDD format. This dataset should be compatible with the operations defined in RDPro, such as those loaded from GeoTIFF files.

### Output
Returns `Int` — the total count of pixels or tiles in the raster dataset.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val pixelCount: Int = raster.count
```

### LLM Instruction Prompt
- Ensure that the `count` method is called on a valid raster dataset that has been loaded into an RDD format.

### Prompt Snippet
```text
To get the total number of pixels in the raster dataset, use the count method on the loaded RDD.
```

### Common Failure Modes
- Calling `count` on an uninitialized or empty raster dataset will result in an unexpected count (likely zero).
- Attempting to call `count` on a non-raster RDD will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the raster dataset is properly loaded before calling count
val raster: RDD[ITile[Int]] = sc.geoTiff("your_raster_file.tif")
val pixelCount: Int = raster.count
```

## API Test: `create`

### Signature
```scala
def create(x1: Double, y1:Double, x2: Double, y2:Double, srid: Int, rasterWidth: Int, rasterHeight: Int, tileWidth: Int, tileHeight: Int): RasterMetadata
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:324_

_Source doc:_ Create a raster metadata that represents a geographical region provided by a rectangle. @param x1 the x-coordinate of the left edge of the pixel at (0, 0) @param y1 the y-coordinate of the top edge of the pixel at (0, 0) @param x2 the x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param y2 the y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param srid the SRID that represents the coordinate reference system of the raster @param rasterWidth the number of columns in the entire raster @param rasterHeight the number of rows in the entire raster @param tileWidth the width of each tile in pixels @param tileHeight the height of each tile in pixels @return a raster metadata with the given information

### Goal
Creates raster metadata that defines the spatial extent and properties of a raster dataset.

### Parameters
- `x1` (`Double`): The x-coordinate of the left edge of the pixel at (0, 0). This value should be less than `x2`.
- `y1` (`Double`): The y-coordinate of the top edge of the pixel at (0, 0). This value should be greater than `y2`.
- `x2` (`Double`): The x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1). This value should be greater than `x1`.
- `y2` (`Double`): The y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1). This value should be less than `y1`.
- `srid` (`Int`): The Spatial Reference System Identifier (SRID) that represents the coordinate reference system of the raster. Common values include 4326 for WGS 84.
- `rasterWidth` (`Int`): The number of columns (pixels) in the entire raster. This should be a positive integer.
- `rasterHeight` (`Int`): The number of rows (pixels) in the entire raster. This should be a positive integer.
- `tileWidth` (`Int`): The width of each tile in pixels. This should be a positive integer and typically less than or equal to `rasterWidth`.
- `tileHeight` (`Int`): The height of each tile in pixels. This should be a positive integer and typically less than or equal to `rasterHeight`.

### Input
The caller must provide valid numerical values for the parameters, ensuring that the coordinates (`x1`, `y1`, `x2`, `y2`) define a valid rectangle and that the dimensions (`rasterWidth`, `rasterHeight`, `tileWidth`, `tileHeight`) are positive integers.

### Output
Returns `RasterMetadata` — an object that encapsulates the metadata for the raster, including its spatial extent, resolution, and tiling information.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
```

### LLM Instruction Prompt
- Ensure that all parameters are provided with valid values according to the specifications. The coordinates must define a valid rectangle, and the raster dimensions must be positive integers.

### Prompt Snippet
```text
Create raster metadata for a geographical region defined by the coordinates and dimensions provided.
```

### Common Failure Modes
- Providing coordinates that do not form a valid rectangle (e.g., `x1` is not less than `x2` or `y1` is not greater than `y2`).
- Using non-positive integers for `rasterWidth`, `rasterHeight`, `tileWidth`, or `tileHeight`.

### Fix Code Hint
```scala
// Ensure that the coordinates and dimensions are valid before calling create
if (x1 < x2 && y1 > y2 && rasterWidth > 0 && rasterHeight > 0 && tileWidth > 0 && tileHeight > 0) {
  val metadata = RasterMetadata.create(x1, y1, x2, y2, srid, rasterWidth, rasterHeight, tileWidth, tileHeight)
} else {
  throw new IllegalArgumentException("Invalid parameters for raster metadata creation.")
}
```

## API Test: `createDateFilter`

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
`createDateFilter` generates a filter that allows for the selection of paths based on a specified date range, facilitating the processing of time-sensitive geospatial raster data.

### Parameters
- `dateStart` (`String`): The start date of the range, formatted as "yyyy.mm.dd" (inclusive).
- `dateEnd` (`String`): The end date of the range, formatted as "yyyy.mm.dd" (inclusive).

### Input
The caller must provide two date strings in the format "yyyy.mm.dd" that define the inclusive range for filtering paths. There are no specific file formats required for this function, but the dates must be valid and correctly formatted.

### Output
Returns `PathFilter` — an object that can be used to filter paths based on the specified date range, ensuring that only paths with dates falling within the range are accepted.

### Valid Call Patterns
```scala
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
```

### LLM Instruction Prompt
- When calling `createDateFilter`, ensure that both `dateStart` and `dateEnd` are valid date strings in the "yyyy.mm.dd" format. The function should be used to create a filter for paths that fall within the specified date range.

### Prompt Snippet
```text
Create a date filter for paths between "2001.02.15" and "2005.02.11" using createDateFilter.
```

### Common Failure Modes
- Providing dates that are not in the "yyyy.mm.dd" format will result in incorrect behavior or runtime errors.
- If `dateStart` is after `dateEnd`, the filter may not function as intended, potentially leading to no paths being accepted.

### Fix Code Hint
```scala
// Ensure that the date strings are in the correct format and that dateStart is before or equal to dateEnd.
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
```

## API Test: `createPartitioner`

### Signature
```scala
def createPartitioner(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: NumPartitions, sizeFunction: IFeature=>Int, opts: BeastOptions ): SpatialPartitioner
def createPartitioner(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], pcriterion: String, pvalue: Long, sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int] = {_.getStorageSize}, opts: BeastOptions ): SpatialPartitioner
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:136  (+1 more definition site/overload)_

_Source doc:_ Constructs a spatial partitioner for the given features. Returns an instance of the spatial partitioner class that is given which is initialized based on the given features. @param features the features to create the partitioner on @param partitionerClass the class of the partitioner to construct @param numPartitions the desired number of partitions (this is just a loose hint not a strict number) @param sizeFunction a function that calculates the size of each feature for load balancing. Only needed if the partition criterion is specified through partition size [[Size]] @return a constructed spatial partitioner

### Goal
Constructs a spatial partitioner for a given set of features to optimize the distribution of spatial data across partitions in a Spark job.

### Parameters
- `features` (`SpatialRDD`): The spatial features on which the partitioner will be constructed. This should be a distributed dataset containing spatial data points or geometries.
- `partitionerClass` (`Class[_ <: SpatialPartitioner], numPartitions: NumPartitions, sizeFunction: IFeature=>Int`): The class of the spatial partitioner to be constructed, along with the desired number of partitions and a function that calculates the size of each feature for load balancing.
- `opts` (`BeastOptions`): Options for configuring the behavior of the partitioner, such as spatial partitioning criteria.

### Input
The caller must provide a `SpatialRDD` containing spatial features, a valid partitioner class, a `NumPartitions` object indicating the desired number of partitions, a size function for load balancing, and `BeastOptions` for additional configuration.

### Output
Returns `SpatialPartitioner` — an instance of the specified spatial partitioner class, initialized based on the provided features, which will be used to manage the distribution of spatial data across partitions.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.{Fixed, NumPartitions}
import edu.ucr.cs.bdlab.beast.indexing.{IndexHelper, RSGrovePartitioner}

val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, new BeastOptions())
```

### LLM Instruction Prompt
When calling `createPartitioner`, ensure that the `features` parameter is a valid `SpatialRDD`, the `partitionerClass` is a class extending `SpatialPartitioner`, and the `numPartitions` is specified correctly. The `sizeFunction` should be a function that returns an integer size for each feature.

### Prompt Snippet
```text
Create a spatial partitioner using the `createPartitioner` method with the appropriate parameters.
```

### Common Failure Modes
- Providing a `features` parameter that is not a valid `SpatialRDD`.
- Specifying an invalid or non-existent `partitionerClass`.
- Incorrectly defining the `numPartitions` which may lead to inefficient partitioning.
- Failing to provide a valid `sizeFunction` when required.

### Fix Code Hint
```scala
// Ensure that the features are a valid SpatialRDD and the partitionerClass is correct.
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, new BeastOptions())
```

## API Test: `createPartitions`

### Signature
```scala
def createPartitions(path: String, opts: BeastOptions, conf: Configuration): Array[FilePartition]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:318_

_Source doc:_ Create all partitions in this RDD for the given input file @return

### Goal
The `createPartitions` function creates partitions for a given input file, enabling distributed processing of geospatial data in a Spark environment.

### Parameters
- `path` (`String`): The file path to the input data, which can be a single file or a comma-separated list of files.
- `opts` (`BeastOptions`): Options that specify the input format and other parameters for reading the data, such as `"iformat" -> "shapefile"` or `"iformat" -> "geojson"`.
- `conf` (`Configuration`): The Hadoop configuration object that provides the necessary settings for reading the input files.

### Input
The caller must provide a valid file path to a supported geospatial data format (e.g., shapefile, geojson) and ensure that the `opts` parameter correctly specifies the input format. The Spark environment must be properly configured to handle the data size and type.

### Output
Returns `Array[FilePartition]` — an array of `FilePartition` objects representing the partitions created for the input data, which can be processed in parallel by Spark.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
- Ensure that the `path` parameter is a valid file path and that the `opts` parameter specifies the correct input format. The `conf` parameter must be the Hadoop configuration for the Spark context.

### Prompt Snippet
```text
Create partitions for the input file using the specified options and configuration.
```

### Common Failure Modes
- Providing an invalid file path that does not exist or is not accessible.
- Specifying an unsupported input format in the `opts` parameter.
- Failing to configure the Spark environment properly, leading to runtime errors during partition creation.

### Fix Code Hint
```scala
// Ensure the file path is correct and the input format is supported
val partitions = SpatialFileRDD.createPartitions("valid_file_path", BeastOptions("iformat" -> "geojson"), sparkContext.hadoopConfiguration)
```

## API Test: `createRingsForOccupiedPixels`

### Signature
```scala
private[davinci] def createRingsForOccupiedPixels: Array[LinearRing]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:671_

_Source doc:_ Creates one linear ring for each contiguous part of occupied pixels. A pixel is connected to the four pixels to its west, east, north, and south. The linear ring is returned in image space based on the pixel location. Think of the corners of pixels as points in space that are connected with orthogonal lines to form the linear rings. @return

### Goal
The `createRingsForOccupiedPixels` function generates linear rings that outline contiguous areas of occupied pixels in a raster dataset, facilitating the analysis of spatial patterns in geospatial raster analytics.

### Parameters
_None._

### Input
The function operates on a raster dataset that has been previously defined and contains occupied pixels. The dataset must be structured such that pixels are connected in a grid format, allowing for identification of contiguous occupied areas.

### Output
Returns `Array[LinearRing]` — an array of linear rings, where each ring represents the boundary of a contiguous area of occupied pixels in image space.

### Valid Call Patterns
```scala
val rings = canvas.createRingsForOccupiedPixels
```

### LLM Instruction Prompt
- When calling `createRingsForOccupiedPixels`, ensure that the raster dataset has been properly initialized and contains occupied pixels. The function does not take any parameters and should be called on an instance of `VectorCanvas`.

### Prompt Snippet
```text
To create linear rings for occupied pixels, call the method `createRingsForOccupiedPixels` on an instance of `VectorCanvas` after ensuring the raster data is set up correctly.
```

### Common Failure Modes
- The function may return an empty array if there are no occupied pixels in the raster dataset.
- If the raster dataset is not properly initialized or does not contain any contiguous occupied areas, the output may not represent valid spatial data.

### Fix Code Hint
```scala
// Ensure the raster data is correctly populated with occupied pixels before calling the function.
val canvas = new VectorCanvas(new Envelope(0, 3, 0, 3), 3, 3, 0, 5)
// Add geometries to the canvas as needed
val rings = canvas.createRingsForOccupiedPixels
```

## API Test: `createSummaryAccumulator`

### Signature
```scala
def createSummaryAccumulator(sc: SparkContext) : SummaryAccumulator
def createSummaryAccumulator(sc: SparkContext, sizeFunction: IFeature => Int) : SummaryAccumulator
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Summary.scala:422  (+1 more definition site/overload)_

_Source doc:_ Create a summary accumulator that uses the method [[IFeature#getStorageSize]] to accumulate the sizes of the features. @param sc the spark context to register the accumulator to @return the initialized and registered accumulator

### Goal
`createSummaryAccumulator` initializes and registers a summary accumulator to collect the sizes of geospatial features during processing.

### Parameters
- `sc` (`SparkContext`): The Spark context used to register the accumulator. It is expected to be an active SparkContext instance that manages the Spark application.
- `sizeFunction` (`IFeature => Int`): A function that takes an `IFeature` and returns its size as an integer. This function is used to determine how to accumulate the sizes of the features.

### Input
The caller must provide an active `SparkContext` and an optional size function that defines how to compute the size of each feature. The input features should be instances of `IFeature`.

### Output
Returns `SummaryAccumulator` — an accumulator that holds the accumulated sizes of the features processed. This accumulator can be queried to retrieve the total size of the features after processing.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = features.map(f => {accumulator.add(f); f})
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- Ensure that the `SparkContext` is active and properly configured before calling `createSummaryAccumulator`. The `sizeFunction` should be defined if custom size accumulation logic is required.

### Prompt Snippet
```text
Create a summary accumulator using the active SparkContext and an optional size function to accumulate feature sizes.
```

### Common Failure Modes
- Attempting to call `createSummaryAccumulator` with an inactive or null `SparkContext` will result in an error.
- If the `sizeFunction` is not provided, the default behavior will use the `getStorageSize` method of `IFeature`, which may not be suitable for all feature types.

### Fix Code Hint
```scala
Ensure that the SparkContext is initialized and active before calling createSummaryAccumulator. If using a custom size function, verify that it correctly handles the input `IFeature` instances.
```

## API Test: `createTileIDFilter`

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
The `createTileIDFilter` function generates a filter that selects raster tiles based on their identifiers, ensuring that only tiles intersecting a specified rectangular area in Sinusoidal space are processed.

### Parameters
- `rect` (`Rectangle2D`): A rectangle defining the extents of the area in Sinusoidal space for which the tile filter is created. The rectangle should be specified in the coordinate system used by the tiles.

### Input
The caller must provide a `Rectangle2D` object that accurately represents the area of interest in Sinusoidal space. This rectangle is essential for determining which tiles to include based on their identifiers.

### Output
Returns `PathFilter` — a filter that matches tile paths based on their identifiers, specifically the `hxxvyy` part of the tile name, allowing for efficient selection of relevant tiles during processing.

### Valid Call Patterns
```scala
val tileIDFilter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale, Math.toRadians(29.0) * HDF4Reader.Scale, Math.toRadians(49.0) * HDF4Reader.Scale))
```

### LLM Instruction Prompt
- When calling `createTileIDFilter`, ensure that the `rect` parameter is a valid `Rectangle2D` object representing the desired area in Sinusoidal space.

### Prompt Snippet
```text
Create a tile ID filter for the specified rectangular area in Sinusoidal space using `createTileIDFilter`.
```

### Common Failure Modes
- Providing a `Rectangle2D` that does not correspond to valid tile identifiers may result in a filter that matches no tiles.
- Failing to account for the coordinate system of the tiles when defining the rectangle can lead to incorrect filtering results.

### Fix Code Hint
```scala
// Ensure the Rectangle2D is defined correctly in Sinusoidal space
val rect = new Rectangle2D.Double(xMin, yMin, width, height) // Replace with actual values
val tileIDFilter = HDF4Reader.createTileIDFilter(rect)
```

## API Test: `crsToSRID`

### Signature
```scala
def crsToSRID(crs: CoordinateReferenceSystem) : Int
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:270_

_Source doc:_ Get an integer SRID that corresponds to the given CRS according to the following logic. 1. If crs is null, return 0 2. Search the local cache as the fastest method of known CRS. 3. If not found in cache, look up the EPSG database to find an SRID, cache, and return it. 4a. If the server is running, contact the server to get the SRID 4b. If the server is not running, assign a custom negative SRID and cache it @param crs the CRS to find an SRID for @return a unique SRID that identifies the given CRS

### Goal
The `crsToSRID` function retrieves a unique integer SRID (Spatial Reference Identifier) corresponding to a given Coordinate Reference System (CRS), facilitating geospatial operations in RDPro.

### Parameters
- `crs` (`CoordinateReferenceSystem`): The CRS for which the SRID is to be determined. This can be a standard CRS (like EPSG:4326 for WGS 84) or a custom CRS.

### Input
The caller must provide a valid `CoordinateReferenceSystem` object. If the `crs` is null, the function will return 0. The function may also require access to a running server to retrieve SRIDs for non-standard CRSs.

### Output
Returns `Int` — an integer representing the unique SRID that identifies the given CRS. This value can be a standard EPSG code or a custom negative SRID for non-standard CRSs.

### Valid Call Patterns
```scala
CRSServer.startServer(sparkContext)
val mercator = CRS.decode("EPSG:3857")
val sridMercator = CRSServer.crsToSRID(mercator)
```

### LLM Instruction Prompt
- When calling `crsToSRID`, ensure that the `crs` parameter is a valid `CoordinateReferenceSystem` object and handle the case where it may be null.

### Prompt Snippet
```text
To retrieve the SRID for a given CRS, use the `crsToSRID` function with a valid `CoordinateReferenceSystem` object.
```

### Common Failure Modes
- Passing a null `CoordinateReferenceSystem` will result in a return value of 0.
- If the CRS is non-standard and the server is not running, a custom negative SRID will be assigned, which may not be suitable for all applications.

### Fix Code Hint
```scala
// Ensure the CRS is not null and the server is running if using non-standard CRS
if (crs != null) {
  val srid = CRSServer.crsToSRID(crs)
} else {
  println("CRS cannot be null.")
}
```

## API Test: `decodeSpatialParquet`

### Signature
```scala
def decodeSpatialParquet(dataframe: DataFrame, geomColumnName: String): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:69_

_Source doc:_ Decodes a [[DataFrame]] that was encoded using the SpatialParquet format @param dataframe @param geomColumnName @return

### Goal
The `decodeSpatialParquet` function decodes a DataFrame that has been encoded in the SpatialParquet format, allowing for the retrieval of spatial data for further processing in geospatial analyses.

### Parameters
- `dataframe` (`DataFrame`): A Spark DataFrame that contains spatial data encoded in the SpatialParquet format. This DataFrame should have been previously encoded using the `encodeSpatialParquet` method.
- `geomColumnName` (`String`): The name of the column in the DataFrame that contains the geometry information. This column is essential for reconstructing the spatial features from the encoded data.

### Input
The input must be a DataFrame that has been encoded in the SpatialParquet format, which typically includes spatial data and a specified geometry column. The DataFrame should be created using a compatible format, such as GeoJSON, and must have been processed through the encoding function prior to decoding.

### Output
Returns `DataFrame` — A Spark DataFrame that contains the decoded spatial data, including the geometry specified by `geomColumnName`. The output DataFrame will be in a format suitable for further geospatial operations within the RDPro library.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
```

### LLM Instruction Prompt
- When calling `decodeSpatialParquet`, ensure that the input DataFrame has been encoded using the SpatialParquet format and that the specified geometry column exists within the DataFrame.

### Prompt Snippet
```text
To decode a DataFrame encoded in SpatialParquet format, use the `decodeSpatialParquet` function, providing the encoded DataFrame and the name of the geometry column.
```

### Common Failure Modes
- The specified `geomColumnName` does not exist in the input DataFrame, leading to a runtime error.
- The input DataFrame was not encoded using the SpatialParquet format, resulting in incorrect or unexpected output.

### Fix Code Hint
```scala
Ensure that the DataFrame passed to `decodeSpatialParquet` was previously encoded using `encodeSpatialParquet` and that the geometry column name is correctly specified.
```

## API Test: `decompress`

### Signature
```scala
protected def decompress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:231_

### Goal
The `decompress` function is used to restore a compressed raster tile to its original uncompressed state, facilitating further processing or analysis.

### Parameters
_None._

### Input
The function operates on an instance of a raster tile that has been previously compressed. There are no additional input parameters required.

### Output
Returns `Unit` — this indicates that the operation is performed in-place on the raster tile and does not produce a new value or output format.

### Valid Call Patterns
```scala
tile.decompress
```

### LLM Instruction Prompt
- Ensure that the `decompress` method is called on a raster tile instance that has been compressed prior to invoking this method.

### Prompt Snippet
```text
Call the `decompress` method on a raster tile instance to restore it to its original uncompressed state.
```

### Common Failure Modes
- Attempting to call `decompress` on a raster tile that is already uncompressed may lead to unexpected behavior or no effect.
- Ensure that the raster tile instance is properly initialized and in a valid state before calling `decompress`.

### Fix Code Hint
```scala
// Ensure the tile is compressed before calling decompress
if (tile.isCompressed) {
    tile.decompress
} else {
    println("Tile is already uncompressed.")
}
```

## API Test: `decompressDatasetFiles`

### Signature
```scala
private[dataExplorer] def decompressDatasetFiles(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:195_

_Source doc:_ Decompresses dataset files that are stored locally. Specifically, it decompress any ZIP files found in the dataset's path. It deletes those ZIP files and finally updates the dataset's status in the database after decompression.

### Goal
The `decompressDatasetFiles` function decompresses any ZIP files located in the dataset's path, cleans up the ZIP files, and updates the dataset's status in the database.

### Parameters
_None._

### Input
The function operates on dataset files that must be stored locally in a specified dataset path. The precondition is that ZIP files must exist in this path for the function to perform decompression.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs actions such as file decompression and database updates.

### Valid Call Patterns
```scala
datasetProcessor.decompressDatasetFiles()
```

### LLM Instruction Prompt
- Ensure that the dataset files are present in the specified local path and contain ZIP files before calling `decompressDatasetFiles`.

### Prompt Snippet
```text
Call `decompressDatasetFiles` on an instance of `DatasetProcessor` to decompress ZIP files in the dataset's path and update the database status.
```

### Common Failure Modes
- The function may fail if there are no ZIP files present in the dataset's path, resulting in no action taken.
- If the database connection is not properly established, the status update may fail.

### Fix Code Hint
```scala
// Ensure that the dataset path contains ZIP files and that the database connection is valid before calling the function.
```

## API Test: `diagonal`

### Signature
```scala
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): JavaSpatialRDD
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:106  (+1 more definition site/overload)_

_Source doc:_ Generate diagonally distributed data @param cardinality the number of records to generate @param percentage the percentage of records exactly on the diagonal line @param buffer the buffer around the diagonal line in which records can be generated @return the RDD that contains the generated data

### Goal
The `diagonal` function generates a spatial dataset with points distributed along a diagonal line, allowing for a specified percentage of points to be exactly on the line and a buffer area around it.

### Parameters
- `cardinality` (`Long`): The total number of records (points) to generate. This value should be a positive integer representing how many points you want in the output dataset.
- `percentage` (`Double`), default `0.5`: The fraction of the total records that should lie exactly on the diagonal line. This value should be between `0.0` and `1.0`, where `0.0` means no points on the diagonal and `1.0` means all points on the diagonal.
- `buffer` (`Double`), default `0.2`: The width of the buffer around the diagonal line within which additional points can be generated. This value should be a non-negative number.

### Input
The caller must provide a valid Spark context to execute the function. There are no specific file formats required as input since this function generates data programmatically.

### Output
Returns `JavaSpatialRDD` — a distributed dataset containing the generated spatial points, which can be used for further spatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .diagonal(1000, percentage = 0.3, buffer = 0.2)
```

### LLM Instruction Prompt
- When calling `diagonal`, ensure that the `cardinality` is a positive integer, `percentage` is between `0.0` and `1.0`, and `buffer` is a non-negative number.

### Prompt Snippet
```text
Generate a spatial dataset with 1000 points, where 30% of the points are exactly on the diagonal line and a buffer of 0.2 is allowed around the diagonal.
```

### Common Failure Modes
- Providing a negative value for `cardinality` will result in an error since it must be a positive integer.
- Setting `percentage` outside the range of `0.0` to `1.0` will lead to an invalid configuration error.
- Using a negative value for `buffer` will also cause an error, as it must be non-negative.

### Fix Code Hint
```scala
// Ensure cardinality is positive, percentage is between 0.0 and 1.0, and buffer is non-negative
val points: SpatialRDD = sc.generateSpatialData.diagonal(1000, percentage = 0.3, buffer = 0.2)
```

## API Test: `distribution`

### Signature
```scala
def distribution(distribution: DistributionType): JavaSpatialGeneratorBuilder
def distribution(distribution: DistributionType): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:55  (+1 more definition site/overload)_

_Source doc:_ Set the distribution of the generated data @param distribution the distributed of the generated data as one of {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[BitDistribution]], [[SierpinskiDistribution]], [[ParcelDistribution]]} @return

### Goal
The `distribution` function sets the statistical distribution type for generating spatial data in a raster processing context.

### Parameters
- `distribution` (`DistributionType`): Specifies the type of distribution to be used for generating spatial data. Expected values include `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `BitDistribution`, `SierpinskiDistribution`, and `ParcelDistribution`.

### Input
The caller must provide a valid `DistributionType` as an argument. There are no specific file formats required for this function, as it is part of the configuration for generating spatial data.

### Output
Returns `JavaSpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data based on the specified distribution type.

### Valid Call Patterns
```scala
val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)

val randomPolygons: RDD[IFeature] = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000)
```

### LLM Instruction Prompt
- When calling `distribution`, ensure that the provided `distribution` parameter is one of the valid `DistributionType` values listed in the documentation.

### Prompt Snippet
```text
Set the distribution for generating spatial data using one of the following types: UniformDistribution, DiagonalDistribution, GaussianDistribution, BitDistribution, SierpinskiDistribution, or ParcelDistribution.
```

### Common Failure Modes
- Providing an invalid `DistributionType` that is not one of the specified options will result in a runtime error.
- Failing to configure the `JavaSpatialGeneratorBuilder` after calling `distribution` may lead to incomplete or incorrect spatial data generation.

### Fix Code Hint
```scala
// Ensure you are using a valid DistributionType
val randomPoints: RDD[IFeature] = sc.generateSpatialData
  .distribution(UniformDistribution) // Correct usage
  .config(UniformDistribution.GeometryType, "box")
  .generate(cardinality=10000000)
```

## API Test: `divideScene`

### Signature
```scala
def divideScene[T: ClassTag](raster: RasterRDD[T], targetMetadata: RasterMetadata, numTilesX: Int, numTilesY: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625_

_Source doc:_ Divides an existing RDD into a new RDD such that every group of tiles is brought together into one Metadata. This is helpful when writing the resulting RDD to files because each group of tiles will be written to a separate file. @param raster the input raster to repartition @param targetMetadata the metadata of the target (output) raster @param numTilesX number of tiles to combine together into one metadata @param numTilesY number of tiles to combine together into one metadata @tparam T @return

### Goal
`divideScene` partitions an existing raster RDD into smaller groups of tiles, each associated with a single metadata object, facilitating efficient writing of the resulting tiles to separate files.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster RDD that contains the pixel data to be repartitioned. It must be a valid `RasterRDD` containing pixel values of type `T`.
- `targetMetadata` (`RasterMetadata`): The metadata for the output raster, which defines the spatial characteristics (such as dimensions and coordinate reference system) of the resulting tiles.
- `numTilesX` (`Int`): The number of tiles to combine horizontally into one metadata object. This determines how the raster is divided along the x-axis.
- `numTilesY` (`Int`): The number of tiles to combine vertically into one metadata object. This determines how the raster is divided along the y-axis.

### Input
The caller must provide a valid `RasterRDD` containing pixel data, a `RasterMetadata` object that describes the desired output raster's characteristics, and two integers specifying how many tiles to combine in each dimension. The input raster must be compatible with the specified metadata.

### Output
Returns `RasterRDD[T]` — a new raster RDD where each group of tiles is associated with a single metadata object, suitable for writing to separate files.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD` and that the `targetMetadata` is correctly defined to match the desired output characteristics. The number of tiles specified must be appropriate for the dimensions of the input raster.

### Prompt Snippet
```text
Divide the raster into smaller tiles using the divideScene function, ensuring the target metadata is correctly set for the output.
```

### Common Failure Modes
- Providing a `RasterRDD` that does not match the expected pixel type `T` for the output.
- Specifying `numTilesX` or `numTilesY` values that do not align with the dimensions of the input raster, leading to unexpected results or errors.
- Using incompatible `RasterMetadata` that does not correspond to the input raster's characteristics.

### Fix Code Hint
```scala
// Ensure the input raster and target metadata are compatible
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, numTilesX, numTilesY)
```

## API Test: `encodeGeoParquet`

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
The input must be a Spark DataFrame loaded from a geospatial data source, such as GeoJSON. The DataFrame should contain a geometry column that can be processed. Ensure that the DataFrame is properly formatted and contains valid geometries.

### Output
Returns `DataFrame` — a new DataFrame in GeoParquet format, which includes the original data with the geometry column replaced by two new columns: one for the Minimum Bounding Rectangle (MBR) and another for the Well-Known Binary (WKB) representation of the geometry.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
```

### LLM Instruction Prompt
- When calling `encodeGeoParquet`, ensure that the input DataFrame contains a valid geometry column and is formatted correctly as a Spark DataFrame.

### Prompt Snippet
```text
To encode a DataFrame into GeoParquet format, use the `encodeGeoParquet` function, ensuring the DataFrame has a geometry column.
```

### Common Failure Modes
- The input DataFrame does not contain a geometry column, leading to an error during encoding.
- The DataFrame is not properly formatted or contains invalid geometries, which may cause the function to fail.

### Fix Code Hint
```scala
// Ensure the DataFrame has a valid geometry column before calling encodeGeoParquet
if (dataframe.columns.contains("geometry")) {
  val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
} else {
  throw new IllegalArgumentException("DataFrame must contain a 'geometry' column.")
}
```

## API Test: `encodeGeometry`

### Signature
```scala
private def encodeGeometry(geometry: Geometry, featureBuilder: Feature.Builder): Unit
private def encodeGeometry(geometry: LiteGeometry, featureBuilder: Feature.Builder): Unit
def encodeGeometry(geometry: Geometry): Seq[InternalRow]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:194  (+2 more definition site/overload)_

_Source doc:_ Encodes a geometry into the given feature @param geometry the geometry to encode @param featureBuilder the feature builder to encode to

### Goal
Encodes a geometric shape into a specified feature builder for further processing or storage in a geospatial context.

### Parameters
- `geometry` (`Geometry`): The geometric shape to be encoded, which can include points, lines, or polygons.
- `featureBuilder` (`Feature.Builder`): A builder object used to construct a feature representation of the geometry.

### Input
The caller must provide a valid `Geometry` object representing the shape to be encoded and a `Feature.Builder` instance to which the encoded geometry will be added.

### Output
Returns `Unit` — this indicates that the encoding process has been completed successfully without returning any value.

### Valid Call Patterns
```scala
val point = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val featureBuilder = new Feature.Builder()
SpatialParquetHelper.encodeGeometry(point, featureBuilder)
```

### LLM Instruction Prompt
- Ensure that the `geometry` parameter is a valid instance of `Geometry` or `LiteGeometry`.
- Provide a properly initialized `Feature.Builder` instance to avoid null reference errors.

### Prompt Snippet
```text
To encode a geometry, create a valid Geometry object and a Feature.Builder instance, then call encodeGeometry with both as arguments.
```

### Common Failure Modes
- Providing a null or uninitialized `geometry` or `featureBuilder` will result in a `NullPointerException`.
- Attempting to encode unsupported geometry types may lead to runtime errors.

### Fix Code Hint
```scala
// Ensure that both geometry and featureBuilder are properly initialized before calling encodeGeometry
val point = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val featureBuilder = new Feature.Builder()
SpatialParquetHelper.encodeGeometry(point, featureBuilder)
```

## API Test: `encodeSpatialParquet`

### Signature
```scala
def encodeSpatialParquet(dataframe: DataFrame): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:81_

_Source doc:_ Parses an existing DataFrame according to the given options that determine the format of the spatial attributes. @param dataframe an existing dataframe @return a dataframe that parses and replaces the spatial attributes with a geometry column

### Goal
`encodeSpatialParquet` transforms an existing DataFrame by parsing its spatial attributes and replacing them with a geometry column, facilitating the storage of spatial data in a Parquet format.

### Parameters
- `dataframe` (`DataFrame`): An existing DataFrame containing spatial attributes that need to be encoded into a geometry column.

### Input
The input must be a valid DataFrame that contains spatial attributes, typically loaded from formats such as GeoJSON. The DataFrame should be structured correctly to ensure that spatial attributes can be parsed and transformed.

### Output
Returns `DataFrame` — a new DataFrame that has parsed the spatial attributes and replaced them with a geometry column, suitable for further spatial analysis or storage in Parquet format.

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
```

### LLM Instruction Prompt
- When calling `encodeSpatialParquet`, ensure that the input DataFrame contains valid spatial attributes and is properly formatted to avoid parsing errors.

### Prompt Snippet
```text
To encode spatial attributes in a DataFrame, use the `encodeSpatialParquet` function from the `SpatialParquetSource` object, ensuring the DataFrame is correctly structured.
```

### Common Failure Modes
- The input DataFrame does not contain any spatial attributes, leading to parsing errors.
- The DataFrame is not properly formatted (e.g., missing required columns), which may result in an exception during the encoding process.

### Fix Code Hint
```scala
Ensure that the DataFrame being passed to `encodeSpatialParquet` contains valid spatial attributes and is loaded from a supported format like GeoJSON.
```

## API Test: `end`

### Signature
```scala
def end: Long
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26_

### Goal
The `end` function retrieves the end value of a spatial partition, which is useful for understanding the extent of the data being processed in a distributed raster analysis context.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Long` — the end value of the spatial partition, which represents the maximum index or boundary of the data being processed.

### Valid Call Patterns
```scala
value.end
```

### LLM Instruction Prompt
- When calling `end`, ensure that it is invoked on a valid instance of the class that contains this method.

### Prompt Snippet
```text
To retrieve the end value of the spatial partition, use the method `value.end`.
```

### Common Failure Modes
- Calling `end` on an uninitialized or null instance may result in a `NullPointerException`.
- Attempting to call `end` on an instance that does not support this method will lead to a compilation error.

### Fix Code Hint
```scala
Ensure that the instance on which `end` is called is properly initialized and of the correct type that includes this method.
```

## API Test: `envelope`

### Signature
```scala
def envelope: java.awt.Rectangle
override def envelope: java.awt.Rectangle
def envelope: Envelope
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:24  (+4 more definition site/overload)_

### Goal
Retrieve the boundaries of the raster data in the model space as an envelope.

### Parameters
_None._

### Input
The function does not require any input parameters. It operates on the raster data that has already been loaded into the context.

### Output
Returns `java.awt.Rectangle` — an object representing the rectangular boundaries of the raster data in model space, defined by its coordinates.

### Valid Call Patterns
```scala
val rasterEnvelope: java.awt.Rectangle = raster.envelope
```

### LLM Instruction Prompt
- Ensure that the raster data has been loaded and is available in the context before calling `envelope`.

### Prompt Snippet
```text
Retrieve the envelope of the loaded raster data using the envelope method.
```

### Common Failure Modes
- Calling `envelope` without having a raster dataset loaded in the context may lead to a runtime error.
- If the raster data is empty or not properly initialized, the returned envelope may not represent valid boundaries.

### Fix Code Hint
```scala
// Ensure the raster is loaded before calling envelope
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_geotiff.tif")
val rasterEnvelope: java.awt.Rectangle = raster.envelope
```

## API Test: `eulerHistogramCount`

### Signature
```scala
def eulerHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the number of records in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `eulerHistogramCount` function computes an Euler histogram that efficiently counts the number of records in each cell for geometries with extents, facilitating spatial analysis in geospatial raster processing.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the size of the histogram, representing the number of partitions along each dimension. For example, `Array(100, 100)` would create a histogram with 100 partitions in both the x and y dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the result. Setting this to `true` can speed up range tests on the histogram.

### Input
The caller must provide a valid geometry dataset that supports the computation of an Euler histogram. The `histogramSize` must be a non-empty array of integers, and the data must be in a format compatible with the operations of the RDPro library.

### Output
Returns `AbstractHistogram` — an object representing the computed Euler histogram, which contains the counts of records in each cell based on the specified histogram size.

### Valid Call Patterns
```scala
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))
```

### LLM Instruction Prompt
- When calling `eulerHistogramCount`, ensure that the `histogramSize` is a valid non-empty array of integers and that the `prefixSum` parameter is set according to the needs of the analysis.

### Prompt Snippet
```text
Compute the Euler histogram for the given geometries with specified histogram size.
```

### Common Failure Modes
- Providing an empty or null `histogramSize` array will result in an error.
- If the input geometries are not compatible with the histogram computation, the function may throw an exception.

### Fix Code Hint
```scala
// Ensure histogramSize is a valid non-empty array of integers
val validHistogramSize = Array(100, 100)
val eulerCountHistogram = polygons.eulerHistogramCount(validHistogramSize)
```

## API Test: `eulerHistogramSize`

### Signature
```scala
def eulerHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the total size of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `eulerHistogramSize` function computes an Euler histogram that efficiently calculates the total size of geometrical features within specified partitions, making it suitable for handling spatial data with extents.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the number of partitions along each dimension for the histogram. For example, `Array(100, 100)` creates a histogram with 100 partitions in both the x and y dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the resulting histogram. Setting this to `true` can speed up range queries on the histogram.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A function that takes an `IFeature` and returns its size. The default function retrieves the storage size of the feature.

### Input
The caller must provide a valid `Array[Int]` for `histogramSize`, which defines the partitioning of the histogram. The input geometries must be compatible with the histogram computation, typically requiring that they have extents (envelopes).

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which contains the size of features aggregated into the specified partitions.

### Valid Call Patterns
```scala
val eulerSizeHistogram = polygons.eulerHistogramSize(Array(100, 100))
```

### LLM Instruction Prompt
- When calling `eulerHistogramSize`, ensure that the `histogramSize` parameter is a valid array of integers representing the desired partition sizes. The `prefixSum` and `sizeFunction` parameters are optional and can be adjusted based on the specific needs of the analysis.

### Prompt Snippet
```text
To compute an Euler histogram for geometries, use the `eulerHistogramSize` method with appropriate partition sizes, such as `polygons.eulerHistogramSize(Array(100, 100))`.
```

### Common Failure Modes
- Providing an invalid `histogramSize` array (e.g., empty or containing negative values) may result in runtime errors.
- If the geometries do not have extents, the histogram computation may not yield meaningful results.

### Fix Code Hint
```scala
// Ensure that the histogramSize array is properly defined and that the geometries have extents before calling the function.
val validHistogramSize = Array(100, 100)
val eulerSizeHistogram = polygons.eulerHistogramSize(validHistogramSize)
```

## API Test: `explode`

### Signature
```scala
def explode: RasterRDD[T]
def explode[T](inputRaster: RasterRDD[T]): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:76  (+1 more definition site/overload)_

_Source doc:_ Returns a new RasterRDD where each tile is in its own raster. @param inputRaster the raster data to explore @tparam T @return a new raster RDD with the same number of tiles but each tile is in a separate raster

### Goal
The `explode` function separates each tile in a `RasterRDD` into its own individual raster, facilitating operations on each tile independently.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster data containing multiple tiles that will be exploded into separate rasters.

### Input
The caller must provide a `RasterRDD[T]` that contains raster data. The input raster should be properly initialized and can be loaded from formats such as GeoTIFF or HDF. Ensure that the input raster is not empty and contains valid tile data.

### Output
Returns `RasterRDD[T]` — a new raster RDD where each tile from the input raster is represented as a separate raster. The output maintains the same pixel type as the input.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsLocal.explode(raster)
```

### LLM Instruction Prompt
- When calling `explode`, ensure that the input is a valid `RasterRDD[T]` containing raster data with multiple tiles. The output will be a `RasterRDD[T]` where each tile is separated.

### Prompt Snippet
```text
To use the `explode` function, provide a `RasterRDD[T]` as input, and it will return a new `RasterRDD[T]` with each tile in its own raster.
```

### Common Failure Modes
- Attempting to call `explode` on an empty `RasterRDD` will result in an error.
- Providing a non-`RasterRDD` type will lead to a compilation error.
- If the input raster does not contain any tiles, the output will also be empty.

### Fix Code Hint
```scala
Ensure that the input raster is properly initialized and contains valid tile data before calling `explode`. For example:
val raster: RasterRDD[Int] = sc.geoTiff("your_raster_file.tif")
val outputRaster = RasterOperationsLocal.explode(raster)
```

## API Test: `extents`

### Signature
```scala
def extents: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:181  (+1 more definition site/overload)_

_Source doc:_ Returns a polygon that represents the boundaries of this tile in the model space. @return a polygon (rectangle) that represents the boundaries of this tile.

### Goal
The `extents` function retrieves the geometric boundaries of a raster tile in model space, represented as a rectangular polygon.

### Parameters
_None._

### Input
The function does not require any input parameters. It operates on the instance of the class it is called on, which must be a valid raster tile with defined extents.

### Output
Returns `Geometry` — a polygon that represents the boundaries of the raster tile in model space.

### Valid Call Patterns
```scala
val geometry: Geometry = rasterMetadata.extents
```

### LLM Instruction Prompt
- When calling `extents`, ensure that it is invoked on a valid instance of a raster tile that has defined extents.

### Prompt Snippet
```text
Call the `extents` method on a valid raster tile instance to obtain its geometric boundaries.
```

### Common Failure Modes
- Calling `extents` on an uninitialized or invalid raster tile instance may result in a runtime error.
- If the raster tile does not have defined extents, the output may not represent a valid polygon.

### Fix Code Hint
```scala
// Ensure the raster tile is properly initialized before calling extents
val rasterMetadata = new RasterMetadata(...) // Initialize with valid parameters
val geometry: Geometry = rasterMetadata.extents
```

## API Test: `extractTables`

### Signature
```scala
def extractTables(sql: String): Set[String]
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/SQLQueryHelper.scala:22_

_Source doc:_ Checks if an SQL query is syntactically correct and extracts table names from it. @param sql The SQL query string to be analyzed. @return Either an error message as a string if the query is incorrect, or a set of table names if the query is correct.

### Goal
`extractTables` analyzes an SQL query to determine its syntactical correctness and retrieves the names of the tables referenced in the query.

### Parameters
- `sql` (`String`): The SQL query string to be analyzed, which should follow standard SQL syntax.

### Input
The input must be a valid SQL query string. The query should be syntactically correct to successfully extract table names. Invalid SQL syntax will result in an error.

### Output
Returns `Set[String]` — a set of table names extracted from the SQL query if the query is correct. If the query is incorrect, an error message will be returned instead.

### Valid Call Patterns
```scala
val validSQL = "SELECT * FROM users"
val tables: Set[String] = SQLQueryHelper.extractTables(validSQL)
```

### LLM Instruction Prompt
- Ensure that the SQL query provided is syntactically correct before calling `extractTables`. Handle any potential exceptions that may arise from invalid SQL syntax.

### Prompt Snippet
```text
Extract table names from the SQL query using `extractTables`. Ensure the query is valid to avoid errors.
```

### Common Failure Modes
- Providing an invalid SQL query (e.g., "SELEC * FROM users") will result in a `SqlParseException`.
- Not handling exceptions when calling `extractTables` may lead to unhandled errors in the application.

### Fix Code Hint
```scala
try {
  val tables: Set[String] = SQLQueryHelper.extractTables(invalidSQL)
} catch {
  case e: SqlParseException => println("Invalid SQL query: " + e.getMessage)
}
```

## API Test: `filterPixels`

### Signature
```scala
def filterPixels(f: T => Boolean)
def filterPixels[T: ClassTag](inputRaster: RasterRDD[T], filter: T => Boolean): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:48  (+1 more definition site/overload)_

_Source doc:_ Retains only the pixels that pass the user-defined filter and clears all other pixels (set to empty) @param inputRaster the input raster @param filter the filter function that tells which pixel values to keep in the output @tparam T the type of the pixels in the input @return a new raster where only pixels that pass the test are retained

### Goal
`filterPixels` retains only the pixels in a raster that meet a specified condition, effectively filtering out unwanted pixel values.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster dataset containing pixel values of type `T`. This raster is expected to be a distributed collection of raster tiles.
- `filter` (`T => Boolean`): A user-defined function that takes a pixel value of type `T` and returns a Boolean indicating whether the pixel should be retained (`true`) or cleared (`false`).

### Input
The caller must provide a `RasterRDD[T]` containing pixel data, which can be loaded from formats such as GeoTIFF or HDF. The filter function must be compatible with the pixel type `T` of the input raster.

### Output
Returns `RasterRDD[T]` — a new raster dataset where only the pixels that pass the filter condition are retained, while all other pixels are set to empty.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperatureK.filterPixels(_ > 300).saveAsGeoTiff("temperature_high")

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val trees = raster.filterPixels(lc => lc >= 1 && lc <= 10)
```

### LLM Instruction Prompt
- When calling `filterPixels`, ensure that the input raster is a valid `RasterRDD` and that the filter function is appropriate for the pixel type of the raster.

### Prompt Snippet
```text
Use the `filterPixels` function to filter a raster dataset based on a user-defined condition, ensuring the input raster is of the correct type and the filter function is compatible with the pixel values.
```

### Common Failure Modes
- The filter function may not be compatible with the pixel type `T`, leading to type mismatch errors.
- The input raster may be empty or improperly loaded, resulting in no output or runtime errors.

### Fix Code Hint
```scala
Ensure that the input raster is correctly loaded and that the filter function is defined for the pixel type of the raster. For example, if the raster contains `Float` values, the filter function should accept a `Float` parameter.
```

## API Test: `findIntersections`

### Signature
```scala
private[davinci] def findIntersections(_x1: Double, _y1: Double, _x2: Double, _y2: Double, intersections: mutable.ArrayBuffer[(Int, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:313_

_Source doc:_ Find all intersections between the given line segment and the horizontal scan line centers @param x1 @param y1 @param x2 @param y2 @param intersections all computed intersections will be appended to this list

### Goal
`findIntersections` computes the intersection points between a specified line segment and horizontal scan lines, appending the results to a provided list.

### Parameters
- `_x1` (`Double`): The x-coordinate of the starting point of the line segment.
- `_y1` (`Double`): The y-coordinate of the starting point of the line segment.
- `_x2` (`Double`): The x-coordinate of the ending point of the line segment.
- `_y2` (`Double`): The y-coordinate of the ending point of the line segment.
- `intersections` (`mutable.ArrayBuffer[(Int, Int)]`): A mutable array buffer that will store the computed intersection points as tuples of integer coordinates.

### Input
The caller must provide valid double values for the coordinates of the line segment endpoints and an initialized mutable array buffer to store the intersection results.

### Output
Returns `Unit` — this indicates that the function does not return a value but modifies the `intersections` array buffer in place to include the computed intersection points.

### Valid Call Patterns
```scala
val intersections = new mutable.ArrayBuffer[(Int, Int)]()
canvas.findIntersections(0, 0, 3, 4, intersections)
```

### LLM Instruction Prompt
- Ensure that the coordinates provided for the line segment are valid double values and that the `intersections` array buffer is initialized before calling `findIntersections`.

### Prompt Snippet
```text
Call `findIntersections` with the coordinates of the line segment and an initialized mutable array buffer to store intersection points.
```

### Common Failure Modes
- Failing to initialize the `intersections` array buffer before passing it to the function will result in a runtime error.
- Providing invalid coordinate values (e.g., non-numeric types) will lead to compilation errors.

### Fix Code Hint
```scala
val intersections = new mutable.ArrayBuffer[(Int, Int)]() // Ensure this is initialized
canvas.findIntersections(0, 0, 3, 4, intersections) // Call with valid coordinates
```

## API Test: `findTransformationInfo`

### Signature
```scala
def findTransformationInfo(sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetSRID: Int): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetCRS: CoordinateReferenceSystem): TransformationInfo
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:146  (+2 more definition site/overload)_

_Source doc:_ Creates or retrieves a cached math transform to transform between the given two CRS @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return the math transformation that transforms from source to destination

### Goal
The `findTransformationInfo` function retrieves or creates a mathematical transformation to convert coordinates from a source coordinate reference system (CRS) to a target CRS, facilitating accurate geospatial analysis.

### Parameters
- `sourceCRS` (`CoordinateReferenceSystem`): The source coordinate reference system from which the transformation will be applied. This can be any valid CRS object representing the spatial reference of the input data.
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system to which the transformation will be applied. This should also be a valid CRS object representing the desired spatial reference for the output data.

### Input
The caller must provide two valid `CoordinateReferenceSystem` objects representing the source and target CRSs. These CRSs must be compatible for transformation, meaning that a mathematical transformation exists between them.

### Output
Returns `TransformationInfo` — an object that encapsulates the mathematical transformation needed to convert coordinates from the source CRS to the target CRS. This object is used internally for performing the actual coordinate transformations.

### Valid Call Patterns
```scala
val transform: TransformationInfo = Reprojector.findTransformationInfo(sourceCRS, targetCRS)
val transformBySRID: TransformationInfo = Reprojector.findTransformationInfo(4326, targetCRS)
```

### LLM Instruction Prompt
- When calling `findTransformationInfo`, ensure that both `sourceCRS` and `targetCRS` are valid `CoordinateReferenceSystem` instances or SRIDs that can be transformed between each other.

### Prompt Snippet
```text
To transform coordinates from one CRS to another, use the findTransformationInfo function with appropriate source and target CRS parameters.
```

### Common Failure Modes
- Providing incompatible CRSs that do not have a defined transformation will result in an error.
- Passing null or invalid `CoordinateReferenceSystem` objects will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure that both sourceCRS and targetCRS are valid and compatible before calling the function.
val sourceCRS: CoordinateReferenceSystem = ... // Initialize with a valid CRS
val targetCRS: CoordinateReferenceSystem = ... // Initialize with a valid CRS
val transform: TransformationInfo = Reprojector.findTransformationInfo(sourceCRS, targetCRS)
```

## API Test: `flatten`

### Signature
```scala
def flatten[T](raster: RasterRDD[T]): RDD[(Int, Int, RasterMetadata, T)]
def flatten: RDD[(Int, Int, RasterMetadata, T)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69  (+1 more definition site/overload)_

_Source doc:_ Extract all pixel values into an RDD @param raster the raster to extract its pixels @tparam T the type of pixel values @return an RDD that contains all pixel locations and values

### Goal
The `flatten` function extracts all pixel values from a raster dataset into a distributed RDD format, enabling further analysis and processing in a Spark environment.

### Parameters
- `raster` (`RasterRDD[T]`): The raster dataset from which pixel values will be extracted. It is expected to be a distributed collection of raster data, where `T` represents the type of pixel values (e.g., `Int`, `Float`).

### Input
The input must be a valid `RasterRDD[T]` containing raster data. The raster should be properly initialized and populated with pixel values, typically loaded from a GeoTIFF or similar raster format.

### Output
Returns `RDD[(Int, Int, RasterMetadata, T)]` — This output represents a distributed collection of tuples, where each tuple contains the pixel's row index, column index, associated raster metadata, and the pixel value of type `T`. This format allows for efficient processing and analysis of raster data in Spark.

### Valid Call Patterns
```scala
val finalPixels: Map[(Int, Int), Double] = RasterOperationsGlobal.flatten(smoothedRaster)
  .map(x => ((x._1, x._2), x._4))
  .collectAsMap()
  .toMap
```

### LLM Instruction Prompt
- When calling `flatten`, ensure that the input raster is a valid `RasterRDD[T]` and that the pixel type `T` is correctly specified to match the raster data.

### Prompt Snippet
```text
Extract pixel values from the raster dataset using the flatten function.
```

### Common Failure Modes
- Attempting to call `flatten` on a non-initialized or empty `RasterRDD` will result in an error.
- Mismatched pixel types (e.g., using `RasterRDD[Int]` when the data is actually `Float`) can lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the raster is properly initialized and populated before calling flatten
val raster: RasterRDD[Int] = RasterOperationsGlobal.rasterizePixels(pixels, metadata, RasterFeature.create(Array("fileName"),Array("testFile.tif")))
val flattenedRaster = RasterOperationsGlobal.flatten(raster)
```

## API Test: `gaussian`

### Signature
```scala
def gaussian(cardinality: Long): JavaSpatialRDD
def gaussian(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:117  (+1 more definition site/overload)_

_Source doc:_ Generate Gaussian distributed data @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `gaussian` function generates a SpatialRDD containing Gaussian distributed spatial data points, useful for simulations and spatial analysis in geospatial applications.

### Parameters
- `cardinality` (`Long`): The number of records (data points) to generate. This value should be a positive integer representing how many Gaussian distributed points you want in the output.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and that the `cardinality` parameter is a valid positive long integer.

### Output
Returns `JavaSpatialRDD` or `SpatialRDD` — an RDD that contains the generated Gaussian distributed spatial data points, which can be used for further spatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .gaussian(1000)
```

### LLM Instruction Prompt
- When calling `gaussian`, ensure that the `cardinality` parameter is a positive long integer to avoid errors in data generation.

### Prompt Snippet
```text
Generate a SpatialRDD of Gaussian distributed data points with a specified cardinality.
```

### Common Failure Modes
- Providing a negative or zero value for `cardinality` will result in an error, as the function expects a positive integer.
- Failing to initialize the Spark context before calling `gaussian` will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure cardinality is a positive integer
val numPoints: Long = 1000 // Example of a valid cardinality
val gaussianPoints: SpatialRDD = sc.generateSpatialData.gaussian(numPoints)
```

## API Test: `generate`

### Signature
```scala
def generate(cardinality: Long): JavaSpatialRDD
def generate(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:87  (+1 more definition site/overload)_

_Source doc:_ Generate the data as an RDD. @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `generate` function creates a distributed dataset (RDD) of spatial features based on the specified cardinality, which is useful for generating synthetic geospatial data for analysis.

### Parameters
- `cardinality` (`Long`): The number of spatial records to generate. This value should be a positive integer representing the desired size of the output dataset.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and configured to handle the generation of the specified number of records.

### Output
Returns `JavaSpatialRDD` or `SpatialRDD` — an RDD containing the generated spatial features, which can be used for further geospatial analysis or processing within the RDPro framework.

### Valid Call Patterns
```scala
val randomPoints: RDD[IFeature] = sc.generateSpatialData.uniform(1000000000)

val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)

val randomPolygons: RDD[IFeature] = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000)
```

### LLM Instruction Prompt
- When calling `generate`, ensure that the cardinality parameter is a positive long integer representing the number of records to generate. The Spark context must be properly initialized.

### Prompt Snippet
```text
Generate a spatial dataset with a specified number of records using the generate function.
```

### Common Failure Modes
- Providing a negative or zero value for the `cardinality` parameter will result in an error, as the function expects a positive integer.
- Failing to initialize the Spark context before calling `generate` will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure cardinality is a positive long integer
val cardinality: Long = 10000000 // Example of a valid cardinality
val randomData: SpatialRDD = sc.generate(cardinality)
```

## API Test: `generateSpatialData`

### Signature
```scala
def generateSpatialData(distribution: DistributionType, cardinality: Long, numPartitions: Int = 0, opts: BeastOptions = new BeastOptions) : SpatialRDD
def generateSpatialData: SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:139  (+1 more definition site/overload)_

_Source doc:_ Return a [[SpatialRDD]] of randomly generated geometries according to the given options. @param distribution the type of distribution {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[SierpinskiDistribution]], [[BitDistribution]], [[ParcelDistribution]]} @param cardinality the number of geometries to generate @param opts additional options depending on the type of generator @return an RDD with the generated geometries

### Goal
The `generateSpatialData` function generates a `SpatialRDD` containing randomly created geometries based on specified distribution types and parameters, facilitating spatial analysis in geospatial applications.

### Parameters
- `distribution` (`DistributionType`): Specifies the type of distribution for generating geometries. Expected values include `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `SierpinskiDistribution`, `BitDistribution`, and `ParcelDistribution`.
- `cardinality` (`Long`): Indicates the number of geometries to generate. This value determines the size of the resulting `SpatialRDD`.
- `numPartitions` (`Int`), default `0`: Defines the number of partitions for the resulting `SpatialRDD`. If set to `0`, the default partitioning strategy will be used.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional options that can modify the behavior of the geometry generator, such as specific parameters related to the chosen distribution.

### Input
The caller must provide a valid `DistributionType` for the `distribution` parameter and a positive `Long` value for `cardinality`. The `opts` parameter can include various options depending on the distribution type selected. Ensure that the Spark environment is properly configured to handle the data size and type.

### Output
Returns `SpatialRDD` — a distributed collection of geometries generated according to the specified distribution and parameters, suitable for further spatial analysis and processing.

### Valid Call Patterns
```scala
val spatialData: SpatialRDD = sparkContext.generateSpatialData(UniformDistribution, 100, opts = Seq("seed" -> 1, UniformDistribution.MaxSize -> "0.1,0.1", "geometry" -> "box"))
```

### LLM Instruction Prompt
- When calling `generateSpatialData`, ensure that the `distribution` is a valid `DistributionType` and `cardinality` is a positive `Long`. Use appropriate options in `opts` based on the selected distribution.

### Prompt Snippet
```text
Generate a SpatialRDD of geometries using the specified distribution and cardinality.
```

### Common Failure Modes
- Providing an invalid `DistributionType` will result in an error.
- Setting `cardinality` to a non-positive value will lead to an exception.
- Incorrectly formatted options in `opts` may cause runtime errors or unexpected behavior.

### Fix Code Hint
```scala
Ensure that the distribution is one of the valid types and that cardinality is a positive integer. Check the format of options in opts for correctness.
```

## API Test: `geoTiff`

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
Loads a GeoTIFF file and returns its data as a distributed collection of raster tiles for further geospatial analysis.

### Parameters
- `path` (`String`): The file path to the GeoTIFF file to be loaded. This should be a valid path to an existing GeoTIFF file.
- `iLayer` (`Int`), default `0`: The index of the band (layer) to load from the GeoTIFF file. The default value is `0`, which typically corresponds to the first band.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional options for loading the file, which can include configurations such as data type handling or performance settings.

### Input
The caller must provide a valid path to a GeoTIFF file. The file must exist and be accessible. The pixel type must be specified correctly when calling the method (e.g., `sc.geoTiff[Int]` for integer data).

### Output
Returns `RDD[ITile[T]]` — a distributed collection of raster tiles representing the data from the specified band of the GeoTIFF file. Each tile contains pixel values of the specified type `T`.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Float]] = sc.geoTiff[Float]("treecover")
val raster: RDD[ITile[Int]] = sc.geoTiff[Int]("glc2000_v1_1.tif", 0)
```

### LLM Instruction Prompt
- Ensure the file path provided to `geoTiff` is valid and points to an existing GeoTIFF file. Specify the correct pixel type when calling the method.

### Prompt Snippet
```text
Load a GeoTIFF file using `geoTiff` and specify the desired band and pixel type.
```

### Common Failure Modes
- Providing an invalid file path that does not point to an existing GeoTIFF file will result in a file not found error.
- Specifying a pixel type that does not match the data in the GeoTIFF file may lead to runtime exceptions or incorrect data interpretation.

### Fix Code Hint
```scala
// Ensure the file path is correct and the pixel type matches the data in the GeoTIFF.
val raster: RDD[ITile[Float]] = sc.geoTiff[Float]("valid_path_to_geotiff.tif")
```

## API Test: `geojsonFile`

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
The input must be a valid GeoJSON file or a directory containing GeoJSON files. Ensure that the file path is correct and accessible from the Spark context.

### Output
Returns `SpatialRDD` — a distributed collection of spatial features extracted from the GeoJSON file, which can be used for spatial operations and analysis.

### Valid Call Patterns
```scala
val records = sparkContext.geojsonFile("input.json")
```

### LLM Instruction Prompt
- When calling `geojsonFile`, ensure that the provided filename points to a valid GeoJSON file or directory. The Spark context must be properly configured to access the file.

### Prompt Snippet
```text
Load a GeoJSON file using the geojsonFile method to obtain a SpatialRDD for spatial analysis.
```

### Common Failure Modes
- Providing an invalid file path or a non-GeoJSON file will result in an error.
- Attempting to read from a directory that does not contain any GeoJSON files will also lead to failure.

### Fix Code Hint
```scala
// Ensure the filename is correct and points to a valid GeoJSON file
val records = sparkContext.geojsonFile("valid_input.json")
```

## API Test: `geometryType`

### Signature
```scala
def geometryType: GeometryType
def geometryType: DataType
def geometryType: String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:60  (+2 more definition site/overload)_

_Source doc:_ The most inclusive geometry type for this partition. This can be interpreted as below. - Empty: All geometries are empty - Point: Contains at least one point and zero or more empty geometries - LineString: Contains at least one linestring and zero or more empty geometries - Polygon: Contains at least one polygon and zero or more empty geometries - MultiPoint: Contains at least one multipoint, and zero or more point or empty geometry. - MultiLineString: Contains at least one MultiLineString, and zero or more linestrings and empty geometries. - MultiPolygon: Contains at least one MultiPolygon, and zero or more polygons and empty geometries. - GeometryCollection: Everything else, i.e., none of the above.

### Goal
The `geometryType` function determines the most inclusive geometry type present in a given spatial partition, which is essential for understanding the nature of geometries being processed in geospatial analyses.

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
To determine the geometry type of a spatial partition, use the `geometryType` method on the partition object.
```

### Common Failure Modes
- Calling `geometryType` on an uninitialized or empty spatial partition may lead to unexpected results or errors.
- If the geometries in the partition are not valid, the function may not return the expected geometry type.

### Fix Code Hint
```scala
// Ensure the spatial partition is initialized and populated with valid geometries before calling geometryType
val spatialPartition = ... // Initialize and populate your spatial partition
val geometryType = spatialPartition.geometryType
```

## API Test: `getAttributeName`

### Signature
```scala
def getAttributeName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:92_

_Source doc:_ If names are associated with attributes, this function returns the name of the attribute at the given position (0-based). @param i the index of the attribute to return its name @return the name of the given attribute index or `null` if it does not exist

### Goal
The `getAttributeName` function retrieves the name of an attribute associated with a feature at a specified index, facilitating access to attribute metadata in geospatial analyses.

### Parameters
- `i` (`Int`): The 0-based index of the attribute whose name is to be returned. Valid values are non-negative integers corresponding to the position of attributes.

### Input
The caller must provide a feature object that contains attributes. The attributes should be indexed, and the index `i` must be within the bounds of the available attributes.

### Output
Returns `String` — the name of the attribute at the specified index, or `null` if the index does not correspond to an existing attribute.

### Valid Call Patterns
```scala
val inputPath = makeFileCopy("/test.partitions")
val data = sparkContext.readWKTFile(inputPath.getPath, "Geometry", '\t', true)
val feature = data.first()
assert(feature.getAttributeName(0) == "ID")
assert(feature.getAttributeName(1) == "File Name")
```

### LLM Instruction Prompt
- When calling `getAttributeName`, ensure that the index provided is valid and corresponds to an existing attribute in the feature. Handle cases where the index may be out of bounds.

### Prompt Snippet
```text
Retrieve the name of the attribute at the specified index using the getAttributeName method.
```

### Common Failure Modes
- Providing an index `i` that is negative or exceeds the number of available attributes will result in a `null` return value.
- Attempting to call `getAttributeName` on a feature that does not have any attributes will also yield `null`.

### Fix Code Hint
```scala
// Ensure the index is within the valid range before calling getAttributeName
if (i >= 0 && i < feature.getAttributeCount) {
    val attributeName = feature.getAttributeName(i)
} else {
    // Handle the case where the index is out of bounds
}
```

## API Test: `getBoolean`

### Signature
```scala
def getBoolean(key: String, defaultValue: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:133_

_Source doc:_ Get value as boolean @param key @param defaultValue @return

### Goal
Retrieve a boolean value associated with a specified key, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The name of the option whose boolean value is to be retrieved. Expected values are option names defined in the command line arguments.
- `defaultValue` (`Boolean`): The value to return if the specified key does not exist. This allows for a fallback option when the key is not found.

### Input
The caller must provide a valid key as a string that corresponds to an option in the command line arguments. The `defaultValue` must be a boolean indicating what to return if the key is absent.

### Output
Returns `Boolean` — the boolean value associated with the specified key, or the `defaultValue` if the key is not found.

### Valid Call Patterns
```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1", "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")
assert(parsed.options.getBoolean("option2", defaultValue = false)) // returns false if "option2" is not present
assert(!parsed.options.getBoolean("option3", defaultValue = true)) // returns true if "option3" is not present
```

### LLM Instruction Prompt
- Ensure that the `key` provided is a valid option name that has been defined in the command line arguments. Use the `defaultValue` to handle cases where the key is not present.

### Prompt Snippet
```text
Retrieve the boolean value for the specified option key, using the provided default value if the key is not found.
```

### Common Failure Modes
- The `key` provided does not match any defined options, leading to the return of the `defaultValue`.
- If the `defaultValue` is not a boolean, it may lead to unexpected behavior.

### Fix Code Hint
```scala
// Ensure the key is correctly defined in the command line arguments
val value = parsed.options.getBoolean("your_option_key", defaultValue = false)
```

## API Test: `getFeatureReaderClass`

### Signature
```scala
def getFeatureReaderClass(path: String, opts: BeastOptions): Class[_ <: FeatureReader]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:398_

_Source doc:_ The class of the feature reader to use with this RDD. All partitions use the same feature reader.

### Goal
Determines the appropriate feature reader class to use for reading spatial data from a specified file path.

### Parameters
- `path` (`String`): The file path to the spatial data source, which can be in formats such as GeoJSON or other supported formats.
- `opts` (`BeastOptions`): Configuration options for the feature reader, specifying the input format and any additional parameters required for reading the data.

### Input
The caller must provide a valid file path to a spatial data file (e.g., GeoJSON) and a `BeastOptions` instance that specifies the input format and any relevant options. The file must be accessible and in a supported format.

### Output
Returns `Class[_ <: FeatureReader]` — the class type of the feature reader that will be used to read the spatial data from the specified path.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
```

### LLM Instruction Prompt
- Ensure that the `path` provided points to a valid spatial data file and that the `opts` parameter is correctly configured to match the file format.

### Prompt Snippet
```text
To read spatial data from a file, use `getFeatureReaderClass` with the file path and appropriate options.
```

### Common Failure Modes
- Providing an invalid or inaccessible file path will result in an error.
- Using an unsupported file format in the `opts` may lead to a failure in determining the correct feature reader class.

### Fix Code Hint
```scala
// Ensure the file path is correct and the options are set for the expected input format.
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(validFilePath, validBeastOptions)
```

## API Test: `getGeometry`

### Signature
```scala
def getGeometry: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:69_

_Source doc:_ The geometry contained in the feature. @return the geometry in this attribute

### Goal
Retrieve the geometric representation of a feature, which is essential for spatial analysis in geospatial raster processing.

### Parameters
_None._

### Input
The caller must provide a feature instance that contains a geometry. This geometry must be compatible with the operations being performed in the context of geospatial analysis.

### Output
Returns `Geometry` — the geometric representation of the feature, which can be used for spatial operations and analysis.

### Valid Call Patterns
```scala
val geometry: Geometry = feature.getGeometry
```

### LLM Instruction Prompt
- Ensure that the feature instance from which `getGeometry` is called is properly initialized and contains valid geometry data.

### Prompt Snippet
```text
Retrieve the geometry of the feature using the `getGeometry` method.
```

### Common Failure Modes
- Calling `getGeometry` on a feature that has not been properly initialized or does not contain valid geometry data may result in a runtime error.

### Fix Code Hint
```scala
if (feature != null && feature.getGeometry != null) {
  val geometry: Geometry = feature.getGeometry
} else {
  // Handle the case where the feature or geometry is not valid
}
```

## API Test: `getInt`

### Signature
```scala
override def getInt(i: Int): Int
def getInt(key: String, defaultValue: Int): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:98  (+1 more definition site/overload)_

_Source doc:_ Get a value of a key as integer @param key @param defaultValue @return

### Goal
Retrieve an integer value associated with a specified key, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The key for which the integer value is to be retrieved. This should be a valid string that corresponds to a stored configuration or option.
- `defaultValue` (`Int`): The integer value to return if the specified key does not exist. This serves as a fallback to ensure that a valid integer is always returned.

### Input
The caller must provide a valid string key and an integer default value. The key should correspond to a configuration option that may or may not be present.

### Output
Returns `Int` — the integer value associated with the specified key if it exists; otherwise, it returns the provided default value.

### Valid Call Patterns
```scala
value.getInt("someKey", 42)
```

### LLM Instruction Prompt
- When calling `getInt`, ensure that the key is a valid string and the default value is an integer. The method will return the integer associated with the key or the default value if the key is not found.

### Prompt Snippet
```text
Retrieve the integer value for the specified key, using the default value if the key is absent.
```

### Common Failure Modes
- If the key is not found, the method will return the default value instead of throwing an error.
- Providing a non-integer default value will result in a compilation error, as the method expects an `Int`.

### Fix Code Hint
```scala
// Ensure the key is a valid string and the default value is an integer.
val value = someObject.getInt("myKey", 10) // Correct usage
```

## API Test: `getLong`

### Signature
```scala
def getLong(key: String, defaultValue: Long): Long
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:114_

_Source doc:_ Get a key value as long @param key @param defaultValue @return

### Goal
`getLong` retrieves a configuration value associated with a specified key as a `Long`, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The configuration key whose associated value is to be retrieved. This should be a valid key defined in the configuration context.
- `defaultValue` (`Long`): The value to return if the specified key does not exist in the configuration. This should be a valid long integer.

### Input
The caller must provide a valid configuration key as a string and a default long value. There are no specific file formats required for this function, as it operates on configuration data.

### Output
Returns `Long` — the value associated with the specified key in the configuration, or the provided `defaultValue` if the key is not found.

### Valid Call Patterns
```scala
value.getLong("someKey", 42L)
```

### LLM Instruction Prompt
- When calling `getLong`, ensure that the key is a valid string representing a configuration key, and provide a sensible default value of type `Long`.

### Prompt Snippet
```text
Retrieve the long value associated with the key "someKey", using 42 as the default if the key is not found.
```

### Common Failure Modes
- Providing a `key` that does not exist in the configuration may lead to returning the `defaultValue`, which could be unexpected if the caller assumes the key exists.
- If the `defaultValue` is not a valid `Long`, it may cause a type mismatch error.

### Fix Code Hint
```scala
// Ensure the key exists in the configuration or provide a meaningful default value.
val value: Long = config.getLong("existingKey", 0L)
```

## API Test: `getName`

### Signature
```scala
def getName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:83_

_Source doc:_ Return the name of the given attribute. @param i the index of the attribute in the range [0, length[ @return the type of the attribute or null if unknown

### Goal
Retrieve the name of a specified attribute from a feature in a geospatial dataset.

### Parameters
- `i` (`Int`): The index of the attribute for which the name is requested. It must be within the range [0, length[ of the attributes available in the feature.

### Input
The caller must provide a valid index `i` that corresponds to an existing attribute in the feature. The feature must be properly initialized and contain attributes.

### Output
Returns `String` — The name of the attribute at the specified index. If the index is out of bounds or the attribute is unknown, it may return `null`.

### Valid Call Patterns
```scala
val attributeName: String = feature.getName(0) // Example of retrieving the name of the first attribute
```

### LLM Instruction Prompt
- Ensure that the index `i` is within the valid range of attribute indices for the feature being queried.

### Prompt Snippet
```text
Retrieve the name of the attribute at index 0 from the feature using getName(0).
```

### Common Failure Modes
- Providing an index `i` that is less than 0 or greater than or equal to the number of attributes in the feature will result in an error or a null return value.

### Fix Code Hint
```scala
if (i < 0 || i >= feature.getAttributeCount) {
  throw new IllegalArgumentException("Index out of bounds for attribute retrieval.")
}
```

## API Test: `getOperationParams`

### Signature
```scala
def getOperationParams(operation: Operation, opts: BeastOptions): Array[OperationParamInfo]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:209_

_Source doc:_ Returns all parameters that are allowed for the given operation. Operation parameters are all parameters annotated with [[OperationParam]] that appear in one of the following: - In the class associated with the given operation - In any additional classes defined in the [[OperationMetadata]] annotation on the class - In any classes that are added through the method [[IConfigurable]].addDependentClasses @param operation the operation in question @param opts any additional user options. This is used to add dependent classes if they depend on some user choice. For example, if the user selects a specific indexer, it can be used to add that specific indexer as a dependent class @return an array of parameters that are allowed

### Goal
The `getOperationParams` function retrieves all parameters that can be used with a specified raster operation in RDPro.

### Parameters
- `operation` (`Operation`): The specific raster operation for which parameters are being requested. This could be any operation defined within the RDPro library, such as a transformation or a zonal statistics computation.
- `opts` (`BeastOptions`): Additional user options that may influence the parameters returned. This can include configurations that determine which dependent classes should be included based on user choices.

### Input
The caller must provide a valid `Operation` instance representing the desired operation and an optional `BeastOptions` instance. The `Operation` should correspond to one of the operations defined in the RDPro library.

### Output
Returns `Array[OperationParamInfo]` — an array of parameter information objects that detail the parameters allowed for the specified operation. Each `OperationParamInfo` object contains metadata about the parameters, such as their names and types.

### Valid Call Patterns
```scala
val params = OperationHelper.getOperationParams(OperationHelper.operations("test"), null)
```

### LLM Instruction Prompt
- Ensure that the `operation` parameter is a valid instance of `Operation` defined in the RDPro library.
- The `opts` parameter can be passed as `null` if no additional options are needed.

### Prompt Snippet
```text
Retrieve the operation parameters for a specific raster operation using `getOperationParams`.
```

### Common Failure Modes
- Passing an invalid or unrecognized `Operation` instance will result in an error or an empty array.
- If the `opts` parameter is not compatible with the selected operation, it may lead to unexpected results or exceptions.

### Fix Code Hint
```scala
// Ensure the operation is valid and check the documentation for required parameters.
val validOperation = OperationHelper.operations("test") // Ensure this operation exists
val params = OperationHelper.getOperationParams(validOperation, null)
```

## API Test: `getPartition`

### Signature
```scala
override def getPartition(tile: Any): Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterPartitioner.scala:43_

_Source doc:_ Returns the partition of the given tileID @param tile the tile ID in the input RasterMetadata to return its partition @return the partition ID associated with the given tile

### Goal
The `getPartition` function determines the partition ID associated with a specific tile ID within the raster metadata, facilitating efficient data processing in distributed raster operations.

### Parameters
- `tile` (`Any`): The tile ID for which the partition is being requested. This ID should correspond to a valid tile within the input raster's metadata.

### Input
The caller must provide a valid tile ID that exists within the raster metadata. The raster metadata should be initialized and associated with a `RasterPartitioner` instance.

### Output
Returns `Int` — the partition ID associated with the given tile ID, indicating which partition the tile belongs to in the distributed processing framework.

### Valid Call Patterns
```scala
val rasterMetadata = new RasterMetadata(0, 0, 1000, 1000, 100, 100, 4326, new AffineTransform())
val partitioner = new RasterPartitioner(rasterMetadata, 25)
assertResult(0)(partitioner.getPartition(0))
assertResult(0)(partitioner.getPartition(11))
assertResult(24)(partitioner.getPartition(99))
```

### LLM Instruction Prompt
- When calling `getPartition`, ensure that the tile ID provided is valid and corresponds to a tile within the initialized raster metadata.

### Prompt Snippet
```text
val partitionId = partitioner.getPartition(tileId)
```

### Common Failure Modes
- Providing a tile ID that does not exist in the raster metadata may result in an incorrect partition ID being returned or an error.
- The raster metadata must be properly initialized before calling `getPartition`; otherwise, it may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the tile ID is valid and corresponds to the initialized raster metadata
val validTileId = 0 // Example of a valid tile ID
val partitionId = partitioner.getPartition(validTileId)
```

## API Test: `getPointValue`

### Signature
```scala
def getPointValue(x: Double, y: Double): T
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93_

_Source doc:_ Return the value of the pixel that contains the given point at model (world) coordinates. @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the value of all components of the given pixel

### Goal
`getPointValue` retrieves the pixel value at specified world coordinates (longitude and latitude) from a raster dataset.

### Parameters
- `x` (`Double`): The x-coordinate of the point, typically representing longitude in model (world) coordinates.
- `y` (`Double`): The y-coordinate of the point, typically representing latitude in model (world) coordinates.

### Input
The caller must provide valid world coordinates (longitude and latitude) that correspond to a pixel in the loaded raster dataset. The raster must be loaded using a compatible method, such as `sc.geoTiff[T]`, where `T` matches the pixel type of the raster.

### Output
Returns `T` — the value of the pixel at the specified coordinates, which may represent a single band value or an array of values for multi-band rasters.

### Valid Call Patterns
```scala
val rasterPath = new Path(makeFileCopy("/rasters/glc2000_small.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val pixelValue = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415)).getPointValue(23.224, 32.415)
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Ensure that the coordinates provided to `getPointValue` are within the bounds of the raster dataset. The raster must be properly initialized and loaded before calling this method.

### Prompt Snippet
```text
Retrieve the pixel value at the specified longitude and latitude using the getPointValue method.
```

### Common Failure Modes
- Calling `getPointValue` with coordinates that are outside the bounds of the raster will result in an error or an undefined value.
- If the raster is not properly initialized or loaded, calling `getPointValue` will lead to runtime exceptions.

### Fix Code Hint
```scala
Ensure the raster is loaded correctly and that the coordinates are within the raster's extent before calling getPointValue.
```

## API Test: `getStorageSize`

### Signature
```scala
def getStorageSize(value: Any, dataType: DataType): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:112  (+1 more definition site/overload)_

### Goal
Estimates the total storage size of a feature in bytes, including its geometry and associated features.

### Parameters
- `value` (`Any`): The feature whose storage size is to be calculated. This can include geometries, attributes, or any other data associated with the feature.
- `dataType` (`DataType`): The type of the data being processed, which helps in determining how to calculate the storage size accurately.

### Input
The caller must provide a valid feature object as `value` and a corresponding `DataType` that matches the feature's structure. The feature can be a geometry or a complex object containing various attributes.

### Output
Returns `Int` — the estimated total size of the feature in bytes, which includes the geometry and its associated features.

### Valid Call Patterns
```scala
val feature = Feature.create(Row.apply(123.25, "name", new PointND(GeometryReader.DefaultGeometryFactory, 2, 0.0, 1.0), "name2", null), null)
val size: Int = feature.getStorageSize(value, dataType)
```

### LLM Instruction Prompt
- Ensure that the `value` provided is a valid feature object and that the `dataType` corresponds to the type of data contained within the feature.

### Prompt Snippet
```text
Calculate the storage size of a feature using `getStorageSize` by providing a valid feature and its data type.
```

### Common Failure Modes
- Providing a `value` that is not a valid feature object may result in an exception or an incorrect size calculation.
- Mismatching the `dataType` with the actual type of the `value` can lead to inaccurate size estimations.

### Fix Code Hint
```scala
Ensure that the `value` is a properly constructed feature and that the `dataType` accurately reflects the type of data contained within the feature.
```

## API Test: `getTileIDAtPixel`

### Signature
```scala
def getTileIDAtPixel(iPixel: Int, jPixel: Int): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:69_

_Source doc:_ Computes the ID of the tile that contains the given pixel. Tiles are numbered in row-wise ordering. @param iPixel the position of the column of the pixel @param jPixel the position of the row of the pixel @return a unique identifier for the tile that contains this pixel location

### Goal
The `getTileIDAtPixel` function retrieves the unique identifier of the tile that contains a specified pixel in a raster dataset, facilitating efficient access to tile-based raster data.

### Parameters
- `iPixel` (`Int`): The column index of the pixel within the raster, where the index starts at 0. Valid values are non-negative integers that are less than the raster's width.
- `jPixel` (`Int`): The row index of the pixel within the raster, where the index starts at 0. Valid values are non-negative integers that are less than the raster's height.

### Input
The caller must provide valid pixel indices (`iPixel` and `jPixel`) that correspond to the dimensions of the raster being processed. The raster must be loaded and accessible in the context where this function is called.

### Output
Returns `Int` — a unique identifier for the tile that contains the specified pixel location, based on a row-wise numbering scheme of the tiles.

### Valid Call Patterns
```scala
val tileID = reader.metadata.getTileIDAtPixel(37, 24)
```

### LLM Instruction Prompt
- When calling `getTileIDAtPixel`, ensure that the pixel indices provided are within the bounds of the raster's dimensions. The raster must be properly initialized and accessible.

### Prompt Snippet
```text
Retrieve the tile ID for the pixel located at column 37 and row 24 in the raster.
```

### Common Failure Modes
- Providing pixel indices (`iPixel` or `jPixel`) that are out of bounds for the raster dimensions will result in an error.
- Attempting to call `getTileIDAtPixel` on an uninitialized or improperly loaded raster will lead to a runtime exception.

### Fix Code Hint
```scala
// Ensure the pixel indices are within the raster dimensions before calling the function
if (iPixel >= 0 && iPixel < rasterWidth && jPixel >= 0 && jPixel < rasterHeight) {
    val tileID = reader.metadata.getTileIDAtPixel(iPixel, jPixel)
} else {
    throw new IllegalArgumentException("Pixel indices are out of bounds.")
}
```

## API Test: `getTileIDAtPoint`

### Signature
```scala
def getTileIDAtPoint(x: Double, y: Double): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:81_

_Source doc:_ Returns the ID of the tile that contains the given point location in model (world) space @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the ID of the tile that contains this pixel or -1 if the point is outside the input space

### Goal
The `getTileIDAtPoint` function retrieves the ID of the raster tile that encompasses a specified geographic point, facilitating efficient access to raster data in large-scale geospatial analyses.

### Parameters
- `x` (`Double`): The x-coordinate of the point, typically representing longitude in model (world) space.
- `y` (`Double`): The y-coordinate of the point, typically representing latitude in model (world) space.

### Input
The caller must provide valid geographic coordinates (longitude and latitude) as `Double` values. The point must lie within the bounds of the raster dataset; otherwise, the function will return -1.

### Output
Returns `Int` — the ID of the tile that contains the specified point. If the point is outside the input space, it returns -1.

### Valid Call Patterns
```scala
val tileId: Int = reader.metadata.getTileIDAtPoint(23.224, 32.415)
```

### LLM Instruction Prompt
- Ensure that the x and y coordinates provided are within the bounds of the raster dataset to avoid receiving -1 as a result.

### Prompt Snippet
```text
Call `getTileIDAtPoint` with valid longitude and latitude values to retrieve the corresponding tile ID from the raster metadata.
```

### Common Failure Modes
- Providing coordinates that are outside the bounds of the raster dataset, which will result in a return value of -1.
- Using incorrect data types for the x and y parameters, which may lead to compilation errors.

### Fix Code Hint
```scala
// Ensure the coordinates are within the raster bounds before calling the function
if (isWithinBounds(x, y)) {
    val tileId: Int = reader.metadata.getTileIDAtPoint(x, y)
} else {
    println("Coordinates are outside the raster bounds.")
}
```

## API Test: `getTitle`

### Signature
```scala
private[davinci] def getTitle(feature: IFeature): String
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SVGPlotter.scala:76_

_Source doc:_ Extract the title of the given feature by interpolating the [[svgTitle]] with feature attributes @param feature the feature to extract the elements from @return the string that interpolates the given string with the feature

### Goal
`getTitle` extracts and returns a formatted title string for a given feature by interpolating the `svgTitle` template with the feature's attributes.

### Parameters
- `feature` (`IFeature`): The feature from which to extract attributes for title interpolation. It is expected to contain attribute names and values that can be used in the `svgTitle` string.

### Input
The caller must provide an `IFeature` instance that contains the necessary attributes for title interpolation. The `svgTitle` should be defined in the context of the `SVGPlotter` class, and it may include placeholders for attributes (e.g., `${id}`, `${name-full}`).

### Output
Returns `String` — A formatted title string that is generated by interpolating the `svgTitle` with the values of the specified attributes from the `feature`.

### Valid Call Patterns
```scala
val plotter = new SVGPlotter
plotter.svgTitle = "record #${id}"
val title = plotter.getTitle(Feature.create(EmptyGeometry.instance, Array("id"), null, Array(15)))
// title will be "record #15"
```

### LLM Instruction Prompt
- When calling `getTitle`, ensure that the `feature` provided contains the attributes referenced in the `svgTitle` string. The `svgTitle` should be set prior to calling `getTitle`.

### Prompt Snippet
```text
To extract a title from a feature, set the svgTitle in the SVGPlotter instance and call getTitle with the feature containing the relevant attributes.
```

### Common Failure Modes
- If the `feature` does not contain the attributes referenced in the `svgTitle`, the resulting string may not be formatted correctly or may contain placeholders instead of actual values.
- If `svgTitle` is not set before calling `getTitle`, the method may return an unexpected or default title.

### Fix Code Hint
```scala
// Ensure svgTitle is set correctly before calling getTitle
plotter.svgTitle = "record #${id}"
val title = plotter.getTitle(feature) // feature must have the 'id' attribute
```

## API Test: `getValue`

### Signature
```scala
def getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)
def getValue(fileSystem: FileSystem, path: Path, key: Long): (Long, Int)
def getValue(i: Int, j: Int, position: Int): T
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91  (+2 more definition site/overload)_

_Source doc:_ Return the value that corresponds to the given key or null if the value is not found. @param in the hashtable file @param offset the offset of the hashtable in the file @param key the key to search for @return the value of the key if found, or `null` if the key is not found.

### Goal
The `getValue` function retrieves the value associated with a specified key from a hashtable stored in a file, returning the value or indicating if the key is not found.

### Parameters
- `in` (`FSDataInputStream`): The input stream from which the hashtable is read. It is expected to be a valid stream that points to a hashtable file.
- `offset` (`Long`): The byte offset in the file where the hashtable begins. This value should be correctly calculated based on the file structure.
- `key` (`Long`): The key for which the value is being searched in the hashtable. This should be a valid key that exists within the hashtable.

### Input
The caller must provide a valid `FSDataInputStream` that points to a hashtable file, a correct byte offset indicating where the hashtable starts, and a key that is expected to be present in the hashtable.

### Output
Returns `(Long, Int)` — the first element is the value associated with the key if found, and the second element is an integer indicating the status (e.g., whether the key was found).

### Valid Call Patterns
```scala
histogram.getValue(inStream, 1024L, 42L)
```

### LLM Instruction Prompt
- Ensure that the `FSDataInputStream` is properly initialized and points to a valid hashtable file. The offset must be accurate, and the key should be a valid long integer that exists in the hashtable.

### Prompt Snippet
```text
Retrieve the value associated with the key from the hashtable file using the provided input stream and offset.
```

### Common Failure Modes
- Providing an invalid `FSDataInputStream` that does not point to a valid hashtable file.
- Using an incorrect offset that does not correspond to the start of the hashtable.
- Searching for a key that does not exist in the hashtable, which may lead to a null return.

### Fix Code Hint
```scala
// Ensure the FSDataInputStream is correctly initialized and the offset is valid
val value: (Long, Int) = getValue(inStream, validOffset, validKey)
```

## API Test: `gridToModel`

### Signature
```scala
def gridToModel(i: Double, j: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:150_

_Source doc:_ Converts a point location from the grid (pixel) space to the model (world) space @param i the position of the column @param j the position of the row @param outPoint the output point that contains the model coordinates

### Goal
The `gridToModel` function converts pixel coordinates (grid space) into geographic coordinates (model space) for raster data.

### Parameters
- `i` (`Double`): The column index of the pixel in the raster grid, typically ranging from `0` to the raster width minus one.
- `j` (`Double`): The row index of the pixel in the raster grid, typically ranging from `0` to the raster height minus one.
- `outPoint` (`Point2D.Double`): An instance of `Point2D.Double` that will be populated with the corresponding geographic coordinates after the conversion.

### Input
The caller must provide valid pixel indices `i` and `j` that correspond to a pixel within the bounds of the raster. The `outPoint` must be a pre-initialized `Point2D.Double` object.

### Output
Returns `Unit` — this indicates that the function does not return a value but instead modifies the `outPoint` parameter to contain the model coordinates corresponding to the provided pixel indices.

### Valid Call Patterns
```scala
val point = new Point2D.Double()
metadata.gridToModel(100, 200, point)
```

### LLM Instruction Prompt
- Ensure that the pixel indices `i` and `j` are within the valid range of the raster dimensions before calling `gridToModel`. The `outPoint` must be a valid, initialized `Point2D.Double` object.

### Prompt Snippet
```text
Call `gridToModel` with valid pixel indices and an initialized `Point2D.Double` to receive the corresponding geographic coordinates.
```

### Common Failure Modes
- Calling `gridToModel` with pixel indices `i` or `j` that are out of bounds for the raster dimensions will lead to incorrect results or runtime errors.
- Failing to initialize the `outPoint` before passing it to `gridToModel` will result in a null reference or unexpected behavior.

### Fix Code Hint
```scala
// Ensure pixel indices are within bounds and outPoint is initialized
if (i >= 0 && i < rasterWidth && j >= 0 && j < rasterHeight) {
    val outPoint = new Point2D.Double()
    metadata.gridToModel(i, j, outPoint)
} else {
    throw new IllegalArgumentException("Pixel indices are out of bounds.")
}
```

## API Test: `hdfFile`

### Signature
```scala
def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]]
def hdfFile(filename: String, layer: String): JavaRasterRDD[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46  (+1 more definition site/overload)_

### Goal
Loads raster data from a Hierarchical Data Format (HDF) file or a directory of HDF files, extracting a specified layer for geospatial analysis.

### Parameters
- `path` (`String`): The file path to the HDF file or directory containing HDF files. This should be a valid path accessible by the Spark cluster.
- `layer` (`String`): The name of the layer within the HDF file that you want to read. This should correspond to a valid layer name present in the specified HDF file.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for configuring the reading process, such as specifying additional parameters for handling the HDF data. This can be left as default for standard operations.

### Input
The caller must provide a valid HDF file path and a layer name that exists within that file. The HDF file must be accessible to the Spark environment, and the specified layer must be correctly named to avoid errors during loading.

### Output
Returns `RDD[ITile[Float]]` — a distributed collection of raster tiles, where each tile contains pixel values of type `Float`. This output represents the raster data extracted from the specified layer of the HDF file, suitable for further geospatial processing.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] = sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
```

### LLM Instruction Prompt
- Ensure that the `path` points to a valid HDF file and that the `layer` name is correct. Use default `BeastOptions` unless specific configurations are needed.

### Prompt Snippet
```text
Load raster data from an HDF file using the hdfFile method, specifying the correct file path and layer name.
```

### Common Failure Modes
- **File Not Found**: If the specified `path` does not point to a valid HDF file or directory, a file not found error will occur.
- **Layer Not Found**: If the specified `layer` does not exist in the HDF file, an error will be raised indicating that the layer could not be found.
- **Access Issues**: If the Spark environment does not have permission to access the specified file path, an access denied error will occur.

### Fix Code Hint
```scala
Check that the file path is correct and that the layer name matches one of the layers in the HDF file. Ensure that the Spark job has the necessary permissions to access the file.
```

## API Test: `id`

### Signature
```scala
def id: Int
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58_

### Goal
The `id` function retrieves the unique identifier for the current dataset or processing instance within the RDPro framework.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Int` — the unique identifier associated with the current dataset or processing instance.

### Valid Call Patterns
```scala
val uniqueId: Int = value.id
```

### LLM Instruction Prompt
- When calling `id`, ensure that it is invoked on an instance of a class that contains this method, as it does not take any parameters.

### Prompt Snippet
```text
Retrieve the unique identifier for the current dataset using the id method.
```

### Common Failure Modes
- Attempting to call `id` on an instance that does not have this method defined will result in a compilation error.

### Fix Code Hint
```scala
// Ensure you are calling id on a valid instance of the class that defines this method.
val uniqueId: Int = value.id
```

## API Test: `image`

### Signature
```scala
private def image(): Unit
```
_Source: beast/satex/src/main/scala/edu/ucr/cs/bdlab/beast/satex/ImageIterator.scala:58_

### Goal
The `image` function is designed to perform internal operations related to raster image processing within the RDPro library.

### Parameters
_None._

### Input
No specific input parameters are required for the `image` function.

### Output
Returns `Unit` — this indicates that the function does not produce a return value but performs an operation related to raster image processing.

### Valid Call Patterns
```scala
value.image()
```

### LLM Instruction Prompt
- When calling `image`, ensure that it is invoked within the appropriate context of the RDPro library, as it does not accept parameters and is intended for internal processing.

### Prompt Snippet
```text
Call the `image` function to execute internal raster image processing operations.
```

### Common Failure Modes
- The function may not execute as expected if called outside the intended context of the RDPro library or if the necessary internal state is not properly initialized.

### Fix Code Hint
```scala
Ensure that the `image` function is called within a properly configured RDPro environment where all necessary dependencies and internal states are set up.
```

## API Test: `initialized`

### Signature
```scala
def initialized: Boolean
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileReader.scala:48_

_Source doc:_ A flag that is raised after the file has been initialized

### Goal
The `initialized` function checks whether the file has been successfully initialized for processing within the RDPro framework.

### Parameters
_None._

### Input
No specific input is required for this function. It is called on an instance of a class that manages file initialization.

### Output
Returns `Boolean` — `true` if the file has been initialized successfully, and `false` otherwise.

### Valid Call Patterns
```scala
value.initialized
```

### LLM Instruction Prompt
- Call `initialized` on an instance of the relevant class to check the initialization status of the file.

### Prompt Snippet
```text
Check if the file has been initialized by calling the initialized method on the instance.
```

### Common Failure Modes
- Calling `initialized` before the file has been initialized will return `false`.
- Ensure that the instance on which `initialized` is called has undergone the initialization process.

### Fix Code Hint
```scala
Ensure that the file is properly initialized before checking the initialized status.
```

## API Test: `isCW`

### Signature
```scala
def isCW: Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:97_

_Source doc:_ Checks whether this list of points form a closed ring stored in CW order @return `true` if the points form a ring and the ring is stored in clock-wise order

### Goal
Determines if a given set of points forms a closed ring in a clockwise order, which is essential for validating geometrical shapes in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a list of points that represent a closed ring. The points should be structured in a way that they can be interpreted as a polygon.

### Output
Returns `Boolean` — `true` if the points form a closed ring and the ring is stored in clockwise order; otherwise, returns `false`.

### Valid Call Patterns
```scala
val isClockwise: Boolean = simplifiedPolygon.isCW
```

### LLM Instruction Prompt
- Ensure that the list of points has been defined as a closed ring before calling `isCW`. The points must be in a format compatible with the geometry being processed.

### Prompt Snippet
```text
Check if the polygon's outer shell is in clockwise order using the isCW method.
```

### Common Failure Modes
- Calling `isCW` on a geometry that does not represent a closed ring will lead to incorrect results.
- If the points are not structured correctly, the method may not function as intended.

### Fix Code Hint
```scala
// Ensure the geometry is a valid polygon with a closed ring before calling isCW
if (polygon.isClosed) {
    val isClockwise: Boolean = polygon.isCW
} else {
    throw new IllegalArgumentException("The geometry must be a closed ring.")
}
```

## API Test: `isDefined`

### Signature
```scala
@inline def isDefined(i: Int, j: Int): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126_

_Source doc:_ Checks if the given pixel is defined (not empty) @param i the index of the column @param j the index of the row @return `true` if pixel has a valid value or `false` if it does not.

### Goal
The `isDefined` function checks whether a specific pixel in a raster dataset has a valid value, indicating that it is not empty.

### Parameters
- `i` (`Int`): The index of the column in the raster grid, representing the horizontal position of the pixel.
- `j` (`Int`): The index of the row in the raster grid, representing the vertical position of the pixel.

### Input
The caller must provide valid indices `i` and `j` that correspond to the dimensions of the raster dataset. The raster must be loaded and accessible in the context where `isDefined` is called.

### Output
Returns `Boolean` — `true` if the pixel at the specified indices has a valid value (is defined), or `false` if it does not (is empty).

### Valid Call Patterns
```scala
val defined: Boolean = raster.isDefined(i, j)
```

### LLM Instruction Prompt
- Ensure that the indices `i` and `j` are within the bounds of the raster dimensions before calling `isDefined`.

### Prompt Snippet
```text
Check if the pixel at column index i and row index j is defined using the isDefined method.
```

### Common Failure Modes
- Calling `isDefined` with indices `i` or `j` that are out of bounds for the raster dimensions will result in an error.
- Attempting to call `isDefined` on a raster that has not been properly loaded or initialized may lead to a null reference error.

### Fix Code Hint
```scala
// Ensure indices are within bounds before calling isDefined
if (i >= 0 && i < raster.cols && j >= 0 && j < raster.rows) {
    val defined: Boolean = raster.isDefined(i, j)
} else {
    throw new IndexOutOfBoundsException("Indices are out of bounds for the raster dimensions.")
}
```

## API Test: `isEmptyAt`

### Signature
```scala
def isEmptyAt(x: Double, y: Double): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:114_

_Source doc:_ Check if the pixel that contains the given location is empty @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return `true` if the pixel at the location is empty, i.e., contains no data

### Goal
The `isEmptyAt` function checks whether the pixel at a specified geographic location contains no data, which is essential for accurate geospatial analysis.

### Parameters
- `x` (`Double`): The x-coordinate of the point, typically representing longitude.
- `y` (`Double`): The y-coordinate of the point, typically representing latitude.

### Input
The function requires valid geographic coordinates (longitude and latitude) as input. The caller must ensure that the coordinates correspond to a pixel within the bounds of the raster dataset being analyzed.

### Output
Returns `Boolean` — `true` if the pixel at the specified location is empty (contains no data), and `false` otherwise.

### Valid Call Patterns
```scala
val rasterPath = locateResource("/rasters/glc2000_small.tif")
val fileSystem = new Path(rasterPath.getPath).getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.getPath, "0", "fillvalue" -> 8)
  val isEmpty = reader.isEmptyAt(23.224, 32.415)
  assert(isEmpty)
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- When calling `isEmptyAt`, ensure that the coordinates provided are within the bounds of the raster dataset and that the dataset has been properly initialized.

### Prompt Snippet
```text
Check if the pixel at the specified coordinates is empty using the isEmptyAt method.
```

### Common Failure Modes
- Calling `isEmptyAt` with coordinates that are outside the bounds of the raster dataset will likely result in an error or unexpected behavior.
- If the raster dataset has not been properly initialized or loaded, the function may not return valid results.

### Fix Code Hint
```scala
Ensure that the raster dataset is loaded and initialized correctly before calling isEmptyAt, and verify that the coordinates are within the raster's extent.
```

## API Test: `isSpatiallyPartitioned`

### Signature
```scala
def isSpatiallyPartitioned: Boolean
def isSpatiallyPartitioned(rdd: JavaSpatialRDD): Boolean
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:45  (+1 more definition site/overload)_

_Source doc:_ Tells whether a SpatialRDD is partitioned using any spatial partitioner or not @return {@code true} if the RDD is partitioned using any spatial partitioner

### Goal
The `isSpatiallyPartitioned` function checks if a `SpatialRDD` is organized using a spatial partitioner, which is essential for optimizing spatial queries and operations in geospatial raster processing.

### Parameters
- `rdd` (`JavaSpatialRDD`): An instance of `JavaSpatialRDD` that represents a distributed collection of spatial data. This argument is used in the overloaded version of the function to determine if the specified RDD is spatially partitioned.

### Input
The caller must provide a `JavaSpatialRDD` that has been created and populated with spatial data. The RDD should be properly initialized and may contain spatial features such as points, lines, or polygons.

### Output
Returns `Boolean` — `true` if the `SpatialRDD` is partitioned using any spatial partitioner, indicating that spatial operations can be performed efficiently; otherwise, it returns `false`.

### Valid Call Patterns
```scala
val isPartitioned: Boolean = value.isSpatiallyPartitioned
```

### LLM Instruction Prompt
- When calling `isSpatiallyPartitioned`, ensure that the `SpatialRDD` is properly initialized and populated with spatial data to avoid runtime errors.

### Prompt Snippet
```text
Check if the SpatialRDD is partitioned using a spatial partitioner by calling isSpatiallyPartitioned on the RDD instance.
```

### Common Failure Modes
- Calling `isSpatiallyPartitioned` on an uninitialized or empty `JavaSpatialRDD` may lead to unexpected results or exceptions.
- The function may return `false` if the RDD was not partitioned using a spatial partitioner, which could affect subsequent spatial operations.

### Fix Code Hint
```scala
// Ensure the JavaSpatialRDD is properly initialized before calling isSpatiallyPartitioned
val spatialRDD: JavaSpatialRDD = new JavaSpatialRDD(...) // Initialize with spatial data
val isPartitioned: Boolean = spatialRDD.isSpatiallyPartitioned
```

## API Test: `lastNFiles`

### Signature
```scala
def lastNFiles(fs: FileSystem, path: Path, n: Int): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:48_

_Source doc:_ Returns information about the last n files in the archive. **Compatibility Note**: This method is not guaranteed to return the correct answer. For efficiency, it tries to locate the directory entries from the end using the ZIP signature. In rare cases, it might retrieve false information since the signature might appear out of coincidence. To be accurate, this method has to read all ZIP entries until it finds the last ones because directory entries are variable size in ZIP. @param fs the file system that contains the ZIP archive @param path the path to the ZIP file @param n the number of entries to retrieve from the end @return file names, offsets, and lengths for the last n entries if the ZIP file contains at least n entries. Otherwise, it returns all entries in the file.

### Goal
The `lastNFiles` function retrieves metadata about the last `n` files stored in a ZIP archive, including their names, offsets, and lengths, which is useful for analyzing the contents of ZIP files in geospatial raster processing.

### Parameters
- `fs` (`FileSystem`): The file system that contains the ZIP archive. This can be a local file system or a distributed file system supported by Spark.
- `path` (`Path`): The path to the ZIP file from which the last `n` entries are to be retrieved. This should point to a valid ZIP file in the specified file system.
- `n` (`Int`): The number of entries to retrieve from the end of the ZIP file. This should be a positive integer indicating how many of the last entries are desired.

### Input
The caller must provide a valid `FileSystem` instance, a `Path` pointing to an existing ZIP file, and a positive integer `n`. The ZIP file must contain at least `n` entries for the function to return the expected results.

### Output
Returns `Array[(String, Long, Long)]` — an array of tuples where each tuple contains the name of a file (as a `String`), the offset of the file within the ZIP archive (as a `Long`), and the length of the file (as a `Long`). If the ZIP file contains fewer than `n` entries, the function returns all available entries.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val filePath = new Path(scratchPath, "test1.zip")
val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, filePath, 2)
```

### LLM Instruction Prompt
When calling `lastNFiles`, ensure that the `FileSystem` and `Path` parameters are correctly instantiated and that `n` is a positive integer. Be aware that the method may not always return accurate results due to its reliance on ZIP signatures.

### Prompt Snippet
```text
Retrieve the last n files from a ZIP archive using the lastNFiles function, ensuring the file system and path are correctly specified.
```

### Common Failure Modes
- Providing a `Path` that does not point to a valid ZIP file will result in an error.
- Specifying a negative or zero value for `n` will lead to unexpected behavior or errors.
- If the ZIP file contains fewer entries than `n`, the function will return all available entries, which may not be the intended outcome.

### Fix Code Hint
```scala
// Ensure the path points to a valid ZIP file and n is a positive integer
val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, validZipPath, validN)
```

## API Test: `listFilesInZip`

### Signature
```scala
def listFilesInZip(fileSystem: fs.FileSystem, zipFilePath: Path): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:478_

_Source doc:_ List all files contained in the given ZIP file @param fileSystem the file system that contains the zip file @param zipFilePath the ZIP file to return its contents @return

### Goal
`listFilesInZip` retrieves a list of all files contained within a specified ZIP file, including their names, offsets, and sizes, facilitating the extraction and processing of geospatial data stored in ZIP archives.

### Parameters
- `fileSystem` (`fs.FileSystem`): The file system instance that provides access to the ZIP file. This can be a local file system or a distributed file system like HDFS.
- `zipFilePath` (`Path`): The path to the ZIP file whose contents are to be listed. This should point to a valid ZIP file accessible through the provided file system.

### Input
The caller must provide:
- A valid `fs.FileSystem` instance that can access the ZIP file.
- A `Path` object pointing to an existing ZIP file. The ZIP file must be properly formatted and not corrupted.

### Output
Returns `Array[(String, Long, Long)]` — an array of tuples where each tuple contains:
- The name of the file within the ZIP archive (as a `String`).
- The offset of the file within the ZIP file (as a `Long`).
- The size of the file in bytes (as a `Long`).

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val zipFilePath = new Path("path/to/your/file.zip")
val contents = ZipUtil.listFilesInZip(fileSystem, zipFilePath)
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly initialized and points to a valid file system.
- Verify that the `zipFilePath` points to an existing ZIP file before calling `listFilesInZip`.

### Prompt Snippet
```text
List all files in the specified ZIP file using the provided file system.
```

### Common Failure Modes
- The specified `zipFilePath` does not point to a valid ZIP file, resulting in an error.
- The `fileSystem` is not properly initialized or does not have access to the specified ZIP file, leading to a failure in reading the file.

### Fix Code Hint
```scala
// Ensure the file system is correctly set up and the ZIP file exists before calling the function.
val fileSystem = FileSystem.getLocal(new Configuration())
val zipFilePath = new Path("path/to/your/file.zip")
if (fileSystem.exists(zipFilePath)) {
    val contents = ZipUtil.listFilesInZip(fileSystem, zipFilePath)
} else {
    println("The specified ZIP file does not exist.")
}
```

## API Test: `locateResource`

### Signature
```scala
def locateResource(srcPath: String): File
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:293_

_Source doc:_ Returns the relative or full path to the given resource @param srcPath a path to a resource that starts with "/" @return the path of the file of the given resource

### Goal
`locateResource` retrieves the file path for a specified resource, ensuring that the path is valid and accessible within the context of the RDPro library.

### Parameters
- `srcPath` (`String`): A string representing the path to a resource, which must start with a "/" to be considered valid.

### Input
The caller must provide a valid resource path as a string that begins with "/". This path should point to a resource that is accessible within the environment where the RDPro library is executed.

### Output
Returns `File` — the `File` object representing the path of the specified resource. This path can be either relative or absolute, depending on the resource's location.

### Valid Call Patterns
```scala
val inputfile = locateResource("/test.partitions")
```

### LLM Instruction Prompt
- When calling `locateResource`, ensure that the `srcPath` parameter is a valid string that starts with a "/". The resource must be accessible in the current execution context.

### Prompt Snippet
```text
Locate the resource file using the path provided, ensuring it starts with a "/".
```

### Common Failure Modes
- Providing a `srcPath` that does not start with "/" will result in an invalid path error.
- Attempting to locate a resource that does not exist or is not accessible will lead to a `FileNotFoundException`.

### Fix Code Hint
```scala
// Ensure the srcPath starts with "/" and points to an existing resource.
val inputfile = locateResource("/valid/resource/path")
```

## API Test: `makeBoxes`

### Signature
```scala
def makeBoxes(maxSize: Int*): JavaSpatialGeneratorBuilder
def makeBoxes(maxSize: Double*): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:76  (+1 more definition site/overload)_

_Source doc:_ Generate boxes around each generated point. The size is measured as a fraction [0, 1] to indicate the ratio of the dataset bounding box. Any value above 1.0 is invalid. @param maxSize the maximum size for each side length of the generated box @return this generator builder.

### Goal
`makeBoxes` generates rectangular boxes around each generated point, with the size of the boxes defined as a fraction of the dataset's bounding box.

### Parameters
- `maxSize` (`Double*`): The maximum size for each side length of the generated box, specified as a fraction in the range [0, 1]. Values above 1.0 are considered invalid.

### Input
The caller must provide a valid Spark context and ensure that the spatial data generation process has been initiated. The `maxSize` values must be within the range [0, 1].

### Output
Returns `SpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data with the specified box sizes.

### Valid Call Patterns
```scala
sparkContext.generateSpatialData
      .makeBoxes(0.3, 0.4)
      .uniform(1000000)

sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- When calling `makeBoxes`, ensure that the `maxSize` values are within the valid range [0, 1] and that the spatial data generation context is properly initialized.

### Prompt Snippet
```text
Generate boxes around each generated point using makeBoxes with maxSize values between 0 and 1.
```

### Common Failure Modes
- Providing `maxSize` values greater than 1.0 will result in an invalid argument error.
- Attempting to call `makeBoxes` without first initializing the spatial data generation context will lead to a runtime error.

### Fix Code Hint
```scala
// Ensure maxSize values are within the valid range
val boxes = sparkContext.generateSpatialData.makeBoxes(0.3, 0.4).uniform(1000000)
```

## API Test: `mapPixels`

### Signature
```scala
def mapPixels[U: ClassTag](f: T => U)
def mapPixels[T: ClassTag, U: ClassTag](inputRaster: RasterRDD[T], f: T => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38  (+1 more definition site/overload)_

_Source doc:_ Apply a user-defined function for each pixel in the input raster to produce the output raster @param inputRaster the input raster RDD @param f the function to apply on each input pixel value to produce the output pixel value @tparam T the type of pixels in the input @tparam U the type of pixels in the output @return the resulting RDD

### Goal
`mapPixels` applies a user-defined function to each pixel in the input raster, transforming the pixel values to produce a new raster.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster represented as a distributed collection of raster tiles, where each tile contains pixel values of type `T`.
- `f` (`T => U`): A function that takes a pixel value of type `T` and returns a transformed pixel value of type `U`.

### Input
The caller must provide a `RasterRDD[T]` containing pixel data, which can be loaded from formats such as GeoTIFF or HDF. The function `f` must be compatible with the pixel type `T` of the input raster.

### Output
Returns `RasterRDD[U]` — a new raster represented as a distributed collection of raster tiles, where each tile contains transformed pixel values of type `U`.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
```

### LLM Instruction Prompt
- Ensure that the input raster is of a compatible pixel type and that the function `f` is defined to handle the input pixel type correctly.

### Prompt Snippet
```text
Transform the pixel values of the input raster using a user-defined function with `mapPixels`.
```

### Common Failure Modes
- The function `f` may not handle all possible pixel values, leading to runtime exceptions.
- The input raster may not be properly loaded or may contain incompatible pixel types.

### Fix Code Hint
```scala
Ensure that the function `f` is defined to handle all expected input pixel values and that the input raster is correctly loaded with the appropriate pixel type.
```

## API Test: `mbr`

### Signature
```scala
def mbr : EnvelopeNDLite
def mbr: EnvelopeNDLite
def mbr(mbr: EnvelopeNDLite): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:97  (+2 more definition site/overload)_

_Source doc:_ Generates data in the given bounding box @param mbr the bounding box of the generated data @return

### Goal
The `mbr` function generates spatial data within a specified bounding box, facilitating the creation of raster datasets for geospatial analysis.

### Parameters
- `mbr` (`EnvelopeNDLite`): The bounding box that defines the spatial extent for the generated data. It specifies the minimum and maximum coordinates in N-dimensional space.

### Input
The caller must provide an `EnvelopeNDLite` object that defines the bounding box. This input must be compatible with the spatial data being generated, ensuring that the dimensions and coordinate system align with the intended analysis.

### Output
Returns `SpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data based on the specified bounding box. This object is used to define additional parameters for the data generation process.

### Valid Call Patterns
```scala
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```
```scala
println(sparkContext.generateSpatialData
  .mbr(new EnvelopeNDLite(2, 1.0, 0.0, 4.0, 8.0))
  .uniform(1000)
  .summary)
```

### LLM Instruction Prompt
- When calling `mbr`, ensure that the `EnvelopeNDLite` parameter accurately represents the desired spatial extent for the generated data.

### Prompt Snippet
```text
Generate spatial data within the bounding box defined by EnvelopeNDLite.
```

### Common Failure Modes
- Providing an `EnvelopeNDLite` that does not conform to the expected dimensions or coordinate system may result in runtime errors or unexpected behavior.
- Failing to configure the `SpatialGeneratorBuilder` after calling `mbr` may lead to incomplete or incorrect data generation.

### Fix Code Hint
```scala
// Ensure the EnvelopeNDLite is correctly defined and matches the expected spatial dimensions.
val validMBR = new EnvelopeNDLite(2, 1.0, 0.0, 4.0, 8.0)
val spatialData = new SpatialGeneratorBuilder(sparkContext).mbr(validMBR).uniform(1000)
```

## API Test: `mergeWith`

### Signature
```scala
def mergeWith(another: VectorCanvas): VectorCanvas
def mergeWith(another: MemoryTileWindow[T]): Unit
def mergeWith(opts: BeastOptions): BeastOptions
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:440  (+2 more definition site/overload)_

_Source doc:_ Merges this canvas with another vector canvas and returns this canvas after the merge. @param another the other canvas to merge with @return this canvas after the merge so that you can chain a number of mergeWith operations.

### Goal
Merges the geometries from another `VectorCanvas` into the current canvas, allowing for the combination of vector data in geospatial analyses.

### Parameters
- `another` (`VectorCanvas`): The other vector canvas containing geometries to be merged with the current canvas.

### Input
The caller must provide a `VectorCanvas` instance that contains geometries. The geometries in both canvases should be compatible in terms of spatial reference and data structure.

### Output
Returns `VectorCanvas` — the current canvas after merging, which now includes geometries from the provided `another` canvas.

### Valid Call Patterns
```scala
canvas1.mergeWith(canvas2)
```

### LLM Instruction Prompt
- When calling `mergeWith`, ensure that the `another` parameter is a valid `VectorCanvas` instance containing geometries to be merged.

### Prompt Snippet
```text
canvas1.mergeWith(canvas2)
```

### Common Failure Modes
- Attempting to merge with a `VectorCanvas` that has incompatible geometries or spatial references may lead to unexpected results or runtime errors.

### Fix Code Hint
```scala
// Ensure both canvases have compatible geometries before merging
if (canvas1.envelope.intersects(canvas2.envelope)) {
    canvas1.mergeWith(canvas2)
}
```

## API Test: `mergeZip`

### Signature
```scala
def mergeZip(fileSystem: fs.FileSystem, mergedFile: Path, @varargs zipFiles: Path*): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:425_

_Source doc:_ Merges multiple ZIP files into one and deletes the input files. @param mergedFile the output file that contains the merged ZIP files @param zipFiles the input files to be merged

### Goal
Merges multiple ZIP files into a single ZIP file and deletes the original input ZIP files.

### Parameters
- `fileSystem` (`fs.FileSystem`): The file system instance used to access the files. This can be a local file system or a distributed file system like HDFS.
- `mergedFile` (`Path`): The path where the merged ZIP file will be saved. This should be a valid path in the specified file system.
- `@varargs zipFiles` (`Path*`): A variable number of paths representing the input ZIP files that will be merged. Each path should point to an existing ZIP file.

### Input
The caller must provide:
- Existing ZIP files located at the paths specified in `zipFiles`.
- A valid `fileSystem` instance that can access the specified paths.
- A valid `mergedFile` path where the output ZIP will be stored.

### Output
Returns `Unit` — this indicates that the operation has completed successfully without returning any value. The merged ZIP file will be located at the specified `mergedFile` path.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val mergedFile = new Path(scratchPath, "merged.zip")
ZipUtil.mergeZip(fileSystem, mergedFile, new Path(scratchPath, "file1.zip"), new Path(scratchPath, "file2.zip"))
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly initialized and that the paths provided in `zipFiles` exist before calling `mergeZip`.

### Prompt Snippet
```text
Merge multiple ZIP files into a single ZIP file using the mergeZip function, ensuring that the file system and paths are correctly set up.
```

### Common Failure Modes
- The specified `zipFiles` paths do not exist, leading to a `FileNotFoundException`.
- The `mergedFile` path is invalid or points to a location where the user does not have write permissions, resulting in an `IOException`.
- The `fileSystem` is not properly initialized, causing issues when attempting to access the files.

### Fix Code Hint
```scala
// Ensure all input ZIP files exist and the file system is correctly set up before calling mergeZip.
```

## API Test: `metadata`

### Signature
```scala
override def metadata: RasterMetadata
def metadata: RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:165  (+2 more definition site/overload)_

### Goal
Retrieve the metadata of the raster file, which includes information about its dimensions, pixel scale, and coordinate reference system.

### Parameters
_None._

### Input
The caller must provide a raster file that has been loaded into a `GeoTiffReader` instance. The file must be in GeoTIFF format.

### Output
Returns `RasterMetadata` — an object that contains metadata about the raster, including properties such as raster width, height, pixel scale, and transformation methods for converting between grid and model coordinates.

### Valid Call Patterns
```scala
val rasterPath = new Path(makeFileCopy("/rasters/glc2000_small.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val metadata = reader.metadata
  assert(metadata.rasterWidth == 256)
  assert(metadata.rasterHeight == 128)
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Ensure that the `metadata` method is called on an initialized `GeoTiffReader` instance that has successfully loaded a raster file.

### Prompt Snippet
```text
val metadata = reader.metadata
```

### Common Failure Modes
- Calling `metadata` on a `GeoTiffReader` instance that has not been initialized with a valid raster file will result in an error.
- Attempting to access `metadata` before the raster file is fully loaded may lead to null reference exceptions.

### Fix Code Hint
```scala
// Ensure the GeoTiffReader is properly initialized before calling metadata
val reader = new GeoTiffReader[Int]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
// Now it's safe to call metadata
val metadata = reader.metadata
```

## API Test: `modelToGrid`

### Signature
```scala
def modelToGrid(x: Double, y: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:161_

_Source doc:_ Converts a point location from model (world) space to grid (pixel) space @param x the x-coordinate in the model space (e.g., longitude) @param y the y-coordinate in the model space (e.g., latitude) @param outPoint the output point that contains the grid coordinates

### Goal
The `modelToGrid` function converts geographic coordinates (longitude and latitude) from model (world) space into pixel coordinates in grid (raster) space.

### Parameters
- `x` (`Double`): The x-coordinate in model space, typically representing longitude.
- `y` (`Double`): The y-coordinate in model space, typically representing latitude.
- `outPoint` (`Point2D.Double`): An output parameter that will hold the resulting pixel coordinates after the conversion.

### Input
The caller must provide valid geographic coordinates for `x` and `y`, which should correspond to the coordinate reference system of the raster being processed. The `outPoint` must be an instance of `Point2D.Double` that is initialized before calling the function.

### Output
Returns `Unit` — this indicates that the function does not return a value but instead modifies the `outPoint` parameter to contain the pixel coordinates corresponding to the input model coordinates.

### Valid Call Patterns
```scala
val outPoint = new Point2D.Double
reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)
```

### LLM Instruction Prompt
- When calling `modelToGrid`, ensure that the `outPoint` is a properly initialized `Point2D.Double` instance to store the output coordinates.

### Prompt Snippet
```text
Call `modelToGrid` with valid longitude and latitude values, and ensure `outPoint` is initialized to receive the pixel coordinates.
```

### Common Failure Modes
- Providing `x` and `y` coordinates that do not correspond to the raster's coordinate reference system may result in incorrect pixel coordinates.
- Failing to initialize `outPoint` before passing it to the function will lead to a runtime error.

### Fix Code Hint
```scala
val outPoint = new Point2D.Double // Ensure outPoint is initialized
reader.metadata.modelToGrid(xCoordinate, yCoordinate, outPoint) // Call with valid coordinates
```

## API Test: `name`

### Signature
```scala
override def name(): String
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileSource.scala:93_

### Goal
Retrieve the name of the operation or process being executed within the RDPro framework.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `String` — the name of the operation or process, which is typically used for identification or logging purposes within the RDPro framework.

### Valid Call Patterns
```scala
val operationName: String = someOperationInstance.name()
```

### LLM Instruction Prompt
- Call `name()` on an instance of an operation to retrieve its name.

### Prompt Snippet
```text
Retrieve the name of the current operation using the `name()` method.
```

### Common Failure Modes
- Calling `name()` on an uninitialized or null instance will result in a `NullPointerException`.

### Fix Code Hint
```scala
if (someOperationInstance != null) {
  val operationName: String = someOperationInstance.name()
} else {
  // Handle the null case appropriately
}
```

## API Test: `normal`

### Signature
```scala
def normal(mu: Double, sigma: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:40_

_Source doc:_ Generate a random number in the range (-inf, +inf) from a normal distribution

### Goal
The `normal` function generates a random number from a normal distribution, which can be useful for simulating random processes in geospatial analysis.

### Parameters
- `mu` (`Double`): The mean of the normal distribution. This value represents the center of the distribution and can be any real number.
- `sigma` (`Double`): The standard deviation of the normal distribution. This value must be a positive number, representing the spread or width of the distribution.

### Input
No specific data formats or files are required as input. The caller must provide valid `Double` values for both `mu` and `sigma`, ensuring that `sigma` is greater than zero.

### Output
Returns `Double` — a random number generated from the specified normal distribution characterized by the provided `mu` and `sigma`.

### Valid Call Patterns
```scala
val randomValue: Double = value.normal(0.0, 1.0)
```

### LLM Instruction Prompt
- When calling `normal`, ensure that `mu` is a valid `Double` representing the mean and `sigma` is a positive `Double` representing the standard deviation.

### Prompt Snippet
```text
Generate a random number using the normal distribution with mean and standard deviation.
```

### Common Failure Modes
- Providing a non-positive value for `sigma` will result in an error, as the standard deviation must be greater than zero.
- Passing non-`Double` types for `mu` or `sigma` will lead to a type mismatch error.

### Fix Code Hint
```scala
// Ensure sigma is positive
val mu: Double = 0.0
val sigma: Double = 1.0 // Must be > 0
val randomValue: Double = value.normal(mu, sigma)
```

## API Test: `numFeatures`

### Signature
```scala
def numFeatures: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:32_

_Source doc:_ Total number of features (records) in this partition

### Goal
`numFeatures` retrieves the total count of features (records) present in the current partition of the dataset.

### Parameters
_None._

### Input
The caller must ensure that the dataset has been properly loaded and partitioned. This typically involves using a method such as `sc.geoTiff(...)` or similar to load raster data into an appropriate RDD.

### Output
Returns `Long` — the total number of features (records) in the current partition, which represents the count of individual geometries or data entries processed.

### Valid Call Patterns
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
assert(summary.numFeatures == 44)
```

### LLM Instruction Prompt
- Ensure that the dataset is loaded and partitioned before calling `numFeatures`. The method should be called on an instance of a class that contains the partitioned data.

### Prompt Snippet
```text
To get the number of features in the current partition, call `summary.numFeatures`.
```

### Common Failure Modes
- Calling `numFeatures` on an uninitialized or improperly loaded dataset may result in a runtime error.
- If the dataset is empty or not partitioned correctly, the method may return `0`, which could be misleading if the dataset was expected to contain features.

### Fix Code Hint
```scala
// Ensure the dataset is loaded and partitioned correctly before calling numFeatures
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)").set("skipheader", true).set("separator", "\t")
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
val featureCount = summary.numFeatures // This should return the correct count of features
```

## API Test: `numFields`

### Signature
```scala
def numFields: Int
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42_

_Source doc:_ Number of attributes in the file

### Goal
`numFields` retrieves the number of attributes present in a given file, which is essential for understanding the structure of the data being processed in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a valid file that has been read into an appropriate object that supports the `numFields` method. This typically involves loading a shapefile or similar data format that contains attributes.

### Output
Returns `Int` — the number of attributes in the file, which indicates how many distinct pieces of information are available for each record in the dataset.

### Valid Call Patterns
```scala
val input = getClass.getResourceAsStream("/001005279.gpx")
val gpxReader = new GPXReader2(input, "001005279.gpx")
val attributeCount = gpxReader.numFields
```

### LLM Instruction Prompt
- Ensure that the object on which `numFields` is called has been properly initialized and contains data. The method should only be called on objects that represent files with attributes.

### Prompt Snippet
```text
To get the number of attributes in the file, use the `numFields` method on the initialized reader object.
```

### Common Failure Modes
- Calling `numFields` on an uninitialized or improperly loaded object may result in a runtime error.
- If the file does not contain any attributes, `numFields` may return zero, which could lead to confusion if the user expects attributes to be present.

### Fix Code Hint
```scala
// Ensure the file is loaded correctly before calling numFields
val gpxReader = new GPXReader2(input, "001005279.gpx")
if (gpxReader != null) {
  val attributeCount = gpxReader.numFields
} else {
  throw new IllegalArgumentException("The GPXReader2 object is not initialized.")
}
```

## API Test: `numNonEmptyGeometries`

### Signature
```scala
def numNonEmptyGeometries: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:35_

_Source doc:_ Number of non-empty geometries in this partition

### Goal
`numNonEmptyGeometries` computes the count of non-empty geometries present in the current partition of spatial data.

### Parameters
_None._

### Input
The function operates on a `SpatialPartition` object that must be initialized and populated with geometries. There are no specific file formats required as input since this method is called on an existing object.

### Output
Returns `Long` — the value represents the total number of non-empty geometries in the partition.

### Valid Call Patterns
```scala
val count: Long = spatialPartition.numNonEmptyGeometries
```

### LLM Instruction Prompt
- Ensure that the `numNonEmptyGeometries` method is called on a valid `SpatialPartition` instance that contains geometries.

### Prompt Snippet
```text
To get the number of non-empty geometries in a spatial partition, use the method `numNonEmptyGeometries` on your `SpatialPartition` object.
```

### Common Failure Modes
- Calling `numNonEmptyGeometries` on a `SpatialPartition` that has not been properly initialized or populated with geometries may lead to unexpected results or errors.

### Fix Code Hint
```scala
// Ensure the SpatialPartition is properly initialized and contains geometries before calling numNonEmptyGeometries
val spatialPartition = new SpatialPartition(...) // Initialize with appropriate geometries
val count: Long = spatialPartition.numNonEmptyGeometries
```

## API Test: `numPartitions`

### Signature
```scala
def numPartitions(num: Int): JavaSpatialGeneratorBuilder
def numPartitions(num: Int): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:66  (+1 more definition site/overload)_

_Source doc:_ Set the number of partitions in the output. If not set or set to zero, one partition will be generated for each one million records @param num the number of partitions in the generated RDD @return

### Goal
The `numPartitions` function sets the number of partitions for the output RDD in a distributed raster processing workflow, optimizing performance for large-scale geospatial analysis.

### Parameters
- `num` (`Int`): The desired number of partitions for the generated RDD. If set to zero or not specified, the default behavior creates one partition for every one million records.

### Input
The caller must provide a valid `num` parameter as an integer. There are no specific file formats required for this function, but it is typically used in the context of an existing spatial dataset that has been loaded into an RDD.

### Output
Returns `JavaSpatialGeneratorBuilder` — an instance of `JavaSpatialGeneratorBuilder` that allows further configuration of the spatial data processing pipeline, specifically regarding how the data will be partitioned for distributed processing.

### Valid Call Patterns
```scala
val partitioner = someSpatialGeneratorBuilder.numPartitions(16)
```

### LLM Instruction Prompt
- When calling `numPartitions`, ensure that the `num` parameter is a positive integer representing the desired number of partitions. If the value is zero or omitted, the default partitioning behavior will apply.

### Prompt Snippet
```text
Set the number of partitions for the output RDD using the numPartitions method, ensuring that the num parameter is a positive integer.
```

### Common Failure Modes
- Providing a negative integer or non-integer value for the `num` parameter will result in an error.
- If the function is called on an uninitialized or improperly configured spatial generator, it may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure that the num parameter is a positive integer before calling numPartitions
val numPartitionsValue = 16 // Example value
if (numPartitionsValue > 0) {
    val partitioner = someSpatialGeneratorBuilder.numPartitions(numPartitionsValue)
} else {
    throw new IllegalArgumentException("Number of partitions must be a positive integer.")
}
```

## API Test: `numPoints`

### Signature
```scala
def numPoints: Int
override def numPoints: Int
def numPoints: Long
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:22  (+4 more definition site/overload)_

### Goal
`numPoints` calculates the total number of points across all geometries, which is useful for understanding the complexity and size of geometric data in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide geometries that have been created and simplified using the RDPro library. The geometries should be valid instances of geometric types (e.g., `LineString`, `Polygon`) that support the `numPoints` method.

### Output
Returns `Int` — the total number of points in the geometries, representing the count of individual coordinate points that make up the geometries.

### Valid Call Patterns
```scala
val interTile = new IntermediateVectorTile(10, 0)
var line = GeometryReader.DefaultGeometryFactory.createLineString(Array(
  new Coordinate(5, 5), new Coordinate(-5, 5), new Coordinate(-5, 6), new Coordinate(-5, 7),
  new Coordinate(-5, 15), new Coordinate(5, 8),
))
val numPoints = line.numPoints
```

### LLM Instruction Prompt
- When calling `numPoints`, ensure that the geometry instance is valid and has been created using the appropriate RDPro methods. The geometry must not be null and should represent a valid shape.

### Prompt Snippet
```text
To get the number of points in a geometry, use the `numPoints` method on a valid geometry instance created with RDPro.
```

### Common Failure Modes
- Calling `numPoints` on a null geometry will result in a `NullPointerException`.
- Attempting to call `numPoints` on a geometry that does not support this method (e.g., a non-geometric object) will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the geometry is not null and is of a valid type before calling numPoints
if (line != null) {
  val count = line.numPoints
} else {
  println("Geometry is null, cannot compute number of points.")
}
```

## API Test: `numTiles`

### Signature
```scala
def numTiles: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:61_

_Source doc:_ Total number of tiles in the raster layer

### Goal
`numTiles` retrieves the total number of tiles that comprise the raster layer, which is essential for understanding the structure of the raster data in large-scale geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster layer that has been loaded into the RDPro framework, typically from a GeoTIFF or HDF file format. The raster must be properly initialized and accessible within the Spark context.

### Output
Returns `Int` — the total number of tiles in the raster layer, representing how the raster data is partitioned for processing.

### Valid Call Patterns
```scala
val numTilesCount: Int = raster.metadata.numTiles
```

### LLM Instruction Prompt
- Ensure that the raster layer is properly initialized and accessible before calling `numTiles`. The raster must be loaded using supported formats like GeoTIFF or HDF.

### Prompt Snippet
```text
To get the total number of tiles in a raster layer, use the `numTiles` method on the raster's metadata.
```

### Common Failure Modes
- Calling `numTiles` on an uninitialized or improperly loaded raster layer will result in a runtime error.
- Attempting to call `numTiles` on a non-raster object will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling numTiles
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val numTilesCount: Int = raster.metadata.numTiles
```

## API Test: `overlay`

### Signature
```scala
def overlay[V](rasters: RasterRDD[T]*)
def overlay[T: ClassTag, V](@varargs inputs: RDD[ITile[T]]*)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96  (+1 more definition site/overload)_

_Source doc:_ Overlays this raster RDD on top other ones @param rasters the other rasters to stack this raster on @return a new RasterRDD which contains the stack of this raster on top of the given ones

### Goal
The `overlay` function stacks one or more raster datasets on top of each other, allowing for combined analysis of geospatial data.

### Parameters
- `rasters` (`RasterRDD[T]*`): One or more raster datasets that will be stacked on top of the calling raster dataset. Each raster must be of the same pixel type.

### Input
The caller must provide raster datasets in the form of `RasterRDD[T]`, which can be loaded from formats such as GeoTIFF. All input rasters should have compatible dimensions and coordinate reference systems (CRS) to ensure proper overlay.

### Output
Returns a new `RasterRDD[Array[T]]`, which represents the stacked raster data. The output format is a raster dataset that contains the pixel values from the calling raster and the provided rasters.

### Valid Call Patterns
```scala
val raster1: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val raster2: RasterRDD[Int] = sc.geoTiff[Int]("vegetation")
val stacked: RasterRDD[Array[Int]] = raster1.overlay(raster2)
```

### LLM Instruction Prompt
- When calling `overlay`, ensure that all input rasters are of the same pixel type and have compatible dimensions and CRS.

### Prompt Snippet
```text
Use the `overlay` function to stack multiple raster datasets for combined analysis.
```

### Common Failure Modes
- Attempting to overlay rasters with different pixel types or incompatible dimensions will result in runtime errors.
- If the input rasters do not share the same CRS, the overlay operation may produce unexpected results or fail.

### Fix Code Hint
```scala
Ensure all input rasters are of the same pixel type and have matching dimensions and CRS before calling `overlay`.
```

## API Test: `parcel`

### Signature
```scala
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): JavaSpatialRDD
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:153  (+1 more definition site/overload)_

_Source doc:_ Generates boxes from the parcel distribution @param cardinality the number of records to generate @param dither the amount of randomization to add to each generated box @param splitRange the range of splitting each box @return the RDD that contains the generated data

### Goal
The `parcel` function generates a specified number of spatial boxes based on a parcel distribution, which can be used for various geospatial analyses.

### Parameters
- `cardinality` (`Long`): The number of spatial boxes (records) to generate. This value should be a positive integer representing how many boxes you want in the output.
- `dither` (`Double`), default `0.2`: The amount of randomization to apply to each generated box. This value should be between `0.0` and `1.0`, where higher values introduce more randomness in the box placement.
- `splitRange` (`Double`), default `0.2`: The range within which each box can be split. This value should be a positive number that determines how much variability is allowed in the dimensions of the generated boxes.

### Input
The caller must provide a valid Spark context and ensure that the `generateSpatialData` method is called prior to invoking `parcel`. The input must be compatible with the spatial data generation process.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial boxes, which can be used for further geospatial processing or analysis.

### Valid Call Patterns
```scala
val parcels: SpatialRDD = sc.generateSpatialData
      .parcel(1000000, dither = 0.1, splitRange = 0.4)

sc.generateSpatialData
  .parcel(100, dither = 0.2, splitRange = 0.3)
  .plotImage(300, 300, "parcel.png")
```

### LLM Instruction Prompt
- When calling `parcel`, ensure that the `cardinality` is a positive integer, and both `dither` and `splitRange` are set to appropriate values within their expected ranges.

### Prompt Snippet
```text
Generate spatial boxes using the parcel function with a specified cardinality, dither, and splitRange.
```

### Common Failure Modes
- Providing a negative or zero value for `cardinality` will result in an error, as it must be a positive integer.
- Setting `dither` or `splitRange` to values outside their expected ranges may lead to unexpected behavior or errors during box generation.

### Fix Code Hint
```scala
// Ensure cardinality is a positive integer
val parcels: SpatialRDD = sc.generateSpatialData.parcel(1000) // Correct usage
```

## API Test: `part`

### Signature
```scala
def part(i: Int): LiteList
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146_

### Goal
The `part` function retrieves a specific part of a geometric object, returning it as a `LiteList`.

### Parameters
- `i` (`Int`): The index of the part to retrieve. This should be a non-negative integer representing the desired part's position within the geometric structure.

### Input
The caller must provide a valid index `i` that corresponds to an existing part of the geometric object. The geometric object must be instantiated and accessible in the context where `part` is called.

### Output
Returns `LiteList` — a lightweight representation of the specified part of the geometric object, which can be used for further processing or analysis.

### Valid Call Patterns
```scala
val partList = geometry.part(0) // Assuming 'geometry' is an instance of a class that has the 'part' method.
```

### LLM Instruction Prompt
- Ensure that the index `i` is within the valid range of parts for the geometric object. If `i` is out of bounds, handle the error appropriately.

### Prompt Snippet
```text
Retrieve a specific part of the geometric object using the part method, ensuring the index is valid.
```

### Common Failure Modes
- Calling `part` with an index `i` that is negative or exceeds the number of available parts in the geometric object will result in an error or unexpected behavior.

### Fix Code Hint
```scala
if (i < 0 || i >= geometry.numParts) {
  throw new IllegalArgumentException("Index i must be within the range of available parts.")
}
```

## API Test: `partitionBy`

### Signature
```scala
def partitionBy(spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionBy(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): PartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:35  (+1 more definition site/overload)_

### Goal
The `partitionBy` function partitions a spatial RDD using a specified spatial partitioner, optimizing the distribution of spatial data across the partitions for efficient processing.

### Parameters
- `spatialPartitioner` (`SpatialPartitioner`): An instance of a spatial partitioner that defines how the spatial data should be divided into partitions. This can include various partitioning strategies such as grid or quad-tree partitioning.

### Input
The caller must provide a `SpatialRDD` that has been previously loaded with spatial data, such as from a shapefile or CSV point data. The input data must be compatible with the spatial partitioning strategy defined by the `spatialPartitioner`.

### Output
Returns `PartitionedSpatialRDD` — a partitioned version of the original spatial RDD, which allows for optimized spatial queries and operations. The output is structured to facilitate efficient processing of spatial data in distributed environments.

### Valid Call Patterns
```scala
// Example of using partitionBy with a spatial partitioner
val testFile = makeFileCopy("/test111.points")
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.partitionBy(gridPartitioner)
assertResult(4)(partitionedData.getNumPartitions)
```

### LLM Instruction Prompt
- When calling `partitionBy`, ensure that the input is a valid `SpatialRDD` and that the `spatialPartitioner` is appropriately defined for the data being processed.

### Prompt Snippet
```text
val partitionedData = data.partitionBy(new GridPartitioner(mbr, Array(2, 2)))
```

### Common Failure Modes
- Attempting to call `partitionBy` on an RDD that is not a `SpatialRDD` will result in a type mismatch error.
- Using an incompatible `SpatialPartitioner` that does not align with the spatial characteristics of the input data may lead to inefficient partitioning or runtime errors.

### Fix Code Hint
```scala
// Ensure the input RDD is a SpatialRDD and the partitioner is suitable for the data
val partitionedData = data.partitionBy(new GridPartitioner(mbr, Array(2, 2)))
```

## API Test: `partitionFeatures`

### Signature
```scala
def partitionFeatures(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaPairRDD[Integer, IFeature]
def partitionFeatures(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaPartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:413  (+3 more definition site/overload)_

### Goal
Partitions the given features using an already initialized `SpatialPartitioner`, enabling efficient spatial queries and operations on the dataset.

### Parameters
- `features` (`SpatialRDD`): The spatial features to be partitioned, which should be in the form of a distributed dataset containing geometrical data.
- `spatialPartitioner` (`SpatialPartitioner`): An instance of a spatial partitioner that defines how the features will be divided into partitions based on their spatial characteristics.

### Input
The caller must provide a `SpatialRDD` containing spatial features, and a `SpatialPartitioner` that has been initialized appropriately. The features should be compatible with the partitioning strategy defined by the spatial partitioner.

### Output
Returns `PartitionedSpatialRDD` — a distributed dataset of spatial features that have been partitioned according to the specified spatial partitioner, allowing for optimized spatial operations.

### Valid Call Patterns
```scala
val geometryFactor: GeometryFactory = FeatureReader.DefaultGeometryFactory
val features = sparkContext.parallelize(Seq[IFeature](
  Feature.create(null, new PointND(geometryFactor, 2, 0, 0)),
  Feature.create(null, new PointND(geometryFactor, 2, 1, 1)),
  Feature.create(null, new PointND(geometryFactor, 2, 3, 1)),
  Feature.create(null, new PointND(geometryFactor, 2, 1, 4))
))
val partitionedFeatures: PartitionedSpatialRDD = IndexHelper.partitionFeatures(features, new RSGrovePartitioner())
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` and that the `spatialPartitioner` is properly initialized before calling `partitionFeatures`.

### Prompt Snippet
```text
To partition spatial features, use the `partitionFeatures` method with a valid `SpatialRDD` and an initialized `SpatialPartitioner`.
```

### Common Failure Modes
- Providing a `SpatialRDD` that is empty or not properly initialized.
- Using an uninitialized or incompatible `SpatialPartitioner`, which may lead to runtime errors or incorrect partitioning.

### Fix Code Hint
```scala
// Ensure the features RDD is properly initialized and the spatial partitioner is set up correctly.
val partitionedFeatures = IndexHelper.partitionFeatures(features, new RSGrovePartitioner())
```

## API Test: `partitionFeatures2`

### Signature
```scala
def partitionFeatures2(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaSpatialRDD
def partitionFeatures2(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:429  (+3 more definition site/overload)_

_Source doc:_ Partitions the given features using a partitioner of the given type. This method first initializes the partitioner and then uses this initialized partitioner to partition the data. @param features the set of features to spatially partition @param partitionerClass the type of the spatial partition @param sizeFunction the function used to computed the size @param opts additional options @return the same set of input features after they are partitioned.

### Goal
`partitionFeatures2` partitions a set of spatial features into distinct spatial regions using a specified partitioning strategy, optimizing data distribution for parallel processing in geospatial analyses.

### Parameters
- `features` (`SpatialRDD`): The set of spatial features that need to be partitioned. This should be a distributed collection of geospatial data that can be processed in parallel.
- `partitionerClass` (`Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int`): The class type of the spatial partitioner to be used for partitioning the features, along with a function that computes the size of each feature, which helps in determining how to distribute the features across partitions.
- `opts` (`BeastOptions`): Additional options that can be used to customize the partitioning process, such as configuration settings that affect the behavior of the partitioner.

### Input
The caller must provide a `SpatialRDD` containing spatial features, a valid partitioner class that extends `SpatialPartitioner`, a size function that takes an `IFeature` and returns an integer, and a `BeastOptions` instance for any additional configurations. The input features should be compatible with the specified partitioner.

### Output
Returns `SpatialRDD` — a partitioned set of spatial features, where the features are distributed across partitions based on the specified partitioning strategy. The output maintains the same format as the input `SpatialRDD`.

### Valid Call Patterns
```scala
val dataset = new RandomSpatialRDD(sparkContext, UniformDistribution, 10000, opts = Seq("maxSize" -> "0.1,0.1", "geometry" -> "box"))
val partitionedFeatures: SpatialRDD = IndexHelper.partitionFeatures2(dataset, new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` and that the `partitionerClass` is a subclass of `SpatialPartitioner`. The `sizeFunction` must be a valid function that computes the size of each feature.

### Prompt Snippet
```text
Use the `partitionFeatures2` function to partition a `SpatialRDD` of features using a specified `SpatialPartitioner` class and a size function.
```

### Common Failure Modes
- Providing a `features` parameter that is not a `SpatialRDD` will result in a type mismatch error.
- Using a `partitionerClass` that does not extend `SpatialPartitioner` will lead to a runtime exception.
- If the `sizeFunction` does not correctly compute the size of the features, it may lead to inefficient partitioning or runtime errors.

### Fix Code Hint
```scala
// Ensure that the features are a valid SpatialRDD and the partitioner class is correctly specified.
val partitionedFeatures: SpatialRDD = IndexHelper.partitionFeatures2(features, new MyCustomPartitioner(), feature => feature.getSize(), new BeastOptions())
```

## API Test: `path`

### Signature
```scala
override def path(): String
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/kmlv2/KMLFormat.scala:49  (+2 more definition site/overload)_

### Goal
Retrieve the file path associated with the current instance, which is useful for understanding the source of the data being processed.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `String` — the file path as a string, representing the location of the data source in the file system.

### Valid Call Patterns
```scala
value.path()
```

### LLM Instruction Prompt
- Call `path()` on an instance of the relevant class to obtain the file path.

### Prompt Snippet
```text
Retrieve the file path of the current instance using the `path()` method.
```

### Common Failure Modes
- Calling `path()` on an uninitialized or null instance may result in a `NullPointerException`.

### Fix Code Hint
```scala
if (instance != null) {
  val filePath = instance.path()
} else {
  // Handle the null case appropriately
}
```

## API Test: `pixelLocations`

### Signature
```scala
def pixelLocations: Iterator[(Int, Int)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:81_

_Source doc:_ An iterator that goes over all pixels in this tile @return an iterator that goes over all pixels (whether empty or not) in this tile

### Goal
`pixelLocations` provides an iterator over the pixel coordinates of a raster tile, allowing users to access each pixel's position for further processing or analysis.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into memory. This tile should be part of a raster dataset, typically loaded using methods like `sc.geoTiff(...)`.

### Output
Returns `Iterator[(Int, Int)]` — an iterator of tuples where each tuple represents the (x, y) coordinates of a pixel in the tile, regardless of whether the pixel is defined or empty.

### Valid Call Patterns
```scala
for ((x, y) <- tile.pixelLocations) {
  // Process each pixel's coordinates
}
```

### LLM Instruction Prompt
- When calling `pixelLocations`, ensure that the tile object is properly initialized and contains pixel data. The method should be called on an instance of a tile that has been read from a raster dataset.

### Prompt Snippet
```text
To iterate over the pixel locations of a raster tile, use the `pixelLocations` method on the tile instance. Ensure the tile is loaded and initialized correctly before calling this method.
```

### Common Failure Modes
- Attempting to call `pixelLocations` on a null or uninitialized tile object will result in a `NullPointerException`.
- If the tile does not contain any pixels (e.g., it is empty), the iterator will still return, but the processing logic should handle the absence of defined pixels appropriately.

### Fix Code Hint
```scala
// Ensure the tile is initialized before calling pixelLocations
if (tile != null) {
  for ((x, y) <- tile.pixelLocations) {
    // Process pixel coordinates
  }
} else {
  println("Tile is not initialized.")
}
```

## API Test: `pixelType`

### Signature
```scala
def pixelType: DataType
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138_

_Source doc:_ Returns the type of the pixel as an SQL data type @return the type of the pixel values

### Goal
The `pixelType` method retrieves the SQL data type of the pixel values contained within a raster tile, which is essential for understanding the data type when performing geospatial analyses.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into an appropriate RDD format, such as `RDD[ITile[T]]`, where `T` is the pixel type (e.g., `Int`, `Float`). The raster must be properly initialized and contain pixel data.

### Output
Returns `DataType` — this value represents the SQL data type of the pixel values, which can be used for type-checking and ensuring compatibility in further processing steps.

### Valid Call Patterns
```scala
val readRaster = new RasterFileRDD(sparkContext, "sample.tif", new BeastOptions())
val pixelDataType = readRaster.pixelType
```

### LLM Instruction Prompt
- When calling `pixelType`, ensure that the raster data has been properly loaded and initialized. The method should be called on an instance of `RasterFileRDD` or a similar raster data structure.

### Prompt Snippet
```text
Retrieve the pixel type of the raster data using the pixelType method on the loaded RasterFileRDD instance.
```

### Common Failure Modes
- Calling `pixelType` on an uninitialized or empty raster tile will result in a runtime error.
- If the raster data is not loaded correctly (e.g., incorrect file path or unsupported format), the method may not return a valid `DataType`.

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and contains valid pixel data before calling pixelType. For example:
val readRaster = new RasterFileRDD(sparkContext, "valid_file_path.tif", new BeastOptions())
val pixelDataType = readRaster.pixelType
```

## API Test: `pixels`

### Signature
```scala
def pixels: Iterator[(Int, Int, T)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84_

### Goal
The `pixels` method retrieves an iterator over the pixel values of a raster tile, providing the pixel's coordinates along with its value.

### Parameters
_None._

### Input
The method operates on a raster tile that has been previously loaded into an `ITile` object. The input raster must be compatible with the expected pixel type `T`, which should be defined when the raster is loaded.

### Output
Returns `Iterator[(Int, Int, T)]` — each element of the iterator is a tuple containing the pixel's x-coordinate (Int), y-coordinate (Int), and the pixel value (T) at that coordinate.

### Valid Call Patterns
```scala
val pixelIterator: Iterator[(Int, Int, Int)] = rasterTile.pixels
```

### LLM Instruction Prompt
- Ensure that the raster tile is properly initialized and contains pixel data before calling `pixels`. The pixel type `T` must match the type used when loading the raster.

### Prompt Snippet
```text
Retrieve pixel values from a raster tile using the `pixels` method to iterate over each pixel's coordinates and values.
```

### Common Failure Modes
- Calling `pixels` on an uninitialized or empty raster tile will result in an error.
- Mismatched pixel types when loading the raster may lead to runtime exceptions when accessing pixel values.

### Fix Code Hint
```scala
// Ensure the raster tile is properly loaded and initialized before calling pixels
val rasterTile: ITile[Int] = sc.geoTiff("path_to_raster.tif")
val pixelIterator: Iterator[(Int, Int, Int)] = rasterTile.pixels
```

## API Test: `plot`

### Signature
```scala
override def plot(layer: Canvas, feature: IFeature): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SVGPlotter.scala:62_

### Goal
The `plot` function is used to render a given feature onto a specified canvas in the context of geospatial visualization.

### Parameters
- `layer` (`Canvas`): Represents the drawing surface where the feature will be rendered. It is expected to be an instance of the `Canvas` class that can handle graphical output.
- `feature` (`IFeature`): Represents the geospatial feature to be plotted. It is expected to be an instance of the `IFeature` interface, which encapsulates the geometry and associated attributes of the feature.

### Input
The caller must provide:
- A valid `Canvas` instance that is properly initialized for rendering.
- A valid `IFeature` instance that contains the geometry and attributes to be visualized.

### Output
Returns `Boolean` — `true` if the plotting operation was successful, and `false` otherwise.

### Valid Call Patterns
```scala
val plotter = new SVGPlotter
val canvas: Canvas = new Canvas() // Assume this is properly initialized
val feature: IFeature = Feature.create(null, new PointND(new GeometryFactory, 2, 0, 0)) // Example feature
val result: Boolean = plotter.plot(canvas, feature)
```

### LLM Instruction Prompt
- When calling `plot`, ensure that the `layer` is a properly initialized `Canvas` and the `feature` is a valid `IFeature` instance. Check for successful rendering by evaluating the returned Boolean value.

### Prompt Snippet
```text
To visualize a geospatial feature, use the `plot` method of the `SVGPlotter` class, providing a valid `Canvas` and an `IFeature` instance.
```

### Common Failure Modes
- Providing a `null` or uninitialized `Canvas` will result in a failure to plot.
- Providing a `null` or invalid `IFeature` may lead to exceptions or a return value of `false`.

### Fix Code Hint
```scala
// Ensure both layer and feature are properly initialized before calling plot
val canvas: Canvas = new Canvas() // Initialize your canvas
val feature: IFeature = Feature.create(null, new PointND(new GeometryFactory, 2, 0, 0)) // Create a valid feature
val result: Boolean = plotter.plot(canvas, feature) // Call plot with valid parameters
```

## API Test: `plotAllTiles`

### Signature
```scala
def plotAllTiles(features: SpatialDataTypes.JavaSpatialRDD, minLevel: Int, maxLevel: Int, resolution: Int, buffer: Int, opts: BeastOptions): JavaPairRDD[java.lang.Long, IntermediateVectorTile]
def plotAllTiles(features: SpatialDataTypes.SpatialRDD, levels: Range, resolution: Int, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): RDD[(Long, IntermediateVectorTile)]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:170  (+1 more definition site/overload)_

_Source doc:_ Plots all tiles in a range of Zoom levels according to the provided specifications and configuration @param features   the set of features to visualize @param minLevel   the minimum level to visualize (inclusive) @param maxLevel   the maximum level to visualize (inclusive) @param resolution the resolution of each tile @param buffer     the buffer around each tile to consider when visualizing @param opts       additional options for generating the tiles @return an RDD that contains all the generated tiles along with their IDs.

### Goal
`plotAllTiles` generates and visualizes vector tiles for a specified range of zoom levels based on the provided spatial features and configuration options.

### Parameters
- `features` (`SpatialDataTypes.JavaSpatialRDD`): The set of spatial features to visualize, typically loaded from a shapefile or other spatial data source.
- `minLevel` (`Int`): The minimum zoom level to visualize (inclusive), which determines the coarseness of the tiles.
- `maxLevel` (`Int`): The maximum zoom level to visualize (inclusive), which determines the fineness of the tiles.
- `resolution` (`Int`): The resolution of each tile, which affects the detail level of the visualized features.
- `buffer` (`Int`): The buffer around each tile to consider when visualizing, allowing for additional context around the features.
- `opts` (`BeastOptions`): Additional options for generating the tiles, such as thresholds or styling parameters.

### Input
The caller must provide a `SpatialDataTypes.JavaSpatialRDD` containing spatial features, along with integer values for `minLevel`, `maxLevel`, `resolution`, and `buffer`. The `opts` parameter should be an instance of `BeastOptions` that may include specific visualization settings.

### Output
Returns `JavaPairRDD[java.lang.Long, IntermediateVectorTile]` — an RDD containing the generated vector tiles along with their unique IDs, which can be used for further processing or visualization.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, minLevel = 0, maxLevel = 6, resolution = 256, buffer = 5, opts)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialDataTypes.JavaSpatialRDD` and that the zoom levels (`minLevel` and `maxLevel`) are within a reasonable range to avoid excessive tile generation.

### Prompt Snippet
```text
Generate vector tiles using the `plotAllTiles` function with the specified features and configuration options.
```

### Common Failure Modes
- Providing an invalid `features` type that is not a `SpatialDataTypes.JavaSpatialRDD` will result in a type mismatch error.
- Setting `minLevel` greater than `maxLevel` will lead to an invalid range error.
- Using a `resolution` that is too high or too low may result in performance issues or tiles that do not render correctly.

### Fix Code Hint
```scala
// Ensure that the features are loaded correctly and that minLevel is less than or equal to maxLevel
val features: SpatialDataTypes.JavaSpatialRDD = sparkContext.shapefile("path_to_your_shapefile.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, minLevel = 0, maxLevel = 6, resolution = 256, buffer = 5, opts)
```

## API Test: `plotFeatures`

### Signature
```scala
def plotFeatures(features: SpatialDataTypes.SpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], canvasMBR: EnvelopeNDLite = null, opts: BeastOptions = new BeastOptions()): Unit
def plotFeatures(features: JavaSpatialRDD, minLevel: Int, maxLevel: Int, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
def plotFeatures(features: SpatialRDD, levels: Range, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SingleLevelPlot.scala:58  (+2 more definition site/overload)_

_Source doc:_ Plots a set of features to a single image. By default, the aspect ratio of the input is maintained and the given dimensions are treated as upper bounds for image width and height, i.e., the produced image might have smaller dimensions. Also, by default, the extents of the canvas will be equal to the input data. This means that the plotted image will occupy the largest portion of the image. If you wish to visualize only a subset of the data or visualize the data on a small portion of the image, you can specify the [[canvasMBR]] parameter. @param features the set of features to plot @param imageWidth the width of the image in pixels @param imageHeight the height of the image in pixels. @param imagePath the path to which the image will be written @param plotterClass the class of the plotter to use for producing the image @param canvasMBR (Optional) the extents of the data (minimum bounding rectangle) @param opts (Optional) additional options to use with the plotter, e.g., colors

### Goal
`plotFeatures` generates a visual representation of spatial features by plotting them onto a specified image, allowing for customization of the output dimensions and appearance.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): A distributed collection of spatial features that will be plotted onto the image. This should contain geometries such as points, lines, or polygons.
- `imageWidth` (`Int`): The maximum width of the output image in pixels. The actual width may be smaller to maintain the aspect ratio.
- `imageHeight` (`Int`): The maximum height of the output image in pixels. The actual height may be smaller to maintain the aspect ratio.
- `imagePath` (`String`): The file path where the generated image will be saved. This should be a valid path for writing image files.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter]`: The class of the plotter to use for rendering the features. By default, it uses `GeometricPlotter`, but other plotter implementations can be specified for different visual styles.

### Input
The caller must provide a `SpatialRDD` containing the spatial features to be plotted, along with valid integer values for `imageWidth` and `imageHeight`. The `imagePath` must be a writable path on the filesystem. The `plotterClass` can be customized, but defaults to `GeometricPlotter`.

### Output
Returns `Unit` — this indicates that the function performs an action (plotting the features) without returning a value. The output is an image file saved at the specified `imagePath`.

### Valid Call Patterns
```scala
val counties = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_county.zip", "shapefile")
MultilevelPlot.plotFeatures(counties, 800, 600, "counties_plot.png", classOf[GeometricPlotter])
```

### LLM Instruction Prompt
- When calling `plotFeatures`, ensure that the `features` parameter is a valid `SpatialRDD` and that the `imageWidth` and `imageHeight` are positive integers. The `imagePath` must be a valid writable path.

### Prompt Snippet
```text
To visualize spatial features, use the `plotFeatures` method with a valid `SpatialRDD`, specify the desired image dimensions, and provide a path for the output image.
```

### Common Failure Modes
- Providing an invalid or non-writable `imagePath` will result in an error when attempting to save the image.
- Specifying negative or zero values for `imageWidth` or `imageHeight` will lead to runtime exceptions.
- Using a `features` parameter that is not a valid `SpatialRDD` will cause the function to fail.

### Fix Code Hint
```scala
// Ensure the image path is valid and writable
val validPath = "output/image_path.png"
MultilevelPlot.plotFeatures(counties, 800, 600, validPath)
```

## API Test: `plotImage`

### Signature
```scala
def plotImage(imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter], opts: BeastOptions): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, opts: BeastOptions): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:239  (+3 more definition site/overload)_

_Source doc:_ Plots the features to an image using the given plotter @param imageWidth the width of the image in pixels @param imageHeight the height of the image in pixels @param imagePath the path to write the generated image @param plotterClass the plotter class @param opts additional user options

### Goal
`plotImage` generates a visual representation of spatial features by plotting them to an image file using a specified plotting class.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial features that will be plotted. This should contain the geometries and attributes of the features to visualize.
- `imageWidth` (`Int`): The width of the output image in pixels. This determines the horizontal resolution of the generated image.
- `imageHeight` (`Int`): The height of the output image in pixels. This determines the vertical resolution of the generated image.
- `imagePath` (`String`): The file path where the generated image will be saved. This should include the desired file name and extension (e.g., ".png").
- `plotterClass` (`Class[_ <: Plotter]`): The class of the plotter to use for rendering the image. Defaults to `GeometricPlotter`, which is suitable for general geometric features. The user can specify a different plotter class if needed.
- `opts` (`BeastOptions`): Additional user options that can modify the behavior of the plotting process. This allows for customization of the output.

### Input
The caller must provide a valid `JavaSpatialRDD` containing spatial features, along with the desired dimensions for the output image and a valid file path for saving the image. The `plotterClass` and `opts` parameters are optional but can be used to customize the plotting behavior.

### Output
Returns `Unit` — this indicates that the function performs an action (plotting the image) without returning a value. The generated image will be saved to the specified `imagePath`.

### Valid Call Patterns
```scala
val buildings = sc.shapefile("MSBuildings_data_index.zip")
buildings.plotImage(1000, 1000, "MSBuildings.png")

sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- Ensure that the `rdd` parameter is a valid `JavaSpatialRDD` containing spatial features before calling `plotImage`.
- Specify valid integer values for `imageWidth` and `imageHeight` to define the output image dimensions.
- Provide a valid file path for `imagePath` where the image will be saved, including the appropriate file extension.

### Prompt Snippet
```text
To plot spatial features to an image, use the plotImage method with a valid JavaSpatialRDD, specify the image dimensions, and provide a file path for saving the output image.
```

### Common Failure Modes
- Providing an invalid `imagePath` that does not have write permissions or does not exist can lead to an error when attempting to save the image.
- Specifying non-positive values for `imageWidth` or `imageHeight` will result in an error, as the dimensions must be greater than zero.
- Using an incompatible `plotterClass` that does not extend `Plotter` will cause a runtime error.

### Fix Code Hint
```scala
// Ensure the image path is valid and writable
val validPath = "output/plot.png" // Ensure this directory exists and is writable
buildings.plotImage(1000, 1000, validPath)
```

## API Test: `plotPyramid`

### Signature
```scala
def plotPyramid(outPath: String, numLevels: Int, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VisualizationMixin.scala:53_

_Source doc:_ Plots the dataset as multilevel tiled image and write the output to the given path. @param outPath the output path to write the image tiles to. @param numLevels the number of levels to create @param plotterClass the plotter class to use for plotting @param opts additional options for the plotter

### Goal
`plotPyramid` generates a multilevel tiled image representation of a dataset and saves it to a specified output path.

### Parameters
- `outPath` (`String`): The file path where the output image tiles will be saved. This should be a valid path where the user has write permissions.
- `numLevels` (`Int`): The number of pyramid levels to create for the tiled image. This determines the detail levels of the output image.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()`: The class of the plotter to use for generating the image. The default is `GeometricPlotter`, which is suitable for general plotting tasks.

### Input
The caller must provide a dataset that has been indexed and is ready for visualization. The dataset should be compatible with the plotting mechanism, typically a spatial file that has been processed through RDPro's spatial operations.

### Output
Returns `Unit` — this indicates that the function completes its execution without returning a value. The output is the generated multilevel tiled images saved in the specified format at the given `outPath`.

### Valid Call Patterns
```scala
sparkContext.shapefile("tl_2018_us_county.zip")
  .plotPyramid("counties_multilevel.zip", 20,
    opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> "1m"))
```

### LLM Instruction Prompt
- When calling `plotPyramid`, ensure that the dataset is properly indexed and that the output path is valid and writable.

### Prompt Snippet
```text
To visualize the dataset as a multilevel tiled image, use the plotPyramid function with appropriate parameters.
```

### Common Failure Modes
- Providing an invalid `outPath` that does not exist or is not writable will result in an error.
- Specifying a `numLevels` that is less than 1 may lead to unexpected behavior or errors.
- Using a dataset that has not been properly indexed or is incompatible with the plotting function may cause runtime exceptions.

### Fix Code Hint
```scala
// Ensure the output path is valid and writable
val outputPath = "valid/output/path/counties_multilevel.zip"

// Ensure the dataset is indexed before calling plotPyramid
sparkContext.shapefile("tl_2018_us_county.zip")
  .spatialPartition(classOf[RSGrovePartitioner])
  .writeSpatialFile("counties_index", "rtree")

// Call plotPyramid with valid parameters
sparkContext.spatialFile("counties_index")
  .plotPyramid(outputPath, 20, opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> "1m"))
```

## API Test: `plotSingleTileParallel`

### Signature
```scala
def plotSingleTileParallel(features: SpatialDataTypes.SpatialRDD, resolution: Int, tileID: Long, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): VectorTile.Tile
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:98_

_Source doc:_ Plots the given set of features as a vector tile according to Mapbox specifications using a Spark job. @param features the set of features to plot @param resolution the resolution of the image in pixels @param tileID the ID of the tile to plot @param buffer additional pixels around the tile to plot from all directions (default is zero) @param opts additional options to customize the plotting @return a vector tile that contains all the given features

### Goal
`plotSingleTileParallel` generates a vector tile from a set of spatial features, allowing for efficient visualization of geospatial data in a specified tile format.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): A distributed collection of spatial features to be plotted as a vector tile. This should contain geometries such as points, lines, or polygons.
- `resolution` (`Int`): The resolution of the output vector tile in pixels, determining the level of detail in the rendered tile.
- `tileID` (`Long`): The unique identifier for the tile being generated, typically encoded using a tile indexing scheme.
- `buffer` (`Int`), default `0`: The number of additional pixels to include around the specified tile, allowing for context beyond the tile boundaries (default is zero).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options to customize the plotting behavior, such as styling or rendering preferences.

### Input
The caller must provide a `SpatialRDD` containing spatial features, a valid integer for resolution, a long integer for tileID, and optionally specify a buffer and BeastOptions. The features should be compatible with the vector tile format.

### Output
Returns `VectorTile.Tile` — a vector tile that encapsulates the plotted features, formatted according to Mapbox specifications, suitable for rendering in web mapping applications.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val wktReader = new WKTReader(factory)
val geometries = Array("LINESTRING(-160 40, -150 20)").map(wkt => wktReader.read(wkt))
val features: RDD[IFeature] = sparkContext.parallelize(geometries).map(g => Feature.create(null, g))

val tile = MVTDataVisualizer.plotSingleTileParallel(features, 128, TileIndex.encode(0, 0, 0), 0)
```

### LLM Instruction Prompt
When calling `plotSingleTileParallel`, ensure that the `features` parameter is a valid `SpatialRDD` containing spatial geometries, and that the `resolution`, `tileID`, and optional parameters are correctly specified.

### Prompt Snippet
```text
To generate a vector tile, use the `plotSingleTileParallel` function with a valid `SpatialRDD` of features, specifying the desired resolution and tile ID.
```

### Common Failure Modes
- Providing an empty or invalid `SpatialRDD` for the `features` parameter may result in runtime errors or empty tiles.
- Specifying a `resolution` that is too low may lead to loss of detail in the output tile.
- Incorrectly encoding the `tileID` may result in unexpected tile outputs or errors.

### Fix Code Hint
```scala
Ensure that the `features` RDD is populated with valid geometries and that the `resolution` and `tileID` are correctly defined before calling `plotSingleTileParallel`.
```

## API Test: `pointSample`

### Signature
```scala
def pointSample(features: SpatialRDD, sampleSize: Int, sampleRatio: Double, seed: Long = System.currentTimeMillis()): Array[Array[Double]]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/PointSampler.scala:47_

_Source doc:_ Reads a point sample from the given spatial RDD. It returns a two dimensional array where the first index is the dimension and the second index is the point. This method runs an action on the given RDD. The method takes both a sample size and sample ratio and it returns whichever is smaller. In other words, it tries to read the given sample ratio and if the result is bigger than the sample size, it truncates it to the sample size. This ensures that the final result will fit in memory regardless of the input size. @param features the input features to sample @param sampleSize number of sample points to read @param sampleRatio the ratio of the points to read @return a two-dimensional array of sample points

### Goal
The `pointSample` function retrieves a sample of points from a given spatial RDD, allowing for efficient sampling of geospatial features.

### Parameters
- `features` (`SpatialRDD`): The input features to sample from, which should be a distributed collection of spatial data points.
- `sampleSize` (`Int`): The maximum number of sample points to read from the `features`. This value limits the output size to ensure it fits in memory.
- `sampleRatio` (`Double`): The ratio of the total points to sample from the `features`. The function will attempt to sample this ratio of points, but will truncate the result to `sampleSize` if necessary.
- `seed` (`Long`), default `System.currentTimeMillis()`: A seed value for random sampling, which can be used to ensure reproducibility of the sample results.

### Input
The caller must provide a `SpatialRDD` containing spatial features, along with an integer for `sampleSize` and a double for `sampleRatio`. The `SpatialRDD` should be properly initialized and contain valid geometries.

### Output
Returns `Array[Array[Double]]` — a two-dimensional array where each inner array represents a sampled point's coordinates. The first index corresponds to the dimension (e.g., x, y), and the second index corresponds to the individual sampled points.

### Valid Call Patterns
```scala
val factory = GeometryReader.DefaultGeometryFactory
val point = factory.createPoint(new Coordinate(3, 4))
val features: RDD[IFeature] = sparkContext.parallelize(Seq(Feature.create(null, point)), 4)
val sample = PointSampler.pointSample(features, 1, 1.0)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing spatial data points.
- Provide appropriate values for `sampleSize` and `sampleRatio` to control the output size.
- Use the `seed` parameter if reproducibility of the sample is required.

### Prompt Snippet
```text
Retrieve a sample of points from a spatial RDD using the pointSample function, specifying the maximum number of points and the sampling ratio.
```

### Common Failure Modes
- Providing an empty or null `SpatialRDD` will result in an error or an empty output.
- Setting `sampleSize` to a negative value will likely cause an exception.
- If `sampleRatio` is set to a value less than 0 or greater than 1, it may lead to unexpected results or errors.

### Fix Code Hint
```scala
// Ensure the SpatialRDD is not empty and sampleSize is a positive integer
val features: RDD[IFeature] = sparkContext.parallelize(Seq(/* valid features */))
val sample = PointSampler.pointSample(features, 10, 0.5) // Example with valid parameters
```

## API Test: `printOperationUsage`

### Signature
```scala
def printOperationUsage(operation: Operation, options: BeastOptions, out: PrintStream): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:334_

_Source doc:_ Prints the usage of a specific operation. @param operation the operation to print the usage to @param out the print stream to write to

### Goal
The `printOperationUsage` function prints the usage information for a specified raster processing operation in the context of geospatial analysis.

### Parameters
- `operation` (`Operation`): The specific operation for which usage information is to be printed. This should be one of the predefined operations available in the RDPro library.
- `options` (`BeastOptions`): Configuration options that may affect the operation's execution. This can include parameters like input/output formats or processing options, though the exact usage of this parameter is not specified in the provided context.
- `out` (`PrintStream`): The output stream where the usage information will be printed. This is typically a `PrintStream` object that directs output to the console or a file.

### Input
The caller must provide a valid `Operation` instance representing the desired operation, a `BeastOptions` instance (which may be null), and a `PrintStream` instance for output. There are no specific file formats required for this function, but the operation should be one that is recognized by the RDPro library.

### Output
Returns `Unit` — this indicates that the function does not return a value but instead performs a side effect by printing the usage information directly to the provided `PrintStream`.

### Valid Call Patterns
```scala
val baos = new ByteArrayOutputStream()
val printer: PrintStream = new PrintStream(baos)
OperationHelper.printOperationUsage(OperationHelper.operations("subtest1"), null, printer)
printer.close()
```

### LLM Instruction Prompt
- When calling `printOperationUsage`, ensure that the `operation` parameter is a valid operation recognized by the RDPro library, and provide a `PrintStream` for output. The `options` parameter can be null if no specific options are needed.

### Prompt Snippet
```text
Print the usage information for a specific operation using the printOperationUsage function.
```

### Common Failure Modes
- Passing an invalid `Operation` that is not recognized by the RDPro library may result in an error or no output.
- Providing a null `PrintStream` will lead to a `NullPointerException` when attempting to print the usage information.

### Fix Code Hint
```scala
// Ensure the operation is valid and the PrintStream is not null before calling the function.
val operation = OperationHelper.operations.get("validOperationName") // Replace with a valid operation name
if (operation.isDefined) {
    val printer: PrintStream = new PrintStream(new ByteArrayOutputStream())
    printOperationUsage(operation.get, null, printer)
} else {
    println("Invalid operation specified.")
}
```

## API Test: `process`

### Signature
```scala
private def process(inputMBR: Rectangle, filePath: String): Option[String]
private def process(filePath: String, pointX: Double, pointY: Double): Option[(String, Int)]
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/raptorhunt/GetPointValue.scala:134  (+1 more definition site/overload)_

### Goal
The `process` function retrieves the value of a raster at a specified point (defined by `pointX` and `pointY`) from a raster file located at `filePath`.

### Parameters
- `filePath` (`String`): The path to the raster file (e.g., a GeoTIFF) from which the value will be extracted.
- `pointX` (`Double`): The X-coordinate (longitude) of the point for which the raster value is to be retrieved.
- `pointY` (`Double`): The Y-coordinate (latitude) of the point for which the raster value is to be retrieved.

### Input
The caller must provide a valid path to a raster file in GeoTIFF format. The coordinates (`pointX` and `pointY`) must correspond to valid locations within the bounds of the raster dataset.

### Output
Returns `Option[(String, Int)]` — an optional tuple where the first element is a `String` representing the raster value's metadata (e.g., a description or identifier), and the second element is an `Int` representing the pixel value at the specified coordinates.

### Valid Call Patterns
```scala
val result: Option[(String, Int)] = value.process("path/to/raster.tif", 34.05, -118.25)
```

### LLM Instruction Prompt
- Ensure that the `filePath` points to a valid raster file and that the coordinates (`pointX`, `pointY`) are within the raster's extent.

### Prompt Snippet
```text
Retrieve the raster value at the specified coordinates from the given raster file.
```

### Common Failure Modes
- The `filePath` does not point to a valid raster file, resulting in a failure to load the raster.
- The coordinates (`pointX`, `pointY`) are outside the bounds of the raster, leading to a `None` return value.

### Fix Code Hint
```scala
// Ensure the file path is correct and the coordinates are within the raster's extent.
```

## API Test: `putStoredFile`

### Signature
```scala
def putStoredFile(zip: ZipOutputStream, filename: String, data: Array[Byte]): Unit
def putStoredFile(zip: org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream, filename: String, data: Array[Byte]): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:584  (+1 more definition site/overload)_

_Source doc:_ Add a file to the given ZIP file using [[ZipEntry.STORED]] method, i.e., no compression. @param zip the ZIP file to write the entry to @param filename the name of the entry in the ZIP file @param data the binary data of the file

### Goal
`putStoredFile` adds a file to a ZIP archive without compression, which is useful for packaging multiple files together in geospatial raster processing workflows.

### Parameters
- `zip` (`ZipOutputStream`): The ZIP output stream to which the file will be added. This stream must be open and ready for writing.
- `filename` (`String`): The name of the file entry within the ZIP archive. This should be a valid file name that will be used to reference the data inside the ZIP.
- `data` (`Array[Byte]`): The binary data of the file to be stored in the ZIP. This should be a non-empty byte array containing the file's contents.

### Input
The caller must provide:
- An open `ZipOutputStream` or `ZipArchiveOutputStream` instance.
- A valid filename as a string that does not contain illegal characters for ZIP entries.
- A non-empty byte array representing the file's binary data.

### Output
Returns `Unit` — this indicates that the operation completes successfully without returning any value. If the operation fails, an exception will be thrown.

### Valid Call Patterns
```scala
val file1 = new File(scratchDir, "test1.zip")
val zip1 = new ZipOutputStream(new FileOutputStream(file1))
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1, 2, 3, 4, 5, 6))
ZipUtil.putStoredFile(zip1, "data.bin", Array[Byte](1, 2, 3))
zip1.close()
```

### LLM Instruction Prompt
- Ensure that the `zip` parameter is an open `ZipOutputStream` or `ZipArchiveOutputStream`.
- The `filename` must be a valid string without illegal characters for ZIP entries.
- The `data` array must not be empty.

### Prompt Snippet
```text
Add a file to the ZIP archive using putStoredFile, ensuring the zip stream is open, the filename is valid, and the data array is populated.
```

### Common Failure Modes
- Attempting to write to a closed `ZipOutputStream` will result in an `IOException`.
- Providing a filename with illegal characters may cause an `IllegalArgumentException`.
- Passing an empty byte array will not throw an error but will result in an entry with no data, which may not be the intended behavior.

### Fix Code Hint
```scala
// Ensure the ZipOutputStream is open and the filename is valid before calling putStoredFile
if (zip1 != null && filename.nonEmpty && data.nonEmpty) {
    ZipUtil.putStoredFile(zip1, filename, data)
} else {
    throw new IllegalArgumentException("Invalid parameters for putStoredFile")
}
```

## API Test: `rangeQuery`

### Signature
```scala
def rangeQuery(range: Geometry, mbrCount: LongAccumulator = null): SpatialRDD
def rangeQuery(range: Geometry, mbrCount: LongAccumulator = null): PartitionedSpatialRDD
def rangeQuery(rdd: JavaSpatialRDD, range: Geometry): JavaSpatialRDD
def rangeQuery(rdd: JavaSpatialRDD, range: Geometry, mbrCount: LongAccumulator): JavaSpatialRDD
def rangeQuery(partitionedRDD: JavaPartitionedSpatialRDD, range: Geometry): JavaPartitionedSpatialRDD
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:131  (+4 more definition site/overload)_

_Source doc:_ Performs a range query while counting the number of MBR tests for profiling the performance. @param rdd the RDD that contains the spatial features @param range the query range @param mbrCount (out) an accumulator that counts the number of MBR tests @return a filtered RDD with the features that intersect the given query range

### Goal
The `rangeQuery` function retrieves spatial features from an RDD that intersect with a specified geometric range, enabling efficient spatial filtering in geospatial analyses.

### Parameters
- `range` (`Geometry`): The spatial range defined by a geometric shape (e.g., a bounding box) within which to search for features. This parameter must be a valid geometry object that represents the area of interest.
- `mbrCount` (`LongAccumulator`): An optional accumulator that tracks the number of Minimum Bounding Rectangle (MBR) tests performed during the query. This can be used for performance profiling and optimization.

### Input
The input must include a `JavaSpatialRDD` containing spatial features, and the `range` must be a valid `Geometry` object. The `mbrCount` is optional and can be set to `null` if profiling is not required.

### Output
Returns `JavaSpatialRDD` — a filtered RDD containing only the spatial features that intersect with the specified `range`. The output retains the same format as the input RDD, allowing for further processing or analysis.

### Valid Call Patterns
```scala
val filteredData: JavaSpatialRDD = partitionedData.rangeQuery(new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40))
val matchedPolygons: JavaSpatialRDD = polygons.rangeQuery(range)
```

### LLM Instruction Prompt
- When calling `rangeQuery`, ensure that the `range` parameter is a valid `Geometry` object and that the input RDD is a `JavaSpatialRDD`. If using `mbrCount`, initialize it as a `LongAccumulator`.

### Prompt Snippet
```text
To perform a range query, use the `rangeQuery` method on a `JavaSpatialRDD` with a valid `Geometry` range. Optionally, provide a `LongAccumulator` to count MBR tests.
```

### Common Failure Modes
- Failing to provide a valid `Geometry` for the `range` parameter will result in runtime errors.
- If the input RDD is not a `JavaSpatialRDD`, the method will not compile.
- Not initializing the `mbrCount` accumulator when profiling is desired may lead to unexpected results in performance metrics.

### Fix Code Hint
```scala
// Ensure the range is a valid Geometry and the input RDD is a JavaSpatialRDD
val range = new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40)
val mbrCount = new LongAccumulator
val filteredData: JavaSpatialRDD = partitionedData.rangeQuery(range, mbrCount)
```

## API Test: `raptorJoin`

### Signature
```scala
def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)
def raptorJoin[T](vectors: JavaSpatialRDD, rasters: JavaRasterRDD[T], opts: BeastOptions): JavaRDD[RaptorJoinFeature[T]]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:269  (+1 more definition site/overload)_

_Source doc:_ Performs a raster X vector join (Raptor join) between the two given RDDs. @param vectors the set of vector features @param rasters the set of raster tiles @param opts additional options for the algorithm @return the intersection between the feature vectors and all raster pixels.

### Goal
The `raptorJoin` function performs a raster-vector join operation, allowing users to combine raster data with vector features to analyze spatial relationships.

### Parameters
- `vectors` (`JavaSpatialRDD`): The set of vector features to join with the raster data. This should be a collection of spatial features, such as polygons or points, that define the areas of interest for the join operation.
- `rasters` (`JavaRasterRDD[T]`): The set of raster tiles that contain pixel data. The type `T` should match the pixel type of the raster data being processed (e.g., `Int`, `Float`).
- `opts` (`BeastOptions`): Additional options to configure the Raptor join operation. This can include parameters that affect the join's behavior, such as spatial tolerance or output settings.

### Input
The caller must provide:
- A `JavaSpatialRDD` containing vector features, which can be loaded from formats like Shapefiles or GeoJSON.
- A `JavaRasterRDD[T]` containing raster data, which can be loaded from GeoTIFF files.
- Ensure that the pixel type of the raster matches the expected type `T` when calling the function.

### Output
Returns `JavaRDD[RaptorJoinFeature[T]]` — a collection of `RaptorJoinFeature` objects representing the intersections between the provided vector features and the raster pixels. Each feature contains information about the overlapping areas, including the vector feature and the corresponding raster pixel values.

### Valid Call Patterns
```scala
val raster: RDD[ITile] = sc.geoTiff("treecover")
val vector: RDD[IFeature] = sc.shapefile("us_states")
val join: RDD[RaptorJoinFeature[Float]] = raster.raptorJoin(vector)
```

### LLM Instruction Prompt
When calling `raptorJoin`, ensure that the input raster and vector data are properly loaded and that the pixel type of the raster matches the expected type for the join operation.

### Prompt Snippet
```text
To perform a raster-vector join using the raptorJoin function, ensure you have a JavaSpatialRDD of vector features and a JavaRasterRDD of raster tiles. The pixel type of the raster must be compatible with the expected type in the join.
```

### Common Failure Modes
- Mismatched pixel types between the raster and the expected type `T` can lead to runtime errors.
- Providing an empty or improperly formatted `JavaSpatialRDD` or `JavaRasterRDD` may result in an empty output or exceptions during execution.

### Fix Code Hint
```scala
Ensure that the raster and vector datasets are correctly loaded and that their types are compatible. For example, use `sc.geoTiff[Int]` for integer raster data and `sc.shapefile(...)` for vector features.
```

## API Test: `raptorJoinFeature`

### Signature
```scala
def raptorJoinFeature[T](raster: RasterRDD[T], features: RDD[IFeature], opts: BeastOptions = new BeastOptions(), numTiles: LongAccumulator = null): RDD[RaptorJoinFeature[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:73_

_Source doc:_ Performs a raptor join between a raster RDD and a set of features. The output contains information about all pixels that match with the set of features. @param raster the raster RDD that contains all the tiles to test @param features the set of features to join with the raster data @param opts additional options for the query processor @param numTiles an optional accumulator to count the number of tiles accesses during the query processing. @tparam T the type of the pixel values @return the set of overlaps between pixels and features

### Goal
`raptorJoinFeature` performs a spatial join between a raster dataset and vector features, returning information about the pixels that intersect with the specified features.

### Parameters
- `raster` (`RasterRDD[T]`): The raster RDD containing the pixel data to be analyzed. It must be loaded from a compatible raster format, such as GeoTIFF, and the pixel type `T` should match the expected data type (e.g., `Int`, `Float`).
- `features` (`RDD[IFeature]`): The RDD of vector features (e.g., polygons, points) that will be joined with the raster data. These features should be loaded from a vector format such as Shapefile or GeoJSON.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options for the query processor, allowing customization of the join operation. This can include parameters like spatial tolerance or filtering criteria.
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator that counts the number of raster tiles accessed during the join operation. This can be useful for performance monitoring.

### Input
The caller must provide:
- A raster dataset loaded as `RasterRDD[T]` from a supported format (e.g., GeoTIFF).
- A set of vector features loaded as `RDD[IFeature]` from a compatible vector format (e.g., Shapefile).
- Ensure that the pixel type `T` of the raster matches the expected type for the operation.

### Output
Returns `RDD[RaptorJoinFeature[T]]` — an RDD containing the results of the join operation, where each element represents a pixel from the raster that intersects with a feature, including details about the feature and the pixel.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val countries = sc.shapefile("ne_10m_admin_0_countries.zip")
val result = RaptorJoin.raptorJoinFeature(raster, countries)
```

### LLM Instruction Prompt
When calling `raptorJoinFeature`, ensure that the raster and features are properly loaded and that the pixel type matches the expected type for the raster data.

### Prompt Snippet
```text
To perform a raptor join between a raster dataset and vector features, use the `raptorJoinFeature` method, ensuring that the raster is loaded as `RasterRDD[T]` and the features as `RDD[IFeature]`.
```

### Common Failure Modes
- Mismatched pixel types between the raster and the expected type `T`.
- Providing an empty RDD for either the raster or the features, which will result in no output.
- Not initializing the `BeastOptions` correctly if specific options are required for the join.

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and that the features RDD is not empty. Check that the pixel type of the raster matches the expected type for the operation.
```

## API Test: `raptorJoinIDFull`

### Signature
```scala
def raptorJoinIDFull[T](raster: RDD[ITile[T]], vector: RDD[(Long, IFeature)], opts: BeastOptions, numTiles: LongAccumulator = null, numRanges: LongAccumulator = null) : RDD[RaptorJoinResult[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180_

_Source doc:_ A Raptor join implementation that returns all the matches between features and pixels along with the raster metadata that puts the pixel in context. @param raster the RDD that contains the raster tiles @param vector the RDD that contains the vector features and their unique IDs @param opts additional options for the query processor @tparam T the type of the pixel values @return RDD that contains all overlaps between pixels and geometries

### Goal
`raptorJoinIDFull` performs a Raptor join between raster tiles and vector features, returning all matches along with the associated raster metadata.

### Parameters
- `raster` (`RDD[ITile[T]]`): An RDD containing raster tiles, where each tile represents a portion of the raster data with pixel values of type `T`.
- `vector` (`RDD[(Long, IFeature)]`): An RDD containing vector features, where each feature is paired with a unique identifier (Long). This represents the geometries to be joined with the raster data.
- `opts` (`BeastOptions`): An instance of `BeastOptions` that provides additional configuration options for the join operation, such as spatial indexing or query parameters.
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator to track the number of tiles processed during the join operation.
- `numRanges` (`LongAccumulator`), default `null`: An optional accumulator to track the number of ranges processed during the join operation.

### Input
The caller must provide:
- An RDD of raster tiles loaded from a supported format (e.g., GeoTIFF) using `sc.geoTiff(...)`.
- An RDD of vector features, which can be created from formats like Shapefile or GeoJSON using appropriate loading methods (e.g., `sc.shapefile(...)`).
- A valid `BeastOptions` instance to configure the join operation.

### Output
Returns `RDD[RaptorJoinResult[T]]` — an RDD containing `RaptorJoinResult` objects, each representing an overlap between raster pixels and vector geometries, along with the associated raster metadata.

### Valid Call Patterns
```scala
val rasterFile = makeFileCopy("/raptor/glc2000_small.tif").getPath
val testPoly = factory.toGeometry(new Envelope(-82.76, -80.25, 31.91, 35.17))
val vector: RDD[(Long, IFeature)] = sparkContext.parallelize(Seq((1L, Feature.create(null, testPoly))))
val raster: RasterFileRDD[Int] = new RasterFileRDD[Int](sparkContext, rasterFile, new BeastOptions())

val values: RDD[RaptorJoinResult[Int]] = RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
```

### LLM Instruction Prompt
When calling `raptorJoinIDFull`, ensure that the raster and vector RDDs are properly defined and that the `BeastOptions` instance is configured according to the requirements of the join operation.

### Prompt Snippet
```text
To perform a Raptor join between raster tiles and vector features, use the following pattern:
val result: RDD[RaptorJoinResult[T]] = RaptorJoin.raptorJoinIDFull(raster, vector, opts)
```

### Common Failure Modes
- The raster and vector RDDs must be compatible in terms of spatial reference; mismatched projections may lead to incorrect results.
- Ensure that the `BeastOptions` instance is properly configured; missing or incorrect options may cause the join to fail or produce unexpected results.
- If the input RDDs are empty, the output will also be empty, which may not be the expected behavior.

### Fix Code Hint
```scala
Check that the raster and vector RDDs are correctly loaded and that the `BeastOptions` are set up with the necessary parameters for the join operation.
```

## API Test: `rasterHeight`

### Signature
```scala
def rasterHeight: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:52_

_Source doc:_ Total number of rows (scanlines) in the raster layer

### Goal
`rasterHeight` retrieves the total number of rows (scanlines) in a raster layer, which is essential for understanding the dimensions of the raster data in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster layer that has been loaded into the RDPro framework, typically from a GeoTIFF or HDF file format. The raster must be properly initialized and accessible within the Spark context.

### Output
Returns `Int` — the total number of rows (scanlines) in the raster layer, representing the vertical dimension of the raster data.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val height: Int = raster.first().rasterHeight
```

### LLM Instruction Prompt
- Ensure that the raster layer is properly loaded and initialized before calling `rasterHeight`. The call should be made on an instance of a raster tile.

### Prompt Snippet
```text
To get the height of the raster layer, ensure the raster is loaded and then call `rasterHeight` on the raster instance.
```

### Common Failure Modes
- Calling `rasterHeight` on an uninitialized or empty raster layer will result in a runtime error.
- Attempting to call `rasterHeight` on a non-raster object will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling rasterHeight
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val height: Int = raster.first().rasterHeight // Ensure raster is not empty
```

## API Test: `rasterWidth`

### Signature
```scala
def rasterWidth: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:49_

_Source doc:_ Total number of columns in the raster layer

### Goal
`rasterWidth` retrieves the total number of columns (width) in a raster layer, which is essential for understanding the raster's spatial dimensions in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster object that has been initialized and contains raster metadata. This typically involves loading a raster from a GeoTIFF or HDF file using the `sc.geoTiff(...)` or `sc.hdfFile(...)` methods.

### Output
Returns `Int` — the total number of columns in the raster layer, representing the width of the raster in pixel units.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val width: Int = raster.metadata.rasterWidth
```

### LLM Instruction Prompt
- When calling `rasterWidth`, ensure that the raster object has been properly initialized and contains valid metadata. The call should be made on a raster object that has been loaded from a supported file format.

### Prompt Snippet
```text
To get the width of a raster layer, use the `rasterWidth` method on a raster object that has been initialized with valid metadata.
```

### Common Failure Modes
- Attempting to call `rasterWidth` on a raster object that has not been properly initialized or does not contain valid metadata will result in a runtime error.
- Calling `rasterWidth` on an empty or non-existent raster will lead to unexpected behavior or exceptions.

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and contains valid metadata before calling `rasterWidth`. For example:
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val width: Int = raster.metadata.rasterWidth
```

## API Test: `rasterizeGeometry`

### Signature
```scala
private[davinci] def rasterizeGeometry(geometry: Geometry): Boolean
private def rasterizeGeometry(geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:220  (+1 more definition site/overload)_

_Source doc:_ Plot the given geometry to the blocked pixels @param geometry the geometry to plot. The geometry should already be in the image space. @return `true` if the pixels changed as a result of this step. Not 100% accurate, though.

### Goal
The `rasterizeGeometry` function plots a given geometry onto the raster's blocked pixels, modifying the pixel values based on the geometry's shape.

### Parameters
- `geometry` (`Geometry`): The geometry to plot, which should already be transformed into the image space coordinates.

### Input
The input must be a valid `Geometry` object that represents the shape to be rasterized. The geometry should be in the same coordinate reference system (CRS) as the raster being modified.

### Output
Returns `Boolean` — `true` if the raster pixels were altered as a result of the rasterization process, indicating that the geometry successfully impacted the raster.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.rasterizeGeometry(factory.createGeometryCollection(Array(factory.createLineString(), factory.createPoint(new CoordinateXY(0, 0)))))
```

### LLM Instruction Prompt
- Ensure that the `geometry` parameter is a valid `Geometry` object that is already in the image space before calling `rasterizeGeometry`.

### Prompt Snippet
```text
canvas.rasterizeGeometry(geometry)
```

### Common Failure Modes
- Calling `rasterizeGeometry` with a `Geometry` that is not in the correct image space may result in no changes to the raster.
- If the `geometry` is null or improperly defined, it may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the geometry is properly defined and in the correct coordinate system before calling
val geometry: Geometry = factory.createPoint(new CoordinateXY(0, 0))
if (geometry != null) {
    canvas.rasterizeGeometry(geometry)
}
```

## API Test: `rasterizePixels`

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Create a raster from a set of pixel values @param pixels the list of pixel locations and values @param metadata the raster metadata that defines the geography of the pixels @return a raster that contains all the pixels

### Goal
`rasterizePixels` creates a raster representation from specified pixel values and their locations, enabling geospatial analysis in a distributed environment.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): A distributed collection of pixel data, where each entry is a tuple containing the x-coordinate, y-coordinate, and the pixel value of type `T`. This represents the pixel locations and their corresponding values in the raster.
- `metadata` (`RasterMetadata`): An object that contains metadata describing the raster, including its spatial extent, resolution, and coordinate reference system (CRS). This information is essential for correctly positioning the raster in geographic space.
- `rasterFeature` (`RasterFeature`): A feature that provides additional context for the raster, such as file name or other attributes. This is used to associate the raster with its source or intended use.

### Input
The caller must provide:
- A valid `RDD` of pixel data in the form of tuples `(Int, Int, T)`, where `T` is the pixel type (e.g., `Int`, `Float`).
- A `RasterMetadata` object that accurately describes the raster's spatial properties.
- A `RasterFeature` object that includes relevant metadata about the raster.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset that contains the specified pixel values, structured according to the provided metadata. This output can be used for further geospatial analysis or saved in formats like GeoTIFF.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (0, 0, 100),
  (3, 4, 200),
  (8, 9, 300)
))
val raster = sc.rasterizePixels(pixels, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
```

### LLM Instruction Prompt
- When calling `rasterizePixels`, ensure that the `pixels` RDD contains tuples of pixel coordinates and values, the `metadata` accurately describes the raster's spatial properties, and the `rasterFeature` provides necessary context for the raster.

### Prompt Snippet
```text
To create a raster from pixel data, use the rasterizePixels method with an RDD of pixel tuples, appropriate metadata, and raster feature.
```

### Common Failure Modes
- Providing an `RDD` of pixel data with incorrect types that do not match the expected pixel type `T`.
- Failing to supply a `RasterMetadata` object that accurately reflects the raster's spatial extent and resolution.
- Omitting the `RasterFeature`, which may lead to issues in associating the raster with its source or intended use.

### Fix Code Hint
```scala
Ensure that the pixel RDD is correctly typed and that the metadata and raster feature are properly instantiated before calling rasterizePixels.
```

## API Test: `rasterizePoints`

### Signature
```scala
def rasterizePoints[T: ClassTag](points: RDD[(Double, Double, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:55  (+1 more definition site/overload)_

_Source doc:_ Creates a raster from a list of point locations and values. @param points point locations and raster values @param metadata the metadata that describes the raster location @tparam T the type of raster values @return a raster that contains the given point locations

### Goal
`rasterizePoints` creates a raster representation from a set of point locations and their associated values, enabling geospatial analysis of point data in a raster format.

### Parameters
- `points` (`RDD[(Double, Double, T)]`): A distributed collection of tuples, where each tuple contains a pair of coordinates (longitude, latitude) and a value of type `T` representing the raster value at that location.
- `metadata` (`RasterMetadata`): An object that contains metadata describing the raster's spatial extent, coordinate reference system, and dimensions, which is essential for correctly placing the raster in geographic space.
- `rasterFeature` (`RasterFeature`): An object that defines the characteristics of the raster being created, such as its data type and any additional features relevant to the rasterization process.

### Input
The caller must provide:
- An `RDD` of point data in the form of `(Double, Double, T)` tuples, where `T` is the type of the raster values (e.g., `Int`, `Float`).
- A `RasterMetadata` object that specifies the raster's spatial properties.
- A `RasterFeature` object, which may be required for specific rasterization features.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset that contains the rasterized representation of the input point locations and their values, suitable for further geospatial analysis and processing.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (-51.3, 30.4, 100),
  (-55.2, 34.5, 200),
  (-56.4, 39.2, 300)
))
val raster = sc.rasterizePoints(pixels, metadata, null)
```

### LLM Instruction Prompt
- Ensure that the `points` RDD contains valid coordinate-value tuples, and that the `metadata` and `rasterFeature` are correctly defined to match the rasterization requirements.

### Prompt Snippet
```text
To create a raster from point data, use the `rasterizePoints` function with an RDD of point coordinates and values, along with appropriate raster metadata.
```

### Common Failure Modes
- Providing an empty `RDD` for `points` will result in an empty raster output.
- Mismatched or incorrect `RasterMetadata` may lead to errors in raster creation or misalignment of raster data.
- If the `rasterFeature` is not compatible with the data type of `T`, it may cause runtime errors during the rasterization process.

### Fix Code Hint
```scala
Ensure that the `points` RDD is populated with valid data, and verify that the `metadata` and `rasterFeature` are correctly configured to match the expected raster characteristics.
```

## API Test: `readCSVPoint`

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
- `filename` (`String`): The path to the CSV file containing the point data. This should be a valid file path accessible by the Spark context.
- `xColumn` (`Any`), default `0`: The index or name of the column that contains the x coordinate. If specified as an index, it defaults to the first column (0).
- `yColumn` (`Any`), default `1`: The index or name of the column that contains the y coordinate. If specified as an index, it defaults to the second column (1).
- `delimiter` (`Char`), default `','`: The character used to separate values in the CSV file. The default is a comma.
- `'`: This parameter appears to be incorrectly listed and does not have a defined purpose.
- `skipHeader` (`Boolean`), default `false`: Indicates whether to skip the first line of the CSV file, which is typically a header. If either `xColumn` or `yColumn` is specified as a `String`, this option will be ignored, and a header line will be assumed.

### Input
The input must be a CSV file where the specified columns contain valid numeric coordinates. The file should be formatted correctly according to the specified delimiter, and if `skipHeader` is set to `true`, the first line should be a header line.

### Output
Returns `SpatialRDD` — a distributed collection of spatial data points, where each point corresponds to a record in the CSV file, represented as x and y coordinates.

### Valid Call Patterns
```scala
val data: SpatialRDD = sparkContext.readCSVPoint("path/to/your/file.csv")
```

### LLM Instruction Prompt
When calling `readCSVPoint`, ensure that the `filename` points to a valid CSV file and that the specified `xColumn` and `yColumn` correspond to the correct data types.

### Prompt Snippet
```text
To read point data from a CSV file, use the readCSVPoint function with the appropriate filename and column indices or names for x and y coordinates.
```

### Common Failure Modes
- Specifying a `filename` that does not exist or is inaccessible will result in a file not found error.
- Incorrectly specifying `xColumn` or `yColumn` that do not exist in the CSV will lead to runtime errors.
- If the delimiter does not match the actual delimiter used in the CSV file, the data may not be parsed correctly.

### Fix Code Hint
```scala
// Ensure the CSV file exists and the specified columns are correct
val data: SpatialRDD = sparkContext.readCSVPoint("path/to/your/file.csv", xColumn = "longitude", yColumn = "latitude", delimiter = ',')
```

## API Test: `readConfigurationXML`

### Signature
```scala
def readConfigurationXML(filename: String): java.util.Map[String, java.util.List[String]]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60_

_Source doc:_ Read all XML configuration files of the given name in the class path and merge them into one object. This method internally caches the configuration so it does not have to be loaded multiple times. The XML is organized in three levels. The first level is the root element and it is always &lt;beast&gt;. The second level is a name of a collection, e.g., &lt;Indexers&gt;. Finally, the third level contains the contents of the collection in their text part. @param filename A path to an XML file that contains the configuration. @return the beast configuration as a map from each key to all values under this key.

### Goal
The `readConfigurationXML` function reads and merges XML configuration files from the class path, providing a structured representation of configuration settings for use in geospatial raster processing.

### Parameters
- `filename` (`String`): A path to an XML configuration file that contains the settings to be read and merged.

### Input
The caller must provide a valid path to an XML file that exists in the class path. The XML file should be structured with a root element `<beast>`, containing collections such as `<Indexers>` and their respective values.

### Output
Returns `java.util.Map[String, java.util.List[String]]` — a map where each key corresponds to a collection name (e.g., "Operations", "Indexers"), and the associated value is a list of strings representing the contents of that collection.

### Valid Call Patterns
```scala
val conf: java.util.Map[String, java.util.List[String]] = OperationHelper.readConfigurationXML("test-beast.xml")
```

### LLM Instruction Prompt
- When calling `readConfigurationXML`, ensure that the provided filename points to a valid XML configuration file in the class path, and be aware that the function caches the configuration for efficiency.

### Prompt Snippet
```text
Read the configuration from the XML file using `readConfigurationXML("your-config-file.xml")`.
```

### Common Failure Modes
- The specified XML file does not exist in the class path, leading to a `FileNotFoundException`.
- The XML file is not well-formed or does not adhere to the expected structure, resulting in parsing errors.

### Fix Code Hint
```scala
// Ensure the XML file exists and is well-formed before calling the function
val conf: java.util.Map[String, java.util.List[String]] = OperationHelper.readConfigurationXML("valid-config.xml")
```

## API Test: `readFile`

### Signature
```scala
def readFile(filename: String): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:170_

_Source doc:_ Read a text file as a single big string. @param filename the name (or path) of the file @return the contents of the file as one big String.

### Goal
`readFile` reads the contents of a specified text file and returns it as an array of strings, where each element represents a line from the file.

### Parameters
- `filename` (`String`): The name or path of the text file to be read.

### Input
The caller must provide a valid path to a text file. The file should be accessible in the environment where the Spark job is running. The file must be in a text format.

### Output
Returns `Array[String]` — an array containing the lines of the text file, with each line represented as a separate string.

### Valid Call Patterns
```scala
val content: Array[String] = readFile("path/to/your/file.txt")
```

### LLM Instruction Prompt
- Ensure that the provided filename points to a valid text file that exists in the specified path.

### Prompt Snippet
```text
Read the contents of the specified text file using the readFile function.
```

### Common Failure Modes
- The specified file does not exist, leading to a file not found error.
- The provided path is incorrect or inaccessible, resulting in an I/O exception.

### Fix Code Hint
```scala
// Ensure the file path is correct and the file exists before calling readFile
val filename = "path/to/your/file.txt"
if (new java.io.File(filename).exists) {
  val content: Array[String] = readFile(filename)
} else {
  println(s"File not found: $filename")
}
```

## API Test: `readInput`

### Signature
```scala
def readInput(sc: JavaSparkContext, opts: BeastOptions, filename: String, iFormat: String): JavaSpatialRDD
def readInput(sc: SparkContext, opts: BeastOptions, filename: String, iFormat: String) : SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialReader.scala:205  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
The `readInput` function loads spatial data from various file formats into a distributed spatial RDD for further geospatial analysis.

### Parameters
- `sc` (`JavaSparkContext`): The Spark context used to manage the distributed computation environment. It is expected to be initialized and running.
- `opts` (`BeastOptions`): Configuration options for the Beast library, which may include settings for data processing and handling.
- `filename` (`String`): The path to the input file containing spatial data, such as a shapefile or GeoJSON.
- `iFormat` (`String`): The format of the input file, which can be "shapefile", "geojson", or other supported formats.

### Input
The caller must provide a valid file path for the `filename` parameter, which should point to a shapefile, GeoJSON, or other supported spatial data formats. The Spark context (`sc`) must be properly initialized, and the `opts` parameter should be configured as needed for the specific processing task.

### Output
Returns `JavaSpatialRDD` — a distributed collection of spatial features that can be used for spatial operations and analysis within the RDPro framework.

### Valid Call Patterns
```scala
// Load a shapefile
JavaRDD<IFeature> polygons = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_state.zip", "shapefile");

// Load points in GeoJSON format
JavaRDD<IFeature> points = SpatialReader.readInput(sparkContext, new BeastOptions(), "Tweets.geojson.gz", "geojson");
```

### LLM Instruction Prompt
- Ensure that the `filename` provided points to a valid spatial data file in the specified format. The Spark context must be active, and the `opts` should be appropriately set for the task.

### Prompt Snippet
```text
Load spatial data using `readInput` by providing a valid Spark context, options, filename, and format.
```

### Common Failure Modes
- Providing an invalid file path in the `filename` parameter will result in a file not found error.
- Using an unsupported format in the `iFormat` parameter will lead to a runtime exception.
- If the Spark context (`sc`) is not initialized or is stopped, the function will fail to execute.

### Fix Code Hint
```scala
// Ensure the Spark context is initialized and the file path is correct
val sparkContext = new JavaSparkContext(...)
val options = new BeastOptions()
val spatialRDD = SpatialReader.readInput(sparkContext, options, "path/to/your/file.zip", "shapefile")
```

## API Test: `readLocal`

### Signature
```scala
def readLocal(path: String, iformat: String, opts: BeastOptions, conf: Configuration): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:492_

_Source doc:_ Reads the given path locally without creating any RDDs. Useful for reading a small file when SparkContext is not accessible, e.g., inside a mapPartition function. @param path path to a single file or a directory @param iformat the format of the data @param opts additional options for reading the file @return an iterator to features in the given path

### Goal
`readLocal` reads geospatial features from a specified local file or directory without creating RDDs, making it suitable for small files when SparkContext is not available.

### Parameters
- `path` (`String`): The file system path to a single file or a directory containing the data to be read.
- `iformat` (`String`): The format of the data being read, such as "wkt(1)" for Well-Known Text or other supported formats.
- `opts` (`BeastOptions`): Additional options for reading the file, which may include parameters like skipping headers or specifying field separators.
- `conf` (`Configuration`): The Hadoop configuration object that provides the necessary settings for file reading operations.

### Input
The caller must provide a valid file path (either to a single file or a directory) containing geospatial data in a supported format (e.g., WKT, CSV). The input file should be small enough to be processed without Spark, as this method is intended for local file access.

### Output
Returns `Iterator[IFeature]` — an iterator over the features read from the specified path, allowing for sequential access to the data without loading it all into memory at once.

### Valid Call Patterns
```scala
val features = SpatialFileRDD.readLocal(input.getPath, "wkt(1)",
  Seq(CSVFeatureReader.SkipHeader -> true, CSVFeatureReader.FieldSeparator -> '\t'), sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
- When calling `readLocal`, ensure that the path points to a valid file or directory and that the format specified is supported by the method.

### Prompt Snippet
```text
Read local features from a specified path using the appropriate format and options.
```

### Common Failure Modes
- Providing an invalid path that does not exist or is inaccessible will result in an error.
- Specifying an unsupported format in `iformat` may lead to a failure in reading the data.
- Incorrectly configured options in `opts` may cause unexpected behavior or errors during file reading.

### Fix Code Hint
```scala
Ensure the path is correct and accessible, and verify that the format and options provided are compatible with the data being read.
```

## API Test: `readPartition`

### Signature
```scala
def readPartition(partition: FilePartition, featureReaderClass: Class[_ <: FeatureReader], applyDuplicateAvoidance: Boolean, opts: BeastOptions): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441_

_Source doc:_ Reads the given partition @param partition the partition to read @param featureReaderClass the class of the feature reader @param opts the user options @return an iterator to the features

### Goal
`readPartition` reads features from a specified partition of geospatial data, utilizing a designated feature reader class to facilitate the extraction process.

### Parameters
- `partition` (`FilePartition`): Represents a segment of the input data file that is to be processed. It is expected to be a valid partition created from a geospatial data source.
- `featureReaderClass` (`Class[_ <: FeatureReader]`): The class type of the feature reader that will be used to read the features from the specified partition. This class must extend `FeatureReader`.
- `applyDuplicateAvoidance` (`Boolean`): A flag indicating whether to apply duplicate avoidance logic during the reading process. If set to `true`, the method will attempt to filter out duplicate features.
- `opts` (`BeastOptions`): User-defined options that may influence the reading process, such as input format specifications or other configurations relevant to the feature reading.

### Input
The caller must provide a valid `FilePartition` that corresponds to a geospatial data file, along with a suitable `featureReaderClass` that can handle the data format. The `opts` parameter should contain any necessary configurations for reading the features.

### Output
Returns `Iterator[IFeature]` — an iterator that provides access to the features read from the specified partition. Each feature is represented as an instance of `IFeature`, which encapsulates the properties and geometry of the geospatial data.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
}
```

### LLM Instruction Prompt
- When calling `readPartition`, ensure that the `partition` is a valid `FilePartition`, the `featureReaderClass` is a class extending `FeatureReader`, and the `opts` parameter is properly configured for the data being read.

### Prompt Snippet
```text
To read features from a partition of geospatial data, use the `readPartition` method with a valid `FilePartition`, a suitable `featureReaderClass`, and appropriate options.
```

### Common Failure Modes
- Providing an invalid `FilePartition` that does not correspond to a valid data source.
- Using a `featureReaderClass` that does not extend `FeatureReader`, leading to runtime errors.
- Failing to configure `opts` correctly, which may result in unexpected behavior or errors during the reading process.

### Fix Code Hint
```scala
Ensure that the `partition` is correctly created from a valid data source and that the `featureReaderClass` is compatible with the data format specified in `opts`.
```

## API Test: `readTextResource`

### Signature
```scala
def readTextResource(resourcePath: String, maxLines: Int): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:153_

_Source doc:_ Read the first n lines from the given resource and return those lines as an array of Strings. If the given upper bound is bigger than the input file, the entire input file is loaded and returned. Therefore, the returned array might be smaller than the given upper bound if the file is smaller. @param resourcePath the path to the resource to read @param maxLines     the upper bound of the number of lines to read @return an array of strings containing the lines read from the input file

### Goal
`readTextResource` reads a specified number of lines from a text resource, which can be useful for loading configuration or data files in geospatial raster processing workflows.

### Parameters
- `resourcePath` (`String`): The path to the text resource file to read. This should be a valid path accessible within the Spark environment.
- `maxLines` (`Int`): The maximum number of lines to read from the resource. If the resource contains fewer lines than this value, all available lines will be returned.

### Input
The caller must provide a valid path to a text resource file (e.g., a WKT file) and specify the maximum number of lines to read. The resource must be accessible in the Spark context.

### Output
Returns `Array[String]` — an array of strings containing the lines read from the input file. The length of the array may be less than or equal to `maxLines` depending on the number of lines in the resource.

### Valid Call Patterns
```scala
val lines: Array[String] = readTextResource("/test.wkt", 10)
```

### LLM Instruction Prompt
- When calling `readTextResource`, ensure that the `resourcePath` is a valid path to a text file and that `maxLines` is a positive integer.

### Prompt Snippet
```text
Read the first 10 lines from the WKT file located at "/test.wkt".
```

### Common Failure Modes
- Providing an invalid `resourcePath` that does not point to an existing file will result in an error.
- Setting `maxLines` to a negative value will likely cause an exception or unexpected behavior.

### Fix Code Hint
```scala
// Ensure the resource path is correct and accessible
val lines: Array[String] = readTextResource("/valid/path/to/resource.txt", 5)
```

## API Test: `readTile`

### Signature
```scala
override def readTile(tileID: Int): ITile[T]
def readTile(tileID: Int): ITile[T]
override def readTile(tileID: Int): ITile[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:167  (+2 more definition site/overload)_

### Goal
Reads a specified tile from a raster dataset, allowing for concurrent access to multiple tiles.

### Parameters
- `tileID` (`Int`): The ID of the tile to be read from the raster dataset. This ID corresponds to the specific tile's position within the raster structure.

### Input
The caller must provide a valid raster dataset that has been initialized and contains tiles. The dataset should be loaded using a compatible method (e.g., `sc.geoTiff(...)`), and the `tileID` must correspond to an existing tile within that dataset.

### Output
Returns `ITile[T]` — an object that contains the tile information, including pixel values and metadata for the specified tile.

### Valid Call Patterns
```scala
val rasterPath = new Path(makeFileCopy("/rasters/glc2000_small.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val tile = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Ensure that the raster dataset is properly initialized and that the `tileID` provided corresponds to a valid tile within that dataset.

### Prompt Snippet
```text
Read a tile from the raster dataset using its tile ID.
```

### Common Failure Modes
- Attempting to read a `tileID` that does not exist in the raster dataset, which may result in an error or exception.
- Not initializing the raster dataset before calling `readTile`, leading to a null reference or similar runtime error.

### Fix Code Hint
```scala
Ensure the raster dataset is loaded and initialized correctly before calling readTile, and verify that the tileID is valid.
```

## API Test: `readWKTFile`

### Signature
```scala
def readWKTFile(filename: String, wktColumn: Any, delimiter: Char = '\t', skipHeader: Boolean = false): SpatialRDD
def readWKTFile(filename: String, wktColumn: String, delimiter: Char, skipHeader: Boolean): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:118  (+1 more definition site/overload)_

_Source doc:_ Read a CSV file with WKT-encoded geometry @param filename the name of the file or directory fo the input @param wktColumn the column that includes the WKT-encoded geometry, either an Integer for the index of the attribute or String for its name @param delimiter the field delimiter, tab by default @param skipHeader whether to skip the header line or not, if wktColumn is a string, this has to be true, if wktColumn is an Integer, this is false by default but can be overloaded @return the set of features in the input file

### Goal
The `readWKTFile` function reads a CSV file containing WKT-encoded geometries and returns a `SpatialRDD` of the features defined by those geometries.

### Parameters
- `filename` (`String`): The name of the input file or directory containing the CSV file with WKT geometries.
- `wktColumn` (`Any`): Specifies the column that contains the WKT-encoded geometry. This can be an `Integer` representing the index of the column or a `String` representing the name of the column.
- `delimiter` (`Char`), default `'\t'`: The character used to separate fields in the CSV file. The default is a tab character.
- `skipHeader` (`Boolean`), default `false`: Indicates whether to skip the header line of the CSV file. If `wktColumn` is a `String`, this must be `true`. If `wktColumn` is an `Integer`, it defaults to `false` but can be overridden.

### Input
The caller must provide a CSV file where one of the columns contains WKT-encoded geometries. The file must be accessible at the specified `filename`, and the `wktColumn` must correctly reference the column containing the geometries. If the column is identified by name, the `skipHeader` parameter must be set to `true`.

### Output
Returns `SpatialRDD` — a distributed collection of spatial features extracted from the input CSV file, where each feature corresponds to a WKT geometry.

### Valid Call Patterns
```scala
val data: RDD[IFeature] = sparkContext.readWKTFile("path/to/file.csv", 0)
```

### LLM Instruction Prompt
- Ensure that the `filename` points to a valid CSV file containing WKT geometries. The `wktColumn` must be specified correctly as either an index or a column name, and the `skipHeader` parameter must be set according to the type of `wktColumn`.

### Prompt Snippet
```text
Read a CSV file containing WKT geometries using the readWKTFile function, ensuring the correct column index or name is provided.
```

### Common Failure Modes
- Providing an invalid `filename` that does not point to an existing file will result in a file not found error.
- Setting `skipHeader` to `true` while using an `Integer` for `wktColumn` will lead to an incorrect reading of the data.
- Specifying a `wktColumn` index that is out of bounds for the number of columns in the CSV will cause an index out of bounds error.

### Fix Code Hint
```scala
// Ensure the filename is correct and accessible, and verify the wktColumn index or name is valid.
```

## API Test: `reproject`

### Signature
```scala
def reproject(targetSRID: Int)
def reproject(targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def reproject[T: ClassTag](raster: RasterRDD[T], targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
def reproject(sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): SpatialRDD
protected def reproject(sourceSRID: Int, targetSRID: Int): SpatialRDD
def reproject(targetCRS: CoordinateReferenceSystem): SpatialRDD
def reproject(targetSRID: Int): SpatialRDD
def reproject(targetCRS: CoordinateReferenceSystem): RasterMetadata
def reproject(metadata: Array[RasterMetadata], targetCRS: CoordinateReferenceSystem): RasterMetadata
def reproject(rdd: JavaSpatialRDD, targetCRS: CoordinateReferenceSystem): JavaSpatialRDD
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:517  (+9 more definition site/overload)_

_Source doc:_ Reproject a raster to a target coordinate reference system. This method uses the same resolution (number of pixels) of the first tile in the source raster. You can use the other [[reshapeAverage()]] method that takes [[RasterMetadata]] to change all the information. @param raster the raster layer to reproject @param targetCRS the target coordinate reference system @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @tparam T the type of the pixels @return

### Goal
Reproject a raster dataset to a specified target coordinate reference system (CRS) while maintaining the resolution of the original raster.

### Parameters
- `raster` (`RasterRDD[T]`): The raster layer to be reprojected. This should be a distributed raster dataset loaded into Spark, such as from a GeoTIFF or HDF file.
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system to which the raster will be reprojected. This should be specified using a valid CRS identifier, such as "EPSG:4326".
- `unifiedRaster` (`Boolean`), default `false`: If set to true, all output tiles will belong to a single `RasterMetadata`, which can be useful for ensuring consistency across the output dataset.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to handle target pixels that overlap multiple source pixels. Options include nearest neighbor, bilinear, and others, depending on the implementation.

### Input
The input must include a `RasterRDD` containing the raster data to be reprojected, and a valid `CoordinateReferenceSystem` for the target CRS. The raster data should be loaded from supported formats like GeoTIFF or HDF. Ensure that the raster is properly initialized and that the Spark environment is configured to handle the data size.

### Output
Returns `RasterRDD[T]` — a new distributed raster dataset that has been reprojected to the specified target CRS, maintaining the resolution of the original raster.

### Valid Call Patterns
```scala
val temperature: RasterRDD[Float] = 
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperature.reproject(CRS.decode("EPSG:4326"))

val temperature: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperature.reproject(CRS.decode("EPSG:4326"), unifiedRaster = true, interpolationMethod = InterpolationMethod.Average)
```

### LLM Instruction Prompt
When calling `reproject`, ensure that the raster data is a valid `RasterRDD` and that the target CRS is specified correctly. Use appropriate interpolation methods based on the desired output quality.

### Prompt Snippet
```text
To reproject a raster dataset, use the `reproject` method with the raster data and the desired target CRS. Ensure that the raster is loaded correctly and that the Spark environment is set up.
```

### Common Failure Modes
- Attempting to reproject a raster that is not properly initialized or is empty.
- Specifying an invalid `CoordinateReferenceSystem` that cannot be recognized.
- Using an unsupported interpolation method that does not exist in the `InterpolationMethod` enumeration.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly and the target CRS is valid
val raster: RasterRDD[Float] = sc.geoTiff("path/to/raster.tif")
val targetCRS = CRS.decode("EPSG:4326")
val reprojectedRaster = raster.reproject(targetCRS)
```

## API Test: `reprojectEnvelope`

### Signature
```scala
def reprojectEnvelope(envelope: Envelope, sourceSRID: Int, targetSRID: Int): Envelope
def reprojectEnvelope(envelope: Envelope, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Envelope
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:427  (+1 more definition site/overload)_

_Source doc:_ Reprojects an envelope from one SRID to another SRID @param envelope the envelope to reproject with dimensions in source SRID @param sourceSRID the SRID of the given envelope @param targetSRID the desired SRID of the reprojected envelope @return the envelope after being reprojected to target SRID

### Goal
The `reprojectEnvelope` function transforms a given geospatial envelope from one spatial reference identifier (SRID) to another, ensuring accurate spatial representation across different coordinate systems.

### Parameters
- `envelope` (`Envelope`): The geospatial envelope that defines a rectangular area in the source coordinate system. It is expected to have dimensions specified in the coordinate system defined by `sourceSRID`.
- `sourceSRID` (`Int`): The spatial reference identifier (SRID) of the input envelope, indicating the coordinate system in which the envelope is defined.
- `targetSRID` (`Int`): The desired spatial reference identifier (SRID) for the output envelope, representing the coordinate system to which the envelope should be transformed.

### Input
The caller must provide:
- An `Envelope` object that represents the area to be reprojected.
- An integer representing the `sourceSRID` that corresponds to the coordinate system of the input envelope.
- An integer representing the `targetSRID` that corresponds to the desired output coordinate system.

### Output
Returns `Envelope` — the reprojected envelope that accurately represents the same area in the target coordinate system specified by `targetSRID`.

### Valid Call Patterns
```scala
val reprojectedEnvelope: Envelope = Reprojector.reprojectEnvelope(originalEnvelope, sourceSRID, targetSRID)
```

### LLM Instruction Prompt
- Ensure that the `envelope` is defined in the coordinate system specified by `sourceSRID` before calling `reprojectEnvelope`. The `targetSRID` must be a valid SRID that corresponds to a known coordinate system.

### Prompt Snippet
```text
To reproject an envelope from one SRID to another, use the `reprojectEnvelope` function with the appropriate parameters.
```

### Common Failure Modes
- Providing an `envelope` that does not match the `sourceSRID` may result in incorrect reprojection.
- Using an invalid `sourceSRID` or `targetSRID` that does not correspond to a recognized coordinate system can lead to runtime errors.

### Fix Code Hint
```scala
// Ensure the envelope is defined in the correct sourceSRID before calling
val reprojectedEnvelope: Envelope = Reprojector.reprojectEnvelope(originalEnvelope, validSourceSRID, validTargetSRID)
```

## API Test: `reprojectEnvelopeInPlace`

### Signature
```scala
def reprojectEnvelopeInPlace(envelope: Array[Double], sourceSRID: Int, targetSRID: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:465_

_Source doc:_ Reproject an envelope (orthogonal rectangle) to the target CRS in-place @param envelope the input envelope to convert in the form (x1, y1, x2, y2) @param sourceSRID the source coordinate reference system (CRS) @param targetSRID the target coordinate reference system (CRS) @return the converted envelope

### Goal
Reproject an orthogonal rectangle defined by the input envelope from a source coordinate reference system (CRS) to a target CRS in-place.

### Parameters
- `envelope` (`Array[Double]`): An array representing the coordinates of the envelope in the form (x1, y1, x2, y2), where (x1, y1) is the bottom-left corner and (x2, y2) is the top-right corner of the rectangle.
- `sourceSRID` (`Int`): The spatial reference identifier (SRID) of the source coordinate reference system from which the envelope is being reprojected.
- `targetSRID` (`Int`): The spatial reference identifier (SRID) of the target coordinate reference system to which the envelope is being reprojected.

### Input
The caller must provide an envelope as an `Array[Double]` with four elements representing the coordinates of the rectangle, and valid SRIDs for both the source and target coordinate reference systems.

### Output
Returns `Unit` — this indicates that the operation modifies the input envelope in-place, and there is no return value.

### Valid Call Patterns
```scala
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

### LLM Instruction Prompt
- Ensure that the envelope is correctly formatted as an `Array[Double]` with four elements representing the coordinates of the rectangle. The source and target SRIDs must be valid integers corresponding to recognized coordinate reference systems.

### Prompt Snippet
```text
Reproject the envelope from the source CRS to the target CRS using the reprojectEnvelopeInPlace function.
```

### Common Failure Modes
- Providing an envelope that does not contain exactly four elements will result in an `ArrayIndexOutOfBoundsException`.
- Using invalid SRIDs that do not correspond to any known coordinate reference systems may lead to unexpected behavior or errors during reprojection.

### Fix Code Hint
```scala
// Ensure the envelope is defined correctly and the SRIDs are valid before calling the function.
val envelope = Array(-180.0, 0, 0, 90)
val sourceSRID = 4326
val targetSRID = 3857
Reprojector.reprojectEnvelopeInPlace(envelope, sourceSRID, targetSRID)
```

## API Test: `reprojectGeometry`

### Signature
```scala
def reprojectGeometry(geometry: Geometry, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetSRID: Int): Geometry
def reprojectGeometry(geometry: Geometry, transform: TransformationInfo): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:274  (+3 more definition site/overload)_

_Source doc:_ Reprojects the given geometry from source to target CRS. This method ignores the SRID of the geometry and assumes it to be in the source CRS. @param geometry the geometry to transform @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return a new geometry that is transformed

### Goal
Reprojects a given geometry from one coordinate reference system (CRS) to another, facilitating accurate spatial analysis in geospatial raster processing.

### Parameters
- `geometry` (`Geometry`): The geometric shape (e.g., point, line, polygon) that needs to be transformed. It is expected to be in the source CRS.
- `sourceCRS` (`CoordinateReferenceSystem`): The original coordinate reference system of the geometry. This defines how the coordinates of the geometry are interpreted.
- `targetCRS` (`CoordinateReferenceSystem`): The desired coordinate reference system to which the geometry will be transformed.

### Input
The caller must provide a valid `Geometry` object, along with the corresponding `sourceCRS` and `targetCRS` as `CoordinateReferenceSystem` instances. The geometry should be assumed to be in the `sourceCRS`.

### Output
Returns `Geometry` — a new geometry object that represents the transformed shape in the `targetCRS`.

### Valid Call Patterns
```scala
val point: Geometry = new GeometryFactory().createPoint(new Coordinate(1, 1))
val sourceCRS: CoordinateReferenceSystem = CRS.decode("EPSG:4326", true)
val targetCRS: CoordinateReferenceSystem = CRS.decode("EPSG:3857", true)
val transformedPoint: Geometry = Reprojector.reprojectGeometry(point, sourceCRS, targetCRS)
```

### LLM Instruction Prompt
- When calling `reprojectGeometry`, ensure that the geometry is in the source CRS and that both the source and target CRS are correctly defined as `CoordinateReferenceSystem` instances.

### Prompt Snippet
```text
Reproject the geometry from the source CRS to the target CRS using the reprojectGeometry function.
```

### Common Failure Modes
- Providing a `Geometry` that is not in the expected `sourceCRS` may lead to incorrect transformations.
- Using incompatible `CoordinateReferenceSystem` instances can result in runtime errors or unexpected behavior.

### Fix Code Hint
```scala
// Ensure the geometry is correctly defined in the source CRS before calling reprojectGeometry
val transformedGeometry = Reprojector.reprojectGeometry(geometry, sourceCRS, targetCRS)
```

## API Test: `reprojectRDD`

### Signature
```scala
def reprojectRDD(sourceRDD: SpatialRDD, targetCRS: CoordinateReferenceSystem): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, targetSRID: Int): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, transform: TransformationInfo): SpatialRDD
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:235  (+2 more definition site/overload)_

_Source doc:_ Reproject the given RDD to the target CRS. The source CRS is retrieved from the first element of the source RDD. @param sourceRDD the RDD to transform @param targetCRS the target Coordinate Reference System @return the transformed RDD

### Goal
Reproject the input `SpatialRDD` to a specified target Coordinate Reference System (CRS).

### Parameters
- `sourceRDD` (`SpatialRDD`): The input RDD containing spatial data that needs to be transformed. The source CRS is derived from the first element of this RDD.
- `targetCRS` (`CoordinateReferenceSystem`): The target CRS to which the `sourceRDD` will be reprojected. This should be a valid CRS object representing the desired spatial reference.

### Input
The caller must provide a `SpatialRDD` containing spatial data, which can be derived from various formats such as GeoTIFF or HDF. The source CRS is automatically determined from the first element of the `sourceRDD`. Ensure that the `sourceRDD` is properly initialized and contains valid spatial data before calling this function.

### Output
Returns `SpatialRDD` — a new RDD containing the reprojected spatial data in the specified target CRS. The output retains the spatial characteristics of the original data but is aligned to the new CRS.

### Valid Call Patterns
```scala
val projectedPolygons: RDD[IFeature] = Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))
```

### LLM Instruction Prompt
- Ensure that the `sourceRDD` is a valid `SpatialRDD` and that the `targetCRS` is a correctly defined Coordinate Reference System. The source CRS will be automatically inferred from the data.

### Prompt Snippet
```text
Reproject the spatial RDD to the desired CRS using the reprojectRDD function.
```

### Common Failure Modes
- The `sourceRDD` is empty or not properly initialized, leading to an inability to determine the source CRS.
- The `targetCRS` is not a valid Coordinate Reference System, which may result in runtime errors during reprojection.

### Fix Code Hint
```scala
// Ensure the sourceRDD is initialized and contains valid spatial data
val validSourceRDD: SpatialRDD = // initialize your SpatialRDD here
val targetCRS: CoordinateReferenceSystem = // define your target CRS here
val reprojectedRDD = Reprojector.reprojectRDD(validSourceRDD, targetCRS)
```

## API Test: `rescale`

### Signature
```scala
def rescale(rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def rescale[T: ClassTag](raster: RasterRDD[T], rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
def rescale(newRasterWidth: Int, newRasterHeight: Int): RasterMetadata
def rescale(metadata: Array[RasterMetadata], rasterWidth: Int, rasterHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:542  (+3 more definition site/overload)_

_Source doc:_ Changes the resolution of the raster to the desired resolution without changing tile size or CRS. @param raster the raster to rescale @param rasterWidth the new raster width in terms of pixels @param rasterHeight the new height of the raster layer in terms of pixels @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @return a new raster RDD with the desired width and height

### Goal
The `rescale` function adjusts the resolution of a raster dataset to specified pixel dimensions while maintaining the original tile size and coordinate reference system (CRS).

### Parameters
- `raster` (`RasterRDD[T]`): The input raster dataset that needs to be rescaled. It is expected to be a distributed collection of raster tiles.
- `rasterWidth` (`Int`): The desired width of the output raster in pixels.
- `rasterHeight` (`Int`): The desired height of the output raster in pixels.
- `unifiedRaster` (`Boolean`), default `false`: If set to true, all output tiles will be combined into a single `RasterMetadata`, which can be useful for simplifying the output structure.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to determine the pixel values in the rescaled raster when a target pixel overlaps multiple source pixels. Options include nearest neighbor and average interpolation methods.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, along with the desired pixel dimensions for width and height. The input raster must be properly loaded using supported formats such as GeoTIFF or HDF.

### Output
Returns `RasterRDD[T]` — a new raster dataset with the specified width and height, maintaining the original CRS and tile size. The output is suitable for further geospatial analysis or saving in formats like GeoTIFF.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val rescaled = raster.rescale(360, 180)
rescaled.saveAsGeoTiff("glc_small", GeoTiffWriter.WriteMode -> "compatibility")

val temperature: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val rescaled = temperature.rescale(360, 180, RasterOperationsFocal.InterpolationMethod.Average)
```

### LLM Instruction Prompt
- When calling `rescale`, ensure that the input raster is a valid `RasterRDD[T]` and that the specified width and height are positive integers. The interpolation method should be chosen based on the desired output quality.

### Prompt Snippet
```text
To rescale a raster dataset, use the `rescale` method on a `RasterRDD` with the desired pixel dimensions and optional parameters for unified raster output and interpolation method.
```

### Common Failure Modes
- Providing a negative or zero value for `rasterWidth` or `rasterHeight` will result in an error.
- Attempting to rescale a raster that has not been properly loaded or is empty may lead to runtime exceptions.

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and that the width and height parameters are positive integers before calling `rescale`.
```

## API Test: `reshapeAverage`

### Signature
```scala
def reshapeAverage[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, _numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the average method to determine the final value of each pixel. If one pixel in the answer overlaps multiple pixels in the source, their average is computed. This method should only be used when pixels represent continuous values, e.g., red, infrared, temperature, or vegetation. If the pixels represent categorical values, e.g., land type, then the nearest neighbor method [[reshapeNN]] should be used instead. @param raster the input raster that should be reshaped @param targetMetadataConv a function that returns the desired metadata for source metadata @param _numPartitions the number of partitions of the produces RDD. If not set, it will be the same as the input @return the new raster with the target metadata

### Goal
`reshapeAverage` reshapes a raster dataset by converting its metadata and averaging pixel values when multiple source pixels overlap.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to contain continuous pixel values, such as temperature or vegetation indices.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, _numPartitions: Int`), default `0`: A function that takes the current raster metadata and returns the desired target metadata. The `_numPartitions` parameter specifies the number of partitions for the resulting RDD; if not set, it defaults to the number of partitions of the input raster.

### Input
The input must be a `RasterRDD[T]` containing continuous pixel values, and the target metadata must be defined through the `targetMetadataConv` function. The input raster should be compatible with the expected pixel type for the operation.

### Output
Returns `RasterRDD[T]` — a new raster with the target metadata applied, where pixel values are averaged from the source raster based on the specified reshaping criteria.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata)
```

### LLM Instruction Prompt
- When calling `reshapeAverage`, ensure that the input raster contains continuous pixel values and that the target metadata conversion function is correctly defined.

### Prompt Snippet
```text
Use the `reshapeAverage` function to reshape a raster dataset by averaging pixel values from the source raster based on the specified target metadata.
```

### Common Failure Modes
- The input raster does not contain continuous pixel values, which may lead to incorrect results or runtime errors.
- The `targetMetadataConv` function does not return valid metadata, causing the operation to fail.

### Fix Code Hint
```scala
// Ensure the input raster is of a continuous type and the target metadata conversion function is correctly implemented.
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata)
```

## API Test: `reshapeNN`

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
`reshapeNN` reshapes the input raster's metadata using the nearest neighbor method to match the target metadata specifications.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to be a distributed collection of raster tiles of type `T`, which can represent various pixel types (e.g., `Int`, `Float`, etc.).
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, numPartitions: Int`), default `0`: A function that takes the source `RasterMetadata` and converts it to the target `RasterMetadata`. This function defines how the raster's metadata should be transformed, including aspects like CRS, tiling, and resolution.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, which can be loaded from formats such as GeoTIFF. The `targetMetadataConv` function must be defined to specify how the input raster's metadata should be transformed. The input raster must be compatible with the expected pixel type `T`.

### Output
Returns `RasterRDD[T]` — a new raster with the reshaped metadata according to the specifications provided in the `targetMetadataConv` function. The output retains the pixel type `T` and is suitable for further processing or saving in formats like GeoTIFF.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

### LLM Instruction Prompt
- When calling `reshapeNN`, ensure that the input raster is a valid `RasterRDD[T]` and that the `targetMetadataConv` function is properly defined to convert the raster's metadata.

### Prompt Snippet
```text
Use the `reshapeNN` function to reshape the raster metadata while ensuring the input raster is a valid `RasterRDD[T]` and the conversion function is correctly implemented.
```

### Common Failure Modes
- The input raster is not a valid `RasterRDD[T]`, leading to type mismatch errors.
- The `targetMetadataConv` function does not return a valid `RasterMetadata`, causing runtime exceptions.
- The number of partitions specified exceeds the available resources, leading to performance issues.

### Fix Code Hint
```scala
// Ensure the input raster is correctly loaded and the targetMetadataConv function is defined as follows:
val targetMetadata = RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100)
val reshaped = RasterOperationsFocal.reshapeNN(raster, _ => targetMetadata)
```

## API Test: `retainIndex`

### Signature
```scala
def retainIndex(index: Int): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168_

_Source doc:_ Keep only the parameters that do not have an index or the ones with the given index. In other words, remove any indexed parameter that have a different index than the one given. The index of the parameter is a suffix between square brackets, e.g., param[1] @param index the index to retain @return a new options with the given index retained

### Goal
`retainIndex` filters the parameters in `BeastOptions` to keep only those that do not have an index or those that match the specified index, effectively allowing users to manage indexed parameters in their geospatial processing workflows.

### Parameters
- `index` (`Int`): The index to retain. This should be a non-negative integer that corresponds to the suffix of the parameters you want to keep (e.g., `1` to retain parameters like `key1[1]`).

### Input
The caller must provide a `BeastOptions` instance that may contain parameters with indexed suffixes (e.g., `key1[1]`, `key1[2]`). There are no specific file formats required for this operation, but the parameters should be set in the `BeastOptions` prior to calling `retainIndex`.

### Output
Returns `BeastOptions` — a new instance of `BeastOptions` that contains only the parameters that do not have an index or those that match the specified index. This allows for streamlined access to relevant parameters in subsequent processing steps.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("key1[1]", "val1")
  .set("key1[2]", "val2")
  .set("key3", "val3")
  .set("key4[2]", "val4")
val opts1 = opts.retainIndex(1) // Retains parameters with index 1
val opts2 = opts.retainIndex(2) // Retains parameters with index 2
```

### LLM Instruction Prompt
- When calling `retainIndex`, ensure that the `index` parameter is a valid integer that corresponds to the desired indexed parameters in the `BeastOptions`. The caller should have previously set parameters in the `BeastOptions` instance.

### Prompt Snippet
```text
To filter parameters in BeastOptions, use the retainIndex method with the desired index.
```

### Common Failure Modes
- Calling `retainIndex` on an empty `BeastOptions` instance will return an empty `BeastOptions`.
- Providing an index that does not match any existing indexed parameters will result in a `BeastOptions` that retains only the parameters without an index.

### Fix Code Hint
```scala
// Ensure that the BeastOptions instance has parameters set before calling retainIndex
val opts = new BeastOptions().set("key1[1]", "val1")
val filteredOpts = opts.retainIndex(1) // This will work as expected
```

## API Test: `retile`

### Signature
```scala
def retile(tileWidth: Int, tileHeight: Int)
def retile[T: ClassTag](raster: RasterRDD[T], tileWidth: Int, tileHeight: Int): RasterRDD[T]
def retile(newTileWidth: Int, newTileHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566  (+2 more definition site/overload)_

_Source doc:_ Regrids the given raster to the target tile width and height @param raster the raster to regrid @param tileWidth the new tile width in pixels @param tileHeight the new tile height in pixels @tparam T the type of the pixel values in the raster @return a new raster with the given tile width and height

### Goal
The `retile` function regrids a raster dataset into specified tile dimensions, facilitating efficient processing and analysis of geospatial data.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster dataset that needs to be regridded. It is expected to be a distributed collection of raster tiles.
- `tileWidth` (`Int`): The desired width of the tiles in pixels after regridding. This value should be a positive integer.
- `tileHeight` (`Int`): The desired height of the tiles in pixels after regridding. This value should also be a positive integer.

### Input
The caller must provide a `RasterRDD[T]` that has been loaded from a supported format (e.g., GeoTIFF) and ensure that the raster is compatible with the specified pixel type `T`. The `tileWidth` and `tileHeight` must be positive integers.

### Output
Returns `RasterRDD[T]` — a new raster dataset that has been regridded to the specified tile dimensions, maintaining the same pixel type as the input raster.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")
```

### LLM Instruction Prompt
- When calling `retile`, ensure that the input raster is a valid `RasterRDD[T]` and that both `tileWidth` and `tileHeight` are positive integers.

### Prompt Snippet
```text
To regrid a raster dataset, use the retile function with the desired tile dimensions.
```

### Common Failure Modes
- Providing a `RasterRDD` that is not properly initialized or is empty may lead to runtime errors.
- Specifying non-positive integers for `tileWidth` or `tileHeight` will result in an IllegalArgumentException.

### Fix Code Hint
```scala
// Ensure that tileWidth and tileHeight are positive integers
val tileWidth = 64
val tileHeight = 64
if (tileWidth <= 0 || tileHeight <= 0) {
  throw new IllegalArgumentException("Tile dimensions must be positive integers.")
}
```

## API Test: `run`

### Signature
```scala
override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
```

### Goal
Run the main function using the given user command-line options and Spark context to perform geospatial raster processing operations.

### Parameters
- `opts` (`BeastOptions`): User options for configuring the operation, such as input format, output format, and other processing parameters.
- `inputs` (`Array[String]`): An array of input file paths, which may include GeoTIFFs, HDF files, or other supported formats.
- `outputs` (`Array[String]`): An array of output file paths where the results will be saved, typically in GeoTIFF or CSV format.
- `sc` (`SparkContext`): The Spark context used to run the operation, which is necessary for distributed processing.

### Input
The caller must provide:
- Input files in supported formats (e.g., GeoTIFF, HDF).
- Valid `BeastOptions` that specify how the operation should be configured.
- A properly initialized `SparkContext` that is configured to handle the data size and type.

### Output
Returns `Any` — an optional result of the operation, which may include summary statistics or other relevant output depending on the specific processing task performed.

### Valid Call Patterns
```scala
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

### LLM Instruction Prompt
- Ensure that the `opts` parameter is properly configured with necessary options before calling `run`.
- Provide valid input file paths in the `inputs` array that match the expected formats.
- Specify output paths in the `outputs` array where results will be saved.

### Prompt Snippet
```text
To run the raster processing operation, configure the BeastOptions and provide the input and output file paths along with the SparkContext.
```

### Common Failure Modes
- Providing input file paths that do not exist or are not accessible will result in file not found errors.
- Incorrectly configured `BeastOptions` may lead to unexpected behavior or processing failures.
- The `SparkContext` must be properly initialized; otherwise, the operation will fail to execute.

### Fix Code Hint
```scala
// Ensure the input file exists and is accessible
val inputfile = locateResource("/test.partitions")
if (inputfile == null) {
  throw new FileNotFoundException("Input file not found.")
}

// Initialize BeastOptions with required parameters
val opts = new BeastOptions().set("iformat", "wkt(Geometry)").set("oformat", "csv")

// Call the run method with valid parameters
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

## API Test: `runDuplicateAvoidance`

### Signature
```scala
private[beast] def runDuplicateAvoidance(features: SpatialRDD): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:354_

_Source doc:_ Run the duplicate avoidance technique on the given set of features if it is spatially partitioned using a disjoint partitioner. Otherwise, the input set is returned as-is. @param features the set of features to remove the duplicates from. @return a set of features with all duplicates removed.

### Goal
The `runDuplicateAvoidance` function removes duplicate features from a spatially partitioned `SpatialRDD`, ensuring that the output contains only unique features.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features from which duplicates need to be removed. This input should be spatially partitioned using a disjoint partitioner for the duplicate avoidance technique to be applied effectively.

### Input
The input must be a `SpatialRDD` that is spatially partitioned. If the input is not partitioned correctly, the function will return the input set as-is. The caller should ensure that the `SpatialRDD` is prepared and partitioned appropriately before invoking this function.

### Output
Returns `SpatialRDD` — a new distributed collection of spatial features with all duplicates removed, if applicable. If the input was not spatially partitioned, the original `SpatialRDD` is returned unchanged.

### Valid Call Patterns
```scala
assert(IndexHelper.runDuplicateAvoidance(partitioned1).count() == 10000)
assert(IndexHelper.runDuplicateAvoidance(partitioned2).count() == 10000)
```

### LLM Instruction Prompt
- When calling `runDuplicateAvoidance`, ensure that the input `features` is a `SpatialRDD` that has been spatially partitioned using a disjoint partitioner. If the input is not partitioned, the function will return the input as-is.

### Prompt Snippet
```text
To remove duplicates from a spatially partitioned SpatialRDD, use the runDuplicateAvoidance function. Ensure the input is correctly partitioned for effective duplicate removal.
```

### Common Failure Modes
- The input `SpatialRDD` is not spatially partitioned, resulting in the function returning the original dataset without any duplicates removed.
- The input `features` is null or improperly initialized, leading to runtime errors.

### Fix Code Hint
```scala
// Ensure the SpatialRDD is partitioned before calling runDuplicateAvoidance
val partitionedFeatures = IndexHelper.partitionFeatures2(features, partitioner)
val uniqueFeatures = IndexHelper.runDuplicateAvoidance(partitionedFeatures)
```

## API Test: `saveAsCSVPoints`

### Signature
```scala
def saveAsCSVPoints(filename: String, xColumn: Int = 0, yColumn: Int = 1, delimiter: Char = ',', header: Boolean = true): Unit
def saveAsCSVPoints(rdd: JavaSpatialRDD, filename: String, xColumn: Int, yColumn: Int, delimiter: Char, header: Boolean): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:212  (+1 more definition site/overload)_

_Source doc:_ Save features to a CSV or text-delimited file. This method should be used only for point features. @param filename the name of the output file @param xColumn the index of the column that contains the x-coordinate in the output file @param yColumn the index of the column that contains the y-coordinate in the output file @param delimiter the delimiter in the output file, comma by default @param header whether to write a header line, true by default

### Goal
The `saveAsCSVPoints` function saves point feature data to a CSV or text-delimited file format, allowing for easy export and analysis of geospatial point data.

### Parameters
- `filename` (`String`): The name of the output file where the point features will be saved. This should include the desired file extension, typically `.csv`.
- `xColumn` (`Int`), default `0`: The index of the column that contains the x-coordinate (longitude) in the output file. The default value is `0`, indicating the first column.
- `yColumn` (`Int`), default `1`: The index of the column that contains the y-coordinate (latitude) in the output file. The default value is `1`, indicating the second column.
- `delimiter` (`Char`), default `','`: The character used to separate values in the output file. The default is a comma (`,`), but it can be set to other characters like a tab or semicolon if needed.
- `'`: This parameter appears to be incorrectly listed in the API facts and does not have a defined meaning or expected values.
- `header` (`Boolean`), default `true`: A flag indicating whether to write a header line in the output file. The default value is `true`, meaning a header will be included.

### Input
The caller must provide a valid `SpatialRDD` containing point features. The output file must be specified with a valid filename, and the x and y column indices must correspond to the correct columns in the data. The data should be structured such that the specified columns contain valid coordinate values.

### Output
Returns `Unit` — This indicates that the function does not return a value but performs the action of saving the data to the specified file.

### Valid Call Patterns
```scala
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)
```

### LLM Instruction Prompt
- Ensure that the `filename` is a valid string representing the output file path, and that the `xColumn` and `yColumn` indices are within the bounds of the data structure. The `delimiter` should be a single character, and the `header` should be a boolean value.

### Prompt Snippet
```text
To save point features to a CSV file, use the `saveAsCSVPoints` method with the appropriate parameters for filename, x and y column indices, delimiter, and header option.
```

### Common Failure Modes
- Providing an invalid filename (e.g., an empty string or a path that cannot be written to) will result in an error.
- Specifying `xColumn` or `yColumn` indices that are out of bounds for the data will lead to an `IndexOutOfBoundsException`.
- Using a delimiter that is not a single character may cause unexpected formatting issues in the output file.

### Fix Code Hint
```scala
// Ensure the filename is valid and the column indices are within the range of the data
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)
```

## API Test: `saveAsGeoJSON`

### Signature
```scala
def saveAsGeoJSON(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsGeoJSON(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:201  (+1 more definition site/overload)_

_Source doc:_ Save features in GeoJSON format @param filename the output filename

### Goal
The `saveAsGeoJSON` function saves geospatial features in GeoJSON format, allowing for easy sharing and visualization of spatial data.

### Parameters
- `filename` (`String`): The name of the output file where the GeoJSON data will be saved. It should include the `.geojson` file extension.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for controlling the behavior of the save operation, such as formatting and compression settings.

### Input
The input must be a valid `SpatialRDD` or `JavaSpatialRDD` containing geospatial features. The data should be prepared and processed as needed before calling this function. The output filename must be specified and should end with `.geojson`.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output file will be in GeoJSON format, which is a widely used format for encoding a variety of geographic data structures.

### Valid Call Patterns
```scala
records.saveAsGeoJSON("output.geojson")
```

### LLM Instruction Prompt
- Ensure that the `filename` parameter is a valid string ending with `.geojson`.
- Use the `opts` parameter to customize the save operation if necessary, but it is optional.

### Prompt Snippet
```text
To save your geospatial features as a GeoJSON file, use the `saveAsGeoJSON` method with the appropriate filename and options.
```

### Common Failure Modes
- The specified `filename` does not end with `.geojson`, which may lead to unexpected behavior or errors.
- The input data is not a valid `SpatialRDD` or `JavaSpatialRDD`, resulting in a runtime error.

### Fix Code Hint
```scala
// Ensure the filename is correct and the input data is a valid SpatialRDD
records.saveAsGeoJSON("output.geojson")
```

## API Test: `saveAsGeoTiff`

### Signature
```scala
def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit
def saveAsGeoTiff[T](rasterRDD: RDD[ITile[T]], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:476  (+1 more definition site/overload)_

### Goal
The `saveAsGeoTiff` function saves a RasterRDD as a set of GeoTIFF files, enabling the output of processed raster data in a widely-used geospatial format.

### Parameters
- `rasterRDD` (`RDD[ITile[T]]`): The input raster data represented as a distributed collection of tiles, where each tile contains pixel values of type `T`. This is the raster data that will be saved as GeoTIFF files.
- `outPath` (`String`): The file path where the output GeoTIFF files will be written. This should be a valid path in the file system where the application has write permissions.
- `opts` (`BeastOptions`): Additional options for saving the GeoTIFF file, such as compression settings or metadata configurations. Defaults to a new instance of `BeastOptions`.

### Input
The caller must provide a valid `RDD[ITile[T]]` containing the raster data to be saved, a string representing the output file path, and optionally, a `BeastOptions` instance for additional configurations. The raster data must be properly loaded and processed before calling this function.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the raster data to the specified GeoTIFF files.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")

val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperatureK.filterPixels(_ > 300).saveAsGeoTiff("temperature_high")
```

### LLM Instruction Prompt
- When calling `saveAsGeoTiff`, ensure that the raster data is properly loaded and processed, and that the output path is valid and writable.

### Prompt Snippet
```text
To save your processed raster data as GeoTIFF files, use the `saveAsGeoTiff` method with the appropriate rasterRDD and output path.
```

### Common Failure Modes
- Attempting to save to a path where the application does not have write permissions will result in an error.
- If the `rasterRDD` is empty or improperly formatted, the function may fail to execute correctly.
- Providing an invalid or non-existent output path may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the output path is valid and writable
val outputPath = "valid/output/path/temperature_f"
temperatureF.saveAsGeoTiff(outputPath)
```

## API Test: `saveAsIndex`

### Signature
```scala
def saveAsIndex(indexPath: String, oformat: String = "rtree"): Unit
def saveAsIndex(partitionedRDD: JavaPartitionedSpatialRDD, indexPath: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92  (+1 more definition site/overload)_

### Goal
The `saveAsIndex` function writes a spatially partitioned RDD as a set of files, one for each partition, and adds a master file that stores information about the partitions.

### Parameters
- `indexPath` (`String`): The output path where the index files will be written. This should be a valid file system path where the user has write permissions.
- `oformat` (`String`), default `"rtree"`: The format of the index to be created. The default value is `"rtree"`, which indicates that an R-tree index will be generated.

### Input
The caller must provide a spatially partitioned RDD, which can be created using methods like `spatialPartition`. The output path specified in `indexPath` must be valid and accessible. The input data should be compatible with the indexing format specified by `oformat`.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the index files to the specified path.

### Valid Call Patterns
```scala
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
```

### LLM Instruction Prompt
- Ensure that the `indexPath` is a valid file system path and that the necessary permissions are in place for writing files.
- Use the appropriate partitioned RDD as input to the `saveAsIndex` function.

### Prompt Snippet
```text
To save a spatially partitioned RDD as an index, use the `saveAsIndex` method with a valid output path and desired index format.
```

### Common Failure Modes
- Attempting to save to a non-existent or inaccessible `indexPath` will result in an error.
- Using an incompatible RDD that is not spatially partitioned will lead to runtime exceptions.

### Fix Code Hint
```scala
Ensure that the RDD is properly partitioned using a spatial partitioner before calling `saveAsIndex`, and verify that the output path is correct and writable.
```

## API Test: `saveAsKML`

### Signature
```scala
def saveAsKML(filename: String): Unit
def saveAsKML(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:86  (+1 more definition site/overload)_

_Source doc:_ Save features in KML format @param filename the name of the output file

### Goal
The `saveAsKML` function saves geospatial features in KML format, which is commonly used for representing geographic data in applications like Google Earth.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial features that you want to save in KML format. This RDD should contain geometries and associated attributes.
- `filename` (`String`): The name of the output KML file, including the desired file path and extension (e.g., "output.kml").

### Input
The caller must provide a `JavaSpatialRDD` containing the spatial features to be saved and a valid filename as a string. The filename must end with the `.kml` extension to ensure proper file format.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output is a KML file saved to the specified location, which can be used in various geospatial applications.

### Valid Call Patterns
```scala
records.saveAsKML("output.kml")
```

### LLM Instruction Prompt
- Ensure that the `filename` parameter is a valid string ending with `.kml` and that the `rdd` parameter is a properly initialized `JavaSpatialRDD` containing spatial features.

### Prompt Snippet
```text
To save your spatial features in KML format, use the `saveAsKML` method with a valid filename and a `JavaSpatialRDD` containing your data.
```

### Common Failure Modes
- Attempting to save without providing a valid `JavaSpatialRDD` will result in an error.
- Providing a filename that does not end with `.kml` may lead to unexpected behavior or file format issues.

### Fix Code Hint
```scala
// Ensure your RDD is properly initialized and your filename is correct
val spatialData: JavaSpatialRDD = // initialize your JavaSpatialRDD
spatialData.saveAsKML("output.kml")
```

## API Test: `saveAsShapefile`

### Signature
```scala
def saveAsShapefile(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsShapefile(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:194  (+1 more definition site/overload)_

_Source doc:_ Save features as a shapefile @param filename the output filename

### Goal
The `saveAsShapefile` function saves geospatial features from an RDD as a shapefile, enabling users to export processed spatial data for use in GIS applications.

### Parameters
- `filename` (`String`): The name of the output shapefile, including the `.shp` extension (e.g., `"output.shp"`).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for controlling the behavior of the shapefile saving process, such as specifying the coordinate reference system or other metadata.

### Input
The input must be a valid RDD containing geospatial features, which can be created from various sources such as CSV points or other spatial data formats. The RDD should be properly formatted to ensure compatibility with shapefile standards.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value, and the output is saved directly to the specified shapefile on the filesystem.

### Valid Call Patterns
```scala
records.saveAsShapefile("output.shp")
```

### LLM Instruction Prompt
- Ensure that the RDD contains valid geospatial features before calling `saveAsShapefile`.
- Specify a valid filename with a `.shp` extension to avoid errors during the saving process.

### Prompt Snippet
```text
To save your geospatial features as a shapefile, use the `saveAsShapefile` method with a valid filename, such as `records.saveAsShapefile("output.shp")`.
```

### Common Failure Modes
- Attempting to save without a valid RDD of geospatial features will result in an error.
- Providing a filename without the `.shp` extension may lead to unexpected behavior or failure to save the file correctly.

### Fix Code Hint
```scala
// Ensure the RDD is properly populated with geospatial features and specify a valid filename.
records.saveAsShapefile("output.shp")
```

## API Test: `saveAsWKTFile`

### Signature
```scala
def saveAsWKTFile(filename: String, wktColumn: Int, delimiter: Char = '\t', header: Boolean = true): Unit
def saveAsWKTFile(rdd: JavaSpatialRDD, filename: String, wktColumn: Int, delimiter: Char, header: Boolean): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:79  (+1 more definition site/overload)_

_Source doc:_ Save features to a CSV file where the geometry is encoded in WKT format @param filename the name of the output file @param wktColumn the index of the column that contains the WKT attribute @param delimiter the delimiter between attributes, tab by default @param header whether to write a header line or not, true by default

### Goal
The `saveAsWKTFile` function saves features from a spatial dataset to a CSV file, encoding geometries in Well-Known Text (WKT) format.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial dataset containing features to be saved, which must include a column with geometries in WKT format.
- `filename` (`String`): The name of the output CSV file where the features will be saved.
- `wktColumn` (`Int`): The index of the column in the dataset that contains the WKT representation of the geometries.
- `delimiter` (`Char`): The character used to separate values in the CSV file, with a tab character (`'\t'`) as the default.
- `header` (`Boolean`): A flag indicating whether to include a header line in the CSV file, defaulting to `true`.

### Input
The caller must provide a `JavaSpatialRDD` containing features with at least one column that holds geometries in WKT format. The `filename` must be a valid path for the output CSV file, and `wktColumn` must be a valid index corresponding to the WKT column in the dataset.

### Output
Returns `Unit` — indicating that the operation has completed successfully without returning any value. The output is a CSV file containing the features, with geometries encoded in WKT format.

### Valid Call Patterns
```scala
records.saveAsWKTFile("output.csv", 0, '\t', false)
```

### LLM Instruction Prompt
When calling `saveAsWKTFile`, ensure that the `JavaSpatialRDD` contains a valid WKT column and that the filename is correctly specified for the output CSV.

### Prompt Snippet
```text
To save your spatial features to a CSV file with geometries in WKT format, use the `saveAsWKTFile` method, ensuring the correct column index for WKT and a valid filename.
```

### Common Failure Modes
- Providing an invalid `wktColumn` index that does not exist in the dataset will result in an `IndexOutOfBoundsException`.
- Specifying a `filename` that is not writable or does not have the correct permissions will lead to an `IOException`.

### Fix Code Hint
```scala
// Ensure the wktColumn index is within the bounds of the dataset's columns
if (wktColumn < 0 || wktColumn >= records.getNumColumns) {
  throw new IllegalArgumentException("Invalid wktColumn index.")
}
```

## API Test: `saveFeatures`

### Signature
```scala
def saveFeatures(features: SpatialRDD, oFormat: String, outPath: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:123_

_Source doc:_ Saves the given set of features to the output using the provided output format. @param features the set of features to store to the output @param oFormat the output format to use for writing @param outPath the path to write the output to @param opts user options to configure the writer

### Goal
The `saveFeatures` function saves a set of geospatial features to a specified output path in a chosen format, facilitating the storage of processed spatial data.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features that are to be saved. This should contain the geometries and associated attributes of the features.
- `oFormat` (`String`): The format in which to save the features, such as "geojson" or "shapefile". This determines how the data will be serialized and stored.
- `outPath` (`String`): The file path where the output will be written. This should include the desired filename and extension corresponding to the output format.
- `opts` (`BeastOptions`): User-defined options to configure the writer, which may include settings for compression, formatting, or other output specifications.

### Input
The caller must provide a valid `SpatialRDD` containing features, a string indicating the output format, a valid file path for the output, and an instance of `BeastOptions` to configure the writing process. The output format must be compatible with the features being saved.

### Output
Returns `Unit` — this indicates that the function completes its operation without returning a value, signifying that the features have been successfully written to the specified output path.

### Valid Call Patterns
```scala
val outputPath = new File(scratchDir, "test.geojson.bz2")
val features: RDD[IFeature] = sparkContext.parallelize(Seq(
  Feature.create(null, GeometryReader.DefaultGeometryFactory.createPoint(new CoordinateXY(1, 2)))
))
SpatialWriter.saveFeatures(features, "geojson", outputPath.getPath, new BeastOptions())
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` and that the `oFormat` matches the expected output format for the features being saved. The `outPath` must be a valid file path, and `opts` should be properly configured.

### Prompt Snippet
```text
Save the features to the specified output path in the desired format using the saveFeatures function.
```

### Common Failure Modes
- Providing an unsupported output format in `oFormat` may result in an error.
- Specifying an invalid or inaccessible `outPath` can lead to file writing failures.
- If `features` is empty or not a valid `SpatialRDD`, the function may not execute as expected.

### Fix Code Hint
```scala
Ensure that the output path is valid and that the output format is supported. Check that the features are correctly populated in the `SpatialRDD` before calling saveFeatures.
```

## API Test: `saveIndex2`

### Signature
```scala
def saveIndex2(partitionFeatures: SpatialRDD, path: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:541_

_Source doc:_ Saves a partitioned RDD to disk. Each partition is stored to a separate file and an additional master file that stores the partition information. @param partitionFeatures a set of partitioned features @param path the path to store the files @param opts additional options for storing the data

### Goal
`saveIndex2` saves a partitioned RDD of spatial features to disk, creating separate files for each partition along with a master file for partition information.

### Parameters
- `partitionFeatures` (`SpatialRDD`): A set of partitioned spatial features that are to be saved. This RDD must be partitioned using a spatial partitioner.
- `path` (`String`): The file path where the partitioned files will be stored. This should be a valid directory path on the filesystem.
- `opts` (`BeastOptions`): Additional options for storing the data, which may include format specifications or other storage parameters.

### Input
The caller must provide a `SpatialRDD` that has been partitioned, a valid file path as a string, and a `BeastOptions` instance with any necessary options for the save operation.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output consists of multiple files saved to the specified path, including individual files for each partition and a master file containing partition metadata.

### Valid Call Patterns
```scala
IndexHelper.saveIndex2(partitionedFeatures, outPath.getPath, BeastOptions("oformat" -> "wkt(0)"))
```

### LLM Instruction Prompt
- Ensure that `partitionFeatures` is a properly partitioned `SpatialRDD`.
- Provide a valid file path in `path` where the files can be written.
- Use a correctly configured `BeastOptions` instance for `opts`.

### Prompt Snippet
```text
To save a partitioned RDD of spatial features, use the `saveIndex2` method with the appropriate parameters.
```

### Common Failure Modes
- Providing a non-partitioned RDD as `partitionFeatures` will result in an error.
- Specifying an invalid or inaccessible file path in `path` will cause a failure during the save operation.
- Omitting necessary options in `opts` may lead to unexpected behavior or defaults that do not meet user requirements.

### Fix Code Hint
```scala
Ensure that `partitionFeatures` is partitioned using a spatial partitioner and that the `path` is a valid writable directory.
```

## API Test: `saveTiles`

### Signature
```scala
def saveTiles(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, opts: BeastOptions): Unit
def saveTiles(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:453  (+1 more definition site/overload)_

_Source doc:_ Save an RDD of tiles to the given output @param tiles   the set of tiles to save @param outPath the path to save the tiles to

### Goal
`saveTiles` saves a distributed collection of raster tiles to a specified output path in a format defined by the provided options.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): A distributed collection of tiles, where each tile is associated with a unique identifier (Long) and contains intermediate vector tile data (IntermediateVectorTile).
- `outPath` (`String`): The file path where the tiles will be saved. This should be a valid path in the file system accessible by the Spark cluster.
- `opts` (`BeastOptions`): Configuration options for the saving process, which may include parameters such as compression settings or output format specifications.

### Input
The caller must provide:
- A valid `JavaPairRDD` or `RDD` containing tiles, which must be of type `IntermediateVectorTile`.
- A valid output path as a string where the tiles will be saved.
- An instance of `BeastOptions` that specifies any additional options for saving the tiles.

### Output
Returns `Unit` — this indicates that the operation is performed without returning a value. The tiles are saved to the specified output path in the format defined by the `opts`.

### Valid Call Patterns
```scala
value.saveTiles(tiles, "output/path/to/tiles", beastOptions)
```

### LLM Instruction Prompt
- Ensure that the `tiles` RDD is properly populated with `IntermediateVectorTile` data before calling `saveTiles`.
- Verify that the `outPath` is a valid and accessible path in the file system.
- Provide a correctly configured `BeastOptions` instance to customize the saving process.

### Prompt Snippet
```text
To save your raster tiles, use the `saveTiles` method with the appropriate parameters: a JavaPairRDD of tiles, a valid output path, and BeastOptions for configuration.
```

### Common Failure Modes
- **Invalid Output Path**: If the `outPath` does not exist or is not writable, the operation will fail.
- **Incorrect Tile Type**: If the `tiles` RDD does not contain `IntermediateVectorTile` data, a runtime error will occur.
- **Misconfigured BeastOptions**: Providing incompatible or incorrect options in `BeastOptions` may lead to unexpected behavior during the save operation.

### Fix Code Hint
```scala
// Ensure the output path is valid and accessible
val validPath = "output/path/to/tiles"
val tiles: JavaPairRDD[Long, IntermediateVectorTile] = // your code to create tiles
val options: BeastOptions = // your code to configure options

// Call saveTiles with the correct parameters
value.saveTiles(tiles, validPath, options)
```

## API Test: `saveTilesCompact`

### Signature
```scala
def saveTilesCompact(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, _opts: BeastOptions): Unit
def saveTilesCompact(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, _opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:495  (+1 more definition site/overload)_

_Source doc:_ A wrapper around [[saveTilesCompact()]]. Saves all the given tiles to a ZIP file. @param tiles   the set of tiles to visualize @param outPath the path of the output ZIP file @param _opts   additional options that were used for visualization.

### Goal
`saveTilesCompact` saves a collection of raster tiles into a compressed ZIP file for efficient storage and visualization.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): A distributed collection of tiles, where each tile is represented as a key-value pair. The key is a unique identifier (Long) for the tile, and the value is an `IntermediateVectorTile` containing the tile's data.
- `outPath` (`String`): The file path where the output ZIP file will be saved. This should be a valid path in the file system where the application has write permissions.
- `_opts` (`BeastOptions`): Additional options for visualization, which may include parameters like thresholds or styling options that affect how the tiles are processed or visualized.

### Input
The caller must provide:
- A valid `JavaPairRDD` or `RDD` containing the tiles to be saved.
- A string representing a valid output file path for the ZIP file.
- An instance of `BeastOptions` with any necessary visualization parameters.

### Output
Returns `Unit` — this indicates that the function completes its operation without returning a value. The output is a ZIP file containing the serialized tiles, which can be used for visualization.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
```

### LLM Instruction Prompt
- Ensure that the `tiles` parameter is a valid `JavaPairRDD` or `RDD` containing the appropriate tile data.
- Provide a valid `outPath` where the ZIP file can be saved.
- Include any necessary options in the `_opts` parameter to customize the visualization.

### Prompt Snippet
```text
MVTDataVisualizer.saveTilesCompact(tiles, "output_path.zip", options)
```

### Common Failure Modes
- Providing an invalid or inaccessible `outPath` may result in a file write error.
- If `tiles` is empty or not properly formatted, the function may not produce the expected output.
- Missing or incorrect options in `_opts` may lead to unexpected visualization results.

### Fix Code Hint
```scala
// Ensure the output path is valid and accessible
val validOutPath = "path/to/output.zip"
MVTDataVisualizer.saveTilesCompact(tiles, validOutPath, opts)
```

## API Test: `seek`

### Signature
```scala
private def seek(pos: Long, newSource: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:37_

### Goal
The `seek` function allows the user to move to a specified position in the input stream, enabling efficient reading of data from that point.

### Parameters
- `pos` (`Long`): The position in the input stream to seek to. This value should be within the bounds of the data being read.
- `newSource` (`Boolean`): A flag indicating whether to load a new chunk of data if the specified position is outside the currently buffered chunk. If `true`, a disk seek will be performed.

### Input
The caller must provide a valid position (`pos`) within the input stream and a boolean value for `newSource`. The input stream must be properly initialized and opened before calling this function.

### Output
Returns `Boolean` — `true` if the seek operation was successful, and `false` otherwise.

### Valid Call Patterns
```scala
val success: Boolean = bufStream.seek(100, true)
```

### LLM Instruction Prompt
- Ensure that the `pos` parameter is a valid position within the input stream and that the stream is open before calling `seek`. The `newSource` parameter should be set based on whether a new chunk needs to be loaded.

### Prompt Snippet
```text
To seek to a specific position in the input stream, use the `seek` method with the desired position and a flag indicating if a new source should be loaded.
```

### Common Failure Modes
- Attempting to seek to a position that is out of bounds of the input stream may result in a failure.
- If the input stream is not properly initialized or opened, the seek operation will not work.

### Fix Code Hint
```scala
// Ensure the input stream is open and the position is valid before calling seek
if (inputStream.isOpen && pos >= 0 && pos < inputStream.length) {
  val success: Boolean = inputStream.seek(pos, true)
} else {
  throw new IllegalArgumentException("Invalid position or stream not open.")
}
```

## API Test: `selectFiles`

### Signature
```scala
def selectFiles(fileSystem: FileSystem, dir: String, range: Geometry): Array[String]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:233_

_Source doc:_ Selects all the raster files that could potentially overlap the given query range from a directory of files. If that directory contains an index file, i.e., "_index.csv", then this index is used to prune files that are not relevant. If no index file is there, then all files are returned. @param fileSystem the file system at which the raster files exist @param dir the directory that contains the raster files @param range the query range to limit the files @return the list of files that potentially overlap the given query range

### Goal
`selectFiles` identifies and returns a list of raster files from a specified directory that may intersect with a given geometric query range, optimizing the search using an index file if available.

### Parameters
- `fileSystem` (`FileSystem`): The file system instance that provides access to the storage where the raster files are located. This is typically obtained from the Spark context's Hadoop configuration.
- `dir` (`String`): The path to the directory containing the raster files. This directory should be accessible within the provided file system.
- `range` (`Geometry`): A geometric shape representing the query area. This defines the spatial extent for which overlapping raster files are to be selected.

### Input
The caller must provide:
- A valid `FileSystem` instance that is configured to access the directory containing the raster files.
- A string representing the directory path where the raster files are stored.
- A `Geometry` object that defines the spatial range for the query, which must be compatible with the coordinate reference system of the raster files.

### Output
Returns `Array[String]` — an array of file paths (as strings) that represent the raster files which potentially overlap with the specified query range. The paths are relative to the provided directory.

### Valid Call Patterns
```scala
val dir = new File(scratchDir, "dir").toString
val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dir, geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly instantiated from the Spark context's Hadoop configuration.
- Verify that the `dir` points to a valid directory containing raster files.
- Confirm that the `range` is a valid `Geometry` object that accurately represents the desired spatial query.

### Prompt Snippet
```text
Select raster files from the specified directory that overlap with the given geometry range using the selectFiles function.
```

### Common Failure Modes
- Providing an invalid or inaccessible directory path in `dir`, which results in an empty array or an error.
- Using a `Geometry` object that does not match the coordinate reference system of the raster files, leading to incorrect results or no files being returned.
- Not having an index file when many raster files are present, which may lead to performance issues as all files will be returned.

### Fix Code Hint
```scala
// Ensure the directory exists and contains raster files, and that the Geometry is correctly defined.
val dir = new File(scratchDir, "dir").toString
if (new File(dir).exists()) {
    val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dir, geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
} else {
    println("Directory does not exist or is inaccessible.")
}
```

## API Test: `set`

### Signature
```scala
def set(key: String, value: Any): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:83_

_Source doc:_ Set a key to any value by converting it to string @param key key name @param value value @return

### Goal
The `set` function allows users to define configuration options by associating a string key with a corresponding value, which can be used in various geospatial processing tasks.

### Parameters
- `key` (`String`): The name of the configuration option to set. This should be a valid string that represents the option's identifier.
- `value` (`Any`): The value to associate with the specified key. This can be any type, but it will be converted to a string for storage.

### Input
The caller must provide a valid key as a string and a value of any type. There are no specific file formats required for this function, as it is used for setting options rather than processing data directly.

### Output
Returns `BeastOptions` — an instance of `BeastOptions` that contains the updated configuration settings, allowing for further customization of geospatial processing tasks.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
val optsWithStroke = opts.set("stroke", "blue")
```

### LLM Instruction Prompt
- When calling `set`, ensure that the key is a valid string and the value is of any type that can be converted to a string. The returned `BeastOptions` instance can be used for further configuration.

### Prompt Snippet
```text
Set a configuration option using the set method of BeastOptions, ensuring the key is a valid string and the value can be any type.
```

### Common Failure Modes
- Providing a null or empty string for the `key` parameter may lead to unexpected behavior or errors.
- Using a value that cannot be converted to a string may result in runtime exceptions.

### Fix Code Hint
```scala
// Ensure the key is not null or empty and the value is of a type that can be converted to a string.
val opts = new BeastOptions()
if (key.nonEmpty) {
  opts.set(key, value)
} else {
  throw new IllegalArgumentException("Key must not be empty")
}
```

## API Test: `setBoolean`

### Signature
```scala
def setBoolean(key: String, value: Boolean): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:141_

_Source doc:_ Set key to a boolean value @param key @param value @return

### Goal
The `setBoolean` function sets a specified configuration key to a boolean value within the context of BeastOptions, allowing for the customization of behavior in raster processing tasks.

### Parameters
- `key` (`String`): The name of the configuration option to be set. This should correspond to a valid key recognized by the BeastOptions configuration system.
- `value` (`Boolean`): The boolean value to assign to the specified key. This can be either `true` or `false`, depending on the desired configuration.

### Input
The caller must provide a valid configuration key as a string and a boolean value. There are no specific file formats required for this function, as it operates on configuration settings rather than data files.

### Output
Returns `BeastOptions` — an instance of BeastOptions that reflects the updated configuration with the specified key set to the provided boolean value.

### Valid Call Patterns
```scala
value.setBoolean("fs.file.impl.disable.cache", true)
```

### LLM Instruction Prompt
- When calling `setBoolean`, ensure that the key is a valid configuration option recognized by the BeastOptions system and that the value is a boolean (`true` or `false`).

### Prompt Snippet
```text
Set a configuration option in BeastOptions using setBoolean, ensuring the key is valid and the value is a boolean.
```

### Common Failure Modes
- Providing an invalid key that is not recognized by the BeastOptions configuration may result in unexpected behavior or errors.
- Attempting to set a key with a non-boolean value will lead to a type mismatch error.

### Fix Code Hint
```scala
// Ensure the key is a valid configuration option and the value is a boolean
val options = new BeastOptions().setBoolean("fs.file.impl.disable.cache", true)
```

## API Test: `setLong`

### Signature
```scala
def setLong(key: String, value: Long): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:122_

_Source doc:_ Set a key to a long value @param key @param value @return

### Goal
`setLong` sets a specified configuration key to a long integer value within the `BeastOptions`, which is used for configuring various parameters in geospatial processing tasks.

### Parameters
- `key` (`String`): The name of the configuration option to be set. This should be a valid key recognized by the `BeastOptions` class.
- `value` (`Long`): The long integer value to assign to the specified key. This value should be appropriate for the configuration option being set.

### Input
The caller must provide a valid key as a string and a long integer value. The key must correspond to a configuration option that can accept a long value.

### Output
Returns `BeastOptions` — an instance of `BeastOptions` with the specified key set to the provided long value, allowing for further configuration in geospatial processing tasks.

### Valid Call Patterns
```scala
new BeastOptions().setLong("threshold", 0)
```

### LLM Instruction Prompt
- When calling `setLong`, ensure that the key is a valid configuration option and that the value is a long integer that makes sense for the context of the operation being configured.

### Prompt Snippet
```text
Set a configuration option in BeastOptions using setLong, ensuring the key is valid and the value is appropriate.
```

### Common Failure Modes
- Providing an invalid key that is not recognized by `BeastOptions`.
- Setting a value that is not a long integer, which may lead to runtime errors.

### Fix Code Hint
```scala
// Ensure the key is valid and the value is a long integer
val options = new BeastOptions().setLong("validKey", 12345L)
```

## API Test: `setPixelValue`

### Signature
```scala
def setPixelValue(i: Int, j:Int, value: T): Unit
def setPixelValue(i: Int, j: Int, value: T): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:147  (+1 more definition site/overload)_

_Source doc:_ Sets the value of the given pixel @param i the column position of the pixel @param j the row position of the pixel @param value the value to set at the given pixel

### Goal
`setPixelValue` updates the value of a specific pixel in a raster tile at the given column and row indices.

### Parameters
- `i` (`Int`): The column position of the pixel, expected to be a non-negative integer within the bounds of the raster's width.
- `j` (`Int`): The row position of the pixel, expected to be a non-negative integer within the bounds of the raster's height.
- `value` (`T`): The value to set at the specified pixel, which must match the pixel type of the raster (e.g., `Float`, `Array[Float]`).

### Input
The caller must provide a raster tile instance that has been initialized and is capable of holding pixel values of type `T`. The indices `i` and `j` must be within the valid range of the raster dimensions.

### Output
Returns `Unit` — this indicates that the operation has been performed successfully without returning a value.

### Valid Call Patterns
```scala
tile1.setPixelValue(0, 0, 0.5f)
tile1.setPixelValue(1, 0, 0.25f)
tile1.setPixelValue(0, 1, Array(3.00f, 2.1f))
```

### LLM Instruction Prompt
- Ensure that the pixel indices `i` and `j` are within the bounds of the raster dimensions before calling `setPixelValue`.
- The `value` must be of the correct type that matches the raster's pixel type.

### Prompt Snippet
```text
Set the pixel value at column i and row j of the raster tile to the specified value using setPixelValue.
```

### Common Failure Modes
- Attempting to set a pixel value with indices `i` or `j` that are out of bounds will result in an `IndexOutOfBoundsException`.
- Providing a `value` of an incorrect type that does not match the raster's pixel type will lead to a type mismatch error.

### Fix Code Hint
```scala
// Ensure indices are within bounds and value type matches the raster's pixel type
if (i >= 0 && i < rasterWidth && j >= 0 && j < rasterHeight) {
    tile.setPixelValue(i, j, value) // Ensure value is of type T
} else {
    throw new IllegalArgumentException("Pixel indices are out of bounds.")
}
```

## API Test: `setup`

### Signature
```scala
override def setup(opts: BeastOptions): Unit
override def setup(ss: SparkSession, opts: BeastOptions): Unit
override def setup(sc: SparkContext, opts: BeastOptions): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DataExplorerServer.scala:91  (+2 more definition site/overload)_

### Goal
The `setup` function initializes the processing environment for RDPro by configuring the Spark context and Beast options.

### Parameters
- `sc` (`SparkContext`): The Spark context used for distributed data processing. It is expected to be properly initialized and configured to handle the data size and type.
- `opts` (`BeastOptions`): Configuration options specific to the Beast framework, which may include settings for data processing, logging, and other operational parameters.

### Input
The caller must provide a valid `SparkContext` and a `BeastOptions` instance. The Spark context must be initialized and running, and the Beast options should be set according to the specific requirements of the processing task.

### Output
Returns `Unit` — this indicates that the setup process has completed successfully without returning any value.

### Valid Call Patterns
```scala
val sc: SparkContext = // initialize SparkContext
val opts: BeastOptions = new BeastOptions() // configure BeastOptions
setup(sc, opts)
```

### LLM Instruction Prompt
- Ensure that the `SparkContext` is properly initialized before calling `setup`.
- Provide a valid instance of `BeastOptions` with the necessary configurations.

### Prompt Snippet
```text
val sc: SparkContext = // your Spark context initialization
val opts: BeastOptions = new BeastOptions() // your Beast options setup
value.setup(sc, opts)
```

### Common Failure Modes
- Attempting to call `setup` without an initialized `SparkContext` will result in a runtime error.
- Providing improperly configured `BeastOptions` may lead to unexpected behavior during processing.

### Fix Code Hint
```scala
// Ensure SparkContext is initialized
val sc: SparkContext = SparkContext.getOrCreate()
// Ensure BeastOptions is properly configured
val opts: BeastOptions = new BeastOptions()
// Call setup with valid parameters
value.setup(sc, opts)
```

## API Test: `shapefile`

### Signature
```scala
def shapefile(filename: String) : SpatialRDD
def shapefile(filename: String) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:76  (+1 more definition site/overload)_

_Source doc:_ Reads features from an Esri Shapefile(c) @param filename the name of the .shp file, a compressed ZIP file that contains shapefiles, or a directory that contains shapefiles or ZIP files. @return an RDD of features

### Goal
The `shapefile` function loads spatial features from an Esri Shapefile or a directory containing shapefiles into a distributed dataset for geospatial analysis.

### Parameters
- `filename` (`String`): The path to the .shp file, a compressed ZIP file containing shapefiles, or a directory that contains shapefiles or ZIP files.

### Input
The caller must provide a valid path to an Esri Shapefile or a ZIP file containing shapefiles. The input must be accessible to the Spark context, and the file must conform to the Esri Shapefile format specifications.

### Output
Returns `SpatialRDD` — a distributed dataset containing the spatial features read from the shapefile, which can be used for further geospatial operations and analyses.

### Valid Call Patterns
```scala
val records = sparkContext.shapefile("input.zip")
// Or
val records = sparkContext.shapefile("input.shp")

val buildings = sc.shapefile("MSBuildings_data_index.zip")
println(buildings.summary)
```

### LLM Instruction Prompt
- When calling `shapefile`, ensure that the provided filename points to a valid shapefile or a ZIP file containing shapefiles. The file must be accessible to the Spark context.

### Prompt Snippet
```text
To load spatial features from a shapefile, use the `shapefile` method with the appropriate filename.
```

### Common Failure Modes
- Providing an invalid path or filename that does not point to a valid shapefile or ZIP file will result in a file not found error.
- Attempting to load a shapefile that does not conform to the Esri specifications may lead to parsing errors.

### Fix Code Hint
```scala
Ensure the filename points to a valid .shp file or a ZIP file containing shapefiles, and that the file is accessible to the Spark context.
```

## API Test: `sierpinski`

### Signature
```scala
def sierpinski(cardinality: Long): JavaSpatialRDD
def sierpinski(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:127  (+1 more definition site/overload)_

_Source doc:_ Generate data from the Sierpinski distribution @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `sierpinski` function generates a specified number of records from the Sierpinski distribution, which is useful for creating spatial datasets in geospatial analysis.

### Parameters
- `cardinality` (`Long`): The number of records to generate. This value should be a positive integer representing how many points from the Sierpinski distribution you want to create.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and running. The `cardinality` parameter must be a valid positive long integer.

### Output
Returns `JavaSpatialRDD` or `SpatialRDD` — an RDD containing the generated spatial data points from the Sierpinski distribution, which can be used for further geospatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .sierpinski(1000)
```

### LLM Instruction Prompt
- When calling `sierpinski`, ensure that the `cardinality` parameter is a positive long integer and that the Spark context is properly initialized.

### Prompt Snippet
```text
Generate 1000 records from the Sierpinski distribution using the following call: sc.generateSpatialData.sierpinski(1000).
```

### Common Failure Modes
- Providing a negative or zero value for `cardinality` will result in an error, as the function expects a positive integer.
- Attempting to call `sierpinski` without an initialized Spark context will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the Spark context is initialized and use a positive integer for cardinality
val spatialData: SpatialRDD = sc.generateSpatialData.sierpinski(1000)
```

## API Test: `simplifyGeometry`

### Signature
```scala
private[davinci] def simplifyGeometry(geometry: Geometry): LiteGeometry
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:207_

_Source doc:_ Takes a geometry that is already projected to the image space of this tile and returns a simplified lite geometry that satisfies the following: - If the geometry does not overlap with the tile boundaries, null is returned - Coordinates are snapped to the nearest integer - Parts of the geometry that are outside the tile boundaries can be simplified without affecting the portion that is within the tile boundaries. - If there are consecutive coordinates that snap to the same pixel, only one can be kept @param geometry the input geometry @return the simplified geometry or null if empty

### Goal
The `simplifyGeometry` function simplifies a given geometry by reducing its complexity while ensuring it fits within the boundaries of the associated raster tile.

### Parameters
- `geometry` (`Geometry`): The input geometry that is already projected to the image space of the tile. This can include various geometric shapes such as points, lines, or polygons.

### Input
The caller must provide a `Geometry` object that is projected to the image space of the tile. If the geometry does not overlap with the tile boundaries, the function will return null.

### Output
Returns `LiteGeometry` — a simplified version of the input geometry that retains only the necessary points and is adjusted to fit within the tile boundaries. If the input geometry does not overlap with the tile, null is returned.

### Valid Call Patterns
```scala
val interTile = new IntermediateVectorTile(10, 0)
val point = GeometryReader.DefaultGeometryFactory.createPoint(new Coordinate(5, 5))
val simplifiedPoint = interTile.simplifyGeometry(point)
```

### LLM Instruction Prompt
- Ensure that the input geometry is projected to the image space of the tile and overlaps with the tile boundaries before calling `simplifyGeometry`.

### Prompt Snippet
```text
Call `simplifyGeometry` with a projected geometry that overlaps with the tile boundaries to obtain a simplified lite geometry.
```

### Common Failure Modes
- The function will return null if the input geometry does not overlap with the tile boundaries.
- If the geometry consists of consecutive coordinates that snap to the same pixel, only one coordinate will be retained, which may lead to unexpected simplification results.

### Fix Code Hint
```scala
// Ensure the geometry overlaps with the tile boundaries before calling simplifyGeometry
val geometry: Geometry = ... // Load or create your geometry
if (geometry.overlaps(tileBoundary)) {
    val simplifiedGeometry = interTile.simplifyGeometry(geometry)
} else {
    // Handle the case where the geometry does not overlap
}
```

## API Test: `size`

### Signature
```scala
def size: Long
override def size: Long
override def size: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:41  (+2 more definition site/overload)_

_Source doc:_ Size in bytes

### Goal
Retrieve the size of the raster data in bytes.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded into memory using RDPro methods, such as `sc.geoTiff(...)`. The dataset must be properly initialized and accessible.

### Output
Returns `Long` — the size of the raster dataset in bytes.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val sizeInBytes: Long = raster.size
```

### LLM Instruction Prompt
- Ensure that the raster dataset is loaded and initialized before calling `size`.

### Prompt Snippet
```text
To get the size of the raster dataset in bytes, use the `size` method on the loaded raster RDD.
```

### Common Failure Modes
- Calling `size` on an uninitialized or empty raster dataset will result in an error.
- Attempting to call `size` on a non-raster RDD will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling size
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val sizeInBytes: Long = raster.size // This should work if raster is properly initialized
```

## API Test: `skipDuplicateAvoidance`

### Signature
```scala
private[beast] def skipDuplicateAvoidance(rdd: RDD[_]): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:535_

_Source doc:_ If the given RDD is based on a SpatialFileRDD, it causes it to skip duplicate avoidance. @param rdd the rdd to skip duplicate avoidance for

### Goal
The `skipDuplicateAvoidance` function allows a user to process a `SpatialFileRDD` without applying duplicate record avoidance, ensuring that all records, including duplicates, are counted in subsequent operations.

### Parameters
- `rdd` (`RDD[_]`): The RDD to skip duplicate avoidance for. This should be an instance of `SpatialFileRDD` that may contain duplicate records.

### Input
The input must be a `SpatialFileRDD` that has been created from a partitioned file containing repeated records. The RDD should be properly initialized and populated with spatial data.

### Output
Returns `Unit` — this indicates that the function does not return any value but modifies the behavior of the RDD to include duplicate records in its operations.

### Valid Call Patterns
```scala
SpatialFileRDD.skipDuplicateAvoidance(features)
```

### LLM Instruction Prompt
- Ensure that the RDD passed to `skipDuplicateAvoidance` is an instance of `SpatialFileRDD` and contains duplicate records that you want to include in processing.

### Prompt Snippet
```text
Call `skipDuplicateAvoidance` on a `SpatialFileRDD` to ensure that duplicate records are included in the RDD's operations.
```

### Common Failure Modes
- Calling `skipDuplicateAvoidance` on an RDD that is not a `SpatialFileRDD` will result in a runtime error.
- If the RDD does not contain duplicate records, the function will still execute but may not have any observable effect.

### Fix Code Hint
```scala
// Ensure the RDD is a SpatialFileRDD and contains duplicates before calling skipDuplicateAvoidance
val features = new SpatialFileRDD(sparkContext, indexPath.getPath, Seq(SpatialFileRDD.InputFormat -> "envelopek(2)"))
SpatialFileRDD.skipDuplicateAvoidance(features)
```

## API Test: `slidingWindow`

### Signature
```scala
def slidingWindow[T: ClassTag, U: ClassTag](raster: RasterRDD[T], w: Int, f: (Array[T], Array[Boolean]) => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:711_

_Source doc:_ Performs a sliding window calculation for a window of size (2w + 1) &times; (2w + 1) given an integer value w. The user-defined window calculation function takes all values in the window ordered in row-major order. Additionally, a Boolean array of the same size is passed to indicate which values are defined and which are not. The Boolean array is useful for two scenarios. 1. When the window is near the edge of the raster, there must be some undefined values outside the raster. 2. Some pixel values in raster might be undefined, e.g., due to cloud coverage. *Note*: This function will only work correctly if all input tiles have the same raster metadata. @param raster the input raster to process @param w the radius of the square window. The window size will be (2w + 1) &times; (2w + 1) @param f the function to perform the calculation. @tparam T the type of values in the input raster @tparam U the type of output values (the result of the user-defined function). @return a new raster with the same dimensions as the input after applying the window function.

### Goal
The `slidingWindow` function computes a user-defined operation over a square window of pixel values in a raster, allowing for handling of undefined values.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster to process, which contains pixel values of type `T`. This raster must have consistent metadata across all tiles.
- `w` (`Int`): The radius of the square window. The total window size will be (2w + 1) &times; (2w + 1), meaning it will include `w` pixels in each direction from the center pixel.
- `f` (`(Array[T], Array[Boolean]) => U`): A user-defined function that takes an array of pixel values from the window and a corresponding Boolean array indicating which values are defined. It returns a value of type `U`, which represents the result of the calculation performed on the defined pixel values.

### Input
The caller must provide a `RasterRDD[T]` containing pixel values, an integer `w` that defines the window size, and a function `f` that specifies how to process the pixel values. The input raster must have consistent metadata across all tiles, and the pixel type `T` must be compatible with the operations defined in the function `f`.

### Output
Returns `RasterRDD[U]` — a new raster with the same dimensions as the input raster, where each pixel value is the result of applying the user-defined function `f` over the corresponding sliding window.

### Valid Call Patterns
```scala
val smoothedRaster: RasterRDD[Double] = RasterOperationsFocal.slidingWindow(raster, 1, (values: Array[Int], defined) => {
  var sum: Int = 0
  var count: Int = 0
  for (i <- values.indices; if defined(i)) {
    sum += values(i)
    count += 1
  }
  sum.toDouble / count
})
```

### LLM Instruction Prompt
When calling `slidingWindow`, ensure that the raster input has consistent metadata, the window size is a positive integer, and the function provided correctly handles the pixel values and their defined states.

### Prompt Snippet
```text
val result = raster.slidingWindow(1, (values: Array[Int], defined) => {
  // Your calculation logic here
})
```

### Common Failure Modes
- Providing a raster with inconsistent metadata across tiles will lead to incorrect results or runtime errors.
- Using a non-positive integer for the window size `w` will result in an invalid window size and may cause exceptions.
- The user-defined function `f` must handle cases where some pixel values are undefined; failing to do so may lead to runtime errors or incorrect calculations.

### Fix Code Hint
```scala
// Ensure the raster has consistent metadata and that w is a positive integer
val validRaster: RasterRDD[Int] = // Load or create a valid raster
val windowSize: Int = 1 // Ensure this is positive
val result = validRaster.slidingWindow(windowSize, (values: Array[Int], defined) => {
  // Implement logic to handle undefined values
})
```

## API Test: `sparkContext`

### Signature
```scala
def sparkContext: SparkContext
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:38_

### Goal
Retrieve the current `SparkContext` instance, which is essential for executing distributed computations in Spark.

### Parameters
_None._

### Input
No specific input is required as this method does not take any parameters.

### Output
Returns `SparkContext` — an instance of Spark's `SparkContext`, which represents the connection to a Spark cluster and is used to create RDDs, accumulators, and broadcast variables.

### Valid Call Patterns
```scala
val sc: SparkContext = value.sparkContext
```

### LLM Instruction Prompt
- When calling `sparkContext`, ensure that a Spark session is already initialized and configured properly to handle the data size and type.

### Prompt Snippet
```text
Retrieve the SparkContext instance to perform distributed raster processing operations.
```

### Common Failure Modes
- Attempting to call `sparkContext` without a properly initialized Spark session may result in a `NullPointerException` or similar errors indicating that the Spark context is not available.

### Fix Code Hint
```scala
// Ensure Spark is initialized before calling sparkContext
val spark = SparkSession.builder().appName("MyApp").getOrCreate()
val sc = spark.sparkContext
```

## API Test: `sparkSession`

### Signature
```scala
override def sparkSession: SparkSession
def sparkSession: SparkSession
```
_Source: beast/spatialtest/src/main/scala/edu/ucr/cs/bdlab/test/BeastSpatialTest.scala:27  (+1 more definition site/overload)_

### Goal
Retrieve the current `SparkSession` instance, which is essential for executing distributed raster processing tasks in RDPro.

### Parameters
_None._

### Input
No specific data or file formats are required as input. However, the Spark environment must be properly configured and running to utilize the `SparkSession`.

### Output
Returns `SparkSession` — an instance of Spark's `SparkSession`, which serves as the entry point for programming Spark with the Dataset and DataFrame API. It encapsulates the Spark context and allows for the execution of Spark jobs.

### Valid Call Patterns
```scala
val session: SparkSession = value.sparkSession
```

### LLM Instruction Prompt
- When calling `sparkSession`, ensure that the Spark environment is initialized and running. This method does not take any parameters and should be called on an instance of the class that contains the method.

### Prompt Snippet
```text
To obtain the current SparkSession, use the method `value.sparkSession` in your RDPro application.
```

### Common Failure Modes
- Attempting to call `sparkSession` when the Spark environment is not initialized will result in an error.
- Calling `sparkSession` from a non-Spark context may lead to runtime exceptions.

### Fix Code Hint
```scala
Ensure that your Spark environment is properly set up and running before calling `sparkSession`.
```

## API Test: `spatialFile`

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
- `opts` (`BeastOptions`), default `new BeastOptions`: Options for reading the spatial data, such as specifying delimiters for CSV files or other format-specific settings.

### Input
The caller must provide a valid file path as `filename`, which should point to a file or directory containing spatial data in a supported format (e.g., CSV, GeoJSON). The function can handle multiple files if a directory is specified. The input data must be correctly formatted according to the specified or detected spatial format.

### Output
Returns `SpatialRDD` — a distributed collection of spatial records that can be used for further geospatial operations, such as joins, transformations, or analyses.

### Valid Call Patterns
```scala
val parks = sparkContext.spatialFile("parks_index", "wkt")
val lakes = sparkContext.spatialFile("lakes_index", "wkt")
val records = sparkContext.spatialFile("input.gpx", "gpx")
```

### LLM Instruction Prompt
When calling `spatialFile`, ensure that the `filename` points to a valid file or directory containing spatial data, and specify the correct format if auto-detection is not desired.

### Prompt Snippet
```text
To load spatial data, use the spatialFile method with the appropriate filename and format. For example:
val parks = sparkContext.spatialFile("parks_index", "wkt")
```

### Common Failure Modes
- Providing an invalid file path or a non-existent file will result in a `FileNotFoundException`.
- Specifying an unsupported format may lead to errors during the loading process.
- If the input data is malformed or does not conform to the expected structure for the specified format, the function may throw parsing errors.

### Fix Code Hint
```scala
Ensure the file path is correct and the file exists. Check the format of the data and ensure it matches the specified or auto-detected format.
```

## API Test: `spatialJoin`

### Signature
```scala
def spatialJoin(rdd2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, method: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(partitionedRDD2: PartitionedSpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, mbrCount: LongAccumulator = null): RDD[(IFeature, IFeature)]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD, predicate: SpatialJoinAlgorithms.ESJPredicate, algorithm: SpatialJoinAlgorithms.ESJDistributedAlgorithm): JavaPairRDD[IFeature, IFeature]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD): JavaPairRDD[IFeature, IFeature]
def spatialJoin(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, joinMethod: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, joinMethod: ESJDistributedAlgorithm, mbrCount: LongAccumulator, opts: BeastOptions): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:146  (+5 more definition site/overload)_

_Source doc:_ The main entry point for spatial join operations. Performs a spatial join between the given two inputs and returns an RDD of pairs of matching features. This method is a transformation. However, if the [[ESJDistributedAlgorithm.PBSM]] is used, the MBR of the two inputs has to be calculated first which runs a reduce action on each dataset even if the output of the spatial join is not used. You can specify a specific spatial join method through the [[joinMethod]] parameter. If not specified, an algorithm will be picked automatically based on the following rules. - If both datasets are spatially partitioned, the distributed join [[ESJDistributedAlgorithm.DJ]] algorithm is used. - If the product of the number of partitions of both datasets is less than [[SparkContext.defaultParallelism]], then the block nested loop join is used [[ESJDistributedAlgorithm.BNLJ]] - If at least one dataset is partition, then the repartition join is used [[ESJDistributedAlgorithm.REPJ]] - If none of the above, then the partition based spatial merge join is used [[ESJDistributedAlgorithm.PBSM]] @param r1 the first (left) dataset @param r2 the second (right) dataset @param joinPredicate the join predicate. The default is [[ESJPredicate.Intersects]] which finds all non-disjoint features @param joinMethod the join algorithm. If not specified the algorithm automatically chooses an algorithm based on the heuristic described above. @param mbrCount an (optional) accumulator to count the number of MBR tests during the algorithm. @return an RDD that contains pairs of matching features.

### Goal
The `spatialJoin` function performs a spatial join between two `SpatialRDD` datasets, returning pairs of matching features based on a specified join predicate.

### Parameters
- `r1` (`SpatialRDD`): The first (left) dataset containing spatial features to be joined.
- `r2` (`SpatialRDD`): The second (right) dataset containing spatial features to be joined.
- `joinPredicate` (`ESJPredicate`), default `ESJPredicate.Intersects`: The condition used to determine how features from the two datasets are matched; defaults to finding all non-disjoint features.
- `joinMethod` (`ESJDistributedAlgorithm`), default `null`: The algorithm used for the join operation; if not specified, an appropriate method is chosen based on the characteristics of the datasets.
- `mbrCount` (`LongAccumulator`), default `null`: An optional accumulator to count the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for configuring the join operation, allowing for customization of behavior.

### Input
The input consists of two `SpatialRDD` datasets that must be properly initialized and can be derived from spatial data formats such as WKT files. Both datasets should be spatially partitioned if applicable, and the join predicate should be relevant to the spatial characteristics of the features.

### Output
Returns `RDD[(IFeature, IFeature)]` — an RDD containing pairs of matching features from the two input datasets based on the specified join predicate.

### Valid Call Patterns
```scala
val joinResults = dataset1.spatialJoin(dataset2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)
val sjResults: RDD[(IFeature, IFeature)] = matchedPolygons.spatialJoin(matchedPoints, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)
```

### LLM Instruction Prompt
- Ensure that both input datasets are of type `SpatialRDD` and are properly initialized before calling `spatialJoin`. The join predicate should be relevant to the spatial characteristics of the features being joined.

### Prompt Snippet
```text
val joinResults = dataset1.spatialJoin(dataset2, ESJPredicate.Intersects)
```

### Common Failure Modes
- Attempting to join datasets that are not of type `SpatialRDD` will result in a compilation error.
- If the datasets are not spatially partitioned when required, the join may not perform optimally or may fail to execute.
- Using an invalid `joinPredicate` that does not correspond to the spatial characteristics of the features may yield unexpected results.

### Fix Code Hint
```scala
// Ensure both datasets are of type SpatialRDD and properly initialized
val dataset1: SpatialRDD = ...
val dataset2: SpatialRDD = ...
val joinResults = dataset1.spatialJoin(dataset2)
```

## API Test: `spatialJoinBNLJ`

### Signature
```scala
def spatialJoinBNLJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null) : RDD[(IFeature, IFeature)]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:418  (+2 more definition site/overload)_

_Source doc:_ Runs a spatial join between the two given RDDs using the block-nested-loop join algorithm. @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @return

### Goal
`spatialJoinBNLJ` performs a spatial join between two `SpatialRDD` datasets using the block-nested-loop join algorithm, allowing for the combination of spatial features based on a specified joining condition.

### Parameters
- `r1` (`SpatialRDD`): The first set of spatial features to be joined. This RDD should contain geometries that will be evaluated against the geometries in `r2`.
- `r2` (`SpatialRDD`): The second set of spatial features to be joined. This RDD should also contain geometries that will be evaluated against the geometries in `r1`.
- `joinPredicate` (`ESJPredicate`): The condition that determines how features from `r1` and `r2` are matched. This predicate defines the spatial relationship (e.g., intersects, contains) that must hold true for a join to occur.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of minimum bounding rectangle (MBR) tests performed during the join operation. This can be useful for performance monitoring.

### Input
The input consists of two `SpatialRDD` datasets (`r1` and `r2`) containing spatial features, and a valid `joinPredicate` that specifies the spatial relationship for the join. The datasets must be properly initialized and populated with spatial geometries before calling this function.

### Output
Returns `RDD[(IFeature, IFeature)]` — a distributed collection of pairs of features, where each pair consists of a feature from `r1` and a feature from `r2` that satisfy the specified `joinPredicate`. The output represents the results of the spatial join operation.

### Valid Call Patterns
```scala
val results = SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate = ESJPredicate.MBRIntersects)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are initialized as `SpatialRDD` containing valid spatial features.
- Provide a valid `joinPredicate` that defines the spatial relationship for the join.
- Optionally, use a `LongAccumulator` for `numMBRTests` to monitor performance.

### Prompt Snippet
```text
To perform a spatial join using the block-nested-loop join algorithm, call `spatialJoinBNLJ` with two `SpatialRDD` datasets and a valid `joinPredicate`.
```

### Common Failure Modes
- The `SpatialRDD` datasets `r1` and `r2` are empty, resulting in an output of zero pairs.
- The `joinPredicate` is not compatible with the geometries in `r1` and `r2`, leading to unexpected results or no matches.
- The `numMBRTests` accumulator is not properly initialized, which may lead to null pointer exceptions if accessed.

### Fix Code Hint
```scala
// Ensure both RDDs are populated and the joinPredicate is correctly defined
val r1: SpatialRDD = sparkContext.parallelize(Seq(/* your features here */))
val r2: SpatialRDD = sparkContext.parallelize(Seq(/* your features here */))
val joinPredicate = ESJPredicate.MBRIntersects
val results = SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate)
```

## API Test: `spatialJoinDJ`

### Signature
```scala
def spatialJoinDJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:461_

_Source doc:_ Distributed join algorithm between spatially partitioned RDDs @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @param numMBRTests   a counter that will contain the number of MBR tests @return a pair RDD for joined features

### Goal
`spatialJoinDJ` performs a distributed join operation between two spatially partitioned RDDs based on a specified join predicate, enabling efficient spatial analysis.

### Parameters
- `r1` (`SpatialRDD`): The first set of spatial features to be joined. This RDD should contain geometries that will be evaluated against the geometries in `r2`.
- `r2` (`SpatialRDD`): The second set of spatial features to be joined. Similar to `r1`, this RDD should contain geometries that will be evaluated against those in `r1`.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the criteria for joining features from `r1` with features from `r2`. This predicate determines how the spatial relationship between the features is evaluated.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional counter that tracks the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation. This can be useful for performance monitoring.

### Input
The caller must provide two `SpatialRDD` instances containing spatial features (geometries) and a valid `ESJPredicate` that specifies the join criteria. The `numMBRTests` parameter is optional and can be used for performance tracking.

### Output
Returns `RDD[(IFeature, IFeature)]` — a pair RDD containing the joined features from `r1` and `r2`. Each element in the RDD is a tuple of `IFeature` instances representing the features that satisfy the join predicate.

### Valid Call Patterns
```scala
val joinedFeatures: RDD[(IFeature, IFeature)] = value.spatialJoinDJ(firstSpatialRDD, secondSpatialRDD, joinPredicate)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are instances of `SpatialRDD` containing valid spatial features. The `joinPredicate` must be properly defined to specify the joining criteria.

### Prompt Snippet
```text
To perform a spatial join between two datasets, use the spatialJoinDJ function with appropriate SpatialRDDs and a join predicate.
```

### Common Failure Modes
- Providing non-`SpatialRDD` types for `r1` or `r2` will result in a compilation error.
- An improperly defined `joinPredicate` may lead to unexpected results or an empty output RDD.
- If `numMBRTests` is used, ensure it is properly initialized as a `LongAccumulator` to avoid null pointer exceptions.

### Fix Code Hint
```scala
// Ensure both RDDs are of type SpatialRDD and the joinPredicate is correctly defined.
val numTests: LongAccumulator = sc.longAccumulator("MBR Tests")
val joinedFeatures: RDD[(IFeature, IFeature)] = value.spatialJoinDJ(firstSpatialRDD, secondSpatialRDD, joinPredicate, numTests)
```

## API Test: `spatialJoinIntersectsPlaneSweepFeatures`

### Signature
```scala
private[beast] def spatialJoinIntersectsPlaneSweepFeatures[T1 <: IFeature, T2 <: IFeature] (r: Array[T1], s: Array[T2], dupAvoidanceMBR: EnvelopeNDLite, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): TraversableOnce[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:244_

_Source doc:_ Runs a plane-sweep algorithm between the given two arrays of input features and returns an iterator of pairs of features. @param r the first set of features @param s the second set of features @param dupAvoidanceMBR the duplicate avoidance MBR to run the reference point technique. @param joinPredicate the join predicate to match features @param numMBRTests an (optional) accumulator to count the number of MBR tests @tparam T1 the type of the first dataset @tparam T2 the type of the second dataset @return an iterator over pairs of features

### Goal
`spatialJoinIntersectsPlaneSweepFeatures` performs a spatial join between two sets of geospatial features using a plane-sweep algorithm, identifying pairs of features that intersect based on a specified join predicate.

### Parameters
- `r` (`Array[T1]`): An array of features representing the first dataset to be joined. Each feature must implement the `IFeature` interface.
- `s` (`Array[T2]`): An array of features representing the second dataset to be joined. Each feature must also implement the `IFeature` interface.
- `dupAvoidanceMBR` (`EnvelopeNDLite`): A minimum bounding rectangle (MBR) used to avoid duplicate feature matches during the join process. This helps in optimizing the join operation.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the criteria for joining features. It specifies how the features from the two datasets should be compared (e.g., whether they intersect).
- `numMBRTests` (`LongAccumulator`): An optional accumulator that counts the number of MBR tests performed during the join operation, useful for performance monitoring.

### Input
The caller must provide two arrays of features (`r` and `s`) that implement the `IFeature` interface. The `dupAvoidanceMBR` must be a valid `EnvelopeNDLite` object that defines the area for duplicate avoidance. The `joinPredicate` must be a valid `ESJPredicate` that specifies the join criteria. The `numMBRTests` can be set to `null` if the count of MBR tests is not needed.

### Output
Returns `TraversableOnce[(IFeature, IFeature)]` — an iterator over pairs of features that intersect according to the specified join predicate. Each pair consists of one feature from the first dataset and one from the second dataset.

### Valid Call Patterns
```scala
val r = List(
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 10.0, 10.0, 10.1, 10.1)),
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 3.0, 1.0, 5.0, 3.0))
)
val s = List(
  Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 2.0, 0.0, 4.0, 2.0))
)
val results = SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(r.toArray, s.toArray,
  new EnvelopeNDLite(2, 2.0, 0.0, 5.0, 3.0), ESJPredicate.Intersects, null)
```

### LLM Instruction Prompt
- Ensure that the input arrays `r` and `s` contain features that implement the `IFeature` interface. The `dupAvoidanceMBR` must be a valid `EnvelopeNDLite`, and the `joinPredicate` must be a valid `ESJPredicate`. The `numMBRTests` can be `null` if not needed.

### Prompt Snippet
```text
Call `spatialJoinIntersectsPlaneSweepFeatures` with two arrays of features, a duplicate avoidance MBR, a join predicate, and an optional accumulator for MBR tests.
```

### Common Failure Modes
- Providing arrays `r` or `s` that do not contain features implementing the `IFeature` interface will result in a compilation error.
- Using an invalid `dupAvoidanceMBR` that does not conform to the `EnvelopeNDLite` type will lead to runtime exceptions.
- Specifying an unsupported `joinPredicate` may cause the function to behave unexpectedly or throw an error.

### Fix Code Hint
```scala
Ensure that both input arrays contain valid `IFeature` instances and that the `dupAvoidanceMBR` and `joinPredicate` are correctly instantiated before calling the function.
```

## API Test: `spatialJoinPBSM`

### Signature
```scala
def spatialJoinPBSM(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate) : JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:297  (+2 more definition site/overload)_

_Source doc:_ Performs a partition-based spatial-merge (PBSM) join as explained in the following paper. Jignesh M. Patel, David J. DeWitt: Partition Based Spatial-Merge Join. SIGMOD Conference 1996: 259-270 https://doi.org/10.1145/233269.233338 @param r1            the first dataset @param r2            the second dataset @param joinPredicate the join predicate @param numMBRTests   (output) the number of MBR tests done during the algorithm @param opts          Additional options for the PBSM algorithm @return a pair RDD for joined features

### Goal
`spatialJoinPBSM` performs a partition-based spatial-merge join between two spatial datasets, allowing for efficient spatial queries and analysis.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset to be joined, which contains features with spatial attributes.
- `r2` (`SpatialRDD`): The second spatial dataset to be joined, which also contains features with spatial attributes.
- `joinPredicate` (`ESJPredicate`): The spatial relationship used to determine how features from `r1` and `r2` are matched (e.g., intersection, containment).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of minimum bounding rectangle (MBR) tests performed during the join operation.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options for configuring the PBSM algorithm, allowing for customization of the join process.

### Input
The caller must provide two `SpatialRDD` datasets (`r1` and `r2`) containing spatial features. The datasets should be properly initialized and populated with spatial data. The `joinPredicate` must be a valid spatial relationship defined in `ESJPredicate`. The `numMBRTests` can be provided if the caller wishes to track MBR tests.

### Output
Returns `RDD[(IFeature, IFeature)]` — a pair RDD containing joined features from both datasets based on the specified `joinPredicate`. Each element in the RDD is a tuple of features that satisfy the join condition.

### Valid Call Patterns
```scala
val geometryFactory = GeometryReader.DefaultGeometryFactory
val dataset1: SpatialRDD = sparkContext.parallelize(Seq(
  Feature.create(null, new PointND(geometryFactory, 2, 1.0, 1.0))
))
val dataset2: SpatialRDD = sparkContext.parallelize(Seq(
  Feature.create(null, new EnvelopeND(geometryFactory, 2, 0.0, 0.0, 2.0, 2.0))
))
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

### LLM Instruction Prompt
- Ensure that both `r1` and `r2` are valid `SpatialRDD` instances containing spatial features. The `joinPredicate` must be a valid spatial relationship. If using `numMBRTests`, it should be initialized as a `LongAccumulator`.

### Prompt Snippet
```text
To perform a spatial join using the PBSM method, ensure you have two SpatialRDD datasets and a valid join predicate. Call the function as follows:
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

### Common Failure Modes
- The datasets `r1` and `r2` are empty, resulting in an empty output RDD.
- The `joinPredicate` is not a valid spatial relationship, causing a runtime error.
- Mismatched spatial data types in `r1` and `r2`, leading to unexpected results or errors.

### Fix Code Hint
```scala
// Ensure both datasets are populated and the join predicate is valid
val dataset1: SpatialRDD = // initialize with valid spatial features
val dataset2: SpatialRDD = // initialize with valid spatial features
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

## API Test: `spatialJoinRepJ`

### Signature
```scala
def spatialJoinRepJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:488_

_Source doc:_ Repartition join algorithm between two datasets: r1 is spatially disjoint partitioned and r2 is not @param r1 the first dataset @param r2 the second dataset @param joinPredicate the join predicate @param numMBRTests an optional accumulator that counts the number of MBR tests @return an RDD of pairs of matching features

### Goal
`spatialJoinRepJ` performs a repartition join between two spatial datasets, where the first dataset is spatially disjoint partitioned, allowing for efficient matching of features based on a specified join predicate.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset that is partitioned in a way that ensures its features do not overlap spatially. This dataset should contain features that will be matched against those in the second dataset.
- `r2` (`SpatialRDD`): The second spatial dataset that may contain overlapping features. This dataset is not required to be partitioned in a specific manner.
- `joinPredicate` (`ESJPredicate`): A predicate that defines the conditions under which features from `r1` and `r2` should be joined. This predicate is crucial for determining the matching criteria.
- `numMBRTests` (`LongAccumulator`), default `null`: An optional accumulator that tracks the number of Minimum Bounding Rectangle (MBR) tests performed during the join operation. This can be useful for performance monitoring.

### Input
The caller must provide two `SpatialRDD` datasets (`r1` and `r2`) that contain spatial features. The first dataset (`r1`) must be spatially disjoint partitioned, while the second dataset (`r2`) can have overlapping features. The `joinPredicate` must be defined to specify how the features from both datasets relate to each other.

### Output
Returns `RDD[(IFeature, IFeature)]` — an RDD containing pairs of matching features from the two input datasets based on the specified join predicate. Each pair consists of one feature from `r1` and one feature from `r2`.

### Valid Call Patterns
```scala
val result: RDD[(IFeature, IFeature)] = value.spatialJoinRepJ(firstDataset, secondDataset, joinCondition)
```

### LLM Instruction Prompt
- Ensure that the first dataset (`r1`) is spatially disjoint partitioned and the second dataset (`r2`) can contain overlapping features. Define a valid `joinPredicate` to specify the matching criteria.

### Prompt Snippet
```text
Call `spatialJoinRepJ` with two spatial datasets, ensuring the first is spatially disjoint and the second can overlap. Provide a valid join predicate for matching features.
```

### Common Failure Modes
- Providing datasets where `r1` is not spatially disjoint partitioned may lead to incorrect results or runtime errors.
- An invalid or poorly defined `joinPredicate` can result in no matches being found or unexpected behavior during the join operation.

### Fix Code Hint
```scala
Ensure that the first dataset is properly partitioned and that the join predicate is correctly defined to match the intended features.
```

## API Test: `spatialPartition`

### Signature
```scala
def spatialPartition(spatialPartitioner: SpatialPartitioner): SpatialRDD
def spatialPartition(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): SpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, spatialPartitioner: SpatialPartitioner): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: Int): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: Int, opts: BeastOptions): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner]): JavaPartitionedSpatialRDD
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:179  (+5 more definition site/overload)_

_Source doc:_ Partition a set of features according to a created spatial partitioner @param spatialPartitioner the partitioner for the data @return partitioned records

### Goal
The `spatialPartition` function partitions a set of spatial features into distinct segments based on a specified spatial partitioner, optimizing data locality for geospatial analysis.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input spatial dataset that contains features to be partitioned. This dataset should be loaded from a supported format such as CSV points or other spatial data formats.
- `spatialPartitioner` (`SpatialPartitioner`): An initialized spatial partitioner that defines how the input features will be divided into partitions. This could be a grid-based partitioner or any custom partitioner that extends the `SpatialPartitioner` class.

### Input
The caller must provide a `JavaSpatialRDD` containing spatial features, which can be loaded from formats like CSV points. The spatial partitioner must be properly initialized before being passed to the function.

### Output
Returns `JavaPartitionedSpatialRDD` — a partitioned version of the input `JavaSpatialRDD`, where the features are organized into partitions according to the specified spatial partitioner. This output is suitable for further spatial operations and analyses.

### Valid Call Patterns
```scala
val testFile = makeFileCopy("/test111.points")
val data: JavaSpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

### LLM Instruction Prompt
- When calling `spatialPartition`, ensure that the input `JavaSpatialRDD` is properly initialized and that the `SpatialPartitioner` is created based on the characteristics of the input data.

### Prompt Snippet
```text
val partitionedFeatures = features.spatialPartition(partitioner)
```

### Common Failure Modes
- Attempting to call `spatialPartition` with an uninitialized or incompatible `SpatialPartitioner` may result in runtime errors.
- If the input `JavaSpatialRDD` is empty or improperly formatted, the function may not produce the expected partitioned output.

### Fix Code Hint
```scala
// Ensure the spatialPartitioner is correctly initialized and matches the input data characteristics
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner], NumPartitions(Fixed, features.getNumPartitions), _ => 1, "disjoint" -> true)
val partitionedFeatures = features.spatialPartition(partitioner)
```

## API Test: `splitGeometryAcrossDateLine`

### Signature
```scala
def splitGeometryAcrossDateLine(geometry: Geometry): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/GeometryQuadSplitter.scala:122_

_Source doc:_ Splits the given geometry across the dateline (-180 or +180 meridian) to avoid errors. 1. This function assumes that the input consists of a polygon with a single ring (outer shell). 1. We assume that the width cannot be greater than 180 degrees. 1. If the geometry width is greater than 180, we assume that it crosses the dateline. 1. To fix the geometry, we rotate all negative longitudes by adding 360. 1. After that, we split the geometry by intersecting it with the western hemisphere once and with the eastern hemisphere once. @param geometry the input geometry to detect and split @return Either the same geometry if it does not cross the dateline, or the same one split into two if it crosses the dateline.

### Goal
The `splitGeometryAcrossDateLine` function is designed to ensure that geometries crossing the dateline are correctly split into separate geometries for accurate geospatial analysis.

### Parameters
- `geometry` (`Geometry`): The input geometry, which is expected to be a polygon with a single ring (outer shell). This function will process the geometry to determine if it crosses the dateline.

### Input
The caller must provide a `Geometry` object that represents a polygon. The geometry should not have a width greater than 180 degrees, as this function assumes that any such geometry crosses the dateline.

### Output
Returns `Geometry` — This value represents either the original geometry if it does not cross the dateline or a new geometry that is split into two separate geometries if it does cross the dateline.

### Valid Call Patterns
```scala
val geometry = GeometryReader.DefaultGeometryFactory.createPolygon(
  Array(new Coordinate(170, 50), new Coordinate(-170, 60), new Coordinate(-170, 50), new Coordinate(170, 50))
)
val split = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)
```

### LLM Instruction Prompt
- When calling `splitGeometryAcrossDateLine`, ensure that the input geometry is a polygon with a single ring and does not exceed a width of 180 degrees. 

### Prompt Snippet
```text
To split a geometry across the dateline, use the `splitGeometryAcrossDateLine` function with a valid polygon geometry as input.
```

### Common Failure Modes
- Providing a geometry that is not a polygon with a single ring will result in an error.
- Input geometries with a width greater than 180 degrees may lead to unexpected behavior if not handled correctly.

### Fix Code Hint
```scala
// Ensure the input geometry is a valid polygon with a single ring before calling the function.
val geometry = GeometryReader.DefaultGeometryFactory.createPolygon(
  Array(new Coordinate(170, 50), new Coordinate(-170, 60), new Coordinate(-170, 50), new Coordinate(170, 50))
)
val split = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)
```

## API Test: `sridToCRS`

### Signature
```scala
def sridToCRS(srid: Int): CoordinateReferenceSystem
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:352_

_Source doc:_ Convert the given SRID to CRS according to the following logic. 1. If the SRID is zero, it indicates an invalid SRID and `null` is returned. 2. It searches the local cache and retrieves the SRID. 3a. If SRID is positive, use it as an EPSG, retrieve the CRS, cache and return it. 3b. If SRID is negative, contact the server, retrieve the CRS, cache and return it. @param srid the SRID that needs to be converted to a CRS @return the converted CRS.

### Goal
The `sridToCRS` function converts a given Spatial Reference Identifier (SRID) into a corresponding Coordinate Reference System (CRS) for use in geospatial raster processing.

### Parameters
- `srid` (`Int`): The Spatial Reference Identifier that needs to be converted to a CRS. It can be a positive EPSG code, a negative value indicating a non-standard CRS, or zero which indicates an invalid SRID.

### Input
The caller must provide an integer value for `srid`. If the value is zero, the function will return `null`. For positive values, it should correspond to a valid EPSG code, while negative values will require server communication to retrieve the CRS.

### Output
Returns `CoordinateReferenceSystem` — this represents the spatial reference system corresponding to the provided SRID, which can be used for geospatial operations in RDPro.

### Valid Call Patterns
```scala
val crs = CRSServer.sridToCRS(sridMercator)
```

### LLM Instruction Prompt
- When calling `sridToCRS`, ensure that the `srid` parameter is a valid integer, either a positive EPSG code or a negative value for non-standard CRS. Handle the case where `srid` is zero to avoid receiving `null`.

### Prompt Snippet
```text
To convert an SRID to a Coordinate Reference System, use the `sridToCRS` function with a valid integer SRID.
```

### Common Failure Modes
- Passing a zero value for `srid` will result in a `null` return value, indicating an invalid SRID.
- Providing a non-integer value will cause a compilation error.
- If a negative SRID is provided, ensure that the server is running to retrieve the CRS; otherwise, it may fail to return a valid CRS.

### Fix Code Hint
```scala
// Ensure the SRID is valid before calling sridToCRS
val validSrid = if (srid > 0) srid else throw new IllegalArgumentException("SRID must be positive or a valid negative value.")
val crs = CRSServer.sridToCRS(validSrid)
```

## API Test: `startServer`

### Signature
```scala
def startServer(defaultPort: Int = DefaultPort): Int
def startServer(sc: SparkContext): Boolean
def startServer(jsc: JavaSparkContext): Boolean
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:91  (+2 more definition site/overload)_

_Source doc:_ Starts the server and returns the port on which it is listening @return the port on which the server is started

### Goal
The `startServer` function initializes the server for RDPro, enabling it to listen for incoming requests on a specified port.

### Parameters
- `defaultPort` (`Int`), default `DefaultPort`: The port number on which the server will listen for incoming connections. If not specified, it defaults to a predefined constant `DefaultPort`.

### Input
The caller must provide a valid `SparkContext` or `JavaSparkContext` if using the overloaded versions. The Spark environment must be properly configured and running to ensure the server can start successfully.

### Output
Returns `Int` — the port number on which the server is actively listening for requests.

### Valid Call Patterns
```scala
CRSServer.startServer(sparkContext)
```

### LLM Instruction Prompt
- Ensure that a valid `SparkContext` or `JavaSparkContext` is provided when calling `startServer`. If using the default port, no argument is needed.

### Prompt Snippet
```text
To start the RDPro server, use the following command:
val port = CRSServer.startServer(sparkContext)
```

### Common Failure Modes
- Attempting to start the server without a valid `SparkContext` or `JavaSparkContext` will result in an error.
- If the specified port is already in use, the server may fail to start or may throw an exception.

### Fix Code Hint
```scala
// Ensure SparkContext is initialized before calling startServer
val sparkContext = new SparkContext(...)
CRSServer.startServer(sparkContext)
```

## API Test: `sumSideLength`

### Signature
```scala
def sumSideLength: Array[Double]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:47_

_Source doc:_ The sum of side length along each dimension. Combined with numNonEmptyGeometries, it can be used to compute average side length per dimension.

### Goal
Calculates the total side length for each dimension of geometries within a spatial partition, aiding in the analysis of geometric properties.

### Parameters
_None._

### Input
The caller must ensure that the spatial partition contains geometries. The method is intended to be called on an instance of a class that represents a spatial partition containing geometries.

### Output
Returns `Array[Double]` — an array where each element represents the sum of side lengths for each dimension of the geometries in the spatial partition.

### Valid Call Patterns
```scala
val sideLengths: Array[Double] = value.sumSideLength
```

### LLM Instruction Prompt
- Ensure that the method is called on a valid instance of a spatial partition containing geometries.

### Prompt Snippet
```text
Call the `sumSideLength` method on a valid spatial partition instance to obtain the total side lengths for each dimension.
```

### Common Failure Modes
- Calling `sumSideLength` on an empty spatial partition may lead to unexpected results or an empty array.
- Ensure that the geometries within the spatial partition are valid and properly initialized.

### Fix Code Hint
```scala
// Ensure the spatial partition is populated with geometries before calling sumSideLength
if (spatialPartition.numNonEmptyGeometries > 0) {
  val sideLengths: Array[Double] = spatialPartition.sumSideLength
} else {
  // Handle the case where there are no geometries
}
```

## API Test: `summarizeData`

### Signature
```scala
private[dataExplorer] def summarizeData(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:219_

_Source doc:_ Summarize the dataset and set the corresponding attributes in the dataset.

### Goal
`summarizeData` summarizes the dataset and updates the dataset attributes accordingly, providing insights into the dataset's characteristics.

### Parameters
_None._

### Input
The function does not require any input parameters. However, it is expected that the dataset has been properly initialized and loaded prior to calling this function.

### Output
Returns `Unit` — this indicates that the function performs an operation without returning a value. The operation modifies the dataset's attributes to reflect the summary information.

### Valid Call Patterns
```scala
value.summarizeData()
```

### LLM Instruction Prompt
- Ensure that the dataset has been initialized and loaded before calling `summarizeData`.

### Prompt Snippet
```text
Call `summarizeData` after loading and preparing your dataset to update its attributes with summary information.
```

### Common Failure Modes
- Calling `summarizeData` without a properly initialized dataset may lead to unexpected behavior or errors.
- If the dataset is empty or not loaded, the summary operation may not yield meaningful results.

### Fix Code Hint
```scala
// Ensure the dataset is loaded before calling summarizeData
val dataset = loadYourDataset() // Replace with actual dataset loading code
dataset.summarizeData()
```

## API Test: `summary`

### Signature
```scala
def summary: Summary
def summary(rdd: JavaSpatialRDD): Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:171  (+2 more definition site/overload)_

_Source doc:_ Compute the geometric summary of the given RDD @param rdd the spatial RDD to compute its summary @return the summary of the given RDD

### Goal
Compute the geometric summary of a set of features in a spatial RDD, providing insights into the dataset's characteristics.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD for which the geometric summary is to be computed. This RDD should contain spatial features with geometries.

### Input
The input must be a `JavaSpatialRDD` containing spatial features, which can be loaded from formats such as Shapefiles or CSV points. Ensure that the RDD is properly initialized and contains valid geometries.

### Output
Returns `Summary` — an object that encapsulates the geometric summary of the RDD, including metrics such as size (in bytes), number of records, number of points, number of non-empty geometries, average side length (width and height), and the geometry type.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
val rdd = sparkContext.shapefile("input.zip")
val summaryResult = rdd.summary()
```

### LLM Instruction Prompt
- When calling `summary`, ensure that the input RDD is a valid `JavaSpatialRDD` containing spatial features. If using the overload, provide the RDD as an argument.

### Prompt Snippet
```text
To compute the geometric summary of a spatial RDD, use the `summary` method on the RDD instance.
```

### Common Failure Modes
- Calling `summary` on an uninitialized or empty `JavaSpatialRDD` may result in a null or empty summary.
- If the RDD does not contain valid geometries, the summary may not accurately reflect the dataset's characteristics.

### Fix Code Hint
```scala
Ensure that the RDD is properly loaded and contains valid spatial features before calling `summary`.
```

## API Test: `tileIDs`

### Signature
```scala
def tileIDs: Iterator[Int]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:91_

_Source doc:_ An iterator that goes over all tile IDs @return an iterator that iterates over all tile IDs in this raster

### Goal
The `tileIDs` function retrieves an iterator over all tile IDs present in the raster, facilitating access to individual tiles for further processing.

### Parameters
_None._

### Input
The caller must provide a raster object that has been properly initialized and contains tile data. This typically involves loading a raster from a GeoTIFF or HDF file using the appropriate RDPro methods.

### Output
Returns `Iterator[Int]` — an iterator of integer tile IDs, where each ID corresponds to a specific tile within the raster dataset.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
for (tileID <- raster.tileIDs) {
  // Process each tile using tileID
}
```

### LLM Instruction Prompt
- When calling `tileIDs`, ensure that the raster has been loaded and initialized correctly. The raster must contain tile data to retrieve valid tile IDs.

### Prompt Snippet
```text
Retrieve tile IDs from a loaded raster using the tileIDs method.
```

### Common Failure Modes
- Attempting to call `tileIDs` on an uninitialized or empty raster will result in an error or an empty iterator.
- If the raster does not contain any tiles, the iterator returned will be empty.

### Fix Code Hint
```scala
// Ensure the raster is properly loaded before calling tileIDs
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
if (raster.isEmpty) {
  throw new IllegalArgumentException("Raster is empty or not initialized.")
}
for (tileID <- raster.tileIDs) {
  // Proceed with processing each tile
}
```

## API Test: `transform`

### Signature
```scala
override def transform(ptSrc: DirectPosition, ptDst: DirectPosition): DirectPosition
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SnapTransform.scala:46  (+4 more definition site/overload)_

### Goal
The `transform` function applies a geometric transformation to a set of source points, converting them into destination points based on specified offsets and the number of points to transform.

### Parameters
- `srcPts` (`Array[Double]`): An array of source point coordinates that need to be transformed. The expected values are the coordinates in the source coordinate reference system (CRS).
- `srcOff` (`Int`): The starting index in the `srcPts` array from which to begin reading the source points. This allows for processing a subset of the array.
- `dstPts` (`Array[Double]`): An array where the transformed destination point coordinates will be stored. The expected values are the coordinates in the destination CRS.
- `dstOff` (`Int`): The starting index in the `dstPts` array where the transformed coordinates will be written. This allows for writing to a specific position in the destination array.
- `numPts` (`Int`): The number of points to transform, indicating how many sets of coordinates will be processed from the source array.

### Input
The caller must provide an array of source points (`srcPts`) in the form of `Array[Double]`, along with the appropriate offsets and the number of points to transform. The source points should be in a compatible coordinate reference system for the transformation to be valid.

### Output
Returns `Unit` — this indicates that the transformation is performed in-place, modifying the `dstPts` array directly without returning any value.

### Valid Call Patterns
```scala
val srcPoints: Array[Double] = Array(0.0, 0.0, 1.0, 1.0)
val dstPoints: Array[Double] = new Array[Double](4)
val srcOffset: Int = 0
val dstOffset: Int = 0
val numberOfPoints: Int = 2

value.transform(srcPoints, srcOffset, dstPoints, dstOffset, numberOfPoints)
```

### LLM Instruction Prompt
- Ensure that the source points are provided in the correct format and that the offsets do not exceed the bounds of the source and destination arrays.

### Prompt Snippet
```text
Transform the source points using the transform function, ensuring the offsets and number of points are correctly specified.
```

### Common Failure Modes
- **Index Out of Bounds**: If `srcOff + numPts` exceeds the length of `srcPts` or `dstOff + numPts` exceeds the length of `dstPts`, an `ArrayIndexOutOfBoundsException` will occur.
- **Invalid Input Types**: Providing non-`Array[Double]` types for `srcPts` or `dstPts` will result in a compile-time error.

### Fix Code Hint
```scala
// Ensure that the source and destination arrays are properly sized and that offsets are within bounds.
if (srcPts.length < srcOff + numPts || dstPts.length < dstOff + numPts) {
  throw new IllegalArgumentException("Offsets and number of points exceed array bounds.")
}
```

## API Test: `trimLineSegment`

### Signature
```scala
private[davinci] def trimLineSegment(x1: Double, y1: Double, x2: Double, y2: Double): (Double, Double, Double, Double)
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:146_

_Source doc:_ Trim a line segment with the boundaries of this tile, i.e., the box (-buffer, -buffer, resolution + buffer, resolution + buffer) @param x1 the x-coordinate of the first point @param y1 the y-coordinate of the first point @param x2 the x-coordinate of the second point @param y2 the y-coordinate of the second point @return the given line segment trimmed to the tile boundaries or null if the line segment is completely outside

### Goal
`trimLineSegment` trims a line segment to fit within the boundaries of a specified tile in a geospatial raster context.

### Parameters
- `x1` (`Double`): The x-coordinate of the first endpoint of the line segment.
- `y1` (`Double`): The y-coordinate of the first endpoint of the line segment.
- `x2` (`Double`): The x-coordinate of the second endpoint of the line segment.
- `y2` (`Double`): The y-coordinate of the second endpoint of the line segment.

### Input
The caller must provide four `Double` values representing the coordinates of the two endpoints of the line segment. The line segment should be defined in relation to the tile boundaries.

### Output
Returns `(Double, Double, Double, Double)` — a tuple containing the trimmed coordinates of the line segment. If the line segment is completely outside the tile boundaries, it returns `null`.

### Valid Call Patterns
```scala
val tile = new IntermediateVectorTile(10, 2)
assertResult((1, 2, 3, 4))(tile.trimLineSegment(1, 2, 3, 4))
assertResult(null)(tile.trimLineSegment(-4, 2, -3, 5))
assertResult((-2, 3, 2, 5))(tile.trimLineSegment(-4, 2, 2, 5))
assertResult((6, 8, 4, 12))(tile.trimLineSegment(6, 8, 3, 14))
```

### LLM Instruction Prompt
- When calling `trimLineSegment`, ensure that the provided coordinates are within the expected range of the tile boundaries. If the line segment is completely outside, expect a return value of `null`.

### Prompt Snippet
```text
Call `trimLineSegment` with the coordinates of the line segment endpoints to get the trimmed segment within the tile boundaries.
```

### Common Failure Modes
- Providing coordinates that do not correspond to a valid line segment (e.g., both endpoints being the same).
- Expecting a non-null return value when the line segment is completely outside the tile boundaries.

### Fix Code Hint
```scala
// Ensure the coordinates provided are within the expected tile boundaries before calling trimLineSegment.
```

## API Test: `uniform`

### Signature
```scala
def uniform(cardinality: Long): JavaSpatialRDD
def uniform(cardinality: Long): SpatialRDD
def uniform(a: Double, b: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:37  (+2 more definition site/overload)_

_Source doc:_ Generate a random value in the range [a, b) from a uniform distribution

### Goal
The `uniform` function generates a random value from a uniform distribution within a specified range, which is useful for creating random spatial data in geospatial analysis.

### Parameters
- `a` (`Double`): The lower bound of the range (inclusive) from which the random value will be generated.
- `b` (`Double`): The upper bound of the range (exclusive) for the random value generation.

### Input
The caller must provide two `Double` values representing the range for the random value generation. There are no specific file formats or data inputs required for this function.

### Output
Returns `Double` — a random value generated from a uniform distribution within the range [a, b).

### Valid Call Patterns
```scala
val randomValue: Double = sc.generateSpatialData.uniform(0.0, 1.0)
```

### LLM Instruction Prompt
- When calling `uniform`, ensure that the values for `a` and `b` are valid `Double` types, with `a` being less than `b`.

### Prompt Snippet
```text
Generate a random value using the uniform distribution with specified bounds.
```

### Common Failure Modes
- If `a` is greater than or equal to `b`, the function may produce unexpected results or throw an error.
- Providing non-Double types for `a` or `b` will result in a compilation error.

### Fix Code Hint
```scala
// Ensure that the lower bound is less than the upper bound
val randomValue: Double = sc.generateSpatialData.uniform(0.0, 1.0) // Correct usage
```

## API Test: `uniformHistogramCount`

### Signature
```scala
def uniformHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:67_

_Source doc:_ Computes a uniform histogram with the given size that counts number of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `uniformHistogramCount` function computes a uniform histogram that counts the number of features in each cell, facilitating efficient range queries in geospatial raster analysis.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the size of the histogram, representing the number of partitions along each dimension. For example, `Array(100, 100)` creates a histogram with 100 partitions in both dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the resulting histogram. Setting this to `true` can speed up range tests.

### Input
The caller must provide a valid `features` object that supports the `uniformHistogramCount` method. The `histogramSize` must be a non-empty array of positive integers.

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which can be used for further analysis or querying of feature counts within specified ranges.

### Valid Call Patterns
```scala
val countHistogram = features.uniformHistogramCount(Array(100, 100))
val histogram = polygons.uniformHistogramCount(Array(100, 100), prefixSum = true)
```

### LLM Instruction Prompt
- When calling `uniformHistogramCount`, ensure that the `histogramSize` is a non-empty array of positive integers and that the `prefixSum` parameter is a boolean value.

### Prompt Snippet
```text
Call the `uniformHistogramCount` method on a valid features object with an array of integers for histogram size and an optional boolean for prefix sum.
```

### Common Failure Modes
- Providing a `histogramSize` array that is empty or contains non-positive integers will result in an error.
- Calling `uniformHistogramCount` on an object that does not support this method will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure histogramSize is a valid non-empty array of positive integers
val validHistogramSize = Array(100, 100)
val histogram = features.uniformHistogramCount(validHistogramSize, prefixSum = true)
```

## API Test: `uniformHistogramSize`

### Signature
```scala
def uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78_

_Source doc:_ Computes a uniform histogram with the given size that calculates the size of the data in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @param sizeFunction  an optional function that computes the size of a feature. @return the created histogram

### Goal
The `uniformHistogramSize` function computes a uniform histogram that partitions data into specified sizes, facilitating efficient data analysis in geospatial raster processing.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the number of partitions along each dimension of the histogram. For example, `Array(100, 100)` creates a histogram with 100 partitions in both dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the histogram results to optimize range queries. Setting this to `true` can improve performance for certain operations.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A function that calculates the size of a feature. The default function retrieves the storage size of the feature, but a custom function can be provided if different size calculations are needed.

### Input
The caller must provide an array of integers for `histogramSize`, which defines the dimensions of the histogram. The input features must be compatible with the `sizeFunction` provided, ensuring that the function can be applied to each feature without errors.

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which contains the size distribution of the data across the specified partitions.

### Valid Call Patterns
```scala
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))
val sizeHistogram = features.uniformHistogramSize(Array(100, 100), sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson"))
```

### LLM Instruction Prompt
- When calling `uniformHistogramSize`, ensure that the `histogramSize` parameter is an array of integers representing the desired partition sizes. The `prefixSum` parameter is optional and defaults to `false`. The `sizeFunction` can be customized to fit specific feature size calculations.

### Prompt Snippet
```text
Call `uniformHistogramSize` with an array of integers for `histogramSize`, and optionally specify `prefixSum` and `sizeFunction` to customize the histogram computation.
```

### Common Failure Modes
- Providing an invalid `histogramSize` array (e.g., empty or containing negative values) may result in runtime errors.
- If the `sizeFunction` is incompatible with the features being processed, it may throw exceptions during execution.

### Fix Code Hint
```scala
Ensure that `histogramSize` is a non-empty array of positive integers and that the `sizeFunction` is correctly defined for the feature type being processed.
```

## API Test: `using`

### Signature
```scala
def using[A <: AutoCloseable, B](resource: A)
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:606  (+1 more definition site/overload)_

### Goal
The `using` function provides a way to manage resources that implement the `AutoCloseable` interface, ensuring that they are properly closed after use, which is essential in geospatial processing to prevent resource leaks.

### Parameters
- `resource` (`A`): An instance of a resource that implements the `AutoCloseable` interface, such as a database connection or file stream, which needs to be closed after its operations are completed.

### Input
The caller must provide a valid `AutoCloseable` resource, such as a database connection obtained from a driver manager. The resource must be properly initialized before being passed to the `using` function.

### Output
Returns `unspecified` — the function does not return a value; instead, it ensures that the provided resource is closed after the block of code using it has been executed.

### Valid Call Patterns
```scala
using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) { dbConnection =>
  // operations using dbConnection
}
```

### LLM Instruction Prompt
- When calling `using`, ensure that the resource passed is an instance of a class that implements `AutoCloseable`, and provide a block of code that operates on this resource.

### Prompt Snippet
```text
Ensure to use `using` with an `AutoCloseable` resource to manage resource closure automatically.
```

### Common Failure Modes
- Attempting to pass a resource that does not implement `AutoCloseable` will result in a compilation error.
- Not providing a valid, initialized resource may lead to runtime exceptions when trying to use the resource.

### Fix Code Hint
```scala
Ensure that the resource you are passing to `using` is properly initialized and implements `AutoCloseable`. For example:
using(DriverManager.getConnection("jdbc:h2:your_database_path", "user", "password")) { connection =>
  // Use the connection here
}
```

## API Test: `value`

### Signature
```scala
override def value: Summary
override def value: Array[PointND]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:68  (+1 more definition site/overload)_

### Goal
The `value` function retrieves the computed summary statistics or point data from the accumulator, which is useful for analyzing raster data in geospatial applications.

### Parameters
_None._

### Input
No specific input parameters are required for this function. However, it is assumed that the accumulator has been properly initialized and populated with data prior to calling `value`.

### Output
Returns `Summary` — this represents the aggregated summary statistics of the raster data processed by the accumulator, which may include metrics such as mean, min, max, and count.

### Valid Call Patterns
```scala
val summary: Summary = value.value
```

### LLM Instruction Prompt
- Ensure that the accumulator has been populated with raster data before calling `value`. The function can be called without any parameters.

### Prompt Snippet
```text
To retrieve the summary statistics from the accumulator, call `value.value` after ensuring it has been populated with data.
```

### Common Failure Modes
- Calling `value` before the accumulator has been populated will result in an empty or null summary.
- If the accumulator is not properly initialized, it may lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the accumulator is populated before calling value
val summary: Summary = if (accumulator.isPopulated) value.value else throw new IllegalStateException("Accumulator is not populated.")
```

## API Test: `visualize`

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
The function does not require any parameters. It operates on the dataset that has been previously loaded and processed within the context of the `DatasetProcessor`.

### Output
Returns `Unit` — this indicates that the function completes its operation without returning a value. The output represents the successful creation of a visualization index for the dataset.

### Valid Call Patterns
```scala
value.visualize()
```

### LLM Instruction Prompt
- Ensure that the dataset has been properly loaded and processed before calling `visualize`. This function should be called within the context of a `DatasetProcessor` instance.

### Prompt Snippet
```text
Call the visualize method on the DatasetProcessor instance to build the visualization index for the dataset.
```

### Common Failure Modes
- Calling `visualize` without having a dataset loaded or processed may result in an error or unexpected behavior.
- Ensure that the `DatasetProcessor` instance is properly initialized before invoking this method.

### Fix Code Hint
```scala
// Ensure the dataset is loaded and processed before calling visualize
val datasetProcessor = new DatasetProcessor("datasetName", dbConnection, datasetsPath.getPath, FileSystem.getLocal(sparkContext.hadoopConfiguration), sparkSession)
datasetProcessor.visualize()
```

## API Test: `writeSpatialFile`

### Signature
```scala
def writeSpatialFile(filename: String, oformat: String, opts: BeastOptions = new BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String, opts: BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:94  (+2 more definition site/overload)_

_Source doc:_ Write this RDD as a spatial file with the given format and additional options @param filename the output file name @param oformat the output file format (short name) @param opts additional user options

### Goal
The `writeSpatialFile` function saves a spatial RDD as a file in a specified format, enabling users to export processed geospatial data for further analysis or sharing.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD containing the geospatial data to be written to a file. This RDD should be properly populated with spatial features before calling this function.
- `filename` (`String`): The name of the output file where the spatial data will be saved. This should include the desired file extension (e.g., `.csv` or `.tif`).
- `oformat` (`String`): The format in which to save the spatial data. This is a short name representing the file format (e.g., `"envelope"` for an envelope format).
- `opts` (`BeastOptions`): Additional user options for writing the file, such as separators for CSV files. This parameter is optional and defaults to a new instance of `BeastOptions`.

### Input
The caller must provide a populated `JavaSpatialRDD`, a valid filename with an appropriate extension, and a supported output format. The `opts` parameter can be used to specify additional options but is not mandatory.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of writing the spatial data to the specified file.

### Valid Call Patterns
```scala
records.writeSpatialFile("output.csv", "envelope", new BeastOptions("oseparator" -> ","))
```

### LLM Instruction Prompt
- Ensure that the `filename` includes the correct file extension and that the `oformat` is a valid format supported by RDPro. The `rdd` must be a properly initialized `JavaSpatialRDD` containing spatial features.

### Prompt Snippet
```text
To save your spatial data, use the `writeSpatialFile` method with a valid `JavaSpatialRDD`, a filename, and the desired output format.
```

### Common Failure Modes
- Providing an invalid or unsupported `oformat` may result in an error during the write operation.
- Attempting to write an empty or uninitialized `JavaSpatialRDD` will lead to a failure, as there is no data to write.
- Not including the appropriate file extension in the `filename` may cause issues with file recognition by other applications.

### Fix Code Hint
```scala
// Ensure the RDD is populated and the filename includes the correct extension
val rdd: JavaSpatialRDD = ... // Initialize your JavaSpatialRDD here
rdd.writeSpatialFile("output.csv", "envelope", new BeastOptions("oseparator" -> ","))
```

## API Test: `x1`

### Signature
```scala
def x1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:14_

### Goal
`x1` retrieves the x-coordinate of the first pixel in a raster tile.

### Parameters
_None._

### Input
No specific input is required to call `x1`, as it operates on the instance of the class it belongs to.

### Output
Returns `Int` — the x-coordinate of the first pixel in the raster tile, which is typically used for indexing or referencing pixel locations within the tile.

### Valid Call Patterns
```scala
val xCoordinate: Int = tile.x1
```

### LLM Instruction Prompt
- When calling `x1`, ensure that it is invoked on an instance of a class that represents a raster tile.

### Prompt Snippet
```text
Retrieve the x-coordinate of the first pixel in the raster tile using the method x1.
```

### Common Failure Modes
- Attempting to call `x1` on a null or uninitialized tile instance will result in a `NullPointerException`.

### Fix Code Hint
```scala
// Ensure the tile instance is properly initialized before calling x1
if (tile != null) {
  val xCoordinate: Int = tile.x1
} else {
  // Handle the null case appropriately
}
```

## API Test: `x2`

### Signature
```scala
def x2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16_

### Goal
The `x2` function retrieves the x-coordinate of the bottom-right corner of a tile in a raster dataset.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Int` — the x-coordinate value representing the horizontal position of the bottom-right corner of the tile.

### Valid Call Patterns
```scala
val xCoordinate: Int = value.x2
```

### LLM Instruction Prompt
- When calling `x2`, ensure that the receiver is an instance of a class that contains this method, and no parameters are needed.

### Prompt Snippet
```text
Retrieve the x-coordinate of the bottom-right corner of the tile using the x2 method.
```

### Common Failure Modes
- Attempting to call `x2` on an instance that does not have this method will result in a compilation error.

### Fix Code Hint
```scala
// Ensure the receiver is of the correct type that includes the x2 method.
val xCoordinate: Int = value.x2
```

## API Test: `y1`

### Signature
```scala
def y1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:15_

### Goal
`y1` retrieves the starting y-coordinate of a tile in a raster dataset.

### Parameters
_None._

### Input
The caller must have a raster tile object that implements the `y1` method. This method is typically called on instances of classes that represent raster tiles, such as `MemoryTile`.

### Output
Returns `Int` — the starting y-coordinate of the tile, which indicates the vertical position of the tile in the raster grid.

### Valid Call Patterns
```scala
val tile: MemoryTile[Int] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
val startY: Int = tile.y1
```

### LLM Instruction Prompt
- When calling `y1`, ensure that it is invoked on a valid raster tile object that has been properly initialized.

### Prompt Snippet
```text
Retrieve the starting y-coordinate of the raster tile using the `y1` method.
```

### Common Failure Modes
- Attempting to call `y1` on an uninitialized or null raster tile object will result in a `NullPointerException`.
- Calling `y1` on an object that does not implement the method will lead to a compilation error.

### Fix Code Hint
```scala
// Ensure the tile is properly initialized before calling y1
val tile: MemoryTile[Int] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
val startY: Int = tile.y1 // This should work if tile is correctly initialized
```

## API Test: `y2`

### Signature
```scala
def y2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17_

### Goal
`y2` retrieves the maximum y-coordinate of the tile, which is useful for understanding the spatial extent of raster data in geospatial analysis.

### Parameters
_None._

### Input
No specific input is required for this method.

### Output
Returns `Int` — the maximum y-coordinate of the tile, representing the upper boundary of the tile's vertical extent.

### Valid Call Patterns
```scala
val maxY: Int = tile.y2
```

### LLM Instruction Prompt
- When calling `y2`, ensure that the receiver is an instance of a tile that has been properly initialized and contains valid raster data.

### Prompt Snippet
```text
Retrieve the maximum y-coordinate of the tile using the `y2` method.
```

### Common Failure Modes
- Calling `y2` on an uninitialized or null tile instance may result in a `NullPointerException`.
- If the tile does not contain valid raster data, the returned value may not represent a meaningful coordinate.

### Fix Code Hint
```scala
// Ensure the tile is properly initialized before calling y2
if (tile != null) {
  val maxY: Int = tile.y2
} else {
  // Handle the null case appropriately
}
```

## API Test: `zigzagDecode`

### Signature
```scala
def zigzagDecode(x: Int): Int
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:150_

_Source doc:_ Decodes a value from Zigzag encoding

### Goal
The `zigzagDecode` function decodes a value that has been encoded using Zigzag encoding, which is commonly used to efficiently encode signed integers.

### Parameters
- `x` (`Int`): The encoded integer value that needs to be decoded from Zigzag encoding.

### Input
The input must be a valid integer that has been encoded using Zigzag encoding. There are no specific file formats or external data requirements for this function, as it operates solely on the integer input.

### Output
Returns `Int` — the decoded integer value, which represents the original signed integer before it was encoded using Zigzag encoding.

### Valid Call Patterns
```scala
val decodedValue: Int = VectorLayerBuilder.zigzagDecode(encodedValue)
```

### LLM Instruction Prompt
- When calling `zigzagDecode`, ensure that the input is a valid encoded integer. The function will return the decoded integer value.

### Prompt Snippet
```text
To decode a Zigzag encoded integer, use the `zigzagDecode` function with the encoded integer as the argument.
```

### Common Failure Modes
- Passing a non-integer value will result in a compilation error.
- The function assumes that the input integer is a valid Zigzag encoded value; if it is not, the output may not represent the expected original signed integer.

### Fix Code Hint
```scala
// Ensure the input is a valid Zigzag encoded integer before calling the function
val encodedValue: Int = 50 // Example of a Zigzag encoded integer
val decodedValue: Int = VectorLayerBuilder.zigzagDecode(encodedValue)
```

## API Test: `zonalStats2`

### Signature
```scala
def zonalStats2[T](zones: RDD[IFeature], raster: RDD[ITile[T]], collectorClass: Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator = null)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:128_

_Source doc:_ Computes zonal statistics between a set of zones (polygons) and a raster file given by its path and a layer in that file. The result is an RDD of pairs of a feature and a collector value @param zones a set of polygons that represent the regions or zones @param raster the RDD of tiles @param collectorClass the class that collects the pixel values to compute the statistics @param opts additional user-defined options @param numTiles an optional accumulator to collect the total number of processed tiles @return a set of (Feature, Statistics)

### Goal
`zonalStats2` computes statistical summaries (e.g., count, sum) of raster pixel values within specified polygonal zones, facilitating analysis of geospatial data.

### Parameters
- `zones` (`RDD[IFeature]`): An RDD containing polygon features that define the zones for which statistics will be computed. Each feature represents a geographic area.
- `raster` (`RDD[ITile[T]]`): An RDD of raster tiles, where each tile contains pixel values corresponding to the geographic area covered by the raster dataset.
- `collectorClass` (`Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator`), default `null`: The class type of the collector that will aggregate pixel values to compute the desired statistics. `opts` are additional user-defined options for processing, and `numTiles` is an optional accumulator to track the total number of tiles processed.

### Input
The caller must provide:
- An RDD of polygon features (`zones`) representing the areas of interest.
- An RDD of raster tiles (`raster`) loaded from a compatible raster format (e.g., GeoTIFF).
- A valid collector class that extends `Collector` to specify how pixel values should be aggregated.
- An instance of `BeastOptions` for any additional processing configurations.

### Output
Returns an RDD of pairs, where each pair consists of a feature (zone) and its corresponding statistics collected from the raster data. The statistics are represented by instances of the specified collector class.

### Valid Call Patterns
```scala
val vectorFile = locateResource("/vectors/ne_110m_admin_1_states_provinces.zip")
val rasterFile = locateResource("/rasters/glc2000_small.tif")

val polygons: RDD[IFeature] = SpatialReader.readInput(sparkContext, new BeastOptions(), vectorFile.getPath, "shapefile")
  .zipWithIndex()
  .map(featureIndex => new Feature((Row.unapplySeq(featureIndex._1).get :+ featureIndex._2.toInt).toArray,
    StructType(featureIndex._1.schema :+ StructField("index", IntegerType))))

val raster: RDD[ITile[Int]] = new RasterFileRDD[Int](sparkContext, rasterFile.getPath, new BeastOptions())

val zsResults: Array[Collector] =
  ZonalStatistics.zonalStats2(polygons, raster, classOf[Statistics], new BeastOptions())
    .map(fc => (fc._1.getAs[Int]("index"), fc._2))
    .collect
    .sortBy(_._1)
    .map(_._2)
```

### LLM Instruction Prompt
When calling `zonalStats2`, ensure that the `zones` parameter is an RDD of polygon features, the `raster` parameter is an RDD of raster tiles, and the `collectorClass` is a valid class extending `Collector`. Provide a `BeastOptions` instance for additional configurations.

### Prompt Snippet
```text
To compute zonal statistics, use the `zonalStats2` function with an RDD of polygon features, an RDD of raster tiles, and a collector class for statistics aggregation.
```

### Common Failure Modes
- Providing an incompatible type for `collectorClass` that does not extend `Collector`.
- Using an empty or null RDD for either `zones` or `raster`.
- Failing to provide a valid `BeastOptions` instance, which may lead to unexpected behavior during processing.

### Fix Code Hint
```scala
Ensure that the RDDs for `zones` and `raster` are properly initialized and that the `collectorClass` is a valid subclass of `Collector`. Check that `BeastOptions` is instantiated correctly.
```

## API Test: `zonalStatsLocal`

### Signature
```scala
def zonalStatsLocal[T](geometries: Array[Geometry], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
def zonalStatsLocal[T](zones: Array[IFeature], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:162  (+1 more definition site/overload)_

_Source doc:_ Run zonal statistics locally in one thread. This is useful when the array of geometries is small and the overhead of partitioning could be high. @param zones the array of features that describe the zones. @param raster the raster reader that points to the raster file being aggregated @param collectorClass the class that computes the statistics @return an array of collectors that is equal in length to the input array of features with the result for each. Features that do not overlap any pixels will have null.

### Goal
`zonalStatsLocal` computes zonal statistics for specified geometries using a raster dataset, returning results in a single-threaded manner.

### Parameters
- `geometries` (`Array[Geometry]`): An array of geometries that define the zones for which statistics will be computed. These geometries should represent areas of interest within the raster data.
- `raster` (`IRasterReader[T]`): An instance of `IRasterReader` that provides access to the raster data being analyzed. This should be initialized with a raster file, such as a GeoTIFF.
- `collectorClass` (`Class[_ <: Collector]`): A class type that extends `Collector`, which specifies the type of statistics to be computed (e.g., mean, sum, count).

### Input
The caller must provide:
- An array of geometries or features that define the zones (e.g., administrative boundaries).
- A raster reader initialized with a raster file (e.g., GeoTIFF) that contains the pixel data to be analyzed.
- A valid collector class that determines how the statistics will be aggregated.

### Output
Returns `Array[Collector]` — an array of collector instances, each corresponding to a geometry in the input array. Each collector contains the computed statistics for its respective zone, with null values for features that do not overlap any pixels.

### Valid Call Patterns
```scala
val vectorFile = new Path(locateResource("/vectors/ne_110m_admin_1_states_provinces.zip").getPath)
val rasterFile = new Path(locateResource("/rasters/glc2000_small.tif").getPath)

val vectorReader = new ShapefileFeatureReader
vectorReader.initialize(vectorFile, new BeastOptions())
import scala.collection.JavaConverters._
val features: Array[IFeature] = vectorReader.iterator().asScala.toArray
val rasterReader: IRasterReader[Int] = new GeoTiffReader[Int]
rasterReader.initialize(rasterFile.getFileSystem(sparkContext.hadoopConfiguration), rasterFile.toString, "0", new BeastOptions())

val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
```

### LLM Instruction Prompt
When calling `zonalStatsLocal`, ensure that the geometries provided are valid and that the raster reader is properly initialized with a compatible raster file. The collector class must be a valid subclass of `Collector`.

### Prompt Snippet
```text
To compute zonal statistics, use the `zonalStatsLocal` function with an array of geometries, a raster reader initialized with a raster file, and a collector class for the desired statistics.
```

### Common Failure Modes
- Providing geometries that do not intersect with the raster data, resulting in null collectors.
- Using an uninitialized or incorrectly configured raster reader, which may lead to runtime errors.
- Specifying an invalid collector class that does not extend `Collector`, causing a compilation error.

### Fix Code Hint
```scala
Ensure that the geometries overlap with the raster data and that the raster reader is correctly initialized with a valid raster file. Verify that the collector class is a valid subclass of `Collector`.
```

