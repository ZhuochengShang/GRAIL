## API Test: `createSummaryAccumulator`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create and register a `SummaryAccumulator` on a Spark `SparkContext` to aggregate `IFeature` summaries during RDD execution.

### Valid Call Patterns|Valid Access Patterns
```scala
import org.apache.spark.SparkContext
import edu.ucr.cs.bdlab.beast.synopses.{Summary, SummaryAccumulator}
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// sc must be org.apache.spark.SparkContext (not SparkSession)
val acc: SummaryAccumulator = Summary.createSummaryAccumulator(sc)

// or overload with exact function type: IFeature => Int
val acc2: SummaryAccumulator =
  Summary.createSummaryAccumulator(sc, (f: IFeature) => f.getStorageSize)

val counted = featuresRDD.map { f: IFeature =>
  acc.add(f)
  f
}
val n = counted.count()   // action required to materialize accumulator updates
val summary = acc.value
```

### LLM Instruction Prompt
- Call this API on `Summary` as receiver: `Summary.createSummaryAccumulator(...)`.
- Do **not** call `new Summary().createSummaryAccumulator(...)` (that method is not on instances).
- First argument must be `org.apache.spark.SparkContext` (`sc`), not `SparkSession`.
- Overload 2 requires exactly `sizeFunction: edu.ucr.cs.bdlab.beast.geolite.IFeature => Int`.
- Accumulator updates happen during Spark execution; run an action (`count`, etc.) before reading `.value`.

### Prompt Snippet
```text
Use:
val acc = Summary.createSummaryAccumulator(sc)

where sc: org.apache.spark.SparkContext.
If custom sizing is needed:
Summary.createSummaryAccumulator(sc, (f: IFeature) => IntValue)

Add via acc.add(f) inside an RDD transformation, trigger an action, then read acc.value.
```

### Common Failure Modes
- **Compile-time failure from wrong receiver:** using `new Summary().createSummaryAccumulator(...)` or any `summaryInstance.createSummaryAccumulator(...)`.
- Passing `SparkSession` where `SparkContext` is required.
- Using wrong type for overload 2 (must be `IFeature => Int`).
- Reading `acc.value` before an action executes (no updates materialized).

### Fix Code Hint
```scala
// Wrong (receiver error):
val s = new Summary()
val acc = s.createSummaryAccumulator(sc)

// Correct:
val acc = Summary.createSummaryAccumulator(sc)
```