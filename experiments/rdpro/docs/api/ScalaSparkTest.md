# ScalaSparkTest

_Retrieve the current `SparkContext` instance, which is essential for executing distributed raster processing tasks in RDPro._

**Receiver:** instance — obtain a `ScalaSparkTest` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `sparkContext` **(primary)**, ⚠️ `copyResource`, ⚠️ `locateResource`, ⚠️ `readFile`, ⚠️ `readTextResource`, ⚠️ `sparkSession`, ⚠️ `using`

---

## API Test: `sparkContext`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def sparkContext: SparkContext
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:38_

### Goal
Retrieve the current `SparkContext` instance, which is essential for executing distributed raster processing tasks in RDPro.

### Parameters
_None._

### Input
No specific input is required for this method.

### Output
Returns `SparkContext` — an instance of Spark's `SparkContext`, which represents the connection to a Spark cluster and is used to create RDDs, accumulators, and broadcast variables.

### Valid Call Patterns
```scala
val sc: SparkContext = sparkContext
```

### LLM Instruction Prompt
- Ensure that a valid Spark session is initialized before calling `sparkContext`, as it relies on an active Spark environment.

### Prompt Snippet
```text
Retrieve the SparkContext instance to perform distributed raster processing operations.
```

### Common Failure Modes
- **[compile]** error: forward reference extends over definition of value sparkContext

### Fix Code Hint
```scala
// Ensure Spark is properly initialized before calling sparkContext
val spark = SparkSession.builder().appName("RDPro Example").getOrCreate()
val sc = spark.sparkContext
```

## API Test: `copyResource`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def copyResource(resourcePath: String, filePath: File, overwrite: Boolean): Unit
def copyResource(resourcePath: String, filePath: File): Unit
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:251  (+1 more definition site/overload)_

_Source doc:_ Copy a resource to a temporary file to allow reading it as a file. @param resourcePath the path of the resource to read @param filePath     the path of the file to write @param overwrite    set this flag to automatically overwrite the output file.

### Goal
`copyResource` copies a specified resource file to a designated file path, allowing it to be accessed as a regular file in the context of geospatial raster processing.

### Parameters
- `resourcePath` (`String`): The path of the resource to read, which should be a valid path to a resource within the project (e.g., `"/test.points"`).
- `filePath` (`File`): The path of the file to write, which should be a valid `File` object representing the destination where the resource will be copied.
- `overwrite` (`Boolean`): A flag indicating whether to overwrite the output file if it already exists. Set to `true` to allow overwriting, or `false` to prevent it.

### Input
The caller must provide:
- A valid `resourcePath` that points to an existing resource within the project.
- A `filePath` that is a valid `File` object where the resource will be copied.
- The `overwrite` parameter must be a boolean value indicating the desired behavior for existing files.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output file will be created or overwritten at the specified `filePath`.

### Valid Call Patterns
```scala
copyResource("/test.points", new File(path, "input.txt"), true)
copyResource("/test.points", new File(path, "input.txt"))
```

### LLM Instruction Prompt
- When calling `copyResource`, ensure that the `resourcePath` is a valid string pointing to an existing resource, the `filePath` is a valid `File` object, and the `overwrite` parameter is set according to the desired file handling behavior.

### Prompt Snippet
```text
To copy a resource, use the following syntax: copyResource("/test.points", new File(path, "input.txt"), true)
```

### Common Failure Modes
- **[compile]** error: overloaded method constructor File with alternatives: _(seen 2x)_
- **[compile]** error: not found: value copyResource _(seen 2x)_

### Fix Code Hint
```scala
// Ensure the resource path is correct and the file path is a valid file location.
val resourcePath = "/test.points"
val destinationFile = new File(path, "input.txt")
copyResource(resourcePath, destinationFile, overwrite = true)
```

## API Test: `locateResource`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def locateResource(srcPath: String): File
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:293_

_Source doc:_ Returns the relative or full path to the given resource @param srcPath a path to a resource that starts with "/" @return the path of the file of the given resource

### Goal
`locateResource` retrieves the file path for a specified resource, which is essential for accessing data files in geospatial raster processing workflows.

### Parameters
- `srcPath` (`String`): A string representing the path to a resource, which must start with a "/" indicating an absolute path.

### Input
The caller must provide a valid resource path as a string that starts with "/". This path should point to a resource that is accessible within the context of the application.

### Output
Returns `File` — the `File` object represents the path of the specified resource, allowing further operations to be performed on the file.

### Valid Call Patterns
```scala
val inputfile = locateResource("/test.partitions")
```

### LLM Instruction Prompt
- When calling `locateResource`, ensure that the `srcPath` parameter is a valid string that starts with a "/" and points to an accessible resource.

### Prompt Snippet
```text
Locate the resource file using the path provided, ensuring it starts with a "/" and is accessible.
```

### Common Failure Modes
- **[compile]** error: not found: value locateResource _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the srcPath starts with "/" and points to a valid resource
val inputfile = locateResource("/valid/resource/path")
```

## API Test: `readFile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readFile(filename: String): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:170_

_Source doc:_ Read a text file as a single big string. @param filename the name (or path) of the file @return the contents of the file as one big String.

