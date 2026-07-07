# GeoJSONScanBuilder

_Finalize the vector layer and return it for further processing or output._

**Receiver:** instance — obtain a `GeoJSONScanBuilder` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `build` **(primary)**

---

## API Test: `build`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def build(): VectorTile.Tile.Layer
override def build(): Scan
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:133  (+4 more definition site/overload)_

_Source doc:_ Finalize the layer and return it @return

### Goal
Finalize the vector layer and return it for further processing or output.

### Parameters
_None._

### Input
The caller must have previously added features to the `VectorLayerBuilder` instance. There are no specific file formats required for this operation, but the features must be valid and properly constructed.

### Output
Returns `VectorTile.Tile.Layer` — this value represents the finalized vector layer containing all added features, ready for use in further geospatial analysis or visualization.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"), null, Array(10, "pt")))
val layer = builder.build()
```

### LLM Instruction Prompt
- Ensure that features are added to the `VectorLayerBuilder` before calling `build`. The features must be valid and should not contain null attributes unless handled appropriately.

### Prompt Snippet
```text
To finalize the vector layer, ensure that all features are added to the builder and then call the `build` method to obtain the finalized layer.
```

### Common Failure Modes
- **[unknown]** two errors found _(seen 4x)_

### Fix Code Hint
```scala
// Ensure features are added before calling build
val layer = builder.build() // This should be called after adding features
```
