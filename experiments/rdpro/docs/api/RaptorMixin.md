# RaptorMixin

_The `flatten` function extracts all pixel values from a `RasterRDD` and returns them along with their respective pixel locations and metadata, facilitating…_

**Receiver:** instance — obtain a `RaptorMixin` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `flatten` **(primary)**, ★ `rasterizePixels`, ★ `rasterizePoints`

---

## API Test: `flatten`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def flatten[T](raster: RasterRDD[T]): RDD[(Int, Int, RasterMetadata, T)]
def flatten: RDD[(Int, Int, RasterMetadata, T)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69  (+1 more definition site/overload)_

_Source doc:_ Extract all pixel values into an RDD @param raster the raster to extract its pixels @tparam T the type of pixel values @return an RDD that contains all pixel locations and values

### Goal
The `flatten` function extracts all pixel values from a `RasterRDD` and returns them along with their respective pixel locations and metadata, facilitating further analysis in geospatial raster processing.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster dataset from which pixel values will be extracted. It must be a valid `RasterRDD` containing pixel data of type `T`.

### Input
The caller must provide a `RasterRDD[T]` that has been properly initialized and populated with pixel data. The raster data can be loaded from formats such as GeoTIFF or HDF using the appropriate loading functions (e.g., `sc.geoTiff(...)`). Ensure that the raster is compatible with the expected pixel type `T`.

### Output
Returns `RDD[(Int, Int, RasterMetadata, T)]` — an RDD containing tuples where each tuple consists of the pixel's row index, column index, associated raster metadata, and the pixel value of type `T`. This output format allows for easy access to pixel locations and values for further processing or analysis.

### Valid Call Patterns
```scala
val finalPixels: Map[(Int, Int), Double] = RasterOperationsGlobal.flatten(smoothedRaster)
  .map(x => ((x._1, x._2), x._4))
  .collectAsMap()
  .toMap
```

### LLM Instruction Prompt
- When calling `flatten`, ensure that the input raster is a valid `RasterRDD` and that the pixel type `T` is correctly specified based on the raster data being processed.

### Prompt Snippet
```text
Extract pixel values from a RasterRDD using the flatten function to facilitate further analysis.
```

### Common Failure Modes
- **[compile]** error: type mismatch;

### Fix Code Hint
```scala
Ensure that the raster is properly loaded and initialized before calling flatten, and verify that the pixel type matches the expected type for the operation.
```

## API Test: `rasterizePixels`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Create a raster from a set of pixel values @param pixels the list of pixel locations and values @param metadata the raster metadata that defines the geography of the pixels @return a raster that contains all the pixels

### Goal
The `rasterizePixels` function creates a raster from a distributed set of pixel values, effectively transforming pixel data into a structured raster format suitable for geospatial analysis.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): A distributed collection of pixel data, where each entry is a tuple containing the x-coordinate, y-coordinate, and the pixel value of type `T`. This represents the location and value of each pixel in the raster.
- `metadata` (`RasterMetadata`): An object that contains metadata about the raster, including its geographical extent, spatial reference system, and dimensions. This information is crucial for correctly positioning the raster in geographic space.
- `rasterFeature` (`RasterFeature`): A feature object that provides additional context for the raster, such as its name and associated file information. This can be used for tracking and managing raster datasets.

### Input
The caller must provide:
- A valid `RDD` of pixel tuples, where each tuple consists of two integers (representing pixel coordinates) and a value of type `T` (e.g., `Int`, `Float`).
- A properly constructed `RasterMetadata` object that defines the raster's spatial properties.
- A `RasterFeature` object that describes the raster's characteristics.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset containing the pixel values organized according to the provided metadata. This output can be further processed or saved in formats like GeoTIFF.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (0, 0, 100),
  (3, 4, 200),
  (8, 9, 300)
))
val raster = sc.rasterizePixels(pixels, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
```

### LLM Instruction Prompt
When calling `rasterizePixels`, ensure that the pixel data is provided as an `RDD` of tuples with valid coordinates and values, and that the metadata and raster feature are correctly defined.

### Prompt Snippet
```text
To create a raster from pixel values, use the `rasterizePixels` function with an RDD of pixel tuples, appropriate raster metadata, and a raster feature.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the pixel coordinates are within the bounds defined by the `RasterMetadata`, and verify that the pixel value type matches the expected type `T`.
```

## API Test: `rasterizePoints`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def rasterizePoints[T: ClassTag](points: RDD[(Double, Double, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:55  (+1 more definition site/overload)_

_Source doc:_ Creates a raster from a list of point locations and values. @param points point locations and raster values @param metadata the metadata that describes the raster location @tparam T the type of raster values @return a raster that contains the given point locations

### Goal
The `rasterizePoints` function converts a set of point locations with associated values into a raster format suitable for geospatial analysis.

### Parameters
- `points` (`RDD[(Double, Double, T)]`): A distributed collection of tuples, where each tuple contains the x-coordinate (longitude), y-coordinate (latitude), and a value of type `T` representing the raster value at that point.
- `metadata` (`RasterMetadata`): An object that contains metadata describing the raster's spatial characteristics, including its extent, spatial reference system, and dimensions.
- `rasterFeature` (`RasterFeature`): An object that defines the specific features or characteristics of the raster being created, which may include additional processing or attributes.

### Input
The input must consist of:
- An `RDD` of point tuples, where each tuple includes valid geographic coordinates (longitude and latitude) and a corresponding value.
- A `RasterMetadata` object that accurately describes the raster's spatial properties.
- A `RasterFeature` object, which may be required for specific raster processing features.

### Output
Returns `RasterRDD[T]` — a distributed raster dataset that contains the rasterized representation of the input point locations and their associated values, structured according to the provided metadata.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (-51.3, 30.4, 100),
  (-55.2, 34.5, 200),
  (-56.4, 39.2, 300)
))
val raster = sc.rasterizePoints(pixels, metadata, null)
```

### LLM Instruction Prompt
- When calling `rasterizePoints`, ensure that the `points` RDD contains valid geographic coordinates and values, and that the `metadata` accurately reflects the raster's spatial properties.

### Prompt Snippet
```text
To create a raster from point data, use the `rasterizePoints` function with an RDD of point tuples, appropriate raster metadata, and a raster feature definition.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the input RDD of points contains valid coordinates and values, and that the metadata accurately describes the raster's spatial extent and resolution. If necessary, provide a valid `RasterFeature` object.
```
