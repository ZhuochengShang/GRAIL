# RDPro — API catalogue

218 APIs across 78 classes. Scan here, then open the one class file you need (each opens with how to obtain its receiver, then its methods).

Legend: ★ verified · ✅ grounded · 🟡 sibling · ⚠️ guessed

## [BeastOptions](api/BeastOptions.md)
_Retrieve an integer value associated with a specified key, returning a default value if the key is not found._
**Receiver:** instance — obtain a `BeastOptions` value, then `<value>.<method>(...)`
**APIs:** ★ `getInt` **(primary)**, ★ `getLong`, ★ `setBoolean`, ★ `setLong`, ⚠️ `getBoolean`, ⚠️ `mergeWith`, ⚠️ `retainIndex`, ⚠️ `set`, ⚠️ `this`

## [BlockCartesianRDD](api/BlockCartesianRDD.md)
_Compute the intersections of a linear ring with a raster grid, facilitating geospatial analysis in the context of raster processing._
**Receiver:** instance — obtain a `BlockCartesianRDD` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `compute` **(primary)**

## [BufferedFSDataInputStream](api/BufferedFSDataInputStream.md)
_The `seek` function is used to move the file pointer to a specified position within a data stream, allowing for random access to the data._
**Receiver:** instance — obtain a `BufferedFSDataInputStream` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `seek` **(primary)**

## [CGOperationsMixin](api/CGOperationsMixin.md)
_The `eulerHistogramCount` function computes an Euler histogram that efficiently counts the number of records in each cell for geometries with extents,…_
**Receiver:** instance — obtain a `CGOperationsMixin` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `eulerHistogramCount` **(primary)**, ⚠️ `eulerHistogramSize`, ⚠️ `uniformHistogramCount`, ⚠️ `uniformHistogramSize`

## [CLIOperation](api/CLIOperation.md)
_The `printUsage` function outputs usage information for the RDPro library, helping users understand how to utilize its features effectively._
**Receiver:** instance — obtain a `CLIOperation` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `printUsage` **(primary)**, ⚠️ `run`

## [CRSServer](api/CRSServer.md)
_The `crsToSRID` function retrieves a unique integer SRID (Spatial Reference System Identifier) corresponding to a given Coordinate Reference System (CRS),…_
**Receiver:** static object — call `CRSServer.<method>(...)`
**APIs:** ★ `crsToSRID` **(primary)**, ★ `sridToCRS`, ⚠️ `startServer`

## [DBFWriter](api/DBFWriter.md)
_`numFields` retrieves the number of attributes present in a given file, which is essential for understanding the structure of the data being processed in…_
**Receiver:** instance — obtain a `DBFWriter` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `numFields` **(primary)**

## [DatasetProcessor](api/DatasetProcessor.md)
_The `decompressDatasetFiles` function decompresses any ZIP files located in the dataset's path, cleans up by deleting the original ZIP files, and updates the…_
**Receiver:** instance — obtain a `DatasetProcessor` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `decompressDatasetFiles` **(primary)**, ⚠️ `geometryType`, ⚠️ `id`, ⚠️ `summarizeData`, ⚠️ `visualize`

## [DefaultReadOnlyTile](api/DefaultReadOnlyTile.md)
_Determines whether a specific tile at the given coordinates `(i, j)` is empty, which is useful for assessing the presence of data in raster processing._
**Receiver:** instance — obtain a `DefaultReadOnlyTile` value, then `<value>.<method>(...)`
**APIs:** ★ `isEmpty` **(primary)**, ⚠️ `getPixelValue`

## [DiskTileHashtable](api/DiskTileHashtable.md)
_The `construct` function creates a compact hashtable from a specified list of entries and writes it to a designated output stream._
**Receiver:** static object — call `DiskTileHashtable.<method>(...)`
**APIs:** ★ `construct` **(primary)**

## [FeatureWriterSize](api/FeatureWriterSize.md)
_The `call` function processes a given feature and returns an integer value, which may represent a specific property or characteristic of the feature in the…_
**Receiver:** instance — obtain a `FeatureWriterSize` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `call` **(primary)**

