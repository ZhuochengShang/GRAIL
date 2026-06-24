# RDPro — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `buildIndex`

### Signature
```scala
def buildIndex(sparkContext: SparkContext, dir: String, indexFile: String): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:186_

_Source doc:_ Build a raster index on all GeoTIFF files in a directory. @param sparkContext spark context to parallelize index creation @param dir the directory that contains raster files @param indexFile the path of the index file to write

### Goal
The `buildIndex` function creates a raster index for all GeoTIFF files located in a specified directory, facilitating efficient access and processing of raster data.

### Parameters
- `sparkContext` (`SparkContext`): The Spark context used to parallelize the index creation process. It is expected to be initialized and configured for the Spark application.
- `dir` (`String`): The directory path containing the GeoTIFF raster files that will be indexed. This directory must exist and contain valid GeoTIFF files.
- `indexFile` (`String`): The file path where the generated index will be written. This should be a valid path where the application has write permissions.

### Input
The caller must provide:
- A valid `SparkContext` instance.
- A directory containing GeoTIFF files (e.g., `"/path/to/raster/files"`).
- A valid file path for the index output (e.g., `"/path/to/output/index.csv"`).

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the side effect of creating an index file at the specified path.

### Valid Call Patterns
```scala
val dir = "/path/to/raster/files"
val indexFile = "/path/to/output/index.csv"
buildIndex(sparkContext, dir, indexFile)
```

### LLM Instruction Prompt
- Ensure that the `sparkContext` is properly initialized and that the `dir` contains valid GeoTIFF files before calling `buildIndex`. The `indexFile` path must be writable.

### Prompt Snippet
```text
To create a raster index for GeoTIFF files, use the buildIndex function with a valid SparkContext, the directory containing the raster files, and the desired output path for the index file.
```

### Common Failure Modes
- The specified directory (`dir`) does not exist or does not contain any GeoTIFF files, leading to an empty index.
- The application lacks write permissions for the specified `indexFile` path, resulting in a failure to create the index file.
- An improperly initialized `SparkContext` may cause the function to fail during execution.

### Fix Code Hint
```scala
// Ensure the directory exists and contains GeoTIFF files before calling buildIndex
val dir = "/path/to/raster/files"
val indexFile = "/path/to/output/index.csv"
if (new File(dir).exists() && new File(dir).listFiles().exists(_.getName.endsWith(".tif"))) {
    buildIndex(sparkContext, dir, indexFile)
} else {
    println("Directory does not exist or contains no GeoTIFF files.")
}
```

## API Test: `compute`

### Signature
```scala
def compute(split: Partition, context: TaskContext): Iterator[ITile[T]]
def compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119  (+1 more definition site/overload)_

_Source doc:_ Compute the intersections for the given linear ring @param pID the ID of the polygon @param ring the list of coordinates that make the ring already projected to the raster space @param w the width of the raster in pixels @param h the height of the raster in pixels

### Goal
Compute the intersections of a linear ring with a raster grid, facilitating geospatial analysis in RDPro.

### Parameters
- `pID` (`Int`): The ID of the polygon that the linear ring represents. This should be a unique identifier for the polygon within the context of the analysis.
- `ring` (`CoordinateSequence`): A sequence of coordinates that define the vertices of the linear ring, which must be projected to the raster space for accurate intersection calculations.
- `w` (`Int`): The width of the raster in pixels, which determines the horizontal resolution of the raster grid.
- `h` (`Int`): The height of the raster in pixels, which determines the vertical resolution of the raster grid.

### Input
The caller must provide a valid `pID`, a `CoordinateSequence` representing the ring, and integer values for `w` and `h` that define the raster dimensions. The `ring` must be properly projected to match the raster's coordinate reference system.

### Output
Returns `Unit` — this indicates that the function performs an operation without returning a value. The result of the computation is applied internally, affecting the state of the raster processing.

### Valid Call Patterns
```scala
val pID = 1
val ring: CoordinateSequence = // initialize with appropriate coordinates
val width = 100
val height = 100
compute(pID, ring, width, height)
```

### LLM Instruction Prompt
- Ensure that the `ring` is correctly projected to the raster space before calling `compute`. The `pID` should be unique and relevant to the polygon being processed.

### Prompt Snippet
```text
Compute the intersections for the polygon with ID 1 using the provided ring coordinates and raster dimensions.
```

### Common Failure Modes
- Providing a `CoordinateSequence` that is not projected to the raster space may lead to incorrect intersection results.
- Using invalid or negative values for `w` and `h` can cause runtime errors or unexpected behavior.

### Fix Code Hint
```scala
// Ensure the ring is projected correctly and dimensions are positive integers
val validRing: CoordinateSequence = // project your coordinates to raster space
val validWidth = 100
val validHeight = 100
compute(pID, validRing, validWidth, validHeight)
```

## API Test: `count`

### Signature
```scala
def count: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860_

### Goal
The `count` function returns the number of tiles in the raster dataset, which is essential for understanding the size and structure of the data being processed.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded into an RDD format, such as `RDD[ITile]`, using methods like `sc.geoTiff`.

### Output
Returns `Int` — the total number of tiles in the raster dataset, representing the granularity of the raster data.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
val tileCount = raster.count
```

### LLM Instruction Prompt
- Ensure that the `count` function is called on a valid raster dataset that has been properly loaded into an RDD format.

### Prompt Snippet
```text
To get the number of tiles in your raster dataset, use the count method on the loaded RDD.
```

### Common Failure Modes
- Calling `count` on an uninitialized or empty raster dataset may lead to unexpected results or errors.
- Attempting to call `count` on a non-raster RDD will result in a type mismatch error.

### Fix Code Hint
```scala
// Ensure the raster dataset is loaded correctly before calling count
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
val tileCount = raster.count
```

## API Test: `create`

### Signature
```scala
def create[T](tiles: Array[MemoryTile[T]]): MemoryTileWindow[T]
def create[T: ClassTag](tileID: Int, metadata: RasterMetadata, rasterFeature: RasterFeature, numValues: Int): MemoryTileWindow[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTileWindow.scala:98  (+1 more definition site/overload)_

### Goal
Creates a `MemoryTileWindow` from the specified tile ID, metadata, raster feature, and number of values, facilitating efficient raster processing in a distributed environment.

### Parameters
- `tileID` (`Int`): An identifier for the tile, which should be unique within the context of the raster processing operation.
- `metadata` (`RasterMetadata`): Contains information about the raster's dimensions, resolution, coordinate reference system (CRS), and other relevant properties.
- `rasterFeature` (`RasterFeature`): Represents the characteristics of the raster data, including file names and associated metadata.
- `numValues` (`Int`): The number of values per pixel in the raster, which defines the dimensionality of the data (e.g., single-band or multi-band).

### Input
The caller must provide a valid `tileID`, a `RasterMetadata` object with appropriate dimensions and CRS, a `RasterFeature` that describes the raster data, and an integer for `numValues` that matches the expected pixel structure.

### Output
Returns `MemoryTileWindow[T]` — a window of memory tiles that allows for efficient access and manipulation of raster data in a distributed processing context.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326, new AffineTransform())
val rasterFeature = RasterFeature.create(Array("fileName"), Array("testFile.tif"))
val tileWindow = create(0, metadata, rasterFeature, 1)
```

### LLM Instruction Prompt
- Ensure that the `tileID`, `metadata`, `rasterFeature`, and `numValues` are correctly defined and match the expected types and structures before calling `create`.

### Prompt Snippet
```text
Create a MemoryTileWindow using the specified tile ID, metadata, raster feature, and number of values.
```

### Common Failure Modes
- Providing a `tileID` that is not unique within the context of the operation.
- Using `RasterMetadata` with dimensions or CRS that do not match the raster data.
- Specifying a `numValues` that does not correspond to the actual number of values per pixel in the raster data.

### Fix Code Hint
```scala
Check that the `tileID` is unique, ensure the `metadata` matches the raster data dimensions, and verify that `numValues` aligns with the pixel structure of the raster.
```

## API Test: `createDateFilter`

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
The `createDateFilter` function generates a filter that allows for the selection of data paths based on a specified date range, facilitating the processing of time-sensitive geospatial raster data.

### Parameters
- `dateStart` (`String`): The start date of the range, formatted as "yyyy.mm.dd" (inclusive). This parameter defines the earliest date that will be accepted by the filter.
- `dateEnd` (`String`): The end date of the range, formatted as "yyyy.mm.dd" (inclusive). This parameter defines the latest date that will be accepted by the filter.

### Input
The caller must provide two date strings in the format "yyyy.mm.dd" that represent the start and end of the date range. The dates must be valid and in chronological order, with `dateStart` being earlier than or equal to `dateEnd`.

### Output
Returns `PathFilter` — an object that represents a filter for file paths, which will match all paths that fall within the specified date range, inclusive of both start and end dates.

### Valid Call Patterns
```scala
val dateFilter = createDateFilter("2001.02.15", "2005.02.11")
assert(dateFilter.accept(new Path("2001.02.15")))
assert(dateFilter.accept(new Path("2005.02.11")))
assert(dateFilter.accept(new Path("2003.07.15")))
assert(!dateFilter.accept(new Path("2005.02.12")))
assert(!dateFilter.accept(new Path("2001.01.31")))
```

### LLM Instruction Prompt
- When calling `createDateFilter`, ensure that both `dateStart` and `dateEnd` are provided as valid date strings in the "yyyy.mm.dd" format, and that `dateStart` is not later than `dateEnd`.

### Prompt Snippet
```text
Create a date filter for paths between "2001.02.15" and "2005.02.11".
```

### Common Failure Modes
- Providing invalid date formats that do not conform to "yyyy.mm.dd".
- Setting `dateStart` to a date that is later than `dateEnd`, which will result in an incorrect filter.

### Fix Code Hint
```scala
// Ensure that dateStart is earlier than or equal to dateEnd and both are in the correct format.
val dateFilter = createDateFilter("start_date", "end_date") // Replace with valid date strings
```

