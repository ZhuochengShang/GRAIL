## API Test: `addFeature`

### Signature
```scala
def addFeature(feature: IFeature): IntermediateVectorTile
def addFeature(feature: IFeature): Unit
def addFeature(feature: Row, geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:92  (+2 more definition site/overload)_

### Goal
Add one vector feature into the current tile/layer builder so it is encoded in the output vector tile.

### Parameters
- `feature` (`Row`): attribute row to add when using the `(Row, LiteGeometry)` overload; for the `IFeature` overload, the feature object contains geometry + attributes together.
- `geometry` (`LiteGeometry`): geometry paired with the `Row` attributes in the `(Row, LiteGeometry)` overload.

### Input
Caller provides an in-memory feature (or row+geometry pair), not a file path.  
From the authoritative doc: the feature is either added as-is, or rasterized and aggregated, depending on the internal state of the tile.  
Verified usage in tests uses `VectorLayerBuilder` as receiver and `Feature.create(...)` to build an `IFeature`.

### Output
Returns `Unit` — for the shown test-backed call form on `VectorLayerBuilder`, this means the builder is mutated by appending the feature.  
For the documented overload `def addFeature(feature: IFeature): IntermediateVectorTile`, the returned value represents the same tile object to support chaining.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, "pt")))
```

```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, null)))
```

### LLM Instruction Prompt
- Use an instance receiver (for example, `builder.addFeature(...)`), not a bare `addFeature(...)`.
- Pass exactly one `IFeature` for the verified call form, or `(Row, LiteGeometry)` for that overload.
- Do not invent file-based inputs; this API consumes already-created in-memory feature objects.
- Keep geometry and attributes aligned when constructing the feature.

### Prompt Snippet
```text
Create a VectorLayerBuilder, construct an IFeature with Feature.create(...), then call builder.addFeature(feature). Do not use file paths as arguments.
```

### Common Failure Modes
- Calling `addFeature(...)` without a receiver object (won’t resolve).
- Passing the wrong argument shape (e.g., `Row` alone, or geometry alone).
- Assuming a return value when using a `Unit` overload.
- Expecting this call to read shapefiles/GeoJSON directly (it does not; input must already be parsed into feature objects).

### Fix Code Hint
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")

val f: IFeature =
  Feature.create(factory.createPoint(new CoordinateXY(50, 50)),
    Array("id", "name"), null, Array(10, "pt"))

builder.addFeature(f) // mutate builder, then build later
val layer = builder.build()
```