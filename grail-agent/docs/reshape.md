## API Test: `reshape`

### Goal
Warp a raster to a target grid and verify the output metadata matches that target.

### Inputs
- `inputRaster`: source raster path variable.
- `targetMetadata`: target `RasterMetadata`.
- `method`: `reshapeNN` or `reshapeAverage`.

### How To Create `targetMetadata`
Use `RasterMetadata.create(xmin, ymax, xmax, ymin, srid, rasterWidth, rasterHeight, tileWidth, tileHeight)` when you need a target grid from explicit bounds and raster dimensions.

```scala
val targetMetadata: RasterMetadata =
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100)
```

Use the constructor only when you already have the affine transform:

```scala
val metadata = new RasterMetadata(
  0, 0, 360, 180,
  90, 90,
  4326,
  new AffineTransform(1, 0, 0, -1, -180, 90)
)
```

Grounding:
- `RasterMetadata` constructor fields are defined in `RDPro_log/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala`
- `RasterMetadata.create(...)`, `rescale(...)`, and `reproject(...)` usage appears in `RDPro_log/cg/src/test/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadataTest.scala`

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int](inputRaster)
val warped: RasterRDD[Int] = RasterOperationsFocal.reshapeNN(raster, _ => targetMetadata)
println("same metadata=" + (warped.first().rasterMetadata == targetMetadata))
```

### LLM Instruction Prompt
- Use `reshape` operations when the raster grid or rasterMetadata must match a target raster.
- Create `targetMetadata` explicitly with `RasterMetadata.create(...)` when the target grid is derived from bounds and raster dimensions.
- Use the direct `new RasterMetadata(...)` constructor only when the affine transform is already known.
- Choose `reshapeNN` for categorical rasters.
- Choose `reshapeAverage` for continuous rasters.
- Verify output rasterMetadata against `targetMetadata`.
- Do not use `mapPixels` or `overlay` as substitutes for alignment.

### Prompt Snippet
```text
Use `reshapeNN` or `reshapeAverage` only when the workflow must match a target raster grid.
Build `targetMetadata` explicitly with `RasterMetadata.create(...)` when the target bounds and raster dimensions are known.
Use `new RasterMetadata(...)` only when the affine transform is already available.
Pick the method from raster semantics and verify the output rasterMetadata equals `targetMetadata`.
```

### Common Failure Modes
- Using `reshapeNN` for continuous data that should be averaged.
- Skipping metadata validation after reshape.
- Using value transforms instead of a reshape step for alignment.

### Fix Code Hint
```scala
val warped: RasterRDD[Float] =
  RasterOperationsFocal.reshapeAverage(raster, _ => targetMetadata)
println(warped.first().rasterMetadata == targetMetadata)
```
