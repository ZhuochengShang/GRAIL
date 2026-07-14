## API Test: `splitGeometryAcrossDateLine`
_Grounding: doc-repaired from source (docfix)._

### Goal
Split a single-ring polygon geometry that crosses the ±180° dateline into valid hemisphere-local pieces to avoid downstream geometric errors.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter` (Scala object; call methods directly on it)
- `org.locationtech.jts.geom.Geometry` (Java class)
- `org.locationtech.jts.geom.Polygon` (Java class)

**Compilable Call Sketch:**
```scala
import edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter
import org.locationtech.jts.geom.{Geometry, Polygon}

// Assume `geom` is an existing org.locationtech.jts.geom.Geometry
// 1. The method strictly requires the SRID to be 4326
geom.setSRID(4326)

// 2. The method strictly requires a single Polygon with 0 interior rings
if (geom.getNumGeometries == 1 && 
    geom.getGeometryType == "Polygon" && 
    geom.asInstanceOf[Polygon].getNumInteriorRing == 0) {
  
  // 3. Call statically on the companion object
  val split: Geometry = GeometryQuadSplitter.splitGeometryAcrossDateLine(geom)
  val witness = (split.getNumGeometries, split.getNumPoints)
  println("__CHECK__ splitGeometryAcrossDateLine " + witness)
}
```

### LLM Instruction Prompt
- `splitGeometryAcrossDateLine` is a method on the `GeometryQuadSplitter` companion object and must be called statically (e.g., `GeometryQuadSplitter.splitGeometryAcrossDateLine(geom)`), not on an instance of the class.
- The input geometry must explicitly have its SRID set to 4326 (`geometry.setSRID(4326)`), otherwise it will fail a runtime `require` check.
- The input geometry must be exactly of type `Polygon` (`geometry.getGeometryType == "Polygon"`), have exactly 1 geometry (`geometry.getNumGeometries == 1`), and have exactly 0 interior rings.

### Prompt Snippet
```text
Given a JTS Geometry, first set its SRID to 4326. Then, verify it is a single Polygon with zero interior rings. If it matches, call the static method GeometryQuadSplitter.splitGeometryAcrossDateLine(geom) to handle dateline crossing. Do not instantiate GeometryQuadSplitter.
```

### Common Failure Modes
- **Instantiating the object:** Attempting to instantiate `new GeometryQuadSplitter(...)` fails because it lacks constructor arguments and the method is defined on the companion object.
- **Missing SRID:** Failing to explicitly call `geometry.setSRID(4326)` triggers a runtime `IllegalArgumentException` ("Can only work with geometries in the EPSG:4326 format").
- **Invalid Geometry Type:** Passing a MultiPolygon, a LineString, or a Polygon with holes triggers runtime `require` failures ("expects a simple geometry", "expects a polygon geometry", "expects a single ring").

### Fix Code Hint
**WRONG:**
```scala
// Fails: Instantiates class instead of using object, misses SRID and type checks
val splitter = new GeometryQuadSplitter(geom, 1)
val split = splitter.splitGeometryAcrossDateLine(geom)
```

**CORRECT:**
```scala
// Succeeds: Sets SRID, checks type/rings, calls statically on the object
geom.setSRID(4326)
if (geom.getNumGeometries == 1 && geom.getGeometryType == "Polygon" && geom.asInstanceOf[org.locationtech.jts.geom.Polygon].getNumInteriorRing == 0) {
  val split = edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter.splitGeometryAcrossDateLine(geom)
}
```