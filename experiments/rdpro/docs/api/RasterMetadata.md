# RasterMetadata

_The `tileIDs` function retrieves an iterator over all tile IDs present in the raster, facilitating operations that require knowledge of the raster's tile…_

**Receiver:** instance — obtain a `RasterMetadata` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `tileIDs` **(primary)**, ⚠️ `envelope`, ⚠️ `getTileIDAtPixel`, ⚠️ `getTileIDAtPoint`, ⚠️ `gridToModel`, ⚠️ `modelToGrid`, ⚠️ `numTiles`, ⚠️ `rasterHeight`, ⚠️ `rasterWidth`, ⚠️ `rescale`, ⚠️ `retile`

---

## API Test: `tileIDs`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def tileIDs: Iterator[Int]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:91_

_Source doc:_ An iterator that goes over all tile IDs @return an iterator that iterates over all tile IDs in this raster

### Goal
The `tileIDs` function retrieves an iterator over all tile IDs present in the raster, facilitating operations that require knowledge of the raster's tile structure.

### Parameters
_None._

### Input
The caller must provide a raster object that has been properly initialized and contains tile data. The raster should be loaded from a supported format such as GeoTIFF.

### Output
Returns `Iterator[Int]` — an iterator that represents the IDs of all tiles in the raster, allowing for iteration over each tile ID for further processing.

### Valid Call Patterns
```scala
val rasterPath = new Path(locateResource("/rasters/FRClouds.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
  for (tileID <- reader.metadata.tileIDs) {
    // Process each tile ID as needed
  }
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- When calling `tileIDs`, ensure that the raster has been initialized and contains valid tile data. Use the returned iterator to access each tile ID for further operations.

### Prompt Snippet
```text
To retrieve all tile IDs from a raster, first ensure the raster is properly initialized. Then, call the `tileIDs` method to obtain an iterator over the tile IDs.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly using `sc.geoTiff(...)` or another supported method before calling `tileIDs`. Check for any initialization errors in the raster loading process.
```

## API Test: `envelope`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def envelope: java.awt.Rectangle
override def envelope: java.awt.Rectangle
def envelope: Envelope
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:24  (+4 more definition site/overload)_

### Goal
The `envelope` function retrieves the bounding rectangle that encompasses the spatial extent of a raster or vector dataset.

### Parameters
_None._

### Input
The caller must ensure that the dataset (raster or vector) has been properly loaded and is accessible within the Spark context. The dataset should be in a compatible format, such as GeoTIFF or CSV, and must have a defined spatial extent.

### Output
Returns `java.awt.Rectangle` — this value represents the bounding box of the dataset, defined by its minimum and maximum x and y coordinates.

### Valid Call Patterns
```scala
val boundingBox: java.awt.Rectangle = raster.envelope
```

### LLM Instruction Prompt
- When calling `envelope`, ensure that the dataset is loaded and has a defined spatial extent. The call should be made on a valid raster or vector object.

### Prompt Snippet
```text
Retrieve the bounding rectangle of the dataset using the envelope method.
```

### Common Failure Modes
- **[compile]** error: value envelope is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 3x)_
- **[compile]** error: value envelope is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Int]]

### Fix Code Hint
```scala
// Ensure the dataset is loaded and has a valid spatial extent before calling envelope
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_geotiff.tif")
val boundingBox: java.awt.Rectangle = raster.envelope
```

## API Test: `getTileIDAtPixel`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getTileIDAtPixel(iPixel: Int, jPixel: Int): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:69_

_Source doc:_ Computes the ID of the tile that contains the given pixel. Tiles are numbered in row-wise ordering. @param iPixel the position of the column of the pixel @param jPixel the position of the row of the pixel @return a unique identifier for the tile that contains this pixel location

### Goal
The `getTileIDAtPixel` function retrieves the unique identifier of the tile that contains a specified pixel in a raster dataset, facilitating efficient access to raster data in geospatial analysis.

### Parameters
- `iPixel` (`Int`): The column index of the pixel within the raster, where the value should be a non-negative integer less than the raster's width.
- `jPixel` (`Int`): The row index of the pixel within the raster, where the value should be a non-negative integer less than the raster's height.

### Input
The caller must provide valid pixel indices (`iPixel` and `jPixel`) that correspond to the dimensions of the raster being processed. The raster must be loaded and accessible in the context where this function is called.

### Output
Returns `Int` — a unique identifier for the tile that contains the specified pixel location, which is determined based on a row-wise ordering of tiles.

### Valid Call Patterns
```scala
val tileID = reader.metadata.getTileIDAtPixel(37, 24)
```

### LLM Instruction Prompt
- Ensure that the pixel indices provided are within the bounds of the raster's dimensions to avoid index out-of-bounds errors.

### Prompt Snippet
```text
Call `getTileIDAtPixel` with valid pixel indices to retrieve the tile ID for the specified pixel location in the raster.
```

### Common Failure Modes
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the pixel indices are within the valid range before calling the function
if (iPixel >= 0 && iPixel < rasterWidth && jPixel >= 0 && jPixel < rasterHeight) {
    val tileID = reader.metadata.getTileIDAtPixel(iPixel, jPixel)
} else {
    throw new IllegalArgumentException("Pixel indices are out of bounds.")
}
```

