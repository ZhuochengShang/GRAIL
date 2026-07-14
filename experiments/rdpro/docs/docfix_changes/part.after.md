## API Test: `part`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retrieve a specific geometry part (as a `LiteList`) by index from a `LiteMultiList` subclass (such as `LiteLineString` or `LitePolygon`).

### Valid Call Patterns
Requires the following Scala classes:
- `edu.ucr.cs.bdlab.davinci.LiteList`
- `edu.ucr.cs.bdlab.davinci.LiteLineString`
- `edu.ucr.cs.bdlab.davinci.LiteMultiList` (abstract base class)

```scala
import edu.ucr.cs.bdlab.davinci.{LiteList, LiteLineString}

// 1. Create coordinate arrays (length > 1)
val xs = Array[Short](0, 10)
val ys = Array[Short](0, 10)

// 2. Instantiate a LiteList
val list = new LiteList(xs, ys)

// 3. Wrap in an array and pass to a LiteMultiList subclass
val lineString = new LiteLineString(Array(list))

// 4. Retrieve the part by index
val p: LiteList = lineString.part(0)
```

### LLM Instruction Prompt
- `part` is a method on `LiteMultiList` and its subclasses (e.g., `LiteLineString`, `LitePolygon`), not on the base `LiteGeometry` class.
- Do not attempt to instantiate `LiteGeometry` directly from a JTS geometry using an `apply` method, as no such factory exists in the provided source.
- To test `part` standalone, instantiate a `LiteList` with `Array[Short]` coordinates (length > 1), wrap it in an array, and pass it to the constructor of a `LiteMultiList` subclass like `LiteLineString`.

### Prompt Snippet
```text
Instantiate a `LiteList` using `Array[Short]` for X and Y coordinates, wrap it in an Array, and pass it to a `LiteLineString`. Then call `.part(0)` on the `LiteLineString` to retrieve the part. Do not use the base `LiteGeometry` class.
```

### Common Failure Modes
- **Calling on base class:** Attempting to call `part` on a `LiteGeometry` reference. The method is only defined on `LiteMultiList` and its subclasses.
- **Inventing factories:** Attempting to create a geometry via `LiteGeometry(g)` (e.g., from a JTS geometry). The companion object lacks an `apply` method.
- **Empty or null parts:** Passing an empty array or an array containing `null` to a `LiteMultiList` subclass constructor (fails `require` checks).
- **Out-of-bounds index:** Passing an index to `part(i)` that is `>= numParts` or `< 0`.

### Fix Code Hint
```scala
// WRONG: Calling on base LiteGeometry or inventing a factory
val geom = LiteGeometry(jtsGeom) // Fails: no apply method
val p = geom.part(0) // Fails: part is not a member of LiteGeometry

// CORRECT: Instantiate a LiteMultiList subclass (e.g., LiteLineString) with LiteList parts
val xs = Array[Short](0, 10)
val ys = Array[Short](0, 10)
val list = new edu.ucr.cs.bdlab.davinci.LiteList(xs, ys)
val lineString = new edu.ucr.cs.bdlab.davinci.LiteLineString(Array(list))
val p = lineString.part(0)
```