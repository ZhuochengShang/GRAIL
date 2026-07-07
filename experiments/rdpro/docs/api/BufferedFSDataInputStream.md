# BufferedFSDataInputStream

_The `seek` function is used to move the file pointer to a specified position within a data stream, allowing for random access to the data._

**Receiver:** instance — obtain a `BufferedFSDataInputStream` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `seek` **(primary)**

---

## API Test: `seek`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def seek(pos: Long): Unit
private def seek(pos: Long, newSource: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:37  (+1 more definition site/overload)_

### Goal
The `seek` function is used to move the file pointer to a specified position within a data stream, allowing for random access to the data.

### Parameters
- `pos` (`Long`): The position in the data stream to which the file pointer should be moved. This value must be non-negative and within the bounds of the data stream length.
- `newSource` (`Boolean`): A flag indicating whether to treat the position as a new source. If `true`, the function may reset the stream or change its state; if `false`, it continues from the current stream state.

### Input
The caller must provide a valid data stream that supports seeking. The stream must be open and accessible, and the `pos` value must be within the valid range of the stream's length.

### Output
Returns `Boolean` — `true` if the seek operation was successful and the file pointer was moved to the specified position; `false` otherwise.

### Valid Call Patterns
```scala
value.seek(100L, true)
```

### LLM Instruction Prompt
- Ensure that the `pos` parameter is within the valid range of the data stream length before calling `seek`. The `newSource` parameter should be set based on whether you want to treat the position as a new source.

### Prompt Snippet
```text
To seek to a specific position in the data stream, use the `seek` method with the desired position and a flag indicating if it's a new source.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor BufferedFSDataInputStream: (in: org.apache.hadoop.fs.FSDataInputStream, bufferSize: Int)edu.ucr.cs.bdlab.beast.util.BufferedFSDataInputStream. _(seen 4x)_

### Fix Code Hint
```scala
if (pos < 0 || pos >= dataStreamLength) {
  throw new IllegalArgumentException("Position must be within the bounds of the data stream.");
}
```
