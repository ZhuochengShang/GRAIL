# Fix-loop report — aideal_run_8_wxxem8

_Generated 2026-07-14 02:50 by `aideal fix-report`._

- kind: **comprehension**  ·  run_id: `20260714-081234Z`  ·  models: audience=google:gemini-3.1-pro-preview, fixer=google:gemini-3.1-pro-preview
- pass **73/171** raw (42.7%)  ·  scored **73/163** (44.8%) after excluding 8 infra
- wall 1.63 h  ·  tokens in 407,516 / out 684,326 ·  llm calls 171  ·  max_fix_rounds 0
- pass-by-round: r0:73  ·  **0 rescued by the fix loop** (pass@0 = 73)

## Chronic failures across runs (38)

_Failed in ≥2 recorded runs with the same error signature at least twice — candidates for doc-repair with deep-dive, exclusion, or a harness/fixture fix rather than more snippet retries._

| API | runs failed | same-sig runs | distinct sigs | first seen |
|---|---|---|---|---|
| `reshapeNN` | 8 | 3 | 5 | 2026-07-07 |
| `build` | 6 | 4 | 3 | 2026-07-07 |
| `divideScene` | 6 | 2 | 5 | 2026-07-07 |
| `encodeGeoParquet` | 6 | 4 | 3 | 2026-07-07 |
| `encodeSpatialParquet` | 6 | 4 | 3 | 2026-07-07 |
| `plotSingleTileParallel` | 6 | 5 | 2 | 2026-07-07 |
| `readCSVPoint` | 6 | 4 | 3 | 2026-07-07 |
| `readWKTFile` | 6 | 2 | 5 | 2026-07-07 |
| `reproject` | 6 | 2 | 5 | 2026-07-07 |
| `saveAsCSVPoints` | 6 | 2 | 5 | 2026-07-07 |
| `saveAsIndex` | 6 | 3 | 4 | 2026-07-07 |
| `setPixelValue` | 6 | 2 | 5 | 2026-07-07 |
| `decodeSpatialParquet` | 5 | 2 | 4 | 2026-07-07 |
| `getTileIDAtPoint` | 5 | 2 | 4 | 2026-07-07 |
| `numPoints` | 5 | 2 | 4 | 2026-07-07 |
| `raptorJoin` | 5 | 3 | 3 | 2026-07-07 |
| `readTile` | 5 | 3 | 3 | 2026-07-07 |
| `rescale` | 5 | 2 | 4 | 2026-07-07 |
| `addFeature` | 4 | 2 | 3 | 2026-07-07 |
| `checkOptions` | 4 | 4 | 1 | 2026-07-07 |
| `extractTables` | 4 | 4 | 1 | 2026-07-07 |
| `flatten` | 4 | 3 | 2 | 2026-07-07 |
| `getOperationParams` | 4 | 3 | 2 | 2026-07-07 |
| `initialized` | 4 | 2 | 3 | 2026-07-07 |
| `pixels` | 4 | 2 | 3 | 2026-07-07 |
| `plotAllTiles` | 4 | 3 | 2 | 2026-07-07 |
| `printOperationUsage` | 4 | 4 | 1 | 2026-07-07 |
| `saveIndex2` | 4 | 2 | 3 | 2026-07-07 |
| `saveTilesCompact` | 4 | 3 | 2 | 2026-07-07 |
| `spatialJoinRepJ` | 4 | 2 | 3 | 2026-07-07 |
| `using` | 4 | 2 | 3 | 2026-07-07 |
| `y1` | 4 | 2 | 3 | 2026-07-07 |
| `area` | 3 | 2 | 2 | 2026-07-07 |
| `getAttributeName` | 3 | 2 | 2 | 2026-07-07 |
| `lastNFiles` | 3 | 2 | 2 | 2026-07-07 |
| `numTiles` | 3 | 2 | 2 | 2026-07-07 |
| `sierpinski` | 3 | 2 | 2 | 2026-07-08 |
| `plotFeatures` | 2 | 2 | 1 | 2026-07-07 |

## Failure clusters (one issue, many APIs)

_Current failures grouped by normalized error signature (identifiers masked). Fixing the top cluster's root cause pays across all its APIs._

- **5x** [compile] <path>:<n>: error: value <name> is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
  - `divideScene`, `envelope`, `reshapeAverage`, `reshapeNN`, `retile`
