# SpatialFileSource

_Returns the name of the operation or process being executed within the RDPro framework._

**Receiver:** instance — obtain a `SpatialFileSource` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `name` **(primary)**

---

## API Test: `name`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def name(): String
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileSource.scala:93_

### Goal
Returns the name of the operation or process being executed within the RDPro framework.

### Parameters
_None._

### Input
No specific input is required for this function.

### Output
Returns `String` — the name of the operation, which is typically used for logging or identification purposes within the RDPro framework.

### Valid Call Patterns
```scala
val operationName: String = someOperationInstance.name()
```

### LLM Instruction Prompt
- Ensure that the `name` method is called on an instance of an operation or process within the RDPro framework.

### Prompt Snippet
```text
Get the name of the current operation using the name() method.
```

### Common Failure Modes
- **[compile]** error: not found: type SomeOperationClass _(seen 2x)_
- **[compile]** error: class SpatialFileSource is abstract; cannot be instantiated
- **[compile]** error: not found: type SomeConcreteOperationClass

### Fix Code Hint
```scala
if (someOperationInstance != null) {
  val operationName: String = someOperationInstance.name()
} else {
  // Handle the null case appropriately
}
```
