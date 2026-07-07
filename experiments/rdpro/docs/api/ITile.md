# ITile

_The `componentType` method retrieves the data type of each component in a raster tile, which is essential for understanding the pixel value representation in…_

**Receiver:** instance — obtain a `ITile` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `componentType` **(primary)**, ★ `numComponents`, ★ `pixelLocations`, ⚠️ `extents`, ⚠️ `getPointValue`, ⚠️ `isDefined`, ⚠️ `isEmptyAt`, ⚠️ `pixelType`, ⚠️ `pixels`

---

## API Test: `componentType`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def componentType: DataType
def componentType: DataType
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:113  (+17 more definition site/overload)_

_Source doc:_ The type of each component in the data. Since convolution requires computing weighted average, we assume that the average is always a floating point number. @return

### Goal
The `componentType` method retrieves the data type of each component in a raster tile, which is essential for understanding the pixel value representation in geospatial raster processing.

### Parameters
_None._

### Input
The method does not require any input parameters. However, it is assumed that the raster tile has been properly initialized and contains valid data.

### Output
Returns `DataType` — this value represents the type of each component in the raster data, indicating whether the pixel values are integers, floating-point numbers, or another type.

### Valid Call Patterns
```scala
val rasterPath = new Path(makeFileCopy("/rasters/NLDAS-64.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Array[Double]]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
val tile = reader.readTile(0)
val dataType: DataType = tile.componentType
```

### LLM Instruction Prompt
- When calling `componentType`, ensure that the raster tile has been initialized and contains valid data to avoid runtime errors.

### Prompt Snippet
```text
Retrieve the component type of the raster tile to understand the pixel value representation.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the raster tile is properly initialized and contains valid data before calling componentType.
```

## API Test: `numComponents`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def numComponents: Int
def numComponents: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:137  (+9 more definition site/overload)_

### Goal
The `numComponents` function returns the number of components (bands) in a raster tile, which is essential for understanding the structure of multi-band raster datasets in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into the RDPro framework, typically from a GeoTIFF or HDF file. The raster must be properly initialized and accessible.

### Output
Returns `Int` — the number of components (bands) in the raster tile, indicating how many separate data layers are present in the tile.

### Valid Call Patterns
```scala
val rasterPath = new Path(makeFileCopy("/rasters/NLDAS-64.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Array[Double]]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
val tile = reader.readTile(0)
val components: Int = tile.numComponents
```

### LLM Instruction Prompt
- Ensure that the raster tile is properly initialized and that the `numComponents` method is called on a valid tile object.

### Prompt Snippet
```text
Call the numComponents method on a raster tile to determine the number of bands it contains.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the raster tile is properly initialized before calling numComponents
val tile = reader.readTile(0)
if (tile != null) {
  val components: Int = tile.numComponents
} else {
  throw new IllegalArgumentException("Tile is not initialized.")
}
```

## API Test: `pixelLocations`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def pixelLocations: Iterator[(Int, Int)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:81_

_Source doc:_ An iterator that goes over all pixels in this tile @return an iterator that goes over all pixels (whether empty or not) in this tile

### Goal
The `pixelLocations` function provides an iterator over the pixel coordinates of a raster tile, allowing users to access each pixel's position for further processing or analysis.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into memory. This tile should be part of a raster dataset, typically loaded using methods like `sc.geoTiff(...)`. Ensure that the tile is properly initialized and contains pixel data.

### Output
Returns `Iterator[(Int, Int)]` — an iterator of tuples where each tuple represents the (x, y) coordinates of a pixel in the tile. The coordinates correspond to the pixel's position within the tile, regardless of whether the pixel is defined or empty.

### Valid Call Patterns
```scala
for ((x, y) <- tile.pixelLocations) {
  // Process each pixel location
}
```

### LLM Instruction Prompt
- When calling `pixelLocations`, ensure that the tile is properly initialized and contains pixel data. The function should be called on an instance of a tile that has been loaded from a raster dataset.

### Prompt Snippet
```text
To iterate over the pixel locations of a raster tile, use the `pixelLocations` method on the tile instance. Ensure the tile is initialized and contains pixel data.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the tile is properly initialized before calling pixelLocations
val tile: ITile[Int] = ... // Load or create the tile
if (tile != null) {
  for ((x, y) <- tile.pixelLocations) {
    // Process each pixel location
  }
}
```

