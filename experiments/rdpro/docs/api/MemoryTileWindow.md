# MemoryTileWindow

_The `getValue` function retrieves the value associated with a specified key from a hashtable stored in a file, returning the value if found or null if not._

**Receiver:** static object — call `MemoryTileWindow.<method>(...)`

**Members** (most robust first): ⚠️ `getValue` **(primary)**

---

## API Test: `getValue`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)
def getValue(fileSystem: FileSystem, path: Path, key: Long): (Long, Int)
def getValue(i: Int, j: Int, position: Int): T
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91  (+2 more definition site/overload)_

_Source doc:_ Return the value that corresponds to the given key or null if the value is not found. @param in the hashtable file @param offset the offset of the hashtable in the file @param key the key to search for @return the value of the key if found, or `null` if the key is not found.

### Goal
The `getValue` function retrieves the value associated with a specified key from a hashtable stored in a file, returning the value if found or null if not.

### Parameters
- `in` (`FSDataInputStream`): The input stream representing the hashtable file from which the value is to be read.
- `offset` (`Long`): The byte offset in the hashtable file where the search for the key begins.
- `key` (`Long`): The key for which the corresponding value is being searched in the hashtable.

### Input
The caller must provide a valid `FSDataInputStream` that points to a hashtable file, a valid byte offset within that file, and a key of type `Long` that exists within the hashtable.

### Output
Returns `(Long, Int)` — a tuple where the first element is the value associated with the key (of type `Long`), and the second element is an integer that may represent additional information about the retrieval (e.g., status or count). If the key is not found, the first element will be null.

### Valid Call Patterns
```scala
// Example of calling getValue with a FSDataInputStream
val (value, status) = histogram.getValue(inputStream, offset, key)
```

### LLM Instruction Prompt
- Ensure that the `FSDataInputStream` is properly initialized and points to a valid hashtable file.
- Confirm that the offset is within the bounds of the file size.
- Use a valid key that is expected to be present in the hashtable.

### Prompt Snippet
```text
Retrieve the value associated with a specific key from a hashtable file using getValue.
```

### Common Failure Modes
- **[compile]** error: not found: value getValue _(seen 3x)_
- **[compile]** error: not found: value histogram

### Fix Code Hint
```scala
// Ensure the FSDataInputStream is correctly initialized and the offset is valid
if (inputStream != null && offset >= 0) {
  val (value, status) = histogram.getValue(inputStream, offset, key)
  if (value == null) {
    println("Key not found.")
  } else {
    println(s"Value found: $value with status: $status")
  }
} else {
  println("Invalid input stream or offset.")
}
```
