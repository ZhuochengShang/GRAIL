# RasterOperationsFocal

_`divideScene` partitions an existing raster RDD into smaller groups of tiles, each associated with a single metadata object, facilitating organized output when…_

**Receiver:** static object — call `RasterOperationsFocal.<method>(...)`

**Members** (most robust first): ⚠️ `divideScene` **(primary)**, ⚠️ `reshapeAverage`, ⚠️ `reshapeNN`, ⚠️ `slidingWindow`

---

## API Test: `divideScene`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def divideScene[T: ClassTag](raster: RasterRDD[T], targetMetadata: RasterMetadata, numTilesX: Int, numTilesY: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625_

_Source doc:_ Divides an existing RDD into a new RDD such that every group of tiles is brought together into one Metadata. This is helpful when writing the resulting RDD to files because each group of tiles will be written to a separate file. @param raster the input raster to repartition @param targetMetadata the metadata of the target (output) raster @param numTilesX number of tiles to combine together into one metadata @param numTilesY number of tiles to combine together into one metadata @tparam T @return

### Goal
`divideScene` partitions an existing raster RDD into smaller groups of tiles, each associated with a single metadata object, facilitating organized output when saving to files.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster RDD that contains the pixel data to be repartitioned. It must be a valid `RasterRDD` containing pixel values of type `T`.
- `targetMetadata` (`RasterMetadata`): The metadata for the output raster, which defines the spatial characteristics and dimensions of the resulting tiles.
- `numTilesX` (`Int`): The number of tiles to combine horizontally into one metadata object. This determines how the raster is divided along the x-axis.
- `numTilesY` (`Int`): The number of tiles to combine vertically into one metadata object. This determines how the raster is divided along the y-axis.

### Input
The caller must provide a valid `RasterRDD` containing pixel data, a `RasterMetadata` object that specifies the output raster's characteristics, and integer values for `numTilesX` and `numTilesY` that define the desired tile grouping. The input raster must be properly formatted and accessible.

### Output
Returns `RasterRDD[T]` — a new raster RDD where each group of tiles is associated with a single metadata object, making it suitable for writing to separate files.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)
```

### LLM Instruction Prompt
- Ensure that the input raster is a valid `RasterRDD` and that the `targetMetadata` is correctly defined for the output raster. The values for `numTilesX` and `numTilesY` should be positive integers.

### Prompt Snippet
```text
To use the `divideScene` function, provide a valid RasterRDD, appropriate RasterMetadata, and specify the number of tiles to combine in both the x and y dimensions.
```

### Common Failure Modes
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]] _(seen 2x)_
- **[compile]** error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- **[compile]** error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Double]

### Fix Code Hint
```scala
// Ensure the input raster is not empty and that numTilesX and numTilesY are positive integers.
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)
```

## API Test: `reshapeAverage`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def reshapeAverage[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, _numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the average method to determine the final value of each pixel. If one pixel in the answer overlaps multiple pixels in the source, their average is computed. This method should only be used when pixels represent continuous values, e.g., red, infrared, temperature, or vegetation. If the pixels represent categorical values, e.g., land type, then the nearest neighbor method [[reshapeNN]] should be used instead. @param raster the input raster that should be reshaped @param targetMetadataConv a function that returns the desired metadata for source metadata @param _numPartitions the number of partitions of the produces RDD. If not set, it will be the same as the input @return the new raster with the target metadata

### Goal
`reshapeAverage` reshapes a raster by converting its metadata and averaging pixel values when multiple source pixels overlap.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to contain continuous pixel values, such as temperature or vegetation indices.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, _numPartitions: Int`), default `0`: A function that takes the source raster's metadata and returns the desired target metadata. The `_numPartitions` parameter specifies the number of partitions for the resulting RDD; if not set, it defaults to the number of partitions of the input raster.

### Input
The input must be a `RasterRDD[T]` containing continuous pixel values, and the `targetMetadataConv` function must be defined to convert the source metadata to the desired target metadata. The input raster should be properly formatted and accessible.

### Output
Returns `RasterRDD[T]` — a new raster with the target metadata, where pixel values are averaged from the source raster based on the specified reshaping criteria.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata)
```

### LLM Instruction Prompt
- When calling `reshapeAverage`, ensure that the input raster contains continuous pixel values and that the target metadata conversion function is correctly defined.

### Prompt Snippet
```text
Use the `reshapeAverage` function to reshape a raster by averaging pixel values based on the specified target metadata.
```

### Common Failure Modes
- **[compile]** error: value copy is not a member of edu.ucr.cs.bdlab.beast.geolite.RasterMetadata _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the input raster is of a continuous type and the target metadata conversion function is correctly implemented.
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata)
```

