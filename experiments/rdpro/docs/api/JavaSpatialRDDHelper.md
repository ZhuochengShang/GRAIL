# JavaSpatialRDDHelper

_`plotImage` generates a visual representation of spatial features from a `JavaSpatialRDD` and saves it as an image file._

**Receiver:** static object — call `JavaSpatialRDDHelper.<method>(...)`

**Members** (most robust first): ★ `plotImage` **(primary)**, ★ `saveAsGeoJSON`, ⚠️ `isSpatiallyPartitioned`, ⚠️ `rangeQuery`, ⚠️ `raptorJoin`, ⚠️ `reproject`, ⚠️ `saveAsCSVPoints`, ⚠️ `saveAsIndex`, ⚠️ `saveAsKML`, ⚠️ `saveAsShapefile`, ⚠️ `saveAsWKTFile`, ⚠️ `spatialPartition`, ⚠️ `summary`, ⚠️ `writeSpatialFile`

---

## API Test: `plotImage`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

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
`plotImage` generates a visual representation of spatial features from a `JavaSpatialRDD` and saves it as an image file.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial features that will be plotted. This can include various geometries such as points, lines, or polygons.
- `imageWidth` (`Int`): The width of the output image in pixels. This determines the horizontal resolution of the generated image.
- `imageHeight` (`Int`): The height of the output image in pixels. This determines the vertical resolution of the generated image.
- `imagePath` (`String`): The file path where the generated image will be saved. This should include the desired file name and extension (e.g., `.png`).
- `plotterClass` (`Class[_ <: Plotter], opts: BeastOptions`): The class of the plotter to be used for rendering the image. This allows customization of the plotting behavior. `opts` are additional user options that can modify the plotting process.

### Input
The caller must provide a valid `JavaSpatialRDD` containing spatial features, specify the desired image dimensions (width and height), and provide a valid file path for saving the image. The `plotterClass` and `opts` are optional but can be used to customize the plotting behavior.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the plotted image to the specified path.

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
- Provide a valid file path for `imagePath` where the image will be saved, including the file extension.
- Optionally, specify a `plotterClass` to customize the plotting behavior.

### Prompt Snippet
```text
To plot spatial features, call `plotImage` with a valid `JavaSpatialRDD`, desired image dimensions, and a file path for the output image.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the RDD is valid and the image dimensions are positive integers
val validRDD: JavaSpatialRDD = sc.shapefile("path_to_shapefile.zip")
validRDD.plotImage(800, 600, "output_image.png")
```

## API Test: `saveAsGeoJSON`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveAsGeoJSON(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsGeoJSON(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:201  (+1 more definition site/overload)_

_Source doc:_ Save features in GeoJSON format @param filename the output filename

### Goal
The `saveAsGeoJSON` function saves spatial features to a file in GeoJSON format, which is widely used for representing geographic data structures.

### Parameters
- `filename` (`String`): The name of the output file where the GeoJSON data will be saved. It should include the `.geojson` extension.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for controlling the behavior of the save operation, such as formatting and compression settings.

### Input
The input must be a spatial dataset that can be represented as features in GeoJSON format. This can be provided as an RDD of spatial features or a JavaSpatialRDD. The dataset must be properly formatted and accessible in the Spark context.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the data to the specified file.

### Valid Call Patterns
```scala
records.saveAsGeoJSON("output.geojson")
```

### LLM Instruction Prompt
- Ensure that the `filename` parameter includes the `.geojson` extension and that the input data is a valid spatial dataset.

### Prompt Snippet
```text
To save your spatial features as a GeoJSON file, use the `saveAsGeoJSON` method with the appropriate filename and options.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the filename is correct and the dataset is valid
records.saveAsGeoJSON("output.geojson")
```

## API Test: `isSpatiallyPartitioned`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def isSpatiallyPartitioned: Boolean
def isSpatiallyPartitioned(rdd: JavaSpatialRDD): Boolean
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:45  (+1 more definition site/overload)_

_Source doc:_ Tells whether a SpatialRDD is partitioned using any spatial partitioner or not @return {@code true} if the RDD is partitioned using any spatial partitioner

### Goal
Determines if a given `JavaSpatialRDD` is organized using a spatial partitioner, which can optimize spatial queries and operations.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial data that may be partitioned spatially. This argument is expected to be a valid instance of `JavaSpatialRDD` containing geospatial features.

