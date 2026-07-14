## API Test: `listFilesInZip`
_Grounding: doc-repaired from source (docfix)._

### Goal
List all file entries inside a ZIP archive returning `Array[(String, Long, Long)]` (name, offset, length). Initial logic and parameters are validated; standard processing applied.

### Valid Call Patterns
Requires `org.apache.hadoop.fs.Path` (Java), `org.apache.hadoop.fs.FileSystem` (Java), and `edu.ucr.cs.bdlab.beast.util.ZipUtil` (Scala).

```scala
import org.apache.hadoop.fs.{Path, FileSystem}
import edu.ucr.cs.bdlab.beast.util.ZipUtil

val zipPath = new Path(vector_zip)
val fileSystem = zipPath.getFileSystem(sc.hadoopConfiguration)
val entries: Array[(String, Long, Long)] = ZipUtil.listFilesInZip(fileSystem, zipPath)

val n = entries.length
val totalBytes = entries.map(_._3).sum
require(n > 0, s"empty result for listFilesInZip at $zipPath")
require(totalBytes > 0L, s"degenerate zip entries (totalBytes=$totalBytes) at $zipPath")

println("__CHECK__ listFilesInZip " + s"count=$n,totalBytes=$totalBytes,first=${entries.head._1}:${entries.head._2}:${entries.head._3}")
```

### LLM Instruction Prompt
- The input file must be a valid ZIP archive. In test harnesses, explicitly use the provided `vector_zip` variable.
- Do not pass a raster or uncompressed file like `raster_tif`.
- Instantiate Hadoop `Path` and resolve `FileSystem` directly from it using `sc.hadoopConfiguration`.

### Prompt Snippet
```text
Use ZipUtil.listFilesInZip(fileSystem, zipFilePath) to enumerate ZIP contents.
Input MUST be a ZIP archive (vector_zip), never a TIFF (raster_tif).
Requires org.apache.hadoop.fs.{Path, FileSystem} and edu.ucr.cs.bdlab.beast.util.ZipUtil.
```

### Common Failure Modes
- **Passing a non-ZIP file (e.g., `raster_tif`):** Will result in an `IllegalArgumentException: Could not find central directory offset in the zip file.` Ensure you are passing `vector_zip` instead of a raster file, as rasters lack the required ZIP central directory signature.

### Fix Code Hint
```scala
// WRONG: Passing a GeoTIFF/raster to a ZIP utility
val badPath = new Path(raster_tif)
val fs = badPath.getFileSystem(sc.hadoopConfiguration)
ZipUtil.listFilesInZip(fs, badPath) // Throws IllegalArgumentException

// CORRECT: Passing a valid ZIP archive
val zipPath = new Path(vector_zip)
val fileSystem = zipPath.getFileSystem(sc.hadoopConfiguration)
val entries: Array[(String, Long, Long)] = ZipUtil.listFilesInZip(fileSystem, zipPath)
```