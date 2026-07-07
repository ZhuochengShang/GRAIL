# RasterOperationsLocal

_The `explode` function separates each tile in a `RasterRDD` into its own individual raster, allowing for more granular processing of raster data._

**Receiver:** static object — call `RasterOperationsLocal.<method>(...)`

**Members** (most robust first): ★ `explode` **(primary)**, ★ `filterPixels`, ★ `mapPixels`, ★ `overlay`

---

## API Test: `explode`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def explode: RasterRDD[T]
def explode[T](inputRaster: RasterRDD[T]): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:76  (+1 more definition site/overload)_

_Source doc:_ Returns a new RasterRDD where each tile is in its own raster. @param inputRaster the raster data to explore @tparam T @return a new raster RDD with the same number of tiles but each tile is in a separate raster

### Goal
The `explode` function separates each tile in a `RasterRDD` into its own individual raster, allowing for more granular processing of raster data.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster data that contains multiple tiles. Each tile will be extracted into a separate raster in the output.

### Input
The caller must provide a `RasterRDD[T]` that contains raster data, which can be loaded from formats such as GeoTIFF or HDF. The input raster must be properly formatted and accessible within the Spark environment.

### Output
Returns `RasterRDD[T]` — A new raster RDD where each tile from the input raster is represented as a separate raster. The output maintains the same pixel type as the input.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsLocal.explode(raster)
```

### LLM Instruction Prompt
- When calling `explode`, ensure that the input is a valid `RasterRDD[T]` containing raster data. The output will be a new `RasterRDD[T]` with each tile as a separate raster.

### Prompt Snippet
```text
To use the explode function, provide a RasterRDD containing multiple tiles. The output will be a RasterRDD where each tile is in its own raster.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the input raster is loaded correctly and contains multiple tiles before calling explode. For example:
val raster: RasterRDD[Int] = sc.geoTiff("path_to_your_geotiff.tif")
val outputRaster = RasterOperationsLocal.explode(raster)
```

## API Test: `filterPixels`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def filterPixels(f: T => Boolean)
def filterPixels[T: ClassTag](inputRaster: RasterRDD[T], filter: T => Boolean): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:48  (+1 more definition site/overload)_

_Source doc:_ Retains only the pixels that pass the user-defined filter and clears all other pixels (set to empty) @param inputRaster the input raster @param filter the filter function that tells which pixel values to keep in the output @tparam T the type of the pixels in the input @return a new raster where only pixels that pass the test are retained

### Goal
`filterPixels` retains only the pixels in a raster that meet a specified condition, effectively filtering out unwanted pixel values.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster dataset containing pixel values of type `T`. This raster is processed to retain only those pixels that satisfy the filter condition.
- `filter` (`T => Boolean`): A user-defined function that takes a pixel value of type `T` and returns a Boolean indicating whether the pixel should be retained (`true`) or cleared (`false`).

### Input
The caller must provide a `RasterRDD[T]` containing pixel data, which can be loaded from formats such as GeoTIFF or HDF. The pixel type `T` must be compatible with the data being processed (e.g., `Int`, `Float`, `Short`). The filter function must be defined to operate on the specific pixel type.

### Output
Returns `RasterRDD[T]` — a new raster dataset where only the pixels that pass the filter condition are retained, and all other pixels are set to empty. The output retains the same pixel type as the input raster.

### Valid Call Patterns
```scala
val inputRaster: RasterRDD[Short] = sparkContext.parallelize(Seq(inputTile))
val outputRaster: RasterRDD[Short] = inputRaster.filterPixels((x: Short) => x < 50)
```

### LLM Instruction Prompt
- When calling `filterPixels`, ensure that the input raster is of the correct type and that the filter function is appropriately defined for the pixel type.

### Prompt Snippet
```text
val filteredRaster = inputRaster.filterPixels(pixelValue => pixelValue > threshold)
```

### Common Failure Modes
- **[compile]** error: value toArray is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Float]

### Fix Code Hint
```scala
// Ensure the filter function is defined correctly for the pixel type
val outputRaster: RasterRDD[Float] = temperatureK.filterPixels(_ > 300)
```

## API Test: `mapPixels`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def mapPixels[U: ClassTag](f: T => U)
def mapPixels[T: ClassTag, U: ClassTag](inputRaster: RasterRDD[T], f: T => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38  (+1 more definition site/overload)_

_Source doc:_ Apply a user-defined function for each pixel in the input raster to produce the output raster @param inputRaster the input raster RDD @param f the function to apply on each input pixel value to produce the output pixel value @tparam T the type of pixels in the input @tparam U the type of pixels in the output @return the resulting RDD

### Goal
`mapPixels` applies a user-defined function to each pixel in the input raster, transforming the pixel values and producing a new raster with the transformed values.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The input raster represented as a distributed collection of raster tiles, where each tile contains pixel values of type `T`.
- `f` (`T => U`): A function that takes a pixel value of type `T` and returns a transformed pixel value of type `U`.

### Input
The caller must provide a `RasterRDD[T]` containing the raster data, which can be loaded from formats such as GeoTIFF or HDF. The pixel type `T` must be compatible with the data being processed (e.g., `Int`, `Float`, etc.).

### Output
Returns `RasterRDD[U]` — a new raster represented as a distributed collection of raster tiles, where each tile contains transformed pixel values of type `U`.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
```

