## API Test: `area`

### Signature
```scala
def area: Double
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115_

### Goal
Compute the area of a geometry value as a `Double` in Beast/RDPro geospatial workflows.

### Parameters
_None._

### Input
Call `area` on an existing geometry instance (instance method form).  
No file path or format is passed directly to this method.

Preconditions from available facts:
- The call shape is inferred from the signature (`def area: Double`) because no README or test snippet in the provided material shows a direct `area` invocation.
- No CRS/unit semantics are explicitly documented in the provided sources for this method, so unit interpretation is not specified here.

### Output
Returns `Double` — the computed area numeric value for the receiver geometry.

### Valid Call Patterns
```scala
val a: Double = geometry.area
```

### LLM Instruction Prompt
- Use instance-call form: `value.area` (no arguments).
- Ensure the receiver is a geometry object that defines `area`.
- Do not add parameters; signature is exactly `def area: Double`.
- If CRS/units are required by the task, state they are not specified in the provided API facts and must be validated in surrounding pipeline code.

### Prompt Snippet
```text
Given a geometry instance `g`, call `g.area` and store the result as Double.
Do not pass arguments to `area`.
If area units are needed, note that units are not documented in the provided API facts.
```

### Common Failure Modes
- Calling `area()` with arguments or extra options (not supported by signature).
- Calling `area` on a non-geometry receiver.
- Assuming specific units (e.g., square meters) without documented CRS/unit guarantees for this method.

### Fix Code Hint
```scala
// Correct: instance call, no arguments
val areaValue: Double = geometry.area
```