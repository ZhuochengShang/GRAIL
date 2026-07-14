## API Test: `pointSample`

### Signature
```scala
def pointSample(features: SpatialRDD, sampleSize: Int, sampleRatio: Double, seed: Long = System.currentTimeMillis()): Array[Array[Double]]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/PointSampler.scala:47_

_Source doc:_ Reads a point sample from the given spatial RDD. It returns a two dimensional array where the first index is the dimension and the second index is the point. This method runs an action on the given RDD. The method takes both a sample size and sample ratio and it returns whichever is smaller. In other words, it tries to read the given sample ratio and if the result is bigger than the sample size, it truncates it to the sample size. This ensures that the final result will fit in memory regardless of the input size. @param features the input features to sample @param sampleSize number of sample points to read @param sampleRatio the ratio of the points to read @return a two-dimensional array of sample points

### Goal
Sample point coordinates from a distributed spatial RDD in Spark, with an explicit cap (`sampleSize`) and ratio (`sampleRatio`) to keep the collected sample memory-bounded.

### Parameters
- `features` (`SpatialRDD`): the input spatial RDD to sample from (point features are the intended input per method purpose and tests).
- `sampleSize` (`Int`): maximum number of sample points to return.
- `sampleRatio` (`Double`): fraction of input points to try sampling before truncation by `sampleSize`.
- `seed` (`Long`), default `System.currentTimeMillis()`: random seed used for sampling reproducibility.

### Input
`pointSample` operates on a Spark `SpatialRDD` already loaded/prepared by your pipeline (no file path is passed directly to this method).  
Preconditions from the provided docs/tests:

- This is an **action** on the RDD (it triggers execution).
- Intended for sampling **points** from spatial features.
- The method uses both `sampleRatio` and `sampleSize`, and returns the smaller effective result.
- Tests show it handles:
  - empty partitions, and
  - rows with null geometries
  without failing.

No additional format/CRS/type-precondition is documented for this specific API.

### Output
Returns `Array[Array[Double]]` — a 2D numeric array of sampled point coordinates where:

- first index = **dimension**
- second index = **point**

So for 2D points, the outer length is expected to be 2 (as validated in tests), and each inner array contains sampled values for that dimension across sampled points.

### Valid Call Patterns
```scala
val sample = PointSampler.pointSample(features, 1, 1.0)
```

```scala
val sample = PointSampler.pointSample(features, 1, 1.0, 12345L)
```

### LLM Instruction Prompt
- Use the tested call form with explicit qualifier: `PointSampler.pointSample(features, sampleSize, sampleRatio[, seed])`.
- Pass an existing `SpatialRDD` variable; do not invent file paths in this call.
- Remember this is an action and returns an in-memory `Array[Array[Double]]`.
- Respect the size/ratio semantics: effective sample count is bounded by the smaller of ratio-based sample and `sampleSize`.
- If deterministic results are needed, provide `seed` explicitly.

### Prompt Snippet
```text
Given a SpatialRDD variable `features`, call:
PointSampler.pointSample(features, sampleSize, sampleRatio, seed)

Use this when you need an in-memory point sample for downstream stats/indexing.
Keep sampleSize conservative to fit driver memory.
```

### Common Failure Modes
- Assuming it is a lazy transformation; it is an **action** and will execute immediately.
- Setting very large `sampleSize` and expecting no driver-memory impact (result is collected as arrays).
- Expecting sampled count to always equal `sampleRatio * N`; method truncates to `sampleSize` when needed.
- Calling with non-reproducible behavior unintentionally (default seed is current time).

### Fix Code Hint
```scala
// Reproducible, bounded sample
val sampleSize = 10000
val sampleRatio = 0.01
val seed = 42L
val sample: Array[Array[Double]] =
  PointSampler.pointSample(features, sampleSize, sampleRatio, seed)
```