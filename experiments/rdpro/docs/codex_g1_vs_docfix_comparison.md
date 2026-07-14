# Codex G1 README vs G1-Based Docfix Evaluation

## Performance

- g1: 106/205 raw = 51.7%; excluding infra = 54.6% (infra 11)
- g4: 24/99 raw = 24.2%; excluding infra = 27.0% (infra 10)
- after: 122/205 raw = 59.5%; excluding infra = 63.2% (infra 12)

G1 -> after-docfix full eval: +16 raw passes (+7.8%).

Snippet g4 recovered: 24/99 = 24.2%.

## README Changes

- Changed entries vs frozen Codex fresh README: 1
  - `createSummaryAccumulator`: 3386 -> 2268 chars, similarity 0.116

## Pass Set Changes

- Newly passing after docfix/full rerun vs g1: 19
  `computePointHistogramSparse`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `geometryType`, `initialized`, `isCW`, `isDefined`, `mapPixels`, `modelToGrid`, `overlay`, `partitionFeatures2`, `pointSample`, `rangeQuery`, `rasterizePixels`, `saveIndex2`, `splitGeometryAcrossDateLine`, `value`, `y1`
- Regressed after docfix/full rerun vs g1: 3
  `computeForFeatures`, `mergeZip`, `plot`

## Grouped Accuracy

- app-specific/dataExplorer: g1 3/4=75.0%; after 3/4=75.0%; delta +0; infra_after 1
- custom geospatial/raster: g1 42/89=47.2%; after 51/89=57.3%; delta +9; infra_after 6
- env/test/framework: g1 0/7=0.0%; after 0/7=0.0%; delta +0; infra_after 0
- format/spark-io: g1 24/38=63.2%; after 28/38=73.7%; delta +4; infra_after 0
- general/util/io: g1 37/67=55.2%; after 40/67=59.7%; delta +3; infra_after 5

## Group Names

### app-specific/dataExplorer
`extractTables`, `summarizeData`, `summary`, `visualize`
### custom geospatial/raster
`add`, `addFeature`, `addGeometry`, `addTile`, `append`, `area`, `build`, `buildIndex`, `call`, `compute`, `computeForFeatures`, `computePointHistogramSparse`, `construct`, `create`, `createDateFilter`, `createRingsForOccupiedPixels`, `createSummaryAccumulator`, `encodeGeometry`, `envelope`, `explode`, `extents`, `filterPixels`, `findIntersections`, `findTransformationInfo`, `flatten`, `geoTiff`, `geometryType`, `hdfFile`, `image`, `isCW`, `isDefined`, `isEmptyAt`, `isSpatiallyPartitioned`, `mapPixels`, `mergeWith`, `metadata`, `numFeatures`, `numNonEmptyGeometries`, `numPoints`, `numTiles`, `overlay`, `part`, `pixelLocations`, `pixelType`, `pixels`, `plot`, `plotAllTiles`, `plotFeatures`, `plotImage`, `plotSingleTileParallel`, `pointSample`, `process`, `raptorJoin`, `raptorJoinFeature`, `rasterHeight`, `rasterizeGeometry`, `rasterizePixels`, `rasterizePoints`, `reproject`, `reprojectEnvelope`, `reprojectEnvelopeInPlace`, `reprojectGeometry`, `reprojectRDD`, `rescale`, `reshapeAverage`, `reshapeNN`, `retile`, `run`, `saveAsGeoTiff`, `saveTiles`, `saveTilesCompact`, `selectFiles`, `simplifyGeometry`, `spatialJoin`, `spatialJoinBNLJ`, `spatialJoinDJ`, `spatialJoinIntersectsPlaneSweepFeatures`, `spatialJoinPBSM`, `spatialJoinRepJ`, `splitGeometryAcrossDateLine`, `startServer`, `transform`, `trimLineSegment`, `x1`, `x2`, `y1`, `y2`, `zonalStats2`, `zonalStatsLocal`
### env/test/framework
`copyResource`, `locateResource`, `readFile`, `readTextResource`, `sparkContext`, `sparkSession`, `using`
### format/spark-io
`affineTransform`, `config`, `createPartitioner`, `createPartitions`, `decodeSpatialParquet`, `diagonal`, `distribution`, `encodeGeoParquet`, `encodeSpatialParquet`, `end`, `gaussian`, `generate`, `generateSpatialData`, `geojsonFile`, `initialized`, `makeBoxes`, `mbr`, `normal`, `numFields`, `numPartitions`, `parcel`, `partitionBy`, `partitionFeatures`, `partitionFeatures2`, `rangeQuery`, `saveAsCSVPoints`, `saveAsGeoJSON`, `saveAsIndex`, `saveAsKML`, `saveAsShapefile`, `saveAsWKTFile`, `saveFeatures`, `saveIndex2`, `shapefile`, `sierpinski`, `spatialFile`, `spatialPartition`, `uniform`
### general/util/io
`available`, `bit`, `checkOptions`, `compress`, `computeForFeaturesWithOutputSize`, `count`, `createTileIDFilter`, `crsToSRID`, `decompress`, `decompressDatasetFiles`, `divideScene`, `eulerHistogramCount`, `eulerHistogramSize`, `getAttributeName`, `getBoolean`, `getFeatureReaderClass`, `getGeometry`, `getInt`, `getLong`, `getName`, `getOperationParams`, `getPartition`, `getPointValue`, `getStorageSize`, `getTileIDAtPixel`, `getTileIDAtPoint`, `getTitle`, `getValue`, `gridToModel`, `id`, `lastNFiles`, `listFilesInZip`, `mergeZip`, `modelToGrid`, `name`, `path`, `plotPyramid`, `printOperationUsage`, `putStoredFile`, `raptorJoinIDFull`, `rasterWidth`, `readCSVPoint`, `readConfigurationXML`, `readInput`, `readLocal`, `readPartition`, `readTile`, `readWKTFile`, `retainIndex`, `runDuplicateAvoidance`, `seek`, `set`, `setBoolean`, `setLong`, `setPixelValue`, `setup`, `size`, `skipDuplicateAvoidance`, `slidingWindow`, `sridToCRS`, `sumSideLength`, `tileIDs`, `uniformHistogramCount`, `uniformHistogramSize`, `value`, `writeSpatialFile`, `zigzagDecode`
