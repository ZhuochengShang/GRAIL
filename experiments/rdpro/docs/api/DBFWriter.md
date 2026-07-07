# DBFWriter

_`numFields` retrieves the number of attributes present in a given file, which is essential for understanding the structure of the data being processed in…_

**Receiver:** instance — obtain a `DBFWriter` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `numFields` **(primary)**

---

## API Test: `numFields`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def numFields: Int
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42_

_Source doc:_ Number of attributes in the file

### Goal
`numFields` retrieves the number of attributes present in a given file, which is essential for understanding the structure of the data being processed in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a valid file that has been loaded into the appropriate reader context. This file should be in a supported format (e.g., GeoTIFF, HDF, Shapefile, GeoJSON) and must contain attributes for the `numFields` method to return a meaningful value.

### Output
Returns `Int` — the number of attributes in the file, which indicates how many distinct pieces of information are available for each record in the dataset.

### Valid Call Patterns
```scala
val numAttributes: Int = r.numFields
```

### LLM Instruction Prompt
- Ensure that the file has been properly loaded and contains attributes before calling `numFields`. The method should be called on an instance of a reader that supports attribute retrieval.

### Prompt Snippet
```text
To get the number of attributes in your loaded file, use the `numFields` method on the reader instance.
```

### Common Failure Modes
- **[compile]** error: value numFields is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD _(seen 3x)_
- **[compile]** error: not found: value SpatialRDD

### Fix Code Hint
```scala
// Ensure the file is loaded correctly and contains attributes before calling numFields
val raster: RDD[ITile[Int]] = sc.geoTiff("your_file.tif")
val numAttributes: Int = raster.numFields // Ensure raster has attributes
```
