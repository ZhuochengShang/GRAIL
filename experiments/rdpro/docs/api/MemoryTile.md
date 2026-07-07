# MemoryTile

_The `compress` function optimizes the storage of raster data by compressing the pixel values in memory, which can improve performance and reduce memory usage…_

**Receiver:** instance — obtain a `MemoryTile` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `compress` **(primary)**, ⚠️ `decompress`

---

## API Test: `compress`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
protected[raptor] def compress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:211_

### Goal
The `compress` function optimizes the storage of raster data by compressing the pixel values in memory, which can improve performance and reduce memory usage during processing.

### Parameters
_None._

### Input
The caller must provide a `MemoryTile` instance containing pixel values that need to be compressed. The pixel values should be in a format compatible with the `MemoryTile` class, such as `Array[Byte]`.

### Output
Returns `Unit` — this indicates that the compression operation has been performed successfully, and there is no return value to represent.

### Valid Call Patterns
```scala
tile.compress
```
Where `tile` is an instance of `MemoryTile[Array[Byte]]`.

### LLM Instruction Prompt
- Ensure that the `compress` method is called on a valid `MemoryTile` instance that has pixel values set. The method does not take any parameters and does not return any value.

### Prompt Snippet
```text
Call the compress method on a MemoryTile instance to optimize the storage of pixel values.
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 3x)_
- **[compile]** error: value metadata is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Byte]

### Fix Code Hint
```scala
// Ensure the MemoryTile is properly initialized with pixel values before calling compress
val metadata = new RasterMetadata(0, 0, 100, 100, 100, 100, 4326, new AffineTransform())
val tile: MemoryTile[Array[Byte]] = new MemoryTile(0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile.setPixelValue(0, 0, Array[Byte](100, 15, 20))
tile.compress // Call compress after setting pixel values
```

## API Test: `decompress`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
protected def decompress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:231_

### Goal
The `decompress` function is used to restore a compressed raster tile to its original uncompressed state, facilitating further processing or analysis.

### Parameters
_None._

### Input
The function operates on an instance of a raster tile that has been previously compressed. There are no additional input parameters required from the caller.

### Output
Returns `Unit` — this indicates that the operation is performed in-place on the raster tile, and there is no return value to represent the state of the tile after decompression.

### Valid Call Patterns
```scala
tile.decompress
```

### LLM Instruction Prompt
- When calling `decompress`, ensure that the raster tile instance has been previously compressed. The function modifies the state of the tile directly without returning any value.

### Prompt Snippet
```text
Call the `decompress` method on a raster tile instance to restore it to its uncompressed state.
```

### Common Failure Modes
- **[compile]** error: value decompress is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing] _(seen 3x)_
- **[compile]** error: value _2 is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]

### Fix Code Hint
```scala
// Ensure the tile is compressed before calling decompress
tile.compress
tile.decompress
```