## API Test: `createTileIDFilter`

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
Create a path filter that selects tiles based on their spatial extents in the Sinusoidal projection, facilitating efficient raster processing in geospatial analysis.

### Parameters
- `rect` (`Rectangle2D`): A rectangle defining the spatial extents in the Sinusoidal space. This rectangle should encompass the area of interest for which tiles are to be selected.

### Input
The caller must provide a `Rectangle2D` object that specifies the extents of the area in the Sinusoidal space. This input is essential for determining which tiles to filter based on their filenames.

### Output
Returns `PathFilter` — a filter that matches tile paths based on the specified rectangle. The filter will only accept paths that correspond to tiles intersecting with the defined rectangle, specifically matching the `hxxvyy` naming convention.

### Valid Call Patterns
```scala
val tileIDFilter = createTileIDFilter(new Rectangle2D.Double(Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale, Math.toRadians(29.0) * HDF4Reader.Scale, Math.toRadians(49.0) * HDF4Reader.Scale))
assert(tileIDFilter.accept(new Path("tile-h03v03.hdf")))
assert(tileIDFilter.accept(new Path("tile-h06v07.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h02v09.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h07v06.hdf")))
```

### LLM Instruction Prompt
- When calling `createTileIDFilter`, ensure that the `rect` parameter is a valid `Rectangle2D` representing the desired spatial extents in the Sinusoidal projection.

### Prompt Snippet
```text
Create a path filter using `createTileIDFilter` with a specified `Rectangle2D` to select tiles that match the given spatial extents in the Sinusoidal space.
```

### Common Failure Modes
- Providing a `Rectangle2D` that does not correspond to any tile extents may result in a filter that accepts no paths.
- Incorrectly formatted tile paths (not following the `hxxvyy` naming convention) will not be accepted by the filter.

### Fix Code Hint
```scala
Ensure that the `Rectangle2D` provided accurately represents the area of interest and that the tile paths conform to the expected naming convention (e.g., "tile-hxxvyy.hdf").
```

## API Test: `divideScene`

### Signature
```scala
def divideScene[T: ClassTag](raster: RasterRDD[T], targetMetadata: RasterMetadata, numTilesX: Int, numTilesY: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625_

_Source doc:_ Divides an existing RDD into a new RDD such that every group of tiles is brought together into one Metadata. This is helpful when writing the resulting RDD to files because each group of tiles will be written to a separate file. @param raster the input raster to repartition @param targetMetadata the metadata of the target (output) raster @param numTilesX number of tiles to combine together into one metadata @param numTilesY number of tiles to combine together into one metadata @tparam T @return

### Goal
`divideScene` partitions an existing raster RDD into smaller groups of tiles based on specified metadata, facilitating efficient writing of the resulting tiles to separate files.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster RDD that contains the pixel data to be repartitioned. It is expected to be a valid RasterRDD containing geospatial raster data.
- `targetMetadata` (`RasterMetadata`): Metadata for the output raster, which defines the spatial characteristics (e.g., dimensions, coordinate reference system) of the resulting tiles.
- `numTilesX` (`Int`): The number of tiles to combine horizontally into one metadata group. This determines how many tiles will be processed together in the output.
- `numTilesY` (`Int`): The number of tiles to combine vertically into one metadata group. This also influences the grouping of tiles in the output.

### Input
The caller must provide a valid `RasterRDD` containing raster data, a `RasterMetadata` object that specifies the desired output characteristics, and two integers representing the number of tiles to combine in the X and Y dimensions. The input raster must be properly formatted and accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster RDD where each group of tiles is combined into a single metadata structure, making it suitable for writing to separate files.

### Valid Call Patterns
```scala
// Example of dividing a raster into 2x2 tiles
val metadata = new RasterMetadata(0, 0, 60, 40, 10, 10, 4326, new AffineTransform())
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val outputRaster = divideScene(raster, metadata, 2, 2)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD` and that the `targetMetadata` is correctly defined for the output. The `numTilesX` and `numTilesY` should be positive integers.

### Prompt Snippet
```text
Divide the raster into smaller tiles using the specified metadata and tile dimensions.
```

### Common Failure Modes
- Providing a `RasterRDD` that is empty or improperly formatted may lead to runtime errors.
- Specifying `numTilesX` or `numTilesY` as zero or negative values will likely result in an IllegalArgumentException.
- Mismatched metadata dimensions compared to the input raster may cause unexpected behavior or errors during processing.

### Fix Code Hint
```scala
// Ensure the input raster and metadata are correctly defined and that numTilesX and numTilesY are positive integers.
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
The `explode` function separates each tile in a `RasterRDD` into its own individual raster, facilitating operations on individual tiles.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster data containing multiple tiles. Each tile will be extracted into a separate raster in the output.

