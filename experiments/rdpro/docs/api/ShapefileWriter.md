# ShapefileWriter

_The `initialize` function sets up the necessary parameters and configurations for reading raster data from a specified source in the RDPro library._

**Receiver:** instance — obtain a `ShapefileWriter` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `initialize` **(primary)**

---

## API Test: `initialize`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def initialize(fileSystem: FileSystem, path: String, layer: String, opts: BeastOptions): Unit
private def initialize(fileSystem: FileSystem, path: Path, iLayer: Int): Unit
def initialize(fileSystem: FileSystem, path: String, layer: String, opts: BeastOptions): Unit
override def initialize(out: OutputStream, conf: Configuration): Unit
override def initialize(inputSplit: InputSplit, conf: BeastOptions): Unit
def initialize(): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:74  (+7 more definition site/overload)_

### Goal
The `initialize` function sets up the necessary parameters and configurations for reading raster data from a specified source in the RDPro library.

### Parameters
- `fileSystem` (`FileSystem`): Represents the file system to be used for accessing the data, typically a Hadoop-compatible file system.
- `path` (`String`): The path to the raster data file (e.g., a GeoTIFF) that needs to be processed.
- `layer` (`String`): The specific layer within the raster data to be accessed or processed.
- `opts` (`BeastOptions`): Configuration options for the Beast processing, which may include settings for performance, memory usage, or other processing parameters.

### Input
The caller must provide a valid `FileSystem` instance, a string path pointing to an accessible raster data file (such as a GeoTIFF), a layer name as a string, and a `BeastOptions` object with the necessary configuration settings. The input file must be correctly formatted and accessible in the specified file system.

### Output
Returns `Unit` — indicating that the initialization process has completed successfully without returning any value.

### Valid Call Patterns
```scala
val inputPath = "path/to/raster/file.tif"
val fileSystem: FileSystem = FileSystem.get(sparkContext.hadoopConfiguration)
val layerName = "desiredLayer"
val options = new BeastOptions()

// Example of calling initialize
gpxReader.initialize(fileSystem, inputPath, layerName, options)
```

### LLM Instruction Prompt
- Ensure that the `fileSystem`, `path`, `layer`, and `opts` parameters are correctly instantiated and passed to the `initialize` method. The `path` must point to a valid raster file, and the `opts` should be configured as needed for the specific processing task.

### Prompt Snippet
```text
To initialize the raster reader, provide a valid FileSystem instance, the path to the raster file, the layer name, and the BeastOptions for configuration.
```

### Common Failure Modes
- **[compile]** error: value read is not a member of edu.ucr.cs.bdlab.raptor.GeoTiffReader[Nothing] _(seen 2x)_
- **[compile]** error: object BeastOptions is not a member of package edu.ucr.cs.bdlab.beast.util
- **[compile]** error: not found: value gpxReader

### Fix Code Hint
```scala
Ensure that the file path is correct and accessible, the layer name matches an existing layer in the raster data, and the BeastOptions are properly configured before calling initialize.
```
