# MVTDataVisualizer

_`plotAllTiles` generates and visualizes raster tiles for a specified range of zoom levels based on the provided spatial features and configuration options._

**Receiver:** static object — call `MVTDataVisualizer.<method>(...)`

**Members** (most robust first): ⚠️ `plotAllTiles` **(primary)**, ⚠️ `plotSingleTileParallel`, ⚠️ `saveTiles`, ⚠️ `saveTilesCompact`

---

## API Test: `plotAllTiles`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def plotAllTiles(features: SpatialDataTypes.JavaSpatialRDD, minLevel: Int, maxLevel: Int, resolution: Int, buffer: Int, opts: BeastOptions): JavaPairRDD[java.lang.Long, IntermediateVectorTile]
def plotAllTiles(features: SpatialDataTypes.SpatialRDD, levels: Range, resolution: Int, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): RDD[(Long, IntermediateVectorTile)]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:170  (+1 more definition site/overload)_

_Source doc:_ Plots all tiles in a range of Zoom levels according to the provided specifications and configuration @param features   the set of features to visualize @param minLevel   the minimum level to visualize (inclusive) @param maxLevel   the maximum level to visualize (inclusive) @param resolution the resolution of each tile @param buffer     the buffer around each tile to consider when visualizing @param opts       additional options for generating the tiles @return an RDD that contains all the generated tiles along with their IDs.

### Goal
`plotAllTiles` generates and visualizes raster tiles for a specified range of zoom levels based on the provided spatial features and configuration options.

### Parameters
- `features` (`SpatialDataTypes.JavaSpatialRDD`): The set of spatial features to visualize, which can be loaded from various geospatial data formats such as shapefiles or GeoJSON.
- `minLevel` (`Int`): The minimum zoom level to visualize (inclusive), indicating the lowest level of detail for the generated tiles.
- `maxLevel` (`Int`): The maximum zoom level to visualize (inclusive), indicating the highest level of detail for the generated tiles.
- `resolution` (`Int`): The resolution of each tile, which determines the pixel density and detail of the visualized output.
- `buffer` (`Int`): The buffer size around each tile to consider when visualizing, allowing for additional context around the features.
- `opts` (`BeastOptions`): Additional options for generating the tiles, which can include parameters like thresholds or styling options.

### Input
The caller must provide a `SpatialDataTypes.JavaSpatialRDD` containing the spatial features, along with integer values for `minLevel`, `maxLevel`, `resolution`, and `buffer`. The `opts` parameter should be an instance of `BeastOptions` containing any additional configuration settings.

### Output
Returns `JavaPairRDD[java.lang.Long, IntermediateVectorTile]` — an RDD containing all the generated tiles along with their unique IDs, where each tile is represented as an `IntermediateVectorTile` object.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, minLevel = 0, maxLevel = 6, resolution = 256, buffer = 5, opts)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialDataTypes.JavaSpatialRDD` and that the zoom levels (`minLevel` and `maxLevel`) are within a reasonable range for the data being visualized.

### Prompt Snippet
```text
To visualize spatial features as raster tiles, use the `plotAllTiles` function with appropriate parameters for features, zoom levels, resolution, buffer, and options.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 3x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.50 executor driver): java.lan

### Fix Code Hint
```scala
// Ensure that the features are loaded correctly and that minLevel is less than or equal to maxLevel
val features = sparkContext.shapefile("path_to_your_shapefile.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, minLevel = 0, maxLevel = 6, resolution = 256, buffer = 5, opts)
```

## API Test: `plotSingleTileParallel`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def plotSingleTileParallel(features: SpatialDataTypes.SpatialRDD, resolution: Int, tileID: Long, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): VectorTile.Tile
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:98_

_Source doc:_ Plots the given set of features as a vector tile according to Mapbox specifications using a Spark job. @param features the set of features to plot @param resolution the resolution of the image in pixels @param tileID the ID of the tile to plot @param buffer additional pixels around the tile to plot from all directions (default is zero) @param opts additional options to customize the plotting @return a vector tile that contains all the given features

### Goal
`plotSingleTileParallel` generates a vector tile from a set of spatial features, allowing for efficient visualization of geospatial data in accordance with Mapbox specifications.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): A distributed collection of spatial features to be plotted as a vector tile. This should contain geometries such as points, lines, or polygons.
- `resolution` (`Int`): The resolution of the output vector tile in pixels. This determines the level of detail in the rendered tile.
- `tileID` (`Long`): The unique identifier for the tile being generated, typically encoded using a tile indexing scheme.
- `buffer` (`Int`), default `0`: The number of additional pixels to include around the tile in all directions. This can be used to provide context around the main tile area.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional options to customize the plotting behavior, such as styling or rendering preferences.

### Input
The input must consist of a valid `SpatialRDD` containing spatial features, and the parameters must be set according to the desired output tile characteristics. The `resolution` must be a positive integer, and the `tileID` must be a valid long integer representing the tile's unique identifier.