- **4x** [compile] <path>:<n>: error: value <name> is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Float]
  - `geoTiff`, `hdfFile`, `reproject`, `y2`
- **3x** [infra] compile-time classpath/version gap (missing or mismatched jar)
  - `addFeature`, `build`, `plotSingleTileParallel`
- **3x** [infra] missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler
  - `checkOptions`, `getOperationParams`, `printOperationUsage`
- **3x** [compile] <path>:<n>: error: not found: value <name>
  - `decodeSpatialParquet`, `encodeGeoParquet`, `encodeSpatialParquet`
- **3x** [runtime] java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader <na
  - `flatten`, `raptorJoinIDFull`, `y1`
- **3x** [compile] <path>:<n>: error: type GeoTiffReader is not a member of package edu.ucr.cs.bdlab.beast.io
  - `getPointValue`, `rasterHeight`, `rasterWidth`
- **2x** [compile] <path>:<n>: error: type mismatch;
  - `diagonal`, `saveAsCSVPoints`
- **2x** [compile] <path>:<n>: error: method simplifyGeometry in class IntermediateVectorTile cannot be accessed in edu.ucr.cs.bdlab.davinci.IntermediateVector
  - `numPoints`, `part`
- **2x** [compile] <path>:<n>: error: value <name> is not a member of org.apache.spark.SparkContext
  - `saveAsWKTFile`, `saveIndex2`
- **1x** [compile] <path>:<n>: error: value <name> is not a member of edu.ucr.cs.bdlab.davinci.LiteGeometry
  - `area`
- **1x** [runtime] org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAI
  - `buildIndex`

## Why each API fails (98 failing)

### `addFeature` — infra

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:82`
- last error: compile-time classpath/version gap (missing or mismatched jar)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] compile-time classpath/version gap (missing or mismatched jar)

### `area` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115`
- last error: ApiTest.scala:377: error: value area is not a member of edu.ucr.cs.bdlab.davinci.LiteGeometry
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:377: error: value area is not a member of ed

### `build` — infra

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:133`
- last error: compile-time classpath/version gap (missing or mismatched jar)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] compile-time classpath/version gap (missing or mismatched jar)

### `buildIndex` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:186`
- last error: org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/_index.csv
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experime

### `checkOptions` — infra

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:293` · reached: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:133`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:128`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:120`
- last error: missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler

### `compute` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119`
- last error: ApiTest.scala:358: error: object BlockCartesianRDD is not a member of package edu.ucr.cs.bdlab.beast.operations
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:358: error: object BlockCartesianRDD is n

### `computeForFeatures` — compile

- canonical source: `beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GriddedSummary.scala:57`
- last error: ApiTest.scala:359: error: value numFeatures is not a member of (edu.ucr.cs.bdlab.beast.synopses.Summary, org.apache.spark.rdd.RDD[(Array[Int], edu.ucr.cs.bdlab.beast.synopses.Summary)])
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: value numFeatures

### `computePointHistogramSparse` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/HistogramOP.scala:72`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result (missing methods to query UniformHistogram for bucket values or partition counts)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result (missing methods to query UniformHistogram fo

