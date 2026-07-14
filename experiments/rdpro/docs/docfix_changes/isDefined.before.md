## API Test: `isDefined`

### Signature
```scala
@inline def isDefined(i: Int, j: Int): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126_

_Source doc:_ Checks if the given pixel is defined (not empty) @param i the index of the column @param j the index of the row @return `true` if pixel has a valid value or `false` if it does not.

### Goal
Check whether a specific raster pixel location in a tile has a valid (non-empty) value before using it in raster analytics.

### Parameters
- `i` (`Int`): Column index of the pixel to test.
- `j` (`Int`): Row index of the pixel to test.

### Input
Call this on an `ITile` instance (or compatible tile object that provides this method), with pixel indices `(i, j)` for the target cell.

Preconditions from available docs/context:
- The method is pixel-level and assumes you are working with raster tile data already loaded/produced in RDPro workflows (e.g., from GeoTIFF/HDF pipelines).
- `i` and `j` should refer to a valid pixel position in that tile’s grid. (Exact out-of-range behavior is not documented in the provided sources.)

### Output
Returns `Boolean` — `true` means the pixel at `(i, j)` is defined (has a valid value), and `false` means it is empty / not defined.

### Valid Call Patterns
```scala
val isSet: Boolean = tile.isDefined(i, j) // inferred from signature; no verbatim README/test call for this overload was provided
```

### LLM Instruction Prompt
- Use instance-method form on a tile-like receiver: `value.isDefined(i, j)`.
- Pass exactly two `Int` arguments in order: column index first, row index second.
- Do not invent extra parameters (e.g., band index, nodata value, CRS, metadata).
- Treat this as a per-pixel validity check only; it does not load data, reproject, reshape, or aggregate.

### Prompt Snippet
```text
Given an existing raster tile object `tile`, check pixel validity with:
`tile.isDefined(i, j)`.
Use `i` as column index and `j` as row index, both Int.
```

### Common Failure Modes
- Calling `isDefined` as a standalone/global function instead of on a tile instance.
- Swapping index meaning/order (`j, i` instead of `i, j`).
- Assuming it performs raster compatibility fixes (CRS/resolution/tile-size alignment). Those are separate reshape/reproject steps in RDPro.
- Using indices that do not correspond to the tile extent (bounds behavior is not specified in provided docs).

### Fix Code Hint
```scala
// Correct call shape: instance method on a tile object
val defined: Boolean = tile.isDefined(i, j)
if (defined) {
  // safe to read/use this pixel in your logic
}
```