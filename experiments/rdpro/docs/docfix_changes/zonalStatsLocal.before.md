## API Test: `zonalStatsLocal`

### Signature
```scala
def zonalStatsLocal[T](geometries: Array[Geometry], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
def zonalStatsLocal[T](zones: Array[IFeature], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:162  (+1 more definition site/overload)_

_Source doc:_ Run zonal statistics locally in one thread. This is useful when the array of geometries is small and the overhead of partitioning could be high. @param zones the array of features that describe the zones. @param raster the raster reader that points to the raster file being aggregated @param collectorClass the class that computes the statistics @return an array of collectors that is equal in length to the input array of features with the result for each. Features that do not overlap any pixels will have null.

### Goal
Compute zonal statistics for a small in-memory set of zones against a raster using a single-thread local execution path.

### Parameters
- `geometries` (`Array[Geometry]`): Zone geometries to aggregate raster pixels over (for the `Geometry` overload).
- `raster` (`IRasterReader[T]`): An initialized raster reader pointing to the raster to aggregate.
- `collectorClass` (`Class[_ <: Collector]`): Collector implementation class that defines which statistics are computed (for example, `classOf[Statistics]` in tests).

### Input
Provide:
- An array of zones (`Array[Geometry]` or `Array[IFeature]` depending on overload).
- An `IRasterReader[T]` that is already initialized and readable.
- A collector class extending `Collector`.

Preconditions and compatibility notes from project context:
- This method is intended for **small arrays of zones** (local, one-thread execution).
- If your raster source is GeoTIFF loaded elsewhere in RDPro, keep type selection consistent with pixel type (`Int`, `Float`, `Array[Int]`, `Array[Float]`) when constructing/using raster readers in your pipeline.
- The method returns per-zone results aligned with input order; non-overlapping zones produce `null`.

### Output
Returns `Array[Collector]`:
- Length matches the input zones length.
- Each position contains that zone’s aggregation result as a `Collector`.
- Zones that do not overlap raster pixels have `null` in their corresponding position.

### Valid Call Patterns
```scala
val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
  .filter(_ != null)
```

### LLM Instruction Prompt
- Use the receiver exactly as `ZonalStatistics.zonalStatsLocal(...)` when following the verified test call form.
- Pass arguments in this order: `(zones/geometries array, raster reader, collector class)`.
- Ensure `raster` is an `IRasterReader[T]` (initialized before call).
- Handle possible `null` entries in returned `Array[Collector]` for non-overlapping zones.
- Do not invent extra parameters (no Spark partition args, no output path, no options map).

### Prompt Snippet
```text
Call ZonalStatistics.zonalStatsLocal with exactly three arguments:
1) Array[IFeature] or Array[Geometry] zones,
2) initialized IRasterReader[T],
3) Class[_ <: Collector] (e.g., classOf[Statistics]).
Then filter null collectors because zones with no overlapping pixels return null.
```

### Common Failure Modes
- Passing a non-initialized `IRasterReader[T]`.
- Using a collector class that is not a subtype of `Collector`.
- Assuming all returned entries are non-null (non-overlapping zones return `null`).
- Using this local API for very large zone arrays where distributed partitioned workflows are more appropriate.

### Fix Code Hint
```scala
val zsResults: Array[Collector] =
  ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])

val nonNull: Array[Collector] = zsResults.filter(_ != null)
```