### Output
Returns `VectorTile.Tile` — a vector tile that encapsulates the plotted features, formatted according to Mapbox specifications, suitable for rendering in web mapping applications.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val wktReader = new WKTReader(factory)
val geometries = Array("POINT(-90 0)").map(wkt => wktReader.read(wkt))
val features: RDD[IFeature] = sparkContext.parallelize(geometries).map(g => Feature.create(null, g))

val tile = MVTDataVisualizer.plotSingleTileParallel(features, 100, TileIndex.encode(0, 0, 0), 0)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing spatial geometries. The `resolution` must be a positive integer, and the `tileID` must be a valid long integer. The `buffer` and `opts` parameters are optional and can be omitted if default values are acceptable.

### Prompt Snippet
```text
Generate a vector tile using `plotSingleTileParallel` with the specified features, resolution, and tileID.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the features RDD is populated and the parameters are correctly set
val features: RDD[IFeature] = sparkContext.parallelize(geometries).map(g => Feature.create(null, g))
val tile = MVTDataVisualizer.plotSingleTileParallel(features, 128, TileIndex.encode(0, 0, 0), 0)
```

## API Test: `saveTiles`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def saveTiles(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, opts: BeastOptions): Unit
def saveTiles(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:453  (+1 more definition site/overload)_

_Source doc:_ Save an RDD of tiles to the given output @param tiles   the set of tiles to save @param outPath the path to save the tiles to

### Goal
`saveTiles` saves a distributed collection of raster tiles to a specified output path, facilitating the storage of processed geospatial data.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): A distributed collection of tiles, where each tile is associated with a unique identifier (Long) and contains intermediate vector tile data (IntermediateVectorTile).
- `outPath` (`String`): The file path where the tiles will be saved. This should be a valid path in the file system accessible by the Spark cluster.
- `opts` (`BeastOptions`): Configuration options for the saving process, which may include parameters such as compression settings or other options specific to the output format.

### Input
The caller must provide:
- A `JavaPairRDD` or `RDD` containing the tiles to be saved, ensuring that the tiles are properly formatted as `IntermediateVectorTile`.
- A valid output path as a string where the tiles will be stored.
- An instance of `BeastOptions` to configure the saving process.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value, signifying that the tiles have been successfully saved to the specified output path.

### Valid Call Patterns
```scala
value.saveTiles(tiles, "output/path/to/tiles", beastOptions)
```

### LLM Instruction Prompt
- Ensure that the `tiles` RDD is properly populated with `IntermediateVectorTile` data before calling `saveTiles`.
- Verify that the `outPath` is a valid and accessible path in the file system.
- Provide appropriate `BeastOptions` to customize the saving behavior if necessary.

### Prompt Snippet
```text
To save the tiles, use the `saveTiles` method with the appropriate parameters, ensuring the tiles are correctly formatted and the output path is valid.
```

### Common Failure Modes
- **[compile]** error: constructor cannot be instantiated to expected type; _(seen 2x)_
- **[compile]** error: not found: value createTilesFromRaster
- **[compile]** error: type RasterRDD takes type parameters

### Fix Code Hint
```scala
// Ensure the tiles RDD is populated and the output path is valid before calling saveTiles
val tiles: JavaPairRDD[Long, IntermediateVectorTile] = // your code to create tiles
val outPath: String = "output/path/to/tiles"
val opts: BeastOptions = // your code to create BeastOptions
saveTiles(tiles, outPath, opts)
```

## API Test: `saveTilesCompact`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

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
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): A distributed collection of tiles, where each tile is associated with a unique identifier (Long) and contains intermediate vector tile data (IntermediateVectorTile) for visualization.
- `outPath` (`String`): The file path where the output ZIP file will be saved. This should be a valid path accessible by the Spark job.
- `_opts` (`BeastOptions`): Additional options that may influence the visualization process, such as rendering thresholds or other parameters specific to the visualization context.

### Input
The caller must provide:
- A valid `JavaPairRDD` or `RDD` containing tiles, which must be generated from a previous visualization operation.
- A valid output path as a string where the ZIP file will be saved.
- An instance of `BeastOptions` containing any necessary visualization options.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs the action of saving the tiles to the specified ZIP file.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
```

### LLM Instruction Prompt
- Ensure that the `tiles` parameter is a valid `JavaPairRDD` or `RDD` containing intermediate vector tiles.
- The `outPath` must be a valid file path where the ZIP file can be created.
- The `_opts` parameter should be an instance of `BeastOptions` with appropriate visualization settings.

### Prompt Snippet
```text
To save the tiles, call `MVTDataVisualizer.saveTilesCompact(tiles, "output_path.zip", options)`, ensuring that `tiles` is a valid RDD of IntermediateVectorTile.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.50 executor driver): java.lan _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the output path is valid and accessible
val validOutPath = "path/to/output.zip"
MVTDataVisualizer.saveTilesCompact(tiles, validOutPath, opts)
```
