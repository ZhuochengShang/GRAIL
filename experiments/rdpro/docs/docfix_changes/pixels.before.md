## API Test: `pixels`

### Signature
```scala
def pixels: Iterator[(Int, Int, T)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84_

### Goal
Iterate over all pixels in an `ITile`, returning each pixel as its tile coordinates plus typed pixel value for downstream raster analysis (e.g., filtering, aggregation, export-ready transformation).

### Parameters
_None._

### Input
- Receiver: an existing tile object (`ITile[T]`) in memory.
- `pixels` itself does **not** load files; raster file formats (GeoTIFF/HDF) are handled earlier by RDPro readers/loaders (for example via `sc.geoTiff[T]` / `sc.hdfFile(...)` workflows).
- Type rule: the tile’s `T` must already match the raster pixel type selected at load time (project rule: typed raster loading must match actual pixel type).
- No additional arguments or options are accepted.

### Output
Returns `Iterator[(Int, Int, T)]` — each element is one pixel as:
1. `Int`: pixel x/index within the tile,
2. `Int`: pixel y/index within the tile,
3. `T`: pixel value (typed to the tile pixel type).

### Valid Call Patterns
```scala
// Inferred from signature/API facts (no direct test or README verbatim call for `pixels`)
val px: Iterator[(Int, Int, T)] = tile.pixels
```

### LLM Instruction Prompt
- Call as an instance member on a tile value: `tile.pixels`.
- Do not add parameters (method has none).
- Preserve generic pixel type `T` from the tile; do not cast unless required by surrounding logic.
- If starting from files, load raster first with correct typed API (`sc.geoTiff[T]`) before reaching tile-level iteration.

### Prompt Snippet
```text
Given an ITile[T] value named `tile`, iterate its pixels using `tile.pixels` (no arguments) and consume the returned Iterator[(Int, Int, T)].
```

### Common Failure Modes
- Calling `pixels(...)` with arguments (signature has none).
- Calling `pixels` without a tile receiver in scope.
- Pixel type mismatch introduced earlier during raster load (e.g., wrong `sc.geoTiff[T]` type), which can break downstream typed logic.
- Assuming `pixels` performs file I/O; it only iterates an already-available tile.

### Fix Code Hint
```scala
// Ensure you already have an ITile[T] named `tile`
val it: Iterator[(Int, Int, T)] = tile.pixels

// Example consumption
it.foreach { case (x, y, v) =>
  // process per-pixel value v at tile coordinate (x, y)
}
```