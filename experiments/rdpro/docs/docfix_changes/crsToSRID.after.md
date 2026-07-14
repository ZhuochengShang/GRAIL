## API Test: `crsToSRID`
_Grounding: doc-repaired from source (docfix)._

### Goal
Convert a `CoordinateReferenceSystem` object into a unique integer SRID for use in Beast/RDPro CRS-aware raster/vector processing pipelines.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS:
import org.opengis.referencing.crs.CoordinateReferenceSystem // Java interface
import org.geotools.referencing.CRS // Java class
import org.apache.spark.beast.CRSServer // Scala object

// To obtain a CoordinateReferenceSystem for testing, decode an EPSG string:
val crs: CoordinateReferenceSystem = CRS.decode("EPSG:4326")
val srid: Int = CRSServer.crsToSRID(crs)

// Null yields 0
val nullSRID: Int = CRSServer.crsToSRID(null)
```

### LLM Instruction Prompt
- To obtain a `CoordinateReferenceSystem` for testing, use `org.geotools.referencing.CRS.decode("EPSG:...")`.
- Do not attempt to extract a CRS from `RasterFeature` using `.raster.getCRS` as it does not exist.
- Provide the fully qualified names for `CoordinateReferenceSystem` (`org.opengis.referencing.crs.CoordinateReferenceSystem`) and `CRS` (`org.geotools.referencing.CRS`).
- Use the receiver exactly as `org.apache.spark.beast.CRSServer.crsToSRID(crs)`.
- Expect `0` for `null`.

### Prompt Snippet
```text
Given a CoordinateReferenceSystem object `crs` (created via `org.geotools.referencing.CRS.decode("EPSG:4326")`), call `CRSServer.crsToSRID(crs)` to get its SRID. Do not try to extract CRS from a RasterFeature.
```

### Common Failure Modes
- **Inventing non-existent methods:** Attempting to extract a CRS from a `rasterRDD` by guessing the internal structure of `RasterFeature` (e.g., calling `.raster.getCRS`). This does not exist.
- **Missing Imports:** Omitting the required fully-qualified imports for `CRS` and `CoordinateReferenceSystem`, leading to compilation failures when trying to decode an EPSG string.
- **Wrong Input Type:** Passing an EPSG string (e.g., `"EPSG:4326"`) directly to `crsToSRID` instead of a decoded `CoordinateReferenceSystem` object.

### Fix Code Hint
```scala
// WRONG: Guessing RasterFeature structure or missing imports
// val crs = feature.raster.getCRS // Fails: getCRS does not exist on RasterFeature
// val srid = CRSServer.crsToSRID(crs)

// CORRECT: Use fully qualified GeoTools CRS decoder
import org.opengis.referencing.crs.CoordinateReferenceSystem
import org.geotools.referencing.CRS
import org.apache.spark.beast.CRSServer

val crs: CoordinateReferenceSystem = CRS.decode("EPSG:4326")
val srid: Int = CRSServer.crsToSRID(crs)
```