## API Test: `reshapeNN`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
`reshapeNN` reshapes the input raster's metadata to match a specified target metadata using the nearest neighbor method for pixel value assignment.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster that should be reshaped. It is expected to be a distributed collection of raster tiles with pixel values of type `T`, such as `Int` or `Float`.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata, numPartitions: Int`), default `0`: A function that takes the source `RasterMetadata` and converts it to the target `RasterMetadata`. The `numPartitions` parameter specifies the number of partitions in the output RDD; if not set, the input raster's number of partitions is used.

### Input
The input must be a `RasterRDD[T]` loaded from a compatible raster format (e.g., GeoTIFF) and a function that defines how to convert the source raster's metadata to the desired target metadata. The input raster must be properly formatted and accessible.

### Output
Returns `RasterRDD[T]` — a new raster with the target metadata applied. The output retains the pixel type `T` and is suitable for further processing or saving in formats like GeoTIFF.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

### LLM Instruction Prompt
When calling `reshapeNN`, ensure that the input raster is a valid `RasterRDD[T]` and that the `targetMetadataConv` function is correctly defined to convert the raster's metadata.

### Prompt Snippet
```text
Use the `reshapeNN` function to reshape a raster's metadata to a target format using the nearest neighbor method for pixel value assignment.
```

### Common Failure Modes
- **[compile]** error: unknown parameter name: pixelWidth _(seen 2x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0 (TID 5) (192.168.68.50 executor driver): java.lan
- **[compile]** error: value xmin is not a member of edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

### Fix Code Hint
```scala
Ensure that the input raster is loaded correctly and that the `targetMetadataConv` function is defined to return valid metadata. Check the number of partitions if performance issues arise.
```

## API Test: `slidingWindow`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def slidingWindow[T: ClassTag, U: ClassTag](raster: RasterRDD[T], w: Int, f: (Array[T], Array[Boolean]) => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:711_

_Source doc:_ Performs a sliding window calculation for a window of size (2w + 1) &times; (2w + 1) given an integer value w. The user-defined window calculation function takes all values in the window ordered in row-major order. Additionally, a Boolean array of the same size is passed to indicate which values are defined and which are not. The Boolean array is useful for two scenarios. 1. When the window is near the edge of the raster, there must be some undefined values outside the raster. 2. Some pixel values in raster might be undefined, e.g., due to cloud coverage. *Note*: This function will only work correctly if all input tiles have the same raster metadata. @param raster the input raster to process @param w the radius of the square window. The window size will be (2w + 1) &times; (2w + 1) @param f the function to perform the calculation. @tparam T the type of values in the input raster @tparam U the type of output values (the result of the user-defined function). @return a new raster with the same dimensions as the input after applying the window function.

### Goal
The `slidingWindow` function computes a user-defined operation over a square window of pixel values in a raster, allowing for handling of undefined values.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster to process, which contains pixel values of type `T`. This raster must have consistent metadata across all tiles.
- `w` (`Int`): The radius of the square window. The total window size will be (2w + 1) &times; (2w + 1), meaning it will include `w` pixels in each direction from the center pixel.
- `f` (`(Array[T], Array[Boolean]) => U`): A user-defined function that takes an array of pixel values from the window and a corresponding Boolean array indicating which values are defined. It returns a value of type `U`, which represents the result of the calculation performed on the window.

### Input
The caller must provide a `RasterRDD` containing pixel values, an integer for the window radius, and a function that defines the operation to be performed on the pixel values. The input raster must have consistent metadata, and the pixel values should be of a type compatible with the specified type parameter `T`.

### Output
Returns `RasterRDD[U]` — a new raster with the same dimensions as the input raster, where each pixel value is the result of applying the user-defined function over the corresponding window.

### Valid Call Patterns
```scala
val smoothedRaster: RasterRDD[Double] = RasterOperationsFocal.slidingWindow(raster, 1, (values: Array[Int], defined) => {
  var sum: Int = 0
  var count: Int = 0
  for (i <- values.indices; if defined(i)) {
    sum += values(i)
    count += 1
  }
  sum.toDouble / count
})
```

### LLM Instruction Prompt
When calling `slidingWindow`, ensure that the raster input has consistent metadata, the window size is a positive integer, and the function provided correctly handles both defined and undefined pixel values.

### Prompt Snippet
```text
Call the slidingWindow function with a RasterRDD, a positive integer for the window size, and a function that processes an array of pixel values and a Boolean array indicating defined values.
```

### Common Failure Modes
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 14 in stage 2.0 failed 1 times, most recent failure: Lost task 14.0 in stage 2.0 (TID 44) (192.168.68.50 executor driver): java. _(seen 2x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 2.0 failed 1 times, most recent failure: Lost task 5.0 in stage 2.0 (TID 35) (192.168.68.50 executor driver): java.la _(seen 2x)_

### Fix Code Hint
```scala
Ensure that the raster has consistent metadata and that the window size is a positive integer. Verify that the user-defined function correctly processes both defined and undefined pixel values.
```
