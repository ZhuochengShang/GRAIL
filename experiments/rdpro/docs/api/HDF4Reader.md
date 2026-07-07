# HDF4Reader

_The `createTileIDFilter` function generates a filter that selects raster tiles based on their identifiers, ensuring they fall within a specified rectangular…_

**Receiver:** instance — obtain a `HDF4Reader` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `createTileIDFilter` **(primary)**, ★ `metadata`, ⚠️ `createDateFilter`, ⚠️ `readTile`

---

## API Test: `createTileIDFilter`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
The `createTileIDFilter` function generates a filter that selects raster tiles based on their identifiers, ensuring they fall within a specified rectangular area in Sinusoidal projection.

### Parameters
- `rect` (`Rectangle2D`): A rectangle defining the extents of the area in Sinusoidal space for which the tile filter will be computed. The rectangle should be specified in the coordinate system used by the tiles.

### Input
The caller must provide a `Rectangle2D` object that accurately represents the desired spatial extents. This rectangle should correspond to the Sinusoidal projection used by the raster tiles.

### Output
Returns `PathFilter` — a filter that matches tile paths based on their identifiers, specifically the `hxxvyy` part of the tile name, allowing for efficient selection of relevant tiles.

### Valid Call Patterns
```scala
val tileIDFilter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale, Math.toRadians(29.0) * HDF4Reader.Scale, Math.toRadians(49.0) * HDF4Reader.Scale))
```

### LLM Instruction Prompt
- When calling `createTileIDFilter`, ensure that the `rect` parameter is a valid `Rectangle2D` object representing the desired spatial extents in Sinusoidal coordinates.

### Prompt Snippet
```text
Create a tile ID filter for the specified rectangular area in Sinusoidal space using `createTileIDFilter`.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the `Rectangle2D` provided to `createTileIDFilter` accurately reflects the desired area in Sinusoidal coordinates to avoid mismatches in tile selection.
```

## API Test: `metadata`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def metadata: RasterMetadata
def metadata: RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:165  (+2 more definition site/overload)_

### Goal
Retrieve the metadata associated with a raster dataset, providing essential information about its dimensions, pixel scale, and coordinate reference system.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded using RDPro, typically from a GeoTIFF file. The dataset must be properly initialized and accessible within the Spark context.

### Output
Returns `RasterMetadata` — an object that encapsulates metadata information about the raster, including properties such as raster width, height, pixel scale, and transformation methods for converting between grid and model coordinates.

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
- Ensure that the raster dataset is properly initialized and accessible before calling `metadata`. The call should be made on an instance of a raster reader that has been set up with a valid raster file.

### Prompt Snippet
```text
Retrieve the metadata for the raster dataset using the `metadata` method on the initialized GeoTiffReader instance.
```

### Common Failure Modes
- **[compile]** error: object BeastOptions is not a member of package edu.ucr.cs.bdlab.beast.util

### Fix Code Hint
```scala
Ensure that the raster file is correctly loaded and the GeoTiffReader is properly initialized before calling `metadata`.
```

## API Test: `createDateFilter`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
The `createDateFilter` function generates a filter that allows for the selection of paths based on a specified date range, facilitating the processing of geospatial raster data within that timeframe.

### Parameters
- `dateStart` (`String`): The start date of the range, formatted as "yyyy.mm.dd" (inclusive).
- `dateEnd` (`String`): The end date of the range, formatted as "yyyy.mm.dd" (inclusive).

### Input
The caller must provide two date strings in the "yyyy.mm.dd" format. The dates must be valid and `dateStart` should be earlier than or equal to `dateEnd`.

### Output
Returns `PathFilter` — an object that can be used to filter paths based on the specified date range, allowing only those paths that fall within the inclusive start and end dates.

### Valid Call Patterns
```scala
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
```

### LLM Instruction Prompt
- Ensure that the `dateStart` and `dateEnd` parameters are provided in the correct "yyyy.mm.dd" format and that `dateStart` is not later than `dateEnd`.

### Prompt Snippet
```text
Create a date filter for paths between "2001.02.15" and "2005.02.11".
```

### Common Failure Modes
- **[compile]** error: type mismatch; _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the date format is correct and that dateStart is not after dateEnd
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
```

## API Test: `readTile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def readTile(tileID: Int): ITile[T]
def readTile(tileID: Int): ITile[T]
override def readTile(tileID: Int): ITile[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:167  (+2 more definition site/overload)_

### Goal
The `readTile` function retrieves a specific tile of raster data identified by the given `tileID` from a GeoTIFF file.

### Parameters
- `tileID` (`Int`): The unique identifier for the tile to be read. This ID corresponds to the tile's position in the raster dataset.

### Input
The caller must provide a valid `tileID` that corresponds to a tile within the loaded raster dataset. The raster data must be loaded using a compatible method, such as `sc.geoTiff[T]`, where `T` matches the expected pixel type (e.g., `Int`, `Float`).

### Output
Returns `ITile[T]` — an instance of `ITile` containing the pixel data for the specified tile. The format of the data is determined by the type parameter `T`, which can represent various pixel types such as integers or floats.

### Valid Call Patterns
```scala
val tile: ITile[Int] = reader.readTile(tileID)
val tileFloat: ITile[Float] = reader.readTile(tileID)
```

### LLM Instruction Prompt
- Ensure that the `tileID` provided is valid and corresponds to a tile in the raster dataset. The raster must be initialized and accessible before calling `readTile`.

### Prompt Snippet
```text
val tile: ITile[Int] = reader.readTile(tileID)
```

### Common Failure Modes
- **[compile]** error: value getReader is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Float]] _(seen 3x)_
- **[compile]** error: value readTile is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Float]]

### Fix Code Hint
```scala
// Ensure the raster is initialized and the tileID is valid before calling readTile
val tileID = reader.metadata.getTileIDAtPoint(x, y) // Example to get a valid tileID
val tile: ITile[Int] = reader.readTile(tileID)
```