## [GeoJSONFormat](api/GeoJSONFormat.md)
_The `path` function retrieves the file path associated with the current instance, which is useful for identifying the location of the data being processed in…_
**Receiver:** instance — obtain a `GeoJSONFormat` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `path` **(primary)**

## [GeoJSONScanBuilder](api/GeoJSONScanBuilder.md)
_Finalize the vector layer and return it for further processing or output._
**Receiver:** instance — obtain a `GeoJSONScanBuilder` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `build` **(primary)**

## [GeoJSONTable](api/GeoJSONTable.md)
_Infers the schema of a dataset based on the provided files and options, facilitating the understanding of the data structure for geospatial analysis._
**Receiver:** instance — obtain a `GeoJSONTable` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `inferSchema` **(primary)**

## [GeoTiffWriter](api/GeoTiffWriter.md)
_The `saveAsGeoTiff` function saves a distributed raster dataset (RDD of tiles) to a GeoTIFF file format, enabling the output of processed geospatial raster…_
**Receiver:** instance — obtain a `GeoTiffWriter` value, then `<value>.<method>(...)`
**APIs:** ★ `saveAsGeoTiff` **(primary)**, ⚠️ `count`

## [GeometricSummary](api/GeometricSummary.md)
_Calculates the estimated output size for a given set of spatial features based on specified options._
**Receiver:** static object — call `GeometricSummary.<method>(...)`
**APIs:** ⚠️ `computeForFeaturesWithOutputSize` **(primary)**

## [GeometryQuadSplitter](api/GeometryQuadSplitter.md)
_The `splitGeometryAcrossDateLine` function is designed to handle geometries that may cross the dateline, ensuring accurate representation in geospatial…_
**Receiver:** instance — obtain a `GeometryQuadSplitter` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `splitGeometryAcrossDateLine` **(primary)**

## [GetPointValue](api/GetPointValue.md)
_The `process` function retrieves the value of a raster at a specified point (defined by `pointX` and `pointY`) from a GeoTIFF file._
**Receiver:** static object — call `GetPointValue.<method>(...)`
**APIs:** ⚠️ `process` **(primary)**

## [GriddedSummary](api/GriddedSummary.md)
_`computeForFeatures` computes a synopsis of the provided spatial features, which can be used for efficient spatial analysis and processing._
**Receiver:** static object — call `GriddedSummary.<method>(...)`
**APIs:** ⚠️ `computeForFeatures` **(primary)**

## [HDF4Reader](api/HDF4Reader.md)
_The `createTileIDFilter` function generates a filter that selects raster tiles based on their identifiers, ensuring they fall within a specified rectangular…_
**Receiver:** instance — obtain a `HDF4Reader` value, then `<value>.<method>(...)`
**APIs:** ★ `createTileIDFilter` **(primary)**, ★ `metadata`, ⚠️ `createDateFilter`, ⚠️ `readTile`

## [HistogramOP](api/HistogramOP.md)
_`computePointHistogramSparse` computes a histogram of point features in a spatial dataset, efficiently aggregating data into specified buckets to facilitate…_
**Receiver:** static object — call `HistogramOP.<method>(...)`
**APIs:** ⚠️ `computePointHistogramSparse` **(primary)**

## [IFeature](api/IFeature.md)
_Retrieve the geometric representation of a feature, which is essential for spatial analysis in geospatial raster processing._
**Receiver:** instance — obtain a `IFeature` value, then `<value>.<method>(...)`
**APIs:** ★ `getGeometry` **(primary)**, ★ `getStorageSize`, ⚠️ `getAttributeName`, ⚠️ `getName`

## [ITile](api/ITile.md)
_The `componentType` method retrieves the data type of each component in a raster tile, which is essential for understanding the pixel value representation in…_
**Receiver:** instance — obtain a `ITile` value, then `<value>.<method>(...)`
**APIs:** ★ `componentType` **(primary)**, ★ `numComponents`, ★ `pixelLocations`, ⚠️ `extents`, ⚠️ `getPointValue`, ⚠️ `isDefined`, ⚠️ `isEmptyAt`, ⚠️ `pixelType`, ⚠️ `pixels`

