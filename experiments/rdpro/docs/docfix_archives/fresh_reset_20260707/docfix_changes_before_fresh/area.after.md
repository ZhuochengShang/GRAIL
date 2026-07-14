## API Test: `area`
_Grounding: doc-repaired from source (docfix)._

### Goal
Compute planar area from coordinate arrays (`xs`, `ys`) using `LiteList.area`, returning a Scala `Double`.

### Valid Call Patterns|Valid Access Patterns
```scala
import edu.ucr.cs.bdlab.davinci.LiteMultiPoint
import edu.ucr.cs.bdlab.davinci.LiteList

val ring: LiteList =
  new LiteMultiPoint(Array[Short](0, 10, 10, 0), Array[Short](0, 0, 10, 10)) // numPoints = 4
val a: Double = ring.area
```

- `area` is an **instance method on `edu.ucr.cs.bdlab.davinci.LiteList`** (and subclasses), **not** on every `LiteGeometry`.
- Receiver precondition from source: `require(numPoints >= 3)`; calling `area` with fewer than 3 points throws at runtime.
- Return type is plain Scala `Double`.

### LLM Instruction Prompt
Use `value.area` only when `value` is typed as `LiteList` (or subtype such as `LiteMultiPoint`).  
Before calling, ensure `numPoints >= 3` to satisfy `require(numPoints >= 3)`.  
Treat the result as a normal `Double` (assign, compare, arithmetic); do not call fabricated members.

### Prompt Snippet
```text
Create or obtain a LiteList (e.g., LiteMultiPoint) with at least 3 points, then call `.area`.

Example:
import edu.ucr.cs.bdlab.davinci.{LiteList, LiteMultiPoint}
val g: LiteList = new LiteMultiPoint(Array[Short](0,10,10,0), Array[Short](0,0,10,10))
val areaValue: Double = g.area
```

### Common Failure Modes
- Calling `.area` on an arbitrary `LiteGeometry` reference: may not compile because `area` is defined on `LiteList`.
- Calling `.area` when `numPoints < 3`: throws due to `require(numPoints >= 3)`.
- Treating result as a special numeric wrapper (e.g., using nonexistent `isInfinite`/`isNaN` members on a non-Double wrapper).

### Fix Code Hint
```scala
// Wrong (receiver too generic; may not compile)
val g: edu.ucr.cs.bdlab.davinci.LiteGeometry = ???
val a = g.area

// Correct (receiver is LiteList/subclass with >=3 points)
import edu.ucr.cs.bdlab.davinci.{LiteList, LiteMultiPoint}
val ring: LiteList = new LiteMultiPoint(Array[Short](0,10,10,0), Array[Short](0,0,10,10))
val a: Double = ring.area
```