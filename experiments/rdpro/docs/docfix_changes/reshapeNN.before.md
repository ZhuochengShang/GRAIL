## API Test: `reshapeNN`

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
Reshape a distributed raster to new target metadata (CRS/grid/resolution/extent/tiling) using nearest-neighbor pixel assignment.

### Parameters
- `raster` (`RasterRDD[T]`): Input raster to reshape.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata,
                             numPartitions: Int`), default `0`: A metadata-conversion function from source `RasterMetadata` to target `RasterMetadata`; `numPartitions` controls output partition count (0 means use input partition count).

### Input
- A `RasterRDD[T]` already loaded in RDPro (for example from GeoTIFF/HDF workflows).
- A target metadata conversion function that returns the desired output `RasterMetadata`.
- Type parameter `T` must match the runtime pixel type when loading rasters (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- This is a low-level reshape primitive; it can perform reproject/regrid/rescale/subset in one step.
- Nearest-neighbor behavior: each target pixel is copied from nearest source pixel; if nearest source is empty or outside source raster range, target pixel is empty.

### Output
Returns `RasterRDD[T]` — a new raster RDD with target metadata and nearest-neighbor sampled pixel values.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

### LLM Instruction Prompt
- Use receiver form exactly as documented: `RasterOperationsFocal.reshapeNN(raster, ...)`.
- Pass a `RasterRDD[T]` and a metadata conversion argument in the second position.
- Keep pixel type consistent with source raster load type.
- Use `reshapeNN` for categorical/general nearest-neighbor reshaping; do not switch to averaging semantics.
- Do not invent extra parameters or alternate signatures.

### Prompt Snippet
```text
Given a RasterRDD[T], call RasterOperationsFocal.reshapeNN(raster, targetMetadataConv, numPartitions).
Use nearest-neighbor semantics and keep T consistent with the raster’s actual pixel type.
If numPartitions is omitted, output partitions default to input partition count.
```

### Common Failure Modes
- Loading raster with wrong type parameter `T` (pixel type mismatch).
- Passing a non-conversion second argument shape (must match metadata conversion usage expected by API/signature).
- Expecting interpolation/averaging behavior from `reshapeNN` (it is nearest neighbor only).
- Assuming out-of-range or empty source pixels will be filled; they remain empty in output.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

val reshaped: RasterRDD[Int] = RasterOperationsFocal.reshapeNN(
  raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100)
  // optional third arg: numPartitions
)

reshaped.saveAsGeoTiff("glc_ca")
```