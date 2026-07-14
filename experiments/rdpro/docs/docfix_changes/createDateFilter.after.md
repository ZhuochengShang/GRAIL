## API Test: `createDateFilter`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create a Hadoop `PathFilter` that accepts only paths whose date string falls within an inclusive date range (`dateStart` to `dateEnd`) using the `yyyy.mm.dd` format.

### Valid Call Patterns
**Required Types & Imports:**
- requires `edu.ucr.cs.bdlab.raptor.HDF4Reader` — a Scala object (companion object).
- requires `org.apache.hadoop.fs.Path` — a Java class.
- requires `org.apache.hadoop.fs.PathFilter` — a Java interface.

```scala
import edu.ucr.cs.bdlab.raptor.HDF4Reader
import org.apache.hadoop.fs.Path

// Called statically on the companion object, NOT on an instance
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")

val checks = Seq(
  dateFilter.accept(new Path("2001.02.15")),
  dateFilter.accept(new Path("2005.02.11")),
  dateFilter.accept(new Path("2003.07.15")),
  !dateFilter.accept(new Path("2005.02.12")),
  !dateFilter.accept(new Path("2001.01.31"))
)

val passed = checks.count(identity)
require(passed == checks.size, s"createDateFilter correctness failed: passed=$passed total=${checks.size}")
```

### LLM Instruction Prompt
- `createDateFilter` is a method on the `HDF4Reader` companion object, not an instance method on the `HDF4Reader` class.
- It must be called statically as `HDF4Reader.createDateFilter(start, end)` without instantiating the reader.
- The returned filter is a Hadoop `org.apache.hadoop.fs.PathFilter` which evaluates `org.apache.hadoop.fs.Path` objects.
- Pass both arguments as `String` in `yyyy.mm.dd` format.
- Treat both bounds as inclusive.

### Prompt Snippet
```text
Call the companion object method HDF4Reader.createDateFilter("YYYY.MM.DD", "YYYY.MM.DD") without instantiating HDF4Reader. The returned org.apache.hadoop.fs.PathFilter evaluates org.apache.hadoop.fs.Path objects for inclusive date range matching.
```

### Common Failure Modes
- **Instantiating the reader:** Attempting to call `createDateFilter` as an instance method on a newly instantiated `HDF4Reader` class (e.g., `new HDF4Reader().createDateFilter(...)`). It is defined strictly on the companion object.
- Using a date format other than `yyyy.mm.dd`.
- Assuming the end date is exclusive (it is inclusive).
- Applying the filter to paths that do not contain comparable date strings in the expected format.

### Fix Code Hint
```scala
// WRONG: Instantiating the reader class
val reader = new edu.ucr.cs.bdlab.raptor.HDF4Reader()
val filter = reader.createDateFilter("2001.02.15", "2005.02.11")

// CORRECT: Calling statically on the companion object
import edu.ucr.cs.bdlab.raptor.HDF4Reader
import org.apache.hadoop.fs.Path

val filter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
val inRange = filter.accept(new Path("2005.02.11")) // true
```