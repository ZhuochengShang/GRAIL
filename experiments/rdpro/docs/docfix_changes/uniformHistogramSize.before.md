## API Test: `uniformHistogramSize`

### Signature
```scala
def uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78_

_Source doc:_ Computes a uniform histogram with the given size that calculates the size of the data in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @param sizeFunction  an optional function that computes the size of a feature. @return the created histogram

### Goal
Compute a uniform grid histogram over spatial features where each cell stores accumulated feature **size** (not just count), optionally as a prefix-sum histogram for faster range tests.

### Parameters
- `histogramSize` (`Array[Int]`): the histogram grid shape, i.e., number of partitions (cells) along each dimension.
- `prefixSum` (`Boolean`), default `false`: if `true`, computes prefix sums on the histogram result to speed up range tests.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: function used to compute each feature’s size contribution to histogram cells.

### Input
Call this on a feature collection/RDD receiver that supports `CGOperationsMixin` methods (as shown by `features.uniformHistogramSize(...)` usage).  
The method itself does not take file paths or formats directly; loading data (e.g., shapefile/GeoJSON/CSV-WKT) happens before this call using Beast I/O APIs.

Preconditions from the API facts:
- `histogramSize` must be provided and should match the dimensionality of your data space (number of partitions per dimension).
- `sizeFunction` must be a valid `IFeature => Int`.

### Output
Returns `AbstractHistogram` — a histogram object representing the accumulated **feature size per uniform grid cell**; if `prefixSum = true`, it stores the prefix-summed form for faster range testing.

### Valid Call Patterns
```scala
val countHistogram = features.uniformHistogramCount(Array(100, 100))
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))

val sizeHistogram = features.uniformHistogramSize(Array(100, 100),
    sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson"))
```

### LLM Instruction Prompt
- Use the instance call form exactly as documented: `features.uniformHistogramSize(...)`.
- Pass `histogramSize` as `Array[Int]`.
- Only use supported optional arguments: `prefixSum` and `sizeFunction`.
- Do not invent extra parameters, return types, or alternate call receivers.
- If customizing feature-size logic, provide a function of type `IFeature => Int`.

### Prompt Snippet
```text
Given a feature dataset `features`, compute a size-based uniform histogram using:
`features.uniformHistogramSize(Array(nx, ny), prefixSum = false)`.
Optionally pass `sizeFunction: IFeature => Int` (for example, FeatureWriterSizeFunction with iformat options).
Do not add unsupported arguments.
```

### Common Failure Modes
- Passing a non-`Array[Int]` value for `histogramSize`.
- Using an invalid `sizeFunction` type (must be `IFeature => Int`).
- Calling as a standalone function (`uniformHistogramSize(...)`) instead of on the dataset receiver (`features.uniformHistogramSize(...)`), which may not compile in user code.

### Fix Code Hint
```scala
// Correct receiver + argument types
val sizeHistogram: AbstractHistogram =
  features.uniformHistogramSize(Array(100, 100), prefixSum = true)

// Custom size function form from docs
val sizeHistogram2: AbstractHistogram =
  features.uniformHistogramSize(
    Array(100, 100),
    sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson")
  )
```