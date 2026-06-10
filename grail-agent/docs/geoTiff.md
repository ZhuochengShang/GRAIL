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
