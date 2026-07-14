## API Test: `end`

### Signature
```scala
def end: Long
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26_

### Goal
Return the partition’s end position as a `Long` value (inferred from the signature; no RDPro README/test usage is provided for this method).

### Parameters
_None._

### Input
`end` takes no arguments and is called on an existing object instance that defines this method (likely a spatial file partition object, based on source path/class name).  
No file format input is passed directly to this call.

Preconditions from available docs for raster/vector compatibility (CRS/resolution/tile-size alignment, typed `geoTiff[T]` loading, etc.) are **not specifically documented for this method**.

### Output
Returns `Long` — a numeric end value from the receiver object, represented as a Scala `Long`.

### Valid Call Patterns
```scala
value.end
```
(Inferred from the signature `def end: Long`; no verified test-suite or README call example exists for this API.)

### LLM Instruction Prompt
- Call it as a parameterless member access on an instance (`value.end`), not as a standalone function.
- Do not add arguments.
- Do not assume units/semantics beyond “end value” unless additional type/context is available in user code.

### Prompt Snippet
```text
Given an instance `value` that has method `def end: Long`, read its end position using `value.end` and store/print the returned Long.
```

### Common Failure Modes
- Calling `end` without a receiver in scope (e.g., `end`) when no such symbol exists.
- Calling `end` on a type that does not define this method.
- Assuming undocumented semantics (e.g., byte offset vs index vs inclusive/exclusive boundary) without checking surrounding API/type docs.

### Fix Code Hint
```scala
// Ensure you have an instance that defines `def end: Long`
val e: Long = value.end
println(e)
```