## [ImageIterator](api/ImageIterator.md)
_The `image` function is designed to perform internal processing related to raster images within the RDPro library._
**Receiver:** instance — obtain a `ImageIterator` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `image` **(primary)**

## [IndexBuilder](api/IndexBuilder.md)
_`buildIndex` creates an index for all GeoTIFF files located in a specified directory, facilitating efficient access and processing of raster data in…_
**Receiver:** static object — call `IndexBuilder.<method>(...)`
**APIs:** ⚠️ `buildIndex` **(primary)**

## [IndexHelper](api/IndexHelper.md)
_Constructs a spatial partitioner for a given set of features to optimize the distribution of spatial data across partitions in a Spark job._
**Receiver:** static object — call `IndexHelper.<method>(...)`
**APIs:** ⚠️ `createPartitioner` **(primary)**, ⚠️ `partitionFeatures`, ⚠️ `partitionFeatures2`, ⚠️ `runDuplicateAvoidance`, ⚠️ `saveIndex2`

## [IndexMixin](api/IndexMixin.md)
_The `partitionBy` function is used to reorganize a spatial RDD into partitions based on a specified spatial partitioning strategy, optimizing spatial queries…_
**Receiver:** instance — obtain a `IndexMixin` value, then `<value>.<method>(...)`
**APIs:** ★ `partitionBy` **(primary)**

## [IntermediateVectorTile](api/IntermediateVectorTile.md)
_The `rasterizeGeometry` function plots a given geometry onto the raster's blocked pixels, allowing for the visualization of vector geometries in a raster…_
**Receiver:** instance — obtain a `IntermediateVectorTile` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `rasterizeGeometry` **(primary)**, ⚠️ `simplifyGeometry`, ⚠️ `trimLineSegment`

## [JavaSpatialRDDHelper](api/JavaSpatialRDDHelper.md)
_`plotImage` generates a visual representation of spatial features from a `JavaSpatialRDD` and saves it as an image file._
**Receiver:** static object — call `JavaSpatialRDDHelper.<method>(...)`
**APIs:** ★ `plotImage` **(primary)**, ★ `saveAsGeoJSON`, ⚠️ `isSpatiallyPartitioned`, ⚠️ `rangeQuery`, ⚠️ `raptorJoin`, ⚠️ `reproject`, ⚠️ `saveAsCSVPoints`, ⚠️ `saveAsIndex`, ⚠️ `saveAsKML`, ⚠️ `saveAsShapefile`, ⚠️ `saveAsWKTFile`, ⚠️ `spatialPartition`, ⚠️ `summary`, ⚠️ `writeSpatialFile`

## [JavaSpatialSparkContext](api/JavaSpatialSparkContext.md)
_Loads a GeoTIFF file and returns its content as a distributed collection of raster tiles for further geospatial analysis._
**Receiver:** instance — obtain a `JavaSpatialSparkContext` value, then `<value>.<method>(...)`
**APIs:** ★ `geoTiff` **(primary)**, ★ `geojsonFile`, ★ `shapefile`, ★ `spatialFile`, ⚠️ `hdfFile`, ⚠️ `readCSVPoint`, ⚠️ `readWKTFile`

## [KryoInputToObjectInput](api/KryoInputToObjectInput.md)
_The `available` method returns the number of bytes that can be read from the input stream without blocking, which is useful for understanding how much data is…_
**Receiver:** instance — obtain a `KryoInputToObjectInput` value, then `<value>.<method>(...)`
**APIs:** ★ `available` **(primary)**, ⚠️ `read`

## [KryoOutputToObjectOutput](api/KryoOutputToObjectOutput.md)
_The `close` method is used to release any resources associated with the raster processing operation, ensuring that all file handles and memory are properly…_
**Receiver:** instance — obtain a `KryoOutputToObjectOutput` value, then `<value>.<method>(...)`
**APIs:** ★ `close` **(primary)**, ⚠️ `write`

## [LRUCache](api/LRUCache.md)
_The `size` function retrieves the size of a raster dataset in bytes, which is essential for understanding memory usage and data management in geospatial…_
**Receiver:** instance — obtain a `LRUCache` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `size` **(primary)**

