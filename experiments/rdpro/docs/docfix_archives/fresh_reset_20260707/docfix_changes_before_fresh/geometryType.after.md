## API Test: `geometryType`
_Grounding: doc-repaired from source (docfix)._

### Goal
Get the partition-wide inclusive geometry classification from a **`SpatialPartition` instance** via `def geometryType: GeometryType`.

### Valid Call Patterns|Valid Access Patterns
```scala
import edu.ucr.cs.bdlab.beast.cg.SpatialPartition
import org.locationtech.jts.geom.GeometryType

val partition: SpatialPartition = ???   // must already exist
val gt: GeometryType = partition.geometryType
val witness = gt.toString
require(witness != null && witness.nonEmpty)
println("__CHECK__ geometryType " + witness)
```
- This API is an instance member on `SpatialPartition` (no args).
- Return type here is `org.locationtech.jts.geom.GeometryType`.
- Do not use `DatasetProcessor` as the receiver for this API call pattern.

### LLM Instruction Prompt
Use `geometryType` only as `partition.geometryType` where `partition` is `edu.ucr.cs.bdlab.beast.cg.SpatialPartition`.  
Do not call `geometryType(...)` with arguments.  
Do not treat `DatasetProcessor.geometryType` as the same API: different class, different return type (`String`), different construction requirements.

### Prompt Snippet
```text
Given an existing SpatialPartition `partition`, call:
val gt: org.locationtech.jts.geom.GeometryType = partition.geometryType
```

### Common Failure Modes
- **Previous failure:** constructing `edu.ucr.cs.bdlab.beast.dataExplorer.DatasetProcessor(featuresRDD)` and calling `geometryType` there. This constructor does not exist for an RDD; `DatasetProcessor` requires `(String, java.sql.Connection, String, org.apache.hadoop.fs.FileSystem, org.apache.spark.sql.SparkSession)`.
- Confusing multiple members named `geometryType` across classes (`SpatialPartition` vs `DatasetProcessor`).
- Treating `geometryType` as a free function or passing arguments.

### Fix Code Hint
```scala
// Wrong
val dp = new edu.ucr.cs.bdlab.beast.dataExplorer.DatasetProcessor(featuresRDD)
val gt = dp.geometryType

// Correct
import edu.ucr.cs.bdlab.beast.cg.SpatialPartition
import org.locationtech.jts.geom.GeometryType
val partition: SpatialPartition = ???
val gt: GeometryType = partition.geometryType
```