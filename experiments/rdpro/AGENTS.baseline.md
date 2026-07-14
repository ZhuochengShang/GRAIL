# AGENTS.md — RDPro (Beast) geospatial analytics library

RDPro (built on the Beast framework) is a Spark-based library for large-scale
geospatial analytics over raster and vector data in Scala.

## Build & run
- Scala + Apache Spark; build the uber jar with Maven, submit with `spark-submit`.
- A `SparkContext` (`sc`) is the entry point; most operations are implicit
  extension methods on RDDs added by importing the Beast package objects.

## How to use the APIs
- Import the Beast entry point so the `sc.*` readers and RDD operations resolve:
  `import edu.ucr.cs.bdlab.beast._`
- Read data with the high-level readers: `sc.geoTiff[Float](path)` for rasters
  (returns a raster RDD), `sc.shapefile(path)` / `sc.geojsonFile(path)` for
  vectors (returns a spatial RDD of features).
- Raster/vector analysis (raptor join, zonal statistics, reprojection, tiling)
  are extension methods on those RDDs; call them on the RDD, not on `sc`.
- Spark is lazy: force a result with an action (`.count()`, `.first()`) and
  write outputs with the library's save methods (e.g. `saveAsGeoTiff`).

## Conventions
- Prefer the documented high-level readers over raw Hadoop file streams.
- Raster pixel type is a type parameter (e.g. `geoTiff[Float]`); match it to
  the file or reads fail at runtime.
- Tests under `src/test` show real, compiling call patterns for most operations.
