# IFeature

_Retrieve the geometric representation of a feature, which is essential for spatial analysis in geospatial raster processing._

**Receiver:** instance — obtain a `IFeature` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `getGeometry` **(primary)**, ★ `getStorageSize`, ⚠️ `getAttributeName`, ⚠️ `getName`

---

## API Test: `getGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getGeometry: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:69_

_Source doc:_ The geometry contained in the feature. @return the geometry in this attribute

### Goal
Retrieve the geometric representation of a feature, which is essential for spatial analysis in geospatial raster processing.

### Parameters
_None._

### Input
The caller must provide an instance of `IFeature` that contains a valid geometry. The geometry must be properly initialized and conform to the expected format for spatial operations.

### Output
Returns `Geometry` — the geometric representation of the feature, which can be used for spatial analysis and operations within the RDPro framework.

### Valid Call Patterns
```scala
val geometry: Geometry = feature.getGeometry
```

### LLM Instruction Prompt
- Ensure that the `IFeature` instance is properly initialized and contains a valid geometry before calling `getGeometry`.

### Prompt Snippet
```text
Retrieve the geometry from the feature using the getGeometry method.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
if (feature != null) {
  val geometry: Geometry = feature.getGeometry
} else {
  // Handle the null feature case appropriately
}
```

## API Test: `getStorageSize`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getStorageSize: Int
def getStorageSize(value: Any, dataType: DataType): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:112  (+1 more definition site/overload)_

### Goal
Calculates the storage size of a given value based on its data type, which is useful for understanding memory usage in geospatial raster processing.

### Parameters
- `value` (`Any`): The input value whose storage size is to be calculated. This can be any object, including raster data or geometries.
- `dataType` (`DataType`): The type of the input value, which helps determine how to calculate the storage size. This should correspond to the actual type of the `value`.

### Input
The caller must provide a valid `value` of any type and a corresponding `dataType` that accurately reflects the type of the `value`. Ensure that the `dataType` is compatible with the `value` to avoid incorrect size calculations.

### Output
Returns `Int` — the storage size in bytes of the provided `value`, which indicates how much memory the value occupies.

### Valid Call Patterns
```scala
val feature = Feature.create(Row.apply(123.25, "name", new PointND(GeometryReader.DefaultGeometryFactory, 2, 0.0, 1.0), "name2", null), null)
val size = feature.getStorageSize

val featureWithMap = Feature.create(new PointND(GeometryReader.DefaultGeometryFactory, 2, 0.0, 1.0), Array("id", "name", "tags"), null, Array(33, "test", Map()))
val sizeWithMap = featureWithMap.getStorageSize
```

### LLM Instruction Prompt
- When calling `getStorageSize`, ensure that the `value` and `dataType` parameters are correctly specified and compatible with each other.

### Prompt Snippet
```text
To calculate the storage size of a feature, use the `getStorageSize` method with the appropriate value and data type.
```

### Common Failure Modes
- **[compile]** error: value getGeometryType is not a member of org.locationtech.jts.geom.GeometryFactory
- **[compile]** error: type mismatch;
- **[compile]** error: overloaded method constructor Point with alternatives:

### Fix Code Hint
```scala
// Ensure that the value and dataType are compatible before calling getStorageSize
val size = feature.getStorageSize(value, dataType) // Check that dataType matches the type of value
```

## API Test: `getAttributeName`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getAttributeName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:92_

_Source doc:_ If names are associated with attributes, this function returns the name of the attribute at the given position (0-based). @param i the index of the attribute to return its name @return the name of the given attribute index or `null` if it does not exist

### Goal
The `getAttributeName` function retrieves the name of an attribute associated with a feature at a specified index, facilitating access to attribute metadata in geospatial analyses.

### Parameters
- `i` (`Int`): The 0-based index of the attribute whose name is to be returned. Valid values are non-negative integers corresponding to the position of attributes in the feature.

### Input
The caller must provide a feature object that contains attributes. The attributes should be properly defined and associated with the feature. The index `i` must be within the bounds of the available attributes.

### Output
Returns `String` — the name of the attribute at the specified index. If the index does not correspond to an existing attribute, it returns `null`.

### Valid Call Patterns
```scala
val inputPath = makeFileCopy("/test.partitions")
val data = sparkContext.readWKTFile(inputPath.getPath, "Geometry", '\t', true)
val feature = data.first()
assert(feature.getAttributeName(0) == "ID")
assert(feature.getAttributeName(1) == "File Name")
```

### LLM Instruction Prompt
- When calling `getAttributeName`, ensure that the index provided is valid and corresponds to an existing attribute in the feature. Handle the possibility of receiving `null` if the index is out of bounds.

### Prompt Snippet
```text
Retrieve the name of the attribute at the specified index using `getAttributeName(i)`, ensuring that `i` is a valid index for the feature's attributes.
```

### Common Failure Modes
- **[compile]** error: value readGeoJSONFile is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the index is within the valid range before calling getAttributeName
if (i >= 0 && i < feature.getAttributeCount) {
    val attributeName = feature.getAttributeName(i)
} else {
    // Handle the case where the index is invalid
}
```

## API Test: `getName`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:83_

_Source doc:_ Return the name of the given attribute. @param i the index of the attribute in the range [0, length[ @return the type of the attribute or null if unknown

### Goal
Retrieve the name of a specified attribute from a feature, which is useful in geospatial analysis for understanding the data structure.

### Parameters
- `i` (`Int`): The index of the attribute whose name is to be retrieved. It must be within the range [0, length[ of the attributes available in the feature.

### Input
The caller must provide a valid index `i` that corresponds to an existing attribute in the feature. The feature must be properly initialized and contain attributes.

### Output
Returns `String` — the name of the attribute at the specified index, or `null` if the index is out of bounds or the attribute name is unknown.

### Valid Call Patterns
```scala
val attributeName: String = feature.getName(0) // Assuming 'feature' is an instance of IFeature
```

### LLM Instruction Prompt
- Ensure that the index provided is valid and corresponds to an existing attribute in the feature. Handle cases where the index may be out of bounds.

### Prompt Snippet
```text
Retrieve the name of the attribute at index 0 from the feature using feature.getName(0).
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Check the index before calling getName to avoid null returns
if (i >= 0 && i < feature.getAttributeCount) {
  val attributeName: String = feature.getName(i)
} else {
  // Handle the error case
}
```