### Input
The caller must provide a `RasterRDD[T]` that contains raster data, which can be loaded from formats such as GeoTIFF or HDF. The input raster should be properly formatted and accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster RDD where each tile from the input raster is represented as a separate raster. The output maintains the same pixel type as the input.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val explodedRaster = explode(raster)
```

### LLM Instruction Prompt
- When calling `explode`, ensure that the input is a valid `RasterRDD` containing multiple tiles. The output will be a `RasterRDD` where each tile is separated.

### Prompt Snippet
```text
Please use the explode function to separate tiles in a RasterRDD into individual rasters.
```

### Common Failure Modes
- Providing an input that is not a `RasterRDD` will result in a type mismatch error.
- If the input raster is empty, the output will also be an empty `RasterRDD`.

### Fix Code Hint
```scala
// Ensure the input raster is a valid RasterRDD with multiple tiles before calling explode.
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
if (raster.count() > 0) {
  val explodedRaster = explode(raster)
} else {
  println("Input raster is empty.")
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
`filterPixels` retains only the pixels in a raster that meet a specified condition, effectively filtering out unwanted pixel values for geospatial analysis.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster dataset containing pixel values of type `T`. This dataset is expected to be a distributed collection of raster tiles that can be processed in parallel.
- `filter` (`T => Boolean`): A user-defined function that takes a pixel value of type `T` and returns a Boolean indicating whether the pixel should be retained (`true`) or cleared (`false`).

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, which can be loaded from formats such as GeoTIFF or HDF. The `filter` function must be defined to specify the criteria for retaining pixel values.

### Output
Returns `RasterRDD[T]` — a new raster dataset where only the pixels that pass the filter condition are retained, while all other pixels are set to empty. The output maintains the same pixel type as the input.

### Valid Call Patterns
```scala
val inputRaster: RDD[ITile[Short]] = sparkContext.parallelize(Seq(inputTile))
val outputRaster: RDD[ITile[Short]] = RasterOperationsLocal.filterPixels(inputRaster, (x: Short) => x < 50)
```

### LLM Instruction Prompt
- When calling `filterPixels`, ensure that the `inputRaster` is a valid `RasterRDD` and that the `filter` function is correctly defined to return a Boolean for each pixel value.

### Prompt Snippet
```text
Use the filterPixels function to retain only the pixels in the raster that are less than a specified threshold.
```

### Common Failure Modes
- The `inputRaster` is empty, resulting in an output that is also empty.
- The `filter` function does not handle all possible pixel values, which may lead to unexpected behavior or runtime errors.

### Fix Code Hint
```scala
Ensure that the filter function is defined to handle all expected pixel values and that the input raster is not empty before calling filterPixels.
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
The `flatten` function extracts all pixel values from a raster dataset into a distributed RDD format, facilitating further analysis and processing in geospatial applications.

### Parameters
- `raster` (`RasterRDD[T]`): The raster dataset from which pixel values will be extracted. It is expected to be a distributed collection of raster tiles containing pixel data of type `T`.

### Input
The caller must provide a `RasterRDD[T]`, which can be loaded from supported formats such as GeoTIFF or HDF. The raster must be properly formatted and accessible in the Spark environment.

### Output
Returns `RDD[(Int, Int, RasterMetadata, T)]` — This output represents a distributed collection where each element is a tuple containing the pixel's x-coordinate, y-coordinate, associated raster metadata, and the pixel value of type `T`.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val flattenedRaster: RDD[(Int, Int, RasterMetadata, Int)] = flatten(raster)
```

### LLM Instruction Prompt
- When calling `flatten`, ensure that the input raster is a valid `RasterRDD` and that the pixel type matches the expected type `T`.

### Prompt Snippet
```text
Extract pixel values from the raster dataset using the flatten function to prepare for further analysis.
```

### Common Failure Modes
- Attempting to call `flatten` on a non-`RasterRDD` type will result in a type mismatch error.
- If the raster data is not properly loaded or is inaccessible, the function may throw an exception during execution.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before calling flatten
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val flattenedRaster: RDD[(Int, Int, RasterMetadata, Int)] = flatten(raster)
```

## API Test: `geoTiff`

### Signature
```scala
def geoTiff[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:40_

_Source doc:_ Loads a GeoTIFF file as an RDD of tiles @param path the path of the file @param iLayer the index of the band to load (0 by default) @param opts additional options for loading the file @return a [[RasterRDD]] that represents all tiles in the file

### Goal
Load a GeoTIFF file as a distributed collection of raster tiles for large-scale geospatial analysis.

### Parameters
- `path` (`String`): The file path to the GeoTIFF file to be loaded. This should be a valid path accessible in the working directory.
- `iLayer` (`Int`), default `0`: The index of the band to load from the GeoTIFF file. The default value is `0`, which typically corresponds to the first band.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional options for loading the file, which can include settings for handling the raster data.

### Input
The caller must provide a valid path to a GeoTIFF file. The file must be accessible in the working directory, and the specified band index should correspond to an existing band in the GeoTIFF.

### Output
Returns `RDD[ITile[T]]` — a distributed collection of raster tiles representing the loaded GeoTIFF file. Each tile contains pixel data of the specified type `T`.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
val temperature: RDD[ITile[Float]] = sc.geoTiff[Float]("path/to/temperature.tif", 1)
```

### LLM Instruction Prompt
- Ensure the provided path is valid and points to an accessible GeoTIFF file. The pixel type `T` should match the expected data type of the raster.

### Prompt Snippet
```text
Load a GeoTIFF file using the geoTiff function, specifying the path and optional parameters.
```

### Common Failure Modes
- Invalid file path: The specified path does not point to a valid GeoTIFF file.
- Band index out of range: The specified `iLayer` index exceeds the number of available bands in the GeoTIFF.
- Unsupported pixel type: The specified pixel type `T` does not match the data type of the raster.

### Fix Code Hint
```scala
Check that the file path is correct and that the specified band index is within the range of available bands in the GeoTIFF.
```

## API Test: `getValue`

### Signature
```scala
def getValue(i: Int, j: Int, position: Int): T
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTileWindow.scala:41_

### Goal
Retrieve the value of a pixel at specified coordinates and band position from a raster dataset.

### Parameters
- `i` (`Int`): The row index of the pixel in the raster grid. Expected values are non-negative integers within the bounds of the raster's height.
- `j` (`Int`): The column index of the pixel in the raster grid. Expected values are non-negative integers within the bounds of the raster's width.
- `position` (`Int`): The band index from which to retrieve the pixel value. Expected values are non-negative integers corresponding to the number of bands in the raster.

### Input
The caller must provide valid indices `i` and `j` that correspond to the dimensions of the raster being processed, as well as a valid `position` that corresponds to the available bands in the raster.

### Output
Returns `T` — the pixel value at the specified `(i, j)` coordinates for the given band `position`. The type `T` will depend on the pixel type of the raster (e.g., `Int`, `Float`).

### Valid Call Patterns
```scala
val pixelValue = raster.getValue(10, 20, 0) // Retrieves the value from the first band at row 10, column 20
```

### LLM Instruction Prompt
- Ensure that the indices `i` and `j` are within the bounds of the raster dimensions and that `position` is a valid band index.

### Prompt Snippet
```text
Retrieve the pixel value at row 10, column 20 from the first band of the raster.
```

### Common Failure Modes
- IndexOutOfBoundsException: Occurs if `i` or `j` are outside the raster dimensions.
- IllegalArgumentException: Occurs if `position` exceeds the number of bands in the raster.

### Fix Code Hint
```scala
// Ensure that the indices are within valid ranges before calling getValue
if (i >= 0 && i < raster.height && j >= 0 && j < raster.width && position >= 0 && position < raster.bands) {
  val pixelValue = raster.getValue(i, j, position)
} else {
  throw new IllegalArgumentException("Invalid indices or band position.")
}
```

## API Test: `hdfFile`

### Signature
```scala
def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46_

### Goal
Load raster data from an HDF file and return it as an RDD of tiles with floating-point pixel values.

### Parameters
- `path` (`String`): The file path to the HDF file from which to load the raster data. This should be a valid path accessible in the working environment.
- `layer` (`String`): The name of the specific dataset layer within the HDF file to be loaded. This should correspond to a valid layer name present in the HDF file.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Options for loading the raster data, which can include configurations such as data type handling or performance settings.

### Input
The caller must provide:
- A valid HDF file path as a string.
- The name of the layer within the HDF file that contains the raster data.
- The environment must have access to the specified HDF file.

### Output
Returns `RDD[ITile[Float]]` — an RDD containing tiles of floating-point pixel values representing the raster data from the specified layer of the HDF file.

### Valid Call Patterns
```scala
val rasterData: RDD[ITile[Float]] = sc.hdfFile("path/to/file.hdf", "dataset_name")
```

### LLM Instruction Prompt
- Ensure that the `path` and `layer` parameters are valid and correspond to an existing HDF file and layer name, respectively. Use the default `opts` unless specific options are required.

### Prompt Snippet
```text
Load raster data from an HDF file using the hdfFile function, specifying the correct path and layer name.
```

### Common Failure Modes
- Providing an invalid file path that does not exist or is inaccessible.
- Specifying a layer name that does not exist within the HDF file.
- Incorrectly configuring `BeastOptions` that may lead to performance issues or errors during loading.

### Fix Code Hint
```scala
Check that the HDF file path is correct and that the specified layer name matches one of the layers in the file. Ensure that the file is accessible from the Spark environment.
```

## API Test: `initialize`

### Signature
```scala
def initialize(fileSystem: FileSystem, path: String, layer: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:74  (+2 more definition site/overload)_

### Goal
Initializes the GeoTIFF reader with the specified file system, path to the raster file, layer identifier, and options for processing.

### Parameters
- `fileSystem` (`FileSystem`): Represents the file system from which the raster data will be read. This is typically a Hadoop-compatible file system.
- `path` (`String`): The file path to the GeoTIFF raster file that needs to be processed. This should be a valid path accessible by the provided `fileSystem`.
- `layer` (`String`): The identifier for the specific layer within the raster file to be read. This is often "0" for the first layer in a multi-layered GeoTIFF.
- `opts` (`BeastOptions`): Configuration options for the Beast processing framework, which may include settings for performance, memory management, or specific processing behaviors.

### Input
The caller must provide a valid `FileSystem` instance, a string path to an existing GeoTIFF file, a layer identifier (typically "0"), and an instance of `BeastOptions` with any necessary configurations.

### Output
Returns `Unit` — this indicates that the initialization process has completed successfully without returning any value. If the initialization fails, it may throw an exception.

### Valid Call Patterns
```scala
val rasterPath = new Path("path/to/your/raster.tif")
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Array[Int]]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly set up and that the `path` points to a valid GeoTIFF file. The `layer` should be a valid string representing the layer to read, and `opts` should be properly configured.

### Prompt Snippet
```text
Initialize the GeoTIFF reader with the specified file system, path, layer, and options.
```

### Common Failure Modes
- The specified `path` does not exist or is not accessible, leading to a file not found error.
- The `layer` identifier is invalid or out of range for the given GeoTIFF file.
- The `fileSystem` is not properly configured, resulting in read errors.

### Fix Code Hint
```scala
Check that the file path is correct and that the file exists in the specified location. Ensure that the layer identifier is valid for the raster file being accessed.
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
The caller must provide a `RasterRDD[T]` containing the raster data, which can be loaded from formats such as GeoTIFF or HDF. The function `f` must be defined to handle the pixel type `T` and return a new pixel type `U`.

### Output
Returns `RasterRDD[U]` — a new raster represented as a distributed collection of raster tiles, where each tile contains transformed pixel values of type `U`.

### Valid Call Patterns
```scala
val raster: RasterRDD[Short] = sc.geoTiff("path/to/file.tif")
val outputRaster: RasterRDD[Int] = raster.mapPixels(pixel => Math.max(pixel, 50))
```

### LLM Instruction Prompt
- Ensure that the input raster is correctly typed and accessible. The function `f` must be compatible with the pixel type of the input raster.

### Prompt Snippet
```text
Transform the pixel values of the raster using a function that applies a threshold.
```

### Common Failure Modes
- The input raster is not properly loaded or is of an unexpected type, leading to type mismatch errors.
- The function `f` does not handle all possible pixel values, which may result in runtime exceptions.

### Fix Code Hint
```scala
Ensure that the input raster is loaded correctly and that the function `f` is defined to handle all expected pixel values.
```

## API Test: `merge`

### Signature
```scala
def merge(other: AbstractConvolutionTile[T]): AbstractConvolutionTile[T]
def merge(other: ReshapeTile[T]): ReshapeTile[T]
def merge(other: SlidingWindowTile[T, U]): SlidingWindowTile[T, U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:77  (+2 more definition site/overload)_

_Source doc:_ Merge another convolution tile into this tile @param other the other convolution tile to merge @return this tile after updating

### Goal
The `merge` function combines the pixel values of the current convolution tile with those from another convolution tile, allowing for the integration of raster data in geospatial analysis.

### Parameters
- `other` (`AbstractConvolutionTile[T]`): The convolution tile to be merged with the current tile. This can be another instance of `ConvolutionTileSingleBand`, `ConvolutionTileMultiBand`, or other subclasses of `AbstractConvolutionTile`.

### Input
The caller must provide two convolution tiles of compatible types (e.g., both should be of the same subclass of `AbstractConvolutionTile`). The input tiles should be properly initialized and contain pixel data that can be merged.

### Output
Returns `AbstractConvolutionTile[T]` — The updated convolution tile that contains the merged pixel values from both the current and the `other` tile.

### Valid Call Patterns
```scala
val convWindow1: ConvolutionTileSingleBand = // initialize first convolution tile
val convWindow2: ConvolutionTileSingleBand = // initialize second convolution tile
val mergedConvWindow: ConvolutionTileSingleBand = convWindow1.merge(convWindow2)
```

### LLM Instruction Prompt
- When calling `merge`, ensure that the `other` tile is of a compatible type and contains valid pixel data. The merging process will update the current tile with the pixel values from the `other` tile.

### Prompt Snippet
```text
Merge the current convolution tile with another convolution tile to integrate pixel values.
```

### Common Failure Modes
- Attempting to merge tiles of incompatible types (e.g., merging a `ConvolutionTileSingleBand` with a `ConvolutionTileMultiBand`).
- Merging tiles that do not contain any pixel data, resulting in an empty output.

### Fix Code Hint
```scala
// Ensure both tiles are of the same type before merging
if (convWindow1.getClass == convWindow2.getClass) {
    val mergedConvWindow = convWindow1.merge(convWindow2)
} else {
    throw new IllegalArgumentException("Tiles must be of the same type to merge.")
}
```

## API Test: `metadata`

### Signature
```scala
def metadata: RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:165  (+2 more definition site/overload)_

### Goal
Retrieve the metadata associated with a raster dataset, providing essential information about its dimensions, pixel scale, and coordinate transformations.

### Parameters
_None._

### Input
The caller must have a raster dataset loaded, typically from a GeoTIFF file, using a method such as `sc.geoTiff("path/to/file.tif")`. The raster must be properly initialized and accessible in the Spark context.

### Output
Returns `RasterMetadata` — an object that encapsulates metadata information about the raster, including its width, height, pixel scale, and methods for coordinate transformations.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
val metadata = raster.metadata
```

### LLM Instruction Prompt
- Ensure that the raster dataset is loaded and initialized before calling `metadata`. The raster must be of a supported format (e.g., GeoTIFF).

### Prompt Snippet
```text
Retrieve the metadata for the loaded raster dataset to understand its dimensions and pixel scale.
```

### Common Failure Modes
- Calling `metadata` on an uninitialized or improperly loaded raster dataset may result in a runtime error.
- Attempting to access `metadata` without first loading a raster will lead to a `NullPointerException`.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly before accessing metadata
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
val metadata = raster.metadata // This should work if raster is properly initialized
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
The `overlay` function combines multiple raster datasets into a single raster by stacking them on top of each other, allowing for complex geospatial analyses.

### Parameters
- `rasters` (`RasterRDD[T]*`): One or more raster datasets that will be overlaid. Each raster must be of the same dimensions and coordinate reference system (CRS) to ensure proper alignment.

### Input
The caller must provide:
- One or more `RasterRDD` instances containing raster data, which can be loaded from formats such as GeoTIFF or HDF.
- All input rasters should have compatible dimensions and CRS to avoid misalignment during the overlay operation.

### Output
Returns a new `RasterRDD` that represents the stacked raster data. The output format is a raster dataset that contains the pixel values from the input rasters, with the topmost raster's values taking precedence in case of overlapping pixels.

### Valid Call Patterns
```scala
val raster1: RasterRDD[Short] = sc.geoTiff("path/to/first.tif")
val raster2: RasterRDD[Short] = sc.geoTiff("path/to/second.tif")
val stackedRaster: RasterRDD[Array[Short]] = RasterOperationsLocal.overlay(raster1, raster2)
```

### LLM Instruction Prompt
- Ensure that all input rasters are of the same dimensions and CRS before calling `overlay`. Use typed loads for raster data to match the expected pixel type.

### Prompt Snippet
```text
Overlay two or more raster datasets using the overlay function to create a combined raster representation.
```

### Common Failure Modes
- Attempting to overlay rasters with different dimensions or CRS will result in an error due to misalignment.
- Providing no rasters or an empty list will lead to an invalid operation.

### Fix Code Hint
```scala
// Ensure all rasters have the same dimensions and CRS before calling overlay
val raster1: RasterRDD[Short] = sc.geoTiff("path/to/first.tif")
val raster2: RasterRDD[Short] = sc.geoTiff("path/to/second.tif")
val stackedRaster: RasterRDD[Array[Short]] = RasterOperationsLocal.overlay(raster1, raster2)
```

## API Test: `raptorJoin`

### Signature
```scala
def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:87_

_Source doc:_ Performs a Raptor join operation with a set of vector features. @param features the set of features to join with @param opts additional options to configure the operation @tparam T the type of the value in the result. Should be compatible with the pixel type of the raster @return all overlaps between the given features and the pixels.

### Goal
`raptorJoin` combines raster data with a set of vector features to identify and return all overlaps between the raster pixels and the vector geometries.

### Parameters
- `features` (`SpatialRDD`): A collection of vector geometries (e.g., points, lines, polygons) that will be joined with the raster data. This parameter represents the spatial features that define the areas of interest for the join operation.
- `opts` (`BeastOptions`), default `new BeastOptions`: Configuration options for the join operation, allowing users to customize aspects of the processing, such as spatial tolerance or output settings.

### Input
The caller must provide a `SpatialRDD` containing vector features. The raster data must be loaded into an appropriate format (e.g., `RDD[ITile]` or `RasterRDD`) prior to performing the join. The input vector features should be in a compatible spatial reference system with the raster data.

### Output
Returns `unspecified` — the result represents all overlapping areas between the raster pixels and the provided vector features, typically in the form of a new RDD containing tuples of the vector features and associated raster pixel values.

### Valid Call Patterns
```scala
val vector: RDD[IFeature] = sc.shapefile("path/to/vector.shp")
val joined: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin(vector)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing vector geometries. The raster data must be loaded and ready for the join operation. Use appropriate `BeastOptions` if needed.

### Prompt Snippet
```text
Join the raster data with the provided vector features using raptorJoin.
```

### Common Failure Modes
- The `features` parameter is not a valid `SpatialRDD`, leading to a type mismatch error.
- The raster data and vector features are in different coordinate reference systems, resulting in no overlaps being found.
- Insufficient memory or resources in the Spark cluster to perform the join operation.

### Fix Code Hint
```scala
// Ensure the vector features are loaded correctly and in the same CRS as the raster
val vector: RDD[IFeature] = sc.shapefile("path/to/vector.shp")
val joined: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin(vector)
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
- `raster` (`RasterRDD[T]`): The raster RDD containing the tiles of raster data to be tested against the features. It is expected to be a distributed collection of raster tiles with pixel values of type `T`.
- `features` (`RDD[IFeature]`): The set of vector features (e.g., polygons, points) to join with the raster data. This RDD should contain geometrical representations that can be used to determine overlaps with the raster pixels.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options for configuring the query processor, such as spatial indexing or filtering criteria. This allows users to customize the join operation based on their specific needs.
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator that counts the number of tile accesses during the query processing. This can be useful for performance monitoring and optimization.

### Input
The caller must provide:
- A `RasterRDD[T]` containing the raster data, which can be loaded from formats like GeoTIFF or HDF.
- An `RDD[IFeature]` containing vector features, which can be loaded from formats like Shapefile or GeoJSON.
- The input data must be accessible in the Spark environment, and the raster and features should be properly aligned in terms of coordinate reference systems (CRS) for meaningful results.

### Output
Returns `RDD[RaptorJoinFeature[T]]` — a distributed collection of `RaptorJoinFeature` objects, each representing the overlaps between raster pixels and the vector features. This output provides detailed information about which pixels intersect with the features, including pixel values and feature attributes.

### Valid Call Patterns
```scala
val raster: RasterRDD[Float] = sc.geoTiff("path/to/raster.tif")
val features: RDD[IFeature] = sc.shapefile("path/to/features.shp")
val joinedFeatures: RDD[RaptorJoinFeature[Float]] = raptorJoinFeature(raster, features)
```

### LLM Instruction Prompt
- Ensure that the raster and features are properly loaded and accessible in the Spark context before calling `raptorJoinFeature`. The pixel type `T` must match the type of the raster data.

### Prompt Snippet
```text
Join the raster data with vector features using raptorJoinFeature to find overlapping pixels.
```

### Common Failure Modes
- The raster and features may not intersect, resulting in an empty output RDD.
- Mismatched coordinate reference systems (CRS) between the raster and features can lead to incorrect results or runtime errors.
- If the raster or features are not properly loaded or accessible, a `NullPointerException` or similar error may occur.

### Fix Code Hint
```scala
Ensure that both the raster and features are loaded correctly and that their coordinate reference systems are aligned before calling raptorJoinFeature.
```

## API Test: `raptorJoinIDFull`

### Signature
```scala
def raptorJoinIDFull[T](raster: RDD[ITile[T]], vector: RDD[(Long, IFeature)], opts: BeastOptions, numTiles: LongAccumulator = null, numRanges: LongAccumulator = null) : RDD[RaptorJoinResult[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180_

_Source doc:_ A Raptor join implementation that returns all the matches between features and pixels along with the raster metadata that puts the pixel in context. @param raster the RDD that contains the raster tiles @param vector the RDD that contains the vector features and their unique IDs @param opts additional options for the query processor @tparam T the type of the pixel values @return RDD that contains all overlaps between pixels and geometries

### Goal
`raptorJoinIDFull` performs a spatial join between raster tiles and vector features, returning all overlapping matches along with relevant raster metadata.

### Parameters
- `raster` (`RDD[ITile[T]]`): An RDD containing raster tiles, where each tile represents a portion of the raster data with pixel values of type `T`.
- `vector` (`RDD[(Long, IFeature)]`): An RDD containing vector features, where each feature is paired with a unique identifier (Long) that allows for tracking and referencing.
- `opts` (`BeastOptions`): An instance of `BeastOptions` that provides additional configuration options for the join operation, such as spatial indexing or query parameters.
- `numTiles` (`LongAccumulator`), default `null`: An optional accumulator to track the number of raster tiles processed during the join operation.
- `numRanges` (`LongAccumulator`), default `null`: An optional accumulator to track the number of spatial ranges processed during the join operation.

### Input
The caller must provide:
- An RDD of raster tiles loaded from a supported format (e.g., GeoTIFF) using `sc.geoTiff[T]`.
- An RDD of vector features, typically loaded from a shapefile or similar format using `sc.shapefile`.
- A properly configured `BeastOptions` instance.

### Output
Returns `RDD[RaptorJoinResult[T]]` — an RDD containing `RaptorJoinResult` objects, each representing an overlap between raster pixels and vector geometries, including the pixel's metadata for context.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/raster.tif")
val vector: RDD[(Long, IFeature)] = sc.shapefile("path/to/vector.shp")
val results: RDD[RaptorJoinResult[Int]] = raptorJoinIDFull(raster, vector, new BeastOptions())
```

### LLM Instruction Prompt
- Ensure that the raster and vector RDDs are properly initialized and contain valid data before calling `raptorJoinIDFull`.
- Use the appropriate pixel type when loading the raster data to match the expected type `T`.

### Prompt Snippet
```text
Join raster data with vector features using raptorJoinIDFull to find overlaps and retrieve metadata.
```

### Common Failure Modes
- Mismatched pixel types between the raster and the expected type `T` can lead to runtime errors.
- Providing an empty RDD for either the raster or vector input will result in an empty output RDD.
- Incorrectly configured `BeastOptions` may lead to unexpected behavior or performance issues during the join operation.

### Fix Code Hint
```scala
// Ensure the raster and vector RDDs are correctly initialized and not empty before calling the function.
val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/raster.tif")
val vector: RDD[(Long, IFeature)] = sc.shapefile("path/to/vector.shp")
val results: RDD[RaptorJoinResult[Int]] = raptorJoinIDFull(raster, vector, new BeastOptions())
```

## API Test: `rasterizePixels`

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Create a raster from a set of pixel values @param pixels the list of pixel locations and values @param metadata the raster metadata that defines the geography of the pixels @return a raster that contains all the pixels

### Goal
The `rasterizePixels` function creates a raster representation from a distributed set of pixel values, enabling large-scale geospatial analysis.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): A distributed collection of pixel data, where each entry is a tuple containing the x-coordinate, y-coordinate, and the pixel value of type `T`. This represents the spatial location and value of each pixel in the raster.
- `metadata` (`RasterMetadata`): An object that contains metadata about the raster, including its dimensions, geographic bounds, and coordinate reference system. This information is essential for correctly positioning the raster in geographic space.
- `rasterFeature` (`RasterFeature`): An object that encapsulates additional features or attributes related to the raster, such as file names or identifiers. This can be used for tracking or managing raster datasets.

### Input
The caller must provide:
- A valid `RDD` of pixel data in the format of `(Int, Int, T)`, where `T` matches the expected pixel type.
- A `RasterMetadata` object that accurately describes the raster's properties.
- A `RasterFeature` object that provides context for the raster being created.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset containing all the pixels specified in the input `pixels` RDD, formatted according to the provided `RasterMetadata`.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 360, 180, 90, 90, 4326, new AffineTransform(1, 0, 0, -1, -180, 90))
val pixels = sparkContext.parallelize(Seq((0, 0, 100f), (180, 0, 200f), (100, 50, 300f)))
val rasterRDD: RasterRDD[Float] = RasterOperationsGlobal.rasterizePixels(pixels, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
```

### LLM Instruction Prompt
- Ensure that the `pixels` RDD contains valid pixel coordinates and values.
- The `metadata` must accurately reflect the raster's spatial properties.
- The `rasterFeature` should be properly instantiated to avoid null references.

### Prompt Snippet
```text
Create a raster from a set of pixel values using `rasterizePixels`. Ensure the pixel data is in the correct format and that the metadata accurately describes the raster's properties.
```

### Common Failure Modes
- Providing an empty `pixels` RDD will result in an empty `RasterRDD`.
- Mismatched pixel types between the `pixels` RDD and the expected type in `RasterMetadata` can lead to runtime errors.
- Incorrectly defined `RasterMetadata` (e.g., invalid bounds or dimensions) may cause the raster to be improperly formed.

### Fix Code Hint
```scala
Ensure that the `pixels` RDD is populated with valid data and that the `metadata` accurately describes the raster's dimensions and geographic bounds before calling `rasterizePixels`.
```

## API Test: `rasterizePoints`

### Signature
```scala
def rasterizePoints[T: ClassTag](points: RDD[(Double, Double, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:55  (+1 more definition site/overload)_

_Source doc:_ Creates a raster from a list of point locations and values. @param points point locations and raster values @param metadata the metadata that describes the raster location @tparam T the type of raster values @return a raster that contains the given point locations

### Goal
The `rasterizePoints` function converts a set of point locations with associated values into a raster format suitable for geospatial analysis.

### Parameters
- `points` (`RDD[(Double, Double, T)]`): A distributed collection of tuples where each tuple contains a pair of coordinates (longitude, latitude) and a value of type `T` representing the raster value at that location.
- `metadata` (`RasterMetadata`): Metadata that describes the properties of the raster, including its spatial reference, dimensions, and resolution.
- `rasterFeature` (`RasterFeature`): An object that defines the characteristics of the raster being created, such as its type and any additional features relevant to the rasterization process.

### Input
The caller must provide:
- An `RDD` of point data in the format of `(Double, Double, T)`, where `Double` represents the coordinates and `T` represents the raster value.
- A `RasterMetadata` object that specifies the raster's spatial properties.
- A `RasterFeature` object that outlines the features of the raster.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset that contains the rasterized representation of the input point locations and values, structured according to the provided metadata.

### Valid Call Patterns
```scala
// Example of rasterizing points with metadata
val metadata = RasterMetadata.create(0, 0, 6, 4, 4326, 60, 40, 60, 40)
val points = sparkContext.parallelize(Seq(
  (2.20, 1.7, 100),
  (2.7, 2.0, 50),
  (5.3, 2.2, 25)
))
val raster: RasterRDD[Int] = rasterizePoints(points, metadata, null)
```

### LLM Instruction Prompt
- When calling `rasterizePoints`, ensure that the `points` RDD is properly formatted with valid coordinate pairs and corresponding raster values. The `metadata` must accurately reflect the desired raster properties.

### Prompt Snippet
```text
Create a raster from the following point data using `rasterizePoints` with appropriate metadata and raster feature.
```

### Common Failure Modes
- Providing an empty `RDD` for `points` will result in an empty raster output.
- Mismatched or incorrect `RasterMetadata` may lead to unexpected raster dimensions or spatial reference issues.
- Using an unsupported type for the raster values in `points` could cause runtime errors.

### Fix Code Hint
```scala
// Ensure that the points RDD is not empty and that the metadata matches the expected raster dimensions.
val points = sparkContext.parallelize(Seq((2.20, 1.7, 100), (2.7, 2.0, 50)))
val metadata = RasterMetadata.create(0, 0, 6, 4, 4326, 60, 40, 60, 40)
val raster = rasterizePoints(points, metadata, null)
```

## API Test: `readTile`

### Signature
```scala
def readTile(tileID: Int): ITile[T]
def readTile(tileID: Int): ITile[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:167  (+2 more definition site/overload)_

### Goal
The `readTile` function retrieves a specific tile of raster data identified by the given `tileID` from a GeoTIFF file, facilitating efficient access to large-scale geospatial raster data.

### Parameters
- `tileID` (`Int`): The unique identifier for the tile to be read. This ID corresponds to the specific tile's position within the raster dataset.

### Input
The caller must provide a valid `tileID` that corresponds to a tile within an initialized GeoTIFF reader. The GeoTIFF file must be properly loaded and accessible in the Spark environment.

### Output
Returns `ITile[T]` — an instance of `ITile` containing the pixel data for the specified tile. The format of the data is dependent on the pixel type defined during the initialization of the GeoTIFF reader (e.g., `ITile[Int]` or `ITile[Float]`).

### Valid Call Patterns
```scala
val tile = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val tileFloat = reader.readTile(reader.metadata.getTileIDAtPoint(33.694, 14.761))
```

### LLM Instruction Prompt
- Ensure that the `tileID` provided corresponds to a valid tile within the loaded GeoTIFF dataset. The GeoTIFF reader must be initialized before calling `readTile`.

### Prompt Snippet
```text
Retrieve the tile data for the specified tileID from the initialized GeoTIFF reader.
```

### Common Failure Modes
- Providing an invalid `tileID` that does not exist in the raster dataset may result in an error or an empty tile being returned.
- Attempting to call `readTile` before initializing the GeoTIFF reader will lead to a runtime exception.

### Fix Code Hint
```scala
// Ensure the GeoTIFF reader is initialized and the tileID is valid before calling readTile
val tileID = reader.metadata.getTileIDAtPoint(23.224, 32.415)
if (tileID >= 0) {
  val tile = reader.readTile(tileID)
} else {
  throw new IllegalArgumentException("Invalid tileID provided.")
}
```

## API Test: `reproject`

### Signature
```scala
def reproject(targetSRID: Int)
def reproject(targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def reproject[T: ClassTag](raster: RasterRDD[T], targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:517  (+2 more definition site/overload)_

_Source doc:_ Reproject a raster to a target coordinate reference system. This method uses the same resolution (number of pixels) of the first tile in the source raster. You can use the other [[reshapeAverage()]] method that takes [[RasterMetadata]] to change all the information. @param raster the raster layer to reproject @param targetCRS the target coordinate reference system @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @tparam T the type of the pixels @return

### Goal
Reproject a raster dataset to a specified coordinate reference system for accurate geospatial analysis.

### Parameters
- `raster` (`RasterRDD[T]`): The raster layer that you want to reproject. It should be a distributed collection of raster tiles.
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system to which the raster will be reprojected. This should be a valid CRS object representing the desired spatial reference.
- `unifiedRaster` (`Boolean`), default `false`: If set to true, all output tiles will be combined into a single `RasterMetadata`, ensuring uniformity across the output raster.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to determine the pixel values in the target raster when multiple source pixels overlap. Options include nearest neighbor, bilinear, etc.

### Input
The caller must provide a `RasterRDD` containing the raster data to be reprojected, a valid `CoordinateReferenceSystem` object for the target CRS, and optionally specify whether to unify the raster tiles and the interpolation method.

### Output
Returns `RasterRDD[T]` — a distributed collection of raster tiles reprojected to the specified coordinate reference system, maintaining the resolution of the first tile in the source raster.

### Valid Call Patterns
```scala
val raster: RasterRDD[Float] = sc.geoTiff("path/to/file.tif")
val targetCRS: CoordinateReferenceSystem = ??? // Define your target CRS here
val reprojectedRaster = raster.reproject(targetCRS)
```

### LLM Instruction Prompt
- Ensure that the `raster` is a valid `RasterRDD` and that the `targetCRS` is correctly defined. Use appropriate interpolation methods as needed.

### Prompt Snippet
```text
Reproject the raster to the specified coordinate reference system using the default interpolation method.
```

### Common Failure Modes
- Providing an invalid `targetCRS` that does not conform to recognized coordinate reference systems.
- Attempting to reproject a `RasterRDD` that is empty or improperly formatted.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly and the target CRS is valid before calling reproject
val raster: RasterRDD[Float] = sc.geoTiff("path/to/file.tif")
val targetCRS: CoordinateReferenceSystem = CRS.fromString("EPSG:4326") // Example of a valid CRS
val reprojectedRaster = raster.reproject(targetCRS)
```

## API Test: `rescale`

### Signature
```scala
def rescale(rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def rescale[T: ClassTag](raster: RasterRDD[T], rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:542  (+1 more definition site/overload)_

_Source doc:_ Changes the resolution of the raster to the desired resolution without changing tile size or CRS. @param raster the raster to rescale @param rasterWidth the new raster width in terms of pixels @param rasterHeight the new height of the raster layer in terms of pixels @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @return a new raster RDD with the desired width and height

### Goal
The `rescale` function adjusts the resolution of a raster dataset to specified pixel dimensions while maintaining the original tile size and coordinate reference system (CRS).

### Parameters
- `raster` (`RasterRDD[T]`): The input raster dataset that needs to be rescaled. It is expected to be a distributed collection of raster tiles.
- `rasterWidth` (`Int`): The desired width of the output raster in pixels.
- `rasterHeight` (`Int`): The desired height of the output raster in pixels.
- `unifiedRaster` (`Boolean`), default `false`: If set to true, all output tiles will be combined into a single `RasterMetadata`, ensuring uniformity across the output.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Specifies the method used to determine the pixel values in the output raster when multiple source pixels overlap. Options include nearest neighbor and other interpolation techniques.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, along with integer values for `rasterWidth` and `rasterHeight` that define the new dimensions. The input raster must be properly formatted and accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster dataset with the specified width and height, preserving the original CRS and tile size. The output is a distributed collection of raster tiles that can be further processed or saved.

### Valid Call Patterns
```scala
val inputRaster: RasterRDD[Short] = sc.geoTiff("path/to/input.tif")
val outputRaster = rescale(inputRaster, 10, 10, unifiedRaster = true)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD[T]` and that the specified width and height are positive integers. The output should be a `RasterRDD[T]` with the desired dimensions.

### Prompt Snippet
```text
Please rescale the provided raster to a width of 10 pixels and a height of 10 pixels, ensuring that all output tiles belong to a single RasterMetadata.
```

### Common Failure Modes
- Providing a `rasterWidth` or `rasterHeight` that is less than or equal to zero will result in an error.
- Attempting to rescale a raster that is not properly formatted as `RasterRDD[T]` will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly and dimensions are positive integers
val inputRaster: RasterRDD[Short] = sc.geoTiff("path/to/input.tif")
val outputRaster = rescale(inputRaster, 10, 10) // Ensure 10 and 10 are valid dimensions
```

## API Test: `reshapeAverage`

### Signature
```scala
def reshapeAverage[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, _numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the average method to determine the final value of each pixel. If one pixel in the answer overlaps multiple pixels in the source, their average is computed. This method should only be used when pixels represent continuous values, e.g., red, infrared, temperature, or vegetation. If the pixels represent categorical values, e.g., land type, then the nearest neighbor method [[reshapeNN]] should be used instead. @param raster the input raster that should be reshaped @param targetMetadataConv a function that returns the desired metadata for source metadata @param _numPartitions the number of partitions of the produces RDD. If not set, it will be the same as the input @return the new raster with the target metadata

### Goal
`reshapeAverage` reshapes a raster by converting its metadata and averaging pixel values when multiple source pixels overlap.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to contain continuous pixel values, such as temperature or vegetation indices.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, _numPartitions: Int`), default `0`: A function that takes the current raster metadata and returns the desired target metadata. The `_numPartitions` parameter specifies the number of partitions for the resulting RDD; if not set, it defaults to the number of partitions of the input raster.

### Input
The caller must provide a `RasterRDD[T]` containing continuous pixel values and a function to convert the raster's metadata. The input raster should be properly formatted and accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster with the target metadata applied, where pixel values are averaged from the source raster based on the specified reshaping criteria.

### Valid Call Patterns
```scala
val inputRaster: RasterRDD[Float] = sc.geoTiff[Float]("path/to/input.tif")
val targetMetadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326, new AffineTransform())
val outputRaster = reshapeAverage(inputRaster, _ => targetMetadata)
```

### LLM Instruction Prompt
- Ensure that the input raster contains continuous pixel values and that the target metadata conversion function is correctly defined. The number of partitions can be specified or left as default.

### Prompt Snippet
```text
Use the `reshapeAverage` function to reshape a raster by averaging pixel values. Ensure the input raster contains continuous values and provide a function for target metadata conversion.
```

### Common Failure Modes
- The input raster contains categorical pixel values instead of continuous values, which may lead to incorrect results.
- The target metadata conversion function does not return valid metadata, causing runtime errors.
- The number of partitions specified is incompatible with the input raster's structure.

### Fix Code Hint
```scala
// Ensure the input raster is of a continuous type and the target metadata is correctly defined.
val outputRaster = reshapeAverage(inputRaster, _ => targetMetadata)
```

## API Test: `reshapeNN`

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
`reshapeNN` reshapes the input raster to match specified target metadata using the nearest neighbor method for pixel value assignment.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to be a distributed collection of raster tiles with a specific pixel type `T`.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, numPartitions: Int`), default `0`: A function that takes the source raster's metadata and converts it to the desired target metadata. The `numPartitions` parameter specifies the number of partitions for the output RDD; if not set, the input raster's number of partitions will be used.

### Input
The caller must provide a `RasterRDD[T]` representing the input raster, along with a function that defines how to convert the raster's metadata. The input raster should be properly formatted and accessible in the Spark environment.

### Output
Returns `RasterRDD[T]` — a new raster with the target metadata applied. The output retains the pixel type `T` and is structured as a distributed collection of raster tiles.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val newMetadata: RasterMetadata = // define target metadata conversion
val reshapedRaster = reshapeNN(raster, newMetadata)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD[T]` and that the metadata conversion function is correctly defined. The output should be a `RasterRDD[T]` with the specified target metadata.

### Prompt Snippet
```text
Call `reshapeNN` with a valid RasterRDD and a metadata conversion function to reshape the raster according to the target specifications.
```

### Common Failure Modes
- The input raster is not a valid `RasterRDD[T]`, leading to type mismatch errors.
- The metadata conversion function does not return a valid `RasterMetadata`, causing runtime exceptions.
- Insufficient resources or incorrect partitioning leading to performance issues.

### Fix Code Hint
```scala
// Ensure the raster is loaded correctly and the metadata conversion function is defined properly.
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val newMetadata: RasterMetadata = // define target metadata conversion
val reshapedRaster = reshapeNN(raster, newMetadata)
```

## API Test: `retile`

### Signature
```scala
def retile(tileWidth: Int, tileHeight: Int)
def retile[T: ClassTag](raster: RasterRDD[T], tileWidth: Int, tileHeight: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566  (+1 more definition site/overload)_

_Source doc:_ Regrids the given raster to the target tile width and height @param raster the raster to regrid @param tileWidth the new tile width in pixels @param tileHeight the new tile height in pixels @tparam T the type of the pixel values in the raster @return a new raster with the given tile width and height

### Goal
The `retile` function regrids a given raster into specified tile dimensions, facilitating efficient processing and analysis of large geospatial datasets.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster data that needs to be regridded. It is expected to be a distributed collection of raster tiles with pixel values of type `T`.
- `tileWidth` (`Int`): The desired width of the output tiles in pixels. This value determines how wide each tile will be after the regridding operation.
- `tileHeight` (`Int`): The desired height of the output tiles in pixels. This value determines how tall each tile will be after the regridding operation.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data to be regridded, along with integer values for `tileWidth` and `tileHeight` that specify the new dimensions of the tiles.

### Output
Returns `RasterRDD[T]` — a new raster represented as a distributed collection of tiles, each with the specified width and height. The pixel values remain of type `T`, consistent with the input raster.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("path/to/file.tif")
val retiledRaster: RasterRDD[Int] = retile(raster, 20, 20)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD` and that the specified tile dimensions are positive integers.

### Prompt Snippet
```text
Regrid the raster to tiles of size 20x20 pixels using the retile function.
```

### Common Failure Modes
- Providing a `RasterRDD` that is empty or not properly initialized may result in runtime errors.
- Specifying non-positive integers for `tileWidth` or `tileHeight` will likely lead to illegal argument exceptions.

### Fix Code Hint
```scala
// Ensure that the raster is properly loaded and that tile dimensions are positive integers.
val raster: RasterRDD[Int] = sc.geoTiff[Int]("path/to/file.tif")
val retiledRaster: RasterRDD[Int] = retile(raster, 20, 20) // Ensure 20 and 20 are positive integers
```

## API Test: `saveAsGeoTiff`

### Signature
```scala
def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit
def saveAsGeoTiff[T](rasterRDD: RDD[ITile[T]], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:476  (+1 more definition site/overload)_

### Goal
The `saveAsGeoTiff` function writes a distributed raster dataset (RDD of tiles) to a GeoTIFF file format, enabling large-scale geospatial analysis.

### Parameters
- `rasterRDD` (`RDD[ITile[T]]`): The input raster data represented as a distributed collection of tiles, where each tile contains pixel values of type `T`. This is expected to be the result of previous raster operations.
- `outPath` (`String`): The file path where the output GeoTIFF will be saved. This should be a valid path in the file system where the application has write permissions.
- `opts` (`BeastOptions`): Options for saving the GeoTIFF, which may include parameters like bits per sample or whether to create a BigTIFF. This allows customization of the output file's properties.

### Input
The caller must provide an `RDD[ITile[T]]` containing the raster data, a valid output file path as a `String`, and an instance of `BeastOptions` to specify any additional saving options. The raster data should be properly formatted and accessible in the Spark environment.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the raster data to the specified GeoTIFF file.

### Valid Call Patterns
```scala
val rasterFile = locateResource("/raptor/glc2000_small.tif")
val rasterRDD = new RasterFileRDD(sparkContext, rasterFile.getPath, IRasterReader.RasterLayerID -> 0)
GeoTiffWriter.saveAsGeoTiff(rasterRDD, "output.tif", new BeastOptions)
```

### LLM Instruction Prompt
- When calling `saveAsGeoTiff`, ensure that the `rasterRDD` is a valid RDD of tiles, the `outPath` is a writable file path, and the `opts` are correctly configured for the desired output format.

### Prompt Snippet
```text
Please save the raster data to a GeoTIFF file using the `saveAsGeoTiff` function. Ensure the raster data is in the correct format and the output path is valid.
```

### Common Failure Modes
- Providing an invalid or inaccessible `outPath` will result in an error when attempting to write the file.
- If `rasterRDD` is empty or improperly formatted, the function may not execute as expected, leading to no output being generated.

### Fix Code Hint
```scala
// Ensure the output path is valid and accessible
val outputPath = "output.tif"
if (new File(outputPath).canWrite) {
    GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputPath, new BeastOptions)
} else {
    throw new IOException("Output path is not writable.")
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
`selectFiles` retrieves a list of raster files from a specified directory that may intersect with a defined geographical range, optimizing the selection process using an index file if available.

### Parameters
- `fileSystem` (`FileSystem`): Represents the file system where the raster files are stored. This is typically the Hadoop file system used in Spark environments.
- `dir` (`String`): The path to the directory containing the raster files. This directory should be accessible and contain the relevant raster files for processing.
- `range` (`Geometry`): A geometric shape defining the spatial query range. This parameter is used to filter the files based on their spatial overlap with the specified geometry.

### Input
The caller must provide:
- A valid `FileSystem` instance that points to the location of the raster files.
- A string representing the directory path where the raster files are located.
- A `Geometry` object that defines the spatial area of interest, which will be used to determine which files may overlap.

### Output
Returns `Array[String]` — an array of file paths (as strings) that represent the raster files which potentially overlap with the specified query range. The paths are relative to the provided directory.

### Valid Call Patterns
```scala
val geometryFactory = new GeometryFactory(new PrecisionModel(PrecisionModel.FLOATING_SINGLE), 4326)
val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), "path/to/raster/files", geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly initialized and points to the appropriate Hadoop configuration.
- Verify that the `dir` exists and contains raster files, and optionally an index file named "_index.csv".
- The `range` should be a valid `Geometry` object that accurately represents the area of interest.

### Prompt Snippet
```text
Select raster files from the specified directory that may overlap with the given geometry range.
```

### Common Failure Modes
- The specified directory does not exist or is inaccessible, leading to a `FileNotFoundException`.
- The `range` parameter is not a valid `Geometry`, which may cause runtime errors during spatial calculations.
- If the index file "_index.csv" is corrupted or improperly formatted, it may lead to incorrect file selections.

### Fix Code Hint
```scala
// Ensure the directory exists and contains valid raster files before calling selectFiles
val dir = "path/to/raster/files"
if (new File(dir).exists()) {
    val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dir, geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
} else {
    throw new IllegalArgumentException(s"Directory $dir does not exist.")
}
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
The `setPixelValue` function updates the value of a specific pixel in a raster tile, enabling precise modifications for geospatial analysis.

### Parameters
- `i` (`Int`): The column index of the pixel to be updated, where valid values range from `0` to the width of the raster tile minus one.
- `j` (`Int`): The row index of the pixel to be updated, where valid values range from `0` to the height of the raster tile minus one.
- `value` (`T`): The new value to assign to the specified pixel, which must match the pixel type of the raster tile (e.g., `Float` for single-band tiles or `Array[Float]` for multi-band tiles).

### Input
The caller must provide a raster tile that has been initialized and loaded with appropriate metadata. The pixel indices (`i` and `j`) must be within the bounds of the tile dimensions.

### Output
Returns `Unit` — this indicates that the operation has been completed successfully without returning any value.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326, new AffineTransform())
val tile = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile.setPixelValue(0, 0, 0.5f)
tile.setPixelValue(1, 1, 1.0f)
```

### LLM Instruction Prompt
- Ensure that the pixel indices provided are within the valid range of the raster tile dimensions. The value must match the expected pixel type.

### Prompt Snippet
```text
Set the pixel value at column {i} and row {j} to {value} in the raster tile.
```

### Common Failure Modes
- Attempting to set a pixel value with indices (`i`, `j`) that are out of bounds will result in an `IndexOutOfBoundsException`.
- Providing a value of an incorrect type that does not match the expected pixel type will lead to a type mismatch error.

### Fix Code Hint
```scala
// Ensure the indices are within bounds and the value type matches the tile's pixel type.
if (i < 0 || i >= tile.width || j < 0 || j >= tile.height) {
  throw new IndexOutOfBoundsException("Pixel indices are out of bounds.")
}
```

## API Test: `slidingWindow`

### Signature
```scala
def slidingWindow[T: ClassTag, U: ClassTag](raster: RasterRDD[T], w: Int, f: (Array[T], Array[Boolean]) => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:711_

_Source doc:_ Performs a sliding window calculation for a window of size (2w + 1) &times; (2w + 1) given an integer value w. The user-defined window calculation function takes all values in the window ordered in row-major order. Additionally, a Boolean array of the same size is passed to indicate which values are defined and which are not. The Boolean array is useful for two scenarios. 1. When the window is near the edge of the raster, there must be some undefined values outside the raster. 2. Some pixel values in raster might be undefined, e.g., due to cloud coverage. *Note*: This function will only work correctly if all input tiles have the same raster metadata. @param raster the input raster to process @param w the radius of the square window. The window size will be (2w + 1) &times; (2w + 1) @param f the function to perform the calculation. @tparam T the type of values in the input raster @tparam U the type of output values (the result of the user-defined function). @return a new raster with the same dimensions as the input after applying the window function.

### Goal
The `slidingWindow` function computes a user-defined operation over a square window of pixels in a raster, allowing for edge handling and undefined pixel values.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster data to process, which must have consistent metadata across all tiles. It represents a distributed collection of raster tiles containing pixel values of type `T`.
- `w` (`Int`): The radius of the square window. The total window size will be (2w + 1) &times; (2w + 1), determining how many neighboring pixels are included in the calculation.
- `f` (`(Array[T], Array[Boolean]) => U`): A user-defined function that takes an array of pixel values from the window and a corresponding Boolean array indicating which values are defined. It returns a value of type `U`, representing the result of the calculation for that window.

### Input
The caller must provide a `RasterRDD` containing pixel data, an integer for the window radius `w`, and a function that defines the operation to be performed on the pixel values. The raster must have consistent metadata, and the pixel values may include undefined values.

### Output
Returns `RasterRDD[U]` — a new raster with the same dimensions as the input raster, where each pixel value is the result of applying the user-defined function over the corresponding window.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff("path/to/file.tif")
val smoothedRaster: RasterRDD[Double] = slidingWindow(raster, 1, (values: Array[Int], defined) => {
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
- Ensure that the input raster has consistent metadata and that the user-defined function correctly handles undefined pixel values.

### Prompt Snippet
```text
Compute a smoothed raster using a sliding window of size 3x3, averaging defined pixel values.
```

### Common Failure Modes
- The function may fail if the input raster tiles do not have the same metadata, leading to inconsistent results.
- If the user-defined function does not handle undefined values correctly, it may throw an error or produce incorrect output.

### Fix Code Hint
```scala
Ensure that all input tiles have the same metadata and that the function `f` properly checks for defined values before performing calculations.
```

## API Test: `this`

### Signature
```scala
def this(filename: String)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:68_

### Goal
Initialize a new instance of the class by loading a raster dataset from the specified GeoTIFF file.

### Parameters
- `filename` (`String`): The path to the GeoTIFF file that contains the raster data to be loaded.

### Input
The caller must provide a valid path to a GeoTIFF file that is accessible in the working directory. The file must be formatted correctly as a GeoTIFF.

### Output
Returns `unspecified` — this constructor initializes an instance of the class, allowing subsequent operations on the loaded raster data.

### Valid Call Patterns
```scala
val rasterInstance = new ClassName("path/to/file.tif")
```

### LLM Instruction Prompt
- Ensure that the provided filename points to a valid GeoTIFF file and is accessible in the working directory.

### Prompt Snippet
```text
Create a new instance of the raster processing class using the GeoTIFF file located at "path/to/file.tif".
```

### Common Failure Modes
- The specified filename does not point to a valid GeoTIFF file.
- The file is not accessible due to incorrect path or permissions.

### Fix Code Hint
```scala
Check that the file path is correct and that the file exists in the specified location.
```

## API Test: `write`

### Signature
```scala
def write(kryo: Kryo, output: Output, tile: MemoryTile[Any]): Unit
def write(kryo: Kryo, output: Output, tile: MemoryTileWindow[T]): Unit
def write(tile: ITile[T]): Unit
def write(kryo: Kryo, output: Output, tile: AbstractConvolutionTile[Any]): Unit
def write(kryo: Kryo, output: Output, tile: MaskTile[T]): Unit
def write(kryo: Kryo, output: Output, tile: AbstractGeoTiffTile[T]): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTileSerializer.scala:26  (+5 more definition site/overload)_

### Goal
The `write` function saves a raster tile to a specified output format, typically a GeoTIFF, enabling the persistence of processed geospatial data.

### Parameters
- `kryo` (`Kryo`): An instance of the Kryo serialization framework used for efficient serialization of the raster tile data.
- `output` (`Output`): The output destination where the raster tile will be written, which can be a file path or a stream.
- `tile` (`MemoryTile[Any]`): The raster tile containing pixel data to be written. This tile must be properly initialized and contain valid pixel values.

### Input
The caller must provide a valid `Kryo` instance, an `Output` destination (such as a file path for a GeoTIFF), and a `MemoryTile` containing the raster data. The tile should be initialized with appropriate metadata and pixel values.

### Output
Returns `Unit` — this indicates that the function completes successfully without returning any value. The output is the written raster tile in the specified format, typically a GeoTIFF file.

### Valid Call Patterns
```scala
val kryo = new Kryo()
val output = new Output(new FileOutputStream("output.tif"))
val tile: MemoryTile[Short] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
write(kryo, output, tile)
```

### LLM Instruction Prompt
- Ensure that the `kryo`, `output`, and `tile` parameters are correctly instantiated and initialized before calling `write`. The output path must be valid and accessible.

### Prompt Snippet
```text
Please write a raster tile to a specified output using the `write` function. Ensure that the Kryo instance and output destination are properly set up.
```

### Common Failure Modes
- Attempting to write a tile that has not been properly initialized or contains invalid pixel values.
- Providing an invalid or inaccessible output path, which may result in an IOException.
- Using a `Kryo` instance that is not configured correctly for the type of tile being written.

### Fix Code Hint
```scala
// Ensure the tile is initialized and contains valid pixel data before calling write
val tile: MemoryTile[Short] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
// Check that the output path is valid and writable
val output = new Output(new FileOutputStream("output.tif"))
write(kryo, output, tile)
```

## API Test: `x1`

### Signature
```scala
def x1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:14_

### Goal
Returns the x-coordinate of the first pixel in a raster tile.

### Parameters
_None._

### Input
No specific input is required as this function does not take parameters.

### Output
Returns `Int` — the x-coordinate of the first pixel in the raster tile, typically representing the leftmost edge of the tile.

### Valid Call Patterns
```scala
val xCoordinate: Int = x1
```

### LLM Instruction Prompt
- Call `x1` to retrieve the x-coordinate of the first pixel in the raster tile.

### Prompt Snippet
```text
Retrieve the x-coordinate of the first pixel using the x1 function.
```

### Common Failure Modes
- The function may not behave as expected if called outside the context of a valid raster tile.

### Fix Code Hint
```scala
Ensure that `x1` is called on a valid raster tile instance to avoid unexpected results.
```

## API Test: `x2`

### Signature
```scala
def x2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16_

### Goal
Returns the x-coordinate of the tile in the raster processing context.

### Parameters
_None._

### Input
No specific input is required as this function does not take parameters.

### Output
Returns `Int` — the x-coordinate value of the tile, which represents its horizontal position in the raster grid.

### Valid Call Patterns
```scala
val xCoordinate: Int = x2
```

### LLM Instruction Prompt
- Call `x2` to retrieve the x-coordinate of the current tile in the raster processing context.

### Prompt Snippet
```text
Retrieve the x-coordinate of the tile using the x2 function.
```

### Common Failure Modes
- The function may not return a meaningful value if it is called outside the context of a valid tile.

### Fix Code Hint
```scala
Ensure that x2 is called within a valid tile context to retrieve the correct x-coordinate.
```

## API Test: `y1`

### Signature
```scala
def y1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:15_

### Goal
Retrieve the starting y-coordinate of a tile in a raster dataset.

### Parameters
_None._

### Input
No specific input data or file formats are required to call this function.

### Output
Returns `Int` — the starting y-coordinate of the tile, which indicates the vertical position of the tile in the raster grid.

### Valid Call Patterns
```scala
val startingY: Int = tile.y1
```

### LLM Instruction Prompt
- Ensure that the function is called on a valid tile object that has been properly initialized.

### Prompt Snippet
```text
Retrieve the starting y-coordinate of the tile using the `y1` method.
```

### Common Failure Modes
- Calling `y1` on an uninitialized or null tile object may result in a runtime error.

### Fix Code Hint
```scala
if (tile != null) {
  val startingY: Int = tile.y1
} else {
  throw new IllegalArgumentException("Tile must be initialized before calling y1.")
}
```

## API Test: `y2`

### Signature
```scala
def y2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17_

### Goal
Retrieve the maximum y-coordinate index of the tile in the context of raster processing.

### Parameters
_None._

### Input
No specific input is required as this function does not take parameters.

### Output
Returns `Int` — the maximum y-coordinate index of the tile, which is used to determine the vertical extent of the raster data.

### Valid Call Patterns
```scala
val maxYIndex: Int = tile.y2
```

### LLM Instruction Prompt
- Ensure that the function is called on a valid tile object that has been properly initialized.

### Prompt Snippet
```text
Retrieve the maximum y-coordinate index of the tile using the `y2` method.
```

### Common Failure Modes
- Calling `y2` on an uninitialized or null tile object may result in a runtime error.

### Fix Code Hint
```scala
if (tile != null) {
  val maxYIndex: Int = tile.y2
} else {
  // Handle the null case appropriately
}
```

## API Test: `zonalStats2`

### Signature
```scala
def zonalStats2[T](zones: RDD[IFeature], raster: RDD[ITile[T]], collectorClass: Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator = null)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:128_

_Source doc:_ Computes zonal statistics between a set of zones (polygons) and a raster file given by its path and a layer in that file. The result is an RDD of pairs of a feature and a collector value @param zones a set of polygons that represent the regions or zones @param raster the RDD of tiles @param collectorClass the class that collects the pixel values to compute the statistics @param opts additional user-defined options @param numTiles an optional accumulator to collect the total number of processed tiles @return a set of (Feature, Statistics)

### Goal
`zonalStats2` computes statistical summaries of raster data over specified polygonal zones, enabling geospatial analysis of raster datasets.

### Parameters
- `zones` (`RDD[IFeature]`): An RDD containing polygon features that define the zones for which statistics will be computed. Each feature represents a geographic area, such as administrative boundaries or land cover regions.
- `raster` (`RDD[ITile[T]]`): An RDD of raster tiles, where each tile contains pixel values representing some geospatial data (e.g., temperature, vegetation index). The pixel type `T` should match the expected data type for the analysis.
- `collectorClass` (`Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator`), default `null`: The class type of the collector that will aggregate pixel values to compute the desired statistics (e.g., mean, sum). `opts` allows for additional user-defined options, and `numTiles` is an optional accumulator to track the total number of processed tiles.

### Input
The caller must provide:
- An RDD of polygon features (`zones`) that represent the areas of interest.
- An RDD of raster tiles (`raster`) loaded from a compatible format (e.g., GeoTIFF).
- A valid collector class that extends `Collector` to specify how pixel values should be aggregated.
- An instance of `BeastOptions` for any additional configuration.

### Output
Returns an RDD of pairs, where each pair consists of a feature from `zones` and the corresponding statistics collected from the raster data. The statistics are represented by instances of the specified collector class.

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
- Ensure that the `zones` and `raster` RDDs are properly initialized and contain valid data before calling `zonalStats2`. The collector class must be a valid subclass of `Collector`.

### Prompt Snippet
```text
Compute zonal statistics for the provided raster data over the specified zones using the zonalStats2 function.
```

### Common Failure Modes
- Mismatched pixel types between the raster data and the expected type in the collector class.
- Empty or invalid RDDs for either `zones` or `raster`, leading to runtime errors.
- Incorrect or unsupported collector class provided, which does not implement the required aggregation methods.

### Fix Code Hint
```scala
Ensure that the RDDs for zones and raster are correctly populated and that the collector class is a valid subclass of Collector. Check for any null or empty values in the input RDDs before invoking zonalStats2.
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
Calculates zonal statistics for specified geometries or features using a raster dataset, providing insights into the pixel values within defined zones.

### Parameters
- `geometries` (`Array[Geometry]`): An array of geometries that define the zones for which statistics will be computed. Each geometry should represent a spatial area that may overlap with the raster data.
- `raster` (`IRasterReader[T]`): An instance of `IRasterReader` that points to the raster data being analyzed. This raster should be loaded and accessible, containing the pixel values to be aggregated.
- `collectorClass` (`Class[_ <: Collector]`): The class type of the collector that will compute the statistics. This class should extend `Collector` and implement the necessary methods to gather statistical data from the raster pixels within the specified geometries.

### Input
The caller must provide:
- An array of geometries or features that define the zones (e.g., administrative boundaries).
- A raster reader initialized with a raster dataset (e.g., a GeoTIFF file).
- A valid collector class that extends `Collector` to compute the desired statistics.

### Output
Returns `Array[Collector]` — an array of collector instances, each corresponding to an input geometry. Each collector contains the computed statistics for the overlapping pixels, while collectors for geometries with no overlap will be `null`.

### Valid Call Patterns
```scala
val vectorFile = new Path("path/to/vector.geojson")  // use .shp with ShapefileFeatureReader for shapefiles
val rasterFile = new Path("path/to/raster.tif")

val vectorReader = new GeoJSONFeatureReader
vectorReader.initialize(vectorFile, new BeastOptions())
import scala.collection.JavaConverters._
val features: Array[IFeature] = vectorReader.iterator().asScala.toArray

val rasterReader: IRasterReader[Int] = new GeoTiffReader[Int]
rasterReader.initialize(rasterFile.getFileSystem(sparkContext.hadoopConfiguration), rasterFile.toString, "0", new BeastOptions())

val stats: Array[Collector] = zonalStatsLocal(features, rasterReader, classOf[Statistics])
```

### LLM Instruction Prompt
- Ensure that the geometries provided overlap with the raster data; otherwise, the corresponding collector will be `null`.
- Use a valid collector class that implements the necessary statistical computations.
- Choose the feature reader that matches the vector file format. `GeoJSONFeatureReader` is valid for GeoJSON inputs; `ShapefileFeatureReader` is valid for Shapefile inputs.

### Prompt Snippet
```text
Calculate zonal statistics for the provided geometries using the specified raster data and collector class.
```

### Common Failure Modes
- Providing geometries that do not overlap with the raster data, resulting in `null` collectors.
- Using an uninitialized or incorrect raster reader, leading to runtime errors.
- Specifying a collector class that does not extend `Collector`, causing a compilation error.

### Fix Code Hint
```scala
// Ensure geometries overlap with raster data and that the raster reader is properly initialized.
val validStats: Array[Collector] = zonalStatsLocal(validGeometries, validRasterReader, classOf[ValidCollector])
```
