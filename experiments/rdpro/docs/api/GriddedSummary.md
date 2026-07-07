# GriddedSummary

_`computeForFeatures` computes a synopsis of the provided spatial features, which can be used for efficient spatial analysis and processing._

**Receiver:** static object — call `GriddedSummary.<method>(...)`

**Members** (most robust first): ⚠️ `computeForFeatures` **(primary)**

---

## API Test: `computeForFeatures`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def computeForFeatures(features: SpatialRDD, synopsisSize: Long = 1024 * 1024): Synopsis
def computeForFeatures(features: SpatialRDD, sizeFunction: IFeature => Int = f => f.getStorageSize) : Summary
def computeForFeatures(features : JavaSpatialRDD) : Summary
def computeForFeatures(features: SpatialRDD, numPartitions: Int*): (Summary, RDD[(Array[Int], Summary)])
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Synopsis.scala:34  (+3 more definition site/overload)_

### Goal
`computeForFeatures` computes a synopsis of the provided spatial features, which can be used for efficient spatial analysis and processing.

### Parameters
- `features` (`SpatialRDD`): A distributed collection of spatial features that represent geometries and associated attributes. This argument is expected to contain valid spatial data that can be processed in a distributed manner.
- `synopsisSize` (`Long`), default `1024 * 1024`: The size of the synopsis to be computed, specified in bytes. This parameter determines the amount of data to be summarized and can be adjusted based on the user's needs.

### Input
The input must be a valid `SpatialRDD` containing spatial features. The features should be properly formatted and accessible within the Spark context. There are no specific file formats required for this function, but the input data must be compatible with the `SpatialRDD` type.

### Output
Returns `Synopsis` — a summary representation of the spatial features, which provides insights into the characteristics of the input data. The format of the synopsis is internal to the library and is used for further spatial analysis.

### Valid Call Patterns
```scala
val summary = Summary.computeForFeatures(features, f => f.getGeometry.getNumPoints * 2 * 4)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` containing spatial data. The `synopsisSize` can be adjusted as needed, but defaults to `1024 * 1024` bytes if not specified.

### Prompt Snippet
```text
Compute a synopsis for the given spatial features using the default synopsis size or a custom size function.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the features are properly loaded as a SpatialRDD before calling computeForFeatures
val features: SpatialRDD = ... // Load or create your SpatialRDD here
val summary = Summary.computeForFeatures(features)
```