### `construct` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:38`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result (no reader provided to verify the written hashtable).
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result (no reader provided to verify the written has

### `create` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:324`
- last error: java.lang.AssertionError: assertion failed: x1 should match the top-left x-coordinate
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: x1 should match the top-left x-coordinate

### `createPartitioner` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:136`
- last error: java.lang.AssertionError: assertion failed: Partitioner should be an instance of RSGrovePartitioner
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Partitioner should be an instance of RSGrovePartitioner

### `decodeSpatialParquet` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:69`
- last error: ApiTest.scala:361: error: not found: value spark
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: not found: value

### `diagonal` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:154`
- last error: ApiTest.scala:361: error: type mismatch;
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: type mismatch;

### `divideScene` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is not a m

### `encodeGeoParquet` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:99`
- last error: ApiTest.scala:360: error: not found: value spark
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:360: error: not found: value spa

### `encodeSpatialParquet` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:81`
- last error: ApiTest.scala:359: error: not found: value spark
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: not found: value

### `end` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26`
- last error: java.lang.AssertionError: assertion failed: Could not find SpatialFilePartition2 in the RDD lineage
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Could not find SpatialFilePartition2 in the RDD lineage

### `envelope` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:170`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is not a memb

### `eulerHistogramCount` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no methods of AbstractHistogram are documented.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no methods of AbstractHistogram are document

### `eulerHistogramSize` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109`
- last error: java.lang.AssertionError: assertion failed: The documented contract for AbstractHistogram is insufficient to verify the result properties (no methods documented).
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract for AbstractHistogram is insufficient to verify the result properties (no methods

### `explode` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:76` · reached: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:471`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:465`, `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:527`
- last error: java.io.IOException: Directory /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/temp/30 is not empty
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.io.IOException: Directory /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/temp/30 is not empty

### `extractTables` — infra

- canonical source: `beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/SQLQueryHelper.scala:22`
- last error: missing dependency on classpath: org/apache/calcite/sql/util/SqlVisitor
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing dependency on classpath: org/apache/calcite/sql/util/SqlVisitor

### `flatten` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69`
- last error: java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')

### `geoTiff` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:40`
- last error: ApiTest.scala:366: error: value getNumPixels is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: value getNumPixels is not a m

### `geometryType` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:60`
- last error: java.lang.AssertionError: assertion failed: Unexpected geometry type returned: MULTIPOLYGON
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Unexpected geometry type returned: MULTIPOLYGON

### `getAttributeName` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:92`
- last error: ApiTest.scala:361: error: value getNumAttributes is not a member of edu.ucr.cs.bdlab.beast.geolite.IFeature
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: value getNumAttribut

### `getName` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:83`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: cannot validate the correctness of arbitrary attribute names without a known schema.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: cannot validate the correctness of arbitrary

### `getOperationParams` — infra

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:209` · reached: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:133`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:128`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:120`
- last error: missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler

### `getPointValue` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93`
- last error: ApiTest.scala:359: error: type GeoTiffReader is not a member of package edu.ucr.cs.bdlab.beast.io
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: type GeoTiffReader is n

### `getStorageSize` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:112`
- last error: java.lang.AssertionError: assertion failed: The documented contract for getStorageSize is insufficient to verify the result because it returns an unspecified in-memory estimate.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract for getStorageSize is insufficient to verify the result because it returns an unsp

### `getTileIDAtPoint` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:81`
- last error: java.lang.AssertionError: assertion failed: Expected -1 for point (-837.0, -728.0) outside raster bounds, but got 25290
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected -1 for point (-837.0, -728.0) outside raster bounds, but got 25290

### `getValue` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because no writer API is provided to create a valid DiskTileHashtable file.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because no writer API is provided to create a

### `hdfFile` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46`
- last error: ApiTest.scala:363: error: value getNumPixels is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:363: error: value getNumPixels is not a m

### `id` — runtime

- canonical source: `beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because DatasetProcessor cannot be instantiated from the provided inputs.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because DatasetProcessor cannot be instantiat

### `initialized` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileReader.scala:48`
- last error: ApiTest.scala:359: error: not enough arguments for constructor ShapefileReader: (conf: org.apache.hadoop.conf.Configuration, file: edu.ucr.cs.bdlab.beast.io.SpatialFilePartition2, filter: org.locationtech.jts.geom.Envelope, skipSHPFile: Boolean, skipDBFFile: Boolean)edu.ucr.cs.bdlab.beast.io.shapefi
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: not enough arguments for

### `isCW` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:97`
- last error: ApiTest.scala:361: error: trait LiteGeometry is abstract; cannot be instantiated
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: trait LiteGeometry is abstract;

### `isDefined` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the specific raster data and NoData values.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the specific raster data and

### `isEmptyAt` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:114`
- last error: java.lang.AssertionError: assertion failed: The documented contract for isEmptyAt is insufficient to verify the boolean result without knowing the expected pixel value or having access to pixel-level getters.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract for isEmptyAt is insufficient to verify the boolean result without knowing the exp

### `lastNFiles` — runtime

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:48`
- last error: java.lang.AssertionError: assertion failed: ZIP file should contain at least one entry
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: ZIP file should contain at least one entry

### `mapPixels` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no ITile pixel access methods are documented to verify the transformation.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no ITile pixel access methods are documented

### `mergeWith` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:440`
- last error: java.lang.AssertionError: assertion failed: Expected 'val1' for 'beast.test.key1', but got Some(val1)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected 'val1' for 'beast.test.key1', but got Some(val1)

### `mergeZip` — runtime

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:425`
- last error: java.lang.AssertionError: assertion failed: Merged zip should contain 2 entries, found 1
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Merged zip should contain 2 entries, found 1

### `metadata` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:66`
- last error: ApiTest.scala:364: error: edu.ucr.cs.bdlab.raptor.HDF4Reader does not take type parameters
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: edu.ucr.cs.bdlab.raptor.HDF4

### `modelToGrid` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:161`
- last error: ApiTest.scala:364: error: value getMinX is not a member of edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: value getMinX is not a me

### `normal` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:40`
- last error: ApiTest.scala:378: error: no type parameters for method flatMap: (f: String => scala.collection.GenTraversableOnce[B])Iterator[B] exist so that it can be applied to arguments (String => Iterable[Class[?0]] forSome { type ?0 })
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:378: error: no type parameters for method

### `numFields` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: DBFWriter constructor is undocumented.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: DBFWriter constructor is undocumented.

### `numNonEmptyGeometries` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:35`
- last error: ApiTest.scala:364: error: value spatialPartitioning is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.IFeature]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: value spatialPa

### `numPartitions` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:75`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no methods to build the RDD or retrieve the partition count are provided.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result: no methods to build the RDD or retrieve the

### `numPoints` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:38`
- last error: ApiTest.scala:371: error: method simplifyGeometry in class IntermediateVectorTile cannot be accessed in edu.ucr.cs.bdlab.davinci.IntermediateVectorTile
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:371: error: method simplifyGeometry in

### `numTiles` — infra

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:61` · reached: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:84`
- last error: missing dependency on classpath: edu/ucr/cs/bdlab/jhdf/HDFFile
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing dependency on classpath: edu/ucr/cs/bdlab/jhdf/HDFFile

### `overlay` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96`
- last error: java.lang.AssertionError: assertion failed: Expected array length 2 from overlaying 2 rasters, got 22
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected array length 2 from overlaying 2 rasters, got 22

### `part` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146`
- last error: ApiTest.scala:368: error: method simplifyGeometry in class IntermediateVectorTile cannot be accessed in edu.ucr.cs.bdlab.davinci.IntermediateVectorTile
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:368: error: method simplifyGeometry in class

### `partitionBy` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:35`
- last error: java.lang.AssertionError: assertion failed: Partitioner must be an instance of RSGrovePartitioner
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Partitioner must be an instance of RSGrovePartitioner

### `partitionFeatures2` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:429`
- last error: java.lang.AssertionError: assertion failed: Partitioned RDD count (8) must match original count (2)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Partitioned RDD count (8) must match original count (2)

### `pixelType` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138`
- last error: java.lang.AssertionError: assertion failed: Expected FloatType for RasterRDD[Float], but got ArrayType(FloatType,false)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected FloatType for RasterRDD[Float], but got ArrayType(FloatType,false)

### `pixels` — runtime

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84`
- last error: java.lang.AssertionError: assertion failed: Expected 65536 pixels based on max local coordinates (255, 255), but got 15699
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: Expected 65536 pixels based on max local coordinates (255, 255), but got 15699

### `plotAllTiles` — runtime

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:170` · reached: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:705`, `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:536`, `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:532`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 1 in stage 12.0 failed 1 times, most recent failure: Lost task 1.0 in stage 12.0 (TID 40) (192.168.68.51 executor driver): java.lang.VerifyError: Bad type on operand stack
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 1 in stage 12.0 failed 1 times, most recent failure: Lost task 1.0 in stage 12

### `plotFeatures` — compile

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SingleLevelPlot.scala:58`
- last error: ApiTest.scala:366: error: not found: type GeometricPlotter
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: not found: type Geometri

### `plotSingleTileParallel` — infra

- canonical source: `beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:98`
- last error: compile-time classpath/version gap (missing or mismatched jar)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] compile-time classpath/version gap (missing or mismatched jar)

