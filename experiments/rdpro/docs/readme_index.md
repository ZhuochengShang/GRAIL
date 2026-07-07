# RDPro — organized API index

63 verified · 117 grounded · 27 sibling · 11 guessed · 78 categories

Legend: ★ verified (compiled + ran) · ✅ grounded (direct test) · 🟡 sibling-grounded · ⚠️ guessed (verify by execution). **primary** = most robust in its group.

## BeastOptions
- ★ `getInt` — verified · exec pass **(primary)**
- ★ `getLong` — verified · exec pass
- ★ `setBoolean` — verified · exec pass
- ★ `setLong` — verified · exec pass
- ✅ `getBoolean` — grounded · exec fail
- ✅ `mergeWith` — grounded · exec fail
- ✅ `retainIndex` — grounded · exec fail
- ✅ `set` — grounded · exec fail
- 🟡 `this` — sibling · exec fail

## BlockCartesianRDD
- ✅ `compute` — grounded · exec fail **(primary)**

## BufferedFSDataInputStream
- ✅ `seek` — grounded · exec fail **(primary)**

## CGOperationsMixin
- ⚠️ `eulerHistogramCount` — guessed · exec fail **(primary)**
- ⚠️ `eulerHistogramSize` — guessed · exec fail
- ⚠️ `uniformHistogramCount` — guessed · exec fail
- ⚠️ `uniformHistogramSize` — guessed · exec fail

## CLIOperation
- ✅ `printUsage` — grounded · exec fail **(primary)**
- ✅ `run` — grounded · exec fail

## CRSServer
- ★ `crsToSRID` — verified · exec pass **(primary)**
- ★ `sridToCRS` — verified · exec pass
- ✅ `startServer` — grounded · exec fail

## DBFWriter
- ✅ `numFields` — grounded · exec fail **(primary)**

## DatasetProcessor
- ✅ `decompressDatasetFiles` — grounded · exec fail **(primary)**
- ✅ `id` — grounded · exec fail
- ✅ `summarizeData` — grounded · exec fail
- ✅ `visualize` — grounded · exec fail
- 🟡 `geometryType` — sibling · exec fail

## DefaultReadOnlyTile
- ★ `isEmpty` — verified · exec pass **(primary)**
- ✅ `getPixelValue` — grounded · exec fail

## DiskTileHashtable
- ★ `construct` — verified · exec pass **(primary)**

## FeatureWriterSize
- ✅ `call` — grounded · exec fail **(primary)**

## GeoJSONFormat
- ✅ `path` — grounded · exec fail **(primary)**

## GeoJSONScanBuilder
- ✅ `build` — grounded · exec fail **(primary)**

## GeoJSONTable
- ✅ `inferSchema` — grounded · exec fail **(primary)**

## GeoTiffWriter
- ★ `saveAsGeoTiff` — verified · exec pass **(primary)**
- ✅ `count` — grounded · exec fail

## GeometricSummary
- ⚠️ `computeForFeaturesWithOutputSize` — guessed · exec fail **(primary)**

## GeometryQuadSplitter
- ✅ `splitGeometryAcrossDateLine` — grounded · exec fail **(primary)**

## GetPointValue
- ⚠️ `process` — guessed · exec fail **(primary)**

## GriddedSummary
- ✅ `computeForFeatures` — grounded · exec fail **(primary)**

## HDF4Reader
- ★ `createTileIDFilter` — verified · exec pass **(primary)**
- ★ `metadata` — verified · exec pass
- ✅ `createDateFilter` — grounded · exec fail
- ✅ `readTile` — grounded · exec fail

## HistogramOP
- ✅ `computePointHistogramSparse` — grounded · exec fail **(primary)**

## IFeature
- ★ `getGeometry` — verified · exec pass **(primary)**
- ★ `getStorageSize` — verified · exec pass
- ✅ `getAttributeName` — grounded · exec fail
- ✅ `getName` — grounded · exec fail

