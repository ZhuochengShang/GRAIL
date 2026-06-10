## API Test: `geoTiff[T]`

### Goal
Load one raster from an injected GeoTIFF path and validate its runtime pixel type.

### Inputs
- `inputA`: GeoTIFF path variable.
- `readType`: expected typed load such as `Int`, `Float`, `Array[Int]`, or `Array[Float]`.

### Valid Call Patterns
```scala
sc.geoTiff[Int](inputA)
sc.geoTiff[Int](inputA, 0)
sc.geoTiff[Int](inputA, 0, opts)
```

```scala
val probe = sc.geoTiff(inputA)
println("pixelType=" + probe.first().pixelType)
```

### LLM Instruction Prompt
- Use `geoTiff` only with provided raster path variables.
- Probe with `sc.geoTiff(path)` before choosing a typed load when later steps depend on numeric type.
- Compare `pixelType` against Spark SQL types such as `IntegerType`, `FloatType`, `DoubleType`, or `ArrayType`.
- Do not invent file paths, option names, or unsupported overloads.
- Prefer `first()` or `take(1)` for validation before `count()`.

### Prompt Snippet
```text
Use `geoTiff` to load the provided raster path.
If downstream code depends on type, inspect `first().pixelType` first and then choose the typed `sc.geoTiff[T](path)` call.
Do not compare pixel types to strings.
```

### Common Failure Modes
- Using a typed load that does not match the actual runtime pixel type.
- Comparing `pixelType` to string literals such as `"int32"`.
- Inventing a raster path instead of reusing the injected variable.

### Fix Code Hint
```scala
val probe = sc.geoTiff(inputA)
probe.first().pixelType match {
  case IntegerType => val raster: RasterRDD[Int] = sc.geoTiff[Int](inputA)
  case FloatType => val raster: RasterRDD[Float] = sc.geoTiff[Float](inputA)
  case other => throw new RuntimeException(s"Unsupported pixel type: $other")
}
```

## API Test: `shapefile`

### Goal
Load vector geometry from a shapefile path and reuse it in geometry-driven raster workflows.

### Inputs
- `vectorPath`: shapefile path variable.

### Valid Call Patterns
```scala
val vector: RDD[IFeature] = sc.shapefile(vectorPath)
val sample = vector.first()
println("geometry type=" + sample.getGeometry.getGeometryType)
```

### LLM Instruction Prompt
- Use `sc.shapefile(vectorPath)` for vector inputs needed by `raptorJoin` or `mask`.
- Treat the result as `RDD[IFeature]`.
- Access geometry with `feature.getGeometry`.
- Accept either normal shapefile inputs or zipped shapefile bundles.
- Prefer `first()` or `take(1)` for validation.

### Prompt Snippet
```text
Use `shapefile` when the workflow needs polygons or other vector features.
Load the injected vector path as `RDD[IFeature]` and reuse that variable in later geometry-driven raster steps.
```

### Common Failure Modes
- Inventing a custom vector loader instead of `sc.shapefile(...)`.
- Treating the loaded vector as a raster or scalar collection.

### Fix Code Hint
```scala
val vector: RDD[IFeature] = sc.shapefile(vectorPath)
val geomType = vector.first().getGeometry.getGeometryType
println("geometry type=" + geomType)
```

## API Test: `IFeature`

### Goal
Access geometry and attribute values from vector features loaded by `sc.shapefile(...)`.

### Relationship To Spark `Row`
- `IFeature` extends Spark SQL `Row`.
- Typed attribute access should use standard Row methods such as `getAs[T](fieldName)` when a field name is known.
- Geometry access should use `feature.getGeometry`.

### Valid Access Patterns
```scala
val vector: RDD[IFeature] = sc.shapefile(vectorPath)
val sample = vector.first()
println(sample.getGeometry.getGeometryType)
println(sample.getAs[String]("name"))
println(sample.getName(0))
println(sample.getDataType(0))
```

### LLM Instruction Prompt
- Treat `IFeature` as a Row-like feature object with geometry plus attributes.
- Use `feature.getGeometry` to access geometry.
- Use `feature.getAs[T](fieldName)` for attribute access when the field name is explicitly known.
- You may inspect field names with `feature.getName(i)` or data types with `feature.getDataType(i)`.
- Do not invent accessors such as `getAttribute(...)` or `getID(...)`.

