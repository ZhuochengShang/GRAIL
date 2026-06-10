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
