## API Test: `pixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Iterate over all defined (non-empty) pixels in an `ITile`, returning each pixel as its tile coordinates plus its typed pixel value `T`. The type `T` represents the pixel value, which will be a scalar for single-band rasters or an array for multi-band rasters.

### Valid Call Patterns
**Required Imports and Types:**
- requires `edu.ucr.cs.bdlab.beast.geolite.ITile` (Scala trait; reference as `classOf[ITile[_]]` or import directly).

```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Assuming rasterRDD is an RDD[ITile[T]]
val firstTile = rasterRDD.first()
val pxIter = firstTile.pixels
val sample = pxIter.take(10).toArray
require(sample.nonEmpty, "empty result for pixels")
println("__CHECK__ pixels " + sample.length)
```

### LLM Instruction Prompt
- Call as an instance member on a tile value: `tile.pixels`.
- The generic type `T` represents the pixel value, which will be a scalar (e.g., `Float`, `Int`) for single-band rasters, but an array (e.g., `Array[Float]`, `Array[Int]`) for multi-band rasters.
- Callers must not assume `T` is always a scalar type when consuming the iterator; pattern matching or checking the type of `T` is required if the number of bands is unknown.
- Do not add parameters (method has none).

### Prompt Snippet
```text
Given an ITile[T] value named `tile`, iterate its defined pixels using `tile.pixels`. Handle `T` carefully: it may be a scalar (single-band) or an Array (multi-band). Do not assume it is a scalar Float.
```

### Common Failure Modes
- **Assuming `T` is always a scalar:** Attempting to call scalar-specific methods (like `java.lang.Float.isNaN`) directly on `T` without checking its type will cause a `ClassCastException` if the raster is multi-band and `T` is actually an `Array[Float]`.
- Calling `pixels(...)` with arguments (signature has none).

### Fix Code Hint
**WRONG:** Assuming `T` is a scalar Float.
```scala
val it = tile.pixels
it.foreach { case (x, y, v) =>
  // CRASHES with ClassCastException if v is an Array[Float] from a multi-band raster
  if (!v.asInstanceOf[Float].isNaN) { 
    println(v) 
  }
}
```

**CORRECT:** Pattern matching on `T` to handle both scalar and array cases safely.
```scala
val it = tile.pixels
it.foreach { case (x, y, v) =>
  v match {
    case f: Float => 
      // handle single-band scalar
      if (!f.isNaN) println(f)
    case arr: Array[Float] => 
      // handle multi-band array
      if (arr.nonEmpty && !arr(0).isNaN) println(arr.mkString(","))
    case _ => 
      // handle other types (Int, Array[Int], etc.)
  }
}
```