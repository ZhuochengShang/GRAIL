## API Test: `addTile`
_Grounding: doc-repaired from source (docfix)._

### Goal
An internal, package-private method to add pixel data from a source `ITile` into a `ConvolutionTile`. This is a low-level component of distributed convolution operations and is not a public API.

### Valid Call Patterns|Valid Access Patterns
This method is `private[raptor]` and is **NOT a public API**. It is for internal library use only and can only be called from code within the `edu.ucr.cs.bdlab.raptor` package. Direct calls from user application code will fail to compile.

The following demonstrates internal usage and requires these types:
- `edu.ucr.cs.bdlab.raptor.ConvolutionTileSingleBand`
- `edu.ucr.cs.bdlab.raptor.MemoryTile`
- `edu.ucr.cs.bdlab.raptor.ITile`
- `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`
- `edu.ucr.cs.bdlab.beast.geolite.RasterFeature`
- `java.awt.geom.AffineTransform`

```scala
// WARNING: The following code will NOT compile unless placed inside the
// `edu.ucr.cs.bdlab.raptor` package. It demonstrates internal usage only.
import edu.ucr.cs.bdlab.raptor.{ConvolutionTileSingleBand, ITile, MemoryTile}
import edu.ucr.cs.bdlab.beast.geolite.{RasterFeature, RasterMetadata}
import java.awt.geom.AffineTransform

val metadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326, new AffineTransform())
val sourceTile: ITile[Float] = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))

val weights = Array.fill[Float](9)(1.0f / 9.0f)
val convTile = new ConvolutionTileSingleBand(0, metadata, sourceTile.rasterFeature, 1, weights, sourceTile.tileID)

// This call is only valid within the `raptor` package.
convTile.addTile(sourceTile)
```

### LLM Instruction Prompt
Do not call the `addTile` method on `AbstractConvolutionTile` or its subclasses. It is `private[raptor]`, meaning it is restricted to internal library use and is not part of the public API. Direct calls from application code will cause a compilation failure. Do not construct `ConvolutionTile` instances directly; they are low-level components managed by higher-level distributed operations.

### Prompt Snippet
`addTile` is a `private[raptor]` method for internal use. Do not call it.

### Common Failure Modes
Compilation error due to visibility restrictions. The method is `private[raptor]` and cannot be accessed from outside the `edu.ucr.cs.bdlab.raptor` package. The error will be similar to: `method addTile in class AbstractConvolutionTile cannot be accessed in ...`

### Fix Code Hint
Do not call this method directly. Use a public, higher-level API for the desired operation.

```scala
// WRONG: Direct call from application code
val convTile = new ConvolutionTileSingleBand(...)
convTile.addTile(sourceTile) // COMPILE ERROR: method addTile ... cannot be accessed

// CORRECT: Do not call the method. Use a public API instead.
// (e.g., a high-level distributed convolution function if available)
```