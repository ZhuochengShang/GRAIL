# IndexBuilder

_`buildIndex` creates an index for all GeoTIFF files located in a specified directory, facilitating efficient access and processing of raster data in…_

**Receiver:** static object — call `IndexBuilder.<method>(...)`

**Members** (most robust first): ⚠️ `buildIndex` **(primary)**

---

## API Test: `buildIndex`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def buildIndex(sparkContext: SparkContext, dir: String, indexFile: String): Unit
private def buildIndex(sparkContext: SparkContext, fs: FileSystem, basePath: String): Map[String, (Int, String)]
private def buildIndex(fs: FileSystem, basePath: String): Map[String, (Int, String)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:186  (+2 more definition site/overload)_

_Source doc:_ Build a raster index on all GeoTIFF files in a directory. @param sparkContext spark context to parallelize index creation @param dir the directory that contains raster files @param indexFile the path of the index file to write

### Goal
`buildIndex` creates an index for all GeoTIFF files located in a specified directory, facilitating efficient access and processing of raster data in distributed geospatial analysis.

### Parameters
- `sparkContext` (`SparkContext`): The Spark context used to parallelize the index creation process. It is essential for executing distributed operations.
- `dir` (`String`): The directory path containing the GeoTIFF raster files that need to be indexed. This directory must be accessible and contain valid GeoTIFF files.
- `indexFile` (`String`): The path where the generated index file will be written. This file typically has a CSV format and contains metadata about the indexed raster files.

### Input
The caller must provide:
- A valid `SparkContext` that is properly configured and running.
- A directory containing GeoTIFF files, which must be accessible and correctly formatted.
- A valid file path for the index file where the output will be saved.

### Output
Returns `Unit` — indicating that the index has been successfully created and written to the specified index file. There is no return value to process, but the presence of the index file confirms successful execution.

### Valid Call Patterns
```scala
RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)
```

### LLM Instruction Prompt
- Ensure that the `sparkContext` is initialized and that the specified directory contains valid GeoTIFF files before calling `buildIndex`.

### Prompt Snippet
```text
To create an index for GeoTIFF files, ensure you have a valid SparkContext and a directory with the raster files. Call `buildIndex` with the SparkContext, directory path, and desired index file path.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: Wrong FS: file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/_index.csv, expected: hdfs://localhost:9000

### Fix Code Hint
```scala
// Ensure the SparkContext is initialized and the directory contains valid GeoTIFF files before calling buildIndex
val sparkContext: SparkContext = // initialize your SparkContext
val dir: String = "path/to/your/geoTIFFs"
val indexFile: String = "path/to/your/index.csv"
RasterFileRDD.buildIndex(sparkContext, dir, indexFile)
```
