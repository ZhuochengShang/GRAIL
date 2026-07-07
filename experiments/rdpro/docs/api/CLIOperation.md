# CLIOperation

_The `printUsage` function outputs usage information for the RDPro library, helping users understand how to utilize its features effectively._

**Receiver:** instance — obtain a `CLIOperation` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `printUsage` **(primary)**, ⚠️ `run`

---

## API Test: `printUsage`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def printUsage(out: PrintWriter): Unit
override def printUsage(out: PrintStream): Unit
def printUsage(out: PrintStream): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:256  (+4 more definition site/overload)_

### Goal
The `printUsage` function outputs usage information for the RDPro library, helping users understand how to utilize its features effectively.

### Parameters
- `out` (`PrintWriter`): A `PrintWriter` instance where the usage information will be printed. This can be a standard output stream or a file writer.

### Input
The caller must provide a valid `PrintWriter` or `PrintStream` instance. There are no specific data formats required, but the output stream must be properly initialized and accessible.

### Output
Returns `Unit` — this indicates that the function does not return a value but performs a side effect by printing usage information to the specified output stream.

### Valid Call Patterns
```scala
val baos = new ByteArrayOutputStream()
val printer: PrintStream = new PrintStream(baos)
OperationHelper.printUsage(printer)
printer.close()
```

### LLM Instruction Prompt
- When calling `printUsage`, ensure that a valid `PrintWriter` or `PrintStream` is provided as an argument. The output will be printed to the specified stream.

### Prompt Snippet
```text
OperationHelper.printUsage(printer)
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/mortbay/jetty/handler/AbstractHandler _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the PrintWriter or PrintStream is properly initialized and not closed before calling printUsage.
val printer: PrintStream = new PrintStream(new ByteArrayOutputStream())
OperationHelper.printUsage(printer)
printer.close()
```

## API Test: `run`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Unit
def run(source: String, tileDir: String, indexFile:FileStatus, z: Int, currX: Int, currY: Int, sc: SparkContext): (BufferedImage,Int)
def run(inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): Array[Int]
def run(opts: BeastOptions, inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): BufferedImage
def run(): Unit
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: JavaSparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], ss: SparkSession): Any
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/NPYTileGeneratorOnthefly.scala:29  (+28 more definition site/overload)_

### Goal
The `run` function processes raster data by generating a `BufferedImage` from specified tile data and returns it along with an integer value, typically representing a status or identifier.

### Parameters
- `source` (`String`): The path to the source raster data, typically a GeoTIFF file.
- `tileDir` (`String`): The directory where tile data is stored, which is used for accessing the raster tiles.
- `indexFile` (`FileStatus`): A `FileStatus` object representing the index file that contains metadata about the raster tiles.
- `z` (`Int`): The zoom level for the raster tiles, which determines the level of detail in the output image.
- `currX` (`Int`): The x-coordinate of the current tile in the tile grid.
- `currY` (`Int`): The y-coordinate of the current tile in the tile grid.
- `sc` (`SparkContext`): The Spark context used for executing the operation in a distributed environment.

### Input
The caller must provide:
- A valid `source` path pointing to a GeoTIFF file.
- A `tileDir` that contains the raster tiles.
- An `indexFile` that is a valid `FileStatus` object.
- Valid integer values for `z`, `currX`, and `currY` that correspond to the tile grid.
- A running `SparkContext` instance.

### Output
Returns `(BufferedImage,Int)` — a tuple where the first element is a `BufferedImage` representing the processed raster tile, and the second element is an integer that may represent a status code or tile identifier.

### Valid Call Patterns
```scala
val source = "path/to/raster.tif"
val tileDir = "path/to/tile/directory"
val indexFile: FileStatus = // obtain FileStatus for the index file
val z = 5
val currX = 10
val currY = 15
val result: (BufferedImage, Int) = run(source, tileDir, indexFile, z, currX, currY, sparkContext)
```

### LLM Instruction Prompt
- Ensure that all parameters are correctly provided and match the expected types. The `source` must be a valid path to a GeoTIFF file, and the `indexFile` must be a valid `FileStatus` object.

### Prompt Snippet
```text
To call the `run` function, provide the source path to the raster data, the tile directory, the index file status, the zoom level, and the current tile coordinates along with the Spark context.
```

### Common Failure Modes
- **[compile]** error: 6 more arguments than can be applied to method run: (sc: org.apache.spark.SparkContext)Unit _(seen 3x)_
- **[compile]** error: not found: type BufferedImage

### Fix Code Hint
```scala
// Ensure the source path is correct and the index file is properly initialized
val indexFile: FileStatus = // obtain FileStatus for the index file
if (indexFile == null) {
  throw new IllegalArgumentException("Index file must be valid and initialized.")
}
```
