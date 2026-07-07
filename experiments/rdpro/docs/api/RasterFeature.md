# RasterFeature

_The `append` function adds an additional attribute to a geospatial feature, returning a new feature that includes the original geometry and attributes along…_

**Receiver:** instance — obtain a `RasterFeature` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `append` **(primary)**, ★ `create`

---

## API Test: `append`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must provide a valid `IFeature` object as the `feature` parameter. The `value` can be any type, and the optional `name` and `dataType` parameters can be specified based on the user's requirements.

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
- When calling `append`, ensure that the `feature` is a valid `IFeature` and that the `value` is of a compatible type. Optionally, provide a `name` and `dataType` for the new attribute.

### Prompt Snippet
```text
Feature.append(point, polygon.getAs[String]("NAME"), "state")
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure that the feature is a valid IFeature and the value is of the expected type
val newFeature = Feature.append(existingFeature, newValue, "attributeName", DataType.StringType)
```

## API Test: `create`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def create[T](tiles: Array[MemoryTile[T]]): MemoryTileWindow[T]
def create[T: ClassTag](tileID: Int, metadata: RasterMetadata, rasterFeature: RasterFeature, numValues: Int): MemoryTileWindow[T]
def create(row: Row, geometry: Geometry): Feature
def create(geometry: Geometry, _names: Array[String], _types: Array[DataType], _values: Array[Any]): Feature
def create(x1: Double, y1:Double, x2: Double, y2:Double, srid: Int, rasterWidth: Int, rasterHeight: Int, tileWidth: Int, tileHeight: Int): RasterMetadata
def create(names: Array[String], values: Array[Any]): RasterFeature
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:324  (+5 more definition site/overload)_

_Source doc:_ Create a raster metadata that represents a geographical region provided by a rectangle. @param x1 the x-coordinate of the left edge of the pixel at (0, 0) @param y1 the y-coordinate of the top edge of the pixel at (0, 0) @param x2 the x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param y2 the y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param srid the SRID that represents the coordinate reference system of the raster @param rasterWidth the number of columns in the entire raster @param rasterHeight the number of rows in the entire raster @param tileWidth the width of each tile in pixels @param tileHeight the height of each tile in pixels @return a raster metadata with the given information

### Goal
Creates raster metadata that defines the spatial extent and properties of a raster dataset based on specified geographical coordinates and dimensions.

### Parameters
- `x1` (`Double`): The x-coordinate of the left edge of the pixel at (0, 0), representing the western boundary of the raster.
- `y1` (`Double`): The y-coordinate of the top edge of the pixel at (0, 0), representing the northern boundary of the raster.
- `x2` (`Double`): The x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1), representing the eastern boundary of the raster.
- `y2` (`Double`): The y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1), representing the southern boundary of the raster.
- `srid` (`Int`): The Spatial Reference System Identifier (SRID) that defines the coordinate reference system of the raster.
- `rasterWidth` (`Int`): The number of columns (pixels) in the entire raster.
- `rasterHeight` (`Int`): The number of rows (pixels) in the entire raster.
- `tileWidth` (`Int`): The width of each tile in pixels, which affects how the raster is processed in chunks.
- `tileHeight` (`Int`): The height of each tile in pixels, which also affects how the raster is processed in chunks.

### Input
The caller must provide valid geographical coordinates (x1, y1, x2, y2) that define a rectangle, along with the SRID, raster dimensions (width and height), and tile dimensions. The values must be consistent with the raster's intended spatial representation.

### Output
Returns `RasterMetadata` — an object that encapsulates the metadata for the raster, including its spatial extent, dimensions, and coordinate reference system.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
```

### LLM Instruction Prompt
- Ensure that the geographical coordinates provided form a valid rectangle and that the raster dimensions are positive integers.

### Prompt Snippet
```text
Create raster metadata for a geographical region defined by the coordinates (-50, 40) and (-60, 30) with an SRID of 4326, a raster width and height of 10 pixels, and tile dimensions of 10x10 pixels.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure that x1 < x2 and y1 > y2, and that rasterWidth, rasterHeight, tileWidth, and tileHeight are positive integers.
```
