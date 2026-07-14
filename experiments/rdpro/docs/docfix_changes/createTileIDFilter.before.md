## API Test: `createTileIDFilter`

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
Create a Hadoop `PathFilter` that keeps only HDF tile files whose `hxxvyy` tile ID intersects a requested rectangle in Sinusoidal space.

### Parameters
- `rect` (`Rectangle2D`): Rectangle extents for the selection window **in Sinusoidal space** (as documented), used to compute which `hxxvyy` tiles should be accepted.

### Input
- A `Rectangle2D` instance representing the target range in Sinusoidal coordinates.
- The returned filter is intended for paths whose filenames include tile IDs in the documented `hxxvyy` form (example from tests: `tile-h03v03.hdf`).
- Precondition: coordinates must already be in the Sinusoidal space expected by this API (the method does not document reprojection/conversion).

### Output
Returns `PathFilter` — a Hadoop path filter that accepts/rejects file paths by parsing the filename tile token (`hxxvyy`) and matching it against the tile set implied by `rect`.

### Valid Call Patterns
```scala
val tileIDFilter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale, Math.toRadians(29.0) * HDF4Reader.Scale, Math.toRadians(49.0) * HDF4Reader.Scale))
assert(tileIDFilter.accept(new Path("tile-h03v03.hdf")))
assert(tileIDFilter.accept(new Path("tile-h06v07.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h02v09.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h07v06.hdf")))
```

### LLM Instruction Prompt
- Call the method with the exact receiver form verified by tests: `HDF4Reader.createTileIDFilter(rect)`.
- Pass exactly one argument of type `Rectangle2D`.
- Provide rectangle extents in Sinusoidal space, not lat/lon degrees unless already converted.
- Use the returned object as a Hadoop `PathFilter` and call `accept(Path)` on candidate files.
- Expect matching based on filename `hxxvyy` token.

### Prompt Snippet
```text
Create a Sinusoidal Rectangle2D, then call HDF4Reader.createTileIDFilter(rect). Use the returned PathFilter to test HDF file paths whose names contain an hxxvyy tile ID (e.g., tile-h03v03.hdf). Do not pass extra parameters.
```

### Common Failure Modes
- Passing a rectangle in the wrong coordinate space (e.g., unconverted geographic degrees) causes wrong tile selection.
- Using filenames that do not contain the expected `hxxvyy` pattern prevents intended matching.
- Calling a different receiver shape (e.g., bare `createTileIDFilter(...)`) may not compile in user code.

### Fix Code Hint
```scala
val rect = new Rectangle2D.Double(
  Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale,
  Math.toRadians(29.0) * HDF4Reader.Scale,
  Math.toRadians(49.0) * HDF4Reader.Scale
)
val tileIDFilter: PathFilter = HDF4Reader.createTileIDFilter(rect)
```