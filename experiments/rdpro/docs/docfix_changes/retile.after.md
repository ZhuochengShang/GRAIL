## API Test: `retile`
_Grounding: doc-repaired from source (docfix)._

### Goal
Generate a new `RasterMetadata` with updated tile dimensions by calling `retile` on an existing `RasterMetadata` instance extracted from a `RasterRDD`.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` — a Scala class.

```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// 1. Extract metadata from the first tile of the RasterRDD
val metadata: RasterMetadata = rasterRDD.first().rasterMetadata

// 2. Call retile on the RasterMetadata instance
val retiledMetadata: RasterMetadata = metadata.retile(64, 64)
```

### LLM Instruction Prompt
- `retile` MUST be called as an instance method on `RasterMetadata`, never directly on a `RasterRDD`.
- Obtain a `RasterMetadata` instance from a `RasterRDD` by accessing the metadata of its first tile (e.g., `rasterRDD.first().rasterMetadata`).
- You must explicitly import `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`.

### Prompt Snippet
```text
Extract the RasterMetadata from the RasterRDD using `rasterRDD.first().rasterMetadata`, then call `.retile(tileWidth, tileHeight)` on that metadata object. Do not call retile directly on the RasterRDD. Ensure you import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata.
```

### Common Failure Modes
- **Spark SQL Serialization Error (`Unrecognized value [F` for `Array[Float]`)**: This occurs if you call `retile` directly on a `RasterRDD` containing float pixels. Because `ITile` extends `Row`, Catalyst cannot natively encode raw float arrays during shuffle/evaluation. Always extract the `RasterMetadata` first and call `retile` on the metadata object instead.

### Fix Code Hint
```scala
// WRONG: Calling retile directly on RasterRDD causes Spark SQL serialization error (Unrecognized value [F)
val retiled = rasterRDD.retile(64, 64)

// CORRECT: Extract RasterMetadata first, then call retile on it
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

val metadata = rasterRDD.first().rasterMetadata
val retiledMetadata = metadata.retile(64, 64)
```