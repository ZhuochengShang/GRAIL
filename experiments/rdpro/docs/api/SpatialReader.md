# SpatialReader

_The `readInput` function loads spatial data from a specified file into a distributed spatial RDD for further geospatial analysis._

**Receiver:** static object — call `SpatialReader.<method>(...)`

**Members** (most robust first): ⚠️ `readInput` **(primary)**

---

## API Test: `readInput`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readInput(sc: JavaSparkContext, opts: BeastOptions, filename: String, iFormat: String): JavaSpatialRDD
def readInput(sc: SparkContext, opts: BeastOptions, filename: String, iFormat: String) : SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialReader.scala:205  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
The `readInput` function loads spatial data from a specified file into a distributed spatial RDD for further geospatial analysis.

### Parameters
- `sc` (`JavaSparkContext`): The Spark context used to manage the distributed computation environment. It is required to initialize the Spark application.
- `opts` (`BeastOptions`): Configuration options for the Beast library, which may include settings for handling spatial data and processing parameters.
- `filename` (`String`): The path to the input file containing spatial data, which can be in formats such as shapefile or GeoJSON.
- `iFormat` (`String`): The format of the input file, indicating how the data should be interpreted (e.g., "shapefile", "geojson").

### Input
The caller must provide a valid file path for the `filename` parameter, which should point to a shapefile or GeoJSON file. The file must be accessible and correctly formatted according to the specified `iFormat`.

### Output
Returns `JavaSpatialRDD` — a distributed collection of spatial features that can be used for spatial operations and analyses within the Spark environment.

### Valid Call Patterns
```scala
// Load a shapefile
JavaRDD<IFeature> polygons = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_state.zip", "shapefile");

// Load points in GeoJSON format
JavaRDD<IFeature> points = SpatialReader.readInput(sparkContext, new BeastOptions(), "Tweets.geojson.gz", "geojson");
```

### LLM Instruction Prompt
- Ensure that the `filename` provided is a valid path to a shapefile or GeoJSON file and that the `iFormat` matches the file type.

### Prompt Snippet
```text
Load spatial data using the readInput function, ensuring the file path and format are correct.
```

### Common Failure Modes
- **[compile]** error: value rawSpatialRDD is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Check that the file exists and is in the correct format before calling readInput
if (new File(filename).exists() && (iFormat == "shapefile" || iFormat == "geojson")) {
    val spatialData = SpatialReader.readInput(sc, new BeastOptions(), filename, iFormat)
} else {
    throw new IllegalArgumentException("Invalid file path or format.")
}
```
