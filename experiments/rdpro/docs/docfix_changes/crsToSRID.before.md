## API Test: `crsToSRID`

### Signature
```scala
def crsToSRID(crs: CoordinateReferenceSystem) : Int
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:270_

_Source doc:_ Get an integer SRID that corresponds to the given CRS according to the following logic. 1. If crs is null, return 0 2. Search the local cache as the fastest method of known CRS. 3. If not found in cache, look up the the EPSG database to find an SRID, cache, and return it. 4a. If the server is running, contact the server to get the SRID 4b. If the server is not running, assign a custom negative SRID and cache it @param crs the CRS to find an SRID for @return a unique SRID that identifies the given CRS

### Goal
Convert a CRS object into a unique integer SRID for use in Beast/RDPro CRS-aware raster/vector processing pipelines.

### Parameters
- `crs` (`CoordinateReferenceSystem`): The CRS instance to resolve to an SRID (can be a standard EPSG CRS or a non-standard/custom CRS; if `null`, result is `0`).

### Input
Caller must provide a `CoordinateReferenceSystem` object (not a file path or raster directly).  
Preconditions and behavior rules from the API doc:

- If `crs == null`, the function returns `0`.
- The method first checks a local CRS→SRID cache.
- If not cached, it tries EPSG lookup.
- If still unresolved:
  - with CRS server running: it contacts the server to obtain SRID.
  - with CRS server not running: it assigns a custom **negative** SRID and caches it.

No raster format/type-selection rule applies directly to this function.

### Output
Returns `Int` — a unique SRID identifier for the input CRS:
- `0` for `null` CRS,
- typically positive EPSG code for standard CRS (e.g., 4326, 3857),
- custom negative SRID for non-standard CRS when needed.

### Valid Call Patterns
```scala
val mercator = CRS.decode("EPSG:3857")
val sridMercator = CRSServer.crsToSRID(mercator)

val wgs84 = CRS.decode("EPSG:4326")
val sridWGS84 = CRSServer.crsToSRID(wgs84)
```

```scala
val sinusoidal = new DefaultProjectedCRS("Sinusoidal", new DefaultGeographicCRS(new DefaultGeodeticDatum("World", DefaultEllipsoid.WGS84, DefaultPrimeMeridian.GREENWICH), DefaultEllipsoidalCS.GEODETIC_2D),
  new DefaultMathTransformFactory().createFromWKT("PARAM_MT[\"Sinusoidal\", \n  PARAMETER[\"semi_major\", 6371007.181], \n  PARAMETER[\"semi_minor\", 6371007.181], \n  PARAMETER[\"central_meridian\", 0.0], \n  PARAMETER[\"false_easting\", 0.0], \n  PARAMETER[\"false_northing\", 0.0]]"), DefaultCartesianCS.PROJECTED)
val sridSinusoidal = CRSServer.crsToSRID(sinusoidal)
```

### LLM Instruction Prompt
- Use the receiver exactly as `CRSServer.crsToSRID(crs)`.
- Pass a `CoordinateReferenceSystem` object only.
- Do not pass file paths, EPSG strings, or integers directly to this function.
- Expect `0` for `null`.
- For standard CRS, expect EPSG-like positive SRIDs when resolvable.
- For non-standard CRS, allow negative SRID assignment (especially when server is not running).

### Prompt Snippet
```text
Given a CoordinateReferenceSystem object `crs`, call `CRSServer.crsToSRID(crs)` to get its SRID.
If `crs` is null, expect 0.
If CRS is standard (e.g., EPSG:4326), expect a positive EPSG SRID when available.
If CRS is custom/non-EPSG, the returned SRID may be negative.
```

### Common Failure Modes
- Passing the wrong input type (e.g., `"EPSG:4326"` string instead of a `CoordinateReferenceSystem` object).
- Assuming non-standard CRS must always map to a positive EPSG SRID.
- Ignoring the documented `null` behavior (`0`).
- Calling as bare `crsToSRID(...)` without `CRSServer` receiver (call form mismatch with verified usage).

### Fix Code Hint
```scala
// Correct: create/obtain a CoordinateReferenceSystem first, then call through CRSServer
val crs: CoordinateReferenceSystem = CRS.decode("EPSG:4326")
val srid: Int = CRSServer.crsToSRID(crs)
```