## ITile
- ★ `componentType` — verified · exec pass **(primary)**
- ★ `numComponents` — verified · exec pass
- ★ `pixelLocations` — verified · exec pass
- ✅ `getPointValue` — grounded · exec fail
- ✅ `isDefined` — grounded · exec fail
- ✅ `isEmptyAt` — grounded · exec fail
- ✅ `pixelType` — grounded · exec fail
- 🟡 `extents` — sibling · exec fail
- 🟡 `pixels` — sibling · exec fail

## ImageIterator
- ⚠️ `image` — guessed · exec fail **(primary)**

## IndexBuilder
- ✅ `buildIndex` — grounded · exec fail **(primary)**

## IndexHelper
- ✅ `createPartitioner` — grounded · exec fail **(primary)**
- ✅ `partitionFeatures` — grounded · exec fail
- ✅ `partitionFeatures2` — grounded · exec fail
- ✅ `runDuplicateAvoidance` — grounded · exec fail
- ✅ `saveIndex2` — grounded · exec fail

## IndexMixin
- ★ `partitionBy` — verified · exec pass **(primary)**

## IntermediateVectorTile
- ✅ `rasterizeGeometry` — grounded · exec fail **(primary)**
- ✅ `simplifyGeometry` — grounded · exec fail
- ✅ `trimLineSegment` — grounded · exec fail

## JavaSpatialRDDHelper
- ★ `plotImage` — verified · exec pass **(primary)**
- ★ `saveAsGeoJSON` — verified · exec pass
- ✅ `isSpatiallyPartitioned` — grounded · exec fail
- ✅ `rangeQuery` — grounded · exec fail
- ✅ `reproject` — grounded · exec fail
- ✅ `spatialPartition` — grounded · exec fail
- ✅ `summary` — grounded · exec fail
- ✅ `writeSpatialFile` — grounded · exec fail
- 🟡 `raptorJoin` — sibling · exec fail
- 🟡 `saveAsCSVPoints` — sibling · exec fail
- 🟡 `saveAsIndex` — sibling · exec fail
- 🟡 `saveAsKML` — sibling · exec fail
- 🟡 `saveAsShapefile` — sibling · exec fail
- 🟡 `saveAsWKTFile` — sibling · exec fail

## JavaSpatialSparkContext
- ★ `geoTiff` — verified · exec pass **(primary)**
- ★ `geojsonFile` — verified · exec pass
- ★ `shapefile` — verified · exec pass
- ★ `spatialFile` — verified · exec pass
- ✅ `readCSVPoint` — grounded · exec fail
- ✅ `readWKTFile` — grounded · exec fail
- 🟡 `hdfFile` — sibling · exec fail

## KryoInputToObjectInput
- ✅ `read` — grounded · exec fail **(primary)**
- 🟡 `available` — sibling · exec fail

## KryoOutputToObjectOutput
- ✅ `close` — grounded · exec fail **(primary)**
- ✅ `write` — grounded · exec fail

## LRUCache
- ✅ `size` — grounded · exec fail **(primary)**

## LiteGeometry
- ✅ `area` — grounded · exec fail **(primary)**
- ✅ `isCW` — grounded · exec fail
- 🟡 `part` — sibling · exec fail

## MVTDataVisualizer
- ✅ `plotSingleTileParallel` — grounded · exec fail **(primary)**
- 🟡 `plotAllTiles` — sibling · exec fail
- 🟡 `saveTiles` — sibling · exec fail
- 🟡 `saveTilesCompact` — sibling · exec fail

## MemoryTile
- ✅ `compress` — grounded · exec fail **(primary)**
- 🟡 `decompress` — sibling · exec fail

## MemoryTile2
- ✅ `setPixelValue` — grounded · exec fail **(primary)**

## MemoryTileWindow
- ✅ `getValue` — grounded · exec fail **(primary)**