### Prompt Snippet
```text
`IFeature` is Row-like. Use `feature.getGeometry` for geometry and `feature.getAs[T](fieldName)` for known attribute names.
Do not invent `getAttribute(...)` or `getID(...)`.
```

### Common Failure Modes
- Using invented methods such as `getAttribute(...)`.
- Using invented feature identifiers such as `getID(...)`.
- Treating `IFeature` as if it were only a geometry object without Row-style attributes.

### Fix Code Hint
```scala
val sample = vector.first()
val geom = sample.getGeometry
val zoneName = sample.getAs[String]("name")
println(geom.getGeometryType)
println(zoneName)
```

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

## API Test: `filterPixels`

### Goal
Filter raster cells with a Boolean predicate while preserving raster structure and explicit output typing.

### Inputs
- `inputA`: raster path variable.
- `readType`: raster read type.
- `nodataValue`: nodata sentinel or exclusion value used by the predicate.

### Valid Call Patterns
```scala
val in: RasterRDD[Float] = sc.geoTiff[Float](inputA)
val out: RasterRDD[Float] = in.filterPixels((v: Float) => v != -9999.0f)
println("filtered pixelType=" + out.first().pixelType)
```

### LLM Instruction Prompt
- Use `filterPixels` when the workflow needs a value-based raster filter rather than geometry-driven masking.
- Ensure the predicate returns `Boolean`.
- Declare the filtered raster type explicitly on assignment.
- Keep `filterPixels` as its own typed step before chaining more raster operations.
- Do not substitute `filterPixels` for vector masking; use `mask` or `raptorJoin` for geometry-aware workflows.

### Prompt Snippet
```text
Use `filterPixels` for value-based raster filtering only.
Write the predicate as an explicit Boolean lambda and assign the result to a typed `RasterRDD[T]`.
```

### Common Failure Modes
- Predicate lambda returns a non-Boolean value.
- Lambda parameter type is inferred incorrectly and causes a compile error.
- Chaining `filterPixels` directly into another raster op, hiding the failing call site.
- Using `filterPixels` when the task actually needs geometry-aware masking.

### Fix Code Hint
```scala
val in: RasterRDD[Float] = sc.geoTiff[Float](inputA)
val out: RasterRDD[Float] = in.filterPixels((v: Float) => v != -9999.0f)
```

## API Test: `flatten`

### Goal
Convert raster pixels to sample tuples for global statistics or joins.

### Inputs
- `inputA`: one raster path.
- `readType`: raster read type.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val hist = raster.flatten.map(_._4).countByValue().toMap
println("hist size=" + hist.size)
```

### LLM Instruction Prompt
- Use `flatten` when analytics needs pixel-level rows such as histograms or class percentages.
- Expect tuples shaped like `(x, y, RasterMetadata, value)`.
- Avoid invented tile helpers when `flatten` already exposes the values needed for analytics.

### Prompt Snippet
```text
Use `flatten` for pixel-level analytics such as counts, histograms, and percentages.
Materialize value tuples only when the workflow actually needs them.
```

### Common Failure Modes
- Using `flatten` inside validation-only sections when metadata inspection is enough.
- Inventing tuple shapes that do not match the returned value.

### Fix Code Hint
```scala
val hist = raster.flatten.map(_._4).countByValue().toMap
println(hist.size)
```

## API Test: `mask`

### Goal
Mask a raster by vector geometry while keeping a raster output.

### Relationship To `raptorJoin`
- `mask` is the raster-output companion to `raptorJoin`, not the same API surface.
- In RDPro internals, `mask` is implemented on top of the raptor join machinery and then cropped back to a raster result.
- Prefer `mask` when the output should remain `RasterRDD[T]`.
- Prefer `raptorJoin` when downstream logic needs per-feature or per-pixel joined records.

### Inputs
- `inputA`: raster path variable.
- `vectorInput`: vector path variable.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int](inputA)
val vector: RDD[IFeature] = sc.shapefile(vectorInput)
val maskedRaster: RasterRDD[Int] =
  raster.mask(vector, RasterOperationsLocal.NoDataValue)
```

