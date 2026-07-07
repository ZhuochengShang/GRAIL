# GeoTiffWriter

_The `saveAsGeoTiff` function saves a distributed raster dataset (RDD of tiles) to a GeoTIFF file format, enabling the output of processed geospatial raster…_

**Receiver:** instance — obtain a `GeoTiffWriter` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `saveAsGeoTiff` **(primary)**, ⚠️ `count`

---

## API Test: `saveAsGeoTiff`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit
def saveAsGeoTiff[T](rasterRDD: RDD[ITile[T]], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:476  (+1 more definition site/overload)_

### Goal
The `saveAsGeoTiff` function saves a distributed raster dataset (RDD of tiles) to a GeoTIFF file format, enabling the output of processed geospatial raster data.

### Parameters
- `rasterRDD` (`RDD[ITile[T]]`): The input raster data represented as a distributed collection of tiles. Each tile contains pixel data of type `T`, which can be an integer, float, or other supported types.
- `outPath` (`String`): The file path where the output GeoTIFF will be saved. This path must be accessible and writable by the Spark job.
- `opts` (`BeastOptions`): Options for saving the GeoTIFF, such as compression settings or metadata configurations. This parameter allows customization of the output file's properties.

### Input
The caller must provide:
- A valid `RDD[ITile[T]]` containing the raster data to be saved.
- A string representing a valid file path for the output GeoTIFF.
- An instance of `BeastOptions` to specify any additional options for the saving process.

### Output
Returns `Unit` — indicating that the operation has completed successfully. The output is a GeoTIFF file saved at the specified `outPath`.

### Valid Call Patterns
```scala
val rasterFile = locateResource("/raptor/glc2000_small.tif")
val rasterRDD = new RasterFileRDD(sparkContext, rasterFile.getPath, IRasterReader.RasterLayerID -> 0)
GeoTiffWriter.saveAsGeoTiff(rasterRDD, "output_path/glc.tif", GeoTiffWriter.BitsPerSample -> 8)
```

### LLM Instruction Prompt
- When calling `saveAsGeoTiff`, ensure that the `rasterRDD` is properly initialized and contains valid raster data. The `outPath` must be a writable path, and `opts` should be configured as needed for the output file.

### Prompt Snippet
```text
To save your raster data as a GeoTIFF, use the `saveAsGeoTiff` method with the appropriate raster RDD, output path, and options.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the output path is valid and writable
val outputPath = "output_path/glc.tif"
if (new File(outputPath).canWrite) {
    GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputPath, new BeastOptions)
} else {
    throw new IOException("Output path is not writable.")
}
```

## API Test: `count`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def count: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860_

### Goal
The `count` function returns the number of elements in the raster dataset, providing a measure of the dataset's size in terms of pixel count.

### Parameters
_None._

### Input
The caller must provide a raster dataset that has been loaded into an appropriate RDD structure. The dataset should be in a compatible format, such as GeoTIFF, and must be accessible within the Spark context.

### Output
Returns `Int` — the value represents the total number of pixels in the raster dataset.

### Valid Call Patterns
```scala
val pixelCount: Int = raster.count
```

### LLM Instruction Prompt
- Ensure that the raster dataset is properly loaded and accessible in the Spark context before calling `count`.

### Prompt Snippet
```text
To get the total number of pixels in the raster dataset, use the count method: val pixelCount: Int = raster.count
```

### Common Failure Modes
- **[compile]** error: type mismatch; _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the raster dataset is loaded correctly before calling count
val raster: RDD[ITile[Int]] = sc.geoTiff("path_to_your_geotiff.tif")
val pixelCount: Int = raster.count
```
