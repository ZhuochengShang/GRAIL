## API Test: `area`
_Grounding: doc-repaired from source (docfix)._

### Goal
Calculates the area of a simple polygon ring using the Shoelace formula. This is an instance method on the `LiteList` class, which represents a single sequence of vertices. The method requires the `LiteList` to contain at least three points.

### Valid Call Patterns|Valid Access Patterns
```scala
// Requires the class edu.ucr.cs.bdlab.davinci.LiteList

// Define the polygon ring vertices as arrays of Short.
// For a polygon, the ring should be closed (first point == last point).
val xs: Array[Short] = Array(0, 100, 100, 0, 0)
val ys: Array[Short] = Array(0, 0, 50, 50, 0)

// Construct a LiteList instance from the coordinate arrays.
val polygonRing = new edu.ucr.cs.bdlab.davinci.LiteList(xs, ys)

// Call the .area method on the LiteList instance.
val calculatedArea: Double = polygonRing.area
```

### LLM Instruction Prompt
Construct an `edu.ucr.cs.bdlab.davinci.LiteList` instance from two `Array[Short]` containing x and y coordinates for a closed polygon ring. Call the `.area` method on this `LiteList` instance to calculate its area.

### Prompt Snippet
```text
Given x and y coordinate arrays of type Short, create a new edu.ucr.cs.bdlab.davinci.LiteList and then compute its area.
```

### Common Failure Modes
Code fails to compile with an error like `value area is not a member of edu.ucr.cs.bdlab.davinci.LiteGeometry`. This occurs when attempting to call `.area` on an abstract geometry type or any class other than a concrete `LiteList` instance.

### Fix Code Hint
```scala
// WRONG: Calling .area on an abstract or incorrect geometry type.
// val someGeometry: LiteGeometry = ...
// val area = someGeometry.area // COMPILE ERROR

// CORRECT: Construct a LiteList first, then call .area on the instance.
val xs: Array[Short] = Array(0, 100, 100, 0, 0)
val ys: Array[Short] = Array(0, 0, 50, 50, 0)
val polygonRing = new edu.ucr.cs.bdlab.davinci.LiteList(xs, ys)
val calculatedArea: Double = polygonRing.area
```