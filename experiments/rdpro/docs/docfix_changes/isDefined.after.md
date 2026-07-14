## API Test: `isDefined`
_Grounding: doc-repaired from source (docfix)._

### Goal
Check whether a specific raster pixel location in a tile has a valid (non-empty) value using absolute grid coordinates.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.beast.geolite.ITile` — a Scala trait; reference as `classOf[ITile[T]]` or import directly.

```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Example: Counting defined pixels across an RDD of tiles
val definedCount = rasterRDD.map { tile: ITile[_] =>
  var c = 0L
  var j = tile.y1
  while (j <= tile.y2) {
    var i = tile.x1
    while (i <= tile.x2) {
      if (tile.isDefined(i, j)) c += 1
      i += 1
    }
    j += 1
  }
  c
}.reduce(_ + _)

require(definedCount > 0, "empty result for isDefined")
println("__CHECK__ isDefined " + definedCount)
```

### LLM Instruction Prompt
- `i` and `j` are absolute grid coordinates within the overall raster, not local 0-based indices relative to the tile.
- To safely iterate over all pixels in a specific tile, `i` must range from `tile.x1` to `tile.x2` (inclusive) and `j` must range from `tile.y1` to `tile.y2` (inclusive).
- Call this on an instance of `ITile`.
- Pass exactly two `Int` arguments in order: column index `i` first, row index `j` second.

### Prompt Snippet
```text
Iterate over a tile's pixels using absolute coordinates: `i` from `tile.x1` to `tile.x2` and `j` from `tile.y1` to `tile.y2`. Check validity with `tile.isDefined(i, j)`. Never use 0-based local loops.
```

### Common Failure Modes
- **`ArrayIndexOutOfBoundsException`**: Caused by assuming `i` and `j` are local `0`-based indices. Passing `0` to `isDefined` for a tile whose bounds do not start at the origin accesses the internal array using an invalid offset based on the tile's global position.
- Swapping index meaning/order (`j, i` instead of `i, j`).

### Fix Code Hint
```scala
// WRONG: Using local 0-based indices causes ArrayIndexOutOfBoundsException
var j = 0
while (j <= 255) {
  var i = 0
  while (i <= 255) {
    // Fails if tile does not start at origin (0,0)
    if (tile.isDefined(i, j)) { /* ... */ } 
    i += 1
  }
  j += 1
}

// CORRECT: Using absolute grid coordinates from tile bounds
var j = tile.y1
while (j <= tile.y2) {
  var i = tile.x1
  while (i <= tile.x2) {
    if (tile.isDefined(i, j)) { /* ... */ }
    i += 1
  }
  j += 1
}
```