## API Test: `getPointValue`

### Signature
```scala
def getPointValue(x: Double, y: Double): T
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93_

_Source doc:_ Return the value of the pixel that contains the given point at model (world) coordinates. @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the value of all components of the given pixel

### Goal
Read the pixel value from a raster tile at a given world-coordinate point (for example longitude/latitude) in RDPro/Beast raster workflows.

### Parameters
- `x` (`Double`): X coordinate in model/world space (e.g., longitude) used to locate the containing pixel.
- `y` (`Double`): Y coordinate in model/world space (e.g., latitude) used to locate the containing pixel.

### Input
A tile instance (`ITile[T]` implementation) that has already been read/loaded from a raster source (e.g., GeoTIFF via `GeoTiffReader` in the tested usage), plus world coordinates `(x, y)` that fall in that tile’s spatial extent.

Preconditions and compatibility notes:
- Coordinates are **model/world coordinates**, not pixel row/column indices.
- The tile should be chosen for the point first (tested pattern uses `reader.metadata.getTileIDAtPoint(...)` then `reader.readTile(...)`).
- Generic pixel type `T` must match the raster data type used when reading (e.g., `Int` for integer single-band, `Array[Float]` for multi-band float), consistent with Beast typed raster rules.

### Output
Returns `T` — the value of the pixel that contains `(x, y)`.  
For single-band rasters this is typically a scalar (e.g., `Int`); for multi-band rasters this is the per-band component array (e.g., `Array[Float]`).

### Valid Call Patterns
```scala
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val v1: Int = tile1.getPointValue(23.224, 32.415)

val tile2 = reader.readTile(reader.metadata.getTileIDAtPoint(31.277, 26.954))
val v2: Array[Float] = tile2.getPointValue(31.277, 26.954)
```

### LLM Instruction Prompt
- Call as an instance method on a tile object: `tile.getPointValue(x, y)`.
- Pass exactly two `Double` world coordinates.
- Ensure the tile is read from the tile ID containing the same point before calling.
- Keep the pixel type `T` consistent with the reader/load type (do not mix `Int` vs `Array[Float]`).

### Prompt Snippet
```text
Given an already loaded tile (ITile[T]) and a world-coordinate point (x, y), call:
tile.getPointValue(x, y)
Use Double coordinates (model/world space), not pixel indices. Ensure T matches raster pixel type.
```

### Common Failure Modes
- Using pixel indices `(col,row)` instead of world coordinates `(x,y)`.
- Calling `getPointValue` on a tile that does not spatially contain the point.
- Type mismatch between reader/load type and expected return type (`Int` vs `Array[Float]`).
- Trying to call `getPointValue` before reading/initializing raster/tile data.

### Fix Code Hint
```scala
val tile = reader.readTile(reader.metadata.getTileIDAtPoint(x, y))
val value = tile.getPointValue(x, y) // x,y are world/model coordinates as Double
```