## MultilevelPlot
- ⚠️ `plotFeatures` — guessed · exec fail **(primary)**

## OperationHelper
- ✅ `checkOptions` — grounded · exec fail **(primary)**
- ✅ `getOperationParams` — grounded · exec fail
- ✅ `printOperationUsage` — grounded · exec fail
- ✅ `readConfigurationXML` — grounded · exec fail

## PointSampleAccumulator
- ★ `add` — verified · exec pass **(primary)**
- ✅ `merge` — grounded · exec fail
- ✅ `value` — grounded · exec fail

## PointSampler
- ✅ `pointSample` — grounded · exec fail **(primary)**

## RaptorJoin
- ★ `raptorJoinFeature` — verified · exec pass **(primary)**
- ★ `raptorJoinIDFull` — verified · exec pass

## RaptorMixin
- ★ `flatten` — verified · exec pass **(primary)**
- ★ `rasterizePixels` — verified · exec pass
- ★ `rasterizePoints` — verified · exec pass

## RasterFeature
- ★ `append` — verified · exec pass **(primary)**
- ★ `create` — verified · exec pass

## RasterFileRDD
- ✅ `selectFiles` — grounded · exec fail **(primary)**

## RasterMetadata
- ★ `tileIDs` — verified · exec pass **(primary)**
- ✅ `envelope` — grounded · exec fail
- ✅ `getTileIDAtPixel` — grounded · exec fail
- ✅ `getTileIDAtPoint` — grounded · exec fail
- ✅ `gridToModel` — grounded · exec fail
- ✅ `modelToGrid` — grounded · exec fail
- ✅ `numTiles` — grounded · exec fail
- ✅ `rasterHeight` — grounded · exec fail
- ✅ `rasterWidth` — grounded · exec fail
- ✅ `rescale` — grounded · exec fail
- ✅ `retile` — grounded · exec fail

## RasterOperationsFocal
- ✅ `divideScene` — grounded · exec fail **(primary)**
- ✅ `reshapeAverage` — grounded · exec fail
- ✅ `slidingWindow` — grounded · exec fail
- 🟡 `reshapeNN` — sibling · exec fail

## RasterOperationsLocal
- ★ `explode` — verified · exec pass **(primary)**
- ★ `filterPixels` — verified · exec pass
- ★ `mapPixels` — verified · exec pass
- ★ `overlay` — verified · exec pass

## RasterPartitioner
- ✅ `getPartition` — grounded · exec fail **(primary)**

## RasterThumbnail
- ★ `addDependentClasses` — verified · exec pass **(primary)**

## ReadWriteMixin
- ★ `generateSpatialData` — verified · exec pass **(primary)**

## Reprojector
- ★ `findTransformationInfo` — verified · exec pass **(primary)**
- ★ `reprojectEnvelope` — verified · exec pass
- ★ `reprojectGeometry` — verified · exec pass
- ★ `reprojectRDD` — verified · exec pass
- ✅ `reprojectEnvelopeInPlace` — grounded · exec fail

## SQLQueryHelper
- ✅ `extractTables` — grounded · exec fail **(primary)**

## SVGPlotter
- ✅ `getTitle` — grounded · exec fail **(primary)**
- 🟡 `plot` — sibling · exec fail

## ScalaSparkTest
- ★ `sparkContext` — verified · exec pass **(primary)**
- ✅ `copyResource` — grounded · exec fail
- ✅ `locateResource` — grounded · exec fail
- ✅ `readFile` — grounded · exec fail
- ✅ `readTextResource` — grounded · exec fail
- ✅ `using` — grounded · exec fail
- 🟡 `sparkSession` — sibling · exec fail

## ShapefileReader
- ⚠️ `initialized` — guessed · exec fail **(primary)**

## ShapefileWriter
- ✅ `initialize` — grounded · exec fail **(primary)**

