## API Test: `computePointHistogramSparse`

### Signature
```scala
@varargs def computePointHistogramSparse(features: SpatialRDD, sizeFunction: IFeature => Int, mbb: EnvelopeNDLite, numBuckets: Int*): UniformHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/HistogramOP.scala:72_

_Source doc:_ Compute a point histogram for sparse histograms. It maps each record to a bucket and then aggregate by bucket. This method can be helpful for very large histograms to avoid moving the entire histogram during the reduce step. @param features the features to compute their histogram @param sizeFunction the function that evaluates the size of each feature @param mbb the minimum bounding box of the histogram, typically, this is the same as the input MBB @param numBuckets the number of buckets in the histogram @return the computed histogram

### Goal
Compute a sparse point histogram from a `SpatialRDD` by assigning each feature to histogram buckets within an `mbb` and aggregating per-bucket values, which is useful for large histogram sizes in distributed Spark execution.

### Parameters
- `features` (`SpatialRDD`): The spatial features (points in the documented tests) to bin into histogram buckets.
- `sizeFunction` (`IFeature => Int,
                                          mbb: EnvelopeNDLite, numBuckets: Int*`): A function applied to each `IFeature` that returns an `Int` contribution (e.g., `_ => 1` for count-style histograms); `mbb` defines histogram bounds; `numBuckets` specifies bucket counts per dimension (varargs).

### Input
- A Spark `SpatialRDD` of features.
- A valid `EnvelopeNDLite` (`mbb`) defining the histogram extent (typically the dataset MBB, e.g., `points.summary` in tests).
- One or more integer bucket counts through `numBuckets`.
- A per-feature sizing function `IFeature => Int`.
- From tests, points outside `mbb` can be present; the method still computes a histogram for the specified bounds.

### Output
Returns `UniformHistogram` — an in-memory histogram object with uniform bucket partitioning over the provided `mbb`, containing aggregated bucket values computed from `sizeFunction`.

### Valid Call Patterns
```scala
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0))))
val mbr = points.summary
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```

```scala
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 5.0, 5.0)),
))
val mbr = new EnvelopeNDLite(2, 1.0, 1.0, 3.0, 3.0)
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```

### LLM Instruction Prompt
- Use the exact qualified call form from verified tests: `HistogramOP.computePointHistogramSparse(features, sizeFunction, mbb, numBuckets...)`.
- Pass a `SpatialRDD` as `features`.
- Pass a function of type `IFeature => Int` for `sizeFunction` (use `_=>1` for simple counts).
- Provide an `EnvelopeNDLite` for `mbb` (often `features.summary`).
- Provide bucket counts as `Int` varargs (e.g., `4`).
- Do not invent overloads, extra parameters, or different return types.

### Prompt Snippet
```text
Given a SpatialRDD `points`, compute a sparse histogram with:
- size function `_=>1`
- histogram bounds `points.summary` (or a provided EnvelopeNDLite)
- bucket count `4`
Use this exact form:
`val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)`
```

### Common Failure Modes
- Calling an unqualified or wrong receiver form (e.g., bare `computePointHistogramSparse(...)`) when `HistogramOP.computePointHistogramSparse(...)` is required by the shown call pattern.
- Passing a wrong `sizeFunction` type (must be `IFeature => Int`).
- Passing non-`SpatialRDD` input as `features`.
- Using an invalid or mismatched `mbb` object type (must be `EnvelopeNDLite`).
- Omitting bucket arguments in `numBuckets` when histogram partitioning is needed.

### Fix Code Hint
```scala
val mbr: EnvelopeNDLite = points.summary
val h: UniformHistogram =
  HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```