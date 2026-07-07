# PointSampler

_The `pointSample` function retrieves a sample of points from a given spatial RDD, ensuring that the sample size does not exceed the specified limit._

**Receiver:** static object — call `PointSampler.<method>(...)`

**Members** (most robust first): ⚠️ `pointSample` **(primary)**

---

## API Test: `pointSample`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def pointSample(features: SpatialRDD, sampleSize: Int, sampleRatio: Double, seed: Long = System.currentTimeMillis()): Array[Array[Double]]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/PointSampler.scala:47_

_Source doc:_ Reads a point sample from the given spatial RDD. It returns a two dimensional array where the first index is the dimension and the second index is the point. This method runs an action on the given RDD. The method takes both a sample size and sample ratio and it returns whichever is smaller. In other words, it tries to read the given sample ratio and if the result is bigger than the sample size, it truncates it to the sample size. This ensures that the final result will fit in memory regardless of the input size. @param features the input features to sample @param sampleSize number of sample points to read @param sampleRatio the ratio of the points to read @return a two-dimensional array of sample points

### Goal
The `pointSample` function retrieves a sample of points from a given spatial RDD, ensuring that the sample size does not exceed the specified limit.

### Parameters
- `features` (`SpatialRDD`): The input features to sample from, which should be a distributed collection of spatial data points.
- `sampleSize` (`Int`): The maximum number of sample points to read from the `features`. This value limits the output size.
- `sampleRatio` (`Double`): The ratio of points to read from the `features`. The function will attempt to sample this ratio of the total points, but will truncate the result to `sampleSize` if necessary.
- `seed` (`Long`), default `System.currentTimeMillis()`: A seed value for random sampling, which ensures reproducibility of the sample selection.

### Input
The caller must provide a `SpatialRDD` containing spatial features, along with an integer for `sampleSize` and a double for `sampleRatio`. The `SpatialRDD` should be properly initialized and contain valid geometries.

### Output
Returns `Array[Array[Double]]` — a two-dimensional array where each inner array represents a sampled point's coordinates. The first index corresponds to the dimension (e.g., x, y), and the second index corresponds to the sampled point.

### Valid Call Patterns
```scala
val factory = GeometryReader.DefaultGeometryFactory
val point = factory.createPoint(new Coordinate(3, 4))
val features: RDD[IFeature] = sparkContext.parallelize(Seq(Feature.create(null, point)), 4)
val sample = PointSampler.pointSample(features, 1, 1.0)
```

### LLM Instruction Prompt
- Ensure that the `features` parameter is a valid `SpatialRDD` and that the `sampleSize` and `sampleRatio` are appropriate for the dataset being sampled.

### Prompt Snippet
```text
Retrieve a sample of points from the provided spatial RDD using the pointSample function.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the SpatialRDD is not empty and sampleSize is greater than zero
val sample = PointSampler.pointSample(features, 10, 0.5)
```
