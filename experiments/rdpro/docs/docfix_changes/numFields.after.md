## API Test: `numFields`
_Grounding: doc-repaired from source (docfix)._

### Goal
Return the number of attributes (fields) defined in the Spark SQL schema passed to a `DBFWriter`.

### Valid Call Patterns
Requires the following types and imports:
- `edu.ucr.cs.bdlab.beast.io.shapefilev2.DBFWriter` (Scala class)
- `java.io.ByteArrayOutputStream` (Java class)
- `org.apache.spark.sql.types.StructType` (Scala class)
- `org.apache.spark.sql.types.StringType` (Scala class)

```scala
import edu.ucr.cs.bdlab.beast.io.shapefilev2.DBFWriter
import java.io.ByteArrayOutputStream
import org.apache.spark.sql.types.{StructType, StringType}

val out = new ByteArrayOutputStream()
val schema = new StructType().add("name", StringType)
val writer = new DBFWriter(out, schema)

val n: Int = writer.numFields
require(n == 1, s"Expected 1 field, got $n")

writer.close()
```

### LLM Instruction Prompt
- `numFields` is an instance method on `edu.ucr.cs.bdlab.beast.io.shapefilev2.DBFWriter`, NOT on a GPX record or `IFeature`.
- To call it, you must instantiate a `DBFWriter` using a `java.io.OutputStream` and a Spark SQL `StructType` schema.
- The method takes no arguments and returns the number of fields (attributes) defined in the schema passed to the writer.
- Call it exactly as `writer.numFields` (no parentheses).

### Prompt Snippet
```text
Instantiate a DBFWriter with an OutputStream and a StructType schema, then get its attribute count with `writer.numFields` and compare it to the expected schema width.
```

### Common Failure Modes
- **Assuming `numFields` is on a reader record:** The most common failure is attempting to call `r.numFields` on an `IFeature` or GPX record from a reader iteration. `IFeature` does not have this method; it strictly belongs to `DBFWriter`.
- **Missing constructor arguments:** Failing to provide both a `java.io.OutputStream` and an `org.apache.spark.sql.types.StructType` when creating the `DBFWriter`.
- **Adding parentheses:** Calling `writer.numFields()` instead of `writer.numFields`.

### Fix Code Hint
**Wrong:**
```scala
// Fails: IFeature/GPX records do not have a numFields method
for (r <- gpxReader) {
  val n = r.numFields 
}
```

**Correct:**
```scala
// Correct: numFields is an instance method on DBFWriter
val out = new java.io.ByteArrayOutputStream()
val schema = new org.apache.spark.sql.types.StructType().add("name", org.apache.spark.sql.types.StringType)
val writer = new edu.ucr.cs.bdlab.beast.io.shapefilev2.DBFWriter(out, schema)

val n: Int = writer.numFields
writer.close()
```