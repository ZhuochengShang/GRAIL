# MemoryTile2

_The `setPixelValue` function sets the value of a specific pixel in a raster tile, allowing for pixel-level modifications in geospatial raster processing._

**Receiver:** instance — obtain a `MemoryTile2` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `setPixelValue` **(primary)**

---

## API Test: `setPixelValue`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def setPixelValue(i: Int, j:Int, value: T): Unit
def setPixelValue(i: Int, j: Int, value: T): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:147  (+1 more definition site/overload)_

_Source doc:_ Sets the value of the given pixel @param i the column position of the pixel @param j the row position of the pixel @param value the value to set at the given pixel

### Goal
The `setPixelValue` function sets the value of a specific pixel in a raster tile, allowing for pixel-level modifications in geospatial raster processing.

### Parameters
- `i` (`Int`): The column position of the pixel to be modified, expected to be within the bounds of the raster tile's width.
- `j` (`Int`): The row position of the pixel to be modified, expected to be within the bounds of the raster tile's height.
- `value` (`T`): The value to set at the specified pixel, which must match the pixel type of the raster tile (e.g., `Float`, `Array[Float]`).

### Input
The caller must provide a raster tile that has been initialized and is accessible. The pixel positions `i` and `j` must be valid indices within the dimensions of the raster tile. The `value` must be of the correct type corresponding to the raster's pixel type.

### Output
Returns `Unit` — indicating that the operation has been completed successfully without returning a value.

### Valid Call Patterns
```scala
tile1.setPixelValue(0, 0, 0.5f)
tile1.setPixelValue(1, 0, Array(0.5f, 0.1f))
```

### LLM Instruction Prompt
- Ensure that the pixel indices `i` and `j` are within the valid range of the raster tile dimensions before calling `setPixelValue`.
- Confirm that the `value` type matches the expected pixel type of the raster tile.

### Prompt Snippet
```text
Set the pixel value at column i and row j of the raster tile to the specified value using setPixelValue.
```

### Common Failure Modes
- **[compile]** error: value width is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the indices are within bounds and the value type matches the raster tile's pixel type
if (i >= 0 && i < tile.width && j >= 0 && j < tile.height) {
  tile.setPixelValue(i, j, value) // Ensure value is of the correct type
} else {
  throw new IllegalArgumentException("Pixel indices are out of bounds.")
}
```
