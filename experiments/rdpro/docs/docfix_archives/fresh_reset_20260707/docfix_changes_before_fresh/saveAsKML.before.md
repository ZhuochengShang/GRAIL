## API Test: `saveAsKML`

### Signature
```scala
def saveAsKML(filename: String): Unit
def saveAsKML(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:86  (+1 more definition site/overload)_

_Source doc:_ Save features in KML format @param filename the name of the output file

### Goal
The `saveAsKML` function saves geospatial features in KML format, which is commonly used for representing geographic data in applications like Google Earth.

### Parameters
- `rdd` (`JavaSpatialRDD`): A distributed collection of spatial features that you want to save in KML format. This RDD should contain geometries and associated attributes.
- `filename` (`String`): The name of the output KML file, including the desired file path and extension (e.g., "output.kml").

### Input
The caller must provide a `JavaSpatialRDD` containing the spatial features to be saved and a valid filename as a string. The filename must end with the `.kml` extension to ensure proper file format.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The output is a KML file saved to the specified location, which can be used in various geospatial applications.

### Valid Call Patterns
```scala
records.saveAsKML("output.kml")
```

### LLM Instruction Prompt
- Ensure that the `filename` parameter is a valid string ending with `.kml` and that the `rdd` parameter is a properly initialized `JavaSpatialRDD` containing spatial features.

### Prompt Snippet
```text
To save your spatial features in KML format, use the `saveAsKML` method with a valid filename and a `JavaSpatialRDD` containing your data.
```

### Common Failure Modes
- Attempting to save without providing a valid `JavaSpatialRDD` will result in an error.
- Providing a filename that does not end with `.kml` may lead to unexpected behavior or file format issues.

### Fix Code Hint
```scala
// Ensure your RDD is properly initialized and your filename is correct
val spatialData: JavaSpatialRDD = // initialize your JavaSpatialRDD
spatialData.saveAsKML("output.kml")
```