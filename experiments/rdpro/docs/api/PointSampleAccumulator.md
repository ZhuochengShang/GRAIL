# PointSampleAccumulator

_The `add` function accumulates features or points into a summary accumulator for further statistical analysis._

**Receiver:** instance — obtain a `PointSampleAccumulator` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `add` **(primary)**, ⚠️ `merge`, ⚠️ `value`

---

## API Test: `add`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
override def add(f: IFeature): Unit
override def add(v: PointND): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:54  (+1 more definition site/overload)_

### Goal
The `add` function accumulates features or points into a summary accumulator for further statistical analysis.

### Parameters
- `f` (`IFeature`): An instance of `IFeature` representing a geometric feature, such as a polygon or point, that will be added to the accumulator for summary statistics.

### Input
The caller must provide a valid `IFeature` object. This object should be derived from a shapefile or other vector data source that is compatible with the RDPro library. The input data must be accessible and correctly formatted.

### Output
Returns `Unit` — this indicates that the operation has been performed successfully without returning any value. The state of the accumulator is updated to include the newly added feature.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = features.map(f => {accumulator.add(f); f})
```

### LLM Instruction Prompt
- When calling `add`, ensure that the input is a valid `IFeature` object and that the accumulator has been properly initialized.

### Prompt Snippet
```text
accumulator.add(feature)
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
val accumulator = Summary.createSummaryAccumulator(sparkContext)
if (feature != null) {
  accumulator.add(feature)
} else {
  throw new IllegalArgumentException("Feature cannot be null")
}
```

## API Test: `merge`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def merge(other: IntermediateVectorTile): IntermediateVectorTile
override def merge(finalCanvas: Canvas, intermediateCanvas: Canvas): Canvas
def merge(other: AbstractConvolutionTile[T]): AbstractConvolutionTile[T]
def merge(other: ReshapeTile[T]): ReshapeTile[T]
def merge(other: SlidingWindowTile[T, U]): SlidingWindowTile[T, U]
override def merge(other: AccumulatorV2[IFeature, Summary]): Unit
override def merge(other: AccumulatorV2[PointND, Array[PointND]]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SVGPlotter.scala:65  (+6 more definition site/overload)_

### Goal
The `merge` function combines two `Canvas` objects into a single `Canvas`, facilitating the integration of raster data for geospatial analysis.

### Parameters
- `finalCanvas` (`Canvas`): The primary canvas that will hold the final merged result. It represents the existing raster data that will be updated with values from the `intermediateCanvas`.
- `intermediateCanvas` (`Canvas`): The secondary canvas containing raster data that will be merged into the `finalCanvas`. This canvas may contain new or updated pixel values.

### Input
The caller must provide two `Canvas` objects that are compatible in terms of their dimensions and pixel types. Both canvases should be properly initialized and contain valid raster data before calling the `merge` function.

### Output
Returns `Canvas` — the resulting `Canvas` represents the merged raster data, combining pixel values from both the `finalCanvas` and `intermediateCanvas`.

### Valid Call Patterns
```scala
val mergedCanvas: Canvas = finalCanvas.merge(intermediateCanvas)
```

### LLM Instruction Prompt
- When calling `merge`, ensure that both `finalCanvas` and `intermediateCanvas` are initialized and contain compatible raster data.

### Prompt Snippet
```text
To merge two canvases, use the following pattern: `finalCanvas.merge(intermediateCanvas)`, ensuring both canvases are properly initialized.
```

### Common Failure Modes
- **[compile]** error: not found: type Canvas _(seen 4x)_

### Fix Code Hint
```scala
// Ensure both canvases are initialized and compatible before merging
if (finalCanvas.isInitialized && intermediateCanvas.isInitialized) {
  val mergedCanvas: Canvas = finalCanvas.merge(intermediateCanvas)
} else {
  throw new IllegalArgumentException("Both canvases must be initialized before merging.")
}
```

## API Test: `value`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def value: Summary
override def value: Array[PointND]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:68  (+1 more definition site/overload)_

### Goal
Retrieve the computed summary statistics or a collection of points from the raster processing operations.

### Parameters
_None._

### Input
No specific input parameters are required for this method. However, it is assumed that the context in which `value` is called has already performed necessary raster processing operations that would lead to the generation of a summary.

### Output
Returns `Summary` — an object that encapsulates the summary statistics derived from the raster data processing. The exact contents of the `Summary` object are not specified in the provided context.

### Valid Call Patterns
```scala
val summary: Summary = value.value
```

### LLM Instruction Prompt
- Ensure that the `value` method is called in the context of an object that has already accumulated summary statistics from raster processing.

### Prompt Snippet
```text
Retrieve the summary statistics from the raster processing operations using the value method.
```

### Common Failure Modes
- **[compile]** error: type mismatch; _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the raster processing operations have been completed before calling value
val summary: Summary = value.value // This should be called after relevant processing
```
