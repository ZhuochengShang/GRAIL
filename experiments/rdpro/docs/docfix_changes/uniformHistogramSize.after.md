## API Test: `uniformHistogramSize`
_Grounding: doc-repaired from source (docfix)._

### Goal
Compute a uniform grid histogram over spatial features where each cell stores accumulated feature size (not just count), optionally as a prefix-sum histogram for faster range tests.

### Valid Call Patterns
```scala
// No additional imports required beyond the standard Beast implicit context.

// 1. Compute the histogram
val sizeHistogram = featuresRDD.uniformHistogramSize(Array(64, 64), prefixSum = true)

// 2. Query the histogram
// AbstractHistogram.getValue requires TWO Array[Int] arguments (min and max bin indices)
val hValue: Long = sizeHistogram.getValue(Array(0, 0), Array(0, 0))
require(hValue >= 0, s"degenerate histogram cell value: $hValue")
```

### LLM Instruction Prompt
- Call `featuresRDD.uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean)`.
- To query the resulting `AbstractHistogram`, `getValue` requires exactly two `Array[Int]` arguments representing the minimum and maximum bin indices for the multidimensional range (e.g., `getValue(Array(0, 0), Array(0, 0))`).
- Never call `getValue` with a single array.
- `getValue` returns a `Long`.

### Prompt Snippet
```text
Compute a size-based uniform histogram using `featuresRDD.uniformHistogramSize(Array(nx, ny), prefixSum = true)`.
Query the resulting `AbstractHistogram` using `getValue(Array(minX, minY), Array(maxX, maxY))`. Remember that `getValue` requires exactly two `Array[Int]` arguments for the range and returns a `Long`.
```

### Common Failure Modes
- **Signature mismatch on `getValue`:** Assuming `AbstractHistogram.getValue` takes a single `Array[Int]` argument to query a single bin. It strictly requires two `Array[Int]` arguments (min and max bin indices) to define a multidimensional range.
- Passing a non-`Array[Int]` value for `histogramSize`.
- Calling as a standalone function instead of on the dataset receiver (`featuresRDD.uniformHistogramSize(...)`).

### Fix Code Hint
```scala
// WRONG: Calling getValue with a single array
val sizeHistogram = featuresRDD.uniformHistogramSize(Array(64, 64), prefixSum = true)
val hValue = sizeHistogram.getValue(Array(0, 0)) // Fails to compile: requires two arguments

// CORRECT: Calling getValue with two arrays (min and max bin indices)
val sizeHistogram = featuresRDD.uniformHistogramSize(Array(64, 64), prefixSum = true)
val hValue: Long = sizeHistogram.getValue(Array(0, 0), Array(0, 0))
```