## API Test: `extents`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def extents: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:181  (+1 more definition site/overload)_

_Source doc:_ The extents of the RasterMetadata in model space as a rectangular polygon @return

### Goal
The `extents` function retrieves the spatial extents of the raster data represented by the `RasterMetadata` as a rectangular polygon in model space.

### Parameters
_None._

### Input
The caller must provide a `RasterMetadata` object that contains the raster data for which the extents are to be calculated.

### Output
Returns `Geometry` — a rectangular polygon representing the spatial extents of the raster data in model space.

### Valid Call Patterns
```scala
val extents: Geometry = metadata.extents
```

### LLM Instruction Prompt
- When calling `extents`, ensure that the `RasterMetadata` object is properly initialized and contains valid raster data.

### Prompt Snippet
```text
Retrieve the extents of the raster data using the extents method on the RasterMetadata object.
```

### Common Failure Modes
- **[compile]** error: value geoTiffRDD is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the RasterMetadata object is properly initialized before calling extents
val metadata = new RasterMetadata(0, 1, 100, 200, 32, 64, 4326, AffineTransform.getQuadrantRotateInstance(33))
val extents: Geometry = metadata.extents
```

## API Test: `getPointValue`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must provide valid world coordinates (longitude and latitude) that correspond to a pixel in the loaded raster dataset. The raster must be loaded using a compatible method (e.g., `sc.geoTiff[T]`), where `T` matches the pixel type of the raster.

### Output
Returns `T` — the value of the pixel that contains the specified point, which may represent a single band value or an array of values for multi-band rasters.

### Valid Call Patterns
```scala
val tile: ITile[Int] = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val value: Int = tile.getPointValue(23.224, 32.415)
```

### LLM Instruction Prompt
- Ensure that the coordinates provided to `getPointValue` are within the bounds of the raster dataset. The raster must be loaded and accessible before calling this method.

### Prompt Snippet
```text
Retrieve the pixel value at the specified longitude and latitude using the getPointValue method.
```

### Common Failure Modes
- **[runtime]** java.lang.ClassCastException: class [F cannot be cast to class java.lang.Integer ([F and java.lang.Integer are in module java.base of loader 'bootstrap') _(seen 3x)_
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]

### Fix Code Hint
```scala
// Ensure the raster is loaded and the coordinates are within bounds before calling getPointValue
if (isValidCoordinate(x, y)) {
  val value = tile.getPointValue(x, y)
} else {
  throw new IllegalArgumentException("Coordinates are out of bounds.")
}
```

## API Test: `isDefined`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
@inline def isDefined(i: Int, j: Int): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126_

_Source doc:_ Checks if the given pixel is defined (not empty) @param i the index of the column @param j the index of the row @return `true` if pixel has a valid value or `false` if it does not.

### Goal
Determines whether a specific pixel in a raster is defined (i.e., contains a valid value) based on its column and row indices.

### Parameters
- `i` (`Int`): The index of the column in the raster, representing the horizontal position of the pixel.
- `j` (`Int`): The index of the row in the raster, representing the vertical position of the pixel.

### Input
The caller must provide valid integer indices `i` and `j` that correspond to the dimensions of the raster being processed. The raster must be loaded and accessible in the context where `isDefined` is called.

### Output
Returns `Boolean` — `true` if the pixel at the specified indices has a valid value (is defined), or `false` if it does not (is empty).

### Valid Call Patterns
```scala
val isPixelDefined: Boolean = raster.isDefined(columnIndex, rowIndex)
```

### LLM Instruction Prompt
- Ensure that the indices `i` and `j` are within the bounds of the raster's dimensions before calling `isDefined`.

### Prompt Snippet
```text
Check if the pixel at column index `i` and row index `j` is defined using the `isDefined` method.
```

### Common Failure Modes
- **[compile]** error: value getWidth is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 3x)_
- **[compile]** error: value cols is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]

### Fix Code Hint
```scala
// Ensure indices are within bounds before calling isDefined
if (i >= 0 && i < raster.cols && j >= 0 && j < raster.rows) {
    val isDefined = raster.isDefined(i, j)
} else {
    throw new IllegalArgumentException("Indices are out of bounds.")
}
```

## API Test: `isEmptyAt`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def isEmptyAt(x: Double, y: Double): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:114_

_Source doc:_ Check if the pixel that contains the given location is empty @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return `true` if the pixel at the location is empty, i.e., contains no data

### Goal
The `isEmptyAt` function checks whether the pixel at a specified geographic location contains no data, which is essential for accurate geospatial analysis.

### Parameters
- `x` (`Double`): The x-coordinate of the point, typically representing longitude in decimal degrees.
- `y` (`Double`): The y-coordinate of the point, typically representing latitude in decimal degrees.

### Input
The function requires valid geographic coordinates (longitude and latitude) as input. The coordinates must correspond to a pixel within the raster data loaded into the RDPro environment.

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
- When calling `isEmptyAt`, ensure that the coordinates provided are within the bounds of the raster data and that the raster has been properly initialized and loaded.

### Prompt Snippet
```text
Check if the pixel at the specified coordinates is empty using the isEmptyAt method.
```

### Common Failure Modes
- **[compile]** error: value isEmptyAt is not a member of edu.ucr.cs.bdlab.raptor.GeoTiffReader[Int] _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the raster is initialized and that the coordinates are within the valid range of the raster before calling isEmptyAt.
```

