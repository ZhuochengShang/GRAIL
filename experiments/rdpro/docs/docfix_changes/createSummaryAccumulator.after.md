## API Test: `createSummaryAccumulator`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create and register a Spark-side `SummaryAccumulator` to aggregate feature summary information (including feature sizes) while processing spatial/vector features in distributed Beast/RDPro workflows.

### Valid Call Patterns
Requires the following imports and types:
- `edu.ucr.cs.bdlab.beast.synopses.Summary` (Scala object)
- `edu.ucr.cs.bdlab.beast.synopses.SummaryAccumulator` (Scala class)
- `edu.ucr.cs.bdlab.beast.geolite.IFeature` (Scala trait)

```scala
import edu.ucr.cs.bdlab.beast.synopses.Summary
import edu.ucr.cs.bdlab.beast.synopses.SummaryAccumulator
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// sc is an existing SparkContext
// featuresRDD is an existing RDD[IFeature]
val acc: SummaryAccumulator = Summary.createSummaryAccumulator(sc)

val counted = featuresRDD.map { f =>
  acc.add(f)
  f
}

val n = counted.count() // Action required to trigger accumulation
require(n > 0, "empty result for createSummaryAccumulator")

val summaryValue = acc.value
require(summaryValue != null, "summary accumulator value is null")
println("__CHECK__ createSummaryAccumulator " + n)
```

### LLM Instruction Prompt
- `createSummaryAccumulator` is a method on the `Summary` companion object, not an instance method on the `Summary` class.
- It must be called statically as `Summary.createSummaryAccumulator(sc)`.
- Do not instantiate `Summary` (e.g., `new Summary()`) to call this method.
- Pass a real `SparkContext` (`sc`); do not substitute `SparkSession` directly.
- Add features with `accumulator.add(f)` inside a transformation, then run an action (like `count()`) before reading `accumulator.value`.

### Prompt Snippet
Call `Summary.createSummaryAccumulator(sc)` statically on the companion object (do not instantiate `Summary`). Add each `IFeature` via `accumulator.add(f)` in an RDD transformation, run an action (e.g., `count()`), then read `accumulator.value`.

### Common Failure Modes
- **Instantiating `Summary`:** Attempting to call `createSummaryAccumulator` as an instance method on a `new Summary()` object. It is defined in the `Summary` companion object and must be called statically.
- **Missing Action:** Reading `accumulator.value` before any Spark action runs (value remains unmaterialized/unchanged).
- **Wrong Context Type:** Passing a `SparkSession` instead of the required `SparkContext`.

### Fix Code Hint
```scala
// WRONG: Calling on an instance of Summary
val summaryObj = new Summary()
val acc = summaryObj.createSummaryAccumulator(sc)

// CORRECT: Calling statically on the Summary companion object
val acc = Summary.createSummaryAccumulator(sc)
val counted = featuresRDD.map { f =>
  acc.add(f)
  f
}
counted.count() // trigger action
val summaryValue = acc.value
```