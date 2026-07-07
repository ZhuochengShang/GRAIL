## 1. Project purpose

Beast is a Spark add-on/system for **Big Exploratory Analytics on spatio-temporal data**, covering both vector and raster workloads. It emphasizes multidimensional data support, scalable indexing/partitioning, visualization, and combined raster+vector analytics via **Raptor** and raster processing via **RDPro**.  
RDPro specifically targets distributed raster analytics (GeoTIFF/HDF loading, pixel transforms, reshape/reproject/rescale, raster writing). Raptor provides raster-vector join semantics for points/lines/polygons and zonal-style aggregation patterns.

Access modes are: (1) CLI (`beast`), (2) interactive Scala shell (`beast-shell`), (3) Scala/Java API for Spark RDD/SparkSQL. The docs consistently position Beast for large-scale datasets and Spark clusters.

## 2. Main workflows

Core documented workflows:

- Install binaries, run CLI operations (`summary`, `cat`, `index`, `splot`, `mplot`, `vmplot`, `server`, `sj`, `zs`, `raptor`).
- Set up development via Maven archetype or dependency `edu.ucr.cs.bdlab:beast-spark:0.10.1`.
- Load vector formats (Shapefile/GeoJSON/CSV-WKT/JSON+WKT/GPX), process/query/join, write to many output formats.
- Spatial partition/index workflow: `spatialPartition(...)`/`beast index ...`, then run `rangeQuery`/`spatialJoin` more efficiently.
- Raster RDPro workflow: load GeoTIFF/HDF as `RasterRDD[T]`/`RDD[ITile[T]]`, run pixel ops (`mapPixels`, `filterPixels`, `flatten`), reshape ops (`retile`, `explode`, `reproject`, `rescale`, `reshapeNN`/`reshapeAverage`), write GeoTIFF with writer options.
- Raster+vector workflow: `raptorJoin` then filter/aggregate for zonal-like statistics.
- Visualization workflow: single image (`splot`/`plotImage`), multilevel raster tiles (`mplot`) and vector MVT tiles (`vmplot`) in efficient/server-backed vs portable/all-tiles modes.

## 3. Important APIs and usage patterns

- Scala import convention: `import edu.ucr.cs.bdlab.beast._`
- Typed raster loading matters: `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`.
- Pixel type inspection pattern: `println(raster.first.pixelType)`.
- RDPro aliases/types: `RasterRDD[T]`, `RDD[ITile[T]]`.
- Raster writing API: `saveAsGeoTiff(path, options...)` with `GeoTiffWriter.Compression`, `GeoTiffWriter.WriteMode`, `GeoTiffWriter.CompactBits`, `GeoTiffWriter.BitsPerSample`.
- Raptor join return forms shown as `RDD[(IFeature, Int, Int, Float)]` and `RDD[RaptorJoinFeature[Float]]` depending on snippet.
- Spatial join API with explicit predicate/algorithm:
  `spatialJoin(..., ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)`.
- Partitioning API: `features.spatialPartition(classOf[RSGrovePartitioner])`; disjoint partitioning via `IndexHelper.createPartitioner(..., "disjoint" -> true)`.
- Vector I/O methods: `shapefile`, `geojson`, `geojsonFile`, `readCSVPoint`, `readWKTFile`, `spatialFile`, and writers (`saveAsGeoJSON`, `saveAsShapefile`, `writeSpatialFile`, etc.).
- Not clearly documented: full API surface for RDPro zonal statistics command (`zs`) in Scala, and exact `RaptorJoinFeature` tuple-field compatibility across snippets.

## 4. Inputs and file formats

Documented vector formats: text-delimited (point/wkt/envelope), Shapefile (zipped/unzipped), GeoJSON (FeatureCollection or one-feature-per-line), JSON+WKT, GPX (input-only), KML/KMZ (output-only). CSV supports `.bz2`/`.gz`. Input auto-detect by extension and best-effort CSV inference.

Raster inputs in RDPro: **GeoTIFF** and **HDF** (`sc.hdfFile(path, layerName)`).

## 5. Outputs and generated artifacts

- Vector outputs: CSV point/WKT/envelope, Shapefile, zipshapefile, GeoJSON, KML, KMZ.
- Raster outputs: GeoTIFF directories/files via `saveAsGeoTiff`.
- Indexing outputs: partitioned files + master metadata (`beast index`).
- Visualization outputs: PNG (`splot`), pyramid zip archives (`mplot`, `vmplot`) plus optional server-generated dynamic tiles.
- Summaries/histograms are in-memory analytics outputs; CLI summary prints JSON-like report.
- Zonal-style aggregations often output to console or `saveAsTextFile`; docs mention CSV in CLI contexts.

