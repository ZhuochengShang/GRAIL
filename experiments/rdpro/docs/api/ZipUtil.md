# ZipUtil

_`putStoredFile` adds a file to a ZIP archive without compression, allowing for efficient storage of binary data._

**Receiver:** static object — call `ZipUtil.<method>(...)`

**Members** (most robust first): ★ `putStoredFile` **(primary)**, ⚠️ `lastNFiles`, ⚠️ `listFilesInZip`, ⚠️ `mergeZip`

---

## API Test: `putStoredFile`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def putStoredFile(zip: ZipOutputStream, filename: String, data: Array[Byte]): Unit
def putStoredFile(zip: org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream, filename: String, data: Array[Byte]): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:584  (+1 more definition site/overload)_

_Source doc:_ Add a file to the given ZIP file using [[ZipEntry.STORED]] method, i.e., no compression. @param zip the ZIP file to write the entry to @param filename the name of the entry in the ZIP file @param data the binary data of the file

### Goal
`putStoredFile` adds a file to a ZIP archive without compression, allowing for efficient storage of binary data.

### Parameters
- `zip` (`ZipOutputStream`): The output stream representing the ZIP file to which the entry will be added. This stream must be open and ready for writing.
- `filename` (`String`): The name of the file entry within the ZIP archive. This should be a valid file name and can include directory paths.
- `data` (`Array[Byte]`): The binary data to be stored in the ZIP file. This array must contain the actual content that you want to save.

### Input
The caller must provide:
- A valid `ZipOutputStream` that is open for writing.
- A `String` representing the desired filename within the ZIP archive.
- An `Array[Byte]` containing the binary data to be stored. The data should not be null and should represent the content intended for the file.

### Output
Returns `Unit` — this indicates that the operation has completed successfully without returning any value. There is no output format as it directly modifies the ZIP file.

### Valid Call Patterns
```scala
val file1 = new File(scratchDir, "test1.zip")
val zip1 = new ZipOutputStream(new FileOutputStream(file1))
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1, 2, 3, 4, 5, 6))
ZipUtil.putStoredFile(zip1, "data.bin", Array[Byte](1, 2, 3))
zip1.close()
```

### LLM Instruction Prompt
- Ensure that the `zip` parameter is a valid and open `ZipOutputStream`.
- The `filename` should be a valid string representing the file name within the ZIP.
- The `data` must be a non-null `Array[Byte]` containing the binary content to be stored.

### Prompt Snippet
```text
Add a file to the ZIP archive using `putStoredFile(zip, filename, data)`, ensuring that `zip` is open and `data` is not null.
```

### Common Failure Modes
- **[compile]** error: overloaded method constructor File with alternatives: _(seen 2x)_

### Fix Code Hint
```scala
// Ensure the ZipOutputStream is open and valid before calling putStoredFile
val zipOutputStream = new ZipOutputStream(new FileOutputStream("output.zip"))
try {
  ZipUtil.putStoredFile(zipOutputStream, "example.txt", Array[Byte](/* your data here */))
} finally {
  zipOutputStream.close()
}
```

## API Test: `lastNFiles`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def lastNFiles(fs: FileSystem, path: Path, n: Int): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:48_

_Source doc:_ Returns information about the last n files in the archive. **Compatibility Note**: This method is not guaranteed to return the correct answer. For efficiency, it tries to locate the directory entries from the end using the ZIP signature. In rare cases, it might retrieve false information since the signature might appear out of coincidence. To be accurate, this method has to read all ZIP entries until it finds the last ones because directory entries are variable size in ZIP. @param fs the file system that contains the ZIP archive @param path the path to the ZIP file @param n the number of entries to retrieve from the end @return file names, offsets, and lengths for the last n entries if the ZIP file contains at least n entries. Otherwise, it returns all entries in the file.

### Goal
The `lastNFiles` function retrieves metadata about the last `n` files stored in a ZIP archive, including their names, offsets, and lengths, which is useful for analyzing the contents of ZIP files in geospatial data processing.

### Parameters
- `fs` (`FileSystem`): The file system that contains the ZIP archive. This can be a local file system or a distributed file system supported by Spark.
- `path` (`Path`): The path to the ZIP file from which the last `n` entries are to be retrieved. This should point to a valid ZIP file.
- `n` (`Int`): The number of entries to retrieve from the end of the ZIP file. This should be a positive integer.

### Input
The caller must provide:
- A valid `FileSystem` instance that can access the ZIP file.
- A `Path` that correctly points to an existing ZIP file.
- An integer `n` that specifies how many of the last entries to retrieve, which must be greater than zero.