## [LiteGeometry](api/LiteGeometry.md)
_Calculates the area of a geometric shape represented in the raster data._
**Receiver:** instance — obtain a `LiteGeometry` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `area` **(primary)**, ⚠️ `isCW`, ⚠️ `part`

## [MVTDataVisualizer](api/MVTDataVisualizer.md)
_`plotAllTiles` generates and visualizes raster tiles for a specified range of zoom levels based on the provided spatial features and configuration options._
**Receiver:** static object — call `MVTDataVisualizer.<method>(...)`
**APIs:** ⚠️ `plotAllTiles` **(primary)**, ⚠️ `plotSingleTileParallel`, ⚠️ `saveTiles`, ⚠️ `saveTilesCompact`

## [MemoryTile](api/MemoryTile.md)
_The `compress` function optimizes the storage of raster data by compressing the pixel values in memory, which can improve performance and reduce memory usage…_
**Receiver:** instance — obtain a `MemoryTile` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `compress` **(primary)**, ⚠️ `decompress`

## [MemoryTile2](api/MemoryTile2.md)
_The `setPixelValue` function sets the value of a specific pixel in a raster tile, allowing for pixel-level modifications in geospatial raster processing._
**Receiver:** instance — obtain a `MemoryTile2` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `setPixelValue` **(primary)**

## [MemoryTileWindow](api/MemoryTileWindow.md)
_The `getValue` function retrieves the value associated with a specified key from a hashtable stored in a file, returning the value if found or null if not._
**Receiver:** static object — call `MemoryTileWindow.<method>(...)`
**APIs:** ⚠️ `getValue` **(primary)**

## [MultilevelPlot](api/MultilevelPlot.md)
_The `plotFeatures` function generates a visual representation of spatial features by plotting them onto a single image, allowing for customizable dimensions…_
**Receiver:** static object — call `MultilevelPlot.<method>(...)`
**APIs:** ⚠️ `plotFeatures` **(primary)**

## [OperationHelper](api/OperationHelper.md)
_`checkOptions` validates the user-provided command line options to ensure that all required options are present and no unexpected options are included._
**Receiver:** static object — call `OperationHelper.<method>(...)`
**APIs:** ⚠️ `checkOptions` **(primary)**, ⚠️ `getOperationParams`, ⚠️ `printOperationUsage`, ⚠️ `readConfigurationXML`

## [PointSampleAccumulator](api/PointSampleAccumulator.md)
_The `add` function accumulates features or points into a summary accumulator for further statistical analysis._
**Receiver:** instance — obtain a `PointSampleAccumulator` value, then `<value>.<method>(...)`
**APIs:** ★ `add` **(primary)**, ⚠️ `merge`, ⚠️ `value`

## [PointSampler](api/PointSampler.md)
_The `pointSample` function retrieves a sample of points from a given spatial RDD, ensuring that the sample size does not exceed the specified limit._
**Receiver:** static object — call `PointSampler.<method>(...)`
**APIs:** ⚠️ `pointSample` **(primary)**

## [RaptorJoin](api/RaptorJoin.md)
_`raptorJoinFeature` performs a spatial join between a raster dataset and a set of vector features, returning information about the pixels that intersect with…_
**Receiver:** static object — call `RaptorJoin.<method>(...)`
**APIs:** ★ `raptorJoinFeature` **(primary)**, ★ `raptorJoinIDFull`

## [RaptorMixin](api/RaptorMixin.md)
_The `flatten` function extracts all pixel values from a `RasterRDD` and returns them along with their respective pixel locations and metadata, facilitating…_
**Receiver:** instance — obtain a `RaptorMixin` value, then `<value>.<method>(...)`
**APIs:** ★ `flatten` **(primary)**, ★ `rasterizePixels`, ★ `rasterizePoints`

## [RasterFeature](api/RasterFeature.md)
_The `append` function adds an additional attribute to a geospatial feature, returning a new feature that includes the original geometry and attributes along…_
**Receiver:** instance — obtain a `RasterFeature` value, then `<value>.<method>(...)`
**APIs:** ★ `append` **(primary)**, ★ `create`