## API Test: `getTileIDAtPoint`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getTileIDAtPoint(x: Double, y: Double): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:81_

_Source doc:_ Returns the ID of the tile that contains the given point location in model (world) space @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the ID of the tile that contains this pixel or -1 if the point is outside the input space

### Goal
The `getTileIDAtPoint` function retrieves the ID of the raster tile that contains a specified geographic point, enabling efficient access to raster data for geospatial analysis.

### Parameters
- `x` (`Double`): The x-coordinate of the point in model (world) space, typically representing longitude.
- `y` (`Double`): The y-coordinate of the point in model (world) space, typically representing latitude.

### Input
The caller must provide valid geographic coordinates (longitude and latitude) as `Double` values. The raster data must be loaded and accessible, and the point must lie within the bounds of the raster dataset.

### Output
Returns `Int` — the ID of the tile that contains the specified point. If the point is outside the input space, it returns -1.

### Valid Call Patterns
```scala
val tileId: Int = reader.metadata.getTileIDAtPoint(23.224, 32.415)
```

### LLM Instruction Prompt
- Ensure that the x and y coordinates provided are within the bounds of the raster dataset. The raster must be properly initialized and accessible before calling `getTileIDAtPoint`.

### Prompt Snippet
```text
Retrieve the tile ID for the geographic coordinates (23.224, 32.415) using the getTileIDAtPoint method.
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 2x)_
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Double]] _(seen 2x)_

### Fix Code Hint
```scala
// Ensure the raster is loaded and the coordinates are within bounds before calling getTileIDAtPoint
if (x >= minLongitude && x <= maxLongitude && y >= minLatitude && y <= maxLatitude) {
  val tileId: Int = reader.metadata.getTileIDAtPoint(x, y)
} else {
  println("Coordinates are outside the raster bounds.")
}
```

## API Test: `gridToModel`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def gridToModel(i: Double, j: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:150_

_Source doc:_ Converts a point location from the grid (pixel) space to the model (world) space @param i the position of the column @param j the position of the row @param outPoint the output point that contains the model coordinates

### Goal
`gridToModel` converts pixel coordinates (grid space) into geographic coordinates (model space) for raster data.

### Parameters
- `i` (`Double`): The column index (horizontal position) of the pixel in the raster grid.
- `j` (`Double`): The row index (vertical position) of the pixel in the raster grid.
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
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 4x)_

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

## API Test: `modelToGrid`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must provide valid geographic coordinates for `x` and `y`, which should correspond to the model space of the raster being processed. The `outPoint` must be an instance of `Point2D.Double` that is initialized before calling the function.

### Output
Returns `Unit` — this indicates that the function does not return a value but instead modifies the `outPoint` parameter to contain the grid coordinates corresponding to the input model coordinates.

### Valid Call Patterns
```scala
reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)
```

### LLM Instruction Prompt
- When calling `modelToGrid`, ensure that the `outPoint` is a properly initialized `Point2D.Double` instance to store the output coordinates.

### Prompt Snippet
```text
Call the modelToGrid function with valid longitude and latitude values, and ensure the outPoint is initialized to receive the grid coordinates.
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 3x)_
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Double]

### Fix Code Hint
```scala
val outPoint = new Point2D.Double
modelToGrid(-6.679688, 53.613281, outPoint) // Ensure outPoint is initialized
```

## API Test: `numTiles`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must provide a raster layer that has been loaded into the RDPro framework, typically from a GeoTIFF or HDF file. The raster must be properly initialized and accessible within the Spark context.

### Output
Returns `Int` — the total number of tiles in the raster layer, representing how the raster data is partitioned for processing.

### Valid Call Patterns
```scala
val numTiles: Int = raster.metadata.numTiles
```

### LLM Instruction Prompt
- Ensure that the raster layer is properly initialized and accessible before calling `numTiles`. The raster must be loaded using supported formats like GeoTIFF or HDF.

### Prompt Snippet
```text
To get the total number of tiles in a raster layer, use the `numTiles` method on the raster's metadata.
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling numTiles
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val totalTiles: Int = raster.metadata.numTiles
```

## API Test: `rasterHeight`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def rasterHeight: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:52_

_Source doc:_ Total number of rows (scanlines) in the raster layer

### Goal
Retrieve the total number of rows (scanlines) in a raster layer, which is essential for understanding the dimensions of the raster data being processed.

### Parameters
_None._

### Input
The caller must provide a raster object that has been initialized and contains raster data, typically loaded from a GeoTIFF file using `sc.geoTiff(...)`. The raster must be accessible and correctly formatted.