## API Test: `pixelType`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def pixelType: DataType
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138_

_Source doc:_ Returns the type of the pixel as an SQL data type @return the type of the pixel values

### Goal
The `pixelType` function retrieves the SQL data type of the pixel values contained within a raster tile, which is essential for understanding the data type being processed in geospatial raster analytics.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into an `RDD` or `RasterRDD`. The raster must be of a compatible type that has been defined during the loading process (e.g., `sc.geoTiff[Int]` for integer data).

### Output
Returns `DataType` — this value represents the SQL data type of the pixel values in the raster tile, which can be used for further processing or analysis.

### Valid Call Patterns
```scala
val readRaster = new RasterFileRDD(sparkContext, "path/to/raster.tif", new BeastOptions())
val pixelDataType = readRaster.pixelType
```

### LLM Instruction Prompt
- When calling `pixelType`, ensure that the raster data has been properly loaded and is accessible. The function should be called on an instance of `RasterFileRDD` or a similar raster data structure.

### Prompt Snippet
```text
To determine the pixel type of a raster tile, use the `pixelType` method on the loaded raster data.
```

### Common Failure Modes
- **[compile]** error: value pixelType is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the raster is loaded correctly and that the pixel type is compatible with the expected SQL data types before calling `pixelType`.
```

## API Test: `pixels`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def pixels: Iterator[(Int, Int, T)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84_

### Goal
The `pixels` method retrieves an iterator over the pixel values of a raster tile, providing their corresponding row and column indices.

### Parameters
_None._

### Input
The caller must provide a raster tile that has been loaded into an `ITile` object. The raster data should be in a compatible format, such as GeoTIFF, and must be accessible in the Spark context.

### Output
Returns `Iterator[(Int, Int, T)]` — each element of the iterator is a tuple containing the row index (Int), the column index (Int), and the pixel value (T) at that position in the raster tile.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val pixelIterator: Iterator[(Int, Int, Int)] = raster.first().pixels
```

### LLM Instruction Prompt
- When calling `pixels`, ensure that the raster tile is properly loaded and that the Spark context is active. The method should be called on an instance of `ITile`.

### Prompt Snippet
```text
To retrieve pixel values from a raster tile, use the `pixels` method on an `ITile` instance after loading the raster data.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: pixel value is not an Int _(seen 2x)_
- **[runtime]** java.lang.ClassCastException: class [F cannot be cast to class java.lang.Integer ([F and java.lang.Integer are in module java.base of loader 'bootstrap') _(seen 2x)_

### Fix Code Hint
```scala
Ensure that the raster tile is loaded correctly and is not empty before calling `pixels`. For example:
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_raster.tif")
val pixelIterator: Iterator[(Int, Int, Int)] = raster.first().pixels
```
