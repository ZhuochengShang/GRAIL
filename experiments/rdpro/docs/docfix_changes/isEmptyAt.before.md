## API Test: `isEmptyAt`

### Signature
```scala
def isEmptyAt(x: Double, y: Double): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:114_

_Source doc:_ Check if the pixel that contains the given location is empty @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return `true` if the pixel at the location is empty, i.e., contains no data

### Goal
Check whether the raster pixel covering a given map location `(x, y)` is no-data/empty in an RDPro/Beast tile.

### Parameters
- `x` (`Double`): X coordinate of the query point (for example, longitude), in the same coordinate space used by the tile metadata.
- `y` (`Double`): Y coordinate of the query point (for example, latitude), in the same coordinate space used by the tile metadata.

### Input
A raster tile object that implements this method (as used in tests: `tile1.isEmptyAt(...)`), plus numeric coordinates as `Double`.

Preconditions from observed usage:
- The tile must already be read/loaded from raster data (e.g., via `GeoTiffReader.readTile(...)`).
- Coordinates should be meaningful for that tile’s georeferencing (same CRS/space as the tile metadata); otherwise the result may not represent the intended location.
- No file format is passed directly to `isEmptyAt`; format handling (GeoTIFF/HDF, etc.) happens earlier when reading raster data.

### Output
Returns `Boolean` — `true` means the pixel containing `(x, y)` is empty (contains no data), and `false` means it is not empty.

### Valid Call Patterns
```scala
val rasterPath = locateResource("/rasters/glc2000_small.tif")
val fileSystem = new Path(rasterPath.getPath).getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.getPath, "0", "fillvalue" -> 8)
  val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
  assert(tile1.isEmptyAt(23.224, 32.415))
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Call this as an instance method on a tile object: `tile.isEmptyAt(x, y)`.
- Pass both coordinates as `Double`.
- Use coordinates in the tile’s coordinate reference space.
- Do not invent extra parameters (there are only `x` and `y`).
- Load/read raster data first; `isEmptyAt` is a per-tile query, not a file-loading API.

### Prompt Snippet
```text
Given a loaded raster tile (e.g., tile1 from GeoTiffReader.readTile), call:
tile1.isEmptyAt(x, y)
where x and y are Double coordinates in the tile’s coordinate system. 
Interpret true as no-data/empty pixel at that location.
```

### Common Failure Modes
- Calling `isEmptyAt` without a tile instance (it is not shown as a static/global function).
- Passing coordinates in a different CRS/space than the tile uses.
- Expecting this method to load files or perform reprojection/alignment automatically (it does neither).
- Using non-`Double` coordinate literals in strict contexts without conversion.

### Fix Code Hint
```scala
// Ensure you already have a tile, then query emptiness at map coordinates
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val isNoData: Boolean = tile1.isEmptyAt(23.224, 32.415)
```