## API Test: `compress`

### Signature
```scala
protected[raptor] def compress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:211_

### Goal
Compress the in-memory pixel storage of a Raptor `MemoryTile` while preserving pixel values for later read/write access in distributed raster processing workflows.

### Parameters
_None._

### Input
Call this on an existing `MemoryTile` instance (as shown in tests: `tile.compress`) after pixel values are already loaded or written (e.g., via `setPixelValue`).

Grounded preconditions from available context:
- This is an internal API (`protected[raptor]`), not a public RDPro user-facing operation.
- No file path or raster format argument is passed to `compress`; it operates on the tile object’s current in-memory state.
- Test-verified behavior indicates automatic decompression on subsequent `getPixelValue` and `setPixelValue` calls.

### Output
Returns `Unit` — no direct return value; the effect is state change on the tile (compressed internal representation), with pixel content still readable/writable afterward via automatic decompression.

### Valid Call Patterns
```scala
tile.compress
```

### LLM Instruction Prompt
- Use the receiver form exactly as verified in tests: `tile.compress`.
- Do not add arguments (the method takes none).
- Do not present this as a public top-level RDPro raster API; it is internal to `raptor` (`protected[raptor]`).
- If generating end-user pipelines, prefer documented public raster APIs (`geoTiff`, `mapPixels`, `reshapeNN`, `saveAsGeoTiff`) unless you are explicitly working inside Raptor internals/tests.

### Prompt Snippet
```text
Given a MemoryTile instance named tile, call compression with:
tile.compress
Do not pass parameters. This mutates tile state and returns Unit.
```

### Common Failure Modes
- Calling `compress` from outside allowed visibility scope (`protected[raptor]`) and getting an access error.
- Incorrectly invoking it like `tile.compress()` with expected return data; it returns `Unit` and is used for side effects.
- Treating `compress` as a file compression/export API (it does not write GeoTIFF/CSV and takes no path).

### Fix Code Hint
```scala
// Internal Raptor usage pattern (as verified by tests)
tile.compress
// Then continue normal pixel access; decompression is automatic on read/write
val v = tile.getPixelValue(0, 0)
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```