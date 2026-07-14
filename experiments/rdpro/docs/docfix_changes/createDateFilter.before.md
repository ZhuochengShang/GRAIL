## API Test: `createDateFilter`

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
Create a Hadoop `PathFilter` that accepts only paths whose date string falls within an inclusive date range (`dateStart` to `dateEnd`) using the `yyyy.mm.dd` format.

### Parameters
- `dateStart` (`String`): Start date of the allowed range, inclusive, in `yyyy.mm.dd` format.
- `dateEnd` (`String`): End date of the allowed range, inclusive, in `yyyy.mm.dd` format.

### Input
Two date strings provided by the caller:
- Both are expected in the exact format `yyyy.mm.dd` per the source doc.
- The filter is intended to be used against `Path` values whose date component is represented in the same `yyyy.mm.dd` form (as shown in tests with paths like `"2001.02.15"`).

### Output
Returns `PathFilter` — a Hadoop path filter object that evaluates each `Path` and returns `true` for dates inside the inclusive range `[dateStart, dateEnd]`, and `false` otherwise.

### Valid Call Patterns
```scala
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
assert(dateFilter.accept(new Path("2001.02.15")))
assert(dateFilter.accept(new Path("2005.02.11")))
assert(dateFilter.accept(new Path("2003.07.15")))
assert(!dateFilter.accept(new Path("2005.02.12")))
assert(!dateFilter.accept(new Path("2001.01.31")))
```

### LLM Instruction Prompt
- Use the receiver exactly as validated in tests: `HDF4Reader.createDateFilter(start, end)`.
- Pass both arguments as `String` in `yyyy.mm.dd` format.
- Treat both bounds as inclusive.
- Apply the returned `PathFilter` to Hadoop `Path` objects.

### Prompt Snippet
```text
Create a date range filter with HDF4Reader.createDateFilter("YYYY.MM.DD", "YYYY.MM.DD"), then use filter.accept(new Path("YYYY.MM.DD")) to test whether a path date is within the inclusive range.
```

### Common Failure Modes
- Using a date format other than `yyyy.mm.dd`.
- Assuming the end date is exclusive (it is inclusive).
- Calling the method without the `HDF4Reader` qualifier shown in compiled tests.
- Applying the filter to paths that do not contain comparable date strings in the expected format.

### Fix Code Hint
```scala
import org.apache.hadoop.fs.Path

val start = "2001.02.15"
val end = "2005.02.11"
val dateFilter = HDF4Reader.createDateFilter(start, end)

// Inclusive bounds
val inRange = dateFilter.accept(new Path("2005.02.11"))  // true
val outOfRange = dateFilter.accept(new Path("2005.02.12")) // false
```