### LLM Instruction Prompt
- Ensure that the input raster is of the correct type and format before calling `mapPixels`. The function `f` must be defined to handle the pixel type `T` and return a value of type `U`.

### Prompt Snippet
```text
Transform the pixel values of the input raster using a user-defined function with `mapPixels`.
```

### Common Failure Modes
- **[compile]** error: not found: value mapPixels _(seen 8x)_
- **[compile]** error: value geoTiff is not a member of org.apache.spark.SparkContext _(seen 4x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0 (TID 5) (192.168.68.50 executor driver): org.apac _(seen 4x)_
- **[compile]** error: not found: value sparkContext _(seen 4x)_
- **[compile]** error: object dynoviz is not a member of package edu.ucr.cs.bdlab _(seen 4x)_
- **[runtime]** org.apache.spark.SparkException: Job aborted due to stage failure: Task 7 in stage 0.0 failed 1 times, most recent failure: Lost task 7.0 in stage 0.0 (TID 7) (192.168.68.50 executor driver): org.apac _(seen 3x)_

### Fix Code Hint
```scala
Ensure that the input raster is loaded correctly and that the function `f` is defined to handle all possible pixel values of type `T`.
```

## API Test: `overlay`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def overlay[V](rasters: RasterRDD[T]*)
def overlay[T: ClassTag, V](@varargs inputs: RDD[ITile[T]]*)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96  (+1 more definition site/overload)_

_Source doc:_ Overlays this raster RDD on top other ones @param rasters the other rasters to stack this raster on @return a new RasterRDD which contains the stack of this raster on top of the given ones

### Goal
The `overlay` function combines multiple raster datasets into a single raster dataset by stacking them on top of each other, allowing for complex geospatial analyses.

### Parameters
- `rasters` (`RasterRDD[T]*`): One or more raster datasets that will be stacked on top of the calling raster dataset. Each raster must be of the same pixel type and compatible in terms of spatial resolution and coordinate reference system (CRS).

### Input
The caller must provide:
- Raster datasets loaded as `RasterRDD` objects, which can be obtained from GeoTIFF files or other supported formats.
- All input rasters must have the same pixel type and be aligned in terms of spatial resolution and CRS to ensure proper overlaying.

### Output
Returns a new `RasterRDD` that represents the stacked raster datasets. The output format is a `RasterRDD[Array[T]]`, where each pixel value is an array containing the values from the input rasters at that pixel location.

### Valid Call Patterns
```scala
val raster1: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val raster2: RasterRDD[Int] = sc.geoTiff[Int]("vegetation")
val stacked: RasterRDD[Array[Int]] = raster1.overlay(raster2)
```

### LLM Instruction Prompt
- When calling `overlay`, ensure that all input rasters are of the same pixel type and are compatible in terms of spatial resolution and CRS. 

### Prompt Snippet
```text
To overlay multiple rasters, use the `overlay` method on a `RasterRDD` instance, passing in other `RasterRDD` instances as arguments. Ensure that all rasters have the same pixel type and are aligned spatially.
```

### Common Failure Modes
- **[runtime]** java.lang.ClassCastException: class java.lang.Float cannot be cast to class java.lang.Integer (java.lang.Float and java.lang.Integer are in module java.base of loader 'bootstrap') _(seen 2x)_
- **[compile]** error: value forall is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Array[Float]]

### Fix Code Hint
```scala
Ensure that all input rasters are loaded with the same pixel type and are aligned in terms of resolution and CRS before calling the `overlay` method.
```
