## API Test: `mapPixels`

### Goal
Apply a deterministic per-pixel value transform while preserving raster geometry and metadata.

### Inputs
- `inputA`: raster path variable.
- `inType`: source pixel type.
- `outType`: mapped pixel type.

### Valid Call Patterns
```scala
val aRaw: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val aF: RasterRDD[Float] = aRaw.mapPixels(v => v.toFloat)
println("mapped pixelType=" + aF.first().pixelType)
```

### LLM Instruction Prompt
- Use `mapPixels` only for element-wise remapping.
- Declare the output raster type explicitly on assignment.
- Do not use `mapPixels` for geometry masking, reprojection, metadata alignment, or stacking rasters.
- If the source raster type is unknown, inspect `pixelType` before mapping.

### Prompt Snippet
```text
Use `mapPixels` for deterministic element-wise value conversion.
Keep the same raster grid and return a clearly typed `RasterRDD[U]`.
```

### Common Failure Modes
- Using `mapPixels` for geometry-driven masking or alignment.
- Leaving the output type implicit when the mapping changes numeric type.

### Fix Code Hint
```scala
val in: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val out: RasterRDD[Float] = in.mapPixels(v => v.toFloat)
```