### Input
The caller must provide a `JavaSpatialRDD` that has been properly initialized and populated with spatial data. The data should be in a format compatible with spatial operations, ensuring that the RDD is ready for partitioning checks.

### Output
Returns `Boolean` — `true` if the provided `JavaSpatialRDD` is partitioned using any spatial partitioner, and `false` otherwise.

### Valid Call Patterns
```scala
val spatialRDD: JavaSpatialRDD = // initialize your JavaSpatialRDD here
val isPartitioned: Boolean = spatialRDD.isSpatiallyPartitioned
```

### LLM Instruction Prompt
- Ensure that the `JavaSpatialRDD` provided is correctly initialized and populated with spatial data before calling `isSpatiallyPartitioned`.

### Prompt Snippet
```text
Check if the spatial RDD is partitioned using a spatial partitioner by calling isSpatiallyPartitioned on the JavaSpatialRDD instance.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the JavaSpatialRDD is properly initialized and contains spatial data before calling the method.
val spatialRDD: JavaSpatialRDD = // your initialization code here
if (spatialRDD.isSpatiallyPartitioned) {
  println("The RDD is spatially partitioned.")
} else {
  println("The RDD is not spatially partitioned.")
}
```

## API Test: `rangeQuery`
_Grounding: test-backed — usage mined from a real, passing test._

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
`rangeQuery` filters spatial features in a given RDD based on whether they intersect with a specified geometric range, while also counting the number of Minimum Bounding Rectangle (MBR) tests performed for performance profiling.

### Parameters
- `rdd` (`JavaSpatialRDD`): The RDD containing spatial features that will be filtered based on the specified range. This RDD should be populated with spatial data, such as points, lines, or polygons.
- `range` (`Geometry`): The geometric area used as the query range for filtering the spatial features. This can be any geometry type supported by the library, such as a point, line, or polygon.
- `mbrCount` (`LongAccumulator`): An accumulator that tracks the number of MBR tests conducted during the range query. This is useful for performance profiling and optimization.

### Input
The caller must provide a `JavaSpatialRDD` containing spatial features, a `Geometry` object defining the query range, and a `LongAccumulator` for counting MBR tests. The spatial features should be properly formatted and accessible in the RDD.

### Output
Returns `JavaSpatialRDD` — a filtered RDD containing only the spatial features that intersect with the specified query range. The output retains the same format as the input RDD.

### Valid Call Patterns
```scala
val testFile = makeFileCopy("/test111.points")
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
val filteredData = partitionedData.rangeQuery(new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40))
```

### LLM Instruction Prompt
- When calling `rangeQuery`, ensure that the `rdd` parameter is a valid `JavaSpatialRDD` containing spatial features, the `range` parameter is a properly defined `Geometry`, and the `mbrCount` is an initialized `LongAccumulator` for counting MBR tests.

### Prompt Snippet
```text
To perform a range query, use the `rangeQuery` method on a `JavaSpatialRDD` with a specified `Geometry` range and a `LongAccumulator` for MBR counting.
```

### Common Failure Modes
- **[compile]** error: value readToGeometryRDD is not a member of object edu.ucr.cs.bdlab.beast.io.SpatialFileRDD _(seen 2x)_
- **[compile]** error: not found: value SpatialRDD
- **[compile]** error: type mismatch;

### Fix Code Hint
```scala
// Ensure the RDD is properly initialized and contains spatial features
val mbrCount = new LongAccumulator
val filteredData = partitionedData.rangeQuery(range, mbrCount)
```

## API Test: `raptorJoin`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)
def raptorJoin[T](vectors: JavaSpatialRDD, rasters: JavaRasterRDD[T], opts: BeastOptions): JavaRDD[RaptorJoinFeature[T]]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:269  (+1 more definition site/overload)_

_Source doc:_ Performs a raster X vector join (Raptor join) between the two given RDDs. @param vectors the set of vector features @param rasters the set of raster tiles @param opts additional options for the algorithm @return the intersection between the feature vectors and all raster pixels.

### Goal
`raptorJoin` performs a raster-vector join operation, allowing users to combine raster data with vector features to analyze spatial relationships and extract relevant information.

### Parameters
- `vectors` (`JavaSpatialRDD`): The set of vector features, such as points, lines, or polygons, that will be used to intersect with the raster data.
- `rasters` (`JavaRasterRDD[T]`): The set of raster tiles containing pixel data, where `T` represents the pixel type (e.g., `Int`, `Float`).
- `opts` (`BeastOptions`): Additional options for the join algorithm, which may include parameters for performance tuning or specific join behaviors.

