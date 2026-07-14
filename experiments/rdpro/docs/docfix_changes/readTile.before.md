## API Test: `readTile`

### Signature
```scala
override def readTile(tileID: Int): ITile[T]
def readTile(tileID: Int): ITile[T]
override def readTile(tileID: Int): ITile[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:167  (+2 more definition site/overload)_

### Goal
Read one raster tile by tile ID from an initialized raster reader (e.g., GeoTIFF reader) for use in pixel access and raster analysis workflows.

### Parameters
- `tileID` (`Int`): The ID of the tile to read (typically obtained from reader metadata, e.g., from pixel or point-to-tile lookup methods).

### Input
A raster reader instance must already be initialized on raster input (project context documents GeoTIFF/HDF support in RDPro; test-backed usage here is `GeoTiffReader`).  
Preconditions from observed usage and API/source doc:
- Call on an initialized reader (`reader.initialize(...)` is done first in tests).
- Provide a valid tile ID for that raster; test usage derives it from metadata (`getTileIDAtPixel`, `getTileIDAtPoint`).
- The interface requires accessors to support multiple concurrent `readTile` calls.
- Returned tile may or may not remain usable after reader close; both behaviors are allowed by the interface, so do not rely on post-close validity unless implementation-specific behavior is known.

### Output
Returns `ITile[T]` — an object containing tile information and pixel values for the requested tile, parameterized by the reader pixel type `T` (or `Float` in the float overload).

### Valid Call Patterns
```scala
val tileID = reader.metadata.getTileIDAtPixel(37, 24)
val tile = reader.readTile(tileID)
```

```scala
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val tile2 = reader.readTile(reader.metadata.getTileIDAtPoint(33.694, 14.761))
```

### LLM Instruction Prompt
- Use the instance call form exactly: `reader.readTile(tileID)`.
- Derive `tileID` from the same reader’s metadata (e.g., point/pixel lookup) rather than inventing IDs.
- Ensure reader initialization happens before calling `readTile`.
- Keep the reader’s type parameter consistent with raster pixel type (e.g., `GeoTiffReader[Int]`, `GeoTiffReader[Array[Int]]`, `GeoTiffReader[Float]`).
- Do not assume the returned tile is valid after `reader.close()` unless explicitly guaranteed by that implementation.

### Prompt Snippet
```text
Initialize a GeoTiffReader[T], compute tileID from reader.metadata (getTileIDAtPixel or getTileIDAtPoint), then call reader.readTile(tileID). Keep T matched to actual raster pixel type and access tile values before closing the reader.
```

### Common Failure Modes
- Calling `readTile` before initializing the reader.
- Passing a tile ID not belonging to the current raster/metadata.
- Mismatching generic pixel type `T` with actual raster pixel encoding.
- Assuming tile lifetime after `reader.close()` (not guaranteed by interface; implementation-dependent).

### Fix Code Hint
```scala
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val tileID = reader.metadata.getTileIDAtPoint(23.224, 32.415)
  val tile = reader.readTile(tileID)
  val v = tile.getPointValue(23.224, 32.415)
} finally {
  reader.close()
}
```