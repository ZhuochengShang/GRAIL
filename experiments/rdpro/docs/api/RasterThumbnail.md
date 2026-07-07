# RasterThumbnail

_`addDependentClasses` registers dependent classes required for processing based on the provided options in the context of geospatial raster analysis._

**Receiver:** static object — call `RasterThumbnail.<method>(...)`

**Members** (most robust first): ★ `addDependentClasses` **(primary)**

---

## API Test: `addDependentClasses`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def addDependentClasses(opts: BeastOptions, classes: util.Stack[Class[_]]): Unit
override def addDependentClasses(opts: BeastOptions, parameterClasses: util.Stack[Class[_]]): Unit
override def addDependentClasses(opts: BeastOptions, classes: java.util.Stack[Class[_]]): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:53  (+5 more definition site/overload)_

### Goal
`addDependentClasses` registers dependent classes required for processing based on the provided options in the context of geospatial raster analysis.

### Parameters
- `opts` (`BeastOptions`): Represents configuration options for the processing task, such as input format specifications (e.g., "wkt").
- `classes` (`util.Stack[Class[_]]`): A stack that holds classes that are dependent on the options provided, which may be used during the processing workflow.

### Input
The caller must provide valid `BeastOptions` that specify the input format and any other necessary configurations. The `classes` stack should be initialized and can be empty before the call.

### Output
Returns `Unit` — this indicates that the method does not return a value but modifies the `classes` stack in place to include the dependent classes based on the provided options.

### Valid Call Patterns
```scala
val input = makeFileCopy("/test_wkt.csv")
val features = new SpatialFileRDD(sparkContext, input.getPath, SpatialFileRDD.InputFormat -> "wkt")
val dependentClasses: util.Stack[Class[_]] = new util.Stack[Class[_]]
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "wkt"
SpatialFileRDD.addDependentClasses(opts, dependentClasses)
```

### LLM Instruction Prompt
- Ensure that the `opts` parameter is correctly configured with valid `BeastOptions` before calling `addDependentClasses`.
- Initialize the `classes` stack before passing it to the method.

### Prompt Snippet
```text
Call `addDependentClasses` with appropriate `BeastOptions` and an initialized stack of dependent classes.
```

### Common Failure Modes
- **[compile]** error: reference to util is ambiguous; _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the classes stack is initialized
val dependentClasses: util.Stack[Class[_]] = new util.Stack[Class[_]]
// Ensure opts is correctly set up with valid options
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "wkt"
```