### Output
Returns `Int` — the total number of rows (scanlines) in the raster layer, representing the vertical dimension of the raster data.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val height: Int = raster.rasterHeight
```

### LLM Instruction Prompt
- Ensure that the raster object is properly initialized and contains valid raster data before calling `rasterHeight`.

### Prompt Snippet
```text
To get the height of the raster, use the rasterHeight method on a valid raster object.
```

### Common Failure Modes
- **[compile]** error: type RasterRDD takes type parameters _(seen 3x)_
- **[compile]** error: value rasterHeight is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Int]]

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling rasterHeight
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val height: Int = raster.rasterHeight
```

## API Test: `rasterWidth`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def rasterWidth: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:49_

_Source doc:_ Total number of columns in the raster layer

### Goal
Retrieve the total number of columns (width) in the raster layer, which is essential for understanding the raster's dimensions in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster object that has been initialized and contains valid raster data, typically loaded from a GeoTIFF file using `sc.geoTiff(...)`.

### Output
Returns `Int` — the total number of columns in the raster layer, representing the width of the raster in pixel units.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val width: Int = raster.metadata.rasterWidth
```

### LLM Instruction Prompt
- Ensure that the raster object is properly initialized and contains valid raster data before calling `rasterWidth`.

### Prompt Snippet
```text
To get the width of the raster, use the `rasterWidth` method on the raster metadata after loading the raster data.
```

### Common Failure Modes
- **[compile]** error: type RasterRDD takes type parameters _(seen 3x)_
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Int]]

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before accessing rasterWidth
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_valid_raster.tif")
val width: Int = raster.metadata.rasterWidth
```

## API Test: `rescale`
_Grounding: test-backed — usage mined from a real, passing test._

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
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to determine the pixel values in the rescaled raster when a target pixel overlaps multiple source pixels. Options include nearest neighbor and average interpolation.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, along with the desired pixel dimensions for width and height. The input raster must be properly formatted and accessible, typically loaded from a GeoTIFF or HDF file.

### Output
Returns `RasterRDD[T]` — a new raster dataset with the specified width and height, preserving the original CRS and tile size. The output is a distributed collection of raster tiles that can be further processed or saved.

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
- When calling `rescale`, ensure that the input raster is a valid `RasterRDD[T]` and that the specified width and height are appropriate for the desired output resolution.

### Prompt Snippet
```text
To rescale a raster dataset, use the `rescale` method on a `RasterRDD` with the desired pixel dimensions and optional parameters for unified raster and interpolation method.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0 (TID 5) (192.168.68.50 executor driver): java.lan _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly and the dimensions are positive integers
val raster: RasterRDD[Int] = sc.geoTiff[Int]("path_to_your_file.tif")
val rescaled = raster.rescale(360, 180) // Ensure 360 and 180 are valid dimensions
```

## API Test: `retile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def retile(tileWidth: Int, tileHeight: Int)
def retile[T: ClassTag](raster: RasterRDD[T], tileWidth: Int, tileHeight: Int): RasterRDD[T]
def retile(newTileWidth: Int, newTileHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566  (+2 more definition site/overload)_

_Source doc:_ Regrids the given raster to the target tile width and height @param raster the raster to regrid @param tileWidth the new tile width in pixels @param tileHeight the new tile height in pixels @tparam T the type of the pixel values in the raster @return a new raster with the given tile width and height

### Goal
The `retile` function regrids a given raster into specified tile dimensions, facilitating efficient processing and analysis of large geospatial datasets.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster data that needs to be regridded. It is expected to be a distributed collection of raster tiles with pixel values of type `T`.
- `tileWidth` (`Int`): The desired width of the new tiles in pixels. This value determines how wide each tile will be after the regridding operation.
- `tileHeight` (`Int`): The desired height of the new tiles in pixels. This value determines how tall each tile will be after the regridding operation.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, where `T` is the type of pixel values (e.g., `Int`, `Float`). The raster must be properly loaded and accessible in the Spark context. The specified tile dimensions must be positive integers.

### Output
Returns `RasterRDD[T]` — a new raster represented as a distributed collection of tiles, each with the specified width and height. The output retains the original pixel type `T`.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")
```

### LLM Instruction Prompt
- When calling `retile`, ensure that the input raster is a valid `RasterRDD[T]` and that the tile dimensions are positive integers.

### Prompt Snippet
```text
To regrid a raster, use the retile function with the desired tile width and height, ensuring the raster is properly loaded.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0 (TID 5) (192.168.68.50 executor driver): java.lan _(seen 3x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 14 in stage 0.0 failed 1 times, most recent failure: Lost task 14.0 in stage 0.0 (TID 14) (192.168.68.50 executor driver): java.

### Fix Code Hint
```scala
// Ensure that the tile dimensions are positive integers and the raster is correctly loaded.
val retiled = raster.retile(64, 64) // Ensure 64 is a positive integer
```