### Goal
`readFile` reads the contents of a specified text file and returns it as an array of strings, where each element represents a line from the file.

### Parameters
- `filename` (`String`): The name or path of the text file to be read.

### Input
The caller must provide a valid path to a text file that is accessible in the environment where the Spark job is running. The file should be formatted as plain text.

### Output
Returns `Array[String]` — an array containing the lines of the text file, with each line represented as a separate string.

### Valid Call Patterns
```scala
val content: Array[String] = readFile("path/to/your/file.txt")
```

### LLM Instruction Prompt
- Ensure that the `filename` parameter points to a valid and accessible text file. The file should be in plain text format.

### Prompt Snippet
```text
Read the contents of a text file using the readFile function, ensuring the file path is correct and accessible.
```

### Common Failure Modes
- **[compile]** error: not found: value readFile _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the file path is correct and the file is accessible
val content: Array[String] = readFile("correct/path/to/file.txt")
```

## API Test: `readTextResource`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readTextResource(resourcePath: String, maxLines: Int): Array[String]
def readTextResource(resourcePath: String): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:153  (+1 more definition site/overload)_

_Source doc:_ Read the first n lines from the given resource and return those lines as an array of Strings. If the given upper bound is bigger than the input file, the entire input file is loaded and returned. Therefore, the returned array might be smaller than the given upper bound if the file is smaller. @param resourcePath the path to the resource to read @param maxLines     the upper bound of the number of lines to read @return an array of strings containing the lines read from the input file

### Goal
`readTextResource` reads a specified number of lines from a text resource, which can be useful for loading configuration or data files in geospatial analysis workflows.

### Parameters
- `resourcePath` (`String`): The path to the text resource file to read. This should be a valid path accessible within the Spark environment.
- `maxLines` (`Int`): The maximum number of lines to read from the resource. If the resource contains fewer lines than this value, all lines will be returned.

### Input
The caller must provide a valid path to a text resource file that is accessible in the Spark environment. The file should be formatted as plain text. There are no specific preconditions beyond ensuring the file exists and is readable.

### Output
Returns `Array[String]` — an array of strings containing the lines read from the input file. The length of the array may be less than or equal to `maxLines` if the file contains fewer lines.

### Valid Call Patterns
```scala
val lines: Array[String] = readTextResource("/test.wkt", 10)
```

### LLM Instruction Prompt
- Ensure that the `resourcePath` points to a valid text file and that the `maxLines` parameter is a positive integer.

### Prompt Snippet
```text
Read the first 10 lines from the specified text resource file.
```

### Common Failure Modes
- **[compile]** error: not found: value readTextResource _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the resource path is correct and the file exists before calling the function.
val lines: Array[String] = readTextResource("/valid/path/to/resource.txt", 10)
```

## API Test: `sparkSession`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
override def sparkSession: SparkSession
def sparkSession: SparkSession
```
_Source: beast/spatialtest/src/main/scala/edu/ucr/cs/bdlab/test/BeastSpatialTest.scala:27  (+1 more definition site/overload)_

### Goal
The `sparkSession` function provides access to the Spark session used for distributed raster processing within the RDPro library.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `SparkSession` — an instance of SparkSession that represents the entry point to programming with Spark, allowing users to execute Spark operations and manage the Spark application.

### Valid Call Patterns
```scala
val session: SparkSession = value.sparkSession
```

### LLM Instruction Prompt
- When calling `sparkSession`, ensure that a valid Spark context is initialized and that the RDPro library is properly set up in your Spark environment.

### Prompt Snippet
```text
To access the Spark session in RDPro, use the following code:
val session: SparkSession = value.sparkSession
```

### Common Failure Modes
- **[compile]** error: value sparkSession is not a member of org.apache.spark.SparkContext _(seen 4x)_

### Fix Code Hint
```scala
Ensure that your Spark application is correctly configured and that the RDPro library is included in your build dependencies before calling sparkSession.
```

## API Test: `using`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def using[A <: AutoCloseable, B](resource: A)
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:606  (+1 more definition site/overload)_

### Goal
The `using` function provides a way to manage resources that implement the `AutoCloseable` interface, ensuring that they are properly closed after use, which is essential in geospatial processing to prevent resource leaks.

### Parameters
- `resource` (`A`): An instance of a resource that implements the `AutoCloseable` interface, such as a database connection or file stream, which will be automatically closed after the block of code using it is executed.

### Input
The caller must provide a valid `AutoCloseable` resource, such as a database connection obtained from a driver manager. The resource must be properly initialized and accessible.

### Output
Returns `unspecified` — the function does not return a value; instead, it ensures that the provided resource is closed after the execution of the block of code that uses it.

### Valid Call Patterns
```scala
using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) { dbConnection =>
  // Code that uses dbConnection
}
```

### LLM Instruction Prompt
- When calling `using`, ensure that the resource provided is an instance of a class that implements `AutoCloseable`, and that it is properly initialized before use.

### Prompt Snippet
```text
Ensure to use `using` with an `AutoCloseable` resource to manage resource cleanup effectively.
```

### Common Failure Modes
- **[compile]** error: not found: value using _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the resource is properly initialized before passing it to `using`
val dbConnection = DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")
using(dbConnection) { connection =>
  // Use the connection safely here
}
```
