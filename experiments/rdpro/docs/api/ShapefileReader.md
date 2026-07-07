# ShapefileReader

_The `initialized` function checks whether the file has been successfully initialized for processing within the RDPro framework._

**Receiver:** instance — obtain a `ShapefileReader` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `initialized` **(primary)**

---

## API Test: `initialized`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def initialized: Boolean
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileReader.scala:48_

_Source doc:_ A flag that is raised after the file has been initialized

### Goal
The `initialized` function checks whether the file has been successfully initialized for processing within the RDPro framework.

### Parameters
_None._

### Input
No specific input is required for this function. However, it is assumed that the file must be initialized prior to calling this method.

### Output
Returns `Boolean` — `true` if the file has been initialized successfully, and `false` otherwise.

### Valid Call Patterns
```scala
value.initialized
```

### LLM Instruction Prompt
- Call `initialized` on an instance of the relevant class after ensuring that the file has been initialized.

### Prompt Snippet
```text
Check if the file has been initialized by calling the initialized method.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor ShapefileReader: (conf: org.apache.hadoop.conf.Configuration, file: edu.ucr.cs.bdlab.beast.io.SpatialFilePartition2, filter: org.locationtech.jts.geom.Envel _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the file is properly initialized before calling the initialized method to get an accurate status.
```
