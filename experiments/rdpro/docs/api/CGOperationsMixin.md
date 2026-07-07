# CGOperationsMixin

_The `eulerHistogramCount` function computes an Euler histogram that efficiently counts the number of records in each cell for geometries with extents,…_

**Receiver:** instance — obtain a `CGOperationsMixin` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `eulerHistogramCount` **(primary)**, ⚠️ `eulerHistogramSize`, ⚠️ `uniformHistogramCount`, ⚠️ `uniformHistogramSize`

---

## API Test: `eulerHistogramCount`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def eulerHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the number of records in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `eulerHistogramCount` function computes an Euler histogram that efficiently counts the number of records in each cell for geometries with extents, facilitating spatial analysis in geospatial raster processing.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the size of the histogram, representing the number of partitions along each dimension. For example, `Array(100, 100)` would create a histogram with 100 partitions in both the x and y dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the result. Setting this to `true` can speed up range tests on the histogram.

### Input
The caller must provide a valid `Array[Int]` for `histogramSize`, which defines the dimensions of the histogram. The input geometries should be compatible with the histogram computation, typically requiring that the geometries have extents (envelopes) defined.

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which contains the counts of records in each cell based on the specified histogram size.

### Valid Call Patterns
```scala
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))
```

### LLM Instruction Prompt
- When calling `eulerHistogramCount`, ensure that the `histogramSize` parameter is an array of integers representing the desired number of partitions along each dimension, and optionally set `prefixSum` to `true` if prefix sums are needed for performance optimization.

### Prompt Snippet
```text
To compute an Euler histogram for the given geometries, use the `eulerHistogramCount` method with the appropriate histogram size and prefix sum option.
```

### Common Failure Modes
- **[compile]** error: value count is not a member of edu.ucr.cs.bdlab.beast.synopses.AbstractHistogram _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the histogramSize is a non-empty array of integers
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))
```

## API Test: `eulerHistogramSize`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def eulerHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the total size of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `eulerHistogramSize` function computes an Euler histogram that efficiently calculates the total size of geometrical features within specified partitions, aiding in geospatial analysis.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the number of partitions along each dimension for the histogram. For example, `Array(100, 100)` creates a histogram with 100 partitions in both the x and y dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the resulting histogram. Setting this to `true` can speed up subsequent range queries.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A function that determines how to calculate the size of each feature. The default implementation retrieves the storage size of the feature.

### Input
The caller must provide a valid `Array[Int]` for `histogramSize`, which defines the partitioning of the histogram. The input geometries must be compatible with the histogram calculation, typically requiring that they have extents (envelopes) defined.

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which contains the size of features aggregated into the specified partitions.

### Valid Call Patterns
```scala
val eulerSizeHistogram = polygons.eulerHistogramSize(Array(100, 100))
```

### LLM Instruction Prompt
- When calling `eulerHistogramSize`, ensure that the `histogramSize` parameter is a valid array of integers representing the desired partition sizes. The `prefixSum` and `sizeFunction` parameters are optional and can be adjusted based on the specific needs of the analysis.

### Prompt Snippet
```text
To compute an Euler histogram for geometries, use the `eulerHistogramSize` method with appropriate partition sizes, like so: `polygons.eulerHistogramSize(Array(100, 100))`.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 2x)_
- **[compile]** error: value getTotalCount is not a member of edu.ucr.cs.bdlab.beast.synopses.AbstractHistogram
- **[compile]** error: value getTotalSize is not a member of edu.ucr.cs.bdlab.beast.synopses.AbstractHistogram

### Fix Code Hint
```scala
// Ensure that the histogramSize is a non-empty array of integers
val validHistogramSize = Array(100, 100)
val eulerSizeHistogram = polygons.eulerHistogramSize(validHistogramSize)
```

## API Test: `uniformHistogramCount`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def uniformHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:67_

_Source doc:_ Computes a uniform histogram with the given size that counts number of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
The `uniformHistogramCount` function computes a uniform histogram that counts the number of features in each cell, facilitating efficient range queries in geospatial raster analysis.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the size of the histogram, representing the number of partitions along each dimension. For example, `Array(100, 100)` creates a histogram with 100 partitions in both dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the resulting histogram. Setting this to `true` can speed up range tests.

### Input
The caller must provide a valid `Array[Int]` for `histogramSize`, which defines the dimensions of the histogram. The input must be compatible with the expected dimensions for the features being processed.

### Output
Returns `AbstractHistogram` — an object representing the created histogram, which can be used for further analysis and querying of feature counts within the specified partitions.

### Valid Call Patterns
```scala
val countHistogram = features.uniformHistogramCount(Array(100, 100))
val histogram = polygons.uniformHistogramCount(Array(100, 100), prefixSum = true)
```

### LLM Instruction Prompt
- When calling `uniformHistogramCount`, ensure that the `histogramSize` parameter is an array of integers representing the desired histogram dimensions, and optionally specify `prefixSum` to optimize range queries.

### Prompt Snippet
```text
Call `uniformHistogramCount` with an array of integers for `histogramSize` to define the histogram dimensions, and set `prefixSum` to `true` if prefix sums are needed for faster range tests.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 3x)_
- **[compile]** error: not found: value spark

### Fix Code Hint
```scala
// Ensure histogramSize is a non-empty array of integers
val validHistogramSize = Array(100, 100)
val histogram = features.uniformHistogramCount(validHistogramSize, prefixSum = true)
```

## API Test: `uniformHistogramSize`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78_

_Source doc:_ Computes a uniform histogram with the given size that calculates the size of the data in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @param sizeFunction  an optional function that computes the size of a feature. @return the created histogram

### Goal
`uniformHistogramSize` computes a uniform histogram that partitions data into specified sizes, facilitating efficient data analysis in geospatial raster processing.

### Parameters
- `histogramSize` (`Array[Int]`): An array specifying the number of partitions along each dimension of the histogram. For example, `Array(100, 100)` creates a histogram with 100 partitions in both dimensions.
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute the prefix sum on the histogram result to optimize range queries. Setting this to `true` can speed up subsequent range tests.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A function that computes the size of a feature. The default function retrieves the storage size of the feature, but a custom function can be provided to calculate size differently.

### Input
The caller must provide:
- An `Array[Int]` for `histogramSize` that defines the dimensions of the histogram.
- Optionally, a `Boolean` for `prefixSum` and a custom `sizeFunction` if different behavior is desired.

### Output
Returns `AbstractHistogram` — an object representing the computed histogram, which can be used for further analysis or visualization of the data distribution across the specified partitions.

### Valid Call Patterns
```scala
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))
val sizeHistogramWithPrefix = features.uniformHistogramSize(Array(100, 100), prefixSum = true)
val customSizeHistogram = features.uniformHistogramSize(Array(100, 100), sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson"))
```

### LLM Instruction Prompt
- When calling `uniformHistogramSize`, ensure that the `histogramSize` parameter is an array of integers representing the desired number of partitions. Optionally, specify `prefixSum` to optimize range queries and provide a custom `sizeFunction` if needed.

### Prompt Snippet
```text
Call `uniformHistogramSize` with an array defining the histogram size, and optionally set `prefixSum` to true for optimized range queries.
```

### Common Failure Modes
- **[compile]** error: value geojson is not a member of org.apache.spark.SparkContext _(seen 3x)_
- **[compile]** error: value getSize is not a member of edu.ucr.cs.bdlab.beast.synopses.AbstractHistogram

### Fix Code Hint
```scala
// Ensure histogramSize is a non-empty array of positive integers
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))
```
