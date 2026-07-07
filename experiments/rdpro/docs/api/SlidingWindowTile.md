# SlidingWindowTile

_`x1` retrieves the x-coordinate of the first pixel in a raster tile._

**Receiver:** instance — obtain a `SlidingWindowTile` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `x1` **(primary)**, ★ `x2`, ★ `y1`, ★ `y2`, ⚠️ `addTile`

---

## API Test: `x1`
_Grounding: test-backed — usage mined from a real, passing test._

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
No specific input is required for this function.

### Output
Returns `Int` — the x-coordinate of the first pixel in the raster tile, typically representing the leftmost edge of the tile.

### Valid Call Patterns
```scala
val xCoordinate: Int = tile.x1
```

### LLM Instruction Prompt
- When calling `x1`, ensure that it is invoked on a valid raster tile object that has been properly initialized.

### Prompt Snippet
```text
Retrieve the x-coordinate of the first pixel in the raster tile using the x1 method.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the raster tile is properly initialized before calling x1
if (tile != null) {
  val xCoordinate: Int = tile.x1
} else {
  // Handle the null case appropriately
}
```

## API Test: `x2`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def x2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16_

### Goal
`x2` retrieves the second dimension size of a raster tile, which is essential for understanding the raster's spatial extent in the vertical direction.

### Parameters
_None._

### Input
No specific input is required for this method.

### Output
Returns `Int` — the value represents the height (number of rows) of the raster tile.

### Valid Call Patterns
```scala
val height: Int = tile.x2
```

### LLM Instruction Prompt
- When calling `x2`, ensure that it is invoked on a valid raster tile object that has been properly initialized.

### Prompt Snippet
```text
Retrieve the height of the raster tile using the x2 method.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
if (tile != null) {
  val height: Int = tile.x2
} else {
  throw new IllegalArgumentException("Raster tile must be initialized before calling x2.")
}
```

## API Test: `y1`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must ensure that the tile object from which `y1` is called is properly initialized and represents a valid raster tile.

### Output
Returns `Int` — the starting y-coordinate of the tile, which indicates the vertical position of the tile in the raster grid.

### Valid Call Patterns
```scala
val startingY: Int = tile.y1
```

### LLM Instruction Prompt
- When calling `y1`, ensure that it is invoked on a valid tile object that has been initialized and represents a raster dataset.

### Prompt Snippet
```text
Retrieve the starting y-coordinate of the raster tile using the `y1` method.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the tile is properly initialized before calling y1
val tile: MemoryTile[Int] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
val startingY: Int = tile.y1
```

## API Test: `y2`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def y2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17_

### Goal
The `y2` function retrieves the maximum y-coordinate index of a tile in a raster dataset.

### Parameters
_None._

### Input
No specific input is required for this function as it operates on the internal state of the tile object.

### Output
Returns `Int` — the maximum y-coordinate index of the tile, which represents the vertical extent of the tile in pixel coordinates.

### Valid Call Patterns
```scala
val maxY: Int = tile.y2
```

### LLM Instruction Prompt
- When calling `y2`, ensure that it is invoked on a valid tile object that has been properly initialized and contains pixel data.

### Prompt Snippet
```text
Retrieve the maximum y-coordinate index of the tile using the y2 method.
```

### Common Failure Modes
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]

### Fix Code Hint
```scala
if (tile != null) {
  val maxY: Int = tile.y2
} else {
  // Handle the null tile case appropriately
}
```

## API Test: `addTile`
_Grounding: test-backed — usage mined from a real, passing test._

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
The caller must provide an `ITile[U]` instance, which represents a raster tile containing pixel values. The input tile should be compatible with the convolution tile's expected data type and structure.

### Output
Returns `Unit` — this indicates that the operation is performed without returning a value, signifying successful integration of the input tile into the convolution tile.

### Valid Call Patterns
```scala
convWindow1.addTile(tile1)
convWindow2.addTile(tile2)
```

### LLM Instruction Prompt
- When calling `addTile`, ensure that the input tile is of the correct type and structure compatible with the convolution tile. The operation should be performed within the context of a convolution tile instance.

### Prompt Snippet
```text
To add a tile to the convolution window, use the addTile method on the convolution tile instance, passing the tile you wish to integrate.
```

### Common Failure Modes
- **[compile]** error: not found: type ConvolutionTile _(seen 3x)_
- **[compile]** error: not enough arguments for constructor ITile: (tileID: Int, rasterMetadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)edu.ucr.cs.b

### Fix Code Hint
```scala
// Ensure the tile being added is of the correct type and that the convolution tile is initialized properly before calling addTile.
```
