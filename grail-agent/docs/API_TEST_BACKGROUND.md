# RDPro API Test Background

## Runtime contract (must be runnable)
- Use spark-shell Scala code.
- Include imports, one `object`, and `def run(sc: SparkContext): Unit`.
- Include at least one action: `count`, `first`, or `saveAsGeoTiff`.
- Use concrete local paths (or known HDFS/S3 URIs).

## Core data model
- `RasterRDD[T]`: distributed raster tiles with value type `T`.
- `ITile[T]`: one tile; values retrieved by `getPixelValue`.
- `pixelType`: runtime Spark SQL type of pixels (`IntegerType`, `FloatType`, `ArrayType(...)`).
- `numComponents`: number of bands/components in each pixel.

## Metadata/alignment requirements
- `overlay` requires matching raster metadata:
  - CRS/SRID
  - extent
  - resolution
  - tile layout
- If mismatch exists, align first (`reshape*`, `reproject`, `rescale`).

## Type safety rules for tests
- Do not assume `sc.geoTiff[T]` always physically converts source pixels.
- Before `overlay` and `saveAsGeoTiff`, print/check:
  - `r.first().pixelType`
  - `r.first().numComponents`
- If mixed numeric types, normalize explicitly:
  - scalar: `r.mapPixels(v => v.toFloat)` (or `toInt`)
  - array: `r.mapPixels(vs => vs.map(_.toFloat))`

## Standard debug prints
- `println("A pixelType=" + a.first().pixelType)`
- `println("A numComponents=" + a.first().numComponents)`
- `println("A count=" + a.count())`

## Common failure patterns
- `Int cannot be cast to Float`:
  - Cause: mixed runtime pixel types in stack/overlay/write path.
  - Fix: read as source type, then explicit `mapPixels` conversion to one target type.
- `Task not serializable`:
  - Cause: non-serializable closure/object captured in Spark action.
  - Fix: keep closures simple; avoid capturing non-serializable values.
