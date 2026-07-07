# Reprojector

_The `findTransformationInfo` function retrieves or creates a mathematical transformation to convert coordinates between two specified coordinate reference…_

**Receiver:** static object — call `Reprojector.<method>(...)`

**Members** (most robust first): ★ `findTransformationInfo` **(primary)**, ★ `reprojectEnvelope`, ★ `reprojectGeometry`, ★ `reprojectRDD`, ⚠️ `reprojectEnvelopeInPlace`

---

## API Test: `findTransformationInfo`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def findTransformationInfo(sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetSRID: Int): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetCRS: CoordinateReferenceSystem): TransformationInfo
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:146  (+2 more definition site/overload)_

_Source doc:_ Creates or retrieves a cached math transform to transform between the given two CRS @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return the math transformation that transforms from source to destination

### Goal
The `findTransformationInfo` function retrieves or creates a mathematical transformation to convert coordinates between two specified coordinate reference systems (CRS).

### Parameters
- `sourceCRS` (`CoordinateReferenceSystem`): The source coordinate reference system from which the transformation will be applied. This can be any valid CRS, such as EPSG codes or custom defined systems.
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system to which the coordinates will be transformed. Similar to `sourceCRS`, this can also be any valid CRS.

### Input
The caller must provide two valid `CoordinateReferenceSystem` instances or their corresponding SRID integers. The input CRS must be properly defined and accessible within the context of the transformation.

### Output
Returns `TransformationInfo` — an object that encapsulates the mathematical transformation needed to convert coordinates from the `sourceCRS` to the `targetCRS`. This object contains the necessary information to perform the transformation.

### Valid Call Patterns
```scala
val transformInfo: TransformationInfo = Reprojector.findTransformationInfo(sourceCRS, targetCRS)
val transformInfoBySRID: TransformationInfo = Reprojector.findTransformationInfo(4326, targetCRS)
```

### LLM Instruction Prompt
- When calling `findTransformationInfo`, ensure that both `sourceCRS` and `targetCRS` are valid instances of `CoordinateReferenceSystem` or valid SRID integers. The function should be used to obtain a transformation for geospatial data processing tasks.

### Prompt Snippet
```text
Use the `findTransformationInfo` function to obtain a transformation between two coordinate reference systems, ensuring that both inputs are valid CRS instances or SRID integers.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the `sourceCRS` and `targetCRS` are correctly defined and accessible. If using SRIDs, verify that they correspond to valid and compatible coordinate reference systems.
```

