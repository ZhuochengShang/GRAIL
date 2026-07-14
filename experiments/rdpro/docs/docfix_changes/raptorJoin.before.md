## API Test: `raptorJoin`

### Signature
```scala
def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)
def raptorJoin[T](vectors: JavaSpatialRDD, rasters: JavaRasterRDD[T], opts: BeastOptions): JavaRDD[RaptorJoinFeature[T]]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:269  (+1 more definition site/overload)_

_Source doc:_ Performs a raster X vector join (Raptor join) between the two given RDDs. @param vectors the set of vector features @param rasters the set of raster tiles @param opts additional options for the algorithm @return the intersection between the feature vectors and all raster pixels.

### Goal
Run a distributed raster–vector overlap join (Raptor) to return all feature/pixel intersections, enabling zonal-style analysis such as per-polygon raster aggregation.

### Parameters
- `vectors` (`JavaSpatialRDD`): the vector features to join against raster pixels (points/lines/polygons are supported by Raptor semantics in project docs).
- `rasters` (`JavaRasterRDD[T]`): the raster tiles to be joined; `T` is the raster pixel value type.
- `opts` (`BeastOptions`): additional algorithm/configuration options for the join.

### Input
Caller must provide:
- A vector RDD (`SpatialRDD` / `JavaSpatialRDD`) and a raster RDD (`RasterRDD` / `JavaRasterRDD[T]`).
- Raster data typically loaded from RDPro-supported formats (GeoTIFF or HDF), and vector data from Beast-supported spatial formats (e.g., Shapefile/GeoJSON), before calling `raptorJoin`.

Preconditions and compatibility rules to enforce:
- **Type compatibility rule:** the join result type parameter `T` should be compatible with the raster pixel type (as stated in the API source doc).
- **Typed raster loading rule:** when loading GeoTIFF, use matching typed load (`sc.geoTiff[Int]`, `sc.geoTiff[Float]`, etc.) so downstream `raptorJoin` type `T` is correct.
- CRS/nodata/default mixed-dataset behavior is **not clearly documented** in the provided sources; do not assume automatic harmonization.

### Output
Returns `JavaRDD[RaptorJoinFeature[T]]` — each record represents an overlap/intersection between an input vector feature and raster pixels, carrying pixel value(s) of type `T` for downstream filtering/aggregation.

### Valid Call Patterns
```scala
val raster: RDD[ITile] = sc.geoTiff("treecover")
val vector: RDD[IFeature] = sc.shapefile("us_states")
val join: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin[Float](vector)

val join: RDD[RaptorJoinFeature[Float]] = treecover.raptorJoin(countries)
  .filter(v => v.m >= 0 && v.m <= 100.0)
```

### LLM Instruction Prompt
- Use the instance/implicit call form exactly as documented: `raster.raptorJoin[...] (vector)` (or with optional options where available), not a bare `raptorJoin(...)`.
- Ensure generic/result pixel type is compatible with the raster’s real pixel type.
- Prepare inputs first (load raster/vector into RDDs); do not pass file paths directly to `raptorJoin`.
- If CRS or nodata handling is required, state that behavior is undocumented here and must be verified before assuming defaults.

### Prompt Snippet
```text
Given a raster RDD and a vector SpatialRDD, call `value.raptorJoin(...)` in RDPro/Beast style, keeping pixel type `T` compatible with raster pixel type. Return/consume overlap records for filtering or zonal-style aggregation. Do not assume undocumented CRS/nodata auto-handling.
```

### Common Failure Modes
- Pixel type mismatch (e.g., forcing `Float` join type when raster is loaded as integer type).
- Calling shape does not match real API usage (e.g., bare `raptorJoin(...)` instead of `value.raptorJoin(...)`).
- Passing raw paths instead of loaded `SpatialRDD`/`RasterRDD`.
- Assuming undocumented behavior for CRS reconciliation or nodata semantics.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val treecover = sc.geoTiff[Float]("treecover")
val countries = sc.shapefile("us_states")

val join: RDD[RaptorJoinFeature[Float]] =
  treecover.raptorJoin(countries, new BeastOptions())
    .filter(v => v.m >= 0 && v.m <= 100.0)
```