### Input
The caller must provide:
- A `JavaSpatialRDD` containing vector features, which can be loaded from formats like Shapefiles or GeoJSON.
- A `JavaRasterRDD[T]` containing raster data, which should be loaded from GeoTIFF or HDF files.
- The `BeastOptions` object, which can be instantiated with default settings or customized as needed.

### Output
Returns `JavaRDD[RaptorJoinFeature[T]]` — a collection of `RaptorJoinFeature` objects representing the intersection of the vector features and raster pixels, where each feature includes the associated raster pixel values.

### Valid Call Patterns
```scala
val raster: JavaRasterRDD[Float] = sc.geoTiff("treecover")
val vector: JavaSpatialRDD = sc.shapefile("us_states")
val join: JavaRDD[RaptorJoinFeature[Float]] = raster.raptorJoin(vector, new BeastOptions())
```

### LLM Instruction Prompt
- When calling `raptorJoin`, ensure that the `vectors` parameter is a valid `JavaSpatialRDD` and the `rasters` parameter is a `JavaRasterRDD` with a matching pixel type. Provide a `BeastOptions` instance for additional configuration.

### Prompt Snippet
```text
To perform a raster-vector join using `raptorJoin`, ensure you have a `JavaSpatialRDD` for your vector features and a `JavaRasterRDD` for your raster data. Specify any additional options using `BeastOptions`.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 16x)_
- **[compile]** error: not found: type JavaRDD _(seen 4x)_
- **[compile]** error: not found: value raptorJoin _(seen 4x)_
- **[compile]** error: polymorphic expression cannot be instantiated to expected type; _(seen 4x)_

### Fix Code Hint
```scala
Ensure that both the vector and raster RDDs are properly loaded and that the pixel type of the raster matches the expected type in the join operation. Consider customizing `BeastOptions` for better performance or specific requirements.
```

## API Test: `reproject`
_Grounding: test-backed — usage mined from a real, passing test._

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
Reproject a raster dataset to a specified coordinate reference system (CRS) while maintaining the resolution of the original raster.

### Parameters
- `raster` (`RasterRDD[T]`): The raster layer that you want to reproject. It should be a distributed collection of raster tiles, where `T` represents the pixel type (e.g., `Int`, `Float`).
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system to which the raster will be reprojected. This should be a valid CRS object, such as one defined by an EPSG code.
- `unifiedRaster` (`Boolean`), default `false`: If set to `true`, all output tiles will be combined into a single `RasterMetadata`, which can simplify further processing. If `false`, the output will maintain separate metadata for each tile.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to determine the pixel values in the target raster when multiple source pixels overlap. Options include nearest neighbor, bilinear, etc.

### Input
The input must include a `RasterRDD` containing the raster data, and a valid `CoordinateReferenceSystem` object. The raster data should be loaded from a supported format (e.g., GeoTIFF or HDF) and must be accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster dataset reprojected to the specified target CRS, maintaining the pixel type `T`. The output is in the same format as the input raster, suitable for further geospatial analysis.

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
When calling `reproject`, ensure that the raster data is properly loaded and that the target CRS is valid. Use appropriate pixel types for the raster and specify the desired interpolation method if necessary.

### Prompt Snippet
```text
To reproject a raster, use the `reproject` method on a `RasterRDD` with the target CRS and optional parameters for unified raster and interpolation method.
```

### Common Failure Modes
- **[compile]** error: '.' expected but '}' found. _(seen 2x)_
- **[compile]** error: Missing closing brace `}' assumed here
- **[no-correctness-check]** ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ reproject " + <witness>).

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and that the target CRS is specified using a valid EPSG code or a defined `CoordinateReferenceSystem` object.
```

## API Test: `saveAsCSVPoints`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

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
- `filename` (`String`): The name of the output file where the point features will be saved. Expected values are valid file paths with a `.csv` extension.
- `xColumn` (`Int`), default `0`: The index of the column that contains the x-coordinate in the output file. This is typically the first column if not specified otherwise.
- `yColumn` (`Int`), default `1`: The index of the column that contains the y-coordinate in the output file. This is typically the second column if not specified otherwise.
- `delimiter` (`Char`), default `','`: The character used to separate values in the output file. The default is a comma, but it can be set to other characters like a tab or semicolon.
- `'`: This parameter appears to be incorrectly listed in the API facts and does not have a defined meaning or expected values.
- `header` (`Boolean`), default `true`: A flag indicating whether to write a header line in the output file. If set to true, the first line will contain the column names.

