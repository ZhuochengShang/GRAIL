## API Test: `numFields`

### Signature
```scala
def numFields: Int
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42_

_Source doc:_ Number of attributes in the file

### Goal
Return how many attributes (columns/fields) are present in the current record schema being read (for example, a GPX record in Beast I/O tests).

### Parameters
_None._

### Input
Call this on a record-like value that exposes `numFields` (authoritatively shown as `r.numFields` in tests while iterating a `GPXReader2`).  
From the provided sources, this is used with GPX input records; no additional arguments are required.

Preconditions from available facts:
- The receiver object must be a valid row/record instance from the reader iteration (e.g., `for (r <- gpxReader)`).
- This API has no type parameter and no file-path argument.

### Output
Returns `Int` — the number of attributes/fields in the record (schema width), e.g., `8` in the provided GPX test.

### Valid Call Patterns
```scala
assertResult(8)(r.numFields)
```

### LLM Instruction Prompt
- Call this as an instance member exactly in the form `r.numFields` (no parentheses needed).
- Do not add arguments; the method takes none.
- Use it on an existing record object from a Beast reader iteration (as in GPXReader2 tests).
- Treat the result as schema field count, not row count.

### Prompt Snippet
```text
Given a Beast record `r` from reader iteration, get its attribute count with `r.numFields` and compare it to the expected schema width.
```

### Common Failure Modes
- Calling `numFields` as a standalone function instead of on a record instance.
- Expecting it to return number of records in a file (it returns number of fields in one record/schema).
- Trying to pass parameters to `numFields` (it accepts none).

### Fix Code Hint
```scala
for (r <- gpxReader) {
  val n: Int = r.numFields
  // use n as the number of attributes in this record/schema
}
```