## API Test: `overlay`

### Goal
Stack two aligned rasters into an array-valued raster.

### Inputs
- `inputA`, `inputB`: raster path variables.
- `targetType`: expected array-valued output type.

### Valid Call Patterns
```scala
val aRaw: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val bRaw: RasterRDD[Int] = sc.geoTiff[Int](inputB)
val a: RasterRDD[Float] = aRaw.mapPixels(v => v.toFloat)
val b: RasterRDD[Float] = bRaw.mapPixels(v => v.toFloat)
val aMeta = a.first().rasterMetadata
val bAligned: RasterRDD[Float] =
  if (b.first().rasterMetadata == aMeta) b else RasterOperationsFocal.reshapeNN(b, _ => aMeta)
val stacked: RasterRDD[Array[Float]] = a.overlay(bAligned)
```

### LLM Instruction Prompt
- Use `overlay` only after raster metadata matches.
- If metadata differs, align first with `reshapeNN` or another documented reshape step.
- If numeric pixel types differ, convert explicitly with `mapPixels` before overlay.
- Expect an array-valued output such as `RasterRDD[Array[Float]]`.

### Prompt Snippet
```text
Before `overlay`, compare `rasterMetadata` for both rasters.
Align metadata first, convert numeric types if needed, then call `a.overlay(b)`.
```

### Common Failure Modes
- Overlaying rasters with mismatched metadata.
- Overlaying rasters with incompatible pixel types.
- Forgetting that the output is array-valued.

### Fix Code Hint
```scala
val aMeta = a.first().rasterMetadata
val bAligned =
  if (b.first().rasterMetadata == aMeta) b else RasterOperationsFocal.reshapeNN(b, _ => aMeta)
val stacked: RasterRDD[Array[Float]] = a.overlay(bAligned)
```
