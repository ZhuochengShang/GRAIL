## API Test: `pointSample`
_Grounding: doc-repaired from source (docfix)._

### Goal
Sample point coordinates from a distributed spatial RDD in Spark, with an explicit cap (`sampleSize`) and ratio (`sampleRatio`) to keep the collected sample memory-bounded. Returns a 2D array where the first index is the dimension and the second index is the point.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.beast.synopses.PointSampler` — a Scala object; reference as `PointSampler`.

```scala
import edu.ucr.cs.bdlab.beast.synopses.PointSampler

val sampleSize = 1000
val sampleRatio = 1.0 // Increased to 1.0 to maximize chance of sampling from small test RDDs
val seed = 42L

val samples: Array[Array[Double]] =
  PointSampler.pointSample(featuresRDD, sampleSize, sampleRatio, seed)

// MUST check for emptiness before accessing elements
if (samples.isEmpty) {
  println("__CHECK__ pointSample returned empty sample")
} else {
  val dims = samples.length
  val minPoints = samples.map(_.length).min
  println("__CHECK__ pointSample dims=" + dims + ",minPoints=" + minPoints + ",first=" + samples(0)(0))
}
```

### LLM Instruction Prompt
- Use the tested call form: `PointSampler.pointSample(featuresRDD, sampleSize, sampleRatio, seed)`.
- **Crucial:** If the input RDD is empty or no points are sampled, the method returns an empty array (`Array.empty[Array[Double]]`), meaning the outer dimension length will be 0.
- Callers MUST check if the returned array is empty (e.g., `samples.isEmpty`) before accessing its elements to avoid `IndexOutOfBoundsException`.
- For small datasets, a low `sampleRatio` may result in 0 sampled points; use a higher ratio or `1.0` if a sample is strictly required.
- Remember this is an action and returns an in-memory `Array[Array[Double]]`.

### Prompt Snippet
```text
Given a SpatialRDD variable `featuresRDD`, call:
val samples = PointSampler.pointSample(featuresRDD, sampleSize, sampleRatio, seed)

Always check `if (samples.isEmpty)` before accessing `samples(0)` because 0 points sampled returns an empty outer array. Use sampleRatio = 1.0 for small test datasets to guarantee points are sampled.
```

### Common Failure Modes
- **Assuming a populated 2D array is always returned:** Asserting `dims > 0` or accessing `samples(0)(0)` without checking `samples.isEmpty` will crash if the RDD is empty or the `sampleRatio` yields 0 points (the method explicitly returns an empty array in this case).
- **Low sample ratio on small datasets:** Using a small `sampleRatio` (e.g., 0.01) on a tiny test RDD results in 0 points sampled.
- **Assuming lazy evaluation:** This is an **action** and will execute immediately, pulling data into driver memory.

### Fix Code Hint
**WRONG:**
```scala
val samples = PointSampler.pointSample(featuresRDD, 1000, 0.01, 42L)
val dims = samples.length // Might be 0!
val firstVal = samples(0)(0) // Throws IndexOutOfBoundsException if empty
```

**CORRECT:**
```scala
val samples = PointSampler.pointSample(featuresRDD, 1000, 1.0, 42L)
if (samples.isEmpty) {
  println("__CHECK__ pointSample returned empty sample")
} else {
  val dims = samples.length
  val firstVal = samples(0)(0)
}
```