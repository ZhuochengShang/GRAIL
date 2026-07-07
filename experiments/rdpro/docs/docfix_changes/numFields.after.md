## API Test: `numFields`
_Grounding: doc-repaired from source (docfix)._

### Goal
`numFields` is a property of a `DBFWriter` instance that returns the number of fields (columns) defined in the `org.apache.spark.sql.types.StructType` schema provided to the writer's constructor. The `DBFWriter` class is used to create the attribute file (`.dbf`) for a shapefile.

### Valid Access Patterns
```scala
// Accesses the numFields property of a DBFWriter instance.
// The DBFWriter constructor requires a java.io.OutputStream and an
// org.apache.spark.sql.types.StructType.

import edu.ucr.cs.bdlab.beast.io.shapefilev2.DBFWriter
import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType}
import java.io.ByteArrayOutputStream

// 1. Define the schema using Spark SQL types.
val schema = StructType(Array(
  StructField("name", StringType, nullable = true),
  StructField("value", IntegerType, nullable = true)
))

// 2. Create a java.io.OutputStream.
val outputStream = new ByteArrayOutputStream()

// 3. Instantiate the writer with the stream and schema.
val writer = new DBFWriter(outputStream, schema)

// 4. Access the numFields property.
val attributeCount: Int = writer.numFields // Returns 2
writer.close()
```

### LLM Instruction Prompt
To get the number of fields, first create a `DBFWriter` instance. Its constructor requires two arguments: a `java.io.OutputStream` (e.g., `java.io.FileOutputStream`) as the first argument, and an `org.apache.spark.sql.types.StructType` defining the attribute schema as the second. Then, access the `numFields` property on the created instance.

### Prompt Snippet
To get the number of fields, construct a `DBFWriter` with a `java.io.OutputStream` and a Spark SQL `StructType` schema, then access its `numFields` property.

### Common Failure Modes
The `DBFWriter` constructor will fail compilation if called with incorrect argument types. Its signature is `(out: java.io.OutputStream, schema: org.apache.spark.sql.types.StructType)`. Providing a file path `String` for the output stream or a simple `Array` instead of a `StructType` for the schema will cause a type mismatch error.

### Fix Code Hint
```scala
// WRONG: Constructor arguments have incorrect types (String, Array).
val writer = new DBFWriter("path.dbf", Array("ID", "City"))

// CORRECT: Provide a java.io.OutputStream and a Spark SQL StructType.
import org.apache.spark.sql.types._
import java.io.FileOutputStream
val schema = StructType(Seq(StructField("ID", IntegerType), StructField("City", StringType)))
val outStream = new FileOutputStream("path.dbf")
val writer = new DBFWriter(outStream, schema)
```