# VectorLayerBuilder

_The `zigzagDecode` function decodes a value that has been encoded using Zigzag encoding, which is commonly used in data serialization to efficiently represent…_

**Receiver:** instance — obtain a `VectorLayerBuilder` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `zigzagDecode` **(primary)**, ⚠️ `addFeature`

---

## API Test: `zigzagDecode`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def zigzagDecode(x: Int): Int
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:150_

_Source doc:_ Decodes a value from Zigzag encoding

### Goal
The `zigzagDecode` function decodes a value that has been encoded using Zigzag encoding, which is commonly used in data serialization to efficiently represent signed integers.

### Parameters
- `x` (`Int`): The encoded integer value that needs to be decoded from Zigzag encoding.

### Input
The input must be an integer value that has been previously encoded using Zigzag encoding. There are no specific file formats or external data requirements for this function, as it operates solely on the integer input.

### Output
Returns `Int` — the decoded integer value, which represents the original signed integer before it was encoded.

### Valid Call Patterns
```scala
val decodedValue: Int = VectorLayerBuilder.zigzagDecode(encodedValue)
```

### LLM Instruction Prompt
- When calling `zigzagDecode`, ensure that the input is a valid encoded integer. The function will return the decoded integer value.

### Prompt Snippet
```text
To decode a Zigzag encoded integer, use the `zigzagDecode` function with the encoded integer as the argument.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the input is a valid Zigzag encoded integer before calling the function.
val encodedValue: Int = 50 // Example of a Zigzag encoded integer
val decodedValue: Int = VectorLayerBuilder.zigzagDecode(encodedValue)
```

## API Test: `addFeature`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def addFeature(feature: IFeature): IntermediateVectorTile
def addFeature(feature: IFeature): Unit
def addFeature(feature: Row, geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:92  (+2 more definition site/overload)_

### Goal
The `addFeature` function adds a feature with associated geometry to a vector layer, enabling the integration of vector data into raster processing workflows.

### Parameters
- `feature` (`Row`): A Row object representing the attributes of the feature being added, which may include various properties such as identifiers or descriptive tags.
- `geometry` (`LiteGeometry`): A LiteGeometry object that defines the spatial representation of the feature, such as points, lines, or polygons.

### Input
The caller must provide:
- A valid `Row` object containing the feature's attributes.
- A valid `LiteGeometry` object representing the geometry of the feature.
- Ensure that the `Row` and `LiteGeometry` are compatible and correctly formatted for the intended use in the vector layer.

### Output
Returns `Unit` — this indicates that the operation has been completed successfully without returning any value. The state of the vector layer is modified to include the newly added feature.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"), null, Array(10, "pt")))
```

### LLM Instruction Prompt
- When calling `addFeature`, ensure that the `feature` parameter is a properly constructed `Row` object and that the `geometry` parameter is a valid `LiteGeometry` instance. The feature should be relevant to the vector layer being built.

### Prompt Snippet
```text
Add a feature to the vector layer using the addFeature method, ensuring that the feature and geometry are correctly defined.
```

### Common Failure Modes
- **[compile]** error: object LiteShape is not a member of package edu.ucr.cs.bdlab.beast.geolite _(seen 2x)_
- **[compile]** error: object CoordinateXY is not a member of package edu.ucr.cs.bdlab.beast.geolite
- **[compile]** error: object LiteGeometry is not a member of package edu.ucr.cs.bdlab.beast.geolite

### Fix Code Hint
```scala
Ensure that the Row object is correctly populated with the necessary attributes and that the LiteGeometry accurately represents the feature's spatial data before calling addFeature.
```
