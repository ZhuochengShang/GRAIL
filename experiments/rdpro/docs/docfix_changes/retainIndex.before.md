## API Test: `retainIndex`

### Signature
```scala
def retainIndex(index: Int): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168_

_Source doc:_ Keep only the parameters that do not have an index or the ones with the given index. In other words, remove any indexed parameter that have a different index than the one given. The index of the parameter is a suffix between square brackets, e.g., param[1] @param index the index to retain @return a new options with the given index retained

### Goal
`retainIndex` filters the parameters in `BeastOptions` to keep only those that do not have an index or those that match the specified index, effectively allowing users to manage indexed parameters in their geospatial processing workflows.

### Parameters
- `index` (`Int`): The index to retain. This should be a non-negative integer that corresponds to the suffix of the parameters you want to keep (e.g., `1` to retain parameters like `key1[1]`).

### Input
The caller must provide a `BeastOptions` instance that may contain parameters with indexed suffixes (e.g., `key1[1]`, `key1[2]`). There are no specific file formats required for this operation, but the parameters should be set in the `BeastOptions` prior to calling `retainIndex`.

### Output
Returns `BeastOptions` — a new instance of `BeastOptions` that contains only the parameters that do not have an index or those that match the specified index. This allows for streamlined access to relevant parameters in subsequent processing steps.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("key1[1]", "val1")
  .set("key1[2]", "val2")
  .set("key3", "val3")
  .set("key4[2]", "val4")
val opts1 = opts.retainIndex(1) // Retains parameters with index 1
val opts2 = opts.retainIndex(2) // Retains parameters with index 2
```

### LLM Instruction Prompt
- When calling `retainIndex`, ensure that the `index` parameter is a valid integer that corresponds to the desired indexed parameters in the `BeastOptions`. The caller should have previously set parameters in the `BeastOptions` instance.

### Prompt Snippet
```text
To filter parameters in BeastOptions, use the retainIndex method with the desired index.
```

### Common Failure Modes
- Calling `retainIndex` on an empty `BeastOptions` instance will return an empty `BeastOptions`.
- Providing an index that does not match any existing indexed parameters will result in a `BeastOptions` that retains only the parameters without an index.

### Fix Code Hint
```scala
// Ensure that the BeastOptions instance has parameters set before calling retainIndex
val opts = new BeastOptions().set("key1[1]", "val1")
val filteredOpts = opts.retainIndex(1) // This will work as expected
```