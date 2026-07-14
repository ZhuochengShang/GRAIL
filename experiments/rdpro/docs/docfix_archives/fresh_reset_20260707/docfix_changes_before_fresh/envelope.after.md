## API Test: `envelope`
_Grounding: doc-repaired from source (docfix)._

### Goal
Get raster bounds in model/world space from a `RasterMetadata` instance.

### Valid Call Patterns|Valid Access Patterns
`envelope` in this API target is **only**:
```scala
def envelope: org.locationtech.jts.geom.Envelope
```
on receiver type:
`edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`.

Compilable usage sketch:
```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import org.locationtech.jts.geom.Envelope

val metadata: RasterMetadata = /* obtain from your raster object/pipeline */
val bounds: Envelope = metadata.envelope

val witness = (bounds.getWidth * bounds.getHeight).toLong
require(witness > 0, s"degenerate envelope: $bounds")
println("__CHECK__ envelope " + witness)
```

### LLM Instruction Prompt
- Call as zero-arg instance member on `RasterMetadata`: `metadata.envelope`.
- Do **not** call on `RasterRDD` directly unless you already extracted a `RasterMetadata`.
- Return type for this target is JTS `Envelope` (`org.locationtech.jts.geom.Envelope`), not `java.awt.Rectangle`.
- Use JTS accessors (`getWidth`, `getHeight`, `getMinX`, `getMaxX`, `getMinY`, `getMaxY`).

### Prompt Snippet
```text
Given `metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`,
use:
  val bounds: org.locationtech.jts.geom.Envelope = metadata.envelope
Then read bounds with JTS methods like getWidth/getHeight.
```

### Common Failure Modes
- Using nonexistent path `rasterRDD.rasterFeature.rasterMetadata` before calling `envelope`.
- Treating `envelope` here as returning `java.awt.Rectangle`; this target returns `org.locationtech.jts.geom.Envelope`.
- Calling `envelope` with arguments (it takes none).

### Fix Code Hint
```scala
// Wrong (nonexistent access path + wrong assumption source):
val b = rasterRDD.rasterFeature.rasterMetadata.envelope

// Correct (obtain RasterMetadata first, then call envelope):
val metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata = /* from your pipeline */
val b: org.locationtech.jts.geom.Envelope = metadata.envelope
```