## [RasterFileRDD](api/RasterFileRDD.md)
_`selectFiles` retrieves a list of raster files from a specified directory that may intersect with a defined geographical range, optimizing the selection using…_
**Receiver:** instance — obtain a `RasterFileRDD` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `selectFiles` **(primary)**

## [RasterMetadata](api/RasterMetadata.md)
_The `tileIDs` function retrieves an iterator over all tile IDs present in the raster, facilitating operations that require knowledge of the raster's tile…_
**Receiver:** instance — obtain a `RasterMetadata` value, then `<value>.<method>(...)`
**APIs:** ★ `tileIDs` **(primary)**, ⚠️ `envelope`, ⚠️ `getTileIDAtPixel`, ⚠️ `getTileIDAtPoint`, ⚠️ `gridToModel`, ⚠️ `modelToGrid`, ⚠️ `numTiles`, ⚠️ `rasterHeight`, ⚠️ `rasterWidth`, ⚠️ `rescale`, ⚠️ `retile`

## [RasterOperationsFocal](api/RasterOperationsFocal.md)
_`divideScene` partitions an existing raster RDD into smaller groups of tiles, each associated with a single metadata object, facilitating organized output when…_
**Receiver:** static object — call `RasterOperationsFocal.<method>(...)`
**APIs:** ⚠️ `divideScene` **(primary)**, ⚠️ `reshapeAverage`, ⚠️ `reshapeNN`, ⚠️ `slidingWindow`

## [RasterOperationsLocal](api/RasterOperationsLocal.md)
_The `explode` function separates each tile in a `RasterRDD` into its own individual raster, allowing for more granular processing of raster data._
**Receiver:** static object — call `RasterOperationsLocal.<method>(...)`
**APIs:** ★ `explode` **(primary)**, ★ `filterPixels`, ★ `mapPixels`, ★ `overlay`

## [RasterPartitioner](api/RasterPartitioner.md)
_The `getPartition` function determines the partition ID associated with a specific tile ID within the raster metadata, facilitating efficient data processing…_
**Receiver:** instance — obtain a `RasterPartitioner` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `getPartition` **(primary)**

## [RasterThumbnail](api/RasterThumbnail.md)
_`addDependentClasses` registers dependent classes required for processing based on the provided options in the context of geospatial raster analysis._
**Receiver:** static object — call `RasterThumbnail.<method>(...)`
**APIs:** ★ `addDependentClasses` **(primary)**

## [ReadWriteMixin](api/ReadWriteMixin.md)
_`generateSpatialData` generates a `SpatialRDD` containing randomly created geometries based on specified distribution types and parameters, facilitating…_
**Receiver:** instance — obtain a `ReadWriteMixin` value, then `<value>.<method>(...)`
**APIs:** ★ `generateSpatialData` **(primary)**

## [Reprojector](api/Reprojector.md)
_The `findTransformationInfo` function retrieves or creates a mathematical transformation to convert coordinates between two specified coordinate reference…_
**Receiver:** static object — call `Reprojector.<method>(...)`
**APIs:** ★ `findTransformationInfo` **(primary)**, ★ `reprojectEnvelope`, ★ `reprojectGeometry`, ★ `reprojectRDD`, ⚠️ `reprojectEnvelopeInPlace`

## [SQLQueryHelper](api/SQLQueryHelper.md)
_`extractTables` analyzes an SQL query to determine its syntactical correctness and retrieves the names of the tables referenced in the query._
**Receiver:** static object — call `SQLQueryHelper.<method>(...)`
**APIs:** ⚠️ `extractTables` **(primary)**

## [SVGPlotter](api/SVGPlotter.md)
_The `getTitle` function extracts and returns a formatted title string for a given feature by interpolating predefined title templates with the feature's…_
**Receiver:** instance — obtain a `SVGPlotter` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `getTitle` **(primary)**, ⚠️ `plot`