## SlidingWindowTile
- ★ `x1` — verified · exec pass **(primary)**
- ★ `x2` — verified · exec pass
- ★ `y1` — verified · exec pass
- ★ `y2` — verified · exec pass
- ✅ `addTile` — grounded · exec fail

## SnapTransform
- ✅ `transform` — grounded · exec fail **(primary)**

## SpatialFilePartition2
- ★ `end` — verified · exec pass **(primary)**

## SpatialFileRDD
- ★ `createPartitions` — verified · exec pass **(primary)**
- ★ `getFeatureReaderClass` — verified · exec pass
- ★ `readLocal` — verified · exec pass
- ★ `readPartition` — verified · exec pass
- ✅ `skipDuplicateAvoidance` — grounded · exec fail

## SpatialFileSource
- ✅ `name` — grounded · exec fail **(primary)**

## SpatialGenerator
- ✅ `uniform` — grounded · exec fail **(primary)**
- 🟡 `affineTransform` — sibling · exec fail
- 🟡 `normal` — sibling · exec fail

## SpatialGeneratorBuilder
- ★ `config` — verified · exec pass **(primary)**
- ★ `diagonal` — verified · exec pass
- ★ `distribution` — verified · exec pass
- ★ `makeBoxes` — verified · exec pass
- ★ `mbr` — verified · exec pass
- ★ `parcel` — verified · exec pass
- ★ `sierpinski` — verified · exec pass
- ✅ `numPartitions` — grounded · exec fail
- 🟡 `bit` — sibling · exec fail
- 🟡 `gaussian` — sibling · exec fail
- 🟡 `generate` — sibling · exec fail

## SpatialJoin
- ✅ `spatialJoin` — grounded · exec fail **(primary)**
- ✅ `spatialJoinBNLJ` — grounded · exec fail
- ✅ `spatialJoinDJ` — grounded · exec fail
- ✅ `spatialJoinIntersectsPlaneSweepFeatures` — grounded · exec fail
- ✅ `spatialJoinPBSM` — grounded · exec fail
- ✅ `spatialJoinRepJ` — grounded · exec fail

## SpatialParquetHelper
- ✅ `encodeGeometry` — grounded · exec fail **(primary)**

## SpatialParquetSource
- ✅ `decodeSpatialParquet` — grounded · exec fail **(primary)**
- ✅ `encodeGeoParquet` — grounded · exec fail
- ✅ `encodeSpatialParquet` — grounded · exec fail

## SpatialPartition
- ★ `numFeatures` — verified · exec pass **(primary)**
- ✅ `numPoints` — grounded · exec fail
- 🟡 `numNonEmptyGeometries` — sibling · exec fail
- 🟡 `sumSideLength` — sibling · exec fail

## SpatialReader
- ✅ `readInput` — grounded · exec fail **(primary)**

## SpatialWriter
- ✅ `saveFeatures` — grounded · exec fail **(primary)**

## StaticFileWebHandler
- ✅ `setup` — grounded · exec fail **(primary)**

## Summary
- ⚠️ `createSummaryAccumulator` — guessed · exec fail **(primary)**

## VectorCanvas
- ★ `addGeometry` — verified · exec pass **(primary)**
- ✅ `createRingsForOccupiedPixels` — grounded · exec fail
- ✅ `findIntersections` — grounded · exec fail

## VectorLayerBuilder
- ★ `zigzagDecode` — verified · exec pass **(primary)**
- ✅ `addFeature` — grounded · exec fail

## VisualizationMixin
- ⚠️ `plotPyramid` — guessed · exec fail **(primary)**

## ZipUtil
- ★ `putStoredFile` — verified · exec pass **(primary)**
- ✅ `lastNFiles` — grounded · exec fail
- ✅ `listFilesInZip` — grounded · exec fail
- ✅ `mergeZip` — grounded · exec fail

## ZonalStatistics
- ✅ `zonalStats2` — grounded · exec fail **(primary)**
- ✅ `zonalStatsLocal` — grounded · exec fail
