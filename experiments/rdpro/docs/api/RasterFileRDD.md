# RasterFileRDD

_`selectFiles` retrieves a list of raster files from a specified directory that may intersect with a defined geographical range, optimizing the selection using…_

**Receiver:** instance — obtain a `RasterFileRDD` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `selectFiles` **(primary)**

---

## API Test: `selectFiles`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def selectFiles(fileSystem: FileSystem, dir: String, range: Geometry): Array[String]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:233_

_Source doc:_ Selects all the raster files that could potentially overlap the given query range from a directory of files. If that directory contains an index file, i.e., "_index.csv", then this index is used to prune files that are not relevant. If no index file is there, then all files are returned. @param fileSystem the file system at which the raster files exist @param dir the directory that contains the raster files @param range the query range to limit the files @return the list of files that potentially overlap the given query range

### Goal
`selectFiles` retrieves a list of raster files from a specified directory that may intersect with a defined geographical range, optimizing the selection using an index file if available.

### Parameters
- `fileSystem` (`FileSystem`): The file system instance that provides access to the storage where the raster files are located. This is typically obtained from the Spark context's Hadoop configuration.
- `dir` (`String`): The path to the directory containing the raster files. This directory should be accessible and contain the relevant raster files for processing.
- `range` (`Geometry`): A geometric representation of the area of interest, defined using the JTS (Java Topology Suite) library. This geometry is used to filter the files based on their spatial overlap with the specified range.

### Input
The caller must provide:
- A valid `FileSystem` instance that can access the directory of raster files.
- A string representing the directory path where the raster files are stored.
- A `Geometry` object that defines the spatial range for filtering the raster files. The geometry should be properly constructed to represent the desired area.

### Output
Returns `Array[String]` — an array of file paths (as strings) that correspond to the raster files which potentially overlap with the specified query range. The paths are relative to the provided directory.

### Valid Call Patterns
```scala
val dir = new File("path/to/raster/files")
val geometryFactory = new GeometryFactory(new PrecisionModel(PrecisionModel.FLOATING_SINGLE), 4326)
val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dir.toString,
  geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
```

### LLM Instruction Prompt
- Ensure that the `fileSystem`, `dir`, and `range` parameters are correctly instantiated and passed to the `selectFiles` function. The `range` should be a valid geometry that accurately represents the area of interest.

### Prompt Snippet
```text
Retrieve raster files from the specified directory that may overlap with the given geographical range using the selectFiles function.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: Wrong FS: file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/grail-agent/examples/fixtures, expected: hdfs://localhost:9000 _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the directory exists and contains raster files, and that the range is a valid Geometry object.
```
