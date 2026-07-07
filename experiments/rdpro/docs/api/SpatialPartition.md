# SpatialPartition

_`numFeatures` retrieves the total count of features (records) present in the current partition of the dataset._

**Receiver:** instance — obtain a `SpatialPartition` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `numFeatures` **(primary)**, ⚠️ `numNonEmptyGeometries`, ⚠️ `numPoints`, ⚠️ `sumSideLength`

---

## API Test: `numFeatures`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def numFeatures: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:32_

_Source doc:_ Total number of features (records) in this partition

### Goal
`numFeatures` retrieves the total count of features (records) present in the current partition of the dataset.

### Parameters
_None._

### Input
The caller must ensure that the dataset has been properly loaded and partitioned. This typically involves using a method such as `GeometricSummary.run(...)` to create a summary object that contains the features.

### Output
Returns `Long` — the total number of features (records) in the current partition.

### Valid Call Patterns
```scala
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
assert(summary.numFeatures == 44)
```

### LLM Instruction Prompt
- Ensure that the dataset has been loaded and processed into a summary object before calling `numFeatures`.

### Prompt Snippet
```text
Retrieve the number of features in the current partition using `numFeatures`.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the dataset is correctly loaded and that the summary object is properly instantiated before calling `numFeatures`.
```

## API Test: `numNonEmptyGeometries`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def numNonEmptyGeometries: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:35_

_Source doc:_ Number of non-empty geometries in this partition

### Goal
`numNonEmptyGeometries` computes the count of non-empty geometries present in the current partition of spatial data.

### Parameters
_None._

### Input
The function operates on a `SpatialPartition` object that must be initialized and populated with geometries. There are no specific file formats required as input since this method is called on an existing object.

### Output
Returns `Long` — the value represents the total number of non-empty geometries in the partition.

### Valid Call Patterns
```scala
val count: Long = spatialPartition.numNonEmptyGeometries
```

### LLM Instruction Prompt
- When calling `numNonEmptyGeometries`, ensure that the `SpatialPartition` object is properly initialized and contains geometries.

### Prompt Snippet
```text
To get the number of non-empty geometries in a spatial partition, use the method `numNonEmptyGeometries` on your `SpatialPartition` instance.
```

### Common Failure Modes
- **[compile]** error: not found: value SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the SpatialPartition is initialized and populated with geometries before calling numNonEmptyGeometries
val spatialPartition = new SpatialPartition(...) // Initialize with appropriate geometries
val count: Long = spatialPartition.numNonEmptyGeometries
```

## API Test: `numPoints`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def numPoints: Int
override def numPoints: Int
def numPoints: Long
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:22  (+4 more definition site/overload)_

### Goal
`numPoints` returns the number of points in a geometric shape, which is essential for understanding the complexity and structure of geometries in geospatial analysis.

### Parameters
_None._

### Input
The caller must provide a geometric shape (e.g., a line string or a linear ring) that has been created using the appropriate geometry factory methods. The geometry must be valid and not null.

### Output
Returns `Int` — the number of points that define the geometric shape. This value represents the count of vertices in the geometry.

### Valid Call Patterns
```scala
val interTile = new IntermediateVectorTile(10, 0)
var line = GeometryReader.DefaultGeometryFactory.createLineString(Array(
  new Coordinate(5, 5), new Coordinate(-5, 5), new Coordinate(-5, 6), new Coordinate(-5, 7),
  new Coordinate(-5, 15), new Coordinate(5, 8)
))
val pointCount = line.numPoints
```

### LLM Instruction Prompt
- Ensure that the geometry is valid and not null before calling `numPoints`. The geometry should be created using the appropriate factory methods.

### Prompt Snippet
```text
To get the number of points in a geometry, ensure the geometry is valid and call `line.numPoints`.
```

### Common Failure Modes
- **[no-correctness-check]** ran without a correctness check: no '__CHECK__' witness printed. End the snippet with require(<result non-degenerate>, ...) then println("__CHECK__ numPoints " + <witness>). _(seen 3x)_
- **[compile]** error: not found: value importorg

### Fix Code Hint
```scala
if (line != null && line.isValid) {
  val pointCount = line.numPoints
} else {
  // Handle the invalid geometry case
}
```

## API Test: `sumSideLength`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def sumSideLength: Array[Double]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:47_

_Source doc:_ The sum of side length along each dimension. Combined with numNonEmptyGeometries, it can be used to compute average side length per dimension.

### Goal
Calculates the total length of the sides of geometries along each dimension, which can be used for further geometric analysis in geospatial raster processing.

### Parameters
_None._

### Input
The caller must ensure that the geometries are properly defined within a `SpatialPartition` context. The method does not require any additional input parameters.

### Output
Returns `Array[Double]` — an array where each element represents the sum of side lengths for each dimension of the geometries contained in the `SpatialPartition`.

### Valid Call Patterns
```scala
val sideLengths: Array[Double] = spatialPartition.sumSideLength
```

### LLM Instruction Prompt
- When calling `sumSideLength`, ensure that it is invoked on an instance of `SpatialPartition` that contains valid geometries.

### Prompt Snippet
```text
To compute the sum of side lengths for the geometries in a spatial partition, use the method `sumSideLength` on the `SpatialPartition` instance.
```

### Common Failure Modes
- **[compile]** error: overloaded method value readInput with alternatives: _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the SpatialPartition is properly initialized and contains valid geometries before calling sumSideLength
val sideLengths: Array[Double] = spatialPartition.sumSideLength
```
