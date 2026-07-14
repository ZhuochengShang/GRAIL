## API Test: `listFilesInZip`

### Signature
```scala
def listFilesInZip(fileSystem: fs.FileSystem, zipFilePath: Path): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:478_

_Source doc:_ List all files contained in the given ZIP file @param fileSystem the file system that contains the zip file @param zipFilePath the ZIP file to return its contents @return

### Goal
List all file entries inside a ZIP archive (including ZIP64 archives) and return each entry’s name plus byte location/size metadata for random-access reading.

### Parameters
- `fileSystem` (`fs.FileSystem`): Hadoop-compatible file system instance that can open/read the ZIP file (for example, local FS from `FileSystem.getLocal(new Configuration())`).
- `zipFilePath` (`Path`): Path to the ZIP file whose internal file entries should be listed.

### Input
A valid ZIP file reachable through the provided `fileSystem` at `zipFilePath`.  
From tests, this works for regular ZIP and ZIP64.  
Preconditions:
- `fileSystem` and `zipFilePath` must refer to the same storage backend/context.
- The path must exist and be readable.
- The file must be a ZIP archive parseable by RDPro/Beast ZIP utilities.

### Output
Returns `Array[(String, Long, Long)]` where each tuple represents one ZIP entry:
1. `String`: entry/file name inside the ZIP (e.g., `"README.bin"`),
2. `Long`: byte offset usable with `FSDataInputStream.seek(...)` on the ZIP file,
3. `Long`: entry byte length.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val contents = ZipUtil.listFilesInZip(fileSystem, new Path(file1.getPath))
```

```scala
val files = ZipUtil.listFilesInZip(fileSystem, file1)
```

### LLM Instruction Prompt
- Use the exact static call form `ZipUtil.listFilesInZip(fileSystem, zipFilePath)`.
- Pass a Hadoop `fs.FileSystem` and a Hadoop `Path`; do not pass plain strings directly.
- Ensure the ZIP path is accessible by that exact filesystem instance.
- Treat returned tuples as `(entryName, offset, length)`.

### Prompt Snippet
```text
Use ZipUtil.listFilesInZip(fileSystem, zipFilePath) to enumerate ZIP contents.
`fileSystem` must be an fs.FileSystem that can open `zipFilePath` (Path).
Interpret each returned tuple as (name, byteOffset, byteLength).
```

### Common Failure Modes
- Passing a path that does not exist or is unreadable on the provided filesystem.
- Filesystem/path mismatch (e.g., local `FileSystem` with a non-local path context).
- Assuming the return type is only names; it also includes offset and size.
- Passing a non-ZIP file and expecting valid ZIP entry metadata.

### Fix Code Hint
```scala
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import edu.ucr.cs.bdlab.beast.util.ZipUtil

val fileSystem = FileSystem.getLocal(new Configuration())
val zipPath = new Path("/path/to/archive.zip") // must exist on this fileSystem
val entries: Array[(String, Long, Long)] = ZipUtil.listFilesInZip(fileSystem, zipPath)

// Example: random-access read of first entry bytes
val in = fileSystem.open(zipPath)
in.seek(entries(0)._2)
val data = new Array[Byte](entries(0)._3.toInt)
in.readFully(data)
in.close()
```