## API Test: `isDefined`
_Grounding: doc-repaired from source (docfix)._

### Goal
On an `ITile` object, checks if the pixel at the specified **global grid coordinates** `(i, j)` has a valid value (is not empty). This method is called on a single tile, typically obtained from an `RDD[ITile[T]]`.

### Valid Call Patterns|Valid Access Patterns
```scala
// Requires an RDD of tiles, e.g., from a GeoTIFF load.
// The RDD element is the ITile object itself, not a (Key, Value) tuple.
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Assuming rasterRDD is RDD[ITile[Float]]
val aTile: ITile[Float] = rasterRDD.first()

// The i and j parameters for isDefined MUST be global grid coordinates.
// To iterate a tile, use its global boundary members: x1, y1, x2, y2.
var definedPixelCount = 0
for (j <- aTile.y1 to aTile.y2; i <- aTile.x1 to aTile.x2) {
  if (aTile.isDefined(i, j)) {
    definedPixelCount += 1
  }
}
```

### LLM Instruction Prompt
Given an `RDD[ITile[Float]]` named `rasterRDD`, get the first tile. Iterate over every pixel in this tile using its **global grid coordinate boundaries** (`x1`, `y1`, `x2`, `y2`). Inside the loop, use the `isDefined` method with the global `i` and `j` coordinates to count the total number of defined pixels.

### Prompt Snippet
```text
From the RDD[ITile[Float]] rasterRDD, get the first tile. Iterate from its global start coordinates (tile.x1, tile.y1) to its end coordinates (tile.x2, tile.y2). For each pixel (i, j), call tile.isDefined(i, j) to check if it has a value. Count the total number of defined pixels.
```

### Common Failure Modes
- **Compilation Error:** An `RDD[ITile[T]]` contains `ITile` objects directly. Accessing an element as if it were a key-value tuple (e.g., `rdd.first()._1`) will fail to compile.
- **Incorrect Logic:** Calling `isDefined(i, j)` with 0-based indices local to the tile. The method requires **global grid coordinates**. Iterating from `0` to `tile.width` will produce incorrect results or errors if the tile is not at the grid origin.

### Fix Code Hint
The `i` and `j` parameters are global grid coordinates, not local 0-based indices.

**Wrong (local indices):**
```scala
// Fails to check correct pixels unless tile is at grid origin (0,0)
for (j <- 0 until aTile.height; i <- 0 until aTile.width) {
  aTile.isDefined(i, j) // Incorrectly passes local indices
}
```

**Correct (global coordinates):**
```scala
// Correctly iterates using the tile's global coordinate space
for (j <- aTile.y1 to aTile.y2; i <- aTile.x1 to aTile.x2) {
  aTile.isDefined(i, j) // Correctly passes global coordinates
}
```