### LLM Instruction Prompt
- Use `mask` for geometry-driven clipping or masking when the output remains a raster.
- Load vector geometry with `sc.shapefile(...)`.
- Pass a documented nodata sentinel such as `RasterOperationsLocal.NoDataValue`.
- Do not replace geometry masking with `mapPixels`.
- Treat `mask` as an accepted alias path for raster-shaped workflows that are otherwise related to `raptorJoin`.

### Prompt Snippet
```text
Use `raster.mask(vector, RasterOperationsLocal.NoDataValue)` for vector-driven masking.
Keep the raster output shape and avoid invented mask config symbols.
```

### Common Failure Modes
- Inventing mask option builders.
- Using value-only transforms instead of a geometry-aware mask.

### Fix Code Hint
```scala
val vector: RDD[IFeature] = sc.shapefile(vectorInput)
val masked: RasterRDD[Int] = raster.mask(vector, RasterOperationsLocal.NoDataValue)
```

## API Test: `raptorJoin`

### Goal
Match raster values to vector features and expose results through named fields.

### Relationship To `mask`
- `raptorJoin` is the canonical raster-vector matching API and returns joined records such as `RDD[RaptorJoinFeature[T]]`.
- `mask` is a related raster-output alias path built on top of the same join machinery, but it returns `RasterRDD[T]` instead of joined feature/value records.
- Use `raptorJoin` when analytics needs per-feature aggregation or joined samples.
- Use `mask` only when the intended output should remain raster-shaped.

### Inputs
- `rasterPath`: raster path variable.
- `vectorPath`: vector path variable.
- `valueType`: raster value type such as `Int` or `Float`.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int](rasterPath)
val vector: RDD[IFeature] = sc.shapefile(vectorPath)
val joined: RDD[RaptorJoinFeature[Int]] = raster.raptorJoin(vector)
val sample = joined.first()
println("sample value=" + sample.m)
println("sample geometry type=" + sample.feature.getGeometry.getGeometryType)
```

```scala
val masked: RasterRDD[Int] = raster.mask(vector, RasterOperationsLocal.NoDataValue)
```

### LLM Instruction Prompt
- Use `raptorJoin` when the workflow needs raster values associated with vector geometries.
- Load vectors with `sc.shapefile(...)`.
- Access joined output with named fields such as `m`, `feature`, `x`, and `y`.
- For geometry masking or clipping that should stay raster-shaped, prefer `raster.mask(vector, ...)`.
- Use documented nodata sentinels only.
- Do not describe `mask` and `raptorJoin` as identical return types; they share machinery but produce different output shapes.

### Prompt Snippet
```text
Use `raptorJoin` for raster-vector matching and use named fields on `RaptorJoinFeature`.
If the task is clip or mask by geometry, call `raster.mask(vector, RasterOperationsLocal.NoDataValue)`.
```

### Common Failure Modes
- Treating `RaptorJoinFeature` as a tuple.
- Inventing mask option objects or nodata constants.
- Using `mapPixels` for geometry-driven masking.

### Fix Code Hint
```scala
val joined: RDD[RaptorJoinFeature[Int]] = raster.raptorJoin(vector)
val sample = joined.first()
println(sample.m)
println(sample.feature.getGeometry.getGeometryType)
```

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

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int](inputRaster)
val warped: RasterRDD[Int] = RasterOperationsFocal.reshapeNN(raster, _ => targetMetadata)
println("same metadata=" + (warped.first().rasterMetadata == targetMetadata))
```

### LLM Instruction Prompt
- Use `reshape` operations when the raster grid or metadata must match a target raster.
- Create `targetMetadata` explicitly with `RasterMetadata.create(...)` when the target grid is derived from bounds and raster dimensions.
- Use the direct `new RasterMetadata(...)` constructor only when the affine transform is already known.
- Choose `reshapeNN` for categorical rasters.
- Choose `reshapeAverage` for continuous rasters.
- Verify output metadata against `targetMetadata`.
- Do not use `mapPixels` or `overlay` as substitutes for alignment.

### Prompt Snippet
```text
Use `reshapeNN` or `reshapeAverage` only when the workflow must match a target raster grid.
Build `targetMetadata` explicitly with `RasterMetadata.create(...)` when the target bounds and raster dimensions are known.
Use `new RasterMetadata(...)` only when the affine transform is already available.
Pick the method from raster semantics and verify the output metadata equals `targetMetadata`.
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
