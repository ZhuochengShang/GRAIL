# Fix-loop report — aideal_run_nos7ok4f

_Generated 2026-07-14 00:53 by `aideal fix-report`._

- kind: **comprehension**  ·  run_id: `20260714-064209Z`  ·  models: audience=google:gemini-3.1-pro-preview, fixer=google:gemini-3.1-pro-preview
- pass **37/88** raw (42.0%)  ·  scored **37/88** (42.0%) after excluding 0 infra
- wall 1.18 h  ·  tokens in 206,599 / out 417,784 ·  llm calls 88  ·  max_fix_rounds 0
- pass-by-round: r0:37  ·  **0 rescued by the fix loop** (pass@0 = 37)

## Chronic failures across runs (14)

_Failed in ≥2 recorded runs with the same error signature at least twice — candidates for doc-repair with deep-dive, exclusion, or a harness/fixture fix rather than more snippet retries._

| API | runs failed | same-sig runs | distinct sigs | first seen |
|---|---|---|---|---|
| `reshapeNN` | 8 | 3 | 5 | 2026-07-07 |
| `readCSVPoint` | 6 | 4 | 3 | 2026-07-07 |
| `reproject` | 6 | 2 | 5 | 2026-07-07 |
| `saveAsCSVPoints` | 6 | 2 | 5 | 2026-07-07 |
| `saveAsIndex` | 6 | 2 | 5 | 2026-07-07 |
| `numPoints` | 5 | 2 | 4 | 2026-07-07 |
| `plotImage` | 5 | 2 | 4 | 2026-07-07 |
| `raptorJoin` | 5 | 3 | 3 | 2026-07-07 |
| `uniformHistogramSize` | 5 | 2 | 4 | 2026-07-07 |
| `pixels` | 4 | 2 | 3 | 2026-07-07 |
| `plotAllTiles` | 4 | 3 | 2 | 2026-07-07 |
| `saveTilesCompact` | 4 | 3 | 2 | 2026-07-07 |
| `using` | 4 | 2 | 3 | 2026-07-07 |
| `sierpinski` | 3 | 2 | 2 | 2026-07-08 |

## Failure clusters (one issue, many APIs)

_Current failures grouped by normalized error signature (identifiers masked). Fixing the top cluster's root cause pays across all its APIs._

- **6x** [compile] <path>:<n>: error: value <name> is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
  - `envelope`, `reproject`, `rescale`, `reshapeAverage`, `reshapeNN`, `retile`
- **5x** [compile] <path>:<n>: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.b
  - `create`, `rasterizePixels`, `x2`, `y1`, `y2`
- **2x** [compile] <path>:<n>: error: type mismatch;
  - `computeForFeatures`, `rangeQuery`
- **1x** [compile] <path>:<n>: error: value <name> is not a member of edu.ucr.cs.bdlab.beast.geolite.RasterFeature
  - `append`
- **1x** [compile] <path>:<n>: error: ambiguous reference to overloaded definition,
  - `computeForFeaturesWithOutputSize`
- **1x** [runtime] java.lang.AssertionError: assertion failed: Expected Polygon geometry for box, but got Envelope
  - `config`
- **1x** [compile] <path>:<n>: error: class GeoTiffWriter takes type parameters
  - `count`
- **1x** [compile] <path>:<n>: error: value <name> is not a member of Int
  - `eulerHistogramCount`
