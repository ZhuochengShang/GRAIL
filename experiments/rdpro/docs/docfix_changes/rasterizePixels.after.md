## API Test: `rasterizePixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create a distributed raster (`RasterRDD[T]`) from explicit pixel coordinates and values, using a newly constructed `RasterMetadata` and `RasterFeature`.

### Valid Call Patterns
**Required Imports & Types:**
- `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala class)
- `edu.ucr.cs.bdlab.beast.geolite.RasterFeature` (Scala class)
- `edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal` (Scala object)
- `java.awt.geom.AffineTransform` (Java class)

```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.beast.geolite.RasterFeature
import edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal
import java.awt.geom.AffineTransform

val pixels = sc.parallelize(Seq(
  (0, 0, 1.0f),
  (1, 0, 2.0f),
  (0, 1, 3.0f),
  (1, 1, 4.0f)
))

// Construct new metadata and feature instances. 
// Do NOT attempt to extract these from an existing RasterRDD.
val metadata = new RasterMetadata(0, 0, 100, 95, 30, 30, 4326, new AffineTransform())
val rf = RasterFeature.create(Array("fileName"), Array("testFile.tif"))

val out = RasterOperationsGlobal.rasterizePixels(pixels, metadata, rf)

val n = out.count()
val sample = out.first()
val v = sample.getPixelValueAsFloat(0, 0)
require(n > 0, s"empty result for rasterizePixels: count=$n")
require(!java.lang.Float.isNaN(v) && !java.lang.Float.isInfinite(v), s"non-finite sample pixel value: $v")
println("__CHECK__ rasterizePixels " + s"count=$n,sample00=$v")
```

### LLM Instruction Prompt
- `RasterRDD` is an RDD (`RDD[ITile[T]]`) and does NOT have a `.rasterFeature` or `.rasterMetadata` field directly on it.
- You must construct a new `RasterMetadata` using `new RasterMetadata(...)`.
- When constructing `RasterMetadata`, the `AffineTransform` parameter requires `java.awt.geom.AffineTransform`.
- Do not attempt to extract metadata from an existing `RasterRDD` via non-existent properties like `rasterRDD.rasterFeature`.
- Use the exact 3-argument form: `RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)`.

### Prompt Snippet
```text
Construct new RasterMetadata(...) (using java.awt.geom.AffineTransform) and RasterFeature.create(...). Pass them along with an RDD[(Int, Int, T)] to RasterOperationsGlobal.rasterizePixels. Never call .rasterFeature or .rasterMetadata on a RasterRDD.
```

### Common Failure Modes
- **Hallucinating properties on RasterRDD:** Attempting to access `rasterRDD.rasterFeature` or `rasterRDD.rasterMetadata`. `RasterRDD` is an alias for `RDD[ITile[T]]` and lacks these fields. You must instantiate them manually.
- **Missing Java Import:** Failing to import `java.awt.geom.AffineTransform` when instantiating `RasterMetadata`.
- **Invalid Tuple Shape:** Passing an RDD of anything other than `(Int, Int, T)` to the `pixels` argument.

### Fix Code Hint
```scala
// WRONG: Hallucinating properties on an existing RasterRDD
val metadata = existingRaster.rasterMetadata // Fails: value rasterMetadata is not a member of RasterRDD
val rf = existingRaster.rasterFeature        // Fails: value rasterFeature is not a member of RasterRDD
val out = RasterOperationsGlobal.rasterizePixels(pixels, metadata, rf)

// CORRECT: Construct new instances explicitly with required imports
import edu.ucr.cs.bdlab.beast.geolite.{RasterMetadata, RasterFeature}
import edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal
import java.awt.geom.AffineTransform

val metadata = new RasterMetadata(0, 0, 100, 95, 30, 30, 4326, new AffineTransform())
val rf = RasterFeature.create(Array("fileName"), Array("testFile.tif"))
val out = RasterOperationsGlobal.rasterizePixels(pixels, metadata, rf)
```