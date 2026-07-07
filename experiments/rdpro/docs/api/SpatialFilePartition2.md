# SpatialFilePartition2

_Retrieve the end value of a spatial file partition, which is relevant for managing raster data processing in distributed environments._

**Receiver:** instance — obtain a `SpatialFilePartition2` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `end` **(primary)**

---

## API Test: `end`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def end: Long
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26_

### Goal
Retrieve the end value of a spatial file partition, which is relevant for managing raster data processing in distributed environments.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `Long` — the end value of the spatial file partition, which typically represents the index or position marking the end of the data range in the context of raster processing.

### Valid Call Patterns
```scala
value.end
```

### LLM Instruction Prompt
- Call `end` without any parameters to retrieve the end value of the spatial file partition.

### Prompt Snippet
```text
Retrieve the end value of the spatial file partition using the `end` method.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the object from which `end` is being called is properly initialized before invoking the method.
```
