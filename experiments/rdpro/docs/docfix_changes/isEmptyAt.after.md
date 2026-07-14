## API Test: `isEmptyAt`
_Grounding: doc-repaired from source (docfix)._

### Goal
Check whether the raster pixel covering a given map location `(x, y)` (model coordinates, e.g., longitude/latitude) is no-data/empty in an RDPro/Beast `ITile`.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.beast.geolite.ITile` (Scala trait, returned directly by `rasterRDD.first()`)
- `org.locationtech.jts.geom.Geometry` (Java class, returned by `tile.extents`)

```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile
import org.locationtech.jts.geom.Geometry

// rasterRDD.first() returns an ITile directly, not a wrapper
val tile: ITile = rasterRDD.first()

// Obtain valid model coordinates from the tile's extents geometry
val centroid = tile.extents.getCentroid

// isEmptyAt expects model coordinates (e.g., lon/lat), not pixel grid coordinates
val isNoData: Boolean = tile.isEmptyAt(centroid.getX, centroid.getY)

val witness = if (isNoData) 1 else 0
println("__CHECK__ isEmptyAt " + witness)
```

### LLM Instruction Prompt
- `rasterRDD.first()` returns an `ITile` directly. Do not attempt to access a `.raster` field on the returned object.
- `isEmptyAt(x, y)` expects model coordinates (e.g., longitude/latitude in the CRS), not pixel grid coordinates (like `x1` or `y1`).
- Valid model coordinates can be obtained from the tile's `extents` geometry (e.g., `tile.extents.getCentroid.getX`).

### Prompt Snippet
```text
Given a raster RDD, extract the first tile directly via `rasterRDD.first()`. Do not look for a `.raster` field. Get model coordinates from `tile.extents.getCentroid` and pass `centroid.getX` and `centroid.getY` to `tile.isEmptyAt(x, y)`.
```

### Common Failure Modes
- **Misreading RDD element type:** Assuming `rasterRDD.first()` returns a wrapper object and attempting to access a non-existent `.raster` field. It returns an `ITile` directly.
- **Coordinate space mismatch:** Passing pixel grid coordinates (like `tile.x1`, `tile.x2`) to `isEmptyAt` instead of model coordinates (longitude/latitude).

### Fix Code Hint
**Wrong:**
```scala
val tile = rasterRDD.first().raster // ERROR: no .raster field, first() is already an ITile
val isNoData = tile.isEmptyAt(tile.x1, tile.y1) // ERROR: uses pixel grid coordinates instead of model coordinates
```

**Correct:**
```scala
val tile: ITile = rasterRDD.first() 
val centroid = tile.extents.getCentroid
val isNoData: Boolean = tile.isEmptyAt(centroid.getX, centroid.getY) 
```