### Output
Returns `Array[(String, Long, Long)]` — an array of tuples where each tuple contains:
- The name of the file as a `String`.
- The offset of the file within the ZIP archive as a `Long`.
- The length of the file in bytes as a `Long`.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val zipPath = new Path("path/to/your/archive.zip")
val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, zipPath, 2)
```

### LLM Instruction Prompt
- When calling `lastNFiles`, ensure that the `FileSystem` and `Path` parameters are correctly instantiated and that `n` is a positive integer. Be aware that the method may not always return accurate results due to its reliance on ZIP signatures.

### Prompt Snippet
```text
Retrieve the last 2 files from the specified ZIP archive using the lastNFiles function.
```

### Common Failure Modes
- **[runtime]** java.io.FileNotFoundException: File file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/grail-agent/examples/fixtures/sample.zip does not exist _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the path points to a valid ZIP file and n is a positive integer.
val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, zipPath, 2)
```

## API Test: `listFilesInZip`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def listFilesInZip(fileSystem: fs.FileSystem, zipFilePath: Path): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:478_

_Source doc:_ List all files contained in the given ZIP file @param fileSystem the file system that contains the zip file @param zipFilePath the ZIP file to return its contents @return

### Goal
`listFilesInZip` retrieves a list of all files contained within a specified ZIP file, including their names, offsets, and sizes, facilitating the management of compressed geospatial data.

### Parameters
- `fileSystem` (`fs.FileSystem`): The file system instance that provides access to the ZIP file. This can be a local file system or a distributed file system, depending on the environment in which the Spark job is running.
- `zipFilePath` (`Path`): The path to the ZIP file whose contents are to be listed. This should be a valid path that points to an existing ZIP file in the specified file system.

### Input
The caller must provide:
- A valid `fs.FileSystem` instance that can access the ZIP file.
- A `Path` object pointing to an existing ZIP file. The ZIP file must be accessible and properly formatted.

### Output
Returns `Array[(String, Long, Long)]` — an array of tuples where each tuple contains:
- The name of the file within the ZIP (`String`).
- The offset of the file within the ZIP (`Long`).
- The size of the file in bytes (`Long`).

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val zipFilePath = new Path("path/to/your/file.zip")
val contents = ZipUtil.listFilesInZip(fileSystem, zipFilePath)
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly initialized and points to a valid file system.
- Verify that the `zipFilePath` points to an existing ZIP file before calling `listFilesInZip`.

### Prompt Snippet
```text
List all files in the specified ZIP file using the provided file system.
```

### Common Failure Modes
- **[no-correctness-check]** ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ listFilesInZip " + <witness>). _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the ZIP file exists and the file system is correctly set up before calling the function.
val fileSystem = FileSystem.getLocal(new Configuration())
val zipFilePath = new Path("path/to/your/file.zip")
if (fileSystem.exists(zipFilePath)) {
    val contents = ZipUtil.listFilesInZip(fileSystem, zipFilePath)
} else {
    println("The specified ZIP file does not exist.")
}
```

## API Test: `mergeZip`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def mergeZip(fileSystem: fs.FileSystem, mergedFile: Path, @varargs zipFiles: Path*): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:425_

_Source doc:_ Merges multiple ZIP files into one and deletes the input files. @param mergedFile the output file that contains the merged ZIP files @param zipFiles the input files to be merged

### Goal
Merges multiple ZIP files into a single ZIP file and deletes the original input ZIP files.

### Parameters
- `fileSystem` (`fs.FileSystem`): The file system instance used to access the ZIP files. This can be a local file system or a distributed file system like HDFS.
- `mergedFile` (`Path`): The path where the merged ZIP file will be saved. This should be a valid path in the specified file system.
- `@varargs zipFiles` (`Path*`): A variable number of paths representing the input ZIP files to be merged. Each path should point to a valid ZIP file.

### Input
The caller must provide:
- Valid paths to existing ZIP files that are accessible in the specified file system.
- The `mergedFile` path must not already exist, as it will be created by the function.
- The input ZIP files must be well-formed ZIP archives.

### Output
Returns `Unit` — this indicates that the operation completes without returning a value. The merged ZIP file will be created at the specified `mergedFile` path, and the original input ZIP files will be deleted.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val mergedFile = new Path(scratchPath, "merged.zip")
val zipFile1 = new Path(scratchPath, "file1.zip")
val zipFile2 = new Path(scratchPath, "file2.zip")

ZipUtil.mergeZip(fileSystem, mergedFile, zipFile1, zipFile2)
```

### LLM Instruction Prompt
- Ensure that the `fileSystem` is correctly initialized and points to a valid file system.
- Verify that the `mergedFile` path does not already exist before calling `mergeZip`.
- Confirm that all `zipFiles` paths point to valid and accessible ZIP files.

### Prompt Snippet
```text
Merge multiple ZIP files into a single ZIP file using the mergeZip function. Ensure that the file system is correctly set up and that the input ZIP files are valid.
```

### Common Failure Modes
- **[runtime]** java.io.FileNotFoundException: File file:/Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/experiments/rdpro/exec_out/file1.zip does not exist _(seen 3x)_
- **[runtime]** java.io.IOException: No such file or directory

### Fix Code Hint
```scala
// Ensure the mergedFile does not exist before calling mergeZip
if (!fileSystem.exists(mergedFile)) {
    ZipUtil.mergeZip(fileSystem, mergedFile, zipFile1, zipFile2)
} else {
    println("Merged file already exists. Please choose a different path.")
}
```
