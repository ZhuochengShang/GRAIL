# GetPointValue

_The `process` function retrieves the value of a raster at a specified point (defined by `pointX` and `pointY`) from a GeoTIFF file._

**Receiver:** static object — call `GetPointValue.<method>(...)`

**Members** (most robust first): ⚠️ `process` **(primary)**

---

## API Test: `process`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
private def process(inputMBR: Rectangle, filePath: String): Option[String]
private def process(filePath: String, pointX: Double, pointY: Double): Option[(String, Int)]
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/raptorhunt/GetPointValue.scala:134  (+1 more definition site/overload)_

### Goal
The `process` function retrieves the value of a raster at a specified point (defined by `pointX` and `pointY`) from a GeoTIFF file.

### Parameters
- `filePath` (`String`): The path to the GeoTIFF file from which the raster data will be read. This should be a valid file path pointing to an accessible GeoTIFF file.
- `pointX` (`Double`): The X-coordinate (longitude) of the point for which the raster value is to be retrieved. This should be in the same coordinate reference system (CRS) as the raster data.
- `pointY` (`Double`): The Y-coordinate (latitude) of the point for which the raster value is to be retrieved. This should also be in the same CRS as the raster data.

### Input
The caller must provide:
- A valid file path to a GeoTIFF file.
- Coordinates (`pointX` and `pointY`) that correspond to a location within the bounds of the raster data. The coordinates must be in the same CRS as the raster.

### Output
Returns `Option[(String, Int)]` — an optional tuple where the first element is a `String` representing the value retrieved from the raster at the specified coordinates, and the second element is an `Int` representing the pixel value at that location. If the point is outside the raster bounds, it returns `None`.

### Valid Call Patterns
```scala
val result: Option[(String, Int)] = value.process("path/to/raster.tif", 34.05, -118.25)
```

### LLM Instruction Prompt
- Ensure that the `filePath` points to a valid GeoTIFF file and that `pointX` and `pointY` are within the raster's bounds.

### Prompt Snippet
```text
Retrieve the raster value at the specified coordinates from the given GeoTIFF file.
```

### Common Failure Modes
- **[compile]** error: not found: value process _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the file path is correct and the coordinates are within the raster bounds before calling process.
```
