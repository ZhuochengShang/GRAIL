## API Test: `isCW`
_Grounding: doc-repaired from source (docfix)._

### Goal
Determines if a simple, closed ring of points is ordered clockwise. Returns `false` if the ring is not closed.

### Valid Call Patterns|Valid Access Patterns
The `isCW` method is called on an instance of a simple geometry class representing a single ring, such as `LiteList`.

```scala
// Requires the LiteList class, defined in Scala.
import edu.ucr.cs.bdlab.davinci.LiteList

// A clockwise ring: (0,0) -> (0,1) -> (1,1) -> (1,0) -> (0,0)
// Coordinates MUST be separate X and Y arrays of type Short.
val xs = Array[Short](0, 0, 1, 1, 0)
val ys = Array[Short](0, 1, 1, 0, 0)

// Construct the geometry object from the coordinate arrays.
val ring = new LiteList(xs, ys)

// Call the method on the instance.
val isClockwise: Boolean = ring.isCW
// isClockwise will be true
```

### LLM Instruction Prompt
- To check if a ring is clockwise, first construct an `edu.ucr.cs.bdlab.davinci.LiteList` object.
- The `LiteList` constructor requires two separate arguments: an `Array[Short]` of x-coordinates and an `Array[Short]` of y-coordinates.
- The ring must be closed (first coordinate equals the last) to be considered clockwise.
- Call the `isCW` method on the resulting `LiteList` instance.

### Prompt Snippet
```text
Given separate x and y coordinate arrays of type Short representing a closed ring, check if the ring is in clockwise order using the isCW method.
```

### Common Failure Modes
- **Type Mismatch Error:** Passing a single, interleaved `Array[Double]` to a geometry constructor will fail. The `LiteList` constructor requires two separate `Array[Short]` arguments for x and y coordinates.
- **Incorrect Receiver Type:** Calling `isCW` on composite geometries like `LiteLineString` or `LiteMultiList` is not the intended use. The method is designed for simple geometries representing a single list of points, like `LiteList`.

### Fix Code Hint
```scala
// WRONG: Using a single Array[Double]
val interleavedCoords: Array[Double] = Array(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0)
// val ring = new LiteLineString(interleavedCoords) // This will not compile

// CORRECT: Using two separate Array[Short] with the LiteList constructor
import edu.ucr.cs.bdlab.davinci.LiteList
val xs = Array[Short](0, 0, 1, 1, 0)
val ys = Array[Short](0, 1, 1, 0, 0)
val ring = new LiteList(xs, ys)
val isClockwise: Boolean = ring.isCW
```