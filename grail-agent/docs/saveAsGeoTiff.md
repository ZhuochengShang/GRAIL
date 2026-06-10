## API Test: `saveAsGeoTiff`

### Goal
Write the final raster output to a GeoTIFF path using documented writer options.

### Inputs
- `inputA`: source raster path variable.
- `readType`: source raster type.
- `output`: output GeoTIFF path variable.

### Valid Call Patterns
```scala
val inRaw: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val in: RasterRDD[Float] = inRaw.mapPixels(v => v.toFloat)
in.saveAsGeoTiff(output, Seq(GeoTiffWriter.Compression -> TiffConstants.COMPRESSION_LZW))
```

```scala
raster.saveAsGeoTiff(output, GeoTiffWriter.WriteMode -> "compatibility")
raster.saveAsGeoTiff(output, GeoTiffWriter.WriteMode -> "distributed")
```

### LLM Instruction Prompt
- Use `saveAsGeoTiff` only on the final raster output.
- Write to the injected output path variable.
- Convert numeric pixel values before writing if the workflow expects a different output type.
- Use documented writer options only, such as `Compression`, `WriteMode`, `CompactBits`, and `BitsPerSample`.
- Do not invent writer modes or option keys.

### Prompt Snippet
```text
Use `saveAsGeoTiff` at the end of the pipeline with the provided output path.
If needed, map pixels to the desired numeric type before writing and pass only documented writer options.
```

### Common Failure Modes
- Writing intermediate rasters instead of the final result.
- Inventing writer options or output paths.
- Using `CompactBits` on non-integer rasters.

### Fix Code Hint
```scala
val out: RasterRDD[Float] = inRaw.mapPixels(v => v.toFloat)
out.saveAsGeoTiff(output, Seq(GeoTiffWriter.Compression -> TiffConstants.COMPRESSION_LZW))
```