### Input
The caller must provide a valid `SpatialRDD` containing point features. The output filename must be accessible and writable. The x and y columns must correspond to valid indices within the data structure.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the data to the specified file.

### Valid Call Patterns
```scala
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)
```

### LLM Instruction Prompt
When calling `saveAsCSVPoints`, ensure that the input data is a `SpatialRDD` containing point features, and specify a valid filename with a `.csv` extension. Adjust the x and y column indices as needed based on the structure of your data.

### Prompt Snippet
```text
To save your point features to a CSV file, use the `saveAsCSVPoints` method with the appropriate parameters for filename, x and y column indices, delimiter, and header option.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the filename is valid and writable, and check that the x and y column indices are within the bounds of your data.
```

## API Test: `saveAsIndex`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveAsIndex(indexPath: String, oformat: String = "rtree"): Unit
def saveAsIndex(partitionedRDD: JavaPartitionedSpatialRDD, indexPath: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92  (+1 more definition site/overload)_

### Goal
The `saveAsIndex` function creates and saves a spatial index for efficient querying of geospatial data.

### Parameters
- `indexPath` (`String`): The file path where the spatial index will be saved. This should be a valid path in the file system where the user has write permissions.
- `oformat` (`String`), default `"rtree"`: The format of the index to be created. The default is `"rtree"`, which is a common spatial index format. Other formats may be supported, but specifics are not provided.

### Input
The caller must provide a partitioned spatial RDD (if using the second overload) or ensure that the spatial data is properly partitioned before calling this function. The input data should be in a format compatible with the spatial indexing operation, typically derived from a shapefile or other geospatial data source.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the index to the specified path.

### Valid Call Patterns
```scala
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
```

### LLM Instruction Prompt
- Ensure that the input data is properly partitioned and in a compatible format before calling `saveAsIndex`. Use the correct index path and format as required.

### Prompt Snippet
```text
To save a spatial index, ensure your data is partitioned and call `saveAsIndex` with the appropriate index path and format.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: Index directory was not created _(seen 3x)_
- **[compile]** error: not found: type RSGrovePartitioner

### Fix Code Hint
```scala
Ensure that the input RDD is partitioned correctly and that the `indexPath` is valid and writable before calling `saveAsIndex`.
```

## API Test: `saveAsKML`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveAsKML(filename: String): Unit
def saveAsKML(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:86  (+1 more definition site/overload)_

_Source doc:_ Save features in KML format @param filename the name of the output file

### Goal
The `saveAsKML` function saves geospatial features from a `JavaSpatialRDD` into a KML file format, which is commonly used for representing geographic data in applications like Google Earth.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial features that will be saved in KML format. This RDD should contain valid spatial data that can be represented in KML.
- `filename` (`String`): The name of the output KML file, including the path where the file will be saved. It must end with the `.kml` extension.

### Input
The caller must provide a `JavaSpatialRDD` containing spatial features and a valid filename for the output KML file. The filename must be accessible and writable in the specified location.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output is a KML file saved at the specified location, which can be used in various GIS applications.

### Valid Call Patterns
```scala
records.saveAsKML("output.kml")
```

### LLM Instruction Prompt
- When calling `saveAsKML`, ensure that the `rdd` parameter is a valid `JavaSpatialRDD` containing spatial features, and the `filename` is a properly formatted string ending with `.kml`.

### Prompt Snippet
```text
To save your spatial features as a KML file, use the `saveAsKML` method with a valid `JavaSpatialRDD` and specify the output filename.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the JavaSpatialRDD is populated and the filename is correctly formatted.
val validRDD: JavaSpatialRDD = // obtain or create a valid JavaSpatialRDD
validRDD.saveAsKML("output.kml")
```

## API Test: `saveAsShapefile`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveAsShapefile(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsShapefile(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:194  (+1 more definition site/overload)_

_Source doc:_ Save features as a shapefile @param filename the output filename

### Goal
The `saveAsShapefile` function saves geospatial features from a dataset into a shapefile format, which is commonly used for vector data in GIS applications.

### Parameters
- `filename` (`String`): The name of the output shapefile, including the `.shp` extension (e.g., `"output.shp"`).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for controlling the behavior of the shapefile saving process, such as specifying the coordinate reference system or other metadata.

### Input
The caller must provide a valid `JavaSpatialRDD` containing the geospatial features to be saved. The output filename must be a valid string that includes the `.shp` extension. Ensure that the input data is properly formatted and accessible.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output is a shapefile saved to the specified location, which can be used in various GIS applications.

### Valid Call Patterns
```scala
records.saveAsShapefile("output.shp")
```

### LLM Instruction Prompt
- When calling `saveAsShapefile`, ensure that the input data is a valid `JavaSpatialRDD` and that the filename includes the `.shp` extension.

### Prompt Snippet
```text
To save your geospatial features as a shapefile, use the `saveAsShapefile` method with a valid `JavaSpatialRDD` and specify the output filename with a `.shp` extension.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the input is a valid JavaSpatialRDD and the filename is correctly formatted
val records: JavaSpatialRDD = // your spatial RDD here
records.saveAsShapefile("output.shp")
```

## API Test: `saveAsWKTFile`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveAsWKTFile(filename: String, wktColumn: Int, delimiter: Char = '\t', header: Boolean = true): Unit
def saveAsWKTFile(rdd: JavaSpatialRDD, filename: String, wktColumn: Int, delimiter: Char, header: Boolean): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:79  (+1 more definition site/overload)_

_Source doc:_ Save features to a CSV file where the geometry is encoded in WKT format @param filename the name of the output file @param wktColumn the index of the column that contains the WKT attribute @param delimiter the delimiter between attributes, tab by default @param header whether to write a header line or not, true by default

### Goal
The `saveAsWKTFile` function saves features from a `JavaSpatialRDD` to a CSV file, encoding geometries in Well-Known Text (WKT) format.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input spatial RDD containing features with geometries that need to be saved in WKT format.
- `filename` (`String`): The name of the output CSV file where the features will be saved.
- `wktColumn` (`Int`): The index of the column in the RDD that contains the WKT representation of the geometries.
- `delimiter` (`Char`): The character used to separate attributes in the CSV file; defaults to a tab character (`'\t'`).
- `header` (`Boolean`): A flag indicating whether to include a header line in the CSV file; defaults to `true`.

### Input
The caller must provide a `JavaSpatialRDD` containing features with geometries in WKT format, a valid filename for the output CSV, and the index of the column containing the WKT data. The delimiter and header options are optional.

### Output
Returns `Unit` — indicating that the operation has completed successfully without returning any value. The output is a CSV file containing the features with geometries encoded in WKT format.

### Valid Call Patterns
```scala
records.saveAsWKTFile("output.csv", 0, '\t', false)
```

### LLM Instruction Prompt
- Ensure that the `JavaSpatialRDD` provided contains valid geometries in the specified WKT column before calling `saveAsWKTFile`. The filename must be a valid path where the application has write permissions.

### Prompt Snippet
```text
To save your spatial features to a CSV file with geometries in WKT format, use the `saveAsWKTFile` method on your `JavaSpatialRDD` instance, specifying the output filename, the index of the WKT column, and any desired delimiter or header options.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 3x)_
- **[compile]** error: not enough arguments for constructor JavaRDD: (rdd: org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.IFeature])(implicit classTag: scala.reflect.ClassTag[edu.ucr.cs.bdlab.beast.geolite.I

### Fix Code Hint
```scala
// Ensure the wktColumn index is valid and the output path is accessible
if (wktColumn < 0 || wktColumn >= records.getNumColumns) {
  throw new IllegalArgumentException("Invalid wktColumn index.")
}
```

## API Test: `spatialPartition`
_Grounding: test-backed — usage mined from a real, passing test._

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
The `spatialPartition` function partitions a set of spatial features into distinct segments based on a specified spatial partitioner, optimizing data locality for distributed processing.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input RDD containing spatial features that need to be partitioned. This RDD should be created from spatial data sources such as CSV points or other supported formats.
- `spatialPartitioner` (`SpatialPartitioner`): An instance of a spatial partitioner that defines how the spatial features should be divided into partitions. This could be a grid-based partitioner or any custom partitioning strategy.

### Input
The caller must provide a `JavaSpatialRDD` containing spatial features, which can be loaded from formats such as CSV points. The spatial partitioner must be appropriately configured to match the spatial characteristics of the input data.

### Output
Returns `JavaPartitionedSpatialRDD` — a partitioned version of the input `JavaSpatialRDD`, where the spatial features are organized into partitions according to the specified spatial partitioner. This output is suitable for further spatial operations and analyses.

### Valid Call Patterns
```scala
val testFile = makeFileCopy("/test111.points")
val data: JavaSpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

### LLM Instruction Prompt
- When calling `spatialPartition`, ensure that the `rdd` is a valid `JavaSpatialRDD` and that the `spatialPartitioner` is correctly configured for the spatial data being processed.

### Prompt Snippet
```text
val partitionedFeatures: JavaPartitionedSpatialRDD = features.spatialPartition(partitioner)
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 2x)_
- **[compile]** error: value readGeoJSON is not a member of org.apache.spark.SparkContext
- **[compile]** error: value readShapefile is not a member of org.apache.spark.SparkContext

### Fix Code Hint
```scala
Ensure that the input RDD is populated with spatial features and that the spatial partitioner is suitable for the data's spatial distribution before calling `spatialPartition`.
```

## API Test: `summary`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def summary: Summary
def summary(rdd: JavaSpatialRDD): Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:171  (+2 more definition site/overload)_

_Source doc:_ Compute the geometric summary of the given RDD @param rdd the spatial RDD to compute its summary @return the summary of the given RDD

### Goal
The `summary` function computes the geometric summary statistics of a given spatial RDD, providing insights into the spatial distribution and characteristics of the data.

### Parameters
- `rdd` (`JavaSpatialRDD`): A spatial RDD containing geometrical features, which can be derived from various input formats such as shapefiles or CSV points.

### Input
The caller must provide a `JavaSpatialRDD` that has been properly loaded from a supported format (e.g., shapefile or CSV). The input data must be accessible and correctly formatted to ensure successful computation of the summary.

### Output
Returns `Summary` — an object representing the geometric summary of the provided spatial RDD, which includes statistics such as the minimum bounding rectangle (MBR) and other relevant spatial metrics.

### Valid Call Patterns
```scala
val rdd = sparkContext.shapefile("input.zip")
val summaryResult = rdd.summary()
```

### LLM Instruction Prompt
- When calling `summary`, ensure that the input is a valid `JavaSpatialRDD` and that it has been loaded from a compatible data source.

### Prompt Snippet
```text
To compute the geometric summary of a spatial RDD, use the `summary` method on the RDD instance, ensuring it is a valid `JavaSpatialRDD`.
```

### Common Failure Modes
- **[compile]** error: edu.ucr.cs.bdlab.beast.synopses.Summary does not take parameters _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the RDD is loaded correctly from a supported format and contains valid geometrical data before calling `summary`.
```

## API Test: `writeSpatialFile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def writeSpatialFile(filename: String, oformat: String, opts: BeastOptions = new BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String, opts: BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:94  (+2 more definition site/overload)_

_Source doc:_ Write this RDD as a spatial file with the given format and additional options @param filename the output file name @param oformat the output file format (short name) @param opts additional user options

### Goal
The `writeSpatialFile` function saves a `JavaSpatialRDD` as a spatial file in a specified format, allowing for the storage of geospatial data for further analysis or sharing.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input RDD containing spatial data that you want to write to a file. This RDD should be properly populated with spatial features.
- `filename` (`String`): The name of the output file where the spatial data will be saved. This should include the desired file extension (e.g., `.csv`).
- `oformat` (`String`): The format in which to save the spatial data. This is a short name representing the file format (e.g., `"envelope"` for envelope format).
- `opts` (`BeastOptions`): Additional options for writing the spatial file, such as separators for CSV files. This parameter can be customized based on user requirements.

### Input
The caller must provide a valid `JavaSpatialRDD` containing spatial features, a string for the filename that includes the appropriate file extension, and a string for the output format. The `BeastOptions` can be customized or left as default.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of writing the spatial data to the specified file.

### Valid Call Patterns
```scala
records.writeSpatialFile("output.csv", "envelope", "oseparator" -> ",")
```

### LLM Instruction Prompt
- When calling `writeSpatialFile`, ensure that the `JavaSpatialRDD` is properly populated and that the filename includes the correct file extension. The output format must be a recognized short name.

### Prompt Snippet
```text
To save your spatial data, use the `writeSpatialFile` method with a valid `JavaSpatialRDD`, a filename with the appropriate extension, and a recognized output format.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the RDD is populated and the filename is correctly formatted
val spatialData: JavaSpatialRDD = ...
spatialData.writeSpatialFile("output.csv", "envelope", new BeastOptions("oseparator" -> ","))
```