### `printOperationUsage` — infra

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:334` · reached: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:133`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:128`, `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:120`
- last error: missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [infra] missing dependency on classpath: org/mortbay/jetty/handler/AbstractHandler

### `raptorJoin` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:87`
- last error: ApiTest.scala:368: error: value getGeometry is not a member of edu.ucr.cs.bdlab.raptor.RaptorJoinFeature[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:368: error: value getGeometry is not a

### `raptorJoinFeature` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:73`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the spatial extents and overlap of the input data.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result without knowing the spatial extents and overl

### `raptorJoinIDFull` — runtime

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180`
- last error: java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.ClassCastException: class [F cannot be cast to class java.lang.Float ([F and java.lang.Float are in module java.base of loader 'bootstrap')

### `rasterHeight` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:52`
- last error: ApiTest.scala:359: error: type GeoTiffReader is not a member of package edu.ucr.cs.bdlab.beast.io
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: type GeoTiffReader is no

### `rasterWidth` — compile

- canonical source: `beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:49`
- last error: ApiTest.scala:359: error: type GeoTiffReader is not a member of package edu.ucr.cs.bdlab.beast.io
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:359: error: type GeoTiffReader is not

### `rasterizePoints` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:68`
- last error: ApiTest.scala:372: error: not enough arguments for method rasterizePoints: (points: org.apache.spark.rdd.RDD[(Double, Double, T)], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata, rasterFeature: edu.ucr.cs.bdlab.beast.geolite.RasterFeature)(implicit evidence$2: scala.reflect.ClassTag[T])edu.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:372: error: not enough arguments

### `readCSVPoint` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:97`
- last error: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0 (TID 0) (192.168.68.51 executor driver): java.lang.RuntimeException: Error parsing dimension #0 column #0, value '0;nldas_boston_30m.tif;4108701;-71.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 0.0 failed 1 times, most recent failure: Lost task 0.0 in stage 0.0

### `readConfigurationXML` — runtime

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60`
- last error: java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because the exact contents of the classpath XML are unknown.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result because the exact contents of the classpath X

### `readPartition` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441`
- last error: ApiTest.scala:358: error: object FilePartition is not a member of package edu.ucr.cs.bdlab.beast.io
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:358: error: object FilePartition is

### `readTile` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/IRasterReader.scala:60`
- last error: ApiTest.scala:362: error: type ITile is not a member of package edu.ucr.cs.bdlab.raptor
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:362: error: type ITile is not a member o

### `readWKTFile` — runtime

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:118` · reached: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:345`, `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:77`, `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:84`
- last error: java.lang.IllegalArgumentException: Pathname /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/.aideal_exec/file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/test_wkt.csv from /Users/clockorangezoe/Documents/phd_projects/code/
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.IllegalArgumentException: Pathname /Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/.aideal_exec/file:/Users/

### `reproject` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:517`
- last error: ApiTest.scala:377: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:377: error: value metadata is not a mem

### `rescale` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:542`
- last error: ApiTest.scala:357: error: object InterpolationMethod is not a member of package edu.ucr.cs.bdlab.raptor
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: object InterpolationMethod is

### `reshapeAverage` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58`
- last error: ApiTest.scala:357: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:357: error: value metadata is not

### `reshapeNN` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408`
- last error: ApiTest.scala:361: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:361: error: value metadata is not a mem

### `retainIndex` — runtime

- canonical source: `beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168`
- last error: java.lang.AssertionError: assertion failed: opts1 key1 expected 'val1', got Some(val1)
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [runtime] java.lang.AssertionError: assertion failed: opts1 key1 expected 'val1', got Some(val1)

### `retile` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566`
- last error: ApiTest.scala:360: error: value metadata is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD[Float]
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:360: error: value metadata is not a member

### `saveAsCSVPoints` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:212`
- last error: ApiTest.scala:366: error: type mismatch;
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: type mismatch;

### `saveAsGeoTiff` — compile

- canonical source: `beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:104`
- last error: ApiTest.scala:364: error: not enough arguments for method saveAsGeoTiff: (rasterRDD: org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[T]], outPath: String, opts: edu.ucr.cs.bdlab.beast.common.BeastOptions)Unit.
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:364: error: not enough arguments fo

### `saveAsIndex` — compile

- canonical source: `beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92`
- last error: ApiTest.scala:366: error: value saveAsIndex is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD
- loop trajectory: **PROGRESSING (error changed every round, 1 rounds)**
- rounds:
  - r0 [compile] ApiTest.scala:366: error: value saveAsIndex is not

_… 18 more failing APIs omitted (--max-api-detail to raise)._

**Infra failures excluded from doc-quality scoring (8):** `addFeature`, `build`, `checkOptions`, `extractTables`, `getOperationParams`, `numTiles`, `plotSingleTileParallel`, `printOperationUsage`
