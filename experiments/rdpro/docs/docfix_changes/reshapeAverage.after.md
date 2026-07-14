## API Test: `reshapeAverage`
_Grounding: doc-repaired from source (docfix)._

### Goal
Reshape a continuous-value raster to new metadata (CRS/grid/resolution/extent) using average resampling. Overlapping source pixels are averaged into each output pixel.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal` (Scala object; reference directly)
- `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala class; reference as `classOf[RasterMetadata]` or instantiate directly)

**Correct Call Sketch:**
```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

val reshaped = RasterOperationsFocal.reshapeAverage(
  rasterRDD,
  meta => new RasterMetadata(
    meta.x1, meta.y1, meta.x2, meta.y2,
    meta.tileWidth, meta.tileHeight,
    meta.srid, meta.g2m
  )
)

val n = reshaped.count()
require(n > 0, "empty result for reshapeAverage")
```

### LLM Instruction Prompt
- `RasterRDD` is an RDD; do not attempt to access `.rasterFeature` or `.rasterMetadata` directly on it.
- Do not pre-compute target metadata outside the function call. The `targetMetadataConv` parameter is a function `RasterMetadata => RasterMetadata`. You must use this lambda to derive and return the new `RasterMetadata` dynamically.
- `RasterRDD[T]` elements are tile objects, not tuples. Do not attempt to access `._2` on them when sampling the result.
- Use only for continuous-value rasters (e.g., temperature, vegetation). For categorical labels, use `reshapeNN`.

### Prompt Snippet
```text
Use RasterOperationsFocal.reshapeAverage(rasterRDD, meta => new RasterMetadata(...)) to reshape continuous rasters. Do not access .rasterMetadata on the RasterRDD itself. Transform metadata inside the lambda. RasterRDD elements are tiles, not tuples (no ._2).
```

### Common Failure Modes
- **Attempting to access `.rasterFeature.rasterMetadata` directly on a `RasterRDD`** to pre-compute target metadata. `RasterRDD` is an RDD and lacks this property.
- **Pre-computing `targetMetadata` outside the function** using an undefined `sourceMetadata` variable, rather than transforming it inside the `RasterMetadata => RasterMetadata` lambda.
- **Attempting to access `._2` on `RasterRDD[T]` elements** when sampling. Elements are tile objects, not tuples.
- **Using `reshapeAverage` on categorical data** (land-cover classes), which causes invalid mixed class values.

### Fix Code Hint
**WRONG:**
```scala
// Fails: RasterRDD has no .rasterMetadata property, and pre-computing outside is invalid
val sourceMetadata = rasterRDD.rasterMetadata 
val targetMetadata = sourceMetadata.rescale(10, 10)
val outputRaster = RasterOperationsFocal.reshapeAverage(rasterRDD, _ => targetMetadata)

// Fails: RasterRDD elements are tiles, not tuples
val sample = outputRaster.first()._2
```

**CORRECT:**
```scala
// Transform metadata dynamically inside the lambda
val outputRaster = edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.reshapeAverage(
  rasterRDD,
  meta => new edu.ucr.cs.bdlab.beast.geolite.RasterMetadata(
    meta.x1, meta.y1, meta.x2, meta.y2,
    meta.tileWidth, meta.tileHeight,
    meta.srid, meta.g2m
  )
)

// RasterRDD elements are tile objects directly
val sampleTile = outputRaster.first()
```