# GeometricSummary

_Calculates the estimated output size for a given set of spatial features based on specified options._

**Receiver:** static object — call `GeometricSummary.<method>(...)`

**Members** (most robust first): ⚠️ `computeForFeaturesWithOutputSize` **(primary)**

---

## API Test: `computeForFeaturesWithOutputSize`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def computeForFeaturesWithOutputSize(features: JavaSpatialRDD, opts: BeastOptions) : Summary
def computeForFeaturesWithOutputSize(features : SpatialRDD, opts : BeastOptions) : Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GeometricSummary.scala:49  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
Calculates the estimated output size for a given set of spatial features based on specified options.

### Parameters
- `features` (`JavaSpatialRDD`): A distributed collection of spatial features that will be analyzed to compute the output size. This should contain geometries and associated attributes relevant to the analysis.
- `opts` (`BeastOptions`): A set of options that influence the computation, such as output format specifications (e.g., "iformat" -> "geojson").

### Input
The caller must provide a `JavaSpatialRDD` containing spatial features and a `BeastOptions` object with relevant options. Ensure that the `features` RDD is properly populated with valid geometries and attributes before calling this function.

### Output
Returns `Summary` — an object that encapsulates the estimated output size and other relevant statistics about the computation based on the provided features and options.

### Valid Call Patterns
```scala
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `JavaSpatialRDD` containing spatial data, and that `opts` is a properly configured `BeastOptions` object.

### Prompt Snippet
```text
Compute the estimated output size for the given spatial features with specified options.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure features are populated and opts are correctly set before calling the function
val features: JavaSpatialRDD = // load or create your spatial RDD
val opts: BeastOptions = // configure your options
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
```