## API Test: `reprojectEnvelope`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def reprojectEnvelope(envelope: Envelope, sourceSRID: Int, targetSRID: Int): Envelope
def reprojectEnvelope(envelope: Envelope, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Envelope
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:427  (+1 more definition site/overload)_

_Source doc:_ Reprojects an envelope from one SRID to another SRID @param envelope the envelope to reproject with dimensions in source SRID @param sourceSRID the SRID of the given envelope @param targetSRID the desired SRID of the reprojected envelope @return the envelope after being reprojected to target SRID

### Goal
Reprojects a given geospatial envelope from one spatial reference system identifier (SRID) to another, allowing for accurate spatial analysis across different coordinate systems.

### Parameters
- `envelope` (`Envelope`): The geospatial envelope that defines a rectangular area in the source coordinate system. It is expected to contain the minimum and maximum coordinates that represent the bounds of the area.
- `sourceSRID` (`Int`): The spatial reference system identifier (SRID) of the provided envelope, indicating the coordinate system in which the envelope's dimensions are defined.
- `targetSRID` (`Int`): The desired spatial reference system identifier (SRID) to which the envelope should be reprojected, allowing for compatibility with other datasets in that coordinate system.

### Input
The caller must provide an `Envelope` object representing the area to be reprojected, along with the integer SRIDs for both the source and target coordinate systems. The input envelope must be valid and properly defined in the source SRID.

### Output
Returns `Envelope` — a new envelope that represents the same area as the input envelope but reprojected to the target SRID. The output envelope maintains the same structure as the input envelope, with updated coordinates reflecting the new coordinate system.

### Valid Call Patterns
```scala
val reprojectedEnvelope: Envelope = Reprojector.reprojectEnvelope(originalEnvelope, sourceSRID, targetSRID)
```

### LLM Instruction Prompt
- Ensure that the input envelope is valid and that the source and target SRIDs are correctly specified. The SRIDs must correspond to valid coordinate reference systems.

### Prompt Snippet
```text
Reproject the envelope from its original SRID to a new target SRID using the reprojectEnvelope function.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the envelope is properly defined and the SRIDs are valid before calling the function.
val validEnvelope: Envelope = new Envelope(minX, minY, maxX, maxY) // Define your envelope correctly
val reprojectedEnvelope: Envelope = Reprojector.reprojectEnvelope(validEnvelope, sourceSRID, targetSRID)
```

## API Test: `reprojectGeometry`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def reprojectGeometry(geometry: Geometry, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetSRID: Int): Geometry
def reprojectGeometry(geometry: Geometry, transform: TransformationInfo): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:274  (+3 more definition site/overload)_

_Source doc:_ Reprojects the given geometry from source to target CRS. This method ignores the SRID of the geometry and assumes it to be in the source CRS. @param geometry the geometry to transform @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return a new geometry that is transformed

### Goal
Reprojects a given geometry from one coordinate reference system (CRS) to another, facilitating accurate spatial analysis in geospatial raster processing.

### Parameters
- `geometry` (`Geometry`): The geometric shape (e.g., point, line, polygon) that needs to be transformed. It is expected to be in the source CRS.
- `sourceCRS` (`CoordinateReferenceSystem`): The original coordinate reference system of the geometry. This defines how the coordinates of the geometry are interpreted.
- `targetCRS` (`CoordinateReferenceSystem`): The desired coordinate reference system to which the geometry will be transformed.

### Input
The caller must provide a valid `Geometry` object, along with the corresponding `sourceCRS` and `targetCRS` as `CoordinateReferenceSystem` instances. The geometry should be in the same CRS as specified by `sourceCRS`.

### Output
Returns `Geometry` — a new geometry object that represents the transformed shape in the target CRS.

### Valid Call Patterns
```scala
val point: Geometry = new GeometryFactory().createPoint(new Coordinate(1, 1))
val sourceCRS: CoordinateReferenceSystem = CRS.decode("EPSG:4326", true)
val targetCRS: CoordinateReferenceSystem = CRS.decode("EPSG:3857", true)
val transformedPoint: Geometry = Reprojector.reprojectGeometry(point, sourceCRS, targetCRS)
```

### LLM Instruction Prompt
When calling `reprojectGeometry`, ensure that the geometry is in the source CRS specified, and provide the correct target CRS for the transformation.

### Prompt Snippet
```text
To reproject a geometry, use the `reprojectGeometry` function with the geometry and the source and target CRS as parameters.
```

### Common Failure Modes
- **[compile]** error: value isFinite is not a member of Double
- **[runtime]** org.apache.spark.sql.AnalysisException: Unable to infer schema for geojson. It must be specified manually.

### Fix Code Hint
```scala
Ensure that the geometry's CRS matches the `sourceCRS` provided, and verify that both CRS are correctly defined before calling `reprojectGeometry`.
```

## API Test: `reprojectRDD`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def reprojectRDD(sourceRDD: SpatialRDD, targetCRS: CoordinateReferenceSystem): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, targetSRID: Int): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, transform: TransformationInfo): SpatialRDD
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:235  (+2 more definition site/overload)_

_Source doc:_ Reproject the given RDD to the target CRS. The source CRS is retrieved from the first element of the source RDD. @param sourceRDD the RDD to transform @param targetCRS the target Coordinate Reference System @return the transformed RDD

### Goal
Reproject the input `SpatialRDD` to a specified target Coordinate Reference System (CRS).

### Parameters
- `sourceRDD` (`SpatialRDD`): The input RDD containing spatial data that needs to be transformed. The source CRS is determined from the first element of this RDD.
- `targetCRS` (`CoordinateReferenceSystem`): The target CRS to which the `sourceRDD` will be reprojected. This should be a valid CRS object representing the desired spatial reference.

### Input
The caller must provide a `SpatialRDD` containing spatial data, which can be derived from various sources such as shapefiles or raster data. The `targetCRS` must be a valid `CoordinateReferenceSystem` object. Ensure that the `sourceRDD` is properly initialized and contains valid spatial data before calling this function.

### Output
Returns `SpatialRDD` — a new RDD containing the reprojected spatial data in the specified target CRS.

### Valid Call Patterns
```scala
val projectedPolygons: RDD[IFeature] = Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))
```

### LLM Instruction Prompt
- When calling `reprojectRDD`, ensure that the `sourceRDD` is a valid `SpatialRDD` and that the `targetCRS` is a properly defined `CoordinateReferenceSystem`. 

### Prompt Snippet
```text
Reproject the spatial RDD to the desired CRS using `reprojectRDD`.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the sourceRDD is initialized and contains valid spatial data
val validSourceRDD: SpatialRDD = // initialize your SpatialRDD here
val targetCRS: CoordinateReferenceSystem = // define your target CRS here
val reprojectedRDD = Reprojector.reprojectRDD(validSourceRDD, targetCRS)
```

## API Test: `reprojectEnvelopeInPlace`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def reprojectEnvelopeInPlace(envelope: Array[Double], sourceSRID: Int, targetSRID: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:465_

_Source doc:_ Reproject an envelope (orthogonal rectangle) to the target CRS in-place @param envelope the input envelope to convert in the form (x1, y1, x2, y2) @param sourceSRID the source coordinate reference system (CRS) @param targetSRID the target coordinate reference system (CRS) @return the converted envelope

### Goal
The `reprojectEnvelopeInPlace` function reprojects a given envelope defined by its coordinates from one coordinate reference system (CRS) to another, modifying the envelope in place.

### Parameters
- `envelope` (`Array[Double]`): An array representing the coordinates of the envelope in the form (x1, y1, x2, y2), where (x1, y1) is the bottom-left corner and (x2, y2) is the top-right corner of the rectangle.
- `sourceSRID` (`Int`): The Spatial Reference Identifier (SRID) of the source coordinate reference system from which the envelope is being reprojected.
- `targetSRID` (`Int`): The SRID of the target coordinate reference system to which the envelope is being reprojected.

### Input
The caller must provide:
- An `Array[Double]` representing the envelope coordinates.
- Valid integer values for `sourceSRID` and `targetSRID` that correspond to recognized coordinate reference systems.

### Output
Returns `Unit` — this indicates that the function modifies the input `envelope` array directly, and there is no return value. The modified `envelope` will contain the reprojected coordinates.

### Valid Call Patterns
```scala
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

### LLM Instruction Prompt
- Ensure that the `envelope` array is correctly formatted and that the `sourceSRID` and `targetSRID` are valid before calling `reprojectEnvelopeInPlace`.

### Prompt Snippet
```text
Reproject the envelope from one CRS to another using the function reprojectEnvelopeInPlace.
```

### Common Failure Modes
- **[compile]** error: value isFinite is not a member of Double _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the envelope is in the correct format and the SRIDs are valid
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```
