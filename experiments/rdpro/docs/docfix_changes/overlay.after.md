## API Test: `overlay`
_Grounding: doc-repaired from source (docfix)._

### Goal
Stack this raster with one or more other rasters so each defined pixel carries values from all overlaid inputs, returning an RDD of tiles containing arrays of the stacked values.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS:
// requires edu.ucr.cs.bdlab.beast.geolite.ITile (a JAVA class)
// requires org.apache.spark.rdd.RDD (a Scala class)
import edu.ucr.cs.bdlab.beast.geolite.ITile
import org.apache.spark.rdd.RDD

// 1. Load compatible rasters
val raster1 = sc.geoTiff[Float]("raster1.tif")
val raster2 = sc.geoTiff[Float]("raster2.tif")

// 2. Call overlay with EXPLICIT type parameter [V]
val stacked: RDD[ITile[Array[Float]]] = raster1.overlay[Float](raster2)

// 3. Accessing the underlying ITile elements safely
val sample = stacked.take(1)
require(sample.nonEmpty, "empty result for overlay")
val tile: ITile[Array[Float]] = sample.head
require(tile != null, "overlay produced null tile")
```

### LLM Instruction Prompt
- The `overlay` method requires the output array type parameter `V` to be explicitly specified (e.g., `raster.overlay[Float](otherRaster)`) or ascribed to the result, as it cannot be inferred from the arguments.
- The returned `RasterRDD[Array[V]]` is an alias for `RDD[ITile[Array[V]]]`, meaning the elements of the RDD are `ITile` objects containing arrays, not raw Scala arrays. 
- Do not call Scala array methods (like `nonEmpty` or `count`) directly on the elements of the returned RDD.
- Only pass raster inputs of compatible metadata (resolution/CRS/tile size); otherwise reshape/reproject first.

### Prompt Snippet
```text
When calling `overlay`, you MUST explicitly provide the output type parameter `V` (e.g., `raster1.overlay[Float](raster2)`). The return type `RasterRDD[Array[V]]` is an alias for `RDD[ITile[Array[V]]]`. The elements are `ITile` objects, not raw arrays, so do not call array methods directly on the elements.
```

### Common Failure Modes
- **Type Inference Failure (`Nothing`):** Omitting the type parameter `V` in `overlay[V]` causes it to default to `Nothing` (e.g., `RasterRDD[Array[Nothing]]`), leading to compilation errors because `V` only appears in the return type.
- **Method Not Found on ITile:** Attempting to call Scala Array methods (like `nonEmpty` or `count`) directly on the elements of the returned RDD. The elements are `ITile` objects, not raw arrays.
- **Metadata Mismatch:** Passing inputs with different CRS, resolution, or tile sizes without reshaping/reprojecting first.

### Fix Code Hint
```scala
// WRONG: Type parameter omitted, and treating ITile as an Array
val stacked = raster1.overlay(raster2)
val firstElement = stacked.first()
val hasData = firstElement.nonEmpty // Fails: ITile has no nonEmpty method

// CORRECT: Explicit type parameter provided, treating elements as ITile
val stacked = raster1.overlay[Float](raster2)
val sample = stacked.take(1)
require(sample.nonEmpty, "empty result for overlay")
val tile = sample.head // tile is of type ITile[Array[Float]]
require(tile != null, "overlay produced null tile")
```