# Summary

_The `createSummaryAccumulator` function initializes a summary accumulator to collect and aggregate the sizes of geospatial features in a distributed Spark…_

**Receiver:** instance — obtain a `Summary` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `createSummaryAccumulator` **(primary)**

---

## API Test: `createSummaryAccumulator`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def createSummaryAccumulator(sc: SparkContext) : SummaryAccumulator
def createSummaryAccumulator(sc: SparkContext, sizeFunction: IFeature => Int) : SummaryAccumulator
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Summary.scala:422  (+1 more definition site/overload)_

_Source doc:_ Create a summary accumulator that uses the method [[IFeature#getStorageSize]] to accumulate the sizes of the features. @param sc the spark context to register the accumulator to @return the initialized and registered accumulator

### Goal
The `createSummaryAccumulator` function initializes a summary accumulator to collect and aggregate the sizes of geospatial features in a distributed Spark environment.

### Parameters
- `sc` (`SparkContext`): The Spark context used to register the accumulator. It is expected to be an active SparkContext instance that manages the Spark application.
- `sizeFunction` (`IFeature => Int`): A function that takes an `IFeature` and returns its size as an integer. This function is optional; if not provided, the default size method will be used.

### Input
The caller must provide an active `SparkContext` and optionally a size function that conforms to the type `IFeature => Int`. The input features should be instances of `IFeature`, which are typically loaded from geospatial data sources such as shapefiles or GeoJSON.

### Output
Returns `SummaryAccumulator` — an accumulator that aggregates the sizes of the features processed. This accumulator can be used to retrieve the total size of all features added to it.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = features.map(f => {accumulator.add(f); f})
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- Ensure that the `SparkContext` is active and properly configured before calling `createSummaryAccumulator`. If using a custom size function, ensure it is compatible with the `IFeature` type.

### Prompt Snippet
```text
Create a summary accumulator using the active SparkContext and an optional size function to aggregate feature sizes.
```

### Common Failure Modes
- **[compile]** error: value > is not a member of edu.ucr.cs.bdlab.beast.synopses.Summary _(seen 4x)_

### Fix Code Hint
```scala
// Ensure SparkContext is initialized and active
val sparkContext = SparkSession.builder().appName("Geospatial Analysis").getOrCreate().sparkContext
val accumulator = Summary.createSummaryAccumulator(sparkContext)
```