- **1x** [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of eulerHistogramSize
  - `eulerHistogramSize`
- **1x** [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in
  - `explode`
- **1x** [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of filterPixels because pixel inspe
  - `filterPixels`
- **1x** [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of MemoryTileWindow.getValue
  - `getValue`

## Why each API fails (51 failing)

### `append` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/Feature.scala:405`
- last error: ApiTest.scala:367: error: value append is not a member of edu.ucr.cs.bdlab.beast.geolite.RasterFeature
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:367: error: value append is not a

### `computeForFeatures` — compile

- canonical source: `beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GriddedSummary.scala:57`
- last error: ApiTest.scala:361: error: type mismatch;
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: type mism

### `computeForFeaturesWithOutputSize` — compile

- canonical source: `beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GeometricSummary.scala:49`
- last error: ApiTest.scala:357: error: ambiguous reference to overloaded definition,
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: er

### `config` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:30`
- last error: java.lang.AssertionError: assertion failed: Expected Polygon geometry for box, but got Envelope
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected Polygon geometry for box, but got Envelope

### `count` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860`
- last error: ApiTest.scala:357: error: class GeoTiffWriter takes type parameters
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: class GeoTiffWriter ta

### `create` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:324`
- last error: ApiTest.scala:368: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$1: scala.reflect.ClassTag[T])edu.ucr.cs
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:368: error: not enough arguments 

### `envelope` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:170`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is n

### `eulerHistogramCount` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98`
- last error: ApiTest.scala:360: error: value length is not a member of Int
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:360: error: value le

### `eulerHistogramSize` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of eulerHistogramSize
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of eulerHistogramSize

### `explode` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:76` · reached: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:136`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:155`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:463`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0 (TID 5) (192.168.68.51 executor driver): java.lang.RuntimeException: Unrecognized value [F@254af7d6 of type class [F
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 5 in stage 0.0 failed 1 times, most recent failure: Lost task 5.0 in stage 0.0

### `filterPixels` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:48`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of filterPixels because pixel inspection methods are not documented.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of filterPixels because pixel inspection meth

### `getValue` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of MemoryTileWindow.getValue
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of MemoryTileWindow.getValue

### `hdfFile` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46`
- last error: ApiTest.scala:357: error: method hdfFile: (path: String, layer: String, opts: edu.ucr.cs.bdlab.beast.common.BeastOptions)org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Float]] does not take type parameters.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: method hdfFile: (pat

### `id` — runtime

- canonical source: `beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result.

### `isSpatiallyPartitioned` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:40`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: it demonstrates saving and checking a partitioned RDD but omits how to actually create 'partitionedFeatures' to test the true condition.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: it demonstrates saving and checking a partit

### `mapPixels` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38`
- last error: java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')

### `metadata` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:66`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: HDF4Reader and its metadata method are not documented.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: HDF4Reader and its metadata method are not d

### `numPoints` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:38`
- last error: ApiTest.scala:364: error: type SpatialPartition is not a member of package edu.ucr.cs.bdlab.beast.indexing
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: type SpatialPartit

### `overlay` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96`
- last error: java.lang.AssertionError: assertion failed: Expected array of length 2, got 22
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected array of length 2, got 22

### `part` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of part on LiteGeometry, as neither LiteGeometry nor part are mentioned in the provided documentation.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of part on LiteGeometry, as neither LiteGeome

### `pixelType` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138`
- last error: java.lang.AssertionError: assertion failed: Expected FloatType, but got ArrayType(FloatType,false)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected FloatType, but got ArrayType(FloatType,false)

### `pixels` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of ITile.pixels
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result of ITile.pixels

### `plotAllTiles` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:170`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the exact number or content of the generated MVT tiles.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the exact number or content of the generated MVT tiles.

### `plotFeatures` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SingleLevelPlot.scala:58`
- last error: ApiTest.scala:364: error: object visualization is not a member of package edu.ucr.cs.bdlab.beast
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: object visualiz

### `plotImage` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VisualizationMixin.scala:41`
- last error: java.lang.AssertionError: assertion failed: Output image file should exist
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Output image file should exist

### `rangeQuery` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:169`
- last error: ApiTest.scala:360: error: type mismatch;
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:360: error: type mismatch;

### `raptorJoin` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:87`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the spatial intersection of the inputs.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the spatial intersection of t

### `rasterizePixels` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:58`
- last error: ApiTest.scala:366: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$1: scala.reflect.ClassTag[T])edu.ucr.cs
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: not enough a

### `rasterizePoints` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:68`
- last error: ApiTest.scala:368: error: not enough arguments for method rasterizePoints: (points: org.apache.spark.rdd.RDD[(Double, Double, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$2: scala.reflect.ClassTag[T])edu.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:368: error: not enough a

### `readCSVPoint` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:97`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.51 executor driver): java.lang.RuntimeException: Error parsing dimension #0 column #0, value '0;nldas_boston_30m.tif;4108701;-71.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0

### `reproject` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:517`
- last error: ApiTest.scala:360: error: value rasterMetadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:360: error: value rasterMetada

### `rescale` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:542`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is no

### `reshapeAverage` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadat

### `reshapeNN` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is 

### `retile` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566`
- last error: ApiTest.scala:359: error: value tileWidth is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: value tileWidth is no

### `run` — compile

- canonical source: `beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/FetchGenerator.scala:35`
- last error: ApiTest.scala:357: error: not found: type BeastServer
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: not found: type BeastSer

### `saveAsCSVPoints` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:212` · reached: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:175`, `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:174`, `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:139`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 1.0 failed 1 times, most recent failure: Lost task 0.0 in stage 1.0 (TID 1) (192.168.68.51 executor driver): java.lang.RuntimeException: Unsupported class type class org.locationtech.jts.geom.Polygon
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 1.0 failed 1 times, most recent failure: Lost task 0.0 in stage 1.0

### `saveAsGeoJSON` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:201`
- last error: ApiTest.scala:364: error: value geojson is not a member of org.apache.spark.SparkContext
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: value geojson 

### `saveAsGeoTiff` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:104` · reached: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:471`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:465`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:527`
- last error: java.io.IOException: Directory /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/temp/15 is not empty
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.io.IOException: Directory /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/temp/15 is not empty

### `saveAsIndex` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92`
- last error: ApiTest.scala:365: error: too many arguments (3) for method saveAsIndex: (partitionedRDD: edu.ucr.cs.bdlab.beast.JavaPartitionedSpatialRDD, indexPath: String)Unit
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:365: error: too many argumen

### `saveAsKML` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:238`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because KML is output only.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because KML is output only.

### `saveTiles` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:453`
- last error: ApiTest.scala:358: error: object MVTDataVisualizer is not a member of package edu.ucr.cs.bdlab.beast.cg
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:358: error: object MVTDataVisu

### `saveTilesCompact` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:495` · reached: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:705`, `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:536`, `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:532`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 4 in stage 3.0 failed 1 times, most recent failure: Lost task 4.0 in stage 3.0 (TID 19) (192.168.68.51 executor driver): java.lang.VerifyError: Bad type on operand stack
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 4 in stage 3.0 failed 1 times, most recent failure: Lost task 4.0 in stage 3.0

### `sierpinski` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:175`
- last error: java.lang.AssertionError: assertion failed: Expected 1000 points, but got 500
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected 1000 points, but got 500

### `size` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:41`
- last error: ApiTest.scala:359: error: Int does not take parameters
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: Int does not take param

### `uniformHistogramSize` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result

### `using` — runtime

- canonical source: `beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:606`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: DatasetProcessor and using are not documented.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: DatasetProcessor and using are not documente

### `x1` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:14`
- last error: ApiTest.scala:358: error: class SlidingWindowTile takes type parameters
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:358: error: class SlidingWindowTile t

### `x2` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16`
- last error: ApiTest.scala:368: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$1: scala.reflect.ClassTag[T])edu.ucr.cs
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:368: error: not enough arguments for 

### `y1` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:15`
- last error: ApiTest.scala:366: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$1: scala.reflect.ClassTag[T])edu.ucr.cs
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: not enough arguments for 

### `y2` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17`
- last error: ApiTest.scala:369: error: not enough arguments for method rasterizePixels: (pixels: org.apache.spark.rdd.RDD[(Int, Int, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$1: scala.reflect.ClassTag[T])edu.ucr.cs
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:369: error: not enough arguments for 
