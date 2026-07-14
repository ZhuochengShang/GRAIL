## API Test: `readTile`
_Grounding: doc-repaired from source (docfix)._

### Goal
Read one raster tile by tile ID from an initialized raster reader (e.g., `GeoTiffReader`) for use in pixel access and raster analysis workflows.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.raptor.GeoTiffReader` (Scala class)
- `edu.ucr.cs.bdlab.beast.common.BeastOptions` (Java class)
- `org.apache.hadoop.fs.FileSystem` (Java class)

```scala
import edu.ucr.cs.bdlab.raptor.GeoTiffReader
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import org.apache.hadoop.fs.FileSystem

// Assume fileSystem: FileSystem and rasterPath: String are provided in scope
val reader = new GeoTiffReader[Int]()
reader.initialize(fileSystem, rasterPath, "0", new BeastOptions())
val tileID = reader.metadata.getTileIDAtPixel(0, 0)
val tile = reader.readTile(tileID)
val sampleValue = tile.getPixelValue(0, 0)
reader.close()
```

### LLM Instruction Prompt
- `initialize` on raster readers (like `GeoTiffReader` or `HDF4Reader`) requires exactly four arguments: `(fileSystem: org.apache.hadoop.fs.FileSystem, path: String, layer: String, opts: edu.ucr.cs.bdlab.beast.common.BeastOptions)`.
- Do not attempt to initialize a reader with an RDD; it reads directly from the Hadoop `FileSystem` path.
- Use `GeoTiffReader[T]` (e.g., `GeoTiffReader[Int]`) when reading GeoTIFF files, as `HDF4Reader` will fail at runtime on GeoTIFF inputs.
- Derive `tileID` from the reader's metadata (e.g., `getTileIDAtPixel`) rather than inventing IDs.
- Do not assume the returned tile is valid after `reader.close()`.

### Prompt Snippet
```text
Instantiate a GeoTiffReader[T] (e.g., GeoTiffReader[Int]) and call initialize(fileSystem, path, layer, opts) with exactly 4 arguments. Do not pass an RDD. Compute tileID from reader.metadata.getTileIDAtPixel, call reader.readTile(tileID), access values, and close the reader.
```

### Common Failure Modes
- **Hallucinating `initialize` signature:** Attempting to initialize a reader by passing a `rasterRDD`. The compiler will fail because `initialize` requires exactly four arguments: `(FileSystem, String, String, BeastOptions)`.
- **Using the wrong reader class:** Using `HDF4Reader` for GeoTIFF files, which fails at runtime. Always use `GeoTiffReader[T]` for GeoTIFFs.
- **Assuming tile lifetime after `reader.close()`:** Not guaranteed by the interface; extract needed pixel values before closing.

### Fix Code Hint
**WRONG:** Hallucinating an RDD argument for `initialize`.
```scala
val reader = new GeoTiffReader[Int]()
reader.initialize(rasterRDD) // ERROR: Wrong signature, cannot initialize with RDD
val tile = reader.readTile(0)
```

**CORRECT:** Passing the exact 4 required arguments to read directly from the Hadoop FileSystem.
```scala
val reader = new edu.ucr.cs.bdlab.raptor.GeoTiffReader[Int]()
reader.initialize(fileSystem, rasterPath, "0", new edu.ucr.cs.bdlab.beast.common.BeastOptions())
val tileID = reader.metadata.getTileIDAtPixel(0, 0)
val tile = reader.readTile(tileID)
val sampleValue = tile.getPixelValue(0, 0)
reader.close()
```