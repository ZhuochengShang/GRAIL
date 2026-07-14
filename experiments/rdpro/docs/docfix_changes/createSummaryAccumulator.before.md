## API Test: `createSummaryAccumulator`

### Signature
```scala
def createSummaryAccumulator(sc: SparkContext) : SummaryAccumulator
def createSummaryAccumulator(sc: SparkContext, sizeFunction: IFeature => Int) : SummaryAccumulator
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Summary.scala:422  (+1 more definition site/overload)_

_Source doc:_ Create a summary accumulator that uses the method [[IFeature#getStorageSize]] to accumulate the sizes of the features. @param sc the spark context to register the accumulator to @return the initialized and registered accumulator

### Goal
Create and register a Spark-side `SummaryAccumulator` to aggregate feature summary information (including feature sizes) while processing spatial/vector features in distributed Beast/RDPro workflows.

### Parameters
- `sc` (`SparkContext`): Spark context where the accumulator is initialized and registered.
- `sizeFunction` (`IFeature => Int`): Function that returns an `Int` size for each `IFeature` to be accumulated (source doc notes storage-size accumulation via `IFeature#getStorageSize` behavior).

### Input
A valid Spark `SparkContext` and, for the 2-argument overload, a per-feature size function of type `IFeature => Int`.  
This API itself does not read files directly; you typically apply the accumulator while mapping over loaded features (for example, from `sc.shapefile(...)` as shown in README usage).  
Precondition: you must trigger an action after adding features to the accumulator; otherwise, no distributed computation runs and accumulator values will not be updated.

### Output
Returns `SummaryAccumulator` — an initialized, Spark-registered accumulator object whose `.value` provides the aggregated summary after actions execute.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = polygons.map(f=> {accumulator.add(f); f})
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- Use receiver/qualifier exactly as documented: `Summary.createSummaryAccumulator(sparkContext)`.
- Pass a real `SparkContext`; do not substitute `SparkSession` directly.
- If using the 2-argument overload, provide exactly `IFeature => Int` for `sizeFunction`.
- Add features with `accumulator.add(f)` inside a transformation, then run an action before reading `accumulator.value`.
- Do not invent extra parameters, options, or return types.

### Prompt Snippet
```text
Create a SummaryAccumulator with Summary.createSummaryAccumulator(sparkContext), add each IFeature via accumulator.add(f) in an RDD transformation, run an action, then read accumulator.value. If custom sizing is needed, call the overload that takes sizeFunction: IFeature => Int.
```

### Common Failure Modes
- Reading `accumulator.value` before any Spark action runs (value remains unmaterialized/unchanged).
- Passing the wrong context object type (must be `SparkContext`).
- Using an invalid size function type for the overload (must be `IFeature => Int`).
- Calling form that drops the documented receiver (can fail depending on imports/scope).

### Fix Code Hint
```scala
val acc = Summary.createSummaryAccumulator(sparkContext)
val counted = features.map(f => { acc.add(f); f })
counted.count()   // trigger action
val summary = acc.value
```