## API Test: `area`
_Grounding: doc-repaired from source (docfix)._

### Goal
Compute the area of a `LiteList` geometry (or its subclasses like `LiteMultiPoint`) as a `Double` in Beast/RDPro geospatial workflows.

### Valid Call Patterns
Requires `edu.ucr.cs.bdlab.davinci.LiteList` (Scala class) and `edu.ucr.cs.bdlab.davinci.LiteMultiPoint` (Scala class).

```scala
import edu.ucr.cs.bdlab.davinci.LiteMultiPoint

val xs = Array[Short](0, 10, 10, 0, 0)
val ys = Array[Short](0, 0, 10, 10, 0)
val liteList = new LiteMultiPoint(xs, ys)
val areaValue: Double = liteList.area
```

### LLM Instruction Prompt
- Ensure the receiver is explicitly typed as `LiteList` or a subclass (e.g., `LiteMultiPoint`). Do NOT call `area` on a generic `LiteGeometry` reference.
- Ensure the geometry has at least 3 points (`numPoints >= 3`) before calling, otherwise it throws an `IllegalArgumentException`.
- Use instance-call form: `value.area` (no arguments).

### Prompt Snippet
```text
Given a `LiteList` or `LiteMultiPoint` instance `g` with at least 3 points, call `g.area` and store the result as Double. Do not call this on a generic `LiteGeometry`.
```

### Common Failure Modes
- **Type Error (Compilation Failure):** Calling `.area` on a `LiteGeometry` reference. The method does not exist on the base class; it is defined in `LiteList` and its subclasses.
- **Runtime Exception:** Calling `area` on a `LiteList` with fewer than 3 points throws an `IllegalArgumentException` (`require(numPoints >= 3)`).
- **Signature Error:** Calling `area()` with arguments or extra options.

### Fix Code Hint
```scala
// WRONG: Calling on base LiteGeometry (fails to compile)
val geom: edu.ucr.cs.bdlab.davinci.LiteGeometry = ...
val a = geom.area 

// CORRECT: Calling on LiteList or subclass (e.g., LiteMultiPoint)
val liteList: edu.ucr.cs.bdlab.davinci.LiteList = new edu.ucr.cs.bdlab.davinci.LiteMultiPoint(xs, ys)
val a: Double = liteList.area
```