## [ScalaSparkTest](api/ScalaSparkTest.md)
_Retrieve the current `SparkContext` instance, which is essential for executing distributed raster processing tasks in RDPro._
**Receiver:** instance — obtain a `ScalaSparkTest` value, then `<value>.<method>(...)`
**APIs:** ★ `sparkContext` **(primary)**, ⚠️ `copyResource`, ⚠️ `locateResource`, ⚠️ `readFile`, ⚠️ `readTextResource`, ⚠️ `sparkSession`, ⚠️ `using`

## [ShapefileReader](api/ShapefileReader.md)
_The `initialized` function checks whether the file has been successfully initialized for processing within the RDPro framework._
**Receiver:** instance — obtain a `ShapefileReader` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `initialized` **(primary)**

## [ShapefileWriter](api/ShapefileWriter.md)
_The `initialize` function sets up the necessary parameters and configurations for reading raster data from a specified source in the RDPro library._
**Receiver:** instance — obtain a `ShapefileWriter` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `initialize` **(primary)**

## [SlidingWindowTile](api/SlidingWindowTile.md)
_`x1` retrieves the x-coordinate of the first pixel in a raster tile._
**Receiver:** instance — obtain a `SlidingWindowTile` value, then `<value>.<method>(...)`
**APIs:** ★ `x1` **(primary)**, ★ `x2`, ★ `y1`, ★ `y2`, ⚠️ `addTile`

## [SnapTransform](api/SnapTransform.md)
_The `transform` function applies a geometric transformation to a set of source points, converting their coordinates to a destination coordinate system._
**Receiver:** instance — obtain a `SnapTransform` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `transform` **(primary)**

## [SpatialFilePartition2](api/SpatialFilePartition2.md)
_Retrieve the end value of a spatial file partition, which is relevant for managing raster data processing in distributed environments._
**Receiver:** instance — obtain a `SpatialFilePartition2` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `end` **(primary)**

## [SpatialFileRDD](api/SpatialFileRDD.md)
_The `createPartitions` function creates partitions for a given input file, enabling distributed processing of geospatial raster data in Spark._
**Receiver:** instance — obtain a `SpatialFileRDD` value, then `<value>.<method>(...)`
**APIs:** ★ `createPartitions` **(primary)**, ★ `getFeatureReaderClass`, ★ `readLocal`, ★ `readPartition`, ⚠️ `skipDuplicateAvoidance`

## [SpatialFileSource](api/SpatialFileSource.md)
_Returns the name of the operation or process being executed within the RDPro framework._
**Receiver:** instance — obtain a `SpatialFileSource` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `name` **(primary)**

## [SpatialGenerator](api/SpatialGenerator.md)
_The `affineTransform` function applies an affine transformation matrix to spatial data, enabling geometric transformations such as scaling, translation, and…_
**Receiver:** instance — obtain a `SpatialGenerator` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `affineTransform` **(primary)**, ⚠️ `normal`, ⚠️ `uniform`

## [SpatialGeneratorBuilder](api/SpatialGeneratorBuilder.md)
_The `config` function sets configuration options for the spatial data generation process in RDPro._
**Receiver:** instance — obtain a `SpatialGeneratorBuilder` value, then `<value>.<method>(...)`
**APIs:** ★ `config` **(primary)**, ★ `diagonal`, ★ `distribution`, ★ `makeBoxes`, ★ `mbr`, ★ `parcel`, ★ `sierpinski`, ⚠️ `bit`, ⚠️ `gaussian`, ⚠️ `generate`, ⚠️ `numPartitions`

## [SpatialJoin](api/SpatialJoin.md)
_`spatialJoin` performs a spatial join operation between two `SpatialRDD` datasets, returning pairs of matching features based on a specified join predicate._
**Receiver:** static object — call `SpatialJoin.<method>(...)`
**APIs:** ⚠️ `spatialJoin` **(primary)**, ⚠️ `spatialJoinBNLJ`, ⚠️ `spatialJoinDJ`, ⚠️ `spatialJoinIntersectsPlaneSweepFeatures`, ⚠️ `spatialJoinPBSM`, ⚠️ `spatialJoinRepJ`