## 6. Configuration and environment assumptions

- JDK 1.8+ recommended.
- Maven or SBT for dev; Git needed for source development.
- Spark environment assumed; many examples set local master if absent.
- CLI install uses Beast 0.10.1 binaries; PATH should include `beast-0.10.1/bin`.
- For NASA LP DAAC downloads, `.netrc` and account are required.
- Some workflows assume input accessible in local FS or HDFS depending Spark config.

## 7. Commands and examples — include the real fenced code blocks VERBATIM, one per major operation, exact receiver/qualifier preserved (not summarized into prose)

```shell
beast index tl_2018_us_primaryroads.zip iformat:shapefile tl_2018_us_primaryroads_index gindex:rsgrove oformat:rtree
```

```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val trees = raster.filterPixels(lc => lc >=1 && lc <= 10)
val countries = sc.shapefile("ne_10m_admin_0_countries.zip")
val result = RaptorJoin.raptorJoinFeature(trees, countries, Seq())
  .map(x => x.feature.getAs[String]("NAME")).countByValue().toMap
println(result)
```

```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")
```

```scala
val raster1: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val raster2: RasterRDD[Int] = sc.geoTiff[Int]("vegetation")
val stacked: RasterRDD[Array[Int]] = raster1.overlay(raster2)
```

```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

```scala
// Load a shapefile. Download from: ftp://ftp2.census.gov/geo/tiger/TIGER2018/STATE/
val polygons = sc.shapefile("tl_2018_us_state.zip")

// Load points in GeoJSON format.
// Download from https://star.cs.ucr.edu/dynamic/download.cgi/Tweets/data_index.geojson.gz?mbr=-117.8538,33.2563,-116.8142,34.4099
val points = sc.geojsonFile("Tweets.geojson.gz")

// Run a spatial join operation between points and polygons (point-in-polygon) query
val sjResults: RDD[(IFeature, IFeature)] =
    matchedPolygons.spatialJoin(matchedPoints, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)
```

```shell
beast vmplot ne_10m_admin_1_states_provinces.zip iformat:shapefile provinces_mvt.zip threshold:0 levels:7 -overwrite
```

## 8. Constraints, preconditions, compatibility rules, and type-selection rules

- **Type-selection rule (critical):** `sc.geoTiff[T]` type parameter must match real pixel type; table given for `IntegerType`, `FloatType`, `ArrayType(IntegerType,true)`, `ArrayType(FloatType, true)`.
- **Overlay precondition:** input rasters must have same metadata (resolution, CRS, tile size); otherwise first convert with reshape operations.
- `reshapeAverage` only for numerical continuous data; `reshapeNN` works for categorical and general use.
- Bit compaction only for integer pixels; float stays 32-bit.
- `-disjoint` indexing only for partitioners that support disjoint partitions; otherwise error.
- Disjoint partitioning may replicate features; duplicate handling required unless using Beast’s built-in `rangeQuery`/`spatialJoin`.
- Efficient multilevel visualization requires running `beast server`; portable mode uses `threshold:0`.
- For visualization URLs, trailing slash `/` is required in documented cases.

## 9. Facts to preserve in the final README

- Beast 0.10.1 setup commands and dependency coordinates.
- Three access modes: CLI, `beast-shell`, Scala/Java API.
- RDPro supports GeoTIFF + HDF input and GeoTIFF output.
- Raptor join supports point/line/polygon semantics and enables zonal-style aggregation.
- Spatial join algorithms: BNLJ, PBSM, DJ, REPJ, plus default-selection logic and quad-split optimization threshold (>100 avg points/geometry).
- R*-Grove / `RSGrovePartitioner` is recommended.
- Visualization has efficient (server-backed) and portable (`threshold:0`) variants for both image pyramid and MVT.

## 10. Missing or weak documentation

- No single consolidated RDPro API index (method signatures/options scattered).
- `zs` CLI operation is listed but not deeply specified here.
- Inconsistencies/typos in examples (`shapefie`, mixed `geojson` vs `geojsonFile`, tuple field usage in one Raptor snippet).
- Not clearly documented: CRS handling defaults for mixed raster/vector joins, nodata semantics across all raster ops, and guaranteed schema/type of `RaptorJoinFeature` across Scala/Java snippets.