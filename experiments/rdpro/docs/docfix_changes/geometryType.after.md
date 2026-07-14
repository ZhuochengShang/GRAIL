## API Test: `geometryType`
_Grounding: doc-repaired from source (docfix)._

### Goal
Return the most inclusive geometry category present in a spatial dataset or partition (e.g., `Empty`, `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, `MultiPolygon`, or `GeometryCollection`).

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._ // REQUIRED: provides the .summary extension method on spatial RDDs

// Assuming featuresRDD is an existing spatial RDD
val summary = featuresRDD.summary
val gt = summary.geometryType
```

### LLM Instruction Prompt
- `geometryType` is a member of `SpatialPartition` and `Summary`, not `DatasetProcessor`.
- Do not attempt to instantiate `DatasetProcessor` to call this method.
- To use this API, obtain a `Summary` object by calling `.summary` on a spatial RDD (e.g., `featuresRDD.summary`), then call `.geometryType` on it.
- You must include `import edu.ucr.cs.bdlab.beast._` to access the `.summary` extension method on spatial RDDs.

### Prompt Snippet
```text
Given a spatial RDD named `featuresRDD`, compute its summary using `featuresRDD.summary` and then call `.geometryType` (no args) to get the dataset's most inclusive geometry type.
```

### Common Failure Modes
- Incorrectly assuming `geometryType` is an instance method on `DatasetProcessor`, leading to compilation failures when attempting to instantiate `DatasetProcessor` with missing arguments.
- Calling `geometryType` directly on an RDD instead of first computing the `Summary` via `.summary`.
- Missing the `import edu.ucr.cs.bdlab.beast._` required to resolve the `.summary` extension method.

### Fix Code Hint
```scala
// WRONG: Attempting to call on DatasetProcessor
val dp = new DatasetProcessor() // Fails: missing arguments
val gt = dp.geometryType

// CORRECT: Call on the Summary object obtained from a spatial RDD
import edu.ucr.cs.bdlab.beast._

val summary = featuresRDD.summary
val gt = summary.geometryType
```