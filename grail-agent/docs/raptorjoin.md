## API Test: `raptorJoin`

### Goal
Match raster values to vector features and expose results through named fields.

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
- Treat `feature` as an `IFeature` / Row-like object. Use `feature.getGeometry` for geometry and `feature.getAs[T](fieldName)` for known attributes.
- Do not invent feature accessors such as `getAttribute(...)` or `getID(...)`.
- For geometry masking or clipping that should stay raster-shaped, prefer `raster.mask(vector, ...)`.
- Use documented nodata sentinels only.

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
