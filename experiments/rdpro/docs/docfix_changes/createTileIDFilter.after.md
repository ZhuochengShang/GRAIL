## API Test: `createTileIDFilter`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create a Hadoop `PathFilter` that keeps only HDF tile files whose `hxxvyy` tile ID intersects a requested rectangle in Sinusoidal space.

### Valid Call Patterns
```scala
// REQUIRED IMPORTS & TYPES:
// requires `edu.ucr.cs.bdlab.raptor.HDF4Reader` — a Scala object; reference directly as HDF4Reader
// requires `java.awt.geom.Rectangle2D` — a Java class
// requires `org.apache.hadoop.fs.PathFilter` — a Java interface
// requires `org.apache.hadoop.fs.Path` — a Java class

import edu.ucr.cs.bdlab.raptor.HDF4Reader
import java.awt.geom.Rectangle2D
import org.apache.hadoop.fs.{Path, PathFilter}

// 1. Define extents in Sinusoidal space
val rect = new Rectangle2D.Double(
  Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale,
  Math.toRadians(29.0) * HDF4Reader.Scale,
  Math.toRadians(49.0) * HDF4Reader.Scale
)

// 2. Call statically on the HDF4Reader companion object
val tileIDFilter: PathFilter = HDF4Reader.createTileIDFilter(rect)

// 3. Test against a Hadoop Path
val isAccepted: Boolean = tileIDFilter.accept(new Path("tile-h03v03.hdf"))
```

### LLM Instruction Prompt
- Call `createTileIDFilter` statically on the `edu.ucr.cs.bdlab.raptor.HDF4Reader` companion object. Do NOT instantiate `HDF4Reader`.
- Pass exactly one argument of type `java.awt.geom.Rectangle2D`.
- Provide rectangle extents in Sinusoidal space, not lat/lon degrees unless already converted.
- Use the returned object as an `org.apache.hadoop.fs.PathFilter` and call `accept(new org.apache.hadoop.fs.Path(...))` on candidate files.
- Expect matching based on the filename's `hxxvyy` token.

### Prompt Snippet
```text
Create a Sinusoidal java.awt.geom.Rectangle2D, then call HDF4Reader.createTileIDFilter(rect) statically on the companion object. Use the returned org.apache.hadoop.fs.PathFilter to test org.apache.hadoop.fs.Path objects whose names contain an hxxvyy tile ID (e.g., tile-h03v03.hdf). Do not instantiate HDF4Reader.
```

### Common Failure Modes
- **Instantiating the Object (The failure that just happened):** Attempting to call `createTileIDFilter` as an instance method on a newly instantiated `HDF4Reader` object (e.g., `new HDF4Reader().createTileIDFilter(...)`). It is defined on the companion object and must be called statically.
- **Coordinate Space Error:** Passing a rectangle in the wrong coordinate space (e.g., unconverted geographic degrees) causes wrong tile selection.
- **Filename Format Error:** Using filenames that do not contain the expected `hxxvyy` pattern prevents intended matching.

### Fix Code Hint
```scala
// WRONG: Attempting to call as an instance method on an instantiated object
val reader = new edu.ucr.cs.bdlab.raptor.HDF4Reader()
val tileIDFilter = reader.createTileIDFilter(rect)

// CORRECT: Calling statically on the companion object
val tileIDFilter = edu.ucr.cs.bdlab.raptor.HDF4Reader.createTileIDFilter(rect)
```