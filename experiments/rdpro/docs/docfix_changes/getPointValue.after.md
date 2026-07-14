## API Test: `getPointValue`
_Grounding: doc-repaired from source (docfix)._

### Goal
Read the pixel value from a raster tile at a given model/world coordinate point (e.g., longitude/latitude).

### Valid Call Patterns
```scala
// REQUIRED IMPORTS:
import org.locationtech.jts.geom.Geometry
import org.locationtech.jts.geom.Point

// Assuming rasterRDD is a loaded RDD of ITile[T]
val tile = rasterRDD.first()

// tile.extents returns a JTS Geometry in world space
val centroid: Point = tile.extents.getCentroid

// getPointValue strictly expects model/world coordinates
val value = tile.getPointValue(centroid.getX, centroid.getY)
```

### LLM Instruction Prompt
- `tile.x1`, `tile.y1`, `tile.x2`, and `tile.y2` are pixel grid indices, not model/world coordinates.
- To obtain valid model/world coordinates from a tile for testing `getPointValue`, use `tile.extents` (which returns a JTS `Geometry` in world space) and extract coordinates from it (e.g., `tile.extents.getCentroid.getX`).
- Passing grid indices to `getPointValue` will cause an `ArrayIndexOutOfBoundsException` because they will be incorrectly transformed by `modelToGrid`.

### Prompt Snippet
```text
Use `tile.extents.getCentroid.getX` and `getY` to get valid world coordinates for `getPointValue(x, y)`. Never pass `tile.x1` or `tile.y1` (grid indices).
```

### Common Failure Modes
- **Passing pixel grid indices (`tile.x1`, `tile.y1`) to `getPointValue`:** Because `getPointValue` internally calls `modelToGrid`, it treats the grid indices as world coordinates and transforms them again. This results in massive out-of-bounds pixel indices and an `ArrayIndexOutOfBoundsException`. `tile.x1` and `tile.x2` represent grid bounds, not world bounds.

### Fix Code Hint
```scala
// WRONG: Passing grid indices causes ArrayIndexOutOfBoundsException via double-transform
val wrongValue = tile.getPointValue(tile.x1, tile.y1)

// CORRECT: Extract world coordinates from tile.extents
val centroid = tile.extents.getCentroid
val correctValue = tile.getPointValue(centroid.getX, centroid.getY)
```