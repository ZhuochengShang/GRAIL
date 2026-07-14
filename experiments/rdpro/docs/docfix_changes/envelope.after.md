## API Test: `envelope`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retrieve the spatial boundaries (extent) of raster data in model space as a JTS `Envelope`.

### Valid Call Patterns|Valid Access Patterns
```scala
// REQUIRED IMPORTS:
// import org.locationtech.jts.geom.Envelope (Java class)
// import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata (Scala class)

// RasterRDD[T] is an RDD[ITile[T]]. Extract a tile first to get RasterMetadata.
val metadata: RasterMetadata = rasterRDD.first().rasterMetadata
val bounds: Envelope = metadata.envelope

// Access dimensions using Java getters (getWidth, getHeight)
val witness = bounds.getWidth * bounds.getHeight
require(witness > 0, s"degenerate envelope: $bounds")
println("__CHECK__ envelope " + witness)
```

### LLM Instruction Prompt
- `RasterRDD` is an `RDD[ITile[T]]`. Do not attempt to call `.rasterFeature` or `.envelope` directly on the RDD.
- To access `RasterMetadata` from a `RasterRDD`, you must extract a tile first (e.g., `rasterRDD.first().rasterMetadata`).
- The `envelope` method on `RasterMetadata` returns an `org.locationtech.jts.geom.Envelope`.
- Because the returned `Envelope` is a JTS Java object, you must use `.getWidth` and `.getHeight` to access its dimensions, not `.width` and `.height`.

### Prompt Snippet
```text
To get the envelope of a RasterRDD, extract a tile first: `rasterRDD.first().rasterMetadata.envelope`. The result is a JTS `Envelope`. Because it is a Java object, you must use `.getWidth` and `.getHeight` (not `.width` or `.height`).
```

### Common Failure Modes
- **Calling `.rasterFeature` or `.envelope` directly on a `RasterRDD`:** Fails because `RasterRDD[T]` is a type alias for `RDD[ITile[T]]`. You must extract a tile (e.g., `.first()`) to access `.rasterMetadata`.
- **Using Scala-style property accessors on the envelope:** Fails with a compilation error when calling `.width` or `.height` on the returned bounds. The returned object is a JTS `Envelope` (Java), requiring `.getWidth` and `.getHeight`.

### Fix Code Hint
```scala
// WRONG: Assuming RDD has rasterFeature/envelope, and using Scala accessors
val bounds = rasterRDD.rasterFeature.envelope
val area = bounds.width * bounds.height

// CORRECT: Extract tile metadata first, use Java getters on JTS Envelope
val metadata = rasterRDD.first().rasterMetadata
val bounds = metadata.envelope
val area = bounds.getWidth * bounds.getHeight
```