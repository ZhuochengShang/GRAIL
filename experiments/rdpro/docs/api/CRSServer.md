# CRSServer

_The `crsToSRID` function retrieves a unique integer SRID (Spatial Reference System Identifier) corresponding to a given Coordinate Reference System (CRS),…_

**Receiver:** static object — call `CRSServer.<method>(...)`

**Members** (most robust first): ★ `crsToSRID` **(primary)**, ★ `sridToCRS`, ⚠️ `startServer`

---

## API Test: `crsToSRID`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def crsToSRID(crs: CoordinateReferenceSystem) : Int
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:270_

_Source doc:_ Get an integer SRID that corresponds to the given CRS according to the following logic. 1. If crs is null, return 0 2. Search the local cache as the fastest method of known CRS. 3. If not found in cache, look up the EPSG database to find an SRID, cache, and return it. 4a. If the server is running, contact the server to get the SRID 4b. If the server is not running, assign a custom negative SRID and cache it @param crs the CRS to find an SRID for @return a unique SRID that identifies the given CRS

### Goal
The `crsToSRID` function retrieves a unique integer SRID (Spatial Reference System Identifier) corresponding to a given Coordinate Reference System (CRS), facilitating geospatial operations in RDPro.

### Parameters
- `crs` (`CoordinateReferenceSystem`): The CRS for which the SRID is to be determined. This can be a standard CRS (e.g., EPSG:4326 for WGS 84) or a custom CRS.

### Input
The caller must provide a valid `CoordinateReferenceSystem` object. If the `crs` is null, the function will return 0. The function may also require access to a running server to retrieve SRIDs for non-standard CRSs.

### Output
Returns `Int` — an integer representing the unique SRID that identifies the given CRS. Standard EPSG codes will be positive, while custom non-standard CRSs may return negative values.

### Valid Call Patterns
```scala
CRSServer.crsToSRID(CRS.decode("EPSG:3857"))
CRSServer.crsToSRID(CRS.decode("EPSG:4326"))
```

### LLM Instruction Prompt
- When calling `crsToSRID`, ensure that the `crs` parameter is a valid `CoordinateReferenceSystem` object. If the CRS is null, expect a return value of 0.

### Prompt Snippet
```text
To retrieve the SRID for a given CRS, use the function `CRSServer.crsToSRID(crs)`, where `crs` is a valid CoordinateReferenceSystem.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
val srid = CRSServer.crsToSRID(validCRS) // Ensure validCRS is a non-null CoordinateReferenceSystem
```

## API Test: `sridToCRS`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def sridToCRS(srid: Int): CoordinateReferenceSystem
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:352_

_Source doc:_ Convert the given SRID to CRS according to the following logic. 1. If the SRID is zero, it indicates an invalid SRID and `null` is returned. 2. It searches the local cache and retrieves the SRID. 3a. If SRID is positive, use it as an EPSG, retrieve the CRS, cache and return it. 3b. If SRID is negative, contact the server, retrieve the CRS, cache and return it. @param srid the SRID that needs to be converted to a CRS @return the converted CRS.

### Goal
The `sridToCRS` function converts a given Spatial Reference Identifier (SRID) into a corresponding Coordinate Reference System (CRS) for use in geospatial raster processing.

### Parameters
- `srid` (`Int`): The Spatial Reference Identifier that needs to be converted. It can be a positive EPSG code, a negative value indicating a non-standard CRS, or zero which indicates an invalid SRID.

### Input
The caller must provide an integer SRID. The input must be a valid SRID, which can be either a positive EPSG code or a negative value for non-standard CRSs. An SRID of zero will result in a null return value.

### Output
Returns `CoordinateReferenceSystem` — this represents the CRS corresponding to the provided SRID, which can be used for geospatial operations in RDPro.

### Valid Call Patterns
```scala
val crs = CRSServer.sridToCRS(3857) // Example for a valid positive EPSG code
```

### LLM Instruction Prompt
- When calling `sridToCRS`, ensure that the provided SRID is either a valid positive EPSG code or a negative value for non-standard CRSs. Avoid using zero as it will return null.

### Prompt Snippet
```text
To convert an SRID to a Coordinate Reference System, use the `sridToCRS` function with a valid integer SRID.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the SRID is valid before calling sridToCRS
val validSrid = 4326 // Example of a valid EPSG code
val crs = CRSServer.sridToCRS(validSrid)
```

## API Test: `startServer`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def startServer(defaultPort: Int = DefaultPort): Int
def startServer(sc: SparkContext): Boolean
def startServer(jsc: JavaSparkContext): Boolean
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:91  (+2 more definition site/overload)_

_Source doc:_ Starts the server and returns the port on which it is listening @return the port on which the server is started

### Goal
The `startServer` function initializes the server for RDPro, enabling it to listen for incoming requests on a specified port.

### Parameters
- `defaultPort` (`Int`), default `DefaultPort`: The port number on which the server will listen for connections. If not specified, it defaults to a predefined constant `DefaultPort`.

### Input
The caller must provide a valid `SparkContext` or `JavaSparkContext` if using the overloaded versions. The server must be able to bind to the specified port, and the environment must have the necessary permissions to open network sockets.

### Output
Returns `Int` — the port number on which the server is successfully started and listening for requests.

### Valid Call Patterns
```scala
CRSServer.startServer(sparkContext)
```

### LLM Instruction Prompt
- When calling `startServer`, ensure that a valid `SparkContext` or `JavaSparkContext` is provided, and be aware of the default port configuration.

### Prompt Snippet
```text
To start the RDPro server, use the `startServer` method with a valid Spark context. For example, `CRSServer.startServer(sparkContext)` will start the server and return the port number.
```

### Common Failure Modes
- **[compile]** error: type mismatch; _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the SparkContext is properly initialized before calling startServer
val sparkContext: SparkContext = new SparkContext(...)
CRSServer.startServer(sparkContext)
```
