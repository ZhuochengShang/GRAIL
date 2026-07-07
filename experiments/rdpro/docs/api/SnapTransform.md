# SnapTransform

_The `transform` function applies a geometric transformation to a set of source points, converting their coordinates to a destination coordinate system._

**Receiver:** instance — obtain a `SnapTransform` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `transform` **(primary)**

---

## API Test: `transform`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def transform(ptSrc: DirectPosition, ptDst: DirectPosition): DirectPosition
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SnapTransform.scala:46  (+4 more definition site/overload)_

### Goal
The `transform` function applies a geometric transformation to a set of source points, converting their coordinates to a destination coordinate system.

### Parameters
- `srcPts` (`Array[Double]`): An array of source point coordinates that need to be transformed. The values represent the coordinates in the source coordinate reference system.
- `srcOff` (`Int`): The starting index in the `srcPts` array from which to read the source point coordinates.
- `dstPts` (`Array[Double]`): An array where the transformed destination point coordinates will be stored. The values will represent the coordinates in the destination coordinate reference system.
- `dstOff` (`Int`): The starting index in the `dstPts` array where the transformed coordinates will be written.
- `numPts` (`Int`): The number of points to transform, indicating how many sets of coordinates will be processed from the source array.

### Input
The caller must provide an array of source point coordinates (`srcPts`) in a compatible format, along with the appropriate offsets and the number of points to transform. The source points should be in a format that matches the expected coordinate system for transformation.

### Output
Returns `Unit` — this indicates that the transformation is performed in-place, modifying the `dstPts` array directly without returning a value.

### Valid Call Patterns
```scala
val pointArray: Array[Double] = Array(0.0, 0.0, 1.0, 1.0)
val transformedPoints: Array[Double] = new Array[Double](4)
val srcOffset: Int = 0
val dstOffset: Int = 0
val numberOfPoints: Int = 2

transform(pointArray, srcOffset, transformedPoints, dstOffset, numberOfPoints)
```

### LLM Instruction Prompt
- Ensure that the source points are provided in the correct format and that the offsets and number of points are correctly specified to avoid index errors.

### Prompt Snippet
```text
Transform the coordinates of the source points using the `transform` function, ensuring that the input arrays and offsets are correctly set.
```

### Common Failure Modes
- **[compile]** error: not found: value transform _(seen 3x)_
- **[compile]** error: not enough arguments for constructor SnapTransform: (bounds: org.locationtech.jts.geom.Envelope)edu.ucr.cs.bdlab.beast.cg.SnapTransform.

### Fix Code Hint
```scala
// Ensure that the number of points specified does not exceed the length of the source and destination arrays.
if (srcPts.length < srcOff + numPts || dstPts.length < dstOff + numPts) {
  throw new IllegalArgumentException("Number of points exceeds array bounds.")
}
```
