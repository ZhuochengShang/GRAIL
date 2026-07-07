# BlockCartesianRDD

_Compute the intersections of a linear ring with a raster grid, facilitating geospatial analysis in the context of raster processing._

**Receiver:** instance — obtain a `BlockCartesianRDD` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `compute` **(primary)**

---

## API Test: `compute`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def compute(split: Partition, context: TaskContext): Iterator[ITile[T]]
protected def compute(geometries: Array[_<:Geometry], metadata: RasterMetadata): Unit
def compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int): Unit
override def compute(split: Partition, context: TaskContext): Iterator[IFeature]
override def compute(split: Partition, context: TaskContext): Iterator[(EnvelopeNDLite, (Iterator[IFeature], Iterator[IFeature]))]
override def compute(split: Partition, context: TaskContext): Iterator[(Iterator[T], Iterator[U])]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119  (+8 more definition site/overload)_

_Source doc:_ Compute the intersections for the given linear ring @param pID the ID of the polygon @param ring the list of coordinates that make the ring already projected to the raster space @param w the width of the raster in pixels @param h the height of the raster in pixels

### Goal
Compute the intersections of a linear ring with a raster grid, facilitating geospatial analysis in the context of raster processing.

### Parameters
- `pID` (`Int`): The ID of the polygon, which uniquely identifies the polygon in the context of the computation.
- `ring` (`CoordinateSequence`): A sequence of coordinates that define the vertices of the linear ring, already projected to the raster space.
- `w` (`Int`): The width of the raster in pixels, which determines the horizontal resolution of the raster grid.
- `h` (`Int`): The height of the raster in pixels, which determines the vertical resolution of the raster grid.

### Input
The caller must provide a valid polygon ID (`pID`), a `CoordinateSequence` representing the ring's coordinates, and the dimensions of the raster (`w` and `h`). The coordinates in `ring` must be in the same projection as the raster.

### Output
Returns `Unit` — this indicates that the computation is performed without returning a value, and any results are likely stored or processed internally.

### Valid Call Patterns
```scala
intersections.compute(pID, ring, w, h)
```

### LLM Instruction Prompt
- Ensure that the `pID` is a valid integer representing a polygon ID, the `ring` is a properly defined `CoordinateSequence`, and both `w` and `h` are positive integers representing the raster dimensions.

### Prompt Snippet
```text
Call the compute method with a valid polygon ID, a coordinate sequence for the ring, and the raster dimensions.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor PixelsInside: (polygons: Array[_ <: org.locationtech.jts.geom.Geometry], metadata: edu.ucr.cs.bdlab.beast.geolite.RasterMetadata)edu.ucr.cs.bdlab.raptor.Pix _(seen 3x)_
- **[compile]** error: value metadata is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]]

### Fix Code Hint
```scala
// Ensure that pID is a valid integer, ring is a properly defined CoordinateSequence, and w and h are positive integers.
val pID = 1
val ring: CoordinateSequence = // initialize with valid coordinates
val w = 10
val h = 10
intersections.compute(pID, ring, w, h)
```
