# SpatialParquetHelper

_Encodes a geometric shape into a feature representation for further processing in geospatial analysis._

**Receiver:** static object — call `SpatialParquetHelper.<method>(...)`

**Members** (most robust first): ⚠️ `encodeGeometry` **(primary)**

---

## API Test: `encodeGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
private def encodeGeometry(geometry: Geometry, featureBuilder: Feature.Builder): Unit
private def encodeGeometry(geometry: LiteGeometry, featureBuilder: Feature.Builder): Unit
def encodeGeometry(geometry: Geometry): Seq[InternalRow]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:194  (+2 more definition site/overload)_

_Source doc:_ Encodes a geometry into the given feature @param geometry the geometry to encode @param featureBuilder the feature builder to encode to

### Goal
Encodes a geometric shape into a feature representation for further processing in geospatial analysis.

### Parameters
- `geometry` (`Geometry`): The geometric shape to be encoded, which can include points, lines, or polygons.
- `featureBuilder` (`Feature.Builder`): A builder object used to construct the feature representation of the geometry.

### Input
The caller must provide a valid `Geometry` object representing the shape to be encoded and a `Feature.Builder` instance to facilitate the encoding process.

### Output
Returns `Unit` — this indicates that the encoding process has been completed without returning a value. In the case of the overloaded method, it returns a `Seq[InternalRow]`, which represents the encoded geometry in a structured format suitable for further processing.

### Valid Call Patterns
```scala
val point = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val featureBuilder = new Feature.Builder()
SpatialParquetHelper.encodeGeometry(point, featureBuilder)
```

### LLM Instruction Prompt
- Ensure that the `geometry` provided is a valid instance of `Geometry` or `LiteGeometry`.
- Use a properly initialized `Feature.Builder` to avoid runtime errors during encoding.

### Prompt Snippet
```text
To encode a geometry, create a valid Geometry object and a Feature.Builder, then call encodeGeometry.
```

### Common Failure Modes
- **[compile]** error: value encodeGeometry in object VectorLayerBuilder cannot be accessed in object edu.ucr.cs.bdlab.davinci.VectorLayerBuilder _(seen 3x)_
- **[compile]** error: object LiteFeature is not a member of package edu.ucr.cs.bdlab.beast.geolite

### Fix Code Hint
```scala
val point = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val featureBuilder = new Feature.Builder() // Ensure this is initialized
SpatialParquetHelper.encodeGeometry(point, featureBuilder)
```
