## API Test: `sierpinski`
_Grounding: doc-repaired from source (docfix)._

### Goal
Generates a `SpatialRDD` of points following the Sierpinski distribution. The `cardinality` parameter specifies the input size for the generator, which produces an RDD containing `cardinality / 2` records. To generate a target number of records, `N`, the function must be called with `cardinality` set to `2 * N`.

### Valid Call Patterns|Valid Access Patterns
```scala
// Required imports for the extension method and return type
import edu.ucr.cs.bdlab.beast.cg.SpatialDataGenerator.implicits._
import edu.ucr.cs.bdlab.beast.SpatialRDD
import org.apache.spark.SparkContext

// sc: SparkContext must be an initialized SparkContext
// To generate exactly 1000 records, the cardinality must be 2000.
val generatedRDD: SpatialRDD = sc.generateSpatialData.sierpinski(2000)
```
- Requires `org.apache.spark.SparkContext` (as `sc`).
- Requires import `edu.ucr.cs.bdlab.beast.cg.SpatialDataGenerator.implicits._` for the `generateSpatialData` extension method.
- Returns `edu.ucr.cs.bdlab.beast.SpatialRDD`.

### LLM Instruction Prompt
Generate a `SpatialRDD` containing a specific number of records, `N`, from the Sierpinski distribution. To do this, you must call `sc.generateSpatialData.sierpinski` with the `cardinality` parameter set to `2 * N`. For example, to get 1000 records, the call must be `sierpinski(2000)`.

### Prompt Snippet
```text
Generate 1000 records from the Sierpinski distribution by calling sc.generateSpatialData.sierpinski(2000).
```

### Common Failure Modes
- The `cardinality` parameter is not the number of output records. Calling `sierpinski(N)` produces an RDD with `N / 2` records, not `N`. This discrepancy is a common cause of incorrect output sizes.

### Fix Code Hint
```scala
// WRONG: This generates 500 records, not 1000.
val generatedRDD = sc.generateSpatialData.sierpinski(1000)

// CORRECT: To generate 1000 records, double the cardinality.
val generatedRDD = sc.generateSpatialData.sierpinski(2000)
```