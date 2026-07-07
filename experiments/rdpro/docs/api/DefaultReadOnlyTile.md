# DefaultReadOnlyTile

_Determines whether a specific tile at the given coordinates `(i, j)` is empty, which is useful for assessing the presence of data in raster processing._

**Receiver:** instance — obtain a `DefaultReadOnlyTile` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `isEmpty` **(primary)**, ⚠️ `getPixelValue`

---

## API Test: `isEmpty`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def isEmpty: Boolean
override def isEmpty(i: Int, j: Int): Boolean
def isEmpty(i: Int, j: Int): Boolean
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:44  (+15 more definition site/overload)_

### Goal
Determines whether a specific tile at the given coordinates `(i, j)` is empty, which is useful for assessing the presence of data in raster processing.

### Parameters
- `i` (`Int`): The row index of the tile in the raster grid, representing the vertical position.
- `j` (`Int`): The column index of the tile in the raster grid, representing the horizontal position.

### Input
The caller must provide valid integer indices `i` and `j` that correspond to the tile coordinates in the raster dataset. The raster must be loaded and accessible in the context where `isEmpty` is called.

### Output
Returns `Boolean` — `true` if the tile at the specified coordinates `(i, j)` is empty (contains no data), and `false` otherwise.

### Valid Call Patterns
```scala
val raster: RDD[ITile[Int]] = sc.geoTiff("glc2000_v1_1.tif")
val isTileEmpty: Boolean = raster.isEmpty(0, 0) // Check if the tile at (0, 0) is empty
```

### LLM Instruction Prompt
- Ensure that the raster data is loaded and accessible before calling `isEmpty`. Use valid integer indices for the tile coordinates.

### Prompt Snippet
```text
Check if the tile at coordinates (i, j) is empty using the isEmpty method.
```

### Common Failure Modes
- **[compile]** error: no arguments allowed for nullary method isEmpty: ()Boolean _(seen 3x)_

### Fix Code Hint
```scala
// Ensure the indices are within the bounds of the raster dimensions before calling isEmpty
if (i >= 0 && i < raster.height && j >= 0 && j < raster.width) {
    val isTileEmpty: Boolean = raster.isEmpty(i, j)
} else {
    throw new IllegalArgumentException("Indices are out of bounds for the raster dimensions.")
}
```

## API Test: `getPixelValue`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def getPixelValue(i: Int, j: Int): Float
override def getPixelValue(i: Int, j: Int): Array[Float]
override def getPixelValue(i: Int, j: Int): T
override def getPixelValue(i: Int, j: Int): Array[Int]
override def getPixelValue(i: Int, j: Int): U
override def getPixelValue(i: Int, j: Int): Array[Double]
override def getPixelValue(i: Int, j: Int): Double
override def getPixelValue(i: Int, j: Int): Int
override def getPixelValue(x: Int, y: Int): Array[T]
def getPixelValue(i: Int, j: Int): T
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:135  (+20 more definition site/overload)_

### Goal
The `getPixelValue` function retrieves the value of a pixel at specified coordinates (i, j) from a raster tile, which is essential for performing pixel-level operations in geospatial raster analysis.

### Parameters
- `i` (`Int`): The row index of the pixel in the raster tile, where the value must be a non-negative integer within the bounds of the raster's height.
- `j` (`Int`): The column index of the pixel in the raster tile, where the value must be a non-negative integer within the bounds of the raster's width.

### Input
The caller must provide a raster tile that has been properly initialized and populated with pixel values. The raster must be accessible and the indices `i` and `j` must be within the valid range of the raster dimensions.

### Output
Returns `Float` — the pixel value at the specified coordinates (i, j). This value represents the intensity or measurement at that pixel location, which can be used for further analysis or transformations.

### Valid Call Patterns
```scala
val pixelValue: Float = convWindow.getPixelValue(0, 0)
val multiBandPixelValue: Array[Float] = convWindow.getPixelValue(1, 1)
```

### LLM Instruction Prompt
- When calling `getPixelValue`, ensure that the indices `i` and `j` are within the valid range of the raster dimensions. The function can return different types based on the context, so ensure the expected return type matches the usage.

### Prompt Snippet
```text
Retrieve the pixel value at coordinates (i, j) from the raster tile using getPixelValue(i, j).
```

### Common Failure Modes
- **[compile]** error: value getHeight is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 2x)_
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 2x)_

### Fix Code Hint
```scala
// Ensure that the indices are within bounds before calling getPixelValue
if (i >= 0 && i < rasterHeight && j >= 0 && j < rasterWidth) {
    val value = raster.getPixelValue(i, j)
} else {
    throw new IllegalArgumentException("Indices are out of bounds.")
}
```