## [SpatialParquetHelper](api/SpatialParquetHelper.md)
_Encodes a geometric shape into a feature representation for further processing in geospatial analysis._
**Receiver:** static object — call `SpatialParquetHelper.<method>(...)`
**APIs:** ⚠️ `encodeGeometry` **(primary)**

## [SpatialParquetSource](api/SpatialParquetSource.md)
_Decodes a `DataFrame` that has been encoded in the SpatialParquet format, allowing for the retrieval of spatial data._
**Receiver:** static object — call `SpatialParquetSource.<method>(...)`
**APIs:** ⚠️ `decodeSpatialParquet` **(primary)**, ⚠️ `encodeGeoParquet`, ⚠️ `encodeSpatialParquet`

## [SpatialPartition](api/SpatialPartition.md)
_`numFeatures` retrieves the total count of features (records) present in the current partition of the dataset._
**Receiver:** instance — obtain a `SpatialPartition` value, then `<value>.<method>(...)`
**APIs:** ★ `numFeatures` **(primary)**, ⚠️ `numNonEmptyGeometries`, ⚠️ `numPoints`, ⚠️ `sumSideLength`

## [SpatialReader](api/SpatialReader.md)
_The `readInput` function loads spatial data from a specified file into a distributed spatial RDD for further geospatial analysis._
**Receiver:** static object — call `SpatialReader.<method>(...)`
**APIs:** ⚠️ `readInput` **(primary)**

## [SpatialWriter](api/SpatialWriter.md)
_`saveFeatures` saves a set of geospatial features to a specified output format, enabling users to persist processed spatial data for further analysis or…_
**Receiver:** static object — call `SpatialWriter.<method>(...)`
**APIs:** ⚠️ `saveFeatures` **(primary)**

## [StaticFileWebHandler](api/StaticFileWebHandler.md)
_The `setup` function initializes the processing environment for RDPro, configuring it with the necessary Spark context or session and options for raster…_
**Receiver:** instance — obtain a `StaticFileWebHandler` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `setup` **(primary)**

## [Summary](api/Summary.md)
_The `createSummaryAccumulator` function initializes a summary accumulator to collect and aggregate the sizes of geospatial features in a distributed Spark…_
**Receiver:** instance — obtain a `Summary` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `createSummaryAccumulator` **(primary)**

## [VectorCanvas](api/VectorCanvas.md)
_The `addGeometry` function adds a specified geometry to the canvas, potentially modifying the existing geometries to ensure the canvas remains manageable._
**Receiver:** instance — obtain a `VectorCanvas` value, then `<value>.<method>(...)`
**APIs:** ★ `addGeometry` **(primary)**, ⚠️ `createRingsForOccupiedPixels`, ⚠️ `findIntersections`

## [VectorLayerBuilder](api/VectorLayerBuilder.md)
_The `zigzagDecode` function decodes a value that has been encoded using Zigzag encoding, which is commonly used in data serialization to efficiently represent…_
**Receiver:** instance — obtain a `VectorLayerBuilder` value, then `<value>.<method>(...)`
**APIs:** ★ `zigzagDecode` **(primary)**, ⚠️ `addFeature`

## [VisualizationMixin](api/VisualizationMixin.md)
_`plotPyramid` generates a multilevel tiled image representation of a dataset and saves it to a specified output path._
**Receiver:** instance — obtain a `VisualizationMixin` value, then `<value>.<method>(...)`
**APIs:** ⚠️ `plotPyramid` **(primary)**

## [ZipUtil](api/ZipUtil.md)
_`putStoredFile` adds a file to a ZIP archive without compression, allowing for efficient storage of binary data._
**Receiver:** static object — call `ZipUtil.<method>(...)`
**APIs:** ★ `putStoredFile` **(primary)**, ⚠️ `lastNFiles`, ⚠️ `listFilesInZip`, ⚠️ `mergeZip`

## [ZonalStatistics](api/ZonalStatistics.md)
_`zonalStats2` computes zonal statistics for specified polygonal regions over a raster dataset, providing insights into the pixel values within those zones._
**Receiver:** static object — call `ZonalStatistics.<method>(...)`
**APIs:** ⚠️ `zonalStats2` **(primary)**, ⚠️ `zonalStatsLocal`
