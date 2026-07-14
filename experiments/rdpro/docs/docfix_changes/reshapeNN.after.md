## API Test: `reshapeNN`
_Grounding: doc-repaired from source (docfix)._

### Goal
Reshape a distributed raster to new target metadata (CRS/grid/resolution/extent/tiling) using nearest-neighbor pixel assignment.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala) and `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal` (Scala).

```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal

// T must exactly match the underlying pixel data type, typically an array type (e.g., Array[Float])
val reshaped = RasterOperationsFocal.reshapeNN[Array[Float]](
  rasterRDD,
  (m: RasterMetadata) => m // Replace with actual RasterMetadata => RasterMetadata conversion
)
```

### LLM Instruction Prompt
- The type parameter `T` in `RasterRDD[T]` and `reshapeNN[T]` must exactly match the underlying pixel data type of the raster. For multi-band or standard RDPro rasters, this is typically an array type (e.g., `Array[Float]` or `Array[Int]`), NOT a scalar primitive.
- Pass a `RasterRDD[T]` as the first argument and a metadata conversion function (`RasterMetadata => RasterMetadata`) as the second argument.
- Use `reshapeNN` for categorical/general nearest-neighbor reshaping; do not switch to averaging semantics.
- Do not invent extra parameters or alternate signatures.

### Prompt Snippet
```text
Given a RasterRDD[T], call RasterOperationsFocal.reshapeNN[T](raster, targetMetadataConv, numPartitions).
CRITICAL: T must be an array type (e.g., Array[Float]) matching the raster's actual pixel type, not a scalar primitive.
If numPartitions is omitted, output partitions default to input partition count.
```

### Common Failure Modes
- **Type mismatch (`Unrecognized value [F...`):** If the runtime encounters an error like `Unrecognized value [F@... of type class [F`, it means the raster contains `Array[Float]` but was incorrectly typed as a scalar `Float`. `[F` is the JVM signature for `float[]`.
- Passing a non-conversion second argument shape (must be a function `RasterMetadata => RasterMetadata`).
- Expecting interpolation/averaging behavior from `reshapeNN` (it is nearest neighbor only).
- Assuming out-of-range or empty source pixels will be filled; they remain empty in the output.

### Fix Code Hint
```scala
// WRONG: Typing as a scalar primitive (causes "Unrecognized value [F..." ClassCastException)
val reshaped = RasterOperationsFocal.reshapeNN[Float](
  rasterRDD,
  m => m
)

// CORRECT: Typing as an array of primitives matching the underlying raster data
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal

val reshaped = RasterOperationsFocal.reshapeNN[Array[Float]](
  rasterRDD,
  m => m // Example identity conversion; replace with actual metadata logic
)
```