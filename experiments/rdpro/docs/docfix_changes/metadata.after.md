## API Test: `metadata`
_Grounding: doc-repaired from source (docfix)._

### Goal
Access the `RasterMetadata` (dimensions, resolution, CRS, tile layout) of a raster file via a parameterless method on an initialized reader.

### Valid Call Patterns
**Required Types & Imports:**
- `edu.ucr.cs.bdlab.raptor.GeoTiffReader` (Scala class)
- `edu.ucr.cs.bdlab.beast.common.BeastOptions` (Java class)
- `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata` (Scala class)
- `org.apache.hadoop.fs.Path` (Java class)

```scala
import edu.ucr.cs.bdlab.raptor.GeoTiffReader
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import org.apache.hadoop.fs.Path

// Assuming `sc` (SparkContext) and `raster_tif` (String path) are provided
val reader = new GeoTiffReader[Int]()
try {
  val fs = new Path(raster_tif).getFileSystem(sc.hadoopConfiguration)
  reader.initialize(fs, raster_tif, "0", new BeastOptions())
  
  val md: RasterMetadata = reader.metadata
  val witness = (md.rasterWidth, md.rasterHeight, md.numTiles)
  
  require(witness._1 > 0 && witness._2 > 0 && witness._3 > 0, s"degenerate metadata: $witness")
  println("__CHECK__ metadata " + witness)
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- ALWAYS use `GeoTiffReader[T]` for reading GeoTIFF files. Do not use `HDF4Reader` unless explicitly reading HDF files.
- Access `metadata` as a parameterless method (`reader.metadata`) only *after* calling `reader.initialize(...)`.
- Ensure `reader.close()` is called in a `finally` block to prevent resource leaks.

### Prompt Snippet
To read GeoTIFF metadata, initialize `GeoTiffReader[T]` (never `HDF4Reader`), then access the parameterless `reader.metadata` property.

### Common Failure Modes
- **Using `HDF4Reader` for GeoTIFFs:** Attempting to use `HDF4Reader` to read a GeoTIFF file. `HDF4Reader` is strictly for HDF files and requires the `jhdf` library (`edu/ucr/cs/bdlab/jhdf/HDFFile`), which is not on the classpath and will cause a `ClassNotFoundException` or similar failure.
- **Uninitialized Reader:** Calling `metadata` before `reader.initialize(...)` (reader is not ready).
- **Method Signature Error:** Treating `metadata` like a method with parameters (e.g., `reader.metadata()`). It has none.

### Fix Code Hint
```scala
// WRONG: Using HDF4Reader for a GeoTIFF (fails due to missing jhdf dependency) and calling metadata with parens
val reader = new HDF4Reader()
reader.initialize(fs, raster_tif, "0", new BeastOptions())
val md = reader.metadata()

// CORRECT: Using GeoTiffReader for GeoTIFFs and accessing parameterless metadata
val reader = new GeoTiffReader[Int]()
try {
  reader.initialize(fs, raster_tif, "0", new BeastOptions())
  val md = reader.metadata
} finally {
  reader.close()
}
```