# `reshapeAverage`: g1 README vs fixed README

## G1 README entry

## API Test: `reshapeAverage`

### Signature
```scala
def reshapeAverage[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, _numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the average method to determine the final value of each pixel. If one pixel in the answer overlaps multiple pixels in the source, their average is computed. This method should only be used when pixels represent continuous values, e.g., red, infrared, temperature, or vegetation. If the pixels represent categorical values, e.g., land type, then the nearest neighbor method [[reshapeNN]] should be used instead. @param raster the input raster that should be reshaped @param targetMetadataConv a function that returns the desired metadata for source metadata @param _numPartitions the number of partitions of the produces RDD. If not set, it will be the same as the input @return the new raster with the target metadata

### Goal
Reshape a raster to new metadata (CRS/grid/resolution/extent) using **average resampling** so overlapping source pixels are averaged into each output pixel.

### Parameters
- `raster` (`RasterRDD[T]`): Input raster RDD to reshape.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata,
                                  _numPartitions: Int`), default `0`: Function that maps source metadata to the desired target metadata; `_numPartitions` controls output partition count (default `0` means keep input partitioning behavior per source doc).

### Input
- A `RasterRDD[T]` (e.g., GeoTIFF/HDF loaded into RDPro types).
- A metadata conversion function `RasterMetadata => RasterMetadata` that defines target CRS/grid/resolution/extent.
- **Precondition:** use this method for **continuous numeric rasters** (e.g., temperature, reflectance, vegetation indices), because values are aggregated by averaging overlaps.
- **Compatibility/type rule:** choose raster load type to match real pixel type (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`) before reshape; mismatched load type is a separate upstream failure mode.
- For categorical rasters (e.g., land cover classes), use `reshapeNN` instead of `reshapeAverage`.

### Output
Returns `RasterRDD[T]` — a new raster with target metadata applied (potentially reprojected/regridded/rescaled/subset), with pixel values computed via average where output pixels overlap multiple input pixels.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)
```

### LLM Instruction Prompt
- Call with receiver/qualifier exactly as verified: `RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)`.
- Provide a `targetMetadataConv` function, not raw metadata.
- Use only for continuous-value rasters; for categorical labels, switch to `reshapeNN`.
- Keep generic type `T` consistent with the raster’s actual pixel type selected at load time.

### Prompt Snippet
```text
Use RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata) to reshape a continuous raster by averaging overlaps. Do not use it for categorical classes; use reshapeNN there. Ensure RasterRDD[T] pixel type matches the source raster type.
```

### Common Failure Modes
- Using `reshapeAverage` on categorical data (land-cover classes) causes invalid mixed class values.
- Passing metadata directly instead of a function (`RasterMetadata => RasterMetadata`) does not match the API shape.
- Loading raster with wrong type parameter (`sc.geoTiff[T]` mismatch) leads to incorrect/failed downstream processing.
- Expecting this low-level function to be the primary user API; source docs state it is low-level and usually wrapped by higher-level ops.

### Fix Code Hint
```scala
// Correct call shape (from tests)
val targetMetadata = sourceMetadata.rescale(10, 10)
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)

// If raster is categorical, use nearest-neighbor instead
// val outputRaster = RasterOperationsFocal.reshapeNN(inputRaster, _=>targetMetadata)
```


---

## Fixed README entry

## API Test: `reshapeAverage`
_Grounding: doc-repaired from source (docfix)._

### Goal
Reshape a continuous-value raster to new metadata (CRS/grid/resolution/extent) using average resampling. Overlapping source pixels are averaged into each output pixel.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal` (Scala object; reference directly)
- `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala class; reference as `classOf[RasterMetadata]` or instantiate directly)

**Correct Call Sketch:**
```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

val reshaped = RasterOperationsFocal.reshapeAverage(
  rasterRDD,
  meta => new RasterMetadata(
    meta.x1, meta.y1, meta.x2, meta.y2,
    meta.tileWidth, meta.tileHeight,
    meta.srid, meta.g2m
  )
)

val n = reshaped.count()
require(n > 0, "empty result for reshapeAverage")
```

### LLM Instruction Prompt
- `RasterRDD` is an RDD; do not attempt to access `.rasterFeature` or `.rasterMetadata` directly on it.
- Do not pre-compute target metadata outside the function call. The `targetMetadataConv` parameter is a function `RasterMetadata => RasterMetadata`. You must use this lambda to derive and return the new `RasterMetadata` dynamically.
- `RasterRDD[T]` elements are tile objects, not tuples. Do not attempt to access `._2` on them when sampling the result.
- Use only for continuous-value rasters (e.g., temperature, vegetation). For categorical labels, use `reshapeNN`.

### Prompt Snippet
```text
Use RasterOperationsFocal.reshapeAverage(rasterRDD, meta => new RasterMetadata(...)) to reshape continuous rasters. Do not access .rasterMetadata on the RasterRDD itself. Transform metadata inside the lambda. RasterRDD elements are tiles, not tuples (no ._2).
```

### Common Failure Modes
- **Attempting to access `.rasterFeature.rasterMetadata` directly on a `RasterRDD`** to pre-compute target metadata. `RasterRDD` is an RDD and lacks this property.
- **Pre-computing `targetMetadata` outside the function** using an undefined `sourceMetadata` variable, rather than transforming it inside the `RasterMetadata => RasterMetadata` lambda.
- **Attempting to access `._2` on `RasterRDD[T]` elements** when sampling. Elements are tile objects, not tuples.
- **Using `reshapeAverage` on categorical data** (land-cover classes), which causes invalid mixed class values.

### Fix Code Hint
**WRONG:**
```scala
// Fails: RasterRDD has no .rasterMetadata property, and pre-computing outside is invalid
val sourceMetadata = rasterRDD.rasterMetadata 
val targetMetadata = sourceMetadata.rescale(10, 10)
val outputRaster = RasterOperationsFocal.reshapeAverage(rasterRDD, _ => targetMetadata)

// Fails: RasterRDD elements are tiles, not tuples
val sample = outputRaster.first()._2
```

**CORRECT:**
```scala
// Transform metadata dynamically inside the lambda
val outputRaster = edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.reshapeAverage(
  rasterRDD,
  meta => new edu.ucr.cs.bdlab.beast.geolite.RasterMetadata(
    meta.x1, meta.y1, meta.x2, meta.y2,
    meta.tileWidth, meta.tileHeight,
    meta.srid, meta.g2m
  )
)

// RasterRDD elements are tile objects directly
val sampleTile = outputRaster.first()
```

