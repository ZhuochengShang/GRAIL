## API Test: `addFeature`
_Grounding: doc-repaired from source (docfix)._

### Goal
Add a vector feature to an `IntermediateVectorTile`. The feature is either added as-is or rasterized and aggregated depending on the tile's internal state. The method mutates the tile in place and returns the tile itself for chaining.

### Valid Call Patterns
Requires the following Scala imports/types:
- `edu.ucr.cs.bdlab.davinci.IntermediateVectorTile`
- `edu.ucr.cs.bdlab.beast.geolite.IFeature`

```scala
import edu.ucr.cs.bdlab.davinci.IntermediateVectorTile
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// Instantiate with resolution (Int) and buffer (Int)
val tile = new IntermediateVectorTile(256, 10)

// Assuming `f` is an existing IFeature (e.g., from featuresRDD.first())
tile.addFeature(f) // Mutates tile in place and returns `this`
```

### LLM Instruction Prompt
- `addFeature` is an instance method on `IntermediateVectorTile`, not `VectorLayerBuilder`.
- `IntermediateVectorTile` is instantiated directly with `resolution` (Int) and `buffer` (Int) parameters.
- The method mutates the tile in place and returns the tile itself for chaining.
- There is no `.build()` method; the tile is ready immediately after mutation.
- The caller must import `edu.ucr.cs.bdlab.davinci.IntermediateVectorTile` and `edu.ucr.cs.bdlab.beast.geolite.IFeature`.
- Do not invent file-based inputs; this API consumes an already-created in-memory `IFeature`.

### Prompt Snippet
```text
Instantiate an IntermediateVectorTile(resolution, buffer). Call tile.addFeature(feature) passing an IFeature. Do not use VectorLayerBuilder and do not call .build().
```

### Common Failure Modes
- **Fabricated Builder/Build Step:** Attempting to call `addFeature` on a `VectorLayerBuilder` and subsequently calling a fabricated `.build()` method. `addFeature` belongs to `IntermediateVectorTile`, which mutates its own state and requires no build step.
- **Missing Imports:** Failing to import `edu.ucr.cs.bdlab.davinci.IntermediateVectorTile`.
- **Wrong Arguments:** Passing file paths instead of an in-memory `IFeature` object.

### Fix Code Hint
```scala
// WRONG: Using non-existent VectorLayerBuilder and fabricated .build()
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(f)
val layer = builder.build()

// CORRECT: Using IntermediateVectorTile directly with resolution and buffer
import edu.ucr.cs.bdlab.davinci.IntermediateVectorTile
import edu.ucr.cs.bdlab.beast.geolite.IFeature

val tile = new IntermediateVectorTile(256, 10)
tile.addFeature(f) // Mutates in place, returns `tile` for chaining
```