## API Test: `mapPixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Apply a user-defined function for each pixel in the input raster to produce an output raster with transformed pixel values.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS & TYPES:
// requires `edu.ucr.cs.bdlab.raptor.RasterOperationsLocal` — a Scala object; reference as `RasterOperationsLocal.mapPixels(...)`
// requires `edu.ucr.cs.bdlab.beast.geolite.ITile` — a Scala trait/class; reference as `ITile[T]`
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Apply per-pixel transformation
val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)

// Verify output
val n = mapped.count()
require(n > 0, "empty result for mapPixels")

// Extract a sample tile (RasterRDD[T] contains ITile[T], not raw pixels)
val sampleTile: ITile[Float] = mapped.take(1).head
println("__CHECK__ mapPixels " + s"count=$n sampleTile=$sampleTile")
```

### LLM Instruction Prompt
- `RasterRDD[T]` is an RDD of tiles (`ITile[T]`), not an RDD of individual pixels.
- Calling `.take(1).head` on a `RasterRDD[T]` returns an `ITile[T]`, not a raw pixel value like `Float` or `Int`.
- Do not attempt to call scalar methods (like `.isFinite` or arithmetic operations) directly on the elements of a `RasterRDD`.
- Use `RasterOperationsLocal.mapPixels(inputRaster, f)` to apply a function `T => U` to each pixel.

### Prompt Snippet
```text
RasterRDD[T] is an RDD of ITile[T], not individual pixels. Calling .take(1).head returns an ITile[T]. Do not call scalar methods (like .isFinite) on the elements of a RasterRDD. Use RasterOperationsLocal.mapPixels(raster, (x: T) => U) to transform pixel values.
```

### Common Failure Modes
- **Misunderstanding `RasterRDD[T]` semantics:** Assuming `RasterRDD[Float]` is an RDD of individual `Float` pixels, meaning `mapped.take(1).head` would return a `Float` on which `.isFinite` could be called. However, `RasterRDD[T]` is an RDD of tiles (`ITile[T]`), so `take(1).head` returns an `ITile[Float]`, which does not have an `isFinite` method.
- **Type mismatch on load:** Loading a raster with the wrong type parameter (e.g., `sc.geoTiff[Int]` when the data is `Float`), causing the `mapPixels` lambda type to fail against the actual pixels.

### Fix Code Hint
```scala
// WRONG: Treating RasterRDD elements as scalar pixels
val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)
val firstPixel = mapped.take(1).head
val isGood = firstPixel.isFinite // FAILS: firstPixel is an ITile[Float], not a Float

// CORRECT: Recognizing RasterRDD elements are ITile[T]
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal
import edu.ucr.cs.bdlab.beast.geolite.ITile

val mapped = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 1.8f + 32.0f)
val n = mapped.count()
require(n > 0, "empty result for mapPixels")
val sampleTile: ITile[Float] = mapped.take(1).head
println("__CHECK__ mapPixels " + s"count=$n sampleTile=$sampleTile")
```